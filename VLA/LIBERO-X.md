---
title: "LIBERO-X: Robustness Litmus for Vision-Language-Action Models"
date: "2026-02-06"
authors: "Guodong Wang; Chenkai Zhang; Qingjie Liu; Jinjin Zhang; Jiancheng Cai; Junjie Liu"
venue: "RSS 2026"
url: https://arxiv.org/abs/2602.06556
pdf: https://arxiv.org/pdf/2602.06556
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.06556)** / [論文ページ](https://arxiv.org/abs/2602.06556)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# LIBERO-X: Robustness Litmus for Vision-Language-Action Models 

Guodong Wang<sup>_∗_1</sup> , Chenkai Zhang<sup>_∗_2</sup> , Qingjie Liu<sup>2</sup> , Jinjin Zhang<sup>2</sup> , Jiancheng Cai<sup>1</sup> , Junjie Liu<sup>_†_1</sup> , Xinmin Liu<sup>_‡_1</sup> 1Meituan, 2Beihang University 

_∗_ Equal Contribution _†_ Corresponding author _‡_ Project Leader Project page: https://zackhxn.github.io/LIBERO-X/ 

**_Abstract_ —Reliable benchmarking is critical for advancing Vision–Language–Action (VLA) models, as it reveals their generalization, robustness, and alignment of perception with languagedriven manipulation tasks. However, existing benchmarks often provide limited or misleading assessments due to insufficient evaluation protocols that inadequately capture real-world distribution shifts. This work systematically rethinks VLA benchmarking from both evaluation and data perspectives, introducing LIBERO-X, a benchmark featuring: 1) A hierarchical evaluation protocol with progressive difficulty levels targeting three core capabilities: spatial generalization, object recognition, and task instruction understanding. This design enables fine-grained analysis of performance degradation under increasing environmental and task complexity; 2) A high-diversity training dataset collected via human teleoperation, where each scene supports multiple finegrained manipulation objectives to bridge the train-evaluation distribution gap. Experiments with representative VLA models reveal significant performance drops under cumulative perturbations, exposing persistent limitations in scene comprehension and instruction grounding. By integrating hierarchical evaluation with diverse training data, LIBERO-X offers a more reliable foundation for assessing and advancing VLA development.** 

## I. INTRODUCTION 

Vision–Language–Action (VLA) models [48, 17, 3, 38, 2, 35, 18, 21, 32] have recently made significant strides in robotic manipulation, emerging as a key paradigm for integrating perception, language understanding, and control. By processing visual observations and natural language instructions in an end-to-end manner, these models directly map multimodal inputs to low-level control signals and have achieved strong performance across a wide range of complex manipulation tasks. With rapid advances in VLA architectures and training algorithms, a central challenge for the field is now the systematic evaluation of their actual capabilities [37, 41, 23]. 

In response, the research community has introduced a series of standardized benchmarks, such as LIBERO [24] and SimpleEnv [23], which provide controlled, reproducible environments covering diverse task configurations, and are widely used to assess multimodal understanding, long-horizon reasoning, and knowledge transfer. Despite impressive results on these existing benchmarks, current VLA evaluations are often confounded by limitations in both **evaluation protocols** and **data distribution** , leading to overly optimistic or even misleading conclusions about model capability. 

First, existing benchmarks typically focus on individual perturbation types, primarily spatial ones. Extensions such as 

SafeLIBERO [13], LIBERO-PRO [47], and LIBERO-Plus [7] increase the diversity of test conditions by introducing additional perturbation factors (e.g., random obstacles for safety studies, or initial states, task instructions, and environment configurations). However, as shown in Figure 1 **(b)** , they still suffer from two major issues: (i) perturbations along different dimensions are mostly modeled independently, failing to capture the multi-source distribution shifts that arise in realistic deployment; and (ii) there is no systematic progression of difficulty from easy to hard, making it difficult to characterize performance degradation as environmental and task complexity increase. Consequently, these limitations hinder a comprehensive assessment of model robustness under realistic, compounded distribution shifts. 

Second, evaluation is frequently unfaithful due to shortcomings in both the training and testing datasets. Specifically, training data lack sufficient diversity, and there is limited divergence between training and testing scenarios and tasks. Benchmarks such as LIBERO typically adopt test configurations that closely resemble the training settings, introducing only minor perturbations, such as small changes in initial object positions, as shown in Figure 1 **(a)** . Under this narrow train–test gap, models often attain near-saturated success rates, illustrating that superficially varied test scenarios do not necessarily reveal the model’s true generalization ability. On the training data side, existing datasets exhibit limited diversity in tasks, scenes, and trajectories, which fundamentally constrains the attainable capability of learned models. A single scene is usually associated with only one or a few tasks, and demonstrations for the same task follow highly homogeneous action sequences and intermediate states, effectively collapsing into a small set of template-like strategies. Overfitting is further exacerbated under such narrow data distributions, causing models to memorize a limited number of stereotyped behaviors and to mechanically replay training actions [7, 47]. 

In this work, we improve benchmarking by jointly addressing evaluation hierarchy and training data diversity, as shown in Figure 1 **(c)** . Regarding the evaluation, we focus on three core capabilities of VLA models for robotic manipulation: spatial generalization, object recognition, and instruction understanding. Centered on these capabilities, we introduce LIBERO-X, an evolved version of the original LIBERO benchmark, where “X” denotes _eXtreme_ to reflect its goal of pushing evaluation limits. LIBERO-X first defines 


Fig. 1: **Comparison with related simulation benchmarks. (a)** : LIBERO lacks diversity by coupling scenes with homogeneous trajectories, inducing action overfitting, while its test set closely mirrors training data. **(b)** : Recent extensions reuse original training trajectories, introducing perturbations but model them independently, failing to capture complex distribution shifts. **(c)** : LIBERO-X enhances training via multi-task scenes with diverse trajectories. Its multi-level evaluation protocol progressively escalates complexity, revealing significant performance degradation across VLA models as difficulty increases, thus enabling rigorous robustness assessment. 

a new evaluation protocol that delivers a progressively challenging, multi-level test suite for assessing the generalization of VLA models in complex environments. Specifically, we adopt a _reuse–adjust–reconstruct_ strategy over training scenes to construct a five-level hierarchy of fine-grained manipulation tasks. The first two levels introduce increasing magnitudes of spatial perturbations, progressing from minor positional jitter to broader spatial randomization. The third level alters scene topology (e.g., swapping target and placement locations), breaking fixed spatial associations learned during training. The fourth level incorporates unseen and confounding objects, and varies fine-grained attributes such as color and texture. The fifth level further incorporates semantic variations in task instructions to evaluate language–vision–action alignment. Higher levels are formed by adding new perturbation dimensions on top of lower levels, thereby progressively escalating difficulty to enable precise analysis of performance degradation as environmental and task complexity increase. Complementing this hierarchy, we implement a multi-label evaluation strategy where each task is annotated with finegrained attributes: interaction type, subtask count, spatial relation, and object attribute. This granular labeling facilitates in-depth diagnostics, allowing researchers to pinpoint specific failure modes across distinct manipulation dimensions. 

To mitigate the overfitting risks associated with the relatively homogeneous scenes and trajectories in the original LIBERO training set, we further construct a high-diversity training dataset via human teleoperation. This dataset fun- 

damentally increases scene and task diversity by incorporating variations in object attributes (e.g., size, color, texture) and spatial relations (e.g., left/right, near/far, front/behind), together with language instructions. Importantly, a single scene is associated with multiple manipulation tasks, avoiding template-like scene–task–trajectory mappings. This design provides a data foundation by exposing models to broader task–scene distributions during training. Consequently, performance on LIBERO-X more faithfully reflects models’ transferability and robustness in complex, dynamic environments. 

Overall, by combining richer training diversity and multidimensional hierarchical perturbations at test time, LIBEROX represents a systematic rethinking of VLA model evaluation for robotic manipulation. We expect it to serve as a comprehensive benchmark that more effectively guides VLA development toward reliable deployment in robotics. 

The main contributions of this work are three-fold. 

- We propose LIBERO-X, a comprehensive benchmark for manipulation that introduces a progressively challenging evaluation framework with multi-label annotations and jointly perturbs spatial layouts, object properties, and instruction semantics to systematically characterize model performance under multi-dimensional distribution shifts. 

- We construct a high-diversity training dataset comprising 2,520 demonstrations, 600 tasks, and 100 scenes collected via human teleoperation, substantially increasing scene diversity and task granularity. 

- Extensive experiments on fine-tuned representative VLA 

models reveal notable performance degradation as task and scene complexity increase, highlighting critical limitations in scene comprehension and instruction grounding and offering empirical insights for future model design. 

## II. RELATED WORK 

**Generalist Robot Policies.** Early imitation learning methods, such as ACT [42] and Diffusion Policy (DP) [5], addressed sequential decision-making via action chunking and conditional denoising, respectively. Building on these, Octo [9] and RDT-1B [26] scaled these architectures on large-scale robot dataset (e.g. the Open X-Embodiment dataset [29]), demonstrating that increasing model capacity significantly improves multi-task manipulation. 

Inspired by the generalization and reasoning capabilities of Large Language Models (LLMs), a new paradigm of VLA models has emerged. These methods aim to leverage the rich semantic representations of pretrained VLM backbones for robotic control, diverging primarily in their action modeling strategies. Discrete approaches like RT-2 [48] and OpenVLA [17] discretize continuous actions into text tokens, treating manipulation as a next token prediction task. Recent work like FAST [16] further optimizes this tokenization for higher efficiency. Conversely, continuous approaches retain the precision of the action space but vary in their formulation. Some methods, such as RoboFlamingo [22] and OpenVLAOFT [18], adopt direct regression heads optimized via mean squared error (MSE) loss. Others integrate more expressive generative policies: CogACT [19] separates high-level understanding from low-level execution by attaching a diffusion head to the VLM, while _π_ 0 [14], _π_ 0 _._ 5 [14] and GR00T [2] achieve state-of-the-art performance by incorporating flow matching directly with VLM backbones. To enhance the grounding of VLA models, recent approaches also focus on explicitly or implicitly incorporating additional information, such as spatial structure and geometry [34, 43] and reasoning and planning signals [39, 14]. 

Despite these advancements, evaluating VLA models remains challenging due to the high cost and variability of realrobot experiments. To address this, we develop a comprehensive simulation benchmark to enable the systematic and reproducible assessment of VLA methods. 

**Robotic Manipulation Benchmarks.** Standardized benchmarks are crucial for evaluating the generalization and robustness of robotic manipulation policies. While numerous benchmarks have been developed for real-world systems, this review focuses primarily on simulation-based benchmarks due to their experimental convenience and reproducibility. Early efforts such as RLBench [15] and LIBERO [24] have significantly advanced the field by establishing unified evaluation protocols. Recent benchmarks [7, 33, 47, 46, 20] have explored specific facets of generalization. For example, AGNOSTOS [46] and CALVIN [27] investigate transfer across tasks, while RoboCerebra [11] and VLABench [41] focus on long-horizon manipulation and complex scene-task understanding. Meanwhile, works such as LIBERO-PRO [47] and LIBERO-Plus [7] 

expand the evaluation by introducing controlled perturbations across dimensions like target placement, object attributes, and robot pose. These studies consistently find that high nominal success rates often decline sharply under minor perturbations, suggesting a reliance on memorization of training data rather than generalized skill acquisition. 

However, such evaluations usually test isolated distribution shifts, like visual appearance or object position, rather than the coupled, multi-factor shifts encountered in real environments. Other works organize test tasks into progressively harder levels to probe model limits. For example, GemBench [8] uses a multi-level protocol from novel placements to long-horizon tasks, observing performance degradation across levels. Yet its limited training scale and task coverage restrict its use for large-scale VLA assessment. Additionally, LIBERO-Plus [7] stratifies difficulty via multi-model averaging, which can introduce bias and lacks interpretability. 

Another limitation of many benchmarks [15, 24] is that training diversity is often secondary to test design, with assessments frequently conducted using off-the-shelf checkpoints [7, 47]. However, the fine-tuning datasets for these VLA models generally lack sufficient variation in scenes, tasks, and trajectories, thereby fundamentally constraining the generalization capacity of the resulting policies [41]. While LIBEROPlus [7] attempts to increase variation by re-rendering scenes using state-action pairs from the original LIBERO [24], it still inherits the limited diversity of trajectories. 

In contrast, our benchmark integrates a highly diverse, teleoperation-collected training set with a multi-level evaluation protocol that systematically increases difficulty through spatial perturbations, object substitutions, and instruction rewrites. This approach enables a more faithful and systematic assessment of VLA models under complex, multi-dimensional distribution shifts, closely reflecting real-world conditions. 

## III. LIBERO-X BENCHMARK 

We introduce LIBERO-X, a comprehensive benchmark designed to advance the evaluation and development of VLA models for robotic manipulation. LIBERO-X provides a highly diverse training dataset and a multi-dimensional evaluation framework tailored to real-world complexity. Specifically, we first describe the training dataset collected via human teleoperation, which covers extensive task and scene variations. We then present the multi-level evaluation framework with fine-grained multi-label metrics, progressively incorporating spatial, object, and semantic perturbations. These dimensions capture the core factors governing perception, reasoning, and action coupling in VLA-based robotic manipulation, enabling a systematic assessment of model generalization and robustness across diverse environmental and task conditions. Following LIBERO [24], we employ the Planning Domain Definition Language (PDDL) [1] to describe scenes and tasks. 

## _A. Training Dataset_ 

To mitigate the overfitting risk arising from the limited scene diversity in the original LIBERO, where each scene is typically 


Fig. 2: **Overview of LIBERO-X.** LIBERO-X provides a high-diversity training dataset constructed through human teleoperation, along with multi-level and multi-label evaluation data. 


