---
title: "SemanticVLA: Towards Semantic Reasoning over Action Memorization via Synergistic Explicit Trace and Latent Action Planning"
date: "2026"
venue: "CVPR 2026"
url: https://openaccess.thecvf.com/content/CVPR2026/html/Ni_SemanticVLA_Towards_Semantic_Reasoning_over_Action_Memorization_via_Synergistic_Explicit_CVPR_2026_paper.html
pdf: https://openaccess.thecvf.com/content/CVPR2026/papers/Ni_SemanticVLA_Towards_Semantic_Reasoning_over_Action_Memorization_via_Synergistic_Explicit_CVPR_2026_paper.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://openaccess.thecvf.com/content/CVPR2026/papers/Ni_SemanticVLA_Towards_Semantic_Reasoning_over_Action_Memorization_via_Synergistic_Explicit_CVPR_2026_paper.pdf)** / [論文ページ](https://openaccess.thecvf.com/content/CVPR2026/html/Ni_SemanticVLA_Towards_Semantic_Reasoning_over_Action_Memorization_via_Synergistic_Explicit_CVPR_2026_paper.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **SemanticVLA: Towards Semantic Reasoning over Action Memorization via Synergistic Explicit Trace and Latent Action Planning** 


Figure 1. **SemanticVLA Overview.** Current VLA models struggle with instruction variations and reasoning-intensive tasks, often memorizing patterns rather than understanding semantics. We introduce a dual-path architecture that generates explicit trace reasoning as interpretable spatial waypoints alongside implicit latent action tokens as compact visuomotor primitives. Built on our curated TraceX240K with trace-annotated trajectories, SemanticVLA demonstrates robust performance and strong generalization across simulation and real-world deployment, maintaining stable success rates under instruction rephrasing where baselines degrade significantly. 

## **Abstract** 

_Vision-Language-Action (VLA) models have emerged as a promising paradigm where pretrained Vision-Language Models (VLMs) serve as System 2 for high-level reasoning, connected to action experts as System 1 for low-level motor control. However, current works fail to genuinely leverage VLM capabilities: VLMs produce latent embeddings that lack semantic interpretability, providing ambiguous and unstable guidance to downstream policies, while solely action supervision further causes VLMs to degenerate into parameter-heavy fusion encoders that memorize action patterns rather than perform generalized reasoning. To bridge this gap, we introduce SemanticVLA, which leverages VLM reasoning through synergistic dual-path design. Explicit trace reasoning generates interpretable spatial waypoints as textual coordinate sequences through the VLM’s native language interface, directly reusing its pretrained spatial grounding to provide a "thinking process" for task planning. Latent action tokens complement trace reasoning by learning compact visuomotor primitives grounded in visual observations, providing more fine-grained action_ 

_representations beyond pure coordinate prediction. This synergy enables trace reasoning to leverage VLM’s multimodal understanding for refining latent token prediction, while latent tokens provide stable and grounded guidance that compensates for trace’s numerical sensitivity. SemanticVLA achieves 97.0% average success rate on LIBERO and 65.1% on SimplerEnv WidowX, substantially outperforming strong baselines. More importantly, SemanticVLA maintains significantly more stable performance under instruction rephrasing in both simulation suites, and demonstrates strong advantages on real-world long-horizon and reasoning-intensive tasks. By bridging VLM reasoning and action expert through semantically explicit trace and visually grounded latent action tokens, our approach enables semantic reasoning rather than action memorization._ 

## **1. Introduction** 

Large-scale pretraining has fundamentally transformed vision-language understanding, enabling Vision-Language Models (VLMs) to excel at multimodal reasoning across diverse domains [15, 29]. Extending these capabilities to robotic manipulation, Vision-Language-Action (VLA) models [5, 6, 26, 38] have emerged as a promising paradigm where pretrained VLMs serve as System 2 for high-level 

> _†_ Corresponding authors. 

12237 

reasoning while specialized action experts act as System 1 for low-level motor control [1, 3, 4]. However, current VLA implementations fail to genuinely leverage VLM reasoning capabilities. Recent studies reveal critical brittleness under instruction rephrasing [17, 18] and sharp performance drops on reasoning-intensive tasks [35, 49]—VLAs succeed at direct instructions like "place the sponge on card number 5" but fail at semantically equivalent forms like "place the sponge on the answer to the math problem on whiteboard", exposing a key dilemma that current VLAs rely on _memorized action patterns_ rather than _genuine reasoning_ . 

This brittleness stems from two fundamental limitations in current VLA architectures. First, action loss gradients backpropagating through VLM parameters optimize for task-specific pattern matching at the expense of semantic reasoning, degrading compositional understanding capabilities. Second, the interface between VLM and action expert relies on opaque latent embeddings without explicit supervision. Under sole action supervision, these representations rapidly drift toward action fitting, inevitably degrading pretrained foundation models into parameter-heavy fusion encoders rather than genuine reasoning systems. Existing approaches address these issues through complementary strategies. Co-training methods [4, 9, 44, 49, 57] preserve VLM capabilities by balancing multimodal data with manipulation tasks, while latent action approaches [7, 10, 47, 47, 50] inject semantics through grounded action tokens bridging VLM and action expert. However, these strategies involve fundamental tradeoffs. Co-training attempts to _retain_ but still fails to effectively _leverage_ VLM reasoning, while latent tokens risk memorizing action patterns rather than engaging in reasoning. This raises a fundamental question: _How can we design an interface that genuinely exploits VLM’s native reasoning capabilities while providing stable, semantically-grounded guidance to action expert?_ 

To this end, we introduce SemanticVLA, a dual-path reasoning framework that synergistically combines explicit trace reasoning and latent action planning. Our key insight is that trace prediction naturally aligns with VLM’s native spatial grounding capabilities, serving as interpretable reasoning that explicitly surfaces manipulation planning while providing auxiliary supervision to refine latent action learning. This synergy enables trace to leverage VLM’s compositional reasoning for structured waypoint generation, while latent tokens learn compact, semantically-rich visuomotor primitives by fusing trace intension with visual observations, achieving both interpretability through explicit coordinates and robustness through compact latent action. To enable large-scale pretraining, we curate TraceX-240K, a comprehensive trace-annotated dataset containing 240K robot trajectories from multiple sub-datasets [5, 16, 22] in Open X-Embodiment [12] and DROID [25], with automated trace extraction providing dense spatial annotations. 

