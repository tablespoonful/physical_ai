---
title: "Wow, wo, val! A Comprehensive Embodied World Model Evaluation Turing Test"
date: "2026-01-07"
authors: "Chun-Kai Fan; Xiaowei Chi; Xiaozhu Ju; Hao Li; Yong Bao; Yu-Kai Wang"
url: https://arxiv.org/abs/2601.04137
pdf: https://arxiv.org/pdf/2601.04137
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.04137)** / [論文ページ](https://arxiv.org/abs/2601.04137)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Wow, wo, val! A Comprehensive Embodied World Model Evaluation Turing Test** 

Chun-Kai Fan<sup>1,2,*</sup> Xiaowei Chi<sup>2,3,*</sup> Xiaozhu Ju<sup>2,†</sup> Hao Li<sup>2</sup> Yong Bao<sup>2</sup> Yu-Kai Wang<sup>1,2</sup> Lizhang Chen<sup>1</sup> Zhiyuan Jiang<sup>2</sup> Kuangzhi Ge<sup>1,2</sup> Ying Li<sup>1</sup> Weishi Mi<sup>2</sup> Qingpo Wuwu<sup>1</sup> Peidong Jia<sup>1,2</sup> Yulin Luo<sup>1</sup> Kevin Zhang<sup>1,2</sup> Zhiyuan Qin<sup>2</sup> Yong Dai<sup>2</sup> Sirui Han<sup>3</sup> Yike Guo<sup>3</sup> Shanghang Zhang<sup>1,‡</sup> Jian Tang<sup>2,‡</sup> 

1State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University 

2Beijing Innovation Center of Humanoid Robotics 3The Hong Kong University of Science and Technology 

## **Abstract** 

## **1. Introduction** 

_As world models gain momentum in Embodied AI, an increasing number of works explore using video foundation models as predictive world models for downstream embodied tasks like 3D prediction or interactive generation. However, before exploring these downstream tasks, video foundation models still have two critical questions unanswered:_ **_(1)_** _whether their generative generalization is sufficient to maintain perceptual fidelity in the eyes of human observers, and_ **_(2)_** _whether they are robust enough to serve as a universal prior for real-world embodied agents. To provide a standardized framework for answering these questions, we introduce the Embodied Turing Test benchmark:_ **_WoWWorld-Eval (Wow,wo,val)_** _. Building upon 609 robot manipulation data, Wow-wo-val examines five core abilities, including perception, planning, prediction, generalization, and execution. We propose a comprehensive evaluation protocol with 22 metrics to assess the models’ generation ability, which achieves a high Pearson Correlation between the overall score and human preference (>0.93) and establishes a reliable foundation for the Human Turing Test. On Wowwo-val, models achieve only 17.27 on long-horizon planning and at best 68.02 on physical consistency, indicating limited spatiotemporal consistency and physical reasoning. For the Inverse Dynamic Model Turing Test, we first use an IDM to evaluate the video foundation models’ execution accuracy in the real world. However, most models collapse to ≈ 0% success, while WoW maintains a 40.74% success rate. These findings point to a noticeable gap between the generated videos and the real world, highlighting the urgency and necessity of benchmarking World Model in Embodied AI._ 

> *Equal contribution. 

> †Project leader. 

> ‡Corresponding author. 

World models – which capture an agent’s understanding of how the world changes with actions [35] – have emerged as a pivotal concept in robotics and Embodied AI. In embodied settings, a world model allows a robot to understand and predict its environment [21, 32, 49, 56], and can function as the robot’s “internal brain”, enabling it to simulate future scenarios for planning and decision-making [17, 43, 72, 85], or operate as an environment simulator [47, 52, 88]. 

Compared with cutting-edge spatial-prediction world models [3, 79], embodied world models operate in contextrich environments that demand a deeper understanding of physical common sense. In robotics, the complexity and lack of standardization across setups further lead to a broad and diverse landscape of embodied-world-model designs. These models vary widely in their control conditions—ranging from approaches conditioned solely on images and language instructions [15–17, 72], to those incorporating keypoints [84], trajectories [9, 31, 34, 41, 51, 69], depth, semantics, and other modalities [50, 92, 99]. They also differ in camera configurations, requiring either singleview inputs [9, 15, 16, 31, 51, 69, 72, 84, 100] or multi-view setups [11, 17, 34, 52, 66, 73, 92]. Moreover, several recent efforts have begun to pursue cross-embodiment generalization [17, 37, 98]. Therefore, despite the broader research of world models in general-purpose robotics, two core questions still remain: 

1. Can these models generalize well enough to maintain perceptual fidelity from a human perspective? 

2. Are they robust and expressive enough to serve as universal priors for real-world embodied agents? 

Existing video-generation benchmarks [29, 40, 46, 53, 54, 95, 97] largely target general-purpose settings or isolated dimensions and overlook the unique requirements of robotic world models. Most evaluations emphasize visual fidelity or coarse task success, but rarely assess deeper embodied abilities such as physical plausibility, planning ra- 

1 


Figure 1. **The Overview of WoW-World-Eval. (Top-left)** A multi-faceted _Metrics_ suite evaluates generated videos across five dimensions: Video Quality, Instruction Understanding, Planning Reasoning, Physical Law, and Execution Accuracy. **(Top-center)** These metrics align with five core _Abilities_ of embodied world models: Perception, Planning, Prediction, Execution, and Generalization. **(Top-right)** Performance gaps across state-of-the-art models. **(Bottom)** The benchmark follows the embodied world model pipeline from Perception to Generalization. 

tionality, and actionability. This gap makes progress difficult to measure: a model may score well on conventional video metrics [27, 65, 81, 86] yet produce physically impossible or contextually incorrect predictions in robotic scenarios. Our results further confirm this misalignment—standard video-quality scores correlate poorly with human judgments in embodied settings—highlighting the need for more reliable evaluation standards. 

Consequently, in this paper, we address these challenges by proposing a new comprehensive benchmark for embodied world models, and use it to systematically evaluate foundational models under the simplest _image-to-video_ setting. Our benchmark, **WoW-World-Eval** , as illustrated in Figure 1, is designed around the core capabilities that an embodied world model should possess: perceiving the environment, understanding and planning based on task instruc- 

2 

tions, predicting and simulating future world states, executing real-world interactions, and generalizing across diverse scenarios and embodiments. It contains about 609 robot manipulation samples with meticulous cleaning and annotation by human annotators. Also we incorporate 22 evaluation metrics aligned with our core dimensions across Video Quality, Instruction Understanding, Planning Reasoning, Physical Law, and Execution Accuracy. 

Moreover, **WoW-World-Eval** follows the twoalternative forced-choice (2AFC) [28] methodology from psychophysics to establish the evaluation as a standardized Turing Test for generative video models. By collecting fine-grained human answers distinguishing real and generated videos, we compute the proportion of generated videos from each model that successfully fool human evaluators. Notably, an overall human preference alignment score exceeding Pearson Correlation = 0.93 demonstrates the effectiveness of our benchmark in evaluating high-quality generations and serves as a reliable proxy for the _Human Turing Test_ . 

In addition to the human-centered evaluation, we also introduce a _Machine Turing Test_ —specifically, an _Inverse Dynamics Model (IDM) Turing Test_ . In this setting, we assess whether videos generated by a model can “fool” an IDM that has only been trained on real-world execution sequences. If the generated videos lead the IDM to output plausible actions that are executable in the real world, it indicates that the model’s outputs are indistinguishable from real data in terms of physical and action plausibility. 

By evaluating existing models under this new benchmark, we reveal which models already exhibit credible world understanding and where they fall short. We believe this benchmark and the accompanying Turing Test criterion will provide a much-needed standard for the field, driving research towards embodied world models that can truly imagine the world with the accuracy and fidelity that robotics applications demand. Our contributions are threefold as follows: 

- A comprehensive World Model Benchmark, **WoWWorld-Eval** , focuses on the Embodied AI domain, introducing a new perspective with a novel framework for the five core abilities in the embodied world model. 

- Based on **WoW-World-Eval** , we propose two novel Turing tests aligned with our benchmark, the Human Turing test and IDM Turing Test, that can distinguish the models’ true ability as an embodied world model to simulate and interact with the real world. 

- We curate 609 high-quality robot manipulation samples with careful human annotations in **WoW-World-Eval** . Using this benchmark, we conduct a comprehensive evaluation of various world models, whose performance provides new insights into the strengths, limitations, and generalization gaps of current embodied world models. 

## **2. Related work** 

Table 1. **Comparison of benchmark features.** A checkmark (✓) indicates that the benchmark explicitly includes the corresponding evaluation dimension or metric, while a cross ( _×_ ) indicates that it does not. In Core Dimensions, Perception(Percept); Prediction(Pred); Planning(Plan); Execution(Exec); Generalization(General); in Metrics Design, Video Quality(VQ); Instruction Understanding(IU); Physical Law(PL); Planning Reasoning(PR); Execution Accuracy(EA). 

|||Core|Dime|nsions||M|etri|cs D|esign||
|---|---|---|---|---|---|---|---|---|---|---|
|Benchmark|Percept|Pred|Plan|Exec|General|VQ|IU|PL|PR|EA|
|Physics-IQ [61]|✓|✓|_×_|_×_|_×_|_×_|_×_|✓|_×_|_×_|
|PhyGenBench [59]|✓|✓|_×_|_×_|_×_|_×_|_×_|✓|_×_|_×_|
|T2V-CompBench [78]|✓|✓|_×_|_×_|_×_|_×_|✓|✓|_×_|_×_|
|VBench-2.0 [97]|✓|✓|_×_|_×_|✓|✓|✓|✓|_×_|_×_|
|WorldModelBench [46]|✓|✓|_×_|_×_|✓|_×_|✓|✓|_×_|_×_|
|EWMBench [95]|✓|✓|_×_|_×_|_×_|_×_|✓|✓|_×_|_×_|
|Ours|✓|✓|✓|✓|✓|✓|✓|✓|✓|✓|


The evaluation of generative world models and video generation models is rapidly evolving. Existing benchmarks can be grouped into: (1) those targeting general video quality, (2) those assessing physical reasoning, and (3) benchmarks for holistic world model evaluation. 

**Video Generation Benchmarks.** Early benchmarks mainly assessed visual fidelity and temporal coherence. TC-Bench [29] studies temporal compositionality with transition-aware metrics. [53] measures perception-aligned motion quality. T2V-CompBench [78] evaluates compositionality via MLLM- and tracking-based methods, challenging metrics like FVD. [15, 40, 54] introduce tasks related to controllability and anticipation. VBench-2.0 [97] focuses on “intrinsic faithfulness,” adding _Physics_ and _Commonsense_ dimensions using VLM/LLM evaluators. 

**Physical Reasoning Benchmarks.** Physics-IQ [61] introduces physics-based diagnostics. PhyGenBench [59] targets semantic and physical plausibility. PhysBench [18] evaluates VLM physical reasoning via QA tasks rather than pixel metrics. Videophy [4] benchmarks physical commonsense using rule-based and learned evaluators. 

**World Model Benchmarks.** WorldModelBench [46] and EWMBench [95] evaluate core dimensions like Perception, Prediction, and Generalization. Critically, as shown in Table 1, these benchmarks do not assess the crucial core dimension of Planning and Execution. Furthermore, no prior benchmark provides a metrics design that covers Planning Reasoning or Execution Accuracy in the robotics domain. Our proposed **WoW-World-Eval** extends these efforts with a robotics-centric design, making it the most comprehensive embodied world model benchmark to date. 

3 


Figure 2. **Overview of WoW-World-Eval Data Construction Pipeline and Data Statistics. (Left)** Public and in-house data are cleaned sequentially by GPT and human annotators to produce high-quality samples consisting of an initial image, prompt, ground-truth video, and annotated keypoints. **(Right)** Data distribution across five different dimensions from overall to fine-grained. 

## **3. WoW-World-Eval: A Multi-faceted Benchmark for Embodied World Models** 

In this section, we introduce **WoW-World-Eval** , a novel benchmark designed to evaluate embodied world models rigorously. We formulate the core evaluation task as **conditional video generation from an initial image and a text instruction (Image-Text-to-Video)** , a setting that directly probes a model’s ability to understand a given state and execute a specified action. Moving beyond metrics of visual appeal, **WoW-World-Eval** specifically assessed a model’s instruction understanding, planning, observation perception abilities, and understanding of physically grounded dynamics in embodied settings. For introducing our benchmark, we structure our presentation by first outlining the five core capabilities that a competent embodied world model must possess (Section 3.1), then detailing our data curation pipeline (Section 3.2), followed by our comprehensive evaluation metrics (Section 3.3). 

### **3.1. Core Evaluation Dimensions** 

We posit that a truly effective embodied world model must demonstrate mastery across five fundamental and orthogonal dimensions, as outlined in our benchmark design (Figure 1, Top-center). 

**Perception Understanding.** A world model must first accurately perceive and represent the environment to enable more reliable subsequent prediction and planning. We assess this through tasks requiring fine-grained **object recognition** [12, 13, 18, 58](attributes like color, shape, number, and size), **spatial understanding** [14, 23, 77, 90] (relative positions and arrangements), and **affordance recognition** [14, 33, 63] (identifying interactive parts of objects). 

**Decision-making and Planning.** Embodied agents must execute long-horizon tasks [10, 12, 48, 74, 91]. Therefore, we assess a model’s planning ability by challenging it to generate coherent video sequences for complex instructions. This requires implicitly understanding **task decomposition** [15, 80] into key sub-goals and respecting their **causal dependencies** . Hence, we collect 25 samples to fill in this long-term planning task, and transform the text instruction into a suitable description for the world model to plan. In order to evaluate the planning ability in the world model, we refer to the metric from RoboBench [57]. The detailed metric will be elaborated in section 3.3. 

**Predictive Reasoning.** This dimension evaluates the model’s internal physics engine. Given an initial state and an action, the model must generate a future that respects core physical principles such as **object permanence** [4, 18], **collision dynamics** [4, 18, 59, 61], and **trajectory plausibility** [24, 46, 68, 95, 97]. This directly probes the model’s capacity to function as a world simulator [7]. Therefore, we design several sub-dimensions that focus on these principles, as illustrated by the pie chart in the right of Figure 2. 

**Interactive Execution.** Interacting with the real world and executing on a real robot is the ultimate goal of an embodied world model. To examine this, we collect 9 different tasks from our in-house data that are compatible with the real robot experiments, for the model to generate. Furthermore, we will have the model generate videos based on this in-house data and use the Gripper-Centric Inverse Dynamics Model(GC-IDM) [17], to interpret generated videos into actions that can be executed for a real robot, finding out the **execution ability** in the world model. The detailed task names and the implementation will be described in the Appendix 10.3. 

4 

**Generative Generalization.** A universal world model should not only perform well on the In-Distribution data, but it should also generalize beyond the data it has seen before to demonstrate its generalization ability. For this reason, we test generalization on the in-house robot data that we collected, by using GPT-5 [39] to perform style transfer or image editing on it, and generating images that the world model had never seen before. We also collected some world-famous masterpiece paintings, such as _"Girl with a Pearl Earring"_ , and asked the world model to execute the task instructions that humans created. These two types of images constitute our **In-house Data** and **Out-ofDistribution (OOD)** dimension. 

### **3.2. Data Curation Pipeline** 

To systematically evaluate these capabilities, we build a principled, semi-automated data curation pipeline (Figure 2 Left). Our dataset combines open-source robotics data (e.g., RoboMIND [87], DROID [42]), in-house trajectories, and AI-generated OOD samples to ensure coverage and diversity. GPT-4o [39] is initially used as an intelligent annotator, scoring the matching level of video–instruction pairs based on our five capability dimensions and their subdivisions, specifically examining which instructions match which dimensions, thereby achieving large-scale filtering and coarse categorization. Human experts then verify all samples to guarantee category accuracy and resolve edge cases. Five additional annotators selected the best initial frames for generation (both the robotic arm and the manipulated object were in the same frame) and key point annotations (the robotic arm gripper, joints, and the manipulated object) on the initial frame for evaluation metrics. 

Each benchmark entry contains: (1) a natural-language instruction, (2) an initial image, (3) a ground-truth video, and (4) annotated keypoints (in Prediction). In total, the dataset comprises 609 samples across all dimensions (Figure 2 Right). Prediction (50.57%) and Perception (40.89%) dominate the ability distribution. The perception subdivisions includes object attribute, object affordance, object function, and spatial-relation tasks (249 samples). Physical interaction covers single-object manipulation (56.08%), multi-object interaction (41.89%), and dual-arm cooperation (2.03%). We further include 107 non-occluded views and 54 semi-occluded views in the initial frames to test robustness. With execution data, we choose 9 real-world tasks from easy to hard for the settings. 

### **3.3. Multi-faceted Evaluation Metrics** 

Our evaluation protocol is a suite of metrics designed to be as comprehensive as the capabilities we measure. We introduce several novel metrics alongside standard ones, grouped by the property they assess. For detailed information of all the metrics, see Appendix 9. 

**Visual Fidelity.** To fully evaluate visual fidelity, we report standard video quality metrics spanning pixel, perceptual-, and distribution-level quality perspectively: **PSNR** [27] measures pixel-level fidelity via the log ratio between the maximum signal value and the mean-squared error. To capture higher-level content consistency beyond pixel statistics, we compute **SSIM** [86] for a structural measure and **DINO** [65] as a semantic/instance-alignment signal, combine with **Dreamsim** [30], a human-aligned perceptual similarity metric trained from human triplet judgments. **FVD** [81] compares the distributions of real and generated videos by computing a Fréchet distance, which reflecting overall realism and temporal dynamics at the dataset level. 

**Instruction Semantic Alignment.** We use GPT-4o [39] as a scalable evaluator to assess semantic alignment between the given instruction and the generated videos. Depending on whether ground-truth (GT) video is available, we adopt two methods: 

- **With Ground-Truth:** We first prompt GPT-4o to extract structured descriptions (Initial-, Processing-, Finalstate) from both the generated and GT videos. A vision–language model then scores their **Caption Score** , which scales from 1-to-5. In addition, GPT-4o also evaluates the generated video action-object pairs against the instruction to produce a **Sequence Match Score** (0–1 scale), which stands for the correctness of the order of the action-object pairs, and an **Execution Quality Score** (1–5 scale) for the correctness of the action-object pairs. _We report all three metrics in this setting._ 

- **Without Ground-Truth (in Generalization):** When GT video is unavailable, we only assess instruction adherence: GPT-4o directly analyzes the generated video and the instruction to output the **Sequence Match Score** and the **Execution Quality Score** . _For this setting, only these two metrics are reported._ 

**Physical Consistency and Causal Reasoning.** To quantify the physical plausibility of generated videos, we compute three kinds of metrics as follows: 

- **Mask-guided Regional Consistency.** To better disentangle inconsistencies in the background, robot arm, and manipulated object, we propose **Mask-guided Regional Consistency** . We first use the GroundedSAM2 [71] with human annotation to obtain masks for the robot arm, the manipulated object(s), and the background in each frame. We then compute region-specific embeddings using a vision foundation model (e.g., DINOv3 [76]) and measure cosine similarity across time for each region separately. This allows us to pinpoint the source of temporal flaws—for instance, identifying a "jittery" robot arm even when the object and background are stable. 

- **Trajectory Consistency:** For comparing the trajectory between generated videos and ground-truth counterparts, 

5 

we track both the end-effector and object trajectories. In our benchmark, we leverage SAM2 [70], given a few representative key points in the initial frame that humans annotated, to follow the motion of objects in both videos. Trajectory similarity is then evaluated using a complementary set of metrics: **Mean Euclidean Distance (MED)** [22] to capture average deviation, **Dynamic Time Warping (DTW)** [62] to assess temporal alignment, and **Fréchet Distance** [25] to measure worst-case path similarity. 

- **Physical common sense:** Physical common sense covers dimensions ranging from object interaction and properties to temporal consistency, lighting, fluid dynamics, and local anomalies. To automatically score these six distinct dimensions, we fine-tuned Qwen-2.5-VL [2] using a twostage GRPO [75] process. First, we used several physical and temporal datasets [5, 18, 19, 44, 55, 96] for an initial GRPO fine-tuning to enhance the model’s understanding of video content, temporal causality, and physical laws. Second, we used a human-annotated dataset of 1,297 ratings (a mix of synthetic and real videos) for further training, aligning the model to human preferences. The finetuned model was finally used to score these dimensions on a 1-to-5 scale. 

**Planning and Task Decomposition.** To evaluate longhorizon planning, we refer to the metric of RoboBench [57] based on Directed Acyclic Graphs (DAGs). We first parse the natural language instruction and ground-truth video into a ground-truth plan DAG, where nodes are atomic actions parameterized by _⟨_ skill _,_ object _,_ args _⟩_ and edges represent dependencies. This representation flexibly handles nonunique but valid action orderings. We then compare the model-generated plan (which also uses the same approach from the video) to the ground-truth DAG using two scores: 

1. **Node Correctness:** The fraction of correctly predicted nodes aligns with the ground-truth nodes. 

2. **Task Completion:** Using the MLLM to conduct a lightweight world-simulation rollout using: (i) firstframe image, (ii) reference action list, and (iii) reference DAG, and record the stage changes that model-predicted DAGs have correctly executed. 

The final planning score **LongHorizon** integrates these aspects to reward both correctness and completeness: 

_S_ LongHorizon = ( _S_ NodeCorrectness + _S_ TaskCompletion) _∗_ 50 _._ 

### **3.4. Overall Benchmark Score** 

**Setup.** For each model _i_ and metric _m_ , we map the raw measurement _xi,m_ to a common desirability score _si,m ∈_ (0 _,_ 100) via a monotone parametric mapping applied after an absolute pre-scaling to [0 _,_ 1]. We then aggregate desirability scores by weighted arithmetic means at both metricgroup and overall levels. 

**Pre-scale to** [0 _,_ 1] **with absolute anchors.** Let _Lm < Um_ be fixed anchors for metric _m_ (documented per= metric). Define the clipping operator clip( _u_ ; _a, b_ ) min _{_ max _{u, a}, b}_ . We first clamp raw values to [ _Lm, Um_ ], then linearly map to [0 _,_ 1]; for “higher-is-better” (HIB) metrics: 


And for “lower-is-better” (LIB) metrics: 


We use absolute anchors for two common metrics: 


For other metrics, ( _Lm, Um_ ) are fixed per protocol (e.g., theoretical bounds for bounded scales, task-specific absolute targets for unbounded ones). 

**Monotone parametric mappings.** After pre-scaling, we apply a single-parameter monotone transform _fm_ ( _·_ ; _θm_ ) and then rescale to (0 _,_ 100): 


**Simple:** _f_ ( _x_ ) = _x,_ 


Particularly detailed information can be found in the Appendix 9.6 . 

**Aggregation (weighted arithmetic mean).** Metrics are grouped into categories _g_ (e.g., _quality_ , _instruction_ , _physical_ , _planning_ ). For each model _i_ , let _Mg_ denote the set of metrics available in group _g_ , and _|Mg|_ = _Ni,g >_ 0 be its cardinality. We aggregate first within each group by averaging and then across groups with normalized weights. 

Let nonnegative group weights _{Wg}_ sum to one over the groups available for model _i_ . The overall score is 


where _Gi_ = _{g_ : _Ni,g >_ 0 _}_ is the set of groups for which model _i_ has at least one valid metric. Setting _Wg ≡_ 1 yields an unweighted overall mean across all available groups. 

6 

Table 2. **Comparative analysis of different video generation models in Video Quality, Instruction Understanding and Planning Reasoning.** All metrics: higher is better. Best results are **bold** with green highlight. Seq. stands for Sequence; Exec. stands for Execution. 

|**Model**|||**Vid**|**eo Qualit**|**y**|||**Instruction Und**|**erstanding**||**Planning Reasoning**|
|---|---|---|---|---|---|---|---|---|---|---|---|
||**FVD**|**PSNR**|**SSIM**|**DINO**|**DreamSim**|**Overall**|**Caption Score**|**Seq. Match Score**|**Exec. Quality Score**|**Overall**|**Planning DAG**|
|||||||**Clo**|**sed-Source Mode**|**l**||||
|**Kling**|80.41|5.41|85.00|36.95|58.43|53.24|81.91|0.25|1.75|27.97|2.50|
|**Hailuo**|85.01|**6.06**|**85.97**|**41.45**|61.95|**56.09**|**88.78**|51.07|**70.48**|70.11|**17.27**|
|||||||**Op**|**en-Source Model**|||||
|**CogVideoX**|50.49|2.48|80.48|17.06|42.09|38.52|79.66|38.44|44.18|54.09|4.55|
|**Cosmos-Predict1**|62.99|2.91|79.86|15.62|33.92|39.06|83.60|50.89|49.89|61.46|8.10|
|**Wan2.1**|62.95|1.85|74.09|20.50|41.76|40.23|82.28|41.43|46.84|56.85|7.95|
|**Cosmos-Predict2**|78.77|2.27|75.69|24.20|53.12|46.81|84.16|55.51|30.72|56.80|13.41|
|**WoW-cosmos1**|83.03|4.88|83.22|21.89|53.71|49.35|85.34|**63.33**|60.38|69.68|5.45|
|**WoW-wan**|84.89|5.95|85.76|37.74|62.57|55.38|84.85|52.45|49.18|62.16|9.32|
|**WoW-cosmos2**|**85.71**|3.52|78.33|38.63|**64.42**|54.12|85.85|59.04|66.18|**70.36**|12.27|


Table 3. **Comparative analysis of different video generation models in Physical Law.** Con. stands for Consistency; Traj. stands for Trajectory; Obj. stands for Object; Cam. stands for Camera. 

|**Model**||||||**Phy**|**sical Law**|||||||**Overall**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**Robot Con.**|**Obj. Con.**|**Scene Con.**|**Robot Traj. L2norm**|**Robot Traj. DTW**|**Robot Traj. FD**<br>|**Obj. Traj. L2norm**|**Obj. Traj. DTW**|**Obj. Traj. FD**|**Physical Score**|**Cam. ATE**|**Cam. RPE**|**Overall**||
|||||||**Closed-Sourc**|**e Model**||||||||
|**Kling**|**57.62**|16.09|89.26|56.08|86.05|25.27|87.14|87.31|41.77|71.72|98.12|99.86|**68.02**|37.93|
|**Hailuo**|56.99|10.08|**89.95**|56.79|86.53|22.79|**87.87**|**88.96**|**44.90**|57.64|98.26|99.86|66.72|**52.55**|
|||||||**Open-Sourc**|**e Model**||||||||
|**CogVideoX**|59.17|5.82|82.12|47.67|81.31|16.62|83.69|83.14|32.16|70.51|97.55|99.85|63.30|40.12|
|**Cosmos-Predict1**|39.02|4.40|71.69|54.87|84.60|23.55|83.93|83.48|36.99|30.21|96.23|99.66|59.05|41.93|
|**Wan2.1**|38.57|4.72|78.38|46.61|80.51|14.57|81.91|81.98|30.71|**74.98**|83.69|99.36|59.66|41.18|
|**Cosmos-Predict2**|34.61|5.83|68.34|53.15|84.99|22.24|84.82|84.92|40.74|48.78|98.41|**99.87**|60.56|44.40|
|**WoW-cosmos1**|44.72|13.46|77.78|56.00|86.77|25.10|86.00|86.49|37.86|37.10|96.42|99.66|62.28|46.70|
|**WoW-wan**|50.27|9.83|87.10|53.61|85.15|21.19|85.84|86.46|40.59|47.96|97.21|99.73|63.75|47.66|
|**WoW-cosmos2**|49.01|**16.76**|85.20|**59.97**|**87.56**|**30.53**|86.93|87.06|44.46|48.17|**98.64**|**99.87**|66.18|50.74|


## **4. Experiments** 

**Models.** We evaluate our benchmark across a diverse set of commercial closed-source, open-source video generation models, and the World Foundation Model using direct Image-Text-to-Video generation. The closed-source models include Kling-2.1 [45] and Hailuo I2V-02 [60], two state-of-the-art proprietary systems optimized for zero-shot text-to-video and image-to-video generation. For opensource baselines, we include CogVideoX1.5-I2V-5B [94], one of the earliest large-scale video diffusion models, and Wan2.1-I2V-14B [83], an advanced text-to-video generator emphasizing temporal coherence. Furthermore, we evaluate the World Foundation Model, Cosmos-Predict1-7B [1] and Cosmos-Predict2-2B [64], which focus on physics, scene, and world modeling under multimodal prompts. Finally, we evaluate the Embodied World Foundation Model called WoW [17], which was trained for physically consistent and instruction-aware video generation in the embodied domain on different backbones. Together, these models cover a broad spectrum of architectures and training paradigms, enabling a comprehensive comparison across diverse dimensions in our benchmark. 

### **4.1. Quantitative Evaluation Results** 

As shown in Figure 1 (Top-left and center), each ability dimension is evaluated by a targeted subset of metrics. We benchmark core dimensions with four categories of met- 

rics—Video Quality, Instruction Understanding, Physical Law, and Planning Reasoning—with all scores normalized to a 0–100 scale. Results are summarized in Tables 2 and 3. 

**Overall Performance.** Overall score balanced the four capabilities. Under this score, the best closedsource model, Hailuo, achieves the highest score (52.55). Among open-source models, WoW-cosmos2 consistently ranks highest, reaching 50.74, with balanced improvements in Video Quality, Instruction Understanding, and Physics Law, whereas earlier baselines, such as CogVideoX, lag in stability and physical consistency. The importance of overall balance is further highlighted by Kling, which is strong in Video Quality and achieves the best Physical Law score, yet attains a low score (37.93) due to severe deficiencies in Instruction Understanding and Planning. In conclusion, these four dimensions are indispensable for embodied world model benchmarks. 

**Video Quality.** In Table 2, on the Video Quality axis, Hailuo obtains the highest closed-source overall score (56.09), while WoW-wan leads the open-source group, achieving a nearly matched performance (55.38). WoW-cosmos2 attains the best DreamSim (64.42) and the strongest FVD (85.71), even slightly exceeding Hailuo. These results suggest that WoW mainly focuses on highlevel perceptual and distributional realism. For commercial models, they gain an excellent balance between low-level fidelity and high-level perceptual and distributional realism. 

7 

**Instruction Understanding.** For Instruction Understanding, WoW-cosmos2 achieves the best overall score among open-source models (70.36), surpassing the strongest closed-source model, Hailuo (70.11). When decomposing the metrics, we observe complementary strengths across sub-dimensions. Hailuo excels at Caption Score (88.78) and Exec. Quality (70.48), while WoWcosmos1 shows the best Seq. Match (63.33), highlighting that both of them benefit from large-scale text–video alignment for instruction comprehension. Especially, WoWcosmos2 better enforces procedural consistency—i.e., correctly ordering and realizing multi-step instructions over time—while remaining competitive in execution quality. 

**Physical Law.** Table 3 shows that closed-source models establish the upper bound on overall score, with Kling and Hailuo scoring 68.02 and 66.72, respectively. Among opensource models, WoW-cosmos2 leads open-source models (66.18), with strong robot trajectory and camera-motion consistency. Firstly, from consistency perspective, the differentiation in Scene Consistency is not as intense as other two, which means all models performed well across this consistency. Secondly, WoW-cosmos2 attains the strongest Robot Trajectory and Hailuo attains the strongest Object Trajectory, indicates that commercial models focus more on object manipulation, while WoW-cosmos2 is more accurate in handling robot arm movements. Thirdly, camera motion is basically saturated; that is, the camera is very stable across all models, and sudden, erratic movements are rare. The last, these results all show that open-source models closely track commercial models in physical realism. 

**Planning Reasoning.** Planning Reasoning remains a primary bottleneck for current world models. As shown in Table 2, Planning DAG scores occupy a markedly lower and more compressed range than others. The best performance is achieved by Hailuo (17.27), whereas Cosmos-Predict2 unexpectedly leads the open-source group (13.41), followed by WoW-cosmos2 (12.27) and WoW-wan (9.32). Models such as CogVideoX and Kling exhibit weak long-term planning, indicating that long-horizon planning and temporal reasoning still represent underexplored and require more explicit planning representations or control. 

### **4.2. Dense prompts quantitative results** 

Prior work [26] has shown that the textual prompt has a substantial impact on video generation quality, particularly for models that rely on language-conditioned. In our setting, Image-Text-to-Video generation—the initial frame is fixed and cannot be altered, making the text prompt the primary controllable input. Our main results, Table 2 and 3, therefore, use concise prompts that specify only the task goal, without detailed descriptions of the scene, or step-bystep execution. Such under-specified prompts may limit the model’s ability to ground the intended task semantics. 

Table 4. **Comparative analysis of different video generation models with dense prompts.** All metrics: higher is better. Best results are **bold** with green highlight. 

|**Model**|**VQ**|**IU**|**PL**|**PR**|**Overall**|
|---|---|---|---|---|---|
|**Cosmos-Predict1**|35.48|61.07|53.78|7.5|39.46|
|**Cosmos-Predict2**|49.75|75.96|64.66|**13.86**|51.06|
|**WoW-cosmos1**|59.41|72.54|**69.71**|11.14|**53.20**|
|**WoW-wan**|**60.55**|50.83|67.48|8.64|46.88|
|**WoW-cosmos2**|56.86|**76.16**|67.15|9.09|52.32|


To study this effect, we use InternVL3-78B [101] to expand each short prompt into a dense prompt containing explicit environment and object references, sub-goals, and physical constraints. We then re-evaluate models on **WoWWorld-Eval** using dense prompts in the above Table 4. 

Across all evaluation dimensions, dense prompts lead to consistent and sometimes substantial improvements. In **Video Quality** , every model benefits from richer textual conditioning, with the best embodied world model surpassing the closed-source commercial baseline (60.55 vs. 56.09). **Instruction Understanding** exhibits even larger gains: nearly all models improve, and Cosmos-Predict2 increases by almost 20, although WoW-cosmos2 remains the most stable performer across both prompt types. Improvements in **Physical Law** are similarly widespread, with WoW-cosmos1 showing the largest jump (+7), surpassing the previous short-prompt SOTA. In contrast, in **Planning Reasoning** , DAG metric shows minimal change, indicating that detailed prompting alone cannot compensate for the current limitations of world models in long-horizon reasoning and structured task decomposition. Overall, dense prompts provide richer semantic and physical cues that meaningfully enhance generation quality, while exposing fundamental gaps in planning capability that require deeper architectural advances beyond prompt refinement. 

### **4.3. Qualitative Evaluation and Human Evaluation** 

**Qualitative Evaluation.** Figure 3a presents a qualitative comparison across models on a representative manipulation instruction, revealing failure patterns consistent with our quantitative results. General video generators such as CogVideoX, Cosmos-Predict1, and Wan2.1 exhibit visual artifacts, unintended camera motion, and even hallucinated human arms, reflecting dataset biases toward human demonstrations. 

In terms of instruction understanding and planning, Cosmos-Predict1, WoW-Cosmos1, and WoW-Cosmos2 correctly execute the multi-step task, whereas CogVideoX and Wan2.1 fail despite producing motion. CosmosPredict2 and WoW-Wan show physics violations such as object duplication or motion without force, while Kling 

8 


Figure 3. **Side-by-side comparison:** (a) qualitative results by different models; (b) display a metric–preference correlation. 

remains static and ignores the task, demonstrating limited planning capability. 

Overall, the videos generated by WoW- Cosmos2 is more likely to be indistinguishable from the real world in all aspects. These results highlight the need to evaluate models across all four dimensions—Video Quality, Instruction Understanding, Physical Law, and Planning Reasoning—as each captures a distinct failure mode in embodied video generation. Additional qualitative examples are included in the Appendix 11. 

**Human Evaluation.** To assess the validity of our evaluation metric, we conduct a human study with 15 domain experts, who rated over 1,200 videos, both real and generated, along four core dimensions that mirror our benchmark and examine the alignment between **WoW-World-Eval** and human judgment. As shown in Figure 3b, both Pearson(r) and Spearman ( _ρ_ ) correlations are reported for the Overall Score and Human Eval Score. 

Results show a strong consistency between metric-based and human evaluations. The Overall Score demonstrates very strong Pearson and Spearman correlation with human judgment (r = 0.93, _ρ_ = 0.91), confirming that our benchmark provides a reliable and effective human-aligned evaluation of video generation performance. 

### **4.4. Turing Test** 

To demonstrate that our benchmark can serve as a principled foundation for Turing-test evaluations—and that performance on the benchmark is strongly correlated with outcomes in such Turing tests—while also addressing two remaining questions about embodied world models, we design and implement two complementary Turing Tests: _Human Turing Test_ and _Inverse Dynamic Model Turing Test_ . 

**Human Turing Test.** Figure 4 examines how **WoWWorld-Eval** scores relate to the Deceive Human Ratio, measured by asking 13 participants to distinguish real videos from generated ones, which shows that models with 

higher overall scores consistently achieve higher deceivehuman ratios, indicating stronger perceptual realism. For example, Hailuo and the WoW-cosmos2 variants are the most effective at fooling humans, consistent with their strong performance on our benchmark. This trend is statistically validated: the deceive-human ratio is strongly correlated with our Overall score (r = 0.679), meaning models that perform well on the benchmark are also more likely to fool humans. Breaking down by dimensions, Video Quality (r = 0.874) and Physical Law (r = 0.753) exhibit the highest correlations, showing that realism in both appearance and physical dynamics is what most convinces humans. 

These results reveal a core insight: both visual quality and physical plausibility are essential for generated videos to appear real to humans. Videos lacking either fidelity or correct physics fail to deceive observers. This strong alignment with human perception underscores that quality and physics are indispensable components of an embodied world model benchmark. 


Figure 4. **Trending between WoW-World-Eval Overall Score and Deceive Human Ratio.** 

9 

**Inverse Dynamic Model Turing Test.** We further introduce a Machine Turing Test using a real-world–trained Inverse Dynamics Model (IDM), GC-IDM [17], to evaluate whether generated videos exhibit physically executable dynamics. We collect 9 different manipulation tasks, from easy to hard, for evaluation. Details are in Appendix 10.3 

As shown in Table 5, most high-scoring models on **WoW-World-Eval** still fail this test: Kling (9.88%), Hailuo (2.47%), and early open-source models all perform near 0%, revealing that visual realism alone is insufficient for embodied execution. Models with real-robot data transfer significantly better—WoW-wan (40.74%) and WoWcosmos2 (18.52%)—consistent with their strong Physical Law and Instruction Understanding scores. 

These results highlight that: (i) The success rate of the generated videos on real robots is also correlated with our benchmark scores. (ii) Passing the IDM Turing Test requires both physics-grounded modeling and real-world exposure, emphasizing that true embodied competence goes beyond appearance quality. (iii) The videos generated by current embodied world models still have a significant gap from the real physical world. 

Table 5. **Execution Accuracy on real world by Inverse Dynamic Model.** All metrics: higher is better. Best results are **bold** with green highlight. Succ. Rate stands for Real-world success rate 

|**Model**|**Real-world Succ. Rate (%)**|
|---|---|
|**Kling**|9.88|
|**Hailuo**|2.47|
|**CogVideoX**|0.00|
|**Cosmos-Predict1**|0.00|
|**Wan2.1**|0.00|
|**Cosmos-Predict2**|8.64|
|**WoW-wan**|**40.74**|
|**WoW-cosmos2**|18.52|


## **5. Conclusion** 

In this work, we present **WoW-World-Eval** , a comprehensive benchmark designed as a Turing Test for evaluating video foundation models in embodied AI. By combining fine-grained human preference assessments and the Inverse Dynamics Model (IDM), we provide a dual-perspective evaluation framework that examines both perceptual realism and physical executability. Through extensive experiments on 609 real-world robot manipulation data, we reveal that while some models achieve high perceptual fidelity, they struggle with long-horizon reasoning and real-world execution, often collapsing under the IDM Turing Test. These findings highlight a substantial gap between visual generation and embodied action, pointing to the urgent need 

for more physically grounded, generalizable world models for robotics. We hope our benchmark will serve as a foundation for future progress in building robust, general-purpose embodied intelligence. 

## **6. Acknowledge** 

This work was supported by the National Natural Science Foundation of China (62476011), and by the Beijing Natural Science Foundation (L252060). 

## **References** 

- [1] Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 7, 1 

- [2] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang, Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5-vl technical report, 2025. 6 

- [3] Philip J. Ball, Jakob Bauer, Frank Belletti, Bethanie Brownfield, Ariel Ephrat, Shlomi Fruchter, Agrim Gupta, Kristian Holsheimer, Aleksander Holynski, Jiri Hron, Christos Kaplanis, Marjorie Limont, Matt McGill, Yanko Oliveira, Jack Parker-Holder, Frank Perbet, Guy Scully, Jeremy Shar, Stephen Spencer, Omer Tov, Ruben Villegas, Emma Wang, Jessica Yung, Cip Baetu, Jordi Berbel, David Bridson, Jake Bruce, Gavin Buttimore, Sarah Chakera, Bilva Chandra, Paul Collins, Alex Cullum, Bogdan Damoc, Vibha Dasagi, Maxime Gazeau, Charles Gbadamosi, Woohyun Han, Ed Hirst, Ashyana Kachra, Lucie Kerley, Kristian Kjems, Eva Knoepfel, Vika Koriakin, Jessica Lo, Cong Lu, Zeb Mehring, Alex Moufarek, Henna Nandwani, Valeria Oliveira, Fabio Pardo, Jane Park, Andrew Pierson, Ben Poole, Helen Ran, Tim Salimans, Manuel Sanchez, Igor Saprykin, Amy Shen, Sailesh Sidhwani, Duncan Smith, Joe Stanton, Hamish Tomlinson, Dimple Vijaykumar, Luyu Wang, Piers Wingfield, Nat Wong, Keyang Xu, Christopher Yew, Nick Young, Vadim Zubov, Douglas Eck, Dumitru Erhan, Koray Kavukcuoglu, Demis Hassabis, Zoubin Gharamani, Raia Hadsell, Aäron van den Oord, Inbar Mosseri, Adrian Bolton, Satinder Singh, and Tim Rocktäschel. Genie 3: A new frontier for world models. 2025. 1 

- [4] Hritik Bansal, Zongyu Lin, Tianyi Xie, Zeshun Zong, Michal Yarom, Yonatan Bitton, Chenfanfu Jiang, Yizhou Sun, Kai-Wei Chang, and Aditya Grover. Videophy: Evaluating physical commonsense for video generation. _arXiv preprint arXiv:2406.03520_ , 2024. 3, 4 

- [5] Hritik Bansal, Clark Peng, Yonatan Bitton, Roman Goldenberg, Aditya Grover, and Kai-Wei Chang. Videophy-2: A challenging action-centric physical commonsense evalua- 

10 

tion in video generation. _arXiv preprint arXiv:2503.06800_ , 2025. 6 

- [6] Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 1 

- [7] Tim Brooks, Bill Peebles, Connor Holmes, Will DePue, Yufei Guo, and OpenAI. Video generation models as world simulators. Technical report, OpenAI, 2024. Sora. 4, 1 

- [8] Jake Bruce, Michael D Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 1 

- [9] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 1 

- [10] Yi Chen, Yuying Ge, Yixiao Ge, Mingyu Ding, Bohao Li, Rui Wang, Ruifeng Xu, Ying Shan, and Xihui Liu. Egoplan-bench: Benchmarking multimodal large language models for human-level planning, 2024. 4 

- [11] Zixuan Chen, Jing Huo, Yangtao Chen, and Yang Gao. Robohorizon: An llm-assisted multi-view world model for long-horizon robotic manipulation, 2025. 1 

- [12] Sijie Cheng, Kechen Fang, Yangyang Yu, Sicheng Zhou, Bohao Li, Ye Tian, Tingguang Li, Lei Han, and Yang Liu. Videgothink: Assessing egocentric video understanding capabilities for embodied ai, 2024. 4 

- [13] Sijie Cheng, Zhicheng Guo, Jingwen Wu, Kechen Fang, Peng Li, Huaping Liu, and Yang Liu. Egothink: Evaluating first-person perspective thinking capability of visionlanguage models, 2024. 4 

- [14] Zhili Cheng, Yuge Tu, Ran Li, Shiqi Dai, Jinyi Hu, Shengding Hu, Jiahao Li, Yang Shi, Tianyu Yu, Weize Chen, Lei Shi, and Maosong Sun. Embodiedeval: Evaluate multimodal llms as embodied agents, 2025. 4 

- [15] Xiaowei Chi, Chun-Kai Fan, Hengyuan Zhang, Xingqun Qi, Rongyu Zhang, Anthony Chen, Chi-min Chan, Wei Xue, Qifeng Liu, Shanghang Zhang, et al. Eva: An embodied world model for future video anticipation. _arXiv preprint arXiv:2410.15461_ , 2024. 1, 3, 4 

- [16] Xiaowei Chi, Kuangzhi Ge, Jiaming Liu, Siyuan Zhou, Peidong Jia, Zichen He, Yuzhen Liu, Tingguang Li, Lei Han, Sirui Han, Shanghang Zhang, and Yike Guo. Mind: Learning a dual-system world model for real-time planning and implicit risk analysis, 2025. 1 

- [17] Xiaowei Chi, Peidong Jia, Chun-Kai Fan, Xiaozhu Ju, Weishi Mi, Kevin Zhang, Zhiyuan Qin, Wanxin Tian, Kuangzhi Ge, Hao Li, et al. Wow: Towards a world omniscient world model through embodied interaction. _arXiv preprint arXiv:2509.22642_ , 2025. 1, 4, 7, 10, 2 

- [18] Wei Chow, Jiageng Mao, Boyi Li, Daniel Seita, Vitor Guizilini, and Yue Wang. Physbench: Benchmarking and enhancing vision-language models for physical world understanding. _arXiv preprint arXiv:2501.16411_ , 2025. 3, 4, 6 

- [19] Daniel Cores, Michael Dorkenwald, Manuel Mucientes, Cees G. M. Snoek, and Yuki M. Asano. Lost in time: A new temporal benchmark for videollms, 2025. 6 

- [20] Sudeep Dasari, Frederik Ebert, Stephen Tian, Suraj Nair, Bernadette Bucher, Karl Schmeckpeper, Siddharth Singh, Sergey Levine, and Chelsea Finn. Robonet: Large-scale multi-robot learning. _arXiv preprint arXiv:1910.11215_ , 2019. 1 

- [21] Jingtao Ding, Yunke Zhang, Yu Shang, Yuheng Zhang, Zefang Zong, Jie Feng, Yuan Yuan, Hongyuan Su, Nian Li, Nicholas Sukiennik, et al. Understanding world or predicting future? a comprehensive survey of world models. _ACM Computing Surveys_ , 58(3):1–38, 2025. 1 

- [22] Ivan Dokmanic, Reza Parhizkar, Juri Ranieri, and Martin Vetterli. Euclidean distance matrices: Essential theory, algorithms, and applications. _IEEE Signal Processing Magazine_ , 32(6):12–30, 2015. 6 

- [23] Mengfei Du, Binhao Wu, Zejun Li, Xuanjing Huang, and Zhongyu Wei. Embspatial-bench: Benchmarking spatial understanding for embodied tasks with large visionlanguage models, 2024. 4 

- [24] Haoyi Duan, Hong-Xing Yu, Sirui Chen, Li Fei-Fei, and Jiajun Wu. Worldscore: A unified evaluation benchmark for world generation, 2025. 4 

- [25] Thomas Eiter and Heikki Mannila. Computing discrete fréchet distance. In _Technical Report CD-TR 94/64, Christian Doppler Laboratory for Expert . . ._ , 1994. 6 

- [26] Tiehan Fan, Kepan Nan, Rui Xie, Penghao Zhou, Zhenheng Yang, Chaoyou Fu, Xiang Li, Jian Yang, and Ying Tai. Instancecap: Improving text-to-video generation via instanceaware structured caption. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 28974– 28983, 2025. 8 

- [27] Fernando A. Fardo, Victor H. Conforto, Francisco C. de Oliveira, and Paulo S. Rodrigues. A formal evaluation of psnr as quality measurement parameter for image segmentation algorithms, 2016. 2, 5 

- [28] Gustav Theodor Fechner. _Elemente der psychophysik_ . Breitkopf u. Härtel, 1860. 3 

- [29] Weixi Feng, Jiachen Li, Michael Saxon, Tsu-jui Fu, Wenhu Chen, and William Yang Wang. Tc-bench: Benchmarking temporal compositionality in text-to-video and image-tovideo generation. _arXiv preprint arXiv:2406.08656_ , 2024. 1, 3 

- [30] Stephanie Fu, Netanel Tamir, Shobhita Sundaram, Lucy Chai, Richard Zhang, Tali Dekel, and Phillip Isola. Dreamsim: Learning new dimensions of human visual similarity using synthetic data, 2023. 5 

- [31] Xiao Fu, Xintao Wang, Xian Liu, Jianhong Bai, Runsen Xu, Pengfei Wan, Di Zhang, and Dahua Lin. Learning video generation for robotic manipulation with collaborative trajectory control. _arXiv preprint arXiv:2506.01943_ , 2025. 1 

- [32] Pascale Fung, Yoram Bachrach, Asli Celikyilmaz, Kamalika Chaudhuri, Delong Chen, Willy Chung, Emmanuel Dupoux, Hongyu Gong, Hervé Jégou, Alessandro Lazaric, et al. Embodied ai agents: Modeling the world. _arXiv preprint arXiv:2506.22355_ , 2025. 1 

11 

- [33] James J Gibson. The theory of affordances:(1979). In _The people, place, and space reader_ , pages 56–60. Routledge, 2014. 4 

- [34] Yanjiang Guo, Lucy Xiaoyang Shi, Jianyu Chen, and Chelsea Finn. Ctrl-world: A controllable generative world model for robot manipulation. _arXiv preprint arXiv:2510.10125_ , 2025. 1 

- [35] David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2(3), 2018. 1 

- [36] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 1 

- [37] Zihao He, Bo Ai, Tongzhou Mu, Yulin Liu, Weikang Wan, Jiawei Fu, Yilun Du, Henrik I Christensen, and Hao Su. Scaling cross-embodiment world models for dexterous manipulation. _arXiv preprint arXiv:2511.01177_ , 2025. 1 

- [38] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 

1 

- [39] Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al. Gpt-4o system card. _arXiv preprint arXiv:2410.21276_ , 2024. 5 

- [40] Pengliang Ji, Chuyang Xiao, Huilin Tai, and Mingxiao Huo. T2vbench: Benchmarking temporal dynamics for text-to-video generation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 5325–5335, 2024. 1, 3 

- [41] Yuxin Jiang, Shengcong Chen, Siyuan Huang, Liliang Chen, Pengfei Zhou, Yue Liao, Xindong He, Chiming Liu, Hongsheng Li, Maoqing Yao, et al. Enerverse-ac: Envisioning embodied environments with action condition. _arXiv preprint arXiv:2505.09723_ , 2025. 1 

- [42] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, Peter David Fagan, Joey Hejna, Masha Itkina, Marion Lepert, Yecheng Jason Ma, Patrick Tree Miller, Jimmy Wu, Suneel Belkhale, Shivin Dass, Huy Ha, Arhan Jain, Abraham Lee, Youngwoon Lee, Marius Memmel, Sungjae Park, Ilija Radosavovic, Kaiyuan Wang, Albert Zhan, Kevin Black, Cheng Chi, Kyle Hatch, Shan Lin, Jingpei Lu, Jean Mercat, Abdul Rehman, Pannag R. Sanketi, Archit Sharma, Cody Simpson, Quan Vuong, Homer Rich Walke, Blake Wulfe, Ted Xiao, Jonathan Heewon Yang, Arefeh Yavary, Tony Z. Zhao, Christopher Agia, Rohan Baijal, Mateo Guaman Castro, Daphne Chen, Qiuyu Chen, Trinity Chung, Jaimyn Drake, Ethan Paul Foster, Jensen Gao, David Antonio Herrera, Minho Heo, Kyle Hsu, Jiaheng Hu, Donovon Jackson, Charlotte Le, Yunshuang Li, Kevin Lin, Roy Lin, Zehan Ma, Abhiram Maddukuri, Suvir Mirchandani, Daniel Morton, Tony Nguyen, Abigail O’Neill, and Rosario Scalise. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 5 

- [43] Po-Chen Ko, Jiayuan Mao, Yilun Du, Shao-Hua Sun, and Joshua B Tenenbaum. Learning to Act from Actionless Videos through Dense Correspondences. _arXiv:2310.08576_ , 2023. 1, 10 

- [44] Benno Krojer, Mojtaba Komeili, Candace Ross, Quentin Garrido, Koustuv Sinha, Nicolas Ballas, and Mahmoud Assran. A shortcut-aware video-qa benchmark for physical understanding via minimal video pairs, 2025. 6 

- [45] Kuaishou. Kling, 2025. https://app.klingai.com/cn/. 7, 1 

- [46] Dacheng Li, Yunhao Fang, Yukang Chen, Shuo Yang, Shiyi Cao, Justin Wong, Michael Luo, Xiaolong Wang, Hongxu Yin, Joseph E Gonzalez, et al. Worldmodelbench: Judging video generation models as world models. _arXiv preprint arXiv:2502.20694_ , 2025. 1, 3, 4 

- [47] Hengtao Li, Pengxiang Ding, Runze Suo, Yihao Wang, Zirui Ge, Dongyuan Zang, Kexian Yu, Mingyang Sun, Hongyin Zhang, Donglin Wang, et al. Vlarft: Vision-language-action reinforcement fine-tuning with verified rewards in world simulators. _arXiv preprint arXiv:2510.00406_ , 2025. 1 

- [48] Jinming Li, Yichen Zhu, Zhiyuan Xu, Jindong Gu, Minjie Zhu, Xin Liu, Ning Liu, Yaxin Peng, Feifei Feng, and Jian Tang. Mmro: Are multimodal llms eligible as the brain for in-home robotics?, 2024. 4 

- [49] Xinqing Li, Xin He, Le Zhang, and Yun Liu. A comprehensive survey on world models for embodied ai. _arXiv preprint arXiv:2510.16732_ , 2025. 1 

- [50] Ying Li, Xiaobao Wei, Xiaowei Chi, Yuming Li, Zhongyu Zhao, Hao Wang, Ningning Ma, Ming Lu, and Shanghang Zhang. Manipdreamer: Boosting robotic manipulation world model with action tree and visual guidance. _arXiv preprint arXiv:2504.16464_ , 2025. 1 

- [51] Ying Li, Xiaobao Wei, Xiaowei Chi, Yuming Li, Zhongyu Zhao, Hao Wang, Ningning Ma, Ming Lu, and Shanghang Zhang. Manipdreamer3d: Synthesizing plausible robotic manipulation video with occupancy-aware 3d trajectory. _arXiv preprint arXiv:2509.05314_ , 2025. 1 

- [52] Yue Liao, Pengfei Zhou, Siyuan Huang, Donglin Yang, Shengcong Chen, Yuxin Jiang, Yue Hu, Jingbin Cai, Si Liu, Jianlan Luo, Liliang Chen, Shuicheng Yan, Maoqing Yao, and Guanghui Ren. Genie envisioner: A unified world foundation platform for robotic manipulation, 2025. 1 

- [53] Xinran Ling, Chen Zhu, Meiqi Wu, Hangyu Li, Xiaokun Feng, Cundian Yang, Aiming Hao, Jiashu Zhu, Jiahong Wu, and Xiangxiang Chu. Vmbench: A benchmark for perception-aligned video motion generation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 13087–13098, 2025. 1, 3 

- [54] Yaofang Liu, Xiaodong Cun, Xuebo Liu, Xintao Wang, Yong Zhang, Haoxin Chen, Yang Liu, Tieyong Zeng, Raymond Chan, and Ying Shan. Evalcrafter: Benchmarking and evaluating large video generation models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 22139–22149, 2024. 1, 3 

- [55] Yuanxin Liu, Shicheng Li, Yi Liu, Yuxiang Wang, Shuhuai Ren, Lei Li, Sishuo Chen, Xu Sun, and Lu Hou. Tempcompass: Do video llms really understand videos?, 2024. 6 

12 

- [56] Xiaoxiao Long, Qingrui Zhao, Kaiwen Zhang, Zihao Zhang, Dingrui Wang, Yumeng Liu, Zhengjie Shu, Yi Lu, Shouzheng Wang, Xinzhe Wei, et al. A survey: Learning embodied intelligence from physical simulators and world models. _arXiv preprint arXiv:2507.00917_ , 2025. 1 

- [57] Yulin Luo, Chun-Kai Fan, Menghang Dong, Jiayu Shi, Mengdi Zhao, Bo-Wen Zhang, Cheng Chi, Jiaming Liu, Gaole Dai, Rongyu Zhang, et al. Robobench: A comprehensive evaluation benchmark for multimodal large language models as embodied brain. _arXiv preprint arXiv:2510.17801_ , 2025. 4, 6 

- [58] Arjun Majumdar, Anurag Ajay, Xiaohan Zhang, Pranav Putta, Sriram Yenamandra, Mikael Henaff, Sneha Silwal, Paul Mcvay, Oleksandr Maksymets, Sergio Arnaud, Karmesh Yadav, Qiyang Li, Ben Newman, Mohit Sharma, Vincent Berges, Shiqi Zhang, Pulkit Agrawal, Yonatan Bisk, Dhruv Batra, Mrinal Kalakrishnan, Franziska Meier, Chris Paxton, Alexander Sax, and Aravind Rajeswaran. Openeqa: Embodied question answering in the era of foundation models. In _2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 16488–16498, 2024. 4 

- [59] Fanqing Meng, Jiaqi Liao, Xinyu Tan, Wenqi Shao, Quanfeng Lu, Kaipeng Zhang, Yu Cheng, Dianqi Li, Yu Qiao, and Ping Luo. Towards world simulator: Crafting physical commonsense-based benchmark for video generation. _arXiv preprint arXiv:2410.05363_ , 2024. 3, 4 

- [60] MiniMax. Hailuo, 2025. https://hailuoai.video/. 7, 1 

- [61] Saman Motamed, Laura Culp, Kevin Swersky, Priyank Jaini, and Robert Geirhos. Do generative video models understand physical principles? _arXiv preprint arXiv:2501.09038_ , 2025. 3, 4 

- [62] Meinard Müller. _Dynamic Time Warping_ , pages 69–84. Springer Berlin Heidelberg, Berlin, Heidelberg, 2007. 6 

- [63] Soroush Nasiriany, Sean Kirmani, Tianli Ding, Laura Smith, Yuke Zhu, Danny Driess, Dorsa Sadigh, and Ted Xiao. Rt-affordance: Affordances are versatile intermediate representations for robot manipulation. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8249–8257. IEEE, 2025. 4 

- [64] Nvidia. Cosmos-predict2, 2025. https://research.nvidia.com/labs/dir/cosmos-predict2/. 7, 1 

- [65] Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy V. Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, Mahmoud Assran, Nicolas Ballas, Wojciech Galuba, Russell Howes, Po-Yao Huang, Shang-Wen Li, Ishan Misra, Michael Rabbat, Vasu Sharma, Gabriel Synnaeve, Hu Xu, Hervé Jegou, and Julien Mairal. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 2, 5 

- [66] Jing-Cheng Pang, Nan Tang, Kaiyuan Li, Yuting Tang, XinQiang Cai, Zhen-Yu Zhang, Gang Niu, Masashi Sugiyama, and Yang Yu. Learning view-invariant world models for visual robotic manipulation. In _The Thirteenth International Conference on Learning Representations_ , 2025. 1 

- [67] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 4195– 4205, 2023. 1 

- [68] Yiran Qin, Zhelun Shi, Jiwen Yu, Xijun Wang, Enshen Zhou, Lijun Li, Zhenfei Yin, Xihui Liu, Lu Sheng, Jing Shao, Lei Bai, Wanli Ouyang, and Ruimao Zhang. Worldsimbench: Towards video generation models as world simulators, 2024. 4 

- [69] Julian Quevedo, Percy Liang, and Sherry Yang. Evaluating robot policies in a world model. _arXiv preprint arXiv:2506.00613_ , 2025. 1 

- [70] Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman Rädle, Chloe Rolland, Laura Gustafson, et al. Sam 2: Segment anything in images and videos. _arXiv preprint arXiv:2408.00714_ , 2024. 6 

- [71] Tianhe Ren, Shilong Liu, Ailing Zeng, Jing Lin, Kunchang Li, He Cao, Jiayu Chen, Xinyu Huang, Yukang Chen, Feng Yan, Zhaoyang Zeng, Hao Zhang, Feng Li, Jie Yang, Hongyang Li, Qing Jiang, and Lei Zhang. Grounded sam: Assembling open-world models for diverse visual tasks, 2024. 5 

- [72] Unitree Robotics. Unifolm-wma-0: A world-model–action (wma) framework under the unifolm family. https:// unigen-x.github.io/unifolm-world-modelaction.github.io/, 2025. Accessed: YYYY-MMDD. 1 

- [73] Younggyo Seo, Junsu Kim, Stephen James, Kimin Lee, Jinwoo Shin, and Pieter Abbeel. Multi-view masked world models for visual robotic manipulation. In _Proceedings of the 40th International Conference on Machine Learning_ , pages 30613–30632. PMLR, 2023. 1 

- [74] Pierre Sermanet, Tianli Ding, Jeffrey Zhao, Fei Xia, Debidatta Dwibedi, Keerthana Gopalakrishnan, Christine Chan, Gabriel Dulac-Arnold, Sharath Maddineni, Nikhil J Joshi, Pete Florence, Wei Han, Robert Baruch, Yao Lu, Suvir Mirchandani, Peng Xu, Pannag Sanketi, Karol Hausman, Izhak Shafran, Brian Ichter, and Yuan Cao. Robovqa: Multimodal long-horizon reasoning for robotics, 2023. 4 

- [75] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 6 

- [76] Oriane Siméoni, Huy V. Vo, Maximilian Seitzer, Federico Baldassarre, Maxime Oquab, Cijo Jose, Vasil Khalidov, Marc Szafraniec, Seungeun Yi, Michaël Ramamonjisoa, Francisco Massa, Daniel Haziza, Luca Wehrstedt, Jianyuan Wang, Timothée Darcet, Théo Moutakanni, Leonel Sentana, Claire Roberts, Andrea Vedaldi, Jamie Tolan, John Brandt, Camille Couprie, Julien Mairal, Hervé Jégou, Patrick Labatut, and Piotr Bojanowski. Dinov3, 2025. 5 

- [77] Chan Hee Song, Valts Blukis, Jonathan Tremblay, Stephen Tyree, Yu Su, and Stan Birchfield. Robospatial: Teaching spatial understanding to 2d and 3d vision-language models for robotics, 2025. 4 

13 

- [78] Kaiyue Sun, Kaiyi Huang, Xian Liu, Yue Wu, Zihan Xu, Zhenguo Li, and Xihui Liu. T2v-compbench: A comprehensive benchmark for compositional text-to-video generation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 8406–8416, 2025. 3 

- [79] HunyuanWorld Team, Zhenwei Wang, Yuhao Liu, Junta Wu, Zixiao Gu, Haoyuan Wang, Xuhui Zuo, Tianyu Huang, Wenhuan Li, Sheng Zhang, et al. Hunyuanworld 1.0: Generating immersive, explorable, and interactive 3d worlds from words or pixels. _arXiv preprint arXiv:2507.21809_ , 2025. 1 

- [80] Wanxin Tian, Shijie Zhang, Kevin Zhang, Xiaowei Chi, Yulin Luo, Junyu Lu, Chunkai Fan, Qiang Zhou, Yiming Zhao, Ning Liu Siyu Lin, et al. Seea-r1: Tree-structured reinforcement fine-tuning for self-evolving embodied agents. _arXiv preprint arXiv:2506.21669_ , 2025. 4 

- [81] Thomas Unterthiner, Sjoerd Van Steenkiste, Karol Kurach, Raphael Marinier, Marcin Michalski, and Sylvain Gelly. Towards accurate generative models of video: A new metric & challenges. _arXiv preprint arXiv:1812.01717_ , 2018. 2, 5 

- [82] Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. _Advances in neural information processing systems_ , 30, 2017. 1 

- [83] Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu, Haiming Zhao, Jianxiao Yang, et al. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 7, 1 

- [84] Boyang Wang, Nikhil Sridhar, Chao Feng, Mark Van der Merwe, Adam Fishman, Nima Fazeli, and Jeong Joon Park. This&that: Language-gesture controlled video generation for robot planning. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 12842–12849. IEEE, 2025. 1 

- [85] Zixing Wang and Ahmed H Qureshi. Anypose: Anytime 3d human pose forecasting via neural ordinary differential equations. _arXiv preprint arXiv:2309.04840_ , 2023. 1 

- [86] Zhou Wang, A.C. Bovik, H.R. Sheikh, and E.P. Simoncelli. Image quality assessment: from error visibility to structural similarity. _IEEE Transactions on Image Processing_ , 13(4): 600–612, 2004. 2, 5 

- [87] Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che, Xiaozhu Ju, Zhuqin Yang, Meng Li, Yinuo Zhao, Zhiyuan Xu, Guang Yang, Shichao Fan, Xinhua Wang, Fei Liao, Zhen Zhao, Guangyu Li, Zhao Jin, Lecheng Wang, Jilei Mao, Ning Liu, Pei Ren, Qiang Zhang, Yaoxu Lyu, Mengzhen Liu, Jingyang He, Yulin Luo, Zeyu Gao, Chenxuan Li, Chenyang Gu, Yankai Fu, Di Wu, Xingyu Wang, Sixiang Chen, Zhenyu Wang, Pengju An, Siyuan Qian, Shanghang Zhang, and Jian Tang. Robomind: Benchmark on multiembodiment intelligence normative data for robot manipulation. In _Proceedings of Robotics: Science and Systems (RSS) 2025_ , 2025. 5 

- [88] Junjin Xiao, Yandan Yang, Xinyuan Chang, Ronghan Chen, Feng Xiong, Mu Xu, Wei-Shi Zheng, and Qing Zhang. World-env: Leveraging world model as a vir- 

   - tual environment for vla post-training. _arXiv preprint arXiv:2509.24948_ , 2025. 1 

- [89] Wilson Yan, Yunzhi Zhang, Pieter Abbeel, and Aravind Srinivas. Videogpt: Video generation using vq-vae and transformers. _arXiv preprint arXiv:2104.10157_ , 2021. 1 

- [90] Jihan Yang, Shusheng Yang, Anjali W. Gupta, Rilyn Han, Li Fei-Fei, and Saining Xie. Thinking in space: How multimodal large language models see, remember, and recall spaces, 2025. 4 

- [91] Rui Yang, Hanyang Chen, Junyu Zhang, Mark Zhao, Cheng Qian, Kangrui Wang, Qineng Wang, Teja Venkat Koripella, Marziyeh Movahedi, Manling Li, Heng Ji, Huan Zhang, and Tong Zhang. Embodiedbench: Comprehensive benchmarking multi-modal large language models for visiondriven embodied agents, 2025. 4 

- [92] Xiuyu Yang, Bohan Li, Shaocong Xu, Nan Wang, Chongjie Ye, Zhaoxi Chen, Minghan Qin, Yikang Ding, Xin Jin, Hang Zhao, et al. Orv: 4d occupancy-centric robot video generation. _arXiv preprint arXiv:2506.03079_ , 2025. 1 

- [93] Ze Yang, Yun Chen, Jingkang Wang, Sivabalan Manivasagam, Wei-Chiu Ma, Anqi Joyce Yang, and Raquel Urtasun. Unisim: A neural closed-loop sensor simulator. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 1389–1399, 2023. 1 

- [94] Zhuoyi Yang, Jiayan Teng, Wendi Zheng, Ming Ding, Shiyu Huang, Jiazheng Xu, Yuanming Yang, Wenyi Hong, Xiaohan Zhang, Guanyu Feng, et al. Cogvideox: Text-tovideo diffusion models with an expert transformer. _arXiv preprint arXiv:2408.06072_ , 2024. 7, 1 

- [95] Hu Yue, Siyuan Huang, Yue Liao, Shengcong Chen, Pengfei Zhou, Liliang Chen, Maoqing Yao, and Guanghui Ren. Ewmbench: Evaluating scene, motion, and semantic quality in embodied world models. _arXiv preprint arXiv:2505.09694_ , 2025. 1, 3, 4 

- [96] Yuan Zhang, Fei Xiao, Tao Huang, Chun-Kai Fan, Hongyuan Dong, Jiawen Li, Jiacong Wang, Kuan Cheng, Shanghang Zhang, and Haoyuan Guo. Unveiling the tapestry of consistency in large vision-language models. _Advances in Neural Information Processing Systems_ , 37: 118632–118653, 2024. 6 

- [97] Dian Zheng, Ziqi Huang, Hongbo Liu, Kai Zou, Yinan He, Fan Zhang, Lulu Gu, Yuanhan Zhang, Jingwen He, WeiShi Zheng, et al. Vbench-2.0: Advancing video generation benchmark suite for intrinsic faithfulness. _arXiv preprint arXiv:2503.21755_ , 2025. 1, 3, 4 

- [98] Hongyan Zhi, Peihao Chen, Siyuan Zhou, Yubo Dong, Quanxi Wu, Lei Han, and Mingkui Tan. 3dflowaction: Learning cross-embodiment manipulation from 3d flow world model. _arXiv preprint arXiv:2506.06199_ , 2025. 1 

- [99] Siyuan Zhou, Yilun Du, Jiaben Chen, Yandong Li, Dit-Yan Yeung, and Chuang Gan. Robodreamer: Learning compositional world models for robot imagination. _arXiv preprint arXiv:2404.12377_ , 2024. 1 

- [100] Fangqi Zhu, Hongtao Wu, Song Guo, Yuxiao Liu, Chilam Cheang, and Tao Kong. Irasim: Learning interactive realrobot action simulators. _arXiv preprint arXiv:2406.14540_ , 2024. 1 

14 

- [101] Jinguo Zhu, Weiyun Wang, Zhe Chen, Zhaoyang Liu, Shenglong Ye, Lixin Gu, Hao Tian, Yuchen Duan, Weijie Su, Jie Shao, et al. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models. _arXiv preprint arXiv:2504.10479_ , 2025. 8 

15 

# **Wow, wo, val! A Comprehensive Embodied World Model Evaluation Turing Test** 

# Supplementary Material 

## **7. More Related Works** 

## **8. Models Detail** 

**Video Generation Models.** The quest for scalable video synthesis has converged on two dominant architectures, both serving as backbones for predictive world modeling. 

**Autoregressive Transformers.** Inspired by Large Language Models, architectures like VideoGPT [89] treat video generation as a discrete sequence modeling task. By tokenizing frames via VQ-VAE [82], these models predict visual token sequence-by-sequence. This paradigm, akin to next-word prediction, naturally aligns with the statetransition logic of world models. Notable examples like Genie [8] utilize this spatiotemporal autoregressive objective to build interactive environments and predictive models from diverse video data. However, the discrete quantization often imposes an upper bound on visual fidelity, resulting in the loss of high-frequency details. 

**The Diffusion Paradigm.** Diffusion Models (DMs) have established a new state-of-the-art by formulating generation as iterative denoising. Early attempts like SVD [6] adapted 2D U-Nets with temporal layers, excelling at texture but often treating time as a secondary dimension. The recent shift to Diffusion Transformers (DiT) [67], exemplified by Wan [83], Cosmos [64], Sora [7], operates on unified spacetime patches. These models demonstrate emergent capabilities akin to a physics engine—simulating fluid dynamics and occlusion—making them ideal candidates for high-fidelity world simulation. 

**Embodied World Models.** Unlike passive video generation, embodied world models function as predictive engines ( _st_ +1 _|st, at_ ) to facilitate agent planning. 

**From Latent States to Pixel Space.** Early research balanced between efficiency and detail. The Dreamer series [36] prioritized computational tractability by learning dynamics in a compact latent space, enabling efficient RL planning but producing schematic visual reconstructions. Conversely, pixel-space approaches like RoboNet [20] predicted future frames directly from interaction logs. While capturing texture, these models often struggled with the stochastic nature of real-world physics, leading to blurry predictions over long horizons. 

**Generalist Simulators.** Recent efforts converge generative AI with robotics to create "Generalist Simulators." Foundation models like UniSim [93] and GAIA-1 [38] leverage internet-scale data to learn high-level physics for zero-shot generalization. 

Since the models have different versions and parameter sizes, and also generate videos of different durations and resolutions, we introduce the models we use, their specific versions and parameter counts, as well as the generated durations and resolutions, to facilitate comparison and reproduction. 

**Kling. [45]** A large-scale diffusion-transformer video generator known for photorealistic long-form outputs, strong motion control, and realistic physics. It employs a latent-space DiT architecture with 3D VAE compression and is optimized for high-consistency content such as sports or human motion. We used the latest Klingv2.1 to generate a 5-second 720p video. 

**Hailuo. [60]** Hailuo is a commercial text-to-video and image-to-video model designed for high-quality short-form generation (6–10 seconds, up to 1080p). It emphasizes photorealism, smooth motion, and subject consistency, making it a strong closed-source baseline for perceptual quality. We use the publicly accessible Hailuo-02 for 5-second 768p video generation and evaluation. 

**CogVideoX. [94]** An open diffusion-transformer video generator available in 2B/5B variants. It can produce 10second clips with improved motion expressiveness using a 3D causal VAE and MoE-style transformer backbone. The model supports both text-to-video and image-to-video generation and serves as a strong open-source baseline for long-duration video synthesis. For evaluation, we use CogVideoX-I2V-5B to generate 5-second 1360x768 videos. 

**Cosmos-Predict. [1, 64]** NVIDIA’s open-source worldmodel family for video-based state prediction. It supports Text-/Image-/Video-to-World forecasting and can generate long-horizon, physics-aware video rollouts. The model is trained on large-scale real-world videos and emphasizes dynamics, object permanence, and 3D geometry consistency. We evaluate both Cosmos-Predict1 and the stronger Cosmos-Predict2 variants. Both Predict1&2 are 5-second 720p, but the parameters of the model are 7B and 2B, respectively. 

**Wan. [83]** Wan is a series of open-source Diffusion Transformer video models (e.g., Wan 2.1/2.2) trained on 

1 

large-scale image–video corpora. They support text-tovideo and image-to-video generation, producing 5–10 second clips with strong spatial–temporal coherence. Wan models use 3D VAE compression and DiT backbones to improve motion consistency and are widely used as highquality open video generation baselines. We fix the resolution for a 5-second 832x480 generation with Wan2.1-I2V14B. 

**WoW. [17]** WoW is a 14B-parameter open-source embodied world model designed for physically grounded video prediction in robotic manipulation. It generates future video rollouts conditioned on visual observations and task instructions, with inductive biases (e.g., DINOv2 token distillation) that encourage spatial and physical consistency. Unlike generic video models, WoW explicitly targets planning, contact dynamics, and multi-step task execution. We use the different backbones of WoW, including Wan, CosmosPredict1, and Cosmos-Predict2, for evaluation; all generated video settings are the same as the backbone models. 

## **9. Detailed Metrics** 

### **9.1. Visual Fidelity.** 

To evaluate the visual fidelity of generated videos, we adopt a suite of complementary metrics that capture low-level reconstruction accuracy, perceptual similarity, and distributional realism. These include FVD, SSIM, PSNR, DINO, and DreamSim. 

**Peak signal-to-noise ratio (PSNR).** PSNR evaluates pixel-level fidelity via the mean squared error (MSE) between reference and generated frames: 


Higher PSNR generally indicates better reconstruction, although it is less aligned with human perception than SSIM or embedding-based metrics. 

**DINO Score.** DINOv2 is a self-supervised visual foundation model trained with large-scale teacher–student distillation. We compute the cosine similarity between DINOv2 embeddings of generated and reference frames: 


where _f_ ( _·_ ) denotes the DINOv2 encoder. Higher similarity indicates closer semantic and structural alignment. 

**DreamSim.** DreamSim combines CLIP, OpenCLIP, and DINO embeddings and is fine-tuned on human perceptual judgments to produce similarity scores aligned with human perception. For frames _x_ and _y_ : 


where _E_ ( _·_ ) is the fused embedding. 

### **9.2. Instruction Semantic Correctness.** 

**Fréchet Video Distance (FVD).** FVD is a distributionlevel metric that measures how closely generated video features match those of real videos. Given feature means and covariances ( _µr,_ Σ _r_ ) for real videos and ( _µg,_ Σ _g_ ) for generated videos extracted using an I3D network, FVD is defined as: 


Lower FVD indicates higher spatial-temporal coherence and distributional realism. 

**Structural Similarity Index measures (SSIM).** The Structural Similarity Index (SSIM) measures perceptual degradation in luminance, contrast, and structural information. For two frames _x_ and _y_ : 


where _µ_ and _σ_ denote means and variances of local patches. Higher SSIM corresponds to better perceptual consistency. 

These three scores—Caption Score, Sequence Match Score, and Execution Quality Score—allow us to evaluate instruction following in both supervised (with ground truth) and fully OOD settings. Empirically, all three metrics show strong agreement with human preference judgments, validating the reliability of our evaluation protocol. 

**Caption Score.** For samples paired with ground-truth videos, we obtain a structured semantic representation of each video. Using a templated prompt, GPT extracts a standardized caption containing: initial state, intermediate process, final state, object descriptions, and action descriptions. The same procedure is applied to the modelgenerated video. A vision–language model (VLM) compares the two captions along these five predefined components, assigning a score of 1 (match), 0.5 (partial match), or 0 (mismatch). The Caption Score is computed as the mean over the five components. 

**Sequence Match Score.** In this score, we directly analyze the alignment between the instruction and the actions depicted in the generated video. GPT identifies the sequence 

2 


Figure 5. **Overview of WoW-World-Eval Metrics.** 

of action–object pairs present in the video and aligns them with the intended execution order specified by the instruction. We measure the degree to which the extracted sequence preserves the correctness of both action selection and temporal ordering, again using a discrete scale of 1 (match), 0.5 (partial match), or 0 (mismatch). This yields the Sequence Match Score. 

**Execution Quality Score.** To further evaluate execution fidelity, we assess how completely the depicted actions are carried out. We employ a five-level rubric measuring the extent of object motion and action completion—from no meaningful change to full task completion. 

1. object does not move, and the action is not executed 

2. object slightly moves, or the action is partially executed 

3. object slightly moves, and the action is partially executed 

4. object reaches goal or action is fully executed 

5. object reaches goal and action is fully executed 

The score ranges from 1 to 5, producing the Execution Quality Score. This score captures the degree to which the video evidences a coherent and physically plausible execution of the instructed task. 

### **9.3. Mask-guided Regional Consistency.** 

**Setup.** We evaluate the mask-guided regional consistency of each model based on three core components, as illustrated in Figure 5: (1) _GroundingSAM-2_ for point-guided segmentation and multi-frame tracking; (2) _DINOv3-Large (standard)_ as a frozen visual encoder to extract patch-level features; (3) _Run-length Encoding (RLE)_ for storing region masks efficiently across all frames. 

then places _3–5 boundary points_ along the visible contour of each region (object and gripper). These point sets provide fine-grained localization cues and are passed to GroundingSAM-2, which returns segmentation masks for the first frame and tracks them throughout the video. For each frame _t_ , GroundingSAM-2 outputs an RLE mask for the object and an RLE mask for the gripper. If a region cannot be tracked in frame _t_ (due to occlusion or motion blur), we record its mask as an _all-zero RLE mask_ . The background region is defined as the complement of the union of the two tracked regions: 


Each RGB frame _It_ is encoded by DINOv3-Large to obtain a grid of patch features 


All masks are decoded from RLE and downsampled to ( _Hp, Wp_ ) so they can serve as per-patch weights. For each region _r ∈{_ obj _,_ arm _,_ bg _}_ we compute a normalized mask: 


which becomes all zero when the region is missing. A region feature is obtained via mask-weighted averaging: 


followed by _ℓ_ 2 normalization if **f** _t_<sup>r</sup> _̸_<sup>= 0.</sup> 

**Implementation.** We begin by manually identifying the first frame in which both the manipulated object and the robot gripper are clearly visible. A human annotator 

**Consistency Score.** We compute temporal consistency for each region separately using cosine similarity. Given 

3 

normalized region features<sup>˜</sup> **f** _t_<sup>r, the consistency between two</sup> frames _a_ and _b_ for region _r_ is 


For each frame _t ≥_ 2 and region _r ∈{_ obj _,_ arm _,_ bg _}_ , we combine long-range and short-range temporal coherence: 


The video-level Mask-guided Regional Consistency for region _r_ is then 


where _T_ is the number of frames. In practice, we report three separate scores 


corresponding to the manipulated object, the gripper, and the background, respectively. 

### **9.4. Trajectory-level Consistency.** 

We evaluate the trajectory-level consistency of each model by comparing the 2D motion trajectories of both the robot end-effector and manipulated objects in the generated videos against those in ground-truth (GT) videos. Human annotators first label representative keypoints on the robot arm and objects in the first frame; these serve as positive point prompts for SAM2 tracking, yielding dense and stable point tracks throughout the sequence, as illustrated in Figure 5. The per-frame trajectory is defined as the mean of the tracked keypoints, normalized to the range [0 _,_ 1]<sup>2</sup> . We align the number of frames of the generated video and the GT video to the smaller one by uniformly sampling. We then compute three complementary metrics—L2Norm Error, Dynamic Time Warping (DTW), and Fréchet Distance—for both the robot end-effector and the manipulated object. 

**Keypoint labeling and SAM2 tracking.** Given a video with frames _{It}_<sup>_T_</sup> _t_ =1<sup>,humanannotatorsplace</sup><sup>_N_represen-</sup> tative points on the robot end-effector or an object in the first frame: 


**Keypoint prompting and SAM2 mask tracking.** Given a video with frames _{It}_<sup>_T_</sup> _t_ =1<sup>,humanannotatorsplace</sup><sup>_N_</sup> representative points on the robot end-effector or an object 

in the first frame. These points serve as positive prompts for SAM2, which returns a binary segmentation mask for the object at each frame: 


Each mask **M**<sup>(</sup><sup>_t_)</sup> defines the set of foreground pixels 


**Mask-to-point trajectory conversion.** To obtain a 2D trajectory from the mask sequence, we compute the centroid of the foreground region: 


Let the video resolution be ( _W, H_ ). We then normalize all coordinates to [0 _,_ 1]<sup>2</sup> : 


This centroid simplification provides a stable 2D trajectory independent of resolution for each tracked component. 

**Camera-motion–aware trajectory correction.** In generated videos with unstable viewpoints, the observed endeffector trajectory entangles true robot motion with camera drift or jitter, leading to biased evaluations. To recover the actual end-effector motion, we subtract the estimated camera trajectory **c** _t_ from the observed end-effector trajectory **p** ˆ _t_ : 


This correction yields a cleaner and more comparable motion signal across videos. Empirically, smaller camera metrics ATE/RPE correspond to more reliable corrected trajectories, whereas larger camera errors introduce evaluation noise and indicate the need for improved video generation or stabilization. 

**Camera trajectory estimation.** Given a video, we uniformly sample frames _{It}_<sup>_T_</sup> _t_ =1<sup>anddetectsparseShi–</sup> Tomasi keypoints on the image boundary of the first frame 


where boundary regions are assumed to be dominated by a static background. We then track these keypoints across subsequent frames with pyramidal Lucas–Kanade optical flow, obtaining correspondences between a reference frame and frame _t_ : 


4 

For each frame _t_ , we robustly estimate a 2D affine transform (restricted to rotation/scale/translation) via RANSAC: 


where **t** _t_ = ( _tx, ty_ ) captures the apparent translation of the static background in the image plane. Because camera motion is opposite to background motion, we define the perframe camera displacement as 


Starting from **c** 1 = (0 _,_ 0), we accumulate these displacements over time, with an additional drift clipping to suppress implausibly large jumps between adjacent frames: 


where **c** _t_ = ( _xt, yt_ ) denotes the cumulative camera offset (in pixels) at frame _t_ relative to the first frame. The original frame resolution ( _W, H_ ) is stored together with the trajectory. 

**Temporal alignment and normalization across videos.** For a GT video and a generated video, we obtain two normalized trajectories: 


To compare two trajectories of different lengths, we first determine the target number of frames: 


We uniformly sample the longer trajectory to obtain exactly _T_ frames. Let the aligned trajectories be 


where _s_<sup>1</sup> and _s_<sup>2</sup> are the sampled indexes. 

**Absolute Trajectory Error (ATE).** ATE measures the absolute discrepancy between the generated and GT camera trajectories over the entire sequence. We define 


where _∥· ∥_ 2 denotes the L2 norm. A lower ATE indicates that the overall camera path in the generated video more closely follows the ground-truth trajectory in the image plane. 

**Relative Pose Error (RPE).** To evaluate the fidelity of _local_ camera motion (e.g., instantaneous velocity and direction), we compute the Relative Pose Error. For a temporal offset ∆ (we use ∆= 1 frame in our experiments), we define normalized relative motion as 


The RPE is then defined as 


RPE focuses on frame-to-frame motion consistency: lower values indicate that the generated video better matches the ground-truth in terms of local camera dynamics (e.g., smoothness, acceleration patterns, and motion direction). 

**L2Norm Error.** The per-frame L2Norm error measures instantaneous positional discrepancy: 


A lower ED indicates that the generated trajectory more closely follows the GT path frame by frame. 

**Dynamic Time Warping (DTW).** DTW preserves the shape similarity of two trajectories while allowing nonlinear temporal alignment. The DTW cost is defined as 


where _π_ is a monotonic warping path. Lower DTW values indicate higher similarity in trajectory geometry, regardless of speed variations. 

**Fréchet Distance.** The Fréchet Distance captures the minimum leash-length needed for two curves to be traversed in order, providing a strict measure of geometric similarity: 


where _α_ and _β_ are continuous, non-decreasing reparameterizations. Unlike DTW, the Fréchet metric enforces simultaneous forward progression along the curves. 

5 

### **9.5. Physical and Causal Reasoning.** 

#### **Base Model and Optimization Algorithm** 

To implement automated evaluation, we selected **Qwen2.5-VL (7B)** [2] as our base vision-language model. We employed the **GRPO** algorithm, optimizing the model through a two-stage fine-tuning process to equip it with precise physical commonsense understanding and scoring capabilities, as illustrated in Figure 5. 

#### **The GRPO Algorithm** 

GRPO optimizes the policy model _πθ_ by maximizing an objective that encourages high-reward outputs while maintaining stability via a clipping mechanism and KL-divergence regularization. 

For each input query _q_ , GRPO samples a group of outputs _{o_ 1 _, o_ 2 _, · · · , oG}_ from the old policy _πθold_ . The optimization objective is defined as: 


where _ε_ is the clipping hyperparameter, and _β_ controls the KL-divergence penalty with respect to the reference model _πref_ . 

The advantage _A_<sup>ˆ</sup> _i_ for the _i_ -th output is calculated based on the relative rewards within the sampled group. Specifically, assuming output _oi_ receives a reward score _ri_ , the advantage is computed by standardizing the rewards: 


This group-relative formulation serves as a dynamic baseline, effectively reducing variance without requiring a separate value network. 

#### **Stage 1: Foundational Video Understanding Fine-tuning** 

**Objective:** To imbue the model with a foundational understanding of physical events and causal relationships. **Data and Method:** We utilized a dataset of approximately 50,000 samples from six video understanding benchmarks. All data was formatted as multiple-choice Video Question Answering (VQA) tasks. 

- **Sampling:** For each video-question pair _q_ , we sampled a group of outputs of size _G_ = 8. 

- **Reward Calculation:** We implemented a rule-based reward function. If a sampled output _oi_ correctly matched the ground-truth option (e.g., "Option A"), it received a reward _ri_ = 1 _._ 0; otherwise, _ri_ = 0 _._ 0. 

- **Optimization:** The model was updated using the calculated group advantages to increase the probability of generating correct answers. 

**Results:** Stage 1 fine-tuning significantly improved the model’s video comprehension abilities. On a comprehensive held-out test set from these benchmarks, the model’s average accuracy increased from **60.83%** (the Qwen-2.5VL 7B backbone) to **71.51%** . 

#### **Stage 2: Scoring Alignment Fine-tuning** 

**Objective:** To train the model to follow instructions and output quantitative 1-5 scores for four dimensions in a JSON format, aligning with human-annotated standards. **Method:** We continued to use the GRPO algorithm, fine-tuning on our internally annotated dataset of 1,297 data points. We used the following prompt template to guide the model in generating the scoring JSON. **Reward Function:** In Stage 2, the GRPO optimization objective was to maximize the expectation of a reward function _R_ ( _yout, ygt_ ), which quantifies the alignment between the model-generated JSON _yout_ and the ground-truth humanannotated JSON _ygt_ . 

The reward _R_ is calculated as follows: 

1. Parse the JSON objects from _yout_ and _ygt_ . 

2. Let _K_ be the set of four evaluation keys (i.e., video_quality, instruction_following, physical_consistency, planning_logic). 

3. For each key _k ∈K_ present in _ygt_ , if _k_ is also present in _yout_ , calculate the normalized absolute error _ek_ . 

4. Before calculating _ek_ , the scores _s_<sup>_gt_</sup> _k_<sup>from</sup><sup>_ygt_and</sup><sup>_s_</sup> _k_<sup>_out_</sup> from _yout_ are clipped to the valid range [1 _._ 0 _,_ 5 _._ 0], yielding _s_<sup>_′_</sup> _k_<sup>_gt_</sup> and _s_<sup>_′_</sup> _k_<sup>_out_</sup> . 

5. The normalized absolute error _ek_ is defined as: 


The denominator 4.0 (i.e., 5 _−_ 1) normalizes the error to the range [0 _._ 0 _,_ 1 _._ 0]. 

6. The mean error _e_ ¯ is calculated over all matched keys _Kmatch ⊆K_ : 


7. The final reward _R_ is defined as 1 _._ 0 _− e_ ¯ and clipped to [0 _._ 0 _,_ 1 _._ 0]: 

   - _R_ ( _yout, ygt_ ) = max(0 _._ 0 _,_ min(1 _._ 0 _,_ 1 _._ 0 _− e_ ¯)) (5) 

If _yout_ or _ygt_ are not valid JSON, or if _Kmatch_ is empty, the reward _R_ = 0 _._ 0. 

6 

#### **Final Inference for Evaluation** 

After completing the two-stage fine-tuning, we obtained an evaluation model with a strong understanding of physical common sense (from S1) and the ability to perform structured scoring tasks (from S2). For the final automated evaluation in our paper, we employed a detailed, zero-shot inference prompt. This prompt instructs the model to focus _exclusively_ on physical plausibility, refining its evaluation criteria into the six dimensions used in our main analysis. 

### **9.6. Overall Benchmark Score.** 

We normalize all metrics to a unified three-digit scale of 0–100 to ensure consistent interpretation and cross-metric comparability. Metrics that naturally fall within this range are retained as-is. For the remaining metrics (including FVD and PSNR, we fix their boundaries up to 2000 and 50, respectively), we first map their values to [0,1], then apply a monotonic transformation, and finally scale the result to [0,100]. 

To determine the optimal mapping method and parameter for each metric, we use a subset of human evaluation scores as supervision. Specifically, we apply different values within a grid over [0,5], compute the Pearson correlation between the transformed metric scores and human ratings, and select the method and parameter that maximizes this correlation. 

**Parametric mappings.** After pre-scaling, we apply a single-parameter monotone transform _fm_ ( _·_ ; _θm_ ) and then rescale to (0 _,_ 100): 


We consider the following families (all are strictly increasing on [0 _,_ 1]): 


In practice, _γ >_ 1 accentuates the high end, while _T <_ 1 or _κ >_ 1 expands the mid-range and compresses extremes. For numerical stability with logit we use a small _ε_ (e.g., 10<sup>_−_6</sup> ) and replace _x_ by clip( _x_ ; _ε,_ 1 _− ε_ ) only inside logit( _·_ ). 

**Parameter selection and freezing.** For each metric _m_ , _θm ∈{γ, T, κ}_ is selected on a fixed development set by maximizing the Fisher- _z_ averaged Pearson correlation between _fm_ (ˆ _x_ ; _θ_ ) and human ratings across _K_ -fold CV; Spearman correlation is used as a tie-breaker. The chosen _θm_ is then _frozen_ and applied to all evaluations. 

The resulting mapping methods and _θm_ values for all metrics _m_ are summarized in Table 6. 

Table 6. **The mapping parameters for all the metrics.** 

|**Metric**|**Mapping**|**Parameter**|
|---|---|---|
|**FVD**|gamma|1.52|
|**PSNR**|tanh|4.71|
|**SSIM**|gamma|0.61|
|**DINO**|gamma|3.06|
|**DreamSim**|gamma|2.94|
|**Caption Score**|gamma|0.12|
|**Seq. Match Score**|gamma|2.45|
|**Exec. Qual Score**|gamma|2.97|
|**Planning DAG**|simple|-|
|**Robot Con.**|gamma|2.93|
|**Obj. Con.**|tanh|4.93|
|**Scene Con.**|gamma|3.94|
|**Robot Traj. L2norm**|gamma|2.86|
|**Robot Traj. DTW**|gamma|1.87|
|**Robot Traj. FD**|gamma|4.00|
|**Obj. Traj. L2norm**|gamma|1.27|
|**Obj. Traj. DTW**|gamma|2.99|
|**Obj. Traj. FD**|gamma|3.52|
|**Physical Score**|simple|-|
|**Cam. ATE**|simple|-|
|**Cam. RPE**|simple|-|


## **10. Extended Experiment Analysis** 

### **10.1. WoW-World-Eval Human Evaluation Rule** 

We evaluate generated videos along four independent dimensions: Video Quality, Instruction Understanding, Physical Law, and Planning. Each dimension is scored on a 1–5 scale, and the Overall Score is defined as the sum of the four scores (range: 4–20). All dimensions are assessed independently. 

**Video Quality.** This dimension assesses the perceptual integrity of the video itself, independent of task correctness or physical feasibility. The focus is strictly on the clarity, stability, and visibility of the content presented. Scoring Criteria will be as follows: 

#### **5 — Excellent** 

- High spatial clarity with sharp and stable rendering 

- Proper exposure and color balance; no notable artifacts or noise 

- All key elements remain continuously visible 

- No distracting visual irregularities 

   - **4 — Good** 

7 

- Minor imperfections (e.g., slight blur, mild exposure fluctuation, low-level noise) 

- Overall visibility remains unaffected 

#### **3 — Fair** 

- Multiple noticeable issues, including moderate blur, frequent autofocus/exposure changes, or significant noise 

- Occasional hindrance to understanding the scene 

- Overall content remains interpretable 

#### **2 — Poor** 

- Significant visual defects: strong blur, over/underexposure, instability, occlusion of key regions 

- Compression artifacts or frame drops are obvious and disruptive 

- Core task content is frequently hard to interpret 

   - **1 — Unusable** 

- Severe degradation: extreme darkness/brightness, pervasive blur, heavy artifacts, or constant frame loss 

- Critical task elements cannot be identified 

- The video cannot support meaningful evaluation 

#### **5 — Fully Physical** 

- All motions are dynamically coherent and physically plausible 

- Object interactions follow realistic physical responses 

- No penetration artifacts or implausible transitions 

- A completely static video (identical to the first frame) is also scored as 5, as it contains no physical violations 

#### **4 — Mostly Physical** 

- Minor deviations from realistic physics, but overall behavior remains plausible 

- No significant physical inconsistencies 

   - **3 — Moderately Physical** 

- Noticeable but non-catastrophic physical inconsistencies 

- Partial deviations from expected object dynamics 

- Movements occasionally appear unnatural 

#### **2 — Poorly Physical** 

- Frequent or severe physics violations 

- Object motion or robot kinematics contradict basic realworld principles 

- Motion discontinuities or penetrations are common 

**Instruction Understanding.** This dimension measures whether the final outcome satisfies the given instruction. It is strictly goal-oriented, disregarding process efficiency or motion plausibility. Scoring Criteria will be as follows: 

#### **5 — Fully Achieved** 

- The instruction is completed precisely and entirely 

- All expected final conditions are satisfied 

- No essential elements are missing 

   - **1 — Physically Impossible** 

- Major violations of fundamental physics (e.g., teleportation, reverse gravity, object behavior without force causality) 

- Substantial geometric inconsistencies (large penetrations) 

- If a generated human performs part or all of the task, the Physical Law score is supposed to be 1, regardless of physical plausibility 

#### **4 — Mostly Achieved** 

- The majority of the instructions is correctly executed 

- Minor deviations exist, but do not compromise overall task success 

#### **3 — Partially Achieved** 

- Only some components of the instruction are fulfilled 

- Significant omissions or inaccuracies remain 

- The intended goal is only partially realized 

#### **2 — Minimally Achieved** 

- Most of the required outcome is not completed 

- The behavior exhibits weak or inconsistent correspondence to the instruction 

#### **1 — Not Achieved** 

- The instruction is not fulfilled at all 

- Actions are irrelevant or contradictory to the task 

- A fully static video always receives a score of 1 in this dimension 

**Planning Reasoning.** This dimension assesses the logical structure and coherence of the robot’s action sequence, independent of final task success. It captures whether the robot demonstrates purposeful, ordered planning. Scoring Criteria will be as follows: 

#### **5 — Well-Structured Planning** 

- Action sequence is coherent, efficient, and well aligned with the task 

- No extraneous or aimless motions 

- Exhibits deliberate, task-driven progression 

#### **4 — Reasonable Planning** 

- Overall logical sequence with minor redundant actions 

- Task progression remains clear and purposeful **3 — Weak Planning** 

- Action sequence contains irregularities or inefficiencies 

- Task intent is visible, but execution lacks structure 

- Multiple corrective attempts may be present 

**Physical Law.** This dimension evaluates whether the depicted motions and object interactions adhere to real-world physical principles, including dynamics, continuity, and plausible human-robot interaction. Scoring Criteria will be as follows: 

#### **2 — Poor Planning** 

- Disorganized or inconsistent action sequence 

- Repeated irrelevant behaviors or unnecessary back-andforth motions 

- Weak alignment between steps and task objective 

8 


Figure 6. **All correlation for WoW-World-Eval and Human Preference.** 

#### **1 — No Planning** 

- Actions are random, chaotic, or entirely absent 

- A fully static video always receives a score of 1 in this dimension 

confirms that perceptual sharpness, temporal consistency, and high-level structure—captured jointly by FVD, PSNR, SSIM, DINO, and DreamSim—align well with how humans evaluate visual sensitivity. 

**Overall Score.** The Overall Score is defined as the sum of the four scores. All dimensions are weighted equally, supporting transparent and reproducible evaluation. 

### **10.2. All correlation of WoW-World-Eval score and Human Preference** 

In section 4.1, we report the correlation between our overall scores and overall human preferences. However, to quantify how well WoW-World-Eval reflects human perception in all perspectives, we also provide the correlation between these four metrics—Video Quality, Instruction Understanding, Physical Law, and Planning. Figure 6 reports both strong Pearson (r) and Spearman ( _ρ_ ) correlations between all groups of benchmark scores and human preferences, which, importantly, confirms that metric-based evaluation can reliably approximate human judgment, supporting the use of WoW-World-Eval as a scalable alternative to costly human evaluations. 

**Video Quality.** Quality metrics exhibit a quite strong correlation with human assessments (r = 0.66, _ρ_ = 0.73). This 

**Instruction Understanding.** The Instruction Understanding score shows robust alignment with human preferences (r = 0.75, _ρ_ = 0.71). Models that accurately capture state transitions, object–action relationships, and multi-step task semantics tend to be judged by humans as better at “following instructions,” validating our caption-, sequence- and execution-based IU metrics. 

**Physical Law.** Correlation is highest for Physical Law (r = 0.81, _ρ_ = 0.83). This indicates that humans are highly sensitive to violations of physics—object irregular motion, penetration, trajectory discontinuities, implausible state changes—and that our physics metrics effectively capture such failures. 

**Planning.** Planning demonstrates only moderate correlation with human ratings (r = 0.43, _ρ_ = 0.51). This reflects the inherent difficulty of automatically evaluating long-horizon reasoning and structured action sequences, as well as the limited planning ability of current video models. 

9 

### **10.3. Ground-truth video replay of IDM** 

To ensure that our Inverse Dynamics Model (IDM) provides reliable supervision in the IDM Turing Test, we first validate the accuracy of a reproduced Gripper-Centric IDM (GC-IDM) following WoW [17]. Before applying the IDM to model-generated videos, it is essential to verify that its action inference is sufficiently accurate on ground-truth real-world data; otherwise, low execution accuracy could stem from model weakness rather than the generated video being physically unrealistic. 

We therefore evaluate GC-IDM across 9 manipulation tasks, each with 10 ground-truth execution videos. They are Easy (Pick bread and place on the plate; Close the drawer; Move the milk in front of the cup), Medium (Pick bread and place it in the upper drawer; Take the cup off the cup holder; Open the drawer) and Hard (Flip the button to the correct position; Hang the cup on the cup holder; Insert chopsticks into the bamboo tube). For each trial, we feed the real video sequence into GC-IDM, infer the corresponding gripper-centric action sequence, and replay it in the real world to measure Replay Execution Accuracy. As shown in Table 7, we showcased four of the tasks, GC-IDM substantially outperforms standard baselines such as ResNet-based inverse dynamics model and AVDC [43] across all tasks, achieving an overall replay accuracy of 90%, demonstrating strong fidelity in mapping real videos to executable actions. Representative frames from ground-truth video replays are provided in Figure 7. 

This high replay accuracy confirms that GC-IDM is a reliable evaluator of physical plausibility. Consequently, when GC-IDM fails on model-generated videos, we can attribute the failure to deficiencies in video realism rather than inaccuracies in the IDM itself. 

Table 7. **Comparison of Success Rate (%) on various tasks across different models on ground-truth video replay.** 

### **GPT Data Selection Prompt** 

- <mark>You are a robotics data selection and instruction rewriting assistant.</mark> 

- <mark>Input: one task instruction (text) and one first-frame image.</mark> 

- <mark>Output: JSON only, describing which data dimensions this sample belongs to, with evidence, confidence scores, and a rewritten instruction only for Perception</mark> 

- <mark>dimensions.</mark> 

##### <mark>Absolute Rules</mark> 

- <mark>Use only what is visible in the first frame and what is stated in the instruction. Do not hallucinate or import outside knowledge.</mark> 

- <mark>A dimension is valid only if:</mark> 

- <mark>The image provides clear visual evidence, and</mark> 

- <mark>The original instruction can be unambiguously rewritten (if Perception) or directly preserved (if Prediction/Planning).</mark> 

- <mark>If evidence is insufficient or ambiguous, do not assign the dimension; instead, explain in issues.</mark> 

- <mark>Multiple dimensions can be assigned; each must include its own score and evidence.</mark> 

- <mark>Instruction rewriting requirement:</mark> 

|**Model / Task**|**Bread to Plate**|**Close Drawer**|**Move Milk**|**Bread in Drawer**|
|---|---|---|---|---|
|**ResNet-MLPs**|6/10|7/10|5/10|4/10|
|**AVDC**[43]|3/10|4/10|4/10|2/10|
|**GC-IDM**[17]|**10/10**|**9/10**|**9/10**|**8/10**|


## **11. Case Results Visualization** 

We also collect more generated results of different models for comparision, as visualized in Figure 8, 9, 10. 

- <mark>Perception including rewrite</mark> 

   - <mark>instruction into an equivalent form using attributes / functions / spatial relations / affordances.</mark> 

- <mark>Prediction and Planning will always keep the original instruction unchanged.</mark> 

- <mark>Dimension Checklist</mark> 

- <mark>A. Perception</mark> 

## **12. Prompts** 

For the prompts that we used in GPT for evaluation and data selection, or our own trained Physical MLLM. 

- <mark>object-centric / object-attribute ( color, number, shape, size, type)</mark> 

10 


Figure 7. **Real-World ground-truth video replay on real robot.** 


Figure 8. **More Case Visualization in Perception.** 


11 


Figure 9. **More Case Visualization in Prediction.** 

<mark>object-centric / object-function</mark> 

<mark>Rewrite into function-based description.</mark> 

<mark>rigid-fluid | multi-object/rigiddeformable | multi-object/fluidfluid | dual-arm-cooperate</mark> 

<mark>corner-case.</mark> 

<mark>scene-centric / spatial-relation</mark> 

<mark>Rewrite into relation-based description.</mark> 

<mark>Keep original instruction (no rewriting).</mark> 

<mark>C. Planning</mark> 

<mark>affordance-centric / object-affordance</mark> 

<mark>Rewrite into affordance-based description.</mark> 

<mark>B. Prediction</mark> 

<mark>camera-view including no-occlude | semi-occlude.</mark> 

<mark>physical-interaction including singleobject/rigid | single-object/fluid | single-object/deformable | single-object/articulated | multiobject/rigid-rigid | multi-object/</mark> 

<mark>long-term-instruction. Keep original instruction (no rewriting). JSON Output Format { "input_instruction": "<original instruction>",</mark> 

<mark>"dimensions": [</mark> 

<mark>{ "path": "Perception/objectcentric/object-attribute/color ",</mark> 

12 

**Put the fruit in the basket CogVideoX Cosmos-Predict1 Cosmos-Predict2 WoW-Cosmos1 WoW-Cosmos2 Wan2.1 WoW-Wan Hailuo Kling** 

Figure 10. **More Case Visualization in Generalization.** 

- <mark>"score": 0.9,</mark> 

<mark>"evidence": "blue plate, red tomato, yellow pepper visible ",</mark> 

- <mark>"rewrite": "move the red and yellow objects to the blue object"</mark> 

<mark>}, { "path": "Prediction/camera-view", "score": 0.8, "evidence": "all target objects fully visible", "rewrite": "keep original instruction" } ], "prediction": { "camera-view": { "label": "no-occlude | semiocclude | unknown",</mark> 

<mark>"evidence": "<short evidence>",</mark> 

<mark>"score": 0.0</mark> 

<mark>"physical-interaction": [ {</mark> 

<mark>"label": "single-object/rigid | ...",</mark> 

<mark>"evidence": "<short evidence>", "score": 0.0</mark> 

<mark>} ] },</mark> 

<mark>"planning": [ {</mark> 

<mark>"label": "long-term-instruction", "evidence": "<short evidence>", "score": 0.0, "rewrite": "keep original instruction"</mark> 

<mark>} ],</mark> 

<mark>"issues": [ "<if there is missing evidence or ambiguity, explain here>"</mark> 

<mark>] }</mark> 

<mark>},</mark> 

13 

<mark>For Perception dimensions, rewrite contains the modified instruction. For Prediction and Planning dimensions , rewrite must be exactly "keep original instruction".</mark> 

<mark>score is confidence for 0 to 1.</mark> 

<mark>evidence is short, factual, visual clues only. **</mark><sup><mark>Example</mark></sup> <mark>**</mark> 

<mark>"score": 0.9 }, "physical-interaction": [ { "label": "single-object/rigid", "evidence": "rigid tabletop objects", "score": 0.8 } ] }, "planning": [], "issues": [] }</mark> 

