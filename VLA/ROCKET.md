---
title: "ROCKET: Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models"
date: "2026-02-20"
authors: "Guoheng Sun; Tingting Du; Kaixi Feng; Chenxiang Luo; Xingguo Ding; Zheyu Shen"
url: https://arxiv.org/abs/2602.17951
pdf: https://arxiv.org/pdf/2602.17951
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.17951)** / [論文ページ](https://arxiv.org/abs/2602.17951)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **ROCKET: Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

**Guoheng Sun**<sup>*****1</sup> **Tingting Du**<sup>2</sup> **Kaixi Feng**<sup>1</sup> **Chenxiang Luo**<sup>3</sup> **Xingguo Ding**<sup>4</sup> **Zheyu Shen**<sup>1</sup> **Ziyao Wang**<sup>1</sup> **Yexiao He**<sup>1</sup> **Ang Li**<sup>_†_1</sup> 

> _∗_ ghsun@umd.edu _†_ angliece@umd.edu 

## **Abstract** 

Vision-Language-Action (VLA) models enable instruction-following robotic manipulation, but they are typically pretrained on 2D data and lack 3D spatial understanding. An effective approach is representation alignment, where a strong vision foundation model is used to guide a 2D VLA model. However, existing methods usually apply supervision at only a single layer, failing to fully exploit the rich information distributed across depth; meanwhile, na¨ıve multi-layer alignment can cause gradient interference. We introduce **ROCKET** , a residual-oriented multi-layer representation alignment framework that formulates multi-layer alignment as aligning one residual stream to another. Concretely, **ROCKET** employs a shared projector to align multiple layers of the VLA backbone with multiple layers of a powerful 3D vision foundation model via a layer-invariant mapping, which reduces gradient conflicts. We provide both theoretical justification and empirical analyses showing that a shared projector is sufficient and outperforms prior designs, and further propose a Matryoshka-style sparse activation scheme for the shared projector to balance multiple alignment losses. Our experiments show that, combined with a training-free layer selection strategy, **ROCKET** requires _only about 4% of the compute budget while achieving 98.5% stateof-the-art success rate on LIBERO_ . We further demonstrate the superior performance of **ROCKET** across LIBERO-Plus and RoboTwin, as well as multiple VLA models. The code and model weights can be found at https://github. com/CASE-Lab-UMD/ROCKET-VLA. 

1University of Maryland, College Park 2University of Wisconsin, Madison<sup>3</sup> City University of Hong Kong<sup>4</sup> St. Paul’s School. Correspondence to: Ang Li _<_ angliece@umd.edu _>_ . 

_Preprint. February 23, 2026._ 

## **1. Introduction** 

Robotic manipulation requires models to integrate semantic intent with precise spatial reasoning about objects, contacts, and constraints in the physical world. Recent visionlanguage-action (VLA) models achieve strong instructionfollowing by leveraging large vision-language backbones, yet these backbones are predominantly pretrained on 2D imagery and often fail to produce representations with stable 3D structure (Zitkovich et al., 2023; Kim et al., 2024; Li et al., 2025). As a result, VLAs may succeed on familiar scenarios but generalize poorly when manipulation depends on accurate geometry, viewpoint changes, or fine-grained spatial relations (Shridhar et al., 2022; Huang et al., 2023). 

To bridge this gap, prior work has pursued three main strategies to equip VLAs with spatial reasoning: (1) augmenting inputs with explicit 3D signals such as depth maps or point clouds (Shridhar et al., 2023); (2) recovering 3D structure from 2D observations via depth estimation (Ranftl et al., 2021); and (3) implicitly aligning intermediate VLA representations to spatial features produced by pretrained 3D foundation models (Li et al., 2025). Compared with the first two approaches, which rely on additional sensors or external depth estimators, implicit alignment is typically more inference-efficient and easier to scale, making it a particularly practical direction for improving spatial grounding in VLAs. 

In _representation alignment_ for improving spatial reasoning, a common practice is to supervise a VLA model’s visualtoken representations to match those of a strong 3D vision foundation model. Most existing methods apply alignment at a single layer (Yu et al., 2024; Huang et al., 2025b; Li et al., 2025; Wang et al., 2024). However, prior work has found that performance is highly sensitive to the chosen layer, and the optimal layer often varies across tasks and data distributions (as shown in Table 1). Since it is difficult to predict which layer contains the most appropriate visual representations _a priori_ , single-layer alignment typically relies on inefficient post-hoc search. Meanwhile, representations in deep residual networks evolve with depth and encode 

1 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

information at multiple levels (Skean et al., 2025; Lee et al., 2025), and prior feature distillation studies similarly suggest benefits from leveraging teacher signals across depths (Sun et al., 2019; Chen et al., 2021; Gong et al., 2025). A natural alternative is multi-layer alignment, which can exploit hierarchical spatial cues from shallow to deep layers. However, in the VLA setting, directly extending classic distillation by aligning multiple depths with _independent_ projectors per layer often backfires: separate projectors tend to learn inconsistent mappings between representation spaces, leading to severe gradient interference and ultimately causing performance collapse. 

To address gradient interference, we propose **ROCKET** , a stable and high-performance multi-layer alignment strategy that formulates multi-layer alignment as aligning one residual stream to another. From a residual-dynamics perspective, we attribute the failure of naive multi-projector designs to gradient conflicts, and show that using a shared projector promotes gradient coherence. Concretely, **ROCKET** learns a cross-layer shared mapping via a lightweight projector that aligns residual streams from multiple layers to a target residual stream. This shared alignment helps reduce gradient interference, enabling fast convergence while continuing to improve late-stage performance. We further observe that, in multi-layer alignment, shallower layers converge more easily; to prevent shallow-layer alignment from dominating the shared projector, **ROCKET** introduces a Matryoshkastyle (Kusupati et al., 2022) sparse activation scheme in which deeper layers activate more projector parameters. Such a scheme balances alignment losses across depths, encouraging shallow layers to quickly capture common local cues while allowing deeper layers to further refine global information. We also analyze layer selection and show that a simple training-free rule yields stable gains. Experiments across multiple models and datasets demonstrate that **ROCKET** improves spatial reasoning in VLA models and consistently outperforms the single-layer alignment paradigm. Our contributions are summarized as follows: 

- We propose **ROCKET** , a multi-layer alignment framework that injects 3D spatial reasoning into 2D-pretrained VLA models, featuring a layer-invariant shared projector to avoid gradient conflicts and a Matryoshka-style sparse activation scheme to balance alignment losses across depths. 

- We develop theoretical and empirical analyses that explain when and why prior multi-layer alignment fails due to gradient interference, and show that a single shared projector is both sufficient and consistently superior to layer-wise projectors. 

- By leveraging complementary spatial cues across depths, **ROCKET** achieves state-of-the-art performance on LIBERO and generalizes across multiple datasets and VLA backbones. 

- **ROCKET** is compute-efficient and converges quickly, reaching state-of-the-art (SOTA) performance with _∼_ 4% of the training compute required by prior SOTA methods, while remaining effective in data-limited regimes relevant to embodied settings. 

## **2. Related Work** 

**Vision-Language-Action Models and Spatial Grounding** VLA models integrate visual perception and language understanding to generate embodied robot actions. Representative works include **OpenVLA** (Kim et al., 2024) and **OpenVLAOFT** (Kim et al., 2025) built upon Prismatic-7B (Karamcheti et al., 2024), as well as **PI0** (Black et al., 2024) and **PI0.5** (Black et al., 2025) based on PaliGemma (Beyer et al., 2024), which primarily rely on 2D Vision-Language Models (VLMs). These models often lack geometric understanding of the 3D world. To address this, several works augment VLA models with 3D information, including point-cloud inputs (Bhat et al., 2025; Sun et al., 2025) or depth-aware encodings (Qu et al., 2025). Meanwhile, recent 3D foundation models such as **VGGT** (Wang et al., 2025a), **Depth Anything** (Lin et al., 2025a), and _π_<sup>3</sup> (Wang et al., 2025b) provide strong spatial representations that can offer rich supervision signals for 2D vision backbones. 

**Representation Alignment for Spatial Supervision** Representation alignment (feature distillation) is widely used to transfer spatial knowledge from pretrained teachers to VLM/VLA models. Most prior work aligns student visualtoken features from one layer to a fixed teacher layer. For example, **Spatial Forcing (SF)** (Li et al., 2025) and **GLaD** (Guo et al., 2025) align _deep_ vision representations to VGGT features; **REPA** (Yu et al., 2024) aligns _shallow_ diffusion-model (Peebles & Xie, 2022) representations to DINOv2-Large (Oquab et al., 2023); and **3DRS** (Huang et al., 2025b) supervises the _final-layer_ visual tokens using VGGT. Although effective, these methods typically supervise a single layer and do not fully exploit the representations across depth. Moreover, as shown in Table 1, the choice of which layer to align is often inconsistent across methods and depends on post-hoc empirical results. 

_Table 1._ Comparison of representation alignment methods for spatial supervision. OpenVLA – **24 / 32** : with a 32-layer backbone, using the 24th-layer features for alignment. 

|**Method**|**Student**||**Teacher**|
|---|---|---|---|
|SF|OpenVLA –**24 / 32**|VGGT|– 24 / 24|
|REPA|DiT –**8 / 24**|DINOv2|– 24 / 24|
|3DRS|LLaVA –**32 / 32**|VGGT|– 24 / 24|


**Multi-layer Distillation and Optimization Challenges** Early studies on knowledge distillation have shown that supervising multiple intermediate layers can lead to more effective knowledge transfer. Methods such as **Pa-** 

2 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

**tient Knowledge Distillation** (Sun et al., 2019), **ReviewKD** (Chen et al., 2021), and recent feature-dynamicsbased approaches (Gong et al., 2025) demonstrate the benefits of multi-layer alignment in deep networks. To enable supervision at intermediate layers, prior methods commonly attach layer-wise _projectors_ (Chen et al., 2022; Miles & Mikolajczyk, 2024; Miles et al., 2024) that reconcile mismatched feature spaces before computing alignment losses. However, extending multi-layer distillation to VLA models introduces additional challenges: gradient interference can arise among the separate projectors, which can degrade alignment quality. 

## **3. Theoretical Framework: Residual Dynamics and Gradient Coherence** 

_h_<sup>_S_</sup> _s_<sup>(</sup><sup>_θ_)</sup><sup>_∈_R</sup><sup>_dS_and</sup><sup>_hT_</sup> _τ_<sup>_∈_R</sup><sup>_dT_denotethestudent/teacher</sup> vision representations at student layer _s_ and teacher layer _τ_ . SF aligns one student layer _s_<sup>_⋆_</sup> to one teacher layer _τ_<sup>_⋆_</sup> (i.e., _S_ = _{s_<sup>_⋆_</sup> _}_ , _T_ = _{τ_<sup>_⋆_</sup> _}_ ) via a lightweight projector _pϕ_ and optimizes 


where _ℓ_ ( _·, ·_ ) can be any similarity-based loss. 

Accordingly, most representation-alignment methods optimize a joint objective: 


where _λ_ balances task learning and representation alignment. 

### **3.2. The Gradient-Conflict of Multi-Layer Alignment** 

### **3.1. Background** 

**VLA as student and manipulation objective.** For ease of understanding, we view representation alignment from the perspective of feature knowledge distillation. We consider a pretrained VLA policy as the _student_ model. Given an observation (e.g., multi-view images) _I_ and an instruction _P_ , the student induces an action policy _πθ_ . One possible instantiation is an autoregressive policy (Kim et al., 2024) that predicts an action sequence _A_ = _{at}_<sup>_K_</sup> _t_ =1<sup>:</sup> 


while our method is agnostic to the specific action parameterization (e.g., continuous regression or discretized action tokens). The student is trained with an action learning loss 


where _A_<sup>_gt_</sup> denotes the ground-truth action sequence from demonstrations. 

**3D vision foundation model as teacher.** We assume access to a _frozen_ 3D-aware vision foundation model as the _teacher_ , which provides geometry-grounded _patch token_ representations. Such models (e.g., VGGT (Wang et al., 2025a), _π_<sup>3</sup> (Wang et al., 2025b), Depth Anything 3 (Lin et al., 2025a)) learn spatially consistent features from monocular or multi-view images and can serve as strong supervision signals for injecting 3D cues into a VLA student’s visual representations. 

**Single-layer representation alignment.** Single-layer alignment applies supervision on the _visual tokens_ of a student model by matching them to a teacher’s intermediate representations at a selected depth to improve spatial awareness. There has been a line of prior work adopting single-layer intermediate feature matching, which is simple yet effective (Li et al., 2025; Guo et al., 2025). Let 

**From single-layer to multi-layer alignment: richer cues, but no gains in practice.** Despite its effectiveness, singlelayer alignment has limitations: (i) _single-point_ alignment requires post-hoc layer selection, and (ii) it fails to use complementary cross-layer signals. A natural extension is to align _multiple_ layers simultaneously, since spatial cues may be distributed across depth and multi-layer distillation is effective in other settings (Skean et al., 2025; Lee et al., 2025). Concretely, given ordered layer lists _S_ = _{si}_<sup>_N_</sup> _i_ =1 (student) and _T_ = _{τi}_<sup>_N_</sup> _i_ =1<sup>(teacher), previous multi-layer</sup> alignment methods use layer-specific projectors _{pϕi}_ : 


However, this prior-style design (Sun et al., 2019; Chen et al., 2021; Gong et al., 2025) _hurts_ downstream VLA manipulation performance (as shown in Fig. 3). 

**Residual-dynamical view: multi-layer alignment should be cone-to-cone, yet learned projectors decouple.** To understand why multi-layer alignment fails, we view both student and teacher backbones as residual dynamical systems (Weinan, 2017; Chang et al., 2017). Let _hl ∈_ R<sup>_d_</sup> be the student residual representation at layer _l_ : 


with ∆ _l_ := _Fl_ ( _hl_ ; _θl_ ). Empirically, the hidden states within each model tend to converge into the same feature space (Gromov et al., 2024; He et al., 2024) (Fig. 4), consistent with the “cone effect” (Gao et al., 2019). This suggests multi-layer alignment should learn a consistent _cone-to-cone_ mapping from the student residual stream to the teacher residual stream. Yet, under naive multi-layer alignment, the learned projectors _{pϕi} diverge_ and become nearly orthogonal in parameter space (Please refer to Appendix E), indicating that different depths follow inconsistent alignment paths rather than sharing a coherent mapping. 

3 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 


_Figure 1._ Cosine similarity between gradients induced by different alignment losses in the VLA’s shallow layers. **Red** indicates gradient coherence, while **Blue** indicates gradient interference. Detailed results are provided in Fig. 13 and Fig. 14. 

**Corollary: early-layer updates are a superposition of future local distillation gradients.** Why do inconsistent projectors matter for optimization? Our key observation is that in a Pre-LN residual stream, back-propagation through depth is close to identity when residual updates are small, so an early-layer representation receives an _additive_ mixture of gradient signals coming from _all_ aligned future layers. Formally, Appendix H derives (Corollary 1) that for an early layer _i_ , 


where _Ei_ is a _transport error_ controlled by residualsmallness and _α_ denotes the layer-wise weight. Thus, _whether multi-layer alignment helps hinges on whether {vl} add constructively or cancel._ 

**Proposition: Jacobian-induced gradient interference under multiple independent projectors.** Let _G ≈_ � _l≥i_<sup>_αlvl_denotethesuperposedgradient(ignoring</sup><sup>_Ei_).</sup> Its squared norm expands as 


where the cross terms determine constructive vs. destructive interference. Crucially, each cross term is a bilinear form on teacher-side error signals: 


With _multiple independent_ projectors, _Mab_ is _not structurally coupled_ across ( _a, b_ ): the interaction matrix _Jpϕa_ ( _ha_ ) _Jpϕb_ ( _hb_ )<sup>_⊤_</sup> need not be symmetric or positive semidefinite (PSD), and can vary arbitrarily across layers. As a result, _⟨va, vb⟩_ may be weak, sign-unstable, or even destructive. Empirically, we observe that cross-layer alignment gradients remain poorly aligned (small pairwise cosine similarity) throughout training (Shown in the upper part of Fig. 1), consistent with gradient conflict under unconstrained cross terms. 

### **3.3. Motivation** 

**Shared projector yields a structured decomposition and improves gradient coherence in practice.** Multi-layer alignment with multiple _independent_ projectors often underperforms due to gradient interference across layers. In contrast, if we _share a single projector_ across layers ( _ϕl ≡ ϕ_ ), Appendix H shows that although _Mab_ = _Jpϕ_ ( _ha_ ) _Jpϕ_ ( _hb_ )<sup>_⊤_</sup> is not necessarily symmetric or PSD, it can be decomposed into a _common PSD reference_ plus a controlled deviation: 


Moreover, on the error-signal subspace _G_ = span _{gl}_ where _M_ is near-isometric, we obtain the signal-aligned lower bound (Theorem H.1): 


for constants _c >_ 0 and _η ∈_ [0 _,_ 1). When _ga_<sup>_⊤gb_is typically</sup> positive and the deviation terms are small, sharing biases cross-layer gradients toward constructive interference. We validate this prediction by visualizing gradient angles: with a shared projector, cross-layer gradient cosine similarities increase substantially compared to the independent-projector baseline (Shown in the lower part of Fig. 1), and this improved coherence translates into significant downstream gains on VLA manipulation tasks (Fig. 3). This motivates **ROCKET** ’s design choice: _share the projector_ to reduce gradient conflict and make multi-layer alignment effective. Full proofs and additional empirical analysis are provided in Appendix H. 

## **4. Methodology** 

### **4.1. Overview of ROCKET** 

We propose **ROCKET** , a multi-layer representation alignment method on the residual stream. As shown in Fig. 2, **ROCKET** has three key designs: 

**(i) Multi-layer representation alignment.** Single-layer alignment cannot fully leverage the rich semantic information across layers and often relies on post-hoc layer selection. 

4 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 


_Figure 2._ Overview of **ROCKET** . On the **left** , we select a sample from LIBERO to showcase **ROCKET** ’s performance. On the **right** , we use the outputs from VGGT layers _{_ 1 _,_ 3 _,_ 9 _,_ 15 _,_ 21 _}_ to directly predict the depth map, demonstrating that different layers contain rich 3D information. Some of the illustrations were generated by GPT-4o (Hurst et al., 2024). 

**ROCKET** aligns multiple layers, and Sec. 6.2 shows that with a simple layer selection strategy, **ROCKET** outperforms the baselines. 

**(ii) Shared projector to reduce gradient conflict.** Naive multi-layer alignment may cause gradient conflicts across layers. **ROCKET** uses a _shared_ projector to learn a common mapping between two residual streams. 

**(iii) Matryoshka-style activation for balancing depths.** As indicated by Eq. 7, gradients from multiple alignment losses approximately add up, so shallow layers receive denser supervision. Our experiments also show that shallow layers are easier to align (Please refer to Appendix F for more details). To prevent shallow layers from dominating the shared projector, **ROCKET** introduces a Matryoshkastyle (Kusupati et al., 2022) parameter-sparse activation mechanism, which progressively increases the activated parameter fraction from shallow to deep layers. 

### **4.2. Multi-layer Alignment with Shared Projector** 

We follow the multi-layer alignment setting in Sec. 3.2, with _N_ aligned layer pairs _{_ ( _si, τi_ ) _}_<sup>_N_</sup> _i_ =1<sup>and the correspond-</sup> ing hidden states _{_ ( _h_<sup>_S_</sup> _si_<sup>_, hT_</sup> _τi_<sup>)</sup><sup>_}_</sup> _i_<sup>_N_</sup> =1<sup>.Crucially,wereplace</sup> the layer-specific projectors _{pϕi}i_<sup>_N_</sup> =1<sup>in Eq. 5 with a sin-</sup> gle shared projector _p_ Φ, which learns a _shared_ student-toteacher mapping that is consistent across depth. For the detailed layer selection strategy, please refer to Sec.6.1 and Sec. 6.2. 

### **4.3. Matryoshka-style Sparse Activation** 

We parameterize a single shared projector _p_ Φ : R<sup>_dS_</sup> _→_ R<sup>_dT_</sup> with a maximum internal width _m_ . Specifically, we present a two-layer MLP projector: 


where _σ_ ( _·_ ) is a pointwise nonlinearity (e.g., GELU), and Φ = _{W_ 1 _, W_ 2 _}_ . 

For each aligned layer _si_ , we activate only the _first mi_ hidden channels of the shared projector, where _mi_ increases monotonically with depth. By default, we use a simple linear width schedule: 


where _ρ_ min = 0 _._ 2 and _ρ_ max = 1 _._ 0, _m_ is the maximum hidden width of the shared projector. When _N_ = 1, this reduces to _ρ_ 1 = _ρ_ max (i.e., activating the full projector). Equivalently, define a binary gating vector _gi ∈{_ 0 _,_ 1 _}_<sup>_m_</sup> as a prefix mask 


and apply it to the hidden activation: 


where _⊙_ denotes element-wise multiplication. This construction yields a _Matryoshka_ (nested) family of projectors 

5 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 


_Table 2._ Comparisons with SOTA VLA models on the LIBERO benchmark. 

|**Method**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|
|**Basic**|**2D VLA**|||||
|Octo (Ghosh et al.,2024)|78.9|85.7|84.6|51.1|75.1|
|OpenVLA (Kim et al.,2024)|84.7|88.4|79.2|53.7|76.5|
|WorldVLA (Cen et al.,2025)|87.6|96.2|83.4|60.0|81.8|
|Dita (Hou et al.,2025)|84.2|96.3|85.4|63.8|82.4|
|PI0 (Black et al.,2024)|96.8|98.8|95.8|85.2|94.2|
|InternVLA (Chen et al.,2025b)|98.0|99.0|93.8|92.6|95.9|
|GR00T N1.6 (Bjorck et al.,2025)|97.7|98.5|97.5|94.3|97.0|
|VOTE (Lin et al.,2025b)|98.8|**99.8**|97.6|95.6|98.0|
|TraceVLA (Zheng et al.,2024)|84.6|85.2|75.1|54.1|74.8|
|ThinkAct (Huang et al.,2025a)|88.3|91.4|87.1|70.9|84.4|
|UniVLA (Bu et al.,2025)|96.5|96.8|95.6|92.0|95.2|
|MemoryVLA (Shi et al.,2025)|98.4|98.4|96.4|93.4|96.5|
|CronusVLA (Shi et al.,2025)|97.3|99.6|96.9|94.0|97.0|
|OpenVLA-OFT (Kim et al.,2025)|97.6|98.4|97.9|94.5|97.1|
|**3D VLA with**|**explicit 3**|**D inputs**||||
|SpatialVLA (Qu et al.,2025)|88.2|89.9|78.6|55.5|78.1|
|GeoVLA (Sun et al.,2025)|98.4|99.0|96.6|96.6|97.7|
|3D-CAVLA (Bhat et al.,2025)|98.2|**99.8**|98.2|96.1|98.1|
|**3D VLA with rep**|**resentati**|**on alignm**|**ent**|||
|GLaD (Guo et al.,2025)|95.0|97.4|94.4|89.4|94.1|
|Spatial Forcing (Li et al.,2025)|**99.4**|99.6|**98.8**|96.0|**98.5**|
|**ROCKET**(Ours)|98.2|**99.8**|**98.8**|**97.0**|**98.5**|


_Figure 3._ Performance on LIBERO across different training stages. See Table 9 for details. 


_Figure 4._ A cone-effect perspective on alignment. _{p_<sup>(</sup> Φ<sup>_i_)</sup><sup>_}_</sup> _i_<sup>_N_</sup> =1<sup>that share parameters, but expose increasing ef-</sup> fective capacity for deeper layers. 

_Table 3._ Success rate (%) of the PI0.5 with different representation alignment strategies on the LIBERO. 

|**Method**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|
|Baseline|96.4|98.2|95.0|82.2|93.0|
|Spatial Forcing|**97.8**|97.8|94.4|85.8|94.0|
|**ROCKET**|96.4|**98.8**|**96.6**|**89.2**|**95.3**|


**Training objective.** Our final training objective combines the task loss for action prediction with the proposed multilayer alignment regularizer: 


we perform LoRA fine-tuning for 50 _,_ 000 steps with batch size 32. In addition, to compare multiple methods under the _full fine-tuning_ regime as in PI0.5, we run full fine-tuning on LIBERO for 30 _,_ 000 steps with batch size 64. 

where _L_ action is defined in Eq. (2), and _λ_ balances task learning and representation alignment. By default, we use _ℓ_ ( _a, b_ ) = 1 _−_ cos( _a, b_ ) and set _λ_ = 0 _._ 5. 

**RoboTwin 2.0.** We follow the official training protocol and perform LoRA fine-tuning for 30 _,_ 000 steps with a batch size of 16. For evaluation, we follow the ROBOTWIN 2.0 (Chen et al., 2025a) evaluation procedure with a random seed of 0, and run 100 trials for both the easy and hard task sets. We use the task subset specified in SF for both training and evaluation. For all benchmarks, we report task execution success rate (SR, %) by default. 

## **5. Main Result** 

### **5.1. Experimental Setup** 

**LIBERO and LIBERO-Plus.** We conduct experiments on LIBERO (Liu et al., 2023) and LIBERO-PLUS (Fei et al., 2025). Each benchmark comprises four sub-datasets (task suites). Following the official protocol of LIBEROPLUS as well as the common practice used in PI0/PI0.5, we mix the four sub-datasets during training and evaluate a _single_ model on the four corresponding test suites. Unless otherwise specified, we fine-tune the OPENVLA-7B pretrained weights on LIBERO and LIBERO-PLUS. We adopt the training setting of SF and OPENVLA-OFT. Specifically, 

**Projector and Alignment Hyperparameters.** To ensure a fair comparison, we keep the projector architecture _identical across all experiments_ . In particular, we use a _single_ projector whose structure and dimensionalities exactly match SF. For the alignment-loss weight _λ_ and the number 

6 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 


_Figure 5._ Success rate (%) on LIBERO-Plus. Results are reported under the seven perturbations defined by LIBERO-Plus. Each column shows the average success rate over four task groups: Spatial, Object, Goal, and Long. Detailed results are provided in Appendix G. 

of layers used by the single-layer alignment baseline in SF, we directly use the best configurations reported by their hyperparameter search. More training hyperparameters and implementation details are provided in Appendix A. 

### **5.2. Performance of ROCKET Across Different Settings** 

**LIBERO with OpenVLA-7B.** As shown in Table 2, we compare representative approaches on LIBERO, including: (i) standard 2D VLA models, covering both direct finetuning of the base VLA and variants that boost performance via additional modules; (ii) 3D VLA methods with explicit 3D inputs, including augmenting inputs with explicit 3D signals and recovering 3D structure via depth estimation; and (iii) two single-layer representation alignment baselines. Results show that **ROCKET** substantially outperforms prior models. Even compared to Spatial Forcing, **ROCKET** matches its performance while using only _∼_ 4% of the compute budget (please refer to Table 7 for more details). 

**LIBERO with PI0.5.** On PI0.5, we compare **ROCKET** with the direct fine-tuning baseline and Spatial Forcing under the full fine-tuning setting. As reported in Table 3, under the same setting, **ROCKET** improves performance by 2 _._ 3%. Overall, this improvement suggests that even for smallerscale models under full fine-tuning, **ROCKET** can effectively inject spatial reasoning capability. 

**LIBERO-Plus with OpenVLA-7B.** We further evaluate **ROCKET** on LIBERO-Plus, a robustness benchmark with seven perturbation dimensions, and find that **ROCKET** is more robust under challenging spatial perturbations. As shown in Fig. 5, **ROCKET** achieves the best average success rate (81.7%), outperforming the baseline (80.0%). Notably, **ROCKET** shows the most pronounced gains under _Robot_ and _Layout_ shifts, which are strongly tied to spatial geometry rather than appearance. These improvements suggest that **ROCKET** enhances spatial reasoning instead of relying on positional shortcuts. 

**RoboTwin 2.0 with PI0.** For bimanual tasks, we evaluate on RoboTwin 2.0 using ALOHA assets (Aldaco et al., 2024). As shown in Fig. 6, **ROCKET** achieves a clear advantage in the Easy setting, while in the Hard setting it is only slightly behind the strongest baseline (finetuned). 

## **6. Discussion** 

### **6.1. Optimal Number of Alignment Layers** 

A key design choice in multi-layer alignment is the number of aligned layer pairs. To ensure a fair comparison, we fix the projector capacity and study how many layers should be aligned under a fixed-size projector. Following the strategy in (Sun et al., 2019), we uniformly sample _N_ layers from the VLA LLM backbone and _N_ layers from VGGT, and align them as _N_ layer pairs. As shown in Table 4, aligning roughly 8–16 layer pairs yields the best trade-off, and performance saturates or degrades beyond this range. Therefore, **ROCKET** uses _N_ = 10 aligned layer pairs by default in all experiments. 

_Table 4._ The impact of the number of aligned layers on final performance, evaluated on LIBERO. 

|**# Layers**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|
|4|98.0|98.8|93.0|**95.2**|96.3|
|8|**98.2**|**99.8**|96.4|95.0|**97.4**|
|16|97.8|99.6|**97.6**|91.6|96.7|
|24|93.2|95.6|97.4|90.0|94.1|


### **6.2. Criteria for Layer Selection** 

We investigate several layer selection strategies. We apply the same strategy to select the same layers for both VGGT and VLA. Specifically, we consider: (i) the Uniform sampling strategy in Sec. 6.1; (ii) selecting 10 layers separately from the <u>Shallow, Middle,</u> and Deep stages; (iii) <u>E2M-Last1:</u> uniformly sampling from early-to-middle layers and additionally including the last layer; and (iv) two importance-based heuristics: Motivated by the hypothesis that layers with higher input–output cosine similarity are less informative (Gromov et al., 2024; He et al., 2024), we design two similarity-based criteria. Specifically, the first criterion computes the cosine similarity between the input and output representations aggregated over windows of 10 consecutive Transformer blocks; Sim-1-Top selects the 10 layers with the highest similarity, while Sim-1-Last selects those with the lowest similarity. The second one computes similarity per block; Sim-2-Top selects the 10 highest-similarity layers, whereas Sim-2-Last selects the 10 lowest-similarity layers. 

7 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 


_Figure 6._ Success rate (%) on RoboTwin 2.0 (ALOHA) under Easy and Hard settings across five bimanual tasks, comparing **ROCKET** with DP (Chi et al., 2025), RDT (Liu et al., 2024), and PI0 (Black et al., 2024). 

Results in Table 5 show that even without expensive posthoc search, most reasonable selection strategies provide consistent gains, suggesting that **ROCKET** is robust to layer choice. Unless otherwise stated, we adopt the E2M-Last1 strategy as the default setting. Implementation details and the exact layer indices are provided in Appendix I.1, I.2. 

_Table 6._ Limited-data training on LIBERO, SR(%). 

|**Ratio**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|
|1%|75.0|88.8|65.0|65.6|73.6|
|5%|94.2|95.0|75.2|69.0|83.4|
|10%|94.0|91.8|78.6|72.6|84.3|
|100%|**96.2**|**98.0**|**97.2**|**93.6**|**96.3**|


_Table 5._ Comparison of layer selection strategies on LIBERO. 

|**Strategy**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|
|Baseline|97.2|98.4|95.6|88.6|95.0|
|Uniform-8|**98.2**|99.8|96.4|**95.0**|**97.4**|
|E2M-Last1|96.2|98.0|**97.2**|93.6|96.3|
|Shallow|97.8|99.8|95.4|85.6|94.7|
|Middle|89.4|99.8|94.2|91.2|93.7|
|Deep|92.0|99.8|95.6|93.6|95.3|
|Sim-1-Top|92.8|99.8|95.0|86.8|93.6|
|Sim-1-Last|93.8|**100.0**|95.6|92.8|95.6|
|Sim-2-Top|91.6|**100.0**|96.0|94.0|95.4|
|Sim-2-Last|91.8|**100.0**|93.6|94.8|95.1|


### **6.3. Data and Computational Efficiency** 

We evaluate the efficiency of **ROCKET** from three perspectives: **(i) Limited-data training.** Using 1%, 5%, and 10% random subsets of LIBERO (each trained for 30k steps), Table 6 shows that **ROCKET** still achieves strong performance, indicating high data efficiency, which is particularly important in robotics where data collection is costly. **(ii) Convergence speed.** In Fig. 3, **ROCKET** outperforms the baseline by _∼_ 10% at around 10k steps and continues to improve thereafter, suggesting that the proposed multi-level alignment mechanism more effectively exploits spatial cues across different layers. Please refer to Table 9 for the complete results. **(iii) Computational cost to reach SOTA.** Table 7 summarizes the compute overhead of same-sized models reported in Table 2. **ROCKET** reaches SOTA performance while the previous best method incurs 24 _×_ higher cost, demonstrating strong overall computational efficiency among post-training methods. 

### **6.4. Ablation Study** 

We ablate the key components of **ROCKET** . Introducing multi-layer alignment with _independent_ projectors degrades performance to 80 _._ 0%, indicating gradient interference across layers. Replacing independent projectors with the 

_Table 7._ Training cost comparison of same-size models on LIBERO. **Cost** is estimated as #Model _×_ BatchSize _×_ Steps. 

|**Method**|**Avg.**|**Cost**|**Details**|
|---|---|---|---|
|ThinkAct|84.4|6_._0_×_|1_×_128_×_75k|
|UniVLA|95.2|0_._96_×_|1_×_192_×_8k|
|OpenVLA-OFT|97.1|25_._6_×_|4_×_64_×_150k|
|GeoVLA|97.7|3_._2_×_|1_×_256_×_20k|
|3D-CAVLA|98.1|3_._0_×_|4_×_8_×_150k|
|Spatial Forcing|**98.5**|24_._0_×_|4_×_64_×_150k|
|<br>**ROCKET**|**98.5**|1_._0_×_|1_×_32_×_50k|


proposed _shared_ projector improves performance to 98 _._ 2%. Finally, adding the Matryoshka-style sparse activation further increases performance to 98 _._ 5%. 

_Table 8._ Ablation study of **ROCKET** on LIBERO. 

|**Method**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|
|Baseline|96.9|98.7|97.6|94.8|96.4|
|+ Multi-layer|93.6|99.2|42.2|85.0|80.0|
|+ Shared|**99.0**|**99.8**|97.0|96.8|98.2|
|+ Matryoshka|98.2|**99.8**|**98.8**|**97.0**|**98.5**|


## **7. Conclusion** 

We presented **ROCKET** , a residual-oriented multi-layer representation alignment framework that transfers 3D spatial priors from a strong vision foundation model into 2Dpretrained VLA models. By using a _layer-invariant shared projector_ , **ROCKET** mitigates gradient interference that arises in na¨ıve multi-layer distillation, and our Matryoshkastyle sparse activation further balances supervision across depths. Extensive experiments show that **ROCKET** consistently improves spatial grounding and generalization across datasets and VLA backbones, achieving near state-of-the-art performance on LIBERO with only a small fraction of the compute. We hope **ROCKET** offers a simple and scalable route to more reliable 3D-aware robotic manipulation. 

8 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

## **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning and Embodied AI. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

Ren, A. Z., Shi, L. X., Smith, L., Springenberg, J. T., Stachowicz, K., Tanner, J., Vuong, Q., Walke, H., Walling, A., Wang, H., Yu, L., and Zhilinsky, U. _π_ 0 _._ 5: a visionlanguage-action model with open-world generalization. In _Proceedings of The 9th Conference on Robot Learning (CoRL)_ , volume 305 of _Proceedings of Machine Learning Research_ , pp. 17–40. PMLR, 2025. 

## **References** 

- Aldaco, J., Armstrong, T., Baruch, R., Bingham, J., Chan, S., Draper, K., Dwibedi, D., Finn, C., Florence, P., Goodrich, S., et al. Aloha 2: An enhanced low-cost hardware for bimanual teleoperation. _arXiv preprint arXiv:2405.02292_ , 2024. 

- Beyer, L., Steiner, A., Pinto, A. S., Kolesnikov, A., Wang, X., Salz, D., Neumann, M., Alabdulmohsin, I., Tschannen, M., Bugliarello, E., Unterthiner, T., Keysers, D., Koppula, S., Liu, F., Grycner, A., Gritsenko, A., Houlsby, N., Kumar, M., Rong, K., Eisenschlos, J., Kabra, R., Bauer, M., Bosnjak, M., Chen, X., Minderer, M., Voigt-ˇ laender, P., Bica, I., Balazevic, I., Puigcerver, J., Papalampidi, P., Henaff, O., Xiong, X., Soricut, R., Harmsen, J., and Zhai, X. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- Bhat, V., Lan, Y.-H., Krishnamurthy, P., Karri, R., and Khorrami, F. 3d cavla: Leveraging depth and 3d context to generalize vision language action models for unseen tasks. _arXiv preprint arXiv:2505.05800_ , 2025. 

- Bjorck, J., Fernando Castaneda,˜ N. C., Da, X., Ding, R., Fan, L. J., Fang, Y., Fox, D., Hu, F., Huang, S., Jang, J., Jiang, Z., Kautz, J., Kundalia, K., Lao, L., Li, Z., Lin, Z., Lin, K., Liu, G., Llontop, E., Magne, L., Mandlekar, A., Narayan, A., Nasiriany, S., Reed, S., Tan, Y. L., Wang, G., Wang, Z., Wang, J., Wang, Q., Xiang, J., Xie, Y., Xu, Y., Xu, Z., Ye, S., Yu, Z., Zhang, A., Zhang, H., Zhao, Y., Zheng, R., and Zhu, Y. GR00T N1: An open foundation model for generalist humanoid robots. In _ArXiv Preprint_ , March 2025. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L. X., Tanner, J., Vuong, Q., Walling, A., Wang, H., and Zhilinsky, U. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. URL https://arxiv.org/abs/2410.24164. 

- Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Galliker, M. Y., Ghosh, D., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., LeBlanc, D., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., 

- Bu, Q., Yang, Y., Cai, J., Gao, S., Ren, G., Yao, M., Luo, P., and Li, H. Univla: Learning to act anywhere with taskcentric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 

- Cen, J., Yu, C., Yuan, H., Jiang, Y., Huang, S., Guo, J., Li, X., Song, Y., Luo, H., Wang, F., et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 

- Chang, B., Meng, L., Haber, E., Tung, F., and Begert, D. Multi-level residual networks from dynamical systems view. _arXiv preprint arXiv:1710.10348_ , 2017. 

- Chen, P., Liu, S., Zhao, H., and Jia, J. Distilling knowledge via knowledge review. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 5008–5017, 2021. 

- Chen, T., Chen, Z., Chen, B., Cai, Z., Liu, Y., Li, Z., Liang, Q., Lin, X., Ge, Y., Gu, Z., et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025a. 

- Chen, X., Chen, Y., Fu, Y., Gao, N., Jia, J., Jin, W., Li, H., Mu, Y., Pang, J., Qiao, Y., et al. Internvla-m1: A spatially guided vision-language-action framework for generalist robot policy. _arXiv preprint arXiv:2510.13778_ , 2025b. 

- Chen, Y., Wang, S., Liu, J., Xu, X., de Hoog, F., and Huang, Z. Improved feature distillation via projector ensemble. _Advances in Neural Information Processing Systems_ , 35: 12084–12095, 2022. 

- Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., and Song, S. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11): 1684–1704, 2025. 

