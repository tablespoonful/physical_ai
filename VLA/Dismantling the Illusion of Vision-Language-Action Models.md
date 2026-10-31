---
title: "Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts"
date: "2026"
venue: "ICML 2026"
url: https://proceedings.mlr.press/v306/zhou26az.html
pdf: https://raw.githubusercontent.com/mlresearch/v306/main/assets/zhou26az/zhou26az.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://raw.githubusercontent.com/mlresearch/v306/main/assets/zhou26az/zhou26az.pdf)** / [論文ページ](https://proceedings.mlr.press/v306/zhou26az.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

**Xueyang Zhou**<sup>1 *</sup> **Yangming Xu**<sup>1 *</sup> **Guiyao Tie**<sup>1</sup> **Chaoran Hu**<sup>1</sup> **Bo Tao**<sup>1</sup> **Xingwei Zhao**<sup>1</sup> **Xiang Xiang**<sup>1</sup> **Pan Zhou**<sup>1</sup> **Lichao Sun**<sup>2</sup> **Yongchao Chen**<sup>3</sup> 

# **Abstract** 

Given that simulation can never exhaustively enumerate reality, generalization is the determining factor for whether Vision-Language-Action (VLA) models can translate benchmark success into real-world functionality. However, current evaluation protocols often incentivize mechanical memorization rather than robust policy learning, leading to a paradoxical duality of failure: highscoring models exhibit _spurious invariance_ to semantic changes while simultaneously displaying _extreme brittleness_ to trivial environmental perturbations. To address this, we introduce **LIBEROGen** , a diagnostic benchmark systematically designed to shift evaluation from intuition-driven heuristics to explicit distributional assumptions. Through a hierarchical protocol spanning **Indistribution** , **Compositional** , and **Domain Generalization** , LIBERO-Gen reveals performance stratifications previously masked by standard metrics. Our analysis identifies Pi0.5 as the top performer (64.0% in Spatial-CG; 21.2% in Task-CG). By identifying perceptual instability and action binding collapse as primary failure modes while validating the efficacy of structured “Stair” sampling, LIBERO-Gen establishes a rigorous baseline for deployment reliability. 

# **1. Introduction** 

Vision–Language–Action (VLA) models have become a central paradigm for embodied agents, unifying perception, understanding, and action (Sun et al., 2025). Due to the 

> *Equal contribution 1 Huazhong University of Science and Technology, Wuhan, China 2 Lehigh University, Bethlehem, PA, USA 3 College of AI, Tsinghua University, Beijing, China . Correspondence to: Pan Zhou _<_ panzhou@hust.edu.cn _>_ , Bo Tao _<_ taobo@hust.edu.cn _>_ , Yongchao Chen _<_ yongchaochen12@gmail.com _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

heterogeneity and cost of real-world hardware, simulation benchmarks are indispensable: they provide standardized, reproducible testbeds and effectively steer methodological progress (James et al., 2020; Liu et al., 2023; Mees et al., 2022; Li et al., 2024; Nasiriany et al., 2024). However, we find that existing benchmarks exemplified by LIBERO (Liu et al., 2023) suffer from a fundamental evaluation limitation. Their test protocols largely mirror the training distribution, differing only through visually subtle and often imperceptible state perturbations. Under such settings, high success rates primarily indicate a scale-enabled capacity to fit a narrow task distribution rather than robust policy learning and generalization (Fang et al., 2025b; Zhou et al., 2025b). 

As shown in Figure 1, the high performance of existing VLA models on LIBERO obscures a paradoxical duality of failure. On one hand, models exhibit Spurious Invariance: in controlled intervention experiments, such as replacing the target object or corrupting instructions into meaningless tokens, the resulting action trajectories remain nearly unchanged. On the other hand, they simultaneously display Extreme Brittleness: trivial environmental perturbations (e.g., minor visual noise or lighting shifts) can cause catastrophic failure. This contrast reveals a reliance on mechanical memorization rather than causal understanding, severely limiting their adaptability to the physical world. 

**_Given that simulation can never exhaustively enumerate reality, generalization is not optional—it is the determining factor for whether VLA models can translate from benchmark success to real-world functionality._** To address this impasse, we introduce LIBERO-Gen. Our central premise is that generalization should not be evaluated through intuition-driven heuristics, but instead grounded in explicit distributional assumptions and diagnostically constructed shifts. For instance, it is unrealistic to expect a model trained under a single context and a fixed set of distractors to spontaneously acquire immunity to distribution shift. To this end, LIBERO-Gen employs a rigorous, theory-guided hierarchical evaluation, systematically probing generalization boundaries across five key dimensions: background, language, distractors, task semantics, and spatial configuration. This evaluation is structured into three 

1 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 


_Figure 1._ Behavior of OpenVLA, Pi0, and Pi0.5 under spatial and semantic perturbations. Despite 100% success on the Original Task, models exhibit rigid behaviors in modified settings: (1) Position Change: Swapping object positions leads models to grasp the distractor at the original coordinates; (2) Task Change & Meaningless Instruction: Altering the text to a new target or random characters results in models persisting with the original action sequence. 

distinct levels: (1) **In-distribution.** Verifies the foundational capability to fit the training support set. (2) **Compositional Generalization.** (Gao et al., 2024) Tests adaptability to novel combinations of known factors. (3) **Domain Generalization.** (Besserve et al., 2021) Probes robustness against completely unseen distribution shifts (e.g., unseen textures). Our key contributions are summarized as follows: 

- We demonstrate that current protocols are insufficient to support the simulation-to-reality transition, emphasizing the critical necessity of robust generalization for ensuring reliable VLA deployment. 

- We introduce a hierarchical evaluation suite LIBEROGen that shifts the paradigm from intuition-driven heuristics to explicit distributional assumptions, employing “staircase” sampling to systematically probe generalization boundaries. 

- While identifying Pi0.5 as the top performer, we pinpoint perceptual instability and action binding collapse as primary failure modes, providing a rigorous baseline and direction for reliable VLA deployment. 

# **2. Formalization** 

**Vision-Language-Action Model.** We formalize the VLA model as a vision-language-conditioned generative policy _πθ_ ( _at|ot, l_ ) within a partially observable Markov Decision Process (POMDP) framework for task execution. The goal of VLA is to model the conditional distribution of actions _P_ ( _at | ot, l_ ), where _ot_ is the visual observation and _l_ is the linguistic instruction at time _t_ . 

For a given task instance, the environment is initialized from a state distribution _s_ 0 _∼ ρ_ ( _·_ ). At time _t_ , the model receives 

an observation _ot ∈O_ and a natural-language instruction _l ∈L_ , generating an action _at ∈A_ . The environment dynamics and observation function are defined by: 


Task completion is evaluated using a binary success indicator Succ( _τ_ ) _∈{_ 0 _,_ 1 _}_ , where _τ_ = _{_ ( _ot, at_ ) _}_<sup>_T_</sup> _t_ =0<sup>_−_1isthe</sup> episode rollout trajectory of horizon _T_ . In common VLA paradigms (e.g., LIBERO), Succ( _τ_ ) is typically determined by an environment-defined task verifier checking for specific goal criteria (e.g., object pose/contact constraints). 

**Compositional Generalization.** We formalize compositional generalization for VLA policies by decomposing each task instance into causal factors. A task is modeled as a tuple: 


where _τ ∈T_ denotes the abstract task semantics (e.g., pickand-place, push, stack), and _ci ∈ Ci_ denotes independent context factors such as visual appearance, instruction phrasing, and spatial layouts. Let _C_ = _C_ 1 _× · · · × Cn_ denote the joint context space. The training dataset _D_ train is sampled from a **restricted support** of the full Cartesian product: 


Many factor combinations may be absent, even though individual factor values are observed during training: 


A VLA policy _πθ_ demonstrates compositional generaliza- 

2 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 


_Figure 2._ Overview of the LIBERO-Gen evaluation framework. The right panel illustrates the data sampling strategies in the factor space. For training, we employ ’L’ (green points) and ’Stair’ (blue points) configurations. For evaluation, the framework specifically tests CG (yellow points) and DG (grey points) to assess model robustness across different distribution shifts. 

tion if, given a training set _D_ train with limited compositional coverage and restricted factor combinations, it achieves low execution error on task-context pairs composed of novel combinations of seen factors without extra supervision. Let _D_<sup>(1)</sup> eval<sup>be an evaluation distribution such that:</sup> 


Then, _πθ_ exhibits compositional generalization if: 


for a small constant _ϵ >_ 0. 

**Domain Generalization.** We next formalize domain generalization (DG) for VLA policies, which captures robustness to _out-of-support_ environmental shifts that cannot be expressed as recombinations of training factors. We assume that task execution is governed by a set of latent, conditionally independent generative mechanisms _{Mj}_<sup>_J_</sup> _j_ =1<sup>(e.g.,</sup> task semantics, object dynamics, language grounding, visual appearance), following the Independent Mechanisms principle (Besserve et al., 2021). A _domain e ∈E_ is defined as a particular instantiation of a subset of these mechanisms, inducing an environment-specific observation distribution: 


while sharing the same underlying task semantics _τ_ and transition dynamics _P_ ( _st_ +1 _| st, at_ ). 

Let _E_ train ⊊ _E_ all denote the set of domains available during training, and let _E_ eval _⊂E_ all _\ E_ train denote unseen test domains, and _c ∈C_ represents context variables instantiated 

under domain _e_ . The training dataset is sampled as: 


Unlike compositional generalization, domain generalization allows evaluation samples whose context realizations lie _outside_ the convex hull of training support: 


A VLA policy _πθ_ exhibits _domain generalization_ if it achieves low execution error when deployed in unseen domains whose underlying generative mechanisms differ from those observed and learned during training, without access to extra domain labels or adaptation data. 

Formally, _πθ_ is domain-generalizable if: 


for a small constant _ϵ >_ 0. 

# **3. LIBERO-Gen: Benchmark Design** 

We instantiate the LIBERO-Gen benchmark across five distinct dimensions, as shown in Figure 2. For each dimension, we strictly define the Training Protocol (designed to induce spurious correlations) and the Evaluation Protocol (designed to test generalization bounds). 

## **3.1. Hierarchical Generalization Design** 

Building on the factorized formulation in Sec. 2, we characterize the generalization boundary of VLA policies under _controlled_ distribution shifts by selecting a set of manipulable factors and systematically intervening on them at evaluation time. Each task instance is specified by an abstract task 

3 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

semantic _τ ∈T_ together with a context configuration _c ∈C_ , where _c_ denotes the joint assignment of the factor subset considered in this suite. The training set _D_ train _⊂T × C_ is sampled from a restricted support over task–context pairs, so that certain portion of valid combinations in _T × C_ are never observed during the policy training process. 


_Figure 3._ Sampling Distributions for Training and Evaluation. 

As shown in Figure 3, we evaluate a policy _πθ_ on a suite of datasets _{D_ eval<sup>_k}k∈{_0</sup><sup>_,_1</sup><sup>_,_2</sup><sup>_}_,where</sup><sup>_k_explicitly corresponds</sup> to an increasing order of distribution shift severity, ranging from identical training support to entirely novel domains: 

- **In-distribution (ID) evaluation** ( _k_ = 0). _D_ eval<sup>0contains</sup> task–context pairs drawn from the same empirical support as _D_ train to assess policy under non-shifted conditions. 

- **Compositional generalization** ( _k_ = 1). _D_ eval<sup>1consists</sup> of _unseen_ task–context pairs ( _τ, c_ ) _∈D/_ train formed by recombining _previously observed_ tasks and contexts. Concretely, it satisfies _D_ eval<sup>1</sup><sup>_∩D_train=∅, proj</sup> _T_<sup>(</sup><sup>_D_</sup> eval<sup>1)</sup><sup>_⊆_</sup> proj _T_ ( _D_ train), and proj _C_ ( _D_ eval<sup>1)</sup><sup>_⊆_proj</sup> _C_<sup>(</sup><sup>_D_train).</sup> 

