---
title: "TRM-VLA: Temporal-Aware Chain-of-Thought Reasoning and Memorization for Vision-Language-Action Models"
date: "2026"
venue: "CVPR 2026"
url: https://openaccess.thecvf.com/content/CVPR2026/html/Li_TRM-VLA_Temporal-Aware_Chain-of-Thought_Reasoning_and_Memorization_for_Vision-Language-Action_Models_CVPR_2026_paper.html
pdf: https://openaccess.thecvf.com/content/CVPR2026/papers/Li_TRM-VLA_Temporal-Aware_Chain-of-Thought_Reasoning_and_Memorization_for_Vision-Language-Action_Models_CVPR_2026_paper.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://openaccess.thecvf.com/content/CVPR2026/papers/Li_TRM-VLA_Temporal-Aware_Chain-of-Thought_Reasoning_and_Memorization_for_Vision-Language-Action_Models_CVPR_2026_paper.pdf)** / [論文ページ](https://openaccess.thecvf.com/content/CVPR2026/html/Li_TRM-VLA_Temporal-Aware_Chain-of-Thought_Reasoning_and_Memorization_for_Vision-Language-Action_Models_CVPR_2026_paper.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# VLA<sup>**TRM-VLA: Temporal-Aware Chain-of-Thought Reasoning and**</sup> **Memorization for Vision-Language-Action Models** 

Xiang Li<sup>1,2,3</sup> Ya-Li Li<sup>1,2,3</sup><sup>_‡_</sup> Yuan Wang<sup>1,2,3</sup> Shengjin Wang<sup>1,2,3</sup> 

1Department of Electronic Engineering, Tsinghua University, China 

2Beijing National Research Center for Information Science and Technology (BNRist), China 3National Engineering Research Center of Dangerous Articles and Explosives Detection Technologies, Beijing; 100084, China 

l-xiang24@mails.tsinghua.edu.cn 

_{_ liyali13, wgsgj _}_ @tsinghua.edu.cn 

> _‡_ Corresponding Author 

## **Abstract** 

_Vision-Language-Action (VLA) models have emerged as a powerful paradigm for general robotic manipulation. However, existing approaches typically omit intermediate reasoning steps and directly regress actions, limiting reasoning interpretability and performance in long-horizon or compositional tasks. Although recent studies introduce Chain-ofThought (CoT) reasoning into VLA models, their effectiveness remains suboptimal due to two key issues: (1) generating a full reasoning trajectory at every timestep introduces substantial redundancy, thereby hinders real-time deployment and (2) reasoning is performed independently, neglecting temporal consistency, which leads to planning conflicts. We propose TRM-VLA, a temporal-aware reasoning and memorization framework that integrates explicit temporal modeling into the VLA reasoning process. TRM-VLA consists of two core components: (1) Keyframe-Triggered Reasoning (KTR), which identifies task progress and performs hierarchical CoT reasoning only at key decision points to reduce redundant inference; and (2) Granularity-adaptable Context Memory (GCM), which dynamically stores and retrieves historical reasoning trajectories to maintain interframe coherence and global context. Extensive experiments on LIBERO-90, SIMPLER, and four real-world robotic tasks demonstrate that TRM-VLA achieves state-of-the-art performance while improving reasoning efficiency._ 

## **1. Introduction** 

Recent years have witnessed significant progress in generalpurpose robotic manipulation policies [4, 5, 18, 25, 31, 41, 58]. Among these advances, VLA models have emerged as a powerful paradigm by leveraging the multimodal understanding of pre-trained Vision-Language Models (VLMs) to enhance embodied generalization [2, 6, 14, 18, 19, 29, 58]. By fine-tuning on robot interaction data, VLA models inherit open-world reasoning capabilities from VLMs [3, 16], map- 


Figure 1. Different reasoning patterns of VLAs. (a) generate full CoT at every frame. (b) generate CoT at fixed intervals without memory. (c) generate hierarchy CoT at critical frames, and maintain a dynamic memory buffer for execution, thus reducing redundant CoT reasonings tokens while improving the success rates. 

ping visual observations and language instructions directly to action spaces for execution. Despite promising results, most existing approaches suffer from the erosion of pre-trained knowledge from the VLM [56] during fine-tuning and lack explicit reasoning processes [18, 22, 58], directly regressing actions from inputs. This omission undermines manipulation interpretability and limits their performance on long-horizon, complex tasks that require structured planning. 

Inspired by the chain-of-thought (CoT) reasoning [1, 44] in large language models (LLMs), wherein complex problems are decomposed into intermediate steps through prompting, thereby enhancing reasoning performance. In robotics, integrating CoT holds promise for grounding reasoning in textual instructions, visual observations, and actions. Prior 

10943 

reasoning-augmented works have explored various strategies: some incorporate embodied-relevant primitives such as keypoints, bounding boxes, or trajectories as reasoning intermediates [11, 14, 26, 50]; others leverage action or video generation models or world models to produce goal-conditioned visual plans that guide step-by-step execution [48, 52]. Additionally, several approaches mitigate knowledge erosion in VLA models through co-training on internet-scale language data and robot interaction data [37, 45–47, 56]. 

However, as shown in Figure 1(a)(b), current reasoningaugmented VLA methods generate a full and independent CoT at every timestep or at fixed intervals, without considering the temporal structure of the task. This design leads to two critical issues: 1) _Redundant reasoning_ . Most methods generate a full CoT trajectory at every timestep, even when adjacent frames share nearly identical visual and linguistic contexts. This results in repetitive reasoning, excessive CoT token generation, and substantial computational overhead with diminishing decision gains. 2) _Independent inter-frame reasoning_ . Each CoT is produced in isolation, without temporal dependency or memory. The absence of historical reasoning causes contradictory action plans, breaking temporal coherence and degrading performance on long-horizon tasks. For instance, in sequential button pressing(e.g., “press red, then green, then blue”), static visuals prevent the agent from tracking which steps are completed, causing repetition and task failure. This non-Markovian dependency cannot be resolved by such frame-wise reasoning [39]. 

To address these limitations, we propose **Temporalaware Reasoning and Memorization** for Vision-LanguageAction models, TRM-VLA — a framework that introduces structured, keyframe-trigger reasoning and explicit contextaware memory mechanisms into the VLA pipeline. 

(1) _Keyframe-Triggered Reasoning (KTR)_ . KTR performs hierarchical CoT reasoning only at key decision points (e.g., when the robot grasps the object) and is informed by task progress, thereby reducing redundant reasoning and token generation while preserving interpretability. 