Fig. 3: **Distribution visualization of training trajectories.** 

associated with a single task and the collected trajectories exhibit high similarity, LIBERO-X constructs a training dataset that better reflects real-world variability. Specifically, the dataset consists of 2,520 demonstration trajectories spanning 600 tasks and 100 scenes, as shown on the left side of Figure 2. Unlike the original LIBERO [24], which emphasizes manipulating targets by category thus encourages learning category-specific action patterns, LIBERO-X introduces finergrained task-level extensions to expose models to diverse task formulations and workspace configurations: 

- **Multi-Task Scene Design** : In contrast to LIBERO [24], 

which is predominantly composed of single-task scenes, resulting in an average of 2.6 tasks per scene, our dataset significantly increases task density to an average of 6 tasks per scene. This design entails multi-object interactions and versatile manipulation skills, requiring models to adapt their manipulation strategies under identical visual and physical conditions. 

- **Attribute-Conditioned Manipulation** : Actions are explicitly conditioned on fine-grained object properties (e.g., size, color, texture) rather than broad categories. To rigorously test perceptual grounding, scenes include distractor objects with similar attributes, requiring the model to distinguish the target amidst visual ambiguity. 

- **Spatial Relationship Reasoning** : Tasks extend beyond target localization to require understanding and reasoning about spatial relationships among objects, including left/right, front/back, and near/far. 

With this training setup, the model is encouraged to learn the composable semantic correspondence between target objects and their language descriptions, rather than relying on template instructions or fixed scene structures to make “memorized” decisions. By increasing the diversity of tasks and scenes at the data source, LIBERO-X raises the upper bound of model performance, allowing models to truly acquire generalizable manipulation strategies. As a result, performance variations observed across subsequent LIBERO-X test levels 


Fig. 4: **Practical examples from the LIBERO-X training dataset.** 

more faithfully reflect the model’s real-world transferability and robustness in dynamic environments. 

_1) Training Trajectory Collection:_ The trajectories were collected via VR teleoperation using a Meta Quest 3 in MuJoCo [36], facilitated by LeRobot [4]. During data collection, strict protocols were followed: state-action sequences were recorded at 20 Hz, where the state included the 6D Cartesian pose of the end effector and the gripper open/close status, and actions consisted of Cartesian increments and gripper commands. Multi-view images (third-person and hand-eye), were rendered by rolling out these recorded actions. To ensure quality, trajectories with noticeable pauses or non-optimal paths were discarded, retaining only smooth and successful demonstrations. As shown in Figure 3, heatmaps visualize the trajectory distributions, where brighter regions correspond to areas with higher trajectory density. Comparing with LIBERO, LIBERO-X exhibits a broader spread and higher trajectory density, demonstrating its greater diversity. 

_2) Example Training Demonstrations:_ The training dataset is built upon **Kitchen** and **Study** base scenes. By integrating diverse object categories, we created 100 scenarios encompassing 600 distinct tasks. These tasks cover object types, ranging from rigid to articulated objects, and include multi-object and attribute-conditioned interactions. Representative examples are illustrated in Figure 4. 

## _B. Evaluation Framework_ 

The LIBERO-X test set employs a multi-level evaluation framework combined with a fine-grained multi-label system, forming a two-dimensional assessment design (Figure 2). Along the vertical axis, the multi-level framework evaluates models on tasks of progressively increasing difficulty, creating a curriculum-style, incremental assessment. Along the horizontal axis, the multi-label system assigns detailed labels 

to tasks, enabling fine-grained quantitative analysis. Together, these two components allow systematic measurement of performance under various perturbations and across diverse tasks and environments. Table I compares LIBERO-X with other simulation benchmarks, highlighting its multi-level framework and fine-grained labeling scheme. 

_1) Multi-level Evaluation:_ The vertical axis of the framework implements a multi-level evaluation following a progressive scene design that incrementally increases task and environmental complexity across spatial reasoning, object recognition, and instruction understanding. Each level builds upon the preceding one by superimposing additional perturbations, ensuring a cumulative assessment of the model’s robustness: 

**Level 1 - Local Spatial Perturbation:** Test scenes closely resemble the training distribution, with minor variations in object positions, designed to measure model stability under small-scale spatial changes. 

**Level 2 - Extended Spatial Perturbation:** Building upon Level 1, spatial variations are amplified by dynamically adjusting the sampling radius according to object proximity, with a safety margin to expand layout space. This level assesses the model’s ability to cope with large-scale positional changes. 

**Level 3 - Scene Topology Reconstruction:** The relative positions of objects are altered, including swapping targets with distractors and adding irrelevant objects, to increase environmental complexity. This stage evaluates task execution under restructured object relationships and modified scene configurations. 

**Level 4 - Visual Attribute Variation:** Objects vary in texture, color, and size; target objects may belong to unseen categories, and visually similar confounders are introduced. This level tests the model’s discriminative ability, robustness to attribute changes, and generalization to unseen objects. 

**Level 5 - Semantic-Equivalent Reformulation:** Instruc- 

TABLE I: **Comparison with other simulation benchmarks. Name:** Name of each benchmark. **Simulator:** ManiSkill2 [10], MuJoCo [36], RLBench [15] and NVIDIA Isaac Sim [28]. **Date:** Release date. **Training Data:** Availability of training set. If provided, indicates automation, indicates manual annotation. **Testing Data:** Availability of independent testing set. ✓ represents full compliance, ✗ represents non-compliance, and indicates partial compliance. **Multi-level Evaluation:** Adoption of multi-level framework. L1: Local Spatial Perturbation, L2: Extended Spatial Perturbation, L3: Scene Topology Reconstruction, L4: Visual Attribute Variation, and L5: Semantic-Equivalent Reformulation. **Multi-label Evaluation:** Task label across multiple dimensions. **IT:** Interaction Type. **SC:** Subtask Count. **SR:** Spatial Relation. **OA:** Object Attribute. 

|**Name**|**Simulator**|**Date**|**Training Data**|**Testing Data**||**Multi-l**|**evel Eva**|**luation**||**M**|**ulti-labe**|**l Evalua**|**tion**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||**L1**|**L2**|**L3**|**L4**|**L5**|**IT**|**SC**|**SR**|**OA**|
|RoboMIND [40]|Isaac Sim|2024.12||✓|✗|✗|✗||✗|✗|✗|✗|✗|
|COLOSSEUM [33]|RLBench|2024.05|✗|✓|✗|✗|||✗|✗|✗|✗|✓|
|AGNOSTOS [46]|RLBench|2025.10|✗|✓|✗|✗|✗|✗|✗|✗||✗|✗|
|GemBench [8]|RLBench|2025.03||✓||✗|✗||✗|✗||✗||
|VLATest [37]|Maniskill2|2025.05|✗|✓|✓|✗|||||||✗|
|INT-ACT [6]|Maniskill2|2025.06|✗|✓||✗|✗|✓||✗|✗|✗|✗|
|RL4VLA [25]|Maniskill2|2026.01||✓|✓|✓|✓|✗||||||
|LIBERO [24]|MuJoCo|2023.06||✓|✓|✗|✗|✗|✗|✗|✗|✗|✗|
|LIBERO-OOD [20]|MuJoCo|2025.05|✗|✓|✗|✗|||✗|✗|✗|✗|✗|
|RoboCerebra [11]|MuJoCo|2025.06||✓|✗|||✗|✗|✗|✗|✗|✗|
|LIBERO-PRO [47]|MuJoCo|2025.10|✗|✓|✗|✗|||||✓|||
|LIBERO-Plus [7]|MuJoCo|2025.10||✓|✗|✓|✗|✗||||✗|✗|
|SafeLIBERO [13]|MuJoCo|2025.12|✗|✓|✗||✗||✗|✗|✗|✗|✗|
|LIBERO-X (Ours)|MuJoCo|2026.01||✓|✓|✓|✓|✓|✓|✓|✓|✓|✓|


tions are rephrased while preserving task semantics, including synonym replacement (L5-1), word compression (L5-2), word order adjustment (L5-3), voice conversion (L5-4), and redundant descriptions (L5-5). This level measures the model’s ability to generalize across diverse linguistic formulations of the same task. 

_2) Multi-label Evaluation:_ The horizontal axis of the framework incorporates a fine-grained multi-label evaluation system. This system enables a detailed, multi-dimensional analysis of model performance, particularly regarding its ability to manage fine-grained aspects of task execution. The multi-label evaluation is organized hierarchically, with each top-level category further divided into sub-categories (detailed definitions are provided in the appendix). 

**Interaction Type:** This dimension categorizes object interactions into three types: (i) Pick-and-Place, where objects are grasped and moved to targets; (ii) Switch-based, such as opening/closing drawers or turning knobs, requiring precise gripper control; and (iii) Combined, integrating both types and requiring flexible transitions. It evaluates the model’s ability to execute diverse manipulation strategies. 

**Subtask Count:** This dimension captures the number of subtasks required to complete a task, ranging from singlestep to three-step sequences. It assesses the model’s planning, sequential reasoning, and ability to maintain task coherence over long-horizon tasks. 

**Spatial Relation:** This dimension characterizes the relative positions and spatial arrangements of objects within a task. It evaluates the model’s spatial reasoning and environmental perception by measuring how effectively it interprets spatial relationships and their impact on task execution. 

**Object Attribute:** This dimension describes the visual object properties, including color, size, texture, and other fine- 

grained features. It evaluates the model’s ability to recognize and leverage object attributes to accomplish tasks, emphasizing the role of precise visual perception in task success. 

## IV. EXPERIMENTS 

## _A. Experimental setup_ 

We selected five representative models for evaluation: OpenVLA-OFT [18], X-VLA [44], GR00T-N1.5 [2], _π_ 0 [3] and _π_ 0 _._ 5 [14]. Architecturally, these methods share a unified paradigm where a VLM backbone is utilized to extract latent representations from visual observations and language instructions, followed by an action head to generate the control sequences. All models were evaluated using their official configurations. Specifically, we employed a behavior cloning approach by performing supervised fine-tuning (SFT) on our self-collected training dataset. Detailed configurations for each model are listed in the appendix. To ensure reproducibility, we recorded the initial state configurations, including the placement and status of all objects, to guarantee consistent starting conditions across runs. Each task was evaluated over 10 trials with slight spatial perturbations applied to object positions during rollouts, following the LIBERO benchmark protocol [24]. Furthermore, the task time limit was dynamically set to 1.1 times the average human completion time, scaling with task difficulty. This temporal buffer accounts for minor deviations in execution speed, such as a model approaching a target more slowly than a human demonstrator, thereby preventing the unfair penalization of near-complete trajectories while maintaining realistic evaluation standards. 

## _B. Multi-level Evaluation_ 

Table II summarizes the evaluation results of the models under the multi-level framework. Notably, in contrast to the near- 

TABLE II: **Accuracy under Multi-level Evaluation.** 


## of-distribution positions. 

**Finding 2: Structural invariance is lacking when facing topological perturbations.** Beyond mere coordinate shifts, Level 3 challenges the models’ understanding of scene topology by altering the relative arrangement of objects (e.g., swapping positions). Crucially, as shown in Figure 5, this level witnesses the most substantial performance degradation of 12.7%, indicating that models lack structural invariance. They struggle to adapt to new scene layouts where the semantic relationships between objects remain valid but their topological organization has been reconstructed, highlighting a failure in reasoning about relative spatial relations. 

TABLE III: **Level 4 Accuracy - Overall, Unseen Objects (UO), and Confounding Objects (CO).** 

|**Category**|OpenVLA-OFT|_π_0|X-VLA|GR00T1.5|_π_0_._5|
|---|---|---|---|---|---|
|**Overall**|6.4|7.6|6.0|13.3|24.1|
|**UO**|0.8|1.1|0.8|2.1|7.2|
|**CO**|8.6|9.6|7.5|16.9|28.9|


Fig. 5: **Success Rate Decline across Multi-level Evaluation.** 

saturated performance (often _∼_ 90%) [7, 47] in LIBERO [24], the models exhibit significant struggles in our setting. Even at Level 1, which involves only minor spatial perturbations relative to the training set, the average success rate across the five models is merely 39.4%, with even the top-performing _π_ 0 _._ 5 capped at 65.2%. This sharp contrast not only underscores the challenging nature of our benchmark but also exposes the limitations of existing evaluation systems, where performance saturation often masks true model differences. By leveraging diverse training data, our benchmark effectively reveals the performance disparities among different methods. 

Despite the overall difficulty, _π_ 0 _._ 5 maintains the most robust generalization across all levels. We attribute this robustness to its joint training strategy, which effectively incorporates pre-training on the Internet-scale data and sub-task planning. However, for all models, a significant downward trend is observed as task complexity increases. With the introduction of spatial, object-level, and semantic variations from Level 1 to Level 5, the models exhibit an average performance decline of 31.2%. These results highlight the increasing difficulty of the tasks and provide insights into the models’ sensitivity to highlevel perturbations. Based on these quantitative evaluations, we summarize our key findings as follows: 

**Finding 1: VLA models struggle with spatial extrapolation beyond training distributions.** While models maintain reasonable performance under minor jitters (Level 1), the transition to Level 2, characterized by larger spatial shifts, triggers a notable 9.8% drop in average success rate (Figure 5). This decline suggests that current VLM-based policies tend to overfit to the specific spatial configurations in the training data, relying on memorized pixel-level patterns rather than acquiring a robust spatial understanding. Consequently, performance degrades significantly when targets are extrapolated to out- 