Building on TraceX-240K, our three-stage training pipeline reflects this design philosophy. We first pretrain latent tokens with trace-guided supervision, learning clean spatialtemporal patterns without language contamination. We then co-train the VLM to jointly predict traces and latent tokens without action decoding, establishing their semantic correspondence. Finally, we finetune the action expert with weak VLM regularization, ensuring action adaptation preserves reasoning capabilities. Comprehensive evaluations demonstrate SemanticVLA achieves 97.0% success rate on LIBERO and 65.1% on SimplerEnv WidowX, substantially outperforming strong baselines. More importantly, SemanticVLA maintains significantly more stable performance than baselines under instruction rephrasing in both LIBERO and SimplerEnv, and shows strong advantages on real-world long-horizon and reasoning-intensive tasks. By bridging VLM reasoning and action control through semantically explicit trace and compact latent action tokens, our approach enables genuine reasoning rather than action memorization. Our contributions are summarized as follows: 

- We propose **SemanticVLA** , a _dual-path VLA framework_ that synergistically combines explicit trace reasoning with implicit latent action planning, genuinely leveraging VLM’s native spatial reasoning for interpretable geometric guidance while providing semantically-grounded action representations for robust control. 

- We curate _TraceX-240K_ , a large-scale trace-annotated dataset, and introduce a _trace-guided training strategy_ where spatial traces serve as both semantic supervision for latent action pretraining and auxiliary reasoning during VLM co-training, ensuring clean separation between flexible VLM reasoning and precise action control. 

- SemanticVLA demonstrates _genuine reasoning over pattern memorization_ , achieving robust generalization under instruction rephrasing and visual perturbations in simulators and real experiments, through compositional reasoning rather than memorized linguistic-action correlations. 

## **2. Related Work** 

**Vision-Language-Action Models** Vision-LanguageAction (VLA) models extend pretrained VLMs to robot control, evolving from autoregressive token-based approaches [5, 26, 43] toward specialized action experts via diffusion or flow matching [1, 3, 4, 38] for faster, continuous action generation. However, this dual-system architecture introduces a critical challenge: action loss gradients backpropagating through the VLM backbone degrade its pretrained semantic capabilities [14, 21]. To mitigate this degradation, recent works [21, 35, 44, 49, 56] incorporate general-domain multimodal data during cotraining to jointly optimize VLM understanding with action prediction through instruction tuning. Nevertheless, these works primarily focus on retain reasoning capabilities 

12238 

rather than genuinely utilizing them. VLMs in current frameworks produce latent embeddings that lack semantic interpretability, causing pretrained models to degenerate into parameter-heavy fusion encoders correlating visual patterns with actions rather than performing compositional reasoning, which highlight the need to explicitly activate VLMs’ native multimodal reasoning for robot control. **Spatial Trace Reasoning** Recent works explore intermediate representations—ranging from visual subgoals [39, 40, 53] to explicit spatial waypoints [2, 51, 55]—to enhance VLA manipulation planning. TraceVLA [55] overlays historical trajectories as visual prompts for spatialtemporal awareness. Subsequent works predict future traces as intermediate control representations: HAMSTER [33] and Magma [48] generate 2D waypoints to condition lowlevel policies through hierarchical architectures, while MolmoAct [30] treats trace prediction as auxiliary reasoning within VLM’s language interface, generating waypoints alongside action tokens to refine spatial understanding. However, both approaches inherit trace’s numerical sensitivity—coordinate prediction errors compound without visual compensation. This motivates our dual-path architecture: explicit trace preserves interpretable spatial reasoning through VLM’s native interface, while implicit latent action tokens provide visually-grounded execution that stabilizes against coordinate imprecision. 

**Latent Action Representations.** Latent action tokens provide compact representations for efficient vocabulary integration into VLMs. Early action-based methods [31, 37, 47] apply vector quantization to raw action trajectories, compressing continuous actions into discrete tokens that reduce dimensionality but lack high-level manipulation semantics. To inject semantic meaning, vision-based methods [13, 34, 50] incorporate language instructions during visual reconstruction, training models to predict future frames conditioned on latent codes and task descriptions to capture semantically-grounded state transitions. However, pure visual reconstruction risks entangling task-irrelevant appearance variations into latent actions—while UniVLA [8] attempts using task language as an intermediate modality to filter such variations through two-stage training, linguistic biases inevitably persist. This motivates using spatial trace as explicit reconstruction target for latent action learning: as a precise geometric carrier, trace provides both semantic grounding and visual observation alignment without relying on language contamination. 

## **3. Method** 

We present SemanticVLA, a dual-path Vision-LanguageAction framework that synergistically combines explicit trace reasoning with implicit latent action semantics. Our approach consists of three stages: ( **1** ) _Semantic Latent Token Pretraining_ (Sec. 3.1), where spatial trace priors guide 

visually-grounded action representations without language contamination; ( **2** ) _VLM Co-training with Trace and Latent Action_ (Sec. 3.2), where both pathways mutually reinforce through joint optimization; and ( **3** ) _Flow Matching Action Decoding_ (Sec. 3.3), mapping latent representations to continuous actions. Throughout our design, we maintain a critical principle: _the VLM provides clean semantic guidance through structured trace coordinates and compact latent tokens, while avoiding direct exposure to raw action supervision that degrades reasoning capabilities_ . 

### **3.1. Semantic Latent Action Tokenizer** 

While compact latent action tokens offer efficient robot learning interfaces [46, 54], existing approaches—whether learning from raw actions [31, 37, 47] or visual reconstruction [13, 34, 50]—entangle task-relevant primitives with appearance variations, lacking semantic grounding in manipulation intent. Attempts at semantic injection through language conditioning [8] introduce fundamental limitations: linguistic variability risks overfitting to specific phrasings rather than style-invariant primitives, while temporal misalignment emerges when trajectory-level descriptions condition token-level representations. _Fundamentally, using language as the conditioning anchor introduces inherent variability bias into latent action learning._ 