(2) _Granularity-adaptable Context Memory (GCM)_ . To overcome the lack of temporal consistency and memory, GCM maintains a dynamic memory buffer of past critical reasoning steps, which are selectively retrieved through cross-attention to inform current decisions. By integrating historical reasoning into the policy state, GCM enforces temporal coherence, allowing the model to maintain consistent plans and to leverage memory to track task progress. 

As illustrated in Figure 1, unlike Pattern (a) [47, 50] (full CoT at every timestep) or Pattern (b) [10, 27] (CoT generated only at fixed intervals without memory), our approach combines hierarchy, keyframe-triggered reasoning with dynamic, multi-granularity memory. This breaks the implicit Markovian assumption of prior methods, endowing TRM-VLA with reasoning efficiency and temporal awareness essential 

for complex, real-world manipulation tasks. 

Our TRM-VLA framework builds upon a state-of-theart multimodal foundation model [16, 18] and a Diffusion Transformer [22, 34] action policy. We adopt a dual-system architecture [6] inspired by cognitive science: the foundation model acts as System 2, responsible for slow, deliberate CoT generation, while the Diffusion Transformer [9] serves as System 1, executing fast, reflexive action prediction. The model is pretrained on the Open X-Embodiment dataset [32] and subsequently fine-tuned on task-specific robot interaction data for deployment. We annotate existing embodied datasets with multi-level temporal labels and employ causal attention with next-token prediction as training objective, enabling the VLM to learn to implicitly identify task progress and generate reasoning at appropriate levels of abstraction, from strategic planning to concrete motor commands. 

Extensive experiments on LIBERO-90, SIMPLER, and four real-world manipulation tasks demonstrate that TRMVLA not only achieves state-of-the-art performance (72.9% on SIMPLER [23]) but also reduces CoT token generation by 4× compared to existing reasoning-enabled VLA models. 

- We propose the TRM-VLA framework, which integrates temporal-aware reasoning and memorization to address the inference redundancy and inconsistency with frame-wise CoT generation for effective robotic manipulation. 

- We introduce keyframe-triggered reasoning (KTR) and granularity-adaptable context memory (GCM), which guarantee temporally-coherent planning by incorporating hierarchical CoT and dynamic memory retrieval. 

- We conduct comprehensive evaluation in real and simulated settings, demonstrating superior performance and efficiency across a diverse set of manipulation tasks. 

## **2. Related Works** 

### **2.1. Generalist Robot Manipulation Policies** 

Recent work has demonstrated that scaling robot manipulation policies across diverse environments and tasks significantly improves their multi-task and cross-scenario generalization capabilities [2, 17, 32, 43]. Training such generalist policies typically requires scalable architectures capable of handling heterogeneous, large-scale, cross-embodiment robot interaction data. Vision-Language-Action models [14, 18, 22, 29, 30, 32, 36, 41, 45, 58] offer a promising paradigm: they build upon pre-trained Vision-Language Models and perform post-training on robot data. This approach effectively transfers the rich multimodal understanding of VLMs to embodied control, circumventing the data-hungry nature of training from scratch. Subsequent research has explored multiple directions to enhance VLA performance, including: Action generation architectures, such as Diffusion-based Action Experts for continuous control [4, 22, 45]; Dualsystem designs that separate high-level reasoning from lowlevel execution [6, 40]; Multimodal data composition strate- 

10944 

gies, incorporating tactile, 3D, or instruction-augmented inputs [13, 14, 47, 53, 56] and reinforcement learning finetuning to refine policies post-supervised training [12, 21, 49]. While chain-of-thought (CoT) reasoning has substantially advanced LLM-based reasoning, its integration into VLA models has brought only marginal improvements. Crucially, most existing methods neglect the temporal structure of reasoning inherent to robotic manipulation—where decisions are non-Markovian and depend on historical context beyond the current observation. In this work, we bridge this gap by introducing temporal-aware hierarchical reasoning with persistent memory as an intermediate representation prior to action generation, enabling temporally consistent decisionmaking in long-horizon and complex manipulation tasks. 

### **2.2. Reasoning in Vision-Language-Action Models** 

Existing reasoning-enabled VLA approaches [8, 14, 50] can be broadly categorized into three lines of work: (1) Primitive-based reasoning. These methods use embodiedrelevant primitives such as subgoals, trajectories, object bounding boxes, or keypoints as explicit reasoning intermediates [11, 14, 20, 26, 52, 57]. By grounding reasoning in taskrelevant visual or geometric cues, they improve policy focus and performance. (2) World model or video-generationaugmented reasoning. Some works employ world models or video generation models to produce goal-conditioned visual plans (e.g., goal images) that guide step-by-step execution [7, 52]. Others learn latent action representations from human demonstration videos and transfer them as priors to robots [2, 48]. (3) Co-training with internet-scale and embodied data. To mitigate language forgetting during robot fine-tuning, several approaches jointly train on internet-scale multimodal data (e.g., image captions, VQA pairs) and robot interaction data [14, 37, 46, 47, 56]. In contrast, we propose a temporal-aware reasoning and memory framework for VLAs: reasoning is triggered only at key decision points, and past reasoning traces are explicitly stored and retrieved to inform current decisions. This design better aligns with the memory-dependent nature of real-world robotic tasks. 


where _at ∈_ R<sup>_d_</sup> typically represents a 7-DoF vector (e.g., [∆ _x,_ ∆ _β,_ gripper]), depending on the robot embodiment, where ∆ _x,_ ∆ _β,_ gripper denote the relative translation, rotation and gripper state of the end effector, and _θ_ is the parameters of the network. While effective for short-horizon tasks, this direct mapping discards intermediate reasoning, leading to poor interpretability and degraded performance on complex, multi-stage robotic manipulation. 

**Reasoning-augmented VLA** introduces an intermediate reasoning trace _rt_ , such as textual planning or visual subgoals, to bridge the gap between perception and action: 


However, these methods typically generate _rt_ independently at every timestep, ignoring temporal structure. This leads to (1) redundant computation due to near-identical reasoning across consecutive frames, and (2) inconsistent subgoal sequencing that undermines long-horizon coherence. **Temporal-Aware Reasoning Formulation for VLA** . We explicitly model temporal dependencies by conditioning action prediction on a memory-augmented reasoning state _mt_ , integrating both current and historical reasoning contexts. 


where _rt_<sup>_h∼Pθ_(</sup><sup>_r_</sup> _t_<sup>_h| ot, lt_) denotes the hierarchy, keyframe-</sup> triggered CoT reasonings produced by our KeyframeTriggered Reasoning module (KTR). Then Granularityadaptable Context Memory (GCM) module ( _Pϕ_ ) dynamically aggregates past reasoning traces _{r_ 1<sup>_h, . . . , r_</sup> _t_<sup>_h}_into</sup> a compact, temporally consistent representation _mt_ . By generating keyframe-triggered reasonings and propagating memory-based context across timesteps, TRM-VLA establishes a coherent temporal reasoning process. This design enables the model to maintain global reasoning context while executing efficient, consistent control across long-horizon and complex tasks. 