- Cortes, C., Mohri, M., and Rostamizadeh, A. Algorithms for learning kernels based on centered alignment. _The Journal of Machine Learning Research_ , 13(1):795–828, 2012. 

- Fei, S., Wang, S., Shi, J., Dai, Z., Cai, J., Qian, P., Ji, L., He, X., Zhang, S., Fei, Z., et al. Libero-plus: In-depth robustness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 

9 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

- Gao, J., He, D., Tan, X., Qin, T., Wang, L., and Liu, T.-Y. Representation degeneration problem in training natural language generation models. _arXiv preprint arXiv:1907.12009_ , 2019. 

- Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., Luo, J., Tan, Y. L., Chen, L. Y., Sanketi, P., Vuong, Q., Xiao, T., Sadigh, D., Finn, C., and Levine, S. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- Gong, G., Wang, J., Xu, J., Xiang, D., Zhang, Z., Shen, L., Zhang, Y., JunhuaShu, J., ZhaolongXing, Z., Chen, Z., Liu, P., and Zhang, K. Beyond logits: Aligning feature dynamics for effective knowledge distillation. In Che, W., Nabende, J., Shutova, E., and Pilehvar, M. T. (eds.), _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pp. 23067–23077, Vienna, Austria, July 2025. Association for Computational Linguistics. ISBN 979-8-89176-251-0. doi: 10.18653/v1/2025.acl-long. 1125. URL https://aclanthology.org/2025. acl-long.1125/. 

