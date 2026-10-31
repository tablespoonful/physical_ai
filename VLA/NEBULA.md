---
title: "NEBULA: Do We Evaluate Vision-Language-Action Agents Correctly?"
date: "2025-10-17"
authors: "Jierui Peng; Yanyan Zhang; Yicheng Duan; Tuo Liang; Vipin Chaudhary; Yu Yin"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2510.16263
pdf: https://arxiv.org/pdf/2510.16263
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.16263)** / [論文ページ](https://arxiv.org/abs/2510.16263)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

NEBULA: DO WE EVALUATE VISION-LANGUAGEACTION AGENTS CORRECTLY? 

**Jierui Peng**<sup>_∗_</sup> **, Yanyan Zhang**<sup>_∗_</sup> **, Yicheng Duan**<sup>_∗_</sup> **, Tuo Liang, Vipin Chaudhary, Yu Yin**<sup>_†_</sup> Department of Computer & Data Sciences Case Western Reserve University 

_{_ jierui.peng,yanyan.zhang,yicheng.duan,tuo.liang,vipin,yu.yin _}_ @case.edu 

Homepage: https://vulab-ai.github.io/NEBULA-Alpha/ 

# ABSTRACT 

The evaluation of Vision-Language-Action (VLA) agents is hindered by the coarse, end-task success metric that fails to provide precise skill diagnosis or measure robustness to real-world perturbations. This challenge is exacerbated by a fragmented data landscape that impedes reproducible research and the development of generalist models. To address these limitations, we introduce **NEBULA** , a unified ecosystem for single-arm manipulation that enables diagnostic and reproducible evaluation. NEBULA features a novel dual-axis evaluation protocol that combines fine-grained _capability tests_ for precise skill diagnosis with systematic _stress tests_ that measure robustness. A standardized API and a large-scale, aggregated dataset are provided to reduce fragmentation and support cross-dataset training and fair comparison. Using NEBULA, we demonstrate that top-performing VLAs struggle with key capabilities such as spatial reasoning and dynamic adaptation, which are consistently obscured by conventional end-task success metrics. By measuring both what an agent can do and when it does so reliably, NEBULA provides a practical foundation for robust, general-purpose embodied agents. 

# 1 INTRODUCTION 

Vision–Language–Action (VLA) agents are advancing rapidly, spanning language-conditioned planners, generalist multi-modal agents, and prompt-conditioned manipulation policies (Brohan et al., 2023; Zitkovich et al., 2023; Jiang et al., 2022). Yet a basic question remains: _are we evaluating what actually matters?_ Most benchmarks tend to prioritize end-task success, a coarse metric that neither reveals which subskills are engaged nor localizes error sources. For example, a failure on “pick-and-place” may arise from language grounding, 3D perception, spatial planning, or control. However, a single success rate cannot identify the failing component. Without capability-resolved, diagnostic evaluation, we cannot measure per-skill capability and expose where and why agents fail. 

Even with precise skill diagnosis, current evaluation overlooks a second deployment-critical dimension: reliability. Passing a test at a single operating point does not imply robustness, nor does it reflect key properties needed for deployment ( _e.g.,_ latency, stability, robustness). Small, realistic shifts in conditions ( _e.g.,_ lighting, textures, phrasing, dynamics, sensor noise) can flip outcomes, while aggregate success rates often hide variability across settings and mask abrupt breakdowns (‘failure cliffs’). Because real-world conditions continually shift along these dimensions, stress tests are needed to characterize reliability boundaries and disentangle competence from robustness. 

Meanwhile, this dual challenge of diagnostic and robust evaluation is compounded by a severely fragmented data landscape. Datasets like ManiSkill (Mu et al., 2021), LeRobot (Cadene et al., 2024), and BEHAVIOR-1k (Li et al., 2023) differ drastically in format, task representation, and embodiment. Even efforts like Open-X (Collaboration et al., 2023), which propose shared interfaces, fall short in defining what capabilities are tested or how to compare them. This fragmentation forces 

> _∗_ Equal contribution. 

> _†_ Corresponding Author 

1 


Figure 1: **NEBULA Ecosystem** unifies fragmented VLA datasets and APIs for cross-dataset training and benchmarking. It introduces a dual-axis evaluation (capability and stress testing) with controlled variable isolation for skill-specific diagnosis. With hierarchical task difficulty, multi-modal annotations, and visual performance summaries, NEBULA converts success rate into a diagnostic signal, exposing failure modes and reliability limits. 

researchers to reimplement pipelines, prevents fair head-to-head comparisons, and limits large-scale generalization studies, which slows progress toward unified embodied intelligence. As a result, the field lacks a unified ecosystem that can simultaneously diagnose agent capabilities, stress-test their robustness, and unify disparate data sources for reproducible, scalable research. 

To address these challenges, we introduce **NEBULA** , an integrated ecosystem designed to shift the focus of embodied AI research from simple task completion to true capability mastery. The ecosystem is built on two core pillars. The first is a **diagnostic evaluation framework** that transforms coarse success rates into an interpretable, multi-faceted signal. It directly confronts the issues of disentangled capability evaluation and reliability by combining: (1) **Capability Tests** , which isolate specific skills like spatial reasoning and grasp synthesis to pinpoint precise reasons for failure, and (2) **Stress Tests** , which systematically vary environmental conditions to map an agent’s robustness and identify hidden failure cliffs. This dual-axis approach provides a holistic view of an agent’s competence, revealing not only what it can do but also the conditions under which it can be trusted. 

Complementing its evaluation suite, NEBULA’s second pillar tackles the critical issue of **data and tooling fragmentation** . We provide a standardized API and data format that unifies disparate benchmarks, including ManiSkill, LeRobot, and others, eliminating the need for engineering work for each new dataset. We also provide a large-scale, aggregated dataset that integrates existing realworld demonstrations, simulator-generated trajectories, and world-model–augmented data. By providing the infrastructure for both unified training and reproducible evaluation, NEBULA empowers researchers to build more generalizable agents and conduct fair, large-scale comparisons that accelerate scientific progress. In summary, the key contributions of our paper include: 

- We introduce **NEBULA** , a unified VLA ecosystem that provides a standardized API and a largescale, aggregated dataset to facilitate reproducible, cross-dataset training and benchmarking. 

- We propose a novel **dual-axis evaluation protocol** that combines fine-grained _capability tests_ for precise skill diagnosis with systematic _stress tests_ to measure an agent’s robustness against real-world perturbations. 

- We present an **in-depth benchmarking study** of current VLAs, revealing critical failure modes ( _e.g.,_ spatial reasoning) that are typically obscured by the traditional success rate metric. 

2 

# 2 RELATED WORKS 

## 2.1 SINGLE-ARM MANIPULATION BENCHMARKS & SIMULATORS 

The landscape of robotic manipulation evaluation has expanded significantly in recent years, yet fundamental questions about what and how we measure remain unresolved. Existing efforts cluster into three threads: (i) **Single-arm tabletop benchmarks** , such as RLBench (James et al., 2020), BulletArm (Wang et al., 2022), ManiSkill2 (Gu et al., 2023), and ManiSkill3 (Tao et al., 2024), provide diverse task libraries, multimodal observations, and extensions toward bimanual, languageconditioned manipulation. (ii) **Long-horizon benchmarks** , such as BEHAVIOR-1K (Li et al., 2023), Meta-World (Yu et al., 2020), ALFRED (Shridhar et al., 2020), FurnitureBench (Heo et al., 2023), Franka Kitchen (Gupta et al., 2019), LIBERO (Liu et al., 2023), CALVIN (Mees et al., 2022), VLABench (Zhang et al., 2024), and MIKASA-Robo (Cherepanov et al., 2025), highlight multi-skill acquisition, temporal reasoning across extended tasks, and memory-centric challenges under partial observability. (ii) **Realism-focused platforms** , such as SIMPLER (Li et al., 2024), Habitat (Savva et al., 2019), SAPIEN (Xiang et al., 2020), THE COLOSSEUM (Pumacay et al., 2024), and Genesis (Authors, 2024), advance physics fidelity and enable evaluation under controlled perturbations and language-conditioned tasks. 

Despite these advances, evaluation in most benchmarks still relies heavily on task-level success rate. While useful for model comparison and easy to compute, these metrics have limited diagnostic value: they indicate neither which abilities failed nor why. Our framework addresses this gap through a dual-axis evaluation that disentangles task requirements from performance quality, enabling structured and interpretable diagnosis. 

## 2.2 EVALUATION PROTOCOLS & METRICS 

Separating sources of failure is essential for evaluating VLA models in robotic manipulation, particularly as tasks grow more complex and as the demand for stronger generalization increases. THE COLOSSEUM (Pumacay et al., 2024) systematically perturbs tasks along controlled axes and reports robustness degradation. VLABench (Zhang et al., 2024) divides evaluation into six high-level capability dimensions to assess models more explicitly. RAMP (Robotic Assembly Manipulation and Planning) (Collins et al., 2023) introduces long-horizon assembly scenarios that challenge reasoning, diagnostics, and fault recovery in addition to pure control and perception. Meanwhile, Robot Policy Evaluation for Sim-to-Real Transfer (Yang et al., 2025) proposes benchmarking strategies that gradually increase task complexity and introduce scenario perturbations to assess robustness and alignment between simulation and real-world performance. Also, Recent surveys on VLA models emphasize the need for evaluation across the full perception–language–control pipeline, combining task success with metrics for generalization, robustness, and instruction understanding (Ma et al., 2024; Shao et al., 2025; Sapkota et al., 2025). Our work builds on the idea of evaluating intelligence across multiple dimensions, and further enforces protocols that disentangle task specifications from execution performance via controlled variation and progressively increasing difficulty. 

# 3 NEBULA ECOSYSTEM 

NEBULA is a unified and comprehensive ecosystem built to overcome critical limitations in existing Embodied AI pipelines. While traditional systems often reduce evaluation to coarse metrics like task success or runtime, NEBULA broadens the scope to answer a deeper question: _how and why does an agent succeed or fail?_ As shown in Figure 1, NEBULA provides a structured, modular framework that includes 1) a standardized data layer with a unified format and APIs to enable cross-task training and reuse; 2) a dual-axis evaluation protocol for disentangling functional capabilities from realtime robustness; and 3) rich diagnostic outputs to support interpretable, skill-specific performance analysis. This section introduces NEBULA’s core design. Section 3.1 details our data collection protocol and unified API design, while Section 3.2 outlines NEBULA’s evaluation framework and the design of its capability and stress test tasks. 