<mark>Input:</mark> 

<mark>instruction: move tomato and pepper to the plate</mark> 

<mark>image: blue plate, red tomato, yellow pepper; no occlusion.</mark> 

<mark>Output:</mark> 

<mark>{ "input_instruction": "move tomato and pepper to the plate", "dimensions": [ { "path": "Perception/objectcentric/object-attribute/color ", "score": 0.95, "evidence": "blue plate; red tomato; yellow pepper visible ", "rewrite": "move the red and yellow objects to the blue object" }, { "path": "Prediction/camera-view", "score": 0.9, "evidence": "all target objects fully visible", "rewrite": "keep original instruction" } ], "prediction": { "camera-view": { "label": "no-occlude", "evidence": "all objects clearly visible",</mark> 

### **Instruction Semantic Correctness: Extract Video Semantic Caption** 

- <mark>Please analyze the instruction that I used to guide the model to generate video and the content of the following groundtruth video( there maybe no groundtruth video, if so please use only the instruction), extract semantic descriptions related to the robot’ s behavior. Focus on the following five aspects and provide one</mark> 

- <mark>clear, concise sentence for each:</mark> 

<mark>1. Initial State: The state of the object(s) and environment before any action (e.g., position, posture, quantity)</mark> 

<mark>2. Processing State: The interaction process while the robot arm is operating (e.g., how it moves or manipulates the object)</mark> 

<mark>3. Final State: The outcome after the action (e.g., new position or state of the object, whether the task goal was achieved)</mark> 

<mark>4. Action: The main type of operation performed (e.g., grasping, pushing , placing)</mark> 

<mark>5. Object: The object being manipulated (e.g., its color, shape, category)</mark> 

<mark>Please output your result in the following format:</mark> 

<mark>‘‘‘</mark> 

<mark>Initial State: ...</mark> 

14 

<mark>Processing State: ... Final State: ... Action: ... Object: ... ‘‘‘</mark> 

<mark>Guidelines:</mark> 

- <mark>Keep each sentence objective, specific, and based only on what is visible in the video.</mark> 

- <mark>Do not add assumptions or imagined information.</mark> 

- <mark>If any aspect is unclear or not visible, write "Unknown" for that field.</mark> 

- <mark>Avoid overly abstract descriptions such as "successfully completed the task."</mark> 

<mark>},</mark> 

<mark>"level_2": { "score": 0.5, "description": "Partially Consistent, Descriptions differ in minor semantic details or omit secondary information, but task intent remains aligned"</mark> 

<mark>},</mark> 

<mark>"level_3": { "score": 0, "description": "Inconsistent, Descriptions conflict semantically, refer to different actions, goals, or object properties"</mark> 

<mark>}</mark> 

<mark>"output_format": {</mark> 

<mark>"initial_state": "Score = [0 / 0.5 / 1] - Reason: ...",</mark> 

### **Instruction Semantic Correctness: Compare Video Semantic Caption** 

- <mark>You are given structured semantic captions from two videos: the original ground truth and a generated version. Compare them across the following five dimensions and evaluate their semantic consistency.</mark> 

- <mark>"comparison_dimensions": {</mark> 

   - <mark>"initial_state": "The object/ environment status before any action",</mark> 

   - <mark>"processing_state": "How the robot interacts with the object during operation",</mark> 

   - <mark>"final_state": "The outcome or resulting object state",</mark> 

   - <mark>"action": "The type of manipulation performed",</mark> 

   - <mark>"object": "The object being manipulated"</mark> 

<mark>},</mark> 

- <mark>"scoring_guidelines": {</mark> 

<mark>"processing_state": "Score = [0 / 0.5 / 1] - Reason: ...", "final_state": "Score = [0 / 0.5 / 1] - Reason: ...",</mark> 

<mark>"action": "Score = [0 / 0.5 / 1] - Reason: ...",</mark> 

<mark>"object": "Score = [0 / 0.5 / 1] - Reason: ...",</mark> 

<mark>"overall": "Score = [0 / 0.5 / 1] - Summary Reason: ..."</mark> 

##### <mark>},</mark> 

<mark>"evaluation_principles": [</mark> 

<mark>"Focus strictly on the semantic content of the captions, do not infer or assume actions or states that are not explicitly stated.",</mark> 

<mark>"The overall score may reflect the average of the five dimensions, but should also consider whether the task intent and outcome remain semantically aligned."</mark> 

<mark>]</mark> 

<mark>Ground truth video caption is: {ground _truth_caption}</mark> 

<mark>Generated video caption is: {generated _caption}</mark> 

- <mark>"level_1": {</mark> 

   - <mark>"score": 1,</mark> 

   - <mark>"description": "Fully Consistent</mark> 

      - <mark>, Descriptions convey the same semantic content with only stylistic or wording differences"</mark> 

### **Instruction Semantic Correctness: Evaluate Video Action Execution** 

<mark>},</mark> 

15 

- <mark>You are given a language instruction describing a series of robot manipulation actions, and a generated video that attempts to follow that instruction.</mark> 

<mark>Your task has two parts:</mark> 

- <mark>PART 1: Action Sequence Consistency ( Proportional Scoring)</mark> 

- <mark>Parse the instruction and extract the intended object-action pairs in order.</mark> 

- <mark>Analyze the generated video to determine the actual order of the executed object-action pairs. Compare the two sequences and compute a sequence match score:</mark> 

   - <mark>Sequence Match Scoring:</mark> 

      - <mark>Score = (number of matching object-action pairs in correct order) / (total number of instruction pairs)</mark> 

      - <mark>Matching means: the objectaction pair appears in the video and in the same relative order as in the instruction. Partial matches or out-of-order actions</mark> 

      - <mark>reduce the score.</mark> 

<mark>Output format:</mark> 

- <mark>4 - Object reached target state OR action completed successfully</mark> 

- <mark>5 - Object reached target state AND action completed successfully</mark> 

<mark>Base this strictly on visible evidence in the video. Be conservative in scoring.</mark> 

<mark>Output format: Execution Quality:</mark> 

- <mark>(object1, action1): Score = [1-5] - Reason: ...</mark> 

- <mark>(object2, action2): Score = [1-5] - Reason: ...</mark> 

<mark>Final Combined Output: Instruction Sequence: ... Video Sequence: ... Sequence Match Score: X.XX (range: 0.00-1.00) - Reason: ... Execution Quality:</mark> 

      - <mark>(object1, action1): Score = [1-5] - Reason: ...</mark> 

      - <mark>- (object2, action2): Score = [1-5] - Reason: ...</mark> 

      - <mark>Instruction is: {instruction}</mark> 

- <mark>Instruction Sequence: [(object1, action1), (object2, action</mark> 

- <mark>2), ...]</mark> 

- <mark>Video Sequence: [(object1, action1), (object2, action2)</mark> 

   - <mark>, ...]</mark> 

<mark>Sequence Match Score: X.XX ( range: 0.00-1.00) - Reason:</mark> 

- <mark>PART 2: Action Execution Quality ( Numerical Evaluation)</mark> 

- <mark>For each (object, action) pair in the instruction, evaluate execution quality using a 1-5 numerical scale:</mark> 

<mark>Execution Quality Scoring:</mark> 

- <mark>1 - Object did not move AND action was not attempted</mark> 

- <mark>2 - Object moved slightly OR action was partially attempted</mark> 

- <mark>3 - Object moved slightly AND action was partially attempted</mark> 

### **Physical Common Sense: Stage 2: Scoring Alignment Fine-tuning Prompt** 

- <mark>You are an expert AI video evaluator. Your task is to analyze the provided video, which was generated from the accompanying text prompt. You must score the video on a scale of 1 to 5 across four dimensions based on the precise criteria listed below.</mark> 

<mark>Evaluation Criteria:</mark> 

<mark>1. Video Quality (1-5):</mark> 

   - <mark>5: Clear, stable, natural colors, no generation artifacts.</mark> 

   - <mark>4: Minor flaws (e.g., occasional flicker, slight blur) that don’ t detract from the overall view</mark> 

16 

- <mark>3: Noticeable flaws (e.g., persistent noise, subject out of focus) but core content is understandable.</mark> 

- <mark>2: Severe defects (e.g., unstable subject form, heavy jitter) that significantly impair understanding.</mark> 

      - <mark>2: A severe physical error that causes the task to fail or its logic to break (e.g., a hand passes through the target object).</mark> 

      - <mark>1: A complete lack of physical logic; chaotic and disorderly interactions.</mark> 

   <mark>4. Planning Logic (1-5):</mark> 

- <mark>1: Extremely poor quality, making the subject or content unrecognizable.</mark> 

      - <mark>5: The plan is logical, efficient, with no redundant actions, and successfully achieves the goal.</mark> 

<mark>2. Instruction Following (1-5):</mark> 

   - <mark>5: Perfectly matches the prompt; all core elements and details are accurately represented.</mark> 

   - <mark>4: Core elements are correct, but a minor detail (e.g., color,</mark> 

   - <mark>location) is missed or incorrect.</mark> 

   - <mark>3: The core element (subject or action) deviates significantly but is still partially related to the prompt.</mark> 

   - <mark>2: The core element is fundamentally misinterpreted; the content is seriously inconsistent with the prompt.</mark> 

   - <mark>1: Completely unrelated to the prompt; a random generation.</mark> 

<mark>3. Physical Consistency (1-5):</mark> 

   - <mark>5: Fully consistent with physics; interactions are believable, no object clipping or floating.</mark> 

   - <mark>4: A momentary, almost unnoticeable physical anomaly (e.g., slight clipping) that doesn’t affect</mark> 

   - <mark>the task.</mark> 

- <mark>4: The plan is effective and successful but contains minor redundant or inefficient movements.</mark> 

- <mark>3: The goal is achieved, but the process is convoluted or clumsy ; the plan is illogical.</mark> 

- <mark>2: The plan has critical errors or missing steps, leading to task failure.</mark> 

- <mark>1: Actions are random and chaotic, with no discernible goal or plan.</mark> 

<mark>Analyze the following inputs:</mark> 

<mark>Original Prompt: {instruction} Generated Video: <video></mark> 

<mark>Your final answer must be a single,</mark> 

- <mark>valid JSON object and nothing else . Do not include any explanations, conversational text, or markdown</mark> 

- <mark>formatting around the JSON block.</mark> 

<mark>Your JSON Answer:</mark> 

- <mark>{</mark> 

   - <mark>"video_quality": <integer_score>, "instruction_following": <integer_ score>,</mark> 

   - <mark>"physical_consistency": <integer_ score>,</mark> 

   - <mark>"planning_logic": <integer_score></mark> 

- <mark>3: A noticeable physical error (e.g ., arm passes through a table) that doesn’t break the core task logic.</mark> 

<mark>}</mark> 

17 

### **Physical Common Sense: 6-Dimension Evaluation Prompt** 

- <mark>Please evaluate the following video strictly based on whether it follows real-world physics laws.</mark> 

<mark>This is not a test of whether it is AI -generated, but only judge its physical plausibility.</mark> 

<mark>Scoring System (1 to 5 scale):</mark> 

- <mark>For each of the six categories below, assign a score from 1 to 5:</mark> 

- <mark>5 = Fully consistent with real-world physics</mark> 

- <mark>4 = Mostly consistent, only small flaws</mark> 

- <mark>3 = Partially consistent, with some clear issues</mark> 

- <mark>2 = Often inconsistent, unrealistic in multiple ways</mark> 

- <mark>1 = Clearly violates physical laws</mark> 

- <mark>null = Not applicable (no relevant content in video)</mark> 

- <mark>For each of the following categories:</mark> 

- <mark>Give a score (1 to 5) or null if the category does not appear at all</mark> 

- <mark>in the video</mark> 

- <mark>Provide a brief explanation (1 to 2 sentences) for each score</mark> 

- <mark>Return your output in structured JSON as shown below.</mark> 

<mark>Evaluation Criteria (Detailed): 1. Object Interaction and State Changes</mark> 

- <mark>Do objects respond naturally when they touch, collide, bounce, break, or are pushed/pulled?</mark> 

- <mark>Is there a realistic cause-andeffect in object contact?</mark> 

- <mark>Do interactions follow Newton’s laws (e.g., action/reaction, inertia)?</mark> 

- <mark>Are deformations (e.g., squashing, bending) consistent with</mark> 

- <mark>materials?</mark> 

- <mark>Do objects maintain consistent color, quantity, shape, and size throughout interactions?</mark> 

<mark>2. Basic Physical Properties</mark> 

- <mark>Does gravity act in the correct direction and magnitude (e.g., falling speed)?</mark> 

- <mark>Is there realistic motion under inertia and deceleration?</mark> 

- <mark>Does friction behave naturally (e. g., sliding slows over time)?</mark> 

- <mark>Are materials (heavy/light) behaving correctly based on mass or density?</mark> 

<mark>3. Temporal and Causal Consistency</mark> 

- <mark>Do effects follow causes in the right order and with realistic timing?</mark> 

- <mark>Are there appropriate delays in mechanical systems, collisions, or triggered motions?</mark> 

- <mark>Is there a consistent flow of time across all elements (e.g., no</mark> 

- <mark>time jumps or impossible overlaps )?</mark> 

<mark>4. Lighting, Shadows, and Reflections</mark> 

- <mark>Are shadows cast in the correct direction and shape relative to light sources?</mark> 

- <mark>Is there consistent lighting across surfaces and objects?</mark> 

- <mark>Do reflective surfaces (mirrors, metal, water) behave correctly based on angles?</mark> 

- <mark>Is light intensity and falloff physically accurate (not flat or overly uniform)?</mark> 

<mark>5. Fluid and Particle Behavior</mark> 

- <mark>Do water, smoke, fire, or dust behave according to fluid dynamics?</mark> 

- <mark>Is there natural turbulence, diffusion, and randomness?</mark> 

- <mark>Do particles (like debris, sparks, splashes) move in a physically</mark> 

- <mark>plausible way?</mark> 

- <mark>Is there appropriate interaction with solid surfaces (e.g., splashes bounce, smoke drifts)?</mark> 

<mark>6. Local Anomalies or Violations</mark> 

- <mark>Are there any visual inconsistencies like:</mark> 

- <mark>sudden object movement without cause</mark> 

- <mark>teleportation or disappearing items</mark> 

- <mark>objects passing through others ( no collision)</mark> 

- <mark>animation glitches, floating artifacts, or broken motion?</mark> 

- <mark>Do all parts of the scene stay consistent frame to frame?</mark> 

18 

- <mark>Return your output in structured JSON as shown below.</mark> 

   - <mark>object_interaction: {score: int| null, comment: str}</mark> 

   - <mark>physical_properties: {score: int| null, comment: str}</mark> 

   - <mark>temporal_consistency: {score: int |null, comment: str}</mark> 

   - <mark>lighting_and_reflections: {score: int|null, comment: str}</mark> 

   - <mark>fluids_and_particles: {score: int |null, comment: str}</mark> 

   - <mark>local_anomalies: {score: int|null , comment: str}</mark> 

### **Dense Prompts Extension Prompt** 

- <mark>You are an expert in Embodied AI tasked with generating dense and standardized textual descriptions of robot episodes. Your goal is to re-caption a brief, potentially</mark> 

- <mark>ambiguous, episode description into a richer, more precise narrative,but no more than 150 words. This serves two main purposes:</mark> 

<mark>1. To clarify ambiguous action descriptions with precise technical terminology.</mark> 

<mark>2. To unify the textual representation of similar actions across</mark> 

<mark>different datasets, ensuring consistency in phrasing and detail</mark> 

- <mark>When generating the dense caption, adhere to the following structure and include these specific details :</mark> 

<mark>1. **Overall Scene & Goal Overview:** *</mark><sup><mark>Beginwithaconcisesummaryof</mark></sup> <mark>the robot’s primary goal or the main action being performed in the scene, directly derived or inferred from the input .</mark> 

<mark>2. **Environment Description:** *</mark><sup><mark>Describetherobot’soperational</mark></sup> <mark>environment (e.g., kitchen,</mark> 

<mark>laboratory, office, cluttered tabletop, outdoor path).</mark> 

   - <sup><mark>Includerelevantambient</mark></sup> <mark>conditions: lighting (e.g., bright, dim, natural, artificial), indoor/outdoor setting, and weather if applicable (e.g., sunny, overcast for outdoor scenes).</mark> 

<mark>3. **Robot Characteristics:**</mark> 

   - <sup><mark>Specifykeycharacteristicsof</mark></sup> <mark>the robot if inferable or if it ’s a common type in embodied AI (e.g., humanoid, mobile</mark> 

   - <mark>manipulator with a single arm, quadruped, drone).</mark> 

   - <sup><mark>Noteitsgeneralappearanceif</mark></sup> <mark>significant (e.g., color scheme , predominant material like metallic or plastic).</mark> 

   - <sup><mark>Mentionitsgrippertypeif</mark></sup> <mark>relevant to the action (e.g., parallel jaw gripper, suction cup, multi-finger dexterous hand).</mark> 

<mark>4. **Camera Perspective & Motion:**</mark> 

   - <sup><mark>Detailthecamera’sperspective(</mark></sup> <mark>e.g., first-person (egocentric/ robot’s POV), third-person fixed, third-person dynamic/ following, eye-in-hand, overhead).</mark> 

   - <sup><mark>Describeanysignificantcamera</mark></sup> <mark>movement (e.g., static, panning to follow action, smooth</mark> 

   - <mark>tracking shot, handheld jitter if applicable).</mark> 

<mark>5. **Robot Sub-goal & Granular Action Breakdown:**</mark> 

   - <sup><mark>Inferandexplicitlystatethe</mark></sup> <mark>immediate sub-goal the robot is trying to achieve based on the input.</mark> 

   - <sup><mark>Provideagranularbreakdownof</mark></sup> <mark>the robot’s actions. Use precise, standardized technical action terminology (e.g., "</mark> 

   - <mark>Navigate_to [location]", " Perceive [object]", "Grasp [ object]", "Lift [object]", " Move_arm_to [target_pose]", " Place [object] at [location]",</mark> 

19 

<mark>"Release [object]", "Push [ object]", "Rotate [object]").</mark> 

   - <sup><mark>Clearlyidentifytheobject(s)</mark></sup> <mark>being manipulated and any changes in their state or location.</mark> 

<mark>6. **Post-Action State:**</mark> 

   - <sup><mark>Brieflydescribethestateofthe</mark></sup> <mark>robot and the key manipulated</mark> 

   - <mark>object(s) *after* the described action sequence is completed.</mark> 

- <mark>**</mark><sup><mark>Constraints:</mark></sup> <mark>**</mark> 

- <sup><mark>Thefinaldescriptionshouldbe</mark></sup> <mark>dense, focusing on factual and observable details.</mark> 

- <sup><mark>Aimforatotallengthof</mark></sup> <mark>approximately 100-150 words.</mark> 

- <sup><mark>Useconsistentterminologyfor</mark></sup> <mark>common actions and objects.</mark> 

- <sup><mark>Avoidfillerwordsorsubjective</mark></sup> <mark>stylistic descriptions not grounded in typical embodied AI contexts.</mark> 

- <sup><mark>Onlydescribeelementsplausibly</mark></sup> <mark>present or inferable from a typical embodied AI episode matching the ‘Given Input‘. Do not invent fantastical details.</mark> 

<mark>stationary or mobile base ( partially visible). The camera is a static third-person view, positioned to offer a clear sideangle of the robot’s arm and the workspace, including the target bowl.</mark> 

- <mark>The robot’s sub-goal is to successfully deposit the apple. The action sequence begins with the robot’s arm, already grasping a red apple, positioned directly above a ceramic bowl. The arm executes a ’Move_arm_to [bowl_ center_above]’ command, followed by a ’Lower_arm’ motion. The gripper then performs a ’Release [ apple]’ action. Finally, the arm might execute a ’Retract_arm’ motion away from the bowl.</mark> 

- <mark>After the action, the red apple rests inside the bowl on the countertop, and the robot’s gripper is open</mark> 

- <mark>and clear of the bowl.</mark> 

<mark>Given Input : {instruction} Your Dense Recaption:</mark> 

- <sup><mark>Nevermentionelementsoutsidethe</mark></sup> <mark>implied scene or action.</mark> 

<mark>**</mark><sup><mark>ExampleofUse:</mark></sup> <mark>**</mark> 

- <mark>Let’s say the given short episode description is: "drop the apple in the bowl"</mark> 

- <mark>**</mark><sup><mark>GivenInput:droptheappleinthe</mark></sup> <mark>bowl</mark> 

- <mark>**</mark><sup><mark>YourDenseRecaption(Outputbased</mark></sup> <mark>on the prompt above):**</mark> 

- <mark>The robot’s primary goal is to place an apple into a designated bowl.</mark> 

- <mark>The scene is set in a brightly lit kitchen environment, specifically on a clean countertop. The robot is a single-arm manipulator, predominantly white with grey joints, equipped with a parallel jaw gripper, likely mounted on a</mark> 

20 