**Finding 3: Data diversity enables emergent generalization, though semantic grounding for novel objects remains a bottleneck.** While models trained on standard datasets typically fail on out-of-distribution tasks [24], our diversified LIBERO-X dataset enables the model to maintain non-zero success rates, suggesting that diversity helps mitigate overfitting to specific training scenes. However, a closer inspection of Table III reveals a significant performance gap: success rates on confounding objects are notably higher than those on unseen objects. This disparity indicates that while the model gains robustness against visual distractions, it still struggles to ground instructions to novel visual concepts. The lower performance on unseen objects suggests that despite the VLM’s capabilities, the alignment between pre-trained representations and the control policy remains imperfect for handling unfamiliar visual features. 

TABLE IV: **Level 5 Accuracy - Overall and by Semantic Equivalence Reconstruction Method.** 

|**Category**|OpenVLA-OFT|_π_0|X-VLA|GR00T1.5|_π_0_._5|
|---|---|---|---|---|---|
|**Overall**|4.2|5.1|4.1|9.7|18.0|
|**5-1 (Synonym)**|5.1|3.9|4.3|8.7|18.0|
|**5-2 (Concise)**|5.0|5.0|4.2|8.3|14.6|
|**5-3 (Reorder)**|4.4|5.1|3.0|8.4|18.0|
|**5-4 (Voice)**|5.2|7.5|5.1|10.8|19.6|
|**5-5 (Verbose)**|1.2|4.2|3.9|12.5|19.6|


**Finding 4: Language instruction variations can influence model performance.** Table IV reveals a modest 3.26% drop in success rate from Level 4 to Level 5, indicating that phrasing changes affect execution. Crucially, voice conversion proved to be the least disruptive variation, achieving the highest success rate among all rephrasing methods. This implies that the model maintains better alignment with instructions under syntactic voice shifts compared to other forms of linguistic conversion. 


Fig. 7: **Impact of Time Factor Thresholds on Success Rate.** The x-axis displays time factor multipliers relative to the manual standard, where _∞_ indicates denotes an unbounded threshold. 

## _C. Multi-label Evaluation_ 

Figure 6 visualizes success rates for task labels across five levels. Macroscopically, the progressive shrinking of the enclosed area from Level 1 to 5 illustrates general performance degradation due to escalating complexity. Crucially, we observe a consistent alignment in performance patterns. Within the same level, methods exhibit synchronized variations; dimensions challenging for one model tend to be universally difficult, reflecting inherent task difficulty. Furthermore, across levels, the relative performance hierarchy remains stable. The degradation manifests as a proportional contraction, where models maintain comparative strengths and weaknesses even as absolute success rates decline. 

**Finding 5: Task horizon length critically limits performance.** As illustrated by the “Subtask Count” category (orange axes <mark>)</mark> , models perform best on single-step tasks but degrade sharply as sequence length increases, dropping to near zero for tasks with three or more steps. Notably, for tasks requiring three or more steps, success rates for nearly all models precipitate towards zero. This non-linear performance drop-off suggests that current VLA models struggle with the compounding errors inherent in sequential manipulation. It reveals a fundamental deficiency in long-horizon reasoning and temporal consistency, where models fail to maintain precise execution over extended periods. Consequently, future research must prioritize error mitigation and long-term planning to enable robust multi-step manipulation. 

## _D. Time Limit Threshold Differences Evaluation_ 

Figure 7 illustrates the impact of time limits set relative to the manual standard, which is defined as the average duration of human operation. For instance, by applying multipliers such 

as 0.8 (stringent) and 1.5 (relaxed) to this baseline, we evaluate the model’s adaptability to varying temporal pressures ranging from 0.8 to 1.5 times the human average. 

**Finding 6: Relaxed time limits buffer execution imperfections, though benefits diminish beyond a saturation point.** As shown in Figure 7, stringent constraints (0.8 _×_ ) severely penalize performance. We attribute this to inevitable inference or control errors that result in deviations from the optimal trajectory, rendering most task completion impossible under tight deadlines. Conversely, extending limits yields substantial gains, particularly between the 1.0 _×_ and 1.1 _×_ , justifying our default selection of 1.1 _×_ . We avoid excessive limits (e.g., 1.5 _×_ or beyond) to prevent success via brute-force trial-and-error. Notably, performance plateaus beyond 1.3 _×_ , suggesting that remaining failures arise from fundamental capability deficits like perceptual hallucinations or logic errors rather than temporal insufficiency, thus further time extension cannot compensate for these intrinsic limitations. 

## V. CONCLUSION 

This work introduces LIBERO-X, a comprehensive benchmark for evaluating vision–language–action models under realistic, multi-dimensional distribution shifts. By combining a hierarchically structured evaluation protocol with a highdiversity teleoperation-based training dataset, LIBERO-X enables systematic analysis of model generalization across spatial layouts, object attributes, and task semantics. Experimental results reveal significant performance degradation as complexity increases, exposing limitations in scene understanding and instruction grounding. Overall, LIBERO-X provides a more faithful and rigorous framework for assessing VLA models and guiding future research toward robust robotic deployment. 

REFERENCES 

- [1] Constructions Aeronautiques, Adele Howe, Craig Knoblock, ISI Drew McDermott, Ashwin Ram, Manuela Veloso, Daniel Weld, David Wilkins Sri, Anthony Barrett, Dave Christianson, et al. Pddl—the planning domain definition language. 1998. 

- [2] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A visionlanguage-action flow model for general robot control. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [4] Remi Cadene, Simon Alibert, Alexander Soare, et al. Lerobot: State-of-the-art machine learning for real-world robotics in pytorch. https://github.com/huggingface/ lerobot, 2024. 

- [5] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _International Journal of Robotics Research (IJRR)_ , 44(10-11):1684–1704, 2025. 

- [6] Irving Fang, Juexiao Zhang, Shengbang Tong, and Chen Feng. From intention to execution: Probing the generalization boundaries of vision-language-action models. _arXiv preprint arXiv:2506.09930_ , 2025. 

- [7] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, Jinlan Fu, Jingjing Gong, and Xipeng Qiu. Liberoplus: In-depth robustness analysis of vision-languageaction models. _arXiv preprint arXiv:2510.13626_ , 2025. 

- [8] Ricardo Garcia, Shizhe Chen, and Cordelia Schmid. Towards generalizable vision-language robotic manipulation: A benchmark and llm-guided 3d policy. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

- [9] Dibya Ghosh, Homer Rich Walke, Karl Pertsch, et al. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- [10] Jiayuan Gu, Fanbo Xiang, Xuanlin Li, et al. Maniskill2: A unified benchmark for generalizable manipulation skills. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2023. 

- [11] Songhao Han, Boxiang Qiu, Yue Liao, Siyuan Huang, Chen Gao, Shuicheng YAN, and Si Liu. Robocerebra: A large-scale benchmark for long-horizon robotic manipulation evaluation. In _Proceedings of the Conference on Neural Information Processing System Datasets and Benchmarks Track (NeurIPS)_ , 2025. 

- [12] Edward J Hu, yelong shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu 

Chen. LoRA: Low-rank adaptation of large language models. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2022. 

- [13] Songqiao Hu, Zeyi Liu, Shuang Liu, Jun Cen, Zihan Meng, and Xiao He. Vlsa: Vision-language-action models with plug-and-play safety constraint layer. _arXiv preprint arXiv:2512.11891_ , 2025. 

- [14] Physical Intelligence, Kevin Black, Noah Brown, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [15] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J. Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters (RA-L)_ , 5(2):3019–3026, 2020. 

- [16] Brian Ichter Karl Pertsch, Kyle Stachowicz et al. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- [17] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, et al. Openvla: An open-source vision-language-action model. In _Proceedings of Conference on Robot Learning (CoRL)_ , 2024. 

- [18] Moo Jin Kim, Chelsea Finn, and Percy Liang. Finetuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- [19] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 

- [20] Quanyi Li. Task reconstruction and extrapolation for _π_ 0 using text latent. _arXiv preprint arXiv:2505.03500_ , 2025. 

- [21] Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran Song. Unified video action model. _arXiv preprint arXiv:2503.00200_ , 2025. 

- [22] Xinghang Li, Minghuan Liu, Hanbo Zhang, et al. Visionlanguage foundation models as effective robot imitators. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2024. 

- [23] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- [24] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. In _Proceedings of the Conference on Neural Information Processing System (NeurIPS)_ , 2023. 

- [25] Jijia Liu, Feng Gao, Bingwen Wei, Xinlei Chen, Qingmin Liao, Yi Wu, Chao Yu, and Yu Wang. What can rl bring to vla generalization? an empirical study. _arXiv preprint arXiv:2505.19789_ , 2025. 

- [26] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, 

Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. RDT-1b: a diffusion foundation model for bimanual manipulation. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2025. 

- [27] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters (RA-L)_ , 7(3):7327–7334, 2022. 

- [28] NVIDIA. NVIDIA Isaac Sim: Robotics simulation and synthetic data. https://developer.nvidia.com/isaac-sim, 2023. 

- [29] Abby O’Neill, Abdul Rehman, Maddukur, et al. Open x- embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration0. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2024. 

- [30] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2023. 

- [31] Ethan Perez, Florian Strub, Harm De Vries, Vincent Dumoulin, and Aaron Courville. Film: Visual reasoning with a general conditioning layer. In _Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)_ , 2018. 

- [32] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- [33] Wilbert Pumacay, Ishika Singh, Jiafei Duan, Ranjay Krishna, Jesse Thomason, and Dieter Fox. The colosseum: A benchmark for evaluating generalization for robotic manipulation. _arXiv preprint arXiv:2402.08191_ , 2024. 

- [34] Delin Qu, Haoming Song, Qizhi Chen, et al. Spatialvla: Exploring spatial representations for visual-languageaction model. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [35] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [36] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2012. 

- [37] Zhijie Wang, Zhehua Zhou, Jiayang Song, Yuheng Huang, Zhan Shu, and Lei Ma. Vlatest: Testing and evaluating vision-language-action models for robotic manipulation. _Proceedings of the ACM on Software Engineering_ , 2(FSE):1615–1638, 2025. 

- [38] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. Tinyvla: Toward fast, data-efficient vision-language-action models for robotic manipulation. 

_IEEE Robotics and Automation Letters (RA-L)_ , 10(4): 3988–3995, 2025. 

- [39] Junjie Wen, Yichen Zhu, Minjie Zhu, et al. DiffusionVLA: Scaling robot foundation models via unified diffusion and autoregression. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2025. 

- [40] Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che, Xiaozhu Ju, Zhuqin Yang, Meng Li, Yinuo Zhao, Zhiyuan Xu, Guang Yang, et al. Robomind: Benchmark on multi-embodiment intelligence normative data for robot manipulation. _arXiv preprint arXiv:2412.13877_ , 2024. 

- [41] Shiduo Zhang, Zhe Xu, Peiju Liu, Xiaopeng Yu, Yuan Li, Qinghui Gao, Zhaoye Fei, Zhangyue Yin, Zuxuan Wu, Yu-Gang Jiang, et al. Vlabench: A large-scale benchmark for language-conditioned robotics manipulation with long-horizon reasoning tasks. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2025. 

- [42] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- [43] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, et al. 3d-vla: a 3d vision-language-action generative world model. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2024. 

- [44] Jinliang Zheng, Jianxiong Li, Zhihao Wang, et al. X-vla: Soft-prompted transformer as scalable crossembodiment vision-language-action model. _arXiv preprint arXiv:2510.10274_ , 2025. 

- [45] Ruijie Zheng, Jing Wang, Scott Reed, Johan Bjorck, Yu Fang, Fengyuan Hu, Joel Jang, Kaushil Kundalia, Zongyu Lin, Lo¨ıc Magne, et al. Flare: Robot learning with implicit world modeling. In _Proceedings of Robotics: Science and Systems (RSS) Workshop on Dexterous Manipulation: Learning and Control with Diverse Data_ . 

- [46] Jiaming Zhou, Ke Ye, Jiayi Liu, Teli Ma, Zifan Wang, Ronghe Qiu, Kun-Yu Lin, Zhilin Zhao, and Junwei Liang. Exploring the limits of vision-language-action manipulation in cross-task generalization. In _Proceedings of the Conference on Neural Information Processing System (NeurIPS)_ , 2025. 

- [47] Xueyang Zhou, Yangming Xu, Guiyao Tie, Yongchao Chen, Guowen Zhang, Duanfeng Chu, Pan Zhou, and Lichao Sun. Libero-pro: Towards robust and fair evaluation of vision-language-action models beyond memorization. _[arXiv preprint arXiv:2510.03827]_ , 2025. 

- [48] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Proceedings of Conference on Robot Learning (CoRL)_ , 2023. 

APPENDIX 

The supplementary materials contain the following sections: 

- **Detailed Results of Multi-label Evaluation** A. 

- **Further Analysis of the Impact of Time Limits** B. 

- **Model Details** C. 

- **Scene Design Details** D. 

- **Visual Attribute Variation Cases Analysis** E. 

- **Semantic-equivalent Reformulation Cases** F. 

- _A. Detailed Results of Multi-label Evaluation_ 


Fig. 8: **Fine-grained Multi-label Evaluation in LIBERO-X.** 

To comprehensively assess the capabilities of VLA models, LIBERO-X introduces a fine-grained evaluation system that assigns specific labels to all evaluation tasks. These labels allow for a detailed analysis of the model’s performance across multiple dimensions, particularly focusing on task execution details. The evaluation covers various aspects, including **Interaction Type** , **Subtask Count** , **Spatial Relation Type** , and **Object Attribute Recognition** , which provide insights into how the model handles semantic and physical changes in different scenarios. 

As shown in Figure 8, the fine-grained multi-label evaluation framework adopts a dual-layer design, divided into four major categories. Each category is further subdivided into multiple subcategories, with the number of subcategories displayed alongside. This structure enables a more comprehensive evaluation, allowing LIBERO-X to assess the model’s ability to handle different task dimensions and providing deeper insights into its performance under various conditions. 