3 

## 3.1 DATA & API SPECIFICATION 

**Data Collection & Annotation.** To ensure consistency and reproducibility, NEBULA collects all training and evaluation data using a customized simulation platform built upon the SAPIEN (Xiang et al., 2020) engine and the ManiSkill3 (Tao et al., 2024) framework. For each manipulation episode, we record a temporally ordered sequence of multimodal observations _Ot_ , system states _St_ , actions _At_ , and binary success labels _SU t ∈_ 0 _,_ 1 at each timestep _t_ . The observations _Ot_ include RGB, depth, and segmentation images from six fixed-viewpoint cameras, as well as proprioceptive inputs such as joint positions _qt_ and velocities _q_ ˜ _t_ . Each episode is annotated with a natural language task instruction, manually written to reflect the intended goal. These instructions serve as the conditioning input for language-conditioned policies and allow precise alignment between episodes and their semantic objectives. NEBULA offers two dataset variants, Alpha and Beta, designed to balance completeness and usability. For data collection, the Alpha version of the dataset is entirely generated using expert trajectories produced via motion planning (LaValle, 2006). In contrast, the Beta version combines motion planning with human teleoperation: for selected hard tasks, expert demonstrations are collected manually to capture more diverse and realistic behaviors. 

**API & Modulated Assets.** To ensure consistency and ease of use across heterogeneous data sources, we introduce a unified data schema that consolidates fields found in modern embodied datasets. This schema standardizes the representation of observations, actions, environment states, and task metadata under a common structure, enabling plug-and-play compatibility with a wide range of learning algorithms. We provide a PyTorch API that abstracts away the low-level data loading and indexing details, exposing a clean, task-agnostic interface for pipeline. For researchers working in the TensorFlow ecosystem, we additionally provide lightweight TF-compatible adapters. To further reduce integration overhead, we include model-specific adapters for several widely used architectures, allowing for immediate benchmarking on NEBULA data with minimal code changes. Please refer to Appendix A.1 for detailed information. 

**Dataset Statistics.** NEBULA offers two dataset Table 1: Dataset statistics variants—Alpha and Beta—for both full-scale across five task families, excluding Robustness. evaluation and lightweight experimentation. As Task shown in Table 1, Alpha includes over 54,000 exFamilies pert demonstrations across five capability famiVideos lies, while Beta is a compact version ( 10% per Control 54,000 task) designed for rapid development and ablaPerception 54,000 tion. Some high-difficulty Beta tasks use huLanguage 48,000 man teleoperation to introduce realistic variaDynamic 36,000 tions. Both datasets provide multimodal inputs Spatial 30,000 (videos, language, trajectories) in PyTorch and Robust N/A TFRecord formats with adapter support. The RoTotal 222,000 bustness and Generalization family is reserved for evaluation only and excluded from both training sets to prevent overfitting and ensure fair comparison under distribution shift. 

Table 1: Dataset statistics of NEBULA-Alpha across five task families, excluding Robustness. 

|Task<br>||Alpha||
|---|---|---|---|
|Families|Videos|Descriptions|Traj|
|Control|54,000|9|36,000|
|Perception|54,000|9,000|36,000|
|Language|48,000|24,000|96,000|
|Dynamic|36,000|6|24,000|
|Spatial|30,000|5,000|24,000|
|Robust|N/A|N/A|N/A|
|Total|222,000|38,015|216,000|


## 3.2 DUAL-AXIS EVALUATION FRAMEWORK 

NEBULA introduces a dual-axis evaluation framework to enable structured, interpretable, and diagnostic assessment of embodied AI systems. This framework decouples the evaluation into two dimensions: **Capability** and **Stress Tests** , each isolating a distinct facet of system performance. The Capability axis evaluates _what the agent can do_ under nominal conditions. The Stress axis probes _how well the agent operates_ under varying levels of real-time or robustness-related pressure. 

## 3.2.1 CAPABILITY TEST TASKS 

NEBULA’s Capability Tests isolate six core embodied skills or capabilities through a suite of procedurally generated tasks. Our evaluation methodology is built on two key principles: _(i) ControlledVariable Isolation_ : Each task is designed to vary a single capability dimension while holding others constant, ensuring that performance changes can be unambiguously attributed to the skill being tested. For example, perception tasks minimize control complexity, while control tasks use fixed visual scenes. _(ii) Systematic Difficulty Scaling_ : Within each family, tasks are generated from pa- 

4 


Figure 2: **Examples of NEBULA Capability Test task** across six core capabilities (Control, Perception, Dynamic Adaptation, Language, Spatial Reasoning, and Robustness) organized into three difficulty levels. Tasks isolate specific skills with controlled complexity. Green marks objects, red marks targets, and blue indicates contextual cues. **Bold underlined** text shows actions; _italic underlined_ text gives clarifications. 