To bridge this gap, we propose leveraging _spatial trace priors as explicit supervision_ to guide latent action learning while excluding language from pretraining. Our key insight is that traces, as structured spatial waypoints, provide temporally-aligned and unambiguous guidance superior to language. Each trace aligns perfectly with its corresponding action window, ensuring temporal consistency. More importantly, traces represent geometric invariants that remain stable across diverse linguistic expressions, naturally encoding manipulation semantics through spatial structure rather than linguistic variability. Specifically, we design a two-stage VQ-VAE framework where the first stage learns stable geometric anchors from pure trace coordinates, while the second stage grounds these anchors into visual observations for clean, transferable manipulation semantics. **Trace-level geometric abstraction.** The first VQ-VAE operates purely on coordinate sequences, deliberately excluding visual observations to avoid entangling spatial structure with appearance variations. Given trace _τ_ = ( _p_ 1 _, . . . , pL_ ) where _pi_ = ( _ui, vi_ ) _∈_ [0 _,_ 1]<sup>2</sup> , we train encoder _ϕ_<sup>trace</sup> enc<sup>and</sup> decoder _ϕ_<sup>trace</sup> dec<sup>with temporal convolutions to extract spatial-</sup> temporal dynamics: 


= Supervised by reconstruction loss _L_<sup>trace</sup> vq _∥τ − ϕ_<sup>trace</sup> dec<sup>(</sup><sup>**c**trace</sup> _q_ trace<sup>)</sup><sup>_∥_2 +</sup><sup>_β∥_sg(</sup><sup>**z**trace)</sup><sup>_−_</sup><sup>**c**trace</sup> _q_ trace<sup>_∥_2, the codebook learns</sup> pure geometric manipulation primitives (e.g., grasping arcs, placing motions) invariant to appearance, lighting, and 

12239 


Figure 2. **Semantic Latent Action Tokenizer.** Two-stage architecture for trace-guided latent tokens. Stage 1 learns geometric patterns from traces. Stage 2 grounds them in visual observations, with dual reconstruction of trace and visual representations producing latent actions with both spatial and visual semantics. 

understanding for interpretable planning, while latent tokens offer compact, visually-grounded execution that compensates for trace’s numerical sensitivity. Critically, this cotraining stage requires no ground-truth robot actions, with supervision derived purely from spatial traces and the pretrained latent vocabulary, shown in Figure 3. 

**Trace as structured spatial reasoning.** Following MolmoAct [30], we generate traces as normalized 2D coordinate sequences through the VLM’s native language interface as textual tokens. This design directly exploits VLM’s inherent spatial grounding capabilities acquired during vision-language pretraining without requiring architectural modifications. Given observation _ot_ and instruction _ℓt_ , the VLM autoregressively predicts waypoints: 


scene layout. These clean geometric priors provide a stable anchor for the subsequent visual grounding stage. 

**Visual grounding with geometric scaffolding.** However, trace-level tokens remain blind to visual context and cannot identify objects or their locations. The second VQ-VAE bridges this gap by fusing geometric patterns with scenespecific visual semantics. We extract DINOv2 [42] features **h** visual from observations _ot, ot_ + _H_ , then combine with trace codebook entry **c**<sup>trace</sup> _q_ trace<sup>through fusion encoder</sup><sup>_ϕ_</sup> enc<sup>fused</sup> employing cross-attention, where geometric priors dynamically attend to task-relevant visual regions while suppressing background clutter. The fused representation is quantized to produce final latent action tokens **e** _a_ = **c**<sup>_a_</sup> _qa_<sup>:</sup> 


To ensure **e** _a_ preserves both geometric structure and visual semantics, we employ dual reconstruction supervision. Trace decoder _ϕ_<sup>spatial</sup> dec enforces geometric precision via _L_<sup>trace</sup> recon<sup>=</sup><sup>_∥ϕ_spatial</sup> dec ( **e** _a_ ) _− τ ∥_<sup>2</sup> , while visual decoder _ϕ_<sup>visual</sup> dec enforces semantic understanding via _L_<sup>visual</sup> recon<sup>=</sup><sup>_∥ϕ_visual</sup> dec<sup>(</sup><sup>**e**</sup><sup>_a_)</sup><sup>_−_</sup> **h**<sup>_t_</sup> visual<sup>+</sup><sup>_H∥_2. Both decoders are discarded after pretraining. The</sup> training objective of latent action tokenizer _L_ LAT combines: 

_L_ LAT = _L_<sup>_a_</sup> vq<sup>+</sup><sup>_L_</sup> recon<sup>trace+</sup><sup>_L_visual</sup> recon (3) where _L_<sup>_a_</sup> vq = _∥_ sg( _ϕ_<sup>fused</sup> enc<sup>(</sup><sup>_·_))</sup><sup>_−_</sup><sup>**c**</sup><sup>_a_</sup> _qa_<sup>_∥_2+</sup><sup>_β∥ϕ_</sup> enc<sup>fused(</sup><sup>_·_)</sup><sup>_−_</sup> sg( **c**<sup>_a_</sup> _qa_<sup>)</sup><sup>_∥_2isthestandardVQloss.Thissequentialdesign</sup> ensures geometric structure remains clean and transferable while visual grounding provides scene-specific adaptation. The resulting **e** _a_ captures both where to move from geometric priors and how to manipulate from visual features through language-free, temporally-aligned supervision. 

### **3.2. VLM Co-training with Trace and Latent Action** 

Having obtained trace-guided latent tokens from pretraining, we now integrate both pathways with the VLM to establish their synergy. Our key insight is that explicit trace reasoning and implicit latent action tokens are complementary modalities: trace leverages VLM’s pretrained spatial 


supervised by cross-entropy loss _L_ trace. By surfacing spatial planning as explicit coordinate sequences, trace reasoning provides an interpretable "thinking process" for manipulation, articulating where the end-effector should move before committing to actions. 

**Latent tokens as visually-grounded action semantics.** To enable latent action prediction, we augment the VLM vocabulary with special tokens {ACT_1, ..., ACT_K} indexing into the pretrained codebook from Section 3.1. After generating trace _τ_ , the VLM predicts a sequence of latent action tokens for action chunking: 


where each _qi_ selects a latent action primitive from the codebook. The optimization combines both pathways: 


where _L_ latent = _−_<sup>�</sup><sup>_N_</sup> _i_ =1<sup>log</sup><sup>_p_(</sup><sup>_qi| ot, ℓt, τ, q<i_).This dual-</sup> path architecture exploits their complementary strengths. Trace provides explicit spatial targets that guide the VLM’s spatial reasoning, while latent tokens encode visuallygrounded primitives that fuse geometric patterns with scene-specific observations. This synergy enables latent tokens to compensate for trace’s coordinate imprecision through learned visual attention to task-relevant context, while trace scaffolding filters visual variations to focus latent predictions on manipulation-relevant regions. The compact vocabulary expansion preserves VLM capabilities while providing semantically-rich action representations. 

