---
title: "FlashRT-PAI: Fast Kernels Are Not Fast Pipelines for Physical AI Inference"
date: "2026-10-17"
authors: "Liang Su; David Chen; Jason Li; Kevin Guo; Teresa Lv"
url: https://arxiv.org/abs/2610.24349
pdf: https://arxiv.org/pdf/2610.24349
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.24349)** / [論文ページ](https://arxiv.org/abs/2610.24349)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **FLASHRT-PAI: FAST KERNELS ARE NOT FAST PIPELINES FOR PHYSICAL AI INFERENCE** 

Liang Su David Chen Jason Li Kevin Guo Teresa Lv 

AnyDevice AI & Alps Lab 

## **ABSTRACT** 

Vision-language-action (VLA), video-action (VA), and world action models (WAMs) form the backbone of modern physical AI systems, yet their real-time single-batch inference remains a defining bottleneck. Latency is dominated not by individual kernel computation, but by system-level overhead: thousands of short kernel launches, intermediate data movement across operator boundaries, and redundant recomputation across consecutive decisions. General-purpose graph compilers cannot address these costs, as they optimize individual calls in isolation and lack visibility into cross-call state semantics and global pipeline structure. 

We present FLASHRT-PAI, a low-latency inference engine built around **model-hardware pipeline co-design** rather than isolated kernel optimization. FLASHRT-PAI combines three core mechanisms: deep kernel fusion with launch overlap eliminates inter-operator boundaries and launch gaps; an execution contract formalizes the pipeline’s stage DAG, update rates, and named buffers to enable cross-decision state reuse and selective refresh; and execution-state capsules enable fast snapshot, restore, and fork of persistent pipeline state. The system also supports drop-in acceleration of unmodified PyTorch models via parity- and latency-gated kernel replacement. Evaluation covers six policies on RTX 5090 and four on Jetson AGX Thor. At matched 16-bit precision, FLASHRT-PAI is **1.3–3.7** _×_ **faster than official compiled paths** . Combining pipeline co-design with reduced precision delivers **3.38–12.66** _×_ **speedup over official eager implementations** . In LIBERO-10, four-bit _π_ 0 _._ 5 achieves 94.04% success on Thor and 93.32% on RTX 5090, compared with 92.4% for the measured official FP16 reference. FLASHRT-PAI is open source, distributed via Hugging Face Kernel Hub, and its opt-in _π_ 0 _._ 5 kernels have been adopted into the LeRobot framework. 

## **1 INTRODUCTION** 

Physical AI places learned policies in robot control loops: VLAs map images and instructions to actions (Physical Intelligence et al., 2025; NVIDIA et al., 2025), VAs generate video and actions autoregressively (Li et al., 2026a), and WAMs jointly denoise future video and actions (Black Forest Labs, 2026; NVIDIA et al., 2026; Bi et al., 2026). Each call returns an action chunk; its inference budget depends on the host’s observation and action-update schedule. We study this inference component on edge and workstation GPUs, with task-level checks in LIBERO simulation. 

Growing policies such as _π_ 0 _._ 7 and FLUX 3 Action have 5–7B parameters (Physical Intelligence et al., 2026; Black Forest Labs, 2026). On Thor, official _π_ 0 _._ 5 takes 222.64 ms eager and 129.17 ms compiled; FLUX 3 Action takes 1.35 s on RTX 5090 (Table 3). Reducing latency must also preserve action fidelity, since numerical drift can change robot behavior. 

Preliminary work. Under review by the Machine Learning and Systems (MLSys) Conference. Do not distribute. 

Closing this gap takes more than faster individual kernels. We present FLASHRT-PAI, an inference engine for lowlatency physical AI, guided by a simple principle: _fast kernels are necessary but not sufficient_ (Dehghani et al., 2021). For each model–hardware pipeline, FLASHRT-PAI decides what can be fused, overlapped, or reused across decisions; an execution contract makes those choices executable. Four limitations motivate these choices. 

First, **small kernels repeatedly materialize intermediates; deep kernel fusion removes selected boundaries** . At batch size one, separate normalization, residual, activation, and quantization kernels between general matrix multiplications (GEMMs) can write values that the next kernel immediately reads. TensorRT (NVIDIA, 2026g), torch.compile (Ansel et al., 2024), and TVM (Chen et al., 2018) already fuse common patterns, but some boundaries depend on deployment-specific facts, such as a validated quantization scale and the next GEMM’s input layout. FLASHRT-PAI uses these facts to hand-write the producer–consumer path, folding quantization into the producer where precision and hardware permit. In _π_ 0 _._ 5 on 

Thor, its FP8 decoder layer uses 12 kernels versus 20 for torch.compile+FP8 (§3.2). 

Second, **remaining kernel dependencies need not serialize all work; launch overlap hides part of their cost** . A successor can load weights before it needs its predecessor’s output, but an ordinary graph dependency waits for the predecessor to finish. At eligible boundaries, FLASHRTPAI marks where the successor may start and where it must wait, then applies CUDA’s Programmatic Dependent Launch (PDL) (NVIDIA, 2026b). PDL is CUDA’s mechanism; FLASHRT-PAI supplies the safe kernel points and pipeline order. On top of the already fused _π_ 0 _._ 5 NVFP4 path, it further shortens each decoder layer on Thor (§3.3). 

Third, **values needed by later decisions are often recomputed; frozen execution state keeps them valid and reusable** . In the official _π_ 0 _._ 5 implementation, stepdependent conditioning is rebuilt on every call; LingBot-VA similarly recomputes cross-attention keys and values derived from an unchanged instruction. CUDA Graph replay gives stable addresses but not the application’s rules for when such values become stale. FLASHRT-PAI names its fixed and persistent buffers, and records each one’s owner and refresh rule in the execution contract. It can replay captured stages without per-kernel host dispatch and reuse prompt- or step-dependent values across decisions. These named buffers also form an _execution-state capsule_ that can be copied to snapshot, restore, or fork a session (§3.4). 

Fourth, **optimized kernels are hard to adopt; checked replacements let an existing host use them selectively** . Fast TensorRT deployments for policies such as _π_ 0 _._ 5 and GR00T require model-specific integration (NVIDIA, 2026f;d), and an existing PyTorch host needs a way to check a replacement before using it. FLASHRT-PAI packages each replaceable region with a PyTorch reference and its kernels; the host keeps its own path unless the replacement matches the reference and lowers end-to-end latency (§5). FLASHRT-PAI kernels are distributed through the Hugging Face Kernel Hub, and LeRobot adopted an opt-in _π_ 0 _._ 5 kernel integration (LeRobot contributors, 2026). 

We evaluate FLASHRT-PAI on a Jetson AGX Thor for robotside inference and an RTX 5090 for workstation inference. Latency and numerical fidelity use fixed or recorded inputs offline; closed-loop task success is evaluated for _π_ 0 _._ 5 and LingBot-VA in LIBERO simulation. We compare official implementations, torch.compile, and available TensorRT deployments (§4), and report public adoption (§6). 

### **1.1 Contributions** 

This paper makes three contributions: 

- **An inference engine built around model–hardware** 

- **pipeline co-design.** We present FLASHRT-PAI, an inference engine that bridges policy models and production deployment through joint choices of GEMM tiling, precision, producer–consumer layouts, fusion, and launch overlap. Rather than stopping at isolated operator tuning, the design also accounts for stage boundaries, input-update cadence, and state reuse. Its kernels support checked integration into existing PyTorch hosts while retaining their control loop and fallback path (§3, §5). 

- **Three complementary mechanisms for small-batch inference.** Deep kernel fusion removes selected interoperator memory round-trips, and launch overlap reduces waiting at the boundaries that remain. The execution contract records stage dependencies, inputupdate methods, and named buffers for cross-decision reuse and selective refresh. Execution-state capsules snapshot, restore, and fork declared continuation state through device-local memory copies. In controlled _π_ 0 _._ 5/Thor runs, reuse reduces decision latency from 37.05 to 21.61 ms; restoring context and generating the next action takes 9.73 ms instead of 21.48 ms for rebuilding it. Reused and restored actions are bit-exact (§3.4, §4.4). 

- **Multi-policy evaluation and open-source impact.** Across six policies on RTX 5090 and four on Thor, evaluated paths are 3.38–12.66 _×_ faster than official eager implementations and 1.3–3.7 _×_ faster than official compiled paths at matched 16-bit precision. Paired LIBERO task checks cover _π_ 0 _._ 5 and LingBot-VA. FLASHRT-PAI is open source, with kernels distributed through the Hugging Face Kernel Hub, opt-in _π_ 0 _._ 5 integration adopted in LeRobot, and public developer and vendor acknowledgments (§4–§6). 

## **2 BACKGROUND AND MOTIVATION** 

### **2.1 Three Classes of Policy Calls** 

Figure 1 illustrates one decision cycle for each policy class. In _π_ 0 _._ 5 (Figure 1a), a 27-layer SigLIP encoder embeds each camera view, an 18-layer PaliGemma language model reads the image and prompt tokens (a prefix of about 500 to 800 tokens) and writes its key/value cache, and an 18-layer action expert attends to that cache while integrating ten flowmatching steps over a chunk of ten action tokens (Black et al., 2024; Physical Intelligence et al., 2025; Lipman et al., 2022). GR00T N1.7 has the same overall structure (NVIDIA et al., 2025). A VA generates video and actions autoregressively, one chunk at a time. In LingBot-VA (Figure 1b), a text encoder reads the instruction once per prompt, a VAE encodes the observed frames, and the backbone denoises the video and action tokens of the next chunk while attending to a key/value cache over earlier chunks; the cache 


_Figure 1._ One decision of (a) a VLA, (b) a VA, and (c) a WAM, with work grouped by how often it has to run. Results of the upper rows are kept in static buffers and state regions that the per-decision stage only reads; inputs and outputs pass through swap windows, buffers whose contents are replaced without touching the captured graphs. The rows are the same for all three kinds of policy; what differs is the cost of a denoising step and the state: the VA keeps a key/value cache over earlier chunks that grows across decisions. A monolithic graph replayed unchanged reruns the per-prompt row at every decision. Dashed outlines mark captured CUDA Graphs. FLASHRT-PAI records this structure in the execution contract (§3.4). 

persists from one decision to the next and grows up to a fixed window (Li et al., 2026a). A WAM also starts from a video generation model. In FLUX 3 Action (Figure 1c), a frozen Qwen3-VL-4B encodes the instruction, a frozen video VAE encodes the camera frames, and a 7B diffusion transformer denoises future frames together with a chunk of 32 actions (Black Forest Labs, 2026). Cosmos and Motus follow the same pattern with other backbones (NVIDIA et al., 2026; Bi et al., 2026). 

All the policy calls share three structural properties: 

1. Parts of the call change at different rates: the instruction once per task, the observation once per decision, and the denoising loop several times within each decision. 

2. A deployment fixes the number of views, contextlength bucket, action horizon, and denoising-step count. These constraints allow fixed-shape stages to be prepared once and replayed. 

3. Shapes vary widely within one call. The _π_ 0 _._ 5 action expert processes ten rows per step, whereas VA and WAM backbones process thousands of video and action tokens. These workloads need different GEMM tiling and fusion choices; a VA also carries history state across decisions. 

Fixed shapes make replay possible, but they do not by themselves determine the fastest execution path. For these policies, action shapes, the formats exchanged between adjacent kernels, and the lifetime of prepared values guide the design choices below. 

### **2.2 Kernel Boundaries and Cross-Decision Reuse** 

More capable models alone do not solve physical AI deployment. On both edge devices and workstation GPUs, policy calls remain small-batch and latency-sensitive. Three 

_Table 1._ Estimated time breakdown of one _π_ 0 _._ 5 decision with the official OpenPI eager implementation on Jetson AGX Thor. Kernels between GEMMs are the small kernels that normalize, add residuals, change layouts, or convert precision; gaps are the time when no kernel runs. Because profiling inflates the gaps, we estimate them as the unprofiled total latency minus the measured kernel time. 

||ms|%|
|---|---|---|
|Kernel execution|172.50|77.48|
|of which, kernels between GEMMs|70.10|31.49|
|Gaps between kernels (estimated)|50.14|22.52|
|Total|222.64|100|


costs recur at batch size one: intermediate traffic between kernels, waiting at the boundaries that remain, and recomputation of unchanged values across calls. Table 1 profiles intermediate-kernel costs in one complete _π_ 0 _._ 5 decision of the official OpenPI PyTorch eager implementation on Jetson AGX Thor; Figure 3 separately tests launch overlap. Within-call timing cannot show whether a value needed by the next decision was retained or recomputed. 

**Observation 1: materialized intermediates cost time and traffic.** The kernel trace records 70.10 ms in non-matrix kernels between GEMMs, about 31.49% of the unprofiled decision latency in this estimate. They normalize, add a residual, transform a layout, or convert precision. Each separate kernel must start and move its intermediate through memory. Folding eligible operations into neighboring kernels reduces launches and intermediate memory traffic. Figure 3 shows that the problem remains after compilation: with torch.compile and FP8, one action-expert layer still runs 20 kernels. Whether a boundary can be removed depends on the producer’s output and its consumer’s precision and layout (§3.2). 

**Observation 2: a remaining dependency need not serialize all work.** Estimated gaps account for 22.52% of an eager decision (Table 1), and fewer kernels leave fewer gaps 

(§3.2). Some boundaries must remain, however. At each of them, a plain dependency makes the next kernel wait for its predecessor to end before it starts any work, even setup or weight loading that does not need the predecessor’s output. The bottom pair in Figure 3 shows that such independent work can start early while the dependency is still respected (§3.3). 

**Observation 3: results needed later can be lost at a call boundary.** Figure 1 shows that an unchanged instruction can supply many decisions. Yet a call-scoped path may recompute the embeddings, tables, or K/V derived from it on every call, or recycle an intermediate buffer as soon as its last consumer in that call finishes. In the official _π_ 0 _._ 5 implementation, for example, the time conditioning of each denoising step depends only on the step index, yet it is recomputed at every step of every call. Keeping such values cuts a decision from 37.05 to 21.61 ms (§4.4). Discarding such values repeats work; retaining them without a refresh rule risks using stale data after the instruction or frame changes. The missing information is how long each value remains valid and who may overwrite it (§3.4). 

These opportunities require scale, shape, and layout for fusion; safe trigger and wait points for overlap; and update rates, validity rules, and owners for reuse (§3.2–§3.4). 

## **3 DESIGN OF FLASHRT-PAI** 

FLASHRT-PAI chooses stage boundaries, update rates, shapes, layouts, precision, and capture granularity together. Hand-written kernels implement fusion and launch overlap; an execution contract then records the completed stage DAG and buffer rules for replay and capsules. The FLASHRT-PAI engine owns the captured graphs and fixed-address buffers. A session manager uses the exported contract to select stage replays when the application reports changed inputs, and copies declared state for capsules. 

### **3.1 Architecture and Model Integration** 

Figure 2 maps a loaded checkpoint into stages with declared inputs, outputs, shapes, buffer roles, and update rates. Instruction-dependent work runs at prompt setup; vision, prefix, and action work run per decision. Setup selects kernels and precision, calibrates scales, checks fidelity, prepares slower-changing values, and chooses launch boundaries. It captures the full decision or split context/action stages, then exports the contract. 

At decision time, the robot loop fills swap windows with observations and noise; the session manager replays the selected captured stages over fixed-address buffers; and the host reads the action chunk. Declared state regions can be copied as capsules. Integration into an existing host is described in §5. 


_Figure 2._ Building and running a FLASHRT-PAI model–hardware pipeline. Setup constructs the pipeline from a checkpoint, chooses stage boundaries and precision, validates the model, and captures the selected stages. The execution contract records the stage DAG, named buffers, and export interface. At each control tick, the host fills swap windows and reads the action chunk while the session manager schedules replay over frozen execution state and can copy declared state for capsules. 

Across models, the reusable components are the buffer roles, contract and kernel interfaces, and qualification procedure. Stage decomposition, precision, layouts, and trigger/wait placement are designed and validated per model–hardware pipeline; the contract records those choices after design. 

### **3.2 Deep Kernel Fusion** 

FLASHRT-PAI fuses memory-bound work around computeheavy kernels: examples include residual addition with normalization and output quantization, RoPE with QKV split and cache write, and patch embedding with layout conversion. Compute-heavy GEMMs and attention keep their specialized implementations. We select a fused boundary when a supported fixed shape and layout let the producer emit the consumer’s required format, all consumers remain valid, and the complete path passes fidelity and latency checks. Other boundaries remain separate. 

**Let the action shape determine the GEMM tile.** The _π_ 0 _._ 5 action expert has ten activation rows, while the stock NVFP4 GEMM tile reserves space for 128. For selected decoder projections, FLASHRT-PAI swaps the operand roles so that the large tile dimension carries weights and the short dimension carries the ten action rows. The output store 


_Figure 3._ Kernel timelines for one _π_ 0 _._ 5 action-expert decoder layer on Jetson AGX Thor (10 action rows), drawn on one time axis. The upper rows compare the PyTorch FP8 baseline with FLASHRT-PAI’s FP8 and NVFP4 pipelines. Bars show measured CUPTI traces under CUDA Graph replay, and hatching marks kernel boundaries. The bottom pair holds the 11-kernel NVFP4 path fixed and enables programmatic dependent launch (PDL) at the FFN and adjacent O/QKV boundaries; green marks overlap. Separately, the PyTorch step recomputes 37 AdaRMS modulation projections in a 1.87 ms FP32-weight kernel; FLASHRT-PAI prepares them once per prompt. 

also matches the next kernel’s input layout, avoiding a separate transpose. The deployment shape therefore determines both the GEMM tile and the producer–consumer interface (Appendix A.3). 

**Choose fusion and the consumer’s layout together.** For an encoder FFN, FLASHRT-PAI packs gate/up weights together so the GEMM can apply the gated activation and produce packed four-bit values directly. The first fused version wrote a full-width result and doubled the next GEMM’s weight traffic, making the feed-forward chain slower. A compact, half-width output preserved the consumer’s original shape and made the chain faster. It also quantized the intermediate once rather than twice. The useful optimization is the complete producer–consumer path: fewer launches help only when the output format also suits the next kernel. Appendix A.3 gives the layout details. 

Figure 3 traces a complete _π_ 0 _._ 5 action-expert decoder layer on Jetson AGX Thor. At FP8 GEMM precision, FLASHRTPAI reduces the layer from 20 kernels in the PyTorch torch.compile path to 12. It fuses the small operations around the FFN’s two GEMMs: residual addition, normalization, and input quantization share one kernel, while GeGLU and output quantization share another (§4.3). The NVFP4 path also folds GeGLU into a GEMM epilogue, leaving 11 kernels per layer. 

At the fused quantization boundaries in Figure 3, the producer emits the GEMM input and its scale without a separate activation read/write pass. This requires a supported precision, shape, and layout; _π_ 0 _._ 5 still has an attention-output path with separate quantization. Selected low-bit paths use 

activation-aware weight scaling (Lin et al., 2024). Scales are calibrated before capture, cached by checkpoint and sequence length, and checked against model-level fidelity results (§4.5). 

### **3.3 Launch Overlap** 

Fusion leaves some producer–consumer boundaries intact. Overlap requires input-independent successor work, a safe wait before dependent reads, and a measured gain despite resource contention. At eligible pairs, FLASHRT-PAI uses CUDA’s programmatic dependent launch (PDL) to start a successor GEMM’s weight loading before its activation is ready, then waits before reading that activation. The pipeline selects the pair, and the kernels mark safe trigger and wait points that an ordinary graph dependency does not expose (NVIDIA, 2026b). PDL permits overlapping execution but does not guarantee it; the successor still waits before it reads the predecessor’s output. In the bottom two rows of Figure 3, enabling PDL at the FFN and adjacent O/QKV boundaries shortens the already fused 11-kernel NVFP4 layer from 62.1 to 52.1 _µ_ s with the same kernels and precision. CUDA supplies PDL; our design chooses and validates the model-specific trigger and wait points. Appendix A.4 gives three cases, including boundaries where more overlap does not help. 

### **3.4 Execution Interface and Reusable State** 

The execution contract exposes a completed pipeline through a shared execution interface. Reuse is valid only while the inputs that produced a retained value are un- 

changed. The interface records stage order, supported shapes, and named buffers with owners, sizes, and update methods. The engine checks stage references and selects a captured replay for the requested shape. Appendix A.1 gives the execution rules, interface fields, and a worked _π_ 0 _._ 5 plan. _Static_ buffers hold prepared values; _swap windows_ hold replaceable inputs and outputs at fixed addresses; _state regions_ retain mutable state between stages or decisions. The engine allocates these buffers once and captures selected stages as CUDA Graphs keyed by shape. 

The interface records stage order, input-update methods, and the buffer regions needed for continuation. In _π_ 0 _._ 5, instruction embeddings can be reused while the instruction is unchanged, whereas a new observation requires rebuilding image-conditioned K/V. If another session overwrites the working buffers, restoring the saved regions lets the original session continue without rebuilding its completed context. 

**Within a decision.** Figure 4 (a) shows the split _π_ 0 _._ 5 plan. The host fills image and noise buffers; context encodes the image and prompt into K/V; action reads that K/V throughout its denoising steps and transforms the noise buffer into the action chunk. Shared named buffers let successive captured stages consume results directly. The session manager orders stage replays according to the contract; captured stages use fixed addresses without replay-time allocation or host-dependent choices. The full-call plan and the split plan return identical actions for identical inputs and noise. 

**Across decisions.** Figure 4 (b) carries prepared values into the next call. The normal _π_ 0 _._ 5 inference path uploads the supplied images and reruns vision and context on every call; it reuses unchanged instruction embeddings and fixed step-conditioning tables. Even the encoder’s text-token K/V depends on the image and is rebuilt. Prompt and robot-state updates enter through the model’s supported input methods. A host driving context and action separately must refresh context for the current inputs before generating the next action. 

At a stage boundary, snapshot copies declared restorable regions into an _execution-state capsule_ ; restore copies them back, and fork copies them into another session. The export lists region names, offsets, and lengths; loading checks the schema and plan fingerprint, and resumption must respect the model’s chunk boundaries. For _π_ 0 _._ 5, the capsule holds the context K/V, the prompt embedding, and the decoder position table (14 MB). For LingBot-VA, it also holds the history K/V, the VAE cache, and the randomnumber state (1.4 GB). After another session overwrites the working buffers, restoring the capsule reproduces the next actions bit for bit, without recapture and without rebuilding the history (§4.4). Capsules remain process-local and plan-specific because captured graphs contain device addresses; they support compatible sessions within a process. 


_Figure 4._ Fixed-buffer reuse in _π_ 0 _._ 5. (a) Circled numbers link stages to their buffer accesses; yellow K/V is shared by the denoising steps within a call. (b) The next call processes a fresh image and rebuilds K/V, while reusing the unchanged instruction’s embeddings and fixed step-conditioning tables. The connector carries these prepared values across the call boundary. 

Integration defines the complete continuation state and valid resumption points; the session manager copies the declared regions. 

## **4 EVALUATION** 

### **4.1 Setup** 

**GPUs.** We evaluate a Jetson AGX Thor (SM110, 128 GB unified memory, MAXN mode) for robot-side inference and an RTX 5090 (SM120, 32 GB, fixed clocks) for workstation inference. Both are Blackwell GPUs supporting FP8 and NVFP4. 

**Policies.** Table 2 lists six policies: two VLAs, one VA, and three WAMs. All six run on RTX 5090; Thor covers _π_ 0 _._ 5, GR00T N1.7, LingBot-VA, and Cosmos3-Edge-Policy. Checkpoints and official code revisions are listed in the supplementary material. 

**Baselines.** All baselines are official open-source implementations: OpenPI on Thor and the existing LeRobot reference on RTX 5090 for _π_ 0 _._ 5, Isaac-GR00T for GR00T N1.7, and the official releases of LingBot-VA, FLUX 3 Action, Cosmos, and Motus (Physical Intelligence, 2025; Hugging Face, 2024; NVIDIA, 2025; Li et al., 2026a; Black Forest Labs, 2026; NVIDIA et al., 2026; Bi et al., 2026), each run eagerly 

_Table 2._ Policies evaluated. Steps: denoising steps per decision (video/action for LingBot-VA); actions: actions returned per decision; views: cameras (Thor/RTX 5090 for GR00T N1.7). 

|Class|Model|Params|Steps|Actions|Views|
|---|---|---|---|---|---|
|VLA|_π_0_._5|3.35B|10|10|2|
||GR00T N1.7|3B|4|16|1/2|
|VA|LingBot-VA|5.3B|20/50|16|2|
|WAM|FLUX 3 Action|7B|4+CFG|32|3|
||Cosmos3-Edge-Policy|4B|4|32|3|
||Motus|_∼_8B|10|16|3|


and with its compiled or CUDA Graph path where one runs. Official TensorRT deployments exist for _π_ 0 _._ 5 and GR00T N1.7 on Thor (NVIDIA, 2026f;e). Corresponding baseline paths were also tested locally under aligned task protocols; published reference values retain their source markers in Table 3. 

**Protocol.** Experiments run offline on fixed or recorded inputs, excluding physical action execution, network transfer, loading, calibration, and capture. These measurements characterize warmed-up inference; control-loop timing depends on the application’s replanning schedule. Comparisons use matching timing boundaries within each model– hardware pipeline; host-specific intervals are described in Appendix A.2. Paired mechanism experiments use identical preprocessed inputs and pinned noise. Warm-up reaches up to 300 calls on Thor to avoid a lower clock state. Table 3 marks published reference values; other latencies are measured locally. Compiled paths follow the available official implementations. Fidelity uses matched noise and the references specified in Table 7. No result uses approximate denoising-step caching such as TeaCache (Liu et al., 2024). Appendix A.2 reports the verified sampling and timing details for the controlled experiments. 

### **4.2 Deployment latency** 

Table 3 compares FLASHRT-PAI with the official eager, compiled, and TensorRT paths, with published deployment references marked separately. For _π_ 0 _._ 5, FLASHRT-PAI is 10.95 _×_ faster than official eager on Thor and 12.66 _×_ faster on RTX 5090. GR00T N1.7 is 5.36 _×_ faster on RTX 5090; its 24.39 ms Thor result compares with the published eager reference of approximately 126 ms (about 5.2 _×_ ). For LingBot-VA on Thor, a chunk takes 0.92 s instead of 9.31 s (10.11 _×_ ), and on the RTX 5090 it is 5.72 _×_ faster. Among the WAMs, FLUX 3 Action and Motus are 4.91 _×_ and 7.10 _×_ faster on the RTX 5090, and Cosmos3-Edge-Policy is 3.38 _×_ faster on Thor and 4.84 _×_ faster on the RTX 5090. LingBotVA/RTX 5090 uses FP8 video-step and INT4 weight-only action-step GEMMs, with the same mixed-precision configuration in the latency and fidelity tables. Appendix A.2 specifies the operator precisions. In the Compile column, the official torch.compile paths are 3.3% slower than ea- 

ger for Cosmos/Thor and 2.2% slower for LingBot-VA/RTX 5090. LingBot-VA uses the official default compiler settings, which leave parts of the pipeline in eager execution. 

Published Thor TensorRT deployments report approximately 49 ms for _π_ 0 _._ 5 and 39.9 ms for GR00T N1.7, compared with FLASHRT-PAI’s locally measured 20.33 and 24.39 ms, respectively. For _π_ 0 _._ 5/Thor, the deployment run has a 20.54 ms p95 over 1000 timed calls after 200 warmups, versus a 20.33 ms median. 

### **4.3 Deep fusion and launch overlap** 

Observations 1 and 2 (§2.2) identify intermediate-kernel costs and independent work across dependent kernels. Deep kernel fusion removes boundaries; launch overlap may hide part of the cost at the boundaries that remain. Table 4 reports latency at each precision tier, Table 5 counts kernels per decision, and Figure 3 gives a measured layer trace and an isolated PDL off/on comparison. 

**Precision tiers.** Table 4 compares the official compiled path with FLASHRT-PAI at 16, 8, and 4 bits. Already at 16 bits, without lower precision, FLASHRT-PAI is 1.3–3.7 _×_ faster than the official compiled path. This deployment comparison combines specialized kernels, fusion, graph replay, and value reuse (§4.4). The table compares pipeline configurations at each precision; the 4-bit entries match Table 3. Precision, layout, fusion, and launch scheduling are co-designed: changing one can require conversions or a different kernel schedule. We therefore interpret these rows as complete configurations, rather than independent gains to add. The paired PDL and reuse experiments hold the accompanying implementation fixed to measure those changes within a valid pipeline. 

**Fusion.** Table 5 counts the GPU kernels in one decision. The complete FLASHRT-PAI pipelines run 59–93% fewer kernels than official eager paths; the reduction includes fusion and removal of repeated work. In the layer trace of Figure 3, the torch.compile+FP8 path takes 193.2 _µ_ s per layer (20 kernels), while the FLASHRT-PAI FP8 path takes 105.2 _µ_ s (12 kernels). Both use FP8 GEMMs; the FLASHRT-PAI layer combines fewer intermediate boundaries with specialized GEMM implementations. This comparison measures the co-designed layer. The NVFP4 path takes 62.1 _µ_ s with 11 kernels, combining its precision choice with a fused GeGLU epilogue. 

**Launch overlap.** The bottom two rows of Figure 3 isolate PDL on Thor: the same NVFP4 path replays the same 11 kernels with PDL off and then on at the FFN and adjacent O/QKV boundaries. The layer period falls from 62.1 to 52.1 _µ_ s, and the FFN window within it falls from 33.92 to 27.30 _µ_ s. In an unprofiled measurement of the whole decoder, enabling PDL at these boundaries lowers the me- 

_Table 3._ Reported deployment latency (ms). Speedup is eager/FLASHRT-PAI for each model and GPU, combining pipeline and precision changes. _†_ marks published values and ratios computed from them; other latencies are measured locally. –: no result. Timing intervals: Appendix A.2. 

||||J|etson AG|X Thor||||RTX 5|090||
|---|---|---|---|---|---|---|---|---|---|---|---|
|Class|Model|Eager|Compile|TRT|FLASHRT-PAI|Speedup|Eager|Compile|TRT|FLASHRT-PAI|Speedup|
|VLA|_π_0_._5<br>GR00T N1.7|222.64<br>_∼_126<sup>_†_</sup>|129.17<br>_∼_105<sup>_†_</sup>|_∼_49<sup>_†_</sup><br>39_._9<sup>_†_</sup>|20.33<br>24.39|10.95<br>_∼_5_._2<sup>_†_</sup>|104.21<br>41.10|58.26<br>32.01|–<br>–|8.23<br>7.67|12.66<br>5.36|
|VA|LingBot-VA|9309.53|6721.44|–|920.9|10.11|2608.53|2666.62|–|455.70|5.72|
|WAM|FLUX 3 Action|–|–|–|–|–|1353.57|1148.95|–|275.51|4.91|
||Cosmos3-Edge-Policy|1223.00|1263.49|–|362.15|3.38|586.28|514.93|–|121.25|4.84|
||Motus|–|–|–|–|–|1186.10|1403.15|–|167.08|7.10|


Host timing intervals, mixed-precision settings, and sampling are detailed in Appendix A.2. 

_Table 4._ Latency (ms) across pipeline configurations at 16, 8, and 4 bits. The 16-bit comparison matches FP16/BF16 precision; lower tiers change precision and kernels. Baseline sources follow Table 3. 

||_π_0|_._5|GR00T|N1.7|LingB|ot-VA|FLUX 3 Action|
|---|---|---|---|---|---|---|---|
|Configuration|Thor|5090|Thor|5090|Thor|5090|5090|
|Official compile, 16-bit|129.17|58.26|_∼_105|32.01|6721.44|2666.62|1148.95|
|FLASHRT-PAI 16-bit|67.47|25.08|54.77|18.85|3174.26|726.10|900.34|
|FLASHRT-PAI 8-bit|40.71|13.85|36.98|12.91|2029.42|532.69|423.92|
|FLASHRT-PAI 4-bit|20.33|8.23|24.39|7.67|920.9|455.70|275.51|
|16-bit vs. 16-bit compile|1.91_×_|2.32_×_|_∼_1.9_×_|1.70_×_|2.12_×_|3.67_×_|1.28_×_|
|4-bit vs. 16-bit compile|6.35_×_|7.08_×_|_∼_4.3_×_|4.17_×_|7.30_×_|5.85_×_|4.17_×_|


_Table 5._ GPU kernels per decision of the official eager implementation and FLASHRT-PAI, counting every kernel inside CUDA Graphs. 

|Policy|GPU|Eager|FLASHRT-PAI|Reduction|
|---|---|---|---|---|
|_π_0_._5|Thor|13,414|2,610|81%|
||RTX 5090|13,134|2,216|83%|
|GR00T N1.7|Thor|5,190|2,148|59%|
||RTX 5090|4,978|1,579|68%|
|LingBot-VA|Thor|180,245|27,089|85%|
||RTX 5090|220,504|35,557|84%|
|FLUX 3 Action|RTX 5090|18,759|1,268|93%|


dian from 10.124 to 9.207 ms, and enabling it at all decoder boundaries lowers it to 9.009 ms. With PDL at all decoder boundaries, the full call falls from 21.960 to 21.044 ms. All paths run the same kernels at the same precision, a 4.2% whole-call gain in the paired PDL experiment (Appendix A.2). On the RTX 5090, PDL shortens one FFN block of the action expert from 14.56 to 12.09 _µ_ s. The whole-call gain is smaller because launch overlap changes only eligible action-expert boundaries; it does not shorten the other stages or host work. 

#### **Takeaway: Fast kernels can still form a slow pipeline.** 

Separate kernels still move intermediate data and wait for dependencies. Fusion removes selected boundaries; launch overlap reduces waiting at those that remain. 

### **4.4 Frozen execution state** 

Observation 3 (§2.2) showed that values needed by later decisions are often recomputed. Frozen execution state 

_Table 6._ Benefits of frozen execution state (ms): reusing values across decisions and resuming a session after another session overwrites its buffers, with the cost of capsule copies. Restored and reused actions match the reference bit for bit. Paired experiment <u>protocol:</u> Appendix A.2. 

|Use|Policy/GPU|Baseline|Frozen state|Speedup||
|---|---|---|---|---|---|
|Reuse values|_π_0_._5/Thor|37.05|21.61|1.71_×_||
|Resume after overwrite|_π_0_._5/Thor|21.48|9.73|2.21_×_||
|Resume after overwrite|LingBot-VA/Thor|1809.32|925.27|1.96_×_||
|_Capsule copy cost_||MB|Snapshot|Restore|Fork|
|_π_0_._5|Thor|14.40|0.48|0.13|0.50|
|LingBot-VA|Thor|1410.65|18.77|11.29|36.03|


makes these values explicit: the execution contract names their buffers, owners, and refresh rules. This lets FLASHRTPAI retain unchanged values and copy declared state regions into an execution-state capsule at a stage boundary. Table 6 summarizes these two uses. 

**Reuse across decisions.** We run _π_ 0 _._ 5 on Thor with the deployed NVFP4 engine over eight recorded observations of one task. Both paths replay the same captured graphs; the baseline also recomputes the prompt embedding and the time conditioning of every denoising step into the same buffers. Keeping these values reduces the mean decision latency from 37.05 to 21.61 ms, and the actions stay bit for bit the same. The baseline uses the existing preparation code rather than a separately optimized implementation. 

**Restore after an interruption.** Persistent values can remain in place while one session runs uninterrupted. When 


_Figure 5._ LingBot-VA on Thor: time until the history state is ready again after another session overwrites it (log scale, median of 10 runs). Generating the next chunk (0.78–0.92 s) is not included. Restore uses the same state-ready interval as Table 6: 11.29 ms at 16 chunks. 

sessions share captured graphs and fixed working buffers, however, another session may overwrite them. At a stage boundary, snapshot copies the declared state regions into an execution-state capsule; restore copies them back before replay resumes. If each session permanently retains its own working buffers, no restore is needed. Capsules serve suspended sessions or rollout branches that share one working set: a saved branch retains declared state without duplicating the entire workspace. Table 6 reports the state footprint and snapshot, restore, and fork times. 

For _π_ 0 _._ 5, we interrupt a session after its context stage, run another session over the shared buffers, and then resume the original session. Rebuilding its instruction- and imageconditioned state and generating the action takes 21.48 ms. Restoring its 14.40 MB capsule and generating the same action takes 9.73 ms. The saved context computation was completed before the interruption; a fresh image would still require a new context stage. 

LingBot-VA carries history across action chunks. After another session overwrites its working buffers, our rebuild baseline re-encodes the saved observations and actions to reconstruct the historical K/V, while skipping the earlier denoising computations. At 16 committed chunks, this reconstruction takes 894.71 ms, whereas restoring the capsule takes 11.29 ms. Both paths must then generate the next action chunk. Including that work, time to the next action is 1809.32 ms after reconstruction and 925.27 ms after restoration, a 1.96 _×_ speedup. Forking the LingBot-VA state into a new session takes 36.03 ms. Figure 5 shows that K/V reconstruction grows from 79.88 ms after one chunk to 894.71 ms after 16, while restoration remains about 11.2 ms because the current implementation copies a fixed allocated state region. Rerunning all past chunks is more expensive still, reaching 14.4 s at 16 chunks. 

_Table 7._ Action agreement: global / worst-sample cosine under matched noise. _n_ marks per-input scores; Motus gives the range over four inputs.<sup>_c_</sup> : six arm channels, 717 chunks, official FP32 reference; full actions: Appendix A.2.1.<sup>_d_</sup> : FP16 frontend reference. Bottom: LIBERO-10 success (100 matched episodes for LingBot-VA). Protocols: Appendix A.2. 

|Class|Model|Thor|RTX 5090|
|---|---|---|---|
|VLA|_π_0_._5|.999713 / .999360|.999850 / .999201<sup>_d_</sup><br>|
||GR00T N1.7|.9997 (_n_=1)|.99999<sup>_d_ </sup>(_n_=1)|
|VA|LingBot-VA, BF16|.999949 / .999920|.999502 / .952046<sup>_c_</sup>|
||LingBot-VA, 4-bit mix|.995361 / .993777|.998907 / .941478<sup>_c_</sup>|
|WAM|FLUX 3 Action|–|.999850 / .998939|
||Cosmos3-Edge-Policy|.998533 / .976768|.998138 / .988953|
||Motus (_n_=4)|–|.99991–.99994|
|LIBER|O-10 success (%)|Thor|RTX 5090|
|_π_0_._5, i|official FP16|92|.4|
|_π_0_._5,|FLASHRT-PAI 4-bit|94.04|93.32|
|LingB i|ot-VA, official BF16|–|98.0|
|LingB|ot-VA, FP8/INT4|–|97.0|


**Takeaway: Useful state can outlive an inference call.** Prepared values remain reusable until their inputs change. After an interruption, restoring saved state can avoid rebuilding completed context. 

### **4.5 Fidelity and task success** 

Table 7 reports matched-input, matched-noise action agreement against the official implementation, except for the FP16-frontend references marked<sup>_d_</sup> . LingBot-VA/RTX 5090 is evaluated on held-out traces without sample filtering. Its six arm channels are reported here; full-action scores including the gripper appear in Appendix A.2.1. On LIBERO-10, _π_ 0 _._ 5 on FLASHRT-PAI with 4-bit precision succeeds in 94.04% of trials on Thor and 93.32% on RTX 5090<sup>1</sup> , compared with 92.4% for the measured official FP16 reference. LingBot-VA’s evaluated FP8/INT4 path succeeds in 97/100 episodes on RTX 5090, versus 98/100 for official BF16, using matched seeds and initial states across ten LIBERO-10 tasks. 

## **5 DEPLOYMENT** 

FLASHRT-PAI offers native C++, a Python frontend, and selective PyTorch-host replacement. All use its kernels; captured-stage exports share the execution contract (§3.4). Pipeline ownership determines the optimization scope. 

**Native engine and frontend.** The native engine owns the pipeline, fixed buffers, and captured graphs. The host fills swap windows and reports changed inputs; the session manager schedules replay and capsule copies. C++ avoids perkernel host dispatch. The Python frontend uses the same kernels and stages for integration and evaluation, with Python orchestration, input preparation, and output conversion. 

1The RTX 5090 result aggregates 4,666 successes over 5,000 trials using ten seeds. 

_Table 8._ Public uses of FLASHRT-PAI as of October 2026. Links beside project names open the corresponding <u>public sources.</u> 

|Project|How it uses FLASHRT-PAI|
|---|---|
|MindOn Mind-1[link]|Inference backend for a robot model|
|EagleVLA-Edge[link]|Edge VLA engine that plugs into FLASHRT-PAI|
|LeRobot[link]|Optional FP8 kernels for_π_0_._5|
|FineART-VLA[link]|Optional kernels for training and inference|
|Jetson AI Lab[link]|TensorRT guide for_π_0_._5, inspired by FLASHRT-PAI|
|APXInf[link]|Edge inference engine that credits FLASHRT-PAI|


**Existing PyTorch hosts.** Each replaceable region has a specification and PyTorch reference. Qualification checks inputs, outputs, state, shapes, and loop count; tensordependent host branches prevent capture. After host-side calibration, activation requires reference agreement and lower whole-call latency, otherwise retaining the original path. Kernels ship through the Kernel Hub. Graph-safe stages can use capture(fn, windows) and export replay and capsule interfaces. The host retains its control loop; local edits may remove synchronization or enable capture. Host module boundaries limit fusion, and preprocessing, postprocessing, and tensor creation remain outside capture. 

**Integration work.** Engineers specify stage boundaries, buffer lifetimes, precision/layout interfaces, and kernel variants, then validate the complete policy. Loading, calibration, and graph capture execute the specified setup; they do not automatically discover this design. Shared kernels and contract interfaces reduce repeated implementation, but a new model–hardware pipeline still requires model-specific design and validation. 

#### **Takeaway: Integration can erase kernel speedups.** 

Extra conversion and synchronization can offset a faster kernel. Evaluate replacements within the complete application path, preserving output agreement and the existing control loop. 

## **6 ECOSYSTEM ADOPTION AND IMPACT** 

FLASHRT-PAI is an open-source inference engine (https: //github.com/flashrt-project/FlashRT), with kernels on the Hugging Face Kernel Hub. The October 2026 repository snapshot records 658 GitHub stars and 89 forks, alongside the public integrations in Table 8. Its public uses span robot-model developers, host frameworks, and vendor deployment guides. Beyond NVIDIA GPUs, it supports AMD Instinct and Ascend; an external team extended the AMD backend from MI350X to MI300X. Table 8 lists uses documented publicly as of October 2026; latency figures are reported by the adopters under their respective setups. 

MindOn reports 82 to 32 ms mean latency for Mind-1 using FLASHRT-PAI (MindOn, 2026). LeRobot’s separate PR setup reports 89.4 to 46.7 ms for opt-in _π_ 0 _._ 5 on RTX 5090: a bit-exact denoising loop reaches 79.3 ms, followed by 

FP8 feed-forward kernels from the Kernel Hub (LeRobot contributors, 2026; Hugging Face, 2026). The option is disabled by default with BF16 fallback. Jetson AI Lab credits FLASHRT-PAI’s Thor results as motivation for its _π_ 0 _._ 5 TensorRT deployment (NVIDIA, 2026f), used as our published baseline. 

## **7 RELATED WORK** 

**Graph compilers.** TVM, TensorRT, and torch.compile provide fusion, layouts, autotuning, and CUDA Graph replay (Chen et al., 2018; NVIDIA, 2026g; Ansel et al., 2024; NVIDIA, 2024). FLASHRT-PAI supplies model–hardware precision/layout interfaces and explicit cross-decision state rules, then records the resulting pipeline in a contract. It complements compiler optimization with the input lifetimes and state-update rules of a deployed policy; compilergenerated regions can use the same interface. 

**Serving systems and reuse.** PagedAttention, SGLang, Prompt Cache, and Hydragen share or reuse text-prefix attention state (Kwon et al., 2023; Zheng et al., 2024; Gim et al., 2024; Juravsky et al., 2024). Marconi manages hybrid KV/recurrent prefix reuse; HCache accelerates contextual KV restoration (Pan et al., 2025; Gao et al., 2025). FLASHRT-PAI applies reuse to instruction, stepconditioning, K/V, VAE, and RNG regions with different update rates in a robot loop, under explicit ownership and valid resumption boundaries. 

**Kernels and LLM runtimes.** CUTLASS and FlashAttention supply GEMM and attention kernels (NVIDIA, 2026c; Dao, 2024); FlashInfer adds customizable, graphcompatible attention (Ye et al., 2025), Marlin optimizes FP16 _×_ INT4 GEMM (Frantar et al., 2024), and TensorRTLLM integrates optimized kernels and LLM request scheduling (NVIDIA, 2026h). FLASHRT-PAI adds policy-stage update rules and compatible resumption boundaries for instruction, observation, step, and history state; these libraries can implement its stages. 

**VLA inference systems.** Ma et al. (2025b) reduce inference overheads for 30 Hz _π_ 0-class execution. BLURR combines prefix caching, mixed precision, and single-step rollout (Ma et al., 2025a). EagleVLA combines a llama.cpp engine with foresight-aligned asynchronous inference on Orin (Yang et al., 2026); its engine is a FLASHRT-PAI provider (PKU SEC Lab, 2026). Reflex adds batched visual encoding and graph replay (Chen et al., 2026); FlashDrive co-designs a driving VLA’s algorithm and system (Li et al., 2026b). Some change model computation; FLASHRT-PAI preserves architecture and denoising schedule across VLA, VA, and WAM pipelines. Public integrations with EagleVLA-Edge and acknowledgments from APXInf are listed as adoption evidence in Table 8. 

**Vendor deployments.** NVIDIA supplies _π_ 0 _._ 5 and GR00T TensorRT paths (NVIDIA, 2026f;d), and reports Cosmos3Edge-Policy at 15 Hz on Thor with 32 actions per inference (NVIDIA, 2026a). DreamZero combines two-GPU parallelism, compilation, kernels, quantization, and caching (Ye et al., 2026). These deployments and FLASHRT-PAI all require model-specific integration; FLASHRT-PAI shares contract and kernel interfaces. 

**Model-side acceleration and scheduling.** Token pruning (Yang et al., 2025), approximate feature caching (Xu et al., 2025; Liu et al., 2024), and fewer-step distillation (Prasad et al., 2024; Akbari et al., 2026) reduce policy computation, whereas FLASHRT-PAI’s state reuse avoids recomputing values whose inputs are unchanged. Real-time chunking (Black et al., 2025) overlaps inference with action execution and is complementary to reducing the inference latency itself. 

## **8 LIMITATIONS AND CONCLUSION** 

**Limitations.** FLASHRT-PAI targets small-batch, fixedshape inference; new shapes need recapture, and new native integrations require model–hardware pipeline co-design, tuning, calibration, and validation (Appendix A). The current evaluation focuses on warmed-up inference on two Blackwell GPUs, with four policies on Thor, six on RTX 5090, and task success for _π_ 0 _._ 5 and LingBot-VA in LIBERO simulation. Physical-robot behavior and complete sensorto-actuator deadlines are outside this evaluation. Broader hardware and task coverage, sustained control-loop characterization, and multi-session resource accounting are directions for further evaluation. Capsules resume compatible sessions within one process (§3.4). 

**Conclusion.** Fast kernels are necessary but not sufficient. FLASHRT-PAI co-designs their interfaces, launch dependencies, and state lifetimes, recording the result in an execution contract. Across four policies on Thor and six on RTX 5090, evaluated paths are 3.38–12.66 _×_ faster than official eager paths and 1.3–3.7 _×_ faster than compiled paths at matched 16-bit precision. FLASHRT-PAI has delivered tangible impact across industry and the open-source research community (§6): it is open source, its kernels are distributed through the Hugging Face Kernel Hub, and its opt-in kernels have been adopted in LeRobot. 

Looking ahead, we envision FLASHRT-PAI as a standard inference engine for physical AI, with pipeline co-design providing a reusable foundation for production deployment. 

## **REFERENCES** 

Arman Akbari, Ci Zhang, Arash Akbari, Lin Zhao, Yixiao Chen, Weiwei Chen, Xuan Zhang, Geng Yuan, and 

Yanzhi Wang. Flash-WAM: Modality-aware distillation for world action models. arXiv:2606.05254, 2026. 

- Jason Ansel, Edward Yang, Horace He, Natalia Gimelshein, Animesh Jain, Michael Voznesensky, Bin Bao, Peter Bell, David Berard, Evgeni Burovski, Geeta Chauhan, Anjali Chourdia, Will Constable, Alban Desmaison, Zachary DeVito, Elias Ellison, Will Feng, Jiong Gong, Michael Gschwind, Brian Hirsh, Sherlock Huang, Kshiteej Kalambarkar, Laurent Kirsch, Michael Lazos, Mario Lezcano, Yanbo Liang, Jason Liang, Yinghai Lu, C. K. Luk, Bert Maher, Yunjie Pan, Christian Puhrsch, Matthias Reso, Mark Saroufim, Marcos Yukio Siraichi, Helen Suk, Shunting Zhang, Michael Suo, Phil Tillet, Xu Zhao, Eikan Wang, Keren Zhou, Richard Zou, Xiaodong Wang, Ajit Mathews, William Wen, Gregory Chanan, Peng Wu, and Soumith Chintala. PyTorch 2: Faster machine learning through dynamic Python bytecode transformation and graph compilation. In _Proceedings of the 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 2 (ASPLOS)_ , 2024. doi: 10.1145/3620665.3640366. 

- Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, Hongyan Zhao, Hanyu Liu, Zhizhong Su, Lei Ma, Hang Su, and Jun Zhu. Motus: A unified latent action world model. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2026. arXiv:2512.13030. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A visionlanguage-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Kevin Black, Manuel Y. Galliker, and Sergey Levine. Realtime execution of action chunking flow policies. _arXiv preprint arXiv:2506.07339_ , 2025. 

- Black Forest Labs. FLUX 3 Action: A world action model for robot control. https://bfl.ai/ models/flux-3-action, 2026. 

- Tianqi Chen, Thierry Moreau, Ziheng Jiang, Lianmin Zheng, Eddie Yan, Meghan Cowan, Haichen Shen, Leyuan Wang, Yuwei Hu, Luis Ceze, Carlos Guestrin, and Arvind Krishnamurthy. TVM: An automated end-to-end optimizing compiler for deep learning. In _13th USENIX Symposium on Operating Systems Design and Implementation (OSDI)_ , 2018. 

- Yuxuan Chen, Wanruo Zhang, and Xiao Li. Reflex: Enabling fast and predictive vision-language-action models for reaction-critical manipulation. arXiv:2608.14379, 2026. 

- Tri Dao. FlashAttention-2: Faster attention with better parallelism and work partitioning. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- Mostafa Dehghani, Anurag Arnab, Lucas Beyer, Ashish Vaswani, and Yi Tay. The efficiency misnomer. _arXiv preprint arXiv:2110.12894_ , 2021. URL https:// arxiv.org/abs/2110.12894. 

- Elias Frantar, Roberto L. Castro, Jiale Chen, Torsten Hoefler, and Dan Alistarh. MARLIN: Mixed-precision autoregressive parallel inference on large language models. _arXiv preprint arXiv:2408.11743_ , 2024. URL https://github.com/IST-DASLab/marlin. 

- Shiwei Gao, Youmin Chen, and Jiwu Shu. Fast state restoration in LLM serving with HCache. In _Proceedings of the Twentieth European Conference on Computer Systems (EuroSys)_ , 2025. doi: 10.1145/3689031.3696072. 

- In Gim, Guojun Chen, Seung seob Lee, Nikhil Sarda, Anurag Khandelwal, and Lin Zhong. Prompt cache: Modular attention reuse for low-latency inference. In _Proceedings of Machine Learning and Systems (MLSys)_ , 2024. arXiv:2311.04934. 

- Hugging Face. LeRobot: State-of-the-art machine learning for real-world robotics in PyTorch. https://github. com/huggingface/lerobot, 2024. 

- Hugging Face. Kernel hub. https://huggingface. co/kernels, 2026. 

- Jordan Juravsky, Bradley Brown, Ryan Ehrlich, Daniel Y. Fu, Christopher Re, and Azalia Mirhoseini.´ Hydragen: High-throughput LLM inference with shared prefixes. _arXiv preprint arXiv:2402.05099_ , 2024. 

- Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model serving with PagedAttention. In _Proceedings of the 29th Symposium on Operating Systems Principles (SOSP)_ , 2023. doi: 10.1145/3600006.3613165. 

- LeRobot contributors. perf(pi052): sync-free denoise loop + opt-in FlashRT FP8 MLP. https://github.com/ huggingface/lerobot/pull/3870, 2026. Hugging Face LeRobot pull request #3870, merged 2026-0624. 

- Lin Li, Qihang Zhang, Yiming Luo, Shuai Yang, Ruilin Wang, Fei Han, Mingrui Yu, Zelin Gao, Nan Xue, Xing Zhu, Yujun Shen, and Yinghao Xu. Causal world modeling for robot control. _arXiv preprint arXiv:2601.21998_ , 2026a. 

- Zekai Li, Yihao Liang, Hongfei Zhang, Jian Chen, Yesheng Liang, and Zhijian Liu. FlashDrive: Flash vision-language-action inference for autonomous driving. arXiv:2608.12932, 2026b. 

- Ji Lin, Jiaming Tang, Haotian Tang, Shang Yang, Wei-Ming Chen, Wei-Chen Wang, Guangxuan Xiao, Xingyu Dang, Chuang Gan, and Song Han. AWQ: Activation-aware weight quantization for on-device LLM compression and acceleration. In _Proceedings of Machine Learning and Systems (MLSys)_ , 2024. 

- Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- Feng Liu, Shiwei Zhang, Xiaofeng Wang, Yujie Wei, Haonan Qiu, Yuzhong Zhao, Yingya Zhang, Qixiang Ye, and Fang Wan. Timestep embedding tells: It’s time to cache for video diffusion model. _arXiv preprint arXiv:2411.19108_ , 2024. 

- Xiaoyu Ma, Zhengqing Yuan, Zheyuan Zhang, Kaiwen Shi, Lichao Sun, and Yanfang Ye. BLURR: A boosted low-resource inference for vision-language-action models. arXiv:2512.11769, 2025a. 

- Yunchao Ma, Yizhuang Zhou, Yunhuan Yang, Tiancai Wang, and Haoqiang Fan. Running VLAs at real-time speed. arXiv:2510.26742, 2025b. 

- MindOn. Mind-1. https://www.mindon.tech/ blog/mind-1/index.html, 2026. Blog post, 30 September 2026. 

- NVIDIA. CUDA C++ programming guide: CUDA graphs. https://docs.nvidia.com/cuda/ cuda-c-programming-guide/, 2024. 

- NVIDIA. Isaac GR00T. https://github.com/ NVIDIA/Isaac-GR00T, 2025. 

- NVIDIA. Beyond VLAs: How world action models reshape robot manipulation. NVIDIA Technical Blog, https://developer.nvidia.com/blog/ beyond-vlas-how-world-action-modelsreshape-robot-manipulation/, 2026a. 

- NVIDIA. CUDA programming guide: Programmatic dependent launch and synchronization. https://docs.nvidia.com/cuda/cudaprogramming-guide/04-special-topics/ 

programmatic-dependent-launch.html, 2026b. 

- NVIDIA. CUTLASS: CUDA templates for linear algebra subroutines. https://github.com/NVIDIA/ cutlass, 2026c. 

- NVIDIA. Isaac GR00T N1.7 deployment: PyTorch and TensorRT inference. https: //github.com/NVIDIA/Isaac-GR00T/blob/ main/scripts/deployment/README.md, 2026d. Accessed 2026-10-01. 

- NVIDIA. Isaac gr00t 1.7 on jetson thor. https: //www.jetson-ai-lab.com/tutorials/ groot_n17_on_thor/, 2026e. Accessed 2026-1006; published JetPack 7.2 MAXN measurements. 

- NVIDIA. OpenPi _π_ 0 _._ 5 on Jetson Thor (Jetson AI Lab tutorial). https://www.jetson-ai-lab.com/ tutorials/openpi_on_thor/, 2026f. 

- NVIDIA. TensorRT. https://developer.nvidia. com/tensorrt, 2026g. 

- NVIDIA. TensorRT-LLM: Overview. https://nvidia. github.io/TensorRT-LLM/overview.html, 2026h. Documentation, accessed October 14, 2026. 

- NVIDIA, Johan Bjorck, Fernando Castaneda, Nikita Cherni-˜ adev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith Llontop, Loic Magne, Ajay Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. GR00T N1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- NVIDIA, Aditi, Niket Agarwal, Arslan Ali, Jon Allen, Martin Antolini, Adeline Aubame, Alisson Azzolini, Junjie Bai, Maciej Bala, Yogesh Balaji, Josh Bapst, Aarti Basant, Mukesh Beladiya, Mohammad Qazim Bhat, Zaid Pervaiz Bhat, Dan Blick, Vanni Brighella, Han Cai, Tiffany Cai, Eric Cameracci, Jiaxin Cao, Yulong Cao, Mark Carlson, Carlos Casanova, Ting-Yun Chang, Yan Chang, Yu-Wei Chao, Prithvijit Chattopadhyay, Roshan Chaudhari, Chieh-Yun Chen, Junyu Chen, Ke Chen, Qizhi Chen, Wenkai Chen, Xiaotong Chen, Yu Chen, An-Chieh Cheng, Click Cheng, Xiu Chia, Jeana Choi, Chaeyeon Chung, Wenyan Cong, Yin Cui, Magdalena Dadela, Nalin Dadhich, Wenliang Dai, Joyjit Daw, Alperen Degirmenci, Rodrigo Vieira Del Monte, Robert Denomme, Sameer 

Dharur, Marco Di Lucca, Ke Ding, Wenhao Ding, Yifan Ding, Yuzhu Dong, Nicole Drumheller, Yilun Du, Aigul Dzhumamuratova, Aleksandr Efitorov, Hamid Eghbalzadeh, Naomi Eigbe, Imad El Hanafi, Hassan Eslami, Benedikt Falk, Jiaojiao Fan, Jim Fan, Amol Fasale, Sergiy Fefilatyev, Liang Feng, Francesco Ferroni, Sanja Fidler, Xiao Fu, Vikram Fugro, Prashant Gaikwad, TJ Galda, Katelyn Gao, Yihuai Gao, Wenhang Ge, Sreyan Ghosh, Arushi Goel, Vivek Goel, Akash Gokul, Rama Govindaraju, Jinwei Gu, Miguel Guerrero, Elfie Guo, Aryaman Gupta, Siddharth Gururani, Hugo Hadfield, Song Han, Ankur Handa, Zekun Hao, Mohammad Harrim, Ali Hassani, Nathan Hayes-Roth, Yufan He, Chris Helvig, Cyrus Hogg, Madison Huang, Michael Huang, Sophia Huang, Yufan Huang, Jacob Huffman, DeLesley Hutchins, Suneel Indupuru, Boris Ivanovic, Arihant Jain, Joel Jang, Ryan Ji, Yanan Jian, Dongfu Jiang, Jingyi Jin, Atharva Joshi, Nikhilesh Joshi, Pranjali Joshi, Andy Ju, Jaehun Jung, Weiwei Kang, Scott Kassekert, Jan Kautz, Ashna Khetan, Julia Kiczka, Slawek Kierat, Gwanghyun Kim, Kuno Kim, Sunny Kim, Kezhi Kong, Xin Kong, Zhifeng Kong, Tomasz Kornuta, Egor Krivov, Hui Kuang, Saurav Kumar, Chia-Wen Kuo, George Kurian, Wojciech Kutak, JF Lafleche, Himangshu Lahkar, Omar Laymoun, Jayjun Lee, Sanggil Lee, Gabriele Leone, Boyi Li, Freya Li, Jiajun Li, Jinfeng Li, Ling Li, Pengcheng Li, Shangru Li, Tingle Li, Xiaolong Li, Xuan Li, Zhaoshuo Li, Zhiqi Li, Hao Liang, Maosheng Liao, Chen-Hsuan Lin, Tsung-Yi Lin, Ming-Yu Liu, Sifei Liu, Zihan Liu, Hai Loc Lu, Xiangyu Lu, Alice Luo, Ruipu Luo, Wenjie Luo, Jiangran Lyu, Martin Ding Ma, Nic Ma, Qianli Ma, Dawid Majchrowski, Louis Marcoux, Miguel Martin, Qing Miao, Ashkan Mirzaei, Shreyas Misra, Kaichun Mo, Durra Mohsin, Hyejin Moon, Pawel Morkisz, Saeid Motiian, Kirill Motkov, Seungjun Nah, Yashraj Narang, Deepak Narayanan, Thabang Ngazimbi, Julian Ouyang, Shubham Pachori, David Page, Yatian Pang, Sehwi Park, Mahesh Patekar, Mostofa Patwary, Marco Pavone, Trung Pham, Wei Ping, Soha Pouya, Shrimai Prabhumoye, Varun Praveen, Delin Qu, Hesam Rabeti, Morteza Ramezanali, Marilyn Reeb, Xuanchi Ren, Kristen Rumley, Wojciech Rymer, Jun Saito, Yeongho Seol, John Shao, Piyush Shekdar, Tianwei Shen, Humphrey Shi, Min Shi, Stella Shi, Kevin Shih, Mohammad Shoeybi, Mateusz Sieniawski, Shuran Song, Alexander Sotelo, Amir Sotoodeh, Sunil Srinivasa, Vignesh Srinivasakumar, Bartosz Stefaniak, Rahul Heinrich Steiger, Shangkun Sun, Jiaxiang Tang, Shitao Tang, Yangyang Tang, Yue Tang, Tolou Tavakkoli, Kayley Ting, Krzysztof Tomala, Wei-Cheng Tseng, Jibin Varghese, Sergei Vasilev, Thomas Volk, Raju Wagwani, Roger Waleffe, Andrew Z. Wang, Boxiang Wang, Haoxiang Wang, Qiao Wang, Shihao Wang, Shijie Wang, TingChun Wang, Yan Wang, Yu Wang, Rohit Watve, David Wehr, Fangyin Wei, Xinshuo Weng, Jay Zhangjie Wu, 

Kedi Wu, Hongchi Xia, Summer Xiao, Tianjun Xiao, Kevin Xie, Daguang Xu, Jiashu Xu, Mengyao Xu, Ruqing Xu, Xingqian Xu, Yao Xu, Dinghao Yang, Dong Yang, Hans Yang, Xiaodong Yang, Xuning Yang, Yichu Yang, Yurong You, Zhiding Yu, Hao Yuan, Simon Yuen, Xiaohui Zeng, Pengcuo Zeren, Cindy Zha, Haotian Zhang, Jenny Zhang, Jing Zhang, Liangkai Zhang, Paris Zhang, Shun Zhang, Xuanmeng Zhang, Zhizheng Zhang, Ann Zhao, Yilin Zhao, Yuliya Zhautouskaya, Charles Zhou, Fengzhe Zhou, Shilin Zhu, Yuke Zhu, Dima Zhylko, and Artur Zolkowski. Cosmos 3: Omnimodal world models for physical AI. _arXiv preprint arXiv:2606.02800_ , 2026. 

- Rui Pan, Zhuang Wang, Zhen Jia, Can Karakus, Luca Zancato, Tri Dao, Yida Wang, and Ravi Netravali. Marconi: Prefix caching for the era of hybrid LLMs. In _Proceedings of Machine Learning and Systems (MLSys)_ , 2025. arXiv:2411.19379. 

- Physical Intelligence. openpi. https://github.com/ Physical-Intelligence/openpi, 2025. 

- Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- Physical Intelligence, Bo Ai, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Greg Balke, Kevin Black, George Bokinsky, Shihao Cao, Thomas Charbonnier, Vedant Choudhary, Foster Collins, Ken Conley, Grace Connors, James Darpinian, Karan Dhabalia, Maitrayee Dhaka, Jared DiCarlo, Danny Driess, Michael Equi, Adnan Esmail, Yunhao Fang, Chelsea Finn, Catherine Glossop, Thomas Godden, Ivan Goryachev, Lachlan Groom, Haroun Habeeb, Hunter Hancock, Karol Hausman, Gashon Hussein, Victor Hwang, Brian Ichter, Connor Jacobsen, Szymon Jakubczak, Rowan Jen, Tim Jones, Gregg Kammerer, Ben Katz, Liyiming Ke, Mairbek Khadikov, Chandra Kuchi, Marinda Lamb, Devin LeBlanc, Brendon LeCount, Sergey Levine, Xinyu Li, Adrian Li-Bell, Vladislav Lialin, Zhonglin Liang, Wallace Lim, Yao Lu, Enyu Luo, Vishnu Mano, Nandan Marwaha, Aikys Mongush, Liam Murphy, Suraj Nair, Tyler Patterson, Karl Pertsch, Allen Z. Ren, Gavin Schelske, Charvi Sharma, Baifeng Shi, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, Will 

Stoeckle, Jiaming Tang, Jimmy Tanner, Shalom Tekeste, Marcel Torne, Kyle Vedder, Quan Vuong, Anna Walling, Haohuan Wang, Jason Wang, XuDong Wang, Chris Whalen, Samuel Whitmore, Blake Williams, Charles Xu, Sukwon Yoo, Lili Yu, Wuming Zhang, Zhuoyang Zhang, and Ury Zhilinsky. _π_ 0 _._ 7: a steerable generalist robotic foundation model with emergent capabilities. _arXiv preprint arXiv:2604.15483_ , 2026. 

- PKU SEC Lab. EagleVLA-Edge: A llama.cppbased inference engine for real-time onboard VLA control. https://github.com/PKU-SEC-Lab/ EagleVLA-Edge, 2026. 

- Aaditya Prasad, Kevin Lin, Jimmy Wu, Linqi Zhou, and Jeannette Bohg. Consistency policy: Accelerated visuomotor policies via consistency distillation. In _Robotics: Science and Systems (RSS)_ , 2024. arXiv:2405.07503. 

- Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, and Chang Xu. VLA-Cache: Efficient visionlanguage-action manipulation via adaptive token caching. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. arXiv:2502.02175. 

- Yantai Yang, Yuhao Wang, Zichen Wen, Luo Zhongwei, Chang Zou, Zhipeng Zhang, Chuan Wen, and Linfeng Zhang. EfficientVLA: Training-free acceleration and compression for vision-language-action models. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. arXiv:2506.10100. 

- Zebin Yang, Qi Wang, Yunhe Wang, Xiurui Guo, Bo Yu, Shaoshan Liu, Jiafeng Xu, Hao Dong, and Meng Li. EagleVLA: Towards onboard real-time robot control via foresight-aligned asynchronous inference. In _Conference on Robot Learning (CoRL)_ , 2026. 

- Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, George Kurian, Suneel Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, Ayaan Malik, Kyungmin Lee, William Liang, Nadun Ranawaka, Jiasheng Gu, Yinzhen Xu, Guanzhi Wang, Fengyuan Hu, Avnish Narayan, Johan Bjorck, Jing Wang, Gwanghyun Kim, Dantong Niu, Ruijie Zheng, Yuqi Xie, Jimmy Wu, Qi Wang, Ryan Julian, Danfei Xu, Yilun Du, Yevgen Chebotar, Scott Reed, Jan Kautz, Yuke Zhu, Linxi Fan, and Joel Jang. World action models are zero-shot policies. _arXiv preprint arXiv:2602.15922_ , 2026. 

- Zihao Ye, Lequn Chen, Ruihang Lai, Wuwei Lin, Yineng Zhang, Stephanie Wang, Tianqi Chen, Baris Kasikci, Vinod Grover, Arvind Krishnamurthy, and Luis Ceze. FlashInfer: Efficient and customizable attention engine for LLM inference serving. In _Proceedings of Machine Learning and Systems_ , volume 7, 2025. URL https://proceedings.mlsys. 

org/paper_files/paper/2025/hash/ dbf02b21d77409a2db30e56866a8ab3aAbstract-Conference.html. 

- Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Chuyue Sun, Jeff Huang, Cody Hao Yu, Shiyi Cao, Christos Kozyrakis, Ion Stoica, Joseph E. Gonzalez, Clark Barrett, and Ying Sheng. SGLang: Efficient execution of structured language model programs. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. arXiv:2312.07104. 

## **A WORKED EXAMPLES** 

The worked examples below show the contract and verified measurement details, then the deployment facts behind fusion, launch overlap, and state reuse. 

### **A.1 Worked Execution Contract** 

The contract is exported through a versioned C interface. It lists captured graphs and their supported shapes, named buffers, restorable byte regions, and an identity fingerprint used to match saved state to its execution plan. The model interface adds inputs with shapes and update methods, plus stages with explicit prerequisites. 

**Execution rules.** A retained value can be reused only while its source inputs are unchanged. Stages consume prerequisite outputs valid for the current inputs. Restored state belongs to a compatible plan and resumes at the declared boundary; a new observation still requires a new context stage. These rules specify correct use of the interface. Listing 1 shows two of its records; names and field types follow the implementation. 


_Listing 1._ Contract records for saved regions and stage order. A region names the buffer bytes to copy; a stage names its graph and prerequisite stages. 

**Engine checks and input updates.** Construction rejects stage references to missing graphs or prerequisites that have not been declared. An input that requires processing must provide its update function. Replay requires a captured variant for the requested shape, and restore checks statelayout and plan compatibility. For example, the GR00T N1.7 Thor frontend rejects a second prompt initialization and requires a new frontend instance for a new prompt. 

**Caller responsibilities.** The normal model call performs its declared input processing and stage sequence. A host driving individual stages must submit current inputs and refresh dependent state before action replay. If it omits an update or reuses context from an older observation, the result can be an action based on outdated inputs. Shape and plan checks do not detect such unreported changes. The interface checks execution compatibility; the host retains responsibility for input freshness and the robot’s control loop. 

**Worked plan.** In the split _π_ 0 _._ 5 plan below, the engine owns the fixed allocations and replay handles; the application supplies input updates, and the session manager orders stages and capsule copies. 

_Table 9._ Buffer roles and update events in the split _π_ 0 _._ 5 <u>plan.</u> 

|Buffer|Role / writer|Refresh event|
|---|---|---|
|Images|Swap / host|Fresh observation|
|Noise|Swap / host|New action generation|
|Prompt embedding|Static / preparation|Prompt change|
|Step conditioning|Static / preparation|Schedule change|
|Context K/V|State / context|Image or prompt change|
|Actions|Swap / action|Action replay|


Preparation writes instruction embeddings and fixed-step conditioning. Context reads images and the prepared prompt and writes K/V. Action depends on context, reads that K/V and the noise window, and produces the action chunk. A fresh observation therefore invalidates context, even when the instruction is unchanged. Each replay plan is selected by its supported shape; changing a shape requires preparation and capture before replay. 

At the post-context boundary, the measured capsule contains context K/V, instruction embeddings, and the decoder position table, totaling 14.40 MB. The exported region list gives names, offsets, and lengths; schema and plan fingerprint checks restrict restore to a compatible session. Weights and fixed step tables remain resident and are not copied in this experiment. Restoring this state permits continuation from the completed context; a new image refreshes the context stage. The application supplies the input-change events that determine when retained values are refreshed. 

### **A.2 Measurement Details and Short-Run Distributions** 

Timing boundaries are specific to each host. The deployed _π_ 0 _._ 5/Thor infer interval includes image upload, model execution, action transfer, and decoding, excluding prompt setup. The 8.23 ms _π_ 0 _._ 5/RTX 5090 entry measures captured GPU replay. Cosmos/Thor measures in-process CPU observation to CPU action. GR00T/RTX 5090 measures GPU infer(aux), including fresh vision features and the complete DiT. LingBot-VA/Thor reports the mean over saturated chunks 43–47; its RTX 5090 measurement covers history update and prediction, excluding reset, network transfer, and text encoding. Cosmos/RTX 5090 includes preprocessing, VAE and text processing, denoising, and action formatting in both paths. Published reference ratios retain their original source protocols; they are distinct from the paired PDL and reuse experiments. 

The controlled _π_ 0 _._ 5/Thor state experiment uses engine source e4bd927, PyTorch 2.14.0+cu130, and CUDA 13.0 in a separate host environment from the deployment image. 

Reuse averages 12 alternating pairs over eight recorded observations; both sides replay identical graphs and differ only in recomputing prompt embeddings and step conditioning. Resume, snapshot, and restore-only statistics use 64 paired trials. Every restored continuation and reuse comparison is bit-exact. The PDL experiment uses the same engine source and kernel inventory, 30 warm-ups and 200 interleaved CUDA-event decoder samples per mode; synchronized whole-call medians span eight recorded observations, with 40 bit-exact gates. 

_Table 10._ Short-run Thor latency distributions (ms). Rows retain their own timing intervals; decoder p95 is not whole-call p95. 

|Interval|Samples|p50|p95|
|---|---|---|---|
|Deployed_π_0_._5 infer|1000|20.33|20.54|
|PDL off, decoder|200|10.124|10.137|
|PDL FFN + O/QKV, decoder|200|9.207|9.220|
|PDL all, decoder|200|9.009|9.024|
|Rebuild + action|64|21.484|21.533|
|Restore + action|64|9.726|9.778|
|Snapshot only|64|0.477|0.531|
|Restore only|64|0.131|0.139|


The deployment run uses 200 warm-ups; the controlled state and PDL results report paired changes under the stated configuration. Their 21.61 ms reuse and 21.960 ms PDLoff intervals were collected in the controlled host environment; the 20.33 ms deployment interval comes from the deployment image. The distributions summarize the stated warmed-up runs. Sampling counts and compiler settings are recorded per configuration: Cosmos/Thor uses default torch.compile settings and 60 timed calls per deployment path, with p90 of 1227.45, 1267.09, and 363.86 ms for eager, compile, and mixed 4-bit respectively. Table 4 compares configurations collected across precision tiers and measurement sessions; controlled mechanism changes are measured by the paired PDL and reuse experiments. Capsule results measure state-copy and continuation operations over shared working buffers. 

**Fidelity samples.** _π_ 0 _._ 5 uses eight observations on Thor and 24 real LIBERO frames on RTX 5090; the latter has 16 separate calibration frames. GR00T/Thor uses one single-view observation. The RTX 5090 GR00T result is one two-view LIBERO observation at four denoising steps, compared with the FP16 frontend; its 0.999985 cosine matches the workload of the 7.67 ms latency entry. Cosmos uses 114 requests (38 observations, three noise seeds) on Thor and 60 requests (12 observations, five seeds) on RTX 5090. Motus uses four RoboTwin2 input bundles (Appendix A.2.2). LingBotVA/RTX 5090 scores 717 chunks from 40 traces held out from calibration, against the official FP32 reference with TF32 disabled. Arm and full-action results are reported below. The evaluated mixed-precision configuration uses FP8 for the video backbone’s cross-attention query/output, self-attention QKV, and FFN output projections, and INT4 

_Table 11._ Recorded validation by <u>policy.</u> 

|Policy|Recorded validation|
|---|---|
|_π_0_._5|Recorded-input action comparisons; LIBERO-10<br>rollouts against the measured FP16 reference.|
|GR00T N1.7|Single-view Thor and two-view RTX 5090<br>LIBERO observations; single-observation cosine.|
|LingBot-VA|RTX 5090: held-out LIBERO traces for arm/full-<br>action agreement; paired 100-episode LIBERO-10<br>success comparison.|
|FLUX 3 Action|Returned-action agreement against the official im-<br>plementation under matched inputs and noise.|
|Cosmos3-Edge-Policy|DROID observations: 114 observation/noise re-<br>quests on Thor and 60 on RTX 5090.|
|Motus|Four RoboTwin2 input bundles;<br>action and<br>decoded-video agreement against saved upstream<br>outputs.|


weight-only GEMMs for action steps; attention operations and history updates retain their higher-precision paths. It retains 20 video and 50 action denoising steps. This configuration is timed at 455.70 ms and is used for both the filtered diagnostic and the unfiltered results below. For _π_ 0 _._ 5, LIBERO success rates compare the measured official FP16 reference with the 4-bit FLASHRT-PAI rollouts. LingBot-VA uses its official BF16 reference and the FP8/INT4 configuration described above. Its paired evaluation runs tasks 0–9 and episodes 0–9 with the same seeds and initial states: 98/100 successes for the reference and 97/100 for FLASHRT-PAI. 

**Validation represented in the tables.** Table 7 reports returned-action comparisons for all six policies, and closedloop success rates for _π_ 0 _._ 5 and LingBot-VA. The accompanying records cover the following inputs and evaluation settings. 

### _A.2.1 LingBot-VA: unfiltered action agreement_ 

Table 12 reports all recorded chunks, including numerically sensitive ones. Each chunk contains 16 actions with six arm channels and a binary gripper command. We report arm motion separately from the complete action because a change in gripper-switch timing can strongly affect the full-action cosine. 

_Table 12._ Unfiltered LingBot-VA/RTX 5090 action agreement against official FP32. Entries are global / worst-chunk cosine. The mixed configuration matches the 455.70 ms deployment. 

|Configuration|Six arm|channels|Fu|ll action|
|---|---|---|---|---|
|BF16|.999502 /|.952046|.997388 /|.643595|
|FP8/INT4 mix|.998907 /|.941478|.994571 /|.405055|


As a diagnostic, 670 chunks have stable arm outputs across numerical configurations of the official reference (relative- _L_ 2 threshold 0.1). This selection uses no FLASHRTPAI outputs. On that subset, arm global/worst cosine is .999691/.985367 for BF16 and .999188/.964353 for the mixed path. The main table uses the unfiltered arm scores. 

### _A.2.2 Motus: four-input action and video agreement_ 

The Stage3 Motus deployment is checked on four RoboTwin2 input bundles using the same ten-step FP4 configuration as the 167.08 ms result, without TeaCache. Each bundle supplies its first frame for calibration. Comparisons use the saved upstream actions and decoded video; Table 13 reports the per-input cosines, summarized over ten graph replays. The main fidelity table reports the range across the four action cosines, rather than treating replays of one input as additional samples. 

_Table 13._ Motus agreement on four RoboTwin2 inputs, compared with saved upstream outputs. The evaluated configuration retains all ten denoising steps. 

|Input|Action cosine|Video cosine|
|---|---|---|
|sample<br>~~0~~0<br><br>|.999929|.999117|
|sample<br>~~0~~1<br>|.999935|.998644|
|sample<br>~~0~~2|.999921|.999144|
|sample<br>~~0~~3|.999913|.998844|


### **A.3 Deep Kernel Fusion Examples** 

**Calibrated producer–consumer quantization.** An FP8 GEMM needs an FP8 input and a scale. In a dynamic path, separate kernels may first find the activation maximum and then convert the activation before the GEMM. For the _π_ 0 _._ 5 encoder FFN, FLASHRT-PAI measures an acceptable scale on representative task inputs before capture. The preceding normalization kernel then emits FP8 directly at that scale, and its single FFN consumer reads those same bytes. The producer and consumer must be selected as a pair: an FP8 output handed to a BF16 entry is an error, not a useful fallback. Attention-output conversion is one boundary that still uses a separate kernel. 

**The ten-row action shape.** The _π_ 0 _._ 5 action expert always presents ten rows, but the stock NVFP4 GEMM tile reserves space for 128 activation rows. Its out-of-bounds rows still cost memory-system work. For selected decoder projections, FLASHRT-PAI swaps the GEMM operands: the large tile carries weights, the ten activation rows use the short dimension, and a column-major store has exactly the bytes the next kernel expects as row-major output. No transpose kernel is needed. The fixed row count is guarded in the implementation. The fixed deployment shape makes this tile choice valid throughout replay. 

**Phase fusion across layers.** After an FFN downprojection, the policy must update a residual, normalize for the next layer, and convert its input for the next GEMM. If those steps run as separate kernels, each boundary adds a launch and moves an intermediate through memory. FLASHRT-PAI’s practical phase kernel combines the gated residual, next-layer adaptive normalization, and FP8 

conversion. The known layer and denoising-step order tells it which next-layer style and scale to read. Figure 3 counts 20 kernels and 193.2 _µ_ s per layer on the compiler path versus 12 kernels and 105.2 _µ_ s on the composed FLASHRTPAI path, measuring the combined pipeline changes at layer granularity. 

**QKV split, RoPE, and cache write.** After the _π_ 0 _._ 5 QKV projection, a conventional sequence can split the combined output, rotate query and key positions, and write the key/value cache in separate passes. FLASHRT-PAI uses one kernel to do all three while those values are already being visited. The pipeline fixes the head geometry and the K/V cache layout; a device-side valid-prefix position tells the kernel where to append K/V even when prompts are padded to a common capture shape. The cache layout and position rule make the combined write valid throughout replay. 

**NVFP4 output directly from a GEMM.** In the _π_ 0 _._ 5 encoder feed-forward block, a GEMM produces two vectors, _gate_ and _up_ . The earlier path launched a separate kernel to compute GELU( _gate_ ) _× up_ , quantize the result, and pack it for the next GEMM. FLASHRT-PAI instead pairs gate and up weights when loading the checkpoint. That puts each pair of results next to each other inside the GEMM, allowing its epilogue to compute the product and write packed fourbit values and block scales directly in the next GEMM’s required layout. An initial fused version wrote a full-width result and doubled the next GEMM’s weight traffic, so its feed-forward chain was slower than the separate-kernel path. A compact, half-width store kept the next GEMM’s original shape; decision latency then fell, and the worst measured output cosine improved because the intermediate was quantized once rather than twice. The layout and producer–consumer format were designed and validated for this pipeline, not inferred from an ordinary operator graph. 

### **A.4 Launch-Overlap Examples** 

**Fetching weights before the activation is ready.** A GEMM cannot read an activation produced by the previous kernel until that kernel finishes, but its fixed weights are already available. FLASHRT-PAI’s decoder GEMM starts streaming a few weight tiles before the wait, then loads the activation only after the dependency is satisfied. This shortened the decoder GEMM chain with identical outputs, but the gain was not monotonic: fetching all seven weight tiles early congested the memory queue, while two or three tiles worked best. Moving the release signal from the load warp to the multiply warp also gave up much of the benefit. The selected variant streams only the profitable prefix. 

**Choosing between persistent and separate GEMMs.** FLASHRT-PAI also built a resident grid that runs several de- 

coder GEMMs in one launch. Its load warp fetches the next GEMM’s weights while the current one finishes. With independent GEMMs, the chain ran faster than separate launches and came close to the measured memory-read ceiling. The version that also performs the required normalization between GEMMs, however, was slower than separate launches. The next GEMM must wait for the normalization result, and a grid-wide rendezvous adds cost that weight prefetch cannot hide. The implementation passed bit-exact checks but is disabled in the shipped path. A faster isolated chain was not a faster pipeline here; the useful rule is to fuse the memorybound work _between_ GEMMs, not every GEMM into one kernel. 

**Knowing when overlap has reached its limit.** More early work is not always better. In Thor tuning, extending early launch to RoPE, softmax, and FP8-conversion kernels produced no further measurable change. Prefetching the next layer’s weights into cache also slowed every tested variant of the decoder chain, because the prefetch competed with demand traffic. Together with the rejected persistent sequence above, these cases bound the technique: it can hide launch setup or input-independent memory traffic, but not work whose result the successor actually needs. FLASHRTPAI therefore tests overlap in the full pipeline as well as in isolated chains. 

### **A.5 Execution-State Reuse Example** 

**Instruction state.** The _π_ 0 _._ 5 action expert has ten denoising steps and eighteen layers; its adaptive-normalization values form a finite step-by-layer table for a given instruction. Rebuilding those values inside every decision repeats work whose input has not changed. FLASHRT-PAI’s set ~~p~~ rompt builds the table and prompt embedding once, keeps them in named buffers, and lets later kernels select the needed row. A same-size prompt update overwrites the existing embedding rather than replacing its address; a device-side valid length masks padding without recapture. In an earlier compiler implementation, in-graph Dense GEMMs rebuilt these styles at every inference, and handediting that graph to precompute them reduced its latency. FLASHRT-PAI uses the same temporal-hoisting idea in its prompt setup. The instruction lifetime and refresh rule specify when this prepared state can be reused and when it must be rebuilt. 