### **3.2. TRM-VLA Framework** 

## **3. Method** 

We present our Temporal-aware Reasoning and Memorization framework for VLAs, designed to enhance the temporal reasoning and memory in robotic manipulation. We first formalize standard and reasoning-augmented VLA models in Sec. 3.1, followed by an overview of our system architecture in Sec. 3.2 as shown in Fig. 2. We then detail the two core modules, Keyframe-Triggered Reasoning in Sec. 3.3 and Granularity-adaptable Context Memory in Sec. 3.4. 

### **3.1. Preliminaries** 

**Standard VLA** aims to map visual observations _ot_ and language instructions _lt_ into robot actions _at_ at timestep _t_ : 

As shown in Fig. 2, TRM-VLA builds upon CogACT [22], a strong baseline that combines a multimodal foundation model with a diffusion-based action policy inspired by cognitive architectures [6]. Our framework follows a dual-system design: a deliberative System 2 (VLM-based reasoning) and a reactive System 1 (diffusion action expert). 

The visual encoder transforms the input image into visual tokens _V_ = _{v_ 1 _, v_ 2 _, . . . , vNv }_ . It consists of two complementary vision transformers pretrained on large-scale internet imagery: DINOv2 [33] for capturing spatially localized features, and SigLIP [51] for encoding semantic-level representations. Together, they provide a comprehensive visual understanding for downstream reasoning. 

10945 


Figure 2. Overview of the proposed TRM-VLA (Sec. 3.2). (a) System design: VLM backbone for reasoning and diffusion expert for execution. (b) Keyframe-Triggered Reasoning (Sec. 3.3) performs hierarchical reasoning only at critical frames supervised by temporal reasoning data. (c) Granularity-adaptable Context Memory (Sec. 3.4) maintains a dynamic memory buffer to enhance inter-frame reasoning coherence. 

The language encoder adopts LLaMA-2 [42], which jointly processes the tokenized instruction _L_ = _{l_ 1 _, l_ 2 _, . . . , lNl }_ , visual tokens _V_ , and a learnable cognition token _c_ through a multimodal transformer. During training, the model is trained on embodied reasoning data annotated with multi-level keyframes and temporal stages, enabling it to learn when and how to reason. At inference time t, it adaptively outputs: 1) a hierarchy reasoning _rt_<sup>_h_</sup> through Keyframe-Triggered Reasoning module whenever _t_ corresponds to a keyframe (and no reasoning is generated otherwise), and 2) a cognition feature _ft_ corresponding to the cognition token _c_ , which encodes the multimodal representation of the current scenario. 

To ensure temporal consistency and contextual reasoning, Granularity-adaptable Context Memory (GCM) maintains a dynamic memory buffer of past critical reasoning features and constructs a memory-augmented state _mt_ . The model integrates _mt_ with _ft_ via a FiLM-based [35] fusion network, effectively propagating temporal dependencies across frames and facilitating consistent reasoning over time. Finally, the action expert—a Diffusion Transformer (DiT) [34]—takes the fused cognition feature as a conditioning input. Given Gaussian noise and _ft_ the DiT performs iterative denoising to generate an action chunk _A_ = ( _a_ 1 _, a_ 2 _, . . . , aNa_ ) _._ This diffusion-based decoding yields smooth, temporally coherent action sequences, crucial for stable real-world execution. 

### **3.3. Keyframe-Triggered Reasoning** 

Our core insight is that effective reasoning in embodied tasks should “think appropriately” at each timestep, generating reasoning most relevant to the current scene (Eq. 3)—and to “think temporally” by integrating historical reasoning across time (Eq. 4). Together, these two capabilities strengthen the 

model’s temporal reasoning and allow it to perform embodied decision-making with long-horizon consistency. KTR achieves this by producing sparse, hierarchical CoT only at critical decision points, thereby aligning reasoning effort with task dynamics. As shown in Fig. 2, KTR is trained on embodied reasoning data augmented with fine-grained temporal annotations, as described below. 

**Embodied Reasoning Annotation** . We extend existing robot manipulation datasets with structured CoT annotations, following the ECoT protocol [50]. Each reasoning trace is decomposed into semantically distinct components: _tag ∈ {task, plan, perception, subtask reasoning, subtask, move reasoning, move, gripper position}_ , which collectively capture high-level task decomposition and low-level, perception-grounded action justification. At timestep _t_ , this yields a structured label _Rt_ = _{rt_<sup>_tag_</sup> _}_ . To improve the quality and temporal consistency of annotations, we introduce three key enhancements: (1) a temporal tracking model [15] for smooth gripper and object trajectory alignment; (2) a unified VLM [3] for joint object detection, captioning, and reasoning to ensure semantic coherence; and (3) an optimized annotation pipeline for improved inter-frame consistency and efficiency. Details can be found in the Appendix. **Keyframe-Based Annotation** . Frame-wise annotation introduces severe redundancy: high-level tags (e.g., _plan_ ) remain static for entire episodes, while low-level tags (e.g., _gripper position_ ) change rapidly. To mitigate this, we introduce _hierarchical keyframe indicators_ that mark meaningful transitions in reasoning structure. Specifically, we define binary flags for three reasoning granularities: 


10946 

where _τ_ = per(perception), s(subtask), m(move) denote levels of temporal granularity. This hierarchical scheme produces three types of keyframes: _b_<sup>per</sup> _t_ stands for signal significant scene or object-state changes; _b_<sup>s</sup> _t_<sup>marks transitions</sup> between distinct subgoals; _b_<sup>m</sup> _t_<sup>captures fine-grained motion</sup> or gripper adjustments. These keyframes serve as supervision signals for when reasoning should be updated. 

**Stage-Wise Temporal Structuring** . To further model temporal dependencies and reduce redundant reasoning, we segment each task episode into three temporal phases: an early stage for high-level planning (task, plan, perception, subtask/move reasoning), a middle stage for perceptionanchored subtask decomposition (activated only at perception keyframes), and a late stage for low-level execution (subtask/move commands and gripper control, triggered by subtask or move keyframes). The temporal-aware hierarchical reasoning set _Tt_ is then defined as: 


where we use abbreviated tag names for brevity (e.g., t = _task_ , p = _plan_ , per = _perception_ , sr = _subtask reasoning_ , mr = _move reasoning_ , g = _gripper position_ ). Note that reasoning is only generated when a corresponding keyframe is active, ensuring sparsity. We train KTR using a standard next-token prediction objective with causal attention: 


