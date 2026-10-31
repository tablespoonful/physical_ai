---
title: "TacMamba: A Tactile History Compression Adapter Bridging Fast Reflexes and Slow VLA Reasoning"
date: "2026-03-02"
authors: "Zhenan Wang; Yanzhe Wang; Meixuan Ren; Peng Li; Yang Liu; Yifei Nie"
url: https://arxiv.org/abs/2603.01700
pdf: https://arxiv.org/pdf/2603.01700
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.01700)** / [論文ページ](https://arxiv.org/abs/2603.01700)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **TacMamba: A Tactile History Compression Adapter Bridging Fast Reflexes and Slow VLA Reasoning** 

Zhenan Wang<sup>1</sup><sup>_,_2</sup><sup>_,†_</sup> , Yanzhe Wang<sup>1</sup><sup>_,†_</sup> , Meixuan Ren<sup>1</sup><sup>_,_3</sup> , Peng Li<sup>2</sup> , Yang Liu<sup>1</sup> , Yifei Nie<sup>1</sup><sup>_,_2</sup> , Limin Long<sup>2</sup> , Yun Ye<sup>2</sup> , Xiaofeng Wang<sup>2</sup> , Zhen Zhu<sup>2</sup> and Huixu Dong<sup>1</sup><sup>_,∗_</sup> 

**_Abstract_ — In visually ambiguous manipulation such as detecting button’s “click” tactile feedback is often the sole source of ground truth. However, fusing tactile data poses a significant challenge due to a spatiotemporal mismatch: tactile perception requires high-frequency processing with long-horizon memory (System 1), whereas visual policies operate at low control frequencies (System 2). Existing architectures struggle to bridge this gap: Transformers are computationally prohibitive for high-frequency loops (** _>_ 100 **Hz), while LSTMs suffer from forgetting over extended interaction histories. In this paper, we introduce TacMamba, a hierarchical architecture that aligns high-bandwidth tactile reflexes with low-frequency visual planning. Our approach comprises three core contributions: (1) a custom high-frequency tactile interface designed for flexible integration; (2) a Mamba-based Tactile History Compressor that encodes continuous force history into a compact state with** _O_ (1) **inference latency (0.45 ms), enabling plug-and-play fusion with VLA models without joint pre-training and (3) a TactileGuided Dual-Stage Training strategy that leverages temporal discrimination for self-supervised representation learning and phase-uniform sampling to mitigate data sparsity. Experiments on discrete counting and implicit state switching demonstrate that TacMamba achieves 100% success rates, significantly outperforming the visual-only** _π_ 0 _._ 5 **baseline, while strictly satisfying hard real-time constraints.** 

## I. INTRODUCTION 

Human dexterity synergizes slow, semantic planning (System 2) with fast, reflexive reactions (System 1) [1]. While recent Vision-Language-Action (VLA) models have demonstrated proficiency in System 2 capabilities [2], [3], [4], [5], [6], [7], they struggle to emulate the reflexive nature of System 1. The fundamental bottleneck lies in a frequency mismatch: existing architectures cannot efficiently process high-frequency tactile history, creating a disconnect between high-level visual reasoning and low-level physical interaction. 

This discrepancy is critical in scenarios characterized by visual ambiguity, such as detecting a subtle button “click” or identifying stripped threads [8], [9], [10]. In such cases, tactile feedback serves as the indispensable ground truth. Unlike vision, which captures discrete snapshots, tactile perception relies on the temporal profile of contact—continuous force curves and transient vibrations. Consequently, robust manipulation necessitates a model with long-term temporal memory to distinguish successful actuation from failure based on 

> _†_ These authors contributed equally to this work. 

> _∗_ Corresponding author. 

> 1 Zhejiang University, Hangzhou, China 

> 2 GigaAI, Beijing, China 

> 3 Harbin Institute of Technology, Harbin, China 

interaction history rather than instantaneous state [11], [12]. However, modeling this extended history imposes a prohibitive computational burden. High-resolution sensors stream data at frequencies exceeding 100Hz [13], [14]. Processing merely two seconds of history with standard Transformers generates hundreds of tokens [15], causing computational costs to scale quadratically ( _O_ ( _N_<sup>2</sup> )). This latency bottlenecks the high-frequency control loop, effectively limiting the “Fast” system to the response time of the “Slow” visual planner. Conversely, traditional RNNs (e.g., LSTMs) offer fast inference but suffer from catastrophic forgetting, failing to retain fine-grained physical details over thousands of time steps [16], [17], [18]. 

Beyond architectural limits, multi-modal training poses two severe bottlenecks. First, integrating high-frequency tactile streams into massive VLAs via end-to-end co-training is computationally prohibitive [3], [2] and risks catastrophic forgetting of established semantic priors [9], [8]. Second, contact-rich tasks suffer from extreme temporal data imbalance [19]. Critical interaction events, such as button “snap-throughs” (Fig. 1), are highly transient ( _<_ 5% of a trajectory) [20]. Standard uniform sampling drowns these vital signals in trivial reaching motions, leading to policy failures precisely at the moment of contact. 

To resolve these spatiotemporal and data challenges, we introduce **TacMamba** , a unified hardware-software framework. As illustrated in Fig. 1, TacMamba bridges the frequency gap through an asynchronous architecture: the tactile encoder (System 1) performs continuous streaming inference at 100Hz to update a compressed hidden vector of tactile history, which is then queried on-demand by the low-frequency ( _∼_ 1Hz) VLA planner (System 2). Our contributions are three fold: 

(1) We propose TacMamba, the first hierarchical architecture that aligns high-bandwidth tactile reflexes (100Hz) with lowfrequency visual reasoning ( _∼_ 1Hz) without downsampling. Unlike prior methods that discard high-frequency data, our design enables lossless, real-time processing of micro-scale contact dynamics. 

(2) A novel Mamba-based tactile encoder [21], [22] that resolves the accuracy-latency trade-off. By achieving constanttime _O_ (1) inference without sacrificing perception fidelity, TacMamba significantly outperforms the Transformer baselines in speed. This represents the first architecture capable of processing ultra-long tactile histories within the hard realtime constraints of embedded hardware. 

(3) We propose a robust plug-and-play two-stage learning 


Fig. 1. **The TacMamba System Architecture.** The framework bridges the spatiotemporal discrepancy between high-speed reflexes and low-frequency reasoning. **Left (System 1):** The tactile encoder processes 1D force streams at 100Hz using Mamba Models, recursively updating the hidden state _ht_ in real-time. **Right (System 2):** This compressed hidden state _ht_ is projected and asynchronously injected as a soft prompt into the low-frequency ( _∼_ 1Hz) Vision-Language-Action (VLA) planner. 

framework that circumvents the need for expensive VLA joint pre-training. This comprises: (i) self-supervised pretraining via Ternary Temporal Discrimination to independently capture causal contact dynamics, and (ii) efficient VLA fine-tuning augmented with a novel Phase-Uniform Sampling strategy. This approach resolves the sparsity of critical interaction frames and seamlessly injects tactile history into the VLA, improving data efficiency multiple times. 

## II. RELATED WORK 

## _A. Temporal model in VLA_ 

Recent advances in VLA models have demonstrated remarkable success in equipping robots with high-level semantic reasoning capabilities (System 2) [3], [4], [2]. Building upon foundation models, recent work has further enhanced the generalization of VLAs in open-world scenarios [5], [6]. Furthermore, to address the challenge of state aliasing in long-horizon tasks, recent frameworks have integrated memory mechanisms. For instance, MAP-VLA [12] constructs a memory bank from historical demonstrations using retrievalaugmented prompting, while MemoryVLA [11] maintains a perceptual-cognitive memory. However, these memoryaugmented VLAs suffer from a critical limitation: they operate exclusively at the low control frequency ( _∼_ 1-10Hz) of the visual planner. Because their memory banks rely entirely on low-frequency visual or proprioceptive states, they inherently lack the high-bandwidth physical feedback 

required for real-time reflexive adjustments, remaining firmly constrained within the “Slow” System 2 paradigm. 

## _B. Tactile-Augmented Robotic Manipulation_ 

Recognizing the limitations of purely visual models in contact-rich tasks, recent works have attempted to integrate tactile and force modalities into VLA architectures. ForceVLA [9] introduces a force-aware Mixture-of-Experts module to integrate 6-DoF force feedback during action decoding, while OmniVTLA [8] employs a semantic-aligned tactile encoder to process multi-modal sensory inputs. Despite these advancements, existing tactile VLAs are fundamentally bottlenecked by their synchronous architectures. Because they feed tactile or force tokens directly into the heavy VLA backbone, the sensory processing is strictly constrained by the VLA’s low inference speed. Consequently, these models can only utilize instantaneous tactile snapshots at a drastically reduced frequency, failing to maintain a continuous, high-frequency historical memory. This lossy integration discards critical high-frequency transients (e.g., sudden micro-slips or the snap-through vibrations of a button). In contrast, TacMamba completely decouples the sensory reflex from visual planning, enabling continuous, lossless encoding of 100Hz tactile history without being bottlenecked by the low-frequency VLA. 

## _C. Efficient Long-Sequence Modeling_ 

Modeling extensive historical sequences is a fundamental challenge in deep learning. While Transformers have been 


Fig. 2. **System Overview.** (a) Modular morphology-based tactile fingertip design, where an integrated compliant contact body supports both fingertip and fingerpad interactions and mechanically projects distributed contacts onto a single-axis force sensor; lateral side panels protect the internal structure, and a reconfigurable dual-clamp interface enables attachment to generic parallel grippers. (b) FEM-based characterization of force projection, showing peak contact pressure versus applied load for fingertip and fingerpad contacts, together with (c) representative visualizations of total deformation, equivalent (von Mises) stress, and contact pressure. 

adapted for long-term time-series forecasting [23], [24], their _O_ ( _N_<sup>2</sup> ) latency renders them unviable for high-frequency embedded control loops. Conversely, traditional Recurrent Neural Networks (RNNs) offer fast inference but are notoriously plagued by catastrophic forgetting over thousands of time steps [16], [17]. Recently, Structured State Space Models (SSMs) [22] and their selective variant, Mamba [21], have emerged as a paradigm shift. By maintaining a compressed hidden state, Mamba achieves linear-time sequence modeling and strict _O_ (1) inference latency [25]. Inspired by this, TacMamba pioneers the application of Mamba to highfrequency tactile streams, effectively resolving the memorylatency trade-off and enabling lossless frequency alignment between System 1 and System 2. 

## III. HARDWARE SYSTEM 

TacMamba is a unified hardware–software system that enables high-frequency tactile reflexes to inform low-frequency VLA reasoning without downsampling, Hardware system overview is shown in (Fig. 2). We develop a modular 

morphology-based tactile fingertip that mechanically projects distributed surface contacts onto a single sensing axis via an integrated compliant contact body,leveraging bio-inspired soft transmission principles [26]. The module consists of the compliant contact body, a single-axis force sensing unit, lateral side panels, and a reconfigurable dual-clamp mounting interface that attaches to generic parallel grippers and can be adapted to different jaw geometries (Fig. 2a). Unlike designs that separate distal and palmar sensing, the fingertip and fingerpad regions are realized as a single continuous compliant structure, allowing both fingertip interactions (e.g., button pressing) and fingerpad interactions (e.g., surface contact and enclosure) to propagate through a continuous force pathway and be mechanically funneled to the force sensor as a unified 1D tactile stream. The side panels shield the internal transmission structure, provide mechanical protection, and constrain undesired lateral deformation during contact [27]. 

To quantify how spatially distinct contacts are mapped to the sensor interface, we perform finite-element analysis under applied loads from 0 to 10 N and report total deformation, equivalent (von Mises) stress, and contact pressure on the sensor face (Fig. 2c). The resulting pressure–load curves exhibit an approximately linear mapping for both fingertip and fingerpad contacts, with the fingerpad configuration showing a higher pressure gain (Fig. 2b). These results confirm that contacts applied at different surface regions are consistently projected onto a single sensing axis through the compliant structure, yielding a predictable and monotonic force transmission pathway. 

We emphasize that this design does not aim to recover explicit contact location from tactile sensing alone. Instead, we intentionally adopt a single-axis force sensor as a systemlevel trade-off. In our framework, coarse contact location is already partially available from visual observations provided by the VLA backbone, whereas critical interaction cues such as click-through, snap-through, and release primarily manifest as high-frequency temporal force variations that are poorly captured by vision. Therefore, a 1D force signal is sufficient to complement visual perception by supplying precise magnitude and dynamic feedback, consistent with findings that aggregated force history contains rich information for complex manipulation [28]. This minimalist tactile interface aligns with TacMamba’s objective of injecting fast physical reflexes into slow visual reasoning. 

## IV. METHODOLOGY 

TacMamba bridges the frequency gap between high-speed tactile reflexes (System 1) and low-frequency visual planning (System 2). The proposed framework comprises two core components: (A) a hardware-aware Mamba encoder designed for continuous-time tactile modeling, and (B) a dual-stage training strategy that enforces temporal causality through adaptive sampling. 

## _A. Tactile Encoder via Mamba Architecture_ 

We adopt the **Mamba** architecture as our backbone, leveraging its core Selective State Space Model (SSM) mech- 

anism. This allows us to model the continuous physics of contact while handling abrupt dynamic discontinuities (e.g., impacts) through input-dependent selectivity. 

_1) Continuous-Discrete Modeling:_ We treat the 1D tactile signal _x_ ( _t_ ) _∈_ R as a continuous-time forcing function driving a latent physical system. This system maps the input to a latent state _h_ ( _t_ ) _∈_ R<sup>_N_</sup> via a linear time-invariant (LTI) ODE: 


