---
title: "Learn2Fold: Structured Origami Generation with World Model Planning"
date: "2026-02-02"
authors: "Yanjia Huang; Yunuo Chen; Ying Jiang; Jinru Han; Zhengzhong Tu; Yin Yang"
url: https://arxiv.org/abs/2603.29585
pdf: https://arxiv.org/pdf/2603.29585
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.29585)** / [論文ページ](https://arxiv.org/abs/2603.29585)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Learn2Fold: Structured Origami Generation with World Model Planning** 

Yanjia Huang<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> Yunuo Chen<sup>1</sup><sup>_∗_</sup> Ying Jiang<sup>1</sup><sup>_∗_</sup> Jinru Han<sup>1</sup> Zhengzhong Tu<sup>2</sup> Yin Yang<sup>3</sup> Chenfanfu Jiang<sup>1</sup> 


Figure 1. **Teaser.** From simple planes to complex articulated forms, Learn2Fold plans origami folding sequences that respect geometric constraints and anticipate future consequences, enabling robust generalization across unseen crease patterns. 

## **Abstract** 

_The ability to transform a flat sheet into a complex threedimensional structure is a fundamental test of physical intelligence. Unlike cloth manipulation, origami is governed by strict geometric axioms and hard kinematic constraints, where a single invalid crease or collision can invalidate the entire folding sequence. As a result, origami demands long-horizon constructive reasoning that jointly satisfies precise physical laws and high-level semantic intent. Existing approaches fall into two disjoint paradigms: optimization-based methods enforce physical validity but require dense, precisely specified inputs, making them unsuitable for sparse natural language descriptions, while generative foundation models excel at semantic and perceptual synthesis yet fail to produce long-horizon, physicsconsistent folding processes. Consequently, generating_ 

* Equal contribution.<sup>1</sup> UCLA,<sup>2</sup> Texas A&M University,<sup>3</sup> University of Utah. yanjia_0812@tamu.edu, yunuoch@math.ucla.edu, anajymua@gmail.com, jinruhan1219@g.ucla.edu, tzz@ tamu.edu, yin.yang@utah.edu, cffjiang@ucla.edu 

_valid origami folding sequences directly from text remains an open challenge. To address this gap, we introduce_ **_Learn2Fold_** _, a neuro-symbolic framework that formulates origami folding as conditional program induction over a crease-pattern graph. Our key insight is to decouple semantic proposal from physical verification. A large language model generates candidate folding programs from abstract text prompts, while a learned graph-structured world model serves as a differentiable surrogate simulator that predicts physical feasibility and failure modes before execution. Integrated within a lookahead planning loop, Learn2Fold enables robust generation of physically valid folding sequences for complex and out-of-distribution patterns, demonstrating that effective spatial intelligence arises from the synergy between symbolic reasoning and grounded physical simulation._ 

## **1. Introduction** 

Recent advances in generative AI have enabled the synthesis of increasingly complex visual content, including im- 

ages, videos, and 3D assets [6, 8, 22, 25, 27]. However, most of these successes focus on generating static or perceptual representations, where physical feasibility and execution constraints are either ignored or only weakly enforced. Extending generative models beyond visual plausibility toward physically executable processes remains an open and largely unexplored challenge. This challenge becomes particularly pronounced in tasks that require longhorizon reasoning under strict geometric and topological constraints. While recent progress in deformable object manipulation, such as cloth folding [19, 21, 23, 38, 41], has demonstrated impressive results, these settings benefit from the inherent compliance and error tolerance of amorphous materials. Garments can accommodate local inaccuracies through smoothing and deformation, allowing learning-based methods to recover from imprecise actions. In contrast, origami folding operates under a fundamentally different regime. Origami is the art of transforming a flat sheet into a three-dimensional structure through a sequence of folds, governed by strict geometric axioms and topological constraints [18, 26]. A single misplaced crease does not merely introduce a local artifact, but can violate surface topology or render all subsequent folding steps mathematically infeasible. As a result, origami demands precise coordination of discrete topological changes and continuous geometric motions over long horizons, with little tolerance for error. 

In this work, we adopt origami folding as a challenging and principled testbed for studying constraint-aware generative planning. Digitally representing and generating origami processes requires modeling both a structured crease pattern and the progressive, constraint-driven folding dynamics that transform a flat sheet into a valid 3D shape. Despite its conceptual simplicity, origami exposes the core limitations of existing generative approaches and serves as a rigorous benchmark for evaluating long-horizon spatial reasoning under hard physical constraints. 

Prior work on origami generation can be broadly categorized into learning based methods and optimization based approaches. Generative models, including large language models and vision language models [36, 39, 40, 46], are trained on large scale multimodal data such as origami videos, images, and textual instructions. These models can produce descriptive tutorials or high level folding guidance conditioned on text prompts or images. However, they typically fail to generate physically executable origami processes, as they optimize for approximate visual plausibility rather than exact physical feasibility, often hallucinating geometries that appear visually coherent but violate folding constraints. In contrast, traditional optimization based methods [12, 18, 35] formulate origami generation as a constrained optimization problem, employing techniques such as circle packing or tuck folding algorithms to mathemat- 

ically guarantee that a target mesh can be folded from a single sheet. These approaches produce simulation ready, physically grounded crease patterns, but require precise 3D mesh inputs, making them difficult to apply to sparse inputs such as a single image or a text prompt. This raises a key question: can we retain the physical rigor and simulation ready representations of computational origami while leveraging the powerful priors of large language and vision language models to reconstruct executable origami processes from enriching semantic descriptions? 

To bridge these gaps, we introduce **Learn2Fold** , a neuro-symbolic framework that formulates origami folding as constraint-aware program induction. Our key insight is that robust generation requires separating _proposal_ from _verification_ . Instead of blindly decoding a sequence, Learn2Fold operates in a propose, verify loop. We leverage a Large Language Model (LLM) to propose high-level structured action tokens, utilizing its semantic planning capabilities. However, acknowledging that LLMs lack intrinsic physics grounding, we integrate a learned GraphStructured World Model for lookahead planning. This world model acts as a differentiable surrogate simulator, allowing the system to _imagine_ the geometric consequences of actions and prune branches that lead to invalid states before execution. We propose a symbolic simulator that performs final constraint verification, complementing neural proposal and learned lookahead with exact geometric feasibility checks. 

Our contributions are summarized as follows: 

- We propose Learn2Fold, a novel framework for origami process generation that integrates a Large Language Model (LLM) for high-level structured action proposal with a learned Graph-Structured World Model for physics-aware lookahead planning and verification. 

- A scalable, simulation-driven data curation engine for origami that generates large-scale folding transitions using counterfactual perturbations and propose a new origami dataset, OrigamiCode dataset containing structured folding programs and verified transitions for learning origami folding dynamics. 

- We validate the effectiveness of the proposed method through comprehensive experiments, demonstrating robust generalization to out-of-distribution physically valid and executable origami generation. 

## **2. Related Work** 

### **2.1. Structured and Constraint-Aware Generation** 

Recent generative models have demonstrated remarkable proficiency in synthesizing high fidelity assets, ranging from static 3D shapes [17, 20, 42, 43] to dynamic video sequences [4, 14, 30, 32]. However, modeling progressive shape formation processes like origami folding still 


Figure 2. **Overview of Learn2Fold.** Learn2Fold formulates origami folding as constraint-aware sequential program generation. During training, a symbolic Level-0 simulator enables scalable data generation and supervision for both a language-based proposal model and a learned world model. At inference time, Learn2Fold combines LM proposals with world-model rollouts and MPC to robustly plan folding sequences under hard constraints. 

remains an open challenge. Unlike one-shot generation methods that directly predict a final geometry, origami folding is intrinsically an _executable, long-horizon action sequence_ . This process operates on a complex hybrid discrete-continuous state space. This task involves discrete topological changes such as face layering, connectivity updates, coupled with continuous kinematic transformations. Crucially, this generation process is governed by strict physical validity. Every folding step must satisfy hard geometric and topological constraints, such as flat-foldability and self-intersection avoidance; a minor violation in early steps compounds, rendering the final result physically invalid. Consequently, this setting demands structured generation paradigms rather than unstructured end-to-end inference. To address similar structural challenges, recent works have adopted intermediate representations, such as scene graphs or layouts [16, 24, 44], to anchor object relations and reduce spurious outputs. Another line of research integrates constraint-aware decoding or verifier-guided search to ensure validity [2, 28, 45]. For instance, recent structural synthesis models like BrickGPT [28] rely on reactive rollback to filter out physically unstable steps. While these assembly generation systems effectively combine auto-regressive proposals with rollback mechanisms, straightforward back- 

tracking becomes computationally prohibitive for complex folding sequences. Distinguishing our work from these approaches, we propose a CP-grounded folding program equipped with diagnostic feedback. Instead of binary success or failure checks, our model performs causal attribution to identify why a fold failed, enabling efficient planning and recovery even on out-of-distribution crease patterns. 

### **2.2. Computational Origami** 

Origami folding is fundamentally governed by rigorous mathematical rules concerning develop ability and flatfoldability like Kawasaki’s and Maekawa’s theorems[3, 7, 15]. To simulate these complex behaviors computationally, researchers have developed kinematic models that treat creases as rotational hinges. Early works focused on rigid origami, modeling the mesh as discrete rigid facets connected by joints [34, 35]. To alleviate this, more recent approaches, such as the bar-and-hinge model used in Origami Simulator [9], introduce compliance to approximate the elastic deformation of paper, enabling real-time folding visualization. While these simulators provide ground truth physics, they are purely forward-process tools where they calculate the geometric consequence of a given fold but do not posses the agency to plan a sequence or reason about 

hight-level semantic goals. 

The problem of generation a crease patter (CP) for a target 3D shape has traditionally been formulated as a geometric optimization problem. Pioneering systems like TreeMaker [18] and Origamizer [34] use circle packing or tuck-folding algorithms to mathematically guarantee that a specific mesh can be folded from a single sheet. However, these methods are strictly geometry-centric and deterministic. They lack the flexibility to handle ambiguous semantic descriptions and are often sensitive to topological errors, where a slight violation in the CP graph renders the entire optimization infeasible. Unlike these optimization-based solvers which require a perfect final mesh as input, our approach treats generation as a sequential decision-making process. This allows for robust recovery from intermediate errors and generalization to out-of-distribution patterns via previous trained structures. 

### **2.3. World Models** 

World models learn action-conditioned dynamics to enable planning via imagined rollouts. This paradigm spans from classical latent-dynamics methods in model-based RL [10, 11, 29] to recent foundation-scale video simulators that model physics in rich visual domains [4, 14, 31]. However, pixel-based or latent world models do not directly enforce hard discrete geometric constraints, nor do they naturally produce structured, executable programs. Furthermore, collecting action-labeled interaction data for specialized domains like origami remains prohibitive [1]. In our work, we learn a state-level world model over CP-graph states, supervised by scalable synthetic transitions from a deterministic constraint engine. Crucially, our training data includes near-boundary perturbations, exposing the model to both feasible and infeasible outcomes. This learned dynamics model enables efficient model-predictive lookahead, allowing the system to verify action feasibility and recover from proposal errors on out-of-distribution crease patterns. 


Figure 3. **Deriving Expert Trajectories from Videos.** We show one data source for obtaining expert folding trajectories. In-thewild instructional videos are processed into State Cards and folding steps, which are then augmented through perturbation and exploration for training. 

## **3. Method** 

We target _physically valid generation_ for Computational Origami: at inference time, our agent augments its base proposal policy with a graph-based world model that _imagines_ future manifold states and converts them into validity scores for planning (Fig. 2). Our approach, Learn2Fold, tightly couples three components: ❶ a _Canonicalized Graph Representation_ that ensures structural invariance; ❷ a _Generative Proposal_ Policy that suggests candidate folds based on semantic goals; and ❸ a _Graph-based World Model_ that rolls out short-horizon geometric futures. At test time, we do not only rely on the policy’s likelihood; instead, the world model’s predictions are fused at the score level via model predictive control (MPC) to rank candidate actions, ensuring strict geometric feasibility without sacrificing generative flexibility. 

In the following sections, Sec. 3.1 details the canonicalized state representation. Sec. 3.2 formalizes the languageconditioned proposal policy. Sec. 3.3 introduces the graph world model, which acts as a differentiable surrogate simulator. Finally, Sec. 3.4 describes the MPC planning strategy that integrates these signals for robust action selection. 

### **3.1. State Representation and Canonicalization** 

We formulate the origami folding process as a sequential manipulation of a graph-structured manifold. An origami instance is represented by a tuple _Ot_ = ( _G, st_ ), where _G_ denotes its static topology and _st_ denotes a dynamic state. 

**Static Graph Topology.** The crease pattern (CP) is a planar graph _G_ = ( _V, E_ ) with points _V_ = _{v_<sup>_i_</sup> _∈_ [0 _,_ 1]<sup>2</sup> _}_<sup>_N_</sup> _i_ =1<sup>_v_</sup> and edges _E_ = _{e_<sup>_j_</sup> _}_<sup>_N_</sup> _j_ =1<sup>_e_.Eachedgemaycarryaninitial</sup> crease type label _z_ 0<sup>_j∈{_M</sup><sup>_,_V</sup><sup>_,_U</sup><sup>_}_(M: mountain, V: valley,</sup> U: unknown). 

**Canonicalization.** Raw CP data often contains arbitrary vertex indexing, which hinders learning. To ensure permutation invariance and robust generalization, we apply a deterministic canonicalization process Φ : _G →G_<sup>_∗_</sup> . Specifically, we (i) reindex vertices via lexicographical sorting of coordinates, and (ii) reindex edges based on the sorted endpoint indices. To further eliminate orientation bias, we augment the training data by applying dihedral symmetries (rotations and reflections) to _V_ prior to canonicalization. This ensures that structurally identical patterns map to the same index space. 

**Dynamic State.** We track the folding status using a state vector _st_ = � _αt, ρt, zt, ψt, bt, t_ �, where _αt ∈_ [ _−π, π_ ]<sup>_|E|_</sup> are signed dihedral angles, _ρt ∈_ [0 _,_ 1]<sup>_|E|_</sup> are progress ratios, _zt ∈{_ M _,_ V _,_ U _}_<sup>_|E|_</sup> are crease types, _ψt_ is the global frame angle, _bt_ is the MV-flip flag, and _t_ is the step counter. 

### **3.2. Policy Learning via Language Models** 

We frame origami folding as a conditional program induction task. The goal is to learn a policy _πθ_ ( _at | Ct_ ) that generates a valid folding operation _at_ given the current context _Ct_ . 

**Unified Token Space.** The action space of folding is inherently hybrid, requiring the selection of discrete graph elements (e.g., target edges) and continuous parameters (e.g., fold angles). To leverage the reasoning capabilities of Transformer-based LLMs, we unify these modalities into a homogeneous vocabulary Σ = Σops _∪_ Σgraph _∪_ Σgeo. Continuous geometric parameters are quantized into discrete bins Σgeo, while canonicalized graph indices are mapped to semantic tokens Σgraph. This formulation transforms the complex control problem into an autoregressive sequence modeling task, enabling the model to capture joint dependencies between topological intent and geometric specifications. 

**Context and Objective.** The policy is conditioned on a context _Ct_ = ( _g_ ; _G_<sup>_∗_</sup> _, st_ ), where _g_ denotes the high-level semantic goal. By operating on the canonicalized graph _G_<sup>_∗_</sup> , the policy learns structure-invariant _folding motifs_ (e.g., “rabbit-ear fold”) rather than overfitting to instance-specific identifiers (e.g., vertex indices). We train the model using Maximum Likelihood Estimation (MLE) on expert demonstrations _D_ : 


where _at,k_ denotes the _k_ -th token of the action sequence at step _t_ . This supervised pre-training instills the _grammar_ of valid folding operations. 

expand( _·_ ) broadcasts the per-edge mask to all state channels. 

### **3.4. Inference via Graph-Guided MPC** 

At test time, we perform a constrained lookahead search on the CP graph _G_ = ( _V, E_ ). At each step _t_ , our proposal policy _πθ_ generates candidate structured actions, which are filtered by a hard verifier (Level-0 simulator) and ranked by the learned world model. 

**Candidate Sampling.** We sample _K_ candidate actions from the proposal distribution using nucleus sampling: 


**Hard Verification (Level-0).** Each candidate is first evaluated by a deterministic constraint kernel: 


where _vt_<sup>(</sup><sup>_k_)</sup> _∈{_ 0 _,_ 1 _}_ indicates fold validity, _rt_<sup>(</sup><sup>_k_)</sup> denotes the reason for invalidity, and _m_<sup>(</sup> _t_<sup>_k_)</sup> _∈{_ 0 _,_ 1 _}_<sup>_|E|_</sup> is the affected-edge mask. We discard invalid candidates and retain _A_<sup>valid</sup> _t_ = _{a_<sup>(</sup> _t_<sup>_k_)</sup> _∈At | vt_<sup>(</sup><sup>_k_)</sup> = 1 _}_ . 

**World-Model Rollout.** For each valid candidate, the world model predicts residual state updates and a soft violation mask: 


where _c_ ˆ<sup>(</sup> _t_ +1<sup>_k_)</sup><sup>_∈_[0</sup><sup>_,_1]</sup><sup>_|E|_estimatesper-edgeconstraintviola-</sup> tion likelihood (a soft counterpart of _mt_ ). 

### **3.3. Graph-Based World Model** 

While the policy proposes plausible actions, ensuring strict physical feasibility requires rigorous verification. To enable efficient lookahead planning without computationally expensive mesh-based simulations, we learn a differentiable world model _Mϕ_ that acts as a surrogate simulator. 

**Residual Graph Dynamics.** Unlike pixel-based world models [5] which lack explicit geometric constraints, our model operates directly on the graph state _st_ . We formulate the transition as a sparse residual update: 


where _m_ ˆ _t ∈_ [0 _,_ 1]<sup>_|E|_</sup> is a locality mask and _c_ ˆ _t_ +1 _∈_ [0 _,_ 1]<sup>_|E|_</sup> estimates per-edge constraint violation likelihood. 

**Action Selection.** We choose the action maximizing a fused objective of proposal likelihood, goal progress, and feasibility: 


Here _λ_ goal _, λ_ cst balance goal pursuit and constraint satisfaction, and _ϵ >_ 0 avoids numerical instability. 

**Failure and Re-sampling.** In the case when _A_<sup>valid</sup> _t_ = _∅_ or max _k J_<sup>(</sup><sup>_k_)</sup> _< τ_ , we construct a negative constraint from the predicted violation mask (e.g., top- _M_ edges with highest ˆ _c_ ) and re-sample candidates under the updated constraint set. 


Figure 4. **Overview of the** **_OrigamiCode_ Benchmark Dataset.** The dataset features diverse categories, structured representations, sequential folding data, detailed statistics, and benchmark downstream tasks. 

### **3.5. Dataset Construction** 

To support learning structured origami folding behaviors, we construct the _OrigamiCode_ dataset (Fig. 4), a large-scale collection of procedural folding sequences derived from canonical crease pattern (CP) representations. The dataset covers 25 common origami object classes, each defined by a parameterized CP graph (Fig. 5) and an associated folding specification stored in a structured JSON format. Unlike previous datasets dominated by simple shapes, our benchmark is carefully stratified into three difficulty tiers based on step count and non-local dependency: **Simple (10 categories):** Basic rigid folding structures with minimal layering (e.g., _Airplanes_ , _Hearts_ , _Cups_ ). **Intermediate (10 categories):** Standard models requiring moderate spatial planning and box-pleating (e.g., _Boats_ , _Flowers_ ). **Complex (5 categories):** High-frequency folding sequences with intricate appendage management and strict circle-packing constraints (e.g., _Cranes_ , _Dragons_ ). 

The CP graph encodes the planar crease topology, including vertex connectivity, edge types (mountain or valley), and boundary constraints, while the JSON specification defines the ordered folding operations and geometric parameters required to generate valid intermediate states. Our data curation pipeline derives expert trajectories from instructional sources and further augments them through perturbation and exploration. This process produces a large set of physically consistent folding trajectories, where each sequence records the evolving mesh geometry, crease states, and fold parameters at every step. In total, we collect 5,760 origami process sequences and 75,000 trajectories in the OrigamiCode dataset, which provides structured supervi- 


Figure 5. **Crease Pattern (CP) Graph.** We created CP graph for each case to represent folding sequence. 

sion for learning fold prediction, sequence generation, and origami manipulation tasks. 

## **4. Experiments** 

### **4.1. Experiment Setup** 

**Implementation Details** We train the world model (WM) using large-scale synthetic folding data generated by the Level-0 simulator. Specifically, we collect approximately 76,000 transitions through expert demonstrations and constraint-guided perturbations, and train the WM with supervised learning for 50 epochs, which takes about 30 hours on a single NVIDIA RTX Pro 6000 GPU. The language model (LM) is a lightweight decoder-only transformer fine-tuned to generate structured folding actions under a fixed JSON schema. It is trained using roughly 10<sup>4</sup> expert folding steps augmented with simulator-verified perturbations, and converges within 6 hours using LoRA adapters on the same hardware. At inference time, Learn2Fold runs in a model predictive control (MPC) loop, where the LM proposes _N_ = 8 candidate actions per step, the simulator 


Figure 6. **Learn2Fold results.** 


Figure 7. **Folding with Reasoning.** Learn2Fold incrementally constructs origami folding programs in CP-graph space. At each step, multiple candidate actions are evaluated through worldmodel rollouts, infeasible options are discarded, and the best action is selected for execution, enabling robust folding and recovery under hard constraint 

filters invalid ones, and the WM scores the remaining candidates via short-horizon rollouts to select the final action. All experiments are conducted with fixed random seeds for reproducibility. 

**Dataset.** To rigorously evaluate topological generalization, we curate a held-out _OrigamiCode_ benchmark dataset of 25 distinct origami categories that span the full spectrum of folding complexity. This taxonomy allows us to disentangle basic instruction following from complex physical 

reasoning. Each instance provides a canonicalized CP and a ground-truth program. Following a standard train–test split, 80% of the data is used for training, while the remaining 20% is reserved for evaluation. 

**Baselines.** We compare our approach against three representative methods. First, we evaluate BrickGPT [28], a reactive baseline adapted from assembly synthesis that employs a physics-aware rollback mechanism to filter unstable steps through trial-and-error execution and is trained on the proposed OrigamiCode dataset. Second, we benchmark against GPT-5.1 and GPT-5.2, the latest state-ofthe-art foundation models. These general-purpose agents are provided with in-context examples to output structured folding programs, representing the upper bound of unconstrained semantic planning without specialized geometric modules. Finally, we compare these against Learn2Fold (Ours), which generates actions under explicit graph-based lookahead verification. 

**Metrics.** We evaluate performance at both the step level and the trajectory level. At the step level, we report Precision, Recall, and F1 to measure how accurately each method predicts structured folding actions under a unified action schema, capturing both the correctness and coverage of discrete decisions. At the trajectory level, we report Category Success Rate (Cat-SR) and Edge-IoU to evaluate long-horizon execution performance and structural alignment, respectively. Cat-SR is defined as the fraction of folding sequences that successfully complete the target origami within each category and is macro-averaged across categories to mitigate class imbalance. Edge-IoU measures whether a predicted action affects the correct set of creases by computing the intersection-over-union between the predicted affected-edge set and the simulator-derived ground truth. 

### **4.2. Quantitative Evaluation** 

In the absence of standard benchmarks for origami process generation, following [28], we construct a custom test set comprising 3,840 text prompts spanning 25 categories. From this set, we select 1,150 cases for validation and perform two independent runs per prompt for each method, yielding 7,680 results per method. As shown in Table 1, our method outperforms all baselines across all metrics in both step-level accuracy and trajectory-level success. At the step level, Learn2Fold achieves a Precision _µ_ /Recall _µ_ /F1 _µ_ of 0.766/0.711/0.739, substantially exceeding the strongest baseline (GPT-5.1, F1 _µ_ = 0.266), corresponding to a +47.3 point absolute improvement in F1. In contrast, LLM-based baselines exhibit a pronounced precision–recall imbalance. For example, GPT-5.2 achieves a relatively high Recall _µ_ (0.358) but very low Precision _µ_ (0.124), suggesting that 


Figure 8. **Qualitative comparison of folding behaviors across methods.** Learn2Fold produces concise, physically feasible folding trajectories on both simple and complex origami tasks. Baseline methods frequently fail due to invalid actions, early termination, or inability to recover from long-horizon errors, especially on complex crease patterns. 

Table 1. Main comparison across methods.<sup>_∗_</sup> indicates prompted models, and<sup>_†_</sup> indicates finetuned models. 

|Method|Prec. _↑_|Rec. _↑_|F1_↑_|Edge-IoU_↑_|Cat-SR_↑_|
|---|---|---|---|---|---|
|Gemini<sup>*</sup>|0.2874|0.4213|0.3420|0.1126|0.4942|
|GPT-5.1<sup>*</sup>|0.2625|0.2996|0.2663|0.0937|0.6753|
|GPT-5.2<sup>*</sup>|0.1243|0.3575|0.1648|0.1322|0.1600|
|BrickGPT<sup>_†_</sup>|0.3969|0.2250|0.2461|0.0505|0.5455|
|**Ours**|0.7661|0.7113|0.7394|0.5820|0.8912|


while many relevant actions are proposed, they are often imprecise or misaligned with the required structural context since LLMs operate at a coarse semantic level, lacking detailed visual guidance. As a result, they can outline plausible folding intentions but cannot resolve the fine-grained, step-specific details. As for BrickGPT, while it benefits from explicit rollback-based execution and achieves higher precision than LLM-based baselines, it still suffers from limited recall, indicating that its reactive trial-and-error strategy produces coarse and incomplete folding actions and fails to consistently recover the full sequence of required steps. 

### **4.3. Qualitative Study** 

Fig. 8 presents qualitative comparisons between Learn2Fold and baseline methods on representative examples from the same test set described in Sec. 4.2. LLM-based baselines typically fail after only a few steps. While the initial actions are often semantically plausible, errors quickly accumulate due to the lack of explicit geometric state tracking. As a result, many predicted 

steps are either structurally incorrect or misaligned with the underlying crease pattern, causing premature termination of the folding process. BrickGPT exhibits improved stability in the early stages of execution. In several examples, the first few predicted actions (e.g., the first three to four steps) are valid and physically feasible, benefiting from its rollback-based mechanism. However, as folding sequences grow longer, BrickGPT struggles to maintain long-term consistency, as it fails to capture fine-grained dependencies between distant steps, resulting in incorrect or incomplete long-horizon folding processes and limiting its ability to represent detailed step-by-step origami procedures for complex models. While Learn2Fold consistently produces coherent and fine-grained folding sequences across the entire trajectory. By explicitly modeling the folding state and verifying feasibility at each step, Learn2Fold maintains structural consistency and accurately captures the intended origami process, even for long and intricate folding sequences. These qualitative results corroborate the quantitative findings and highlight the advantage of explicit state modeling for reliable origami process generation. 

### **4.4. Ablation** 

We conduct an ablation study of the key components of our framework to evaluate the contribution of each proposed component to the final origami process generation’s performance. We progressively ablate the system by comparing three configurations: (i) an LLM-only proposer, (ii) LLM augmented with a learned world model (LM+WM), and (iii) the full system Learn2Fold that further incorporates the Level0Sim constraint kernel (LM+WM+Level0Sim). These variants are evaluated under both in-distribution (IID) 

Table 2. Ablations on IID (top) and OOD (bottom). Blue and teal indicate the best and second-best results. 

|Method|Step Valid_↑_|Traj SR_↑_|Goal Dist_↓_|
|---|---|---|---|
|LM|70.8%_±_45.5%|22.2%_±_45.5%|0.796_±_0.194|
|LM+WM|54.2%_±_49.8%|25.0%_±_43.3%|0.759_±_0.214|
|Full (Ours)|64.2%_±_41.8%|33.3%_±_47.1%|0.855_±_0.196|
|Method|Step Valid_↑_|Traj SR_↑_|Goal Dist_↓_|
|LM|47.6%_±_29.2%|20.7%_±_55.5%|0.633_±_0.192|
|LM+WM|32.3%_±_28.7%|17.8%_±_51.7%|0.560_±_0.248|
|Full (Ours)|41.2%_±_32.3%|27.7%_±_50.1%|0.487_±_0.353|


and out-of-distribution (OOD) CP holdout settings using step-level validity, trajectory success rate (Traj SR), and final goal distance. Incorporating the world model alters the decision-making behavior by introducing short-horizon lookahead. Compared to the LLM-only baseline, LM+WM exhibits a modest improvement in trajectory-level success (IID Traj SR: 22.2% _→_ 25.0%), and consistently reduces the final goal distance in both IID (0.796 _→_ 0.759) and OOD settings (0.633 _→_ 0.560). However, this improvement comes with a decrease in step-level validity, indicating that the world model prioritizes global progress over local action safety, occasionally selecting actions that are locally risky but potentially beneficial for long-horizon objectives. Adding Level0Sim consistently improves long-horizon performance. The full system achieves the highest trajectory success in both IID and OOD settings, while recovering step-level validity and further reducing final goal distance under distribution shift. Overall, the ablation indicates complementary roles of the LLM proposer, the world model, and Level0Sim, whose combination is required for robust long-horizon folding. 

## **5. Conclusion** 

In this work, we present **Learn2Fold** , a neuro-symbolic framework for physically valid origami process generation that unifies semantic reasoning with rigorous geometric constraint enforcement. By formulating origami folding as a constraint-aware program induction over a CP graph, Learn2Fold addresses a fundamental limitation of prior generative models: the inability to reliably generate long-horizon, executable action sequences under strict topological and kinematic constraints. We view origami not merely as an application, but as a principled testbed for future spatial reasoning systems, where it exposes core challenges in reasoning over structured space: discrete topological decisions coupled with continuous geometry, irreversible constraints, and long-horizon dependency. 

## **References** 

- [1] Bo Ai, Stephen Tian, Haochen Shi, Yixuan Wang, Tobias Pfaff, Cheston Tan, Henrik I. Christensen, Hao Su, Jiajun Wu, and Yunzhu Li. A review of learning-based dynamics models for robotic manipulation. _Science Robotics_ , 10(106): eadt1497, 2025. 4 

- [2] Peter Anderson, Basura Fernando, Mark Johnson, and Stephen Gould. Guided open vocabulary image captioning with constrained beam search. In _Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing_ , pages 936–945, Copenhagen, Denmark, 2017. Association for Computational Linguistics. 3 

- [3] Marshall Bern and Barry Hayes. The complexity of flat origami. In _Proceedings of the Seventh Annual ACM-SIAM Symposium on Discrete Algorithms (SODA)_ , pages 175–183. Society for Industrial and Applied Mathematics, 1996. 3 

- [4] Jake Bruce, Michael Dennis, Ashley Edwards, Jack ParkerHolder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, Yusuf Aytar, Sarah Bechtle, Feryal Behbahani, Stephanie Chan, Nicolas Heess, Lucy Gonzalez, Simon Osindero, Sherjil Ozair, Scott Reed, Jingwei Zhang, Konrad Zolna, Jeff Clune, Nando de Freitas, Satinder Singh, and Tim Rockt¨aschel. Genie: Generative interactive environments, 2024. 2, 4 

- [5] Jake Bruce, Michael D Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 5 

- [6] Zhaoxi Chen, Guangcong Wang, and Ziwei Liu. Scenedreamer: Unbounded 3d scene generation from 2d image collections. _IEEE transactions on pattern analysis and machine intelligence_ , 45(12):15562–15576, 2023. 2 

- [7] Erik D Demaine and Joseph O’Rourke. _Geometric Folding Algorithms: Linkages, Origami, Polyhedra_ . Cambridge University Press, 2007. 3 

- [8] Jun Gao, Tianchang Shen, Zian Wang, Wenzheng Chen, Kangxue Yin, Daiqing Li, Or Litany, Zan Gojcic, and Sanja Fidler. Get3d: A generative model of high quality 3d textured shapes learned from images. _Advances in neural information processing systems_ , 35:31841–31854, 2022. 2 

- [9] Amanda Ghassaei, Erik D Demaine, and Neil Gershenfeld. Fast, interactive origami simulation using gpu compute shaders. In _Proceedings of the 7th International Meeting on Origami in Science, Mathematics and Education (OSME7)_ , pages 1151–1166, 2018. 3 

- [10] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels, 2019. 4 

- [11] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations (ICLR)_ , 2020. 4 

- [12] Can He, Lingxiao Meng, Zhirui Sun, Jiankun Wang, and Max Q. H. Meng. Fabricfolding: Learning efficient fabric folding without expert demonstrations, 2023. 2 

- [13] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Liang Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _Iclr_ , 1(2):3, 2022. 12 

- [14] Yanjia Huang, Xianshun Jiang, Xiangbo Gao, Mingyang Wu, and Zhengzhong Tu. Vistav2: World imagination for indoor vision-and-language navigation, 2025. 2, 4 

- [15] Thomas C. Hull. The combinatorics of flat folds: A survey. In _Origami_<sup>3</sup> _: Third International Meeting of Origami Science, Mathematics, and Education_ , pages 29–38. A K Peters, 2002. 3 

- [16] Justin Johnson, Agrim Gupta, and Li Fei-Fei. Image generation from scene graphs, 2018. 3 

- [17] Yushi Lan, Fangzhou Hong, Shangchen Zhou, Shuai Yang, Xuyi Meng, Yongwei Chen, Zhaoyang Lyu, Bo Dai, Xingang Pan, and Chen Change Loy. Ln3diff++: Scalable latent neural fields diffusion for speedy 3d generation. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , page 1–18, 2025. 2 

- [18] Robert J Lang. _Origami Design Secrets: Mathematical Methods for an Ancient Art_ . CRC Press, 2 edition, 2011. 2, 4 

- [19] Robert Lee, Jad Abou-Chakra, Fangyi Zhang, and Peter Corke. Learning fabric manipulation in the real world with human videos. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 3124–3130. IEEE, 2024. 2 

- [20] Weiyu Li, Xuanyang Zhang, Zheng Sun, Di Qi, Hao Li, Wei Cheng, Weiwei Cai, Shihao Wu, Jiarui Liu, Zihao Wang, Xiao Chen, Feipeng Tian, Jianxiong Pan, Zeming Li, Gang Yu, Xiangyu Zhang, Daxin Jiang, and Ping Tan. Step1x-3d: Towards high-fidelity and controllable generation of textured 3d assets, 2025. 2 

- [21] Yinxiao Li, Yonghao Yue, Danfei Xu, Eitan Grinspun, and Peter K Allen. Folding deformable objects using predictive simulation and trajectory optimization. In _2015 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 6000–6006. IEEE, 2015. 2 

- [22] Yangguang Li, Zi-Xin Zou, Zexiang Liu, Dehu Wang, Yuan Liang, Zhipeng Yu, Xingchao Liu, Yuan-Chen Guo, Ding Liang, Wanli Ouyang, et al. Triposg: High-fidelity 3d shape synthesis using large-scale rectified flow models. _arXiv preprint arXiv:2502.06608_ , 2025. 2 

- [23] Yiming Liu, Lijun Han, Enlin Gu, and Hesheng Wang. Learning a general model: Folding clothing with topological dynamics. _arXiv preprint arXiv:2504.20720_ , 2025. 2 

- [24] Yunlong Liu, Shuyang Li, Pengyuan Liu, Yu Zhang, and Rudi Stouffs. From pixels to predicates structuring urban perception with scene graphs. _arXiv preprint arXiv:2512.19221_ , 2025. 3 

- [25] Yuanxun Lu, Jingyang Zhang, Shiwei Li, Tian Fang, David McKinnon, Yanghai Tsin, Long Quan, Xun Cao, and Yao Yao. Direct2. 5: Diverse text-to-3d generation via multi-view 2.5 d diffusion. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 8744– 8753, 2024. 2 

- [26] Jeremy Maitin-Shepard, Marco Cusumano-Towner, Jinna Lei, and Pieter Abbeel. Cloth grasp point detection based 

on multiple-view geometric cues with application to robotic towel folding. In _2010 IEEE International Conference on Robotics and Automation_ , pages 2308–2315, 2010. 2 

- [27] Gimin Nam, Mariem Khlifi, Andrew Rodriguez, Alberto Tono, Linqi Zhou, and Paul Guerrero. 3d-ldm: Neural implicit 3d shape generation with latent diffusion models. _arXiv preprint arXiv:2212.00842_ , 2022. 2 

- [28] Ava Pun, Kangle Deng, Ruixuan Liu, Deva Ramanan, Changliu Liu, and Jun-Yan Zhu. Generating physically stable and buildable brick structures from text. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 14798–14809, 2025. 3, 7, 12 

- [29] Rafael Rafailov, Tianhe Yu, Aravind Rajeswaran, and Chelsea Finn. Offline reinforcement learning from images with latent space models, 2020. 4 

- [30] Aditya Ramesh, Prafulla Dhariwal, Alex Nichol, Casey Chu, and Mark Chen. Hierarchical text-conditional image generation with clip latents, 2022. 2 

diverse text-to-3d generation with variational score distillation. _Advances in neural information processing systems_ , 36: 8406–8441, 2023. 2 

   - [44] Danfei Xu, Yuke Zhu, Christopher B Choy, and Li Fei-Fei. Scene graph generation by iterative message passing. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 5410–5419, 2017. 3 

   - [45] Kun Yan, Lei Ji, Huaishao Luo, Ming Zhou, Nan Duan, and Shuai Ma. Control image captioning spatially and temporally. In _Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)_ , pages 2014–2025, Online, 2021. Association for Computational Linguistics. 3 

   - [46] Jingyi Zhang, Jiaxing Huang, Sheng Jin, and Shijian Lu. Vision-language models for vision tasks: A survey, 2024. 2 

