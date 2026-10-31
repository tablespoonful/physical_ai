---
title: "SparkVLA: Stop-Aware Hierarchical VLA with Adaptive Action Chunking for Long-Horizon Manipulation"
date: "2026-08-17"
authors: "Xunyao Lei; Renjun Wu; Tianlin Huo; Xuesong Li"
url: https://arxiv.org/abs/2608.16172
pdf: https://arxiv.org/pdf/2608.16172
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2608.16172)** / [論文ページ](https://arxiv.org/abs/2608.16172)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SparkVLA: Stop-Aware Hierarchical VLA with Adaptive Action Chunking for Long-Horizon Manipulation** 

**Xunyao Lei**<sup>**1,***</sup> **, Renjun Wu**<sup>**1,***</sup> **, Tianlin Huo**<sup>**2**</sup> **, Xuesong Li**<sup>**1,**�</sup> 

1Beijing Institute of Technology 

2Tsinghua University 

*Equal contribution �Corresponding author Project page: https://icr-lab.github.io/SparkVLA 

#### **Abstract** 

At every re-observation point in a hierarchical VisionLanguage-Action (VLA) system, two interface decisions must be made: _when_ to terminate the current subtask and _how far_ to execute the proposed action chunk. These decisions are mutually dependent—the optimal stopping point depends on what the executor plans to do, while the optimal execution length depends on where the subtask boundary lies—yet existing architectures evaluate them in isolation, an asymmetry neither module can overcome alone. We present **SparkVLA** , a stop-aware hierarchical VLA that resolves this mutual dependency by formulating both decisions as a single ranking: Stop competes against every action-prefix length in a unified candidate set, and the system selects the highest-scoring option, eliminating threshold tuning and requiring only offline ordinal preferences. An _Anchor-Conditioned Context Encoding_ module caches a history-aware subtask anchor encoding onsetstate memory and goal semantics, guiding visual-token pruning toward task-relevant regions; a _Stop-Aware Action-Prefix Selection_ head scores all candidates via full self-attention at chunk boundaries for efficiency. On RoboCerebra, SparkVLA achieves **47.12%** success rate, surpassing the official hierarchical baseline by **30.57%** and the strongest reproducible method by 26.83% Real-robot experiments on multi-step tasks further validate these gains on physical hardware. 

## **Introduction** 

Recent Vision-Language-Action (VLA) models (Zitkovich et al. 2023; Kim et al. 2025; Black et al. 2026; Team et al. 2024; Black et al. 2025; Liu et al. 2025; NVIDIA et al. 2025; Shukor et al. 2025) have demonstrated remarkable generalization on robotic manipulation, yet they are predominantly trained on short trajectory segments and struggle to compose multiple skills over long horizons (Yang et al. 2026; Han et al. 2026). Hierarchical VLA architectures (Brohan et al. 2023; Yang et al. 2026; Zhang et al. 2025; Jiang et al. 2025; Torne et al. 2026; Chen et al. 2026) address this by pairing a high-level VLM planner with a low-level VLA executor, achieving multi-step manipulation (Torne et al. 2026; Jiang et al. 2025), cross-embodiment transfer (Bu et al. 2025), and improved long-horizon robustness (Chen et al. 2026). A systematic study (Yang et al. 2026) identifies the _interface mechanisms_ —particularly the termination condition and execution horizon—as the highest-leverage design choices. Yet a critical interface decision remains under-explored: 

at every re-observation boundary the system must simultaneously judge _when to terminate the current subtask_ and _how far to execute the proposed action chunk_ . These two decisions jointly govern closed-loop behavior—premature termination discards progress, late termination causes overshooting, over-commitment leads to drift, and under-commitment wastes replanning budget—yet existing approaches treat each in isolation. On the termination side, hierarchical systems employ binary detectors (Jiang et al. 2025), VLM-predicted lengths (Yang et al. 2026), or progress signals (Liu et al. 2026)—all deciding _whether_ to stop without access to the upcoming plan. On the horizon side, DEHP (Zhao et al. 2026), ACH (Shin et al. 2026), AQC (Gireesh, Ju, and Wang 2026), and AAC (Liang et al. 2026) adaptively select how far to commit but cannot signal subtask completion. Crucially, these decisions are _mutually dependent_ : the optimal stopping point depends on what the executor plans to do next, while the optimal execution length depends on where the subtask boundary lies. This mutual dependency cannot be resolved by independent modules—it demands joint evaluation. 

We observe that both decisions reduce to a common assessment—how well the proposed chunk serves the current subtask from the present state—and formulate a unified candidate set in which Stop competes against every actionprefix lengthunder the same scoringhead (Figure 1).Because all candidates are scored within a single shared representation, termination can leverage the content of the proposed plan and horizon selection can leverage proximity to the subtask boundary—precisely the mutual information that isolated modules lack. Both decisions then reduce to selecting the highest-scoring candidate, eliminating threshold tuning and requiring only ordinal supervision. 

Building on this insight, we present SparkVLA, a stopaware hierarchical VLA built from a shared pretrained VLA: the high-level branch retains the VLM backbone for subtask generation and hosts the selector, while the low-level branch produces action chunks. An _Anchor-Conditioned Context Encoding_ module caches a history-aware subtask anchor encoding onset-state memory and goal semantics, guiding visual-token pruning toward task-relevant regions. A _StopAware Action-Prefix Selection_ head then scores all candidates via full self-attention and selects the highest-scoring option, trained from offline ordinal preferences. The selector operates only at chunk boundaries, improving both speed and 


Figure 1: Existing hierarchical VLAs either execute fixed-length chunks with a separate stop detector (b) or adapt the horizon without an explicit termination signal (c), addressing each decision in isolation. SparkVLA (a) unifies both into a single ranking over Stop and all action-prefix lengths, enabling joint adaptive execution and threshold-free subtask termination. 

accuracy over per-step monitoring. 

On RoboCerebra, SparkVLA achieves 47.12% success rate, outperforming the official hierarchical baseline by 30.57% and the strongest reproducible method by 26.83%. Real-robot experiments on three multi-step tasks validate these gains on physical hardware. 

Our contributions are threefold: 

- We formulate subtask termination and execution-horizon selection as a single ranking over a unified candidate set, resolving the mutual dependency without separate detectors, threshold tuning, or online reward signals. 

- We introduce _Anchor-Conditioned Context Encoding_ and _Stop-Aware Action-Prefix Selection_ , realizing this decision with a single scoring pass at chunk boundaries. 

- We demonstrate that SparkVLA’s high-level system generalizes across different low-level executors and transfers in both simulation and real-world platforms. 

## **Related Work** 

### **Hierarchical VLA Systems** 

Hierarchical architectures for robotic manipulation separate high-level planning from low-level execution to tackle longhorizon tasks (Yang et al. 2026; Zhang et al. 2025; Jiang et al. 2025; Bu et al. 2025; Torne et al. 2026; Chen et al. 2026). Representative systems pass latent features (Zhang et al. 2025), subtask-level language commands (Jiang et al. 2025), multi-scale memory (Torne et al. 2026), or task-phase classifiers (Chen et al. 2026) across the interface. MEM (Torne et al. 2026) combines short-term video with long-term language memory, enabling tasks spanning up to fifteen minutes; PALM (Liu et al. 2026) integrates affordance reasoning 

and continuous progress signals for subtask-aware execution. A systematic study (Yang et al. 2026) unifies these designs under an options-framework loop and identifies the termination condition as the highest-leverage interface mechanism. Despite this variety, all existing systems treat subtask termination as an isolated binary decision—judging whether to stop without access to the upcoming action plan or the execution horizon it implies. SparkVLA instead places termination inside a unified ranking over the proposed chunk, enabling joint assessment with execution length. 

### **Adaptive Action Chunking** 

Action chunking—predicting and committing to a short action sequence before replanning—is standard in modern visuomotor policies (Zhao et al. 2023; Chi et al. 2025), but a fixed execution horizon creates a fundamental tradeoff between smoothness and reactivity. DEHP (Zhao et al. 2026) trains a lightweight RL head to predict execution length while keeping the base policy frozen. ACH (Shin et al. 2026) and AQC (Gireesh, Ju, and Wang 2026) estimate Q-values for all candidate lengths in one forward pass, selecting the highest-value horizon without requiring online interaction. AAC (Liang et al. 2026) uses action entropy as a trainingfree cue for adaptive chunk-size selection at inference time. These methods improve over fixed horizons but cannot signal subtask completion. SparkVLA bridges both lines by scoring Stop and all action-prefix lengths under a shared head, trained from offline ordinal preferences without online RL. 


Figure 2: Overview of SparkVLA. At each subtask onset, the high-level planner autoregressively generates a subtask command, extracts a raw anchor from the penultimate layer, and fuses it with the anchor history pool via self-attention to form a historyaware anchor. At every decision boundary, anchor-conditioned context encoding extracts task-relevant visual features, while the stop-aware selector ranks Stop against all action-prefix candidates. 

## **Method** 

### **Problem Formulation** 

We formulate SparkVLA as a hierarchical VLA with a highlevel VLM planner and a low-level VLA executor. At a decision boundary _t_ , defined as a re-observation point at which a new execution decision is made, the robot receives camera observations _It_<sup>(1)</sup> _, . . . , It_<sup>(</sup><sup>_C_)</sup> from _C_ cameras and proprioceptive state _st ∈_ R<sup>_ds_</sup> , including the end-effector pose and gripper width. At the beginning of each subtask, the planner autoregressively generates a natural-language subtask command _ck_ , whose complete inputs are specified below. Conditioned on _ck_ , the current camera observations, and proprioceptive state, the executor produces an action chunk _At_ = ( _at, . . . , at_ + _H−_ 1) _∈_ R<sup>_H×da_</sup> . 

We define a unified candidate set _C_ = _{_ 0 _,_ 1 _, . . . , H}_ , where candidate 0 is **Stop** and each candidate _n ≥_ 1 denotes the **action-prefix** consisting of the first _n_ actions in _At_ . The selector ranks these candidates from the action chunk and two context representations, _αk_ and _mt_ , described next: 


Selecting an action-prefix executes its _n_ actions before reobserving, whereas selecting Stop completes the current subtask and triggers autoregressive generation of the next subtask command. The following subsections describe the closed-loop architecture, context construction, and candidate scoring, respectively. 

### **SparkVLA Architecture** 

SparkVLA derives two separately parameterized branches from the pre-trained _π_ 0 _._ 5 VLA. The high-level branch is built from the VLM backbone of _π_ 0 _._ 5 and serves as the autoregressive subtask generator, whereas the low-level branch uses the complete _π_ 0 _._ 5 VLA, including its action expert, to propose action chunks. The action-prefix selector is implemented on the high-level planner branch and is invoked at every decision boundary. 

At the beginning of subtask _k_ , the planner autoregressively generates _ck_ from the global instruction, the ordered semantic history _Hk_ = ( _c_ 1 _, . . . , ck−_ 1), and the current observations and state. This history records previously completed subtask commands as an explicit semantic memory. Conditioned on _ck_ , the executor proposes _At_ at each decision boundary. If the selector chooses an action-prefix, its actions are executed before the robot re-observes and reaches the next decision boundary. If it chooses Stop, _ck_ is completed and appended to the history, _Hk_ +1 = ( _Hk, ck_ ), after which the planner generates _ck_ +1 from the updated history, current camera observations, and proprioceptive state. 

### **Anchor-Conditioned Context Encoding** 

The selector context is constructed in three stages: extracting a history-aware subtask anchor _αk_ , pruning visual tokens under anchor guidance, and computing the high-level hidden feature _mt_ . 

**History-Aware Subtask Anchor.** At subtask onset, after the planner generates command _ck_ , we extract a raw anchor 

from the penultimate transformer layer. Let _h_<sup>(</sup> _c_<sup>_ℓ_</sup> _k_<sup>)</sup> _,_ last<sup>denote</sup> the hidden state at the final generated token from layer _ℓ_ . Because this representation is conditioned on the global instruction, semantic subtask history, subtask-onset observations, proprioceptive state, and the complete generated command, it encodes both a persistent memory of the onset environment and a semantic expectation of the subtask goal: 


A single raw anchor captures goal semantics and onset-state memory but lacks awareness of how preceding subtasks have shaped the workspace. To propagate cross-subtask context, we maintain an anchor history pool _Ak_ = _{α_ ˆ1 _, . . . ,_ ˆ _αk−_ 1 _}_ and fuse the current raw anchor with its history via selfattention: 


where [ _·_ ]last extracts the output at the position of ˆ _αk_ . Through self-attention, _αk_ inherits information about which regions have been manipulated in earlier subtasks—context critical for memory-dependent conditions. For the first subtask ( _k_ =1), self-attention reduces to a linear projection. The fused anchor is computed once per subtask and cached throughout. 

**Anchor-Guided Visual Pruning.** The frozen SigLIP (Zhai et al. 2023) encoder produces dense visual tokens _Vt_<sup>(</sup><sup>_i_)</sup> _∈_ R<sup>_N×dv_</sup> for each camera _i_ . We prune to _K_ task-relevant tokens using Grid-Sampler (Feng et al. 2026), a differentiable operator that predicts _K_ normalized 2D coordinates from a conditioning representation and retrieves features via bilinear interpolation. We condition on the subtask anchor _αk_ , directing sampling toward subtask-relevant regions: 


Here, CrossAttn produces an anchor-conditioned visual summary that MLPcoord maps to sampling coordinates **_ξ_**<sup>(</sup> _t_<sup>_i_),</sup> reducing the visual sequence from _N_ to _K_ tokens per camera. **High-Level Hidden Feature Encoding.** The pruned vi= sual tokens are projected into the backbone width ( _V_<sup>¯</sup> _t_<sup>(</sup><sup>_i_)</sup> _V_ ˜ _t_<sup>(</sup><sup>_i_)</sup> _Wv ∈_ R<sup>_K×d_</sup> ), concatenated with proprioceptive-state and subtask-command embeddings, and processed through the first _ℓm_ layers of the high-level VLM backbone with LoRA (Hu et al. 2022) adapters: 


A prefix-attention mask aggregates the multimodal context into _mt ∈_ R<sup>_d_</sup> . Pruning and the shallow pass are recomputed at each decision boundary. 

### **Stop-Aware Action-Prefix Selection** 

At each decision boundary the selector receives the action chunk _At_ proposed by the low-level executor, the cached subtask anchor _αk_ , and the current high-level hidden feature _mt_ . 

It maps these inputs to scores over the unified candidate set and selects either Stop or the highest-scoring action-prefix to execute before re-observing: 


**Unified Candidate Scoring.** The scoring head is a fullattention transformer in which Stop and all action-prefix candidates attend to one another. Each candidate can therefore evaluate its length against the complete proposed chunk, including what later actions would accomplish. The anchor and current high-level hidden feature are projected into context tokens: 


where _Wα, Wm ∈_ R<sup>_dr×d_</sup> project into the scoring space of dimension _dr_ . The Stop candidate uses a learned embedding _e_ 0 _∈_ R<sup>_dr_</sup> , and subtask and multimodal context are supplied by _eα_ and _em_ through self-attention. Each length- _n_ candidate token is initialized from the terminal action of its prefix plus a learned length embedding: 


Full self-attention over the complete token set contextualizes each candidate: 


A scoring layer maps each candidate’s output _hi_ to a scalar _st,i_ = MLPscore( _hi_ ) _∈_ R, _i_ = 0 _, . . . , H_ . The context outputs _hα_ and _hm_ provide conditioning only, and scores are computed from the candidate representations _h_ 0 _, . . . , hH_ . Although _e_ 0 is fixed, self-attention makes the resulting Stop representation context-dependent. Each invocation requires one anchor-guided pruning step, one shallow backbone pass, and one compact scoring-head pass. Anchor extraction is amortized over the entire subtask. Figure 3 visualizes the resulting selection behavior over a full episode. 

**Stop-Aware Ranking Objective.** We optimize the selector with two complementary losses over the same candidate scores: a pairwise ranking loss for relative ordering, and a stop-aware auxiliary loss that strengthens the termination decision. For pairwise ranking, we assign ordinal priorities _ρi_ from offline execution outcomes. Let _τ_ denote the subtask completion boundary and _n_<sup>_⋆_</sup> = _τ − t_ the remaining actions. The priority design encodes three principles: (1) after completion ( _t ≥ τ_ ), Stop ranks highest; (2) before completion, covering prefixes ( _n ≥ n_<sup>_⋆_</sup> ) outrank non-covering ones, and among covering prefixes the one ending closest to the boundary is preferred; (3) for unsuccessful rollouts where _τ_ is undefined, all action-prefixes tie above Stop, encouraging continued exploration (the episode-level horizon bound guarantees safe termination). This construction leverages the temporal structure of successful demonstrations: because expert trajectories reach the subtask boundary efficiently, the alignment _n_<sup>_⋆_</sup> = _τ − t_ provides a natural ordinal supervision 


Figure 3: Stop-aware action-prefix selection over a representative pouring episode. Top: observation frames at decision boundaries with selected prefix length. Bottom: the selected candidate (solid line) over environment steps, with softmax probability shown as a heatmap (darker = higher probability). Replan boundaries (circles) mark subtask transitions. Long prefixes dominate during coarse reach and transport, short prefixes appear during fine alignment, and Stop fires at task completion (green square). 

signal—a standard inductive bias in offline preference learning. During training, we apply uniform random perturbation _τ_<sup>_′_</sup> = _τ_ + ∆ _,_ ∆ _∼U_ ( _−k, k_ ) to boundary annotations, making the ordinal labels robust to annotation noise. The full priority assignment is provided in the supplementary material. 

From the target priorities, we form comparable pairs _Pt_ = _{_ ( _i, j_ ) : _ρi̸_ = _ρj}_ with labels _yij_ = ⊮[ _ρi > ρj_ ]. The ranking loss is: 


Since termination events occur only at subtask boundaries, we add a stop-aware auxiliary to provide stronger gradient signal for the stop decision: 


where _ut_ contrasts the Stop score against a log-sum-exp aggregation of continuation scores, and _yt_<sup>stop</sup> = ⊮[ _t ≥ τ_ ]. The total loss is _L_ = _L_ rank + _λ_ stop _L_ stop. Both objectives shape the same scores, so inference uses the unified rule in Eq. (7); _L_ stop sharpens the stop boundary without defining a separate inference pathway. A short confirmation window filters transient score fluctuations before committing a stop decision. 

## **Experiments** 

**Training.** Both the high-level planner and low-level executor are independently fine-tuned from pre-trained _π_ 0 _._ 5 checkpoints on target manipulation data. The high-level branch is then trained in two phases: we first supervise the planner backbone for subtask command prediction, then freeze both base branches and train the selector modules to jointly optimize stop and dynamic chunk selection via the unified ranking objective. Further implementation details are provided in the supplementary material. 

### **Simulation Experiments** 

**Benchmarks.** Our primary benchmark is RoboCerebra, a long-horizon manipulation benchmark with 1,000 annotated trajectories spanning 100 task variants (avg. 9.1 subtasks, 2,972 steps). Six conditions test complementary capabilities: _Dynamic_ (randomized layouts / changing observations), _Memory_ (subtask-history recall), _Mix_ , and a static _Ideal_ control. We use 60 held-out cases with ten rollouts each (600 episodes total). We additionally evaluate on LIBERO (Liu et al. 2023)(Spatial, Object, Goal, Long; 40 tasks, 100 episodes each) with subtask annotations from LaRA-VLA (Bai et al. 2026). 

**Metrics.** Following the official RoboCerebra protocol, we report _Success Rate_ (SR) as the primary metric, defined as the fraction of evaluation episodes in which the robot completes the full task. _Avg_ denotes the micro-average SR across all six conditions. We additionally report _Stop Acc._ , the agreement between the selector’s stop decisions and annotated subtask boundaries, measuring how precisely the system identifies subtask completion. 

**Baselines.** We compare two paradigms. (i) **Standalone VLA** : OpenVLA-OFT (Kim, Finn, and Liang 2025), SmolVLA (Shukor et al. 2025), and _π_ 0 _._ 5 (Black et al. 2025), each receiving a global task prompt without subtask decomposition. (ii) **Hierarchical VLA** : HPE (Han et al. 2026), the hierarchical planning-execution framework whose results are reported in the original RoboCerebra paper; Mem0 (Chen et al. 2026), a recent open-source hierarchical VLA that we reproduce on RoboCerebra. Two additional SparkVLA variants swap the low-level executor (OpenVLAOFT, SmolVLA) to test generalization. We focus on baselines that are publicly accessible and technically reproducible on RoboCerebra. 

**Results.** Table 1 summarizes results on RoboCerebra. SparkVLA achieves 47.12% average SR, outperforming stan- 

|**Category**|**Method**|**Avg**|**Dyna**|**mic**|**Mem**|**ory**|**Mix**|**Ideal**|
|---|---|---|---|---|---|---|---|---|
||||Ran.|Obs.|Exp.|Exe.|||
||OpenVLA-OFT|1.68|3.95|0.00|0.84|0.96|1.04|3.95|
|Standalone VLA|SmolVLA|2.80|5.90|4.33|0.95|1.51|0.52|5.90|
||_π_0_._5|12.29|11.84|9.09|12.61|10.58|17.71|10.53|
||HPE|16.55|18.63|19.18|9.06|17.83|13.21|21.10|
||Mem-0|20.29|18.42|18.42|25.21|18.27|19.81|19.74|
|Hierarchical VLA|SparkVLA + OpenVLA-OFT|24.15|18.22|20.99|28.56|26.63|27.54|18.22|
||SparkVLA + SmolVLA|25.32|18.22|19.07|30.68|30.26|27.54|19.88|
||**SparkVLA (ours)**|**47.12**|**33.13**|**43.87**|**60.30**|**43.58**|**48.52**|**46.38**|


Table 1: Main comparison on RoboCerebra (SR %). _Avg_ is the micro-average across all conditions. 

|**Method**|**Spa.**|**Obj.**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|
|Diffusion Policy|78.3|92.5|68.3|50.5|72.4|
|OpenVLA|84.7|88.4|79.2|53.7|76.5|
|SmolVLA|93.0|94.0|91.0|77.0|88.8|
|OpenVLA-OFT|97.6|98.4|97.9|94.5|97.1|
|_π_0_._5|**99.4**|**98.2**|97.8|92.4|96.9|
|SparkVLA (ours)|99.2|97.6|**99.2**|**98.0**|**98.5**|


Table 2: Task-level success rate (%) on LIBERO. 

dalone _π_ 0 _._ 5 by 34.83% and the official RoboCerebra baseline (HPE) by 30.57%. SparkVLA also surpasses the independently reproduced Mem-0 by 26.83%, confirming its advantage over recent open-source hierarchical methods. The largest gains appear on _Dynamic Obs._ (+34.78%) and _Memory Exp._ (+47.69%): adaptive shorter prefixes enable more frequent re-observation under changing scenes, while the history-enriched anchor prevents revisiting completed targets. Figure 3 visualizes this behavior. Gains are consistent across executors (+22.47 and +22.52%) over standalone OpenVLA-OFT and SmolVLA), confirming that SparkVLA’s high-level system generalizes to different lowlevel executors. We isolate the contribution of each design choice in the ablation below. 