To align with the discrete control cycles (time step ∆ _t_ ) of robotic hardware, we discretize Eq. 1 using the Zero-Order Hold (ZOH) principle, preserving physical consistency: 


where **A**<sup>¯</sup> = exp(∆ _t_ **A** ) and **B**<sup>¯</sup> are the discretized system parameters. 

_2) Capturing Hybrid Dynamics via Selectivity:_ Standard LTI systems rely on fixed parameters, which are insufficient for manipulation tasks characterized by hybrid dynamics. Mamba addresses this through its core selective mechanism, which parameterizes the system dynamics as a function of the input: specifically, we compute input-dependent parameters (∆ _t,_ **B** _t,_ **C** _t_ ) = Linear( _xt_ ) before discretization. This allows the model to function as an adaptive physical filter, capable of suppressing noise during static grasping while aggressively updating its internal state upon detecting transient contact events like a “click”. 

_3) Efficient Hierarchical Architecture with O_ (1) _Inference:_ As illustrated in Fig. 3 (Top), our network processes multivariate non-stationary force signals **X** . To handle sensor heterogeneity, we briefly apply RevIN and Channel Independence to extract universal physical features. The core backbone consists of stacked Mamba blocks (detailed in Fig. 3, Bottom-Left) that hierarchically capture features ranging from high-frequency impulses to long-term stability trends. 