### **3.3. Flow Matching Action Decoding** 

While the VLM produces discrete latent token indices _q_ 1: _N_ and explicit trace coordinates _τ_ , robot execution requires continuous action chunks **a** _t_ : _t_ + _H ∈_ R<sup>_H×D_</sup> . We bridge this gap through a lightweight flow matching decoder that synthesizes guidance from both pathways, leveraging explicit 

12240 


Figure 3. **SemanticVLA Architecture Overview.** Our dual-path framework synergistically combines explicit trace reasoning and implicit latent action planning. The VLM processes visual observations and language instructions to generate interpretable trace coordinates and latent action tokens, which are then fused to condition the flow matching action decoder for continuous robot control. 

spatial structure from trace and implicit visuomotor semantics from latent tokens for robust continuous control. **Dual-path conditioning mechanism.** We extract complementary representations from both pathways to condition the action decoder. For latent action guidance, we obtain hidden states **E** _a_ = _{_ **h** _q_ 1 _, . . . ,_ **h** _qN }_ from the VLM’s final layer, encoding multimodal reasoning over visual observations, spatial plans, and language instructions. For trace guidance, we process predicted coordinates _τ_ through the frozen trace encoder _ϕ_<sup>trace</sup> enc from Section 3.1, yielding **e** _τ_ = _ϕ_<sup>trace</sup> enc<sup>(</sup><sup>_τ_) that extracts pure spatial-temporal dynamics</sup> invariant to visual appearance. The flow decoder takes as input noisy action **a**<sup>_t_</sup> at denoising timestep _t ∈_ [0 _,_ 1] and conditions on the fused guidance **v** _θ_ ( **a**<sup>_t_</sup> _, t,_ **e** _τ ,_ **E** _a,_ **E** _v_ ) _→_ **a** _t_ : _t_ + _H_ , where **e** _τ_ provides geometric guidance, **E** _a_ supplies semantic grounding, and **E** _v_ offers visual context. Following established architectures [4, 11], the decoder predicts velocity fields through cross-attention between latent and visual features, generating actions via iterative denoising. For the final stage, we fine-tune end-to-end on robot demonstrations with the combined objective: 


where _λ_ VLM provides weak supervision to preserve the dual-path reasoning established during co-training, preventing VLM degradation into action fitting while enabling action decoder adaptation. We employ LoRA [19] on the VLM while fully training the flow decoder from scratch, ensuring the VLM preserves high-level spatial reasoning while the decoder specializes in low-level motor control. 

### **3.4. Training Recipe** 

**Data construction.** To enable large-scale pretraining of our trace-guided latent action tokenizer, we curate TraceX240K, a comprehensive trace-annotated dataset containing 240K robot trajectories from Bridge V2 [16], Frac- 

tal [5], BC-Z [22] from Open X-Embodiment [12], and DROID [25]. Following MolmoAct [30], we employ Molmo-72B to uniformly sample keyframes from each trajectory for trace annotation, where more semantic keyframe extraction methods [28, 52] could further improve annotation quality. To obtain dense spatial annotations between keyframes, we apply CoTracker [23] for interpolation, ensuring temporally-aligned trace sequences covering complete manipulation trajectories. 

**Training pipeline.** Our training follows the three-stage pipeline described in Sections 3.1-3.3. We initialize the VLM backbone from Prismatic-7B [24], following UniVLA [8], which integrates SigLIP and DINOv2 visual encoders with LLaMA-2. In Stage 1, we pretrain the semantic latent action tokenizer on TraceX-240K for 50K steps with batch size 512, learning clean geometric primitives without language contamination. In Stage 2, we co-train the VLM to jointly predict trace coordinates and latent action tokens on the same dataset for 100K steps with batch size 256, establishing their semantic correspondence without action decoding. Finally in Stage 3, we fine-tune the complete model end-to-end on downstream benchmarks, enabling flow matching action decoding while preserving VLM reasoning through weak regularization. All training is conducted on 16 NVIDIA H200 GPUs. 

## **4. Experiments** 

We conduct extensive evaluations demonstrating that SemanticVLA achieves strong manipulation performance while preserving VLM semantic reasoning through synergistic dual-path design. Our experiments validate three core properties: **Effectiveness** (Section 4.1, 4.2) competitive task success rates on simulation benchmarks and real-world deployments; **Robustness** (Section 4.3) stable performance under instruction variations that expose genuine language 

12241 

Table 1. **Performance comparison** on LIBERO and SimplerEnv. Underlined scores show best results excluding SemanticVLA. 

|Models||LIBERO|(Franka|) benchm|ark|||WidowX|benchma|rk in Simpl|erEnv||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Spatial|Objects|Goal|Long|Avg|Rank|Put<br>Spoon|Put<br>Carrot|Stack<br>Block|Put<br>Eggplant|Avg|Rank|
|RT-1-X [5]|-|-|-|-|-|-|0.0|4.2|0.0|0.0|1.1|14|
|Octo-Base [41]|78.9|85.7|84.6|51.1|75.1|11|12.5|8.3|0.0|43.1|16.0|11|
|OpenVLA [26]|84.7|88.4|79.2|53.7|76.5|10|12.5|0.0|0.0|4.1|4.2|13|
|SpatialVLA [45]|88.2|89.9|78.6|55.5|78.1|9|20.8|20.8|25.0|70.8|34.4|7|
|CoT-VLA [53]|87.5|91.6|87.6|69.0|83.9|8|-|-|-|-|-|-|
|TraceVLA [55]|84.6|85.2|75.1|54.1|74.8|12|12.5|16.6|16.6|65.0|27.7|10|
|VQ-VLA [47]|82.1|80.2|75.2|60.0|74.4|13|12.5|8.0|6.0|0.0|6.6|12|
|GR00T N1 [3]|94.4|97.6|93.0|90.6|93.9|4|59.5|43.0|45.0|48.5|49.0|3|
|_π_0 [4]|96.8|98.8|95.8|85.2|94.2|3|49.1|20.0|36.6|82.5|47.1|4|
|_π_0-FAST [43]|96.4|96.8|88.6|60.2|85.5|6|29.1|21.9|10.8|66.6|32.1|8|
|Magma [48]|-|-|-|-|-|-|37.5|29.2|20.8|91.7|44.8|5|
|MolmoAct [30]|87.0|95.4|87.6|77.2|86.6|5|70.3|50.0|45.3|60.0|51.4|2|
|ThinkAct [20]|88.3|91.4|87.1|70.9|84.4|7|58.3|37.5|8.7|70.8|43.8|6|
|<br>UniVLA [8]|96.5|96.8|95.6|92.0|95.2|2|41.6|29.2|4.2|50.0|31.3|9|
|**SemanticVLA**|**98.0**|**98.6**|**96.8**|**94.4**|**97.0**|**1**|**83.6**|**54.5**|**40.3**|**81.8**|**65.1**|**1**|