- [31] Marc Rigter, Tarun Gupta, Agrin Hilmkil, and Chao Ma. Avid: Adapting video diffusion models to world models, 2024. 4 

- [32] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bj¨orn Ommer. High-resolution image synthesis with latent diffusion models, 2022. 2 

- [33] Aaditya Singh, Adam Fry, Adam Perelman, Adam Tart, Adi Ganesh, Ahmed El-Kishky, Aidan McLaughlin, Aiden Low, AJ Ostrow, Akhila Ananthram, et al. Openai gpt-5 system card. _arXiv preprint arXiv:2601.03267_ , 2025. 12 

- [34] Tomohiro Tachi. Simulation of rigid origami. In _Origami_<sup>4</sup> _: Fourth International Meeting of Origami Science, Mathematics, and Education_ , pages 175–187. AK Peters/CRC Press, 2009. 3, 4 

- [35] Tomohiro Tachi. Freeform variations of origami. _Journal for Geometry and Graphics_ , 14(2):203–215, 2010. 2, 3 

- [36] ByteDance Seed Team. Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023. 2 

- [37] Gemini Team, Rohan Anil, Sebastian Borgeaud, JeanBaptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. 12 

- [38] Gemini Robotics Team. Gemini robotics: Bringing ai into the physical world, 2025. 2 