The most critical advantage of this architecture is its Constant-Time Inference capability. Exploiting the recurrent formulation in Eq. 2, we maintain the compressed hidden state _ht−_ 1 in memory, making the update for a new force reading _xt_ strictly _O_ (1). This stands in sharp contrast to Transformers, ensuring that our “Fast” tactile system (100Hz) remains completely decoupled from the latency of the “Slow” visual policy. 

## _B. Training Strategy_ 

To mitigate the scarcity of labeled tactile data and the inherent temporal sparsity of critical contact events, we propose a robust two-stage protocol. 

_1) Stage 1: Self-Supervised Pre-training via Temporal Discrimination:_ To enable the Mamba encoder to comprehend contact dynamics without manual labels, we design a Ternary Temporal Discrimination task. 

Automatic Segmentation: First, we treat the tactile stream as a sequence of physical sub-tasks. We automatically segment long trajectories into discrete _sub-task phases_ based on 


Fig. 3. The TacMamba Network Architecture. Top: The core TacMamba backbone processes continuous tactile streams via a hierarchical Selective SSM, utilizing RevIN and Channel Independence for feature extraction. Bottom-Left: An expanded view of the Mamba block mechanism, illustrating how input-dependent parameters (∆ _t, Bt, Ct_ ) model hybrid dynamics. Bottom-Right: The auxiliary discriminator network, employed _exclusively during the training phase_ to facilitate robust feature learning and enforce temporal causality. 