- Gromov, A., Tirumala, K., Shapourian, H., Glorioso, P., and Roberts, D. A. The unreasonable ineffectiveness of the deeper layers. _arXiv preprint arXiv:2403.17887_ , 2024. 

- Guo, M., Cao, M., Tao, J., Xu, R., Yan, Y., Liang, X., Laptev, I., and Chang, X. Glad: Geometric latent distillation for vision-language-action models. _arXiv preprint arXiv:2512.09619_ , 2025. 

- He, S., Sun, G., Shen, Z., and Li, A. What matters in transformers? not all attention is needed. _arXiv preprint arXiv:2406.15786_ , 2024. 

- Hou, Z., Zhang, T., Xiong, Y., Duan, H., Pu, H., Tong, R., Zhao, C., Zhu, X., Qiao, Y., Dai, J., and Chen, Y. Dita: Scaling diffusion transformer for generalist visionlanguage-action policy. _arXiv preprint arXiv:2503.19757_ , 2025. 

- Hu, E. J., Shen, Y., Wallis, P., et al. Lora: Low-rank adaptation of large language models. _arXiv preprint arXiv:2106.09685_ , 2021. 

- Huang, C.-P., Wu, Y.-H., Chen, M.-H., Wang, Y.-C. F., and Yang, F.-E. Thinkact: Vision-language-action reasoning via reinforced visual latent planning. _arXiv preprint arXiv:2507.16815_ , 2025a. 