rameterized templates into three tiers (Easy, Medium, Hard), allowing for a fine-grained analysis of an agent’s limits. This modular structure enables reproducible, fine-grained evaluation of the following capabilities (see Fig. 2 and Appendix A.2.1): 

- (1) **_Control_ :** The Control task family isolates low-level manipulation by fixing non-control factors, with tasks progressing from simple actions (Easy) to precise, multi-step sequences (Hard). 

- (2) **_Perception_ :** The Perception task family isolates visual recognition by minimizing control demands, with difficulty scaling from clear distinctions to subtle differences and cluttered scenes. 

- (3) **_Language_ :** The Language task family tests instruction understanding, from basic grounding to reasoning and conditionals, with fixed scenes to isolate linguistic skills. 

- (4) **_Dynamic Adaptation_ :** This task family evaluates how well an agent adapts to dynamic changes, from object attribute switching (Easy) to predictable moving (Medium) and unpredictable realtime events (Hard), testing reactivity and robustness. 

- (5) **_Spatial Reasoning_ :** The Spatial task family tests spatial reasoning from 2D placement to 6-DoF planning, with difficulty scaling from planar to full 3D geometric understanding. 

- (6) **_Robustness/Generalization_ :** The Robustness task family assesses generalization under distribution shifts, from distractors to unseen attributes to novel scenes. 

## 3.2.2 STRESS TEST TASKS 

To complement capability-based evaluations, NEBULA introduces a suite of Stress Tests ( _Inference Frequency_ , _Latency_ , _Stability Score_ , and _Adaptation_ ) that isolate and quantify system performance under targeted operational constraints. Each test is a single-indicator probe. These tests avoid confounding variables and support controlled ablation studies by being independently applied. Each is instantiated at three calibrated pressure levels ( _v_ 1– _v_ 3), defined by measurable parameters normal- 

5 


Figure 3: **Capability Radar Chart.** This figure presents a radar plot comparing the performance of evaluated policies across six core capability families in NEBULA: Perception, Control, Language, Spatial Reasoning, Dynamic Adaptation, and Robustness. Each axis shows the averaged success rate across task variants in each difficulty level. Higher values toward the outer edge indicate stronger performance in the isolated skill. The visualization reveals distinct strength–weakness profiles across models, highlighting complementary capabilities and critical failure modes. 

ized to baseline conditions. This structure enables detailed stress-response profiling and fair comparisons across systems, helping identify bottlenecks and guide robustness optimization for real-world deployment. Full test definitions appear in Appendix A.2.2. 

- (1) **_Inference Frequency_ :** This test measures action rate to assess real-time responsiveness, with increasing motion complexity exposing inference speed limits. 

- (2) **_Latency_ :** This measures the delay from perception to action. Three tiers introduce increasing scene dynamics to responsiveness. Low latency is essential for precise, time-sensitive manipulation. 

- (3) **_Stability Score_ :** Stability quantifies action smoothness by measuring action variation between consecutive timesteps given an action sequence _{a_ 0 _, a_ 1 _, ..., at}_ : 


where _|| ||_ 2 represents the _L_ 2 nortm and higher scores ( _∈_ [0 _,_ 1]) indicate smoother trajectories. Tests progress from coarse force control ( _v_ 1) to precise, contact-rich manipulation ( _v_ 3), revealing whether policies produce stable outputs suitable for deployment. 

- (4) **_Adaptability_ :** Adaptability tests how well agents adjust to changing goals, from target shifts to instruction switches and rapid re-planning, revealing robustness under dynamic conditions. 

# 4 EXPERIMENTS 

To demonstrate the utility, coverage, and diagnostic strength of the NEBULA benchmark, we conduct comprehensive experiments across both capability and stress axes. These evaluations aim to answer several core questions: _Can current embodied agents handle a wide range of skills? Where_ 

6 


Figure 4: This figure presents two radar charts summarizing model performance across six capability task families. The **left** chart shows the mean _±_ standard deviation of success rates across all models for each task family at three difficulty levels. The **right** chart displays the average performance of individual models on Easy and Medium tasks, allowing for comparison across architectures. 

_do they fail under specific challenges?_ And _how can structured benchmarks help improve their design?_ All experiments are conducted using the Alpha dataset to ensure consistency and reproducibility across tasks and conditions. This section focuses on the evaluated models (Section 4.1) and their performance under the dual-axis evaluation framework (Section 4.2 and Section 4.3). 

## 4.1 BASELINES 

We evaluate a diverse set of state-of-the-art embodied agents to benchmark performance across NEBULA’s evaluation framework. Specifically, we include GR00T-1.5 (Bjorck et al., 2025), SpatialVLA (Qu et al., 2025), RDT-1B (Liu et al., 2024), MT-ACT (Bharadhwaj et al., 2024), Diffusion Policy (Chi et al., 2023), and ACT (Zhao et al., 2023), which together represent a wide spectrum of architectural designs and control paradigms. For fair comparison, we unify data loading to match NEBULA’s format, keeping each model’s architecture, loss, and hyperparameters unchanged. All models are fine-tuned on NEBULA Alpha using their original training protocols. 

## 4.2 CAPABILITY TEST RESULTS 

As shown in Figure 3 and the left chart from Figure 4, the radar chart reveals several key trends in agent capabilities. Most models demonstrate strong performance in _Perception_ and _Language_ tasks. Nearly all baselines reliably identify object attributes like color and shape, even with distractors, indicating robust visual recognition. Similarly, these agents exhibit solid instruction grounding, successfully executing complex, conditional, and multi-step commands. 

Performance on _Control_ and _Spatial_ tasks is more varied. SpatialVLA and GR00T-1.5 lead in _Control_ , handling long-horizon action sequences with high success. However, models like MT-ACT and ACT lag behind, revealing a need for better motor planning modules. _Spatial reasoning_ remains a key bottleneck for most models, with only SpatialVLA and RDT-1B achieving moderate success. Notably, even these models show clear drops from easy to medium level, especially under occlusion and containment conditions, indicating significant room for improvement in geometric reasoning. 

All models struggle on _Dynamic Adaptation_ and _Robustness_ tasks, as shown in Figure 4. None of the evaluated VLA systems reliably adapts to time-sensitive triggers, distractors, or goal shifts, with radar scores near zero across the board. Similarly, robustness to distribution shifts( _e.g.,_ novel object appearances, unseen layouts) is consistently poor, especially at higher difficulty levels. These 

7 


Figure 5: **Stress Test Evaluations.** This figure compares four models across three stress levels ( _v_ 1, _v_ 2, _v_ 3), evaluating inference frequency (Hz), latency (ms), stability score (0–1), and adaptability. Higher values indicate better performance for all metrics except latency, where lower is preferred. 

results expose a major gap in current VLA capabilities and highlight two urgent research directions: real-time adaptive planning and out-of-distribution generalization. 

We exclude the Hard level from the right radar chart in Figure 4 because most models exhibit nearzero performance at this difficulty tier, especially in tasks involving robustness and dynamic adaptation. By focusing on Easy and Medium tasks, the chart provides clearer insights into current model capabilities. We hope this visualization encourages future research to close the gap at the Hard level, ultimately enabling more capable and resilient VLA systems. 

## 4.3 STRESS TEST RESULTS 