the tactile gradient magnitude _∥∇xt∥_ , specifically detecting transitions from non-contact to contact. 

Objective: Based on these phases, we generate state pairs ( _hi, hj_ ) and train a discriminator _D_ to classify their temporal relationship into three categories: _yij ∈{_ 0 : _ti < tj,_ 1 : _ti ≈ tj,_ 2 : _ti > tj}_ . Crucially, we employ a RelationBalanced Sampling strategy to rigorously enforce a uniform distribution across these three classes (Early, Simultaneous, Late). This prevents the model from collapsing into trivial guessing strategies (e.g., always predicting ”future”) and forces the encoder to embed the causal structure of physical interactions into the hidden state space. 

We train the discriminator by minimizing the standard Cross-Entropy loss: 


_2) Stage 2: Tactile-Guided VLA Tuning with Phase Sampling:_ In this stage, we freeze the pre-trained Mamba encoder and project its compressed state _ht_ as a “Soft Prompt” _ztac_ into the VLA. 

Phase-Uniform Sampling: A critical challenge in robotic manipulation is that key interaction frames (e.g., contact transition) are extremely sparse compared to long-duration idle modes. As shown in the sparse force peaks of Fig. 1, critical events occupy a tiny fraction of the timeline. 

To address this, we utilize the automatic segmentation from Stage 1 to decompose each trajectory into a sequence of _K_ discrete sub-task phases _P_ = _{P_ 1 _, P_ 2 _, . . . , PK}_ . Standard uniform sampling ( _p_ ( _t_ ) _∝_ 1 _/T_ ) biases the model towards long-duration phases (e.g., static holding). In contrast, we employ a Phase-Uniform Sampling strategy that enforces a 

uniform distribution across phases: 


This ensures that each sub-task mode contributes equally to the training batch regardless of its temporal duration. Consequently, transient but critical phases (like the instant of snap-through) are weighted equally with stable modes, ensuring the VLA learns the complete manipulation logic without ignoring short-duration tactile cues. 

## V. EXPERIMENTS 

## _A. Experimental Setup_ 

Hardware Platform: We utilize an AgileX PiPER lightweight 6-DoF manipulator equipped with a parallel gripper. To capture contact dynamics, a custom single-point high-frequency force sensor is integrated into the fingertip, streaming 1D force data at 100Hz. This section aims to answer two core research questions: 

(1) Efficiency & Scalability: Can TacMamba maintain realtime responsiveness for high-frequency closed-loop control while modeling ultra-long tactile histories? 

(2) Robustness under Ambiguity: Does the injection of highfrequency tactile history significantly improve manipulation success rates in scenarios with visual occlusion or state ambiguity? 

