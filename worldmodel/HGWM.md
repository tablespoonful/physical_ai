---
title: "HGWM: Hierarchical Graph-guided World Model for Zero-shot Object Navigation via Scene-Goal Graph Matching"
date: "2026"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2610.32554
pdf: https://arxiv.org/pdf/2610.32554
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.32554)** / [論文ページ](https://arxiv.org/abs/2610.32554)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **HGWM: Hierarchical Graph-Guided World Model for Zero-Shot Object Navigation via Graph Matching** 

I-Tak Ieong Hao Tang<sup>*</sup> 

Tsinghua University Peking University 

*Corresponding author. 

Project page Code 

## **Abstract** 

Zero-shot object navigation requires an agent to reason about where a target may be found while retaining evidence from previous observations. We present HGWM, a hierarchical graph-guided world model that combines a category-conditioned room–anchor prior with persistent spatial-semantic memory. A coarse stage uses a vision-language model to score candidate headings, while a fine stage explicitly compares observed objects and relations with the goal prior. Phase-dependent fusion integrates these signals with a language-model recommendation to guide local navigation. HGWM achieves 62.6% success rate (SR) and 31.5% success weighted by path length (SPL) on HM3D v0.1, improving over WMNav by 4.5 and 0.3 percentage points, respectively. On MP3D, it achieves 46.8% SR and 17.9% SPL, with gains of 1.4 and 0.7 points. On HM3D v0.2, the full model reaches 74.4% SR and 31.9% SPL; removing individual components reduces SR by 0.9–2.3 points and SPL by 0.6–1.5 points. These results support the use of relational priors and persistent graph memory for target-directed search. 

## **1 Introduction** 

Navigation in an unfamiliar environment benefits from both recognizing visible objects and anticipating where a target might be found. Foundation-model agents provide openvocabulary semantic cues [17, 26], but ambiguous observations and incomplete spatial memory can still lead to unproductive search. A useful prior should guide exploration without being mistaken for a verified map of the environment. 

We study two design challenges: retaining observations across viewpoints and using prior room–object relations to assess candidate directions. VLM detections can be incorrect, while common indoor associations need not hold in every scene. Structural checks may therefore help reject some misleading interpretations but can also suppress valid, atypical observations. 

HGWM addresses these challenges through a _predict-thenground_ design. An LLM first generates a hierarchical goal graph describing plausible rooms, anchors, and connections. During navigation, RGB-D observations populate a persistent spatial-semantic graph. Coarse visual-semantic scoring and fine prior-conditioned matching then inform action selection. Here, grounding means relating a hypothesis to sensor-derived evidence, not proving that either graph is correct. 

A category such as bed specifies no room instance, route, or viewpoint. A room–anchor hypothesis supplies plausible search contexts before the target appears, while memory records encountered evidence. Their compatibility gives relational context a defined role in ranking where to look next. Our contributions are threefold: 

- A symbolic predictive navigation state coupling a hierarchical goal prior with persistent spatial-semantic graph memory. 

- A two-stage decision rule that separates prior-conditioned visual scoring from explicit, direction-specific matching of observed and hypothesized relations. 

- Evaluation on HM3D and MP3D, including four additional component ablations on HM3D v0.2, analysis of success and path efficiency, and qualitative navigation examples. 

Relative to WMNav, HGWM improves SR by 4.5 percentage points (pp) on HM3D v0.1 and 1.4 pp on MP3D, with SPL gains of 0.3 and 0.7 pp. We examine the contribution of each component through ablations and use navigation traces to illustrate how the agent responds to changing observations. 

## **2 Related Work** 

**Semantic search and spatial maps.** ObjectNav methods differ in how they represent prior knowledge and retain observations [13, 20]. Habitat-Web and OVRL-V2 learn navigation capabilities from task data [19, 24]; ZSON, CoW, ESC, OpenFMNav, and semantic-frontier approaches exploit pretrained representations or commonsense knowledge [6, 9, 15, 16, 35]. VLFM accumulates visual-language relevance in a frontier value map [28]. VoroNav uses a reduced Voronoi graph and path descriptions for waypoint reasoning [22], while BeliefMapNav estimates target-location belief in a 3D voxel space and plans sequences of destinations [36]. Together with 3D-Aware and ApexNav [30, 31], these systems establish spatial memory and target-directed search as important design choices. HGWM focuses on a complementary question: how a category-conditioned relational hypothesis should influence the score assigned to each candidate heading. 

1 


Figure 1: HGWM architecture. The LLM generates a hypothetical room–anchor prior, observations populate spatial-semantic memory, and graph-guided reasoning informs navigation. Hallucinated Prior and Structural Verification denote prior generation and heuristic compatibility checks; neither establishes scene truth. System 1/2 labels are conceptual analogies. 

**Scene graphs for embodied reasoning.** SOON, HOZ, and ConceptGraphs use structured scene representations [10, 32, 37]. SG-Nav builds an online hierarchy of objects, groups, and rooms, uses hierarchical language-model reasoning, and introduces graph-based re-perception [25]. HGWM therefore builds on an established use of graphs for context and perception review. Its specific design couples observed memory with a separate room–anchor hypothesis and makes their compatibility an explicit decision signal alongside visual-semantic scores. The contribution concerns this prior-to-action interface, rather than scene-graph construction alone. 

**Goal graphs and the ObjectNav setting.** UniGoal is the closest graph-matching reference [26]. It unifies object, image, and text goals, matches node and edge embeddings, evaluates graph-edit similarity, and switches exploration strategies according to the matching state. Its paper explicitly notes that an ObjectNav category becomes a single goal node, disabling goal-graph decomposition and anchor-pair alignment in that setting. HGWM expands the category into room hypotheses, anchor objects, and relations before observation. This expansion supplies relational search cues even when the requested goal is only an object category. HGWM then scores headings with explicit symbolic features and phase-dependent fusion; UniGoal uses matched graph structure and, where applicable, anchor alignment to generate exploration destinations. Both use graph matching and staged reasoning, but they differ in the 

category-goal representation and the mechanism connecting matching to navigation. 

**VLM decision memory.** WMNav scores panoramic views, accumulates a curiosity value map, and combines subtask feedback with a two-stage action proposer [17]. HGWM retains this useful map-and-policy structure while adding a separate goal prior, persistent relational evidence, and a fine compatibility channel. Its decision rule combines visual promise, graph compatibility, and an LLM direction recommendation using coefficients selected from the current matching state. This specifies how graph context changes the input to the stored direction-value map; it does not treat memory or subtask decomposition as new in themselves. 

**Predictive models and HGWM’s contribution.** SGM predicts missing regions of semantic maps [33]. World Models, Dreamer, Pathdreamer, and Navigation World Models learn predictive representations of environments [2, 11, 12, 14]. HGWM uses pretrained models to form a symbolic hypothesis and compare it with observed evidence, without training a dynamics model or synthesizing future observations. Predictive coding is a conceptual motivation [7, 8]. The methodological contribution is the combination of category-to-graph expansion, direction-specific compatibility, and phase-dependent fusion within persistent decision memory. The experiments distinguish whole-configuration performance from evidence 

2 

about each component. 

## **3 The Proposed Method** 

HGWM maintains a symbolic predictive navigation state: a goal prior, an observation memory, and scores for candidate headings. The term _world model_ denotes this state, not a learned dynamics simulator. Figure 1 shows the perception– memory–decision loop. Section 4.2 describes the experimental setup. 

### **3.1 Task and Decision State** 

The target is an object category _c_ . At decision step _t_ , the agent receives RGB-D observations _Ot_ = ( _It , Dt_ ) and a planar pose _Pt ∈ SE_ (2). The panoramic scorer uses six relative headings _A_ = _{_ 30 _,_ 90 _,_ 150 _,_ 210 _,_ 270 _,_ 330 _}_<sup>_◦_</sup> . A high-level decision selects a search direction and a short-horizon subtask; the local navigator then selects a feasible displacement. The 40-step horizon counts agent decision iterations, not a uniform metric distance traveled. 


Here _ct_<sup>_α∈_[0</sup><sup>_,_10] is a coarse score and</sup><sup>_f α_</sup> _t_<sup>_∈_[0</sup><sup>_,_1] is a symbolic</sup> compatibility score. Neither is a posterior probability. Success requires the stopping condition within 1 _._ 0m of a target instance under the evaluation protocol, rather than complete alignment of the graphs. 

### **3.2 Goal Prior and Observation Memory** 

Given _c_ , an LLM returns a structured prior containing likely rooms, alternative rooms, anchor objects, and room connections: 


This graph is a category-conditioned hypothesis, not a map of the particular scene. We cache each goal prior within an episode and clear the cache on reset; independent episodes can therefore use different priors. 

**What is predicted.** The prior describes object categories and plausible relations, rather than asserting coordinates for unseen objects. For example, a bed query can suggest a bedroom and nearby furniture as search context. A detected anchor contributes evidence for a direction even before the bed is visible; failure to observe that anchor is not proof that a bed is absent. Alternative rooms in the prior preserve multiple search hypotheses. Hypothetical nodes are kept separate from observation records so that an expected object is not counted as a detected object merely because the LLM mentioned it. 

Spatial-semantic memory stores object names, inferred rooms, observation counts, and estimated map positions. The agent queues depth-based navigation rays before the VLM response arrives, then associates each directional description with the nearest available view-center ray within 30<sup>_◦_</sup> . Projection uses pose, a maximum ray distance of 3m, and 100 

map pixels per meter. These are coarse positional estimates for a view, not precise object bounding-box projections. The current local graph additionally uses textual spatial and depth cues. 

For each direction, current observations and retrieved memory are normalized into one graph contract before matching. It exposes consistent flat and typed views of room nodes, object nodes, adjacency, object relations, and containment. Field aliases are resolved once, objects retain stable identifiers, and observed room membership supplies containment edges. Current attributes take precedence for the same identifier. This boundary prevents a scorer from silently reading a different graph representation. Matching uses symbolic features, without a learned graph-embedding network. 

### **3.3 Coarse Visual-Semantic Scoring** 

The VLM receives the panorama, goal, and prior context and returns a JSON record per heading with a score, objects, room, path assessment, and explanation: 


The requested score range is 0–10. A score of 10 is reserved for a visible target according to the model; 0 denotes a dead end with no visible target; 1–9 encodes intermediate opportunities. This is a model judgment, not a validated detector confidence. Because the same goal prior already enters this prompt, the fine stage adds an explicit computation rather than exclusive access to prior knowledge. The parser supplies 5 when a score is absent, and uses score 5 for all headings if the entire directional extraction fails. The fusion routine consumes this scale directly: it does not apply candidate-set min–max normalization or episode-level z-score normalization. Malformed or out-of-range responses remain an implementation concern, not an assumed probabilistic guarantee. 

### **3.4 Fine Symbolic Compatibility** 

The refinement prompt asks the LLM to review relations using scene descriptions and goal context. The application routine retains nodes, accepts proposed relations between known nodes, and preserves unmodified edges with confidence greater than 0.7. All typed edge views are rebuilt from the edited edge set, preventing discarded relations from surviving in a stale representation. This operation remains heuristic and can mishandle atypical arrangements; it is not a verified node-pruning procedure. 

Let **s**<sup>_α_</sup> = ( _sr, so, sp, sm, sd_ ) denote five features: room, object, spatial, semantic, and depth. The code compares names, sets, and relations. The room feature combines Jaccard overlap of room names (0.5), overlap of spatial regions (0.3), and connectivity (0.2). The object feature compares visible objects and stored objects with the prior, and with each other. It also rewards matching anchors and rooms. Spatial compatibility combines room relations (0.4), object relations (0.4), and relations between levels (0.2). Each term compares canonical endpoint names and relation labels, dividing the intersection size 

3 


Figure 2: Coarse-to-fine illustration with example trajectory views. Coarse VLM scores use 0–10: 0 for a dead end without a visible target, 1–9 for intermediate opportunities, and 10 for a model-reported visible target. The example fine scores are heuristic compatibility values, not calibrated probabilities. The ordered phase thresholds are defined in the text. 


Figure 3: Fine-matching illustration. Corrected Scene Graph denotes the graph after heuristic relation proposals, not verified truth. The illustrated embedding similarity is interpreted as symbolic feature comparison, without a learned graphembedding network. Equation 6 specifies all five features, including semantic and depth terms in addition to the illustrated object, room, and spatial terms. 

by the larger relation-set size; absent evidence gives zero. Semantic consistency combines agreement of visible and stored objects (0.4), graph richness (0.3), and goal relevance (0.3). The supplement defines the bonuses, defaults, and weight 

cases. For name and region sets, the overlap convention is 


For depth-layer proportions **p** and reference proportions **q** = (0 _._ 3 _,_ 0 _._ 4 _,_ 0 _._ 3), define 


Missing depth observations give _sd_ = 0. The fine score is 


Weights depend on detected prior-associated objects, scene quality, and room/object match scores. The default vector in room, object, spatial, semantic, and depth order is (0 _._ 35 _,_ 0 _._ 30 _,_ 0 _._ 20 _,_ 0 _._ 10 _,_ 0 _._ 05). The bonus _b_<sup>_α_</sup> rewards partial matches and reliable relations. _d_<sup>_α_</sup> is direction relevance of nearby stored observations, and _h_<sup>_α_</sup> is a depth-direction factor; both default to 1 when the corresponding memory is unavailable. An exception in overlap calculation returns _ft_<sup>_α_= 0</sup><sup>_._5</sup> and records its cause. Empty observations receive no positive graph-match evidence. Per-direction diagnostics record graph sizes, feature scores, and fallback status; the score remains a heuristic rather than a calibrated probability. 

4 

Table 1: Phase-dependent fusion coefficients. 

|Phase|_a_(coarse)|_b_(fine)|_e_(LLM)|
|---|---|---|---|
|Frontier exploration|0.6|0.1|0.5|
|Focused search|0.6|0.4|0.4|
|Target verification|0.8|0.5|0.2|


### **3.5 Phase-Dependent Fusion** 

Let _f_<sup>¯</sup> _t_ and _ft_<sup>_max_</sup> be the mean and maximum fine scores across the six headings. Target verification takes precedence when _ft_<sup>_max_</sup> _≥_ 0 _._ 7; otherwise focused search applies when _f_<sup>¯</sup> _t ≥_ 0 _._ 4 or _ft_<sup>_max_</sup> _≥_ 0 _._ 5; frontier exploration applies otherwise. The LLM receives the directional scene descriptions, scores, and phase, and returns a recommended direction _α_ ˆ _t_ and a scalar _ut_ . The scalar is a reasoning output, not a calibrated confidence interval. Its contribution is 


For _ct_<sup>_α<_10, the fusion rule is</sup> 


If _ct_<sup>_α≥_10,the implementation sets</sup><sup>_q_</sup> _t_<sup>_α_= 10.Table 1 gives</sup> the actual fusion coefficients. They are heuristic coefficients, not convex-mixture probabilities; clipping is therefore part of the definition. 

**Prior information versus explicit matching.** Prompting can exploit relations implicitly. HGWM additionally compares named endpoints and relation labels, so equal object sets can receive different spatial scores when their relations differ. At a fixed state with _ct_<sup>_α<_10, hold the prior, graph, coarse scores,</sup> phase coefficients, and LLM output constant. Replacing the fine contribution by an equal-coefficient coarse contribution gives the unclipped diagnostic 


This separates the numerical matching channel from prior access and coefficient mass. It is an algebraic diagnostic, not a measured navigation ablation; phase selection and LLM outputs can themselves depend on matching. The supplement defines controls for these distinct effects. 

### **3.6 Memory Update and Local Action Selection** 

Fused directional values update the spatial curiosity map. Regions shared by adjacent headings receive the mean of their values; the base policy merges them with stored map values and selects the heading with the greatest regional mean. Thus selecting the largest instantaneous _qt_<sup>_α_alonedoesnot</sup> fully specify the policy. A planning VLM uses the selected view, previous subtask, goal, and graph context to propose the next subtask and goal flag. The local action selector reasons 

over annotated feasible displacements; depth-derived navigability constrains motion. Stopping and navigation remain model-driven decisions and can fail despite a high score. The accompanying code provides the prompt builders and scoring routines. 

More precisely, let _Vt_ ( _x_ ) denote the stored curiosity value at map cell _x_ , and let _vt_ ( _x_ ) be the fused value projected from the current panorama. For cells updated by the base policy, the merge is 


Cells outside the update mask retain their previous values; cells in the goal mask are assigned 10. A valid directional region is ranked by its mean stored value. This inherited conservative update makes the decision depend on previously accumulated evidence, not just the latest panorama. It can also preserve an erroneous low score, which motivates evaluating failures at the trajectory level. 

### **3.7 Execution and Information Flow** 

Each navigation decision follows the same information flow: 

1. Obtain the panorama, depth, and pose; generate or reuse the goal prior for the current episode. 

2. Request the six visual direction scores together with object, room, and path descriptions. 

3. Associate semantic descriptions with spatial memory and form direction-specific graph evidence. Where enabled, request relation proposals before computing compatibility features. 

4. Compute the fine scores, choose the exploration phase, and obtain the joint LLM direction recommendation. Apply the phase coefficients and score clipping. 

5. Update the curiosity map, select a direction, and use the chosen view and previous subtask to produce the next local objective. 

6. Select a feasible displacement from the annotated action candidates, execute it, and use the next observation to continue or stop. 

This ordering separates the goal hypothesis, observed evidence, direction ranking, and motion interface. It also identifies what an ablation changes: the prior affects contextual conditioning; relation refinement affects graph evidence; arbitration affects the fused score; and weight adaptation changes the fine feature mixture. None of these changes requires treating an LLM score as a calibrated probability. 

## **4 Experiments** 

We report simulation experiments on HM3D and MP3D to evaluate the complete HGWM configuration. The experiments do not include physical-robot trials or a systematic sensornoise robustness protocol. 

5 


Figure 4: Decision process comparison between WMNav and HGWM. In these selected examples, HGWM visits different regions and exhibits less repeated exploration. These trajectories illustrate behavior; they do not establish an aggregate reduction in looping or isolate the effect of graph matching. 

### **4.1 Datasets and Evaluation Metrics** 

Datasets. We evaluate on HM3D v0.1, HM3D v0.2, and MP3D [5, 18]. We report main comparisons on HM3D v0.1 for consistency with prior work, and use HM3D v0.2 for the threeconfiguration component comparison. Results from these splits should not be pooled as if they used the same episodes. Evaluation metrics. We report Success Rate (SR) and Success weighted by Path Length (SPL), following standard ObjectNav evaluation protocols [1, 3]. These metrics measure navigation effectiveness and efficiency, respectively. Figure 4 illustrates selected trajectories; repeated exploration is not reported as a quantitative metric. 

**Reading SR and SPL together.** For _N_ episodes, let _si_ indicate success, _li_ be the shortest valid path length, and _pi_ be the traveled path length. The reported percentage metrics are 


SR measures completion frequency; SPL also penalizes excess travel on successful episodes. A higher SR therefore need not imply a higher SPL. All differences below are absolute percentage-point changes, computed within a dataset and split; HM3D v0.1 and v0.2 results are kept separate. 

### **4.2 Implementation and Reproducibility** 

The agent is configured for at most 40 navigation steps per episode, with a cylindrical body of radius 0 _._ 18m and height 0 _._ 88m. Its RGB-D camera has a resolution of 640 _×_ 480, a 79<sup>_◦_</sup> horizontal field of view, and a 14<sup>_◦_</sup> downward pitch. The success threshold is _dthres_ = 1 _._ 0m. The navigation-map scale is 100 pixels per meter. 

Gemini-1.5-Pro provides scene understanding and coarse scores, while Qwen2.5-7B-Instruct generates goal priors, proposes relation updates, and recommends directions. Goal priors are cached within each episode. The implementation records configuration and source identifiers, episode identities, model-call counts, and elapsed time. We use HM3D v0.1 and MP3D for comparisons with prior methods and HM3D v0.2 for component analysis. For the main HGWM setting on HM3D v0.1, we also summarize variation across three runs. 

### **4.3 Main Results** 

Table 2 reports HGWM at 62.6% SR and 31.5% SPL on HM3D v0.1, compared with WMNav’s 58.1% and 31.2%: gains of 4.5 pp SR and 0.3 pp SPL. On MP3D, HGWM reports 46.8% SR and 17.9% SPL versus 45.4% and 17.2%, giving 1.4 pp SR and 0.7 pp SPL. In particular, the path-efficiency gains are modest. OVRL-V2 has a higher reported HM3D SR (64.7%) but uses a different training regime. 

Across three HGWM runs on HM3D v0.1, SR ranges from 62.3 to 62.8 and SPL from 31.2 to 31.7. These observed 

6 

Table 2: Comparison on HM3D v0.1 and MP3D. SR and SPL are percentages; higher is better. Baseline results are taken from the cited papers and use their respective training and model settings. For HGWM on HM3D v0.1, superscripts and subscripts <u>give the maximum and minimum deviations across three runs, not confidence intervals.</u> 

|**Method**|**Vision**|**Language**|**HM3**<br>|**D v0.1**<br>|**MP**<br>|**3D**<br>|
|---|---|---|---|---|---|---|
||||**SR**_↑_|**SPL**_↑_|**SR**_↑_|**SPL**_↑_|
|Habitat-Web [19]|-|-|41.5|16.0|31.6|8.5|
|OVRL [23]|-|-|-|-|28.6|7.4|
|OVRL-V2 [24]|-|-|64.7|28.1|-|-|
|ZSON [16]|CLIP|-|25.5|12.6|15.3|4.8|
|PSL [21]|CLIP|-|42.4|19.2|18.9|6.4|
|PixNav [4]|LLaMA-Adapter|GPT-4|37.9|20.5|-|-|
|SGM [33]|-|-|60.2|30.8|37.7|14.7|
|VLFM [28]|BLIP-2|-|52.5|30.4|36.4|17.5|
|CoW [9]|CLIP|-|-|-|9.2|4.9|
|ESC [35]|-|GPT-3.5|39.2|22.3|28.7|14.2|
|L3MVN [29]|-|GPT-2|50.4|23.1|-|-|
|VoroNav [22]|BLIP|GPT-3.5|42.0|26.0|-|-|
|HyPerNav [27]|Qwen-VL-7B-Instruct|-|56.3|29.7|43.8|16.9|
|TopV-Nav [34]|-|-|45.9|28.0|31.9|16.1|
|SG-Nav [25]|LLaVA-1.6-7B|GPT-4|54.0|24.9|40.2|16.0|
|UniGoal [26]|LLaVA-1.6-7B|LLaMA-2-7B|54.5|25.1|41.0|16.4|
|WMNav [17]|Gemini-1.5-Pro|-|58.1|31.2|45.4|17.2|
|**HGWM (Ours)**|**Gemini-1.5-Pro**|**Qwen2.5-7B-Instruct**|**62**_._**6**<sup>+0</sup><sup>_._2</sup><br>_−_0_._3|**31**_._**5**<sup>+0</sup><sup>_._2</sup><br>_−_0_._3|**46.8**|**17.9**|


Table 3: Differences between configurations in percentage points, computed from the corresponding SR and SPL values. 

|Comparison|∆SR|∆SPL|
|---|---|---|
|HGWM–WMNav, HM3D v0.1|+4.5|+0.3|
|HGWM–WMNav, MP3D|+1.4|+0.7|
|Voxel–no memory, HM3D v0.2|+3.1|+0.8|
|HGWM–voxel, HM3D v0.2|+3.5|+1.8|


Table 4: Two-backbone sensitivity on HM3D v0.1. Changes from the default are in percentage points (pp). 

|**VLM Backbone**|**SR (%)**|**SPL (%)**|
|---|---|---|
|Gemini-1.5-Pro|**62.6**|**31.5**|
|Gemini 2.0 Flash|59.2|30.8|
|Change (pp)|_−_3_._4|_−_0_._7|


### **4.5 Backbone Sensitivity** 

ranges are not confidence intervals. The SPL range reaches WMNav’s point estimate of 31.2, so the clearest improvement is in completion rate rather than a consistent gain in path efficiency. 

Table 3 summarizes the gains in success rate and SPL within each dataset. 

### **4.4 Qualitative Navigation Behavior** 

Figure 4 illustrates selected WMNav and HGWM trajectories. The supplementary case collection contains 18 navigation traces, covering 338 step directories and 337 text records. Each case includes its available step logs and views selected by the same first/middle/last rule. These examples show the observations, model responses, and decisions underlying a search trajectory; they complement the quantitative evaluation rather than estimate loop frequency. 

Table 4 compares two VLM settings on HM3D v0.1. Replacing Gemini-1.5-Pro with Gemini 2.0 Flash changes SR from 62.6% to 59.2% and SPL from 31.5% to 30.8%, decreases of 3.4 and 0.7 pp. The larger change in SR suggests that successful search is more sensitive to the backbone in this comparison. Evaluating additional model families would help determine how broadly this pattern holds. 

### **4.6 Component Analysis on HM3D v0.2** 

Table 5 compares three memory configurations and four component ablations on HM3D v0.2. The full model achieves 74.4% SR and 31.9% SPL. Basic VLM navigation obtains 67.8/29.3, while voxel memory with direct VLM scoring obtains 70.9/30.1. The configuration comparison changes both memory representation and decision scoring; the component ablations examine specific parts of the full system. 

**Prior and relation evidence.** Removing the goal prior yields 72.1% SR and 30.8% SPL, decreases of 2.3 and 1.1 

7 

Table 5: Configurations and component ablations on HM3D v0.2. Metrics are percentages; differences are percentage points relative to full HGWM. The first two baselines change the overall configuration. Non-adaptive weights denote a single control, not separate uniform and static experiments. 

|Configuration|SR (%)|SPL (%)|∆SR|∆SPL|
|---|---|---|---|---|
|Basic VLM / no memory|67.8|29.3|_−_6_._6|_−_2_._6|
|Voxel memory + direct VLM scoring|70.9|30.1|_−_3_._5|_−_1_._8|
|**HGWM (full)**|**74.4**|**31.9**|0.0|0.0|
|Without goal prior|72.1|30.8|_−_2_._3|_−_1_._1|
|Without relation refinement|72.1|30.4|_−_2_._3|_−_1_._5|
|Without LLM arbitration|72.7|31.1|_−_1_._7|_−_0_._8|
|With non-adaptive fine weights|73.5|31.3|_−_0_._9|_−_0_._6|


points. Disabling relation refinement gives 72.1% SR and 30.4% SPL, decreases of 2.3 and 1.5 points. The larger SPL drop supports the contribution of relation processing at the aggregate level. The prior supplies scoring context; refinement changes matching evidence. Paired trajectories are needed to determine which episodes benefit. 

**Meaning of the interventions.** The no-prior control retains the target category but uses an unknown room, empty room connections, and a minimal goal anchor. It removes the explicit room–anchor hypothesis while retaining the pretrained models’ background knowledge. The no-refinement control bypasses relation updates. The no-arbitration control removes the LLM term without renormalizing the remaining coefficients, so it changes both information and score scale. The non-adaptive control changes the five fine-feature weights rather than the phase-dependent fusion coefficients. 

**Arbitration and adaptive weighting.** Without LLM arbitration, performance is 72.7/31.1, below the full model by 1.7 SR and 0.8 SPL points. The non-adaptive fine-weight control gives 73.5/31.3, decreases of 0.9 and 0.6 points. Both results favor the full fusion design in this comparison. Their relative drops should not be interpreted as additive contributions: each intervention is evaluated against the full configuration, and joint removals are not reported. Separate uniform and static controls would be needed to compare those two choices. 

comparison, scene–goal graph matching improves SR by 1.5 points and SPL by 1.4 points over prior prompting. These gains suggest that computing compatibility between observed and expected relations can provide useful information beyond including the prior in a prompt. The latter comparison is summarized by aggregate differences rather than split-specific absolute scores, so it provides supporting evidence rather than a complete isolation of all downstream matching effects. 

### **4.7 Efficiency and Limitations** 

Gemini-1.5-Pro inference takes approximately 2.3 seconds per call, while graph updates take 12–25 ms at the tested episode lengths. Model inference therefore dominates the graphprocessing cost. Reusing the goal prior within an episode avoids repeated prior-generation calls. These component timings do not measure complete navigation latency, which also includes perception, planning, communication, and motion. **Query and latency accounting.** One panoramic response covers six headings; prior generation, relation reasoning, arbitration, and planning can add calls. Thus per-call latency is not full-step latency. The runner records client calls and elapsed time by role. Provider-internal retries, token usage, simulation time, and motion time still require separate accounting; using the same evaluation episodes does not ensure equal inference cost. 

**Separating information from score scale.** A scale-matched counterpart to the no-arbitration control can be defined as 


This preserves the total coefficient mass while removing the LLM term. The no-arbitration result in Table 5 uses the unnormalized removal. The scale-matched alternative offers a way to separate the loss of reasoning information from the effect of rescaling the fused scores. The supplement discusses analogous controls for graph matching. 

**Evidence and robustness limits.** Our experiments use static Habitat environments. Physical deployment introduces localization and depth noise, moving objects, and atypical room layouts that may conflict with the prior. Errors in perception or pose can also persist in memory. The present comparisons do not quantify these effects or provide paired significance tests. The non-adaptive result does not distinguish uniform from static weighting, and the matching gain is summarized without split-specific absolute scores. Broader robustness tests, matched-cost comparisons, and complete per-run summaries would strengthen these findings. 

**Success, efficiency, and attribution.** Full HGWM improves over voxel memory by 3.5 SR and 1.8 SPL points. In a separate 

8 

## **5 Conclusion** 

HGWM expands category goals into relational priors and combines observed graph memory with scoring on a 0–10 decision scale. Simulation results show SR gains over WMNav and smaller SPL gains. Additional HM3D v0.2 interventions reduce SR by 0.9–2.3 points and SPL by 0.6–1.5 points relative to full HGWM. These findings support the combined design; component interactions, paired uncertainty, query cost, and deployment beyond simulation remain open evaluation questions. 

**Code Availability.** Code, prompt builders, and the case gallery are available at `https://github.com/itak04/ HGWM` and `https://itak04.github.io/HGWM/` . 

9 

## **Supplementary Material** 

## **A Goal Prior Construction** 

### **A.1 LLM Prompt Template** 

We present the high-level strategy template for goal subgraph construction; the source index identifies the executable builder, including its output schema and examples. The template is dynamically instantiated for each target object category, with `{goal}` replaced by the specific target (e.g., “bed”, “sofa”). 

You are an expert in residential navigation and spatial understanding. Create a comprehensive navigation strategy for efficiently locating a {GOAL} in a typical home environment. 

NAVIGATION STRATEGY ANALYSIS FOR {GOAL}: 

1. TARGET ROOM ANALYSIS: 

- (1) Primary room: The most likely room type where {goal} is typically found 

- (2) Secondary rooms: 1-2 alternative room types where {goal} might also be located 

- (3) Adjacent zones: Connected areas that provide visual access or pathways to target rooms 

2. PATHWAY and CONNECTIVITY MAPPING: 

- (1) Hallway connections: Common routes to reach target rooms from main areas 

- (2) Visual access points: Doorways/openings that help identify target rooms 

- (3) Navigation landmarks: Key reference points for wayfinding 

3. TARGET-ORIENTED SPATIAL ANCHORS 

- and NAVIGATION CUES: 

- (1) Directional anchors: 3-4 objects that DIRECTLY indicate where {goal} is likely located 

- (2) Visual pathways: Objects that form visual lines leading toward typical {goal} placement areas 

- (3) Distance indicators: Objects that help estimate proximity to {goal} 

- (4) Positioning cues: Furniture/fixtures indicating the specific area where {goal} is usually found 

4. SYSTEMATIC EXPLORATION APPROACH: 

- (1) Exploration priorities: Which areas to check first when searching 

- (2) Recovery strategies: What to do when initial search paths fail 

This structured prompt enables the LLM to generate hierarchical spatial knowledge encompassing room classifications, connectivity patterns, and object-based navigation cues, which are then parsed into the formal goal subgraph representation _Ggoal_ = ( _Vgoal, Egoal_ ) where nodes represent rooms/objects and edges encode spatial relationships. 

## **B Implementation Details** 

### **B.1 Agent Configuration** 

We configure the agent with a maximum of 40 navigation steps per episode. The agent has a cylindrical body with radius 0.18m and height 0.88m, equipped with an egocentric RGB-D camera at 640 _×_ 480 resolution and 79<sup>_◦_</sup> horizontal FOV. The camera is tilted down with a 14<sup>_◦_</sup> pitch to improve navigable area identification. The success threshold _dthres_ is set to 1.0m. Gemini-1.5-Pro is the primary VLM used for the reported experiments. 

### **B.2 Model Choices** 

**VLM Backbone:** Gemini-1.5-Pro serves as our primary vision-language model for both scene understanding (object detection, room classification) and coarse semantic scoring. The reported experiments do not include a matched cost or spatial-reasoning comparison against GPT-4V. 

**LLM Reasoner:** Qwen2.5-7B-Instruct generates goal priors, proposes relation updates, and recommends navigation directions. The implementation accesses the model through the SiliconFlow API. Its calls contribute to the overall reasoning cost alongside VLM perception and planning. 

## **C Coarse-to-Fine Reasoning** 

### **C.1 Score Domains and Phase Selection** 

For the six panorama headings, the coarse VLM prompt requests scores in [0 _,_ 10]. A model-reported visible target receives 10; an unpromising dead end without a visible target receives 0; intermediate opportunities receive 1–9. Missing individual scores default to 5, and failed directional extraction defaults all six headings to 5. A target score is not a ground-truth detection. 

The fine overlap is _f_<sup>_α_</sup> _∈_ [0 _,_ 1] in the intended score path. Let _f_<sup>¯</sup> and _f_<sup>_max_</sup> denote the mean and maximum over headings. The implemented schedule is ordered as follows: 

1. If _f_<sup>_max_</sup> _≥_ 0 _._ 7, use target verification. 

2. Otherwise, if _f_<sup>¯</sup> _≥_ 0 _._ 4 or _f_<sup>_max_</sup> _≥_ 0 _._ 5, use focused search. 

3. Otherwise, use frontier exploration. 

The main paper lists the three coefficient triples for verification, focused search, and exploration. The source names them spatial, semantic, and LLM weights. Here the first coefficient multiplies the coarse VLM score, despite its name; it does not multiply a separate depth score. 

The arbitrator returns a recommended heading _α_ ˆ and a scalar _u_ . The boost is _u_ for the recommended heading and max(0 _._ 2 _, u/_ 2) elsewhere. Fusion multiplies the fine score and LLM boost by 10, adds the weighted coarse score, clips to [0 _,_ 10], and rounds to two decimal places. A coarse score at least 10 overrides this rule with 10. The coefficients do not sum to one. No candidate-set or episode-level normalization, 

10 

estimated confidence bounds, or additional position-score multiplier is applied by this routine. Equal directional scores therefore require no division by a zero range or variance. Final heading selection also depends on the stored curiosity map. 

### **C.2 Symbolic Feature Definitions** 

All name-based set comparisons below lowercase strings. Define _J_ ( _A, B_ ) = _|A ∩ B|/_ max(1 _, |A ∪ B|_ ), so two empty sets have overlap zero. These are symbolic matching operations, not cosine similarity of learned embeddings. 

**Room feature** _sr_ **.** The prior room set contains names in its `nodes` list with one of the substrings kitchen, bathroom, bedroom, living, dining, or office. The observed set uses `room_nodes` . Known spatial-region labels form a second pair of sets. The score is 0 _._ 5 _J_ (rooms)+ 0 _._ 3 _J_ (regions)+ 0 _._ 2 _C_ , capped at one, where _C_ is the fraction of room pairs passing the room-connection predicate. For fewer than two observed rooms, we set _C_ = 0. The remaining connectivity predicate is heuristic, not a verified floor-plan relation. 

**Object feature** _so_ **.** Let _V_ be current VLM object names, _H_ observed graph object names, and _T_ the union of the requested category, prior anchors, and named prior object nodes. Let _P ⊆ H_ contain objects in matched rooms; if no rooms match, all observed graph objects are prioritized. Put _n_ = _|V ∩ T |_ and 


with _v_ = 0 when _n_ = 0. The stored-object score is 


The object feature is min _{_ 1 _,_ 0 _._ 7 _v_ + 0 _._ 2 _h_ + 0 _._ 1 _J_ ( _V, H_ )+ 0 _._ 1 _sr}_ if _n >_ 0, and min _{_ 1 _,_ 0 _._ 4 _v_ + 0 _._ 4 _h_ + 0 _._ 2 _J_ ( _V, H_ )+ 0 _._ 1 _sr}_ otherwise. The source’s `target_detected` flag means any member of _T_ matches, including an anchor; it is not exclusively detection of the navigation target. 

**Spatial feature** _sp_ **.** The spatial scorer uses _sp_ = 0 _._ 4 _r_ +0 _._ 4 _o_ + 0 _._ 2 _x_ . The three terms compare room, object, and containment relation sets respectively. A relation key consists of canonical endpoint names and a relation label, so different instance IDs do not prevent matching. Known symmetric relations (near, adjacent, connected) ignore endpoint order. Each score is the intersection size divided by the larger set size; a missing observed or expected set gives zero. 

**Semantic and depth features.** The semantic feature is the capped weighted sum 


where _A_ measures VLM–graph semantic alignment, _R_ measures hierarchical semantic richness, and _G_ measures goal 

relevance. Specifically, _A_ = _J_ ( _V, H_ ) with _A_ = 0 for two empty sets. For room, object, and total edge counts _nr, no, ne_ , richness is 


Goal relevance divides the number of matching observed objects by the number of named prior nodes, capped at one. Exact name matches count as 1 and predefined semantic-group matches as 0.5. No named prior nodes gives _G_ = 0 _._ 5. The groups are seating/work furniture; bedding; kitchen fixtures; bathroom fixtures; and books/shelves. The exact group members and predicates are listed in the source index. Exceptions in these three subterms return 0.5. These are deterministic heuristics, not a learned semantic model. For foreground, mid-ground, and background proportions _pk_ , the depth term is _sd_ = 3<sup><u>1</u>∑</sup><sup>_k_(1</sup><sup>_−|pk −qk|_) with</sup><sup>**q**= (0</sup><sup>_._3</sup><sup>_,_0</sup><sup>_._4</sup><sup>_,_0</sup><sup>_._3).When no</sup> depth-layer observations are present, the depth score is _sd_ = 0 rather than a near-reference default distribution. 

### **C.3 Fine Weights, Bonuses, and Direction Factors** 

The first satisfied row of Table 6 determines the weight vector. Scene quality is 


capped at one. Here _v frac_ and _h frac_ are the fractions of voxelvalidated and high-precision objects, and the two means summarize relation and room confidence fields. Terms with no supporting objects/relations/rooms contribute zero. 

The additive bonus has three independently applicable terms: (i) min(0 _._ 15 _,_ 0 _._ 2 _sosd_ ) if 0 _._ 3 _≤ sr <_ 0 _._ 8, _so >_ 0 _._ 5, and _sd >_ 0 _._ 6; (ii) min(0 _._ 15 _,_ 0 _._ 15 _sr_ + 0 _._ 1 _Q_ ) if 0 _._ 3 _≤ so <_ 0 _._ 8 and _sr >_ 0 _._ 5; and (iii) min(0 _._ 1 _,_ 0 _._ 1¯ _crel_ ) if relations exist and their mean confidence exceeds 0.7. 

For a stored map cell _i_ at distance _ri <_ 200 map pixels, let _δi_ be the wrapped angular difference to the candidate heading, _vi_ = max(0 _._ 1 _,_ 1 _− ri/_ 200), and _ni_ = min(1 _, Ni/_ 5) for observation count _Ni_ . Direction relevance is 


It defaults to 1 without stored semantic memory or an available agent pose. The depth-direction factor is _h_<sup>_α_</sup> = min(1 _._ 2 _, pF uF_ + _pBuB_ + 1 _− pF − pB_ ): ( _uF , uB_ ) = (1 _._ 2 _,_ 0 _._ 8) for 30/330 degrees, (0 _._ 9 _,_ 1 _._ 1) for 90/270 degrees, and (1 _,_ 1) otherwise. It defaults to 1 without depth-layer objects. The fine routine receives its direction argument from the caller; the primary scoring caller converts numeric degree strings directly to degree values. 

### **C.4 Memory, Prompts, and Execution** 

The default configuration specifies a navigation map scale of 100 pixels per meter, high-level horizon 40, RGB-D resolution 640 _×_ 480, horizontal field of view 79<sup>_◦_</sup> , camera pitch _−_ 0 _._ 25 

11 

Table 6: Fine-feature weights used by the fine-scoring routine, in first-match order. These are implementation settings, not fitted performance results. 

|Condition|Room|Object|Spatial|Semantic|Depth|
|---|---|---|---|---|---|
|Any prior-associated object detected|0.25|0.50|0.20|0.03|0.02|
|Scene quality_Q >_0_._8|0.35|0.30|0.25|0.05|0.05|
|Room score_sr >_0_._7|0.45|0.25|0.20|0.05|0.05|
|Object score_so >_0_._7|0.30|0.40|0.20|0.05|0.05|
|Otherwise|0.35|0.30|0.20|0.10|0.05|


radians, body radius 0 _._ 18m, body height 0 _._ 88m, and success distance 1 _._ 0m. 

Goal priors are generated at runtime, cached within an episode, and cleared on reset. Provider-specific sampling settings are defined in `src/api.py` . Because independent episodes can use different priors and model outputs, the pipeline does not assume deterministic inference across runs. 

The prompt template above describes the goal-prior construction strategy. The executable builders specify the output schemas, examples, and error handling for prior generation, panorama scoring, relation refinement, arbitration, and local planning. 

### **C.5 Graph Representation and Memory Updates** 

Before scoring, the graph interface normalizes node and relation fields and merges retrieved memory with current observations. Flat and typed edge collections represent the same edited graph. Room aliases and goal-schema aliases are resolved consistently, while canonical endpoint names support matching across different instance identifiers. Missing observation, relation, or depth evidence contributes zero to its corresponding match term. 

Depth-ray positions are stored until the panoramic VLM response is available. Object descriptions are associated with the closest view-center ray and then added to persistent memory. The resulting positions are coarse view-level estimates. Planning uses the room descriptions and heading angles expressed in degrees. 

### **C.6 Ablation Settings and Evaluation Tools** 

Uniform fine weights assign 0.2 to each feature. Static weights normalize a configured vector; the default vector is 

(0 _._ 30 _,_ 0 _._ 40 _,_ 0 _._ 20 _,_ 0 _._ 05 _,_ 0 _._ 05) _,_ 

ordered by room, object, spatial, semantic, and depth features. These are separate modes. The non-adaptive result in Table 9 represents one configuration and does not distinguish these two modes. 

The no-arbitration control removes the LLM contribution without rescaling the other terms. A separate scalematched variant multiplies the remaining coefficients by ( _a_ + _b_ + _e_ ) _/_ ( _a_ + _b_ ). The prior-prompt-only setting bypasses 

Table 7: Component runtime and memory usage at different episode lengths. VLM timing is per call and does not include the full navigation pipeline. 

|Episode length|10|20|40|
|---|---|---|---|
|Memory (MB)|1.2|2.8|5.1|
|Graph update (ms)|12|18|25|
|VLM inference (ms)|2300|2300|2300|


graph scoring and graph context in planning; the graphmemory/direct-scoring setting retains graph context while using raw visual direction scores. These broader settings should be distinguished from an intervention that changes only the numerical matching term. 

Runs save manifests with source hashes, configuration, and seed; selected episode identities; client-call counts and times by role; graph diagnostics; and JSON episode outcomes. Client meters exclude provider-internal retries and token counts. The analysis script matches dataset, split, scene, episode, and seed, rejects omitted episodes, and resamples paired scene clusters. With fewer than two scenes it returns no interval. The experiments here use observed ranges and point differences; bootstrap intervals are not included. 

### **C.7 Runtime** 

These measurements do not establish end-to-end latency, asymptotic scaling, or total evaluation cost. 

## **D Additional Analyses** 

### **D.1 Roles of Coarse and Fine Stages** 

The stages are intended to rank directions and check compatibility with the prior. The current component comparison does not separately measure coarse-stage recall, fine-stage precision, pruning error rates, or loop frequency. It therefore cannot explain the results through a proven division of labor. In particular, prior consistency is not a ground-truth test: correct but unusual observations can be rejected, and plausible errors can remain. 

12 

Table 8: Memory configurations on HM3D v0.2 [18]. The final row changes both memory and scoring; it does not isolate their effects or measure ambiguity robustness. 

|**Configuration**|**SR(%)**_↑_|**SPL(%)**_↑_|
|---|---|---|
|Basic VLM / no memory|67.8|29.3|
|VLM / voxel memory|70.9|30.1|
|**HGWM / graph matching**|**74.4**|**31.9**|


Table 9: Additional HM3D v0.2 component results. 

|Configuration|SR (%)|SPL (%)|
|---|---|---|
|Full HGWM|74.4|31.9|
|Without goal prior|72.1|30.8|
|Without relation refinement|72.1|30.4|
|Without LLM arbitration|72.7|31.1|
|With non-adaptive fine weights|73.5|31.3|


### **D.2 Full Component Configuration** 

Table 8 restates the three memory configurations. Basic VLM uses no persistent memory; the voxel configuration retains direct VLM scoring; HGWM changes both memory and decision scoring. 

### **D.3 Additional Component Results** 

Table 9 compares the component ablations with full HGWM at 74.4% SR and 31.9% SPL. The non-adaptive weight setting is evaluated as a single control. The voxel-memory baseline uses direct VLM scoring and obtains 70.9% SR and 30.1% SPL. 

Removing the prior decreases SR/SPL by 2.3/1.1 points; removing relation refinement decreases them by 2.3/1.5 points. Removing arbitration and using non-adaptive weights yield decreases of 1.7/0.8 and 0.9/0.6 points, respectively. These comparisons favor the complete configuration, although the effects of individual removals need not be additive. 

Table 10: Memory, refinement, and matching comparisons. Gains and drops are percentage-point differences. The matching row summarizes an additional comparison and is not an absolute SR/SPL pair. 

|Quantity|Evidence|
|---|---|
|Full vs. voxel-memory SR/SPL gains|3.5/1.8 pp|
|Removal of refinement SR/SPL drops|2.3/1.5 pp|
|Scene–goal matching vs. prompting:|+1.5/+1.4 pp|
|SR/SPL gains||


Such a comparison would use identical episode sets, model versions, sampling settings, and cached goal priors. Memory construction, relation refinement, access to graph context, map updates, stopping rules, and the local action interface would remain unchanged. 

A common phase rule independent of fine scores, together with an identical arbitration prompt that omits those scores, would remove two indirect paths through which matching affects decisions. The two configurations would then differ in whether fusion uses the fine score or the equal-coefficient coarse substitution defined in the main paper. Clipping and the coarse-score override would remain unchanged. Because actions can diverge, subsequent observations need not be identical. This design defines a further experiment rather than a reinterpretation of the current full-model result. 

**Scope of the control settings.** The existing prior-promptonly switch also removes persistent graph context, refinement, and arbitration. The graph-memory/direct switch preserves graph context but removes refinement, fine scoring, and arbitration. Neither is the matched comparison just defined. The no-prior and no-refinement rows answer narrower intervention questions; they cannot substitute for a direct test of explicit matching. This stricter protocol is a proposed extension to the existing control settings. 

### **D.5 Three-Run Range on HM3D v0.1** 

### **D.4 Prior Information and Graph Matching** 

The goal prior has two roles: text conditioning for the coarse VLM and a relational reference for symbolic scoring. Prompting can reason about these relations implicitly, while the matching stage converts their compatibility with observations into an explicit directional score. The two channels therefore use the same prior information through different computations. 

**Comparison with prompting.** Matching the scene and goal graphs improves SR by 1.5 percentage points and SPL by 1.4 points over prior prompting. Table 10 summarizes this gain alongside the memory and refinement comparisons. The matching result is expressed as a difference rather than splitspecific absolute scores. A stricter controlled comparison would help separate the direct scoring effect from related changes in planning. 

We evaluate the main Gemini-1.5-Pro configuration three times on HM3D v0.1. Relative to the reference scores of 62.6 SR and 31.5 SPL, both metrics vary by _−_ 0 _._ 3 to +0 _._ 2 percentage points. The observed ranges are therefore 62.3–62.8 SR and 31.2–31.7 SPL. These marginal minima and maxima may occur in different runs and are not confidence intervals or standard deviations. The range applies only to this configuration. Its SPL lower bound equals the WMNav point estimate, motivating a cautious interpretation of the small SPL gain. 

### **D.6 Further Evaluation** 

Replaying recorded states with the same prior, graph, coarse scores, phase, and LLM output would help characterize the direct numerical matching channel. Replacing 10 _bf_<sup>_α_</sup> with _bc_<sup>_α_</sup> would reveal changes in ranking before and after clipping 

13 

and map updates. This diagnostic would complement navigation experiments, since fixed-state replay cannot estimate closed-loop SR or SPL. 

Further comparisons could examine graph and voxel memory under the same decision rule, coarse-only and fine-only scoring, and joint component removals. Matching episodes, prompts, seeds, and inference budgets would improve comparability. Annotations of relation updates, revisitation rates, and failure categories would also help explain when the method succeeds and where it fails. 

**Robustness beyond the current setting.** Controlled depth and localization perturbations, unusual room–object arrangements, and dynamic scenes are useful next steps beyond the present simulation experiments. Physical-robot evaluation would additionally test the effects of sensing, communication, and motion latency on the complete system. 

## **E Limitations and Future Work** 

#### **Current Limitations.** 

- _Simulation-only Evidence:_ No physical-robot results or controlled noise robustness tests are available. Backbone sensitivity is evaluated for only two VLM settings on one split. 

- _Component Attribution:_ The memory baselines change representation and scoring together. Additional component results are available, but their interactions and statistical uncertainty remain unestablished. 

- _Static Environments:_ Our current framework assumes static scenes. Dynamic objects (e.g., people, pets) or movable furniture could violate the structural priors encoded in _Ggoal_ . 

- _Foundation Model Dependency:_ Performance is constrained by the capabilities of the underlying VLMs/LLMs. Detection errors can propagate to graph construction; heuristic pruning can also remove correct atypical observations. 

- _Computational Cost:_ Despite caching optimizations, realtime deployment remains challenging due to VLM inference latency ( 2.3s per call). 

Future studies could evaluate temporal graph updates and search for multiple targets. Active perception and physical robot trials are also untested directions. 

## **F Implementation Availability** 

The implementation at `https://github.com/itak04/HG WM` includes configuration files, prompt builders, ablation settings, and analysis scripts. Experiment records store source 

Table 11: Navigation case collection. Counts refer to recorded steps and available text logs. 

|Case|Logged target|Steps|Logs|
|---|---|---|---|
|115_853<br>|sofa|6|6|
|160_853|tv screen|7|7|
|199_890|plant|29|29|
|220_890|plant|40|40|
|249_890|tv screen|40|40|
|265_890|toilet|19|19|
|289_890|chair|40|40|
|297_843|toilet|8|8|
|2_877|bed|4|4|
|310_843|sofa|2|2|
|32_877|chair|6|6|
|352_843|toilet|15|15|
|382_843|bed|24|24|
|399_824|bed|14|14|
|450_824|bed|40|40|
|546_880|chair|4|4|
|594_829|chair|10|9|
|63_877|sofa|30|30|


and configuration identifiers, episode identities, and modelcall statistics. The code and case collection provide the implementation details and qualitative context for the experiments. Access to benchmark datasets and model services follows the respective providers’ terms. 

**LLM roles and writing assistance.** Model roles and executable prompts are documented in the code. AI-assisted tools were used for language editing and formatting. The authors take responsibility for the methodology, results, and conclusions. 

**Code availability.** The code directory contains a README, implementation notes, source index, and configuration files. The project page links the manuscript, source, and case gallery. 

## **G Archived Navigation Cases** 

The supplementary archive covers 18 navigation cases. It indexes 338 step directories and retains 337 available text logs. Table 11 lists the coverage, including one missing text record. Open the case gallery linked from `https://itak04.githu b.io/HGWM/` to browse each case and its prompts, responses, selected views, curiosity maps, and navigation maps. 

**Selection and fidelity.** The original collection is about 913 MB. To fit the supplementary limit, the first, middle, and last available step of each folder are selected by one deterministic rule, without consulting outcomes. The selected PNG files are copied byte-for-byte. All available step text is preserved, with a manifest recording source checksums and inclusion 

14 


Figure 5: Unedited archived views. Top: case 115_853 at steps 0, 3, and 5. Bottom: case 220_890 at steps 0, 20, and 39. Text and action annotations are part of the original images. The examples illustrate how observations evolve during a short and a longer search. 

decisions. Additional frames and GIFs are omitted; pickle files are not deserialized or required by the gallery. The original source directory is unchanged. 

**What these records establish.** The logs expose what the model was prompted with and what it returned. For example, case 115_853 begins with an open-door subtask and ends with a logged sofa locator response; the final image visibly contains a sofa. Such observations help inspect a decision sequence, but a model goal flag or termination overlay is not a verified simulator success value. Some logged prior summaries contain zero node/edge counts; these summaries are retained as written and are not assumed to fully describe a hidden runtime graph. 

The cases provide qualitative examples rather than a benchmark sample for estimating SR, SPL, or failure frequencies. We retain error-marked steps and identify missing text records in the index to make the selection process transparent. 

15 

## **References** 

- [1] Peter Anderson, Angel X. Chang, Devendra Singh Chaplot, Alexey Dosovitskiy, Saurabh Gupta, Vladlen Koltun, Jana Kosecka, Jitendra Malik, Roozbeh Mottaghi, Manolis Savva, and Amir R. Zamir. On evaluation of embodied navigation agents. _arXiv preprint arXiv:1807.06757_ , 2018. doi: 10.48550/arXiv.1807.06757. 

- [2] Amir Bar, Gaoyue Zhou, Danny Tran, Trevor Darrell, and Yann LeCun. Navigation world models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 15791–15801. IEEE, 2025. doi: 10.1109/CVPR52734.2025.01472. URL `https://openaccess.thecvf.com/content/CVPR 2025/html/Bar_Navigation_World_Models_CVPR _2025_paper.html` . 

- [3] Dhruv Batra, Aaron Gokaslan, Aniruddha Kembhavi, Oleksandr Maksymets, Roozbeh Mottaghi, Manolis Savva, Alexander Toshev, and Erik Wijmans. Objectnav revisited: On evaluation of embodied agents navigating to objects. _arXiv preprint arXiv:2006.13171_ , 2020. doi: 10.48550/arXiv.2006.13171. 

- [4] Wenzhe Cai, Siyuan Huang, Guangran Cheng, Yuxing Long, Peng Gao, Changyin Sun, and Hao Dong. Bridging zero-shot object navigation and foundation models through pixel-guided navigation skill. In _Proceedings of the IEEE International Conference on Robotics and Automation_ , pages 5228–5234. IEEE, 2024. doi: 10.1109/ICRA57147.2024.10610499. 

- [5] Angel X. Chang, Angela Dai, Thomas Funkhouser, Maciej Halber, Matthias Niessner, Manolis Savva, Shuran Song, Andy Zeng, and Yinda Zhang. Matterport3D: Learning from RGB-D data in indoor environments. In _Proceedings of the International Conference on 3D Vision_ , pages 667–676. IEEE, 2017. doi: 10.1109/3DV.2017.00081. 

- [6] Junting Chen, Guohao Li, Suryansh Kumar, Bernard Ghanem, and Fisher Yu. How to not train your dragon: Training-free embodied object goal navigation with semantic frontiers. In _Robotics: Science and Systems XIX_ . Robotics: Science and Systems Foundation, 2023. doi: 10.15607/RSS.2023.XIX.075. URL `https: //roboticsproceedings.org/rss19/p075.html` . 

- [7] Andy Clark. Whatever next? predictive brains, situated agents, and the future of cognitive science. _Behavioral and brain sciences_ , 36(3):181–204, 2013. doi: 10.1017/ S0140525X12000477. 

- [8] Karl Friston. The free-energy principle: a unified brain theory? _Nature reviews neuroscience_ , 11(2):127–138, 2010. doi: 10.1038/nrn2787. 

- [9] Samir Yitzhak Gadre, Mitchell Wortsman, Gabriel Ilharco, Ludwig Schmidt, and Shuran Song. CoWs on 

pasture: Baselines and benchmarks for language-driven zero-shot object navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 23171–23181. IEEE, 2023. doi: 10.1109/CVPR52729.2023.02219. URL `https: //openaccess.thecvf.com/content/CVPR2023 /html/Gadre_CoWs_on_Pasture_Baselines_and_ Benchmarks_for_Language-Driven_Zero-Shot_ Object_CVPR_2023_paper.html` . 

- [10] Qiao Gu, Alihusein Kuwajerwala, Sacha Morin, Krishna Murthy Jatavallabhula, Bipasha Sen, Aditya Agarwal, Corban Rivera, William Paul, Kirsty Ellis, Rama Chellappa, Chuang Gan, Celso Miguel de Melo, Joshua B. Tenenbaum, Antonio Torralba, Florian Shkurti, and Liam Paull. ConceptGraphs: Open-vocabulary 3D scene graphs for perception and planning. In _Proceedings of the IEEE International Conference on Robotics and Automation_ , pages 5021–5028. IEEE, 2024. doi: 10.1109/ICRA57147.2024.10610243. 

- [11] David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018. doi: 10.48550/arXiv .1803.10122. 

- [12] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse control tasks through world models. _Nature_ , 640:647–653, 2025. doi: 10.1038/s41586-025-08744-2. 

- [13] I-Tak Ieong and Hao Tang. Multimodal perception for goal-oriented navigation: A survey. _arXiv preprint arXiv:2504.15643_ , 2025. doi: 10.48550/arXiv.2504.15 643. 

- [14] Jing Yu Koh, Honglak Lee, Yinfei Yang, Jason Baldridge, and Peter Anderson. Pathdreamer: A world model for indoor navigation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 14718–14728. IEEE, 2021. doi: 10.1109/ICCV48922. 2021.01447. URL `https://openaccess.thecvf.co m/content/ICCV2021/html/Koh_Pathdreamer_A_ World_Model_for_Indoor_Navigation_ICCV_202 1_paper.html` . 

- [15] Yuxuan Kuang, Hai Lin, and Meng Jiang. OpenFMNav: Towards open-set zero-shot object navigation via visionlanguage foundation models. In _Findings of the Association for Computational Linguistics: NAACL 2024_ , pages 338–351, Mexico City, Mexico, 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.findi ngs-naacl.24. URL `https://aclanthology.org/2 024.findings-naacl.24/` . 

- [16] Arjun Majumdar, Gunjan Aggarwal, Bhavika Devnani, Judy Hoffman, and Dhruv Batra. ZSON: Zero-shot object-goal navigation using multimodal goal embeddings. In _Advances in Neural Information Processing Systems_ , volume 35, pages 32340–32352, 2022. doi: 10.52202/068431-2343. URL `https://proceedings.` 

16 

`neurips.cc/paper_files/paper/2022/hash/d0b 8f0c8f79d3a621af945cafb669f4b-Abstract-Con ference.html` . 

- [17] Dujun Nie, Xianda Guo, Yiqun Duan, Ruijun Zhang, and Long Chen. WMNav: Integrating vision-language models into world models for object goal navigation. In _Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 2392–2399. IEEE, 2025. doi: 10.1109/IROS60139.2025.11246684. 

- [18] Santhosh K. Ramakrishnan, Aaron Gokaslan, Erik Wijmans, Oleksandr Maksymets, Alexander Clegg, John Turner, Eric Undersander, Wojciech Galuba, Andrew Westbury, Angel X. Chang, Manolis Savva, Yili Zhao, and Dhruv Batra. Habitat-matterport 3D dataset (HM3D): 1000 large-scale 3D environments for embodied AI. In _Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks_ , volume 1, 2021. URL `https://datasets-benchmark s-proceedings.neurips.cc/paper_files/pape r/2021/hash/34173cb38f07f89ddbebc2ac912830 3f-Abstract-round2.html` . 

- [19] Ram Ramrakhya, Eric Undersander, Dhruv Batra, and Abhishek Das. Habitat-Web: Learning embodied objectsearch strategies from human demonstrations at scale. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 5163–5173. IEEE, 2022. doi: 10.1109/CVPR52688.2022.00511. URL `https://openaccess.thecvf.com/content/CVPR 2022/html/Ramrakhya_Habitat-Web_Learning_ Embodied_Object-Search_Strategies_From_Hu man_Demonstrations_at_Scale_CVPR_2022_pape r.html` . 

- [20] Jingwen Sun, Jing Wu, Ze Ji, and Yu-Kun Lai. A survey of object goal navigation. _IEEE Transactions on Automation Science and Engineering_ , 22:2292–2308, 2025. doi: 10.1109/TASE.2024.3378010. 

- [21] Xinyu Sun, Lizhao Liu, Hongyan Zhi, Ronghe Qiu, and Junwei Liang. Prioritized semantic learning for zero-shot instance navigation. In _Computer Vision – ECCV 2024_ , volume 15070 of _Lecture Notes in Computer Science_ , pages 161–178. Springer Nature Switzerland, 2025. doi: 10.1007/978-3-031-73254-6_10. URL `https://doi. org/10.1007/978-3-031-73254-6_10` . 

- [22] Pengying Wu, Yao Mu, Bingxian Wu, Yi Hou, Ji Ma, Shanghang Zhang, and Chang Liu. VoroNav: Voronoibased zero-shot object navigation with large language model. In _Proceedings of the 41st International Conference on Machine Learning_ , volume 235 of _Proceedings of Machine Learning Research_ , pages 53757–53775. PMLR, 2024. URL `https://proceedings.mlr.pr ess/v235/wu24u.html` . 

- [23] Karmesh Yadav, Ram Ramrakhya, Arjun Majumdar, Vincent-Pierre Berges, Sachit Kuhar, Dhruv Batra, 

   - Alexei Baevski, and Oleksandr Maksymets. Offline visual representation learning for embodied navigation. _arXiv preprint arXiv:2204.13226_ , 2022. doi: 10.48550/arXiv.2204.13226. 

- [24] Karmesh Yadav, Arjun Majumdar, Ram Ramrakhya, Naoki Yokoyama, Alexei Baevski, Zsolt Kira, Oleksandr Maksymets, and Dhruv Batra. OVRL-V2: A simple state-of-art baseline for ImageNav and ObjectNav. _arXiv preprint arXiv:2303.07798_ , 2023. doi: 10.48550/arXiv.2303.07798. 

- [25] Hang Yin, Xiuwei Xu, Zhenyu Wu, Jie Zhou, and Jiwen Lu. SG-Nav: Online 3D scene graph prompting for LLM-based zero-shot object navigation. In _Advances in Neural Information Processing Systems_ , volume 37, pages 5285–5307, 2024. URL `https://proceeding s.neurips.cc/paper_files/paper/2024/hash/0 98491b37deebbe6c007e69815729e09-Abstract-C onference.html` . 

- [26] Hang Yin, Xiuwei Xu, Linqing Zhao, Ziwei Wang, Jie Zhou, and Jiwen Lu. UniGoal: Towards universal zeroshot goal-oriented navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 19057–19066. IEEE, 2025. doi: 10.1 109/CVPR52734.2025.01775. URL `https://openac cess.thecvf.com/content/CVPR2025/html/Yin_ UniGoal_Towards_Universal_Zero-shot_Goal-o riented_Navigation_CVPR_2025_paper.html` . 

- [27] Zecheng Yin, Hao Zhao, and Zhen Li. Hypernav: Hybrid perception for object-oriented navigation in unknown environment. _arXiv preprint arXiv:2510.22917_ , 2025. doi: 10.48550/arXiv.2510.22917. 

- [28] Naoki Yokoyama, Sehoon Ha, Dhruv Batra, Jiuguang Wang, and Bernadette Bucher. VLFM: Vision-language frontier maps for zero-shot semantic navigation. In _Proceedings of the IEEE International Conference on Robotics and Automation_ , pages 42–48. IEEE, 2024. doi: 10.1109/ICRA57147.2024.10610712. 

- [29] Bangguo Yu, Hamidreza Kasaei, and Ming Cao. L3MVN: Leveraging large language models for visual target navigation. In _Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 3554–3560. IEEE, IEEE, 2023. doi: 10.1109/IR OS55552.2023.10342512. 

- [30] Jiazhao Zhang, Liu Dai, Fanpeng Meng, Qingnan Fan, Xuelin Chen, Kai Xu, and He Wang. 3D-aware object goal navigation via simultaneous exploration and identification. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 6672– 6682. IEEE, 2023. doi: 10.1109/CVPR52729.2023.006 45. URL `https://openaccess.thecvf.com/cont ent/CVPR2023/html/Zhang_3D-Aware_Object_Go al_Navigation_via_Simultaneous_Exploration _and_Identification_CVPR_2023_paper.html` . 

17 

- [31] Mingjie Zhang, Yuheng Du, Chengkai Wu, Jinni Zhou, Zhenchao Qi, Jun Ma, and Boyu Zhou. Apexnav: An adaptive exploration strategy for zero-shot object navigation with target-centric semantic fusion. _IEEE Robotics and Automation Letters_ , 10(11):11530–11537, 2025. doi: 10.1109/LRA.2025.3606388. URL `https://doi.org/10.1109/LRA.2025.3606388` . 

- [32] Sixian Zhang, Xinhang Song, Yubing Bai, Weijie Li, Yakui Chu, and Shuqiang Jiang. Hierarchical objectto-zone graph for object navigation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 15110–15120. IEEE, 2021. doi: 10.1109/ ICCV48922.2021.01485. URL `https://openaccess .thecvf.com/content/ICCV2021/html/Zhang_Hi erarchical_Object-to-Zone_Graph_for_Object _Navigation_ICCV_2021_paper.html` . 

- [33] Sixian Zhang, Xinyao Yu, Xinhang Song, Xiaohan Wang, and Shuqiang Jiang. Imagine before go: Self-supervised generative map for object goal navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 16414–16425. IEEE, 2024. URL `https://openaccess.thecvf.com/co ntent/CVPR2024/html/Zhang_Imagine_Before_G o_Self-Supervised_Generative_Map_for_Objec t_Goal_Navigation_CVPR_2024_paper.html` . 

- [34] Linqing Zhong, Chen Gao, Zihan Ding, Yue Liao, Huimin Ma, Shifeng Zhang, Xu Zhou, and Si Liu. TopVNav: Unlocking the top-view spatial reasoning potential of MLLM for zero-shot object navigation. _arXiv preprint arXiv:2411.16425_ , 2024. doi: 10.48550/arXiv.2411.16 425. 

- [35] Kaiwen Zhou, Kaizhi Zheng, Connor Pryor, Yilin Shen, Hongxia Jin, Lise Getoor, and Xin Eric Wang. ESC: Exploration with soft commonsense constraints for zeroshot object navigation. In _Proceedings of the 40th International Conference on Machine Learning_ , volume 202 of _Proceedings of Machine Learning Research_ , pages 42829–42842. PMLR, PMLR, 2023. URL `https: //proceedings.mlr.press/v202/zhou23r.html` . 

- [36] Zibo Zhou, Yue Hu, Lingkai Zhang, Zonglin Li, and Siheng Chen. Beliefmapnav: 3d voxel-based belief map for zero-shot object navigation. _arXiv preprint arXiv:2506.06487_ , 2025. doi: 10.48550/arXiv.250 6.06487. 

- [37] Fengda Zhu, Xiwen Liang, Yi Zhu, Qizhi Yu, Xiaojun Chang, and Xiaodan Liang. SOON: Scenario oriented object navigation with graph-based exploration. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 12684–12694. IEEE, 2021. doi: 10.1109/CVPR46437.2021.01250. URL `https://openaccess.thecvf.com/content/CVPR 2021/html/Zhu_SOON_Scenario_Oriented_Objec t_Navigation_With_Graph-Based_Exploration _CVPR_2021_paper.html` . 

18 