**(1) Interaction Type** aims to describe the core actions involved in the task, reflecting the basic behaviors and complexity of task execution. Each interaction type represents 

a key operation the model performs when handling a task, helping evaluate its performance under different action modes. 

- **Placement** : Entails positioning an object onto a target surface or within a container. This category evaluates the model’s precision and stability in executing basic manipulation tasks. 

- **State Change** : Involves altering the environment’s state, such as manipulating articulated objects (e.g., opening drawers or turn the knob). This assesses the model’s capability to perform state transitions effectively. 

- **Composite Actions** : These tasks involve multiple action types simultaneously, such as placing followed by closing, or grabbing followed by placing. These tasks test the model’s ability to coordinate multi-step operations and handle complex planning. 

**(2) Subtask Count** dimension categorizes tasks by the number of required action steps, assessing the model’s capacity for long-horizon planning. Varying the sequence length allows for a granular evaluation of decision-making capabilities across different complexity levels. 

- **Single Action** : Involves a single atomic operation without intermediate steps. This serves as a baseline benchmark for the model’s fundamental execution capability. 

- **Two Actions** : Requires performing two sequential actions (e.g., placing an object and then closing a drawer). This evaluates the model’s ability to handle short-term transitions and maintain logical consistency between consecutive steps. 

- **Three or More Actions** : Involves complex sequences consisting of multiple operations (e.g., grasping, transporting, and placing). These tasks evaluate the model’s robustness in long-horizon reasoning and its ability to mitigate error accumulation over extended task durations. 

**(3) Spatial Relation Type** label describes the relative position and spatial layout of objects in the task, assessing the model’s performance in spatial reasoning and environmental perception. The model must understand the spatial relationships between objects and how these relationships impact task execution. 

- **Surface** : Involves placing objects onto open planar surfaces, such as tables or countertops. This evaluates the model’s precision in identifying and utilizing flat substrates for placement. 

- **Container** : Involves placing objects into enclosed volumes, such as drawers or cabinets. This assesses the model’s ability to navigate constrained spaces and execute insertion tasks accurately. 

- **Left–Right Relation** : Specifies positioning relative to a lateral reference frame (e.g., the left side of a desk caddy). This tests the model’s lateral spatial reasoning and its ability to interpret directional instructions. 

- **Ordinal Region** : Requires selecting a target based on sequential order or rank, such as the top, middle, or bottom drawer. This evaluates the model’s understanding of hierarchical spatial relationships. 

- **Relative Distance** : Involves selecting objects based on proximity to a reference point (e.g., the closest or farthest object). This assesses the model’s depth perception and ability to estimate relative distances. 

**(4) Object Attribute Recognition** label assesses the model’s visual perception accuracy regarding object properties. It focuses on the model’s ability to ground textual instructions to specific visual attributes, such as color, size, pattern, and category, to correctly identify targets in the environment. 

- **Color** : Evaluates the ability to distinguish objects based on chromatic features. The model must accurately identify target objects by hue, even in scenes containing distractors with similar or contrasting color. 

- **Size** : Assesses spatial reasoning regarding object scale. The model is tested on its ability to differentiate relative sizes (e.g., small, medium, large) and select objects that satisfy specific spatial constraints. 

- **Pattern** : Focuses on the recognition of surface details and textures (e.g., stripes, spots). This tests the model’s finegrained visual discrimination capabilities, particularly when identifying objects in visually complex or cluttered scenes. 

- **Category** : Involves semantic classification of objects. The evaluation focuses on the model’s ability to correctly identify and select objects based on their class identity, distinguishing the target from multiple distractors of various categories. 

As shown in Tables V, VI, VII, VIII, and IX, the detailed results of Fine-grained Multi-label Evaluation across Levels 1 to 5 demonstrate the model’s performance under varying task complexities and evaluation dimensions, highlighting its execution capabilities and adaptability when faced with diverse tasks. 

## _B. Further Analysis of the Impact of Time Limits_ 

As shown in Tables V, VI, VII, VIII, and IX, a consistent trend is observed across LEVEL 1 to LEVEL 5: success rates correlate positively with extended time limits. Specifically, with 1.0 _×_ representing the human reference time, the 1.1 _×_ threshold (a 10% extension) yields the most significant performance gain. The improvement is attributed to the temporal buffer, which compensates for inevitable execution noise and environmental dynamics. Although models learn optimal trajectories from human demonstrations, they cannot perfectly replicate human precision. The additional time provides a critical margin for error correction and recovery from deviations. Consequently, 1.1 _×_ is established as the baseline time limit for our evaluation by default. 

Between 1.1 _×_ to 1.5 _×_ , success rates show continued but diminishing improvements. This gain is largely attributable to the increased window for trial-and-error interactions, allowing the model to exhaustively interact with objects rather than robust long-horizon planning (as shown in Figure 9). Data from Table V underscores this limitation: while the _π_ 0 _._ 5 model’s success rate in the “Three or More Actions” category 

surges by 12.4% from 1.0 _×_ to 1.1 _×_ , it only increases by a marginal 1.9% from 1.1 _×_ to 1.5 _×_ . Beyond 1.5 _×_ , performance plateaus. This saturation indicates that time is no longer the limiting factor; instead, the model is constrained by intrinsic bottlenecks in perception and reasoning. Consequently, further extending the time limit fails to yield significant gains on complex tasks. 

## _C. Model Details_ 

In this section, we detail the experimental setup, covering model architectures, training data, and hyperparameter configurations. We provide an in-depth analysis of each model’s structural design and the specific components that drive its performance. Furthermore, we describe the fine-tuning protocols employed to adapt these models to our evaluation tasks. This comprehensive background serves to contextualize the experimental results, elucidating the strengths and limitations of each architecture while establishing a baseline for future optimizations. 

As summarized in Table X, we evaluate a diverse set of VLA models. We initialize these models using their official pre-trained checkpoints and fine-tune them on the LIBERO-X dataset. This approach allows us to rigorously assess how different architectures adapt to complex manipulation scenarios within our proposed multi-level evaluation framework. 

## _•_ OpenVLA-OFT [18] 

**Model Structure:** OpenVLA-OFT [18] is an optimized variant of OpenVLA [17], engineered for real-time, highfrequency robotic control. It integrates parallel decoding and action chunking, enabling the generation of action sequences in a single inference pass. This design significantly enhances inference efficiency and reduces the need for frequent replanning in long-horizon tasks. Furthermore, the model adopts continuous action representations trained with an L1 regression objective to accelerate convergence. To improve language grounding, FiLM (Feature-wise Linear Modulation) [31] is incorporated, ensuring precise adherence to linguistic instructions during execution. 

**Training Data and Configuration:** On data preparation, we utilize Any4LeRobot convert datasets from LeRobot format to RLDS/TFDS format. This conversion preserves the original temporal structure of episodes, mapping observations, actions, and instructions to standard RLDS fields for compatibility with downstream learning frameworks. 

Fine-tuning was conducted using torchrun in a distributed setup (8 processes per node), initialized from the OpenVLA-7B checkpoint. The training configuration specified an L1 training objective, a batch size of 8, a learning rate of 5e-4, and a total of 150,000 steps. We employed LoRA (rank 32) [12] for parameter-efficient adaptation. Image augmentation was used, while diffusion modules and FiLM were disabled in this specific configuration. 

_• π_ 0 [3] and _π_ 0 _._ 5 [14] 

_π_ 0 **Model Structure:** The _π_ 0 model is a VLA framework designed for general-purpose robot control, capable of handling complex and dexterous tasks. By combining a VLM 

## TABLE V: **Results of Fine-grained Multi-label Evaluation and Different Time Limit Thresholds in LEVEL 1.** 