- **Domain generalization (DG)** ( _k_ = 2). _D_ eval<sup>2evalu-</sup> ates robustness to _unseen_ appearance domains outside the training support. We treat each texture/material set as a domain and adopt the standard DG protocol that trains on a set of available domains _E_ avail and tests on a larger domain set _E_ all _⊃ E_ avail, thereby probing genuine out-of-distribution shifts beyond factor recombination. 

## **3.2. Multi-dimensional Evaluation** 

Our suite measures robustness along five complementary dimensions: (i) **background** (textures/materials of the floor, walls, and table), (ii) **language** (instruction wording and paraphrases), (iii) **distractor objects** (irrelevant objects present in the scene), (iv) **task** (the task semantic goal), and (v) **spatial configuration** (object and target positions/layouts). For each dimension, we specify the training distribution and evaluation sampling strategy as follows. 

**Visual Generation.** To instantiate the **_background_** dimension on the LIBERO-Object benchmark, we define the two independent variables as the task semantics ( _τ ∈T_ ) and the tabletop textures ( _c ∈C_ ), constructing the training set as a subset of their compositional pairs. For the training 


_Figure 4._ Example of Sampling for Distractor Generation. 

distribution, we select five tabletop textures as the seen set _C_ seen = _{c_ 1 _, . . . , c_ 5 _}_ , partition the 10 LIBERO-Object base tasks into five disjoint groups with two tasks per group, and use a structured task–texture split in which each group is paired with a single texture (see Appendix C.1 for detailed texture assets and training configurations in Table 6). At test time, we evaluate the same set of tasks under three levels of controlled texture perturbations (refer to Table 7 in Appendix C.1). 

**Language Generation.** To instantiate the **_language_** dimension on the LIBERO-Object benchmark, we define the two independent variables as the task semantics ( _τ ∈T_ ) and the linguistic templates ( _c ∈C_ ), constructing the training set as a subset of their compositional pairs. The training distribution uses five semantically invariant but syntactically distinct instruction templates as _C_ seen = _{c_ 1 _, . . . , c_ 5 _}_ , partitions the 10 tasks into five groups following the same division rule, and pairs each task group with a single instruction template to form a structured task–language split (detailed training configurations are provided in Table 10 of Appendix C.3). For evaluation sampling, we set three generalization levels (specific evaluation templates and paraphrase examples are listed in Table 11 of Appendix C.3). 

**Distractor Generation.** To instantiate the _distractor_ dimension on the LIBERO-Object benchmark, we define the two independent variables as the task semantics ( _τ ∈T_ ) and the distractor configurations ( _c ∈C_ ), constructing the training set as a subset of their compositional pairs. We construct five distractor configurations as _C_ seen = _{c_ 1 _, . . . , c_ 5 _}_ by selecting distinct irrelevant object categories with multiple instances per category, and pair each task group with a corresponding distractor configuration to obtain a structured task–distractor split (see Appendix C.2 for detailed distractor assets and training settings in Table 8). During evaluation, we set three generalization levels (fixed evaluation configurations are shown in Table 9 of Appendix C.2). 

4 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

_Table 1._ Evaluation Results on LIBERO-Gen Benchmark. Success rates (%) across different generalization axes: Original (Ori.), In-Distribution ( _k_ 1), Compositional Generalization ( _k_ 2), and Domain Generalization ( _k_ 3). **Bold** results indicate the best performance, and underlined results indicate the worst performance among base models. 

|**Models**||**Backg**|**round**|||**Lang**|**uage**||**U**|**nrelate**|**d Obje**|**ct**||**Posi**|**tion**|||**Ta**|**sk**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Ori.|_k_1|_k_2|_k_3|Ori.|_k_1|_k_2|_k_3|Ori.|_k_1|_k_2|_k_3|Ori.|_k_1|_k_2|_k_3|Ori.|_k_1|_k_2|_k_3|
|OpenVLA|98.0|**99.6**|94.0|99.4|98.0|0.0|0.0|39.2|98.0|67.2|63.8|52.0|98.0|51.5|6.8|10.0|93.0|95.0|0.0|0.0|
|Pi0|98.0|97.6|95.6|**99.6**|98.0|96.8|**99.2**|94.0|98.0|90.4|95.2|88.4|95.4|93.2|7.2|3.6|95.0|98.8|13.6|36.4|
|Pi0.5|**99.0**|99.2|**99.0**|98.8|**99.0**|**98.8**|98.8|**99.2**|**99.0**|**99.2**|**99.2**|**99.2**|**98.8**|**97.2**|49.2|**27.2**|96.4|**99.6**|**21.2**|**46.0**|
|Molmoact|95.4|94.0|92.0|88.0|95.4|86.0|84.0|90.0|95.4|90.0|90.0|88.0|87.0|87.6|2.8|0.8|92.0|87.6|6.0|6.0|
|NORA|95.4|82.4|94.0|93.2|95.4|93.4|93.2|93.2|95.4|70.8|70.0|0.0|92.2|92.8|1.6|0.8|88.8|88.0|8.8|12.8|
|x-VLA|98.6|98.0|96.8|98.4|98.6|96.8|99.0|97.0|98.6|64.8|46.0|63.8|98.2|96.2|0.0|12.8|**98.1**|98.9|15.6|8.2|
|Univla|96.8|94.0|93.0|96.0|96.8|93.0|95.0|91.0|96.8|74.0|61.0|54.0|96.5|49.0|0.0|0.0|94.4|86.2|9.0|9.0|
|_Fine-tuned_|||||||_Mo_|_dels fine_|_-tuned_|_on LIB_|_ERO-G_|_en spe_|_cific su_|_bsets_|||||||
|Pi0*|–|97.8|97.2|98.8|–|97.6|**99.2**|96.0|–|95.6|98.0|97.0|–|95.4|13.2|4.2|–|98.8|13.6|36.4|
|Pi0.5*|–|98.0|97.0|98.4|–|97.0|98.4|97.0|–|95.4|97.4|97.4|–|**97.2**|**64.0**|27.0|–|**99.6**|**21.2**|**46.0**|


## **Task Compositionality: Action–Object Generalization.** 

We instantiate the _task semantic_ dimension on LIBEROObject and LIBERO-10 to evaluate whether VLA policies can generalize across action–object semantics beyond the combinations observed during training. The training data combines 10 single-object manipulation tasks from LIBERO-Object and 3 composite tasks from LIBERO-10, covering all single objects but only three specific object pairs (refer to Appendix C.5 for the full training task list in Table 12). For evaluation sampling, we set three generalization levels (specific evaluation task pairs are detailed in Table 13 of Appendix C.5). 

**Spatial Generalization: Layout Extrapolation.** We instantiate the _spatial_ dimension on LIBERO-Spatial, where each task relocates a bowl initialized at one of 10 discrete locations to a plate. We take the bowl and plate initial locations as the context variables, i.e., _c_ = ( _p_ bowl _, p_ plate). For the training distribution, we construct a structured spatial split over the bowl–plate location grid by including the original 10 tasks that move the bowl from each location to the fixed plate, together with 9 auxiliary tasks where the bowl is fixed at _p_<sup>_⋆_</sup> bowl<sup>and the plate is placed at the other 9 locations</sup> (see Appendix C.4 for detailed spatial assets and sampling protocols). At test time, we set three generalization levels (configurations are detailed in Appendix C.4). 

## **3.3. Evaluation Protocol** 

Based on the five evaluation suites described above and the three perturbation regimes, we design a unified protocol to assess the generalization of each VLA policy. 

**Suites and perturbation regimes.** Let _Q_ = _{_ Background _,_ Language _,_ Distractors _,_ Task _,_ Spatial _}_ denote the set of evaluation suites (one per dimension) and _K_ = _{_ 0 _,_ 1 _,_ 2 _}_ denote the perturbation regimes (ID, compositional generalization, and OOD/DG, respectively). For each suite 

_q ∈Q_ and regime _k ∈K_ , we evaluate each task _t ∈Tq_ by rolling out the policy from _N_ independently sampled initializations drawn from the suite-specific distribution _D_ eval<sup>_q,k_.</sup> 

**Task-level success.** We report the task success rate as 


where _τ_<sup>(</sup><sup>_t_)</sup> _q,k,i_<sup>denotesthecompleteexecutedtrajectoryin</sup> the _i_ -th rollout. Correspondingly, ( _Eq,k,i_<sup>(</sup><sup>_t_)</sup><sup>_,l_</sup> _q,k,i_<sup>(</sup><sup>_t_)) represent</sup> the environment initialization (including the suite-specific perturbation) and language instruction provided to the policy. Here, the binary indicator function Succ( _τ_ ) _∈{_ 0 _,_ 1 _}_ indicates whether the rollout successfully completes task _t_ . 

# **4. Experiments** 

In this section, we present a comprehensive empirical evaluation on LIBERO-Gen. Our experiments address three pivotal research questions: 

- **RQ1:** Do high simulation scores truly reflect the robustness required for real-world functionality? 

- **RQ2:** What specific failure modes and generalization challenges hinder VLA adaptation to distribution shifts? 

- **RQ3:** How can models trained on finite data achieve the robust generalization needed for reliable deployment? 

## **4.1. Main Results** 

We conduct a comprehensive evaluation of representative VLA models on LIBERO-Gen, with detailed results summarized in Table 1. 

(1) **The Illusion of Competence.** While most models saturate standard benchmarks with _>_ 95% success rates, LIBERO-Gen reveals this performance stems from mechan- 

5 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 


_Figure 5._ Latent Feature Visualization under Distribution Shifts. 

ical memorization rather than robust understanding. For instance, OpenVLA matches Pi0.5 on original tasks but suffers catastrophic collapse under minimal variations. Specifically, it drops to 0.0% under semantic paraphrasing and 67.2% in the presence of irrelevant clutter, exposing a fundamental brittleness to minor, goal-irrelevant perturbations. 

(2) **Variable-Dependent Generalization Hierarchy.** Generalization difficulty varies significantly across distinct types of distribution perturbations. Models exhibit high robustness to Background variations (mostly _>_ 90% success). However, Position and Task generalization emerge as the primary bottlenecks; nearly all baselines (e.g., OpenVLA, Molmoact, Univla) plummet to near-zero success rates in these categories. This distinct hierarchy highlights that current VLA architectures struggle most with spatial extrapolation and compositional task planning. 

(3) **Differentiation via Hierarchical Generalization.** LIBERO-Gen effectively stratifies capabilities that standard metrics conflate. While OpenVLA and x-VLA fail to generalize on spatial tasks (achieving 6.8% and 0.0% on Position-CG, respectively), Pi0.5 demonstrates superior structural generalization, achieving 49.2% on Position-CG and 46.0% on Task-DG. Furthermore, models like NORA and x-VLA show competitive semantic understanding on Language tasks ( _>_ 93%) but lack the physical grounding required for spatial robustness. 

(4) **Decoupling Model Capabilities from Data Bias.** The 

prevailing generalization failures should not be ascribed solely to architectural deficits; rather, they reflect the inherent impossibility of deriving unbiased policies from biased training distributions. LIBERO-Gen addresses this by establishing a rigorous protocol that ensures fair capability assessment under controlled distributions. This value is empirically validated by our fine-tuning results: when trained under our structured regime, models demonstrate significantly unlocked potential, with Pi0 and Pi0.5 improving their Position-CG performance from 7.2% to 13.2% and 49.2% to 64.0%, respectively. 

## **4.2. Failure Mechanisms** 

To answer **RQ2** , we visualize the latent feature of the encoder under different perturbation regimes. We identify two distinct failure mechanisms: 

**Type I: Perceptual Instability.** The encoder fails to marginalize out goal-irrelevant nuisance variables. As illustrated in Figure 5 (Column 2), _OpenVLA-Libero_ (Row 1) projects semantically equivalent instructions onto disjoint latent manifolds, directly precipitating task failure. In contrast, _OpenVLA-Base_ (Row 2) maintains high feature overlap under similar perturbations. This divergence indicates that distribution biases within the _Libero-object_ dataset drive _OpenVLA-Libero_ to learn spurious language-vision correlations rather than robust semantic representations. 