On LIBERO (Table 2), SparkVLA reaches 98.5% average success. Most suites are near ceiling for strong baselines; the clearest separation is on LIBERO-Long (5.6%), where multistep sequences benefit most from subtask decomposition. 

### **Ablation Studies** 

We ablate chunk-selection method, unified stop integration, context encoding with selector placement, and inference scheduling. All variants use the same RoboCerebra protocol. 

**Chunk selection and stop integration.** Table 3 isolates two design axes. Block (a) fixes an independent stop head and varies only the chunk-selection method: upgrading from a fixed horizon to RLPD (Ball et al. 2023) and AQC (Gireesh, Ju, and Wang 2026) progressively raises SR from 34.26% to 40.92%; our pairwise ranking further yields 42.53%. Notably, Stop Acc. remains near 80% throughout, confirming 

|**Configuration**<br>**SR**|**Stop Acc.**|
|---|---|
|_(a) Chunk selection (independent stop head)_||
|Fixed<br>34.26|79.52|
|RLPD<br>37.62|80.05|
|AQC<br>40.92|80.43|
|Pairwise ranking<br>42.53|80.37|
|_(b) Stop integration (pairwise ranking fixed)_||
|Unified candidate set (ours)<br>**47.12**|**96.65**|


Table 3: Ablation of chunk selection and stop integration. Block (a) varies only the selection method while keeping an independent stop head; block (b) unifies stop into the same candidate set, yielding gains in _both_ SR and Stop Acc. 