where _D_ denotes the annotated dataset and _T_ the episode length. This objective encourages the model to learn _when_ to reason (via keyframe-triggered activation) and _what_ to reason about (via hierarchical tag prediction). In summary, KTR equips the VLA model with adaptive temporal reasoning: it automatically identifies critical decision points, generates multi-granularity CoT aligned with task structure, and suppresses redundant computation. This enables a smooth transition from abstract planning to concrete execution—mirroring human-like problem solving in embodied tasks. 

### **3.4. Granularity-adaptable Context Memory** 

While the KTR module enables the model to produce hierarchical reasoning aligned with temporal keyframes, relying solely on the reasoning of the current timestep can be suboptimal. For instance, when the model generates only low-level reasoning at a subtask keyframe, it may overlook high-level planning information that remains relevant throughout the task. To address this limitation, we introduce the GCM module, which maintains a dynamic, multi-granularity memory 

of past reasoning to form a temporally coherent context _C_ , enabling the model to “reason across time.” 

**Dynamic Reasoning Context** . In a task of length _T_ with _Nk_ keyframes _{ki}_<sup>_N_</sup> _i_ =1<sup>_k_where0</sup><sup>_<k_1</sup><sup>_<· · ·<kN_</sup> _k_<sup>_<T_,the</sup> reasoning context at the current keyframe _kc_ is represented as a dictionary-based memory buffer _Ckc_ , which stores hierarchical reasoning tokens _{rk_<sup>tag</sup> _i_<sup>_}_</sup> _i_<sup>_c_</sup> =1<sup>frompreviouslyob-</sup> served keyframes. When the model generates new reasoning components _rk_<sup>tag</sup> _c_<sup>, they are inserted into</sup><sup>_Ckc_, overwriting any</sup> existing entries with the same tag. _Ckc_ = _Ckc−_ 1 _∪{rk_<sup>tag</sup> _c_<sup>_},_</sup> (8) 

To account for the temporal stability of different reasoning levels, we assign hierarchical lifetimes: high-level reasoning ( _rk_<sup>task</sup><sup>_, r_</sup> _k_<sup>plan</sup> ) is generated mainly in the early stage and preserved in the context until the task ends. Mid-level reasoning ( _rk_<sup>p</sup><sup>_, r_</sup> _k_<sup>sr</sup><sup>_, r_</sup> _k_<sup>mr) is retained for a moderate duration, replaced</sup> only when new reasoning of the same tag appears. Lowlevel reasoning ( _rk_<sup>s</sup><sup>_, r_</sup> _k_<sup>m</sup><sup>_, r_</sup> _k_<sup>g) has a shorter lifespan, updated</sup> frequently to reflect real-time control variations. Compared with per-frame CoT reasoning, GCM provides a memoryefficient alternative that preserves long-range task consistency without redundant computation. 

**Temporal Reasoning Integration** . To inject historical context into action generation, GCM employs a learnable thinking query _qt_ that retrieves the most relevant reasoning features from _Ct_ . Specifically, we encode all entries in _Ct_ through the vision-language model to obtain contextual embeddings _f_ rc, which serve as keys and values in a crossattention mechanism. To avoid redundant computation, both _Ct_ and _f_ rc are jointly maintained and updated. This design enables GCM to efficiently reuse past reasoning without repeated forward passes through the VLM, reducing inference cost while preserving temporal coherence and context: 


The retrieved feature _f_ att is then fused with the current cognition token feature _fc_ (from the VLM) via a Feature-wise Linear Modulation (FiLM) network [35]: 


yielding a fused feature _ft_ that encodes both immediate perception and historical reasoning. This context-enriched representation serves as the conditioning signal for the downstream diffusion-based action policy. 

**Action Diffusion and Training Objective** . The fused feature _ft_ is passed to a diffusion-based action expert [34], which iteratively denoises a latent action sequence to produce a smooth action chunk _A_ = ( _a_ 1 _, a_ 2 _, . . . , aNa_ ). Following standard diffusion policy training, we minimize the mean squared error between predicted and ground-truth noise: 


10947 

where _ϵ_ ˆ<sup>_i_</sup> is the noise prediction at denoising step _i_ for a noisy action sequence ( _a_<sup>_i_</sup> _t_<sup>_, ai_</sup> _t_ +1<sup>_, . . . , ai_</sup> _t_ + _N_<sup>).This learning</sup> objective encourages the policy to generate actions that are not only physically plausible but also semantically grounded in temporally consistent reasoning. 

## **4. Experiments** 

### **4.1. Datasets and Benchmarks** 

**SIMPLER Benchmark** . We evaluate on SIMPLER [23], a high-fidelity simulation suite that closely matches real-world robot dynamics and visual appearance. A key feature of SIMPLER is its real-to-sim evaluation protocol: policies trained on real-world data are tested in simulation, with strong empirical correlation to physical-world performance under distribution shifts. This makes SIMPLER ideal for assessing reasoning-intensive methods, as it preserves the semantic and temporal structure of manipulation tasks while enabling scalable, reproducible evaluation. 

**LIBERO Benchmark** . We further test on LIBERO90 [28], a challenging long-horizon benchmark comprising 90 language-conditioned tasks across 10 household domains. Tasks require fine-grained object interaction, multi-stage planning, and precise control—making it a rigorous testbed for temporal reasoning and memory. 

**Real-World Benchmark** . We collect 410 expert demonstration trajectories on an AIRBOT Player robot across four carefully designed tasks that probe distinct reasoning capabilities: (1) _Scoop Washers with Shovel_ : The robot uses a non-end-effector tool (shovel) to scoop small metal washers, testing generalization to tool-based manipulation; (2) _Clean Table_ : The robot clears diverse objects (bear, banana, cup, etc.) into a bin, evaluating long-horizon planning and object-agnostic execution; (3) _Push Buttons in Order_ : The robot presses three colored buttons in a specified sequence, explicitly testing temporal memory and sequential reasoning; (4) _Place Toy Bear into Box_ : The robot grasps a deformable object from varied poses and places it into a container, assessing robustness to object shape and pose variations. Together, these tasks span tool use, memory-dependent sequencing, sustained planning, and precise manipulation—core challenges addressed by our framework. 

**Embodied Reasoning Datasets** . For the SIMPLERWidowX benchmark, we build upon the BridgeData V2 [43] dataset and adopt the CoT annotations generated by ECoT [50]. For LIBERO-90 [28], we use the reasoning annotations from ECoT-Lite [8], a streamlined variant of ECoT tailored to the LIBERO task suite. For real-world experiments, we employ the Qwen3-VL [3] multimodal language model to automatically produce embodied CoT labels from video-language-action sequences. Our annotation pipeline simplifies and consolidates the original protocol resulting in 