understanding rather than pattern memorization; **Synergy** (Section 4.4, 4.5) complementary benefits between explicit trace reasoning and implicit latent action tokens . 

### **4.1. Simulation Benchmarks** 

We evaluate on two established simulation suites testing complementary generalization aspects. LIBERO [36] provides language-conditioned manipulation across spatial, object, goal, and long-horizon task variations on Franka arm. SimplerEnv [32] probes cross-domain robustness through visual appearance shifts on short-horizon WidowX tasks. **LIBERO.** Following established protocols [27], we finetune independently per suite on 16 H200 GPUs for 30K steps with batch size 128 and action chunk size 12, then evaluate over 500 trials with randomized initial states. As shown in Table 1, SemanticVLA achieves 97.0% average success rate, outperforming strong baselines across task categories. Compared to _π_ 0 and GR00T which connect System 1 and 2 through opaque latent embeddings, we follow UniVLA’s philosophy of imposing semantic constraints on latent action tokens for grounded representations. Our trace-guided latent pretraining provides explicit spatial semantics beyond UniVLA and VQ-VLA, whose latents lack geometric scaffolding and rely solely on visual reconstruction or raw actions. Combined with explicit trace reasoning during inference, this dual-path design preserves VLM capabilities—unlike MolmoAct which expands vocabulary with raw action tokens, we maintain modality separation through latent tokens and the flow matching decoder. **SimplerEnv.** We evaluate on the WidowX manipulation suite, training on Bridge dataset demonstrations and testing across four tasks with controlled visual variations over 24 episodes each. SemanticVLA achieves 65.1% average success rate, outperforming competitive baselines and demonstrating effective transfer of trace-guided spatial understanding across manipulation primitives. Reasoning- 

enhanced approaches such as ThinkAct, MolmoAct, and Magma substantially outperform direct action prediction models including OpenVLA and RT-1-X, confirming the importance of structured reasoning for cross-domain robustness. Although _π_ 0 and GR00T achieve strong results through massive-scale pretraining, our method reaches comparable performance by leveraging VLM’s native reasoning through semantically-grounded latent embeddings that bridge spatial understanding and motor control. 

### **4.2. Real-world Robotics Evaluation** 

**Experiment Settings.** We further conduct real-world experiments using a Franka Research 3 robot arm with Franka hand and two Intel RealSense D435 cameras. The model runs on a single NVIDIA RTX 3090 GPU achieving realtime control. We evaluate two complementary categories with 20 rollouts per task across 5 variants that vary objects, positions and scene layouts. **Long-horizon compositional tasks** require maintaining coherent plans across 3- 5 sequential subtasks: table sorting organizes vegetables, fruits, or meat into designated categories; food preparing involves multi-step meal assembly such as sandwich making. **Reasoning-intensive tasks** demand explicit reasoning beyond manipulation: math calculation interprets whiteboard arithmetic to place blocks at correct positions; word spelling composes words from letter blocks based on whiteboard specifications, requiring integrated visual understanding, calculation, and linguistic reasoning. **Results.** As shown in Table 2, SemanticVLA achieves 62% success across both categories. Reasoning-enhanced methods such as MolmoAct and Magma substantially outperform non-reasoning baselines including OpenVLA and UniVLA, confirming that explicit reasoning is critical for complex manipulation. Explicit trace reasoning surfaces spatial planning as coordinate sequences through the VLM’s language interface, selecting answer positions or de- 

12242 


terminingnative letter arrangementscapabilities. byLatentdirectlyactionreusingtokensVLM’sthendirectlyactionreusingtokensVLM’sthenreusingtokensVLM’sthenVLM’sthen native reasoningletter capabilities. LatentdirectlyactionreusingtokensVLM’sthenactionreusingtokensVLM’sthentokensVLM’sthenthen compress these spatial patterns with visual observations into semantically-grounded representations that guide the action expert for precise continuous control. Compared to MolmoAct which expands vocabulary with raw action tokens, our latent interface maintains modality separation and enables stable decoding through the flow matching decoder. 

Figure 5. **Instruction Rephrasing Robustness.** Performance on LIBERO and SimplerEnv benchmarks under instruction variations. Dashed bars: success rates with original instructions; Solid bars: rephrased instructions with similar task semantics. 

Table 2. **Success rate evaluation** in real robot experiments in long-horizon and reasoning scenarios. 

||**Long-hori**|**zon tasks**|**Reasoning**|**tasks**||
|---|---|---|---|---|---|
|**Models**|Food<br>Preparing|Desktop<br>Sorting|Math<br>Calculation|Spell<br>Words|**Avg**|
|OpenVLA [26]|16|10|6|3|8.8|
|UniVLA [8]|47|41|27|16|32.8|
|Magma [48]|51|42|29|19|35.3|
|MolmoAct [30]|59|47|36|19|40.3|
|_π_0 [4]|63|54|43|32|48.0|
|**SemanticVLA**|**77**|**69**|**58**|**45**|**62.3**|


across perturbations, only 9.4% on LIBERO and significantly outperforming baselines on SimplerEnv. Baselines show substantial brittleness under rephrasing, with OpenVLA degrading by 18.4% and UniVLA by 23.9%. In contrast, reasoning-enhanced MolmoAct demonstrates improved robustness with 11.9% drops, confirming that explicit reasoning mechanisms enhance linguistic generalization. SemanticVLA achieves the most stable performance through modality separation that enables explicit trace reasoning to reuse the VLM’s compositional understanding for generating consistent spatial waypoints across linguistic variations, while implicit latent tokens ground these abstract patterns in visual observations for robust execution. 