- Huang, W., Wang, C., Zhang, R., Li, Y., Wu, J., and Fei-Fei, L. Voxposer: Composable 3d value maps for robotic manipulation with language models. In Tan, J., Toussaint, M., and Darvish, K. (eds.), _Proceedings of The 7th Conference on Robot Learning_ , volume 229 of _Proceedings_ 

_of Machine Learning Research_ , pp. 2225–2240. PMLR, 06–09 Nov 2023. 

- Huang, X., Wu, J., Xie, Q., and Han, K. Mllms need 3daware representation supervision for scene understanding. _arXiv preprint arXiv:2506.01946_ , 2025b. 

- Hurst, A., Lerer, A., Goucher, A. P., Perelman, A., Ramesh, A., Clark, A., Ostrow, A., Welihinda, A., Hayes, A., Radford, A., et al. Gpt-4o system card. _arXiv preprint arXiv:2410.21276_ , 2024. 

- Karamcheti, S., Nair, S., Balakrishna, A., Liang, P., Kollar, T., and Sadigh, D. Prismatic vlms: Investigating the design space of visually-conditioned language models. In _Forty-first International Conference on Machine Learning_ , 2024. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake, R., Sadigh, D., Levine, S., Liang, P., and Finn, C. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- Kusupati, A., Bhatt, G., Rege, A., Wallingford, M., Sinha, A., Ramanujan, V., Howard-Snyder, W., Chen, K., Kakade, S., Jain, P., et al. Matryoshka representation learning. _Advances in Neural Information Processing Systems_ , 35:30233–30249, 2022. 