**Type II: Spurious Invariance vs. Binding Collapse.** Un- 

6 

### **Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 


_Figure 6._ Visualizing Attention Inertia and Cross-Modal Disconnect: OpenVLA (Top) vs. Pi0 (Bottom). We observe that both models fail to effectively redirect attention when the instruction shifts from Soup” to Butter”. 

der task-critical goal shifts, we distinguish two bottlenecks: 

- **Spurious Invariance (Encoder Failure):** In object replacement (e.g., _Soup → Cheese_ , Column 3-4), all models exhibit significant latent overlap with the original states. This implies the encoders remain invariant to critical visual cues, causing the policy to erroneously persist with the original action plan. 

- **Binding Collapse (Representation or Decoder Failure):** Conversely, for “New Tasks” (Column 5), _OpenVLALibero_ can project OOD states onto distinct latent manifolds. However, latent separability does not guarantee correct action generation. Such failures may stem from either encoder-side representation failure, where the fused representation does not preserve task-critical object separability, or decoder-side binding failure, where the decoder cannot map an unseen task composition to valid actions. For example, in _LIBERO-GOAL_ , _π_ 0 can solve seen tasks such as placing the bowl on the stove and placing the bowl on the plate, but fails on the unseen composition of placing the plate on the stove. 

## **4.3. Path to Generalization** 

To answer **RQ3** , we move beyond black-box optimization and adopt a divide-and-conquer strategy that decouples the vision-language encoder from the policy decoder, applying targeted structural interventions to each component. 

**Regularizing Representation Space (** _fθf_ **): Balancing Invariance and Sensitivity.** To mitigate Type I instability and Type II spurious invariance, the encoder must effectively marginalize nuisance variables without sacrificing task-relevant sensitivity. 

- **Consistency Regularization via Augmentation.** We in- 

_Table 2._ Ablation study results. We compare the OpenVLA baseline ( **Origin** ) against the model fine-tuned on LIBERO-Gen ( **Finetuning** ) and training with data augmentation ( **Enhanced** ). 

|**Regime**|**Origin**|**Fine-**|**tuning**<br>|**Enh**|**anced**<br>|
|---|---|---|---|---|---|
||Acc.|Acc.|∆|Acc.|∆|
||**_Dimen_**|**_sion: B_**|**_ackgroun_**|**_d_**||
|_k_1(ID)|99.6|98.8|-0.8|**99.6**|0.0|
|_k_2(CG)|94.0|**99.6**|+5.6|98.8|+4.8|
|_k_3(DG)|99.4|**99.6**|+0.2|98.8|-0.6|
|<br>|**_Dime_**|**_nsion: L_**|**_anguag_**|**_e_**<br>||
|_k_1(ID)|0.0|91.4|+91.4|**98.5**|+98.5|
|_k_2(CG)|0.0|90.2|+90.2|**99.2**|+99.2|
|_k_3(DG)|39.2|88.0|+48.8|**98.6**|+59.4|
||**_Dim_**|**_ension:_**|**_Object_**|||
|_k_1(ID)|67.2|**78.4**|+11.2|86.2|+19.0|
|_k_2(CG)|63.8|**81.8**|+18.0|88.0|+24.2|
|_k_3(DG)|52.0|**66.0**|+14.0|78.4|+26.4|


troduce a modality-specific consistency loss to enforce logical constraints on the latent manifold. Formally, we optimize for invariance against nuisance perturbations augnuis (i.e., _fθf_ (augnuis( _x_ )) _≈ fθf_ ( _x_ )) while maximizing divergence under critical state shifts _δ_ crit (i.e., _∥fθf_ ( _x_ + _δ_ crit) _− fθf_ ( _x_ ) _∥ > ϵ_ ). As shown in Table 2, this explicitly decouples visual noise from semantic content, significantly enhancing robustness against background and linguistic distractions without requiring additional action labels. 

- **Architectural Insight: Cross-Modal Filtering.** Embodied control demands strict instruction-conditional filtering. However, Figure 6 reveals that VLA exhibits “attention inertia”: altering the target (e.g., _Soup → Cheese_ ) fails to redirect visual focus. We attribute this to the naive to- 

7 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

ken concatenation used in baselines, which lacks explicit feature interaction. To structurally prevent such spurious correlations, we advocate for dense _cross-modal attention_ mechanisms to dynamically re-weight visual patches conditional on linguistic intent. 

We further corroborate this diagnosis through a **linear probing analysis** on the model’s fused hidden states, as show in Figure 7. By training classifiers to predict the target object specified by the instruction, we uncover a catastrophic _binding collapse_ : despite balanced evaluation samples, the model yields **0.00% accuracy** on specific object categories (e.g., _Milk_ , _Butter_ ), while consistently misclassifying diverse inputs as high-saliency objects (e.g., _Cookies_ , _Ketchup_ ). This “mode collapse” in the feature space confirms that naive token concatenation fails to suppress task-irrelevant visual signals. 


_Figure 7._ Linear Probing Analysis of Cross-Modal Binding. The chart displays the recognition accuracy (left, green) versus the sample count (right, red) for each object category. 

**Enhancing Action Binding.** Generalization in the decoder requires robustly binding novel features to valid action sequences. We address this through improved data topology and output space formulation. 

- **Structured Data Sampling:** Addressing the intractability of covering real-world diversity, we conducted a controlled comparison between random sampling and our structured “Stair” sampling under identical data budgets. As illustrated in Figure 8, the structured approach yields significant gains over random sampling. For example, pi0.5 improves from 52.3% to 64.0% in Position generalization and from 14.2% to 21.2% in Task generalization. This demonstrates that the topological structure of “Stair” sampling creates a more uniform variable exposure, preventing the decoder from overfitting to sampling biases and thereby facilitating the learning of generalized control rules rather than memorizing dominant modes. 

- **Continuous vs. Discrete Action Modeling.** Empirical results highlight the autoregressive **OpenVLA** fails completely on Task generalization ( **0.0%** ), exhibiting se- 


_Figure 8._ Generalization Comparison under Different Sampling Strategies. We compare the performance of models trained using **Random** (yellow) versus structured **Stair** (green) sampling strategies across Position and Task generalization. 

vere “Binding Collapse.” In contrast, the continuous flowmatching **Pi0.5** retains significantly higher robustness. While acknowledging that disparate model capacities and pre-training data confound a strictly controlled comparison, these results suggest that continuous trajectory modeling enables smoother interpolation and superior adaptation compared to rigid discrete binning. 

# **5. Related Work** 

**Vision-Language-Action Models.** Vision-language-action (VLA) models have emerged as a unifying paradigm for embodied intelligence, enabling robotic agents to map visual observations and language instructions into executable actions (Kim et al., 2024; Black et al., 2024; Bu et al., 2025; Qu et al., 2025; Cen et al., 2025; Li et al., 2025; Liu et al., 2025; Sun et al., 2025; Deng et al., 2025; Ma et al., 2025). Beyond individual policy architectures, recent studies also explore agentic robot frameworks, embodied AI development workflows, and broader language-modelbased robotics systems (Yang et al., 2025b; Zhou et al., 2026; Zeng et al., 2023). In parallel, post-training techniques have become increasingly important for adapting large foundation models to downstream tasks (Tie et al., 2025). Despite this rapid progress, the field still faces a critical bottleneck: current evaluation protocols often fail to predict real-world reliability (Yang et al., 2025a; Sun et al., 2024; Zhang et al., 2025b; Jain et al., 2025). Bridging the gap between simulation performance and physical deployment therefore requires standardized benchmarks that can diagnose not only whether a model succeeds, but also under what type of distributional shift it fails. 

**Benchmarks for VLA Evaluation.** To support systematic evaluation, various benchmarks (Fan et al., 2026; Guruprasad et al., 2024; Sedlacek et al., 2025; Mees et al., 2022; Walke et al., 2023) have been proposed, including RLBench (James et al., 2020), VLABench (Zhang et al., 2025c), RoboTwin (Mu et al., 2024), and VLA-Arena (Zhang et al., 

8 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

2025a). Among them, LIBERO (Liu et al., 2023) has established itself as a de facto standard for VLA evaluation. Its standardized task suites and unified reporting metrics have enabled fair comparison across models and have made it a primary benchmark in recent VLA research. 

Recent benchmarks have further extended VLA evaluation toward robustness, out-of-distribution behavior, and broader generalization. LIBERO-Plus (Fei et al., 2025) focuses on perturbation robustness by introducing heuristic variations to existing tasks. THE COLOSSEUM (Pumacay et al., 2024) evaluates manipulation robustness under environmental and physical changes. AGNOSTOS (Zhou et al., 2025a) studies cross-task generalization by testing policies on unseen tasks, while INT-ACT (Fang et al., 2025a) examines the gap between intention understanding and action execution under unseen objects and language variations. RoboTwin (Mu et al., 2024), as a domain-randomizationrelated benchmark, evaluates policy robustness under broad unseen variations in objects, layouts, and environments. These benchmarks are valuable for exposing model fragility from different perspectives, but their notions of OOD and generalization are often defined through heuristic unseen cases, such as unseen perturbations, unseen tasks, unseen objects, unseen language instructions, or environmental changes. 

**Robustness and Generalization Gaps.** While robustnessoriented benchmarks such as LIBERO-Pro (Zhou et al., 2025d) and VLA-Arena (Zhang et al., 2025a) have advanced VLA evaluation by introducing environmental perturbations, distractors, and real-world variations, they typically treat training-unseen cases as a broad OOD category. Related security studies further reveal that multimodal and VLA systems can be vulnerable to adversarial or backdoor attacks (Zhou et al., 2025c; Cai et al., 2026). Such evaluations and analyses are effective for exposing model fragility, but they do not explicitly characterize the distributional structure behind different generalization failures. 

LIBERO-Gen complements these benchmarks by evaluating VLA generalization under controlled data-distribution assumptions. Instead of treating all unseen cases uniformly, it distinguishes in-distribution generalization (ID), compositional generalization (CG), and domain generalization (DG), enabling a more fine-grained diagnosis of when and why VLA models fail to generalize. 

# **6. Conclusion** 

We challenge the ”illusion of competence” in current VLA evaluation by introducing LIBERO-Gen, which exposes mechanical memorization through rigorous, hierarchical probing. By decomposing policy failures, we show that a divide-and-conquer strategy combining structured data 

sampling with continuous flow-matching decoders such as Pi0 outperforms discrete baselines, providing a verifiable path toward robust embodied generalization. 

# **Acknowledgements** 

National Natural Science Foundation of China (NSFC) under Grant No. 62476107. 

# **Impact Statement** 

We present LIBERO-Gen, a theory-grounded evaluation framework based on compositional generalization for assessing the reliability of Vision-Language-Action (VLA) models under controlled distribution shifts. Rather than claiming to replace real-robot evaluation, LIBERO-Gen provides a more structured and validity-oriented protocol for measuring generalization within constrained dataset settings. By systematically varying objects, scenes, instructions, and task compositions, LIBERO-Gen uncovers the Generalization Mirage: high benchmark scores can coexist with pronounced fragility under distribution shifts. Our results suggest that part of the observed performance may arise from spurious training-set correlations rather than transferable physical competence. The proposed protocols therefore serve as a diagnostic tool to better separate memorizationdriven behavior from robust policy learning, while also surfacing recurring failure modes in discrete action modeling, such as Binding Collapse. Overall, our study provides empirical evidence toward narrowing the gap between simulation-based metrics and physical utility, and motivates deployment criteria that combine controlled generalization evaluation with real-world robot development. 

# **References** 

- Besserve, M., Sun, R., Janzing, D., and Scholkopf,¨ B. A theory of independent mechanisms for extrapolation in generative models. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 35, pp. 6741–6749, 2021. 