Baselines: We compare our method against two categories of baselines: 

- 1) _Backbone Baselines:_ For the tactile encoder, we compare TacMamba against 1D-CNN (local convolution), LSTM (recurrent), and Transformer (global attention) to evaluate history compression capabilities. 

- 2) _System Baseline:_ For the end-to-end policy, we compare against _π_ 0 _._ 5 [2], a state-of-the-art generalist Vision-Language-Action (VLA) model, to assess the value of specialized tactile memory. 

## _B. Performance Evaluation: Accuracy & Efficiency_ 

We benchmark TacMamba against standard architectures on the exact same dataset. The quantitative results are summarized in Fig. 4 and Table I. 

_1) Comprehensive Analysis: Accuracy-Efficiency Tradeoff:_ We present a holistic evaluation of the trade-off between perception fidelity and real-time feasibility on the augmented real-world dataset. The comparison reveals distinct characteristics for each architecture: 

TacMamba (Ours): TacMamba achieves **SOTA accuracy (88.89%)** with an ultra-low inference latency of 0.45 ms. Its _O_ (1) complexity offers a 21 _×_ speedup over the LSTM, uniquely satisfying high-frequency control requirements ( _>_ 100Hz) without sacrificing precision. 

RNNs (LSTM): The Bi-LSTM achieves 82.50% accuracy but requires re-evaluating the entire history at each step, resulting in a 9.20 ms latency that breaches strict streaming constraints. The Single-LSTM is fast (0.54 ms) but suffers from catastrophic forgetting over high-frequency sequences, degrading accuracy to 65.33%. 


Fig. 4. **Efficiency Analysis.** Inference latency and memory growth. 

TABLE I 

COMPARISON ON THE AUGMENTED REAL-WORLD DATASET 

|**Model**|**Acc.**|**Lat.** (ms)|**Mem.** (MB)|
|---|---|---|---|
|1D-CNN|56.25%|0_._23_±_0_._02|19.14|
|Transformer|81.25%|11_._37_±_0_._17|2164.71|
|Bi-LSTM|82.50%|9_._20_±_0_._13|67.79|
|Single-LSTM|65.33%|0_._54_±_0_._01|63.70|
|**TacMamba**|**88.89%**|0_._45_±_0_._02|60.85|


Transformer: The Transformer achieves only 81.25% accuracy due to data inefficiency in extracting features from noisy tactile streams. Furthermore, its _O_ ( _L_<sup>2</sup> ) complexity spikes latency to 11.37 ms with excessive memory usage, rendering it infeasible for edge computing. 

1D-CNN: While computationally efficient (0.23 ms), the 1D-CNN exhibits the lowest accuracy (56.25%). Its limited receptive field fails to contextualize local vibrations within the broader task history, leading to state confusion. 

## _C. Real-World Validation: Sequential Interaction under Occlusion_ 

To comprehensively validate performance in physical environments and explicitly evaluate the limitations of traditional visual models in long-horizon scenarios, we designed three distinct manipulation tasks—“Sequential Button Pressing”, “Blind French Fry Packing”, and “Deformable Clothes Folding”. These tasks are formulated to rigorously benchmark TacMamba against the visual-only _π_ 0 _._ 5 baseline across varying degrees of visual occlusion and state ambiguity. 

Baseline Selection Strategy: While we performed extensive comparisons with LSTM and Transformer architectures on the offline dataset (Sec. V-B), we exclude them from these real-world closed-loop tasks. A critical constraint for System 1 reflexes is the 100Hz (10 ms) control cycle. However, the inference latency of both Transformer (quadratic complexity) and LSTM (sequential processing) scales with the input history length. As the tactile history grows during long-horizon manipulation, their computation time inevitably breaches this strict real-time limit, introducing dangerous delays. Consequently, TacMamba, with its constant-time _O_ (1) inference, is the only architecture capable of sustaining the high-frequency control loop, making _π_ 0 _._ 5 (visual-only) the only viable system-level baseline. 


Fig. 5. **Global Task Success Rate.** Comparison of full-task completion rates over training steps. TacMamba (Red) achieves rapid convergence and high robustness, while _π_ 0 _._ 5 (Blue) suffers from catastrophic failure in the button task due to static frame overfitting. 

_1) Task Definition:_ Task 1: Sequential Button Pressing. The robot is required to press three buttons in a specific color sequence (Blue _→_ Pink _→_ Purple). This task introduces three critical challenges: 

- 1) Visual Occlusion: The robot’s end-effector completely occludes the target area during operation, rendering the _π_ 0 _._ 5 visual encoder blind. 

- 2) State Ambiguity: The button trigger state (“Click”) provides only subtle vibration feedback, which is visually imperceptible. 

- 3) Perceptual Aliasing (Memory Gap): Since the buttons appear identical and the visual feed remains static due to occlusion, a model relying solely on current observation cannot distinguish the sequence phase (e.g., the first press vs. the second). Success requires persistent memory of past interactions. 