As shown in Figure 5, all evaluated models exhibit consistent performance degradation as stress levels increase, revealing sensitivity to deployment-time challenges such as computational bottlenecks and real-time demands. Inference frequency shows a clear decline across models: GR00T-1.5B remains the most resilient, maintaining 17 _Hz_ under _v_ 3, while DP and SpatialVLA fall below 2 _Hz_ . This suggests many models struggle to meet real-time requirements under stress, and performance in ideal conditions may not generalize to practical deployment. 

Latency results mirror this trend: with rising pressure, most models exhibit notable increases in response delay. Particularly, DP shows significant latency inflation, with its average step time nearly quadrupling from _v_ 1 to _v_ 3, peaking at around 800ms. This is indicative of inefficient model behavior under strain, potentially caused by unstable sampling mechanisms or computation-heavy policy architectures. In comparison, models like GR00T and RDT show slower rates of degradation, maintaining sub-300ms latency even under _v_ 3. These observations collectively highlight a key bottleneck for real-world deployment, where maintaining both throughput and response time is essential for safe and effective robot operation. 

The stability score, measuring the smoothness of action trajectories (1.0 indicates perfect stability), also reveals growing fragility under stress. While RDT and DP maintain high scores above 0.95, SpatialVLA drops from 0.96 to 0.86 under _v_ 3, suggesting vulnerabilities in policy determinism. This decline may stem from increased decision-making stochasticity or sensitivity to input noise, leading to unreliable behaviors in dynamic scenarios where smooth, precise motion is essential. 

Finally, the Adaptability results demonstrate that most current models are unable to handle dynamically evolving conditions. Except for GR00T, which shows modest success under adaptive task settings, all other models fail almost completely, with near-zero success rates across stress levels. This indicates a fundamental limitation in current VLA systems when faced with shifting goals, interactive feedback, or rapid environmental changes. 

8 

## 4.4 VALIDITY OF FACTOR ISOLATION 

Table 2: Success rates of GR00T-1.5 on three Perception (Easy level) tasks, comparing settings with isolated factors versus unisolated scenes with additional distractors. Results highlight the im- <u>pact of scene confounding on perceptual accuracy.act of scene confounding on perceptual accuracy.</u> 

We validate NEBULA’s factor isolation by Table 2: Success rates of comparing perception tasks in isolated vs. enPerception (Easy level) tasks, tangled settings. In isolation, the robot only with isolated factors versus unisolated scenes with needs to touch the correct object using simadditional distractors. Results ple language; in contrast, the entangled base- <u>pact of scene confounding on perceptual accuracy.act of scene confounding on perceptual accuracy.</u> line requires full grasp-and-place execution involving multiple skills. As shown in Table 2, GR00T-1.5B achieves 100% success in isolated Isolated PlaceBigger settings, but drops to 92%, 68%, and 76% when Factors Sphere entangled. Video review shows failures are due ✓ 100 to control and 3D spatial reasoning errors, high✗ 92 lighting how unrelated bottlenecks can obscure perception performance and validating NEBULA’s controlled-variable design. 

||Percepti|on (Easy Level)|
|---|---|---|
|Isolated|PlaceBigger|Place<br>Place|
|Factors|Sphere|Red Sphere<br>Sphere|
|✓|100|100<br>100|
|✗|92|68<br>76|


# 5 DISCUSSION 

## 5.1 WHY ARE GENERALIZATION AND DYNAMIC PERFORMANCE POOR? 

To investigate why embodied agents struggle with generalization and dynamics, we decoupled the visionlanguage backbone from action head. Using SpatialVLA and GR00T’s VLMs, we prompted high-level plans from static NEBULA scenes and had human annotators assess their validity. 

As shown in Table 3, the standalone VLMs produce consistently valid strategies even in robustness tasks. However, their integrated VLA counterparts fail to execute these plans, with success rates dropping to zero under even moderate difficulty. This highlights a critical bottleneck: strong reasoning from VLMs does not guarantee successful embodied behavior, due to limitations in the action heads’ ability to translate abstract plans into precise control actions. 

Table 3: Success rates of different models on Robustness tasks, used to evaluate whether performance drop stems from high-level planning or low-level execution failures. 

|Model|Robust/Gen|eralization|
|---|---|---|
||Easy<br>StackCube|Medium<br>StackCube|
|PaliGemma|85|75|
|SpatialVLA|0|0|
|Qwen|100|90|
|GR00T-1.5|75|0|


This issue is compounded by the inadequacy of conventional benchmarks that rely solely on success rate, obscuring whether failures arise from perception, reasoning, or control. NEBULA’s dualaxis evaluation addresses this by disentangling high-level reasoning from low-level execution and surfacing weaknesses under stress, offering the diagnostic granularity needed to build more robust and generalizable embodied systems. 

## 5.2 FAST INFERENCE IS KEY TO DYNAMIC ADAPTATION 

As shown in the Capability Test (Figure 4), nearly all models fail to handle Dynamic tasks. To further investigate this weakness, we introduced an Adaptation Stress Test to simulate dynamic environments and evaluate model robustness under goal shifts and real-time disruptions. Table 4 compares inference frequency, latency, and adaptation success across models to help uncover underlying causes. 

Table 4: Comparison of inference speed, latency, and adaptation score across models. Only GR00T1.5 demonstrates meaningful adaptation, likely due to its significantly lower latency and higher inference frequency. 

|Model|Avg.<br>Inference<br>Frequency|Avg.<br>Latency|Avg.<br>Adaptation|
|---|---|---|---|
|GR00T-1.5|16.98 Hz|58.62 ms|28|
|RDT-1B|4.84 Hz|206.77 ms|1|
|SpatialVLA|1.92 Hz|520.48 ms|0|


Results show that GR00T-1.5 is the only model RDT-1B 4.84 Hz 206.77 ms 1 with moderate adaptation (success rate = 28), SpatialVLA 1.92 Hz 520.48 ms 0 while RDT-1B and SpatialVLA perform poorly. GR00T-1.5 also demonstrates the fastest response—16.98 Hz inference frequency and 58.62 ms latency—whereas slower models show little adaptive behavior. This suggests that fast perception and replanning are crucial for dynamic environments. 

9 

Overall, these findings highlight a critical bottleneck: real-time adaptation requires not only highlevel reasoning but also fast, low-latency control pipelines. Future work should focus on optimizing system responsiveness—especially in the action head—to enable effective online replanning and robust behavior under dynamic conditions. 

# 6 CONCLUSION 

In this work, we introduced NEBULA, an evaluation-first ecosystem that unifies fragmented data formats and establishes a dual-axis framework for embodied AI. By disentangling capability tests from stress tests and enforcing controlled-variable isolation, NEBULA provides interpretable, skillspecific, and robust performance diagnostics that go beyond conventional success rates. Our experiments demonstrate how this design reveals hidden bottlenecks, clarifies model strengths and weaknesses, and lays the foundation for systematic progress toward reliable VLA agents. 

10 

# REFERENCES 

- Genesis Authors. Genesis: A generative and universal physics engine for robotics and beyond, December 2024. URL https://github.com/Genesis-Embodied-AI/Genesis. 

- Homanga Bharadhwaj, Jay Vakil, Mohit Sharma, Abhinav Gupta, Shubham Tulsiani, and Vikash Kumar. Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 4788–4795. IEEE, 2024. 

- Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Anthony Brohan, Yevgen Chebotar, Chelsea Finn, Karol Hausman, Alexander Herzog, Daniel Ho, Julian Ibarz, Alex Irpan, Eric Jang, Ryan Julian, et al. Do as i can, not as i say: Grounding language in robotic affordances. In _Conference on robot learning_ , pp. 287–318. PMLR, 2023. 