- Black, K., Brown, N., Driess, D., et al. _π_ 0: A visionlanguage-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Bu, Q., Yang, Y., Cai, J., et al. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 

- Cai, X., Liu, D., Qu, X., Fang, X., Dong, J., Tang, K., Zhou, P., Sun, L., and Hu, W. Towards building model/prompttransferable attackers against large vision-language models. _Advances in Neural Information Processing Systems_ , 38:174022–174058, 2026. 

9 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

- Cen, J., Yu, C., Yuan, H., et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 

- Deng, S., Yan, M., Wei, S., et al. Graspvla: a grasping foundation model pre-trained on billion-scale synthetic action data. _arXiv preprint arXiv:2505.03233_ , 2025. 

- Fan, C. K., Chi, X., Ju, X., Li, H., Bao, Y., Wang, Y. K., others, and Tang, J. Wow, wo, val! a comprehensive embodied world model evaluation turing test. _arXiv preprint arXiv:2601.04137_ , 2026. 

- Fang, I., Zhang, J., Tong, S., and Feng, C. From intention to execution: Probing the generalization boundaries of vision-language-action models. _arXiv preprint arXiv:2506.09930_ , 2025a. 

- Fang, I., Zhang, J., Tong, S., and Feng, C. From intention to execution: Probing the generalization boundaries of vision-language-action models. _arXiv preprint arXiv:2506.09930_ , 2025b. 

- Fei, S., Wang, S., Shi, J., Dai, Z., Cai, J., Qian, P., Ji, L., He, X., Zhang, S., Fei, Z., Fu, J., Gong, J., and Qiu, X. LIBERO-Plus: In-depth robustness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 

- Fu, J., Zhang, Z., Lu, Y., and Zheng, N. A general theory for compositional generalization. _arXiv preprint arXiv:2405.11743_ , 2024. 

- Gao, J., Xie, A., Xiao, T., Finn, C., and Sadigh, D. Efficient data collection for robotic manipulation via compositional generalization. _arXiv preprint arXiv:2403.05110_ , 2024. 

- Ge, J., Wang, A., Tang, S., and Jin, C. Principled out-ofdistribution generalization via simplicity. _arXiv preprint arXiv:2505.22622_ , 2025. 

- Guruprasad, P., Sikka, H., Song, J., Wang, Y., and Liang, P. P. Benchmarking vision, language, & action models on robotic learning tasks. _arXiv preprint arXiv:2411.05821_ , 2024. 

- Jain, A., Zhang, M., Arora, K., Chen, W., Torne, M., Irshad, M. Z., others, and Pertsch, K. Polaris: Scalable realto-sim evaluations for generalist robot policies. _arXiv preprint arXiv:2512.16881_ , 2025. 

- James, S., Ma, Z., Arrojo, D. R., and Davison, A. J. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 5(2):3019–3026, 2020. 

- Kim, M. J., Pertsch, K., Karamcheti, S., et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Li, H., Yang, S., Chen, Y., Chen, X., Yang, X., Tian, Y., Wang, H., Wang, T., Lin, D., Zhao, F., et al. Cronusvla: Towards efficient and robust manipulation via multiframe vision-language-action modeling. _arXiv preprint arXiv:2506.19816_ , 2025. 

- Li, X., Hsu, K., Gu, J., Pertsch, K., Mees, O., Walke, H. R., Fu, C., Lunawat, I., Sieh, I., Kirmani, S., et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- Lippl, S. and Stachenfeld, K. When does compositional structure yield compositional generalization? a kernel theory. _arXiv preprint arXiv:2405.16391_ , 2024. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- Liu, Z., Gu, Y., Zheng, S., et al. Trivla: A triple-systembased unified vision-language-action model for general robot control. _arXiv e-prints_ , pp. arXiv:2507.01424, 2025. 

- Ma, X., Yuan, Z., Zhang, Z., Shi, K., Sun, L., and Ye, Y. BLURR: A boosted low-resource inference for vision-language-action models. _arXiv preprint arXiv:2512.11769_ , 2025. 

- Mees, O., Hermann, L., Rosete-Beas, E., and Burgard, W. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3):7327–7334, 2022. 

- Mu, Y., Chen, T., Peng, S., Chen, Z., Gao, Z., Zou, Y., others, and Luo, P. Robotwin: Dual-arm robot benchmark with generative digital twins (early version). In _European Conference on Computer Vision_ , pp. 264–273, Cham, 2024. Springer Nature Switzerland. 

- Nasiriany, S., Maddukuri, A., Zhang, L., Parikh, A., Lo, A., Joshi, A., Mandlekar, A., and Zhu, Y. Robocasa: Largescale simulation of everyday tasks for generalist robots. _arXiv preprint arXiv:2406.02523_ , 2024. 

- Pumacay, W., Singh, I., Duan, J., Krishna, R., Thomason, J., and Fox, D. THE COLOSSEUM: A benchmark for evaluating generalization for robotic manipulation. In _Proceedings of Robotics: Science and Systems_ , 2024. 

- Qu, D., Song, H., Chen, Q., et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- Sedlacek, M., Yefanov, P., Ponimatkin, G., Bardhan, J., Pilc, S., Fourmy, M., others, and Petrik, V. Realm: A realto-sim validated benchmark for generalization in robotic manipulation. _arXiv preprint arXiv:2512.19562_ , 2025. 

10 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

- Sun, F., Chen, R., Ji, T., Luo, Y., Zhou, H., and Liu, H. A comprehensive survey on embodied intelligence: Advancements, challenges, and future perspectives. _CAAI Artificial Intelligence Research_ , 3(9150042):1, 2024. 

- Sun, L., Xie, B., Liu, Y., et al. Geovla: Empowering 3d representations in vision-language-action models. _arXiv preprint arXiv:2508.09071_ , 2025. 

- Tie, G., Zhao, Z., Song, D., Wei, F., Zhou, R., Dai, Y., Yin, W., Yang, Z., Yan, J., Su, Y., Dai, Z., Xie, Y., Cao, Y., Sun, L., Zhou, P., He, L., Chen, H., Zhang, Y., Wen, Q., Liu, T., Gong, N. Z., Tang, J., Xiong, C., Ji, H., Yu, P. S., and Gao, J. A survey on post-training of large language models. _arXiv preprint arXiv:2503.06072_ , 2025. 

- Walke, H. R., Black, K., Zhao, T. Z., Vuong, Q., Zheng, C., Hansen-Estruch, P., He, A. W., Myers, V., Kim, M. J., Du, M., et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pp. 1723–1736. PMLR, 2023. 

- Wiedemer, T., Mayilvahanan, P., Bethge, M., and Brendel, W. Compositional generalization from first principles. _Advances in Neural Information Processing Systems_ , 36: 6941–6960, 2023. 

- Yang, X., Eppner, C., Tremblay, J., Fox, D., Birchfield, S., and Ramos, F. Robot policy evaluation for sim-to-real transfer: A benchmarking perspective. _arXiv preprint arXiv:2508.11117_ , 2025a. 

   - Zhang, S., Xu, Z., Liu, P., Yu, X., Li, Y., Gao, Q., others, and Qiu, X. Vlabench: A large-scale benchmark for language-conditioned robotics manipulation with longhorizon reasoning tasks. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 11142– 11152, 2025c. 

   - Zhou, J., Ye, K., Liu, J., Ma, T., Wang, Z., Qiu, R., Lin, K.-Y., Zhao, Z., and Liang, J. Exploring the limits of vision-language-action manipulations in cross-task generalization. _arXiv preprint arXiv:2505.15660_ , 2025a. 

   - Zhou, J., Ye, K., Liu, J., Ma, T., Wang, Z., Qiu, R., others, and Liang, J. Exploring the limits of vision-languageaction manipulations in cross-task generalization. _arXiv preprint arXiv:2505.15660_ , 2025b. 

   - Zhou, X., Tie, G., Zhang, G., Wang, H., Zhou, P., and Sun, L. BadVLA: Towards backdoor attacks on visionlanguage-action models via objective-decoupled optimization. _arXiv preprint arXiv:2505.16640_ , 2025c. 

   - Zhou, X., Xu, Y., Tie, G., Chen, Y., Zhang, G., Chu, D., and Sun, L. LIBERO-PRO: Towards robust and fair evaluation of vision-language-action models beyond memorization. _arXiv preprint arXiv:2510.03827_ , 2025d. 

   - Zhou, X., Sun, Y., Gong, X., Tie, G., Zhou, P., Sun, L., and Chen, Y. EmbodiedClaw: Conversational workflow execution for embodied ai development. _arXiv preprint arXiv:2604.13800_ , 2026. 

- Yang, Z., Chen, Y., Zhou, X., Yan, J., Song, D., Liu, Y., Li, Y., Zhang, Y., Zhou, P., Chen, H., and Sun, L. Agentic robot: A brain-inspired framework for visionlanguage-action models in embodied agents. _arXiv preprint arXiv:2505.23450_ , 2025b. 

- Ye, H., Xie, C., Cai, T., Li, R., Li, Z., and Wang, L. Towards a theoretical framework of out-of-distribution generalization. _Advances in Neural Information Processing Systems_ , 34:23519–23531, 2021. 

- Zeng, F., Gan, W., Huai, Z., Sun, L., Chen, H., Wang, Y., Liu, N., and Yu, P. S. Large language models for robotics: A survey. _arXiv preprint arXiv:2311.07226_ , 2023. 

- Zhang, B., Li, J., Shen, J., Cai, Y., Zhang, Y., Chen, Y., others, and Yang, Y. Vla-arena: An open-source framework for benchmarking vision-language-action models. _arXiv preprint arXiv:2512.22539_ , 2025a. 

- Zhang, K., Sha, S., Jiang, H., Loper, M., Song, H., Cai, G., et al. Real-to-sim robot policy evaluation with gaussian splatting simulation of soft-body interactions. _arXiv preprint arXiv:2511.04665_ , 2025b. 

11 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

# **A. Theory** 

## **A.1. Compositional Generalization** 

We extend the formalization of compositional generalization (CG) for Vision-Language-Action (VLA) policies by deriving sufficient conditions for its emergence and theoretical error bounds, integrating core insights from kernel theory (Lippl & Stachenfeld, 2024), general CG frameworks (Fu et al., 2024), and compositional data-generating process analysis (Wiedemer et al., 2023). 

## A.1.1. SUFFICIENT CONDITIONS FOR COMPOSITIONAL GENERALIZATION 

For a VLA policy _πθ_ to exhibit CG, the following conditions must hold, ensuring alignment between the policy’s inductive biases, the task-context structure, and the training data’s statistical properties: 

**Compositional Structured Representations** The policy’s latent representation _ϕ_ ( _τ, c_ ) (mapping task-context tuples _x_ = ( _τ, c_ 1 _, c_ 2 _, ..., cn_ ) to feature space) must be compositionally structured. Formally, the kernel induced by _ϕ_ , _K_ (( _τ, c_ ) _,_ ( _τ_<sup>_′_</sup> _, c_<sup>_′_</sup> )) = _ϕ_ ( _τ, c_ )<sup>_T_</sup> _ϕ_ ( _τ_<sup>_′_</sup> _, c_<sup>_′_</sup> ), depends only on the number of identical causal factors between ( _τ, c_ ) and ( _τ_<sup>_′_</sup> _, c_<sup>_′_</sup> )—where causal factors include the abstract task semantics _τ_ and independent context factors _ci_ (e.g., visual appearance, object identities). This ensures generalization relies on compositional similarity rather than spurious correlations. Such representations conserve compositional structure through nonlinear transforms: for random weight neural networks in the infinite-width limit, the kernel of the transformed representation depends only on the input kernel, preserving the compositional structure of the input (Lippl & Stachenfeld, 2024). 