higher annotation quality and efficiency.<sup>1</sup> 

### **4.2. Quantitative Results** 

**Simulated Evaluation** . We evaluate TRM-VLA on the SIMPLER-Bridge benchmark [23], which provides highfidelity simulated environments. For each task, we report Grasp Rate (percentage of trials with successful object contact) and Success Rate (SR) (full task completion). As shown in Table 2, TRM-VLA achieves state-of-the-art performance across all tasks, significantly outperforming prior VLA and generalist policy models. Notably, TRM-VLA attains a 72.9% average success rate, surpassing the baseline method [22] by +21.6%. This substantial gain underscores the effectiveness of our temporal-aware reasoning and memory framework in long-horizon manipulation. 

We further evaluate TRM-VLA on the LIBERO-90 benchmark [28]. As shown in Table 1, TRM-VLA achieves a new state-of-the-art success rate of 94.8%, surpassing all prior methods by a significant margin. Notably, TRM-VLA outperforms the baseline model, CogACT-Base (88.4%), by +6.4%, and exceeds strong contemporaries like _π_ 0-Fast (83.1%) and UniACT (73.0%). This demonstrates that our framework excels at complex, multi-stage tasks requiring sustained planning and temporal awareness. 

**Real-World Evaluation** . We evaluate TRM-VLA on four challenging real-world manipulation tasks designed to probe distinct aspects of embodied reasoning: Place Toy Bear into Box (precision grasping), Push Buttons in Order (memorydependent sequencing), Clean Table (long-horizon planning), and Scoop Washers using Shovel (tool use). As shown in Tab. 3, TRM-VLA achieves the highest success rate across all four tasks, outperforming strong baselines. 

On Push Buttons in Order, which demands explicit memory of the button sequence, TRM-VLA achieves a 67% success rate, significantly surpassing CogACT-ECoT’s 45%. This gain underscores the effectiveness of our GCM module in preserving and leveraging historical reasoning traces. On Clean Table, a multi-step, long-horizon task involving object clearing, TRM-VLA attains a 72% success rate, compared to 41% for CogACT-ECoT. This highlights the benefit of our hierarchical, coarse-to-fine reasoning via KTR, which enables sustained planning over extended task horizons. Furthermore, TRM-VLA exhibits superior inference efficiency: it generates only 4.3 CoT tokens per step on average, a dramatic reduction compared to ECoT (26.8). This efficiency stems from our key design principle: triggering reasoning only at critical frames rather than generating full CoT at every timestep. This reduces computation and mitigates context pollution, allowing the policy to focus on essential decision points. As shown in Fig. 4, our method accurately identifies keyframes, and the generated hierarchical CoT 

> 1More details about **dataset** , **metrics** , **implementation details** , holistic ablations, visualizations, and related works are available in the **Appendix** . 

10948 


Figure 3. Cross-task, cross-embodiment evaluation environments: Simpler-Env [23] with WidowX robot, LIBERO-90 [28] with Franka robot, and real-world tasks based on AIRBOT Player robot, focusing on manipulation accuracy, tool-using, temporal memory, and long-horizon. 

|Mdl|Pbliti|Put S|poon|Put C|arrot|Stack|Cube|Put Eg|gplant|ASR(%)_↑_|
|---|---|---|---|---|---|---|---|---|---|---|
|oe|ucaon|Grasp(%)|SR(%)|Grasp(%)|SR(%)|Grasp(%)|SR(%)|Grasp(%)|SR(%)|vg.|
|RT-1-X [5]|ICRA 2024|16.7|0.0|20.8|4.2|8.3|0.0|0.0|0.0|1.1|
|OpenVLA [18]|CoRL 2025|4.1|4.2|33.3|0.0|12.5|0.0|8.3|4.1|1.0|
|SpatialVLA [38]|Arxiv 2024|20.8|16.7|29.2|25.0|62.5|29.2|**100.0**|**100.0**|42.7|
|Magma [46]|CVPR 2025|-|37.5|-|29.2|-|20.8|-|91.7|44.8|
|_π_0-Fast [36]|Arxiv 2025|-|29.1|-|21.9|-|10.8|-|66.6|32.1|
|Octo-Base [31]|ICRA 2024|34.7|12.5|52.8|8.3|31.9|0.0|66.7|43.1|17.5|
|TraceVLA [55]|ICLR 2025|-|12.5|-|16.6|-|16.6|-|65.0|27.7|
|RoboVLM [24]|Arxiv 2025|70.8|45.8|33.3|20.8|54.2|4.2|91.7|79.2|37.5|
|CogACT-Base [22]|Arxiv 2025|79.2|71.7|66.7|50.8|54.2|15.0|75.0|67.5|51.3|
|_π_0 [4]|CoRL 2025|-|**83.8**|-|52.5|-|**52.5**|-|87.9|69.2|
|TRM-VLA|——|**91.7**<sup>_±._08</sup>|83.3<br>_±._08|**79.2**<sup>_±._04</sup>|**75.0**<sup>_±._04</sup>|**79.2**<sup>_±._04</sup>|41.7<br>_±._04|91.7<br>_±._08|91.7<br>_±._08|**72.9**<sup>_±._04 </sup>(+21.6)|


Table 1. Quantitative comparison with SOTA methods on SimplerEnv-Bridge benchmark. ‘SR’ indicates the success rates. 

|Method|Publication|Success Rate(%)|
|---|---|---|
|SpatialVLA [38]|Arxiv 2025|46.2|
|OpenVLA [18]|CoRL 2025|73.5|
|UniACT [54]|CVPR 2025|73.0|
|CogACT-Base [22]|Arxiv 2025|88.4|
|CogACT-ECoT [50]|CoRL 2025|92.1|
|_π_0-Fast [36]|Arxiv 2025|83.1|
|TRM-VLA|——|**94.8**(+6.4)|


Table 2. Comparison with SOTA methods on LIBERO-90. 

aligns well with the actual actions. Refer to the appendix. 

**Out-of-Distribution Evaluation** . We evaluate robustness under real-world distribution shifts, including changes in lighting, background, distractors, spatial layout, and camera pose. As shown in Fig. 5, TRM-VLA consistently outperforms the CogACT baseline [22]. The bar charts quantify the drop in success count ( _−_ ∆ success count) under each 


Figure 4. Qualitative Results on real-world evaluation. The TRMVLA model adaptively triggers reasoning at critical frames. 

shift, where a lower value indicates better robustness. In “Push Buttons in Order” task, which requires memory and 

10949 