that the independent head cannot benefit when the two decisions are decoupled. Block (b) keeps pairwise ranking and unifies Stop into the same candidate set: Stop Acc. jumps from 80.37% to 96.65% (+16.28%, precision 94.3%, recall 98.1%) while SR rises from 42.53% to 47.12% , confirming bidirectional benefit: stop decisions gain from action-prefix context, and prefix selection gains from an accurate termination signal. 

**Context encoding and selector placement.** Table 4 isolates visual-token processing and backbone choice. Progressive improvements from no pruning (40.03%) to spatial pruning (43.46%), raw anchor (45.18%), and the full historyaware anchor (47.12%) confirm that each stage contributes; the history-aware gain (1.94%) comes from resolving spatial ambiguity in memory-dependent conditions. For selector placement, the planner backbone adds 9.84% over the executor backbone, because the planner encodes richer taskprogress and subtask-history context that the executor which trained only for action generation does not retain. 

**Inferencescheduling.** Two runtimeoptimizationsimprove efficiency: caching the subtask command at subtask onset provides a 2 _._ 91 _×_ speedup with no accuracy loss, and invoking the selector only at chunk boundaries (vs. every step) yields 2 _._ 10 _×_ speed while improving Stop Acc. from 93.10% to 96.65% (+3.55 pp), since stationary inter-chunk frames are free of motion blur. With both optimizations, SparkVLA 