**Sufficient Support of Training Distribution** The training set _D_ train must have sufficient compositional support with respect to the joint task-context space _T × C_ , where _C_ = _C_ 1 _× C_ 2 _× · · · × Cn_ denotes the joint context space. First, for every task _τ ∈_ proj _T_ ( _D_ train), there exist contexts _c_<sup>(1)</sup> _, ..., c_<sup>(</sup><sup>_k_)</sup> _∈C_ such that the subset _{_ ( _τ, c_<sup>(1)</sup> ) _, ...,_ ( _τ, c_<sup>(</sup><sup>_k_)</sup> ) _} ⊆D_ train covers all marginal contexts _ci ∈_ proj _Ci_ ( _D_ train). Second, for every context factor _ci ∈_ proj _Ci_ ( _D_ train), the training set includes pairs ( _τ_<sup>(1)</sup> _, c_ ) and ( _τ_<sup>(2)</sup> _, c_ ) (for distinct _τ_<sup>(1)</sup> _, τ_<sup>(2)</sup> ) to disentangle task semantics from context. The support must be an open set, and for any latent configuration of a component, there exists a finite subset of training points such that the sum of the derivatives of the composition function (mapping component representations to final outputs) has full rank—ensuring sufficient variability to reconstruct component-specific behaviors without ambiguity (e.g., resolving occlusions in visual contexts by observing multiple configurations) (Wiedemer et al., 2023). 

**Conjunction-Wise Additive Computation** The policy’s action mapping must be conjunction-wise additive. For any test tuple ( _τ, c_ ) _∈D_ eval<sup>(1)(composed of novel combinations of seen factors), the policy’s output satisfies:</sup> 


Here, _J_ denotes a subset of causal factors (task + context), Conj(( _τ, c_ ) _| D_ train) is the set of factor conjunctions observed in _D_ train (i.e., _J ⊆{_ 1 _, ..., n_ + 1 _}_ where there exists ( _τ_<sup>_tr_</sup> _, c_<sup>_tr_</sup> ) _∈D_ train such that _τJ_ = _τJ_<sup>_tr_and</sup><sup>_cJ_=</sup><sup>_ctr_</sup> _J_<sup>for all indices in</sup><sup>_J_),</sup> and _fJ_ are task-context agnostic functions mapping conjunctions of factors to action contributions. This form means the policy generalizes by combining learned factor-specific behaviors, avoiding memorization of spurious task-context pairs. For kernel models with compositionally structured representations, this additive form is a fundamental constraint—they cannot learn non-additive tasks (e.g., transitive equivalence relations requiring _A_ = _B_ and _B_ = _C_ implies _A_ = _C_ ) as these demand reasoning beyond summing observed conjunctions (Lippl & Stachenfeld, 2024). 

**Minimal Mutual Information with Spurious Rules** The policy’s latent representation _ϕ_ ( _τ, c_ ) must minimize mutual information with spurious correlations between input features and the target (shortcut bias) given the training distribution _D_ train. Formally: 


for a small _δ >_ 0, where _T_ spurious denotes spurious compositional rules (e.g., associating ”pick” tasks exclusively with red objects). This avoids shortcut learning, where models exploit task-irrelevant correlations that do not hold in novel combinations—such as over-reliance on context cues that predict the target in training data but fail in _D_ eval<sup>(1)(Fu et al., 2024).</sup> 

12 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

## A.1.2. ERROR BOUND FOR COMPOSITIONAL GENERALIZATION 

We derive a generalization error bound for _πθ_ on _D_ eval<sup>(1), integrating IID generalization bounds and the information-theoretic</sup> analysis from (Fu et al., 2024) and (Lippl & Stachenfeld, 2024): 

**Theorem A.1** Let _πθ_ be a VLA policy satisfying Conditions 1–4 above. Let _err_ ( _πθ_ ; _D_ ) denote the expected execution error (1 - Succ( _τ_ )) of _πθ_ on distribution _D_ , and assume _err_ ( _πθ_ ; _·_ ) is _L_ -bounded (i.e., 0 _≤ err_ ( _πθ_ ; _D_ ) _≤ L_ for all _D_ ). Let Gen _IID_ denote any IID generalization bound (e.g., Rademacher complexity, uniform stability) for _πθ_ on _D_ train. Then: 

E( _τ,c_ ) _∼D_ eval(1)<sup>[</sup><sup>_err_(</sup><sup>_πθ_; (</sup><sup>_τ, c_))]</sup><sup>_≤_Gen</sup><sup>_IID_+</sup><sup>_κnL_Φ (</sup><sup>_I_(</sup><sup>_ϕ_(</sup><sup>_τ, c_);</sup><sup>_T_spurious</sup><sup>_| D_train)) + Erradd +</sup><sup>_O_(</sup><sup>_ϵ_0)</sup> 

where: 

- _<u>|</u>_ E _D_ <u>train [</u> _err_ <u>(</u> _πθ_ ; _D_ <u>eval</u><sup>(1))</sup><sup>_−err_</sup><sup><u>(</u></sup><sup>_πθ_;</sup><sup>_D_train)]</sup><sup>_<u>|</u>_</sup> 

- • _κn_ = quantifies data efficiency, with _κn →_ 1 as _|D_ train _| →∞_ (capturing convergence _|_ err( _πθ_<sup>_∗_;</sup><sup>_D_</sup> eval<sup>(1))</sup><sup>_−_err(</sup><sup>_π_</sup> _θ_<sup>_∗_;</sup><sup>_D_train)</sup><sup>_|_</sup> 

- of finite-sample training to infinite-data performance), 

- Φ( _x_ ) = ~~�~~ min _{x/_ 2 _,_ 1 _−_ exp( _−x_ ) _}_ is an information-theoretic penalty term for shortcut bias, 

- <u>(</u> _<u>p−</u>_ 2) _S_ <u>(1;</u> _n_ <u>+1)</u> 

- • Erradd = 1+( _p−_ 2) _S_ (1; _n_ +1)<sup>_· ϵ_train is the memorization leak penalty—here,</sup><sup>_p_=</sup><sup>_|_proj</sup><sup>_T_(</sup><sup>_D_train)</sup><sup>_|_+ �</sup> _i_<sup>_n_</sup> =1<sup>_|_proj</sup> _Ci_<sup>(</sup><sup>_D_train)</sup><sup>_|_</sup> denotes the size of observed factor values, _S_ (1; _n_ + 1) is the representational salience of individual factors (normalized contribution of single-component conjunctions to the representation, with saliences _S_ ( _k_ ; _C_ ) summing to 1 across all conjunction sizes _k_ ), and _ϵ_ train = E( _τ,c_ ) _∼D_ train [ _err_ ( _πθ_ ; ( _τ, c_ ))] is the training error, 

- _ϵ_ 0 = max( _τ,c_ ) _∈T ×C_ min _π err_ ( _π_ ; ( _τ, c_ )) is the Bayes error of the VLA task, capturing inherent task difficulty (e.g., physical constraints on action execution). 

**Interpretation of Error Components** The bound consists of four key terms: 

- Gen _IID_ is the standard generalization error from fitting the training distribution, decreasing with larger training set size and lower model complexity. 

- _κnL_ Φ( _I_ ( _·_ ; _·_ )) is the penalty for shortcut bias, increasing with mutual information between the representation and spurious rules—this term vanishes as the policy avoids relying on task-irrelevant correlations. 

- Erradd is the penalty for memorization leak, where the model partially relies on full conjunctions (rather than individual components) during training, distorting generalization. This term decreases as _S_ (1; _n_ + 1) (salience of individual factors) increases (e.g., in disentangled representations) and as training set size _p_ grows (reducing the model’s need to rely on conjunctions for fitting). 

- _O_ ( _ϵ_ 0) is the inherent error floor from task difficulty, representing the minimal achievable error for any VLA policy. 

## A.1.3. DISCUSSION 

**Necessity of Conditions** Violating any condition leads to CG failure: unstructured representations enable shortcut learning by conflating spurious correlations with compositional structure; insufficient support prevents factor disentanglement (e.g., a context factor paired with only one task cannot be generalized to others); non-additive computations block generalization to novel conjunctions; and high mutual information with spurious rules degrades out-of-distribution performance. 

**Practical Implications** The bound highlights that CG performance improves with three key factors: (1) larger training sets, which reduce Gen _IID_ and _κn_ ; (2) more disentangled representations, which increase _S_ (1; _n_ + 1) and reduce Erradd; (3) lower mutual information with spurious rules, which reduces Φ( _I_ ( _·_ ; _·_ )). For deep neural networks (e.g., ConvNets, ResNets, Vision Transformers), these insights hold qualitatively: deeper networks tend to encode full conjunctions (lower _S_ (1; _C_ )) and suffer more from memorization leak, while increased spatial separation between components in inputs boosts _S_ (1; _C_ ) and improves generalization. Additionally, context-dependent tasks with strong spurious correlations (e.g., context predicting most training targets) are more sensitive to architectural choices (depth, nonlinearity) that shape representational geometry, aligning with observations that shortcut bias is task-dependent. 

13 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

## **A.2. Domain Generalization** 

## A.2.1. INDEPENDENT MECHANISMS IN VLA SETTINGS 

We formalize the **Independent Mechanisms (IM)** principle for VLA policies, aligning with the causal framework in (Besserve et al., 2021) and extending it to Vision-Language-Action triples. A VLA system’s generative process is governed by a set of latent causal mechanisms _{Mj}_<sup>_J_</sup> _j_ =1<sup>, where each</sup><sup>_Mj_corresponds to a modular component of task execution:</sup> 

- _M_ 1: Task semantics (e.g., goal specification, sub-task decomposition), 

- _M_ 2: Object dynamics (e.g., physical interactions between objects), 

- _M_ 3: Language grounding (e.g., mapping natural language to actionable goals), 

- _M_ 4: Visual appearance (e.g., object textures, lighting, camera viewpoints), 

- _M_ 5: Action execution (e.g., mapping policy outputs to motor commands). 

The Independent Mechanisms principle imposes three key conditions on these mechanisms. First, conditional independence requires that for any two distinct mechanisms _Mj_ and _Mk_ , the conditional distribution of their outputs is independent given their respective causal parents. Here, _P_ ( _·_ ) denotes a probability distribution, and Pa( _M_ ) denotes the set of causal parent nodes of mechanism _M_ in the causal graph, which means _P_ ( _Mj_ ( _·_ ) _|_ Pa( _Mj_ )) _⊥⊥ P_ ( _Mk_ ( _·_ ) _|_ Pa( _Mk_ )). Second, modular invariance ensures that interventions on one mechanism such as altering visual appearance do not disrupt the functionality of other mechanisms, meaning task semantics for instance remain unchanged. Third, structural consistency dictates that all domains _e ∈E_ all share the same causal graph structure of mechanisms, with differences only arising in the instantiation of mechanism parameters. For example, parameters of the visual appearance mechanism _M_ 4 may vary across lighting conditions, while parameters of the task semantics mechanism _M_ 1 remain fixed for a given task _τ_ . This definition extends the work of (Besserve et al., 2021) by explicitly incorporating VLA-specific mechanisms (language grounding and action execution) and linking mechanism modularity to domain shifts. Unseen visual appearances for example correspond to intervened parameters of _M_ 4. 

## A.2.2. DOMAIN GENERALIZATION ERROR BOUNDS 

We derive error bounds for VLA domain generalization, building on the expansion function framework by (Ye et al., 2021) and the simplicity principle by (Ge et al., 2025). Our focus is on the worst-case error across unseen domains, which captures robustness to out-of-support mechanism instantiations. 

**Notation** We denote the VLA policy as _πθ_ ( _at | ot, l, e_ ), which maps observations _ot_ , language _l_ , and domain _e_ to actions _at_ . The mechanism variation of _πθ_ , denoted _V_ ( _πθ, E_ train), refers to the maximum difference in policy behavior across training domains, measured by the Total Variation (TV) distance between action distributions induced by different mechanism instantiations. The expansion function _s_ : R<sup>+</sup> _→_ R<sup>+</sup> —as defined by (Ye et al., 2021)—characterizes how mechanism variation amplifies from training to unseen domains, with properties of being monotonically increasing, satisfying _s_ ( _x_ ) _≥ x_ , and approaching 0 as _x_ approaches 0. Finally, the informativeness of the policy, denoted _δ_ , is the minimum TV distance between action distributions for distinct task semantics, ensuring the policy does not rely on spurious domain-specific cues. 