|**Model**||**Interaction **|**Type**||**Subtask Co**|**unt**|||**Spatial Rel**|**ation**|||**Object **|**Attribute**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Placement|State Change|Composite Action|s Single Action|Two Actions T|hree or More Actio|ns<br>Surface|Container<br>|Left–Right Relati|on Ordinal Region|Relative Distanc|e<br>Color|Size|Pattern|Category|
|OpenVLA-OFT (1.0_×_)|**20.3**|**0.0**|**0.0**|**25.3**|**3.8**|**0.0**|**15.9**|**19.9**|**22.1**|**11.5**|**0.0**|**22.8**|**4.1**|**18.5**|**5.7**|
|OpenVLA-OFT (1.1_×_)|**30.3** (+10.0)|**1.6** (+1.6)|**2.0** (+2.0)|**37.7** (+12.4)|**6.5** (+2.7)|**0.0** (+0.0)|**24.9** (+9.0)|**29.2** (+9.3)|**31.9** (+9.8)|**14.7** (+3.2)|**5.0** (+5.0)|**33.8** (+11.0)|**9.6** (+5.5)|**25.4** (+6.9)|**10.2** (+4.5)|
|OpenVLA-OFT (1.5_×_)|**39.6** (+9.3)|**6.8** (+5.2)|**7.3** (+5.3)|**49.0** (+11.3)|**10.2** (+3.7)|**0.4** (+0.4)|**32.5** (+7.6)|**38.4** (+9.2)|**40.5** (+8.6)|**23.6** (+8.9)|**12.0** (+7.0)|**42.6** (+8.8)|**12.7** (+3.1)|**35.7** (+10.3)|**20.3** (+10.1)|
|OpenVLA-OFT (_∞_)|**43.0** (+3.4)|**13.0** (+6.2)|**9.0** (+1.7)|**53.8** (+4.8)|**11.7** (+1.5)|**0.4** (+0.0)|**36.8** (+4.3)|**41.7** (+3.3)|**43.6** (+3.1)|**28.2** (+4.6)|**16.0** (+4.0)|**45.9** (+3.3)|**14.7** (+2.0)|**38.5** (+2.8)|**26.9** (+6.6)|
|_π_0 (1.0_×_)|**19.3**|**9.5**|**5.0**|**24.8**|**4.2**|**0.0**|**22.6**|**15.5**|**16.2**|**21.1**|**2.0**|**19.7**|**15.7**|**15.2**|**14.0**|
|_π_0 (1.1_×_)|**29.9** (+10.6)|**15.4** (+5.9)|**10.7** (+5.7)|**37.5** (+12.7)|**9.8** (+5.6)|**0.0** (+0.0)|**34.1** (+11.5)|**24.9** (+9.4)|**25.6** (+9.4)|**30.7** (+9.6)|**7.0** (+5.0)|**30.2** (+10.5)|**26.9** (+11.2)|**22.0** (+6.8)|**23.1** (+9.1)|
|_π_0 (1.5_×_)|**41.0** (+11.1)|**24.9** (+9.5)|**18.0** (+7.3)|**51.2** (+13.7)|**15.4** (+5.6)|**0.0** (+0.0)|**45.1** (+11.0)|**35.7** (+10.8)|**36.0** (+10.4)|**42.5** (+11.8)|**9.0** (+2.0)|**41.2** (+11.0)|**43.1** (+16.2)|**26.5** (+4.5)|**33.6** (+10.5)|
|_π_0 (_∞_)|**45.4** (+4.4)|**29.6** (+4.7)|**19.0** (+1.0)|**56.9** (+5.7)|**17.4** (+2.0)|**0.0** (+0.0)|**51.1** (+6.0)|**38.9** (+3.2)|**39.3** (+3.3)|**46.4** (+3.9)|**16.0** (+7.0)|**45.2** (+4.0)|**48.2** (+5.1)|**28.5** (+2.0)|**40.6** (+7.0)|
|X-VLA (1.0_×_)|**18.3**|**5.4**|**1.7**|**23.1**|**5.0**|**0.0**|**21.1**|**14.0**|**15.9**|**4.7**|**0.0**|**19.4**|**12.2**|**11.9**|**14.8**|
|X-VLA (1.1_×_)|**31.0** (+12.7)|**7.7** (+2.3)|**4.7** (+3.0)|**37.6** (+14.5)|**12.6** (+7.6)|**0.2** (+0.2)|**35.3** (+14.2)|**23.8** (+9.8)|**27.3** (+11.4)|**12.9** (+8.2)|**1.0** (+1.0)|**32.3** (+12.9)|**24.3** (+12.1)|**23.7** (+11.8)|**20.4** (+5.6)|
|X-VLA (1.5_×_)|**44.7** (+13.7)|**11.8** (+4.1)|**10.0** (+5.3)|**53.7** (+16.1)|**19.7** (+7.1)|**0.9** (+0.7)|**47.9** (+12.6)|**37.3** (+13.5)|**38.4** (+11.1)|**31.3** (+18.4)|**10.0** (+9.0)|**46.3** (+14.0)|**41.2** (+16.9)|**31.9** (+8.2)|**27.8** (+7.4)|
|X-VLA (_∞_)|**48.8** (+4.1)|**14.6** (+2.8)|**12.0** (+2.0)|**58.8** (+5.1)|**21.8** (+2.1)|**0.9** (+0.0)|**51.8** (+3.9)|**41.4** (+4.1)|**42.3** (+3.9)|**33.6** (+2.3)|**18.0** (+8.0)|**50.7** (+4.4)|**43.9** (+2.7)|**34.1** (+2.2)|**31.4** (+3.6)|
|GR00T1.5 (1.0_×_)|**33.2**|**22.1**|**15.0**|**41.1**|**14.8**|**0.4**|**41.7**|**25.6**|**25.8**|**31.5**|**20.0**|**33.4**|**33.7**|**18.3**|**30.6**|
|GR00T1.5 (1.1_×_)|**43.6** (+10.4)|**29.3** (+7.2)|**21.7** (+6.7)|**53.4** (+12.3)|**21.0** (+6.2)|**0.9** (+0.5)|**53.5** (+11.8)|**34.5** (+8.9)|**34.6** (+8.8)|**45.5** (+14.0)|**28.0** (+8.0)|**43.3** (+9.9)|**45.9** (+12.2)|**23.3** (+5.0)|**42.1** (+11.5)|
|GR00T1.5 (1.5_×_)|**52.0** (+8.4)|**42.6** (+13.3)|**30.7** (+9.0)|**64.0** (+10.6)|**26.1** (+5.1)|**1.3** (+0.4)|**63.1** (+9.6)|**42.6** (+8.1)|**41.7** (+7.1)|**56.9** (+11.4)|**34.0** (+6.0)|**51.3** (+8.0)|**56.1** (+10.2)|**28.5** (+5.2)|**54.9** (+12.8)|
|GR00T1.5 (_∞_)|**54.9** (+2.9)|**48.2** (+5.6)|**32.3** (+1.6)|**67.9** (+3.9)|**28.0** (+1.9)|**1.3** (+0.0)|**67.6** (+4.5)|**44.7** (+2.1)|**43.7** (+2.0)|**62.7** (+5.8)|**39.0** (+5.0)|**54.0** (+2.7)|**58.6** (+2.5)|**30.9** (+2.4)|**60.8** (+5.9)|
|_π_0_._5 (1.0_×_)|**45.4**|**34.0**|**29.7**|**50.2**|**35.9**|**18.7**|**45.4**|**42.4**|**45.0**|**44.0**|**27.0**|**46.7**|**39.6**|**45.2**|**34.4**|
|_π_0_._5 (1.1_×_)|**65.8** (+20.4)|**49.8** (+15.8)|**48.3** (+18.6)|**70.9** (+20.7)|**56.7** (+20.8)|**31.1** (+12.4)|**65.1** (+19.7)|**62.7** (+20.3)|**66.4** (+21.4)|**62.5** (+18.5)|**37.0** (+10.0)|**67.7** (+21.0)|**61.0** (+21.4)|**60.4** (+15.2)|**51.2** (+16.8)|
|_π_0_._5 (1.5_×_)|**78.2** (+12.4)|**67.7** (+17.9)|**62.0** (+13.7)|**85.9** (+15.0)|**65.4** (+8.7)|**33.0** (+1.9)|**79.8** (+14.7)|**73.9** (+11.2)|**76.4** (+10.0)|**77.5** (+15.0)|**46.0** (+9.0)|**79.9** (+12.2)|**73.7** (+12.7)|**67.6** (+7.2)|**67.8** (+16.6)|
|_π_0_._5 (_∞_)|**81.2** (+3.0)|**73.0** (+5.3)|**63.7** (+1.7)|**89.9** (+4.0)|**67.1** (+1.7)|**33.0** (+0.0)|**83.8** (+4.0)|**76.7** (+2.8)|**78.5** (+2.1)|**82.4** (+4.9)|**51.0** (+5.0)|**82.7** (+2.8)|**75.5** (+1.8)|**68.5** (+0.9)|**74.8** (+7.0)|
|TABLE|VI: **R**|**esults o**|**f Fine-g**|**rained **|**Multi-la**|**bel Eval**|**uation **|**and D**|**ifferent **|**Time Li**|**mit Thr**|**esholds**|**in L**|**EVEL **|**2.**|
|**Model**||**Interaction **|**Type**||**Subtask Co**|**unt**|||**Spatial Rel**|**ation**|||**Object **|**Attribute**||
||Placement|State Change|Composite Action|s Single Action|Two Actions T|hree or More Actio|ns<br>Surface|Container<br>|Left–Right Relati|on Ordinal Region|Relative Distanc|e<br>Color|Size|Pattern|Category|
|OpenVLA-OFT (1.0_×_)|**12.5**|**0.5**|**0.0**|**15.7**|**2.1**|**0.2**|**10.8**|**11.7**|**12.5**|**7.6**|**1.0**|**14.3**|**1.4**|**9.6**|**3.8**|
|OpenVLA-OFT (1.1_×_)|**18.3** (+5.8)|**1.8** (+1.3)|**1.0** (+1.0)|**22.8** (+7.1)|**4.2** (+2.1)|**0.2** (+0.0)|**15.1** (+4.3)|**17.6** (+5.9)|**19.2** (+6.7)|**10.4** (+2.8)|**3.0** (+2.0)|**20.7** (+6.4)|**4.3** (+2.9)|**14.1** (+4.5)|**6.0** (+2.2)|
|OpenVLA-OFT (1.5_×_)|**26.1** (+7.8)|**5.4** (+3.6)|**3.7** (+2.7)|**32.6** (+9.8)|**6.7** (+2.5)|**0.4** (+0.2)|**22.1** (+7.0)|**24.9** (+7.3)|**26.3** (+7.1)|**15.1** (+4.7)|**8.0** (+5.0)|**29.5** (+8.8)|**5.9** (+1.6)|**20.4** (+6.3)|**10.6** (+4.6)|
|OpenVLA-OFT (_∞_)|**29.2** (+3.1)|**8.6** (+3.2)|**4.3** (+0.6)|**36.7** (+4.1)|**7.5** (+0.8)|**0.4** (+0.0)|**24.9** (+2.8)|**28.1** (+3.2)|**29.4** (+3.1)|**20.0** (+4.9)|**10.0** (+2.0)|**32.4** (+2.9)|**9.6** (+3.7)|**22.4** (+2.0)|**14.3** (+3.7)|
|_π_0 (1.0_×_)|**13.9**|**6.1**|**1.3**|**18.3**|**2.0**|**0.0**|**15.8**|**11.2**|**12.2**|**13.1**|**2.0**|**15.3**|**8.6**|**10.7**|**7.2**|
|_π_0 (1.1_×_)|**22.2** (+8.3)|**9.6** (+3.5)|**5.0** (+3.7)|**28.5** (+10.2)|**4.7** (+2.7)|**0.0** (+0.0)|**24.3** (+8.5)|**18.2** (+7.0)|**19.3** (+7.1)|**20.4** (+7.3)|**3.0** (+1.0)|**24.3** (+9.0)|**15.9** (+7.3)|**15.0** (+4.3)|**11.0** (+3.8)|
|_π_0 (1.5_×_)|**32.3** (+10.1)|**16.1** (+6.5)|**9.0** (+4.0)|**41.0** (+12.5)|**9.3** (+4.6)|**0.0** (+0.0)|**33.6** (+9.3)|**28.1** (+9.9)|**28.5** (+9.2)|**32.4** (+12.0)|**4.0** (+1.0)|**35.0** (+10.7)|**27.8** (+11.9)|**20.2** (+5.2)|**17.3** (+6.3)|
|_π_0 (_∞_)|**35.7** (+3.4)|**21.1** (+5.0)|**10.3** (+1.3)|**45.6** (+4.6)|**10.6** (+1.3)|**0.0** (+0.0)|**38.1** (+4.5)|**31.0** (+2.9)|**31.5** (+3.0)|**35.8** (+3.4)|**5.0** (+1.0)|**38.6** (+3.6)|**32.9** (+5.1)|**21.3** (+1.1)|**21.2** (+3.9)|
|X-VLA (1.0_×_)|**14.1**|**4.7**|**2.7**|**17.8**|**3.6**|**0.0**|**15.5**|**11.2**|**12.9**|**2.4**|**0.0**|**15.0**|**7.8**|**9.3**|**10.2**|
|X-VLA (1.1_×_)|**23.3** (+9.2)|**6.3** (+1.6)|**4.7** (+2.0)|**28.9** (+11.1)|**7.2** (+3.6)|**0.0** (+0.0)|**25.3** (+9.8)|**18.5** (+7.3)|**20.8** (+7.9)|**8.5** (+6.1)|**2.0** (+2.0)|**25.0** (+10.0)|**16.9** (+9.1)|**16.1** (+6.8)|**13.1** (+2.9)|
|X-VLA (1.5_×_)|**36.2** (+12.9)|**8.1** (+1.8)|**6.7** (+2.0)|**44.5** (+15.6)|**11.8** (+4.6)|**0.4** (+0.4)|**37.5** (+12.2)|**30.4** (+11.9)|**31.8** (+11.0)|**22.5** (+14.0)|**5.0** (+3.0)|**38.3** (+13.3)|**29.6** (+12.7)|**25.6** (+9.5)|**19.8** (+6.7)|
|X-VLA (_∞_)|**40.6** (+4.4)|**11.9** (+3.8)|**8.7** (+2.0)|**50.1** (+5.6)|**13.2** (+1.4)|**0.4** (+0.0)|**41.8** (+4.3)|**34.6** (+4.2)|**35.7** (+3.9)|**27.3** (+4.8)|**8.0** (+3.0)|**42.8** (+4.5)|**33.3** (+3.7)|**27.8** (+2.2)|**24.1** (+4.3)|
|GR00T1.5 (1.0_×_)|**25.1**|**11.2**|**6.3**|**31.4**|**8.7**|**0.0**|**31.3**|**18.2**|**18.8**|**21.6**|**11.0**|**25.8**|**24.3**|**15.0**|**18.4**|
|GR00T1.5 (1.1_×_)|**33.4** (+8.3)|**14.7** (+3.5)|**8.7** (+2.4)|**41.5** (+10.1)|**12.5** (+3.8)|**0.0** (+0.0)|**40.6** (+9.3)|**25.1** (+6.9)|**25.7** (+6.9)|**28.0** (+6.4)|**18.0** (+7.0)|**34.4** (+8.6)|**33.1** (+8.8)|**19.4** (+4.4)|**24.0** (+5.6)|
|GR00T1.5 (1.5_×_)|**41.4** (+8.0)|**25.6** (+10.9)|**13.3** (+4.6)|**51.9** (+10.4)|**16.5** (+4.0)|**0.0** (+0.0)|**49.0** (+8.4)|**33.1** (+8.0)|**32.9** (+7.2)|**40.4** (+12.4)|**21.0** (+3.0)|**42.4** (+8.0)|**42.0** (+8.9)|**24.1** (+4.7)|**34.7** (+10.7)|
|GR00T1.5 (_∞_)|**44.4** (+3.0)|**30.5** (+4.9)|**14.3** (+1.0)|**56.0** (+4.1)|**17.9** (+1.4)|**0.0** (+0.0)|**53.2** (+4.2)|**35.6** (+2.5)|**35.3** (+2.4)|**44.9** (+4.5)|**26.0** (+5.0)|**45.2** (+2.8)|**45.5** (+3.5)|**26.1** (+2.0)|**40.0** (+5.3)|
|_π_0_._5 (1.0_×_)|**37.9**|**26.1**|**20.3**|**42.9**|**26.2**|**15.4**|**37.6**|**35.4**|**38.0**|**30.2**|**15.0**|**39.1**|**35.1**|**36.7**|**27.7**|
|_π_0_._5 (1.1_×_)|**53.5** (+15.6)|**36.8** (+10.7)|**28.0** (+7.7)|**59.8** (+16.9)|**40.1** (+13.9)|**21.3** (+5.9)|**53.1** (+15.5)|**49.8** (+14.4)|**53.6** (+15.6)|**44.0** (+13.8)|**21.0** (+6.0)|**56.4** (+17.3)|**47.5** (+12.4)|**49.4** (+12.7)|**36.3** (+8.6)|
|_π_0_._5 (1.5_×_)|**66.8** (+13.3)|**49.8** (+13.0)|**37.7** (+9.7)|**75.6** (+15.8)|**49.1** (+9.0)|**23.0** (+1.7)|**66.8** (+13.7)|**62.7** (+12.9)|**65.7** (+12.1)|**60.7** (+16.7)|**28.0** (+7.0)|**70.5** (+14.1)|**59.6** (+12.1)|**57.8** (+8.4)|**47.8** (+11.5)|
|_π_0_._5 (_∞_)|**69.8** (+3.0)|**55.1** (+5.3)|**39.0** (+1.3)|**79.7** (+4.1)|**50.7** (+1.6)|**23.0** (+0.0)|**70.8** (+4.0)|**65.5** (+2.8)|**68.2** (+2.5)|**64.7** (+4.0)|**34.0** (+6.0)|**73.1** (+2.6)|**62.5** (+2.9)|**60.0** (+2.2)|**54.2** (+6.4)|
|TABLE|VII: **R**|**esults **|**of Fine-**|**grained **|**Multi-l**|**abel Eval**|**uation **|**and D**|**ifferent **|**Time Li**|**mit Thr**|**eshold**|**s in L**|**EVEL**|**3.**|