Figure 4: Real-world task rollouts. Top to bottom: Shelf Arrangement (6 subtasks), Drawer Restocking (6 subtasks), Tea Preparation (12 subtasks). 

|**Variant**|**SR**|**Stop Acc.**|
|---|---|---|
|_Visual token processing_|||
|No pruning|40.03|88.82|
|Spatial pruning only|43.46|92.16|
|Raw anchor only|45.18|94.03|
|History-aware anchor (ours)|**47.12**|**96.65**|
|_Selector backbone_|||
|Low-level executor|37.28|92.60|
|High-level planner (ours)|**47.12**|**96.65**|


Table 4: Ablation of anchor design and selector placement. 

runs at 4.14 Hz (41.4 action steps/s) vs. 4.68 Hz for standalone _π_ 0 _._ 5, retaining 88% throughput. 

|**Method**|**Arr.**|**Restock**|**Brew Tea**|**Avg.**|
|---|---|---|---|---|
|OpenVLA-OFT|44.0|36.0|10.0|30.0|
|_π_0_._5|64.0|54.0|26.0|48.0|
|SparkVLA (ours)|**78.0**|**74.0**|**56.0**|**69.3**|


Table 5: Real-world success rate (%) on three multi-step tasks. 

execution near contact events and extend it during free-space transport—the same behavioral pattern observed in simulation (Figure 3), confirming that the learned policy transfers qualitatively to physical dynamics. 

## **Conclusion** 

### **Real-World Experiments** 

To validate whether the adaptive prefix selection and stopaware termination transfer to physical hardware, we deploy SparkVLA on an AirbotPlay dual-arm platform with two wrist and one head RGB cameras across three tasks (Figure 4): (1) _Shelf Arrangement_ (6 subtasks), repeated pickand-place requiring persistent spatial binding; (2) _Drawer Restocking_ (6 subtasks), articulated-object interaction with drawer-state tracking; and (3) _Tea Preparation_ (12 subtasks), combining exploration, observation-based confirmation, constrained pouring, and long-horizon chaining. We collect 50 demonstrations per task and evaluate over 50 rollouts with matched initial states. Success requires completing all subtasks and satisfying final-state conditions. 

SparkVLA achieves 69.3% average success, outperforming _π_ 0 _._ 5 by +21.3%(Table 5). The largest margin appears on Tea Preparation (+30.0%), where the 12-subtask horizon magnifies the benefit of explicit subtask memory and stopaware termination. Across all tasks, adaptive prefixes shorten 

We have shown that subtask termination and executionhorizon selection in hierarchical VLA systems are mutually dependent decisions that existing architectures evaluate in isolation, creating a structural information asymmetry at the planning-execution interface. We have proposed SparkVLA, a novel hierarchical VLA framework resolving this by placing both decisions in a single unified candidate set and selecting the highest-scoring option, which is trained entirely from offline ordinal preferences. Experiments on RoboCerebra, LIBERO, and real-robot tasks demonstrate substantial improvements over both standalone and hierarchical baselines, with consistent executor-agnostic transfer confirming that the gains derive from the unified interface design rather than a particular model pairing. The current evaluation focuses on tabletop manipulation with fixed object categories and offline training; extending SparkVLA to open-world settings, online adaptation, and a broader range of planner–executor combinations remains a promising future direction. 

## **References** 

Bai, S.; Lyu, J.; Zhou, W.; Li, Z.; Wang, D.; Xing, L.; Zhao, X.; Wang, P.; Wang, Z.; Chi, C.; Chen, B.; and Zhang, S. 2026. Latent Reasoning VLA: Latent Thinking and Prediction for Vision-Language-Action Models. arXiv:2602.01166. 