**Theorem B.1 (Worst-Case Domain Generalization Error Bound)** Suppose the VLA system satisfies Definition A.1 (Independent Mechanisms), and the domain generalization problem is ( _s_ ( _·_ ) _, δ_ )-learnable as per (Ye et al., 2021). For a policy _πθ_ with mechanism variation _V_ ( _πθ, E_ train) = _ε_ and informativeness _I_ ( _πθ_ ) _≥ δ_ , the worst-case domain generalization error is bounded by: 


where _d_ represents the dimensionality of the policy’s latent mechanism representations, and _n_ is the number of training samples across _E_ train. The _O_ ( _·_ ) term depends on _δ_ , the Lipschitz constant of the mechanism functions, and the boundedness of the action space. 

**Proof Sketch** The proof unfolds in three key steps. First, the link between mechanism variation and error is established: by virtue of IM modularity, policy error on unseen domains is determined by the deviation of unseen mechanism instantiations 

14 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

from those encountered during training, a deviation captured by _s_ ( _ε_ )—the expanded variation from training to evaluation domains as defined by (Ye et al., 2021). Second, the sample complexity term<sup>lo</sup> _~~√~~_<sup><u>g</u></sup> _<u>n</u>_<sup>_d_arises from the statistical error associated</sup> with estimating mechanism parameters from finite training data, aligning with the simplicity principle by (Ge et al., 2025), which posits that simple mechanisms with low variation can be estimated more accurately. Third, the informativeness constraint _I_ ( _πθ_ ) _≥ δ_ ensures the policy relies on invariant task semantics rather than spurious domain cues, preventing error amplification from uninformative mechanisms as noted by (Ye et al., 2021). 

**Corollary B.2 (Linear Error Bound for Linear Policies)** When the policy’s mechanism mappings are linear—such as linear language grounding or linear action projection—the expansion function takes the form _s_ ( _x_ ) = _kx_ where _k ≥_ 1 is a constant, simplifying the error bound to: 


This result aligns with the linear top-model bound by (Ye et al., 2021), demonstrating that linear mechanisms lead to predictable error scaling with variation. 

# **B. Additional Experiments** 

## **B.1. Confidence Interval Analysis for Main Results** 

To verify that our conclusions are not caused by evaluation randomness, we perform an additional statistical analysis based on repeated evaluations. All main results reported in Tables 1 and 2 are averaged over 50 independent evaluation runs. For each setting, we compute the sample variance and the 95% confidence interval. Unless otherwise specified, each confidence interval is reported as the mean plus/minus the half-width of the 95% confidence interval. Table 3 presents representative confidence intervals for the _π_ 0 and _π_ 0 _._ 5 results in Table 1. Across different perturbation groups, most confidence intervals are narrow, indicating that the observed performance trends are stable across repeated evaluations. This further supports the reliability of the main conclusions. 

_Table 3._ Representative 95% confidence intervals for the _π_ 0 and _π_ 0 _._ 5 results in Table 1. Each entry is reported as mean _±_ half-width of the 95% confidence interval over 50 independent evaluation runs. 

|**Group**|**Ind**|**ex 0**|**Ind**|**ex 1**|**Ind**|**ex 2**|
|---|---|---|---|---|---|---|
||**_π_0**|**_π_0****_._5**|**_π_0**|**_π_0****_._5**|**_π_0**|**_π_0****_._5**|
|position|0_._95_±_0_._03|0_._98_±_0_._03|0_._07_±_0_._02|0_._62_±_0_._04|0_._05_±_0_._02|0_._25_±_0_._05|
|task|0_._98_±_0_._02|0_._99_±_0_._01|0_._14_±_0_._03|0_._20_±_0_._03|0_._40_±_0_._05|0_._52_±_0_._06|
|object|0_._91_±_0_._03|0_._99_±_0_._02|0_._98_±_0_._02|1_._00_±_0_._00|0_._88_±_0_._04|1_._00_±_0_._01|
|texture|0_._97_±_0_._02|1_._00_±_0_._01|0_._96_±_0_._02|1_._00_±_0_._00|0_._99_±_0_._02|1_._00_±_0_._00|
|language|0_._99_±_0_._02|1_._00_±_0_._01|0_._98_±_0_._02|1_._00_±_0_._01|0_._95_±_0_._04|0_._99_±_0_._01|


## **B.2. Statistical Significance of Stair vs. Random** 

We further evaluate whether the advantage of STAIR over RANDOM in Fig. 8 is statistically reliable. Tables 4 and 5 summarize the mean, sample variance, and 95% confidence interval under the position and task settings, respectively. 

_Table 4._ Statistical comparison between STAIR and RANDOM under the position setting. 

|**Method**|**Mean**|**Sample Variance**|**95% Confidence Interval**|
|---|---|---|---|
|_π_0_._5-STAIR|0_._64|5_._000_×_10<sup>_−_3</sup><br>|[0_._607_,_0_._673]|
|_π_0_._5-RANDOM|0_._52|2_._000_×_10<sup>_−_3</sup><br>|[0_._499_,_0_._541]|
|OpenVLA-STAIR|0_._26|1_._286_×_10<sup>_−_4</sup>|[0_._2547_,_0_._2653]|
|OpenVLA-RANDOM|0_._02|4_._000_×_10<sup>_−_7</sup>|[0_._0197_,_0_._0203]|


The results show that STAIR consistently outperforms RANDOM. For _π_ 0 _._ 5, the improvement is statistically significant under both the position setting and the task setting, with _p_ = 3 _._ 24 _×_ 10<sup>_−_7</sup> and _p_ = 1 _._ 91 _×_ 10<sup>_−_4</sup> , respectively. For OpenVLA, the improvement is also statistically significant under the position setting, with _p_ = 5 _._ 37 _×_ 10<sup>_−_27</sup> . Under the task setting, both 

15 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

_Table 5._ Statistical comparison between STAIR and RANDOM under the task setting. 

|**Method**|**Mean**|**Sample Variance**|**95% Confidence Interval**|
|---|---|---|---|
|_π_0_._5-STAIR|0_._21|1_._000_×_10<sup>_−_3</sup>|[0_._195_,_0_._225]|
|_π_0_._5-RANDOM|0_._15|3_._000_×_10<sup>_−_3</sup>|[0_._124_,_0_._176]|
|OpenVLA-STAIR|0_._00|0_._000|[0_._000_,_0_._000]|
|OpenVLA-RANDOM|0_._00|0_._000|[0_._000_,_0_._000]|


OpenVLA variants achieve zero success rate across all 50 runs, so we do not report a significance test for this comparison. Overall, these results confirm that the advantage of STAIR is statistically reliable rather than an artifact of random evaluation noise. 

# **C. LIBERO-Gen Design Details** 

This appendix delineates the granular specifications and data generation protocols for the five evaluation suites constituting the LIBERO-Gen benchmark. We detail the precise construction of the training distributions ( _Dtrain_ ) and the hierarchical evaluation regimes ( _k ∈{_ 0 _,_ 1 _,_ 2 _}_ ) to ensure the reproducibility of the ”Stair” and ”L-shape” sampling strategies discussed in Section 3. 

## **C.1. LIBEROGEN-Texture** 

In this suite, we evaluate the visual invariance of VLA policies by systematically varying the background textures (specifically the floor appearance) while keeping task semantics and object layouts constant. We utilize the 10 atomic object manipulation tasks from LIBERO-Object as the foundation. 


_Figure 9._ Overview of Pattern Designs. 

**Texture Assets.** We curated two disjoint sets of floor texture assets to strictly separate in-distribution (ID) visual features from out-of-distribution (OOD) features, as shown in Figure 9. 

- **Seen Textures (** _Cseen_ **).** Used for training and compositional generalization. The set includes five distinct textures: (1) dark (Dark wood flooring), (2) rustic (Rustic wooden planks), (3) light-gray (Smooth light gray tiling), (4) white-marble (Polished white marble), and (5) wood-plank (Standard wooden deck). 

- **Unseen Textures (** _Cunseen_ **).** Used exclusively for domain generalization ( _k_ = 2). The set includes: (1) brown-ceramic, (2) gray-ceramic, (3) patterned-tile, (4) terrazzo, and (5) red-brick. 

16 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

**Training Distribution): “Stair” Sampling Protocol.** To induce spurious correlations while ensuring sufficient support (as defined in Appendix A), we employ a ”Stair” sampling strategy. We partition the 10 tasks into 5 groups ( _G_ 1 _. . . G_ 5) and bind each group to a sliding window of textures. Specifically, each task group is trained on two adjacent textures from the ordered set _Cseen_ , forming a diagonal band in the task-texture matrix, as shown in Figure 10. The exact training configurations are detailed in Table 6. 

_Table 6._ Training Distribution ( _Dtrain_ ) for LIBEROGEN-Texture with Stair Sampling. Each task group is associated with a sliding window of two textures. 

|**Task Group**|**Tasks Included (Full Instructions)**|**Associated Textures**|
|---|---|---|
|**Group 1**|1. pick<br>~~u~~p<br>~~t~~he<br>~~a~~lphabet<br>~~s~~oup<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket<br>2. pick<br>~~u~~p<br>~~t~~he<br>~~b~~bq<br>~~s~~auce<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|dark,rustic|
|**Group 2**|3. pick<br>~~u~~p<br>~~t~~he<br>~~b~~utter<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket<br>4. pick<br>~~u~~p<br>~~t~~he<br>~~c~~hocolate<br>~~p~~udding<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|rustic,light-gray|
|**Group 3**|5. pick<br>~~u~~p<br>~~t~~he<br>~~c~~ream<br>~~c~~heese<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket<br>6. pick<br>~~u~~p<br>~~t~~he<br>~~k~~etchup<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|light-gray,white-marble|
|**Group 4**|7. pick<br>~~u~~p<br>~~t~~he<br>~~m~~ilk<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket<br>8. pick<br>~~u~~p<br>~~t~~he<br>~~o~~range<br>~~j~~uice<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|white-marble,wood-plank|
|**Group 5**|9. pick<br>~~u~~p<br>~~t~~he<br>~~s~~alad<br>~~d~~ressing<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket<br>10. pick<br>~~u~~p<br>~~t~~he<br>~~t~~omato<br>~~s~~auce<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|wood-plank,dark|


**Evaluation Distribution.** It is important to note that while a robust evaluation in a controlled setting could theoretically involve randomized combinations of tasks and textures, such randomness can introduce variance that hinders direct model comparison. To ensure strict experimental reproducibility and provide a standardized reference for comparison in this paper, we explicitly list the specific evaluation set used in our experiments in Table 7. 

_Table 7._ Fixed Evaluation Set for LIBEROGEN-Texture. We report the specific background textures used for Compositional Generalization (CG, _k_ = 1) and Domain Generalization (DG, _k_ = 2) for each task to guarantee reproducibility. 