- Lee, B.-K., Hachiuma, R., Wang, Y.-C. F., Ro, Y. M., and Wu, Y.-H. Vlsi: Verbalized layers-to-interactions from large to small vision language models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 29545–29557, 2025. 

- Li, F., Song, W., Zhao, H., Wang, J., Ding, P., Wang, D., Zeng, L., and Li, H. Spatial forcing: Implicit spatial representation alignment for vision-language-action model. _arXiv preprint arXiv:2510.12276_ , 2025. 

- Lin, H., Chen, S., Liew, J., Chen, D. Y., Li, Z., Shi, G., Feng, J., and Kang, B. Depth anything 3: Recovering the visual space from any views. _arXiv preprint arXiv:2511.10647_ , 2025a. 

- Lin, J., Taherin, A., Akbari, A., Akbari, A., Lu, L., Chen, G., Padir, T., Yang, X., Chen, W., Li, Y., et al. Vote: visionlanguage-action optimization with trajectory ensemble voting. _arXiv preprint arXiv:2507.05116_ , 2025b. 

- Liu, H., Zhu, Y., Anand, A., Guo, Z., Stone, P., and Levine, S. Libero: Benchmarking knowledge transfer for lifelong robot learning. _arXiv preprint arXiv:2306.03310_ , 2023. 

10 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