- [39] OpenAI Team. Gpt-4 technical report, 2024. 2 

- [40] Qwen Team. Qwen3 technical report, 2025. 2 

- [41] Tongxuan Tian, Haoyang Li, Bo Ai, Xiaodi Yuan, Zhiao Huang, and Hao Su. Diffusion dynamics models with generative state estimation for cloth manipulation. _arXiv preprint arXiv:2503.11999_ , 2025. 2 

- [42] Vikram Voleti, Chun-Han Yao, Mark Boss, Adam Letts, David Pankratz, Dmitry Tochilkin, Christian Laforte, Robin Rombach, and Varun Jampani. Sv3d: Novel multi-view synthesis and 3d generation from a single image using latent video diffusion. In _European Conference on Computer Vision_ , pages 439–457. Springer, 2024. 2 

- [43] Zhengyi Wang, Cheng Lu, Yikai Wang, Fan Bao, Chongxuan Li, Hang Su, and Jun Zhu. Prolificdreamer: High-fidelity and 

# **Appendix** 

## **A. More Model and Implementation Details** 

_Learn2Fold_ is implemented as a neuro-symbolic planning system over a canonicalized crease-pattern graph representation. Given a high-level semantic goal and the current origami state, the system maintains a unified graph-state interface that is shared across data generation, model training, and inference-time planning. Concretely, each instance is represented by a canonicalized crease-pattern graph together with its dynamic folding state, so that structurally equivalent patterns can be processed in a consistent index space. On top of this representation, we train a lightweight decoder-only language model to generate structured folding actions under a fixed JSON schema, which serves as the proposal policy during inference. To ground the proposal process in physical feasibility, we additionally train a graph-structured world model on large-scale synthetic folding transitions produced by the symbolic Level-0 simulator. The world model is optimized with supervised learning to predict short-horizon state evolution and soft constraintviolation signals, allowing the planner to estimate future failure modes before execution. In our implementation, the world model is trained on approximately 76,000 transitions collected from expert demonstrations and constraint-guided perturbations for 50 epochs, which takes about 30 hours on a single NVIDIA RTX Pro 6000 GPU. The language model is trained on roughly 10<sup>4</sup> expert folding steps augmented with simulator-verified perturbations, and converges within 6 hours on the same hardware using LoRA adapters [13]. At inference time, _Learn2Fold_ operates in a model predictive control loop: at each step, the language model proposes _N_ = 8 candidate actions, the Level-0 simulator deterministically filters out invalid candidates, and the world model performs short-horizon lookahead scoring over the remaining valid actions to select the final execution step. All experiments are conducted with fixed random seeds for reproducibility. 