Ball, P. J.; Smith, L.; Kostrikov, I.; and Levine, S. 2023. Efficient online reinforcement learning with offline data. In _International Conference on Machine Learning_ , 1577–1594. PMLR. 

Black, K.; Brown, N.; Darpinian, J.; Dhabalia, K.; Driess, D.; Esmail, A.; Equi, M. R.; Finn, C.; Fusai, N.; Galliker, M. Y.; et al. 2025. _\_ pi {_ 0.5 _}_ : a Vision-Language-Action Model with Open-World Generalization. In _9th Annual Conference on Robot Learning_ . 

Black, K.; Brown, N.; Driess, D.; Esmail, A.; Equi, M.; Finn, C.; Fusai, N.; Groom, L.; Hausman, K.; Ichter, B.; Jakubczak, S.; Jones, T.; Ke, L.; Levine, S.; Li-Bell, A.; Mothukuri, M.; Nair, S.; Pertsch, K.; Shi, L. X.; Tanner, J.; Vuong, Q.; Walling, A.; Wang, H.; and Zhilinsky, U. 2026. _π_ 0: A VisionLanguage-Action Flow Model for General Robot Control. arXiv:2410.24164. 

Brohan, A.; Chebotar, Y.; Finn, C.; Hausman, K.; Herzog, A.; Ho, D.; Ibarz, J.; Irpan, A.; Jang, E.; Julian, R.; et al. 2023. Do as i can, not as i say: Grounding language in robotic affordances. In _Conference on robot learning_ , 287– 318. PMLR. 

Bu, Q.; Li, H.; Chen, L.; Cai, J.; Zeng, J.; Cui, H.; Yao, M.; and Qiao, Y. 2025. Towards Synergistic, Generalized, and Efficient Dual-System for Robotic Manipulation. arXiv:2410.08001. 

Chen, T.; Wang, Y.; Li, M.; Qin, Y.; Shi, H.; Li, Z.; Hu, Y.; Zhang, Y.; Wang, K.; Chen, Y.; Wang, H.; Xu, R.; Wu, R.; Mu, Y.; Yang, Y.; Dong, H.; and Luo, P. 2026. RMBench: Memory-Dependent Robotic Manipulation Benchmark with Insights into Policy Design. arXiv:2603.01229. 

Chi, C.; Xu, Z.; Feng, S.; Cousineau, E.; Du, Y.; Burchfiel, B.; Tedrake, R.; and Song, S. 2025. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11): 1684–1704. 

Feng, Y.; Zhao, Z.; Ma, Y.; Xia, C.; Du, C.; Wang, Y.; and Xu, C. 2026. See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model. arXiv:2605.11817. 

Gireesh, N.; Ju, Y.; and Wang, H. 2026. Adaptive Q- Chunking for Offline-to-Online Reinforcement Learning. arXiv:2605.05544. 

Han, S.; Qiu, B.; Liao, Y.; Huang, S.; Gao, C.; Yan, S.; and Liu, S. 2026. Robocerebra: A large-scale benchmark for long-horizon robotic manipulation evaluation. _Advances in Neural Information Processing Systems_ , 38. 

Hu, E. J.; Shen, Y.; Wallis, P.; Allen-Zhu, Z.; Li, Y.; Wang, S.; Wang, L.; Chen, W.; et al. 2022. Lora: Low-rank adaptation of large language models. _Iclr_ , 1(2): 3. 

Jiang, T.; Yuan, T.; Liu, Y.; Lu, C.; Cui, J.; Liu, X.; Cheng, S.; Gao, J.; Xu, H.; and Zhao, H. 2025. Galaxea 

Open-World Dataset and G0 Dual-System VLA Model. arXiv:2509.00576. 

Kim, M. J.; Finn, C.; and Liang, P. 2025. Fine-Tuning VisionLanguage-Action Models: Optimizing Speed and Success. arXiv:2502.19645. 

Kim, M. J.; Pertsch, K.; Karamcheti, S.; Xiao, T.; Balakrishna, A.; Nair, S.; Rafailov, R.; Foster, E. P.; Sanketi, P. R.; Vuong, Q.; et al. 2025. OpenVLA: An Open-Source VisionLanguage-Action Model. In _Conference on Robot Learning_ , 2679–2713. PMLR. 

Liang, Y.; Wang, X.; Wang, K.; Wang, S.; Peng, X.; Chen, H.; Chua, D. K. H.; and Vadakkepat, P. 2026. Adaptive Action Chunking at Inference-time for Vision-Language-Action Models. arXiv:2604.04161. 

Liu, B.; Zhu, Y.; Gao, C.; Feng, Y.; Liu, Q.; Zhu, Y.; and Stone, P. 2023. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36: 44776–44791. 

Liu, S.; Wu, L.; Li, B.; Tan, H.; Chen, H.; Wang, Z.; Xu, K.; Su, H.; and Zhu, J. 2025. Rdt-1b: a diffusion foundation model for bimanual manipulation. In _International Conference on Learning Representations_ , volume 2025, 29982– 30009. 

Liu, Y.; Zhu, J.; Mo, Y.; Li, G.; Cao, X.; Jin, J.; Shen, Y.; Li, Z.; Yu, T.; Yuan, W.; Ding, F.; and Lourentzou, I. 2026. PALM: Progress-Aware Policy Learning via Affordance Reasoning for Long-Horizon Robotic Manipulation. arXiv:2601.07060. 

NVIDIA; :; Bjorck, J.; Castañeda, F.; Cherniadev, N.; Da, X.; Ding, R.; Fan, L. J.; Fang, Y.; Fox, D.; Hu, F.; Huang, S.; Jang, J.; Jiang, Z.; Kautz, J.; Kundalia, K.; Lao, L.; Li, Z.; Lin, Z.; Lin, K.; Liu, G.; Llontop, E.; Magne, L.; Mandlekar, A.; Narayan, A.; Nasiriany, S.; Reed, S.; Tan, Y. L.; Wang, G.; Wang, Z.; Wang, J.; Wang, Q.; Xiang, J.; Xie, Y.; Xu, Y.; Xu, Z.; Ye, S.; Yu, Z.; Zhang, A.; Zhang, H.; Zhao, Y.; Zheng, R.; and Zhu, Y. 2025. GR00T N1: An Open Foundation Model for Generalist Humanoid Robots. arXiv:2503.14734. 

Shin, Y.; Chae, J.; Kim, S.; Park, J.; and Sung, Y. 2026. Adaptive Action Chunking via Multi-Chunk Q Value Estimation. arXiv:2605.10044. 

Shukor, M.; Aubakirova, D.; Capuano, F.; Kooijmans, P.; Palma, S.; Zouitine, A.; Aractingi, M.; Pascal, C.; Russi, M.; Marafioti, A.; Alibert, S.; Cord, M.; Wolf, T.; and Cadene, R. 2025. SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics. arXiv:2506.01844. 