### **4.3. Instruction Variance Robustness** 

Beyond in-domain performance, we systematically evaluate whether SemanticVLA genuinely understands language instructions or merely memorizes linguistic-action correlations. Following recent robustness protocols [17, 18], we test on instruction perturbations across LIBERO and SimplerEnv. The evaluation settings include paraphrased variants with appearance-based references such as "orange object" instead of "carrot", negation phrases like "not the towel", and commonsense cues including "rabbit’s favorite vegetable", yielding 200 test cases per benchmark to probe linguistic robustness under distributional shifts. As shown in Figure 5, SemanticVLA exhibits minimal degradation 

### **4.4. Explicit Trace-Guided Latent Action Learning** 

To validate that trace guidance produces semanticallygrounded latent tokens beyond architectural benefits, we conduct ablations on LIBERO instruction rephrasing with three variants: SemanticVLA with full dual-path reasoning, an ablation removing explicit trace that directly predicts latent tokens from VLM embeddings, and UniVLA that predicts latent tokens without trace supervision during pre- 

12243 


Figure 6. **The analysis of latent learning.** Training curves on LIBERO instruction rephrasing. Solid lines: success rate (right y- axis); Dashed lines: latent prediction accuracy (left y-axis). 

training. As shown in Figure 6, latent prediction accuracy strongly correlates with manipulation performance. The full model achieves 93.6% latent prediction accuracy and 87.6% task success under rephrasing. Removing trace reasoning degrades accuracy to 85.6% and success to 79.2%, revealing that explicit trace reasoning proves essential under instruction rephrasing by distinguishing genuine semantic understanding from pattern memorization. More critically, to isolate the effect of trace-guided pretraining, we conduct a controlled ablation comparing our latent tokens against UniVLA’s—both trained without explicit trace reasoning. Our tokens achieve substantially higher accuracy and success rates, with gaps exceeding 12%, demonstrating that trace supervision during pretraining imbues latent embeddings with richer semantic grounding. The geometric scaffolding from trace sequences acts as a strong inductive bias, filtering task-irrelevant variations and forcing the codebook to capture true manipulation semantics. 

### **4.5. Latent Tokens Stabilize Trace Execution** 

While trace guidance improves latent learning, we examine whether latent tokens reciprocally stabilize trace-based execution. We evaluate on real-world Franka manipulation under three generalization axes: visual shifts, task variations, and language rephrasing. We compare against trace-only baselines including TraceVLA with visual overlay, HAMSTER with direct trace conditioning, and MolmoAct with trace reasoning plus raw action tokens. As shown in Figure 7, SemanticVLA substantially outperforms all baselines across all generalization types. TraceVLA performs worst as passive trace rendering lacks forward planning capability. HAMSTER exhibits brittleness from directly conditioning on predicted coordinates, where raw trace coordinates lack semantic grounding to visual observations and prediction errors compound under distribution shifts. MolmoAct generates spatial plans through trace reasoning before action prediction. However, expanding the VLM vocabulary with discrete action tokens degrades language capabilities through gradient interference. Our ablation without la- 


Figure 7. **Real-world generalization evaluations** under visual perturbation, instruction rephrasing, and task variation. 

tent action planning achieves 48% on language rephrasing compared to MolmoAct’s 33%, directly validating that expanding VLM vocabulary with raw action tokens corrupts reasoning capabilities. The full SemanticVLA further improves to 56% by incorporating latent tokens that provide visually-grounded semantic primitives. While trace reasoning surfaces high-level spatial planning through VLM’s native language interface, latent tokens offer fine-grained guidance for precise action prediction by fusing geometric patterns with scene-specific visual observations, enabling robust execution under distribution shifts. 

## **5. Conclusion** 

In this work, we introduce SemanticVLA, a dual-path VLA framework that genuinely exploits VLM’s native reasoning capabilities through synergistic design. _Explicit trace reasoning_ generates interpretable spatial waypoints via VLM’s language interface as a "thinking process" for manipulation planning, while _implicit latent action tokens_ provide fine-grained, semantically-rich guidance to the action expert through compact visuomotor primitives. To enable large-scale pretraining, we curate TraceX-240K containing trace-annotated robot trajectories with automated dense spatial annotations. Our three-stage training pipeline ensures clean modality separation: trace-guided latent pretraining learns spatial-temporal patterns without language contamination, VLM co-training establishes semantic correspondence between traces and latent tokens, and tracelatent conditioned action decoding enables precise motor control while preserving VLM reasoning capabilities. SemanticVLA substantially outperforms strong baselines on simulation benchmarks including LIBERO and SimplerEnv. More critically, it maintains significantly more stable performance under instruction rephrasing, especially for long-horizon and reasoning-intensive tasks in real-world. We believe this synergistic fusion of explicit trace and latent action tokens pathways provides a promising and principled approach to designing more effective VLA architectures that genuinely leverage VLMs as _generalized reasoners_ rather than degrade them into _action memorizers_ . 

12244 

## **Acknowledgements** 

S. Zafeiriou was funded by the EPSRC Fellowship DEFORM (EP/S010203/1), EPSRC Project GNOMON (EP/X011364/1) and Turing AI Fellowship (EP/Z534699/1). J. Deng was supported by the NVIDIA Academic Grant. 

## **References** 

- [1] Figure AI. Helix, 2024. 2 

- [2] Suneel Belkhale, Tianli Ding, Ted Xiao, Pierre Sermanet, Quon Vuong, Jonathan Tompson, Yevgen Chebotar, Debidatta Dwibedi, and Dorsa Sadigh. Rt-h: Action hierarchies using language. <u>arXiv preprint arXiv:2403.01823, 2024.</u> 3 

- [3] Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. <u>arXiv preprint arXiv:2503.14734, 2025.</u> 2, 6 