## **B. Evaluation Protocol** 

This section provides additional details on the evaluation setup used in the main paper. To assess both structured action prediction and long-horizon folding reliability, we evaluate all methods on a held-out benchmark constructed from 25 origami categories spanning three difficulty tiers: simple, intermediate, and complex. As described in the main paper, the benchmark is designed to cover a broad range of folding complexity, from basic rigid-folding patterns with minimal layering to long-horizon sequences involving nonlocal dependencies and strict structural constraints. Following the dataset split used throughout the paper, 80% of the _OrigamiCode_ data is used for training and the remaining 

20% is reserved for evaluation. Each evaluation instance consists of a canonicalized crease pattern together with its target semantic goal and reference folding program. The final test suite contains 3,840 text prompts spanning the 25 categories, from which we select 1,150 cases for validation. For each evaluated method, we perform two independent runs per prompt in order to reduce variance due to stochastic decoding and obtain a more stable estimate of long-horizon generation performance. 

We compare _Learn2Fold_ against two classes of baselines. The first class consists of prompted foundation models, including GPT-5.1, GPT-5.2 [33], and Gemini [37], which are prompted to generate structured folding programs from the same held-out benchmark inputs. These baselines are provided with in-context demonstrations and are evaluated under the same structured output interface as our method whenever possible, so that their predictions can be parsed by the same evaluator. The second class is BrickGPT [28], a finetuned reactive baseline adapted from assembly synthesis, which uses rollback-based trial-and-error execution to reject unstable steps and is trained on the same _OrigamiCode_ dataset as described in the main paper. This evaluation design allows us to compare semantic-only proposal systems, reactive execution-based baselines, and our full graph-guided planning system under a common benchmark protocol. 