Team, O. M.; Ghosh, D.; Walke, H.; Pertsch, K.; Black, K.; Mees, O.; Dasari, S.; Hejna, J.; Kreiman, T.; Xu, C.; Luo, J.; Tan, Y. L.; Chen, L. Y.; Sanketi, P.; Vuong, Q.; Xiao, T.; Sadigh, D.; Finn, C.; and Levine, S. 2024. Octo: An Open-Source Generalist Robot Policy. arXiv:2405.12213. Torne, M.; Pertsch, K.; Walke, H.; Vedder, K.; Nair, S.; Ichter, B.; Ren, A. Z.; Wang, H.; Tang, J.; Stachowicz, K.; Dhabalia, K.;Equi,M.;Vuong,Q.;Springenberg,J.T.;Levine,S.;Finn, C.; and Driess, D. 2026. MEM: Multi-Scale Embodied Memory for Vision Language Action Models. arXiv:2603.03596. Yang, T.; Chen, G.; Chen, Y.; Liang, Z.; Liu, Y.; Chen, Z.; Xu, C.; Liang, H.; Pang, J.; Mu, Y.; and Luo, P. 2026. HiVLA: 

A Visual-Grounded-Centric Hierarchical Embodied Manipulation System. arXiv:2604.14125. 

Zhai, X.; Mustafa, B.; Kolesnikov, A.; and Beyer, L. 2023. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , 11975–11986. 

Zhang, J.; Guo, Y.; Chen, X.; Wang, Y.-J.; Hu, Y.; Shi, C.; and Chen, J. 2025. HiRT: Enhancing Robotic Control with Hierarchical Robot Transformers. In _Conference on Robot Learning_ , 933–946. PMLR. 

Zhao, T.; Kumar, V.; Levine, S.; and Finn, C. 2023. Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. _Robotics: Science and Systems XIX_ . 

Zhao, Y.; Bogdanovic, M.; Sohal, A.; Tao, L.; Darvish, K.; Aspuru-Guzik, A.; Shkurti, F.; and Garg, A. 2026. Dynamic Execution Horizon Prediction for Chunk-based Robot Policies. arXiv:2606.11408. 

Zitkovich, B.; Yu, T.; Xu, S.; Xu, P.; Xiao, T.; Xia, F.; Wu, J.; Wohlhart, P.; Welker, S.; Wahid, A.; Vuong, Q.; Vanhoucke, V.; Tran, H.; Soricut, R.; Singh, A.; Singh, J.; Sermanet, P.; Sanketi, P. R.; Salazar, G.; Ryoo, M. S.; Reymann, K.; Rao, K.; Pertsch, K.; Mordatch, I.; Michalewski, H.; Lu, Y.; Levine, S.; Lee, L.; Lee, T.-W. E.; Leal, I.; Kuang, Y.; Kalashnikov, D.; Julian, R.; Joshi, N. J.; Irpan, A.; brian ichter; Hsu, J.; Herzog, A.; Hausman, K.; Gopalakrishnan, K.; Fu, C.; Florence, P.; Finn, C.; Dubey, K. A.; Driess, D.; Ding, T.; Choromanski, K. M.; Chen, X.; Chebotar, Y.; Carbajal, J.; Brown, N.; Brohan, A.; Arenas, M. G.; and Han, K. 2023. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. In _7th Annual Conference on Robot Learning_ . 

## **Supplementary Material** 

This document supplements the main paper with the details needed to interpret and reproduce its central claims.It covers the complete ordinal supervision, paper-aligned implementation settings, closed-loop inference, common evaluation controls, physical-system protocol, and representative simulation scenes. Definitions and results already given in the main paper are not repeated. 

## **Complete Ordinal Supervision** 

### **Priority Assignment** 

The main paper gives the principles used to supervise the unified candidate set. Here we provide the complete assignment, including trajectory-end masking and failure rollouts. Let _T_ be the number of recorded actions in a training trajectory, and define candidate validity by 


For compactness, write succ and fail for successful and unsuccessful trajectories. For a successful trajectory, we perturb its annotated completion boundary during training as _τ_<sup>_′_</sup> = _τ_ + ∆, where _k_ = 2 and ∆ is sampled uniformly from _{−_ 2 _, −_ 1 _,_ 0 _,_ 1 _,_ 2 _}_ , and set _n_<sup>_⋆_</sup> = _τ_<sup>_′_</sup> _− t_ . The Stop priority is 


For each valid action-prefix candidate _n ∈{_ 1 _, . . . , H}_ , 


Thus, after completion, Stop outranks every action-prefix. Before a reachable boundary, every covering prefix outranks every non-covering prefix, and lower overshoot is preferred among covering prefixes. If the boundary lies beyond the proposed chunk ( _n_<sup>_⋆_</sup> _> H_ ), longer prefixes receive higher priority. In an unsuccessful rollout, all action-prefixes tie above Stop; such samples supervise continuation but do not impose an arbitrary preferred execution length. 

Only valid candidates with unequal priorities form a training pair: 


The strict upper-triangular construction in Eq. (18) includes each unordered comparison once. Consequently, tied actionprefixes in unsuccessful rollouts do not enter the pairwise loss, whereas their Stop-versus-prefix comparisons remain active. Unsuccessful-rollout ranking samples are assigned a weight of 0 _._ 1. Algorithm 1 gives the complete procedural construction used by the released preprocessing code. 

**Algorithm 1** Ordinal supervision for unified candidates 

- **Input** : decision step _t_ , trajectory metadata ( _T, q, τ_ ) (with _τ_ defined only if _q_ = 1), horizon _H_ **Output** : priorities **_ρ_** , validity **v** , Stop label _y_<sup>stop</sup> , weights _w_<sup>rank</sup> _, w_<sup>stop</sup> , pair set _Pt_ 1: Initialize **_ρ_** _←_ **0** , **v** _←_ **0** , and _v_ 0 _←_ 1 2: **for** _n_ = 1 _, . . . , H_ **do** 3: _vn ←_ ⊮[ _t_ + _n −_ 1 _< T_ ] 4: **end for** 5: **if** _q_ = 0 **then** 6: _ρ_ 0 _←_ 0 and _ρn ←_ 1 for each valid _n ≥_ 1 7: _y_<sup>stop</sup> _←_ 0, _w_<sup>rank</sup> _←_ 0 _._ 1, _w_<sup>stop</sup> _←_ 1 _._ 5 8: **else** 9: Sample ∆ uniformly from _{−_ 2 _, −_ 1 _,_ 0 _,_ 1 _,_ 2 _}_ 

- 10: _τ_<sup>_′_</sup> _← τ_ + ∆ and _n_<sup>_⋆_</sup> _← τ_<sup>_′_</sup> _− t_ 11: _w_<sup>rank</sup> _←_ 1 12: **if** _t ≥ τ_<sup>_′_</sup> **then** 13: _ρ_ 0 _← H_ + 1 and _ρn ← H − n_ + 1 for each valid _n ≥_ 1 

- 14: _y_<sup>stop</sup> _←_ 1 and _w_<sup>stop</sup> _←_ 3 15: **else** 16: _ρ_ 0 _←_ 0 and _y_<sup>stop</sup> _←_ 0 17: _w_<sup>stop</sup> _←_ 3 if _n_<sup>_⋆_</sup> _≤_ 80, and 1 otherwise 18: **for** each valid _n_ = 1 _, . . . , H_ **do** 19: **if** _n_<sup>_⋆_</sup> _> H_ or _n < n_<sup>_⋆_</sup> **then** 20: _ρn ← n_ 21: **else** 22: _ρn ←_ 2 _H −_ ( _n − n_<sup>_⋆_</sup> ) 23: **end if** 24: **end for** 25: **end if** 

26: **end if** 27: _Pt ←{_ ( _i, j_ ) _|_ 0 _≤ i < j ≤ H, vivj_ = 1 _, ρi̸_ = _ρj}_ 28: **return** **_ρ_** _,_ **v** _, y_<sup>stop</sup> _, w_<sup>rank</sup> _, w_<sup>stop</sup> _, Pt_ 