- Remi Cadene, Simon Alibert, Alexander Soare, Quentin Gallouedec, Adil Zouitine, Steven Palma, Pepijn Kooijmans, Michel Aractingi, Mustafa Shukor, Dana Aubakirova, Martino Russi, Francesco Capuano, Caroline Pascal, Jade Choghari, Jess Moss, and Thomas Wolf. Lerobot: State-of-the-art machine learning for real-world robotics in pytorch. https://github.com/ huggingface/lerobot, 2024. 

- Egor Cherepanov, Nikita Kachaev, Alexey K. Kovalev, and Aleksandr I. Panov. Memory, benchmark & robots: A benchmark for solving complex tasks with reinforcement learning, 2025. URL https://arxiv.org/abs/2502.10550. 

- Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , pp. 02783649241273668, 2023. 

- Open X-Embodiment Collaboration, Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, Albert Tung, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anchit Gupta, Andrew Wang, Andrey Kolobov, Anikait Singh, Animesh Garg, Aniruddha Kembhavi, Annie Xie, Anthony Brohan, Antonin Raffin, Archit Sharma, Arefeh Yavary, Arhan Jain, Ashwin Balakrishna, Ayzaan Wahid, Ben Burgess-Limerick, Beomjoon Kim, Bernhard Sch¨olkopf, Blake Wulfe, Brian Ichter, Cewu Lu, Charles Xu, Charlotte Le, Chelsea Finn, Chen Wang, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine Chan, Christopher Agia, Chuer Pan, Chuyuan Fu, Coline Devin, Danfei Xu, Daniel Morton, Danny Driess, Daphne Chen, Deepak Pathak, Dhruv Shah, Dieter B¨uchler, Dinesh Jayaraman, Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Ethan Foster, Fangchen Liu, Federico Ceola, Fei Xia, Feiyu Zhao, Felipe Vieira Frujeri, Freek Stulp, Gaoyue Zhou, Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Gilbert Feng, Giulio Schiavi, Glen Berseth, Gregory Kahn, Guangwen Yang, Guanzhi Wang, Hao Su, Hao-Shu Fang, Haochen Shi, Henghui Bao, Heni Ben Amor, Henrik I Christensen, Hiroki Furuta, Homanga Bharadhwaj, Homer Walke, Hongjie Fang, Huy Ha, Igor Mordatch, Ilija Radosavovic, Isabel Leal, Jacky Liang, Jad Abou-Chakra, Jaehyung Kim, Jaimyn Drake, Jan Peters, Jan Schneider, Jasmine Hsu, Jay Vakil, Jeannette Bohg, Jeffrey Bingham, Jeffrey Wu, Jensen Gao, Jiaheng Hu, Jiajun Wu, Jialin Wu, Jiankai Sun, Jianlan Luo, Jiayuan Gu, Jie Tan, Jihoon Oh, Jimmy Wu, Jingpei Lu, Jingyun Yang, Jitendra Malik, Jo˜ao Silv´erio, Joey Hejna, Jonathan Booher, Jonathan Tompson, Jonathan Yang, Jordi Salvador, Joseph J. Lim, Junhyek Han, Kaiyuan Wang, Kanishka Rao, Karl Pertsch, Karol Hausman, Keegan Go, Keerthana Gopalakrishnan, Ken Goldberg, Kendra Byrne, Kenneth Oslund, Kento Kawaharazuka, Kevin Black, Kevin Lin, Kevin Zhang, Kiana Ehsani, Kiran Lekkala, Kirsty Ellis, Krishan Rana, Krishnan Srinivasan, Kuan Fang, Kunal Pratap Singh, Kuo-Hao Zeng, Kyle Hatch, Kyle Hsu, Laurent Itti, Lawrence Yunliang Chen, Lerrel Pinto, Li Fei-Fei, Liam Tan, Linxi ”Jim” Fan, Lionel Ott, Lisa Lee, Luca Weihs, Magnum Chen, Marion Lepert, Marius Memmel, Masayoshi Tomizuka, Masha Itkina, Mateo Guaman Castro, Max Spero, Maximilian Du, Michael Ahn, Michael C. Yip, Mingtong Zhang, Mingyu Ding, Minho Heo, Mohan Kumar Srirama, Mohit Sharma, Moo Jin Kim, Muhammad Zubair Irshad, Naoaki Kanazawa, Nicklas Hansen, Nicolas Heess, Nikhil J 

11 

Joshi, Niko Suenderhauf, Ning Liu, Norman Di Palo, Nur Muhammad Mahi Shafiullah, Oier Mees, Oliver Kroemer, Osbert Bastani, Pannag R Sanketi, Patrick ”Tree” Miller, Patrick Yin, Paul Wohlhart, Peng Xu, Peter David Fagan, Peter Mitrano, Pierre Sermanet, Pieter Abbeel, Priya Sundaresan, Qiuyu Chen, Quan Vuong, Rafael Rafailov, Ran Tian, Ria Doshi, Roberto Mart’in-Mart’in, Rohan Baijal, Rosario Scalise, Rose Hendrix, Roy Lin, Runjia Qian, Ruohan Zhang, Russell Mendonca, Rutav Shah, Ryan Hoque, Ryan Julian, Samuel Bustamante, Sean Kirmani, Sergey Levine, Shan Lin, Sherry Moore, Shikhar Bahl, Shivin Dass, Shubham Sonawani, Shubham Tulsiani, Shuran Song, Sichun Xu, Siddhant Haldar, Siddharth Karamcheti, Simeon Adebola, Simon Guist, Soroush Nasiriany, Stefan Schaal, Stefan Welker, Stephen Tian, Subramanian Ramamoorthy, Sudeep Dasari, Suneel Belkhale, Sungjae Park, Suraj Nair, Suvir Mirchandani, Takayuki Osa, Tanmay Gupta, Tatsuya Harada, Tatsuya Matsushima, Ted Xiao, Thomas Kollar, Tianhe Yu, Tianli Ding, Todor Davchev, Tony Z. Zhao, Travis Armstrong, Trevor Darrell, Trinity Chung, Vidhi Jain, Vikash Kumar, Vincent Vanhoucke, Vitor Guizilini, Wei Zhan, Wenxuan Zhou, Wolfram Burgard, Xi Chen, Xiangyu Chen, Xiaolong Wang, Xinghao Zhu, Xinyang Geng, Xiyuan Liu, Xu Liangwei, Xuanlin Li, Yansong Pang, Yao Lu, Yecheng Jason Ma, Yejin Kim, Yevgen Chebotar, Yifan Zhou, Yifeng Zhu, Yilin Wu, Ying Xu, Yixuan Wang, Yonatan Bisk, Yongqiang Dou, Yoonyoung Cho, Youngwoon Lee, Yuchen Cui, Yue Cao, Yueh-Hua Wu, Yujin Tang, Yuke Zhu, Yunchu Zhang, Yunfan Jiang, Yunshuang Li, Yunzhu Li, Yusuke Iwasawa, Yutaka Matsuo, Zehan Ma, Zhuo Xu, Zichen Jeff Cui, Zichen Zhang, Zipeng Fu, and Zipeng Lin. Open X-Embodiment: Robotic learning datasets and RT-X models. https://arxiv.org/abs/2310.08864, 2023. 

- Jack Collins, Mark Robson, Jun Yamada, Mohan Sridharan, Karol Janik, and Ingmar Posner. Ramp: A benchmark for evaluating robotic assembly manipulation and planning. _IEEE Robotics and Automation Letters_ , 9(1):9–16, 2023. 

- Jiayuan Gu, Fanbo Xiang, Xuanlin Li, Zhan Ling, Xiqiang Liu, Tongzhou Mu, Yihe Tang, Stone Tao, Xinyue Wei, Yunchao Yao, et al. Maniskill2: A unified benchmark for generalizable manipulation skills. _arXiv preprint arXiv:2302.04659_ , 2023. 