|**Model**||**Interaction T**|**ype**||**Subtask Cou**|**nt**|||**Spatial Rela**|**tion**|||**Object **|**Attribute**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Placement|State Change|Composite Actions|Single Action|Two Actions T|hree or More Actions|Surface|Container|Left–Right Relatio|n Ordinal Region|Relative Distance|Color|Size|Pattern|Category|
|OpenVLA-OFT (1.0_×_)|**6.9**|**0.0**|**0.0**|**8.8**|**0.8**|**0.0**|**4.4**|**7.6**|**7.6**|**8.4**|**1.0**|**7.8**|**2.2**|**6.3**|**1.4**|
|OpenVLA-OFT (1.1_×_)|**9.2** (+2.3)|**0.0** (+0.0)|**0.0** (+0.0)|**11.7** (+2.9)|**0.9** (+0.1)|**0.0** (+0.0)|**6.0** (+1.6)|**9.8** (+2.2)|**9.8** (+2.2)|**9.5** (+1.1)|**1.0** (+0.0)|**10.3** (+2.5)|**2.4** (+0.2)|**8.1** (+1.8)|**2.6** (+1.2)|
|OpenVLA-OFT (1.5_×_)|**13.5** (+4.3)|**0.7** (+0.7)|**0.0** (+0.0)|**17.3** (+5.6)|**1.4** (+0.5)|**0.0** (+0.0)|**9.6** (+3.6)|**13.9** (+4.1)|**13.2** (+3.4)|**14.7** (+5.2)|**3.0** (+2.0)|**15.0** (+4.7)|**2.5** (+0.1)|**10.9** (+2.8)|**5.6** (+3.0)|
|OpenVLA-OFT (_∞_)|**16.0** (+2.5)|**1.2** (+0.5)|**0.0** (+0.0)|**20.5** (+3.2)|**1.6** (+0.2)|**0.0** (+0.0)|**11.9** (+2.3)|**16.2** (+2.3)|**15.1** (+1.9)|**18.0** (+3.3)|**4.0** (+1.0)|**17.9** (+2.9)|**4.1** (+1.6)|**11.1** (+0.2)|**7.0** (+1.4)|
|_π_0 (1.0_×_)|**7.6**|**4.6**|**1.0**|**10.2**|**0.5**|**0.0**|**7.8**|**6.9**|**6.5**|**12.5**|**0.0**|**7.9**|**1.8**|**8.0**|**6.4**|
|_π_0 (1.1_×_)|**10.9** (+3.3)|**6.3** (+1.7)|**1.3** (+0.3)|**14.7** (+4.5)|**0.9** (+0.4)|**0.0** (+0.0)|**11.8** (+4.0)|**9.5** (+2.6)|**9.1** (+2.6)|**15.8** (+3.3)|**0.0** (+0.0)|**11.7** (+3.8)|**2.2** (+0.4)|**9.4** (+1.4)|**9.4** (+3.0)|
|_π_0 (1.5_×_)|**16.9** (+6.0)|**9.5** (+3.2)|**3.7** (+2.4)|**22.1** (+7.4)|**3.2** (+2.3)|**0.0** (+0.0)|**17.5** (+5.7)|**15.0** (+5.5)|**13.9** (+4.8)|**23.8** (+8.0)|**0.0** (+0.0)|**18.3** (+6.6)|**3.5** (+1.3)|**12.4** (+3.0)|**13.8** (+4.4)|
|_π_0 (_∞_)|**19.9** (+3.0)|**12.6** (+3.1)|**3.7** (+0.0)|**26.2** (+4.1)|**3.9** (+0.7)|**0.0** (+0.0)|**20.1** (+2.6)|**18.1** (+3.1)|**17.4** (+3.5)|**27.3** (+3.5)|**0.0** (+0.0)|**21.8** (+3.5)|**4.3** (+0.8)|**13.7** (+1.3)|**16.2** (+2.4)|
|X-VLA (1.0_×_)|**7.3**|**1.8**|**0.0**|**9.4**|**1.2**|**0.0**|**6.7**|**6.6**|**6.8**|**4.4**|**0.0**|**8.1**|**3.9**|**6.9**|**3.6**|
|X-VLA (1.1_×_)|**10.5** (+3.2)|**3.2** (+1.4)|**1.0** (+1.0)|**13.5** (+4.1)|**1.9** (+0.7)|**0.0** (+0.0)|**9.4** (+2.7)|**9.8** (+3.2)|**9.8** (+3.0)|**8.2** (+3.8)|**0.0** (+0.0)|**11.6** (+3.5)|**5.7** (+1.8)|**8.9** (+2.0)|**5.2** (+1.6)|
|X-VLA (1.5_×_)|**18.0** (+7.5)|**6.3** (+3.1)|**4.3** (+3.3)|**22.9** (+9.4)|**3.8** (+1.9)|**0.0** (+0.0)|**16.7** (+7.3)|**16.7** (+6.9)|**15.8** (+6.0)|**19.6** (+11.4)|**1.0** (+1.0)|**19.7** (+8.1)|**9.2** (+3.5)|**14.4** (+5.5)|**9.6** (+4.4)|
|X-VLA (_∞_)|**22.1** (+4.1)|**9.3** (+3.0)|**6.3** (+2.0)|**28.2** (+5.3)|**4.8** (+1.0)|**0.0** (+0.0)|**20.8** (+4.1)|**20.6** (+3.9)|**19.3** (+3.5)|**26.5** (+6.9)|**5.0** (+4.0)|**24.1** (+4.4)|**12.9** (+3.7)|**15.9** (+1.5)|**13.1** (+3.5)|
|GR00T1.5 (1.0_×_)|**13.4**|**8.9**|**3.3**|**17.7**|**2.6**|**0.0**|**16.1**|**10.2**|**10.7**|**19.6**|**9.0**|**14.2**|**6.7**|**8.7**|**12.7**|
|GR00T1.5 (1.1_×_)|**18.7** (+5.3)|**11.4** (+2.5)|**4.3** (+1.0)|**24.2** (+6.5)|**4.6** (+2.0)|**0.0** (+0.0)|**22.5** (+6.4)|**13.9** (+3.7)|**14.4** (+3.7)|**25.6** (+6.0)|**11.0** (+2.0)|**19.5** (+5.3)|**10.4** (+3.7)|**12.0** (+3.3)|**17.6** (+4.9)|
|GR00T1.5 (1.5_×_)|**25.4** (+6.7)|**20.4** (+9.0)|**7.3** (+3.0)|**33.3** (+9.1)|**6.6** (+2.0)|**0.0** (+0.0)|**31.3** (+8.8)|**19.5** (+5.6)|**18.6** (+4.2)|**36.4** (+10.8)|**15.0** (+4.0)|**26.6** (+7.1)|**15.9** (+5.5)|**13.3** (+1.3)|**27.0** (+9.4)|
|GR00T1.5 (_∞_)|**29.2** (+3.8)|**27.0** (+6.6)|**9.0** (+1.7)|**38.7** (+5.4)|**8.3** (+1.7)|**0.0** (+0.0)|**37.1** (+5.8)|**22.4** (+2.9)|**20.8** (+2.2)|**43.5** (+7.1)|**22.0** (+7.0)|**30.3** (+3.7)|**19.6** (+3.7)|**15.4** (+2.1)|**34.7** (+7.7)|
|_π_0_._5 (1.0_×_)|**26.0**|**21.1**|**14.5**|**30.9**|**15.3**|**7.2**|**26.0**|**24.1**|**24.3**|**28.4**|**0.0**|**28.3**|**10.0**|**25.4**|**21.2**|
|_π_0_._5 (1.1_×_)|**35.5** (+9.5)|**35.1** (+14.0)|**24.6** (+10.1)|**42.4** (+11.5)|**22.0** (+6.7)|**9.1** (+1.9)|**37.5** (+11.5)|**32.2** (+8.1)|**31.7** (+7.4)|**42.7** (+14.3)|**0.0** (+0.0)|**38.5** (+10.2)|**17.8** (+7.8)|**32.2** (+6.8)|**30.3** (+9.1)|
|_π_0_._5 (1.5_×_)|**48.1** (+12.6)|**48.8** (+13.7)|**34.7** (+10.1)|**57.7** (+15.3)|**29.6** (+7.6)|**10.9** (+1.8)|**51.0** (+13.5)|**44.1** (+11.9)|**42.2** (+10.5)|**56.4** (+13.7)|**1.0** (+1.0)|**52.6** (+14.1)|**28.2** (+10.4|) **35.9** (+3.7)|**41.3** (+11.0)|
|_π_0_._5 (_∞_)|**52.6** (+4.5)|**54.5** (+5.7)|**36.2** (+1.5)|**63.7** (+6.0)|**31.6** (+2.0)|**10.9** (+0.0)|**56.1** (+5.1)|**48.5** (+4.4)|**46.4** (+4.2)|**63.5** (+7.1)|**1.0** (+0.0)|**56.9** (+4.3)|**34.1** (+5.9)|**39.3** (+3.4)|**47.5** (+6.2)|


with flow matching, _π_ 0 generates continuous actions. It is pre-trained on diverse robot data (single/dual-arm, mobile) to ensure broad generalization across various hardware and complex multi-stage tasks. 

_π_ 0 _._ 5 **Model Structure:** An evolution of _π_ 0 focused on broader semantic generalization. It incorporates internet-scale data and employs a two-stage training process. _π_ 0 _._ 5 integrates high-level subtask prediction with low-level control, significantly improving performance in novel environments and 

reducing the need for task-specific retraining. 

**Training Data and Configuration:** Visual inputs include resized 224 _×_ 224 wrist and third-person images. Both models are fine-tuned on LIBERO-X using pre-trained weights. 

- _π_ 0: Fine-tuned via LoRA [12] on 1 A100 GPU (Batch Size: 32, Action Chunk: 50). 

- _π_ 0 _._ 5: Full-parameter fine-tuning on 4 A100 GPUs (Batch Size: 256, Action Chunk: 10). 

Both models undergo 30,000 training iterations with standard 

TABLE VIII: **Results of Fine-grained Multi-label Evaluation and Different Time Limit Thresholds in LEVEL 4.** 

|**Model**||**Interaction T**|**ype**||**Subtask Cou**|**nt**|||**Spatial Rel**|**ation**|||**Object **|**Attribute**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Placement|State Change|Composite Actions|Single Action|Two Actions T|hree or More Actions|Surface|Container<br>L|eft–Right Relatio|n Ordinal Region|Relative Distance|Color|Size|Pattern|Category|
|OpenVLA-OFT (1.0_×_)|**4.7**|**0.4**|**0.0**|**5.6**|**0.2**|**0.0**|**3.7**|**4.8**|**5.0**|**6.3**|**0.0**|**5.6**|**2.0**|**4.4**|**1.2**|
|OpenVLA-OFT (1.1_×_)|**6.6** (+1.9)|**0.5** (+0.1)|**0.0** (+0.0)|**7.8** (+2.2)|**0.3** (+0.1)|**0.0** (+0.0)|**5.7** (+2.0)|**6.3** (+1.5)|**7.1** (+2.1)|**6.8** (+0.5)|**0.0** (+0.0)|**8.0** (+2.4)|**3.4** (+1.4)|**6.2** (+1.8)|**1.6** (+0.4)|
|OpenVLA-OFT (1.5_×_)|**9.7** (+3.1)|**0.7** (+0.2)|**0.0** (+0.0)|**11.5** (+3.7)|**0.5** (+0.2)|**0.0** (+0.0)|**8.9** (+3.2)|**9.0** (+2.7)|**9.6** (+2.5)|**10.0** (+3.2)|**0.0** (+0.0)|**11.8** (+3.8)|**6.4** (+3.0)|**9.6** (+3.4)|**2.9** (+1.3)|
|OpenVLA-OFT (_∞_)|**11.9** (+2.2)|**2.8** (+2.1)|**0.3** (+0.3)|**14.4** (+2.9)|**0.7** (+0.2)|**0.0** (+0.0)|**11.2** (+2.3)|**11.1** (+2.1)|**11.2** (+1.6)|**16.3** (+6.3)|**0.0** (+0.0)|**14.6** (+2.8)|**8.1** (+1.7)|**12.8** (+3.2)|**4.2** (+1.3)|
|_π_0 (1.0_×_)|**5.1**|**5.6**|**1.3**|**6.4**|**0.7**|**0.0**|**6.4**|**4.1**|**4.6**|**8.5**|**0.0**|**6.3**|**2.4**|**5.6**|**2.8**|
|_π_0 (1.1_×_)|**7.5** (+2.4)|**6.8** (+1.2)|**1.7** (+0.4)|**9.3** (+2.9)|**0.8** (+0.1)|**0.0** (+0.0)|**9.1** (+2.7)|**6.0** (+1.9)|**6.8** (+2.2)|**12.3** (+3.8)|**0.0** (+0.0)|**9.1** (+2.8)|**3.5** (+1.1)|**8.9** (+3.3)|**3.7** (+0.9)|
|_π_0 (1.5_×_)|**11.7** (+4.2)|**9.8** (+3.0)|**2.0** (+0.3)|**14.4** (+5.1)|**1.5** (+0.7)|**0.0** (+0.0)|**14.1** (+5.0)|**9.4** (+3.4)|**10.0** (+3.2)|**19.0** (+6.7)|**0.0** (+0.0)|**14.4** (+5.3)|**6.6** (+3.1)|**14.6** (+5.7)|**5.8** (+2.1)|
|_π_0 (_∞_)|**14.3** (+2.6)|**12.8** (+3.0)|**2.3** (+0.3)|**17.8** (+3.4)|**2.1** (+0.6)|**0.0** (+0.0)|**16.9** (+2.8)|**11.9** (+2.5)|**12.6** (+2.6)|**24.2** (+5.2)|**2.9** (+2.9)|**17.7** (+3.3)|**8.9** (+2.3)|**18.1** (+3.5)|**7.0** (+1.2)|
|X-VLA (1.0_×_)|**4.2**|**2.1**|**0.0**|**5.2**|**0.4**|**0.0**|**4.9**|**3.4**|**3.6**|**3.2**|**0.0**|**5.4**|**4.7**|**3.6**|**1.7**|
|X-VLA (1.1_×_)|**6.0** (+1.8)|**3.0** (+0.9)|**0.3** (+0.3)|**7.2** (+2.0)|**0.8** (+0.4)|**0.0** (+0.0)|**6.9** (+2.0)|**4.9** (+1.5)|**5.2** (+1.6)|**4.4** (+1.2)|**0.0** (+0.0)|**7.5** (+2.1)|**5.9** (+1.2)|**4.7** (+1.1)|**2.8** (+1.1)|
|X-VLA (1.5_×_)|**10.2** (+4.2)|**4.9** (+1.9)|**0.3** (+0.0)|**12.4** (+5.2)|**1.1** (+0.3)|**0.2** (+0.2)|**11.8** (+4.9)|**8.4** (+3.5)|**8.5** (+3.3)|**9.7** (+5.3)|**1.4** (+1.4)|**12.5** (+5.0)|**10.2** (+4.3)|**8.7** (+4.0)|**5.0** (+2.2)|
|X-VLA (_∞_)|**12.9** (+2.7)|**7.5** (+2.6)|**0.7** (+0.4)|**15.8** (+3.4)|**1.5** (+0.4)|**0.2** (+0.0)|**14.3** (+2.5)|**11.2** (+2.8)|**11.0** (+2.5)|**13.0** (+3.3)|**1.4** (+0.0)|**15.8** (+3.3)|**14.2** (+4.0)|**11.4** (+2.7)|**6.0** (+1.0)|
|GR00T1.5 (1.0_×_)|**10.0**|**6.8**|**1.7**|**12.3**|**1.2**|**0.0**|**13.1**|**7.2**|**7.6**|**14.4**|**0.0**|**12.3**|**11.0**|**8.5**|**3.7**|
|GR00T1.5 (1.1_×_)|**13.1** (+3.1)|**9.5** (+2.7)|**2.0** (+0.3)|**16.0** (+3.7)|**2.1** (+0.9)|**0.0** (+0.0)|**17.6** (+4.5)|**9.2** (+2.0)|**9.7** (+2.1)|**18.9** (+4.5)|**0.0** (+0.0)|**16.2** (+3.9)|**13.4** (+2.4)|**12.3** (+3.8)|**4.8** (+1.1)|
|GR00T1.5 (1.5_×_)|**18.1** (+5.0)|**16.7** (+7.2)|**3.0** (+1.0)|**22.4** (+6.4)|**3.2** (+1.1)|**0.0** (+0.0)|**25.1** (+7.5)|**12.8** (+3.6)|**12.9** (+3.2)|**27.2** (+8.3)|**1.4** (+1.4)|**22.1** (+5.9)|**20.3** (+6.9)|**16.2** (+3.9)|**8.8** (+4.0)|
|GR00T1.5 (_∞_)|**21.5** (+3.4)|**24.6** (+7.9)|**3.3** (+0.3)|**27.0** (+4.6)|**4.1** (+0.9)|**0.0** (+0.0)|**31.0** (+5.9)|**15.1** (+2.3)|**15.2** (+2.3)|**33.1** (+5.9)|**4.3** (+2.9)|**26.5** (+4.4)|**23.9** (+3.6)|**19.1** (+2.9)|**12.3** (+3.5)|
|_π_0_._5 (1.0_×_)|**17.3**|**16.7**|**4.0**|**21.2**|**3.5**|**2.0**|**18.2**|**16.3**|**17.5**|**22.4**|**4.3**|**21.5**|**15.7**|**16.5**|**9.7**|
|_π_0_._5 (1.1_×_)|**23.4** (+6.1)|**25.3** (+8.6)|**7.7** (+3.7)|**28.5** (+7.3)|**6.1** (+2.6)|**2.8** (+0.8)|**26.1** (+7.9)|**21.2** (+4.9)|**22.7** (+5.2)|**29.0** (+6.6)|**7.1** (+2.8)|**29.0** (+7.5)|**21.7** (+6.0)|**22.4** (+5.9)|**14.4** (+4.7)|
|_π_0_._5 (1.5_×_)|**30.5** (+7.1)|**39.1** (+13.8)|**13.0** (+5.3)|**37.4** (+8.9)|**9.6** (+3.5)|**3.5** (+0.7)|**35.6** (+9.5)|**27.5** (+6.3)|**28.1** (+5.4)|**39.4** (+10.4)|**18.6** (+11.5)|**36.9** (+7.9)|**31.8** (+10.1|) **29.3** (+6.9)|**21.6** (+7.2)|
|_π_0_._5 (_∞_)|**38.0** (+7.5)|**43.2** (+4.1)|**13.3** (+0.3)|**46.5** (+9.1)|**11.0** (+1.4)|**3.7** (+0.2)|**42.7** (+7.1)|**35.1** (+7.6)|**34.6** (+6.5)|**49.0** (+9.6)|**21.4** (+2.8)|**45.5** (+8.6)|**38.0** (+6.2)|**36.7** (+7.4)|**25.7** (+4.1)|


