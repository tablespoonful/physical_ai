---
title: "Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning"
date: "2026-02-07"
authors: "Jingyi Hou; Leyu Zhou; Chenchen Jing; Jinghan Yang; Xinbo Yu; Wei He"
url: https://arxiv.org/abs/2602.07541
pdf: https://arxiv.org/pdf/2602.07541
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.07541)** / [論文ページ](https://arxiv.org/abs/2602.07541)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

**Jingyi Hou**<sup>1</sup> **Leyu Zhou**<sup>1</sup> **Chenchen Jing**<sup>2</sup> **Jinghan Yang**<sup>1</sup> **Xinbo Yu**<sup>1</sup> **Wei He**<sup>1 3</sup> 

## **Abstract** 

As robots are expected to perform increasingly diverse tasks, they must understand not only lowlevel actions but also the higher-level structure that determines how a task should unfold. Existing vision-language-action (VLA) models struggle with this form of task-level reasoning. They either depend on prompt-based in-context decomposition, which is unstable and sensitive to linguistic variations, or end-to-end long-horizon training, which requires large-scale demonstrations and entangles task-level reasoning with lowlevel control. We present in-parameter Structured <u>TAsk Reasoning</u> (iSTAR), a framework for enhancing VLA models via functional differentiation induced by in-parameter structural reasoning. Instead of treating VLAs as monolithic policies, iSTAR embeds task-level semantic structure directly into model parameters, enabling differentiated task-level inference without external planners or handcrafted prompt inputs. This injected structure takes the form of implicit dynamic scenegraph knowledge that captures object relations, subtask semantics, and task-level dependencies in parameter space. Across diverse manipulation benchmarks, iSTAR achieves more reliable task decompositions and higher success rates than both in-context and end-to-end VLA baselines, demonstrating the effectiveness of parameter-space structural reasoning for functional differentiation and improved generalization across task variations. 

## **1. Introduction** 

Vision-language-action (VLA) models have emerged as a powerful paradigm for grounding natural language instructions in perception and control, enabling robots to perform a wide range of manipulation tasks (Jiang et al., 2023; Kim 

1University of Science and Technology Beijing 2Zhejiang University of Technology<sup>3</sup> Beijing Information Science and Technology University. 

_Preprint. February 10, 2026._ 


_Figure 1._ Our iSTAR transitions from a monolithic VLA with entangled reasoning to functionally differentiated modules where task-level structure (dynamic scene graphs) is injected into the model parameters. By the semantic-guided task resolution, iSTAR enhances the long-horizon reliability of VLA while maintaining end-to-end execution. 

et al., 2024; Shridhar et al., 2022). Despite their success, most existing VLAs are used in a monolithic manner, where task-level reasoning and action execution are implicitly entangled within a single inference process. For long-horizon and procedurally constrained tasks, this coupling becomes a potential limitation, as errors in high-level reasoning can directly propagate into low-level control. Therefore, beyond simply scaling models or data, improving VLAs requires rethinking how their internal capabilities are organized. 

Recent efforts to improve the reasoning ability of VLAs can be understood as introducing additional reasoning signals through in-context mechanisms. A common strategy enriches reasoning through language (Ichter et al., 2022; Singh et al., 2023) or multimodal interaction (Kim et al., 2025; Huang et al., 2025; Black et al., 2025), allowing models to reason about goals or task structure for action generation. While effective at guiding high-level intent, these reasoning processes rely primarily on prompt-based reasoning, rather than directly engaging with the action representations that govern physical execution. As a result, task-level decisions are only indirectly reflected in action generation, making performance highly sensitive to how explicitly the instruction specifies task structure. Other methods (Zhao et al., 2025; Ni et al., 2024) perform reasoning in visual spaces to model object relations and temporal structure more explicitly. Although visual representations can faithfully capture 

1 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

physical scenes, reasoning within such high-dimensional manifolds is computationally demanding, making it less efficient to distill and manipulate the task-relevant structure needed for action execution. Consequently, there is a lack of a reusable mechanism for resolving and reusing task-level semantic structure at the level where actions are actually generated. 

This perspective leads to the question of how a monolithic VLA can be enhanced to explicitly resolve task-level structure while preserving end-to-end action generation. A closer look reveals that, although modern VLAs inherit strong reasoning capabilities from their vision–language components, such capabilities are often underutilized when task understanding and action execution are entangled within a single inference process. In this work, we argue that enhancing VLAs requires a different design principle— _functional differentiation induced by in-parameter structural reasoning_ , as illustrated in Figure 1. We differentiate the functional roles of a single VLA by embedding task-level semantic structure directly into its parameters without introducing external planners or separating reasoning and control into distinct models. This enables task-level reasoning to be resolved explicitly and reused during inference, while preserving the expressive capacity of end-to-end VLA models. 

Guided by this principle, we introduce <u>in-parameter Structured TAsk Reasoning (iSTAR), a framework that re-</u> alizes functional differentiation through in-parameter structural reasoning. iSTAR injects implicit and dynamic scenegraph knowledge into model parameters, capturing objectcentric relations, subtask semantics, and task-phase dependencies in a form that can be reused across task instances. This structural knowledge is distilled from vision-language models (VLMs) that observes task execution videos and produces subtask-level semantic descriptions, which are then used to guide the learning of dynamic scene structure within the VLA. By internalizing such distilled structure, iSTAR resolves task-level reasoning to improve the reliability and generalization of long-horizon behavior without relying on handcrafted prompts and external planners. Experiments across diverse manipulation benchmarks demonstrate that iSTAR consistently outperforms prompt-based and end-toend VLA baselines, highlighting in-parameter structural reasoning as a principled mechanism for enhancing VLA models.<sup>1</sup> 

## **2. Related Work** 

Robot manipulation planning has traditionally been studied under hierarchical task and motion planning (TAMP), which decomposes long-horizon tasks into symbolic tasklevel decisions and continuous motion generation (Kaelbling 

> 1Our code is available at https://github.com/ hugezhuwo/iSTAR_code. 

& Lozano-Perez´ , 2011). Learning-based extensions incorporate visual perception and neural representations to improve robustness and scalability (Zhu et al., 2021), but typically rely on predefined task structure. With the emergence of LLMs, recent work explores language-driven planning for robotic manipulation. Methods such as SayCan (Ichter et al., 2022) and ProgPrompt (Singh et al., 2023) generate highlevel action sequences from natural language, while related approaches translate instructions into symbolic plans (Zhou et al., 2024; Guo et al., 2024). In these methods, task-level reasoning is generally externalized and executed separately from action generation. 

More recently, end-to-end VLA models (Jiang et al., 2023; Kim et al., 2024; Black et al., 2025; Shridhar et al., 2022; Fu et al., 2025) encode planning implicitly within action prediction, with recent work further studying post-training or online improvement of such policies (Wagenmaker et al., 2025). While effective at scale, this monolithic formulation tightly entangles task-level reasoning with low-level control in latent action spaces, making it difficult to isolate and reuse task-level structure across task compositions and long-horizon variations. Hierarchical VLA approaches introduce intermediate representations to decompose planning and execution (Shi et al., 2025; Li et al., 2025b; Dalal et al., 2024; Chen et al., 2025; Zhao et al., 2025; Ni et al., 2024). These methods relieve high-level models from finegrained control, but their intermediate representations are usually limited to paths, poses, or visual subgoals, which makes it difficult to capture compositional semantic structure. Related work further explores efficient control via architectural (Zhang et al., 2026) or modality augmentation (Yu et al., 2025). OpenVLA-OFT (Kim et al., 2025) improves task performance by parameter-efficiently finetuning a VLA with visual reasoning (Perez et al., 2018). By explicitly resolving and reusing task-level semantic structure _in parameter space_ , iSTAR provides a principled pathway toward systematic compositional generalization in longhorizon vision-language-action tasks. 

## **3. Method** 

Motivated by the limitations of monolithic VLAs discussed above, the core goal of iSTAR is to explicitly resolve tasklevel semantic structure before action execution, while keeping such reasoning internal to the model parameters and compatible with end-to-end VLA inference. To this end, iSTAR introduces functional differentiation within a pretrained VLA by assigning distinct roles to different instances of the same backbone. Specifically, one instance operates on the VLA backbone before the action head (the _pre-action VLA module_ ) to perform semantic concept reasoning, while another instance is used for action generation conditioned on the resolved task structure. Figure 2 illustrates an overview 

2 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 


_Figure 2._ Overview of the proposed iSTAR framework. 

of this differentiated inference structure. 

Given a multimodal instruction _c_ and visual observations _I_ , iSTAR first extracts object- and action-centric concept representations from the pre-action VLA module. To guide these representations toward task-relevant semantic reasoning, we inject dynamic concept-graph structure into this module, enabling structured reasoning among concepts and enriching concept representations that capture the semantics required for the current task stage. These structure-aware concept representations are then mapped to subtask-level textual descriptions (subprompts), which serve as explicit semantic commitments. Conditioned on these subtask descriptions as prompt embeddings, the action-generating VLA solves a simplified short-horizon decision problem. Overall, iSTAR decomposes a monolithic VLA inference process into differentiated concept reasoning and action execution stages, while keeping both stages within the same VLA parameter family and without introducing external planners. 

### **3.1. Concept Extraction** 

Our iSTAR uses the pre-action VLA module to perform semantic concept reasoning. This module is responsible for extracting object- and action-centric representations that summarize the task-relevant semantics at each stage. Given a task instruction _c_ and a sequence of visual observations _I_ = _{It}_<sup>_T_</sup> _t_ =1<sup>,wemaintainateachtimestep</sup><sup>_t_anobject</sup> embedding _ot_ derived from the current observation and an action embedding _at−_ 1 carried over from the previous step. These embeddings are processed by a multimodal autoregressive encoder, i.e., the pre-action VLA module, 

producing object- and action-centric concept embeddings 


where _at−_ 1 = 0 for _t_ = 1 and equals the previous action concept _vt_<sup>act</sup> _−_ 1<sup>for</sup><sup>_t>_1.Theresulting</sup><sup>_v_</sup> _t_<sup>obj</sup> remains an object-centric representation grounded in the current observation, while _vt_<sup>act</sup> encodes a high-level action intent inferred at timestep _t_ . The autoregressive loop is closed by feeding _vt_<sup>act</sup> forward as _at_ for the next step, allowing concept representations to evolve coherently across timesteps. Collecting all concept embeddings yields the node set 


which constitutes the semantic concept set over which iSTAR performs in-parameter structural reasoning. This set serves as the input to the dynamic implicit concept graph module described in Section 3.2. For clarity, unless otherwise specified, we assume all concept representations correspond to the current timestep, and the explicit time index _t_ is omitted in the following discussion. 

### **3.2. Dynamic Implicit Concept Graph Construction** 

Given the concept set _V_ = _{v_ 1 _, . . . , vN }_ , the goal of the implicit dynamic graph module is to infer the task-level structure that determines which objects and action cues are relevant for the current subtask, as well as how these concepts interact temporally and relationally. 

**Attribute gating.** To select concepts relevant to the current subtask, each node is modulated by an attribute gate: 


3 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

This operation suppresses dimensions unrelated to the underlying task semantics and highlights candidate objects and action cues. 

**Dynamic positional encoding.** Temporal structure across subtasks is modeled through a recurrent state that accumulates information across decoding steps: 


Unlike static positional encodings, these representations evolve with the inferred subtask sequence and capture temporal ordering cues. 

**Order gating and fusion.** To refine temporal relevance, a second gate modulates the positional representation: 


The gated representations are then fused with the attributefiltered nodes: 


The resulting node states encode both object relevance and temporal phase information. 

**Implicit relational reasoning.** Relational structure is captured through multi-head attention, optionally incorporating edge-level representations when available: 


where _E_<sup>(fused)</sup> denotes optional edge embeddings (if provided). The resulting attention patterns implement latent message passing within the implicit concept graph. 

**Structure-learning objective.** Let _pt_ denote the subtask description at decoding step _t_ , represented either as a textual embedding or a multimodal prompt embedding depending on the downstream VLA interface. To guide the implicit graph toward task-relevant structure, we introduce an auxiliary objective that aligns concept relevance with subtask semantics while maintaining uncertainty over temporal ordering: 


The first term encourages the gated concept representations _v_ ˜ _i_ to align with the semantic content of the current subtask, promoting correct object and action selection. The second 

term regularizes the entropy of the order gate, preventing premature commitment to a fixed temporal structure and allowing the model to explore multiple plausible subtask orderings during learning. 

### **3.3. Subtask Prompt Projector** 

After dynamic structural reasoning, the fused concept representations _V_<sup>(fused)</sup> = _{v_ 1<sup>(fused)</sup> _, . . . , vN_<sup>(fused)</sup> _}_ encode object relevance, temporal phase, and relational context for the current subtask. The subtask prompt projector maps these structure-aware semantic representations to subtasklevel language space that serves as semantic commitment for downstream action generation. 

In fact, the projector acts more like a _semantic embedding mapper_ , translating representations from the semantic concept space into the language embedding space expected by the downstream VLA. Since subtask prompts correspond to short, structurally constrained intents, the projection can be implemented in either a non-autoregressive or autoregressive manner in embedding space, without encountering the challenges of long-form language modeling. The resulting subtask embedding is used to condition the actiongenerating VLA, reducing the burden of long-horizon semantic reasoning during action decoding. 

### **3.4. Subtask Prompt Distillation and Supervision** 

Most VLA datasets do not provide explicit subtask-level prompts, but they do include step-wise visual observations aligned with action trajectories. We leverage this property to construct subtask prompt supervision via online language model distillation without additional manual annotation. For each subtask step, we collect several textual descriptions from a powerful VLM of the task context, which is used as supervision for training the subtask prompt decoder. This enables the decoder to learn a compact subtask-level description aligned with the underlying execution, while remaining agnostic to the full multimodal input. 

For VIMA-Bench, where prompts are inherently multimodal, we first obtain descriptions with placeholders and then ground them using the provided action trajectories and object segmentation annotations. Object masks and spatial references are recovered from the dataset annotations, allowing reconstruction of multimodal subtask prompts compatible with token-based VLAs such as VIMA. 

## **4. Theory and Extensions** 

The empirical gains observed in real-world tasks suggest that explicitly modeling semantic commitment before action decoding improves generalization. In this section, we formalize this intuition and analyze why structured seman- 

4 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

tic reasoning yields advantages in large-horizon and lowinformation regimes. 

### **4.1. Structured Advantage in the Large-Horizon Regime** 

We consider a structured policy _π_ ˆ = ( _f,_<sup>ˆ</sup> ˆ _r, h_<sup>ˆ</sup> ), which first predicts a semantic graph _G_<sup>ˆ</sup> _t_ , realizes it into a subprompt _p_ ˆ _t_ , and then decodes a one-step action _at ∼ h_<sup>ˆ</sup> ( _· | It,_ ˆ _pt_ ). We compare it to an end-to-end policy _π_ ˆe2e that directly predicts discrete action tokens _at ∈A_ . 

Assume the expert policy admits latent semantic witnesses ( _G_<sup>_∗_</sup> _t_<sup>_, p_</sup> _t_<sup>_∗_)suchthattheexpertactiondistributionsatisfies</sup> _a_<sup>_∗_</sup> _t_<sup>_∼h∗_(</sup><sup>_·|It, p_</sup> _t_<sup>_∗_),where</sup><sup>_p∗_</sup> _t_<sup>=</sup><sup>_r∗_(</sup><sup>_G_</sup> _t_<sup>_∗_).Understan-</sup> dard performance sensitivity arguments, according to standard analyses in imitation learning and structured prediction (Ross & Bagnell, 2010; Ross et al., 2011), the performance gap of the structured policy admits the decomposition _J_ ( _π_<sup>_∗_</sup> ) _− J_ (ˆ _π_ ) _≤ Ca ϵa_ + _Cr ϵr_ + _CG ϵG,_ (8) 

where _ϵa_ denotes the one-step action decoding error under the correct semantic commitment, _ϵr_ denotes the realization error from semantic graph to subprompt, and _ϵG_ denotes the semantic graph prediction error. 

Conditioned on the correct semantic commitment, action decoding reduces to a one-step supervised learning problem, so _ϵa_ does not require modeling long-horizon dependencies. If the realization step is implemented via constrained templates or grammar, _ϵr_ is bounded and can be treated as a lower-order term. As a result, the dominant contribution arises from _ϵG_ . 

**Proposition 4.1** (Structured advantage for large horizons) **.** _Consider discrete action tokens at ∈A. Suppose the effective complexity of semantic commitment over a horizon T scales as_ 


_while an end-to-end policy predicting action tokens induces_ 


_If_ log _|C| <_ log _|A| and the supervision budgets are of the same order, then there exists T_ 0 _such that for all T ≥ T_ 0 _, the generalization bound of the structured policy is strictly tighter than that of the end-to-end policy._ 

**Proof Sketch.** We outline the main steps of the comparison; full proofs are provided in Appendix A. 

We begin by bounding the structured policy. Using the decomposition in Eq. (8), the global performance gap is reduced to the sum of three terms corresponding to action decoding, realization, and semantic graph prediction. The first two terms are well-conditioned: conditioned on the correct semantic commitment _p_<sup>_∗_</sup> _t_<sup>, the action decoder only needs</sup> 

to model a one-step conditional distribution ( _It, p_<sup>_∗_</sup> _t_<sup>)</sup><sup>_�→a∗_</sup> _t_<sup>,</sup> and therefore its generalization behavior does not scale with the task horizon. Similarly, when the realization from graph to subprompt is implemented via templates or constrained grammar, the induced realization error remains bounded and does not accumulate over time. 

The remaining term, _ϵG_ , captures the difficulty of predicting semantic commitments. Applying standard uniform convergence arguments to the semantic graph predictor yields a bound of the form 


where � _ϵG_ is the empirical graph prediction error and _nG_ is the number of supervised graph samples. Substituting this bound into Eq. (8) and absorbing horizon-independent terms gives an overall structured bound whose leading term scales as ~~�~~ _T_ log _|C|_ . 

For the end-to-end policy, directly predicting a length- _T_ sequence of discrete action tokens induces an effective output space of size _|A|_<sup>_T_</sup> . As a result, standard complexity-based generalization arguments yield a bound whose leading term scales as ~~�~~ _T_ log _|A|_ . 

Since log _|C| <_ log _|A|_ , the dominant term of the structured bound grows strictly more slowly than that of the end-toend bound. Moreover, as analyzed above, the remaining two error components of the structured policy ( _ϵr_ and _ϵa_ ) are horizon-insensitive and therefore do not accumulate as the task horizon increases. Consequently, there exists a horizon length _T_ 0 such that for all _T ≥ T_ 0, the structured policy admits a strictly tighter generalization bound than the end-to-end policy. □ 

To complete the argument in Proposition 4.1, we briefly explain why the condition log _|C| <_ log _|A|_ holds in practice. The semantic commitment space _C_ is constructed from a set of discrete semantic attributes, 


Crucially, a semantic commitment is specified by selecting one value for each attribute, so _C_ scales as 


This reflects that semantic graphs encode abstract attributes (e.g., object identity, relations, constrains) whose contributions accumulate additively. The multiplicative space � _k_<sup>_|Ck|_can be viewed as a discrete combinatorial abstrac-</sup> tion of executable behaviors, but it is already a simplification of the true action space _A_ . In practice, _A_ represents lowlevel physical control and is typically a discretization of a 

5 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

high-dimensional continuous space. Its effective complexity therefore grows with both control dimensionality and resolution, far exceeding that of the semantic space. Consequently, the complexity of the semantic commitment space is much smaller than that of the action space, justifying the regime 

log _|C| ≪_ log _|A|_ 

### assumed in Proposition 4.1. 

### **4.2. Advantage in the Low-Information Regime** 

Beyond long-horizon execution, structured decomposition is also advantageous in tasks with low perceptual information but high semantic reasoning demands, such as relational instructions (e.g., “place all objects with the same shape as X into the bowl”) or procedural tasks (e.g., making a cup of coffee). In such regimes, the challenge lies not in action execution but in resolving semantic ambiguity under weak supervision. This difficulty has been widely observed in sequence-to-sequence models, which often succeed at surface-level generalization but fail when correct behavior requires extracting and systematically applying abstract compositional rules rather than exploiting latent statistical correlations (e.g., Lake & Baroni, 2018). Our method resolves this ambiguity at the semantic level, enabling systematic reuse of abstract rules and yielding improved compositional generalization under limited perceptual information. 

### **4.3. Extending iSTAR beyond VIMA** 

Although Section 3 uses VIMA as an example, iSTAR is architecture-agnostic and can be applied to a broad range of VLA backbones. The only requirement is access to intermediate representations before the action head, from which task-relevant semantic information can be extracted. VIMA is used for illustration due to its explicit multimodal token structure and the suitability of VIMA-Bench for evaluating task-level reasoning. 

For decoder-based VLAs, iSTAR follows the same principle by operating on backbone representations before the action head to produce structure-aware subtask embeddings. For large-scale VLAs, subtask embeddings can be extracted from higher-level hidden states close to the action head, avoiding excessive reuse of lower-level features and unnecessary parameter growth. 

diverse task and object configurations. These benchmarks emphasize grounding language instructions in visual scenes, handling object relations, spatial arrangements, and longhorizon execution under standardized task formulations, enabling controlled comparisons with prior work. 

While benchmark evaluations focus on visual grounding and execution under fixed task specifications, they provide limited coverage of task-level generalization when execution structure must be inferred beyond the given instruction. To complement this, we further conduct real-world robotic experiments that explicitly probe task-level reasoning and generalization. In real-world settings, prompts specify only the desired goal state and omit prerequisite subtasks or execution order, requiring the model to infer execution structure from the current scene. Moreover, real-world execution involves irreversible errors and environmental variability, making it a necessary testbed for evaluating whether task-level semantic structure learned in parameter space can generalize beyond benchmark distributions. 

Together, these experimental settings provide a comprehensive evaluation of visual reasoning, action grounding, and task-level generalization, allowing us to assess the practical effectiveness of in-parameter structural reasoning from simulation to real-world deployment. 

### **5.2. Experiments on VIMA-Bench** 

Experiments on VIMA-Bench organize tasks into 4 levels of increasing difficulty (L1–L4), reflecting progressively more complex compositional structure and longer horizons, following the official task stratification provided by VIMABench. 

To ensure fair comparison, all VIMA-based results reported in this paper are obtained by fine-tuning the official pretrained VIMA models on the task configurations used in our experiments. Detailed task settings and per-task success rates are provided in Appendix E. VIMA provides two backbone configurations with 2M and 4M model sizes, denoted as VIMA (Small) and VIMA (Large), respectively. In our experiments, iSTAR is built upon the VIMA (Small) backbone. Due to the additional structural reasoning components introduced by iSTAR, the total parameter count of iSTAR is comparable to that of the VIMA (Large) model. We therefore report results for both VIMA (Small) and VIMA (Large) as reference baselines. 

## **5. Experiments** 

### **5.1. Experimental Overview** 

We evaluate our method across two public benchmarks and a real-world robotic system, with each setting targeting a complementary aspect of vision-language-action reasoning. VIMA-Bench and LIBERO are designed to assess visual reasoning and perception-conditioned manipulation under 

**iSTAR variants for ablation.** All iSTAR ablation variants share the same backbone and differ only in the components of the dynamic implicit concept graph. Specifically, we evaluate: 

**iSTAR (Stacked VIMA).** This variant tests whether performance gains arise from increased model depth alone, by 

6 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

_Table 1._ Success rate (%) across VIMA-Bench task levels (L1–L4). Best results are in **bold** , second-best are underlined. 

|**Method**|**L1**|**L2**|**L3**|**L4**|
|---|---|---|---|---|
|VIMA (Small)|72.4|73.8|71.1|35.0|
|VIMA (Large)|73.9|74.5|72.0|**59.0**|
|iSTAR (Stacked VIMA)|72.4|73.6|72.4|34.0|
|iSTAR (w/o Graph)|74.8|76.0|74.9|37.7|
|iSTAR (w/o Concept Alignment)|77.8|77.5|77.0|40.0|
|iSTAR (w/o Order Entropy)|76.4|77.6|76.3|42.7|
|iSTAR (Ours)|**78.6**|**79.2**|**78.3**|44.3|


stacking a pre-action VIMA with a frozen pretrained VIMA, without subtask supervision or structural reasoning. 

**iSTAR (w/o Graph).** This variant removes the dynamic implicit graph and all structural losses, while retaining subtask embeddings to condition the action VLA, isolating the effect of subtask-level supervision without explicit structure. 

**iSTAR (w/o Concept Alignment).** This variant retains the implicit graph but removes the concept–subtask alignment term, eliminating explicit supervision of concept relevance. 

**iSTAR (w/o Order Entropy).** This variant retains the implicit graph but removes order entropy regularization, allowing early commitment to a fixed subtask ordering. 

**Result Analysis.** The ablation results in Table 1 highlight the respective roles of intermediate supervision and structural inductive biases in iSTAR. Simply stacking two VIMA backbones without intermediate supervision yields performance comparable to VIMA (Large) at L1-L3 level, indicating that increased model depth alone provides limited benefits. iSTAR (w/o Graph) already leads to noticeable improvements, suggesting that subtask-level supervision provides a strong semantic signal that the VLA backbone can partially exploit. iSTAR (w/o Concept Alignment) and iSTAR (w/o Order Entropy) show higher performance than iSTAR (w/o Graph). While the averaged metrics aggregate tasks of varying difficulty within each level, we observe consistent and non-trivial improvements across all task levels. In particular, the gains become more obvious at higher task levels that involve more objects and longer execution horizons. These results indicate that explicitly supervising concept relations and maintaining uncertainty over subtask ordering are especially effective in complex, long-horizon settings. Overall, the full iSTAR model achieves the best overall performance. 

We further observe that VIMA (Large) exhibits a notably stronger performance on L4. A closer inspection reveals that one task (Task 08, “novel ~~a~~ dj ~~a~~ nd ~~n~~ oun” described in Jiang et al. (2023)) of L4 contains prompts requiring the most complex reasoning over all tasks, such as one-shot 

_Table 2._ Success rate (SR, %) on four task suites. Best results are in **bold** , second-best are underlined. 

|**Method**|**Spatial**|**Object**|**Goal**|**Long**|
|---|---|---|---|---|
|OpenVLA (2024)|84.7|88.4|79.2|53.7|
|_π_0 (2024)|**96.8**|**98.8**|95.8|85.2|
|Evo-1 (2025)|92.7|97.7|**96.3**|**92.3**|
|OpenVLA-OFT (2025)|96.2|98.3|96.2|90.7|
|iSTAR (Ours)|**96.8**|98.4|96.0|92.2|


concept grounding and attribute comparison, which place heavy demands on the vision-language encoding capacity rather than on action generation. This suggests that the observed performance gap is primarily caused by insufficient visual-language encoding capacity, which leads to underfitting on tasks requiring complex multimodal reasoning, rather than deficiencies in task-level reasoning itself. iSTAR is designed to explicitly elicit and organize the reasoning capabilities already present in the underlying VLA, but cannot compensate for missing representational capacity; as a result, while it substantially improves performance over smaller backbones, its effectiveness is ultimately bounded by the model’s intrinsic visual-language reasoning capacity. 

Consistent with this hypothesis, in a supplementary experiment we replace the task-level pre-action VLA with a VIMA large backbone while keeping the rest of iSTAR unchanged (consistent with the 2M backbone), which improves the success rate from 85% to 97%. 

### **5.3. Experiments on LIBERO** 

Table 2 reports success rates on the LIBERO benchmark. Our iSTAR model is built upon the OpenVLA-OFT backbone and follows the same evaluation protocol as prior work: each task is evaluated with 10 trials, repeated 5 runs. 

Overall, iSTAR achieves performance comparable to stateof-the-art VLA models across all four task suites and consistently outperforms its OpenVLA-OFT backbone. The improvement margins are moderate, which we attribute to the characteristics of LIBERO: task instructions are explicit and execution order is largely fixed, leaving limited ambiguity for additional task-level semantic reasoning. Under such conditions, strong end-to-end VLA backbones already perform near saturation. Nevertheless, iSTAR remains competitive on all task suites, including long-horizon tasks, indicating that in-parameter structural reasoning does not hinder end-to-end execution and can be seamlessly integrated with strong VLA backbones even when the benefit of explicit reasoning is less pronounced. 

### **5.4. Real-World Experiments** 

To evaluate whether iSTAR generalizes beyond simulation and benchmark settings, we conduct real-world manipula- 

7 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 


_Figure 3._ Examples of real-world experiments. For each task, the prompt is shown along with the detailed execution stages, from initial state to final completion. 

tion experiments on an industrial robotic platform. These experiments are designed to assess task-level reasoning under realistic control constraints, while minimizing the impact of low-level manipulation difficulty. Following the protocol of OpenVLA-OFT, we fine-tune the model on our UR3 platform for approximately 50-150K steps with an action chunk size _K_ = 25. At inference time, we adopt a synchronous execution strategy where the full 25-step chunk is executed before the next model re-query. To match the UR3’s 125Hz RTDE control loop, each predicted action in the chunk (originally representing a 40ms interval at 25Hz) is internally expanded into 5 sub-steps through linear interpolation, ensuring consistent and fluid mechanical motion. **Task Settings.** In all tasks, the prompt specifies the desired final state but does not list prerequisite subtasks. As a result, the same prompt may require different execution structures depending on the initial world state. Figure 3 depicts the examples of tasks. 

**Open / Close Lid.** Open or close a container lid. _Train_ : 20 demos. _Test_ : 10 trials. 

**Stack.** Stack one object onto another, including stacking onto a closed container. The prompt does not specify the valid spatial relation. _Train_ : 30 demos. _Test_ : 10 trials. 

**Pour.** Pour liquid from one receptacle into another. The prompt specifies the transfer goal but not intermediate pouring actions. _Train_ : 20 demos. _Test_ : 10 trials. 

**Place.** Place an object into a container, with the final state optionally requiring the lid to be closed. The prompt does not indicate whether opening the lid is necessary. _Train_ : 80 demos. _Test_ : 30 trials. 

**Stack & Place.** Stack one object onto another and place the stacked objects into a container. The prompt does not specify whether the container must be opened before placement. _Train_ : 60 demos. _Test_ : 20 trials. 

**Task Performance.** We report the average success rate (SR) in Table 3. Each task is evaluated with randomized 

_Table 3._ Real-world task success rates (%) on the UR3 platform. 

|**Task**|**OFT+Goal**|**OFT+Subs**|**Ours**|
|---|---|---|---|
|Open / Close Lid|80.0|80.0|**90.0**|
|Stack|80.0|80.0|**90.0**|
|Pouring|70.0|70.0|**80.0**|
|Place|60.0|80.0|**86.7**|
|Stack & Place|45.0|55.0|**75.0**|
|**Average SR**|67.0|73.0|**84.3**|


object poses and two different tabletop backgrounds. We compare our method against the OpenVLA-OFT backbone under two input settings: a goal-only input that specifies only the final task objective (OFT+Goal), and an instructionfollowing variant that concatenates explicit subtask prompts as input (OFT+Subs), allowing us to isolate the effect of task-level reasoning and generalization. 

As shown in Table 3, both OFT+Subs and our method improve over the goal-only baseline, indicating that providing subtask-level guidance partially alleviates failures caused by missing prerequisite information. However, OFT+Subs still struggles to generalize well under variations in initial states and object configurations. We observe behaviors of redundant actions (e.g., attempting to open an already open lid) and failures when the prescribed subtask sequence does not align with the current scene. In contrast, by resolving semantic choices in a structured low-dimensional space before action decoding, our approach can reorganize its execution structure when encountering shifted conditions. 

**Inference Efficiency.** Despite incorporating enriched tasklevel instructions, our model maintains efficient real-time inference. On the UR3 platform, our implementation achieves an average latency of 0.426s and a throughput of 64.3Hz, supporting reactive closed-loop control. 

## **6. Conclusion** 

We introduced iSTAR, a framework that enhances VLA models by embedding task-level semantic structure directly into model parameters. Through in-parameter structural reasoning and functional differentiation, iSTAR explicitly resolves and reuses task structure before action decoding, without relying on external planners or prompt-based decomposition. We provided both theoretical and empirical evidence that such structured semantic commitments improve generalization in long-horizon and ambiguous task settings. Experiments on VIMA-Bench, LIBERO, and real-world robotic manipulation demonstrate more reliable execution and state-conditioned task reorganization, particularly when execution order and prerequisites must be inferred. Overall, iSTAR highlights in-parameter semantic commitment as a principled pathway toward robust and generalizable long-horizon robotic behavior. 

8 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

## **References** 

- Bahdanau, D., Murty, S., Noukhovitch, M., Nguyen, T. H., de Vries, H., and Courville, A. C. Systematic generalization: What is required and can it be learned? In _ICLR_ , 2019. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv.2410.24164_ , 2024. 

- Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., et al. _π_ 0 _._ 5: A vision-language-action model with open-world generalization. arXiv:2504.16054, 2025. 

- Chen, Z., Huo, J., Chen, Y., and Gao, Y. Robohorizon: An LLM-assisted multi-view world model for long-horizon robotic manipulation. arXiv:2501.06605, 2025. 

- Dalal, M., Chiruvolu, T., Chaplot, D. S., and Salakhutdinov, R. Plan-seq-learn: Language model guided RL for solving long horizon robotics tasks. In _ICLR_ , 2024. 

- Fu, M., Huang, H., Datta, G., Chen, L. Y., Panitch, W., Liu, F., Li, H., and Goldberg, K. Icrt: In-context imitation learning via next-token prediction. In _ICRA_ , pp. 5937– 5944, 2025. 

- Guo, W., Kingston, Z., and Kavraki, L. E. CaStL: Constraints as specifications through llm translation for longhorizon task and motion planning. arXiv:2410.22225, 2024. 

- Huang, H., Liu, F., Fu, L., Wu, T., Mukadam, M., Malik, J., Goldberg, K., and Abbeel, P. OTTER: A vision-languageaction model with text-aware visual feature extraction. In _ICML_ , 2025. 

- Hudson, D. A. and Manning, C. D. Gqa: A new dataset for real-world visual reasoning and compositional question answering. In _CVPR_ , pp. 6700–6709, 2019. 

- Ichter, B., Brohan, A., Chebotar, Y., Finn, C., Hausman, K., Herzog, A., Ho, D., Ibarz, J., Irpan, A., Jang, E., Julian, R., Kalashnikov, D., Levine, S., Lu, Y., Parada, C., Rao, K., Sermanet, P., Toshev, A., Vanhoucke, V., Xia, F., Xiao, T., Xu, P., Yan, M., Brown, N., Ahn, M., Cortes, O., Sievers, N., Tan, C., Xu, S., Reyes, D., Rettinghouse, J., Quiambao, J., Pastor, P., Luu, L., Lee, K., Kuang, Y., Jesmonth, S., Joshi, N. J., Jeffrey, K., Ruano, R. J., Hsu, J., Gopalakrishnan, K., David, B., Zeng, A., and Fu, C. K. Do as I can, not as I say: Grounding language in robotic affordances. In _CoRL_ , volume 205, pp. 287–318, 2022. 

- Jiang, Y., Gupta, A., Zhang, Z., Wang, G., Dou, Y., Chen, Y., Fei-Fei, L., Anandkumar, A., Zhu, Y., and Fan, L. VIMA: 

General robot manipulation with multimodal prompts. In _ICML_ , 2023. 

- Kaelbling, L. P. and Lozano-Perez, T.´ Hierarchical task and motion planning in the now. In _ICRA_ , pp. 1470–1477, 2011. 

- Keysers, D., Scharli, N., Scales, N., Buisman, H., Furrer, D.,¨ Kashubin, S., Momchev, N., Sinopalnikov, D., Stafiniak, L., Tihon, T., Tsarkov, D., Wang, X., van Zee, M., and Bousquet, O. Measuring compositional generalization: A comprehensive method on realistic data. In _ICLR_ , 2020. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E. P., Sanketi, P. R., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake, R., Sadigh, D., Levine, S., Liang, P., and Finn, C. OpenVLA: An open-source vision-language-action model. In _CoRL_ , volume 270, pp. 2679–2713, 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. In _RSS_ , 2025. 

- Lake, B. M. and Baroni, M. Generalization without systematicity: On the compositional skills of sequence-tosequence recurrent networks. In _ICML_ , volume 80, pp. 2879–2888, 2018. 

- Langley, P. Crafting papers on machine learning. In Langley, P. (ed.), _Proceedings of the 17th International Conference on Machine Learning (ICML 2000)_ , pp. 1207–1216, Stanford, CA, 2000. Morgan Kaufmann. 

- Li, C., Li, Z., Jing, C., Fan, X., Ye, W., Wu, Y., and Jia, Y. Consistency of compositional generalization across multiple levels. In _AAAI_ , pp. 4661–4669, 2025a. 

- Li, Y., Deng, Y., Zhang, J., Jang, J., Memmel, M., Garrett, C. R., Ramos, F., Fox, D., Li, A., Gupta, A., and Goyal, A. Hamster: Hierarchical action models for open-world robot manipulation. In _ICLR_ , 2025b. 

- Lin, T., Zhong, Y., Du, Y., Zhang, J., Liu, J., Chen, Y., Gu, E., Liu, Z., Cai, H., Zou, Y., et al. Evo-1: Lightweight vision-language-action model with preserved semantic alignment. _arXiv preprint arXiv:2511.04555_ , 2025. 

- Ni, F., Hao, J., Wu, S., Kou, L., Liu, J., Zheng, Y., Wang, B., and Zhuang, Y. Generate subgoal images before act: Unlocking the chain-of-thought reasoning in diffusion model for robot manipulation with multimodal prompts. In _CVPR_ , pp. 13991–14000, 2024. 

- Perez, E., Strub, F., de Vries, H., Dumoulin, V., and Courville, A. C. Film: Visual reasoning with a general conditioning layer. In _AAAI_ , pp. 3942–3951, 2018. 

9 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

- Ross, S. and Bagnell, D. Efficient reductions for imitation learning. In _AISTATS_ , pp. 661–668, 2010. 

- Ross, S., Gordon, G., and Bagnell, D. A reduction of imitation learning and structured prediction to no-regret online learning. In _AISTATS_ , pp. 627–635, 2011. 

- Shi, L. X., Ichter, B., Equi, M., Ke, L., Pertsch, K., Vuong, Q., Tanner, J., Walling, A., Wang, H., Fusai, N., Li-Bell, A., Driess, D., Groom, L., Levine, S., and Finn, C. Hi robot: Open-ended instruction following with hierarchical vision-language-action models. In _ICML_ , 2025. 

   - Zhou, Z., Song, J., Yao, K., Shu, Z., and Ma, L. Isr-llm: Iterative self-refined large language model for long-horizon sequential task planning. In _ICRA_ , pp. 2081–2088, 2024. 

   - Zhu, Y., Tremblay, J., Birchfield, S., and Zhu, Y. Hierarchical planning for long-horizon manipulation with geometric and symbolic scene graphs. In _ICRA_ , pp. 6541–6548, 2021. 

- Shridhar, M., Manuelli, L., and Fox, D. Perceiver-actor: A multi-task transformer for robotic manipulation. In _CoRL_ , pp. 785–799, 2022. 

- Singh, I., Blukis, V., Mousavian, A., Goyal, A., Xu, D., Tremblay, J., Fox, D., Thomason, J., and Garg, A. Progprompt: Generating situated robot task plans using large language models. In _ICRA_ , pp. 11523–11530, 2023. 

- Wagenmaker, A., Nakamoto, M., Zhang, Y., Park, S., Yagoub, W., Nagabandi, A., Gupta, A., and Levine, S. Steering your diffusion policy with latent space reinforcement learning. arXiv:2506.1579, 2025. 

- Wu, X., Wang, R., Hou, J., Lin, H., and Luo, J. Spatial– temporal relation reasoning for action prediction in videos. _IJCV_ , 129(5):1484–1505, 2021. 

- Yi, K., Wu, J., Gan, C., Torralba, A., Kohli, P., and Tenenbaum, J. Neural-symbolic VQA: disentangling reasoning from vision and language understanding. In Bengio, S., Wallach, H. M., Larochelle, H., Grauman, K., Cesa-Bianchi, N., and Garnett, R. (eds.), _NeurIPS_ , pp. 1039–1050, 2018. 

- Yu, J., Liu, H., Yu, Q., Ren, J., Hao, C., Ding, H., Huang, G., Huang, G., Song, Y., Cai, P., Lu, C., and Zhang, W. ForceVLA: Enhancing VLA models with a force-aware moe for contact-rich manipulation. In _NeurIPS_ , 2025. 

- Zhang, R., Dong, M., Zhang, Y., Heng, L., Chi, X., Dai, G., Du, L., Wang, D., Du, Y., and Zhang, S. MoLe-VLA: Dynamic layer-skipping vision language action model via mixture-of-layers for efficient robot manipulation. In _AAAI_ , 2026. 

- Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. CoT-VLA: Visual chain-of-thought reasoning for vision-language-action models. In _CVPR_ , pp. 1702–1713, 2025. 

- Zhou, S., Du, Y., Chen, J., Li, Y., Yeung, D.-Y., and Gan, C. Robodreamer: Learning compositional world models for robot imagination. In _ICLR_ , 2025. 

10 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

## **A. Related Work – Semantic Reasoning from Vision and Language** 

In VLA settings, semantic reasoning over compositional and relational structure is critical for high-level decisions. Such semantic reasoning has been widely studied and shown to be useful in vision–language research. Early studies on systematic generalization show that learned models tend to exploit statistical regularities in the training distribution, rather than acquiring compositional rules, even when such rules are supported by the training data (Lake & Baroni, 2018; Keysers et al., 2020). Subsequent work suggests that systematic generalization is difficult to achieve without explicit structural priors or inductive bias (Bahdanau et al., 2019). In the vision–language domain, vision–language researches (Yi et al., 2018; Hudson & Manning, 2019) explicitly disentangle perception from reasoning, achieving strong robustness and interpretability on VQA benchmarks. Recent evidence further suggests that even large VLMs struggle to maintain consistent compositional generalization across multiple semantic levels, highlighting the limitations of implicit reasoning in latent representations (Li et al., 2025a). Beyond static question answering, structured semantic reasoning has also been explored in spatiotemporal settings, where explicit modeling of semantic relations over time improves action understanding and prediction (Wu et al., 2021; Zhou et al., 2025). Differently, our method treats semantic structure as an explicit commitment for planning, rather than grounding it in generative or visual representations. 

## **B. Detailed Proofs for Proposition 4.1** 

### **B.1. Preliminaries and Notation** 

We consider a finite-horizon decision problem with horizon _T_ . Let _π_<sup>_∗_</sup> denote the expert policy and _π_ ˆ a learned policy. 

At each time step _t_ , the expert admits a latent semantic commitment 


such that the expert action is sampled as 


The structured policy _π_ ˆ consists of three components: (i) a semantic graph predictor ˆ _g_ : _I_ 1: _T �→ c_ ˆ1: _T_ , (ii) a realization map _r_ ˆ : _C →P_ , and (iii) an action decoder _h_<sup>ˆ</sup> : ( _It, pt_ ) _�→ at_ . 

We measure performance using expected cumulative cost 


where the per-step loss is bounded as _ℓ ∈_ [0 _,_ 1]. 

### **B.2. Error Decomposition** 

We restate the decomposition used in Eq. (6). 

**Lemma B.1** (Structured Error Decomposition) **.** _Assume the expert policy admits latent semantic commitments_ ( _c_<sup>_∗_</sup> _t_<sup>_, p∗_</sup> _t_<sup>)</sup><sup>_._</sup> _Then the performance gap of the structured policy satisfies_ 


_where ϵa is the one-step action decoding error conditioned on the correct realization, ϵr is the realization error from semantic graph to subprompt, and ϵG is the semantic graph prediction error. The constants Ca, Cr, CG are independent of the horizon T ._ 

**Proof.** The result follows the standard performance sensitivity arguments. We introduce intermediate policies that successively replace learned components with their expert counterparts. Each replacement induces a bounded deviation in expected cost proportional to the corresponding prediction error. Summing these deviations yields the stated inequality. This decomposition does not rely on trajectory-level coupling or no-regret assumptions. □ 

11 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

### **B.3. Horizon-Insensitive Error Terms** 

We now formalize why _ϵa_ and _ϵr_ do not scale with the horizon. 

**Lemma B.2** (Action Decoding Error) **.** _Conditioned on the correct semantic realization p_<sup>_∗_</sup> _t_<sup>_, the action decoding error_</sup> 


_does not accumulate with T ._ 

**Proof.** Given _p_<sup>_∗_</sup> _t_<sup>,theactiondecodermodelsasingle-stepconditionaldistribution(</sup><sup>_It, p∗_</sup> _t_<sup>)</sup><sup>_�→a∗_</sup> _t_<sup>.Thisisastandard</sup> supervised learning problem whose generalization behavior depends only on the model class and the sample size, not on the rollout horizon. □ **Lemma B.3** (Realization Error) **.** _If the realization map_ ˆ _r is implemented via templates or a constrained grammar, then the realization error ϵr is bounded by a constant independent of T ._ **Proof.** Each semantic commitment is realized independently into a subprompt. Under deterministic or bounded-stochastic realization, realization errors do not propagate across time steps. □ 

### **B.4. Semantic Graph Prediction Error** 

We now analyze the only horizon-sensitive term. 

Let _C_ denote the semantic commitment space. The semantic predictor outputs a sequence ˆ _c_ 1: _T ∈C_<sup>_T_</sup> . 

**Lemma B.4** (Generalization of Semantic Graph Prediction) **.** _Let nG be the number of supervised semantic graph samples. Then with high probability,_ 


_where_ � _ϵG denotes the empirical semantic prediction error._ 

**Proof.** Predicting semantic commitments over a horizon _T_ corresponds to a multi-class prediction problem with output space _C_<sup>_T_</sup> . Applying a union bound over time steps together with standard uniform convergence arguments for discrete hypothesis classes yields the stated bound. This bound is intentionally loose and serves only to characterize the horizon dependence. □ 

Substituting Lemma B.4 into Lemma B.1 and absorbing horizon-independent terms yields 


### **B.5. Comparison with End-to-End Policies** 

For an end-to-end policy that directly predicts a length- _T_ sequence of discrete action tokens, the effective output space is _A_<sup>_T_</sup> . Standard complexity-based generalization arguments imply 


Since log _|C| <_ log _|A|_ , the structured policy admits a strictly tighter leading-order bound for sufficiently large _T_ . This completes the proof of Proposition 4.1. □ 

### **B.6. Effective Complexity of the Semantic Commitment Space** 

The semantic commitment space is constructed from a set of discrete semantic attributes: 


12 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

Although a semantic commitment can be represented as a tuple, its effective complexity is additive across attributes. Specifically, 


reflecting that each attribute contributes independently to the semantic choice. 

This contrasts with the multiplicative complexity<sup>�</sup> _k_<sup>_|Ck|_, which corresponds to a combinatorial abstraction of executable</sup> behaviors and already underestimates the true complexity of the low-level action space _A_ . In practice, _A_ represents discretized physical control over a high-dimensional continuous space, whose effective complexity grows with both control dimensionality and resolution. Consequently, 

log _|C| ≪_ log _|A|,_ 

justifying the regime assumed in Proposition 4.1. 

## **C. Model Integration and Architectural Details** 

### **C.1. Integration with OpenVLA-OFT** 

To integrate our method with OpenVLA-OFT, we freeze the first 28 layers of the vision-language model and use them solely as a prompt token embedding extractor. This design mirrors the role of token embeddings in modular architectures such as VIMA, allowing high-level semantic representations to be reused without altering the backbone’s pretrained reasoning capacity. The remaining layers are reused for action generation, ensuring that low-level execution remains consistent with the original OpenVLA-OFT model. 

### **C.2. Dynamic Positional Encoding on LIBERO** 

OpenVLA-OFT adopts step-level training, where each action chunk is processed independently and temporal structure is not explicitly modeled. However, when tasks are decomposed into ordered subtasks, awareness of subtask progression is necessary to avoid redundant or inconsistent execution. 

To encode subtask progression while remaining compatible with i.i.d. chunked training, we construct a lightweight historyaware positional embedding from teacher-forced subtask representations. For each demonstration, we obtain an ordered subtask sequence _{p_ 1 _, . . . , pS}_ and cache the corresponding embeddings _{e_ 1 _, . . . , eS}_ extracted from an intermediate language-model layer. Given a training sample associated with the current subtask index _i_ , we summarize the preceding subtasks by an aggregation operator 


and fuse it with the current embedding via a gated update to produce a dynamic positional encoding 


where Agg( _·_ ) can be a simple pooling (e.g., mean/max) or a lightweight prefix encoder. The resulting _pi_ conditions action generation (e.g., FiLM-style modulation), providing semantic progress cues without requiring trajectory-level recurrence across chunks. 

## **D. Subtask Prompt Distillation and Supervision Details** 

This appendix details the construction of subtask prompt supervision for LIBERO, including subtask prompt generation, demonstration segmentation, visual grounding, and uncertainty-aware label refinement. 

### **D.1. Subtask Prompt Set Generation** 

LIBERO provides high-level textual task descriptions but does not define explicit subtask-level semantic structure. To obtain a canonical set of subtask prompts for each task, we first perform subtask inference from task descriptions using a pretrained large language model (GPT-4o). 

For each LIBERO task, the original textual instruction is provided to the language model, which is prompted to decompose the task into a small set of semantically meaningful subtasks that correspond to executable stages (e.g., opening a container, 

13 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

grasping an object, placing it at a target location). The resulting subtask prompts form a task-specific subtask vocabulary that is shared across all demonstrations of the task. 

_Listing 1._ Subtask inference prompt used for LIBERO annotation. 

You are given a robotic manipulation task from the LIBERO benchmark. Each task contains a natural language instruction and a formal goal condition. Your job is to decompose the task into a minimal sequence of atomic subtasks that correspond to semantically meaningful execution stages. Guidelines: - Subtasks should be short, executable action phrases. - Each subtask should correspond to a single semantic intent. - Do NOT include low-level motions or control details. - Do NOT include redundant or implicit steps. - Only include actions that are necessary to satisfy the given goal. - Do NOT explain your reasoning. Below are examples. === Example 1 === Language: put the frying pan under the cabinet shelf Goal: (:goal (And (In chefmate_8_frypan_1 wooden_two_layer_shelf_1_bottom_region))) Subtask: 1. pick up the frying pan and place it under the cabinet shelf === Example 2 === Language: put the white bowl on top of the cabinet Goal: (:goal (And (On white_bowl_1 wooden_two_layer_shelf_1_top_side))) Subtask: 1. pick up the white bowl and place it on top of the cabinet === Example 3 === Language: turn on the stove and put the frying pan on it Goal: (:goal (And (Turnon flat_stove_1) (On chefmate_8_frypan_1 flat_stove_1_cook_region))) Subtask: 1. turn on the stove 2. pick up the frying pan and place it on the stove === Task === Language: {TASK_LANGUAGE} Goal: {TASK_GOAL} Subtask: 

### **D.2. Demonstration Segmentation and Keyframe Extraction** 

Each LIBERO demonstration is segmented into subtask-level intervals based on gripper state changes and action transitions. Specifically, we detect grasp and release events from the gripper state and use them as anchors to partition a trajectory into semantically coherent segments. 

For every segment, we extract a fixed number of keyframes (eight in our implementation, see Figure 4) that summarize the visual context of the segment. Subtask classification is performed independently for each segment by conditioning a vision-language model on the keyframes and a predefined set of candidate subtasks. 

For robustness, each segment is classified multiple times with independent sampling. The final subtask label for a segment 

14 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 


_Figure 4._ Example of demonstration segmentation and visual subtask classification. A demonstration of the task “put the white mug on the plate and put the chocolate pudding to the right of the plate” is segmented into four subtask-level segments. For each segment, eight representative keyframes are extracted and independently classified into one of the candidate subtasks. Segment-level predictions are merged in temporal order to form the final subtask sequence. 

is determined by majority voting. Segment-level predictions are then merged in temporal order to obtain a subtask sequence for the full demonstration. 

### **D.3. Visual Subtask Classification via GPT-4o** 

Given a segmented demonstration and the task-specific subtask prompt set, we classify each segment by querying GPT-4o with the extracted keyframes and the candidate subtask list. The model is instructed to assign the most likely subtask label based solely on the visual evidence and the predefined subtask vocabulary. 

To estimate prediction uncertainty, each classification query is repeated five times with independent sampling. We compute an uncertainty score based on label disagreement across samples. Segments with low uncertainty are automatically assigned the predicted subtask label. 

**Classification prompt.** The prompt used for visual subtask classification is shown below. 

_Listing 2._ Visual subtask classification prompt used for segment-level annotation. 

- You are a robotic perception and task grounding model. Given: 1. The current RGB observation from the robot. 2. A list of candidate subtasks. Image structure: - The input image is a composite image arranged in a grid. - The TOP ROW shows images from the global (scene-level) camera. - The BOTTOM ROW shows images from the end-effector (egocentric) - Each COLUMN corresponds to the same time step. - Images in the same column are synchronized. View usage: 

- The BOTTOM ROW shows images from the end-effector (egocentric) camera. 

- Use the GLOBAL view to judge object states and relations (e.g., on/off, on top of). 

15 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

- Use the END-EFFECTOR view to judge active manipulation or physical contact. 

Your task: 

Select the ONE subtask that best matches the CURRENT visual state. 

Critical rules: 

- Choose ONLY ONE subtask from the list. 

- Do NOT infer task order or future steps. 

- Do NOT select a subtask whose required object state is NOT visible. 

- If a subtask is not currently happening or its preconditions are not met, it must be rejected. 

- Base the decision strictly on visible object states and relations. 

- The RIGHTMOST column corresponds to the FINAL time step. 

- The decision should focus primarily on the images in the FINAL column. 

Subtasks: {text} Output format: Selected subtask: <copy the exact subtask text> 

### **D.4. Uncertainty-Aware Manual Refinement** 

Segments with high classification uncertainty are flagged for manual inspection. In practice, these cases typically correspond to visually ambiguous transitions or rare execution patterns. A lightweight manual correction step is applied to these segments to ensure label consistency and semantic correctness. 

This uncertainty-aware refinement strategy significantly reduces annotation effort while maintaining high-quality subtask supervision. In our experiments, only a small fraction of segments require manual correction. 

### **D.5. Summary** 

Through task-level subtask inference, execution-aligned segmentation, visual classification, and uncertainty-aware refinement, we construct reliable subtask prompt supervision for LIBERO without requiring dense manual annotation. This supervision enables structured semantic reasoning within iSTAR while remaining compatible with standard VLA training pipelines. 

_Table 4._ Detailed L1-level results across different task categories. 

|Task|VIMA<br>(Small)|VIMA<br>(Large)|iSTAR<br>(Stacked VIMA)|iSTAR<br>(w/o Graph)|iSTAR<br>(w/o Order Entropy)|iSTAR<br>(w/o Concept Alignment)|iSTAR|
|---|---|---|---|---|---|---|---|
|follow<br>~~o~~rder|0.75|0.84|0.77|0.82|0.82|0.81|0.87|
|manipulate<br>~~o~~ld<br>~~n~~eighbor|0.43|0.47|0.44|0.48|0.50|0.50|0.50|
|novel<br>~~a~~dj|0.99|0.99|0.99|1.00|1.00|1.00|1.00|
|novel<br>~~n~~oun|0.99|0.99|0.99|1.00|1.00|1.00|1.00|
|pick<br>~~i~~n<br>~~o~~rder<br>~~t~~hen<br>~~r~~estore|0.61|0.57|0.60|0.63|0.66|0.70|0.68|
|rearrange|0.73|0.65|0.75|0.72|0.75|0.79|0.81|
|rearrange<br>~~t~~hen<br>~~r~~estore|0.16|0.14|0.14|0.18|0.18|0.25|0.22|
|rotate|1.00|1.00|0.99|0.99|1.00|0.98|1.00|
|same<br>~~s~~hape|0.95|0.98|0.95|0.96|0.98|0.97|0.99|
|scene<br>~~u~~nderstanding|1.00|1.00|1.00|1.00|1.00|1.00|1.00|
|twist|0.09|0.24|0.09|0.18|0.25|0.22|0.23|
|visual<br>~~m~~anipulation|1.00|1.00|1.00|1.00|1.00|1.00|1.00|
|Average|0.724|0.739|0.724|0.748|0.764|0.778|0.786|


## **E. Extended Ablation Studies** 

We report additional ablation results examining alternative design choices, including static positional encoding and different subtask selection strategies. These results further confirm the necessity of state-conditioned subtask reasoning and dynamic 

16 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

_Table 5._ Detailed L2-level results across different task categories. 

|Task|VIMA<br>(Small)|VIMA<br>(Large)|iSTAR<br>(Stacked VIMA)|iSTAR<br>(w/o Graph)|iSTAR<br>(w/o Order Entropy)|iSTAR<br>(w/o Concept Alignment)|iSTAR|
|---|---|---|---|---|---|---|---|
|follow<br>~~o~~rder|0.81|0.78|0.81|0.88|0.90|0.89|0.94|
|manipulate<br>~~o~~ld<br>~~n~~eighbor|0.48|0.47|0.45|0.47|0.51|0.49|0.50|
|novel<br>~~a~~dj|0.99|1.00|1.00|1.00|1.00|1.00|1.00|
|novel<br>~~n~~oun|1.00|1.00|1.00|1.00|1.00|1.00|1.00|
|pick<br>~~i~~n<br>~~o~~rder<br>~~t~~hen<br>~~r~~estore|0.61|0.63|0.64|0.70|0.70|0.72|0.73|
|rearrange|0.74|0.76|0.74|0.75|0.80|0.82|0.85|
|rearrange<br>~~t~~hen<br>~~r~~estore|0.16|0.24|0.13|0.19|0.19|0.21|0.24|
|rotate|1.00|0.99|1.00|1.00|1.00|1.00|1.00|
|same<br>~~s~~hape|0.98|0.96|1.00|0.99|1.00|1.00|1.00|
|scene<br>~~u~~nderstanding|1.00|1.00|0.97|0.99|0.99|1.00|1.00|
|twist|0.09|0.11|0.09|0.15|0.22|0.17|0.24|
|visual<br>~~m~~anipulation|1.00|1.00|1.00|1.00|1.00|1.00|1.00|
|Average|0.738|0.745|0.736|0.760|0.776|0.775|0.792|


_Table 6._ Detailed L3-level results across different task categories. 

|Task|VIMA<br>(Small)|VIMA<br>(Large)|iSTAR<br>(Stacked VIMA)|iSTAR<br>(w/o Graph)|iSTAR<br>(w/o Order Entropy)|iSTAR<br>(w/o Concept Alignment)|iSTAR|
|---|---|---|---|---|---|---|---|
|follow<br>~~o~~rder|0.80|0.88|0.89|0.92|0.90|0.94|0.96|
|manipulate<br>~~o~~ld<br>~~n~~eighbor|0.46|0.38|0.40|0.44|0.55|0.53|0.55|
|novel<br>~~a~~dj|0.98|0.99|1.00|1.00|1.00|1.00|1.00|
|novel<br>~~n~~oun|0.99|0.99|1.00|1.00|1.00|1.00|1.00|
|pick<br>~~i~~n<br>~~o~~rder<br>~~t~~hen<br>~~r~~estore|0.36|0.32|0.40|0.51|0.51|0.54|0.55|
|rearrange|0.69|0.70|0.66|0.75|0.71|0.76|0.79|
|rearrange<br>~~t~~hen<br>~~r~~estore|0.16|0.22|0.23|0.25|0.25|0.29|0.28|
|rotate|1.00|0.99|1.00|1.00|1.00|1.00|1.00|
|same<br>~~s~~hape|0.95|0.95|0.94|0.95|0.99|0.95|1.00|
|scene<br>~~u~~nderstanding|0.98|0.99|1.00|1.00|1.00|1.00|1.00|
|twist|0.17|0.16|0.17|0.17|0.25|0.23|0.27|
|visual<br>~~m~~anipulation|0.99|0.99|1.00|1.00|1.00|1.00|1.00|
|Average|0.711|0.720|0.724|0.749|0.763|0.770|0.783|


temporal modeling. 

**L1–L4: Four levels of zero-shot generalization.** VIMA-BENCH defines a four-level evaluation protocol in which each level deviates further from the training distribution and is therefore harder than the previous one. 

- **L1: Placement generalization.** All prompt templates are seen during training; at test time, only the object placement on the tabletop is randomized. 

- **L2: Combinatorial generalization.** All objects and textures are seen during training, but novel combinations of them appear at test time. 

- **L3: Novel object generalization.** The test prompts and the simulated workspace include novel objects and textures that were not seen in training. 

- **L4: Novel task generalization.** Test time introduces new tasks specified by novel prompt templates (i.e., unseen task templates). 

We report detailed success rates for each task across different VIMA task-level groups, as shown in Tables 4–7. Across long-horizon tasks such as _follow_ _~~o~~ rder_ and _rearrange_ , our method consistently achieves substantial improvements over the baselines. These tasks require reasoning over prerequisite satisfaction and execution order, highlighting the advantage of state-conditioned subtask reasoning. In contrast, performance on the _twist_ task remains significantly lower across all methods. Although the underlying motor primitive in _twist_ is identical to that in _rotate_ , the two tasks differ critically in their 

17 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

_Table 7._ Detailed L4-level results across different task categories. 

|Task|VIMA|VIMA|iSTAR|iSTAR|iSTAR|iSTAR|iSTAR|
|---|---|---|---|---|---|---|---|
||(Small)|(Large)|(Stacked VIMA)|(w/o Graph)|(w/o Order Entropy)|(w/o Concept Alignment)||
|follow<br>~~m~~otion|0.00|0.00|0.00|0.01|0.05|0.05|0.06|
|novel<br>~~a~~dj<br>~~a~~nd<br>~~n~~oun|0.10|0.85|0.09|0.15|0.23|0.18|0.24|
|same<br>~~t~~exture|0.95|0.92|0.93|0.97|1.00|0.97|1.00|
|Average|0.350|0.590|0.340|0.377|0.427|0.400|0.433|


specification. While _rotate_ explicitly provides a target rotation angle, _twist_ only specifies the desired post-rotation visual appearance of the object. As a result, successful execution of _twist_ requires accurate visual inference of object orientation and precise grounding of this inferred state into action commands. This discrepancy suggests that a major challenge for VLA models lies in the tight coupling between visual reasoning and action execution. Estimating object rotation angles from visual observations demands strong perceptual and geometric reasoning capabilities. To further investigate this issue, we conducted preliminary experiments using both traditional computer vision pipelines and learning-based approaches to directly estimate object rotation angles. The results indicate that these methods achieve accuracies of only around 50%, suggesting that the difficulty of the _twist_ task may exceed the current capacity of the models and perceptual tools employed in this work. 

We further investigate the effect of different subprompt projector designs. Tables 8–11 report results using alternative projector architectures across different VIMA task-level groups. In addition to our default encoder-based design, denoted as _iSTAR (Enc)_ , which predicts all subprompt embeddings in a single forward pass, we evaluate an encoder–decoder variant, _iSTAR (Enc–Dec)_ . The encoder–decoder model generates subprompt embeddings autoregressively, introducing an explicit temporal dependency among subprompts. Empirically, we observe that _iSTAR (Enc–Dec)_ yields slightly inferior performance compared to the encoder-only variant across most task groups. A plausible explanation is that the additional autoregressive structure introduces unnecessary modeling complexity for the considered subprompt space. In our setting, subprompts are relatively simple and template-based, and predicting them jointly with a shared encoder appears sufficient and more parameter-efficient. 

_Table 8._ Comparison of different subprompt projectors on the L1 set. 

|Task|VIMA (Small)|VIMA (Large)|iSTAR (Enc-Dec)|iSTAR (Enc)|
|---|---|---|---|---|
|follow<br>~~o~~rder|0.75|0.84|0.77|0.82|
|manipulate<br>~~o~~ld<br>~~n~~eighbor|0.43|0.47|0.44|0.48|
|novel<br>~~a~~dj|0.99|0.99|0.99|1.00|
|novel<br>~~n~~oun|0.99|0.99|0.99|1.00|
|pick<br>~~i~~n<br>~~o~~rder<br>~~t~~hen<br>~~r~~estore|0.61|0.57|0.65|0.63|
|rearrange|0.73|0.65|0.67|0.72|
|rearrange<br>~~t~~hen<br>~~r~~estore|0.16|0.14|0.14|0.18|
|rotate|1.00|1.00|0.99|0.99|
|same<br>~~s~~hape|0.95|0.98|0.97|0.96|
|scene<br>~~u~~nderstanding|1.00|1.00|1.00|1.00|
|twist|0.09|0.24|0.11|0.18|
|visual<br>~~m~~anipulation|1.00|1.00|1.00|1.00|
|Average|0.724|0.739|0.723|0.748|


## **F. Additional Real-World Experimental Details** 

### **F.1. Hardware Platform and Sensing** 

All real-world experiments are conducted on a UR3 industrial robotic arm with 6 degrees of freedom, equipped with a parallel-jaw gripper. The system provides two visual observation streams: a wrist-mounted eye-in-hand camera capturing first-person views during manipulation, and an overhead third-person camera (Intel RealSense D415i) providing a global 

18 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

_Table 9._ Comparison of different subprompt projectors on the L2 set. 

|Task|VIMA (Small)|VIMA (Large)|iSTAR (Enc-Dec)|iSTAR (Enc)|
|---|---|---|---|---|
|follow<br>~~o~~rder|0.81|0.78|0.80|0.88|
|manipulate<br>~~o~~ld<br>~~n~~eighbor|0.48|0.47|0.45|0.47|
|novel<br>~~a~~dj|0.99|1.00|0.99|1.00|
|novel<br>~~n~~oun|1.00|1.00|1.00|1.00|
|pick<br>~~i~~n<br>~~o~~rder<br>~~t~~hen<br>~~r~~estore|0.61|0.63|0.65|0.70|
|rearrange|0.74|0.76|0.78|0.75|
|rearrange<br>~~t~~hen<br>~~r~~estore|0.16|0.24|0.22|0.19|
|rotate|1.00|0.99|1.00|1.00|
|same<br>~~s~~hape|0.98|0.96|0.94|0.99|
|scene<br>~~u~~nderstanding|1.00|1.00|1.00|0.99|
|twist|0.09|0.11|0.09|0.15|
|visual<br>~~m~~anipulation|1.00|1.00|0.99|1.00|
|Average|0.737|0.745|0.743|0.760|


_Table 10._ Comparison of different subprompt projectors on the L3 set. 

|Task|VIMA (Small)|VIMA (Large)|iSTAR (Enc-Dec)|iSTAR (Enc)|
|---|---|---|---|---|
|follow<br>~~o~~rder|0.80|0.88|0.80|0.92|
|manipulate<br>~~o~~ld<br>~~n~~eighbor|0.46|0.38|0.42|0.44|
|novel<br>~~a~~dj|0.98|0.99|1.00|1.00|
|novel<br>~~n~~oun|0.99|0.99|1.00|1.00|
|pick<br>~~i~~n<br>~~o~~rder<br>~~t~~hen<br>~~r~~estore|0.36|0.32|0.44|0.51|
|rearrange|0.69|0.70|0.72|0.75|
|rearrange<br>~~t~~hen<br>~~r~~estore|0.16|0.22|0.21|0.25|
|rotate|1.00|0.99|1.00|1.00|
|same<br>~~s~~hape|0.95|0.95|0.95|0.95|
|scene<br>~~u~~nderstanding|0.98|0.99|1.00|1.00|
|twist|0.17|0.16|0.18|0.17|
|visual<br>~~m~~anipulation|0.99|0.99|1.00|1.00|
|Average|0.716|0.720|0.726|0.751|


scene view. In addition to visual inputs, the policy receives proprioceptive robot state observations consisting of the 7-dimensional joint angles and gripper width. This multi-view sensing configuration enables both local object interaction and global scene understanding during task execution. 

### **F.2. Control Interface and Action Execution** 

The UR3 robot operates at a native control frequency of 125 Hz via the RTDE interface. To maintain consistency with the OpenVLA-OFT backbone, our VLA policy predicts actions at 25 Hz using action chunking. At inference time, a synchronous execution strategy is adopted, where each predicted action chunk is fully executed before querying the model again. 

To bridge the frequency mismatch between the policy and the robot controller, we employ interpolation to upsample the predicted actions. Specifically, each action in the 25 Hz chunk, corresponding to a 40 ms interval, is expanded into five evenly spaced sub-steps, resulting in smooth and stable motion at the robot’s native control rate. This interpolation is applied purely at the execution layer and does not alter the policy architecture or training procedure. 

19 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

_Table 11._ Comparison of different subprompt projectors on the L4 set. 

|Task|VIMA (Small)|VIMA (Large)|iSTAR (Enc-Dec)|iSTAR (Enc)|
|---|---|---|---|---|
|follow<br>~~m~~otion|0.00|0.00|0.00|0.01|
|novel<br>~~a~~dj<br>~~a~~nd<br>~~n~~oun|0.10|0.85|0.11|0.15|
|same<br>~~t~~exture|0.95|0.92|0.92|0.97|
|Average|0.350|0.590|0.343|0.377|


_Figure 5._ Hardware platform and sensing in our real-world experiments: one UR3 industrial robotic arm and two Intel RealSense D415i cameras. The left figure shows an overview of the experimental hardware platform, and the right figure provides a close-up view of the robotic arm. 

### **F.3. Task Setting Details** 

For all real-world tasks, the language prompt specifies the desired final state of the task, such as the target object configuration or whether a container lid should be closed at completion. However, the prompt does not enumerate prerequisite subtasks or intermediate actions. As a result, the execution structure required to reach the specified goal depends on the initial world state. This design ensures that task completion requires inferring valid action structure conditioned on the scene, rather than following explicitly provided procedural instructions. We describe the tasks and summarize the corresponding prompts and subprompts in Table 12. 

### **F.4. Task-Specific Success Rate** 

We show the task-specific results on the real-world experiment in Table 13. 

### **F.5. Comparative Analysis of Initial State Robustness** 

To understand the performance gap between instruction-following baselines and our proposed method, we evaluate Task (Place) and Task (Stack & Place) under two distinct initial world states: Lid Closed and Lid Open. While OFT+Subs benefits from fine-grained subtask prompts, it lacks the visual closed-loop adaptability required to reorganize its plan when prerequisites are already satisfied. 

To provide a granular assessment of policy performance, we implement a staged scoring system. Each task is decomposed into semantic milestones, with points awarded cumulatively. This structure is designed to isolate the performance of the high-level reasoning branch from low-level motor control. 

20 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

_Table 12._ Summary of real-world tasks with corresponding prompts and subprompts. Prompts specify the desired final state, while subprompts represent intermediate semantic goals that must be inferred based on the initial world state. 

|**Task**|**Initial State**|**Prompt (Goal)**|**Subprompt(s)**<br>**#**|**Demos  **|**# Trials**|
|---|---|---|---|---|---|
|Open / Close|Lid closed<br>Lid closed|Open the lid<br>Close the lid|Open the lid<br>Close the lid|10<br>10|5<br>5|
|Stack|-|Stack X on Y|Stack X on Y|30|10|
|Pouring|-|Pour liquid from cup A into<br>cup B|Pour liquid from cup A into<br>cup B|10|5|
||-|Pour liquid from cup into con-<br>tainer|Pour liquid from cup into con-<br>tainer|10|5|
|Place|Lid closed|Put X into the container and<br>close the lid|Open the lid; put X into the<br>container; close the lid|20|10|
||Lid closed|Put X into the container|Open lid; put X into container|30|10|
||Lid open|Put X into the container|Put X into container|30|10|
|Stack & Place|Lid closed|Stack the X on Y and put<br>them into the container|Stack X on Y; open lid; put<br>the stacked objects into the con-<br>tainer|30|10|
||Lid open|Stack X on Y and put them<br>into the container|Stack X on Y; put the stacked<br>objects into the container|30|10|


### **Place Object into Container (100 pts)** 

- **Stage 1 (20 pts):** _Reaching_ — End-effector successfully approaches the target object. 

- **Stage 2 (20 pts):** _Grasping_ — Securely lifting the object and maintaining stability. 

- **Stage 3 (30 pts):** **_Reasoning Branch (Lid Constraint)_** — 

   - **Condition A (Lid Closed):** Successfully executes the “Open Lid” subtask. 

   - **Condition B (Lid Open):** Corrects the plan by bypassing the “Open” skill and moving directly to the container. 

- **Stage 4 (30 pts):** _Final Placement_ — Releasing the object in the right place. 

### **Stack and Place into Container (100 pts)** 

- **Stage 1 (20 pts):** _Nesting_ — Accurate stacking objects. 

- **Stage 2 (20 pts):** _Assembly Transport_ — Lifting the nested assembly and moving towards the box. 

- **Stage 3 (30 pts):** **_Reasoning Branch (Lid Constraint)_** — 

   - **Condition A (Lid Closed):** Successfully executes the “Open Lid” subtask. 

   - **Condition B (Lid Open):** Corrects the plan by bypassing the “Open” skill and moving directly to the container. 

- **Stage 4 (30 pts):** _Final Placement_ — Releasing the object in the right place. 

Table 14 provides a fine-grained analysis of policy behavior under different initial world states by decomposing each task into semantic stages. Across both _Place_ and _Stack & Place_ tasks, low-level motor stages (Stage 1,2 and Stage 4) show relatively small performance gaps among methods, indicating that execution-level control is not the primary source of failure. 

In contrast, the largest and most consistent performance differences appear in **Stage 3 (Reasoning Branch)** , which requires adapting the execution plan based on the initial lid state. When the lid is already open, both OFT+Goal and OFT+Subs 

21 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

_Table 13._ Detailed Success Rates (%) by Task Variant and Execution Structure on the UR3 platform. We compare our dynamic reasoning approach against _OFT+Goal_ and the instruction-following _OFT+Subs_ baseline. 

|**Task**|**Variant / Execution Structure**|**OFT+Goal**|**OFT+Subs**|**Ours**|
|---|---|---|---|---|
|Open / Close Lid|Open Lid<br>Close Lid|80.0<br>80.0|80.0<br>80.0|**100.0**<br>**80.0**|
|Stack|On Object|80.0|80.0|**90.0**|
|Pour|Cup-to-Cup|60.0|60.0|**80.0**|
||Cup-to-Container|80.0|80.0|**80.0**|
||Open_−_Place_−_Close|40.0|80.0|**90.0**|
|Place|Open_−_Place|60.0|80.0|**80.0**|
||Place|80.0|80.0|**90.0**|
|Stk & Pl|Stack_−_Open_−_Place|30.0|50.0|**70.0**|
|ac  ace|Stack_−_Place|60.0|60.0|**80.0**|
|**Average SR**|—|67.0|73.0|**84.3**|


frequently fail to bypass the redundant “Open Lid” subtask, leading to unnecessary actions and cascading failures. Although OFT+Subs benefits from subtask supervision, it still lacks the ability to reorganize its plan based on visual feedback. 

Our method consistently achieves near-optimal scores in Stage 3 under both lid conditions, demonstrating robust stateconditioned task reorganization. These results confirm that the performance gains primarily stem from improved task-level reasoning and closed-loop adaptation, highlighting the advantage of explicit semantic reasoning for handling varying initial states. 

_Table 14._ Detailed performance breakdown (average scores) across task stages on the UR3 platform. Scores are cumulative (100 pts total per task). We highlight the performance drop in **Stage 3 (Reasoning Branch)** , where baselines struggle to adapt to varying initial lid states. 

|**Task & Initial State**|**Method**|**Stage 1**<br>(Reach/Nest)|**Stage 2**<br>(Grasp/Trans)|**Stage 3**<br>**(Reasoning)**|**Stage 4**<br>(Placement)|**Total**<br>**(Score)**|
|---|---|---|---|---|---|---|
|**Place & Close**|OFT+Goal|15|14|15|12|56|
|_(Lid Closed)_|OFT+Subs|19|18|27|24|88|
||**Ours**|**20**|**20**|**30**|**27**|**97**|
|**Place**|OFT+Goal|17|17|18|18|70|
|_(Lid Closed)_|OFT+Subs|19|18|27|24|88|
||**Ours**|**19**|**19**|**30**|**24**|**92**|
|**Place**|OFT+Goal|18|18|24|24|84|
|_(Lid Open)_|OFT+Subs|18|18|24|24|84|
||**Ours**|**19**|**19**|**27**|**27**|**92**|
|**Stack & Place**|OFT+Goal|16|14|12|9|51|
|_(Lid Closed)_|OFT+Subs|18|16|21|15|70|
||**Ours**|**18**|**16**|**27**|**21**|**82**|
|**Stack & Place**|OFT+Goal|16|14|18|18|66|
|_(Lid Open)_|OFT+Subs|**18**|16|24|18|76|
||**Ours**|16|**20**|**30**|**24**|**90**|


## **G. Visualization** 

In this appendix, we provide qualitative visualizations to complement the quantitative evaluations in the main paper. Each visualization presents the full task prompt, the subprompts, and step-wise execution snapshots, enabling a transparent view 

22 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 

of how high-level instructions are grounded into action sequences. 

We include examples from both the VIMA benchmark (Figure 6) and real-world experiments (Figure 7). 


_Figure 6._ Example of VIMA-Bench. 

We additionally show failure cases from real-world experiments, as shown in Figure 8. The figure highlights several typical failure modes observed during execution. 

The first failure case is an incorrect prerequisite assessment, where the policy attempts to open a container that is already open. This behavior indicates residual limitations in reliably grounding object states from visual observations under real-world conditions. The second failure mode arises from spatial misalignment, where the manipulated object is not properly aligned with the target location. Such errors are often amplified by physical uncertainties, including imperfect grasping, slippage, and calibration noise, and can lead to cascading failures in subsequent steps. Together, these cases illustrate that while our method improves high-level task reasoning and execution structure, robustness to fine-grained state perception and precise spatial alignment remains a key challenge in real-world robotic manipulation. 

23 

**Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** 


_Figure 7._ Example of the real-world experiment. 


**Prompt: put the yellow cube into the container** 


_Figure 8._ Failure case of the real-world experiment. 

24 