- Abhishek Gupta, Vikash Kumar, Corey Lynch, Sergey Levine, and Karol Hausman. Relay policy learning: Solving long-horizon tasks via imitation and reinforcement learning. _arXiv preprint arXiv:1910.11956_ , 2019. 

- Minho Heo, Youngwoon Lee, Doohyun Lee, and Joseph J Lim. Furniturebench: Reproducible realworld benchmark for long-horizon complex manipulation. _The International Journal of Robotics Research_ , pp. 02783649241304789, 2023. 

- Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 5(2):3019– 3026, 2020. 

- Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yongqiang Dou, Yanjun Chen, Li FeiFei, Anima Anandkumar, Yuke Zhu, and Linxi Fan. Vima: General robot manipulation with multimodal prompts. _arXiv preprint arXiv:2210.03094_ , 2(3):6, 2022. 

- Steven M LaValle. _Planning algorithms_ . Cambridge university press, 2006. 

- Chengshu Li, Ruohan Zhang, Josiah Wong, Cem Gokmen, Sanjana Srivastava, Roberto Mart´ınMart´ın, Chen Wang, Gabrael Levine, Michael Lingelbach, Jiankai Sun, et al. Behavior-1k: A benchmark for embodied ai with 1,000 everyday activities and realistic simulation. In _Conference on Robot Learning_ , pp. 80–93. PMLR, 2023. 

- Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

12 

- Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, and Irwin King. A survey on visionlanguage-action models for embodied ai. _arXiv preprint arXiv:2405.14093_ , 2024. 

- Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters (RA-L)_ , 7(3):7327–7334, 2022. 

- Tongzhou Mu, Zhan Ling, Fanbo Xiang, Derek Yang, Xuanlin Li, Stone Tao, Zhiao Huang, Zhiwei Jia, and Hao Su. Maniskill: Generalizable manipulation skill benchmark with large-scale demonstrations. _arXiv preprint arXiv:2107.14483_ , 2021. 

- Wilbert Pumacay, Ishika Singh, Jiafei Duan, Ranjay Krishna, Jesse Thomason, and Dieter Fox. The colosseum: A benchmark for evaluating generalization for robotic manipulation. _arXiv preprint arXiv:2402.08191_ , 2024. 

- Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visuallanguage-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- Ranjan Sapkota, Yang Cao, Konstantinos I Roumeliotis, and Manoj Karkee. Vision-language-action models: Concepts, progress, applications and challenges. _arXiv preprint arXiv:2505.04769_ , 2025. 

- Manolis Savva, Abhishek Kadian, Oleksandr Maksymets, Yili Zhao, Erik Wijmans, Bhavana Jain, Julian Straub, Jia Liu, Vladlen Koltun, Jitendra Malik, Devi Parikh, and Dhruv Batra. Habitat: A Platform for Embodied AI Research. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2019. 

- Rui Shao, Wei Li, Lingsen Zhang, Renshan Zhang, Zhiyang Liu, Ran Chen, and Liqiang Nie. Large vlm-based vision-language-action models for robotic manipulation: A survey. _arXiv preprint arXiv:2508.13073_ , 2025. 

- Mohit Shridhar, Jesse Thomason, Daniel Gordon, Yonatan Bisk, Winson Han, Roozbeh Mottaghi, Luke Zettlemoyer, and Dieter Fox. Alfred: A benchmark for interpreting grounded instructions for everyday tasks. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 10740–10749, 2020. 

- Stone Tao, Fanbo Xiang, Arth Shukla, Yuzhe Qin, Xander Hinrichsen, Xiaodi Yuan, Chen Bao, Xinsong Lin, Yulin Liu, Tse-kai Chan, et al. Maniskill3: Gpu parallelized robotics simulation and rendering for generalizable embodied ai. _arXiv preprint arXiv:2410.00425_ , 2024. 

- Dian Wang, Colin Kohler, Xupeng Zhu, Mingxi Jia, and Robert Platt. Bulletarm: An open-source robotic manipulation benchmark and learning framework. In _The International Symposium of Robotics Research_ , pp. 335–350. Springer, 2022. 

- Fanbo Xiang, Yuzhe Qin, Kaichun Mo, Yikuan Xia, Hao Zhu, Fangchen Liu, Minghua Liu, Hanxiao Jiang, Yifu Yuan, He Wang, Li Yi, Angel X. Chang, Leonidas J. Guibas, and Hao Su. SAPIEN: A simulated part-based interactive environment. In _The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2020. 

- Xuning Yang, Clemens Eppner, Jonathan Tremblay, Dieter Fox, Stan Birchfield, and Fabio Ramos. Robot policy evaluation for sim-to-real transfer: A benchmarking perspective. _arXiv preprint arXiv:2508.11117_ , 2025. 

- Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on robot learning_ , pp. 1094–1100. PMLR, 2020. 

13 

- Shiduo Zhang, Zhe Xu, Peiju Liu, Xiaopeng Yu, Yuan Li, Qinghui Gao, Zhaoye Fei, Zhangyue Yin, Zuxuan Wu, Yu-Gang Jiang, and Xipeng Qiu. Vlabench: A large-scale benchmark for languageconditioned robotics manipulation with long-horizon reasoning tasks, 2024. URL https:// arxiv.org/abs/2412.18194. 

- Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

- Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

14 

# A APPENDIX 

## A.1 UNIFIED DATA PLATFORM 

This section details the NEBULA Unified Data Platform, a comprehensive ecosystem designed to address the severe data fragmentation that hinders progress in embodied AI research. The current landscape, characterized by numerous benchmarks with disparate and incompatible data formats, forces researchers to reimplement data processing pipelines for each new dataset. This fundamental challenge not only prevents fair head-to-head model comparisons but also limits the large-scale generalization studies necessary for advancing the field. Our platform overcomes this bottleneck by unifying these varied data sources into a modular and extensible interface. It provides a structured, robot-agnostic foundation for working with large-scale VLA datasets, thereby establishing the necessary infrastructure for the fair and scalable evaluation our work introduces. 

The platform’s architecture is founded on two core design principles that ensure both consistency and extensibility. The first is its Unified and Structured Episode Format, which establishes a canonical, robot-agnostic data structure for representing any robot interaction trajectory. An Episode is defined as one complete task attempt, containing a language instruction, a time-ordered sequence of Steps, and comprehensive metadata. Each Step encapsulates the system’s state at a discrete timestep, comprising a multi-modal Observation (including multiple camera views and proprioceptive states) and the corresponding Action taken by the agent. The second principle is a Robot-Abstracted Embodiment Layer, which decouples robot-specific properties from the core data logic. Instead of being hardcoded, hardware characteristics such as degrees of freedom, gripper types, and multi-arm configurations are defined in a centralized configuration system, making the platform inherently extensible to new robotic hardware with minimal effort. 

This architecture is made accessible to researchers through a high-level Python Software Development Kit (SDK) designed to streamline the research workflow. The SDK abstracts away the complexities of file discovery, parsing, and data decoding, providing a clean interface for programmatic access. Its central feature is a powerful, fluent query engine that allows researchers to efficiently filter and sample data based on a wide range of metadata attributes, including task family, success status, trajectory length, or even natural language instructions. To further support robust and reproducible experimentation, the platform also includes built-in utilities for common machine learning workflows, such as stratified train-test splitting, which ensures that model validation is performed on balanced and representative data subsets. 

