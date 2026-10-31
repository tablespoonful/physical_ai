---
title: "When Robots Obey the Patch: Universal Transferable Patch Attacks on Vision-Language-Action Models"
date: "2025-11-26"
authors: "Hui Lu; Yi Yu; Yiming Yang; Chenyu Yi; Qixin Zhang; Bingquan Shen"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2511.21192
pdf: https://arxiv.org/pdf/2511.21192
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.21192)** / [論文ページ](https://arxiv.org/abs/2511.21192)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **When Robots Obey the Patch: Universal Transferable Patch Attacks on Vision-Language-Action Models** 

Hui Lu<sup>1</sup><sup>_,_2</sup> Yi Yu<sup>2*</sup> Yiming Yang<sup>3</sup> Chenyu Yi<sup>2</sup> Qixin Zhang<sup>3</sup> Bingquan Shen<sup>4</sup> Alex C. Kot<sup>2</sup> Xudong Jiang<sup>2</sup> 

1ROSE Lab, Interdisciplinary Graduate Programme, Nanyang Technological University 2ROSE Lab, School of Electrical and Electronic Engineering, Nanyang Technological University 3CCDS, Nanyang Technological University 4DSO National Laboratories 

_{_ hui007, yu.yi, yiming014, cyyi, qixin.zhang, eackot, exdjiang _}_ @ntu.edu.sg, sbingqua@dso.org.sg 

## **Abstract** 

_Vision-Language-Action (VLA) models are vulnerable to adversarial attacks, yet universal and transferable attacks remain underexplored, as most existing patches overfit to a single model and fail in black-box settings. To address this gap, we present a systematic study of_ **_universal, transferable adversarial patches_** _against VLA-driven robots under unknown architectures, finetuned variants, and sim-to-real shifts. We introduce_ **_UPA-RFAS_** _(Universal Patch Attack via Robust Feature, Attention, and Semantics), a unified framework that learns a single physical patch in a shared feature space while promoting cross-model transfer. UPARFAS combines (i) a feature-space objective with an ω_ 1 _deviation prior and repulsive InfoNCE loss to induce transferable representation shifts, (ii) a robustness-augmented two-phase min-max procedure where an inner loop learns invisible sample-wise perturbations and an outer loop optimizes the universal patch against this hardened neighborhood, and (iii) two VLA-specific losses: Patch Attention Dominance to hijack text→vision attention and Patch Semantic Misalignment to induce image-text mismatch without labels. Experiments across diverse VLA models, manipulation suites, and physical executions show that UPARFAS consistently transfers across models, tasks, and viewpoints, exposing a practical patch-based attack surface and establishing a strong baseline for future defenses. Code is at https://github.com/yuyi-sd/UPA-RFAS._ 

## **1. Introduction** 

Vision-Language-Action (VLA) models have made significant strides, facilitating open-world manipulation [5, 6], language-conditioned planning [23], and cross-embodiment 

> *Corresponding author. 

transfer [7, 89]. By coupling a visual encoder with language grounding and an action head, modern VLA models are capable of parsing free-form instructions and executing multi-step skills in both simulation and the physical world [34, 54]. Despite their potential, such multi-modal pipelines are vulnerable to structured visual perturbations, _aka_ adversarial attacks [8, 14, 27–29, 32, 64, 70, 76–85], which can mislead perception, disrupt cross-modal alignment, and cascade into unsafe actions. This issue is particularly severe in robotics, as attacks that merely flip a class in perception can translate into performance drops, collisions, or violations of task constraints on real-world systems [47, 57, 73]. Motivated by that, we conduct a systematic study of universal and transferable adversarial patches for VLA-driven robots, where black-box conditions, varying camera poses, and domain shifts from simulation to the real world are the norm in practical robotic deployments. 

Though vulnerabilities in VLAs have received growing attention [15, 47, 57, 67, 80], universal and transferable attacks remain largely under-explored. Reported patches often co-adapt to a specific model, datasets, or prompt template, and their success degrades sharply on unseen architectures or finetuned variants [24], precisely the black-box regimes that matter for safety assessment. As a result, current evaluations can overestimate security when the attacker lacks white-box access, and underestimate the risks of patch-based threats that exploit cross-modal bottlenecks [21]. Bridging this gap requires attacks that generalize across families of VLAs ( _e.g.,_ OpenVLA [23], lightweight OFT variants [24], and flow-based policies such as _εo_ [5]). 

We bridge the surrogate and victim gap by learning a universal patch in a shared feature space, guided by two principles: enlarge surrogate-side deviations that provably persist on the target, and concentrate changes along stable directions. An _ω_ 1 deviation term drives sparse, high-salience shifts [10] that avoid surrogate-specific quirks, while a re- 

22867 


Figure 1. **Overall transferable patch attack (UPA-RFAS) for VLA robotics.** The framework operates in two coordinated stages within a shared feature-space objective. _Phase 1 – Inner minimization_ learns a small, invisible, sample-wise perturbation **_ω_** via PGD that _minimizes_ the feature objective _J_ in (§ 3.3) with the patch frozen (§ 3.4). _Phase 2 – Outer maximization_ freezes **_ω_** and optimizes a _single_ physical patch **_ε_** to _maximize J_ out (§ 3.7), which combines an _ω_ 1 deviation with a repulsive contrastive term and two VLA-specific objectives: **Patch Attention Dominance** (PAD) (§ 3.5) and **Patch Semantic Misalignment** (PSM) (§ 3.6). Red dashed arrows indicate back-propagation. UPA-RFAS yields a universal physical patch that transfers across models, prompts, and viewpoints. 

pulsive InfoNCE loss [11] pushes patched features away from their clean anchors along batch-consistent, high-CCA directions [46], strengthening black-box transfer. To further raise universality, we adopt a Robustness-augmented Universal Patch Attack (RAUP). The inner minimization loop learns a small, sample-wise invisible perturbation that reduces the feature-space objective around each input, emulating local adversarial training and hardening the surrogate. The outer maximization loop then optimizes a single physical patch against this hardened neighborhood with randomized placements and transformations, distilling the stable, cross-input directions revealed by the inner loop. For robotics, we further couple feature transfer with policy-relevant signals: _(i)_ the Patch Attention Dominance (PAD) loss increases patch-routed text _→_ vision attention and suppresses non-patch increments with a one-sided margin, yielding location-agnostic attention attraction; _(ii)_ the Patch Semantic Misalignment (PSM) loss pulls the pooled patch representation toward probe-phrase anchors while repelling it from the current instruction embedding, creating a persistent image–text mismatch that perturbs instructionconditioned policies without labels. Together, these components form **Universal Patch Attack via Robust Feature, Attention, and Semantics (UPA-RFAS)** , a universal, transferable patch framework that aligns attack feature shifts, cross-modal attention, and semantic steering. 

Our contributions are summarized as follows: 

- We present the first _universal, transferable_ patch attack framework for VLA robotics, using a feature-space objective that combines _ω_ 1 deviation with repulsive contrastive alignment for model-agnostic transfer. 

- We propose a _robustness-augmented_ universal patch attack, with invisible sample-wise perturbations as hard augmenters and a universal patch trained under heavy ge- 

ometric randomization. 

- We design two VLA-specific losses: _Patch Attention Dominance_ and _Patch Semantic Misalignment_ to hijack text _→_ vision attention and misground instructions. 

- Extensive experiments across VLA models, tasks, and sim-to-real settings show strong black-box transfer, revealing a practical patch-based threat and a transferable baseline for future defenses. 

## **2. Related Work** 

**Vision-Language-Action (VLA) Models.** Advances in large vision–language models (LVLMs) [3, 44, 50, 72, 86] have prompted robotic manipulation to leverage the powerful capabilities of vision–language modeling. VLA models extend LVLMs to robotic control by coupling perception, language grounding, and action generation. Autoregressive VLAs discretize actions into tokens and learn endto-end policies from large demonstrations, yielding scalable instruction-conditioned manipulation [7, 23, 31, 45, 61, 89]. Diffusion-based VLAs generate continuous trajectories with denoisers for smooth rollouts and flexible conditioning, at the cost of higher inference latency [4–6, 30, 62]. RL-enhanced VLAs optimize robustness and adaptability beyond supervised imitation by introducing reinforcement objectives over VLA backbones [18, 39, 51]. VLA models exemplify strong vision–language alignment for compositional task understanding and end-to-end action generation, while raising new questions about robustness under instruction-conditioned deployment. 

**Adversarial Attacks in Robotics.** Adversarial attacks are commonly grouped by access level: white-box methods assume full knowledge and directly use model gradients [17, 55, 69, 71], whereas black-box methods operate without internals-either by querying the model for 

22868 

feedback [9, 35, 36] or by exploiting cross-model transferability of crafted examples [40, 41, 63]. To strengthen transfer, optimization-driven approaches refine or stabilize gradient signals to avoid local minima arising from mismatched decision boundaries across architectures [12, 26, 33, 37, 58, 87]. Augmentation-based strategies diversify inputs to induce gradient variation and reduce overfitting to a single surrogate [13, 33, 56, 59, 66, 88]. Finally, feature-space attacks aim at intermediate representations to promote cross-model invariance and further improve transfer [16, 60, 74, 75]. Patch-based physical attacks [8, 19, 48, 65, 68] are practical for real-world deployment, remaining effective under changes in viewpoint and illumination, which makes them suitable for robotic systems. VLA models [20, 52] couple visual and linguistic modalities to align perception with action, and visual streams are high-dimensional and can be subtly perturbed in ways that are difficult to detect [2, 53]. Accordingly, our work targets the visual modality with a universal, transferable patch attack. To our knowledge, it is the first to investigate blackbox transfer vulnerabilities of VLAs in real-world settings. 

## **3. Methodology** 

### **3.1. Preliminary** 

**Adversarial Patch Attack.** We consider a robot whose decisions are based on RGB visual streams **x** _t ↑_ [0 _,_ 1]<sup>_H→W →_3</sup> across time step _t_ . An adversary tampers with this stream using a _single universal_ patch **_ω_** _↑_ [0 _,_ 1]<sup>_hp→wp→_3</sup> . At each time step _t_ , an area-preserving geometric transformation _Tt ↓T_ ( _e.g.,_ random position, skew, and rotation) is sampled, and the transformed patch is rendered onto the frame. Given **M** _Tt ↑{_ 0 _,_ 1 _}_<sup>_H→W_</sup> as the binary placement mask induced by _Tt_ , and _R_ ( **_ω_** ; _Tt_ ) _↑_ [0 _,_ 1]<sup>_H→W →_3</sup> as the rendered patch, the pasting function _P_ and resulting patched frame is 


where _↗_ is the Hadamard product, **1** is an all-ones matrix, _S_ ( _·_ ) returns the patch area ( _i.e., hp ↘ wp_ ), and _ϑ_ is an area budget controlling the maximal visible size of the patch. 

Let _ε_ denote a _victim_ policy. Given visual inputs **x** drawn from a task distribution _p_ ( **x** ) and random patch placements _Tt ↓T_ , an adversarial patch attack aims to _learn_ a single universal patch **_ω_** that maximizes an evaluation objective _J_ eval ( _e.g.,_ task loss increase or action-space deviation [57]) under pasting _P_ in Eq. 1 and these randomized conditions: 


This objective captures a _single_ patch that is robustly effective across time, viewpoints, and scene configurations. 

**VLAs.** We follow the OpenVLA formulation [23], where a policy is decomposed into a _vision encoder f_ v, a _visual projector f_ prj, and a _language-model backbone f_ llm equipped with an _action head f_ act. Given an RGB observation **x** and an instruction _c_ , the model predicts an action vector **y** as 


The computation can be unpacked as: **(i)** the vision encoder _f_ v maps the image into a set of multi-granularity visual embeddings, for example by concatenating DINOv2 [44] and SigLIP [72] features, yielding **E** _v ↑_ R<sup>_Nv→Dv_</sup> from **x** ; **(ii)** the projector _f_ prj aligns these embeddings to the LLM token space, producing visual tokens **Z** _v ↑_ R<sup>_N →_</sup> _v_<sup>_→Dt_</sup> ; **(iii)** the backbone _f_ llm takes the concatenation of **Z** _v_ and the tokenized command tok( _c_ ), and fuses them into hidden states **H** _ϑ_ ; **(iv)** the action head _f_ act decodes **H** _ϑ_ into the continuous control output **y** _↑_ R<sup>_Da_</sup> ( _e.g.,_ a 7-DoF command). 

### **3.2. Problem Formulation** 

Existing VLA patch attacks [57] assume white-box access to the victim model, which limits their practicality and says little about cross-policy transfer. In our setting, the attacker instead only has gradient access to a _single_ surrogate model _ε_ ˆ and aims to learn one universal patch that transfers to a family of unseen target policies !tgt. To formalize this threat model, we separate _optimization_ and _evaluation_ : the patch is optimized in the surrogate feature space via a differentiable objective _J_ tr, and its success is assessed by an evaluation objective _J_ eval on target policies drawn from !tgt. Following [57], we adopt the untargeted attack setting, and summarize this transferable patch attack as follows. 

**Definition 1 (Transferable adversarial patch attack via VLA feature space)** _Let_ ˆ _ε be a surrogate model and_ !tgt _a family of target policies. Let fϖ_ ˆ( _·_ ) _extract features from ε_ ˆ _. A patch_ **_ω_** _is a_ universal transferable adversarial patch in the VLA feature space _, it satisfies_ 


_where J_ tr _measures feature discrepancy using_ ” _:_ 


Here, _P_ is the pasting function defined in Eq. 1, and _J_ tr is the transferable attack strategy. Although _ε_ ˆ and _ε_ differ in training recipe and data, we probe whether their feature spaces admit a stable _cross-model relation_ as follows: 

**Shared Representational Structure across VLA Policies.** Empirically, we observe a strong linear relationship between the surrogate and target feature spaces. Let **z** _s_ and 

22869 

**z** _t_ denote visual features from _ε_ ˆ and _ε_ on the same inputs. We first apply Canonical Correlation Analysis (CCA) to test whether these representations lie in a _shared linear subspace_ : large top Canonical Correlation indicates a nearinvertible linear map aligning the two subspaces [43, 46]. In parallel, we fit a _linear regression probe_ from **z** _s_ to **z** _t_ and use the explained variance ( _R_<sup>2</sup> ) to quantify how well a _single_ linear map accounts for the target features, complementing CCA’s subspace view [1, 25]. In our case, _R_<sup>2</sup> _≃_ 0 _._ 654 together with near-unity top- _k_ Canonical Correlations indicates a shared low-dimensional subspace, with some residual components not captured by one linear map. Consequently, patch updates that steer _ε_ ˆ’s features within this shared subspace tend to induce homologous displacements in _ε_ , supporting the transferability of patches. Motivated by these observations, we make the following Assumption 1. 

### **3.3. Learning Transferable Patches with Featurespace** _ω_ 1 **and Contrastive Misalignment** 

Let _fϖ_ ˆ _, fϖ_ : _X →_ R<sup>_d_</sup> be the surrogate and target encoders with dimension _d_ , where _f·_ consists of vision encoder _f_ v and visual projector _f_ prj. For any pair ( **x** _i,_ ˜ **x** _i_ ), define the surrogate-side feature deviation ” **z** _i_ := _fϖ_ ˆ(˜ **x** _i_ ) _↔ fϖ_ ˆ( **x** _i_ ) and the target-side deviation ” **g** _i_ := _fϖ_ (˜ **x** _i_ ) _↔ fϖ_ ( **x** _i_ ). 

**Assumption 1 (Linear alignment with bounded residual)** _There exists a matrix A_<sup>_ω_</sup> _↑_ R<sup>_d→d_</sup> _such that_ 


_where the alignment residual e_ ( **x** ) _satisfies ⇐ e_ (˜ **x** ) _↔ e_ ( **x** ) _⇐_ 2 _⇒ ϖE for all pairs_ ( **x** _,_ ˜ **x** ) _considered._ 

Assumption 1 states that the effect of a surrogate deviation must persist on the target with strength governed by _ϱ_ min( _A_<sup>_ω_</sup> ), the smallest singular value of the alignment map _A_<sup>_ω_</sup> . The proposition below makes this dependence explicit. 

**Proposition 1 (Lower-bounded target displacement)** _Under Assumption 1, for any_ ( **x** _i,_ ˜ **x** _i_ ) 


Proof is in _Appendix_ A. Proposition 1 links target-side deviation to the surrogate-side. Therefore, any strategy that enlarges _⇐_ ” **z** _i⇐_ ( _e.g.,_ via an _ω_ 1 objective) necessarily induces a nontrivial response on the target. Thus we can capture why we could use **L1 loss** _L_ 1 to maximize feature discrepancy: 

**Corollary 1 (Effect of maximizing** _ω_ 1 **deviation)** _If an attack increases the surrogate-side ω_ 1 _deviation, e.g. by maximizing L_ 1 = _⇐_ ” **z** _i⇐_ 1 _, then the target-side deviation obeys the linear lower bound in Eq. 8. In particular, when the alignment is well-conditioned (ϱ_ min( _A_<sup>_ω_</sup> ) _not small) and the residual coupling ϖE is modest, increasing ⇐_ ” **z** _i⇐_ 1 _necessarily induces a nontrivial increase of ⇐_ ” **g** _i⇐_ 1 _._ 

**Repulsive Contrastive Regularization.** Complementing the _L_ 1 deviation term, we introduce a _repulsive_ contrastive objective that explicitly pushes the patched feature ˜ **z** _i_ away from its clean anchor **z** _i_ . For each sample _i_ , we still treat ( **z** _i,_ ˜ **z** _i_ ) as a distinguished pair and _{_ **z** ˜ _j}j↓_ = _i_ as a reference set, and adopt the InfoNCE [11] as a repulsion term 


where sim denotes cosine similarity and _ς_ is a temperature. Maximizing (minimizing) _L_ con encourages the similarity sim( **z** _i,_ ˜ **z** _i_ ) to _decrease (increase)_ , effectively pushing **z** ˜ _i_ away (pulling **z** ˜ _i_ close) from its clean anchor and concentrating the change along directions that are consistently shared across the batch. 

**Overall Feature-space Objective.** Combining both components, we obtain the objective for ” as given in Eq. 5: 


where _L_ 1 is the _ω_ 1 loss term and _L_ con is the repulsive contrastive objective, and _φ >_ 0 balances their contributions. 

### **3.4. Robustness-augmented Universal Patch Attack** 

**Emulate Robust Surrogates without Retraining VLAs.** Transfer-based attacks on image classifiers have shown that adversarial examples generated on _adversarially trained_ or _slightly robust_ source models transfer significantly better than those crafted on standard models [22, 49]. Robust training encourages the source model to rely on more “universal” features shared across architectures, so perturbations aligned with these features exhibit stronger crossmodel transferability. A natural strategy would be to use an adversarially trained VLA as the surrogate. However, adversarially trained large VLA policies is practically prohibitive: it requires massive interactive data and computing, and can substantially degrade task performance. Instead, we still optimize a _single universal physical patch_ , but augment it with a _sample-wise, invisible_ perturbation that _emulates_ adversarial (robust) training on the surrogate. This perturbation is applied globally and updated to _counteract_ patchinduced feature deviations, effectively “hardening” the surrogate along the directions the patch tries to exploit. Since the universal patch is localized while the sample-wise perturbations remain invisible and input-specific, their inter- 

22870 

ference is limited, and the patch can then exploit the robust feature directions revealed by this hardening step. 

**Bi-level Robustness-augmented Optimization.** Formally, let **_ω_** denote the universal patch and **_ε_** a sample-wise perturbation confined to the patch mask. Given a optimizing loss _J_ tr on the surrogate _ε_ ˆ, we consider the following robustness-augmented bi-level objective: 


The inner problem “adversarially trains” the surrogate locally by finding a small, sample-wise perturbation to _reduce_ the attack loss, and the outer problem then maximizes the same loss with respect to **_ω_** in this hardened neighborhood. 

To further strengthen transferability, the outer maximization is not driven by the feature displacement alone. In the following subsections, we introduce **additional loss components** that shape _where_ the model attends and _what_ semantics the patch encodes, and jointly optimize them within this robustness-augmented framework. 

### **3.5. Patch Attention Dominance: Cross-Modal Hijack Loss** 

**Action-relevant Queries as the Attack Handle.** In VLA policies, actions are largely driven by a small set of _actionrelevant_ text queries whose cross-modal attention to vision decides which visual regions control the policy. Our universal patch is therefore designed as a _location-agnostic attention attractor_ : regardless of placement, skew, or orientation, it should **redirect the attention** of these actionrelevant queries _from true semantic regions to the patch_ . Concretely, we aim to _increase_ the attention increments on the patch vision tokens while _reducing_ increments on nonpatch tokens, based on the difference between patched and clean runs under random placements. 

**Patch-induced Attention Increments for Action-relevant queries.** From clean and patched runs, we collect the last _N_ attention blocks **A** from _f_ llm, average over heads, and slice out the text _→_ vision submatrix via tv( _·_ ): 


where _l_ = _L ↔ N_ + 1 _, . . . , L_ indexes the last _N_ layers. We row-normalize over vision tokens (index _p_ ) and average across layers to obtain attention _shares_ , then define the 

patch-induced share increment: 


where rn( _·_ ) denotes row-normalization over _p_ . By optimizing **!** rather than raw attention, the objective depends only on _patch-induced_ changes. 

**Action-relevant Queries.** To focus precisely on actionrelevant queries and avoid surrogate-specific overfitting, we restrict the optimization to the top- _ϑ_ text tokens (per batch) that already receive the highest clean attention: 


where TopKMask returns a binary mask over the text positions, broadcast across vision tokens. These top- _ϑ_ tokens are our proxy for action-relevant queries. 

**Patch vs. Non-patch Attention Increments.** To capture the effect of patch location on visual tokens, we map the pixel-level mask **M** _Tt ↑{_ 0 _,_ 1 _}_<sup>_H→W_</sup> to a token-level mask **M** _z ↑_ [0 _,_ 1]<sup>_p_</sup> via bilinear interpolation, where _p_ is the number of visual tokens ( _e.g., p_ = _g_<sup>2</sup> for a _g ↘ g_ ViT grid), and then flatten it to length _p_ . We then aggregate the attention increments routed from action-relevant queries into patch versus non-patch vision tokens: 


where _⇔·, ·↖p_ sums over the vision index _p_ . _d_ patch ( _d_ non) measures how much extra attention the patch induces on patch (non-patch) tokens from action-relevant text queries. **Patch Attention Dominance (PAD) Loss.** Finally, we define the attention-hijack objective to maximize by explicitly _increasing_ patch-related increments and _decreasing_ nonpatch increments, with a margin against the strongest nonpatch route: 


where E[ _·_ ] averages over the selected (action-relevant) text tokens. The first term increases patch attention increments, the second penalizes positive increments on non-patch tokens, and the margin term enforces that the patch’s increment exceeds the strongest non-patch increment by at least _m_ . Together, these terms induce _Patch Attention Dominance_ , where action-relevant queries direct their additional attention to the patch rather than true semantic regions. 

### **3.6. Patch Semantic Misalignment: Text-Similarity Attack Loss** 

**Semantic Steering beyond Attention.** Merely hijacking cross-modal attention does not guarantee a consistent behavioral bias across models or tasks. To further enhance 

22871 

transferability, we constrain the patch also in _semantic_ space: we **steer** the visual representation of patch-covered tokens **toward** a set of cross-model-stable action/direction primitives ( _probe phrases_ ), while simultaneously **pushing it away from the holistic representation** of the current instruction. The probes ( _e.g.,_ “put”, “pick up”, “place”, “open”, “close”, “left”, “right”) act as architecture-agnostic anchors, and the repulsion from the instruction embedding induces a persistent, context-dependent semantic misalignment that more reliably derails the policy decoder. 

**Patch Pooling and Semantic Anchors.** Let **z** _j ↑_ R<sup>_D_</sup> be visual token features and _mj ↑_ **M** _z_ the corresponding patchtoken mask. We pool and _ω_ 2–normalize the patch feature: 


Let _{_ **p** ˆ _k}_<sup>_K_</sup> _k_ =1<sup>benormalized</sup><sup>_probeprototypes_(</sup><sup>_e.g.,_action</sup> and direction anchors), and let<sup>ˆ</sup> **t** denote a normalized representation of the whole current instruction ( _e.g.,_ the mean of the last-layer text states from _f_ llm). 

**Patch Semantic Misalignment (PSM) Loss.** We then define the text-similarity attack loss to maximize as 


with temperatures _ς >_ 0 and weights _↼, ↽>_ 0. 

Eq. 17 yields a location-agnostic semantic descriptor for the patch-covered tokens. In Eq. 18, the first (LogSumExp) term _pulls_ **v** ˆpatch toward any probe prototype, avoiding dependence on a single phrase while focusing gradients on the most compatible anchors as _ς_ decreases. The second term _pushes_ the patch feature away from the instruction embedding, inducing a persistent, context-dependent semantic mismatch, with _↼, ↽_ balancing pull and push. The loss is fully differentiable w.r.t. patch parameters via **z** _j_ and complements attention hijacking by steering the _attended_ content toward a stable, transferable semantic direction. 

### **3.7. Universal Patch Attack via Robust Feature, Attention, and Semantics (UPA-RFAS)** 

The overall optimization process is in Algorithm 1 where: 

**Inner Minimization.** Given **x** at time _t_ and the current patch **_ω_** , we initialize a global invisible perturbation **_ε_**<sup>(0)</sup> = **0** and update it by Projected Gradient Descent (PGD) [42]: 


where _Jin_ = _Jtr_ is in Eq. 10, ! _↔·↔↑↗ϱω_ projects onto the _ω≃_ ball of radius _⇁ς_ , _⇀_ **_ε_** is the step size, and _Tt_ is sampled once from _T_ across iterations. **_ε_**<sup>_ω_</sup> is the final perturbation. 

#### **Algorithm 1** UPA-RFAS 

- 1: **Input:** surrogate _fϖ_ ˆ, subset _Ds_ , universal patch **_ω_** _↑_ [0 _,_ 1]<sup>_hp→wp→_3</sup> , budget _⇁ς_ , inner steps _I_ , outer steps _K_ , step sizes _⇀_ **_ε_** _, ⇀_ **_ω_** , weights _φ_ con _, φ_ PAD _, φ_ PSM 

- 2: **for** mini-batch data ( **x** _, c, t_ ) _′ Ds_ **do** 3: # Inner minimization 4: Initialize sample-wise perturbation **_ε_**<sup>(1)</sup> _↙_ **0** 5: Sample _Tt ↓T_ 6: **for** _i_ = 1 **to** _I_ **do** 7: _J_ in = _J_ tr� _P_ ( **x** + **_ε_**<sup>(</sup><sup>_i_)</sup> _,_ **_ω_** _, Tt_ ); ˆ _ε_ � via Eq. 1 and 10 8: **_ε_**<sup>(</sup><sup>_i_+1)</sup> _↙_ ! _↔·↔↑↗ϱω_ � **_ε_**<sup>(</sup><sup>_i_)</sup> _↔ ⇀ς∝_ **_ε_** _J_ in� 9: **end for** 

- 10: **_ε_**<sup>_ω_</sup> _↙_ **_ε_**<sup>(</sup><sup>_I_)</sup> #Outer maximization 

- 11: **for** _k_ = 1 **to** _K_ **do** 12: Sample _Tt ↓T_ 13: Compute _J_ out via Eq. 1, 16, 18 and 20 14: **_ω_** _↙_ AdamW _↔J_ out _P_ ( **x** + **_ε_**<sup>_ω_</sup> ( **x** ) _,_ **_ω_** _, Tt_ ); ˆ _ε_ ; _⇀_ **_ω_** � � � � 

- 15: **_ω_** _↙_ Clip[0 _,_ 1]( **_ω_** ) 16: **end for** 17: **end for** 18: **return** **_ω_** 

**Outer Maximization.** With **_ε_**<sup>_ω_</sup> ( **x** ) fixed, we update the universal patch **_ω_** by AdamW [38] to maximize the objective with additional losses under randomized transformations: 


where the patch **_ω_** _↑_ [0 _,_ 1]<sup>_hp→wp→_3</sup> respects the area budget, and _⇀_ **_ω_** is the learning rate. At each iteration, we sample _Tt ↓T_ and clamp **_ω_** to the valid range [0 _,_ 1]. 

## **4. Experiments** 

**Datasets.** We evaluate our attacks on BridgeData V2 [54] and LIBERO [34] using the corresponding VLA models. BridgeData V2 is a real-world corpus spanning 24 environments and 13 manipulation skills ( _e.g.,_ grasping, placing, object rearrangement), comprising 60,096 trajectories. LIBERO is a simulation suite with four task familiesSpatial, Object, Goal, and Long, where LIBERO-Long combines diverse objects, layouts, and extended horizons, making multi-step planning particularly challenging. 

**Baseline.** We adopt RoboticAttack [57]’s 6 objectives as the baselines, including Untargeted Manipulation Attack (UMA), Untargeted Action Discrepancy Attack (UADA), and Targeted Manipulation Attack (TMA) corresponding to 

22872 

Table 1. Task success rate (%) when transferring from the surrogate OpenVLA-7B to different victim models on LIBERO. 

||||**V**|**ictim**|**: Ope**|**nVLA-**|**oft-w**||||||**Vict**|**im: Op**|**enVLA**|**-oft**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|objective||Sim|ulate|d|||Ph|ysical|||Sim|ulate|d|||Ph|ysical||
||spatial|object|goal|long|avg.<br>|spatial|object|goal|long avg.|spatial|object|goal|lon|g avg.<br>|spatial|object|goal|long avg.|
|Benign|99|99|98|97|98.25|99|99|98|97 98.25|98|98|98|94|97.00|98|98|98|94 97.00|
|UMA1|25|86|40|31|45.50|83|89|76|73 80.25|79|95|69|3|61.50|96|90|90|83 89.75|
|UMA1_→_3|46|88|38|39|52.75|90|87|83|81 85.25|90|93|57|3|60.75|96|81|93|80 87.50|
|UADA1|35|82|27|21|41.25|71|90|57|74 73.00|94|86|61|3|61.00|92|96|79|84 87.75|
|UADA1_→_3|37|74|21|33|41.25|65|88|46|61 65.00|87|90|64|4|61.25|92|95|61|90 84.50|
|TMA1|69|89|58|61|69.25|78|92|74|83 81.75|99|93|81|25|74.50|98|92|84|86 90.00|
|TMA7|47|78|47|34|51.50|90|96|89|90 91.25|83|93|75|62|78.25|97|88|89|87 90.25|
|Our|**7**|**0**|**10**|**6**|**5.75**|**26**|**53**|**54**|**28 40.25**|**66**|**43**|**62**|**3**|**43.50**|**69**|**74**|**76**|**27 61.50**|


different Degree-of-freedom (DoF). For each, experiments follow the original loss definitions and evaluation protocol. We further consider both **simulated and physical victim settings** : a model trained in simulation on the LIBEROLong suite using the _OpenVLA-7B-LIBERO-Long_ variant, and a model trained on real-world BridgeData v2 data with the _OpenVLA-7B_ model, respectively. 

**Surrogate and Victim VLAs.** We evaluate universal, transferable patches under a strict black-box transfer protocol. Surrogate models are chosen from publicly available, widely used VLA [23] to reflect prevailing design trends. The primary surrogate models are _OpenVLA-7B_ trained on physical dataset BridgeData V2 [54] and _OpenVLA-7BLIBERO-Long_ fine-tuned on LIBERO-Long. During transfer, **no information about victim models** is used, including weights, architecture details beyond public model names, fine-tuning datasets, recipes, or hyperparameters. Specifically, we select _OpenVLA-oft_ [24] and _ε_ series [5, 6] models as victim models. Built on OpenVLA, _OpenVLA-oft_ introduces an optimized fine-tuning recipe that notably improves success rates (from 76.5% to 97.1%) and delivers _↓_ 26 _↘_ throughput. To stress cross-recipe and cross-task vulnerability, we test on four variants fine-tuned on four distinct LIBERO task suites, as well as a multi-suite model trained jointly on all four ( _OpenVLA-oft-w_ ). The _ε_ family differs fundamentally from OpenVLA in backbone choice, pretraining/fine-tuning data, and training strategy, making transfer substantially harder. We therefore assess black-box transfer on _ε_ 0 [5], which provide a stringent test of modelagnostic patch behavior across heterogeneous VLA designs. 

**Implementation & Evaluation Details.** We evaluate on the LIBERO benchmark [34]. Each suite contains 10 tasks, and each task is attempted in 10 independent trials, yielding 100 rollouts per suite, following [5]. Consistent with [57], patch placement sites are predetermined for each suite to avoid occluding objects in the test scenes. More implementation details can be found in the _Appendix_ B. Regarding the evaluation metric, we adopt the concept of Success Rate 

(SR) introduced in LIBERO [34] across all setting. 

### **4.1. Main Results** 

We first evaluate the white-box performance of our patches, where the victim model is identical to the surrogate. The results in _Appendix_ C demonstrate that our method achieves strong white-box attack capability. For the _OpenVLA-7B_ [23] to _OpenVLA-oft-w_ [24] transfer experiment, Tab. 1 shows that our patch objective induces the strongest degradation of task success rates. In the simulated setting, the clean policy succeeds on 98.25% of tasks on average, while our method reduces the success rate to only 5.75%, corresponding to more than a 92% point drop. Existing objectives such as UMA, UADA, and TMA do transfer to the victim but remain much less destructive: their average success rates stay between 41.25% and 69.25%, and they leave certain categories almost intact, for example, object-centric tasks still above 74% success for UMA and UADA. In contrast, our patch almost completely disables the policy across all four task types. Tab. 1 also reports the attack results under physical setting. A similar trend appears: all baselines still retain high average success (65.00%-91.25%), whereas our method again yields the lowest success rate of 40.25%. This indicates that our patch objective not only transfers more effectively to the simulated environments, but also produces substantially stronger degradation under the physical environment, establishing a consistently harder universal patch baseline across both settings. 

Beyond the transfer from _OpenVLA-7B_ to _OpenVLA-oftw_ , we further evaluate transfer to four different _OpenVLAoft_ variants that are separately fine-tuned on different LIBERO task suites, creating a larger distribution and policy gap from the surrogate. Tab. 1 shows that our objective still achieves consistently stronger transfer than all baselines across both simulated and physical setups, highlighting the effectiveness of our design. **Additional transfer results** , including attacks transferred to _ε_ 0, are in _Appendix_ D, and show that our methods still enhance attacks in the most challenging case of transferring to entirely different VLAs. 

22873 

Table 2. Ablation for transfer to openvla-oft under physical setting. 

|objective|spatial|object|goal|long|avg.|
|---|---|---|---|---|---|
|Our|69|74|76|27|61.50|
|w/o RUPA|70|75|71|33|62.25|
|w/o PAD|68|67|77|38|62.50|
|w/o PSM|69|72|81|32|63.50|
|w/o_J_tr|90|86|94|73|85.75|
|w/o_L_con|93|63|79|48|70.75|
|w/o_L_1|74|74|77|31|64.00|


Table 3. Ablation on text-probe phrasing for transfer to openvlaoft in the physical setting. 

|objective|spatial|object|goal|long|avg.|
|---|---|---|---|---|---|
|Our|69|74|76|27|61.50|
|Action|76|67|94|48|71.25|
|Direction|72|75|78|75|75.00|


### **4.2. Ablation Study** 

**Impact of Each Design.** Tab. 2 further validates the role of each component in our objective. Dropping any single module (RUPA, PAD, or PSM) consistently weakens the attack, reflected by higher average success rates than the full model. The most severe degradation appears in the _w/o J_ tr variant, where the average success rate jumps to 85.75%, close to the benign and baseline levels. Since _J_ tr jointly contains both _L_ 1 and _L_ con ( _i.e.,_ it removes the entire firststage feature-space minimization), this indicates that our feature-space _ω_ 1 and contrastive misalignment objectives, together with the RUPA designs, are essential for strong transfer. Moreover, the impact of _L_ con is noticeably larger than that of _L_ 1. By Prop. 1 and Cor. 1, _L_ 1 is a distancebased term that mainly controls the _magnitude_ of the surrogate deviation, whereas _L_ con, built on cosine similarity, focuses on feature angles and thus shapes the _direction_ of the displacement. Consequently, even without _L_ 1, _L_ con can still drive patched features away from their clean anchors along transferable directions, so the attack remains relatively strong. 

**Impact of Text Probes.** Tab. 3 analyzes how text-probe phrasing influences transfer in the physical setting. We compare our default probes, which jointly encode both action and spatial direction, against two reduced variants: **Action** probes that only include verbs ( _e.g.,_ “put”, “pick up”, “place”, “turn on”, “push”, “open”, “close”) and **Direction** probes that only contain spatial words ( _e.g.,_ “left”, “right”, “bottom”, “back”, “middle”, “top”, “front”). Using actiononly or direction-only probes markedly weakens the attack: the average success rate increases to 71.25% and 75.00%, respectively, compared to 61.5% with our design. This suggests that jointly encoding action and directional cues produces text queries that more closely match the policy’s 


Figure 2. **Patch visualization and comparison.** The first row is trained in a simulated setting, and the second row is trained in a physical setting. 

action-relevant channels, thereby enabling more effective cross-model transfer. Ablation study of more specific parameters can be found in _Appendix_ E. 

### **4.3. Patch Pattern Analysis** 

As shown in Fig. 2, we can see that baseline end-to-end methods [57] produce scene-tied patterns: UADA yields textures that closely resemble the robot gripper in both simulation and physical settings (Fig. 2a and 2d), while TMA generates more abstract yet surrogate-specific shapes (Fig. 2b and 2e). These behaviors indicate overfitting to object/embodiment cues, which hampers cross-model and cross-setting transfer. In contrast, our universal transferable patch (Fig. 2c and 2f) is learned in feature space to perturb higher-level, model-agnostic representations shared across VLAs. By jointly optimizing feature-space, attention, and semantic objectives, our patch combines the strengths of prior designs, avoids object mimicry, and yields a universal patch that reliably transfers across tasks, embodiments, and environments, resulting in stronger black-box transfer. 

## **5. Conclusion** 

In this paper, we present the first study of universal, transferable patch attacks on VLA-driven robots and introduce UPA-RFAS, a unified framework that couples an _ω_ 1 feature deviation with repulsive contrastive alignment to steer perturbations into model-agnostic, high-transfer directions. UPA-RFAS integrates a robustness-augmented patch optimization and two VLA-specific losses, Patch Attention Dominance and Patch Semantic Misalignment, which achieve strong black-box transfer across models, tasks, and sim-to-real settings, revealing a practical patch-based threat and a solid baseline for future defenses. 

22874 

## **Acknowledgement** 

This work was carried out at the Rapid-Rich Object Search (ROSE) Lab, School of Electrical & Electronic Engineering, Nanyang Technological University (NTU), Singapore. This research is supported by the National Research Foundation, Singapore and Infocomm Media Development Authority under its Trust Tech Funding Initiative and the DSO National Laboratories, Singapore, under the project agreement No. DSOCL25023. Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not reflect the views of National Research Foundation, Singapore and Infocomm Media Development Authority. 

## **References** 

- [1] Guillaume Alain and Yoshua Bengio. Understanding intermediate layers using linear classifier probes. _arXiv preprint arXiv:1610.01644_ , 2016. 4 

- [2] Anish Athalye, Nicholas Carlini, and David Wagner. Obfuscated gradients give a false sense of security: Circumventing defenses to adversarial examples. In _Proc. Int’l Conf. Machine Learning_ , pages 274–283. PMLR, 2018. 3 

- [3] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 2 

- [4] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 2 

- [5] Kevin Black et al. _ε_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 1, 7, 2 

- [6] Kevin Black et al. _ε_ 0 _._ 5: a vision-language-action model with open-world generalization. 2025. 1, 2, 7 

- [7] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 1, 2 

- [8] Tom B Brown, Dandelion Man´e, Aurko Roy, Mart´ın Abadi, and Justin Gilmer. Adversarial patch. _arXiv preprint arXiv:1712.09665_ , 2017. 1, 3 

- [9] Pin-Yu Chen, Huan Zhang, Yash Sharma, Jinfeng Yi, and Cho-Jui Hsieh. Zoo: Zeroth order optimization based blackbox attacks to deep neural networks without training substitute models. In _Proceedings of the 10th ACM workshop on artificial intelligence and security_ , 2017. 3 

- [10] Pin-Yu Chen, Yash Sharma, Huan Zhang, Jinfeng Yi, and Cho-Jui Hsieh. Ead: elastic-net attacks to deep neural networks via adversarial examples. In _Proc. AAAI Conf. on Artificial Intelligence_ , 2018. 1 

- [11] Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey Hinton. A simple framework for contrastive learning of visual representations. In _Proc. Int’l Conf. Machine Learning_ , pages 1597–1607. PmLR, 2020. 2, 4 

- [12] Yinpeng Dong, Fangzhou Liao, Tianyu Pang, Hang Su, Jun Zhu, Xiaolin Hu, and Jianguo Li. Boosting adversarial attacks with momentum. In _Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition_ , 2018. 3 

- [13] Yinpeng Dong, Tianyu Pang, Hang Su, and Jun Zhu. Evading defenses to transferable adversarial examples by translation-invariant attacks. In _Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition_ , 2019. 3 

- [14] Kevin Eykholt, Ivan Evtimov, Earlence Fernandes, Bo Wei, Yongdae Bo, Amir Rahmati, Dawn Song, Patrick Traynor, Atul Prakash, and Tadayoshi Kohno. Robust physical-world attacks on deep learning visual classification. In _Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition_ , 2018. 1 

- [15] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, et al. Libero-plus: In-depth robustness analysis of visionlanguage-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 1 

- [16] Aditya Ganeshan, Vivek BS, and R Venkatesh Babu. Fda: Feature disruptive attack. In _Proc. IEEE Int’l Conf. Computer Vision_ , 2019. 3 

- [17] Ian J Goodfellow, Jonathon Shlens, and Christian Szegedy. Explaining and harnessing adversarial examples. In _Proc. Int’l Conf. Learning Representations_ , 2015. 2 

- [18] Yanjiang Guo, Jianke Zhang, Xiaoyu Chen, Xiang Ji, YenJen Wang, Yucheng Hu, and Jianyu Chen. Improving visionlanguage-action model with online reinforcement learning. _arXiv preprint arXiv:2501.16664_ , 2025. 2 

- [19] Hao Huang, Ziyan Chen, Huanran Chen, Yongtao Wang, and Kevin Zhang. T-sea: Transfer-based self-ensemble attack on object detection. In _Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition_ , pages 20514–20523, 2023. 3 

- [20] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models. _arXiv preprint arXiv:2307.05973_ , 2023. 3 

- [21] Xiaojun Jia, Sensen Gao, Simeng Qin, Tianyu Pang, Chao Du, Yihao Huang, Xinfeng Li, Yiming Li, Bo Li, and Yang Liu. Adversarial attacks against closed-source mllms via feature optimal alignment. _arXiv preprint arXiv:2505.21494_ , 2025. 1 

- [22] Haydn T Jones, Jacob M Springer, Garrett T Kenyon, and Juston S Moore. If you’ve trained one you’ve trained them all: inter-architecture similarity increases with robustness. In _Uncertainty in Artificial Intelligence_ , pages 928–937. PMLR, 2022. 4 

- [23] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2, 3, 7 

22875 

- [24] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 1, 7, 2 

- [25] Simon Kornblith, Mohammad Norouzi, Honglak Lee, and Geoffrey Hinton. Similarity of neural network representations revisited. In _Proc. Int’l Conf. Machine Learning_ , pages 3519–3529. PMlR, 2019. 4 

- [26] Alexey Kurakin, Ian J Goodfellow, and Samy Bengio. Adversarial examples in the physical world. In _Artificial intelligence safety and security_ , pages 99–112. 2018. 3 

- [27] Fengpeng Li, Kemou Li, Haiwei Wu, Jinyu Tian, and Jiantao Zhou. DAT: Improving adversarial robustness via generative amplitude mix-up in frequency domain. In _Proc. Annual Conf. Neural Information Processing Systems_ , pages 127099–127128, 2024. 1 

- [28] Fengpeng Li, Kemou Li, Haiwei Wu, Jinyu Tian, and Jiantao Zhou. Toward robust learning via core feature-aware adversarial training. _IEEE Trans. on Information Forensics and Security_ , 20:6236–6251, 2025. 

- [29] Fengpeng Li, Kemou Li, Qizhou Wang, Bo Han, and Jiantao Zhou. AEGIS: Adversarial target–guided retention-data-free robust concept erasure from diffusion models. In _Proc. Int’l Conf. Learning Representations_ , 2026. 1 

- [30] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational visionlanguage-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 2 

- [31] Xiaoqi Li, Mingxu Zhang, Yiran Geng, Haoran Geng, Yuxing Long, Yan Shen, Renrui Zhang, Jiaming Liu, and Hao Dong. Manipllm: Embodied multimodal large language model for object-centric robotic manipulation. In _Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition_ , pages 18061–18070, 2024. 2 

- [32] Xiao Li, Yiming Zhu, Yifan Huang, Wei Zhang, Yingzhe He, Jie Shi, and Xiaolin Hu. Pbcat: Patch-based composite adversarial training against physically realizable attacks on object detection. _arXiv preprint arXiv:2506.23581_ , 2025. 1 

- [33] Jiadong Lin, Chuanbiao Song, Kun He, Liwei Wang, and John E Hopcroft. Nesterov accelerated gradient and scale invariance for adversarial attacks. _arXiv preprint arXiv:1908.06281_ , 2019. 3 

- [34] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. In _Proc. Annual Conf. Neural Information Processing Systems_ , pages 44776– 44791, 2023. 1, 6, 7 

- [35] Jun Liu, Jiantao Zhou, Jiandian Zeng, and Jinyu Tian. Difattack: Query-efficient black-box adversarial attack via disentangled feature space. In _Proc. AAAI Conf. on Artificial Intelligence_ , pages 3666–3674, 2024. 3 

- [36] Jun Liu, Jiantao Zhou, Jiandian Zeng, Jinyu Tian, and Zheng Li. Difattack++: Query-efficient black-box adversarial attack via hierarchical disentangled feature space in crossdomain. _arXiv preprint arXiv:2406.03017_ , 2024. 3 

- [37] Yanpei Liu, Xinyun Chen, Chang Liu, and Dawn Song. Delving into transferable adversarial examples and blackbox attacks. In _Proc. Int’l Conf. Learning Representations_ , 2017. 3 

- [38] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. _arXiv preprint arXiv:1711.05101_ , 2017. 6 

- [39] Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, and Ziwei Wang. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning. _arXiv preprint arXiv:2505.18719_ , 2025. 2 

- [40] Hui Lu, Yi Yu, Song Xia, Yiming Yang, Deepu Rajan, Boon Poh Ng, Alex Kot, and Xudong Jiang. From pretrain to pain: Adversarial vulnerability of video foundation models without task knowledge. In _Proc. AAAI Conf. on Artificial Intelligence_ , 2026. 3 

- [41] Hui Lu, Yi Yu, Yiming Yang, Chenyu Yi, Xueyi Ke, Qixing Zhang, Bingquan Shen, Alex Kot, and Xudong Jiang. Make anything match your target: Universal adversarial perturbations against closed-source mllms via multi-crop routed meta optimization. _arXiv preprint arXiv:2601.23179_ , 2026. 3 

- [42] Aleksander Madry, Aleksandar Makelov, Ludwig Schmidt, Dimitris Tsipras, and Adrian Vladu. Towards deep learning models resistant to adversarial attacks. _arXiv preprint arXiv:1706.06083_ , 2017. 6 

- [43] Ari Morcos, Maithra Raghu, and Samy Bengio. Insights on representational similarity in neural networks with canonical correlation. In _Proc. Annual Conf. Neural Information Processing Systems_ , 2018. 4 

- [44] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 2, 3 

- [45] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 2 

- [46] Maithra Raghu, Justin Gilmer, Jason Yosinski, and Jascha Sohl-Dickstein. Svcca: Singular vector canonical correlation analysis for deep learning dynamics and interpretability. In _Proc. Annual Conf. Neural Information Processing Systems_ , 2017. 2, 4 

- [47] Alexander Robey, Zachary Ravichandran, Vijay Kumar, Hamed Hassani, and George J Pappas. Jailbreaking llmcontrolled robots. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11948–11956. IEEE, 2025. 1 

- [48] Prashant Shekhar, Bidur Devkota, Dumindu Samaraweera, Laxima Niure Kandel, and Manoj Babu. Do adversarial patches generalize? attack transferability study across realtime segmentation models in autonomous vehicles. In _2025 IEEE Security and Privacy Workshops (SPW)_ , pages 322– 328. IEEE, 2025. 3 

- [49] Jacob Springer, Melanie Mitchell, and Garrett Kenyon. A little robustness goes a long way: Leveraging robust features 

22876 

   - for targeted transfer attacks. In _Proc. Annual Conf. Neural Information Processing Systems_ , pages 9759–9773, 2021. 4 

- [50] Andreas Steiner, Andr´e Susano Pinto, Michael Tschannen, Daniel Keysers, Xiao Wang, Yonatan Bitton, Alexey Gritsenko, Matthias Minderer, Anthony Sherbondy, Shangbang Long, et al. Paligemma 2: A family of versatile vlms for transfer. _arXiv preprint arXiv:2412.03555_ , 2024. 2 

- [51] Shuhan Tan, Kairan Dou, Yue Zhao, and Philipp Kr¨ahenb¨uhl. Interactive post-training for vision-languageaction models. _arXiv preprint arXiv:2505.17016_ , 2025. 2 

- [52] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 3 

- [53] Florian Tramer. Detecting adversarial examples is (nearly) as hard as classifying them. In _Proc. Int’l Conf. Machine Learning_ , pages 21692–21702. PMLR, 2022. 3 

- [54] Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pages 1723–1736. PMLR, 2023. 1, 6, 7 

- [55] Chong Wang, Yi Yu, Lanqing Guo, and Bihan Wen. Benchmarking adversarial robustness of image shadow removal with shadow-adaptive attacks. In _Proc. IEEE Int’l Conf. Acoustics, Speech, and Signal Processing_ , 2024. 2 

- [56] Kunyu Wang, Xuanran He, Wenxuan Wang, and Xiaosen Wang. Boosting Adversarial Transferability by Block Shuffle and Rotation. In _Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition_ , 2024. 3 

- [57] Taowen Wang, Cheng Han, James Liang, Wenhao Yang, Dongfang Liu, Luna Xinyu Zhang, Qifan Wang, Jiebo Luo, and Ruixiang Tang. Exploring the adversarial vulnerabilities of vision-language-action models in robotics. In _Proc. IEEE Int’l Conf. Computer Vision_ , pages 6948–6958, 2025. 1, 3, 6, 7, 8, 4 

- [58] Xiaosen Wang and Kun He. Enhancing the transferability of adversarial attacks through variance tuning. In _Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition_ , 2021. 3 

- [59] Xiaosen Wang, Xuanran He, Jingdong Wang, and Kun He. Admix: Enhancing the transferability of adversarial attacks. In _Proc. IEEE Int’l Conf. Computer Vision_ , 2021. 3 

- [60] Zhibo Wang, Hengchang Guo, Zhifei Zhang, Wenxin Liu, Zhan Qin, and Kui Ren. Feature importance-aware transferable adversarial attacks. In _Proc. IEEE Int’l Conf. Computer Vision_ , 2021. 3 

- [61] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 2 

- [62] Junjie Wen, Yichen Zhu, Minjie Zhu, Zhibin Tang, Jinming Li, Zhongyi Zhou, Xiaoyu Liu, Chaomin Shen, Yaxin Peng, and Feifei Feng. Diffusionvla: Scaling robot foun- 

dation models via unified diffusion and autoregression. In _Proc. Int’l Conf. Machine Learning_ , 2025. 2 

- [63] Song Xia, Wenhan Yang, Yi Yu, Xun Lin, Henghui Ding, Lingyu Duan, and Xudong Jiang. Transferable adversarial attacks on sam and its downstream models. In _Proc. Annual Conf. Neural Information Processing Systems_ , pages 87545– 87568, 2024. 3 

- [64] Song Xia, Yi Yu, Xudong Jiang, and Henghui Ding. Mitigating the curse of dimensionality for certified robustness via dual randomized smoothing. In _Proc. Int’l Conf. Learning Representations_ , 2024. 1 

- [65] Zihao Xiao, Xianfeng Gao, Chilin Fu, Yinpeng Dong, Wei Gao, Xiaolu Zhang, Jun Zhou, and Jun Zhu. Improving transferability of adversarial patches on face recognition with generative models. In _Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition_ , pages 11845–11854, 2021. 3 

- [66] Cihang Xie, Zhishuai Zhang, Yuyin Zhou, Song Bai, Jianyu Wang, Zhou Ren, and Alan L Yuille. Improving transferability of adversarial examples with input diversity. In _Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition_ , 2019. 3 

- [67] Haochuan Xu, Yun Sing Koh, Shuhuai Huang, Zirun Zhou, Di Wang, Jun Sakuma, and Jingfeng Zhang. Model-agnostic adversarial attack and defense for vision-language-action models. _arXiv preprint arXiv:2510.13237_ , 2025. 1 

- [68] Kaidi Xu, Gaoyuan Zhang, Sijia Liu, Quanfu Fan, Mengshu Sun, Hongge Chen, Pin-Yu Chen, Yanzhi Wang, and Xue Lin. Adversarial t-shirt! evading person detectors in a physical world. In _Proc. IEEE European Conf. Computer Vision_ , pages 665–681. Springer, 2020. 3 

- [69] Yi Yu, Wenhan Yang, Yap-Peng Tan, and Alex C Kot. Towards robust rain removal against adversarial attacks: A comprehensive benchmark analysis and beyond. In _Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition_ , 2022. 2 

- [70] Yi Yu, Song Xia, Xun Lin, Chenqi Kong, Wenhan Yang, Shijian Lu, Yap-Peng Tan, and Alex C Kot. Towards model resistant to transferable adversarial examples via trigger activation. _IEEE Trans. on Information Forensics and Security_ , 2025. 1 

- [71] Yi Yu, Qixin Zhang, Shuhan Ye, Xun Lin, Qianshan Wei, Kun Wang, Wenhan Yang, Dacheng Tao, and Xudong Jiang. Time is all it takes: Spike-retiming attacks on event-driven spiking neural networks. In _Proc. Int’l Conf. Learning Representations_ , 2026. 2 

- [72] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _Proc. IEEE Int’l Conf. Computer Vision_ , 2023. 2, 3 

- [73] Hangtao Zhang, Chenyu Zhu, Xianlong Wang, Ziqi Zhou, Changgan Yin, Minghui Li, Lulu Xue, Yichen Wang, Shengshan Hu, Aishan Liu, et al. Badrobot: Jailbreaking embodied llms in the physical world. _arXiv preprint arXiv:2407.20242_ , 2024. 1 

- [74] Jianping Zhang, Weibin Wu, Jen-tse Huang, Yizhan Huang, Wenxuan Wang, Yuxin Su, and Michael R Lyu. Improving adversarial transferability via neuron attribution-based 

22877 

attacks. In _Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition_ , 2022. 3 

- [75] Yaoyuan Zhang, Yu-an Tan, Tian Chen, Xinrui Liu, Quanxin Zhang, and Yuanzhang Li. Enhancing the transferability of adversarial examples with random patch. In _International Joint Conference on Artificial Intelligence_ , 2022. 3 

- [76] Mengnan Zhao, Lihe Zhang, Yuqiu Kong, and Baocai Yin. Fast adversarial training with smooth convergence. In _Proc. IEEE Int’l Conf. Computer Vision_ , pages 4720–4729, 2023. 1 

   - [88] Rongyi Zhu, Zeliang Zhang, Susan Liang, Zhuo Liu, and Chenliang Xu. Learning to transform dynamically for better adversarial transferability. In _Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition_ , 2024. 3 

   - [89] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 1, 2 

- [77] Mengnan Zhao, Lihe Zhang, Yuqiu Kong, and Baocai Yin. Catastrophic overfitting: A potential blessing in disguise. In _Proc. IEEE European Conf. Computer Vision_ , pages 293– 310. Springer, 2024. 

- [78] Mengnan Zhao, Lihe Zhang, Wei Wang, Yuqiu Kong, and Baocai Yin. Adversarial attacks on scene graph generation. _IEEE Trans. on Information Forensics and Security_ , 19:3210–3225, 2024. 

- [79] Mengnan Zhao, Lihe Zhang, Jingwen Ye, Huchuan Lu, Baocai Yin, and Xinchao Wang. Adversarial training: A survey. _arXiv preprint arXiv:2410.15042_ , 2024. 

- [80] Xueyang Zhou, Guiyao Tie, Guowen Zhang, Hechang Wang, Pan Zhou, and Lichao Sun. Badvla: Towards backdoor attacks on vision-language-action models via objectivedecoupled optimization. _arXiv preprint arXiv:2505.16640_ , 2025. 1 

- [81] Ziqi Zhou, Shengshan Hu, Minghui Li, Hangtao Zhang, Yechao Zhang, and Hai Jin. Advclip: Downstream-agnostic adversarial examples in multimodal contrastive learning. In _ACM Trans. Multimedia_ , pages 6311–6320, 2023. 

- [82] Ziqi Zhou, Minghui Li, Wei Liu, Shengshan Hu, Yechao Zhang, Wei Wan, Lulu Xue, Leo Yu Zhang, Dezhong Yao, and Hai Jin. Securely fine-tuning pre-trained encoders against adversarial examples. In _Proceedings of the 2024 IEEE Symposium on Security and Privacy (SP’24)_ , 2024. 

- [83] Ziqi Zhou, Yufei Song, Minghui Li, Shengshan Hu, Xianlong Wang, Leo Yu Zhang, Dezhong Yao, and Hai Jin. Darksam: Fooling segment anything model to segment nothing. In _Proc. Annual Conf. Neural Information Processing Systems_ , 2024. 

- [84] Ziqi Zhou, Yifan Hu, Yufei Song, Zijing Li, Shengshan Hu, Leo Yu Zhang, Dezhong Yao, Long Zheng, and Hai Jin. Vanish into thin air: Cross-prompt universal adversarial attacks for sam2. In _Proc. Annual Conf. Neural Information Processing Systems_ , 2025. 

- [85] Ziqi Zhou, Bowen Li, Yufei Song, Shengshan Hu, Wei Wan, Leo Yu Zhang, Dezhong Yao, and Hai Jin. Numbod: A spatial-frequency fusion attack against object detectors. In _Proc. AAAI Conf. on Artificial Intelligence_ , 2025. 1 

- [86] Bin Zhu, Bin Lin, Munan Ning, Yang Yan, Jiaxi Cui, HongFa Wang, Yatian Pang, Wenhao Jiang, Junwu Zhang, Zongwei Li, et al. Languagebind: Extending video-language pretraining to n-modality by language-based semantic alignment. _arXiv preprint arXiv:2310.01852_ , 2023. 2 

- [87] Hegui Zhu, Yuchen Ren, Xiaoyan Sui, Lianping Yang, and Wuming Jiang. Boosting adversarial transferability via gradient relevance attack. In _Proc. IEEE Int’l Conf. Computer Vision_ , 2023. 3 

22878 