Task 2: Blind French Fry Packing. The robot must sequentially pick three french fries from a plate and place them into an opaque box. The core difficulty lies in Cumulative State Estimation: 

Since the box’s interior is occluded and external vision cannot penetrate it, the robot is effectively “blind” to the task progress. The system must rely entirely on long-horizon tactile history to track counting (i.e., remembering previous successful picks) to determine when to terminate the task. 

Task 3: Deformable Clothes Folding. As depicted in Fig. 7, the robot executes a five-step workflow: folding the garment across four directions (top, bottom, right, left) and placing it into a basket. This extended deformable manipulation rigorously tests VLA models against three core challenges: 

- 1) Precise Control: The fabric’s extreme thinness demands fine-grained, continuous physical interaction. 

- 2) Visual Ambiguity: Dynamic wrinkles easily deceive purely visual models, making tactile feedback indispensable to confirm a secure “pinch”. 

- 3) Long-Horizon Overfitting: The prolonged sequence exacerbates state forgetting and policy overfitting to static non-contact frames, degrading execution quality over time. 

Evaluation Metrics: To provide a granular analysis of physical interaction quality, we report performance on two levels: 


Fig. 6. **Atomic Action Success Rate.** Evaluation of fine-grained interaction quality (e.g., successful single button press without overshoot). TacMamba maintains high physical precision, whereas the baseline struggles with hallucinations and execution errors. 

- 1) Global Task Success: The percentage of episodes where the robot completes the entire long-horizon sequence (e.g., all 3 buttons pressed in correct order, or 3 fries packed). 

- 2) Atomic Action Success: Strict criteria to rule out “lucky” sub-task successes. _For Button Pressing:_ Must trigger the tactile “click” and halt immediately (overshoot or phantom presses are failures). _For Fries Packing:_ Must firmly grasp, transport, and release the fry into the box (grasping air, dropping, or edge-snagging are failures). 

_2) Results Comparison and Analysis:_ We evaluate TacMamba (with and without our sampling strategy) against _π_ 0 _._ 5 across different training stages. 

To ensure statistical significance and eliminate stochasticity, we adopted a rigorous evaluation protocol: for each training checkpoint, we conducted experiments across 10 randomized initial positions, with 5 independent trials per position (totaling 50 evaluation episodes per data point). 

TABLE II 

PERFORMANCE ON SEQUENTIAL BUTTON PRESSING TASK 

|Method|Success Rate|
|---|---|
|_External Visual Baselines_<sup>_∗_</sup>_:_||
|OpenVLA [29]|6%|
|CogACT [30]|15%|
|MemoryVLA [11]|58%|
|_Our Implementations:_||
|_π_0_._5 [2] (Early stage, 5k steps)|37.5%|
|_π_0_._5 [2] (Converged, 20k steps)|0%|
|**TacMamba (Phase-Uniform, Ours, 20k steps)**|**100%**|


> _∗_ Results for external visual baselines are directly sourced from [11]. Their experimental setup is identical to ours, with the sole exception of utilizing a Franka Panda manipulator instead of our AgileX PiPER. 

1. Baseline Limitations and Temporal Overfitting to Static Frames: The pure visual baseline ( _π_ 0 _._ 5) struggles in longhorizon tasks, as tracked in Fig. 5. In the _Sequential Button Pressing_ task, a temporal degradation is observed: the baseline achieves 37.5% success at 5k steps, but drops to 0% by 20k steps. This performance regression exposes the vulnerability of vision-only VLA models to temporal overfitting caused by data sampling bias. Because standard random sampling over-represents static, non-contact frames (which dominate the long-horizon sequence), the visual 


Fig. 7. **Qualitative folding results comparison.** (a) Successful cloth folding workflow executed by the full TacMamba model. The zoomed-in views highlight precise and stable grasps on the fabric corners enabled by high-frequency tactile feedback. (b) and (c) Typical failure modes observed when the phase-prioritized sampling strategy is disabled (ablation): ”Failed to grasp” (missing the corner due to visual ambiguity) and ”Shape crumpled” (improper tension control causing deformation). 

policy overfits to these stationary features over time. Consequently, the converged model tends to hover above the button, losing the ability to execute the dynamic pressing action. This degradation is not an isolated issue; as summarized in Table II, visual memory architectures like MemoryVLA [11] plateau at a 58% success rate on similar tasks. This performance ceiling stems from the low-frequency nature of visual observations: micro-scale physical events often fall into the blind spots between camera frames, causing state confusion. In contrast, TacMamba overcomes this staticframe overfitting, maintaining a 100% success rate upon convergence by anchoring its policy on high-frequency tactile reflexes. Similarly, in the Fries Packing task, visual occlusion limits _π_ 0 _._ 5 to a 47.5% global success rate. 

