---
title: "WorldArena: A Unified Benchmark for Evaluating Perception and Functional Utility of Embodied World Models"
date: "2026-02-09"
authors: "Yu Shang; Zhuohang Li; Yiding Ma; Weikang Su; Xin Jin; Ziyou Wang"
url: https://arxiv.org/abs/2602.08971
pdf: https://arxiv.org/pdf/2602.08971
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.08971)** / [論文ページ](https://arxiv.org/abs/2602.08971)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **WorldArena: A Unified Benchmark for Evaluating Perception and Functional Utility of Embodied World Models** 

**Yu Shang**<sup>1 *</sup><sup>_§_</sup> **Zhuohang Li**<sup>1 *</sup> **Yiding Ma**<sup>1 *</sup> **Weikang Su**<sup>1 *</sup> **Xin Jin**<sup>_‡_</sup> **Ziyou Wang**<sup>1</sup><sup>_‡_</sup> **Lei Jin**<sup>1</sup> **Xin Zhang**<sup>1</sup> **Yinzhou Tang**<sup>1</sup> **Haisheng Su**<sup>2</sup> **Chen Gao**<sup>1</sup> **Wei Wu**<sup>1</sup> **Xihui Liu**<sup>3</sup> **Dhruv Shah**<sup>4</sup> **Zhaoxiang Zhang**<sup>5</sup> **Zhibo Chen**<sup>6</sup> **Jun Zhu**<sup>1</sup> **Yonghong Tian**<sup>7</sup> **Tat-Seng Chua**<sup>8</sup> **Wenwu Zhu**<sup>1</sup> **Yong Li**<sup>1</sup><sup>_†_</sup> 

## **Abstract** 

## **1. Introduction** 

While world models have emerged as a cornerstone of embodied intelligence by enabling agents to reason about environmental dynamics through action-conditioned prediction, their evaluation remains fragmented. Current evaluation of embodied world models has largely focused on perceptual fidelity (e.g., video generation quality), overlooking the functional utility of these models in downstream decision-making tasks. In this work, we introduce WorldArena, a unified benchmark designed to systematically evaluate embodied world models across both perceptual and functional dimensions. WorldArena assesses models through three dimensions: video perception quality, measured with 16 metrics across six subdimensions; embodied task functionality, which evaluates world models as data engines, policy evaluators, and action planners integrating with subjective human evaluation. Furthermore, we propose EWMScore, a holistic metric integrating multi-dimensional performance into a single interpretable index. Through extensive experiments on 14 representative models, we reveal a significant perception–functionality gap, showing that high visual quality does not necessarily translate into strong embodied task capability. WorldArena benchmark with the public leaderboard is released at https://world-arena.ai, providing a framework for tracking progress toward truly functional world models in embodied AI. 

1Tsinghua University, Beijing, China 2Shanghai Jiao Tong University, Shanghai, China<sup>3</sup> The University of Hong Kong, Hong Kong SAR, China<sup>4</sup> Princeton University, Princeton, NJ, USA 5Chinese Academy of Sciences, Beijing, China 6University of Science and Technology of China, Hefei, China<sup>7</sup> Peking University, Beijing, China<sup>8</sup> National University of Singapore, Singapore. * Equal contribution. _‡_ Equal contribution. _§_ Project lead. Correspondence to: Yong Li _<_ liyong07@tsinghua.edu.cn _>_ . 

_Preprint. February 12, 2026._ 

In recent years, world models (Ding et al., 2025; Kong et al., 2025; Zhu et al., 2024b) have emerged as a foundational component of embodied intelligence. A world model (WM) learns to predict future environment states conditioned on current observations and actions, enabling agents to reason about dynamics and interaction outcomes. Embodied World Model (EWM) forecasts future states based on robot actions and external instructions, effectively functioning as a mental simulator guiding robot action planning and decision-making, or an environment proxy to support scalable robotic training and evaluation (Shang et al., 2025a; Long et al., 2025). Unlike general-purpose video generation models, EWMs must capture not only perceptual fidelity but also physically grounded, action-consistent dynamics that are critical for downstream embodied tasks. 

However, existing evaluation protocols suffer from significant limitations. First, they lack comprehensive evaluations oriented toward embodied tasks, including the role of world models as environment proxies and embodied agents. Current benchmarks (Yue et al., 2025; Li et al., 2025a; Lu et al., 2025) mainly focus on video-level quality metrics, which fail to reflect the real-world value of embodied world models for practical embodied applications, as shown in the comparison of Table 1. Although some recent studies (Qin et al., 2024; Zhang et al., 2025; Fan et al., 2026) evaluate embodied world models through closed-loop action execution, broader embodied capabilities such as their roles as synthetic data engines or tools for policy evaluation remain largely unassessed. Second, the coverage of evaluated models is insufficient. Most existing benchmarks (Yue et al., 2025; Fan et al., 2026) focus on general text-conditioned video generation models (Wan et al., 2025; Yang et al., 2024b), while many recent robot-specialized world models (Chi et al., 2025; Team et al., 2025; Liao et al., 2025; Zhen et al., 2025; Guo et al., 2025), have received little systematic attention and remain largely unevaluated. 

To bridge this gap, we present **WorldArena** , the first embodied world model benchmark that integrates perceptual and three functional evaluations, combining both objective 

1 

**Preprint** 


_Figure 1._ EWMScore results (a) and performance comparisons across different evaluation dimensions (b) for 14 representative embodied world models. 

and subjective assessments. WorldArena provides a holistic evaluation framework across three complementary aspects: (1) multi-faceted video quality, comprising 16 numerical metrics across 6 key sub-dimensions, including visual quality, motion quality, content consistency, physics adherence, 3D accuracy, and controllability; (2) embodied task utility, which evaluates model performance in data synthesis, policy evaluation, and action planning; and (3) human evaluation, which complements automated metrics by capturing qualitative aspects of model behavior that are difficult to quantify, such as physical plausibility and instruction adherence. Additionally, we introduce EWMScore, a unified metric that combines multi-dimensional metrics into a single index, offering a comprehensive assessment of embodied world models’ generative performance. An overview of the evaluation result is shown in Figure 1. 

For the evaluation data, we select bimanual robotic manipulation as a representative embodied scenario and conduct evaluations based on the RobotTwin 2.0 dataset (Chen et al., 2025), which covers 50 diverse robotic scenarios, ensuring both scenario diversity and evaluation reliability. We perform a unified evaluation on 14 representative world models, including both general video generation world models and specialized embodied world models. The results reveal a significant gap between visual fidelity and embodied task performance, indicating that current visual quality has not yet reached the level required to effectively support embodied tasks. Overall, our main contributions can be summarized as follows: 

- We introduce the first comprehensive benchmark tailored for embodied world models, enabling a unified evaluation of their perceptual and functional capabilities. 

- We propose EWMScore, a unified objective metric for embodied world models, and conduct extensive human studies to validate its effectiveness. Results demonstrate 

that EWMScore highly aligns with subjective judgment, serving as a reliable and interpretable index. 

- We conduct a systematic evaluation of 14 representative embodied world models and provide a multi-dimensional analysis of their strengths and limitations, offering insights and guidance for future research. 

## **2. Related Works** 

### **2.1. Embodied World Models** 

Embodied world models are generative models that predict future observations of physical scenes involving robot locomotion and manipulation. These models can be broadly categorized into three types: video generation-based models (Liao et al., 2025; Shang et al., 2025b; Team et al., 2025), 3D reconstruction-based models (Huang et al., 2025; Qian et al., 2025), and latent-space world models (Assran et al., 2025; Liu & Chen, 2025; Hafner et al., 2025). In practice, embodied world models serve three key roles: (1) as data synthesis engines (Jang et al., 2025) for generating video-action sequences to augment robot policy training; (2) as policy evaluation environments (Shang et al., 2025b; Li et al., 2025b) for scalable virtual testing through policyworld model interaction; and (3) as action planners (Hu et al., 2024; Fan et al., 2026), where predicted states are decoded into executable actions for robot control. Given the diversity of model paradigms and functional roles, embodied world models are inherently challenging to evaluate comprehensively, underscoring the need for a holistic benchmark that systematically assesses them across both perceptual and functional dimensions, driving their future development. 

### **2.2. World Model Benchmarks** 

Existing benchmarks for world models can be broadly categorized into general-purpose and embodied benchmarks. 

2 

**Preprint** 

_Table 1._ Comparison of existing world model benchmarks and WorldArena across three key evaluation dimensions. 

|**Benchmark**|||**Video Q**|**uality**|||**Em**|**bodied T**|**asks**|**Human**|
|---|---|---|---|---|---|---|---|---|---|---|
||Visual<br>Quality|Motion<br>Quality|Content <br>Consist.|Physics<br>Adher.|Control<br>ability|3D<br>Acc.|Data<br>Engine|Policy<br>Eval.|Action<br>Planner||
|WorldModelBench (Li et al.,2025a)|_×_|_×_|_×_|✓|✓|_×_|_×_|_×_|_×_|✓|
|WorldSimBench (Qin et al.,2024)|✓|✓|✓|_×_|✓|_×_|_×_|_×_|✓|✓|
|WorldScore (Duan et al.,2025)|✓|✓|✓|_×_|✓|✓|_×_|_×_|_×_|✓|
|4DWorldBench (Lu et al.,2025)|✓|✓|✓|✓|✓|✓|_×_|_×_|_×_|✓|
|EWMBench (Yue et al.,2025)|_×_|✓|✓|_×_|✓|_×_|_×_|_×_|_×_|✓|
|WorldEval (Li et al.,2025b)|_×_|_×_|_×_|_×_|_×_|_×_|_×_|✓|_×_|_×_|
|World-in-World (Zhang et al.,2025)|✓|✓|_×_|_×_|✓|_×_|_×_|_×_|✓|_×_|
|WoW-World-Eval (Fan et al.,2026)|✓|✓|✓|✓|✓|_×_|_×_|_×_|✓|✓|
|**WorldArena (Ours)**|✓|✓|✓|✓|✓|✓|✓|✓|✓|✓|


General-purpose benchmarks (Duan et al., 2025; Li et al., 2025a; Lu et al., 2025) primarily evaluate world models from a perceptual and generative perspective, focusing on video quality aspects such as visual fidelity, motion realism, content consistency, and, in some cases, physical plausibility or geometric consistency. While these benchmarks are effective for standardizing generative evaluation, they largely treat world models as video generators and do not assess their functional roles in decision-making or interaction. More recent embodied world model benchmarks (Yue et al., 2025; Li et al., 2025b; Zhang et al., 2025; Fan et al., 2026) extend evaluation to controllability, action conditioning, and limited closed-loop interaction. However, existing embodied benchmarks remain limited in scope, often focusing on a single embodied role and predominantly targeting text-conditioned video models, with insufficient coverage of action-conditioned and robot-centric world models. Moreover, most existing benchmarks evaluate fewer than ten models, which further limits the scope and comprehensiveness. In contrast, WorldArena provides a unified benchmark that systematically evaluates embodied world models across both perceptual and functional dimensions, integrating objective metrics with human subjective assessments. 

## **3. The WorldArena Benchmark** 

The evaluation framework of WorldArena consists of three key components. First, we assess video quality from 6 dimensions with 16 metrics, focusing on the world model’s open-loop prediction ability (Section 3.1). Second, we evaluate the world model’s closed-loop performance across 3 typical embodied downstream tasks (Section 3.2). Third, to complement objective measurements with subjective judgment, we collect human annotations to assess qualitative aspects of model performance (Section 3.3). Finally, we integrate multi-dimensional video metrics into an interpretable index EWMScore to reflect overall performance (Section 3.4). 

### **3.1. Video Quality Evaluation** 

We begin by evaluating the quality of the videos generated by different embodied world models, considering 16 video metrics across six sub-dimensions, as shown in Figure 1 (b). The detailed metric explanations can be found in Appendix A and the case visualization is shown in Appendix C. 

### 3.1.1. VISUAL QUALITY 

Visual quality assesses whether generated videos are perceptually reliable for embodied scenarios, considering low-level fidelity, perceptual appeal, and similarity to real data. We evaluate it using three metrics: 

**Image Quality** measures clarity and sharpness of frames using the MUSIQ (Ke et al., 2021) model, which detects distortions such as overexposure, noise, and compression artifacts (Huang et al., 2024). Higher scores indicate cleaner and more coherent images. 

**Aesthetic Quality** evaluates the visual appeal of the video, considering lighting and color composition. Using the LAION aesthetic predictor (LAION-AI, 2022), we map frames to an aesthetic feature space and derive an average score (Huang et al., 2024), capturing both perceptual consistency and artistic quality. 

**JEPA Similarity** quantifies similarity between feature distributions extracted by the pretrained V-JEPA encoder (Bardes et al., 2023), using maximum mean discrepancy (MMD) with a second-order polynomial kernel (Luo et al., 2024). Higher values indicate greater similarity to the ground-truth video. 

### 3.1.2. MOTION QUALITY 

Motion quality reflects whether a model captures physically meaningful and temporally coherent dynamics. We assess both the strength of motion and its temporal continuity. To 

3 

**Preprint** 

### this end, we introduce the following three metrics: 

**Dynamic Degree** quantifies the motion intensity within the video. Using the RAFT (Teed & Deng, 2020) optical flow model, we extract motion vector fields between consecutive frames and focus on the top 5% of active pixels (Huang et al., 2024). A higher dynamic degree score indicates more pronounced and meaningful movement in the video, capturing the intensity of motion in key areas such as robotic arm gestures. 

**Flow Score** measures the overall intensity of motion across the video by averaging optical flow magnitudes over time (Liu et al., 2023). This score reflects the degree of dynamic interaction, where a higher value indicates greater motion intensity and more physically meaningful dynamics throughout the video. 

**Motion Smoothness** evaluates the temporal coherence of motion, assessing whether movements between consecutive frames are smooth and consistent with physical inertia. Using a frame interpolation model (Zhang et al., 2024), we predict intermediate frames and compare them to real frames (Duan et al., 2025). This approach incorporates motion magnitude as a weighting factor to prevent overestimating static backgrounds and ensure rapid motion sequences are not unfairly penalized. 

### 3.1.3. CONTENT CONSISTENCY 

Content consistency measures the stability of objects and scenes throughout the video, evaluated at both semantic and appearance levels using three metrics: 

**Subject Consistency** assesses object consistency across frames by calculating cosine similarity between DINO (Caron et al., 2021) features from the first, current, and previous frames (Huang et al., 2024). Higher similarity scores indicate better consistency. 

**Background Consistency** evaluates scene stability using CLIP (Radford et al., 2021) features, measuring cosine similarity between the current frame and the first and previous frames to assess scene stability (Huang et al., 2024). 

**Photometric Consistency** measures pixel-level texture stability by calculating the average end-point error (AEPE) using optical flow (Duan et al., 2025). A higher AEPE indicates poorer alignment, while a higher score reflects better consistency. 

### 3.1.4. PHYSICS ADHERENCE 

Physics adherence evaluates whether generated behaviors conform to real-world physical constraints rather than merely appearing visually plausible. We therefore assess both local interaction realism and global motion correctness with the following two metrics: 

**Interaction Quality** evaluates the physical plausibility of interactions between the robot and objects. We use Qwen3VL (Bai et al., 2025a) to assess factors such as contact behavior and force transmission, checking whether the interactions are physically realistic. The interaction quality score is based on a 1–5 scale, normalized to [0,1], showing how well the robot’s actions align with expected physical behaviors. 

**Trajectory Accuracy** quantifies the accuracy of the robotic arm’s grasping trajectory. Using the SAM 3 (Carion et al., 2025) model, we extract bounding boxes for the arm in each frame and compute the normalized dynamic time warping (NDTW) distance to evaluate alignment with the groundtruth trajectory (Yue et al., 2025). A higher score reflects better spatial-temporal alignment and more accurate trajectory prediction. 

### 3.1.5. 3D ACCURACY 

3D accuracy assesses whether generated videos preserve real-world spatial structure beyond image appearance. We evaluate geometric consistency and perspective plausibility with the following two metrics: 

**Depth Accuracy** evaluates whether the generated video preserves real-world spatial geometry by comparing depth maps between the generated and ground-truth videos. We use monocular depth estimation and apply a median-based scaling strategy to address scale ambiguity. A higher depth accuracy score indicates better geometric consistency with the real-world scene. 

**Perspectivity** evaluates the 3D plausibility of the video, focusing on factors such as scale variation with depth, lighting consistency, and occlusion relationships. We use Qwen3VL as a judge to assess the perspective, judging whether the video adheres to realistic 3D geometry. A higher score reflects better perspective alignment with real-world scenes. 

### 3.1.6. CONTROLLABILITY 

Controllability measures the model’s ability to respond to external instructions. We evaluate whether generated videos align with intended actions and instructions using three metrics: 

**Instruction Following** assesses the model’s accuracy in following instructions regarding action type, target object, and task state, measured by a VLM-based judge (Qwen3VL) and scores normalized to [0,1]. 

**Semantic Alignment** measures how well the generated video matches the semantic meaning of the instruction by computing cosine similarity between Qwen2.5-VLgenerated (Bai et al., 2025b) descriptions of the generated and reference videos. 

4 

**Preprint** 


_Figure 2._ Illustrations of the video quality evaluations across six dimensions: visual quality, motion quality, content consistency, physics adherence, 3D accuracy, and controllability. 

**Action Following** evaluates video diversity in response to different instructions. For a given initial frame, we automatically generate three distinct instructions and then use the world model to generate corresponding videos. The diversity score is the average pairwise feature dissimilarity, with higher values indicating greater diversity. 

### **3.2. Embodied Task Evaluation** 

In this section, we evaluate the capabilities of world models through three embodied tasks, as illustrated in Figure 3. 

**Embodied Data Engine.** World models can generate future observations based on external instructions, enabling synthetic data generation to supplement training data for downstream embodied policy models and alleviate the scarcity of real-world data. In this part, we treat world models as embodied data synthesis engines and evaluate their performance by measuring the gain they provide to policy models. We employ a two-phase training procedure. In the first phase, we fine-tune the world model on the RobotTwin 2.0 dataset and generate synthetic videos conditioned on the first frame and external instructions. In the second phase, we freeze the world model’s weights and integrate an inverse dynamics model (IDM) to extract actions from video features. Specifically, we follow the VPP (Hu et al., 2024) design of the diffusion policy head, guiding an action denoising head with intermediate world model features for action prediction. This process produces paired video-action sequences. We then evaluate the impact of world model–generated synthetic data by training a baseline _π_ 0 _._ 5 (Intelligence et al., 2025) policy model with varying amounts of synthetic data. The performance gain of the policy model reflects the world model’s capability to enhance policy learning. 

an action-controllable world model, generating observation videos through a rollout process that continues until it exceeds 20% more frames than the corresponding ground truth video. Task success is evaluated using a VLM, which determines whether the embodied task was executed successfully. The used prompt for the VLM is shown in Appendix B. The success rate from the world model’s evaluation is compared to that from the RoboTwin simulator. A high correlation between the two suggests effective simulation of real-world dynamics, while a low correlation indicates a mismatch in environmental transition simulation. 

**Embodied Action Planner.** By predicting future state transitions, world models can function as the action-planning ”brain” of an embodied agent. In this part, we investigate the ability of world models to execute embodied tasks in a closed-loop manner. Similar to the data synthesis engine setup, we pair the world model with an inverse dynamics model, where the world model takes textual instructions and the initial frame as input and outputs the corresponding action sequence for future operations. This sequence is then executed in the RoboTwin simulator, and the task success rate is measured to evaluate the world model’s performance in closed-loop action execution. 

### **3.3. Human Evaluation** 

Since video quality metrics alone cannot fully capture aspects like physical plausibility and instruction adherence, we incorporate two types of human evaluations. The first type involves scoring three key dimensions: overall video quality, instruction following, and physical adherence on a 1 to 5 scale, then normalizing to a 0-100 range. The second type is a head-to-head comparison, where annotators choose the superior video generated by two different models from the same prompt, yielding a win-rate metric. We recruited 70 annotators who evaluated a total of 3500 videos. 

### **3.4. EWMScore Metric** 

After computing the 16 video quality metrics spanning six perceptual dimensions, we apply a linear normalization based on empirically defined metric boundaries to map all scores into the range, and subsequently scale them to [0,100]. We then compute the arithmetic mean across all normalized metrics to obtain a single composite score, referred to as **EWMScore** . EWMScore serves as an objective and automated metric for assessing the overall generative quality of embodied world models. 

**Embodied Policy Evaluator.** In this section, we assess the capability of world models as environment proxies for evaluating policy performance. We train a series of policy models ( _π_ 0 _._ 5) with varying capabilities using the RoboTwin 2.0 dataset. These models are evaluated by interacting with 

5 

**Preprint** 


_Figure 3._ Overview of the embodied task evaluation systems, including the assessment of world models as embodied data engines (measuring success rate of trained downstream policies), policy evaluators (measuring correlation between world model and real-world evaluation results), and action planners (measuring success rate of world model-based policies). 

## **4. Experiments** 

### **4.1. Experimental Setup** 

**Dataset.** We focus on robotic manipulation scenarios, using the RoboTwin 2.0 (Chen et al., 2025) dataset and simulator for evaluation, which includes 50 task scenarios and 2500 videos. For video quality evaluation, we use 2000 videos to train the world model and 500 videos for testing. For the embodied data engine task, we train the _π_ 0 _._ 5 policy model with 10%, 20%, 30%, 50%, and 100% of the data, resulting in a series of policy models with varying performance. For policy evaluation and action planning tasks, we conduct evaluations within the RoboTwin simulator environment. 

**Tested Models.** We evaluate 14 representative world models, covering both general-purpose video world models and embodied-specific models. The evaluated general video world models include CogvideoX (Yang et al., 2024b), Wan 2.2 (Wan et al., 2025), Wan 2.6 (Wan et al., 2025), and Veo 3.1<sup>1</sup> . The text-conditioned embodied world models consist of Genie Envisioner (Liao et al., 2025), GigaWorld (Team et al., 2025), TesserAct (Zhen et al., 2025), Cosmos-Predict 2.5 (Gu, 2025), WOW (Chi et al., 2025), RoboMaster<sup>2</sup> , Cosmos-Predict 2.5 (text) (Gu, 2025), and Vidar (Feng et al., 2025). In addition, we include action-conditioned embodied world models, namely IRASim (Zhu et al., 2024a), Cosmos-Predict 2.5 (action) (Gu, 2025) and CtrlWorld (Guo 

et al., 2025). For fair comparison, all models with available training code are post-trained on the used dataset following their official implementations. 

### **4.2. Results** 

### 4.2.1. VISUAL QUALITY EVALUATION 

Tables 2 and 3 summarize video quality evaluation results across six evaluation dimensions. Overall, embodied world models exhibit stronger performance on structureand interaction-related metrics, while general-purpose video models mainly excel in perceptual quality. Among embodied models, CtrlWorld and TesserAct score highly in subject consistency, background stability, and trajectory accuracy, indicating better alignment with manipulation dynamics. WoW shows strong action-following ability, while RoboMaster and Vidar maintain balanced performance across motion smoothness and content consistency. The open-source video model CogvideoX excels in visual quality and content consistency but lags in physics adherence and motion quality. Closed-source commercial models (Veo 3.1 and Wan 2.6) achieve the highest visual and aesthetic scores, though they show limited improvements in embodied-specific metrics. Qualitative results suggest that visually strong models tend to suffer from semantic drift, while embodied world models produce more coherent and goal-consistent action sequences. 

> 1https://aistudio.google.com/models/veo-3 

> 2https://huggingface.co/datasets/robomaster2025/RoboMaster 

6 

**Preprint** 

_Table 2._ Video quality evaluation results across visual quality, motion quality and content consistency dimensions. 

|**Models**||**Visual Quali**|**ty**|**M**|**otion Qu**|**ality**|**C**|**ontent Consis**|**tency**|
|---|---|---|---|---|---|---|---|---|---|
||Image<br>Quality|Aesthetic<br>Quality|JEPA<br>Similarity|Dynamic<br>Degree|Flow<br>Score|Motion<br>Smoothness|Subject<br>Consist.|Background<br>Consist.|Photometric<br>Consist.|
|GigaWorld-0|0.5041|0.3991|0.4413|0.6709|0.3118|0.7811|0.7303|0.8563|0.1756|
|Genie Envisioner|0.2305|0.3289|0.3340|0.6930|0.0855|0.6966|0.7760|0.9024|0.2006|
|TesserAct|0.3322|0.4590|0.4579|0.5150|0.2447|0.7579|0.8250|**0.9238**|0.2491|
|RoboMaster|0.3487|0.3842|0.2966|0.6124|0.1484|0.6940|0.8295|0.9123|0.3356|
|Vidar|0.4145|0.4068|0.5608|0.2767|0.1426|0.7973|0.7629|0.8300|0.2350|
|Cosmos-Predict 2.5 (text)|0.6668|0.4501|0.3126|0.5911|0.4302|0.7882|0.7488|0.8511|0.1383|
|<br>Cosmos-Predict 2.5 (action)|0.4489|0.3576|0.9296|0.3994|0.0573|0.7100|0.8197|0.8894|0.3528|
|WoW|0.4587|0.3868|0.7440|0.4608|0.2706|0.7692|0.8161|0.9025|0.2170|
|CtrlWorld|0.3522|0.3893|0.9185|0.4257|0.3449|0.7377|**0.8411**|0.9057|0.1729|
|Wan 2.2|0.3884|0.3963|0.7575|0.4349|0.1269|0.7019|0.8388|0.9042|**0.4776**|
|CogvideoX|0.3582|0.3777|**0.9384**|0.3166|0.2189|0.7391|0.8083|0.8773|0.3580|
|IRASim|0.3489|0.3623|0.9330|0.4139|0.2083|0.7052|0.8312|0.9068|0.3522|
|Veo 3.1|0.6605|**0.4632**|0.5694|0.5450|0.1396|0.6989|0.7878|0.8710|0.3247|
|Wan 2.6|**0.6824**|0.4433|0.7229|**0.7421**|**0.4532**|**0.8539**|0.7517|0.8687|0.1904|


_Table 3._ Video quality evaluation results across physics adherence, 3D accuracy and controllability dimensions. 

|**Models**|**Physics A**|**dherence**|**3D**|**Accuracy**|**C**|**ontrollabilit**|**y**|
|---|---|---|---|---|---|---|---|
||Interaction<br>Quality|Trajectory<br>Acc.|Depth<br>Acc.|Perspectivity|Instruction<br>Following|Semantic<br>Alignment|Action<br>Following|
|GigaWorld-0|0.5368|0.1552|0.6316|0.7596|0.6156|0.8591|0.1134|
|Genie Envisioner|0.2052|0.0679|0.8663|0.5284|0.2028|0.8544|0.0109|
|TesserAct|0.5800|0.1396|0.7159|0.7920|0.6152|0.8783|0.0311|
|RoboMaster|0.5364|0.1158|0.8335|0.7588|0.5772|0.8761|0.0352|
|Vidar|0.5348|0.1928|0.7872|0.7592|0.5912|0.8826|0.0819|
|Cosmos-Predict 2.5 (text)|0.3872|0.0816|0.7051|0.7964|0.2664|0.7733|**0.1418**|
|Cosmos-Predict 2.5(action)|0.5500|0.2945|0.8862|0.7644|0.5840|0.8879|0.0133|
|WoW|0.5564|0.2058|0.7283|0.7672|0.5692|0.8842|0.0434|
|CtrlWorld|0.6212|**0.4766**|0.9300|0.7960|0.7272|0.8912|0.0210|
|Wan 2.2|0.5184|0.1627|0.7768|0.7660|0.5376|0.8877|0.0512|
|CogvideoX|0.5940|0.3526|0.9097|0.7828|0.7268|**0.8977**|0.0076|
|IRASim|0.5656|0.3639|**0.9312**|0.7788|0.6604|0.8849|0.0526|
|Veo 3.1|**0.7872**|0.1231|0.7421|**0.8276**|**0.9328**|0.8607|0.0852|
|Wan 2.6|0.7280|0.1182|0.7144|0.8032|0.8536|0.8728|0.0992|


### 4.2.2. EMBODIED TASK EVALUATION 

In this section, we evaluate the capabilities of world models through three embodied tasks. 

**Embodied Data Engine.** We evaluate six representative 

world models as data synthesis engines by measuring their impact on downstream policy learning. The evaluation is conducted on two manipulation tasks: _adjust bottle_ (Task 1) and _click bell_ (Task 2), each executed 100 times, with the success rate averaged. For each task, we train a _π_ 0 _._ 5 policy using 25 synthetic trajectories generated by each world model. As shown in Table 4, we observe that synthetic 

7 

**Preprint** 


_Figure 5._ Correlation between EWMScore with human evaluation and embodied task performance results. 

_Table 5._ Task success rate of different world models directly as action planners in the RoboTwin simulator. 

|Model|Task 1|Task 2|
|---|---|---|
|_π_0_._5policy model|77%|66%|
|Genie Envisioner (Liao et al.,2025)|10%|20%|
|TesserAct (Zhen et al.,2025)|1%|35%|
|RoboMaster (rob,2025)|8%|20%|
|Vidar (Feng et al.,2025)|2%|19%|
|WoW (Chi et al.,2025)|20%|21%|
|Wan 2.2 (Wan et al.,2025)|12%|20%|


action sequences in the RoboTwin simulator. As shown in Table 5, while several world models achieve non-trivial success rates across tasks, their overall performance remains substantially lower than that of VLA policies such as _π_ 0 _._ 5. These results indicate that, although current embodied world models capture useful predictive structure, they still struggle to reliably support closed-loop task execution, particularly over long horizons. This indicates significant room for improvement in leveraging world models for autonomous embodied control. 

### 4.2.3. HUMAN EVALUATION 

data from most world models provides some performance gains across both tasks but still lags behind real data. Only generated data from RoboMaster and WoW surpass realdata training on Task 2. These results suggest that the quality of generated data remains insufficient for effective policy training, indicating that current embodied world models are not yet reliable data sources for downstream learning. 

**Embodied Policy Evaluator.** We investigate whether world models can serve as proxy simulation environments for policy evaluation. To this end, we train five policy models _π_ 0 _._ 5 with varying performance levels. Each policy is then evaluated by interacting with an action-controllable world model, which generates observation rollouts conditioned on the policy’s actions. As shown in Figure 4, CtrlWorld exhibits a strong correlation with the evaluation results from the RoboTwin simulator, indicating that it effectively captures meaningful environment transition dynamics. In contrast, Cosmos-Predict 2.5 shows a weaker correlation, suggesting that it struggles to accurately model the environment dynamics. Moreover, both models have consistently higher success rates than those measured in the simulator, suggesting partial overfitting to successful trajectories. 

**Embodied Action Planner.** Similar to the data engine task setting, we evaluate six representative world models as end-to-end action planners by executing their predicted 

As shown in Figure 1 (b), human evaluations reveal that commercial and large-scale general video models (e.g., Veo 3.1 and Wan 2.6) consistently achieve the highest scores across overall quality, instruction following, and physical adherence, indicating strong perceptual realism and semantic alignment. Among embodied world models, actionconditioned approaches such as CtrlWorld demonstrate notably better physical adherence and higher win rates than text-only counterparts, suggesting that explicit action modeling plays a critical role in producing physically plausible interactions. In contrast, earlier text-conditioned embodied models (e.g., Genie Envisioner) receive substantially lower scores across all dimensions, reflecting persistent gaps in long-horizon coherence and instruction compliance. 

### **4.3. Inter-metric Analysis** 

Figure 5 presents a cross-dimensional analysis relating EWMScore to both human evaluation and embodied task performance. We observe a strong correlation between EWMScore and human judgments (Pearson _r_ = 0 _._ 825), indicating a high degree of alignment with subjective perceptual assessments. In contrast, EWMScore exhibits only moderate correlation with data synthesis performance ( _r_ = 0 _._ 600) and a weak correlation with action planning performance ( _r_ = 0 _._ 360). These results suggest that while perceptual realism is a necessary condition for favorable 

8 

**Preprint** 

human evaluation, it does not directly translate into proportional gains in downstream embodied tasks. In particular, the limited correlation with action planning indicates that current synthetic data, despite achieving high visual fidelity, remains insufficient to provide strong predictive or decisionrelevant signals for complex embodied reasoning. 

## **5. Conclusion and Future Work** 

In this work, we present WorldArena, a unified benchmark for systematically evaluating embodied world models from both perceptual and functional perspectives, integrating multi-dimensional video quality metrics, embodied task evaluations, and human assessments. Through an extensive evaluation of 14 representative models, we reveal consistent gaps between perceptual quality and embodied task performance, highlighting that strong visual generation alone is insufficient for reliable embodied decision-making. We further demonstrate that EWMScore effectively captures overall generative capability and correlates well with human judgments. In the future, we will continue to expand WorldArena, incorporating more models to support the advancement of perceptually strong and functionally reliable embodied world models. 

## **References** 

Robomaster. https://www.robomaster.com/, 2025. 

- Assran, M., Bardes, A., Fan, D., Garrido, Q., Howes, R., Muckley, M., Rizvi, A., Roberts, C., Sinha, K., Zholus, A., et al. V-jepa 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 

- Bai, S., Cai, Y., Chen, R., Chen, K., Chen, X., Cheng, Z., Deng, L., Ding, W., Gao, C., Ge, C., Ge, W., Guo, Z., Huang, Q., Huang, J., Huang, F., Hui, B., Jiang, S., Li, Z., Li, M., Li, M., Li, K., Lin, Z., Lin, J., Liu, X., Liu, J., Liu, C., Liu, Y., Liu, D., Liu, S., Lu, D., Luo, R., Lv, C., Men, R., Meng, L., Ren, X., Ren, X., Song, S., Sun, Y., Tang, J., Tu, J., Wan, J., Wang, P., Wang, P., Wang, Q., Wang, Y., Xie, T., Xu, Y., Xu, H., Xu, J., Yang, Z., Yang, M., Yang, J., Yang, A., Yu, B., Zhang, F., Zhang, H., Zhang, X., Zheng, B., Zhong, H., Zhou, J., Zhou, F., Zhou, J., Zhu, Y., and Zhu, K. Qwen3-vl technical report. _arXiv preprint arXiv:2511.21631_ , 2025a. 

- Bai, S., Chen, K., Liu, X., Wang, J., Ge, W., Song, S., Dang, K., Wang, P., Wang, S., Tang, J., Zhong, H., Zhu, Y., Yang, M., Li, Z., Wan, J., Wang, P., Ding, W., Fu, Z., Xu, Y., Ye, J., Zhang, X., Xie, T., Cheng, Z., Zhang, H., Yang, Z., Xu, H., and Lin, J. Qwen2.5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025b. 

- Bardes, A., Garrido, Q., Ponce, J., Chen, X., Rabbat, M., LeCun, Y., Assran, M., and Ballas, N. V-jepa: Latent video prediction for visual representation learning. 2023. 

- Carion, N., Gustafson, L., Hu, Y.-T., Debnath, S., Hu, R., Suris, D., Ryali, C., Alwala, K. V., Khedr, H., Huang, A., et al. Sam 3: Segment anything with concepts. _arXiv preprint arXiv:2511.16719_ , 2025. 

- Caron, M., Touvron, H., Misra, I., Jegou,´ H., Mairal, J., Bojanowski, P., and Joulin, A. Emerging properties in self-supervised vision transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 9650–9660, 2021. 

- Chen, T., Chen, Z., Chen, B., Cai, Z., Liu, Y., Li, Z., Liang, Q., Lin, X., Ge, Y., Gu, Z., et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- Chi, X., Jia, P., Fan, C.-K., Ju, X., Mi, W., Zhang, K., Qin, Z., Tian, W., Ge, K., Li, H., et al. Wow: Towards a world omniscient world model through embodied interaction. _arXiv preprint arXiv:2509.22642_ , 2025. 

- Ding, J., Zhang, Y., Shang, Y., Zhang, Y., Zong, Z., Feng, J., Yuan, Y., Su, H., Li, N., Sukiennik, N., et al. Understanding world or predicting future? a comprehensive survey of world models. _ACM Computing Surveys_ , 58(3):1–38, 2025. 

- Duan, H., Yu, H.-X., Chen, S., Fei-Fei, L., and Wu, J. Worldscore: A unified evaluation benchmark for world generation. _arXiv preprint arXiv:2504.00983_ , 2025. 

- Fan, C.-K., Chi, X., Ju, X., Li, H., Bao, Y., Wang, Y.-K., Chen, L., Jiang, Z., Ge, K., Li, Y., et al. Wow, wo, val! a comprehensive embodied world model evaluation turing test. _arXiv preprint arXiv:2601.04137_ , 2026. 

- Feng, Y., Tan, H., Mao, X., Xiang, C., Liu, G., Huang, S., Su, H., and Zhu, J. Vidar: Embodied video diffusion model for generalist manipulation. _arXiv preprint arXiv:2507.12898_ , 2025. 

- Gu, J. Cosmos world foundation models for physical ai. In _Proceedings of the 3rd International Workshop on Rich Media With Generative AI_ , pp. 39–39, 2025. 

- Guo, Y., Shi, L. X., Chen, J., and Finn, C. Ctrl-world: A controllable generative world model for robot manipulation. _arXiv preprint arXiv:2510.10125_ , 2025. 

- Hafner, D., Pasukonis, J., Ba, J., and Lillicrap, T. Mastering diverse control tasks through world models. _Nature_ , pp. 1–7, 2025. 

9 

**Preprint** 

- Hu, Y., Guo, Y., Wang, P., Chen, X., Wang, Y.-J., Zhang, J., Sreenath, K., Lu, C., and Chen, J. Video prediction policy: A generalist robot policy with predictive visual representations. _arXiv preprint arXiv:2412.14803_ , 2024. 

- Huang, S., Chen, L., Zhou, P., Chen, S., Jiang, Z., Hu, Y., Liao, Y., Gao, P., Li, H., Yao, M., et al. Enerverse: Envisioning embodied future space for robotics manipulation. _arXiv preprint arXiv:2501.01895_ , 2025. 

- Huang, Z., He, Y., Yu, J., Zhang, F., Si, C., Jiang, Y., Zhang, Y., Wu, T., Jin, Q., Chanpaisit, N., et al. Vbench: Comprehensive benchmark suite for video generative models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 21807–21818, 2024. 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Galliker, M. Y., Ghosh, D., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., LeBlanc, D., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Ren, A. Z., Shi, L. X., Smith, L., Springenberg, J. T., Stachowicz, K., Tanner, J., Vuong, Q., Walke, H., Walling, A., Wang, H., Yu, L., and Zhilinsky, U. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. 2025. URL https: //arxiv.org/abs/2504.16054. 

- Jang, J., Ye, S., Lin, Z., Xiang, J., Bjorck, J., Fang, Y., Hu, F., Huang, S., Kundalia, K., Lin, Y.-C., et al. Dreamgen: Unlocking generalization in robot learning through video world models. _arXiv preprint arXiv:2505.12705_ , 2025. 

- Ke, J., Wang, Q., Wang, Y., Milanfar, P., and Yang, F. Musiq: Multi-scale image quality transformer. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 5148–5157, 2021. 

- Kong, L., Yang, W., Mei, J., Liu, Y., Liang, A., Zhu, D., Lu, D., Yin, W., Hu, X., Jia, M., et al. 3d and 4d world modeling: A survey. _arXiv preprint arXiv:2509.07996_ , 2025. 

- LAION-AI. Aesthetic predictor. https://github. com/LAION-AI/aesthetic-predictor, 2022. Accessed: 2024. 

- Li, D., Fang, Y., Chen, Y., Yang, S., Cao, S., Wong, J., Luo, M., Wang, X., Yin, H., Gonzalez, J. E., et al. Worldmodelbench: Judging video generation models as world models. _arXiv preprint arXiv:2502.20694_ , 2025a. 

- Li, Y., Zhu, Y., Wen, J., Shen, C., and Xu, Y. Worldeval: World model as real-world robot policies evaluator. _arXiv preprint arXiv:2505.19017_ , 2025b. 

- Liang, A., Kong, L., Yan, T., Liu, H., Yang, W., Huang, Z., Yin, W., Zuo, J., Hu, Y., Zhu, D., Lu, D., Liu, Y., Jiang, G., Li, L., Li, X., Zhuo, L., Ng, L. X., Cottereau, B. R., Gao, C., Pan, L., Ooi, W. T., and Liu, Z. WorldLens: Full-spectrum evaluations of driving world models in real world. _arXiv preprint arXiv:2512.10958_ , 2025. 

- Liao, Y., Zhou, P., Huang, S., Yang, D., Chen, S., Jiang, Y., Hu, Y., Cai, J., Liu, S., Luo, J., et al. Genie envisioner: A unified world foundation platform for robotic manipulation. _arXiv preprint arXiv:2508.05635_ , 2025. 

- Liu, B. K. and Chen, Z. P. Jepa-reasoner: Decoupling latent reasoning from token generation. _arXiv preprint arXiv:2512.19171_ , 2025. 

- Liu, Y., Cun, X., Liu, X., Wang, X., Zhang, Y., Chen, H., Liu, Y., Zeng, T., Chan, R., and Shan, Y. Evalcrafter: Benchmarking and evaluating large video generation models. _arXiv preprint arXiv:2310.11440_ , 2023. 

- Long, X., Zhao, Q., Zhang, K., Zhang, Z., Wang, D., Liu, Y., Shu, Z., Lu, Y., Wang, S., Wei, X., et al. A survey: Learning embodied intelligence from physical simulators and world models. _arXiv preprint arXiv:2507.00917_ , 2025. 

- Lu, Y., Luo, W., Tu, P., Li, H., Zhu, H., Yu, Z., Wang, X., Chen, X., Peng, X., Li, X., et al. 4dworldbench: A comprehensive evaluation framework for 3d/4d world generation models. _arXiv preprint arXiv:2511.19836_ , 2025. 

- Luo, G. Y., Favero, G., Luo, Z. H., Jolicoeur-Martineau, A., and Pal, C. Beyond fvd: Enhanced evaluation metrics for video generation quality, 2024. URL https://arxiv. org/abs/2410.05203. 

- Muller,¨ M. _Information Retrieval for Music and Motion_ . 01 2007. ISBN 978-3-540-74047-6. doi: 10.1007/ 978-3-540-74048-3. 

- Qian, Z., Chi, X., Li, Y., Wang, S., Qin, Z., Ju, X., Han, S., and Zhang, S. Wristworld: Generating wrist-views via 4d world models for robotic manipulation. _arXiv preprint arXiv:2510.07313_ , 2025. 

- Qin, Y., Shi, Z., Yu, J., Wang, X., Zhou, E., Li, L., Yin, Z., Liu, X., Sheng, L., Shao, J., et al. Worldsimbench: Towards video generation models as world simulators. _arXiv preprint arXiv:2410.18072_ , 2024. 

- Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G., and Sutskever, I. Learning transferable visual models from natural language supervision, 2021. URL https://arxiv.org/abs/2103.00020. 

10 

**Preprint** 

- Shang, Y., Tang, Y., Zhang, X., Wang, S., Yan, Y., Zhang, H., Zheng, Z., Zhao, J., Feng, J., Gao, C., et al. A survey of embodied world models. 2025a. 

- Shang, Y., Zhang, X., Tang, Y., Jin, L., Gao, C., Wu, W., and Li, Y. Roboscape: Physics-informed embodied world model. _arXiv preprint arXiv:2506.23135_ , 2025b. 

- Team, G., Ye, A., Wang, B., Ni, C., Huang, G., Zhao, G., Li, H., Zhu, J., Li, K., Xu, M., et al. Gigaworld-0: World models as data engine to empower embodied ai. _arXiv preprint arXiv:2511.19861_ , 2025. 

- Teed, Z. and Deng, J. Raft: Recurrent all-pairs field transforms for optical flow. In _European conference on computer vision_ , pp. 402–419. Springer, 2020. 

- Wan, T., Wang, A., Ai, B., Wen, B., Mao, C., Xie, C.-W., Chen, D., Yu, F., Zhao, H., Yang, J., et al. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 

- Yang, L., Kang, B., Huang, Z., Zhao, Z., Xu, X., Feng, J., and Zhao, H. Depth anything v2. _arXiv:2406.09414_ , 2024a. 

- Yang, Z., Teng, J., Zheng, W., Ding, M., Huang, S., Xu, J., Yang, Y., Hong, W., Zhang, X., Feng, G., et al. Cogvideox: Text-to-video diffusion models with an expert transformer. _arXiv preprint arXiv:2408.06072_ , 2024b. 

- Yue, H., Huang, S., Liao, Y., Chen, S., Zhou, P., Chen, L., Yao, M., and Ren, G. Ewmbench: Evaluating scene, motion, and semantic quality in embodied world models. _arXiv preprint arXiv:2505.09694_ , 2025. 

- Zhang, G., Liu, C., Cui, Y., Zhao, X., Ma, K., and Wang, L. Vfimamba: Video frame interpolation with state space models, 2024. URL https://arxiv.org/ abs/2407.02315. 

- Zhang, J., Jiang, M., Dai, N., Lu, T., Uzunoglu, A., Zhang, S., Wei, Y., Wang, J., Patel, V. M., Liang, P. P., et al. World-in-world: World models in a closed-loop world. _arXiv preprint arXiv:2510.18135_ , 2025. 

- Zhen, H., Sun, Q., Zhang, H., Li, J., Zhou, S., Du, Y., and Gan, C. Tesseract: learning 4d embodied world models. _arXiv preprint arXiv:2504.20995_ , 2025. 

- Zhu, F., Wu, H., Guo, S., Liu, Y., Cheang, C., and Kong, T. Irasim: Learning interactive real-robot action simulators. _arXiv preprint arXiv:2406.14540_ , 2024a. 

- Zhu, Z., Wang, X., Zhao, W., Min, C., Li, B., Deng, N., Dou, M., Wang, Y., Shi, B., Wang, K., et al. Is sora a world simulator? a comprehensive survey on general world models and beyond. _arXiv preprint arXiv:2405.03520_ , 2024b. 

11 

**Preprint** 

## **A. Additional Details on Metrics** 

### **A.1. Image Quality** 

The per-frame sharpness of a generated video constitutes the foundation of its visual presentation. Unlike traditional reference-based metrics such as PSNR, which rely on ground-truth images, we adopt the **MUSIQ** (Multi-scale Image Quality Transformer) model (Ke et al., 2021) to evaluate technical distortions in a no-reference setting, including overexposure, sensor noise, and compression artifacts. MUSIQ leverages a multi-scale Transformer architecture to capture the relationships between local details and global composition. 

For a video sequence _V_ = _{I_ 1 _, I_ 2 _, . . . , IT }_ ,where _V_ represents a specific video and _Ii_ represents the _i_ th frame of the video _V_ , the image quality score _S_ img is defined as: 


where Φmusiq( _·_ ) denotes the pretrained quality prediction function. A higher value of _S_ img indicates greater visual purity and clarity at the level of digital image (Huang et al., 2024). 

### **A.2. Aesthetic Quality** 

Beyond technical fidelity, generated videos are also required to conform to human aesthetic principles, such as harmonious lighting and visually pleasing color composition. We employ the **LAION Aesthetic Predictor** (LAION-AI, 2022) to perform aesthetic feature mapping for each frame. Similarly, for a video sequence _V_ = _{I_ 1 _, I_ 2 _, . . . , IT }_ , the aesthetic quality score _S_ aes is defined as: 


where Ψaes( _·_ ) maps each image into a high-dimensional feature space and predicts an aesthetic score. This formulation ensures that the evaluation extends beyond pixel-level sharpness to encompass perceptual coherence and artistic consistency (Huang et al., 2024). 

### **A.3. JEPA Similarity** 

To evaluate video quality from a global feature-distribution perspective and detect high-level spatiotemporal collapse, we introduce the **JEPA Similarity** . Unlike traditional FVD metric, which relies on Gaussian assumptions, JEPA measures the maximum mean discrepancy (MMD) between feature distributions to provide evaluation results that better align with human perception: 


where _α_ = 40 is a scaling factor that enhances numerical distinguishability, _F_ gen and _F_ refdenote the feature space distributions of the generated video set and the reference expert demonstration(GT) set, respectively, extracted by a pretrained **V-JEPA** encoder (Bardes et al., 2023) which is pre-trained via masked prediction tasks and enables the model to capture high-level spatio-temporal causality and physical logic in videos, offering greater robustness to temporal warping 2 and content variations.MMD<sup>�</sup> poly<sup>represents the squared estimator of the Maximum Mean Discrepancy using a second-order</sup> polynomial kernel, defined as _k_ ( **x** _,_ **y** ) = ( _γ⟨_ **x** _,_ **y** _⟩_ + _c_ 0)<sup>2</sup> ,with _γ_ = 1 _, c_ 0 = 0, It measures the distance between the two feature sets in the reproducing kernel Hilbert space (RKHS), computed as follows: 


where _m_ and _n_ denote the number of samples in the generated videos and the reference videos, **f** _i_<sup>gen</sup> and **f** _i_<sup>ref</sup> are the corresponding V-JEPA feature vectors. Higher values indicate closer alignment to reference demonstrations (Luo et al., 2024). 

12 

**Preprint** 

This metric is not only sensitive to breakdowns in high-level spatio-temporal logic but also avoids the Gaussian distribution assumption, offering significantly better sample efficiency than conventional metrics. Moreover, it achieves a enormous improvement in correlation with human subjective assessments, especially when evaluating complex embodied operation logic, thereby more reliably reflecting the physical plausibility and spatio-temporal consistency of the generated videos. 

### **A.4. Dynamic Degree** 

We employ the **RAFT** (Recurrent All-Pairs Field Transforms) (Teed & Deng, 2020) optical flow model to extract motion vector fields between adjacent frames. To accurately capture the most representative and salient motions in a video,such as robotic arm grasping,we focus on pixels whose optical flow magnitudes fall within the top 5% (Huang et al., 2024). 

Let **u** _t,t_ +1 denote the two-dimensional optical flow field between consecutive frames. We define the average magnitude of the active pixel set as ¯ _v_ top5. To obtain a smooth numerical mapping while introducing resolution adaptivity, we define the dynamic degree score as: 


where _τ_ = 2566<sup>_×_min(</sup><sup>_H, W_) is a resolution-adaptive threshold constant,</sup><sup>_α_controls the steepness of the mapping curve,</sup> and _S_ dyn _∈_ (0 _,_ 1). Values closer to 1 indicate more pronounced dynamic responses in the video. 

### **A.5. Flow Score** 

To quantify overall physical motion intensity and dynamic activity, we compute an optical-flow-based motion score. Given a generated video _V_ = _{I_ 1 _, . . . , IT }_ with frame width _W_ and height _H_ , we use **RAFT** (Teed & Deng, 2020) to estimate dense optical flow fields **u** _t ∈_ R<sup>_H×W ×_2</sup> between consecutive frames _It_ and _It_ +1. By averaging the magnitude of optical flow across all pixels,the average motion intensity is defined as: 


where ( _i, j_ ) indexes pixel locations, _∥· ∥_ 2 denotes the Euclidean norm ( _L_ 2 norm), which quantifies the magnitude of pixel displacement per unit time (Liu et al., 2023). In the context of embodied intelligence tasks, this metric serves a dual evaluative purpose: on the one hand, it effectively identifies whether a video degenerates into ”static frames” or exhibits only ”minimal drift” due to insufficient generative capability of the model; on the other hand, it captures whether unnatural, non-physical distortions are present in the overall scene. 

Higher values of _S_ flow ~~r~~ aw<sup>typicallyindicatemorepronounceddynamicinteractionandphysicallymeaningfulmotion.</sup> Compared to **Dynamic Degree** , this metric focuses on assessing overall motion intensity and detecting implausible global dynamics. To ensure consistent interpretation and comparability with other metrics, we will normalize _S_ flow ~~r~~ aw<sup>to the range</sup> [0 _,_ 1] in Section A.17, denoting the normalized value as _S_ flow, while preserving the property that higher values correspond to better performance. 

### **A.6. Motion Smoothness** 

To evaluate whether motion is temporally coherent and consistent with physical inertia, we adopt a reconstruction-based strategy using a video frame interpolation model ( **VFI-Mamba** )(Zhang et al., 2024). Given all frames of a video, we take the odd-indexed frames _{I_ 1 _, I_ 3 _, . . . }_ as inputs and predict the corresponding intermediate frames _I_ mid, which are then compared with the ground-truth(GT) frames. If the motion is physically plausible and smooth, the intermediate frame _I_ mid should be accurately reconstructed from its surrounding frames ( _I_ prev _, I_ next) via nonlinear interpolation. 

The key innovation lies in incorporating motion magnitude as a weighting factor to avoid overestimating static backgrounds. The final motion smoothness score is defined as: 


where _N_ denotes the number of predicted intermediate frames (typically equal to or one less than the number of evenindexed frames), _I_<sup>ˆ</sup> pred is the interpolated frame predicted by the model, _I_ mid is the real frame between _I_ prevand _I_ next, and diff( _·_ ) 

13 

**Preprint** 

represents the mean raw pixel-wise difference between two frames. The logarithmic weighting ln(1 + _x_ ) compensates for the increased difficulty of interpolation under large motion, thereby assigning higher rewards to sequences that maintain high reconstruction fidelity even during rapid motion. For consistency with other evaluation metrics, _S_ smooth ~~r~~ aw<sup>will be</sup> normalized to the range [0 _,_ 1] in Section A.17, yielding the final smoothness score _S_ smooth, where higher values indicate superior temporal coherence and motion consistency. 

### **A.7. Subject Consistency** 

For a video sequence _V_ = _{I_ 1 _, I_ 2 _, . . . , IT }_ , we extract frame-level features using **DINO** (Caron et al., 2021), denoted as _fi_ = DINO( _Ii_ ), which emphasize the spatial topological structure of objects. We compute the cosine similarity between the feature _fi_ of the current frame and both the first-frame feature _f_ 1 and the previous-frame feature _fi−_ 1, and average the similarities across all frames (Huang et al., 2024): 


However, a common “shortcut” phenomenon in video generation evaluation is that models may produce nearly static videos to obtain artificially high consistency scores. To faithfully reflect dynamic generation capability in embodied scenarios, we introduce the dynamic degree _S_ dyn defined in Section A.4 as a weighting factor for subject consistency. Specifically, when the video’s dynamic degree falls below a predefined threshold _γ_ , the raw score is penalized as: 


This mechanism ensures that static or near-static videos cannot achieve high scores even when frame-level similarity is extremely high, leading to more reasonable evaluation in embodied tasks. 

### **A.8. Background Consistency** 

Analogous to subject consistency, for a video sequence _V_ = _{I_ 1 _, I_ 2 _, . . . , IT }_ , we extract frame-level features using **CLIP** (Radford et al., 2021), denoted as _hi_ = CLIP( _Ii_ ), which place greater emphasis on global scene semantics and prevent uncontrolled background variation during generation. We compute the cosine similarity between _hi_ and both _h_ 1 and _hi−_ 1, and average the results across all frames (Huang et al., 2024): 


Similarly, the final background consistency score is adjusted using the dynamic degree: 

### **A.9. Photometric Consistency** 

Photometric consistency measures the physical stability of textures at the pixel level. For a video _V_ = _{I_ 1 _, I_ 2 _, . . . , IT }_ , we use the forward optical flow field **u** _t_ between frames _It_ and _It_ +1, as well as the backward flow field **u**<sup>_′_</sup> _t_ +1<sup>, to warp pixels</sup> from frame _t_ to frame _t_ + 1 and then back to frame _t_ . The average end-point error (AEPE) is defined as (Duan et al., 2025): 


Since this metric quantifies pixel-level reconstruction error, lower values correspond to superior visual quality. To obtain a positively correlated measure that appropriately rewards sequences with meaningful motion while penalizing trivial solutions in static videos, we compute the pre-normalized photometric consistency score as: 

14 

**Preprint** 

where _S_ dyn denotes the dynamic degree (formally defined in Section A.4), quantifying the overall motion intensity within a video sequence, and _γ_ serves as a dynamic threshold that modulates the penalty for insufficient motion. The inclusion of _S_ dyn addresses a critical limitation of conventional photometric metrics: static or near-static sequences often achieve artificially high scores due to minimal frame-to-frame variations, even though they fail to demonstrate meaningful dynamic modeling. 

By scaling the raw reciprocal score with the normalized dynamic degree, our formulation ensures that only videos with sufficient motion ( _S_ dyn _≥ γ_ ) retain their full photometric consistency score, while static sequences are proportionally penalized. This encourages the model to maintain high reconstruction fidelity under actual motion rather than exploiting static scenarios. Subsequently, _S_ photo ~~r~~ aw<sup>isnormalizedtotheinterval[0</sup><sup>_,_1]inSectionA.17,whichproducesthefinal</sup> photometric consistency metric _S_ photo, where higher values denote enhanced visual fidelity and temporal coherence. 

### **A.10. Interaction Quality** 

This metric evaluates the physical plausibility of interactions between the robotic arm and environmental objects, including contact behavior, force transmission, friction, inertia, and boundary integrity. We employ the pretrained multimodal model **Qwen3-VL-8B** (Bai et al., 2025a) as a VLM-based judge. Given _N_ sample sampled frames and the task instruction, the model assigns a 1–5 Likert score, which is normalized to [0 _,_ 1] to yield the final interaction quality score,the prompt used to evaluate interaction quality can be found in A.10. 

### **VLM Evaluation Prompt** 

You are an expert evaluator for robot interaction videos. You are evaluating videos generated for **embodied AI manipulation scenarios**, specifically focusing on robotic arms interacting with objects in tabletop environments. 

- **EVALUATION CONTEXT:** 

- Target scenario: Robotic manipulation (e.g., pick-place, push, grasp) 

- Expected agent: **Robotic arm/end-effector**, NOT human hands 

- Expected environment: Tabletop with objects, typical for robot manipulation tasks 

- Expected physics: Realistic robot-object interactions following physical laws 

- **CRITICAL EVALUATION PRINCIPLES:** 

1. Base ALL judgments ONLY on what is visually observable in the sampled frames 

2. DO NOT infer information not shown (no assumptions about unseen parts) 

3. Evaluate temporal coherence across the sampled frames 

4. For instruction following: Compare STRICTLY against the provided text instruction 

#### **EVALUATION DIMENSIONS & SCORING RUBRICS:** 

1. Interaction ~~Q~~ uality (Quality of robot-object interactions) 

- Score 1: Objects pass through robot or other objects; no proper contact 

- Score 2: Contact exists but interaction is unrealistic (e.g., sliding without friction, incorrect force response) 

- Score 3: Mostly plausible interactions with minor issues (e.g., slight penetration, imperfect grasping) 

- Score 4: Realistic contact physics (proper friction, force transfer, object deformation) 

- Score 5: Perfect interaction physics; indistinguishable from real robot manipulation 

2. PERSPECTIVITY (3D consistency and camera geometry) 

- Score 1: Scene has no coherent 3D structure; objects float inconsistently 

- Score 2: 3D structure is unstable (e.g., scale changes, incorrect occlusion) 

- Score 3: Reasonable 3D consistency with minor issues (e.g., slight perspective drift) 

- Score 4: Stable camera perspective with consistent depth relationships 

- Score 5: Perfect camera geometry and 3D consistency 

3. INSTRUCTION FOLLOWING (Adherence to given instruction:**VIDEO INSTRUCTION**) 

- **HALLUCINATION CHECK**: If the video shows human hands instead of robotic arms, score _≤_ 2 immediately 

- Score 1: Completely different from instruction (wrong action, wrong objects, wrong scene) 

- Score 2: Partially related but major errors (e.g., wrong target object, incorrect manipulation type) 

- Score 3: Follows general intent but with execution errors (e.g., correct action sequence but imprecise) 

- Score 4: Mostly correct with minor deviations (e.g., slight position error, extra unnecessary motion) 

- Score 5: Perfect execution of all specified elements (action, object, scene, outcome) 

- **SPECIFIC ROBOT-RELATED CHECKS:** 

- Robotic arm should have mechanical appearance, NOT human limbs 

- End-effector (gripper) should maintain consistent form throughout interaction 

- Robot motion should show appropriate joint movement and kinematics 

15 

**Preprint** 

- Object manipulation should respect object mass and inertia - Contact should be maintained appropriately during grasping/lifting **OUTPUT FORMAT REQUIREMENTS:** You MUST output a SINGLE, VALID JSON object with EXACTLY three keys: - ’Interaction ~~Q~~ uality’ - ’Perspectivity’ - ’Instruction ~~F~~ ollowing’ Each value must be an object with exactly two keys: - ‘”score”‘: integer 1-5 - ‘”reason”‘: concise explanation citing SPECIFIC visual evidence from frames **EXAMPLE OUTPUT:** { "Interaction_Quality": { "score": 2, "reason": "Object slides without friction during pushing; gripper penetrates object slightly" }, "Perspectivity": { "score": 4, "reason": "Stable camera perspective with consistent depth ordering" }, "Instruction_Following": { "score": 1, "reason": "Video shows human hand instead of robotic arm (hallucination)" } } **CRITICAL INSTRUCTIONS:** 1. Output ONLY the JSON object, no other text 2. Base scoring on observed visual evidence only 3. For instruction following: Strictly compare with the provided instruction 4. Consider temporal coherence across all sampled frames 5. Penalize hallucinations (e.g., human hands instead of robot) heavily 

Now evaluate the provided video frames based on the above criteria. 

### **A.11. Trajectory Accuracy** 

In embodied intelligence tasks, the accuracy of the robotic arm’s grasping trajectory is a core indicator of whether the model generates _effective actions_ . Trajectories encode not only low-level physical consistency but also high-level task logic and interaction constraints. To quantify this property, we first apply **SAM3** (Segment Anything Model 3) (Carion et al., 2025) to extract bounding boxes of the robotic arm in each frame. After non-maximum suppression(nms) and confidence filtering, we construct the raw trajectory sequences using the centers of candidate boxes. 

Let the ground-truth trajectory be _GT_ = ( _r_ 1 _, r_ 2 _, . . . , r|R|_ ) and the generated trajectory be _P_ = ( _p_ 1 _, p_ 2 _, . . . , p|P |_ ), where _|R|_ and _|P |_ denote the sequence lengths, respectively. To address missing detections caused by occlusion or tracking interruption, we apply linear interpolation to ensure temporal continuity. For a missing point _pi_ with _i ∈/ M_ , its position is computed as: 


where prev and next denote the nearest valid observation indices before and after _i_ . 

We then compute the normalized dynamic time warping distance (NDTW) (Muller¨ , 2007) to evaluate global alignment between the generated trajectory and the ground-truth trajectory: 


where _π_ denotes the optimal alignment path. This metric captures both temporal causality and task-stage ordering, enabling discrimination between correct and incorrect execution sequences such as ”approach-grasp-move.” Since lower NDTW 

16 

**Preprint** 

values indicate better alignment, we first derive a pre-normalized trajectory alignment score (Yue et al., 2025): 


where higher values correspond to more accurate spatial-temporal alignment with the real trajectory and more accurate actions. To ensure consistency with our evaluation framework and facilitate direct comparison with other metrics, we normalize _S_ traj ~~r~~ aw<sup>to the range [0</sup><sup>_,_1] in Section A.17, yielding the final trajectory alignment score</sup><sup>_S_</sup> traj<sup>.This normalized</sup> metric preserves the property that higher values indicate superior trajectory fidelity and task-stage adherence. 

### **A.12. Depth Accuracy** 

To evaluate whether the generated video preserves real-world spatial geometry, we compute depth discrepancies between the generated video and the ground-truth reference using the monocular depth estimation model **Depth-Anything** (Yang et al., 2024a). Since monocular depth prediction suffers from scale ambiguity, we adopt a **median-based scaling** strategy (Liang et al., 2025). 

The procedure is as follows: 

1. **Uniform Sampling** : We uniformly sample _T_ target = 40 frames from both the generated video and the ground-truth video to ensure temporal alignment. 

2. **Scale Alignment** : Depth maps _D_ gen and _D_ gt are estimated for the generated and ground-truth frames, respectively. Their medians are computed as _m_ gen = median( _D_ gen) and _m_ gt = median( _D_ gt). The scaling factor _α_ = _mm_ gengt<sup>is applied</sup> to obtain the aligned depth _D_<sup>ˆ</sup> gen = _D_ gen _· α_ . 

3. **AbsRel Error** : Within the valid pixel mask _M_ (which typically filters out noise and distant regions with ground-truth depth _D_ gt _<_ 1 _e −_ 3), the absolute relative error is computed as follows: 


where _ϵ_ is a small constant to prevent division by zero. Lower values indicate stronger depth accuracy with the real-world scene. To align this metric with our evaluation framework where higher scores correspond to better performance, we will normalize _E_ Depth to the range [0 _,_ 1] and invert its direction in Section A.17,such that higher values correspond to higher accuracy, resulting in the final normalized depth accuracy score _S_ Depth. 

### **A.13. Perspectivity** 

This metric evaluates three-dimensional geometric plausibility. The VLM examines perspective cues such as scale variation with depth, lighting consistency, and occlusion relationships during camera motion. We use **Qwen3-VL-8B** as a judge and normalize the Likert-scale output to [0 _,_ 1],which is normalized to [0 _,_ 1] to yield the final perspectivity score,the prompt used to evaluate perspectivity can be found in A.10. 

### **A.14. Instruction Following** 

This metric evaluates the semantic consistency between each generated video _Vi_ and its corresponding instruction _Insti_ , focusing on action type, target object, and final task state. We again use **Qwen3-VL-8B** as a VLM-based judge with a normalized 1–5 Likert scale, which is normalized to [0 _,_ 1] to yield the final instruction following score,the prompt used to evaluate instruction following can be found in A.10. 

### **A.15. Semantic Alignment** 

To assess whether the generated video truly understands and executes the given textual instruction, we evaluate semantic alignment as follows: 


17 

**Preprint** 

where _f_ gen _∈_ R<sup>_d_</sup> denotes the semantic feature vector of the generated video. Specifically, we first employ a vision–language model (VLM), **Qwen2.5-VL** (Bai et al., 2025b), to produce a dense structured description _L_ gen of the generated video under task-oriented prompting, covering both task summary and action sequence. This text is then encoded by the CLIP (Radford et al., 2021) text encoder Φtxt, yielding _f_ gen = Φtxt( _L_ gen). 

Similarly, _f_ gt _∈_ R<sup>_d_</sup> denotes the semantic feature vector of the ground-truth(GT) video, obtained via the same pipeline as _f_ gt = Φtxt( _L_ gt), where _L_ gt is the structured description of the reference video. The scaling factor _w_ ensures score normalization. A higher value of _S_ clip indicates stronger semantic alignment between the generated video and the reference execution. 

### **A.16. Action Following** 

This metric evaluates the model’s ability to produce distinct and correct outcomes for different action instructions. In open-loop prediction tasks, a robust model should execute multiple instructions faithfully rather than collapsing into repetitive patterns. Given a single action instruction, we manually annotate or automatically generate multiple distinct action instructions and prompt the model to generate _N_ corresponding videos. 

For each generated video _Vk_ , we extract a global CLIP feature vector _fk_ . The action-following diversity score is computed as the average pairwise feature dissimilarity(1-cosine similarity between two vectors _fi_ and _fj_ (Yue et al., 2025): 


A higher value of this metric indicates stronger capability of the model in correctly executing action instructions,which is already normalized. 

### **A.17. Score Normalization** 

Several metrics in our evaluation framework require normalization and direction alignment to ensure consistent interpretation and fair comparison across different models. Specifically, the **Flow Score** , **Trajectory Accuracy** , **Photometric Consistency** , and **Motion Smoothness** metrics are initially measured on different scales, while some metrics such as **JEPA Similarity** and **Depth Accuracy** represent error measures where lower values indicate better performance. To address these inconsistencies, we apply a two-step normalization procedure. 

For the **Flow Score** , **Trajectory Accuracy** , **Photometric Consistency** , and **Motion Smoothness** metrics, we employ **empirical min-max** normalization based on the distribution of scores across all evaluated models. We compute the 99<sup>th</sup> and 1<sup>st</sup> percentiles of each metric across all videos generated by the 8 models, which serve as the empirical maximum and minimum bounds, respectively.And the specific numerical values for these empirical bounds are provided in Table 6. The final normalized score is calculated as: 


where _S_ raw denotes the raw metric value, _S_ empirical<sup>maxand</sup><sup>_S_</sup> empirical<sup>minrepresent the empirical bounds.This transformation ensures</sup> that all scores reside within the interval [0 _,_ 1], with higher values indicating better performance. 

For **Depth Accuracy** , which originally measures reconstruction error (lower values are better), we apply the same normalization but invert the direction: 


This comprehensive normalization strategy ensures that all metrics are scaled to the unit interval [0 _,_ 1], aligned in direction (higher values always denote better performance), and comparable across different evaluation dimensions. 

18 

**Preprint** 

_Table 6._ Empirical bounds for metric normalization. The values represent the 99<sup>th</sup> percentile (maximum) and 1<sup>st</sup> percentile (minimum) of each metric across all evaluated videos. 

|**Metric**||**Empirical Maximum**|(_S_<sup>max</sup><br>empirical<sup>)</sup>|**Empirical Minimum**(_S_<sup>min</sup><br>empirical<sup>)</sup>|
|---|---|---|---|---|
|Photometric Consisten|cy**(Higher is Better)**|6.7899||0.1257|
|Motion Smoothness|**(Higher is Better)**|2.6413||0.0000|
|Trajectory Accuracy|**(Higher is Better)**|40.8540||0.0000|
|Flow Score|**(Higher is Better)**|8.9414||0.0531|
|Depth Accuracy|**(Lower is Better)**|4.3711||0.2228|


## **B. The Prompt of VLM-based Policy Success Judgement in Policy Evaluator Task** 

In the embodied policy evaluator task (Section 4.2.2), we assess whether world models can serve as proxy simulation environments for policy evaluation. To determine task success, we employ a VLM-based judge that compares the policygenerated video rollouts against ground-truth reference trajectories. The judge evaluates three critical aspects: (1) correct arm selection when specified in the instruction, (2) task completion by comparing final states between generated and ground-truth videos, and (3) overall action intent consistency. This evaluation approach accounts for visual artifacts inherent to world model rendering while focusing on functional correctness, enabling scalable and automated assessment of policy execution quality. The complete system prompt used for this VLM-based evaluation is provided below. 

### **Policy Execution Evaluation System Prompt** 

You are a robot task execution judge. Please determine if the policy model correctly executed the instruction. 

- **Task Instruction**: _{_ instruction _}_ 

- **INPUT DESCRIPTION:** 

- First 5 images: GT (Ground Truth) video frames (uniformly sampled: first frame, 3 middle frames, last frame), showing the correct task execution 

- Last 5 images: Policy model generated video frames, showing the policy model’s execution 

- **EVALUATION CRITERIA** (by priority): 

1. Arm Selection - If the instruction explicitly requires left/right arm, the correct arm must be used, otherwise fail 

2. Task Completion - Compare GT’s final state with Policy’s final state: 

- GT’s final frame shows the completed task state 

- Policy’s final frame should show a similar completion state 

- If Policy’s final frame differs significantly from GT’s final frame, judge as failure 

3. Action Intent - Is Policy’s entire motion process consistent with the instruction’s semantic meaning? 

- **TOLERABLE DIFFERENCES:** 

- Visual hallucinations from world model rendering (object deformation, color shifts) 

- Minor differences in action trajectory 

- Video length differences 

- **JUDGE AS SUCCESS (1):** 

- Correct arm used 

- Final state similar to GT (task basically completed) - Correct action intent 

- **JUDGE AS FAILURE (0):** 

- Wrong arm used 

- Final state significantly different from GT (task not completed or completed incorrectly) 

- Completely wrong action direction 

- Grabbed/operated wrong object 

Please carefully compare the **final frames** of GT and Policy to judge if the task is basically completed. 

**OUTPUT FORMAT REQUIREMENTS:** Please respond in this format: thinking: [Analysis: 1. Is arm correct? 2. Compare final frame task completion states 3. Is action intent consistent?] answer: [0 or 1] 

19 

**Preprint** 

## **C. Case Comparison of Each Metric in EWMScore** 


_Figure 6._ **Typical examples of Visual Quality.** _Top:Image Quality._ The bad example on the right-hand-side exhibits significant motion blur and noise, while the good example preserves sharp structural details. _Middle:Aesthetic Quality._ The bad example suffers from severe geometric distortion and artifacts. Conversely, the good example demonstrates superior contrast and realistic lighting with clear reflections. _Bottom:JEPA Similarity._ In the good example, the style and morphology closely align with the GT, while in the bad example, the robotic gripper shows color discrepancies and introduces unintended grid artifacts not present in the GT. 


_Figure 7._ **Typical examples of Motion Quality.** _Top:Dynamic Degree._ The good example shows the robotic arm exhibiting a complete and distinct motion sequence from picking up the bottle to placing it in the dustbin, while in the bad example, robotic arm remains static with only minor flickering of the bottle. _Middle:Flow Score._ The good example demonstrates a fluid manipulation of rotating the bottle with significant pixel-level movement and the bad example shows negligible motion, with only slight deformation at the top of the bottle. _Bottom:Motion Smoothness._ The good example features a stable and continuous translation of the hammer, but the bad example suffers from erratic shaking and disjointed,sharp movements immediately after grasping the object. 

20 

**Preprint** 


_Figure 8._ **Typical examples of Content Consistency.** _Top:Subjective Consistency._ In the good example, the bottle’s shape, color, and packaging remain stable and coherent throughout the grasping process. In the bad example, the bottle suffers from severe deformation and structural chaos, losing its original identity. _Middle:Background Consistency._ The good example maintains a stable background and camera perspective during the cabinet interaction. Conversely, the bad example on the right exhibits a sudden camera shift to a top-down view, leading to an unstable and rapidly changing background. _Bottom:Photometric Consistency._ In the good example, the appearance and color of both the block and the robotic arm are consistently preserved. In the bad example, the grasped block undergoes an unnatural color transition from green to red, indicating poor photometric stability. 


_Figure 9._ **Typical examples of Physics Adherence.** _Top:Interaction Quality._ In the good example, the robotic gripper interacts with the bread appropriately. In the bad example, the bread is lifted without any physical contact with the gripper, violating the fundamental physics laws. _Bottom:Trajectory Accuracy._ The good example demonstrates a movement trajectory that highly aligns with GT. Conversely, the bad example exhibits significant deviations from the GT trajectory, characterized by anomalous movements and jitter. 

21 

**Preprint** 


_Figure 10._ **Typical examples of 3D Accuracy.** _Top:Depth Accuracy._ In the good example, the generated depth map highly aligns with the GT, ensuring stable spatial and geometric structures, but the bad example suffers from severe geometric distortion, where the gripper unnaturally merges with the green block, leading to a collapse of spatial integrity. _Bottom:Perspectivity._ The good example maintains realistic perspective and lighting. Conversely, the bad example shows significant ghosting and blurring during movement, failing to preserve the object’s contour and exhibiting no shadow of robotic arm that deviate from physical reality. 


_Figure 11._ **Typical examples of Controllability.** _Top:Instruction Following._ In the good example, the model strictly adheres to the task instruction, but the bad example shows the movement of the incorrect object (knife), failing to execute instruction. _Middle:Semantic Alignment._ The good example demonstrates high semantic fidelity, but the bad example exhibits low alignment by transforming the QR code into a clothing tag and introducing irrational human hands not present in the target semantics. _Bottom:Action Following._ The good example successfully performs distinct actions based on varying prompts, placing the shoe at both the blue marker and to its left, but the bad example shows the model demonstrates limited discriminative ability, executing a singular action regardless of the instruction. 

22 