|Model|Place Toy<br>Progress(%)|Bear<br> Success|Push Buttons<br> Progress(%)|in Order<br> Success|Clean the<br> Progress(%)|Table<br> Success|Scoop W<br> Progress(%|ashers<br>) Success|Avg. SR(%)_↑_|Avg. Tokens_↓_|
|---|---|---|---|---|---|---|---|---|---|---|
|OpenVLA [18]|0.40|6/20|0.21|3/20|0.15|2/20|0.30|6/20|21.0|7.0|
|CogACT-Base[22]|0.56|10/20|0.51|9/20|0.37|7/20|0.70|14/20|50.0|1.0|
|ECoT [50]|0.42|7/20|0.27|5/20|0.18|3/20|0.35|7/20|28.0|26.8|
|CogACT-ECoT [50]|0.52|8/20|0.45|8/20|0.41|6/20|0.60|12/20|44.0|26.3|
|TRM-VLA|0.77|15/20|0.67|12/20|0.72|11/20|0.85|17/20|69.0|4.3|


Table 3. Quantitative comparison with SOTA methods on real-world tasks. ‘SR’ indicates the success rates. ’Tokens’ denotes the average number of generated CoT tokens per step, and ’Progress’ is the average completion progress of the task. 


Figure 5. Qualitative Results on generalization evaluation. 

sequential reasoning, CogACT’s success drops by 7 trials under camera pose variation, while TRM-VLA’s drop is only 4. Similarly, on “Clean the Table,” a long-horizon task, TRM-VLA maintains higher stability under lighting and background changes. This enhanced robustness arises from temporal memory aggregation: by fusing past reasoning traces, TRM-VLA maintains a consistent understanding of the task goal even when perceptual cues vary. It thus focuses on semantic and procedural invariants rather than transient visual features, enabling stronger generalization. 

### **4.3. Ablation Study** 

**Inference Efficiency** . Since all compared models share the same backbone [16], generated CoT tokens per timestep serve as a direct proxy for computational cost. As shown in Tab. 1, our TRM-VLA achieves superior efficiency: it generates only 4.3 tokens per step, a dramatic reduction compared to prior reasoning-augmented models. For instance, while ECoT (the reasoning version of OpenVLA) improves the success rate over its base model, it incurs a 3.8x increase in token generation (7.0 vs. 26.8). Similarly, CogACT-ECoT builds upon CogACT-Base but increases the tokens from 1.0 to 26.3. In contrast, TRM-VLA achieves a trade-off between performance and efficiency. This efficiency stems from our design principle of triggering reasoning only at critical frames, thereby avoiding redundant computation. **Effectiveness of KTR and GCM** . As shown in Tab. 4 and Tab. 5, both KTR and GCM modules are essential. On the SIMPLER, removing either KTR (ID a) or GCM (ID c) 

|ID<br>|KTR<br>KBA STS|GC<br>DRC|M<br>TRI|Put<br>Spoon|Put<br>Carrot|Stack<br>Cube|Put<br>Eggplan|Avg. SR<br>t|
|---|---|---|---|---|---|---|---|---|
|(a)|✗<br>✗|✗|✗|0.67|0.63|0.21|0.67|0.54|
|(b)|✗<br>✓|✗|✗|0.75|0.50|0.33|0.83|0.60|
|(c)|✓<br>✓|✗|✗|0.83|0.58|0.25|0.92|0.65|
|(d)|✓<br>✓|✗|✓|0.92|0.63|0.29|0.92|0.69|
|(e)|✓<br>✓|✓|✗|**0.92**|0.63|0.25|**1.00**|0.70|
|(f)|✓<br>✓|✓|✓|0.83|**0.75**|**0.42**|0.92|**0.73**|
|T|able 4. Ab|latio|n stu|dy of K|TR an|d GC|M on SIM|PLER.|
|ID|KTR G|CM|<sup>Plac</sup><br>Bea|<sup>e</sup><br>Pu<br>r<br>But|sh<br>C<br>ton<br>T|lean<br>able|Scoop<br>Washer|Avg. SR|
|(a)|✗|✗|0.5|0<br>0.|45<br>0|.35|0.7|0.50|
|(b)|✓|✗|0.7|0<br>0.|45<br>0|.45|0.75|0.59|
|(c)|✓|✓|**0.7**|**5**<br>**0.**|**6**<br>**0**|**.55**|**0.85**|**0.69**|


Table 5. Ablation study of KTR and GCM on real-world evaluation. 

leads to a significant drop in SR from 0.73 to 0.65 and 0.54, respectively. This confirms that both temporal reasoning and memory are essential for long-horizon task completion. Comparing (a)(b)(c), within KTR, the Stage-wise Temporal Structuring (STS) and Keyframe-based Annotation (KBA) each improve SR by +6%/+5%, suggesting the effectiveness of structuring reasoning hierarchically and triggering it at keyframes. Comparing (d)(e)(f), within GCM, Dynamic Reasoning Context (DRC) and Temporal Reasoning Integration (TRI) further improve the SR by +4%/+5%, highlighting the importance of memory buffer and cross-attention retrieval. 

## **5. Conclusion** 

We present TRM-VLA, a novel Vision-Language-Action framework that integrates temporal-aware reasoning and explicit memory into robotic policy learning. By triggering hierarchical chain-of-thought reasoning only at critical decision points and dynamically maintaining a structured memory of past reasoning traces, TRM-VLA achieves strong performance on long-horizon, memory-intensive manipulation tasks while drastically reducing computational overhead. Extensive experiments across simulated and real-world benchmarks demonstrate that our method sets new state-of-the-art results in both success rate and inference efficiency. We hope TRM-VLA will serve as a foundation for future work on temporally grounded, memory-augmented agents that reason strategically and act efficiently in complex environments. 

10950 

## **6. Acknowledgement** 

This work is supported by the research fund under Grant No. 20242910035 from the Tsinghua UniversityJiangsu CRRC Digital Technology Co.,Ltd. Joint Research Center for Data Driven Intelligence of Industry. 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. <u>arXiv preprint arXiv:2303.08774, 2023.</u> 1 

- [2] AgiBot-World-Contributors, Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xu Huang, Shu Jiang, Yuxin Jiang, Cheng Jing, Hongyang Li, Jialun Li, Chiming Liu, Yi Liu, Yuxiang Lu, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. <u>arXiv preprint arXiv:2503.06669, 2025.</u> 1, 2, 3 

- [3] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang, Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5vl technical report. <u>arXiv preprint arXiv:2502.13923, 2025.</u> 1, 4, 6 