We report both step-level and trajectory-level metrics. At the step level, we measure Precision, Recall, and F1 on structured action tokens under a unified action schema. These metrics quantify how accurately a method predicts the discrete content of each folding action, including operation type and associated structured arguments, while also capturing coverage over the full program. In the main paper, these are reported as the evaluator’s category-averaged micro scores. At the trajectory level, we report Category Success Rate (Cat-SR) and Edge-IoU. Cat-SR is defined as the fraction of folding sequences that successfully complete the target origami within each category and is then macroaveraged across categories to mitigate class imbalance. Edge-IoU measures structural alignment between predicted and reference actions by computing the intersection-overunion between the affected-edge set induced by the predicted action and the simulator-derived ground-truth mask. Together, these metrics distinguish local action correctness from global execution success and allow us to separately assess symbolic fidelity, structural grounding, and longhorizon robustness. 

For _Learn2Fold_ , evaluation follows the same inference procedure described in the main paper. At each step, the language model proposes multiple candidate actions, the Level-0 simulator discards invalid candidates, and the learned world model scores the remaining valid actions through short-horizon lookahead before one action is se- 

lected for execution. A trajectory is rolled out autoregressively until the program terminates or the method fails to produce a valid continuation. For the ablation experiments, we use the same held-out protocol and compare three configurations: LM only, LM+WM, and the full LM+WM+Level0Sim system. These variants are evaluated under both IID and OOD CP holdout settings using step validity, trajectory success rate, and final goal distance, following the setup described in Sec. 4.4 of the main paper. This shared protocol ensures that gains from the world model and the symbolic verifier are measured under the same benchmark conditions rather than under separate task definitions. 

Unless otherwise noted, all experiments are conducted with fixed random seeds. The same canonicalized CP representation and unified action schema are used for training, decoding, parsing, and evaluation, which avoids representation mismatch across methods and allows all predictions to be assessed under a common symbolic interface. In the supplementary material, we additionally provide more qualitative examples, representative failure cases, and example structured outputs to further clarify how the above protocol is instantiated in practice. 