### **Stop-Aware Optimization** 

The training objective contains the two terms stated in the main paper: the pairwise relative-ranking loss and the stopaware binary loss, both applied to the same _H_ + 1 candidate scores. To counter the sparsity of completion boundaries without changing the inference rule, Stop-positive samples and near-boundary Stop-negative samples receive weight 3 _._ 0; negative samples from unsuccessful rollouts receive weight 1 _._ 5; all remaining samples use unit weight. We set _λ_ stop = 1 in _L_ = _L_ rank + _λ_ stop _L_ stop. The pairwise term includes every valid Stop–action-prefix comparison with unequal priority and therefore directly supervises the score ordering used at inference. The stop-aware term adds a boundary-focused aggregate contrast over the same scores. At inference, the selector applies the unified comparison rule from the main paper to this score vector, so the auxiliary term strengthens boundary supervision while preserving a single decision pathway. Algorithm 2 expands the minibatch computation. In particular, it does not introduce an additional prediction head or optimization term. 

|**Alg**|**orithm 2**Two-loss optimization of the unified selector|
|---|---|
|**Inp**|**ut**: minibatch of selector inputs and Algorithm 1 targets|
|**Par**|**ameter**:_λ_stop = 1|
|**Ou**|**tput**:_L_|
|1:|Initialize_R, ZR, S, ZS ←_0|
|2:|**for**each sample_b_= 1_, . . . , B_ **do**<br><br>|
|3:|**s**_b ←f_ <sup>sel</sup><br>_ϕ,θ_<sup>(</sup><sup>_At, αk, mt_)</sup>|
|4:|_Pb ←{_(_i, j_)_|_0_≤i < j ≤H, vivj_ = 1_, ρi̸_ =_ρj}_|
|5:|_̸_<br>**for**each(_i, j_)_∈Pb_ **do**|
|6:|_yij ←_⊮[_ρi > ρj_]<br>|
|7:|_R ←R_+_w_<sup>rank</sup><br>_b_<br>BCE(_sb,i −sb,j, yij_)|
|8:|_ZR ←ZR_+_w_<sup>rank</sup><br>_b_|
|9:|**end for**<br>|
|10:|_ub ←sb,_0_−_log <sup>�</sup><sup>_H_</sup><br>_n_=1 <sup>exp(</sup><sup>_sb,n_)</sup><br><br>|
|11:|_S ←S_+_w_<sup>stop</sup><br>_b_<br>BCE(_ub, y_<sup>stop</sup><br>_b_<br>)|
|12:|_ZS ←ZS_ +_w_<sup>stop</sup><br>_b_|
|13:|**end for**|
|14:|_L_rank _←R/_max(_ZR,_1)|
|15:|_L_stop _←S/_max(_ZS,_1)|
|16:|_L ←L_rank+_λ_stop_L_stop|
|17:|Update the LoRA, context-encoding, and scoring param-<br>eters|
|18:|**return**_L_|


## **Simulation Training Details** 

### **Model Configuration** 

Table 6 lists the selector-specific settings that are omitted from the main paper for space. The SigLIP visual encoder and the base parameters of both _π_ 0 _._ 5 branches are frozen during selector training. Trainable parameters comprise the high-level LoRA adapters, anchor projection and history attention, coordinate-prediction module, context projections, and unified scoring head. 

### **Training Data Construction** 

Selector training combines 6,660 demonstration records and 5,630 policy-rollout records, from which 2,034,310 decision samples are constructed. The mixed sampler draws 30% demonstration samples and 70% rollout samples. For a successful demonstration segment, _τ_ is the annotated end of the completed subtask; for a successful policy rollout, it is the recorded completion step. Failed rollouts have no completion boundary and use the last case of Eq. (17). We retain at most 80 frames after a successful boundary and cap failed rollouts at 300 frames. These failure samples expose the selector to off-demonstration states while avoiding false Stop supervision. 

### **Optimization and Compute** 

The planner and executor are initialized independently from the pre-trained _π_ 0 _._ 5 VLA and optimized for subtaskcommand generation and action-chunk prediction, respectively. The autoregressive subtask-generation phase runs for 2,000 optimizer steps. Starting from that planner, selector training runs for 20,000 optimizer steps in bfloat16 with gradient checkpointing. We use AdamW, a global batch size of 

|**Component**|**Setting**|
|---|---|
|Action-chunk horizon_H_|50|
|Visual tokens per camera_K_|32|
|Input image resolution|224_×_224|
|Anchor width_d_|2,048|
|High-level depth_ℓm_|8 layers|
|Anchor source_ℓ_deep|penultimate layer|
|Scoring width_dr_|1,024|
|Scoring transformer|2 layers, 8 heads|
|Scoring feed-forward width|4,096|
|Scoring dropout|0|
|Coordinate context|4 queries, width 512|
|LoRA rank / scaling|16 / 16|
|LoRA layers|high-level layers 1–<br>8|
|State normalization|quantile|


Table 6: Selector and context-encoding configuration. 

256, weight decay 0 _._ 01, 1,000 linear warmup steps, gradientnorm clipping at 1 _._ 0, and random seed 7. Learning rates are 3 _×_ 10<sup>_−_5</sup> for LoRA parameters, 3 _×_ 10<sup>_−_4</sup> for the scoring and projection heads, and 1 _×_ 10<sup>_−_4</sup> for the visual coordinate module. Checkpoints are saved every 1,000 optimizer steps. 

The reported selector run uses four NVIDIA A100 GPUs with 80 GB memory each and an Intel Xeon Platinum 8470Q host under Ubuntu 24.04. The software environment uses Python 3.11, PyTorch 2.1.2, and CUDA 11.8; the effective global batch is distributed with NCCL. The complete package-level dependency versions are recorded in the Code and Data Supplement. 

## **Closed-Loop Inference Details** 

### **Execution Procedure** 

The following procedure makes explicit when each high- and low-level operation is invoked. It is a procedural restatement of the model interface, not an additional inference module. 

1. Initialize the ordered semantic history as _H_ 1 = () and acquire the current camera observations and proprioceptive state. 

2. At the onset of subtask _k_ , autoregressively generate command _ck_ from the global instruction, _Hk_ , and the current robot observation. Extract and cache the history-aware anchor _αk_ . 

3. At decision boundary _t_ , query the low-level executor for action chunk _At_ and recompute the anchor-conditioned high-level hidden feature _mt_ . 

4. Score [Stop _,_ 1 _, . . . , H_ ] jointly. If an action-prefix _n_ is selected, execute its first _n_ actions, re-observe, and return to Step 3. 

5. When a Stop decision is committed, append _ck_ to the history, set _Hk_ +1 = ( _Hk, ck_ ), and return to Step 2 for the next subtask, unless the configured global termination condition ends the episode. 

**Algorithm 3** SparkVLA closed-loop inference 