TABLE IX: **Results of Fine-grained Multi-label Evaluation and Different Time Limit Thresholds in LEVEL 5.** 

|**Model**||**Interaction **|**Type**||**Subtask Co**|**unt**|||**Spatial Rel**|**ation**|||**Object **|**Attribute**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Placement|State Change|Composite Actions|Single Action|Two Actions T|hree or More Actions|Surface|Container|Left–Right Relatio|n Ordinal Region|Relative Distance|Color|Size|Pattern|Category|
|OpenVLA-OFT (1.0_×_)|**3.0**|**0.5**|**0.0**|**3.6**|**0.2**|**0.0**|**2.5**|**3.1**|**3.1**|**5.2**|**0.0**|**3.6**|**1.2**|**3.1**|**0.8**|
|OpenVLA-OFT (1.1_×_)|**4.3** (+1.3)|**0.5** (+0.0)|**0.0** (+0.0)|**5.1** (+1.5)|**0.2** (+0.0)|**0.0** (+0.0)|**3.8** (+1.3)|**4.1** (+1.0)|**4.4** (+1.3)|**5.9** (+0.7)|**0.0** (+0.0)|**5.2** (+1.6)|**1.6** (+0.4)|**4.5** (+1.4)|**1.3** (+0.5)|
|OpenVLA-OFT (1.5_×_)|**6.4** (+2.1)|**0.7** (+0.2)|**0.0** (+0.0)|**7.6** (+2.5)|**0.3** (+0.1)|**0.0** (+0.0)|**6.0** (+2.2)|**5.8** (+1.7)|**6.1** (+1.7)|**7.5** (+1.6)|**0.0** (+0.0)|**7.8** (+2.6)|**3.4** (+1.8)|**7.1** (+2.6)|**1.9** (+0.6)|
|OpenVLA-OFT (_∞_)|**8.1** (+1.7)|**1.2** (+0.5)|**0.0** (+0.0)|**9.8** (+2.2)|**0.4** (+0.1)|**0.0** (+0.0)|**7.6** (+1.6)|**7.6** (+1.8)|**7.4** (+1.3)|**12.5** (+5.0)|**0.0** (+0.0)|**10.1** (+2.3)|**4.8** (+1.4)|**9.6** (+2.5)|**2.5** (+0.6)|
|_π_0 (1.0_×_)|**3.5**|**3.5**|**0.0**|**4.4**|**0.4**|**0.0**|**4.9**|**2.4**|**2.7**|**7.7**|**0.0**|**4.6**|**1.9**|**4.3**|**1.4**|
|_π_0 (1.1_×_)|**5.0** (+1.5)|**4.6** (+1.1)|**0.0** (+0.0)|**6.3** (+1.9)|**0.4** (+0.0)|**0.0** (+0.0)|**6.8** (+1.9)|**3.6** (+1.2)|**4.1** (+1.4)|**10.0** (+2.3)|**0.0** (+0.0)|**6.2** (+1.6)|**2.6** (+0.7)|**6.2** (+1.9)|**2.2** (+0.8)|
|_π_0 (1.5_×_)|**8.6** (+3.6)|**8.2** (+3.6)|**0.3** (+0.3)|**10.9** (+4.6)|**0.6** (+0.2)|**0.0** (+0.0)|**12.3** (+5.5)|**5.9** (+2.3)|**6.5** (+2.4)|**16.8** (+6.8)|**0.0** (+0.0)|**10.7** (+4.5)|**5.9** (+3.3)|**11.2** (+5.0)|**4.1** (+1.9)|
|_π_0 (_∞_)|**11.3** (+2.7)|**11.2** (+3.0)|**0.7** (+0.4)|**14.2** (+3.3)|**1.0** (+0.4)|**0.0** (+0.0)|**15.7** (+3.4)|**7.9** (+2.0)|**8.3** (+1.8)|**22.5** (+5.7)|**0.0** (+0.0)|**13.8** (+3.1)|**8.4** (+2.5)|**13.8** (+2.6)|**5.6** (+1.5)|
|X-VLA (1.0_×_)|**2.7**|**2.6**|**0.3**|**3.4**|**0.1**|**0.0**|**4.0**|**1.8**|**1.9**|**2.0**|**0.0**|**3.6**|**3.1**|**1.7**|**1.2**|
|X-VLA (1.1_×_)|**4.0** (+1.3)|**3.3** (+0.7)|**0.3** (+0.0)|**5.0** (+1.6)|**0.3** (+0.2)|**0.0** (+0.0)|**5.8** (+1.8)|**2.7** (+0.9)|**2.9** (+1.0)|**2.4** (+0.4)|**0.0** (+0.0)|**5.3** (+1.7)|**4.8** (+1.7)|**2.5** (+0.8)|**1.7** (+0.5)|
|X-VLA (1.5_×_)|**7.0** (+3.0)|**5.1** (+1.8)|**0.3** (+0.0)|**8.7** (+3.7)|**0.5** (+0.2)|**0.0** (+0.0)|**10.1** (+4.3)|**4.7** (+2.0)|**5.0** (+2.1)|**6.1** (+3.7)|**0.0** (+0.0)|**8.6** (+3.3)|**9.0** (+4.2)|**4.7** (+2.2)|**3.6** (+1.9)|
|X-VLA (_∞_)|**10.0** (+3.0)|**7.2** (+2.1)|**0.7** (+0.4)|**12.4** (+3.7)|**0.7** (+0.2)|**0.0** (+0.0)|**13.4** (+3.3)|**7.3** (+2.6)|**7.5** (+2.5)|**10.8** (+4.7)|**0.0** (+0.0)|**12.3** (+3.7)|**12.6** (+3.6)|**7.8** (+3.1)|**4.8** (+1.2)|
|GR00T1.5 (1.0_×_)|**7.1**|**6.0**|**1.7**|**8.8**|**1.0**|**0.0**|**10.0**|**4.7**|**5.2**|**7.5**|**0.0**|**8.8**|**6.8**|**5.8**|**3.7**|
|GR00T1.5 (1.1_×_)|**9.6** (+2.5)|**7.2** (+1.2)|**2.3** (+0.6)|**11.7** (+2.9)|**2.1** (+1.1)|**0.0** (+0.0)|**13.3** (+3.3)|**6.4** (+1.7)|**7.2** (+2.0)|**10.0** (+2.5)|**0.0** (+0.0)|**11.9** (+3.1)|**8.7** (+1.9)|**8.8** (+3.0)|**4.2** (+0.5)|
|GR00T1.5 (1.5_×_)|**13.9** (+4.3)|**14.6** (+7.4)|**2.7** (+0.4)|**17.2** (+5.5)|**2.9** (+0.8)|**0.0** (+0.0)|**19.9** (+6.6)|**9.3** (+2.9)|**9.6** (+2.4)|**18.6** (+8.6)|**2.9** (+2.9)|**17.0** (+5.1)|**14.4** (+5.7)|**12.6** (+3.8)|**7.4** (+3.2)|
|GR00T1.5 (_∞_)|**17.3** (+3.4)|**22.5** (+7.9)|**3.3** (+0.6)|**21.8** (+4.6)|**3.6** (+0.7)|**0.0** (+0.0)|**25.7** (+5.8)|**11.5** (+2.2)|**11.6** (+2.0)|**26.1** (+7.5)|**4.3** (+1.4)|**21.3** (+4.3)|**18.8** (+4.4)|**15.5** (+2.9)|**10.5** (+3.1)|
|_π_0_._5 (1.0_×_)|**12.5**|**16.5**|**3.3**|**15.7**|**2.1**|**1.1**|**14.3**|**11.5**|**11.8**|**13.7**|**4.3**|**15.4**|**13.0**|**10.4**|**9.3**|
|_π_0_._5 (1.1_×_)|**17.1** (+4.6)|**22.8** (+6.3)|**5.3** (+2.0)|**21.5** (+5.8)|**3.9** (+1.8)|**1.5** (+0.4)|**20.1** (+5.8)|**15.6** (+4.1)|**15.6** (+3.8)|**19.0** (+5.3)|**7.1** (+2.8)|**21.1** (+5.7)|**18.5** (+5.5)|**14.8** (+4.4)|**12.4** (+3.1)|
|_π_0_._5 (1.5_×_)|**23.0** (+5.9)|**33.3** (+10.5)|**8.7** (+3.4)|**28.5** (+7.0)|**7.3** (+3.4)|**2.4** (+0.9)|**28.4** (+8.3)|**20.3** (+4.7)|**19.3** (+3.7)|**27.0** (+8.0)|**15.7** (+8.6)|**27.5** (+6.4)|**28.7** (+10.2)|**19.5** (+4.7)|**18.2** (+5.8)|
|_π_0_._5 (_∞_)|**28.9** (+5.9)|**36.8** (+3.5)|**9.0** (+0.3)|**35.7** (+7.2)|**8.4** (+1.1)|**2.4** (+0.0)|**34.2** (+5.8)|**26.2** (+5.9)|**23.6** (+4.3)|**33.9** (+6.9)|**18.6** (+2.9)|**34.4** (+6.9)|**35.8** (+7.1)|**24.8** (+5.3)|**21.3** (+3.1)|


TABLE X: **Model Checkpoint Addresses.** 

|**Model**|**Checkpoint Address**|
|---|---|
|OpenVLA-OFT<br>_π_0|https://huggingface.co/openvla/openvla-7b<br>https://storage.googleapis.com/openpi-assets/checkpoints/pi0<br>base|
|X-VLA|https://huggingface.co/2toINF/X-VLA-Pt|
|GR00T1.5<br>_π_0_._5|https://huggingface.co/nvidia/GR00T-N1.5-3B<br>https://storage.googleapis.com/openpi-assets/checkpoints/pi05<br>base|