2. TacMamba’s High-Frequency Robustness: TacMamba effectively bypasses these perceptual bottlenecks. As demonstrated in both the global success (Fig. 5) and atomic action success (Fig. 6) curves, our full model maintains exceptional stability. By processing 1D tactile streams at 100Hz, it reliably captures transient events and maintains strict physical precision. TacMamba achieves 100% success in the button task by 8k steps and reaches 95% in the fries task, successfully performing implicit counting via longhorizon tactile history without visual confirmation. 

3. Ablation on Phase-Uniform Sampling: Comparing TacMamba trained with our Phase-Uniform Sampling against 

a Standard Uniform variant highlights the strategy’s data efficiency and fine-grained control capabilities. As explicitly tracked by the atomic action success rate in Fig. 6, the phaseuniform approach significantly reduces micro-level execution errors (e.g., overshoot or phantom grasps). Consequently, at 8k steps in the fries task, it yields an 82.5% global success rate, nearly doubling the uniform baseline (47.5%). By explicitly prioritizing sparse, high-frequency contact events, our strategy improves overall sample efficiency by approximately 2.5 _×_ . 

4. Deformable Manipulation & Hardware Constraints: Due to the fabric’s extreme thinness, unconverged policies often apply excessive downward force, risking physical damage to the custom tactile sensor against the rigid tabletop. Therefore, we evaluated the _Clothes Folding_ task exclusively at full convergence (20k steps). While all models achieved 100% macro-folding success, fine-grained quality varied. The visual baseline and the uniform-sampling ablation suffered from micro-failures (e.g., “Failed to grasp” or “Shape crumpled”) due to ambiguous visual wrinkles (Fig. 7). The full TacMamba model maintained robust reflexes, reliably pinching exactly when the fabric edge was felt. 

## VI. CONCLUSIONS 

In this work, we presented TacMamba, a hardwaresoftware architecture that successfully bridges the critical spatiotemporal gap between high-frequency tactile reflexes 

and low-frequency visual reasoning. By formulating continuous 1D tactile streams through a Mamba-based architecture, our approach achieves SOTA accuracy (88.89%) with strict _O_ (1) inference latency (0.45 ms). This outperforms Transformer baselines by a 25 _×_ speedup and completely bypasses their latency bottlenecks, representing the first architecture capable of processing ultra-long tactile histories ( _L_ = 5000) within the hard real-time constraints of embedded hardware. Furthermore, it overcomes the catastrophic forgetting inherent in standard LSTMs, enabling lossless, real-time processing of micro-scale contact dynamics. 

Additionally, our phase-uniform sampling strategy effectively mitigates the data imbalance of sparse contact events, drastically improving sample efficiency during VLA finetuning. Extensive physical evaluations confirm that TacMamba entirely overcomes the temporal overfitting to static frames that causes purely visual baselines (e.g., _π_ 0 _._ 5) to fail. By strictly satisfying 100Hz control loop constraints and maintaining fine-grained physical precision without overshoot, our system achieves robust task execution across visually occluded and long-horizon scenarios, reliably solving complex challenges like sequential button pressing, implicit state counting, and deformable clothes folding. 

Despite these advances, our system has certain limitations. Our current setup utilizes a 1D force sensor rather than high-resolution vision-based tactile sensors (e.g., GelSight). While sufficient for isolating high-frequency temporal dynamics and avoiding the computational overhead of image processing [31], this prevents the extraction of fine-grained spatial topologies. Additionally, rather than exhaustive largescale benchmarking, our physical evaluation deliberately targets specific edge cases (e.g., severe occlusion), comparing primarily against the state-of-the-art _π_ 0 _._ 5 [2]. Nevertheless, TacMamba’s decoupled nature naturally supports plug-andplay integration with broader open-source VLA frameworks. 

Future work will address these constraints by integrating high-dimensional GelSight image sequences directly into the Mamba network for spatially-rich contact tasks, and investigate its potential to facilitate zero-shot sim-to-real transfer for multi-fingered dexterous hands. 

## REFERENCES 

- [1] D. Kahneman, _Thinking, fast and slow_ . New York: Farrar, Straus and Giroux, 2011. 

- [2] K. Black _et al._ , “ _π_ 0 _._ 5: A vision-language-action model with openworld generalization,” in _9th Annual Conference on Robot Learning (CoRL)_ , 2025. 

- [3] A. Brohan _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Proceedings of the 7th Conference on Robot Learning (CoRL)_ , 2023, pp. 2165–2183. 

- [4] Octo Model Team _et al._ , “Octo: An open-source generalist robot policy,” in _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- [5] G. Team _et al._ , “Gigabrain-0: A world model-powered visionlanguage-action model,” _arXiv preprint arXiv:2510.19430_ , 2025. 

- [6] Zhai _et al._ , “Igniting vlms toward the embodied space,” _arXiv preprint arXiv:2509.11766_ , 2025. 