|**Inp**|**ut**: global instruction_g_, planner, executor, unified selec-|
|---|---|
|tor,|horizon_H_|
|**Ou**|**tput**: executed task trajectory|
|1: <br>|Initialize semantic history _H_1 _←_(), anchor history<br>_A_1 _←_(), and_k ←_1<br>|
|2:|Acquire current observations_{I_<sup>(</sup><sup>_i_)</sup><br>_t _<sup>_}C_</sup><br>_i_=1 <sup>and propriocep-</sup><br>tive state_st_|
|3:|**while**the global termination criterion is not satisfied**do**|
|4:|Autoregressively<br>generate<br>_ck_<br>_←_<br><br>|
||_f_ <sup>plan</sup><br>_ϕ_<br>(_g, Hk, {I_<sup>(</sup><sup>_i_)</sup><br>_t _<sup>_}, st_)</sup><br>|
|5:|ˆ_αk ←_MLPanchor(_h_<sup>(</sup><sup>_ℓ_deep)</sup><br>_ck,_last<sup>)</sup>|
|6:|_αk ←_[SelfAttn(_Ak,_ˆ_αk_)]lastand cache_αk_|
|7:|**while**the current subtask is active**do**<br>|
|8:|Propose action chunk_At ←π_L(_ck, {I_<sup>(</sup><sup>_i_)</sup><br>_t _<sup>_}, st_)</sup>|
|9:|Compute anchor-guided visual tokens and shallow<br>high-level feature_mt_<br><br>|
|10:|**s**_t ←f_ <sup>sel</sup><br>_ϕ,θ_<sup>(</sup><sup>_At, αk, mt_)</sup>|
|11:|Mask any action-prefix candidate not provided as<br>valid by the executor|
|12:|ˆ_nt ←_arg max_i∈{_0_,...,H} st,i_|
|13:|**if** ˆ_nt_ = 0**then**<br>|
|14:|_Hk_+1 _←_(_Hk, ck_)and_Ak_+1 _←_(_Ak,_ˆ_αk_)|
|15:|_k ←k_+ 1and exit the inner loop|
|16:|**else**|
|17:|Execute the first ˆ_nt_actions of_At_<br>|
|18:|Re-observe_{I_<sup>(</sup><sup>_i_)</sup><br>_t _<sup>_}C_</sup><br>_i_=1 <sup>and</sup><sup>_st_ at the next decision</sup><br>boundary|
|19:|**end if**|
|20:|**end while**|
|21:|**end while**|
|22:|**return**the executed trajectory|


The selector is invoked only at decision boundaries; neither the planner nor selector interrupts an action-prefix between two such boundaries. This scheduling preserves a closed-loop observation after every selected prefix while amortizing high-level computation. Algorithm 3 summarizes the full execution loop and makes explicit that semantic and anchor histories are updated only after Stop is selected. 

## **Evaluation Controls** 

For each benchmark, all reproduced methods receive the same task instructions and observation streams and use common action interfaces, held-out evaluation cases, rollout budget, episode horizon, reset distribution, and success criteria. Externally reported results are included only when they follow the official benchmark protocol and are identified as such in the main paper. A common metric definition is applied to the resulting episode outcomes. Within each ablation block, only the named design factor is changed; the remaining data, training, checkpoint-selection, and evaluation settings are retained. These controls make the main comparison an evaluation of complete systems while allowing the ablation blocks to isolate individual SparkVLA design choices. 

Locally reproduced baselines follow a common taskspecific fine-tuning protocol with matched data volume, training compute, and hyperparameter-selection budgets. Planner access and model inputs are kept consistent within controlled comparisons and otherwise follow the corresponding method configuration. Model selection is performed independently of the evaluation episodes. 

Training uses seed 7, while evaluation uses the distinct base seed 2027. A deterministic per-episode seed is derived from the benchmark, condition, case identifier, and rollout index, and is applied to Python, NumPy, PyTorch, and all visible CUDA devices. For physical trials, the seed controls trial ordering; task-specific reset ranges define the initial states. The derivation function and machine-readable seed configuration are included in the Code and Data Supplement. 

## **RoboCerebra Task Visualizations** 

Figure 5 shows representative initial scenes from the six RoboCerebra conditions used in the main paper. The columns preserve the table order in the main paper; the five rows show different held-out task instances and layouts. The gallery illustrates the changes in object placement, distractors, containers, and scene configuration covered by the benchmark without repeating its metric or split definitions. 

## **Real-World Experimental Details** 

### **Inference Platform and Control Stack** 

The real-world evaluation uses a fixed tabletop manipulation platform with RGB observation streams and proprioceptive feedback. A common local deployment stack provides perception, model inference, and robot control for every compared method. Thus, sensing and control conditions remain fixed while only the evaluated policy changes. Action commands are streamed at approximately 20 Hz, corresponding to 50 ms per action step. Model-side planning and selection support approximately 4.14 boundary updates per second, as reported in the main paper; the realized selector invocation rate is lower and varies with the selected action-prefix length because the selector runs only at decision boundaries. All compared methods use the same action-command rate. 

### **Physical Task Definitions** 

The physical evaluation contains three ordered long-horizon tasks. _Shelf Arrangement_ contains six subtasks: pick up the cola and place it in the left shelf compartment; pick up the cup and place it in the center compartment; then pick up the small block and place it in the right compartment. _Drawer Restocking_ contains six subtasks: open the top drawer, store the block, close the top drawer, open the middle drawer, store the cup, and close the middle drawer. _Tea Preparation_ contains twelve subtasks: open the top drawer, verify that it is empty, close it, open the middle drawer, retrieve the tea bag, place it in the cup, close the middle drawer, pick up the water bottle, pour the bottle contents into the cup, set down the bottle, pick up the prepared cup, and place it on the serving tray. These ordered sequences define the subtask histories and completion events used in data segmentation 


Figure 5: Representative RoboCerebra simulation scenes. From left to right, the columns show Dynamic Randomization, Dynamic Observation, Memory Exploration, Memory Execution, Mix, and Ideal; rows contain distinct held-out task instances. 

and evaluation. The task-level language retains the semantic terms _water bottle_ and _pour water_ . In the physical setup, however, the bottle contains white plastic beads, which serve as a safe and repeatable dry surrogate for water. The substitution preserves the manipulation sequence relevant to this task: grasping and transporting the bottle, aligning it above the cup, controlling its orientation during transfer, returning it upright, and placing it back on the table. The same bottle contents and task setup are used for all compared methods. 

### **Data Collection and Reset Protocol** 

Demonstrations are collected with the global instructions and predefined subtask sequences used by the corresponding tasks. Each trajectory is segmented at subtask-completion events, and the resulting boundary labels are used only for offline supervision. Each rollout begins from a matched taskspecific initial state; object poses are randomized only within the corresponding evaluation range. A rollout is reset after success, violation of a safety bound, loss of an object from the workspace, or expiration of the task horizon. Operator intervention terminates the trial and is counted as a failure. 

### **Final-State Criteria and Safety** 

For Shelf Arrangement, success requires the cola, cup, and block to be stable in the left, center, and right shelf compartments, respectively, without a drop or placement beyond a compartment edge. For Drawer Restocking, the block and cup must be fully contained in the top and middle drawers, respectively, and both drawers must finish with less than 2 cm residual opening. For Tea Preparation, the system must verify the empty top drawer, retrieve the tea bag from the middle drawer, place it in the cup, transfer the prescribed amount of white plastic beads from the bottle into the cup without substantial scattering outside the cup, return the bottle to the table, and leave the prepared cup stably on the serving tray. The transfer outcome is checked against the same predefined target level in every trial. 

No liquid is used in the physical evaluation. The pouring task uses a small quantity of white plastic beads. This dry surrogate avoids liquid contact with the equipment and permits consistent resets while retaining the target-directed transfer operation. A shallow containment tray collects any scattered beads. Robot speed and gripper force are capped, and drawers have mechanical travel limits. A physical emergency stop remains accessible; any intervention terminates 

and fails the rollout. The safety mechanisms operate independently of SparkVLA’s task-state estimation. 