|**Task Instruction**|**CG Texture (**_k_ = 1**)**|**DG Texture (**_k_ = 2**)**|
|---|---|---|
|pick<br>~~u~~p<br>~~t~~he<br>~~a~~lphabet<br>~~s~~oup<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|rustic|brown-ceramic|
|pick<br>~~u~~p<br>~~t~~he<br>~~c~~ream<br>~~c~~heese<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|white-marble|brown-ceramic|
|pick<br>~~u~~p<br>~~t~~he<br>~~s~~alad<br>~~d~~ressing<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|dark|tile<br>~~g~~rigia<br>~~c~~aldera|
|pick<br>~~u~~p<br>~~t~~he<br>~~b~~bq<br>~~s~~auce<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|light-gray|gray-ceramic|
|pick<br>~~u~~p<br>~~t~~he<br>~~k~~etchup<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|wood-plank|gray-ceramic|
|pick<br>~~u~~p<br>~~t~~he<br>~~t~~omato<br>~~s~~auce<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|rustic|gray-ceramic|
|pick<br>~~u~~p<br>~~t~~he<br>~~b~~utter<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|rustic|tile<br>~~g~~rigia<br>~~c~~aldera|
|pick<br>~~u~~p<br>~~t~~he<br>~~m~~ilk<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|wood-plank|gray-ceramic|
|pick<br>~~u~~p<br>~~t~~he<br>~~c~~hocolate<br>~~p~~udding<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|white-marble|tile<br>~~g~~rigia<br>~~c~~aldera|
|pick<br>~~u~~p<br>~~t~~he<br>~~o~~range<br>~~j~~uice<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|rustic|gray-ceramic|


## **C.2. LIBEROGEN-Object** 

In this suite, we evaluate the robustness of VLA policies against visual distractors (task-irrelevant objects) while keeping task semantics and object layouts constant. Similar to the texture suite, we utilize the 10 atomic object manipulation tasks from LIBERO-Object as the foundation. 

**Distractor Assets.** We curated two disjoint sets of object assets to strictly separate in-distribution (ID) visual features from out-of-distribution (OOD) features. 

- **Seen Distractors (** _Cseen_ **).** Used for training and compositional generalization. We define 5 distinct distractor configurations, where each configuration consists of 5 instances of a specific object category: (1) akita ~~b~~ lack ~~b~~ owl, (2) glazed ~~r~~ im ~~p~~ orcelain ~~r~~ amekin, (3) moka ~~p~~ ot, (4) porcelain ~~m~~ ug, and (5) wine ~~b~~ ottle. 

17 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 


_Figure 10._ LIBEROGEN-Texture. 

- **Unseen Distractors (** _Cunseen_ **).** Used exclusively for domain generalization ( _k_ = 2). The pool includes 10 object categories: alphabet ~~s~~ oup, bbq ~~s~~ auce, butter, chocolate ~~p~~ udding, cream ~~c~~ heese, ketchup, milk, orange ~~j~~ uice, salad ~~d~~ ressing, and tomato ~~s~~ auce. 

**Training Distribution: ”Stair” Sampling Protocol.** To induce spurious correlations while ensuring sufficient support, we employ the same ”Stair” sampling strategy used in the texture suite. We partition the 10 tasks into 5 groups ( _G_ 1 _. . . G_ 5) and bind each group to a sliding window of distractor configurations. Specifically, each task group is trained with two adjacent distractor configurations from the ordered set _Cseen_ . The exact training configurations are detailed in Table 8. 

**Evaluation Distribution.** Consistent with our protocol for visual textures, we establish a fixed evaluation set to ensure reproducibility. For Compositional Generalization ( _k_ = 1), tasks are paired with seen distractor configurations that were not present in their training window. For Domain Generalization ( _k_ = 2), each task is evaluated against a unique, fixed combination of 5 objects randomly sampled from the _Cunseen_ pool. These fixed sets are listed in Table 9. 

18 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

_Table 8._ Training Distribution ( _Dtrain_ ) for LIBEROGEN-Object with Stair Sampling. Each task group is associated with a sliding window of two distractor configurations (each containing 5 instances of the specified object). 

|**Task Group**|**Tasks Included (Full Instructions)**|**Associated Distractors (5x)**|
|---|---|---|
|**Group 1**|1. pick<br>~~u~~p<br>~~t~~he<br>~~a~~lphabet<br>~~s~~oup<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket<br>2. pick<br>~~u~~p<br>~~t~~he<br>~~b~~bq<br>~~s~~auce<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|akita<br>~~b~~lack<br>~~b~~owl,glazed<br>~~r~~im<br>~~p~~orcelain<br>~~r~~amekin|
|**Group 2**|3. pick<br>~~u~~p<br>~~t~~he<br>~~b~~utter<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket<br>4. pick<br>~~u~~p<br>~~t~~he<br>~~c~~hocolate<br>~~p~~udding<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|glazed<br>~~r~~im<br>~~p~~orcelain<br>~~r~~amekin,moka<br>~~p~~ot|
|**Group 3**|5. pick<br>~~u~~p<br>~~t~~he<br>~~c~~ream<br>~~c~~heese<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket<br>6. pick<br>~~u~~p<br>~~t~~he<br>~~k~~etchup<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|moka<br>~~p~~ot,porcelain<br>~~m~~ug|
|**Group 4**|7. pick<br>~~u~~p<br>~~t~~he<br>~~m~~ilk<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket<br>8. pick<br>~~u~~p<br>~~t~~he<br>~~o~~range<br>~~j~~uice<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket.bddl|porcelain<br>~~m~~ug,wine<br>~~b~~ottle|
|**Group 5**|9. pick<br>~~u~~p<br>~~t~~he<br>~~s~~alad<br>~~d~~ressing<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket.bddl<br>10. pick<br>~~u~~p<br>~~t~~he<br>~~t~~omato<br>~~s~~auce<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|wine<br>~~b~~ottle,akita<br>~~b~~lack<br>~~b~~owl|


## **C.3. LIBEROGEN-Language** 

In this suite, we evaluate the robustness of VLA policies to linguistic variations, specifically testing whether agents rely on syntactic pattern matching or achieve true semantic grounding. We utilize the same 10 atomic tasks from LIBERO-Object but systematically vary the instruction phrasing. 

**Language Assets.** We constructed two disjoint sets of instructions to separate in-distribution (ID) syntactic patterns from out-of-distribution (OOD) semantic and noisy variations. 

- **Seen Templates (** _Cseen_ **).** Used for training and compositional generalization. We designed 5 semantically equivalent but syntactically distinct templates, where _{x}_ denotes the object and _{y}_ denotes the receptacle (e.g., ”the basket”): (1) ”Pick _{x}_ and put it in _{y}_ .” (2) ”Pick up _{x}_ , then place it in _{y}_ .” (3) ”Move _{x}_ into _{y}_ .” (4) ”Put _{x}_ into _{y}_ .” (5) ” _{x}_ should be picked up and placed in _{y}_ .” 

- **Unseen Variations (** _Cunseen_ **).** Used exclusively for domain generalization ( _k_ = 2). For each task, we generated 10 novel instructions using an LLM (GPT-4), comprising 5 _Semantic Paraphrases_ (diverse vocabulary/structure) and 5 _Noisy/Irrelevant Contexts_ (embedded in conversational filler or environmental descriptions). 

**Training Distribution: ”Stair” Sampling Protocol.** To prevent the model from observing all syntactic variations for every task, we employ a ”Stair” sampling strategy. We partition the 10 tasks into 5 groups ( _G_ 1 _. . . G_ 5) and bind each group to a sliding window of instruction templates. Specifically, each task group is trained on only two specific adjacent templates from _Cseen_ . The exact training configurations are detailed in Table 10. 

**Evaluation Distribution.** To ensure reproducibility, we define a fixed evaluation set. For Compositional Generalization ( _k_ = 1), we evaluate tasks using a seen template that was _not_ in their training window (e.g., Group 1 is evaluated on Template 3). For Domain Generalization ( _k_ = 2), we evaluate on the fixed set of 10 unseen variations per task. Table 11 lists the specific CG template and representative DG examples used. 

## **C.4. LIBEROGEN-Position** 

In this suite, we evaluate the spatial reasoning capabilities of VLA policies, specifically testing whether agents can extrapolate learned spatial relationships to novel configurations. Unlike previous suites that vary semantic factors, here we fix the task semantic to ”Pick up the bowl and place it on the plate” and treat the spatial locations of the _Bowl_ (Start Position) and _Plate_ (Target Position) as the independent context variables. 

**Spatial Assets.** We define the workspace using a set of semantic regions for in-distribution (grid-based) tasks and continuous coordinates for out-of-distribution tasks. 

- **Seen Discrete Regions (** _Cseen_ **).** We identified 9 distinct semantic regions on the tabletop to construct a discretized 9 _×_ 9 grid. Let _L_ = _{L_ 0 _, . . . , L_ 8 _}_ denote these locations: (1) _L_ 0: main ~~t~~ able ~~t~~ able ~~c~~ enter (Canonical Anchor), (2) _L_ 1: wooden ~~c~~ abinet ~~1 t~~ op ~~r~~ egion, (3) _L_ 2: main ~~t~~ able ~~n~~ ext ~~t~~ o ~~b~~ ox ~~r~~ egion, (4) _L_ 3: main ~~t~~ able ~~n~~ ext ~~t~~ o ~~p~~ late ~~r~~ egion, (5) _L_ 4: main ~~t~~ able ~~n~~ ext ~~t~~ o ~~r~~ amekin ~~r~~ egion, (6) _L_ 5: cookies ~~1~~ (On top of cookies), (7) _L_ 6: glazed ~~r~~ im ~~p~~ orcelain ~~r~~ amekin ~~1~~ , (8) _L_ 7: 

19 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

_Table 9._ Fixed Evaluation Set for LIBEROGEN-Object. We report the specific distractor configurations used for Compositional Generalization (CG, _k_ = 1) and Domain Generalization (DG, _k_ = 2). For DG, each entry represents a set of 5 distractor objects present in the scene. 

|**Task Instruction**|**CG Distractors (**_k_ = 1**)**|**DG Distractors (**_k_ = 2**)**|
|---|---|---|
|pick<br>~~u~~p<br>~~t~~he<br>~~a~~lphabet<br>~~s~~oup<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|glazed<br>~~r~~im<br>~~p~~orcelain<br>~~r~~amekin(5x)|milk, butter, ketchup,<br>bbq<br>~~s~~auce, cream<br>~~c~~heese|
|pick<br>~~u~~p<br>~~t~~he<br>~~c~~ream<br>~~c~~heese<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|akita<br>~~b~~lack<br>~~b~~owl(5x)|orange<br>~~j~~uice, tomato<br>~~s~~auce,<br>salad<br>~~d~~ressing,<br>chocolate<br>~~p~~udding,|
|||alphabet<br>~~s~~oup|
|pick<br>~~u~~p<br>~~t~~he<br>~~s~~alad<br>~~d~~ressing<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|porcelain<br>~~m~~ug(5x)|butter, cream<br>~~c~~heese, milk,<br>tomato<br>~~s~~auce, bbq<br>~~s~~auce|
|pick<br>~~u~~p<br>~~t~~he<br>~~b~~bq<br>~~s~~auce<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|wine<br>~~b~~ottle(5x)|ketchup, orange<br>~~j~~uice,<br>salad<br>~~d~~ressing,<br>alphabet<br>~~s~~oup,<br>chocolate<br>~~p~~udding|
|pick<br>~~u~~p<br>~~t~~he<br>~~k~~etchup<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|wine<br>~~b~~ottle(5x)|milk, bbq<br>~~s~~auce, butter,<br>cream<br>~~c~~heese, tomato<br>~~s~~auce|
|pick<br>~~u~~p<br>~~t~~he<br>~~t~~omato<br>~~s~~auce<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|porcelain<br>~~m~~ug(5x)|orange<br>~~j~~uice, ketchup,<br>alphabet<br>~~s~~oup,|
|||salad<br>~~d~~ressing, milk|
|pick<br>~~u~~p<br>~~t~~he<br>~~b~~utter<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|glazed<br>~~r~~im<br>~~p~~orcelain<br>~~r~~amekin(5x)|chocolate<br>~~p~~udding, butter,<br>cream<br>~~c~~heese, bbq<br>~~s~~auce,<br>orange<br>~~j~~uice|
|pick<br>~~u~~p<br>~~t~~he<br>~~m~~ilk<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|moka<br>~~p~~ot(5x)|tomato<br>~~s~~auce, salad<br>~~d~~ressing,<br>ketchup, alphabet<br>~~s~~oup, milk|
|pick<br>~~u~~p<br>~~t~~he<br>~~c~~hocolate<br>~~p~~udding<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|moka<br>~~p~~ot(5x)|bbq<br>~~s~~auce, cream<br>~~c~~heese,<br>orange<br>~~j~~uice, butter,<br>chocolate<br>~~p~~udding|
|pick<br>~~u~~p<br>~~t~~he<br>~~o~~range<br>~~j~~uice<br>~~a~~nd<br>~~p~~lace<br>~~i~~t<br>~~i~~n<br>~~t~~he<br>~~b~~asket|glazed<br>~~r~~im<br>~~p~~orcelain<br>~~r~~amekin(5x)|salad<br>~~d~~ressing, tomato<br>~~s~~auce,<br>milk, ketchup, alphabet<br>~~s~~oup|