- [7] M. J. Kim _et al._ , “Fine-tuning vision-language-action models: Optimizing speed and success,” _arXiv preprint arXiv:2502.19645_ , 2025. 

   - [9] Yu _et al._ , “Forcevla: Enhancing vla models with a force-aware moe for contact-rich manipulation,” _arXiv preprint arXiv:2505.22159_ , 2025. 

   - [10] F. Yang _et al._ , “Binding touch to everything: Learning unified multimodal tactile representations,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 26 340–26 353. 

   - [11] H. Shi _et al._ , “Memoryvla: Perceptual-cognitive memory in visionlanguage-action models for robotic manipulation,” _ArXiv_ , vol. abs/2508.19236, 2025. 

   - [12] Li _et al._ , “Map-vla: Memory-augmented prompting for visionlanguage-action model in robotic manipulation,” _arXiv preprint arXiv:2511.09516_ , 2025. 

   - [13] W. Yuan _et al._ , “Gelsight: High-resolution robot tactile sensors for estimating geometry and force,” _Sensors_ , vol. 17, no. 12, p. 2762, 2017. 

   - [14] M. Lambeta _et al._ , “Digit: A novel design for a low-cost compact highresolution tactile sensor with application to in-hand manipulation,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 3, pp. 3838–3845, 2020. 

   - [15] A. Vaswani _et al._ , “Attention is all you need,” _Advances in neural information processing systems_ , vol. 30, 2017. 

   - [16] R. Pascanu _et al._ , “On the difficulty of training recurrent neural networks,” in _International conference on machine learning_ . Pmlr, 2013, pp. 1310–1318. 

   - [17] S. Bai, “An empirical evaluation of generic convolutional and recurrent networks for sequence modeling,” _arXiv preprint arXiv:1803.01271_ , 2018. 

   - [18] U. Khandelwal _et al._ , “Sharp Nearby, Fuzzy Far Away: How Neural Language Models Use Context,” _Association of Computational Linguistics (ACL)_ , 2018. 

   - [19] X. Fang _et al._ , “Kalm: Keypoint abstraction using large models for object-relative imitation learning,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 8307–8314. 

   - [20] E. Johns, “Coarse-to-fine imitation learning: Robot manipulation from a single demonstration,” in _2021 IEEE international conference on robotics and automation (ICRA)_ . IEEE, 2021, pp. 4613–4619. 

   - [21] A. Gu _et al._ , “Mamba: Linear-time sequence modeling with selective state spaces,” in _First conference on language modeling_ , 2024. 

   - [22] ——, “Efficiently modeling long sequences with structured state spaces,” in _The International Conference on Learning Representations (ICLR)_ , 2022. 

   - [23] Y. Nie _et al._ , “A time series is worth 64 words: Long-term forecasting with transformers,” in _International Conference on Learning Representations (ICLR)_ , 2023. 

   - [24] T. Kim _et al._ , “Reversible instance normalization for accurate timeseries forecasting against distribution shift,” in _International conference on learning representations_ , 2021. 

   - [25] M. A. Ahamed _et al._ , “Timemachine: A time series is worth 4 mambas for long-term forecasting,” in _ECAI 2024: 27th European Conference on Artificial Intelligence_ , vol. 392, 2024, p. 1688. 

   - [26] N. Wettels, V. J. Santos, R. S. Johansson, and G. E. Loeb, “Biomimetic tactile sensor array,” in _2008 2nd IEEE RAS & EMBS International Conference on Biomedical Robotics and Biomechatronics_ . IEEE, 2008. 

   - [27] L. U. Odhner _et al._ , “A compliant, underactuated hand for robust manipulation,” _The International Journal of Robotics Research_ , 2014. 

   - [28] N. Fazeli, M. Oller, J. Wu, Z. Wu, J. B. Tenenbaum, and A. Rodriguez, “See, feel, act: Hierarchical learning for complex manipulation skills with multisensory fusion,” _Science Robotics_ , 2019. 

   - [29] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi _et al._ , “Openvla: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

   - [30] Q. Li, Y. Liang, Z. Wang, L. Luo, X. Chen, M. Liao, F. Wei, Y. Deng, S. Xu, Y. Zhang _et al._ , “Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation,” _arXiv preprint arXiv:2411.19650_ , 2024. 

   - [31] Q. Ye, Q. Liu, S. Wang, J. Chen, Y. Cui, K. Jin, H. Chen, X. Cai, G. Li, and J. Chen, “Visual-tactile pretraining and online multitask learning for humanlike manipulation dexterity,” _Science Robotics_ , vol. 11, no. 110, p. eady2869, 2026. 

- [8] Z. Cheng _et al._ , “Omnivtla: Vision-tactile-language-action model with semantic-aligned tactile sensing,” _arXiv preprint arXiv:2508.08706_ , 2025. 

