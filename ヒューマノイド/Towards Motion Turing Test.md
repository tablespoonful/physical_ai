---
title: "Towards Motion Turing Test: Evaluating Human-Likeness in Humanoid Robots"
date: "2026-03-06"
authors: "Mingzhe Li; Mengyin Liu; Zekai Wu; Xincheng Lin; Junsheng Zhang; Ming Yan"
url: https://arxiv.org/abs/2603.06181
pdf: https://arxiv.org/pdf/2603.06181
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.06181)** / [論文ページ](https://arxiv.org/abs/2603.06181)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Towards Motion Turing Test: Evaluating Human-Likeness in Humanoid Robots** 

Mingzhe Li<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> , Mengyin Liu<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> , Zekai Wu<sup>1</sup><sup>_,_2</sup> , Xincheng Lin<sup>1</sup><sup>_,_2</sup> , Junsheng Zhang<sup>1</sup><sup>_,_2</sup> , Ming Yan<sup>1</sup><sup>_,_2</sup><sup>_,_3</sup> , Zengye Xie<sup>1</sup><sup>_,_2</sup> , Changwang Zhang<sup>4</sup> , Chenglu Wen<sup>1</sup><sup>_,_2</sup> , Lan Xu<sup>5</sup> , Siqi Shen<sup>1</sup><sup>_,_2</sup><sup>_†_</sup> , Cheng Wang<sup>1</sup><sup>_,_2</sup> 1Fujian Key Laboratory of Urban Intelligent Sensing and Computing, Xiamen University 2Key Laboratory of Multimedia Trusted Perception and Efficient Computing, Ministry of Education of China, School of Informatics, Xiamen University 3National Institute for Data Science in Health and Medicine, Xiamen University 4OPPO Research Institute, 5ShanghaiTech University 

## **Abstract** 

_Humanoid robots have achieved significant progress in motion generation and control, exhibiting movements that appear increasingly natural and human-like. Inspired by the Turing Test, we propose the_ **_Motion Turing Test_** _, a framework that evaluates whether human observers can discriminate between humanoid robot and human poses using only kinematic information. To facilitate this evaluation, we present the_ **_H_** _uman-_ **_H_** _umanoid_ **_Motion_** _(_ **_HHMotion_** _) dataset, which consists of 1,000 motion sequences spanning 15 action categories, performed by 11 humanoid models and 10 human subjects. All motion sequences are converted into SMPL-X representations to eliminate the influence of visual appearance. We recruited 30 annotators to rate the human-likeness of each pose on a 0–5 scale, resulting in over 500 hours of annotation. Analysis of the collected data reveals that humanoid motions still exhibit noticeable deviations from human movements, particularly in dynamic actions such as jumping, boxing, and running. Building on HHMotion, we formulate a_ **_human-likeness evaluation task_** _that aims to automatically predict humanlikeness scores from motion data. Despite recent progress in multimodal large language models, we find that they remain inadequate for assessing motion human-likeness. To address this, we propose a simple_ **_baseline_** _model and demonstrate that it outperforms several contemporary LLM-based methods. The dataset, code, and benchmark will be publicly released to support future research in the community._ 

## **1. Introduction** 

Research on humanoid robot motion has made remarkable progress in motion generation [5, 7, 23, 27, 28, 34, 41, 53, 76, 91] and motion control [16, 21, 25, 29, 44, 61], enabling increasingly natural, stable, and human-like movements. At recent robotics conferences and events [1–3], hu- 

> *Equal contribution. 

> †Corresponding author. 


Figure 1. **Motion Turing Test** : Evaluators judge whether the pose sequence resembles human motion, focusing solely on motion without appearance cues. 

manoid robots have been observed performing actions such as walking, running, dancing, and even gymnastics motions with impressive fluidity. 

Inspired by the concept of the _Turing Test_ [79] in artificial intelligence, we propose a **Motion Turing Test** for humanoid robots: _given a robot’s motion, if a human evaluator cannot distinguish whether it originates from a human or a robot, the robot’s motion is considered to have passed the Motion Turing Test_ . This test provides an intuitive and motion-centered approach to evaluating the human-likeness of robot motions, offering valuable insights for optimizing motion generation. Similar thinking about _Turing Test_ has been proposed previously [11, 55, 56, 59, 60]. For example, the Embodied Turing Test [95] evaluates whether an AI animal model is indistinguishable from its living counterpart. Different from them, we specifically focus on the motion of humanoid robots. 

Table 1. **Comparisons with related datasets.** The “-” symbol indicates that it is not included in the dataset. The “*” symbol denotes that this specific data type in the dataset is a combination of prior datasets and does not incorporate newly acquired data. 

|Dataset|Hum<br>MoCap|an<br>Video|Human<br>Simulation|oid<br>Real|#Humanoid<br>Models|Human&Humanoid|Human-likeness score|Duration|Motion|#Category|#Clips|
|---|---|---|---|---|---|---|---|---|---|---|---|
|AMASS [51]|�*|-|-|-|-|-|-|40+h|General|-|26.3k|
|Human3.6M [32]|�|�|-|-|-|-|-|-|Daily|15|-|
|LAFAN1 [26]|�|-|-|-|-|-|-|4.6h|Sports|-|-|
|Motion-X [47]|�|�|-|-|-|-|-|144.2h|General|-|81,084|
|IDEA400 (Motion-X) [47]|�|�|-|-|-|-|-|-|General|400|13k|
|SMART [15]|�|�|-|-|-|-|-|-|Sports|-|5000|
|DHRP [30]|-|-|�|�|11|-|-|-|Daily+Sports|-|462|
|HumanoidRobotPose [6]|-|-|-|�|10+|-|-|-|Football|-|23|
|PHUMA [39]|�*|�|�|-|2|�|-|72.96h|General|11|76.01k|
|LAFAN1 Retarget [65]|-|-|�|-|3|-|-|-|Sport|8|120|
|AMASS Retarget [99]|-|-|�|-|1|-|-|-|General|-|-|
|**HHMotion(Ours)**|�|�|�|�|**11**|�|�|**21.7h**|**Daily+Sports**|**15**|**1,000**|


To enable this evaluation, we collected more than 21 hours of humanoid robot video data from major international events such as the World Robot Conference (WRC) [3], World Artificial Intelligence Conference (WAIC) [1], World Humanoid Robot Games (WHRG) [2], and others [65], which represent the current state of the art in humanoid robotics. However, as current robot appearances are still far from fully human-like, directly showing raw robot videos to humans would allow them to easily identify whether the motion is human or robotic based on appearance cues. To ensure that our Motion Turing Test focuses purely on motion rather than appearance, we estimate the corresponding SMPL-X [58] models, a whole-body body model without texture information, from RGB videos of humanoid robots and humans. We ask human evaluators to rate the human-likeness of these pose sequences. This process is shown in Fig. 1. 

Our collected dataset includes videos of 11 robot models (e.g., Unitree G1 [64], ENGINEAI PM01 [63]), covering a diverse set of **15 motion categories** , including standing, walking, running, and other daily and sports activities. We recruited 10 human participants performing the same category actions to enable direct **H** uman– **H** umanoid **Motion** comparison. Notably, we also collected motion data from simulated robotic environments and invited humans to mimic specific robot movements. The proposed **HHMotion** contains **1,000** video clips of humans and humanoids. 

This work involved **30 human annotators** to score all pose sequences on a _Likert scale_ [46] of 0 to 5, where 0 denotes “completely robotic”, and 5 denotes “completely human-like”. On average, each participant spent approximately one minute per video, totaling over **500 hours** of annotation effort for the entire dataset. We find that, despite significant advancements in humanoid robot motion, contrary to common misconceptions, existing robot poses still exhibit noticeable differences from human poses that humans can relatively easily distinguish. In particular, motions such as boxing received noticeably lower scores, while actions like walking show a closer resemblance to human 

ones. Tab. 1 summaries the difference among HHMotion and other datasets. _As far as we know, this is the first dataset that rates the human-likeness of motions._ 

The HHMotion enables a novel task that evaluates the human-likeness of motions. Given a 3D pose (either from a human or a humanoid), predict its degree of human-likeness ranging from 0 to 5. To establish a robust and trainable groundwork for the Motion Turing Test, we propose a simple baseline, Pose-Temporal Regression Network ( **PTRNet** ), framing the evaluation of motion human-likeness as a quantitative regression task. PTR-Net notably surpasses several large vision-language model (VLM)-based methods [4, 8, 19], even with well-crafted prompting strategies. Our proposed baseline can also serve as a motion evaluation task for humanoid robot motion generation [5, 76] and as a reward model in reinforcement learning [16, 25] to enhance humanoid robot motion synthesis. 

Both the dataset and baseline implementations will be open-sourced to benefit the research community. 

## **2. Related Work** 

### **2.1. Human and Humanoid Robot Pose Estimation** 

Research on 3D Human Pose Estimation (HPE) commonly employs parametric body models such as Skinned MultiPerson Linear Model (SMPL) [49] and Skinned MultiPerson Linear Model-X (SMPL-X) [58] to reconstruct 3D human pose and shape from 2D visual inputs. RGBbased HPE methods [10, 15, 18, 20, 35, 36, 43, 57, 67, 68, 72–74, 82, 83, 87, 92, 100] have achieved remarkable progress. Recently, world-grounded RGB-based HPE approaches [37, 42, 70, 71, 75, 88–90, 93, 94] recover human motion in real-world coordinates, enabling temporally coherent, metrically aligned 3D reconstructions. 

Research on humanoid robot pose estimation has primarily focused on 2D pose estimation [6, 30, 80]. In recent years, 3D pose estimation for humanoid robots [17] has also emerged. However, they are limited to specific types of robots, which limits their applicability. 


Figure 2. **Action sources, types, and category distribution** in the HHMotion dataset, illustrating the diverse actions of both humans and humanoid robots. 

### **2.2. Human and Humanoid Motion Generation** 

Human motion generation aims to synthesize natural and diverse motion sequences for both virtual humans and humanoid robots [101]. Recent methods span autoregressive architectures [33, 50, 96], diffusion-based generative models [14, 45, 69, 78, 86], and adversarial frameworks [9, 52]. Multimodal extensions integrating text or audio guidance further enhance motion fidelity and expressiveness [97, 98]. 

In humanoid robotics, imitation learning approaches [5, 23, 41, 76] and reinforcement learning with physics-based control [16, 21, 25, 29, 44, 61] have enabled robots to perform human-like tasks. Motion retargeting techniques [7, 27, 28, 34, 53, 77, 91] further bridge human–robot embodiment gaps. However, despite rapid progress in motion generation, a unified and quantitative evaluation of motion human-likeness remains largely unexplored. 

### **2.3. Motion Datasets** 

Despite recent advances in human and humanoid motion generation, a standardized dataset for evaluating the human-likeness of motion remains absent. Existing motion datasets [32, 40, 47, 51] focus solely on humans rather than humanoid robots. With the rise of motion retargeting methods that transfer human movements to humanoid robots [7, 27, 91], many robots can now mimic human actions. The LAFAN1 Retargeting Dataset [65] aims to make humanoid robot motions more natural. It is based on the original LAFAN1 [26] motion capture dataset, where human motion data is retargeted to a humanoid robot [64]. However, these approaches often exhibit a noticeable gap between simulation and real-world performance. 

## **3. Human-humanoid Motion Dataset** 

### **3.1. Dataset Overview** 

In this work, we propose the Human-Humanoid Motion (HHMotion) Dataset. Overall, HHMotion contains a bal- 

anced and diverse set of humanoid robot and human motion sequences, totaling **21.7h** of raw video data across both realworld and simulated environments. It consists of motions from **5 different sources** : real robot motions from significant events, robot motions from simulation, human motions from volunteers, human motions from volunteers mimicking robots, and human motions from YouTube. The dataset covers a wide range of **15 action categories** and **11 humanoid robot** models. The action category distribution is depicted in Fig. 2. 

HHMotion consists of **10 subjects** performing actions in the same category as robots. Moreover, to increase the dataset’s diversity, we collected multiple human motion videos from YouTube (see detailed dataset sources and humanoid models in Supplementary File). 

Each video is standardized into a 5-second clip, resulting in **1,000 motion clips** . Each motion clip is scored by human annotators on a Likert scale of 0 to 5. 0 represents “complete robotic,” whereas 5 represents “complete human-like” (which is described in Sec. 3.4). 

### **3.2. Dataset Construction** 

#### **3.2.1. Humanoid robot data** 

To uncover how to establish the world’s most advanced motion benchmark for humanoid robots, we collected 21.7 hours of original videos from the WRC [3], WAIC [1], and WHRG [2]. Data from the WRC and WAIC were sourced from platforms like YouTube, while 2025 WHRG data originated from official competition broadcasts. This authentic humanoid robot dataset represents the world’s most advanced level of humanoid robotics development. Among these conferences, we collected data from 11 robot models, encompassing algorithms from 28 different teams. 

Many robot motion generation methods adopt sim-toreal approaches, which rely on simulated robot motions. To comprehensively evaluate the human-like scale of humanoid robot motions, we also collected robot motion sequences in simulated environments. We visualized and recorded the LAFAN1 Retargeting Dataset [65] in a simulation environment, collecting raw robotic motion sequences across 7 action categories: dance, fall and get up, fight, jump, kicking ball, run, and walk. 

To enable more precise evaluation for each action category, each video action in the dataset was segmented into 5-second action clips, each containing a simple but complete action. In total, we obtained **500 humanoid motion clips** , comprising 257 clips from real humanoid robots and 243 clips from robots in the simulation environment. After a rigorous data sanitation and standardization process, we retained about 5,000 seconds of high-quality motion clips (including human and humanoid). Low-resolution, occluded, or truncated videos were removed. 


Figure 3. **Overview of the human scoring pipeline** , where all the humanoid robot and human motions are converted into SMPL-X poses and evaluated by human annotators. The resulting 0–5 scores quantitatively assess the human-likeness of each motion. 

#### **3.2.2. Human motion data** 

To enable comparative evaluation between robotic and human motions, we collected corresponding human actions based on the categories gathered from humanoid robots. For each category, 10 subjects performed 25–30 specific motions. This dataset comprehensively covers all robotic motion categories collected, spanning both indoor and outdoor scenarios. To align with robotic motions, the collected data was consistently edited into 5-second clips. In addition, in order to increase the diversity of the human sample, videos of various people performing the corresponding action categories were collected from YouTube. In total, we collected **500 human motion clips** across 15 categories, comprising 365 clips from 10 subjects and 135 clips from the internet. 

Notably, to reinforce the Motion Turing Test principle of our benchmark, we also included a subset where human subjects **intentionally imitated** the movement patterns of humanoid robots (refer to the Supplementary File for the detailed evaluation). The goal was to create ambiguous motion samples that blur the distinction between human and robotic behaviors, thereby making the evaluation more challenging and faithful to the essence of Motion Turing Test. 

### **3.3. Human-humanoid Pose Estimation** 

As humanoid robots still exhibit distinctive appearances such as metallic shells and exposed joints, evaluators may rely on visual cues rather than motion to distinguish them from humans. To ensure that our Motion Turing Test focuses purely on motion rather than appearance, we adopt a pose-level strategy that converts all videos into the SMPLX [58] model, ensuring that only motion information is focused for evaluation. 

To obtain the SMPL-X model used for human-likeness evaluation, we systematically compared multiple SOTA human pose estimation (HPE) [70, 71, 89, 90] and robot pose estimation (RPE) [6, 17, 30] methods. We found that existing robot-specific pose estimators often overfit to particular robot morphologies or kinematic constraints, leading to degraded generalization when applied to diverse humanoid models. In contrast, general HPE methods demonstrated stronger robustness and better alignment across human and humanoid subjects. Among these HPE methods, 


Figure 4. **Human-likeness scoring rules** used in evaluating motion clips on a 0–5 Likert scale, focusing solely on motion quality. 

GVHMR [70] achieved the most stable and temporally coherent results in our experiments (refer to Supplementary File). Although it was initially designed for human motion, we observed that it generalized well to humanoid robots, providing accurate and temporally smooth reconstructions. 

### **3.4. Human-likeness Scoring** 

Current humanoid motion researches predominantly assess task-oriented metrics, such as completion rate, efficiency, robustness, or end-effector trajectory accuracy [5, 22, 31, 48, 54, 66, 84, 91]. However, high task performance does not necessarily imply perceptually human-like motion. In human–robot interaction, subjective impressions of naturalness, fluidity, and anthropomorphism are equally critical [13, 24, 38], yet these aspects are often overlooked in existing evaluation systems. 

The human scoring pipeline is shown in Fig. 3. To quantitatively assess the human-likeness of humanoid robot motions, we collected large-scale human annotations for each motion clip in the HHMotion. Specifically, we recruited **30 human evaluators** to assign human-likeness scores to all SMPL-X motion sequences on a 0–5 _Likert scale_ [46], where 0 indicates “completely inhuman-like motion” and 5 indicates “indistinguishable from human motion” as shown 


Figure 5. Overall distribution of motion human-likeness scores for **human and humanoid** motions ( **left** ) and human-likeness scores for **humanoid in simulation and real** scenarios ( **right** ). 

in Fig. 4. Each participant was asked to carefully watch a set of motion sequences and evaluate how closely each motion resembled natural human movement in terms of posture, rhythm, and coordination. We have obtained IRB approval to conduct this study. All the volunteers and the annotators agree that their data can be used for research purposes. 

For evaluation, we selected 500 human and 500 humanoid robot motion sequences, randomly mixed and shuffled to hide their sources, and presented them to each evaluator to prevent any prior bias toward a specific class or motion type. Each annotator evaluated 1000 sequences and spent approximately an average of 16.7 hours completing the task, leading to a total of over 500 annotation hours across all participants. Finally, we aggregated all annotators’ scores to obtain the average human-likeness score for each action sequence, forming the “human evaluators annotation” within the HHMotion dataset. 

### **3.5. Dataset Quality** 

**Motion sequence Quality.** To ensure reliability of the obtained SMPL-X motion sequences for human and robot, all reconstructed motion sequences underwent manual crossvalidation to remove failed or noisy samples (e.g., from occlusion or reflective surfaces). Furthermore, a subset of videos was manually annotated with bounding boxes for correction, where we also report detailed comparisons of tested HPE methods (refer to Supplementary File for details). Through this pipeline, we obtain high-quality, temporally smooth SMPL-X motion sequences for both human and humanoid subjects, establishing a robust foundation for our Motion Turing Test benchmark. 

**Annotation quality.** An **I** nter- **A** nnotator **C** onsistency (IAC) check was calculated to confirm high agreement levels among human evaluators. As a result, five annotators were identified as inconsistent with the overall distribution and were excluded from the final dataset. The remaining 25 evaluators demonstrated high IAC and provided stable, accurate assessments. This rigorous filtering process ensures the credibility and robustness of the human-likeness score annotations (see IAC process and result in Supplementary). 

Table 2. **Top 5 and bottom 5 action categories** ranked by score difference between human and real humanoid motions. The scores here are calculated based on the average score of the last 25 annotators after the IAC check. 

|**Action Category**|**Human**|**Humanoid**|**Score Difference**|
|---|---|---|---|
|_Smallest Differences_||||
|<br>stand|3.80|1.97|1.83|
|sit|4.18|2.63|1.55|
|ski|3.13|1.76|1.37|
|walk|3.92|2.61|1.31|
|dance|3.47|2.26|1.21|
|_Largest Differences_||||
|jump|4.43|1.20|3.23|
|boxing|3.76|1.23|2.53|
|run|3.73|1.47|2.26|
|pingpong|4.33|2.09|2.24|
|kicking ball|3.93|1.79|2.14|


### **3.6. Analysis of Human-likness Scores** 

To quantitatively understand how human evaluators assess the similarity between humanoid robot and human motions, we conducted a detailed analysis of the human evaluators’ annotations across 15 action categories. Fig. 5 (left) illustrates the overall score distribution for human and humanoid motions, revealing that human actions consistently receive higher rating counts. Fig. 5 (right) illustrates the score distribution for humanoids in simulation and real scenarios, showing that humanoid actions in simulation environments perform better than real humanoid robots. This indicates that, despite recent advances in humanoid control, a noticeable gap in human-likeness remains between human and robotic motion quality. Tab. 2 presents the top and bottom five categories ranked by the score differences between human and humanoid motions. In this comparison, our analysis focuses exclusively on real humanoid robots to ensure fairness and reliability. 

Overall, our human-likeness score analysis demonstrates that, contrary to common misconceptions, there remains a significant gap between human and robotic movements, even with the remarkable advancements in humanoid robot motion control. Evaluators could easily distinguish humanoid motions from natural human movements, even under the appearance-disentangled evaluation setting. Notably, actions involving high-frequency coordination and rapid limb transitions, such as _jump_ , _boxing_ , and _pingpong_ (see upper part of Fig. 6), showed the largest score discrepancies, suggesting that humanoid robots continue to struggle with dynamic, contact-rich, and reactive movements. 

In contrast, relatively smooth or cyclic motion types such as _walk_ , _stand_ (see lower part of Fig. 6), achieved closer human–humanoid score alignment. These findings indicate that current humanoid robots can reproduce structured or rhythmically repetitive movements with reasonable fidelity but still lack the fine-grained fluidity, adaptiveness, and balance control characteristic of human motor behavior. 

Comprehensive score analysis for all **simulated** cate- 


Figure 6. Representative SMPL-X sequences illustrate where humanoid robots perform poorly (upper part) and well (lower part). 


Figure 7. **Our proposed PTR-Net baseline** consists of a temporal encoder, spatial-temporal graph convolution, and attention pooling, then uses a score regressor to **predict the human-likeness score.** 

malized into a local root coordinate frame to remove global translation and rotation effects. 

### **4.2. PTR-Net: A Simple Baseline** 

gories is provided in the Supplementary File for completeness. The analysis shows that the humanoid’s performance in the simulated environment is superior to its performance in the real world. 

## **4. Robot Motion Turing Test Benchmark** 

To quantitatively assess the human-likeness of humanoid robot motions, we construct a unified **Robot Motion Turing Test Benchmark** based on the HHMotion. This benchmark examines whether different models can approximate human judgments of motion human-likeness. We first describe the Motion human-likeness task (Sec. 4.1), then introduce our supervised PTR-Net for human-likeness prediction from pose sequences (Sec. 4.2) and describe the evaluation metrics for model–human alignment in Sec. 4.3. 

### **4.1. Motion Human-likeness Assessment task** 

The Robot Motion Turing Test is inspired by the classical _Turing Test_ [79] but focuses exclusively on motion and pose realism, rather than visual appearance. Specifically, a humanoid robot is considered to “pass” the Motion Turing Test if human evaluators cannot reliably distinguish whether a given pose sequence was performed by a human or a humanoid, based solely on its body motion information (without facial, textual, and color information). To implement such a Turing test, we propose a novel task for assessing motion human-likeness. We formulate the assessment of human-likeness as a quantitative regression task. 

In this task, a model is required to predict continuous human-likeness scores directly from motion sequences, aligned with human annotators’ judgments. It takes a motion sequence as input and outputs a human-likeness score ranging from 0 to 5, where 0 represents a complete difference from a human and 5 indicates indistinguishability from a human. Each motion sequence is represented as a temporal series of the SMPL-X model. The sequence is nor- 

We propose Pose-Temporal Regression Network (PTR-Net) for the motion human-likeness assessment tasks. It consists of three main components, and the pipeline of PTR-Net is shown in Fig. 7. 

**Temporal Encoder.** A two-layer bidirectional LSTM captures long-range temporal dependencies and outputs temporally encoded features **H** _t ∈_ R<sup>2</sup><sup>_h_</sup> . 

**Spatial–Temporal Graph Convolution (ST-GCN).** The encoded sequence is reshaped into a graph representation of the human body and processed through a stack of ST-GCN blocks. Each block alternates spatial graph convolution and temporal convolution to extract coordination patterns across joints and frames. Unlike conventional skeleton-based GCNs, PTR-Net adopts a parameter-free adjacency design, allowing more adaptive feature aggregation. 

**Attention Pooling and Regression Head.** A temporal attention module highlights salient motion segments, followed by a lightweight MLP regressor that outputs a scalar human-likeness score. Formally, PTR-Net learns an end-toend mapping: 


where _fθ_ denotes the network parameters and _s ∈_ [0 _,_ 5] is the predicted score (see more PTR-Net details in Supplementary File). 

**Training Objective.** PTR-Net is optimized with an L2 regression loss and a regularization term: 


where _s_<sup>_∗_</sup> denotes the human-likeness score, _s_ ˆ denotes the predicted score and _L_ reg penalizes excessive temporal fluctuations in the predicted scores to encourage smoothness and stability. 

### **4.3. Evaluation Metrics** 

To quantitatively assess how well model predictions align with human judgement, we employ three complementary 

metrics: Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and Spearman’s Rank Correlation ( _ρ_ ). Detailed formulations of these metrics and uses are provided in the Supplementary File. 

## **5. Experiments** 

In this section, we evaluate the performance of the proposed baseline and others on the motion human-likeness task. 

### **5.1. Experimental Setup** 

We evaluate both our proposed pose-based baseline model and the Gemini-2.5 Pro [19] and Qwen3-vl-plus [8] on the Motion Turing Test benchmark; it serves as a representative SOTA VLMs capable of processing video sequences. Each SMPL-X based motion clip is fed into the model for evaluation. The baseline PTR-Net is trained on the HHMotion dataset (see training details in Supplementary File). 

### **5.2. VLM Human-likeness Assessment Baselines** 

Beyond our trainable baseline, we further investigate whether VLMs can serve as evaluators for motion humanlikeness. We employ Gemini 2.5 Pro [19] and Qwen3-vlplus [8] as VLM evaluators. The model receives rendered SMPL-X motion videos as input and rates them on a 0–5 human-likeness scale. To explore the model’s reasoning capability, we design four different prompting strategies: Direct Evaluation **(DE)** , Context-Guided Evaluation **(CGE)** , Prototype-Driven Evaluation **(PDE)** [12], Direct Evaluation Chain-of-Thought ( **DE** -CoT), and **Posture-Aware** Chainof-Thought ( **PA** -CoT). 

In the DE method, the VLM directly evaluates the target motion solely based on the instruction, without any demonstration. The CGE setup introduces a single example with a reference score and a description to guide the VLM’s understanding of evaluation style. The PDE setup provides six labeled examples covering all score levels (0–5) to calibrate the human-likeness score, each paired with a humanwritten description. The DE-CoT method introduces a CoT approach [85], enabling the model to reason step-by-step to reason the result. The PA-CoT method we proposed adopts a structured reasoning process that mirrors human evaluators’ thought patterns. The model is first instructed to identify the motion type (upper limb, lower limb, or full-body) and then to analyze the motion along three interpretable dimensions: **posture fluency** , **movement coordination** , and **core stability** . Based on these analyses, the model synthesizes a final score and generates a qualitative description. 

### **5.3. Quantitative Results** 

The quantitative comparison is shown in Tab. 3. Despite the impressive reasoning capabilities of recent LLMs, assessing human-likeness in motion remains highly challenging. Even with structured strategies such as PA-CoT, Gem- 

Table 3. **Quantitative results for different models** on the Motion Turing Test benchmark. “*” indicates VLM-based evaluation without task-specific training. Qwen3-VL-Plus (shot)* denotes that its results remain identical in DE/CGE/PED/DE-CoT/PA-CoT settings. “–” indicates invalid _ρ_ due to constant outputs. 

|**Model**|**MAE**_↓_|**RMSE**_↓_|**Spearman’s**_ρ ↑_|
|---|---|---|---|
|Gemini 2.5 Pro (DE)*|1.3105|1.5873|0.1609|
|Gemini 2.5 Pro (CGE)*|1.3314|1.5986|0.1658|
|Gemini 2.5 Pro (PDE)*|1.2616|1.5397|0.2188|
|Gemini 2.5 Pro (DE-CoT)*|1.6040|1.9146|0.1353|
|Gemini 2.5 Pro (PA-CoT)*|1.2682|1.5214|0.2303|
|Qwen3-VL-Plus (shot)*|1.7714|2.1018|–|
|MotionBERT (Frozen Backbone)|0.6846|0.9025|0.5315|
|MotionBERT (Fine-tuned)|0.6252|0.8465|0.6142|
|Transformer (Lightweight)|0.6387|0.8259|0.5728|
|**PTR-Net (Ours)**|**0.5813**|**0.7926**|**0.6841**|


Figure 8. Four representative motion examples with **PTR-Net predictions compared to human-annotated scores.** 

ini 2.5 Pro exhibits large deviations from human judgments. Qwen3-VL-Plus shows even lower sensitivity to motion details, yielding nearly identical predictions across different setups and a higher error. To provide stronger motioncentric baselines, we further compare PTR-Net with MotionBERT [100] under both frozen and fine-tuned settings, as well as a Transformer-based [81] lightweight baseline. 

Overall, PTR-Net consistently outperforms all baselines across metrics, achieving lower MAE and RMSE and higher _ρ_ . However, the 0.80 RMSE indicates that there is still room for improvement in this task. 

### **5.4. Qualitative Evaluation** 

To further illustrate the interpretability and reliability of PTR-Net’s evaluation behavior, we visualize four representative examples across both human and humanoid motion types in Fig. 8, PTR-Net’s predictions exhibit strong alignment with human-likeness scores across diverse categories. 

Table 4. **Ablation study of PTR-Net components** on the Motion Turing Test benchmark. 

|**Model Variant**|**MAE**_↓_|**RMSE**_↓_|**Spearman’s**_ρ ↑_|
|---|---|---|---|
|w/o Temporal Encoder|0.7631|0.9691|0.3610|
|w/o Attention Pooling|0.6185|0.8203|0.6255|
|w/o_Lreg_|0.5983|0.7958|0.6215|
|**PTR-Net(Full Model)**|**0.5813**|**0.7926**|**0.6841**|


For human actions, PTR-Net’s predictions closely align with human evaluations. In kicking ball (label 3.8 / pred 3.71) and playing ping pong (label 4.8 / pred 4.27), the model correctly captures smooth coordination and natural limb transitions. For humanoid actions, it accurately identifies mechanical rigidity. PTR-Net reflects human judgments by assigning lower scores due to visible stiffness and rhythmic discontinuities. Overall, these examples show that the proposed PTR-Net not only matches human ratings numerically but also captures interpretable motion cues such as fluency, coordination, and balance. 


Figure 9. (a–b) Score distributions of **human annotators and PTR-Net predictions** for both **human (imitating humanoid) and humanoid motions** . (Bottom) Representative dance imitation pairs illustrating near-indistinguishable motion patterns. 

### **5.5. Ablation Study** 

To better understand the contribution of each component in PTR-Net, we conduct an ablation study by selectively removing or modifying key modules. As shown in Tab. 4, removing the temporal encoder results in an increase in MAE and RMSE errors. Disabling attention pooling also reduces correlation with human ratings, indicating its role in capturing global temporal context. The regularization term _Lreg_ further stabilizes training and improves score consistency. The full model achieves the optimal overall balance between error reduction and ranking consistency, verifying the rationality of the collaborative design of each component. 

### **5.6. Discussion on Humans Imitating Humanoids** 

We analyze the _human-imitating-humanoid_ subset to examine evaluation boundaries of motion human-likeness. As shown in Fig. 9(a–b), PTR-Net closely follows human annotators’ distributions, suggesting its ability to capture subtle temporal and coordination cues. Human ratings show partial overlap between imitating humans and humanoids, indicating that intentional imitation can blur the evaluation boundary of human-likeness. 

The bottom dance imitation pairs further support this observation, that both human and humanoid motions receive nearly identical scores. These findings highlight a **nontrivial** ambiguity in human-likeness evaluation: when humans intentionally mimic humanoids’ mechanical rigidity, the kinematic cues become insufficient for reliable discrimination. This suggests that true human-likeness involves not only smoothness and coordination but also the intentionality and adaptability underlying human motion dimensions, which remain challenging for both the generation and model assessment of humanoids. 


Figure 10. **Out-of-distribution evaluation** on the **XPeng IRON [62]** humanoid robot. 

### **5.7. Out-of-Distribution Evaluation** 

To examine the generalization ability of our benchmark beyond the distribution of the collected data, we further tested it on motions from unseen humanoid robots, including the recently released (Nov. 2025) XPeng IRON [62] as shown in Fig. 10. PTR-Net predicts an outstanding performance of the XPeng IRON human-likeness score of 4.25, closely matching the human annotation average of 4.36. This strong alignment not only demonstrates the robustness of PTR-Net in handling unseen humanoid models but also validates the consistency and reliability of motion human-likeness scoring. More OOD examples will be added as they become open-sourced (see more examples in Supplementary File). 

## **6. Conclusion** 

In this work, we introduce the Motion Turing Test and HHMotion dataset, a comprehensive benchmark of humanoid and human motions annotated by 30 annotators. Despite advances, robots still lag in complex actions. Our PTR-Net baseline effectively predicts motion human-likeness, outperforming existing VLM models and serving as a tool for evaluation and reinforcement learning. Together, they provide a rigorous, human-centered foundation for developing more natural and expressive humanoid motions. 

**Acknowledgment.** This work was partially supported by the Fundamental Research Funds for the Central Universities (No. 20720230033), by Xiaomi Young Talents Program. We would like to thank the anonymous reviewers for their valuable suggestions. 

## **References** 

- [1] The 2025 World AI Conference. https://www. worldaic.com.cn/, 2025. 1, 2, 3 

- [2] The 2025 World Humanoid Robot Games. https:// www.whrgoc.com/, 2025. 2, 3 

- [3] The 2025 World Robot Conference. https://www. worldrobotconference.com/, 2025. 1, 2, 3 

- [4] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 2 

- [5] Arthur Allshire, Hongsuk Choi, Junyi Zhang, David McAllister, Anthony Zhang, Chung Min Kim, Trevor Darrell, Pieter Abbeel, Jitendra Malik, and Angjoo Kanazawa. Visual imitation enables contextual humanoid control. _arXiv preprint arXiv:2505.03729_ , 2025. 1, 2, 3, 4 

- [6] Arash Amini, Hafez Farazi, and Sven Behnke. Real-time pose estimation from images for multiple humanoid robots. In _Robot World Cup_ , pages 91–102. Springer, 2021. 2, 4 

- [7] Sujin Baek, Ahyeon Kim, Jin-Young Choi, Eunju Ha, and Jong-Wook Kim. Human motion retargeting to a full-scale humanoid robot using a monocular camera and human pose estimation. _International Journal of Control, Automation and Systems_ , 22(9):2860–2870, 2024. 1, 3 

- [8] Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang, et al. Qwen technical report. _arXiv preprint arXiv:2309.16609_ , 2023. 2, 7 

- [9] Emad Barsoum, John Kender, and Zicheng Liu. Hp-gan: Probabilistic 3d human motion prediction via gan. In _Proceedings of the IEEE conference on computer vision and pattern recognition workshops_ , pages 1418–1427, 2018. 3 

- [10] Federica Bogo, Angjoo Kanazawa, Christoph Lassner, Peter V. Gehler, Javier Romero, and Michael J. Black. Keep it smpl: Automatic estimation of 3d human pose and shape from a single image. In _ECCV_ , 2016. 2 

- [11] Rodney A Brooks. Intelligence without representation. _Artificial intelligence_ , 47(1-3):139–159, 1991. 1 

- [12] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. _Advances in neural information processing systems_ , 33:1877–1901, 2020. 7 

- [13] Pedro C´ardenas, Jos´e Garc´ıa, Rolinson Begazo, Ana Aguilera, Irvin Dongo, and Yudith Cardinale. Evaluation of robot emotion expressions for human–robot interaction. _International Journal of Social Robotics_ , 16(9):2019–2041, 2024. 4 

- [14] Angela Castillo, Maria Escobar, Guillaume Jeanneret, Albert Pumarola, Pablo Arbel´aez, Ali Thabet, and Artsiom Sanakoyeu. Bodiffusion: Diffusing sparse observations for full-body human motion synthesis. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 4221–4231, 2023. 3 

- [15] Xin Chen, Anqi Pang, Wei Yang, Yuexin Ma, Lan Xu, and Jingyi Yu. Sportscap: Monocular 3d human motion capture and fine-grained understanding in challenging sports videos. _International Journal of Computer Vision_ , 129: 2846–2864, 2021. 2 

- [16] Zixuan Chen, Xialin He, Yen-Jen Wang, Qiayuan Liao, Yanjie Ze, Zhongyu Li, S Shankar Sastry, Jiajun Wu, Koushil Sreenath, Saurabh Gupta, et al. Learning smooth humanoid locomotion through lipschitz-constrained policies. _arXiv preprint arXiv:2410.11825_ , 2024. 1, 2, 3 

- [17] Youngdae Cho, Wooram Son, Jaewan Bak, Yisoo Lee, Hwasup Lim, and Youngwoon Cha. Full-body pose estimation of humanoid robots using head-worn cameras for digital human-augmented robotic telepresence. _Mathematics_ , 12(19):3039, 2024. 2, 4 

- [18] Hai Ci, Mingdong Wu, Wentao Zhu, Xiaoxuan Ma, Hao Dong, Fangwei Zhong, and Yizhou Wang. Gfpose: Learning 3d human pose prior with gradient fields. In _CVPR_ , pages 4800–4810, 2023. 2 

- [19] Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit Dhillon, Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities. _arXiv preprint arXiv:2507.06261_ , 2025. 2, 7 

- [20] Zhiyang Dou, Qingxuan Wu, Cheng Lin, Zeyu Cao, Qiangqiang Wu, Weilin Wan, Taku Komura, and Wenping Wang. TORE: token reduction for efficient human mesh recovery with transformer. In _ICCV_ , 2023. 2 

- [21] Yahao Fan, Tianxiang Gui, Kaiyang Ji, Shutong Ding, Chixuan Zhang, Jiayuan Gu, Jingyi Yu, Jingya Wang, and Ye Shi. One policy but many worlds: A scalable unified policy for versatile humanoid locomotion. _arXiv preprint arXiv:2505.18780_ , 2025. 1, 3 

- [22] Mahmoud Farhat, Yassine Kali, Maarouf Saad, Mohammad H Rahman, and Roberto E Lopez-Herrejon. Walking position commanded nao robot using nonlinear disturbance observer-based fixed-time terminal sliding mode. _ISA transactions_ , 146:592–602, 2024. 4 

- [23] Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. Humanplus: Humanoid shadowing and imitation from humans. In _Conference on Robot Learning (CoRL)_ , 2024. 1, 3 

- [24] Carl Gaebert, Oliver Rehren, Sebastian Jansen, Katharina Jahn, Peter Ohler, G¨unter Daniel Rey, and Ulrike Thomas. Effects of human-like characteristics in sampling-based motion planning on the legibility of robot arm motions. _ACM Transactions on Human-Robot Interaction_ , 14(3):1– 25, 2025. 4 

- [25] Xinyang Gu, Yen-Jen Wang, and Jianyu Chen. Humanoidgym: Reinforcement learning for humanoid robot 

with zero-shot sim2real transfer. _arXiv preprint arXiv:2404.05695_ , 2024. 1, 2, 3 

- [26] F´elix G. Harvey, Mike Yurick, Derek Nowrouzezahrai, and Christopher Pal. Robust motion in-betweening. 39(4), 2020. 2, 3 

- [27] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 1, 3 

- [28] Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning humanto-humanoid real-time whole-body teleoperation. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 8944–8951. IEEE, 2024. 1, 3 

- [29] Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Jan Kautz, Changliu Liu, Guanya Shi, Xiaolong Wang, et al. Hover: Versatile neural wholebody controller for humanoid robots. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9989–9996. IEEE, 2025. 1, 3 

- [30] Seokhyeon Heo, Youngdae Cho, Jeongwoo Park, Seokhyun Cho, Ziya Tsoy, Hwasup Lim, and Youngwoon Cha. Diverse humanoid robot pose estimation from images using only sparse datasets. _Applied Sciences_ , 14(19):9042, 2024. 2, 4 

- [31] Zhifeng Huang, Zijun Wang, Jinglun Zhou, Kairong Wu, Shunjie Zhu, Lei Nie, Yuwei Liang, Liang Yang, and Yun Zhang. Quasi-static balancing for biped robot to perform extreme postures using ducted-fan propulsion system. _Robotics and Autonomous Systems_ , 165:104429, 2023. 4 

- [32] Catalin Ionescu, Dragos Papava, Vlad Olaru, and Cristian Sminchisescu. Human3.6M: Large Scale Datasets and Predictive Methods for 3D Human Sensing in Natural Environments. _Transactions on Pattern Analysis and Machine Intelligence (TPAMI)_ , 36(7):1325–1339, 2014. 2, 3 

- [33] Biao Jiang, Xin Chen, Wen Liu, Jingyi Yu, Gang Yu, and Tao Chen. Motiongpt: Human motion as a foreign language. _Advances in Neural Information Processing Systems_ , 36:20067–20079, 2023. 3 

- [34] Zhenyu Jiang, Yuqi Xie, Jinhan Li, Ye Yuan, Yifeng Zhu, and Yuke Zhu. Harmon: Whole-body motion generation of humanoid robots from language descriptions. In _Conference on Robot Learning (CoRL)_ , 2024. 1, 3 

- [35] Muhammed Kocabas, Nikos Athanasiou, and Michael J. Black. Vibe: Video inference for human body pose and shape estimation. _2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 5252– 5262, 2020. 2 

- [36] Muhammed Kocabas, Chun-Hao P. Huang, Otmar Hilliges, and Michael J. Black. Pare: Part attention regressor for 3d human body estimation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 11127–11137, 2021. 2 

- [37] Muhammed Kocabas, Ye Yuan, Pavlo Molchanov, Yunrong Guo, Michael J Black, Otmar Hilliges, Jan Kautz, and Umar Iqbal. Pace: Human and camera motion estimation 

   - from in-the-wild videos. In _2024 International Conference on 3D Vision (3DV)_ , pages 397–408. IEEE, 2024. 2 

- [38] Laura Kunold, Nikolai Bock, and Astrid Rosenthal-von der P¨utten. Not all robots are evaluated equally: the impact of morphological features on robots’ assessment through capability attributions. _ACM Transactions on Human-Robot Interaction_ , 12(1):1–31, 2023. 4 

- [39] Kyungmin Lee, Sibeen Kim, Minho Park, Hyunseung Kim, Dongyoon Hwang, Hojoon Lee, and Jaegul Choo. Phuma: Physically-grounded humanoid locomotion dataset. _arXiv preprint arXiv:2510.26236_ , 2025. 2 

- [40] Jialian Li, Jingyi Zhang, Zhiyong Wang, Siqi Shen, Chenglu Wen, Yuexin Ma, Lan Xu, Jingyi Yu, and Cheng Wang. Lidarcap: Long-range marker-less 3d human motion capture with lidar point clouds. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 20502–20512, 2022. 3 

- [41] Jinhan Li, Yifeng Zhu, Yuqi Xie, Zhenyu Jiang, Mingyo Seo, Georgios Pavlakos, and Yuke Zhu. Okami: Teaching humanoid robots manipulation skills through single video imitation. In _8th Annual Conference on Robot Learning (CoRL)_ , 2024. 1, 3 

- [42] Jiefeng Li, Ye Yuan, Davis Rempe, Haotian Zhang, Pavlo Molchanov, Cewu Lu, Jan Kautz, and Umar Iqbal. Coin: Control-inpainting diffusion prior for human and camera motion estimation. In _European Conference on Computer Vision_ , pages 426–446. Springer, 2025. 2 

- [43] Zhihao Li, Jianzhuang Liu, Zhensong Zhang, Songcen Xu, and Youliang Yan. Cliff: Carrying location information in full frames into human pose and shape estimation. In _ECCV_ , 2022. 2 

- [44] Zhongyu Li, Xue Bin Peng, Pieter Abbeel, Sergey Levine, Glen Berseth, and Koushil Sreenath. Robust and versatile bipedal jumping control through reinforcement learning. In _Robotics: Science and Systems XIX, Daegu, Republic of Korea, July 10-14, 2023_ , 2023. 1, 3 

- [45] Han Liang, Wenqian Zhang, Wenxuan Li, Jingyi Yu, and Lan Xu. Intergen: Diffusion-based multi-human motion generation under complex interactions. _International Journal of Computer Vision_ , 132(9):3463–3483, 2024. 3 

- [46] Rensis Likert. A technique for the measurement of attitudes. _Archives of psychology_ , 1932. 2, 4 

- [47] Jing Lin, Ailing Zeng, Shunlin Lu, Yuanhao Cai, Ruimao Zhang, Haoqian Wang, and Lei Zhang. Motion-x: A largescale 3d expressive whole-body human motion dataset. _Advances in Neural Information Processing Systems_ , 36: 25268–25280, 2023. 2, 3 

- [48] Fukang Liu, Zhaoyuan Gu, Yilin Cai, Ziyi Zhou, Hyunyoung Jung, Jaehwi Jang, Shijie Zhao, Sehoon Ha, Yue Chen, Danfei Xu, et al. Opt2skill: Imitating dynamicallyfeasible whole-body trajectories for versatile humanoid loco-manipulation. _IEEE Robotics and Automation Letters_ , 2025. 4 

- [49] Matthew Loper, Naureen Mahmood, Javier Romero, Gerard Pons-Moll, and Michael J. Black. Smpl: A skinned multi-person linear model. _ACM Trans. Graph._ , 34(6): 248:1–248:16, 2015. 2 

- [50] Thomas Lucas, Fabien Baradel, Philippe Weinzaepfel, and Gr´egory Rogez. Posegpt: Quantization-based 3d human motion generation and forecasting. In _European Conference on Computer Vision_ , pages 417–435. Springer, 2022. 3 

- [51] Naureen Mahmood, Nima Ghorbani, Nikolaus F. Troje, Gerard Pons-Moll, and Michael J. Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2019. 2, 3 

- [52] Matthew Malek-Podjaski and Fani Deligianni. Adversarial attention for human motion synthesis. In _2023 IEEE Symposium Series on Computational Intelligence (SSCI)_ , pages 69–74. IEEE, 2023. 3 

- [53] Jiageng Mao, Siheng Zhao, Siqi Song, Tianheng Shi, Junjie Ye, Mingtong Zhang, Haoran Geng, Jitendra Malik, Vitor Guizilini, and Yue Wang. Learning from massive human videos for universal humanoid pose control. _arXiv preprint arXiv:2412.14172_ , 2024. 1, 3 

- [54] Andre Meixner, Mischa Carl, Franziska Krebs, No´emie Jaquier, and Tamim Asfour. Towards unifying human likeness: Evaluating metrics for human-like motion retargeting on bimanual manipulation tasks. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 13015–13022. IEEE, 2024. 4 

- [55] Jean-Arcady Meyer and Stewart W Wilson. _Proceedings of the first international conference on simulation of adaptive behavior on From animals to animats_ . MIT press, 1991. 1 

- [56] Charles L Ortiz Jr. Why we need a physically embodied turing test and what it might look like. _AI magazine_ , 37(1): 55–62, 2016. 1 

- [57] Chaitanya Patel, Zhouyingcheng Liao, and Gerard PonsMoll. Tailornet: Predicting clothing in 3d as a function of human pose, shape and garment style. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2020. 2 

- [58] Georgios Pavlakos, Vasileios Choutas, Nima Ghorbani, Timo Bolkart, Ahmed AA Osman, Dimitrios Tzionas, and Michael J Black. Expressive body capture: 3d hands, face, and body from a single image. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 10975–10985, 2019. 2, 4 

- [59] Rolf Pfeifer and Josh Bongard. _How the body shapes the way we think: a new view of intelligence_ . MIT press, 2006. 1 

- [60] Rolf Pfeifer and Christian Scheier. _Understanding intelligence_ . MIT press, 2001. 1 

- [61] Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 9(89):eadi9579, 2024. 1, 3 

- [62] XPeng AI Robot. XPeng IRON. https://www. xiaopeng.com/airobot.html, 2025. 8 

- [63] ENGINEAI Robotics. ENGINEAI PM01. https:// www.engineai.com.cn/product-pm01.html, 2025. 2 

- [64] Unitree Robotics. Unitree G1. https://www. unitree.com/cn/g1, 2025. 2, 3 

- [65] U. Robotics and Contributors. LAFAN1 Retargeting Dataset. https://huggingface.co/datasets/ lvhaidong / LAFAN1 _ Retargeting _ Dataset, 2025. 2, 3 

- [66] Carolina Rutili de Lima, Said Khan, Muhammad Tufail, Syed Shah, and Marcos Maximo. Humanoid robot motion planning approaches: a survey. _Journal of Intelligent & Robotic Systems_ , 110, 2024. 4 

- [67] Shunsuke Saito, Zeng Huang, Ryota Natsume, Shigeo Morishima, Angjoo Kanazawa, and Hao Li. Pifu: Pixel-aligned implicit function for high-resolution clothed human digitization. In _The IEEE International Conference on Computer Vision (ICCV)_ , 2019. 2 

- [68] Shunsuke Saito, Tomas Simon, Jason M. Saragih, and Hanbyul Joo. Pifuhd: Multi-level pixel-aligned implicit function for high-resolution 3d human digitization. In _2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2020, Seattle, WA, USA, June 13-19, 2020_ , pages 81–90. Computer Vision Foundation / IEEE, 2020. 2 

- [69] Yoni Shafir, Guy Tevet, Roy Kapon, and Amit Haim Bermano. Human motion diffusion as a generative prior. In _The Twelfth International Conference on Learning Representations_ , 2024. 3 

- [70] Zehong Shen, Huaijin Pi, Yan Xia, Zhi Cen, Sida Peng, Zechen Hu, Hujun Bao, Ruizhen Hu, and Xiaowei Zhou. World-grounded human motion recovery via gravity-view coordinates. In _SIGGRAPH Asia 2024 Conference Papers_ , pages 1–11, 2024. 2, 4 

- [71] Soyong Shin, Juyong Kim, Eni Halilaj, and Michael J Black. Wham: Reconstructing world-grounded humans with accurate 3d motion. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 2070–2080, 2024. 2, 4 

- [72] Zhuo Su, Lan Xu, Zerong Zheng, Tao Yu, Yebin Liu, and Lu Fang. Robustfusion: Human volumetric capture with data-driven visual cues using a rgbd camera. In _ECCV_ , 2020. 2 

- [73] Yu Sun, Qian Bao, Wu Liu, Yili Fu, Black Michael J., and Tao Mei. Monocular, One-stage, Regression of Multiple 3D People. In _ICCV_ , 2021. 

- [74] Yu Sun, Wu Liu, Qian Bao, Yili Fu, Tao Mei, and Michael J Black. Putting People in their Place: Monocular Regression of 3D People in Depth. In _CVPR_ , 2022. 2 

- [75] Yu Sun, Qian Bao, Wu Liu, Tao Mei, and Michael J Black. Trace: 5d temporal regression of avatars with dynamic cameras in 3d environments. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 8856–8866, 2023. 2 

- [76] Annan Tang, Takuma Hiraoka, Naoki Hiraoka, Fan Shi, Kento Kawaharazuka, Kunio Kojima, Kei Okada, and Masayuki Inaba. Humanmimic: Learning natural locomotion and transitions for humanoid robot via wasserstein adversarial imitation. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 13107–13114. IEEE, 2024. 1, 2, 3 

- [77] Tangfei Tao, Zhiwei Zhang, and Xingyu Yang. Visual perception method based on human pose estimation for hu- 

manoid robot imitating human motions. In _Proceedings of the 2021 2nd international conference on control, robotics and intelligent system_ , pages 54–61, 2021. 3 

- [78] Guy Tevet, Sigal Raab, Brian Gordon, Yonatan Shafir, Daniel Cohen-Or, and Amit H Bermano. Human motion diffusion model. _arXiv preprint arXiv:2209.14916_ , 2022. 3 

- [79] Alan M Turing. Computing machinery and intelligence. In _Parsing the Turing test: Philosophical and methodological issues in the quest for the thinking computer_ , pages 23–65. Springer, 2007. 1, 6 

- [80] Amik Rafly Azmi Ulya, Nathanael Hutama Harsono, Eko Mulyanto Yuniarno, and Mauridhi Hery Purnomo. Hiroposeestimation: A dataset of pose estimation for kid-size humanoid robot. _Journal of Information Technology and Computer Science_ , 8(3):231–240, 2023. 2 

- [81] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 7 

- [82] Ziniu Wan, Zhengjia Li, Maoqing Tian, Jianbo Liu, Shuai Yi, and Hongsheng Li. Encoder-decoder with multi-level attention for 3d human shape and pose estimation. In _2021 IEEE/CVF International Conference on Computer Vision, ICCV 2021, Montreal, QC, Canada, October 10-17, 2021_ , pages 13013–13022. IEEE, 2021. 2 

- [83] Kuan-Chieh Wang, Zhenzhen Weng, Maria Xenochristou, Jo˜ao Pedro Ara´ujo, Jeffrey Gu, Karen Liu, and Serena Yeung. Nemo: Learning 3d neural motion fields from multiple video instances of the same action. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 22129–22138, 2023. 2 

- [84] Xiaoying Wang and Tong Zhang. Reinforcement learning with imitative behaviors for humanoid robots navigation: synchronous planning and control. _Autonomous Robots_ , 48 (2–3), 2024. 4 

- [85] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural information processing systems_ , 35:24824–24837, 2022. 7 

- [86] Yiming Xie, Varun Jampani, Lei Zhong, Deqing Sun, and Huaizu Jiang. Omnicontrol: Control any joint at any time for human motion generation. In _The Twelfth International Conference on Learning Representations_ , 2024. 3 

- [87] Yuliang Xiu, Jinlong Yang, Dimitrios Tzionas, and Michael J. Black. ICON: implicit clothed humans obtained from normals. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2022, New Orleans, LA, USA, June 18-24, 2022_ , pages 13286–13296. IEEE, 2022. 2 

- [88] Ming Yan, Xin Wang, Yudi Dai, Siqi Shen, Chenglu Wen, Lan Xu, Yuexin Ma, and Cheng Wang. Cimi4d: A large multimodal climbing motion dataset under human-scene interactions. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 12977– 12988, 2023. 2 

- [89] Ming Yan, Yan Zhang, Shuqiang Cai, Shuqi Fan, Xincheng Lin, Yudi Dai, Siqi Shen, Chenglu Wen, Lan Xu, Yuexin 

   - Ma, et al. Reli11d: A comprehensive multimodal human motion dataset and method. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 2250–2262, 2024. 4 

- [90] Ming Yan, Xincheng Lin, Yuhua Luo, Shuqi Fan, Yudi Dai, Qixin Zhong, Lincai Zhong, Yuexin Ma, Lan Xu, Chenglu Wen, et al. Climbingcap: Multi-modal dataset and method for rock climbing in world coordinate. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 12312–12323, 2025. 2, 4 

- [91] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interactionpreserving data generation for humanoid whole-body locomanipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 1, 3, 4 

- [92] Ze Yang, Shenlong Wang, Siva Manivasagam, Zeng Huang, Wei-Chiu Ma, Xinchen Yan, Ersin Yumer, and Raquel Urtasun. S3: Neural shape, skeleton, and skinning fields for 3d human modeling. In _CVPR_ , 2021. 2 

- [93] Vickie Ye, Georgios Pavlakos, Jitendra Malik, and Angjoo Kanazawa. Decoupling human and camera motion from videos in the wild. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 21222–21232, 2023. 2 

- [94] Ye Yuan, Umar Iqbal, Pavlo Molchanov, Kris Kitani, and Jan Kautz. Glamr: Global occlusion-aware human mesh recovery with dynamic cameras. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022. 2 

- [95] Anthony Zador, Sean Escola, Blake Richards, Bence ¨Olveczky, Yoshua Bengio, Kwabena Boahen, Matthew Botvinick, Dmitri Chklovskii, Anne Churchland, Claudia Clopath, et al. Catalyzing next-generation artificial intelligence through neuroai. _Nature communications_ , 14(1): 1597, 2023. 1 

- [96] Jianrong Zhang, Yangsong Zhang, Xiaodong Cun, Yong Zhang, Hongwei Zhao, Hongtao Lu, Xi Shen, and Ying Shan. Generating human motion from textual descriptions with discrete representations. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 14730–14740, 2023. 3 

- [97] Jianrong Zhang, Yangsong Zhang, Xiaodong Cun, Yong Zhang, Hongwei Zhao, Hongtao Lu, Xi Shen, and Ying Shan. Generating human motion from textual descriptions with discrete representations. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 14730–14740, 2023. 3 

- [98] Mingyuan Zhang, Zhongang Cai, Liang Pan, Fangzhou Hong, Xinying Guo, Lei Yang, and Ziwei Liu. Motiondiffuse: Text-driven human motion generation with diffusion model. _IEEE transactions on pattern analysis and machine intelligence_ , 46(6):4115–4128, 2024. 3 

- [99] Kun Zhao. Retargeted AMASS for Robotics. https : / / huggingface . co / datasets / fleaven/Retargeted_AMASS_for_robotics, 2025. 2 

- [100] Wentao Zhu, Xiaoxuan Ma, Zhaoyang Liu, Libin Liu, Wayne Wu, and Yizhou Wang. Motionbert: Unified pretraining for human motion analysis. In _ICCV_ , 2023. 2, 7 

- [101] Wentao Zhu, Xiaoxuan Ma, Dongwoo Ro, Hai Ci, Jinlu Zhang, Jiaxin Shi, Feng Gao, Qi Tian, and Yizhou Wang. Human motion generation: A survey. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 46(4):2430– 2449, 2023. 3 