- [4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _\pi_ 0: A vision-languageaction flow model for general robot control. <u>arXiv preprint arXiv:2410.24164, 2024.</u> 2, 5, 6, 7 

- [5] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. <u>arXiv preprint arXiv:2212.06817, 2022.</u> 1, 2, 5, 6 

- [6] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. <u>arXiv preprint arXiv:2307.15818, 2023.</u> 1 

- [7] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. <u>arXiv preprint arXiv:2503.06669, 2025.</u> 2 

- [8] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. <u>arXiv preprint arXiv:2505.06111, 2025.</u> 3, 5, 6, 7 

- [9] Xinyi Chen, Yilun Chen, Yanwei Fu, Ning Gao, Jiaya Jia, Weiyang Jin, Hao Li, Yao Mu, Jiangmiao Pang, Yu Qiao, et al. Internvla-m1: A spatially guided vision-languageaction framework for generalist robot policy. <u>arXiv preprint arXiv:2510.13778, 2025.</u> 2 

- [10] Yi Chen, Yuying Ge, Yizhuo Li, Yixiao Ge, Mingyu Ding, Ying Shan, and Xihui Liu. Moto: Latent motion token as the bridging language for robot manipulation. <u>arXiv preprint arXiv:2412.04445, 2024.</u> 2 

- [11] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In <u>Proceedings of Robotics: Science and Systems (RSS), 2023.</u> 5 

- [12] Open X-Embodiment Collaboration, Abby O’Neill, and Zipeng Lin. Open X-Embodiment: Robotic learning datasets and RT-X models. https://arxiv.org/abs/2310. 08864, 2023. 2, 5 

- [13] Zichen Cui, Hengkai Pan, Aadhithya Iyer, Siddhant Haldar, and Lerrel Pinto. Dynamo: In-domain dynamics pretraining for visuo-motor control. <u>Advances in Neural Information Processing Systems, 37:33933–33961, 2024.</u> 3 

- [14] Danny Driess, Jost Tobias Springenberg, Brian Ichter, Lili Yu, Adrian Li-Bell, Karl Pertsch, Allen Z Ren, Homer Walke, Quan Vuong, Lucy Xiaoyang Shi, et al. Knowledge insulating vision-language-action models: Train fast, run fast, generalize better. <u>arXiv preprint arXiv:2505.23705,</u> 2025. 2 

- [15] Haodong Duan, Junming Yang, Yuxuan Qiao, Xinyu Fang, Lin Chen, Yuan Liu, Xiaoyi Dong, Yuhang Zang, Pan Zhang, Jiaqi Wang, et al. Vlmevalkit: An open-source toolkit for evaluating large multi-modality models. In <u>Proceedings of the 32nd ACM International Conference on Multimedia,</u> pages 11198–11201, 2024. 1 

- [16] Frederik Ebert, Yanlai Yang, Karl Schmeckpeper, Bernadette Bucher, Georgios Georgakis, Kostas Daniilidis, Chelsea Finn, and Sergey Levine. Bridge data: Boosting generalization of robotic skills with cross-domain datasets. <u>arXiv preprint arXiv:2109.13396, 2021.</u> 2, 5 

- [17] Irving Fang, Juexiao Zhang, Shengbang Tong, and Chen Feng. From intention to execution: Probing the generalization boundaries of vision-language-action models. <u>arXiv preprint arXiv:2506.09930, 2025.</u> 2, 7 

- [18] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, et al. Libero-plus: In-depth robustness analysis of visionlanguage-action models. <u>arXiv preprint arXiv:2510.13626,</u> 2025. 2, 7 

- [19] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. <u>ICLR,</u> 1(2):3, 2022. 5 

- [20] Chi-Pin Huang, Yueh-Hua Wu, Min-Hung Chen, YuChiang Frank Wang, and Fu-En Yang. Thinkact: Visionlanguage-action reasoning via reinforced visual latent planning. <u>arXiv preprint arXiv:2507.16815, 2025.</u> 6 

- [21] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _pi_ 0 _._ 5: a vision-language-action model with open-world generalization. <u>arXiv preprint arXiv:2504.16054, 2025.</u> 2 

- [22] Eric Jang, Alex Irpan, Mohi Khansari, Daniel Kappler, Frederik Ebert, Corey Lynch, Sergey Levine, and Chelsea Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In <u>Conference on Robot Learning,</u> pages 991– 1002. PMLR, 2022. 2, 5 

- [23] Nikita Karaev, Yuri Makarov, Jianyuan Wang, Natalia Neverova, Andrea Vedaldi, and Christian Rupprecht. Cotracker3: Simpler and better point tracking by pseudolabelling real videos. In <u>Proceedings of the IEEE/CVF International Conference on Computer Vision,</u> pages 6013– 6022, 2025. 5 

12245 

- [24] Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models. In <u>Forty-first International Conference on Machine Learning, 2024.</u> 5 

- [25] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. <u>arXiv preprint arXiv:2403.12945, 2024.</u> 2, 5 

- [26] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. <u>arXiv preprint arXiv:2406.09246, 2024.</u> 1, 2, 6, 7 

- [27] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. <u>arXiv preprint arXiv:2502.19645, 2025.</u> 6 

- [28] Longxin Kou, Fei Ni, Yan Zheng, Jinyi Liu, Yifu Yuan, Zibin Dong, and Jianye Hao. Kisa: A unified keyframe identifier and skill annotator for long-horizon robotics demonstrations. In <u>Forty-first International Conference on Machine Learning,</u> 2024. 5 

- [29] Longxin Kou, Fei Ni, Yan Zheng, Peilong Han, Jinyi Liu, Haiqin Cui, Rui Liu, and Jianye Hao. Roboannotatorx: A comprehensive and universal annotation framework for accurate understanding of long-horizon robot demonstration. In <u>Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 10353–10363, 2025.</u> 1 

- [30] Jason Lee, Jiafei Duan, Haoquan Fang, Yuquan Deng, Shuo Liu, Boyang Li, Bohan Fang, Jieyu Zhang, Yi Ru Wang, Sangho Lee, et al. Molmoact: Action reasoning models that can reason in space. <u>arXiv preprint arXiv:2508.07917, 2025.</u> 3, 4, 5, 6, 7 

- [31] Seungjae Lee, Yibin Wang, Haritheja Etukuru, H Jin Kim, Nur Muhammad Mahi Shafiullah, and Lerrel Pinto. Behavior generation with latent actions. <u>arXiv preprint arXiv:2403.03181, 2024.</u> 3 

- [32] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. <u>arXiv preprint arXiv:2405.05941, 2024.</u> 6 

- [33] Yi Li, Yuquan Deng, Jesse Zhang, Joel Jang, Marius Memmel, Raymond Yu, Caelan Reed Garrett, Fabio Ramos, Dieter Fox, Anqi Li, et al. Hamster: Hierarchical action models for open-world robot manipulation. <u>arXiv preprint arXiv:2502.05485, 2025.</u> 3 

- [34] Yue Liao, Pengfei Zhou, Siyuan Huang, Donglin Yang, Shengcong Chen, Yuxin Jiang, Yue Hu, Jingbin Cai, Si Liu, Jianlan Luo, et al. Genie envisioner: A unified world foundation platform for robotic manipulation. <u>arXiv preprint arXiv:2508.05635, 2025.</u> 3 

- [35] Fanqi Lin, Ruiqian Nai, Yingdong Hu, Jiacheng You, Junming Zhao, and Yang Gao. Onetwovla: A unified visionlanguage-action model with adaptive reasoning. <u>arXiv preprint arXiv:2505.11917, 2025.</u> 2 

- [36] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. <u>Advances in Neural Information Processing Systems, 36, 2024.</u> 6 

- [37] Atharva Mete, Haotian Xue, Albert Wilcox, Yongxin Chen, and Animesh Garg. Quest: Self-supervised skill abstractions for learning continuous control. <u>Advances in Neural Information Processing Systems, 37:4062–4089, 2024.</u> 3 

- [38] Fei Ni, Jianye Hao, Yao Mu, Yifu Yuan, Yan Zheng, Bin Wang, and Zhixuan Liang. Metadiffuser: Diffusion model as conditional planner for offline meta-rl. In <u>International Conference on Machine Learning,</u> pages 26087–26105. PMLR, 2023. 1, 2 

- [39] Fei Ni, Jianye Hao, Shiguang Wu, Longxin Kou, Jiashun Liu, Yan Zheng, Bin Wang, and Yuzheng Zhuang. Generate subgoal images before act: Unlocking the chain-ofthought reasoning in diffusion model for robot manipulation with multimodal prompts. In <u>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition,</u> pages 13991–14000, 2024. 3 

- [40] Fei Ni, Jianye Hao, Shiguang Wu, Longxin Kou, Yifu Yuan, Zibin Dong, Jinyi Liu, MingZhi Li, Yuzheng Zhuang, and Yan Zheng. Peria: Perceive, reason, imagine, act via holistic language and vision planning for manipulation. <u>Advances in Neural Information Processing Systems,</u> 37:17541–17571, 2024. 3 

- [41] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In <u>Proceedings of Robotics: Science and Systems, Delft, Netherlands, 2024.</u> 6 

- [42] Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without supervision. <u>arXiv preprint arXiv:2304.07193, 2023.</u> 4 

- [43] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. <u>arXiv preprint arXiv:2501.09747,</u> 2025. 2, 6 

- [44] Delin Qu, Haoming Song, Qizhi Chen, Zhaoqing Chen, Xianqiang Gao, Xinyi Ye, Qi Lv, Modi Shi, Guanghui Ren, Cheng Ruan, et al. Eo-1: Interleaved vision-textaction pretraining for general robot control. <u>arXiv preprint arXiv:2508.21112, 2025.</u> 2 

- [45] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. <u>arXiv preprint arXiv:2501.15830, 2025.</u> 6 

- [46] Nur Muhammad Shafiullah, Zichen Cui, Ariuntuya Arty Altanzaya, and Lerrel Pinto. Behavior transformers: Cloning _k_ modes with one stone. <u>Advances in neural information processing systems, 35:22955–22968, 2022.</u> 3 

12246 

- [47] Yating Wang, Haoyi Zhu, Mingyu Liu, Jiange Yang, HaoShu Fang, and Tong He. Vq-vla: Improving visionlanguage-action models via scaling vector-quantized action tokenizers. <u>arXiv preprint arXiv:2507.01016, 2025.</u> 2, 3, 6 

- [48] Jianwei Yang, Reuben Tan, Qianhui Wu, Ruijie Zheng, Baolin Peng, Yongyuan Liang, Yu Gu, Mu Cai, Seonghyeon Ye, Joel Jang, et al. Magma: A foundation model for multimodal ai agents. <u>arXiv preprint arXiv:2502.13130, 2025.</u> 3, 6, 7 

- [49] Shuai Yang, Hao Li, Yilun Chen, Bin Wang, Yang Tian, Tai Wang, Hanqing Wang, Feng Zhao, Yiyi Liao, and Jiangmiao Pang. Instructvla: Vision-language-action instruction tuning from understanding to manipulation. <u>arXiv preprint arXiv:2507.17520, 2025.</u> 2 

- [50] Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Sejune Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar, Reuben Tan, Yu-Wei Chao, Bill Yuchen Lin, et al. Latent action pretraining from videos. <u>arXiv preprint arXiv:2410.11758, 2024.</u> 2, 3 

- [51] Yifu Yuan, Haiqin Cui, Yaoting Huang, Yibin Chen, Fei Ni, Zibin Dong, Pengyi Li, Yan Zheng, and Jianye Hao. Embodied-r1: Reinforced embodied reasoning for general robotic manipulation, 2025. 3 

- [52] Zichen Zhang, Yunshuang Li, Osbert Bastani, Abhishek Gupta, Dinesh Jayaraman, Yecheng Jason Ma, and Luca Weihs. Universal visual decomposer: Long-horizon manipulation made easy. In <u>2024 IEEE International Conference on Robotics and Automation (ICRA), pages 6973–6980. IEEE,</u> 2024. 5 

- [53] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In <u>Proceedings of the Computer Vision and Pattern Recognition Conference,</u> pages 1702–1713, 2025. 3, 6 

- [54] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. <u>arXiv preprint arXiv:2304.13705, 2023.</u> 3 

- [55] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daumé III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. <u>arXiv preprint arXiv:2412.10345, 2024.</u> 3, 6 

- [56] Zhongyi Zhou, Yichen Zhu, Junjie Wen, Chaomin Shen, and Yi Xu. Vision-language-action model with open-world embodied reasoning from pretrained knowledge. <u>arXiv preprint arXiv:2505.21906, 2025.</u> 2 

- [57] Zhongyi Zhou, Yichen Zhu, Minjie Zhu, Junjie Wen, Ning Liu, Zhiyuan Xu, Weibin Meng, Ran Cheng, Yaxin Peng, Chaomin Shen, et al. Chatvla: Unified multimodal understanding and robot control with vision-language-action model. <u>arXiv preprint arXiv:2502.14420, 2025.</u> 2 

12247 