- Liu, S., Wu, L., Li, B., Tan, H., Chen, H., Wang, Z., Xu, K., Su, H., and Zhu, J. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- Mesnard, T., Hardin, C., Dadashi, R., Bhupatiraju, S., Pathak, S., Sifre, L., Riviere,` M., Kale, M. S., Love, J., et al. Gemma: Open models based on gemini research and technology. _arXiv preprint arXiv:2403.08295_ , 2024. 

- Miles, R. and Mikolajczyk, K. Understanding the role of the projector in knowledge distillation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pp. 4233–4241, 2024. 

- Miles, R., Elezi, I., and Deng, J. Vkd: Improving knowledge distillation using orthogonal projections. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 15720–15730, 2024. 

- Oquab, M., Darcet, T., Moutakanni, T., Vo, H., Szafraniec, M., Khalidov, V., Fernandez, P., Haziza, D., Massa, F., ElNouby, A., et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 

- Peebles, W. and Xie, S. Scalable diffusion models with transformers. _arXiv preprint arXiv:2212.09748_ , 2022. 

- Perez, E., Strub, F., De Vries, H., Dumoulin, V., and Courville, A. Film: Visual reasoning with a general conditioning layer. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 32, 2018. 

- Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., Wang, Z., Gu, J., Zhao, B., Wang, D., and Li, X. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- Ranftl, R., Bochkovskiy, A., and Koltun, V. Vision transformers for dense prediction. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pp. 12179–12188, 2021. 

- Shi, H., Xie, B., Liu, Y., Sun, L., Liu, F., Wang, T., Zhou, E., Fan, H., Zhang, X., and Huang, G. Memoryvla: Perceptual-cognitive memory in vision-languageaction models for robotic manipulation. _arXiv preprint arXiv:2508.19236_ , 2025. 

- Shridhar, M., Manuelli, L., and Fox, D. Cliport: What and where pathways for robotic manipulation. In Faust, A., Hsu, D., and Neumann, G. (eds.), _Proceedings of The 5th Conference on Robot Learning_ , volume 164 of _Proceedings of Machine Learning Research_ , pp. 894–906. PMLR, 08–11 Nov 2022. URL https://proceedings. mlr.press/v164/shridhar22a.html. 

- Shridhar, M., Manuelli, L., and Fox, D. Perceiveractor: A multi-task transformer for robotic manipulation. In Liu, K., Kulic, D., and Ichnowski, J. (eds.), _Proceedings of The 6th Conference on Robot Learning_ , volume 205 of _Proceedings of Machine Learning Research_ , pp. 785–799. PMLR, 14–18 Dec 2023. URL https://proceedings.mlr.press/ v205/shridhar23a.html. 

- Skean, O., Arefin, M. R., Zhao, D., Patel, N., Naghiyev, J., LeCun, Y., and Shwartz-Ziv, R. Layer by layer: Uncovering hidden representations in language models. _arXiv preprint arXiv:2502.02013_ , 2025. 

- Sun, L., Xie, B., Liu, Y., Shi, H., Wang, T., and Cao, J. Geovla: Empowering 3d representations in vision-language-action models. _arXiv preprint arXiv:2508.09071_ , 2025. 

- Sun, S., Cheng, Y., Gan, Z., and Liu, J. Patient knowledge distillation for bert model compression. _arXiv preprint arXiv:1908.09355_ , 2019. 

- Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi, A., Babaei, Y., Bashlykov, N., Batra, S., Bhargava, P., Bhosale, S., Bikel, D., Blecher, L., Ferrer, C. C., Chen, M., Cucurull, G., Esiobu, D., Fernandes, J., Fu, J., Fu, W., Fuller, B., Gao, C., Goswami, V., Goyal, N., Hartshorn, A., Hosseini, S., Hou, R., Inan, H., Kardas, M., Kerkez, V., Khabsa, M., Kloumann, I., Korenev, A., Koura, P. S., Lachaux, M.-A., Lavril, T., Lee, J., Liskovich, D., Lu, Y., Mao, Y., Martinet, X., Mihaylov, T., Mishra, P., Molybog, I., Nie, Y., Poulton, A., Reizenstein, J., Rungta, R., Saladi, K., Schelten, A., Silva, R., Smith, E. M., Subramanian, R., Tan, X. E., Tang, B., Taylor, R., Williams, A., Kuan, J. X., Xu, P., Yan, Z., Zarov, I., Zhang, Y., Fan, A., Kambadur, M., Narang, S., Rodriguez, A., Stojnic, R., Edunov, S., and Scialom, T. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 

- Wang, H., Zheng, A., Zhao, Y., Wang, T., Ge, Z., Zhang, X., and Zhang, Z. Reconstructive visual instruction tuning. _arXiv preprint arXiv:2410.09575_ , 2024. 

- Wang, J., Chen, M., Karaev, N., Vedaldi, A., Rupprecht, C., and Novotny, D. Vggt: Visual geometry grounded transformer. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 5294–5306, 2025a. 

- Wang, Y., Zhou, J., Zhu, H., Chang, W., Zhou, Y., Li, Z., Chen, J., Pang, J., Shen, C., and He, T. _π_<sup>3</sup> : Permutationequivariant visual geometry learning. _arXiv preprint arXiv:2507.13347_ , 2025b. 

- Weinan, E. A proposal on machine learning via dynamical systems. _Communications in Mathematics and Statistics_ , 5(1):1–11, 2017. 

11 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

- Yu, S., Kwak, S., Jang, H., Jeong, J., Huang, J., Shin, J., and Xie, S. Representation alignment for generation: Training diffusion transformers is easier than you think. _arXiv preprint arXiv:2410.06940_ , 2024. 

- Zhai, X., Mustafa, B., Kolesnikov, A., and Beyer, L. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 11975–11986, 2023. 

- Zheng, R., Liang, Y., Huang, S., Gao, J., Daume´ III, H., Kolobov, A., Huang, F., and Yang, J. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ , 2024. 

- Zitkovich, B., Joshi, A., Brohan, A., Brown, N., Chebotar, Y., Cortes, O., Ding, T., Driess, D., Dubey, A. K., Florence, P., Fu, C., Gopalakrishnan, K., Han, K., Hausman, K., Herzog, A., Hsu, J., Ichter, B., Irpan, A., Kollar, T., Lam, G., Levine, S., Liang, P., Nair, S., Narang, Y., Pathak, D., Radosavovic, I., Raff, E., Rao, K., Rettinghouse, Z., Salazar, J., Sermanet, P., Sievers, T., Tan, J., Toussaint, M., Vanhoucke, V., Vuong, Q., Wulfmeier, M., Xiao, T., Finn, C., and Guadarrama, S. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In Tan, J., Toussaint, M., and Darvish, K. (eds.), _Proceedings of The 7th Conference on Robot Learning_ , volume 229 of _Proceedings of Machine Learning Research_ , pp. 2165–2183. PMLR, 06–09 Nov 2023. URL https://proceedings.mlr.press/ v229/zitkovich23a.html. 

12 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

## **A. Training Details** 

**Teacher Freezing.** Throughout the entire training pipeline, we keep the teacher model frozen and only fine-tune the student VLA model. 

**Learning Rate Schedule and Batch Size.** We train OPENVLA-7B for a total of 50 _,_ 000 steps, following its default learning-rate decay strategy with a minor adjustment: we keep the learning rate at 5 _×_ 10<sup>_−_4</sup> for the first 10 _,_ 000 steps, and then decay it to 5 _×_ 10<sup>_−_5</sup> for the remainder of training. We use a batch size of 32. 

For the search-oriented experiments in Sec. 6.1, Sec. 6.2 and Table 6, to reduce computational cost we decrease the batch size to 16. Meanwhile, to avoid under-training, we keep the learning rate at 5 _×_ 10<sup>_−_4</sup> for the first 30 _,_ 000 steps and then decay it to 5 _×_ 10<sup>_−_5</sup> afterwards. 

**PI-Model Experiments.** For experiments related to PI0.5, we set the batch size to 64 and train the model in PyTorch; all other settings follow the default configuration. For PI0 experiments on ROBOTWIN 2.0, we use a batch size of 16 and train with the JAX implementation. 

We also observe that in such single-task settings, the action loss typically converges quickly. Therefore, we reduce the coefficient of the alignment loss from its default value of 0.5 to 0.125, which yields strong empirical performance. 

## **B. Performance Trajectories on LIBERO Across Training** 

Table 9 reports success rates on the four LIBERO suites (Spatial, Object, Goal, and Long) at different training stages, together with the overall average. Unlike single-point evaluation at the end of training, this table highlights performance trajectories over the full training course, enabling a more complete comparison of training dynamics across methods. 

_Table 9._ Success rates (%) on the LIBERO benchmarks. We compare the performance trajectories of multiple methods over the full training course; **bold** indicates the best final result, and underlining indicates the best result achieved during training. 

|**Method**|**Steps**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|---|
||10k|74.6|89.4|78.6|37.2|70.0|
|Bli|20k|93.0|99.6|97.6|94.4|96.2|
|asene|30k|94.6|99.2|98.2|93.6|96.4|
||50k|94.0|97.2|98.0|92.4|95.4|
||10k|83.4|99.8|52.6|31.6|66.9|
|Sil Fi|20k|94.2|99.8|94.8|90.4|94.8|
|pata orcng|30k|97.8|**100.0**|92.6|95.2|96.4|
||50k|97.8|98.8|96.2|90.6|95.9|
||10k|86.2|74.6|22.4|52.6|59.0|
||20k|93.8|99.8|35.0|83.4|78.0|
|Multi-layer Alignment|30k|94.6|**100.0**|37.4|81.8|78.5|
||50k|93.6|99.2|42.2|85.0|80.0|
||10k|94.2|95.2|70.4|70.2|82.5|
|hl|20k|94.0|99.6|97.4|94.6|96.4|
|**ROCKET**(Sared-ony)|30k|97.0|99.6|98.6|92.4|96.9|
||50k|**99.0**|99.8|97.0|96.8|98.2|
||10k|90.8|91.4|74.0|55.6|78.0|
||20k|93.4|**100.0**|98.0|94.4|96.5|
|**ROCKET**|30k|96.0|99.2|98.0|93.8|96.8|
||50k|98.2|99.8|**98.8**|**97.0**|**98.5**|


## **C. Dataset Details** 

### **C.1. LIBERO** 

LIBERO (Liu et al., 2023) is a benchmark suite for language-conditioned robotic manipulation, designed to evaluate multi-task imitation learning and generalization. The original LIBERO release consists of **12** manipulation tasks grouped 

13 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

into **4** task suites, instantiated across **3** robot embodiments. Tasks are defined with natural language instructions, enabling direct study of vision-language-action (VLA) policy learning. 

The four task suites capture complementary generalization axes. LIBERO-SPATIAL focuses on spatial configuration variation, LIBERO-OBJECT emphasizes object-level diversity, LIBERO-GOAL introduces goal variation within shared task structures, and LIBERO-LONG contains long-horizon, multi-stage manipulation tasks requiring sequential reasoning (Liu et al., 2023). This structured design enables controlled evaluation of cross-task and cross-goal generalization. 

LIBERO provides expert demonstration trajectories collected in simulation using RoboSuite. The original dataset contains approximately **20,000** demonstration episodes in total, with each task comprising roughly **1,500–2,000** trajectories depending on task complexity. Each episode consists of temporally dense state-action sequences spanning hundreds of timesteps. 

Each episode includes synchronized multimodal observations, including RGB images from fixed camera viewpoints and robot proprioceptive states such as joint positions and gripper status. Actions are specified in continuous control space, typically as end-effector pose commands. Data are stored in a standardized trajectory format, facilitating efficient loading and integration with common imitation learning pipelines. 

### **C.2. LIBERO-Plus** 

LIBERO-Plus (Fei et al., 2025) is an extended version of the original LIBERO benchmark, designed to scale up task diversity and data volume while preserving the same language-conditioned manipulation setting. LIBERO-Plus significantly expands the number of tasks and demonstrations, enabling evaluation of large-capacity vision-language-action (VLA) models under more data-rich and heterogeneous training regimes. 

Compared to the original LIBERO benchmark, LIBERO-Plus includes **over 100** manipulation tasks spanning a broader range of object configurations, goal specifications, and scene layouts. Tasks are defined using natural language instructions and are organized to support both multi-task learning and compositional generalization. The expanded task set increases structural and semantic diversity, making LIBERO-Plus more suitable for training and evaluating foundation-scale robotic policies. 

LIBERO-Plus provides a substantially larger collection of expert demonstration trajectories generated in simulation. In total, the dataset contains **hundreds of thousands of demonstration episodes** , with each task comprising thousands of trajectories. Each episode consists of temporally dense state-action sequences, supporting long-horizon policy learning and sequence modeling. 

Each episode includes synchronized multimodal observations, including RGB visual inputs, robot proprioceptive states, and continuous control actions specified in end-effector space. Data are stored in the same standardized trajectory format as LIBERO, enabling seamless reuse of training pipelines and direct comparison across LIBERO and LIBERO-Plus benchmarks. 

### **C.3. RoboTwin 2.0** 

RoboTwin 2.0 (Chen et al., 2025a) is a large-scale simulation benchmark and dataset for bimanual robotic manipulation, providing both an automated data generator and unified evaluation protocols. The official release instantiates **50 dual-arm tasks** across **5 robot embodiments** , targeting robust long-horizon manipulation with diverse object interactions. RoboTwin 2.0 is built on an annotated object library (RoboTwin-OD) containing **731 object instances** spanning **147 categories** , enabling systematic task variation in object geometry, placement, and scene composition. 

In addition to the generator, RoboTwin 2.0 provides **over 100,000** pre-collected expert trajectories/episodes for downstream training and benchmarking. Each episode consists of temporally aligned state-action sequences with multimodal observations. Visual observations include rendered RGB images from calibrated cameras (often multi-view) to capture both global context and fine-grained contact-relevant details. Proprioceptive observations include robot joint states (e.g., positions/velocities) and gripper states. Actions are specified in continuous control space (e.g., end-effector or joint-space commands), which makes the dataset compatible with standard imitation learning and policy learning pipelines. 

Overall, RoboTwin 2.0 is designed to support scalable training and controlled evaluation of general-purpose policies, particularly for studying cross-task and cross-embodiment generalization under instruction- or goal-conditioned settings. 

14 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

## **D. Model Details** 

### **D.1. OpenVLA** 

OpenVLA (Kim et al., 2024) is a 7B-parameter VLA based on the **Prismatic-7B VLM** (Karamcheti et al., 2024) framework. The architecture’s vision tower employs a fused visual encoder (totaling 600M parameters) constructed by combining two pretrained vision models: **DINOv2** (Oquab et al., 2023) and **SigLIP** (Zhai et al., 2023). Specifically, input image patches are passed separately through both encoders, and the resulting feature vectors are concatenated channel-wise. These fused visual features are then mapped into the language embedding space via a small 2-layer Multi-Layer Perceptron **(MLP) projector** . The central reasoning engine is a 7B-parameter **Llama 2** (Touvron et al., 2023) language model backbone, which processes the interleaved visual tokens and language instructions to predict 7-dimensional robot actions. It features **32 Transformer layers** with **a hidden dimension of 4096** and **32 attention heads** . OpenVLA represents robot actions by discretizing them into **256 bins per dimension** , treating them as specialized tokens within the LLM’s vocabulary. 

### **D.2. OpenVLA-OFT** 

OpenVLA-OFT (Kim et al., 2025) is a fine-tuning variant of OpenVLA that inherits the same base components. Instead of discretizing actions, OpenVLA-OFT employs a **continuous action prediction head** —a 2-block MLP ResNet that directly predicts 7-dimensional continuous actions from the LLM’s hidden states via L1 regression. During fine-tuning, OpenVLA-OFT freezes the vision tower and projector and applies **LoRA** (Hu et al., 2021) adapters to the LLM backbone, targeting all linear layers in self-attention and MLP blocks. OpenVLA-OFT+ extends it with **FiLM** (Perez et al., 2018) for enhanced language grounding. Specifically, FiLM applies learnable affine transformations to the visual features based on the language instruction, enabling the model to modulate visual representations according to task-specific language cues. 

### **D.3. PI0** 

PI0(Black et al., 2024) is a vision-language-action (VLA) model that generates robot action sequences using flow matching. The model employs a dual-expert architecture: a vision-language expert and an action expert. The vision tower uses **SigLIP So400m/14** (Zhai et al., 2023). The language model is **PaliGemma** (Beyer et al., 2024) based on Gemma 2B (Mesnard et al., 2024), with **hidden dimension 2048, 18 transformer layers** . The action expert is a **Gemma 300M** model with hidden dimension 1024, 18 layers. During training, PI0 learns a velocity field _vt_ ( _x_ ) via **flow matching** . 

### **D.4. PI0.5** 

PI0.5 (Black et al., 2025) shares the same architectural foundation as PI0 but introduces two key modifications for improved open-world generalization through knowledge insulation. First, instead of providing the robot state as a continuous vector in the suffix, PI0.5 discretizes the state into **256 bins** over [ _−_ 1 _,_ 1] and incorporates it as discrete tokens in the language prefix. Second, PI0.5 replaces MLP-based timestep fusion with adaptive RMS normalization ( **AdaRMSNorm** ) for timestep conditioning. The timestep embedding is processed through a two-layer MLP with Swish activations to produce a 1024dimensional condition vector. This condition is injected into the action expert through AdaRMSNorm layers in each of the 18 transformer layers, where AdaRMSNorm dynamically generates scale and shift parameters, which provides more flexible timestep conditioning compared to the MLP fusion approach in PI0. 

## **E. Projector Similarity** 

We flatten the MLP parameters of each independently initialized projector (i.e., _ϕ_ = _{W_ 1 _, W_ 2 _}_ ) and compute the pairwise cosine similarities. As shown in Fig. 7, the similarities between different projectors are nearly zero, indicating that naive multi-layer alignment with multiple independent projectors tends to learn distinct mapping trajectories when modeling the transformation from one residual stream to another. This discrepancy can lead to gradient conflicts, which in turn degrades the final performance. 

## **F. Why We Need a Nested Sparse-Activation Mechanism to Balance Multiple Alignment Losses** 

We compute the similarity between the student model OpenVLA-7B and the teacher model VGGT using centered kernel alignment (CKA) (Cortes et al., 2012). As shown in Fig.8, we observe that the shallow layers of VGGT are more similar to OpenVLA-7B, while the similarity gradually decreases as the depth increases. This finding not only suggests that different 

15 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 


_Figure 7._ Pairwise cosine similarity of flattened MLP parameters for independently initialized projectors. The similarities are nearly zero, suggesting that naive multi-layer alignment with multiple independent projectors learns distinct mapping trajectories, which can induce gradient conflicts and harm final performance. 

layers of VGGT contain semantic information with varying levels of richness, but also indicates that it is easier to align VGGT and OpenVLA-7B at shallow layers. In practice, a shared projector typically learns a mapping that works well for aligning shallow layers; however, it often fails to achieve equally good alignment for deeper layers. 

To address this multi-layer alignment mismatch, we propose a nested sparse-activation mechanism. The key idea is to let shallow layers activate (and thus update/use) fewer parameters in the projector, and gradually increase the number of activated parameters as the layer depth increases, until reaching the full projector capacity at the deepest layers. 

**CKA principle.** CKA measures the similarity between two representation spaces by comparing their induced pairwise similarity structure, and can be viewed as a normalized version of HSIC (Hilbert-Schmidt Independence Criterion). Concretely, suppose we collect representations from one layer of the student model as a matrix _X ∈_ R<sup>_n×dx_</sup> and from one layer of the teacher model as _Y ∈_ R<sup>_n×dy_</sup> , where _n_ is the number of matched observations (e.g., the same _n_ tokens or image regions), while _dx_ and _dy_ can be different. 

A common choice is _linear CKA_ , computed via Gram matrices: 


Then CKA is 


where _⟨A, B⟩F_ = tr( _A_<sup>_⊤_</sup> _B_ ) is the Frobenius inner product. Equivalently, for centered _X_ and _Y_ , linear CKA can be written as: 


Importantly, the above formulation does _not_ require _dx_ = _dy_ ; it only requires that _X_ and _Y_ share the same number of rows _n_ (i.e., aligned observations). Intuitively, CKA compares how similarly the two models organize the same set of examples in 

16 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 


_Figure 8._ **Layer-wise CKA similarity between OpenVLA-7B and VGGT.** We compute linear CKA between OpenVLA-7B vision-token representations and VGGT visual features across layers. Higher values indicate more similar representations. Shallow VGGT layers exhibit higher similarity to OpenVLA-7B, and similarity generally decreases with depth. 

17 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

representation space, and it is invariant to isotropic scaling (and, in the linear case, robust to orthogonal transformations), making it suitable for cross-model, cross-dimension similarity analysis. 

**Details of computing CKA similarity between OpenVLA-7B and VGGT.** Since OpenVLA-7B and VGGT have different hidden dimensions, we adopt CKA because it can compare representations of different feature dimensions as long as they are evaluated on the same set of samples (tokens/images), i.e., the same number of observations. 

In our implementation, we measure representation similarity between OpenVLA-7B (student) and VGGT (teacher) using _linear CKA_ on a held-out set of samples. For each input batch, we extract the vision-token hidden states from selected layers of OpenVLA-7B and the corresponding visual features from selected layers of VGGT. Since the two models have different spatial resolutions and hidden dimensions, we first resample the VGGT features to match the spatial layout of OpenVLA’s vision tokens, then flatten both representations into per-sample feature vectors and concatenate all samples to form matrices _X ∈_ R<sup>_N×Dx_</sup> and _Y ∈_ R<sup>_N×Dy_</sup> . We then compute linear CKA for every layer pair by constructing and centering Gram matrices _K_ = _XX_<sup>_⊤_</sup> and _L_ = _Y Y_<sup>_⊤_</sup> , and reporting the normalized HSIC score CKA( _X, Y_ ) = _⟨K,_<sup>˜</sup> _L_<sup>˜</sup> _⟩F /_ ( _∥K_<sup>˜</sup> _∥F ∥L_<sup>˜</sup> _∥F_ ), which is comparable even when _Dx̸_ = _Dy_ . 

## **G. Per-task Results on LIBERO-Plus** 

Detailed per-task results corresponding to Fig. 5 are provided in Figs. 9–12. 


_Figure 9._ Per-task success rate (%) on LIBERO-Plus **Spatial** tasks under the seven perturbations. 


_Figure 10._ Per-task success rate (%) on LIBERO-Plus **Object** tasks under the seven perturbations. 


_Figure 11._ Per-task success rate (%) on LIBERO-Plus **Goal** tasks under the seven perturbations. 

18 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 


_Figure 12._ Per-task success rate (%) on LIBERO-Plus **Long** tasks under the seven perturbations. 

## **H. Analysis: Why Shared Projectors Increase Cross-Layer Gradient Coherence** 

### **H.1. Takeaway: shared projector makes cross-layer gradients add constructively** 

This section explains why a _shared_ nonlinear projector tends to yield more _cross-layer coherent_ distillation gradients than _layer-specific_ independent projectors in a Pre-LN Transformer. The argument has two steps: (i) under Pre-LN _residual-smallness_ , back-propagation through the residual stream is close to identity, so the gradient at an earlier layer is approximately a superposition of _future local_ distillation gradients; (ii) the stability of this superposition is governed by _cross-layer interference_ terms, and a shared projector imposes a common operator structure on these terms (up to controlled deviation), whereas Multiple independent projectors do not. 

### **H.2. Setup: Pre-LN residual stream, nonlinear projector, and distillation loss** 

Let the student network be a Pre-LN Transformer written on the residual stream: 


where _hl ∈_ R<sup>_d_</sup> denotes the (flattened) residual representation at layer _l_ , LN( _·_ ) is LayerNorm, and _θl_ are the block parameters. Define _ul_ := LN( _hl_ ) and ∆ _l_ := _Fl_ ( _ul_ ; _θl_ ) so that _hl_ +1 = _hl_ + ∆ _l_ . 

**Nonlinear projector.** For each distillation layer _l ∈S_ , we attach a two-layer MLP projector (with input normalization LN _v_ ): 


where _ϕ_ = _{W_ 1 _, W_ 2 _}_ (and potentially LN _v_ parameters). 

**Layerwise distillation loss.** Let _tl_ denote the teacher representation used as the distillation target for the student’s layer _l_ , selected via a fixed layer mapping. We define the multi-layer distillation objective: 


where _ℓ_ ( _·, ·_ ) is any differentiable similarity loss (e.g., 1 _−_ cos( _·, ·_ )), and _αl ≥_ 0 is the coefficient of the alignment loss; by default, we use uniform (mean) weighting. 

### **H.3. Jacobians needed for gradient transport and projector-induced coupling** 

**Pre-LN residual Jacobian.** Differentiating (17) yields 


**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

where _J_ LN( _hl_ ) denotes the Jacobian of LN at _hl_ . Thus, for _i < l_ , 


**Projector Jacobian.** Let _x_ := _W_ 1 _h_<sup>˜</sup> and _Dσ_ ( _x_ ) := diag( _σ_<sup>_′_</sup> ( _x_ )). Then the Jacobian of (19) is 


where _J_ LN _v_ ( _h_ ) is the Jacobian of LN _v_ . 

### **H.4. Exact gradient at an early layer and its superposition approximation** 

This subsection writes the exact distillation gradient at _hi_ and then states the approximation that removes deep transport effects under Pre-LN residual-smallness. 

For each _l ∈S_ , define the local gradient from the distillation loss: 


By the chain rule, the gradient at the student layer _l_ is: 


For an earlier layer _i < l_ , the gradient is back-propagated through the residual blocks. Note that for a product of matrices _Ml−_ 1 _. . . Mi_ , the transpose reverses the order to _Mi_<sup>_⊤. . . M_</sup> _l_<sup>_⊤_</sup> _−_ 1<sup>.Thus, we have:</sup> 


where the product is ordered from _k_ = _i_ (leftmost) to _l −_ 1 (rightmost). Summing over all distillation layers _l ≥ i_ gives the total gradient at layer _i_ : 


### **H.5. Residual-smallness implies near-identity transport** 

**Assumption (Residual-smallness for Pre-LN).** There exists _ε >_ 0 such that for all _k_ of interest, 


**Lemma 1 (Near-identity transport).** Under (28), for any _i < l_ , the back-propagation matrix remains close to the identity: 


For small depth or residuals (i.e., ( _l − i_ ) _ε ≪_ 1), this bound is approximately ( _l − i_ ) _ε_ . 

**Corollary 1 (Gradient is a sum of local distillation gradients, up to transport error).** Substituting the bound from Lemma 1 into (27), we obtain that the gradient at layer _i_ is the superposition of future local gradients plus an error term dependent on depth: 


where the error _Ei_ is bounded by order _O_ <u>�</u> _ε_<sup>�</sup> _l≥i_<sup>(</sup><sup>_l −i_)</sup><sup>_αl∥J_</sup> _p_<sup>_⊤_</sup> _ϕl_<sup>_gl∥_</sup> <u>�.</u> 

20 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

### **H.6. Shared projector makes cross-layer interference constructive** 

By Corollary 1, the stability of the early-layer update is controlled by how the terms _Jpϕl_ ( _hl_ )<sup>_⊤_</sup> _gl_ interact across distillation layers. We now show that sharing the projector creates a _common operator_ governing these interactions (up to controlled deviation), yielding a signal-aligned lower bound on cross-layer interference. 

We compare two parameterization strategies for the auxiliary tasks: 

- **Multiple independent projectors:** each _l ∈S_ has distinct parameters _ϕl_ . 

- **Shared projector:** a single set of parameters _ϕl ≡ ϕ_ is used for all _l ∈S_ . 

**Gradient forms and the interference term.** Recalling (30), the gradient at representation _hi_ is a superposition of terms. Let 


The squared norm expands as 


where the cross terms _⟨va, vb⟩_ determine whether different distillation layers reinforce or cancel each other. 

**Proposition 1 (Cross-layer interference as a bilinear form on teacher-side error signals).** For any _a, b ∈S_ , 


**Error-signal subspace.** Let the _error-signal subspace_ be 


All teacher-side signals that affect the student update through distillation lie in _G_ by construction. Accordingly, we will only require geometric regularity of the shared projector on _G_ . 

### H.6.1. **CASE 1 (SHARED PROJECTOR): A COMMON PSD OPERATOR GOVERNS CROSS-LAYER INTERFERENCE.** 

The advantage of shared projector is that cross-layer interactions are governed by (approximately) a _single_ operator on the teacher-side error signals. The following assumptions control how the shared projector Jacobian varies along the residual stream, enabling us to relate _Mab_ to a fixed PSD reference operator. 

**Assumption (Bounded residual increments).** There exists _δ >_ 0 such that for all layers _l_ , 


**Assumption (Projector Jacobian Lipschitz).** There exists _LJ >_ 0 such that for all _x, y_ in the bounded feature domain, 


**Lemma 2 (Cross-layer Jacobian closeness under residual dynamics).** Under (35) and (36), for any _a < b_ , 


To convert Jacobian closeness into a statement about alignment, we introduce an _on-subspace_ near-isometry requirement on the teacher-side signals that actually occur. 

21 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

**Assumption (Near-isometry on the error-signal subspace).** For a reference layer<sup>¯</sup> _l ∈S_ and _h_<sup>¯</sup> := _h_ ¯ _l_ , define 


Assume there exist constants _c >_ 0 and _η ∈_ [0 _,_ 1) such that for all _x ∈G_ , 


Equivalently, _M_ has condition number at most 1<sup>1</sup> _−_<sup><u>+</u></sup><sup>_<u>η</u>_</sup> _η_<sup>when restricted to</sup><sup>_G_.</sup> 

**Lemma 3 (Approximate inner-product preservation on** _G_ **).** Under (39), for all _x, y ∈G_ , 


_Proof sketch._ Use the polarization identity _x_<sup>_⊤_</sup> _My_ = 4<sup><u>1</u></sup> �( _x_ + _y_ )<sup>_⊤_</sup> _M_ ( _x_ + _y_ ) _−_ ( _x − y_ )<sup>_⊤_</sup> _M_ ( _x − y_ )� and apply the quadratic bounds (39) to _x ± y_ . 

**Proposition 2 (Shared projector cross terms decompose into a common PSD part plus deviation).** Let _h_<sup>¯</sup> = _h_ ¯ _l_ and decompose 


where the bound follows from Lemma 2. Then for any _a, b ∈S_ with _a, b ≥ i_ , 


where the deviation satisfies 


Moreover, if _ga, gb ∈G_ , then by Lemma 3, 


_Interpretation._ When (i) the teacher error signals are consistent across layers ( _ga_<sup>_⊤gb_positive and not too small), (ii) the shared</sup> projector is near-isometric on _G_ (small _η_ ), and (iii) adjacent-layer Jacobians are close (small _∥El∥_ , i.e., small ( _|l −_<sup>¯</sup> _l|δ_ )), the cross-layer interference term is biased toward being non-destructive and often constructive. 

**Theorem H.1** (Shared projector induces coherent cross-layer interference under Pre-LN transport) **.** _Consider the Pre-LN student_ (17) _with multi-layer distillation_ (20) _. Under residual-smallness_ (28) _, the gradient at an earlier representation hi admits the superposition form_ (30) _. For the shared projector parameterization (ϕl ≡ ϕ), assume bounded residual increments_ (35) _, projector Jacobian Lipschitzness_ (36) _, and near-isometry on the error-signal subspace_ (39) _. Then for any a, b ∈S with a, b ≥ i and ga, gb ∈G, the cross-layer interference term ⟨va, vb⟩ in_ (32) _satisfies the shared projector decomposition_ (42) _with deviation bounded by_ (43) _, and furthermore admits the signal-aligned lower bound_ (44) _. Consequently, when teacher-side error signals are positively correlated across layers (large ga_<sup>_⊤gb) and the controlled-deviation terms are small,_</sup> _shared projector gradients exhibit reduced destructive interference and higher cross-layer coherence in the superposition_ (31) _._ 

H.6.2. **CASE 2 (MULTIPLE INDEPENDENT PROJECTORS): LACK OF A UNIFORM CONSTRUCTIVE LOWER BOUND.** 

For Multiple independent projectors, the cross term becomes 


which does not reduce to a single PSD form _ga_<sup>_⊤_(</sup><sup>_JJ⊤_)</sup><sup>_gb_and therefore admits no analogue of (40) or (44) without additional</sup> coupling assumptions. A generic upper bound is 


22 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

but this bound does not preclude sign flips (destructive interference) since the bilinear form _Jpϕa_ ( _ha_ ) _Jpϕb_ ( _hb_ )<sup>_⊤_</sup> is not constrained to be PSD or even symmetric. 

_Empirical specialization and orthogonalization._ In our experiments, we observe a consistent “decoupling” behavior: as training proceeds and the per-layer alignment losses saturate, different projectors tend to rotate their effective Jacobian row spaces into near-orthogonal subspaces. Concretely, if we measure the pairwise similarity between projector weights (or their local linearizations), e.g., cos(vec( _Wa_ ) _,_ vec( _Wb_ )) for linear heads or an analogous metric based on _Jpϕl_ ( _hl_ ), the values decrease toward (and remain close to) zero in the early stage after training has stabilized, and this behavior persists consistently until the end of training (The visualization results are provided in Appendix E (Fig.7).). This indicates that, rather than enforcing a shared representation geometry across layers, independent heads can absorb layer-specific discrepancies by specializing into mutually orthogonal directions, which suppresses cross-layer coupling in (45). In Fig. 1 (top), we show the cosine similarity between the gradients induced by different alignment losses at an early layer (the projector between the vision tower and the LLM backbone) during the early stage of training and the mid-to-late stage. For the 10 layers, we compute the pairwise cosine similarities among their gradients. The visualization shows that the gradients in the early stage are nearly perfectly orthogonal, indicating substantial training fluctuations; in the mid-to-late stage, this low cosine similarity persists. In Fig. 1 (bottom), we visualize the corresponding results for **ROCKET** . From the very early stage of training to the mid-to-late stage, the shared-projector mechanism in **ROCKET** keeps the gradients induced by different alignment losses consistently aligned. This directional consistency holds throughout training, and the resulting mutual reinforcement among gradients contributes to the superior performance of **ROCKET** . Specifically, Fig. 13 shows the gradient similarities in the early stage of training, while Fig. 14 shows the gradient similarities in the mid-to-late stage. 

As a consequence, even when the teacher error signals are correlated across layers (i.e., _ga_<sup>_⊤gb>_0), the induced student-side</sup> gradients _va_ and _vb_ can become weakly correlated because the interaction matrix _Jpϕa_ ( _ha_ ) _Jpϕb_ ( _hb_ )<sup>_⊤_</sup> itself shrinks in the relevant directions. In practice, this often yields a small average cross term E[ _⟨va, vb⟩_ multi] and can even lead to destructive interference when the effective interaction changes sign across mini-batches. 

**Consequence for gradient stability.** Plugging (44) (shared projector) into (32) shows that the second summation in (32) admits a _signal-aligned_ lower bound (up to controlled errors), while Multiple independent projectors admit only the trivial magnitude bound (46). Thus, under the same transport approximation of Corollary 1, shared projector gradients tend to exhibit higher cross-layer coherence and reduced destructive interference, consistent with empirical observations. 

23 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 


_Figure 13._ Gradient cosine similarity in the early stage of training. 

24 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 


_Figure 14._ Gradient cosine similarity in the mid-to-late stage of training. 

25 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

## **I. Details of Layer Selection Strategies** 

### **I.1. Similarity-based Layer Selection** 


_Figure 15._ **Similarity-based layer selection strategies.** We evaluate two criteria for selecting alignment layers: **Sim-1** (left) measures 10-layer window similarity by computing cosine similarity between layer _i_ ’s input and layer _i_ +9’s output; **Sim-2** (right) measures single-layer similarity between each layer’s input and output. For each criterion, we select 10 layers with either highest similarity ( **Top** , green squares) or lowest similarity ( **Last** , orange triangles). 

Figure 15 shows that VGGT (24 layers, top row) and VLA (32 layers, bottom row) reveal distinct similarity distributions across the network depth. Lower similarity indicates greater information transformation, potentially identifying more informative layers for alignment. 

26 

**ROCKET : Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models** 

### **I.2. Detailed Chosen indices for All Layer Selection Strategies** 

|**Strategy**|**# Layers**|**VLA Layers**|**VGGT Layers**|
|---|---|---|---|
|||_Uniform Sampling_||
|Uniform-4|4|8, 16, 24, 32|5, 11, 17, 23|
|Uniform-8|8|4, 8, 12, 16, 20, 24, 28, 32|2, 5, 8, 11, 14, 17, 20, 23|
|Uniform-16|16|4, 5, 6, 7, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,<br>31|1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23|
|Uniform-24|24|2, 3, 4, 6, 7, 8, 10, 11, 12, 14, 15, 16, 18, 19, 20, 22,<br>23, 24, 26, 27, 28, 30, 31, 32|0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,<br>17, 18, 19, 20, 21, 22, 23|
|||_Depth-based Sampling_||
|Shallow|10|1, 2, 3, 4, 5, 6, 7, 8, 9, 10|0, 1, 2, 3, 4, 5, 6, 7, 8, 9|
|Middle|10|12, 13, 14, 15, 16, 17, 18, 19, 20, 21|7, 8, 9, 10, 11, 12, 13, 14, 15, 16|
|Deep|10|23, 24, 25, 26, 27, 28, 29, 30, 31, 32|14, 15, 16, 17, 18, 19, 20, 21, 22, 23|
|||<br>_Even-to-Max (E2M) Sampling_||
|_E_2_M_-_Last_1<sup>_∗_</sup>|10|2, 4, 6, 8, 10, 12, 14, 16, 18, 33|2, 4, 6, 8, 10, 12, 14, 16, 18, 23|
|_E_2_M_-_Last_1<sup>_†_</sup>|10|2 3 4 5 6 7 8 9 10 18|2 4 6 8 10 12 14 16 18 23|
|||, , , , , , , , ,<br>_Similarity-based Sampling_|, , , , , , , , ,|
|Sim-1-Top|10|20, 21, 22, 23, 24, 25, 26, 27, 28, 29|2, 3, 4, 5, 6, 7, 8, 9, 10, 11|
|Sim-1-Last|10|1, 2, 3, 4, 5, 6, 7, 8, 9, 10|8, 9, 10, 11, 12, 13, 14, 15, 16, 17|
|Sim-2-Top|10|4, 5, 6, 7, 24, 26, 27, 28, 29, 30|2, 3, 4, 5, 6, 7, 8, 9, 18, 19|
|Sim-2-Last|10|1, 2, 3, 11, 12, 14, 15, 16, 17, 32|0, 11, 12, 13, 14, 15, 16, 17, 22, 23|


_Table 10._ Detailed layer selection for multi-layer alignment. We show the aligned layer indices for both the student VLA visual backbone and the teacher VGGT model. For OpenVLA, we count the projector between vision tower and LLM as a layer so there are total 33 indices in our default setting. The selected layers are sorted in ascending order for both VLA and VGGT.<sup>_∗_</sup> For OpenVLA (32 layers, or 33 including the projector), we select layers uniformly using indices 2–18 plus the last layer.<sup>_†_</sup> For PI0 and PI0.5 (18 layers), since layer 18 coincides with the last layer, we instead select indices 2–10 plus the last layer. 

27 