- [4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. pi0 : A vision-languageaction flow model for general robot control. <u>arXiv preprint arXiv:2410.24164, 2024.</u> 1, 2, 7 

- [5] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alexander Herzog, Jasmine Hsu, et al. RT-1: robotics transformer for real-world control at scale. In <u>Robotics: Science and Systems, 2023.</u> 1, 7 

- [6] Qingwen Bu, Hongyang Li, Li Chen, Jisong Cai, Jia Zeng, Heming Cui, Maoqing Yao, and Yu Qiao. Towards synergistic, generalized, and efficient dual-system for robotic manipulation. <u>arXiv preprint arXiv:2410.08001, 2024.</u> 1, 2, 3 

- [7] Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, Hanbo Zhang, and Minzhao Zhu. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. <u>arXiv preprint arXiv:2410.06158, 2024.</u> 3 

- [8] William Chen, Suneel Belkhale, Suvir Mirchandani, Oier Mees, Danny Driess, Karl Pertsch, and Sergey Levine. Training strategies for efficient embodied reasoning. <u>arXiv preprint arXiv:2505.08243, 2025.</u> 3, 6 

- [9] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. <u>The International Journal of Robotics Research, 2024.</u> 2 

- [10] Zhekai Duan, Yuan Zhang, Shikai Geng, Gaowen Liu, Joschka Boedecker, and Chris Xiaoxuan Lu. Fast ecot: Efficient embodied chain-of-thought via thoughts reuse. <u>arXiv preprint arXiv:2506.07639, 2025.</u> 2 

- [11] Jiayuan Gu, Sean Kirmani, Paul Wohlhart, Yao Lu, Montserrat Gonzalez Arenas, Kanishka Rao, Wenhao Yu, Chuyuan Fu, Keerthana Gopalakrishnan, Zhuo Xu, et al. Rt-trajectory: Robotic task generalization via hindsight trajectory sketches. In <u>International Conference on Learning Representations,</u> 2024. 2, 3 

- [12] Chi-Pin Huang, Yueh-Hua Wu, Min-Hung Chen, YuChiang Frank Wang, and Fu-En Yang. Thinkact: Visionlanguage-action reasoning via reinforced visual latent planning. <u>arXiv preprint arXiv:2507.16815, 2025.</u> 3 

- [13] Jialei Huang, Shuo Wang, Fanqi Lin, Yihan Hu, Chuan Wen, and Yang Gao. Tactile-vla: Unlocking vision-language-action model’s physical knowledge for tactile generalization. <u>arXiv preprint arXiv:2507.09160, 2025.</u> 3 

- [14] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. pi0.5: a vision-language-action model with open-world generalization. <u>arXiv preprint arXiv:2504.16054, 2025.</u> 1, 2, 3 

- [15] Nikita Karaev, Ignacio Rocco, Benjamin Graham, Natalia Neverova, Andrea Vedaldi, and Christian Rupprecht. Cotracker: It is better to track together. In <u>European Conference on Computer Vision, 2024.</u> 4 

- [16] Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models. <u>arXiv preprint arXiv:2402.07865, 2024.</u> 1, 2, 8 

- [17] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. In <u>Proceedings of Robotics: Science and Systems, 2024.</u> 2 

- [18] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. OpenVLA: An open-source visionlanguage-action model. In <u>Conference on Robot Learning,</u> 2024. 1, 2, 7, 8 

- [19] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. <u>arXiv preprint arXiv:::2502.19645, 2025.</u> 1 

- [20] Jason Lee, Jiafei Duan, Haoquan Fang, Yuquan Deng, Shuo Liu, Boyang Li, Bohan Fang, Jieyu Zhang, Yi Ru Wang, Sangho Lee, Winson Han, Wilbert Pumacay, Angelica Wu, Rose Hendrix, Karen Farley, Eli VanderBilt, Ali Farhadi, Dieter Fox, and Ranjay Krishna. Molmoact: Action reasoning models that can reason in space. <u>arXiv preprint arXiv:2508.07907, 2025.</u> 3 

- [21] Hao-Si Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang, Tianxing Chen, Ganqu Cui, Dehui Wang, Dingxiang Luo, Yuchen 

10951 

Fan, Youbang Sun, Jia Zeng, Jiangmiao Pang, Shanghang Zhang, Yu Wang, Yao Mu, Bowen Zhou, and Ning Ding. Simplevla-rl: Scaling vla training via reinforcement learning. <u>arXiv preprint arXiv:2509.09674, 2025.</u> 3 

- [22] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, Xiaofan Wang, Bei Liu, Jianlong Fu, Jianmin Bao, Dong Chen, Yuanchun Shi, Jiaolong Yang, and Baining Guo. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. <u>arXiv preprint arXiv:2411.19650, 2024.</u> 1, 2, 3, 6, 7, 8 

- [23] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea Finn, Hao Su, Quan Vuong, and Ted Xiao. Evaluating real-world robot manipulation policies in simulation. <u>arXiv preprint arXiv:2405.05941, 2024.</u> 2, 6, 7 

- [24] Xinghang Li, Peiyan Li, Minghuan Liu, Dong Wang, Jirong Liu, Bingyi Kang, Xiao Ma, Tao Kong, Hanbo Zhang, and Huaping Liu. Towards generalist robot policies: What matters in building vision-language-action models. <u>arXiv preprint arXiv:2412.14058, 2024.</u> 7 

- [25] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, Hang Li, and Tao Kong. Vision-language foundation models as effective robot imitators. In <u>International Conference on Learning Representations, 2024.</u> 1 

- [26] Yi Li, Yuquan Deng, Jesse Zhang, Joel Jang, Marius Memmel, Caelan Reed Garrett, Fabio Ramos, Dieter Fox, Anqi Li, Abhishek Gupta, and Ankit Goyal. HAMSTER: hierarchical action models for open-world robot manipulation. In <u>International Conference on Learning Representations, 2025.</u> 2, 3 

- [27] Fanqi Lin, Ruiqian Nai, Yingdong Hu, Jiacheng You, Junming Zhao, and Yang Gao. Onetwovla: A unified visionlanguage-action model with adaptive reasoning. <u>arXiv preprint arXiv:2505.11917, 2025.</u> 2 

- [28] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. In <u>Advances in Neural Information Processing Systems, pages 44776–44791, 2023.</u> 6, 7 

- [29] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. RDT-1b: a diffusion foundation model for bimanual manipulation. In <u>International Conference on Learning Representations, 2025.</u> 1, 2 

- [30] Nvidia, Johan Bjorck, Fernando Castaneda, Nikita Cherniadev, Xingye Da, Runyu Ding, LinxiJimFan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyuan Jiang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. <u>arXiv preprint arXiv:2503.14734, 2025.</u> 2 

- [31] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted 

Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In <u>Proceedings of Robotics: Science and Systems, Delft, Netherlands, 2024.</u> 1, 

7 

- [32] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, Albert Tung, et al. Open x-embodiment: Robotic learning datasets and RT-X models : Open x-embodiment collaboration. In <u>IEEE International Conference on Robotics and Automation,</u> pages 6892–6903, 2024. 2 

- [33] Maxime Oquab, Timothee Darcet, Th´ eo Moutakanni, Huy Vo,´ Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without supervision. <u>arXiv preprint arXiv:2304.07193, 2023.</u> 3 

- [34] William S. Peebles and Saining Xie. Scalable diffusion models with transformers. <u>International Conference on Computer Vision, pages 4172–4182, 2023.</u> 2, 4, 5 

- [35] Ethan Perez, Florian Strub, Harm de Vries, Vincent Dumoulin, and Aaron C. Courville. Film: Visual reasoning with a general conditioning layer. In <u>Proceedings of the AAAI Conference on Artificial Intelligence, 2017.</u> 4, 5 

- [36] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. <u>arXiv preprint arXiv:2501.09747,</u> 2025. 2, 7 

- [37] Delin Qu, Haoming Song, Qizhi Chen, Zhaoqing Chen, Xianqiang Gao, Xinyi Ye, Qi Lv, Modi Shi, Guanghui Ren, Cheng Ruan, Maoqing Yao, Haoran Yang, Jiacheng Bao, Bin Zhao, and Dong Wang. Embodiedonevision: Interleaved vision-textaction pretraining for general robot control. <u>arXiv preprint arXiv:2508.21112, 2025.</u> 2, 3 

- [38] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yani Ding, Zhigang Wang, Jiayuan Gu, Bin Zhao, Dong Wang, and Xuelong Li. Spatialvla: Exploring spatial representations for visual-language-action model. <u>arXiv preprint arXiv:2501.15830, 2025.</u> 7 

- [39] Hao Shi, Bin Xie, Yingfei Liu, Lin Sun, Fengrong Liu, Tiancai Wang, Erjin Zhou, Haoqiang Fan, Xiangyu Zhang, and Gao Huang. Memoryvla: Perceptual-cognitive memory in vision-language-action models for robotic manipulation. <u>arXiv preprint arXiv:2508.19236, 2025.</u> 2 

- [40] Haoming Song, Delin Qu, Yuanqi Yao, Qizhi Chen, Qi Lv, Yiwen Tang, Modi Shi, Guanghui Ren, Maoqing Yao, Bin Zhao, Dong Wang, and Xuelong Li. Hume: Introducing system-2 thinking in visual-language-action model. <u>arXiv preprint arXiv:2505.21432, 2025.</u> 2 

- [41] Gemini Team, Saminda Abeyruwan, Joshua Ainslie, JeanBaptiste Alayrac, Montse Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza,´ et al. Gemini robotics: Bringing ai into the physical world. <u>arXiv preprint arXiv:2503.20020, 2025.</u> 1, 2 

- [42] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: 

10952 

Open foundation and fine-tuned chat models. <u>arXiv preprint arXiv:2307.09288, 2023.</u> 4 

- [43] Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In <u>Conference on Robot Learning, pages 1723–1736, 2023.</u> 2, 6 

- [44] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-ofthought prompting elicits reasoning in large language models. <u>Advances in Neural Information Processing Systems, 35:</u> 24824–24837, 2022. 1 

- [45] Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. Dexvla: Vision-language model with plug-in diffusion expert for general robot control. <u>arXiv preprint arXiv:2502.05855, 2025.</u> 2 

- [46] Jianwei Yang, Reuben Tan, Qianhui Wu, Ruijie Zheng, Baolin Peng, Yongyuan Liang, Yu Gu, Mu Cai, Seonghyeon Ye, Joel Jang, Yuquan Deng, Lars Liden, and Jianfeng Gao.´ Magma: A foundation model for multimodal ai agents. <u>Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 14203–14214, 2025.</u> 3, 7 

- [47] Shuai Yang, Hao Li, Yilun Chen, Bin Wang, Yang Tian, Tai Wang, Hanqing Wang, Feng Zhao, Yiyi Liao, and Jiangmiao Pang. Instructvla: Vision-language-action instruction tuning from understanding to manipulation. <u>arXiv preprint arXiv:2507.17520, 2025.</u> 2, 3 

Zhang, and Xianyuan Zhan. Universal actions for enhanced embodied foundation models. <u>Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition,</u> pages 22508–22519, 2025. 7 

   - [55] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daume III, Andrey Kolobov, Furong Huang, and Jianwei´ Yang. Tracevla: Visual trace prompting enhances spatialtemporal awareness for generalist robotic policies. <u>arXiv preprint arXiv:2412.10345, 2024.</u> 7 

   - [56] Zhongyi Zhou, Yichen Zhu, Junjie Wen, Chaomin Shen, and Yi Xu. Chatvla-2: Vision-language-action model with openworld embodied reasoning from pretrained knowledge. <u>arXiv preprint arXiv:2505.21906, 2025.</u> 1, 2, 3 

   - [57] Minjie Zhu, Yichen Zhu, Jinming Li, Zhongyi Zhou, Junjie Wen, Xiaoyu Liu, Chaomin Shen, Yaxin Peng, and Feifei Feng. Objectvla: End-to-end open-world object manipulation without demonstration. <u>arXiv preprint arXiv:2502.19250,</u> 2025. 3 

   - [58] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. RT-2: vision-language-action models transfer web knowledge to robotic control. In <u>Conference on Robot Learning, pages 2165–2183, 2023.</u> 1, 2 

- [48] Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Se June Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar, Reuben Tan, YuWei Chao, Bill Yuchen Lin, Lars Liden, Kimin Lee, Jianfeng Gao, Luke Zettlemoyer, Dieter Fox, and Minjoon Seo. Latent action pretraining from videos. In <u>International Conference on Learning Representations, 2025.</u> 2, 3 

- [49] Yifu Yuan, Haiqin Cui, Yaoting Huang, Yibin Chen, Fei Ni, Zibin Dong, Pengyi Li, Yan Zheng, and Jianye Hao. Embodied-r1: Reinforced embodied reasoning for general robotic manipulation. <u>arXiv preprint arXiv:2508.13998,</u> 2025. 3 

- [50] Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. In <u>Conference on Robot Learning, pages 3157–3181. PMLR, 2025.</u> 2, 3, 4, 6, 7, 8 

- [51] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In <u>Proceedings of the IEEE International Conference on Computer Vision, pages 11975–11986, 2023.</u> 3 

- [52] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In <u>Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 2025.</u> 2, 3 

- [53] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3d-vla: A 3d vision-language-action generative world model. <u>arXiv preprint arXiv:2403.09631, 2024.</u> 3 

- [54] Jinliang Zheng, Jianxiong Li, Dongxiu Liu, Yinan Zheng, Zhihao Wang, Zhonghong Ou, Yu Liu, Jingjing Liu, Ya-Qin 

10953 