_Table 10._ Training Distribution ( _Dtrain_ ) for LIBEROGEN-Language with Stair Sampling. Each task group is strictly bound to a sliding window of two syntactic templates. 

|**Task Group**|**Tasks Included**|**Associated Templates**|
|---|---|---|
|**Group 1**|1. alphabet<br>~~s~~oup<br>2. cream<br>~~c~~heese|1. Pick_{x}_and put it in_{y}_.<br>2. Pick up_{x}_, then place it in_{y}_.|
|**Group 2**|3. salad<br>~~d~~ressing<br>4. bbq<br>~~s~~auce|2. Pick up_{x}_, then place it in_{y}_.<br>3. Move_{x}_into_{y}_.|
|**Group 3**|5. ketchup<br>6. tomato<br>~~s~~auce|3. Move_{x}_into_{y}_.<br>4. Put_{x}_into_{y}_.|
|**Group 4**|7. butter<br>8. milk|4. Put_{x}_into_{y}_.<br>5. _{x}_should be picked up...|
|**Group 5**|9. chocolate<br>~~p~~udding<br>10. orange<br>~~j~~uice|5. _{x}_should be picked up...<br>1. Pick_{x}_and put it in_{y}_.|


flat ~~s~~ tove ~~1 c~~ ook ~~r~~ egion, and (9) _L_ 8: wooden ~~c~~ abinet ~~1 t~~ op ~~s~~ ide. 

- **Unseen Continuous Regions (** _Cunseen_ **).** Used exclusively for domain generalization ( _k_ = 2). Instead of adhering to the fixed semantic regions, object positions are sampled uniformly from the continuous tabletop surface ( _x, y_ ) _∈_ R<sup>2</sup> , excluding the specific coordinates of the grid centers defined in _Cseen_ . 

## **Training Distribution: ”L-Shaped” Sampling Protocol.** 

To test compositional generalization, we employ an ”LShaped” sampling strategy that creates a sparse training support. We utilize _L_ 0 (main ~~t~~ able ~~t~~ able ~~c~~ enter) as the pivot location. The training set _Dtrain_ consists of 


_Figure 13._ Example of Position. 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 


_Figure 11._ LIBEROGEN-Object. 

the union of two subsets: (1) **Row Support** : The Plate is fixed at _L_ 0, while the Bowl varies across all discrete locations _{L_ 0 _. . . L_ 8 _}_ . (2) **Column Support** : The Bowl is fixed at _L_ 0, while the Plate varies across the remaining locations _{L_ 1 _. . . L_ 8 _}_ . This structure ensures the model observes every location individually but only in restricted combinations. 

**Evaluation Distribution.** We establish a fixed evaluation set to ensure reproducibility. 

- **CG (** _k_ = 1 **)** : We evaluate on ”Off-Axis” grid combinations where both the Bowl and Plate are at non-center locations (e.g., Bowl at _L_ 1, Plate at _L_ 2). These pairs require the model to recombine spatial knowledge learned separately during training. 

- **DG (** _k_ = 2 **)** : We evaluate on 10 fixed random seeds where Bowl and Plate positions are sampled continuously from the table surface, ensuring no collision with training grid points. 

21 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

_Table 11._ Fixed Evaluation Set for LIBEROGEN-Language. For DG ( _k_ = 2), we evaluate on a fixed set of 10 variations per task; we show one representative _Semantic_ and one _Noisy_ example below. 

|**Target Object**|**CG Template (**_k_ = 1**)**|**DG Variations (**_k_ = 2**) [Examples]**|
|---|---|---|
|alphabet<br>~~s~~oup|Move_{_x_}_into_{_y_}_.|**S:**Transfer the can of alphabet soup into the basket.<br>**N:**It looks cloudy outside... Just grab the alphabet soup...|
|cream<br>~~c~~heese|Move_{_x_}_into_{_y_}_.|**S:**Transport the cream cheese to the basket.<br>**N:**They didn’t have the other brand... Put the cream cheese...|
|salad<br>~~d~~ressing|Put_{_x_}_into_{_y_}_.|**S:**Place the bottle of salad dressing into the basket.<br>**N:**I really don’t feel like eating greens, but put the...|
|bbq<br>~~s~~auce|Put_{_x_}_into_{_y_}_.|**S:**Locate the bbq sauce and set it down inside the basket.<br>**N:**I completely forgot to clean the grill... take the bbq sauce...|
|ketchup|_{_x_}_should be...|**S:**Don’t forget the condiment; place the ketchup in the basket.<br>**N:**Fries are just not the same without it. Place the ketchup...|
|tomato<br>~~s~~auce|_{_x_}_should be...|**S:**Take the can of tomato sauce and move it to the basket.<br>**N:**Be careful, glass breaks easily. Put the tomato sauce...|
|butter|Pick_{_x_}_and put...|**S:**Shift the butter into the basket.<br>**N:**I’m trying to cut down on calories... Put the butter...|
|milk|Pick_{_x_}_and put...|**S:**Transfer the milk to the basket.<br>**N:**My coffee was terrible... Please put the milk in the basket.|
|chocolate<br>~~p~~udding|Pick up_{_x_}_, then...|**S:**Retrieve the chocolate pudding and add it to the items...<br>**N:**It’s not for me... Take the chocolate pudding and insert...|
|orange<br>~~j~~uice|Pick up_{_x_}_, then...|**S:**Deposit the orange juice into the basket.<br>**N:**The doctor said I need more Vitamin C. Pick the orange...|


## **C.5. LIBEROGEN-Task** 

In this suite, we evaluate the combinatorial generalization of VLA policies, specifically testing whether agents can compose learned atomic skills into novel long-horizon sequences or generalize to entirely new task semantics. 

**Task Assets.** We define the task space based on the 10 manipulatable objects from LIBERO-Object. Let _O_ be the set of objects in LIBERO-Object, and _P_ = _O × O_ denote all possible object pairs. 

- **Atomic Tasks (** _Tatomic_ **).** Corresponding to LIBERO-Object tasks, with semantics _τ_ = ( _o_ ) for each _o ∈O_ . These are the foundational ”Pick-and-Place” primitives: ”Pick up the [Object] and place it in the basket”. There are 10 such tasks corresponding to the 10 objects in _O_ . 

- **Seen Composites (** _Tseen_ _~~c~~ omp_<sup>**).**Corresponding to LIBERO-10 tasks, with semantics</sup><sup>_τ_= (</sup><sup>_o_</sup> _i_<sup>_, o_</sup> _j_<sup>)</sup><sup>_∈P_</sup> seen<sup>_⊂P_, where</sup> _P_ seen denotes the set of observed object pairs during training. We select 3 specific sequential pairs (i.e., _P_ seen contains 3 pairs) to serve as the sparse support for compositionality (e.g., ”Pick _oi_ then Pick _oj_ ”). 

- **Unseen Semantics (** _Tood_ **).** Used for Domain Generalization ( _k_ = 2). These are paired-object tasks absent from any training composite task, requiring extrapolation beyond observed compositions and task structures, rather than introducing new predicates. 

**Training Distribution: Sparse Compositional Support.** Unlike the ”Stair” sampling used in visual suites, the task dimension employs a ”Sparse Union” strategy. The training set _Dtrain_ comprises all 10 Atomic Tasks plus exactly 3 specific Composite Tasks. This setup tests if the model can infer the general rule of composition from minimal examples. The exact training set is listed in Table 12. 

**Evaluation Distribution.** We establish a fixed evaluation set to ensure reproducibility. 

- **CG (** _k_ = 1 **)** : We evaluate the policy on novel combinations of the seen atomic tasks. These are pairs ( _oi, oj_ ) _∈P/_ seen formed by recombining objects from _O_ into arbitrary pairs that were never sequenced together during training (e.g., 

22 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 


_Figure 12._ LIBEROGEN-Language. 

”Pick Ketchup then Pick Soup”). 

- **DG (** _k_ = 2 **)** : We test the policy on paired-object tasks absent from any training composite task, requiring extrapolation beyond observed compositions and task structures—going beyond mere recombination of seen atomic skills. 

# **D. Fault Examples** 

We visualize representative generalization failure cases in Figure 15. 

23 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 


_Figure 14._ LIBEROGEN-Position. 

_Table 12._ Training Distribution ( _Dtrain_ ) for LIBEROGEN-Task. Includes all atomic tasks and a sparse set of 3 composite chains. 

|**Task Type**|**Included Tasks (Full Instructions)**|
|---|---|
|**Atomic (10x)**|1. Pick up the alphabet soup and place it in the basket.<br>2. Pick up the cream cheese and place it in the basket.<br>. ..(Includes all 10 objects defined in LIBERO-Object) . . .<br>10. Pick up the orange juice and place it in the basket.|
|**Seen Composites (3x)**|11. Pick up the alphabet soup and place it in the basket,<br>then pick up the cream cheese and place it in the basket.<br>12. Pick up the salad dressing and place it in the basket,<br>then pick up the bbq sauce and place it in the basket.<br>13. Pick up the butter and place it in the basket,<br>then pick up the milk and place it in the basket.|


24 

**Dismantling the Illusion of Vision-Language-Action Models Competence via Explicit Distributional Shifts** 

_Table 13._ Fixed Evaluation Set for LIBEROGEN-Task. CG ( _k_ = 1) tests novel sequential compositions. DG ( _k_ = 2) tests the unseen object-pairs. 

|**ID**|**CG Sequences (**_k_ = 1**) [Novel Pairs]**|**DG Semantics (**_k_ = 2**) [Unseen Objects]**|
|---|---|---|
|1|Pickorange<br>~~j~~uicethen Pickalphabet<br>~~s~~oup|Pickwine<br>~~b~~ottlethen Pickalphabet<br>~~s~~oup|
|2|Pickchocolate<br>~~p~~uddingthen Pickmilk|Pickalphabet<br>~~s~~oupthen Pickmug|
|3|Pickalphabet<br>~~s~~oupthen Picktomato<br>~~s~~auce|Pickblack<br>~~b~~owlthen Pickbutter|
|4|Pickcream<br>~~c~~heesethen Pickalphabet<br>~~s~~oup|Pickblack<br>~~b~~owlthen Picktomato<br>~~s~~auce|
|5|Pickketchupthen Picktomato<br>~~s~~auce|Pickboth<br>~~c~~ream<br>~~c~~heese|
|6|Pickmilkthen Pickbutter|Pickmoka<br>~~p~~otthen Pickbutter|
|7|Pickcream<br>~~c~~heesethen Pickmilk|Picktomato<br>~~s~~aucethen Pickmoka<br>~~p~~ot|
|8|Pickmilkthen Picktomato<br>~~s~~auce|Pickplatethen Pickcream<br>~~c~~heese|
|9|Pickorange<br>~~j~~uicethen Pickbutter|Pickmugthen Pickcream<br>~~c~~heese|
|10|Picktomato<br>~~s~~aucethen Pickketchup|Pickwine<br>~~b~~ottlethen Picktomato<br>~~s~~auce|


_Figure 15._ Examples of Pi0 and Pi0.5. 

25 

