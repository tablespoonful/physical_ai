---
title: "MAPS: Preserving Vision-Language Representations via Module-Wise Proximity Scheduling for Better Vision-Language-Action Generalization"
date: "2025-11-25"
authors: "Chengyue Huang; Mellon M. Zhang; Robert Azarcon; Glen Chou; Zsolt Kira"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2511.19878
pdf: https://arxiv.org/pdf/2511.19878
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.19878)** / [論文ページ](https://arxiv.org/abs/2511.19878)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **MAPS: Preserving Vision-Language Representations via Module-Wise Proximity Scheduling for Better Vision-Language-Action Generalization** 

Chengyue Huang<sup>*</sup> Mellon M. Zhang<sup>*</sup> Robert Azarcon Glen Chou Zsolt Kira Georgia Institute of Technology 

_{_ chuang475,meilongz,razarcon3,chou,zkira _}_ @gatech.edu mapsvla.github.io 

## **Abstract** 

_Vision-Language-Action (VLA) models inherit strong priors from pretrained Vision-Language Models (VLMs), but na¨ıve fine-tuning often disrupts these representations and harms generalization. Existing fixes – freezing modules or applying uniform regularization – either overconstrain adaptation or ignore the differing roles of VLA components. We present_ **_MAPS (Module-Wise Proximity Scheduling)_** _, the first robust fine-tuning framework for VLAs. Through systematic analysis, we uncover an empirical order in which proximity constraints should be relaxed to balance stability and flexibility. MAPS linearly schedules this relaxation, enabling visual encoders to stay close to their pretrained priors while action-oriented language layers adapt more freely. MAPS introduces no additional parameters or data, and can be seamlessly integrated into existing VLAs. Across MiniVLA-VQ, MiniVLA-OFT, OpenVLAOFT, and challenging benchmarks such as SimplerEnv, CALVIN, LIBERO, as well as real-world evaluations on the Franka Emika Panda platform, MAPS consistently boosts both in-distribution and out-of-distribution performance (up to +30%). Our findings highlight empirically guided proximity to pretrained VLMs as a simple yet powerful principle for preserving generalization in VLM-to-VLA transfer._ 

## **1. Introduction** 

Vision-Language-Action (VLA) models have recently emerged as a unifying framework for robotic learning, enabling agents to perceive their environment, understand natural language instructions, and execute actions in an endto-end manner [1–4]. However, the scarcity of large-scale robotics data makes it infeasible to train these models from scratch. As a result, most VLA systems initialize from powerful vision-language models (VLMs) [5–7] pretrained on 

> *Equal contribution. 

web-scale data, leveraging their rich visual and semantic priors before finetuning on robotics datasets to learn action policies. However, while this strategy has led to impressive task performance, it often comes at the cost of generalization – models degrade in performance when faced with novel tasks, objects, or environments [8, 9]. 

This loss of generalization arises from a fundamental mismatch between large-scale pretraining and the limited scope of robot-specific finetuning [1]. Robotics datasets are typically sparse and task-specific, and finetuning extensively on them induces spurious correlations and overfitting, which in turn causes catastrophic forgetting of spatial reasoning, world knowledge, and linguistic grounding. The core challenge in VLA training therefore lies in balancing the tradeoff between action adaptation and preservation of pretrained generalization. Excessive finetuning causes the model to drift too far from its pretrained initialization, diminishing robustness to distribution shifts [10]. Conversely, insufficient finetuning limits the model’s ability to align with the action space. 

Several approaches attempt to balance adaptation and generalization. Freezing visual encoders preserves pretrained perception but limits adaptation to robotics-specific cues. Dual-encoder designs [9] maintain both frozen and trainable visual pathways, improving flexibility at the cost of doubled memory and compute. Weight interpolation techniques [8] gradually revert visual weights to their pretrained state while adapting the language backbone, but require multiple training stages. In these efforts, generalization often comes at the expense of higher computational and architectural complexity, with most methods emphasizing visual preservation while overlooking the role of semantic priors in language components. 

Seeking a lightweight alternative to preserving pretrained knowledge, we begin by revisiting the common practice of model freezing. Through a systematic analysis of freezing different VLM components during action fine- 

32451 

tuning, we confirm a widely held but rarely quantified intuition: visual modules should remain strongly constrained. Early visual backbones such as DINOv2 [11] capture essential geometric and spatial priors for manipulation, whereas language-aligned modules like SigLIP [12] and deeper language layers benefit from greater flexibility to adapt taskspecific semantics and action grounding. However, we also find that freezing itself introduces task-specific inductive biases, and certain freeze configurations fail to generalize across new domains and environments. 

Instead of hard constraints from model freezing, soft regularization offers a more flexible and robust alternative with comparable efficiency [10, 13–16]. Projection-based selective tuning methods, such as selective projection decay [13], replace conventional weight decay with a projection operator that limits how far parameters drift from their pretrained values – enabling adaptive regularization across layers without added complexity. However, existing approaches typically use a single hyperparameter to enforce a uniform regularization strength, implicitly assuming all layers should deviate equally. We find this assumption ill-suited for VLA models, where different components encode distinct priors and vary in their sensitivity to fine-tuning. Some modules must stay near their pretrained state to preserve structural knowledge, while others require greater flexibility to adapt task-specific grounding. 

This introduces a new tradeoff: naive freezing provides modularity but is brittle due to strong inductive bias, whereas robust finetuning relaxes this bias but sacrifices modularity. To bridge this tradeoff and successfully adapt the robust finetuning paradigm to the action domain, we propose **MAPS (Module-Wise Proximity Scheduling)** , a robust finetuning framework designed specifically for VLA models. MAPS extends traditional projection-based selective tuning [13] by modulating the _projection strength rate of change_ hyperparameter across model components and training steps via a linear scheduler. This encourages more careful updates of the visual components to preserve pretrained geometric priors while allowing more explorative updates of the language components to quickly adapt to the action space. Importantly, this scheduling is implemented with no additional models, data, or parameters and integrates seamlessly with existing VLA architectures. 

We validate MAPS across a wide range of VLA backbones, including MiniVLA-VQ [17, 18], MiniVLA-OFT, OpenVLA-OFT [19], etc. Experiments on a diverse set of evaluation benchmarks - SimplerEnv Bridge Data [20], CALVIN [21] (ABC→D), LIBERO [22] (train on LIBERO-90, test on Goal/Spatial/Object/Long), and realworld evaluations on a Franka Emika Panda robot consistently show that MAPS improves out-of-distribution (OOD) generalization while preserving pretrained structure and indistribution (ID) performance. These findings suggest that 

maintaining proximity to pretrained VLMs in a selective manner is a simple yet powerful principle that could guide future scaling and pre-training of VLA systems. 

## **2. Related Works** 

**Vision-Language-Action Models.** Vision-LanguageAction (VLA) models advance unified embodied intelligence by leveraging large pretrained foundation models [5– 7] and their components [11, 12, 23]. Systems like RT1, PaLM-E, and RT-2 [2, 3, 24] showed that grounding vision-language pretraining in experience enables crosstask transfer. Large frameworks such as Open-X Embodiment, OpenVLA, and _π_ 0 [1, 4, 19, 25–27] scale data and architectures for generalization. Recent work improves action tokenization [18, 28–32], efficiency [17, 33, 34], and grounding/reasoning [35–41], while emerging work explores chain-of-thought reasoning for interpretable control [42–44]. Despite progress, most VLAs rely on finetuning that disrupts pretrained priors; MAPS instead preserves them via module-wise proximity scheduling for selective adaptation. 

**VLA Generalization.** Improving generalization in VLA models focuses on preserving pretrained representations while adapting to new tasks. Data-oriented approaches reformulate robotic data for better VLM alignment (directional prediction [45] or textual trajectory conversion [46]) and co-train with action objectives [9, 28]. Trainingoriented methods retain learned priors via weight interpolation [8], dual encoders [9], frozen cross-attention [47], embedding regularization [48], or action perturbation [49]. These add computational overhead, whereas MAPS constrains updates by module importance and proximity to pretrained weights, preserving priors and improving OOD generalization without extra data or parameters. 

## **3. Background** 

### **3.1. Vision-Language-Action Models** 

A Vision-Language-Action (VLA) model [1, 3, 4, 15] seeks to learn a policy _πθ_ ( _at | ot, x_ ) that maps a multimodal observation _ot_ and a language instruction _x_ to an action _at_ in an embodied environment. Typically, the visual and language inputs are encoded by _fv_ and _fl_ separately, and fused by a multimodal transformer _fm_ to produce a policy embedding _zt_ = _fm_ ([ _fv_ ( _ot_ ) _, fl_ ( _x_ )]). Action parameterization varies across families of VLAs: **continuous-action models** predict low-level control vectors directly and are trained to make their outputs closely match the expert’s actions, using objectives such as _ℓ_ 1 regression [19], diffusion-based denoising [44], or flow matching [4]. In contrast, **discreteaction models** convert actions or short action segments into a finite set of tokens [1]. Modern VLAs build upon pretrained vision-language backbones such as DINOV2 [11], 

32452 


Figure 1. **Module-Wise Proximity Scheduling (MAPS)** . MAPS is applied on pretrained VLM components during the action finetuning stage. MAPS (blue dash line) enforces strong preservation on early vision layers while progressively relaxing constraints toward higherlevel language layers. In contrast, vanilla finetuning (green dash line) distorts the VLM representation completely away from its pretrained weights (black solid line), and uniform SPD (orange dash/dot line) applies the same constraint everywhere. 

SIGLIP [12], and LLAMA [7], using either a multi-modal transformer or a lightweight cross-attention “bridge” to fuse representations before an action head maps _zt_ into either continuous controls or discrete tokens. Models such as _π_ 0- Fast [29], and OpenVLA-OFT [19] follow this template but introduce small projection heads or adapters for rapid finetuning and deploying. During training on robot demonstrations, the model grounds linguistic semantics in actionconditioned representations that transfer across tasks, objects, and embodiments. 

### **3.2. Robust Fine-Tuning** 

We revisit projection-based robust fine-tuning (RFT) methods [10, 13, 15, 50, 51] that constrain fine-tuning to remain close to the pretrained weights, enabling models to adapt to downstream tasks while preserving pretrain generalization. **From L2 regularization to projection.** Vanilla fine-tuning updates model parameters to minimize the task loss _L_ without constraining deviation from the pretrained model. This often leads to feature drift and catastrophic forgetting [10, 14, 15]. L2-SP [14] addresses this issue by penalizing the distance between the fine-tuned parameters _θt_ and the pretrained initialization _θ_ 0 with regularization strength _λ_ reg at each gradient iteration step _t_ : 


Instead of regularizing _∥θt∥_ 2, L2-SP explicitly preserves proximity to the pretrained model. Building on this idea, TPGM [10] reformulates L2-SP by enforcing the model to 

stay within a distance of _γ_ from the pre-trained model: 


To enforce this constraint during training, TPGM applies the _Projected Gradient Method_ (PGM), projecting the updated weights back into an _ℓ_ 2 ball with radius _γ_ around _θ_ 0, where _θ_<sup>˜</sup> _t_ is the unconstrained updated weight: 


**Selective Projection Decay (SPD).** SPD [13] builds on the projection view of L2-SP and TPGM by determining whether and how much the uncontrained update _θ_<sup>˜</sup> _t_ should be projected back toward the pretrained weights _θ_ 0. **Step 1: When to project.** Motivated by the derivative of _L_ w.r.t. _λ_ reg, i.e.<sup>_∂_</sup> _∂λ_<sup>_L_</sup><sup><u>(</u></sup> reg<sup>_θt_</sup><sup><u>)</u></sup> =<sup>_∂L_</sup> _∂θ_<sup><u>(</u></sup><sup>_θ_</sup> _t_<sup>_t_</sup><sup><u>)</u></sup> ⊺ _∂λ∂θ_ reg _<u>t</u>_<sup>=</sup><sup>_α ∗−g_</sup> _t_<sup>⊺</sup> +1<sup>(˜</sup><sup>_θt −θ_0)</sup> where _α_ is the learning rate and _g_ is the gradient, SPD uses the sign of _ct_ := _−gt_<sup>_⊤_</sup> +1<sup>(˜</sup><sup>_θt−θ_0)astheselectioncondi-</sup> tion, since it determines the direction of the hyper-update: if _ct <_ 0, gradient descent increases _λ_ reg and strengthens L2SP regularization, whereas if _ct >_ 0, it decreases _λ_ reg and weakens the regularization. Thus, SPD triggers a projection step if _ct <_ 0; otherwise the update is left unchanged. **Step 2: How much to project.** L2-SP’s optimization step after unconstrained update can be written as _θt_ = = _θ_ ˜ _t − λ_ reg _α_ (˜ _θt − θ_ 0). Reformulating Eq. (3) as _θt θ_ ˜ _t −_ 1 _−_ _<u>γ</u> ∗_ ( _θ_<sup>˜</sup> _t − θ_ 0), L2-SP (regular� max _{γ,∥θ_<sup>˜</sup> _t−θ_ 0 _∥_ 2 _}_ � ization) and projection are equivalent if _λ_ reg _α_ = (1 _−_ max _{γ,∥γθ_<sup>˜</sup> _t−θ_ 0 _∥_ 2 _}_<sup>).SPD then defines a deviation ratio</sup><sup>_rt_=</sup> 

32453 


Figure 2. Qualitative comparison of freezing configurations for LIBERO-90 task ”put the bowl on the plate” (left to right: full finetuning (FFT), freeze VLM, freeze language, freeze vision). FFT fails most, targetting the cabinet instead of the bowl. Freezing VLM/language/vision preserves 2D localization of the bowl but impairs depth reasoning. When vision is frozen, the policy can grasp the bowl but fails to accurately place it on the plate. 

max _<u>{γt−γt−</u>_ 1 _<u>}</u>_ based on the current deviation radius (before _γt_ regularization) _γt_ = _∥θ_<sup>˜</sup> _t − θ_ 0 _∥_ 2 and the previous radius _γt−_ 1 = _∥θt−_ 1 _− θ_ 0 _∥_ 2, and replace the learning rate _α_ in L2SP with the deviation ratio _rt_ . This makes the _new hyperparameter λ_ tuning more intuitive, where _λ_ reg _α_ = _λrt_ . Intuitively, with _λ_ = 1, _θt_ = _θ_<sup>˜</sup> _t −_<sup>max</sup><sup>_<u>{</u>_0</sup><sup>_<u>,γ</u>_</sup> _γ_<sup>_t_</sup> _t_<sup>_−γt−_1</sup><sup>_<u>}</u>_</sup> ( _θ_<sup>˜</sup> _t − θ_ 0) = _θ_ 0 + max _{γγtt−−_ 11 _,γt}_<sup>_∗_(˜</sup><sup>_θt−θ_0),theregularizationisequiv-</sup> alent to projecting the updated parameters onto a ball with radius equal to the previous deviation whenever the current deviation exceeds that value. Now, a single hyperparameter _λ_ replaces the conventional weight decay and controls how aggressively the constraint radius expands or contracts during training. When _λ_ = 0, SPD reduces to full finetuning with no projection; 0 _< λ <_ 1 allows the radius to expand, enabling flexible adaptation; _λ_ = 1 keeps the deviation from the pretrained model fixed; and _λ >_ 1 contracts the radius, pulling parameters back toward _θ_ 0. Despite being a single scalar, _λ_ enables dynamic and layer-specific projection across optimization steps. 

## **4. Method** 

### **4.1. Catastrophic Forgetting in VLAs** 

VLA models are well known to struggle with zero-shot generalization across new tasks, environments, and instructions. Prior work traces this largely to catastrophic forgetting during action finetuning. ReVLA [8] attributes the issue to collapse in the DINOv2 [11] encoder, where depth estimation degrades into low-detail, spatially uniform maps – losing the rich geometry preserved in the pretrained DINOv2 features of PrismaticVLM [52]. [48] similarly find that fine-tuned VLAs attend to irrelevant regions under OOD conditions, with t-SNE analyses revealing compressed, degenerate feature spaces. [9] further observe oversensitivity to background variation and instruction phrasing, suggesting overfitting to language form rather than meaning. Collectively, these studies identify action finetuning as the primary source of generalization failure, motivating efforts to preserve VLM representations during adaptation. 

Freezing parts of a pretrained VLM is a simple yet ef- 

fective way to preserve learned representations, preventing weights from drifting in suboptimal directions during finetuning. Recent works have refined this idea in various ways: [9] freeze the vision encoder and train a separate copy, [48] regularize against a frozen teacher, and ReVLA [8] interpolates vision-encoder weights between pretrained and adapted models while tuning the language backbone. While these strategies improve generalization, they often incur extra computation and supervision. Motivated by this line of work, we investigate how far simple freezing alone can bridge the generalization gap between VLMs and VLAs. 

### **4.2. How good is model freezing?** 

To study the impact of model freezing, we decompose the VLA architecture into four components – DINOv2, SigLIP, early language layers, and late language layers – and systematically evaluate different freezing configurations on both ID and OOD settings. We focus on the OpenVLA [1] family, which integrates a joint DINOv2–SigLIP visual encoder. This modular design allows precise control over which capabilities are retained during adaptation: DINOv2 contributes depth perception and geometric priors, while SigLIP provides strong vision–language alignment. To ensure coverage across model scales and benchmarks, we conduct experiments with VLA-Adapter [53] on LIBERO and MiniVLA-OFT [17] on SimplerEnv BridgeV2 (see Sec. 5 and Appendix Sec. 7 for experimental details). 

Our results (Tables 1 and 2) reveal several key insights into the efficacy of freezing: 

1. **Language adaptation is essential.** Freezing the language backbone severely limits adaptation to the action space, yielding near-zero performance on SimplerEnv and up to a 60% drop on LIBERO. 

2. **Freezing the vision encoder generally improves performance.** On SimplerEnv, ID accuracy increases by 7– 17% and OOD by 7–25%; on LIBERO, gains are smaller but consistent (around 5% ID). In Fig. 2, freezing vision components allows the robot arm to grasp the bowl, whereas all other configurations struggle. 

3. **Late language layers drive task performance.** Finetuning late language layers while freezing early ones boosts OOD generalization by 1–3%, aligning with their direct role in producing action outputs. 

4. **Preserving DINOv2 matters more than SigLIP.** Freezing DINOv2 yields roughly 5% higher OOD performance than freezing SigLIP, underscoring the importance of maintaining strong geometric priors. 

5. **Freezing effects are not universally consistent.** Freezing demonstrates improvements over full fine-tuning. Yet, some configurations (ex. freeze early language) improve one benchmark but harm another, indicating that freezing introduces task-dependent inductive biases. Overall, our findings suggest a hierarchy of importance 

32454 

Table 1. Comparison of freezing or robust fine-tuning (RFT) different parts of VLA on SimplerEnv’s ID and OOD tasks (details in Sec. 5.2). Early L and Last L denote early and the last language layers. � and � represent freeze and full fine-tune. 

||**Mod**|**ules**||||**ID**|||||**OOD**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|DINOv2|SigLIP|Early L|Last L|T1: Spoon|T2: Carrot|T3: Stack|T4: Eggplant|Avg. ID|Visual|Novel Object|Novel Category|Avg. OOD|
||MiniVLA|-OFT<sup>_†_</sup>||22.0|30.0|0.0|2.0|13.5|12.7|2.0|12.0|8.9|
|�|�|�|�|22.0|24.0|0.0|34.0|20.0|20.0|13.3|10.7|15.0|
|�|�|�|�|0.0|0.0|0.0|0.0|0.0|1.3|0.0|2.7|1.2|
|�|�|�|�|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|
|�|�|�|�|42.0|32.0|6.0|42.0|30.5|32.7|51.3|11.3|33.6|
|�|�|�|�|12.0|10.0|12.0|90.0|31.0|29.3|35.3|22.7|29.7|
|�|�|�|�|0.0|0.0|0.0|0.0|0.0|4.0|0.7|2.0|2.2|
||RF|T||4.0|8.0|0.0|94.0|26.5|6.7|20.0|14.0|13.6|


Table 2. Comparison of freezing different parts of VLA on LIBERO. Early L and Last L denote early and the last language layers. � and � represent freeze and full fine-tune. 

||**Modu**|**les**||**ID**|||**OOD**|||
|---|---|---|---|---|---|---|---|---|---|
|DINOv2|SigLIP|Early L|Last L|LIBERO-90|-Spatial|-Object|-Goal|-Long|**Avg. OOD**|
||VLA-Ad|apter<sup>_†_</sup>||83.0|2.0|5.0|1.0|2.0|2.5|
|�|�|�|�|92.0|0.0|3.0|0.0|6.0|2.3|
|�|�|�|�|29.0|1.0|4.0|1.0|0.0|1.5|
|�|�|�|�|19.0|0.0|0.0|1.0|0.0|0.3|
|�|�|�|�|89.0|0.0|6.0|0.0|6.0|3.0|
|�|�|�|�|73.0|1.0|0.0|0.0|3.0|1.0|
|�|�|�|�|91.0|0.0|4.0|6.0|8.0|4.5|
|�|�|�|�|59.0|0.0|0.0|0.0|0.0|0.0|
||RF|T||88.0|1.0|2.0|0.0|6.0|2.3|


among modules: 

DINOv2 _>_ SigLIP _>_ Early language _>_ Late language 

Yet, **freezing alone is not a reliable path to generalization** . While it allows selective preservation of pretrained knowledge, it also imposes strong biases that can degrade performance in unseen settings. A more robust alternative lies in soft regularization, where finetuning is guided rather than restricted. 

### **4.3. From hard constraints to soft constraints** 

The robust finetuning (RFT) literature (see Sec. 3.2) offers a natural foundation for our goal of constraining weight updates while preserving pretrained representations. In principle, RFT lowers task loss while keeping parameter drift minimal. While the intuition fits seamlessly with our goals, we find that naively applying RFT directly on the action finetuning offers only modest improvements over the baseline in both SimplerEnv (Tab. 1) and LIBERO (Tab. 2). This is because RFT techniques impose a single hyperparameter constraint across the entire model, meaning that layers either constrict closer towards or expand away from the pretrained weights at a uniform rate. As shown at the bottom of Fig. 3, this results in all components of the VLM diverging equal amounts from their pretrained representations. As we observed from Sec. 4.2, however, different components should evolve at different rates – some should be allowed more flexibility to adapt to the action space, whereas others should be constrained to preserve their pretrained priors. 

### **4.4. Module-Wise Proximity Scheduling** 

Our preliminary studies highlights a key tradeoff: model freezing offers high modularity at the cost of heavy inductive bias, RFT offers lighter inductive bias but has no modularity. To bridge the two paradigms and successfully adapt robust finetuning for the action domain, we introduce a new framework of RFT methods specifically tailored for VLA models, known as **Module-Wise Proximity Scheduling (MAPS).** 

MAPS assigns distinct proximity schedules to different components of the base VLM, enabling strong preservation where pretrained structure is crucial (e.g., early vision and early language layers) while allowing more aggressive adaptation where grounding to actions is most beneficial (e.g., higher-level language layers and the action head). In other words, MAPS is designed to _learn when to preserve and when to adapt_ , avoiding the rigidity of full freezing and the instability of uniform finetuning. 

Concretely, MAPS modifies SPD by replacing its _global_ proximity hyperparameter _λ_ with a _layer-wise_ , architectureaware schedule. Let _L_ = ( _ℓ_ 1 _, . . . , ℓ|L|_ ) denote the ordered stack of model submodules (DINOV2 _→_ SIGLIP _→_ BRIDGE _→_ LANGUAGE). For each layer index _k_ , MAPS assigns a proximity weight 


yielding a linear decay from _λ_ 1 = _λ_ max for early visual layers to _λ|L|_ = 0 for language layers. In addition, MAPS assigns _λk_ = 0 for all modules that are initialized from scratch, such as the action head, proprioceptive-state projector, and other non-pretrained components. Since these modules have no pretrained parameters _θ_ 0 to preserve, MAPS simply performs full fine-tuning on them. 

During optimization, let _θ_ denote the parameters of the current layer, _θ_ 0 their pretrained initialization, and _gt_ the gradient at iteration _t_ . MAPS first computes an unconstrained step _θ_<sup>�</sup> _t_ , after which it evaluates the gradient– displacement correlation 


32455 

Whenever _ct <_ 0, indicating that the update direction is inconsistent with preserving pretrained structure, MAPS applies a projection toward _θ_ 0 with _layer-specific_ strength: 


where _rt_ is the SPD deviation ratio (see Sec. 3.2). 

Unlike SPD, which uses a single global constraint and therefore cannot differentiate between layers with distinct gradient scales or semantic roles, MAPS explicitly encodes architectural structure: visual layers remain strongly anchored to pretrained perceptual representations, while deeper language layers are allowed to adapt more flexibly to task-level semantics. This is highlighted in Fig. 3, where DINOv2 weights diverge least, followed by SigLIP weights, and finally language weights adapt most. As shown in Appendix Sec. 9, the linear schedule outperforms constant and cosine alternatives, underscoring the importance of structured, layer-wise proximity control. Additional intuition on MAPS is also included in Appendix Sec. 11. 


Figure 3. We calculate the _ℓ_ 2 distance between fine-tuned and pre-trained weights. MAPS produces a smooth, module-aware decay in deviation from pretrained initialization (top). Applying robust finetuning only to the vision stack and full finetuning on language (RFT-V+FFT-L) constrains DINOv2 heavily but leaves SigLIP and language relatively unconstrained (middle). Uniform _λ_ (RFT) constrains all layers equally (bottom). 

Crucially, MAPS is lightweight and plug-and-play: it introduces no additional parameters, requires no auxiliary networks or extra data, and can be applied to existing VLA architectures without modification. By directly encoding the empirical hierarchy revealed in our preliminary studies, MAPS strikes an effective balance between retaining essential pretrained priors and adapting to new action domains. 

## **5. Experiments** 

We evaluate MAPS through three guiding questions. **(RQ1)** How well does it generalize across ID and OOD tasks? To test this, we use three diverse benchmarks – SimplerEnv 

[20] (Sec. 5.2), CALVIN [21] (Sec. 5.3), and LIBERO [22] (Sec. 5.4) – that span semantic, environmental, and visual shifts, providing a comprehensive measure of robustness. **(RQ2)** Are MAPS’ gains consistent across architectures? We evaluate five state-of-the-art VLA backbones – MiniVLA-VQ, MiniVLA-OFT, VLA-Adapter, OpenVLAOFT, and NORA – to test architecture-agnostic benefits. **(RQ3)** Does the robustness afforded by MAPS transfer to real-world deployment? We assess real-world transfer by deploying MAPS on a Franka Emika Panda manipulator (Sec. 5.1). Importantly, across all benchmarks, _we evaluate MAPS by fine-tuning the base VLM weights directly_ . In other words, we initialize each VLA backbone from its pretrained VLM and train it from scratch using MAPS. 

**Backbones.** Because MAPS does not rely on architecturespecific hyperparameters, it can be dropped into models with any visual encoder, language model, or action tokenization strategy. To demonstrate this flexibility, we instantiate MAPS across four widely used VLA backbones: MiniVLA-VQ [17], MiniVLA-OFT, OpenVLA-OFT [19], and VLA-Adapter [53]. To demonstrate generalizability beyond the OpenVLA family, we also evaluate MAPS on the NORA [54] backbone in Appendix Sec. 10. For details about these backbones, please see Appendix Sec. 7. 

### **5.1. Performance on Franka Emika Panda** 

**Experimental setting.** We conduct real-world tabletop manipulation experiments using a single Franka Emika Panda robotic arm. Our task suite consists of 4 paired ID and OOD tasks, which includes: (1) Grab coke can; (2) Stack blocks; (3) Stack cups; and (4) Close laptop. We form a pretraining corpora of 150 demonstrations per task following [55], and train MiniVLA-OFT (directly updating the VLM weights) using our self-collected demonstration dataset with both vanilla finetuning and MAPS. We provide our quantitative results below. Details on our task suite, extended fine-grained task analysis, qualitative results, rollout visualizations, setup details, and an in-depth results discussion along with observed success and failure modes can be found in Appendix Sec. 8. 

**Evaluation results.** Table 3 presents the success rates for each task together with the overall average performance. MAPS yields substantial gains over MiniVLA-OFT on both ID and OOD tasks. On the ID tasks, MAPS raises average performance from 40.0% to 72.5%, demonstrating much stronger policy learning from limited demonstrations. MAPS also improves generalization under distribution shift, boosting average OOD success from 22.5% to 52.5%. Overall, MAPS enhances both robustness and task success across diverse manipulation scenarios, showing clear benefits for real-world policy training (RQ3). 

32456 

Table 3. **Franka Results** . 

|**Model**|||**ID**|||||**OOD**|||
|---|---|---|---|---|---|---|---|---|---|---|
||T1: Coke|T2: Block|T3: Cup|T4: Laptop|Avg. ID|T1: Coke|T2: Block|T3: Cup|T4: Laptop|Avg. OOD|
|MiniVLA-OFT<sup>_†_</sup>|30.0|30.0|0.0|100.0|40.0|50.0|20.0|0.0|30.0|22.5|
|**+MAPS**(_Ours_)|50.0|70.0|80.0|90.0|72.5|100.0|30.0|20.0|60.0|52.5|
|∆|+20.0|+40.0|+80.0|-10.0|+32.5|+50.0|+10.0|+20.0|+30.0|+30.0|


Table 4. **SimplerEnv Results** . ID includes 4 tasks following SimplerEnv-Bridge setup. OOD evaluation suites include Visual, Novel Object, and Novel Category.<sup>_∗_</sup> model checkpoints borrowed from original papers.<sup>_†_</sup> models pretrained from scratch on SimplerEnv. 

|**Model**|||**ID**|||||**OOD**||
|---|---|---|---|---|---|---|---|---|---|
||T1: Spoon|T2: Carrot|T3: Stack|T4: Eggplant|Avg. ID|Visual|Novel Object|Novel Category|Avg. OOD|
|RT-1-X [2]|4.2|0.0|0.0|0.0|1.1|0.0|4.0|6.1|3.4|
|Octo [56,57]|12.5|41.7|15.8|0.0|17.5|12.6|10.8|8.4|10.6|
|_π_0[4]|52.5|87.9|83.8|52.5|69.2|71.4|30.2|21.0|40.9|
|MiniVLA-VQ <sup>_†_ </sup>[17]|52.0|24.0|42.0|58.0|44.0|37.3|34.0|27.3|32.9|
|**+MAPS**(_Ours_)|44.0|30.0|76.0|20.0|42.5|48.0|26.0|29.3|34.4|
|∆|-8.0|+6.0|+34.0|-38.0|-1.5|+10.7|-8.0|+2.0|+1.5|
|MiniVLA-OFT<sup>_†_</sup>|22.0|30.0|0.0|2.0|13.5|12.7|2.0|12.0|8.9|
|**+MAPS**(_Ours_)|34.0|38.0|0.0|48.0|30.0|32.0|48.7|26.7|35.8|
|∆|+12.0|+8.0|+0.0|+46.0|+16.5|+19.3|+46.7|+14.7|+26.9|
|OpenVLA-OFT<sup>_†_ </sup>[19]|16.0|18.0|0.0|58.0|23.0|16.0|9.3|0.7|8.7|
|**+MAPS**(_Ours_)|2.0|16.0|0.0|74.0|23.0|18.7|20.0|12.7|17.1|
|∆|-14.0|-2.0|+0.0|+16.0|+0.0|+2.7|+10.7|+12.0|+8.4|


Figure 4. SimplerEnv qualitative example (new object: Red Bull can). Top: Full fine-tuning fails to complete the task. Bottom: MAPS successfully places the can on the plate. 

### **5.2. Performance on SimplerEnv** 

**Experimental setting.** SimplerEnv is a lightweight simulation benchmark for efficient robotic manipulation evaluation. Because its tasks are originally text-only, we follow [57] to add visual observations and align it with the VLA setting. For ID evaluation, we use the standard WidowX BridgeData V2 Visual Matching setup and report performance on four tasks: spoon on towel, carrot on plate, stack cube, and put eggplant in basket. For OOD evaluation, we adopt the extended suite from [57], which includes: (1) Visual Generalization, placing three ID tasks in unseen environments; (2) Novel Object, introducing new instances from known categories; and (3) Novel Category, involving entirely new object types. We report success rates on both ID and OOD splits (Table 4). 

**Evaluation results.** On MiniVLA-OFT, MAPS matches the ID performance of Vanilla finetuning, but demonstrates 10-20% improvement on OOD generalization. Notably, despite a substantially smaller pretraining corpora of just the 

BridgeData V2 Visual Matching tasks, MAPS matches and even surpasses the OOD generalizability of much larger and much more extensively pretrained baselines such as RT-1X, Octo and _π_ 0. On MiniVLA-VQ, MAPS maintains similar ID performance and offers a moderate increase in OOD performance. On OpenVLA-OFT, MAPS maintains similar ID performance and improves average OOD by 8.4%. Again, this suggests that MAPS scales effectively across a variety of backbone sizes and architectures (RQ2). 

### **5.3. Performance on CALVIN** 

**Experimental setting.** CALVIN features long-horizon tabletop manipulation tasks in a real-to-sim setting, partitioned into the A, B, C, and D splits that increasingly withhold task–environment combinations. We follow the standard ABC _→_ D protocol: models are trained on splits A–C and evaluated OOD on split D. During evaluation, agents must complete sequences of five instructions; each new instruction is provided only after the previous one is completed, with success defined by reaching the instruction’s 

32457 


Figure 5. **CALVIN Results** . MAPS improves success rates across all action horizons (25% for MiniVLA-OFT and 3% for OpenVLA-OFT) and average length (+0.7 for MiniVLA-OFT and +0.1 for OpenVLA-OFT). 

goal state. The benchmark reports two metrics: _tasks completed in a row_ , the success rate for completing exactly _k_ consecutive tasks ( _k_ = 1–5), and _average length (avg. len)_ , the mean number of tasks completed per five-instruction sequence across all episodes. 

**Evaluation results.** As shown in Fig. 5, MAPS leads to a +0.7 gain in average sequence length and consistently improves success rates across all task horizons on MiniVLAOFT. The largest gains are observed for longer horizons: MAPS improves the success rate of completing 2-, 3-, 4-, and 5-task sequences by roughly 15% each, while the 1-task success rate increases by 7%. MAPS demonstrates modest improvements over OpenVLA-OFT, boosting success rates by 2% across task horizons. Notably, MAPS demonstrates larger gains on stronger baselines, suggesting that it complements rather than replaces existing capabilities, and scales effectively with model quality (RQ2). 

### **5.4. Performance on LIBERO** 

**Experimental setting.** The LIBERO benchmark consists of procedurally generated household manipulation tasks designed to evaluate generalization across task configurations, object appearances, and spatial layouts. It includes several predefined splits – LIBERO-90, LIBERO-Long, LIBEROGoal, LIBERO-Spatial, and LIBERO-Object – each targeting a specific type of generalization, such as task diversity, long-horizon planning, unseen goals, spatial rearrangements, or novel objects. Previous works often rely on largescale external pretraining – such as on Open X Embodiment – followed by fine-tuning separate model variants for each LIBERO split, and reporting results using these tailored models. In contrast, **our approach uses no external pretraining whatsoever** . Instead, we follow the more challenging protocol of [53]: we pre-train solely on the LIBERO-90 subset, and evaluate both ID performance on LIBERO-90 and OOD generalization on LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-Long. We 

Table 5. **LIBERO Results** .<sup>_∗_</sup> Results from [17].<sup>_†_</sup> Pretrained from scratch on LIBERO-90.<sup>_‡_</sup> Finetuned on LIBERO-90. 

|**Model**|**ID (%)**|||**OOD (%**|**)**||
|---|---|---|---|---|---|---|
||LIBERO-90|-Spatial|-Object|-Goal|-Long|**Avg. OOD**|
|OpenVLA|62.0|-|-|-|-|-|
|miniVLA<sup>_∗_</sup>|61.4|0.0|0.0|0.0|1.0|0.25|
|miniVLA-VQ<sup>_∗_</sup>|77.0|0.0|0.0|3.0|1.0|1.0|
|miniVLA-hist.<sup>_∗_</sup>|82.0|0.0|1.0|2.0|7.0|2.5|
|miniVLA-wrist<sup>_∗_</sup><br>|82.1|0.0|0.0|0.0|0.0|0.0|
|SpatialVLA<sup>_‡_</sup>|46.2|0.0|0.0|0.67|1.33|0.5|
|MiniVLA-VQ<sup>_†_</sup>|79.0|0.0|0.0|0.0|0.0|0.0|
|**+MAPS**(_Ours_)|82.0|0.0|1.0|8.0|10.0|4.75|
|∆|+3.0|+0.0|+1.0|+8.0|+10.0|+4.75|
|MiniVLA-OFT<sup>_†_</sup>|91.0|0.0|8.0|7.0|4.0|4.75|
|**+MAPS**(_Ours_)|91.0|6.0|14.0|0.0|8.0|7.0|
|∆|+0.0|+6.0|+6.0|-7.0|+4.0|+2.25|
|VLA-Adapter<sup>_†_</sup>|83.0|2.0|5.0|1.0|2.0|2.5|
|**+MAPS**(_Ours_)|88.0|0.0|7.0|6.0|6.0|4.75|
|∆|+5.0|-2.0|+2.0|+5.0|+4.0|+2.25|
|OpenVLA-OFT<sup>_†_</sup>|92.0|3.0|9.0|3.0|5.0|5.0|
|**+MAPS**(_Ours_)|90.0|0.0|11.0|1.0|10.0|5.5|
|∆|-2.0|-3.0|+2.0|-2.0|+5.0|+0.5|


report the success rates using 10 trials per task in Table 5. **Evaluation results.** MAPS delivers consistent improvements in OOD performance across all four model backbones, yielding an average gain of 1–5%. Notably, the base MiniVLA model shows no inherent OOD generalization capability; however, with MAPS, its performance increases by 8% on LIBERO-Goal and 10% on LIBEROLong. For MiniVLA-OFT, MAPS enhances generalization on LIBERO-Spatial and LIBERO-Object by 6%. Similarly, MAPS improves the VLA-Adapter’s performance on LIBERO-Goal and LIBERO-Long by 5% and OpenVLAOFT’s performance on LIBERO-Long by 5%. Beyond OOD gains, MAPS also provides moderate improvements on ID tasks, boosting MiniVLA-VQ performance by 3% and VLA-Adapter by 5%. This suggests that MAPS’ gains are indeed consistent across architectures and generalize well to different action tokenization schemes (RQ2). These results, in conjunction with results on the other benchmarks, also suggest that MAPS generalizes effectively across diverse ID and OOD tasks (RQ1). 

## **6. Conclusion** 

We present Module-Wise Proximity Scheduling (MAPS), a robust finetuning framework designed specifically for adapting pretrained VLM backbones to action data. By uncovering a clear hierarchy in how different model components should be constrained, MAPS applies a linear schedule that selectively regularizes each module. This yields conservative updates for visual layers – preserving essential geometric priors – while allowing more flexible adaptation in language components. Across SOTA backbones and standard benchmarks, MAPS delivers consistent improvements, enhancing both ID and OOD performance. Our findings highlight guided proximity to pretrained VLMs as a simple yet powerful principle for scalable VLA adaptation. 

32458 

**Acknowledgements.** The authors gratefully acknowledge Jeremiah Coholich for his early contributions to the development of the Franka setup as well as support with the real robot experiments. This material is based upon work partially supported by the National Science Foundation under Grant No. 2239292. This research was also supported in part by Lambda, Inc. and through research cyberinfrastructure resources and services provided by the Partnership for an Advanced Computing Environment (PACE) at the Georgia Institute of Technology, Atlanta, Georgia, USA. 

## **References** 

- [1] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An opensource vision-language-action model, 2024. URL https: //arxiv.org/abs/2406.09246. 1, 2, 4 

- [2] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Tomas Jackson, Sally Jesmonth, Nikhil J Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Kuang-Huei Lee, Sergey Levine, Yao Lu, Utsav Malla, Deeksha Manjunath, Igor Mordatch, Ofir Nachum, Carolina Parada, Jodilyn Peralta, Emily Perez, Karl Pertsch, Jornell Quiambao, Kanishka Rao, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Kevin Sayed, Jaspiar Singh, Sumedh Sontakke, Austin Stone, Clayton Tan, Huong Tran, Vincent Vanhoucke, Steve Vega, Quan Vuong, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-1: Robotics transformer for realworld control at scale, 2023. URL https://arxiv. org/abs/2212.06817. 2, 7 

- [3] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alexander Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait Singh, Radu Soricut, Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023. URL https://arxiv.org/abs/2307.15818. 2 

- [4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mo- 

hith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2024. URL https: //arxiv.org/abs/2410.24164. 1, 2, 7 

- [5] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, Thomas Unterthiner, Daniel Keysers, Skanda Koppula, Fangyu Liu, Adam Grycner, Alexey Gritsenko, Neil Houlsby, Manoj Kumar, Keran Rong, Julian Eisenschlos, Rishabh Kabra, Matthias Bauer, Matko Boˇsnjak, Xi Chen, Matthias Minderer, Paul Voigtlaender, Ioana Bica, Ivana Balazevic, Joan Puigcerver, Pinelopi Papalampidi, Olivier Henaff, Xi Xiong, Radu Soricut, Jeremiah Harmsen, and Xiaohua Zhai. Paligemma: A versatile 3b vlm for transfer, 2024. URL https://arxiv.org/abs/2407. 07726. 1, 2 

- [6] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang, Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5-vl technical report, 2025. URL https: 

   - //arxiv.org/abs/2502.13923. 1, 6 

- [7] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony Hartshorn, Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa, Isabel Kloumann, Artem Korenev, Punit Singh Koura, Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schelten, Ruan Silva, Eric Michael Smith, Ranjan Subramanian, Xiaoqing Ellen Tan, Binh Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu, Zheng Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Aurelien Rodriguez, Robert Stojnic, Sergey Edunov, and Thomas Scialom. Llama 2: Open foundation and finetuned chat models, 2023. URL https://arxiv.org/ abs/2307.09288. 1, 2, 3 

- [8] Sombit Dey, Jan-Nico Zaech, Nikolay Nikolov, Luc Van Gool, and Danda Pani Paudel. Revla: Reverting visual domain limitation of robotic foundation models, 2024. URL https://arxiv.org/abs/2409.15250. 1, 2, 4, 5 

- [9] Shresth Grover, Akshay Gopalkrishnan, Bo Ai, Henrik I. Christensen, Hao Su, and Xuanlin Li. Enhancing generalization in vision-language-action models by preserving pretrained representations, 2025. URL https://arxiv. org/abs/2509.11417. 1, 2, 4, 5 

- [10] Junjiao Tian, Xiaoliang Dai, Chih-Yao Ma, Zecheng He, 

32459 

Yen-Cheng Liu, and Zsolt Kira. Trainable projected gradient method for robust fine-tuning, 2023. URL https: //arxiv.org/abs/2303.10720. 1, 2, 3 

- [11] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, Mahmoud Assran, Nicolas Ballas, Wojciech Galuba, Russell Howes, Po-Yao Huang, Shang-Wen Li, Ishan Misra, Michael Rabbat, Vasu Sharma, Gabriel Synnaeve, Hu Xu, Herv´e Jegou, Julien Mairal, Patrick Labatut, Armand Joulin, and Piotr Bojanowski. Dinov2: Learning robust visual features without supervision, 2024. URL https://arxiv.org/ abs/2304.07193. 2, 4 

- [12] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training, 2023. URL https://arxiv.org/abs/2303.15343. 2, 3 

- [13] Junjiao Tian, Chengyue Huang, and Zsolt Kira. Rethinking weight decay for robust fine-tuning of foundation models, 2024. URL https://arxiv.org/abs/2411.01713. 2, 3 

- [14] Xuhong Li, Yves Grandvalet, and Franck Davoine. Explicit inductive bias for transfer learning with convolutional networks, 2018. URL https://arxiv.org/abs/1802. 01483. 3 

- [15] Junjiao Tian, Yen-Cheng Liu, James Seale Smith, and Zsolt Kira. Fast trainable projection for robust fine-tuning, 2023. URL https://arxiv.org/abs/2310.19182. 2, 3, 

   - 6 

- [16] Henry Gouk, Eibe Frank, Bernhard Pfahringer, and Michael J. Cree. Regularisation of neural networks by enforcing lipschitz continuity, 2020. URL https:// arxiv.org/abs/1804.04368. 2 

- [17] Suneel Belkhale and Dorsa Sadigh. Minivla: A better vla with a smaller footprint, 2024. URL https://github. com/Stanford-ILIAD/openvla-mini. 2, 4, 6, 7, 8, 1 

- [18] Seungjae Lee, Yibin Wang, Haritheja Etukuru, H. Jin Kim, Nur Muhammad Mahi Shafiullah, and Lerrel Pinto. Behavior generation with latent actions, 2024. URL https: //arxiv.org/abs/2403.03181. 2, 1 

- [19] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success, 2025. URL https://arxiv.org/abs/2502. 19645. 2, 3, 6, 7, 1 

- [20] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea Finn, Hao Su, Quan Vuong, and Ted Xiao. Evaluating realworld robot manipulation policies in simulation, 2024. URL https://arxiv.org/abs/2405.05941. 2, 6 

- [21] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks, 2022. URL https://arxiv.org/abs/ 2112.03227. 2, 6 

- [22] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking 

knowledge transfer for lifelong robot learning, 2023. URL https://arxiv.org/abs/2306.03310. 2, 6 

- [23] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. Learning transferable visual models from natural language supervision, 2021. URL https://arxiv.org/abs/2103.00020. 2 

- [24] Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, Yevgen Chebotar, Pierre Sermanet, Daniel Duckworth, Sergey Levine, Vincent Vanhoucke, Karol Hausman, Marc Toussaint, Klaus Greff, Andy Zeng, Igor Mordatch, and Pete Florence. Palm-e: An embodied multimodal language model, 2023. URL https://arxiv.org/abs/ 2303.03378. 2 

- [25] Embodiment Collaboration, Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, Albert Tung, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anchit Gupta, Andrew Wang, Andrey Kolobov, Anikait Singh, Animesh Garg, Aniruddha Kembhavi, Annie Xie, Anthony Brohan, Antonin Raffin, Archit Sharma, Arefeh Yavary, Arhan Jain, Ashwin Balakrishna, Ayzaan Wahid, Ben Burgess-Limerick, Beomjoon Kim, Bernhard Sch¨olkopf, Blake Wulfe, Brian Ichter, Cewu Lu, Charles Xu, Charlotte Le, Chelsea Finn, Chen Wang, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine Chan, Christopher Agia, Chuer Pan, Chuyuan Fu, Coline Devin, Danfei Xu, Daniel Morton, Danny Driess, Daphne Chen, Deepak Pathak, Dhruv Shah, Dieter B¨uchler, Dinesh Jayaraman, Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Ethan Foster, Fangchen Liu, Federico Ceola, Fei Xia, Feiyu Zhao, Felipe Vieira Frujeri, Freek Stulp, Gaoyue Zhou, Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Gilbert Feng, Giulio Schiavi, Glen Berseth, Gregory Kahn, Guangwen Yang, Guanzhi Wang, Hao Su, Hao-Shu Fang, Haochen Shi, Henghui Bao, Heni Ben Amor, Henrik I Christensen, Hiroki Furuta, Homanga Bharadhwaj, Homer Walke, Hongjie Fang, Huy Ha, Igor Mordatch, Ilija Radosavovic, Isabel Leal, Jacky Liang, Jad Abou-Chakra, Jaehyung Kim, Jaimyn Drake, Jan Peters, Jan Schneider, Jasmine Hsu, Jay Vakil, Jeannette Bohg, Jeffrey Bingham, Jeffrey Wu, Jensen Gao, Jiaheng Hu, Jiajun Wu, Jialin Wu, Jiankai Sun, Jianlan Luo, Jiayuan Gu, Jie Tan, Jihoon Oh, Jimmy Wu, Jingpei Lu, Jingyun Yang, Jitendra Malik, Jo˜ao Silv´erio, Joey Hejna, Jonathan Booher, Jonathan Tompson, Jonathan Yang, Jordi Salvador, Joseph J. Lim, Junhyek Han, Kaiyuan Wang, Kanishka Rao, Karl Pertsch, Karol Hausman, Keegan Go, Keerthana Gopalakrishnan, Ken Goldberg, Kendra Byrne, Kenneth Oslund, Kento Kawaharazuka, Kevin Black, Kevin Lin, Kevin Zhang, Kiana Ehsani, Kiran Lekkala, Kirsty Ellis, Krishan Rana, Krishnan Srinivasan, Kuan Fang, Kunal Pratap Singh, Kuo-Hao Zeng, Kyle Hatch, Kyle Hsu, Laurent Itti, Lawrence Yunliang Chen, Lerrel Pinto, Li FeiFei, Liam Tan, Linxi ”Jim” Fan, Lionel Ott, Lisa Lee, Luca 

32460 

Weihs, Magnum Chen, Marion Lepert, Marius Memmel, Masayoshi Tomizuka, Masha Itkina, Mateo Guaman Castro, Max Spero, Maximilian Du, Michael Ahn, Michael C. Yip, Mingtong Zhang, Mingyu Ding, Minho Heo, Mohan Kumar Srirama, Mohit Sharma, Moo Jin Kim, Muhammad Zubair Irshad, Naoaki Kanazawa, Nicklas Hansen, Nicolas Heess, Nikhil J Joshi, Niko Suenderhauf, Ning Liu, Norman Di Palo, Nur Muhammad Mahi Shafiullah, Oier Mees, Oliver Kroemer, Osbert Bastani, Pannag R Sanketi, Patrick ”Tree” Miller, Patrick Yin, Paul Wohlhart, Peng Xu, Peter David Fagan, Peter Mitrano, Pierre Sermanet, Pieter Abbeel, Priya Sundaresan, Qiuyu Chen, Quan Vuong, Rafael Rafailov, Ran Tian, Ria Doshi, Roberto Mart´ın-Mart´ın, Rohan Baijal, Rosario Scalise, Rose Hendrix, Roy Lin, Runjia Qian, Ruohan Zhang, Russell Mendonca, Rutav Shah, Ryan Hoque, Ryan Julian, Samuel Bustamante, Sean Kirmani, Sergey Levine, Shan Lin, Sherry Moore, Shikhar Bahl, Shivin Dass, Shubham Sonawani, Shubham Tulsiani, Shuran Song, Sichun Xu, Siddhant Haldar, Siddharth Karamcheti, Simeon Adebola, Simon Guist, Soroush Nasiriany, Stefan Schaal, Stefan Welker, Stephen Tian, Subramanian Ramamoorthy, Sudeep Dasari, Suneel Belkhale, Sungjae Park, Suraj Nair, Suvir Mirchandani, Takayuki Osa, Tanmay Gupta, Tatsuya Harada, Tatsuya Matsushima, Ted Xiao, Thomas Kollar, Tianhe Yu, Tianli Ding, Todor Davchev, Tony Z. Zhao, Travis Armstrong, Trevor Darrell, Trinity Chung, Vidhi Jain, Vikash Kumar, Vincent Vanhoucke, Vitor Guizilini, Wei Zhan, Wenxuan Zhou, Wolfram Burgard, Xi Chen, Xiangyu Chen, Xiaolong Wang, Xinghao Zhu, Xinyang Geng, Xiyuan Liu, Xu Liangwei, Xuanlin Li, Yansong Pang, Yao Lu, Yecheng Jason Ma, Yejin Kim, Yevgen Chebotar, Yifan Zhou, Yifeng Zhu, Yilin Wu, Ying Xu, Yixuan Wang, Yonatan Bisk, Yongqiang Dou, Yoonyoung Cho, Youngwoon Lee, Yuchen Cui, Yue Cao, Yueh-Hua Wu, Yujin Tang, Yuke Zhu, Yunchu Zhang, Yunfan Jiang, Yunshuang Li, Yunzhu Li, Yusuke Iwasawa, Yutaka Matsuo, Zehan Ma, Zhuo Xu, Zichen Jeff Cui, Zichen Zhang, Zipeng Fu, and Zipeng Lin. Open x-embodiment: Robotic learning datasets and rt-x models, 2025. URL https: //arxiv.org/abs/2310.08864. 2 

- [26] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. URL https://arxiv.org/abs/2504. 16054. 

- [27] Danny Driess, Jost Tobias Springenberg, Brian Ichter, Lili Yu, Adrian Li-Bell, Karl Pertsch, Allen Z. Ren, Homer Walke, Quan Vuong, Lucy Xiaoyang Shi, and Sergey Levine. Knowledge insulating vision-language-action models: Train fast, run fast, generalize better, 2025. URL https:// 

arxiv.org/abs/2505.23705. 2 

- [28] Andrew Szot, Bogdan Mazoure, Harsh Agrawal, R Devon Hjelm, Zsolt Kira, and Alexander Toshev. Grounding multimodal large language models in actions. _Advances in Neural Information Processing Systems_ , 37:20198–20224, 2024. 2 

- [29] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models, 2025. URL https://arxiv. org/abs/2501.09747. 3, 6 

- [30] Suneel Belkhale, Tianli Ding, Ted Xiao, Pierre Sermanet, Quon Vuong, Jonathan Tompson, Yevgen Chebotar, Debidatta Dwibedi, and Dorsa Sadigh. Rt-h: Action hierarchies using language, 2024. URL https://arxiv.org/ abs/2403.01823. 

- [31] Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware, 2023. URL https://arxiv.org/ abs/2304.13705. 

- [32] Moritz Reuss, Hongyi Zhou, Marcel R¨uhle, Omer<sup>¨</sup> Erdinc¸ Ya˘gmurlu, Fabian Otto, and Rudolf Lioutikov. FLOWER: Democratizing generalist robot policies with efficient visionlanguage-flow models. In _9th Annual Conference on Robot Learning_ , 2025. URL https://openreview.net/ forum?id=JeppaebLRD. 2 

- [33] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, Simon Alibert, Matthieu Cord, Thomas Wolf, and Remi Cadene. Smolvla: A vision-language-action model for affordable and efficient robotics, 2025. URL https://arxiv. org/abs/2506.01844. 2 

- [34] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, Yaxin Peng, Feifei Feng, and Jian Tang. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation, 2025. URL https://arxiv.org/abs/ 2409.12514. 2 

- [35] Zhongyi Zhou, Yichen Zhu, Minjie Zhu, Junjie Wen, Ning Liu, Zhiyuan Xu, Weibin Meng, Ran Cheng, Yaxin Peng, Chaomin Shen, and Feifei Feng. Chatvla: Unified multimodal understanding and robot control with visionlanguage-action model, 2025. URL https://arxiv. org/abs/2502.14420. 2 

- [36] Zhongyi Zhou, Yichen Zhu, Junjie Wen, Chaomin Shen, and Yi Xu. Chatvla-2: Vision-language-action model with open-world embodied reasoning from pretrained knowledge, 2025. URL https://arxiv.org/abs/2505. 21906. 

- [37] Lucy Xiaoyang Shi, Brian Ichter, Michael Equi, Liyiming Ke, Karl Pertsch, Quan Vuong, James Tanner, Anna Walling, Haohuan Wang, Niccolo Fusai, Adrian Li-Bell, Danny Driess, Lachy Groom, Sergey Levine, and Chelsea Finn. Hi robot: Open-ended instruction following with hierarchical vision-language-action models, 2025. URL https://arxiv.org/abs/2502.19417. 

- [38] Jason Lee, Jiafei Duan, Haoquan Fang, Yuquan Deng, Shuo Liu, Boyang Li, Bohan Fang, Jieyu Zhang, Yi Ru Wang, 

32461 

Sangho Lee, Winson Han, Wilbert Pumacay, Angelica Wu, Rose Hendrix, Karen Farley, Eli VanderBilt, Ali Farhadi, Dieter Fox, and Ranjay Krishna. Molmoact: Action reasoning models that can reason in space, 2025. URL https: //arxiv.org/abs/2508.07917. 

- [39] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, and Xuelong Li. Spatialvla: Exploring spatial representations for visual-language-action model, 2025. URL https://arxiv.org/abs/2501.15830. 

- [40] Yang Tian, Sizhe Yang, Jia Zeng, Ping Wang, Dahua Lin, Hao Dong, and Jiangmiao Pang. Predictive inverse dynamics models are scalable learners for robotic manipulation, 2024. URL https://arxiv.org/abs/2412.15109. 

- [41] Andrew Szot, Bogdan Mazoure, Omar Attia, Aleksei Timofeev, Harsh Agrawal, Devon Hjelm, Zhe Gan, Zsolt Kira, and Alexander Toshev. From multimodal llms to generalist embodied agents: Methods and lessons. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 10644–10655, 2025. 2 

- [42] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, Ankur Handa, Ming-Yu Liu, Donglai Xiang, Gordon Wetzstein, and Tsung-Yi Lin. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models, 2025. URL https://arxiv.org/abs/2503. 22020. 2 

- [43] Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning, 2025. URL https: //arxiv.org/abs/2407.08693. 

- [44] Junjie Wen, Minjie Zhu, Yichen Zhu, Zhibin Tang, Jinming Li, Zhongyi Zhou, Chengmeng Li, Xiaoyu Liu, Yaxin Peng, Chaomin Shen, and Feifei Feng. Diffusion-vla: Generalizable and interpretable robot foundation model via selfgenerated reasoning, 2025. URL https://arxiv.org/ abs/2412.03293. 2 

- [45] Ji Zhang, Shihan Wu, Xu Luo, Hao Wu, Lianli Gao, Heng Tao Shen, and Jingkuan Song. Inspire: Visionlanguage-action models with intrinsic spatial reasoning, 2025. URL https://arxiv.org/abs/2505.13888. 2 

- [46] Asher J. Hancock, Xindi Wu, Lihan Zha, Olga Russakovsky, and Anirudha Majumdar. Actions as language: Fine-tuning vlms into vlas without catastrophic forgetting, 2025. URL https://arxiv.org/abs/2509.22195. 2 

- [47] Huang Huang, Fangchen Liu, Letian Fu, Tingfan Wu, Mustafa Mukadam, Jitendra Malik, Ken Goldberg, and Pieter Abbeel. Otter: A vision-language-action model with text-aware visual feature extraction, 2025. URL https: //arxiv.org/abs/2503.03734. 2 

- [48] Nikita Kachaev, Mikhail Kolosov, Daniil Zelezetsky, Alexey K. Kovalev, and Aleksandr I. Panov. Don’t blind your vla: Aligning visual representations for ood generalization, 2025. URL https://arxiv.org/abs/2510.25616. 2, 4 

Chen, Kai Chen, Qi Dou, Yaodong Yang, Xianglong Liu, Huijie Zhao, Weifeng Lv, and Simin Li. On robustness of vision-language-action model against multi-modal perturbations, 2025. URL https://arxiv.org/abs/2510. 00037. 2 

   - [50] Chengyue Huang, Junjiao Tian, Brisa Maneechotesuwan, Shivang Chopra, and Zsolt Kira. Directional gradient projection for robust fine-tuning of foundation models, 2025. URL https://arxiv.org/abs/2502.15895. 3 

   - [51] Chengyue Huang, Brisa Maneechotesuwan, Shivang Chopra, and Zsolt Kira. Frames-vqa: Benchmarking fine-tuning robustness across multi-modal shifts in visual question answering, 2025. URL https://arxiv.org/abs/2505.21755. 3 

   - [52] Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models, 2024. URL https://arxiv.org/ abs/2402.07865. 4 

   - [53] Yihao Wang, Pengxiang Ding, Lingxiao Li, Can Cui, Zirui Ge, Xinyang Tong, Wenxuan Song, Han Zhao, Wei Zhao, Pengxu Hou, Siteng Huang, Yifan Tang, Wenhui Wang, Ru Zhang, Jianyi Liu, and Donglin Wang. Vla-adapter: An effective paradigm for tiny-scale vision-language-action model, 2025. URL https://arxiv.org/abs/2509. 09372. 4, 6, 8, 1, 5 

   - [54] Chia-Yu Hung, Qi Sun, Pengfei Hong, Amir Zadeh, Chuan Li, U-Xuan Tan, Navonil Majumder, and Soujanya Poria. Nora: A small open-sourced generalist vision language action model for embodied tasks, 2025. URL https:// arxiv.org/abs/2504.19854. 6 

   - [55] Jeremiah Coholich, Justin Wit, and Zsolt Kira. Sim2real image translation enables viewpoint-robust policies from fixed-camera datasets. In _Proceedings of the 6th Annual Embodied AI Workshop (EAI) at the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , Nashville, Tennessee, USA, June 2025. URL https: //www.jeremiahcoholich.com/publication/ iros_2025/CVPR_EAI_Workshop_2025.pdf. 6, 2 

   - [56] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy, 2024. URL https://arxiv.org/abs/2405.12213. 7 

   - [57] Cunxin Fan, Xiaosong Jia, Yihang Sun, Yixiao Wang, Jianglan Wei, Ziyang Gong, Xiangyu Zhao, Masayoshi Tomizuka, Xue Yang, Junchi Yan, and Mingyu Ding. Interleave-vla: Enhancing robot manipulation with interleaved image-text instructions, 2025. URL https:// arxiv.org/abs/2505.02152. 7 

- [49] Jianing Guo, Zhenhong Wu, Chang Tu, Yiyao Ma, Xiangqi Kong, Zhiqian Liu, Jiaming Ji, Shuning Zhang, Yuanpei 

32462 