Ultimately, the NEBULA Unified Data Platform makes a critical contribution to the field by removing the significant engineering overhead associated with data fragmentation. This allows the research community to shift its focus from the tedious work of data wrangling to the core challenges of model innovation and architectural design. More importantly, this unified infrastructure is the essential foundation upon which our dual-axis evaluation framework is built. By ensuring data consistency and enabling plug-and-play compatibility with a wide range of models , the platform provides the necessary conditions for the fair, large-scale, and diagnostic evaluations required to systematically advance the development of robust and generalizable embodied agents. 

## A.2 TEST TASKS DESIGN & EVALUATION 

## A.2.1 CAPABILITY TEST TASKS 

This section provides the full specification for all capability tasks used in NEBULA. Each task family targets a specific embodied competency and includes _Easy_ , _Medium_ , and _Hard_ tiers. Each task tier comprises three unique task sets instantiated from templates, with randomized object attributes and layout to ensure diversity. Success is determined through well-defined, programmatic criteria based on object positions, interactions, and task logic. 

**Control** The Control task family is specifically designed to isolate an agent’s low-level manipulation and motion planning capabilities by systematically removing all non-control-related confounding factors. To ensure this isolation, each task instance provides fully specified and fixed object states, including fixed positions, orientations, and visual properties such as color and size. This eliminates any reliance on perception, semantic understanding, or language grounding. Instructions 

15 


Figure 6: The **Control capability** family evaluates an agent’s ability to perform precise and reliable motor actions under varying levels of complexity. Green marks objects, red marks targets, and blue indicates contextual cues. **<u>Bold underlined</u>** text shows actions; _<u>italic underlined</u>_ text gives clarifications. 

are deliberately minimal and unambiguous, ensuring that task success depends purely on motor execution. 

The task suite is divided into three difficulty tiers based on control sequence complexity. _Easy_ tasks involve one to two atomic actions such as picking and pushing. Success is determined based on 

16 


Figure 7: The **Perception capability** test is designed to evaluate an agent’s ability to identify target objects based solely on their visual attributes. red marks targets, and blue indicates contextual cues. **<u>Bold underlined</u>** text shows actions. 

the object reaching its goal position under proper spatial relation. _Medium_ tasks extend to multiple sequential steps, often requiring coordination across multiple objects, with success requiring completion of the full action sequence with all spatial constraints satisfied. _Hard_ tasks require extended action sequences involving more steps and include fine-grained manipulation challenges that demand high precision and stability, such as multi-object stacking arrangements or sub-centimeter insertion tolerances. This progression allows for a nuanced evaluation of an agent’s capacity to generate, maintain, and adjust action sequences in increasingly demanding scenarios. The visualization and corresponding language commands are demonstrated in Figure 6. 

17 

## **Base Task Environment** 


## **Easy: Straight** 

## **Medium: Negation** 

## **Hard: Condition** 

- “ **<u>Pick</u>** the red cube.” 

- “ **<u>Grab</u>** the red cube.” 

- “ **<u>Select</u>** the red cube.” 

- " **<u>Do not pick</u>** the blue and green cubes" 

- " **<u>Pick</u>** the cube that is not blue or green" 

- "If there is a red cube, **<u>pick</u>** it” 

- " **<u>Pick</u>** the red cube only if there is a blue one." 

- "If there is a red cube, pick it; otherwise, do nothing." 

- " **<u>Pick</u>** the red cube unless the task says not to" 

Figure 8: The **Language capability** in NEBULA evaluates a model’s ability to interpret and act upon natural language instructions in robotic manipulation settings. red marks targets, and blue indicates contextual cues. **<u>Bold underlined</u>** text shows actions. 

**Perception** The Perception task family evaluates an agent’s ability to recognize and distinguish object-level attributes such as color, shape, and size, while explicitly eliminating confounding factors from downstream control. To ensure a clean probe into perceptual capacity, control difficulty is minimized: all target objects are placed within reachable, uncluttered regions, and the task is considered successful as long as the robot makes contact with the correct object—regardless of grasp success or trajectory smoothness. This design mitigates potential confounds from hardware instability and isolates perception as the sole bottleneck. 

Task difficulty increases across three tiers: _Easy_ tasks involve clearly distinct attributes; _Medium_ tasks introduce ambiguity via subtle shape or color variations across multiple distractors; and _Hard_ tasks incorporate partial occlusions and low-contrast distractors, requiring the agent to resolve finegrained visual distinctions under constrained viewpoints. This progression enables robust evaluation of perceptual skills under increasingly realistic and complex visual conditions. The visualization and corresponding language commands are demonstrated in Figure 7. 

**Language** The Language task family is designed to isolate and evaluate an agent’s ability to interpret natural language instructions with minimal interference from perception, control, or environmental variability. To enforce this isolation, all scenes are fully standardized across difficulty levels—identical objects, visual attributes, and spatial configurations are used for every task variant. Only the instruction text changes, ensuring that observed performance differences stem solely from linguistic understanding rather than scene-specific cues or motor complexity. 

18 

The tasks are categorized into three difficulty tiers: _Easy_ tasks test basic grounding of surface-level attributes ( _e.g.,_ “Pick the red cube”); _Medium_ tasks require relative position analysis and selective instruction comprehension ( _e.g.,_ “Place the cube that is not red” or “Pick the small green cube”); and _Hard_ tasks assess deeper linguistic reasoning, including conditional logic, instruction filtering, and multi-step execution tracking ( _e.g.,_ “If the green cube is smaller than the red one, place it in the bin. Otherwise, discard it”). This setup provides a clean and controlled probe into the agent’s ability to parse, interpret, and act upon language-based directives of increasing semantic and logical complexity. The visualization and corresponding language commands are demonstrated in Figure 8. 

**Dynamic Adaptation** The Dynamic Adaptation task family targets an agent’s ability to operate under time-varying and non-stationary conditions, evaluating how well it can adjust to moving objects, time-sensitive constraints, and external perturbations. 

This task family is structured into three difficulty tiers, each progressively increasing the level of environmental dynamics and required reactivity. _Easy_ tasks involve static scenes with time-critical or distraction-based events, such as pressing a switch within a short time window. _Medium_ tasks introduce slow, predictable dynamics in the scene—objects may roll, slide, or shift position over time, requiring the agent to adjust its plan on-the-fly. These tasks require basic perception-action adaptation and temporal anticipation. _Hard_ tasks present high-variability and multi-modal dynamics. These tasks demand complex real-time perception, state tracking, and policy re-evaluation, pushing the limits of an agent’s reactive robustness and memory. By scaling the difficulty along temporal variability and unpredictability, this task family offers a comprehensive stressor for evaluating embodied agents in non-static environments. The visualization and corresponding language commands are demonstrated in Figure 9. 

**Spatial Reasoning** The Spatial task family evaluates an agent’s ability to reason over object positions and geometric relationships in 3D space. Unlike perception tasks that focus on attribute recognition, these tasks isolate spatial understanding by holding visual appearance and control difficulty fixed, ensuring that success depends solely on interpreting and executing spatial constraints. 

_Easy_ tasks are confined to 2D planar reasoning where relations like left, right, or between are defined on a flat surface. _Medium_ tasks expand to 3D spatial concepts, introducing both horizontal and vertical relationships.” _Hard_ tasks demand full 6-DoF motion planning, requiring the agent to align and manipulate objects in all three spatial axes with rotational precision, such as stacking irregularly shaped items in complex orientations. This progression enables controlled, fine-grained evaluation of spatial reasoning skills across increasing geometric complexity. The visualization and corresponding language commands are demonstrated in Figure 10. 