normalization. 

## _•_ X-VLA [44] 

**Model Structure:** The X-VLA architecture is a scalable, cross-embodiment VLA framework designed for robust adaptation across diverse robotic platforms. It incorporates learnable soft prompts to condition the model on specific hardware configurations and task distributions. The architecture fuses visual observations, language instructions, and proprioceptive states via a Transformer encoder, while employing a flowmatching policy to refine continuous action outputs for dexterous execution. 

**Training Data and Configuration:** Data preparation utilizes the LeRobot pipeline. Raw data is converted into the standard LeRobot format (parquet + multi-view video), and for each dataset, a meta.json file is generated, containing the dataset name, episode list, and instruction information. The corresponding dataset name is then registered in X-VLA. At 

training, the built-in processor dynamically tokenizes images and trajectories into the unified format required by the model. 

Fine-tuning is conducted using the accelerate library with bf16 mixed precision to optimize computational efficiency. We initialize from a pre-trained checkpoint and train for 100,000 iterations with a batch size of 16. The optimization schedule includes a learning rate of 1e-4 and a coefficient of 0.1. To ensure stable adaptation, we employ a two-phase strategy: 1,000 steps of backbone freezing, followed by a 2,000-step learning rate warm-up. 

_•_ GR00T1.5 [2] 

**Model Structure:** GR00T N1.5 is a generalist humanoid foundation model developed by NVIDIA. Its architecture comprises three modular components: a frozen VLM for semantic embedding extraction, an Adapter for cross-modal alignment, and a Diffusion Transformer (DiT) [30] for policy generation. The VLM encodes visual and linguistic inputs, which the Adapter projects into the DiT’s latent space to synthesize actions via attention mechanisms. A critical innovation in N1.5 is FLARE (Future Latent Representation Alignment) [45], a mechanism that aligns predicted future states with ground truth, significantly enhancing generalization in few-shot scenarios. 

**Training Data and Configuration:** GR00T1.5 is fine- 


Fig. 9: **Visualization of the Model’s Enumeration Behavior under Increased Time Limits.** 

tuned from the GR00T-N1.5-3B checkpoint using min/max normalization for input scaling. Training is performed on a single GPU with a batch size of 32 over 60,000 steps. To optimize memory efficiency and stability, we employ gradient accumulation (4 steps). 

## _D. Scene Design Details_ 

To facilitate the design of more complex and diverse scenarios, we enhance the original LIBERO framework by optimizing core features and expanding the 3D asset library. 

## **(1) Addition of Novel Predicates** 

The original LIBERO [24] determines task success or failure by evaluating object relationships defined by predicates. To support a wider range of tasks, we additionally introduce new predicates to describe object relations, including ExactIn, UprightOn, and SideOn. 


Fig. 10: **Comparison between In and ExactIn.** 

As illustrated in Figure 10, the legacy In logic suffers from imprecise success detection, often flagging a task as complete the moment an object breached the container’s boundary, regardless of stability or depth. This results in frequent false positives where tasks were marked successful before the object was truly contained. 

To rectify this, we introduce the ExactIn predicate. Unlike its predecessor, ExactIn enforces strict containment criteria by calculating the vertical (z-axis) displacement between the object and the container base. The predicate returns true only when this distance falls below a predefined threshold, confirming that the object is fully inserted and resting at the bottom. This mechanism effectively eliminates premature success signals, ensuring robust task evaluation. 


Fig. 11: **Comparison between UprightOn and SideOn.** 

In object placement tasks, accurately determining the posture of objects such as books is essential for successful execution. Unlike objects such as bowls or cups, books can be placed either upright or side-on, providing greater flexibility in placement. To improve posture recognition, we introduce two new predicates, as illustrated in Figure 11. 

For upright placement, the object’s up-vector should be closely aligned with the surface normal. The object is classified as upright when the angle between the up-vector and the surface normal is less than approximately 37°. 

For side-on placement, the object’s up-vector should be nearly perpendicular to the surface normal. The object is classified as side-on when the angle between the up-vector 

and the surface normal is within 17° of perpendicular. 

This enhancement enables more precise posture recognition in object placement tasks, thereby improving task accuracy and system performance in complex environments. It supports reliable execution, particularly in scenarios that require clear differentiation between object postures. 

## **(2) Addition of Novel Objects** 

To increase the diversity of scenes and tasks, we expand the training and testing datasets. The new additions focus on enhancing color, texture, and size diversity, ensuring a broader range of objects for training. Additionally, we make full use of the functional zones of existing objects, such as different shelves in a bookshelf and the various drawers in a cabinet. For the testing dataset, we include objects that are not seen in the training set to assess the model’s generalization ability. 

Table XI presents the frequency of all Predicate, Object, and Container across various scenes and tasks in the training dataset. Table XII provides the corresponding counts for all levels (from level 1 to level 5) in the test dataset. Figure 12 offers a detailed visualization of the data flow relationships between Predicate, Object, and Container. 

TABLE XI: **Predicate, Object and Container Frequency in the Training Set across Scenes and Tasks.** 

|**Name**<br>|**Scene Count**<br>|**Task Count**<br>**Predi**<br>|**Name**<br>**S**<br>**cate**<br>|**cene Count**<br>|**Task Count**<br>|
|---|---|---|---|---|---|
|ExactIn|40|240|On|53|185|
|In|41|116|UprightOn|10|27|
|SideOn|9|25|Close|6|17|
|Open|9|18|Turnon|8|13|
|Turnoff|5|10||||
|||**Obj**<br>|**ect**<br>|||
|yellow book|34|84|black book|29|79|
|red coffee mug|37|77|red book|22|60|
|green bowl|21|56|striped book|24|54|
|black bowl|16|50|orange book|20|50|
|small black bowl|9|29|white yellow mug|23|29|
|green book|14|27|flat stove|13|23|
|frypan|10|21|yellow bowl|9|20|
|white cabinet|5|16|moka pot|10|15|
|blue bowl|5|14|porcelain mug|4|14|
|red bowl|7|13|wooden cabinet|7|12|
|large black bowl|4|10|white bowl|4|9|
|wine bottle|3|8|cream cheese|3|7|
|microwave|3|7|ramekin|1|3|
|||**Conta**<br>|**iner**<br>|||
|desk caddy|20|100|back desk caddy|20|95|
|wooden two layer shelf|21|94|right desk caddy|10|60|
|plate|26|80|bowl drainer|12|51|
|flat stove|16|33|white cabinet|5|14|
|wooden cabinet|4|13|basket|5|11|
|black bowl|4|9|wooden tray|1|6|
|large black bowl|3|8|green bowl|4|6|
|microwave|3|5|wine rack|2|4|
|blue bowl|3|3|small black bowl|2|2|
|wooden shelf|1|2||||


## _E. Visual Attribute Variation Cases Analysis_ 

In this section, we analyze test cases under **Visual Attribute Variation (Level 4)** , focusing on **Confounding Objects (CO)** and **Unseen Objects (UO)** . These cases assess the model’s performance when exposed to variations in object attributes such as color, size, and texture, as well as when encountering objects that were not present in the training data. As shown in Figures 13 and 14, the results presented here are based on tests conducted with the _π_ 0 _._ 5 model. 

TABLE XII: **Predicate, Object and Container Frequency in the Test Set across Scenes and Tasks.** 

|**Name**<br>**S**|**cene Count**|**Task Count**<br>**P**|**Name**<br><br>**redicate**|**Scene Count**|**Task Count**|
|---|---|---|---|---|---|
|ExactIn|211|530|On|238|428|
|In|226|324|SideOn|33|65|
|UprightOn|27|54|Close|23|34|
|Open|27|36|Turnon|21|26|
|Turnoff|15|20||||
||||**Object**|||
|yellow book|34|84|black book|29|79|
|red coffee mug|37|77|black bowl|40|74|
|red book|22|60|green bowl|22|57|
|striped book|24|54|orange book|20|50|
|small black bowl|38|58|flat stove|36|46|
|purple book|43|43|white cabinet|21|32|
|white yellow mug|23|29|navy speckle book|40|40|
|teal wavy book|39|39|green book|14|27|
|light yellow book|40|40|yellow green striped book|39|39|
|white speckle book|38|38|cream cheese|28|32|
|dark grey book|34|34|cyan bowl|33|33|
|cyan grid book|32|32|pink bowl|32|32|
|wooden cabinet|19|24|orange bowl|32|32|
|frypan|10|21|pink wavy book|30|30|
|yellow bowl|9|20|teal bowl|29|29|
|brown grid book|27|27|tomato sauce|26|26|
|dark striped book|25|25|large black bowl|14|20|
|light red book|25|25|small light green bowl|25|25|
|porcelain mug|6|16|moka pot|10|15|
|butter|22|22|popcorn|22|22|
|blue bowl|5|14|alphabet soup|20|20|
|dark orange book|20|20|red bowl|7|13|
|bbq sauce|19|19|chocolate pudding|19|19|
|macaroni and cheese|19|19|ketchup|18|18|
|microwave|10|14|salad dressing|16|16|
|cookies|15|15|orange juice|15|15|
|light green book|14|14|white bowl|4|9|
|milk|13|13|wine bottle|3|8|
|large light red bowl|10|10|small dark yellow bowl|10|10|
|large dark blue bowl|8|8|large light grey bowl|8|8|
|large off white bowl|7|7|ramekin|1|3|
|||**C**|**ontainer**|||
|desk caddy|120|250|desk caddy back|115|229|
|wooden two layer shelf|115|229|plate|106|206|
|desk caddy right|70|150|bowl drainer|63|102|
|flat stove|49|70|wooden cabinet|17|32|
|white cabinet|19|31|basket|16|26|
|wooden tray|7|15|black bowl|13|18|
|large black bowl|11|16|green bowl|10|12|
|microwave|8|10|wine rack|6|8|
|bluebowl|6|6|smallblackbowl|4|4|
|<br>wooden shelf|3|4||||


**Incorrect Target Selection and Environmental Disruption:** The failure cases in Figure 13 (1), (2), and (3) show that when tasked with grabbing confounding objects, the model sometimes initially selects objects that resemble the target rather than the correct target itself. Although the model may later attempt to grasp the intended object, the initial incorrect selection disrupts the environment. These disruptions can alter the scene or occupy the target position, both of which contribute to task failure. This behavior suggests difficulty in distinguishing visually similar objects and maintaining task consistency in complex environments. 

**Instruction Neglect and Target Deviation:** The failure cases in Figure 13 (4) and (5) and Figure 14 (7), (8), and (10) indicate that, despite receiving clear instructions, the model sometimes grasps objects unrelated to the task. It repeatedly attempts to interact with these irrelevant objects and fails to complete the task within the allotted time. This behavior reflects limitations in interpreting task instructions and in aligning them with the correct target object. The model also fails to effectively filter out confounding objects based on task requirements and instead focuses on irrelevant items, demonstrating weaknesses in target recognition and decisionmaking. These failure patterns highlight the need to improve 

instruction following and target selection accuracy. 

**Multi-Step Trajectory Switching and Target Grabbing Difficulties:** As shown in failure case (6) in Figure 14, the model may fail to complete the full task despite successfully executing the initial step. One contributing factor is difficulty in trajectory switching, which prevents smooth transitions between successive steps and disrupts task execution. In addition, the target object may become harder to grasp in later stages or may be misidentified due to environmental interference. These factors cause the model to perform adequately in early subtasks but ultimately fail to complete the multi-step task. This behavior indicates that, while the model can handle localized actions, it struggles with global task continuity. Improving overall planning and execution in multi-step scenarios, particularly ensuring effective transitions between steps, is therefore essential for enhancing performance. 

## _F. Semantic-Equivalent Reformulation Cases_ 

As shown in Table XIII, **Semantic-Equivalent Reformulation (Level 5)** evaluates robustness to variations in task descriptions. The applied modification strategies include **synonym replacement (L5-1)** , which substitutes phrases using a synonym mapping table while maintaining the original meaning; **word compression (L5-2)** , which removes redundant elements such as auxiliary verbs and articles to retain only the core semantics; **word order adjustment (L5-3)** , which changes sentence structure without affecting meaning; **voice conversion (L5-4)** , which transforms imperative sentences into the passive voice; and **redundant descriptions (L5-5)** , which add supplementary phrases at the beginning or end of instructions to enhance clarity or emphasis. 

TABLE XIII: **Example of Semantic-Equivalent Reformulation (Level 5).** 

|**level5**|**Converted**|**Example**|
|---|---|---|
|**5-1**|Original|_Place the pink bowl on the plate._|
||Converted|_Lay down the pink soup bowl over the serving plate._|
|**5-2**|Original|_Place the left dark grey book into the left desk caddy’s back compartment._|
||Converted|_left dark grey book into left caddy back_|
|**5-3**|Original|_Place the small dark yellow bowl on top of the wooden cabinet._|
||Converted|_On top of the wooden cabinet, place the small dark yellow bowl._|
|**5-4**|Original|_Place the navy speckle book in the top region of the shelf._|
||Converted|_The navy speckle book should be placed in the top region of the shelf_|
||Original|_Place the small light green bowl on the plate._|
|**5-5**|Converted|_In this scene, the goal is to place the small light green bowl on the plate,_<br>_no additional actions are required._|


Fig. 12: **Sankey Diagram of the Flow between Predicate, Object, and Container.** 


Fig. 13: **Visualization of Test Samples with Confounding Objects (CO) under Visual Attribute Variation (Level 4).** 


Fig. 14: **Visualization of Test Samples with Unseen Objects (UO) under Visual Attribute Variation (Level 4).** 