**Robustness/Generalization** The Robustness and Generalization task family is designed to assess an agent’s ability to perform reliably under distribution shifts in object attributes, scene composition, and out-of-distribution (OOD) scenarios. 

_Easy_ tasks introduce distractor objects (1-2 objects) into familiar scenes while keeping the main task unchanged, testing an agent’s selective attention. _Medium_ tasks alter object attributes such as color—for instance, changing the sphere from blue to orange while maintaining the same scene structure and task requirements—probing the agent’s ability to generalize across visual variations. _Hard_ tasks present completely novel environments, layouts, or object configurations that were never encountered during training, thereby measuring the agent’s generalization capacity to OOD scenarios. The success criteria are the same as the original task or are evaluated according to the correct spatial relations, positions, and orientations. Together, these progressively challenging setups evaluate how well embodied agents can adapt their learned policies to unfamiliar or perturbed conditions without retraining or explicit guidance. The visualization and corresponding language commands are demonstrated in Figure 11. 

## A.2.2 STRESS TEST TASKS 

This section presents the stress test specifications for evaluating system performance under operational constraints. Each test systematically varies a single performance indicator across three calibrated levels, with specific criteria detailed below. 

19 


Figure 9: The **Dynamic Adaptation capability** tests in NEBULA are designed to evaluate an agent’s ability to perceive and respond to changes in the environment in real time. Green marks objects, red marks targets, and blue indicates contextual cues. **<u>Bold underlined</u>** text shows actions; _<u>italic underlined</u>_ text gives clarifications. 

**Inference Frequency** Inference frequency measures the rate at which an agent generates control actions in hertz. This metric directly impacts an agent’s ability to respond to dynamic environments and maintain smooth control. The test evaluates inference frequency under three scenarios: _v_ 1 tests slow and uniform movements; _v_ 2 tests alternating movement at medium speed; _v_ 3 tests fast irregular 

20 


Figure 10: The **Spatial Reasoning capability** family evaluates an agent’s ability to interpret and execute spatial relationships and geometric constraints in 3D manipulation tasks. Green marks objects, red marks targets, and blue indicates contextual cues. **<u>Bold underlined</u>** text shows actions; _<u>italic underlined</u>_ text gives clarifications. 

movements. Performance degradation across tiers reveals how VLA models handle increasing computational demands, exposing whether failures stem from insufficient inference speed and model architecture limitations. 

**Latency** Latency quantifies the delay between sensory input and action output, measured in milliseconds from perception trigger to control signal generation. esting occurs across three conditions: 

21 


Figure 11: The **Robustness/Generalization** capability in NEBULA evaluates an agent’s ability to perform reliably across diverse, unseen conditions. Tasks in this category are intentionally designed to expose the agent to variations it has not encountered during training. Green marks objects, red marks targets, and blue indicates contextual cues. **<u>Bold underlined</u>** text shows actions. 

_v_ 1 measures static scene; _v_ 2 measures dynamic scene with moving objects; _v_ 3 measures dynamic scene with fast-moving objects. This metric is critical for time-sensitive manipulation where delayed responses lead to task failure. Lower latency enables tighter control loops and more responsive behavior, particularly crucial for contact-rich manipulation and dynamic grasping tasks. 

**Stability Score** Stability scores quantifies trajectory smoothness by measuring action variation between consecutive timesteps. Given an action sequence _{a_ 0 _, a_ 1 _, ..., at}_ , the score is computed as: 

22 


Figure 12: Visualization of NEBULA **Stress Test** . Green marks objects, red marks targets, and blue indicates contextual cues. **<u>Bold underlined</u>** text shows actions; _<u>italic underlined</u>_ text gives clarifications. 


where _||_ **a** _t −_ **a** _t−_ 1 _||_ 2 represents the _L_ 2 norm of action changes between neighboring timesteps and the exponential decay of mean action changes yields a normalized score _∈_ [0 _,_ 1], with 1 indicating perfect stability. The test evaluates three precision levels: _v_ 1 tests coarse continuous force control such as object pushing; _v_ 2 requires smoother and more accurate trajectories like grasping and lifting operations; _v_ 3 demands high-precision position and orientation control for tasks like plug insertion. This metric reveals whether VLA policies generate stable control signals suitable for physical deployment, distinguishing smooth execution from erratic behaviors that could damage hardware or cause task failure. Figure 12 shows the task design. 

**Adaptability** Adaptability measures an agent’s ability to adjust its behavior in response to environmental changes, task interruptions, or modified objectives during execution. The test evaluates the model’s performance across three scenarios: _v_ 1 tests response to object displacement where the target suddenly moves to a new position; _v_ 2 introduces mid-task instruction changes, requiring the agent to switch between objectives ( _e.g.,_ ”Pick up the blue cube” _→_ ”Pick up the green cube”); _v_ 3 demands rapid re-planning under sequential instructions ( _e.g.,_ ”Pick up the cube” _→_ ”Release the cube”). This progression assesses whether VLA policies can maintain task coherence under dynamic conditions, distinguishing reactive agents that gracefully handle perturbations from rigid controllers that fail when initial assumptions are violated. The visualization and corresponding language commands are demonstrated in Figure 12. 

23 

Table 5: Comparison of NEBULA and existing single-arm manipulation benchmarks across task design and evaluation protocols. NEBULA uniquely supports both capability evaluation and stress testing. Unlike prior benchmarks, it adopts a dual-axis protocol that evaluates skills and stress responses separately, ensuring each score reflects a specific factor. Other benchmarks mostly report task-level success rate without isolating capabilities or stress conditions, limiting diagnostic insight. 

|Benchmark||Task D|esign||Data De|sign|
|---|---|---|---|---|---|---|
||Task Families|Language|Tiered Difficulty|Evaluation|# Modality|# View|
|ManiSkill|Multiple|✗|✗|TSR|1|3|
|RLBench|Multiple|✗|✗|TSR|1|2|
|FurnitureBench|Furniture|✗|✗|TSR|1|2|
|BridgeDataV2|Pick/Place|✗|✗|TSR|1|2|
|Meta-World|Multiple|✗|✗|TSR|1|2|
|FrankaKitchen|Kitchen-related|✗|✗|TSR|1|2|
|CLVIN|Visual Reasoning|✓|✗|TSR|1|2|
|ALFRED|Compositional|✓|✗|TSR|1|2|
|LIBERO|Language|✓|✓|TSR|1|2|
|VLABench|Realistic|✓|✓|TSR|1|2|
|**NEBULA (Ours)**|6 Capabilities|✓|✓|DAE|3|6|


( **Notes** : _SR_ represents _Success Rate_ , _TSR_ represents _Task-level Success Rate_ , _DAE_ represents _DualAxis Evaluation_ ) 

**Resources** The resources stress test evaluates the computational efficiency and scalability of embodied agents by measuring runtime resource consumption across multiple dimensions as well as the static memory usage. This test quantifies GPU memory usage, CPU memory usage, and model size. By profiling memory footprint and model size alongside task performance, this test enables practitioners to assess deployment feasibility across hardware-constrained platforms and identify computational bottlenecks that may limit real-world applicability. 

## A.3 BENCHMARK COMPARISON 

Table 5 indicates that NEBULA uniquely implements dual-axis evaluation (DAE) that separates capability assessment from stress testing, while all other benchmarks report only task-level success rates. Table 5 also highlights NEBULA’s comprehensive data collection: three modalities (RGB, depth, segmentation) and six camera viewpoints versus the single modality and 1-2 views standard in other benchmarks. Only LIBERO and VLABench match NEBULA’s tiered difficulty structure, though neither provides the diagnostic isolation of specific capabilities that NEBULA’s six distinct task families enable. 

24 

