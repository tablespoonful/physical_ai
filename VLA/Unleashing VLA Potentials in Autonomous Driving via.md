---
title: "Unleashing VLA Potentials in Autonomous Driving via Explicit Learning from Failures"
date: "2026-03-01"
authors: "Yuechen Luo; Qimao Chen; Fang Li; Shaoqing Xu; Jaxin Liu; Ziying Song"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2603.01063
pdf: https://arxiv.org/pdf/2603.01063
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.01063)** / [論文ページ](https://arxiv.org/abs/2603.01063)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **Unleashing VLA Potentials in Autonomous Driving via Explicit Learning from Failures** 

Yuechen Luo<sup>1*</sup> , Fang Li<sup>2*</sup> , Qimao Chen<sup>1*</sup> , Shaoqing Xu<sup>2,‡</sup> , Jiaxin Liu<sup>1</sup> , Ziying Song<sup>3</sup> , Zhi-xin Yang<sup>2,✉</sup> , Fuxi Wen<sup>1,✉</sup> 

1 Tsinghua University, 2 University of Macau, 3 Beijing Jiaotong University 

luo-yc24@mails.tsinghua.edu.cn 

## **Abstract** 

_Vision-Language-Action (VLA) models for autonomous driving often hit a performance plateau during Reinforcement Learning (RL) optimization. This stagnation arises from exploration capabilities constrained by previous Supervised Fine-Tuning (SFT), leading to “persistent failures” in long-tail scenarios. In these critical situations, all explored actions yield a zero-value driving score. This information-sparse reward signals a failure, yet fails to identify its root cause—whether it is due to incorrect planning, flawed reasoning, or poor trajectory execution. To address this limitation, we propose_ **_VLA_** _with_ **_E_** _xplicit_ **_L_** _earning from_ **_F_** _ailures (_ **_ELF-VLA_** _), a framework that augments RL with structured diagnostic feedback. Instead of relying on a vague scalar reward, our method produces detailed, interpretable reports that identify the specific failure mode. The VLA policy then leverages this explicit feedback to generate a_ **_Feedback-Guided Refinement_** _. By injecting these corrected, high-reward samples back into the RL training batch, our approach provides a targeted gradient, which enables the policy to solve critical scenarios that unguided exploration cannot. Extensive experiments demonstrate that our method unlocks the latent capabilities of VLA models, achieving state-of-the-art (SOTA) performance on the public NAVSIM benchmark for overall PDMS, EPDMS and high-level planning accuracy._ 

## **1. Introduction** 

The development of autonomous driving systems is undergoing a paradigm shift from traditional modular architectures to end-to-end frameworks [4, 11]. Vision-LanguageAction (VLA) models are at the forefront of this transition [15]. These models map raw camera sensor inputs to coherent vehicle motion commands by applying supervised fine-tuning (SFT) and reinforcement learning (RL) 

*Equal contribution. ‡Project Leader. ✉ Corresponding author. 


Figure 1. **The comparison between RL fine-tuning of general VLA and ELF-VLA.** Top: VLA training with RL algorithm suffers from a performance plateau: in certain scenarios, the policy model’s rollouts consistently yield low-scoring answers, trapping the agent and preventing it from discovering a better policy. Bottom: ELF-VLA addresses this by using a teacher model to provide structured feedback, which is then used to re-rollout a refinement, forcing the policy to break through this performance plateau. 

to large Vision-Language Models (VLMs). This integrated design eliminates manually engineered interfaces and supports large-scale, data-driven policy learning. Notably, VLA models can generate intermediate reasoning trajectories via a “think” module, mimicking human problemsolving strategies, offering a promising direction toward achieving explainable and trustworthy autonomous driving [17, 25, 41]. 

Despite this progress, RL fine-tuning continues to exhibit a performance plateau: we observe that after SFT, the model’s policy exploration capability is severely constrained by the SFT dataset’s limitations, where common scenarios are highly prevalent and the safety-critical scenarios that rigorously test the autonomous system’s capabilities are rare [8, 23]. Consequently, under safety-critical and challenging scenarios (such as complex unprotected left turns or emergency evasions), all exploratory rollouts consistently fail, yielding a zero driving score, as shown in the top row of Fig. 1. Existing VLA-RL approaches 

24833 

simplify performance evaluation during training to a single scalar reward (e.g., PDMS [7]). When the model fails, this information-sparse reward is insufficient to pinpoint the root cause of the error, making it unclear whether the failure stems from the cumulative errors of high-level planning in the “think” module, flawed cognitive reasoning about critical targets, or dynamic deficiencies in the low-level trajectory. 

To address these limitations and enable continual learning, this paper proposes a novel VLA training framework for autonomous driving that bridges failure diagnosis and policy correction. As shown in the bottom row of Fig. 1, the main idea is to provide feedback with structured failure analysis to help VLA with its “Think-then-Act” architecture, rather than relying on simple scalar rewards. This approach features two core innovations: 

- **VLA Ability-aligned Feedback:** We introduce a feedback mechanism using a teacher model, which is triggered when the VLA encounters persistent failures. This model generates a structured diagnostic report aligned with VLA’s ability that pinpoints specific errors within the VLA’s planning, reasoning, or execution levels. 

- **Feedback-Guided Refinement and Re-injection:** The VLA policy model (student) leverages this diagnostic report to generate a corrected trajectory. This high-reward corrected sample is then re-injected into the GRPO training batch. This process provides a goal-directed gradient signal that was previously non-existent in the rollout batch. 

Through extensive evaluations on the Navsim benchmark, our method demonstrates significant performance improvements over existing VLA baselines. Our approach achieves SOTA performance on both the overall driving metric (PDMS) and high-level planning accuracy. By bridging explainable feedback with policy correction, our work provides a practical path for VLA models to overcome performance plateaus in autonomous driving. 

## **2. Related Work** 

**VLA models for autonomous driving.** The integration of visual and textual data for unified perception, planning, and decision-making has led to a surge of interest in VisionLanguage Models (VLMs) for autonomous driving in recent years. Two primary paradigms currently dominate the field. The first is dedicated to scene understanding and high-level reasoning [13, 14, 26, 28, 33]. An example of this approach, Senna [13], processes sensory inputs to generate meta-actions for downstream planners, yet substantial improvements in actual driving performance have not been fully realized. The alternative paradigm concentrates on the direct prediction of driving trajectories from raw inputs [10, 12, 24, 30, 34, 35, 40]. A notable development, aimed at enhancing model interpretability and accu- 

racy, is the increasing use of intermediate reasoning (e.g., Chain-of-Thought, CoT) to reveal internal cognitive processes. Evidence from EMMA [12], ReasonPlan [24], and Sce2DriveX [40] confirms that domain-specific reasoning markedly improves the precision of trajectory forecasting. **RL fine-tuning for VLA models.** Currently, VLA models in autonomous driving are typically trained using a twostage paradigm: an initial supervised fine-tuning (SFT) phase on a driving dataset, followed by a reinforcement learning (RL) training phase. In this framework, the efficacy of the RL stage is heavily dependent on the performance of the preceding SFT. Current approaches [17, 25, 41] employ the Group Relative Policy Optimization (GRPO) [31] algorithm for RL training, where rewards are measured by VLA’s driving score (e.g., PDMS). This leads to a significant training deficiency: the VLA model, following SFT phase, struggles to handle the rare, long-tail scenarios present in the training dataset. Consequently, when the model enters RL stage, its driving score in these specific scenarios remains extremely low, regardless of the number of rollouts. This causes the model’s overall learning to stagnate, resulting in a performance plateau. In LLM literature, approaches have successfully used non-numerical feedback, such as textual critiques, to provide detailed guidance [3, 39]. Others [27, 37] have used mix-policy methods to internalize knowledge from high-quality data, enhancing exploration and policy quality. Inspired by these approaches, our work introduces a feedback mechanism to address this limitation in the autonomous driving domain, which employs a teacher model to analyze and rectify the VLA model’s erroneous driving behaviors by structured feedback, correcting them into proper actions. 

## **3. Methods** 

In this section, we present our proposed method (Fig. 2), which contains two main components: (1) a two-stage Supervised fine-Tuning (SFT) process, and (2) a Reinforcement Learning (RL) framework enhanced with failure feedback. 

### **3.1. VLA Inputs Formulation** 

In our method, the VLA model is as the generator and refiner simultaneously, designed to accept two distinct types of inputs: the original, feedback-free **base inputs** , and the **feedback inputs** , which incorporate corrective guidance. **Base inputs.** The base input query _q_<sup>_base_</sup> includes a frontview image denoted as _I_ cam, high-level navigation commands _q_ com (e.g., _Move Forward, Turn Left, Turn Right_ ), ego state information _q_ ego (e.g., _velocity and acceleration_ ), and the historical trajectory of the last three frames _q_ his = _{ht−_ 3 _, ht−_ 2 _, ht−_ 1 _}_ at a frequency of 2Hz. **Feedback inputs.** Based on the base inputs, the VLA model outputs an original response _o_ consisting of trajec- 

24834 


Figure 2. **Overview of ELF-VLA.** First, the model is pre-trained on an autonomous driving Q&A dataset to provide it with foundational driving knowledge. Subsequently, it undergoes SFT on a mixed dataset of “Base Inputs” and “Feedback Inputs”, enabling it to learn trajectory prediction and feedback-based refinement simultaneously. Finally, in the RL phase, a teacher model is used to generate feedback, thereby reducing the proportion of zero-reward rollouts. 

tory with CoT (details in Appendix 7.2), which is then classified based on a threshold _s_ : responses with a PDMS exceeding _s_ are deemed “correct” ( _oc_ ), while those with a score below _s_ are deemed “wrong” ( _ow_ ). 


In the case of a correct response, the corresponding feedback inputs are composed of three components: the original base inputs _qbase_ , the correct response _oc_ itself, and a rule-based positive feedback _f_<sup>_rule_</sup> . For wrong responses, we employ an external intervention through a VLM teacher model. This teacher model takes the base inputs _q_<sup>_base_</sup> , the erroneous trajectory _ow_ , and the ground-truth trajectory _ogt_ to generate a structured feedback _f_<sup>_teacher_</sup> . This feedback includes (1) Meta Action Analysis, (2) Think Process Analysis, (3) Safety Failure Analysis, (4) Efficiency Failure Analysis and (5) Actionable Correction (with lateral and longitudinal components). The final feedback inputs for the VLA are then constructed by combining the base inputs, the original wrong response _oi_ , and the generated structured feedback. Detailed examples of base inputs and feedback inputs are in the Appendix 7.2. 

This dataset is assembled from a diverse collection of opensource driving QA datasets, including DriveLM [32], LingoQA [28], ImpromptuVLA [5], and other open-source driving datasets [9, 29, 34]. In addition, we constructed a multi-turn Q&A reasoning dataset for NAVSIM following the CoT paradigm. This phase addresses tasks like road boundary estimation (drivable area), critical object identification (object localization), ego action prediction, and related traffic semantics. Further details on dataset composition are provided in the Appendix 7.1. 

Subsequently, the second stage introduces the trajectory prediction and refinement task. For each query _q_<sup>_base_</sup> and _q_<sup>_fb_</sup> (defined in Sec. 3.3), the model’s output is supervised by the ground-truth trajectory _ogt_ , aiming to maximize the conditional likelihood: 


_D_ denotes the dataset including _{_ ( _qbase, ogt_ ) _,_ ( _qfb, ogt_ ) _}_ and _πθ_ denotes the VLA model. This mixed-dataset training approach equips the model with the dual capabilities of trajectory prediction and feedback-based trajectory refinement, thereby enabling the model to leverage failure feedback during the reinforcement learning phase. 

### **3.3. RL with Failure Feedback** 

### **3.2. Two-Stage SFT for Cognition and Refinement** 

We employ a two-stage supervised fine-tuning procedure to develop a model that combines both driving knowledge and trajectory planning capabilities. The first stage is designed to infuse the model with general driving knowledge. The second stage is dedicated to equipping the model with the capacity for trajectory prediction, along with the ability to implement refinements based on received feedback. 

As shown in Fig. 2, in the first stage, the model is pretrained on a large dataset of driving-related Q&A pairs to enhance its understanding of driving domain cognition. 

Our failure-feedback mechanism is applied during the rollout phase of the GRPO algorithm. Conventional VLA models for autonomous driving typically hit a performance bottleneck during RL training. This occurs because they cannot manage complex, long-tail scenarios; consequently, the trajectories sampled in these situations receive extremely low driving scores, resulting in a sparse reward problem. Our method addresses this by introducing a feedback mechanism that successfully boosts the model’s driving scores in these critical scenarios, enabling the agent to break through the performance plateau. 

24835 


Figure 3. **Overview of GRPO with feedback** . The policy model generates initial responses. Based on the rewards, teacher model (Qwen3VL-32B) provides feedback, guiding the policy to sample improved refinement responses. A high-quality refinement response is selected and combined with the initial response set for joint optimization. Policy Shaping is applied to the final probability. 

**Efficient Difficult-Sample Curation.** Before introducing the GRPO with a feedback mechanism, we first perform a cost-effective data curation to maximize training efficiency. Naive RL training often wastes resources on overly simple (already mastered) scenarios that provide weak learning signals. Our curation aims to filter out these samples and focus the agent on high-value, informative scenarios, which include both difficult samples (where the model consistently fails) and ambiguous samples (where the model is most uncertain). To achieve this, we utilize the SFT model to sample _N_ rollouts for each query, estimating its mean reward and reward variance. We then discard samples characterized by high mean reward and low variance, as these indicate consistent success. This strategy effectively concentrates training on the difficult (low mean, low variance) and ambiguous (high variance) scenarios. Through this method, we filter the initial 85k training entries down to a core dataset of 24k high-value scenarios. 

**Reward modeling.** To incentivize the VLA model to learn effective driving behaviors and to ensure the stability of its output format, we designed a reward function with three components: the PDMS Reward, the Format Reward, and the Goal Reward. The **PDMS Reward** _rtraj_ is a comprehensive trajectory evaluation metric based on the Predictive Driver Model Score [7]. It is represented as a continuous value ranging from 0 to 1. The specific formula used to calculate this score is provided in Appendix 9.1. The **Format Reward** _rfmt_ is a binary (1 or 0) reward designed to enforce adherence to the required output format strictly. Finally, the **Goal Reward** _rgoal_ incentivizes endpoint accu- 

racy by assigning a tiered reward based on the L1 distance to the GT endpoint. Detailed calculations for each reward are provided in the Appendix 8.1. The overall reward in the reinforcement learning process is computed by integrating four designed reward components, which are presented as follows: 

_r_ = _rtraj_ + _rfmt_ + _rgoal._ (3) 

**GRPO with feedback.** Our method employs a feedback mechanism, illustrated in Fig. 3, to refine trajectories and increase rewards, thereby enabling the VLA model to surpass its performance plateau. More specifically, the process begins by sampling a batch of trajectory responses _{oi}_<sup>_n_</sup> _i_ =1 using the base inputs _q_<sup>_base_</sup> . The rewards for this batch _{ri}_<sup>_n_</sup> _i_ =1<sup>arethencomputed,whichinclude</sup><sup>_{rtraj,i}_</sup> _i_<sup>_n_</sup> =1<sup>,</sup> _{rfmt,i}_<sup>_n_</sup> _i_ =1<sup>,and</sup><sup>_{rgoal,i}_</sup> _i_<sup>_n_</sup> =1<sup>.</sup> Based on the predefined threshold _s_ , these responses are then classified into two groups: correct responses _{oc}_ and wrong responses _{ow}_ . Finally, following Sec. 3.1, both the correct and wrong responses are processed accordingly and then assembled to create the final feedback inputs _{qi_<sup>_fb}_</sup> _i_<sup>_n_</sup> =1<sup>.</sup> 

Subsequently, the VLA model generates a new batch of responses _{o_<sup>_fb_</sup> _i_<sup>_}_</sup> _i_<sup>_n_</sup> =1<sup>fromthefeedbackinputs(</sup><sup>_{q_</sup> _i_<sup>_fb}_</sup> _i_<sup>_n_</sup> =1<sup>)</sup> and calculates their rewards _{ri_<sup>_fb}_</sup> _i_<sup>_n_</sup> =1<sup>.We randomly select</sup> _k_ responses from the subset of _{o_<sup>_fb_</sup> _i_<sup>_}_</sup> _i_<sup>_n_</sup> =1<sup>whosetrajectory</sup> rewards ( _rtraj_<sup>_fb_)exceedtheoriginalbatch’smaximumtra-</sup> jectory reward _max_ ( _rtraj_ ). If fewer than _k_ such “better” responses exist, the remaining slots are filled by duplicating the original response that achieved this maximum reward. This results in a final batch of _n_ + _k_ rollout samples _{_ ( _qi_<sup>_final_</sup> _, o_<sup>_final_</sup> _i_ ) _}_<sup>_n_</sup> _i_ =1<sup>+</sup><sup>_k_,fromwhichtherelativeadvantage</sup> 

24836 

_{Ai}_<sup>_n_</sup> _i_ =1<sup>+</sup><sup>_k_isthencomputed.Detailsoftherolloutupdate</sup> algorithm are in Alg. 1. The final optimization objective for GRPO is defined as follows: 


where _Dfinal_ = _{_ ( _qi_<sup>_final_</sup> _, o_<sup>_final_</sup> _i_ ) _}_<sup>_n_</sup> _i_ =1<sup>+</sup><sup>_k_,</sup><sup>_πref_istherefer-</sup> ence policy of the initial SFT model, and _β_ is a hyperparameter. We apply the CLIP only to the original batch rollout samples, not to the responses that have been refined by feedback. To compute the advantages, we first merge both sets of rewards into a unified set _runion_ . The mean and standard deviation of this combined set are then used to normalize the rewards and calculate the relative advantages, _Ai_ and _A_<sup>_fb_</sup> _j_<sup>, as follows:</sup> 


For the token-level probability ratios of the feedbackgenerated outputs, a challenge arises from a mismatch in conditioning. These samples are generated using the feedback query _q_<sup>_fb_</sup> , but our optimization objective is conditioned on the base query _q_<sup>_base_</sup> . This discrepancy can cause the refined responses _{o_<sup>_fb_</sup> _}_ to have very low probabilities under the optimization policy, leading to high variance, potential gradient explosion, and training instability. Therefore, inspired by LUFFY [37], we employ Policy Shaping _f_ ( _x_ ) = _x_ + _<u>x</u> γ_<sup>(0</sup><sup>_<γ<_1).Thistechniqueassignshigher</sup> weights to low-probability tokens within the _{o_<sup>_fb_</sup> _}_ . Such mechanism encourages the model to learn valuable knowledge from rare but correct trajectories that might otherwise be overlooked. The standard ratio _ci_ ( _θ_ ) and the shaped ratio _f_ ( _c_<sup>_fb_</sup> _j_<sup>(</sup><sup>_θ_)) are defined as:</sup> 


## **4. Experiment** 

### **4.1. Implementation details** 

**Dataset.** We perform comprehensive experiments and evaluations on NAVSIM [7], a planning-oriented autonomous driving dataset built on the OpenScene platform. In addition to the reasoning data collected from NAVSIM, we 

**Algorithm 1** Rollout Update of GRPO with Feedback 

#### **Input:** 


**Output:** 

also leverage several open-source datasets, as described in Sec. 3.2. 

**Metric.** We evaluate our method’s performance on two distinct aspects of autonomous driving: **high-level planning** and **trajectory prediction** . 

For high-level planning evaluation, we use High-Level Planning Accuracy, which strictly requires the entire metaaction, comprising both longitudinal speed and lateral path, to match the ground truth exactly. Here, the ground truth is generated by GT trajectory, detailed infos in Appendix 9.1. 

For trajectory prediction evaluation on the NAVSIM benchmark, we utilize the Predictive Driver Model Score (PDMS) for **NAVSIMv1** [7] and the Extended Predictive Driver Model Score (EPDMS) for **NAVSIMv2** [2] as the closed-loop planning metrics. 

**Training Details.** We use InternVL3-8B [42] as the base model, trained in three stages. First, we pretrain on a largescale driving knowledge dataset. Second, we fine-tune the model on a hybrid dataset, consisting of curated Navsim planning dataset (with CoT annotations) and the feedback dataset from Sec. 3. Third, we apply reinforcement learning using 64 NVIDIA H20 GPUs. We use Qwen3-VL-32B [1] as the teacher model. Key RL parameters include 8 rollouts per batch, a threshold _s_ = 0 _._ 8, a policy shaping parameter _γ_ = 0 _._ 1, and _k_ = 1 refinement response. Additional details and hyperparameters are in the Appendix 9.1. 

24837 

Table 1. Comparison with state-of-the-art methods on the NAVSIMv1 with PDMS. 

|**Method**|**Image**|**Lidar**|**NC**_↑_|**DAC**_↑_|**TTC**_↑_|**CF**_↑_|**EP**_↑_|**PDMS**_↑_|
|---|---|---|---|---|---|---|---|---|
|Constant Velocity|||68.0|57.8|50.0|100|19.4|20.6|
|Ego Status MLP|||93.0|77.3|83.6|100|62.8|65.6|
|UniAD [11]|✓||97.8|91.9|92.9|100|78.8|83.4|
|TransFuser [6]|✓|✓|97.7|92.8|92.8|100|84.0|84.0|
|DiffusionDrive [22]|✓|✓|98.2|96.2|94.7|100|82.2|88.1|
|WoTE [18]|✓|✓|98.5|96.8|94.9|99.9|81.9|88.3|
|Hydra-NeXt [21]|✓||98.1|97.7|94.6|100|81.8|88.6|
|AutoVLA-3B [41]|✓||98.4|95.6|98.0|100|81.9|89.1|
|DriveVLA-W0-3B [36]|✓||98.7|**99.1**|95.3|99.3|83.3|90.3|
|GoalFlow [36]|✓|✓|98.4|98.3|94.6|100|85.0|90.3|
|InternVL3-8B-SFT|✓||98.5|95.5|95.3|100|81.2|87.4|
|InternVL3-8B-RL|✓||98.5|96.7|95.4|100|83.2|89.0|
|**ELF-VLA-8B**(Ours)|✓||**98.9**|98.1|**96.0**|**100**|**85.3**|**91.0**|


Table 2. Comparison with state-of-the-art methods on the NAVSIMv2 with EPDMS. 

|**Method**|**NC**_↑_|**DAC**_↑_|**DDC**_↑_|**TLC**_↑_|**EP**_↑_|**TTC**_↑_|**LK**_↑_|**HC**_↑_|**EC**_↑_|**EPDMS**_↑_|
|---|---|---|---|---|---|---|---|---|---|---|
|Recogdrive-8B [19]|98.3|95.2|99.5|**99.8**|87.1|97.5|96.6|**98.3**|86.5|83.6|
|DiffusionDrive [22]|98.2|95.9|99.4|**99.8**|87.5|97.3|96.8|**98.3**|**87.7**|84.5|
|HydraMDP++ [20]|98.5|98.5|99.5|99.7|87.4|97.9|95.8|98.2|75.7|85.6|
|DriveVLA-W0-3B [16]|98.5|**99.1**|98.0|99.7|86.4|98.1|93.2|97.9|58.9|86.1|
|DriveSuprim [38]|98.4|98.6|**99.6**|**99.8**|**90.5**|97.8|**97.0**|**98.3**|78.6|**87.1**|
|**ELF-VLA-8B**(Ours)|**98.9**|98.1|99.4|**99.8**|88.5|**98.4**|96.9|**98.3**|87.2|**87.1**|


### **4.2. Performance Comparison** 

**Navsim Benchmark.** Tab. 1 presents the performance comparison between ELF-VLA and current leading methods on the NAVSIMv1 benchmark. Under the vision-only setting, ELF-VLA achieves a PDMS of 91.0, establishing a new state-of-the-art (SOTA). This result represents a significant improvement of 1.9 PDMS over the previous best visiononly method, AutoVLA. Furthermore, ELF-VLA outperforms the SFT-only (InternVL3-8B-SFT) and traditional RL (InternVL3-8B-RL) baselines by 3.6 and 2.0 PDMS, respectively. On the NAVSIMv2 benchmark (Tab. 2), ELFVLA continues its strong performance by achieving a new SOTA of 87.1 EPDMS. This score is on par with the recent SOTA DriveSuprim, demonstrating its highly competitive driving capability. These findings demonstrate that ELFVLA substantially enhances the model’s driving capabilities over conventional RL approaches, particularly in addressing challenging driving scenarios. Moreover, the outstanding performance across both benchmarks confirms that ELF-VLA is not merely overfitting to the PDMS metric; rather, it exhibits robust generalization by excelling on the distinct and more comprehensive EPDMS as well. 

**Quantitative Evaluation.** We compare ELF-VLA (Tab. 3) against several ablation models (detailed definitions in Ap- 

Table 3. Performance comparison of ELF-VLA against conventional GRPO and other feedback strategies. 

|Method|NC_↑_|DAC_↑_|TTC_↑_|CF_↑_|EP_↑_|PDMS_↑_|
|---|---|---|---|---|---|---|
|SFT|98.5|95.5|95.3|100|81.3|87.4|
|GRPO|98.5|96.7|95.4|100|83.2|89.0|
|GT-GRPO|98.1|97.1|93.5|100|85.2|89.2|
|Rule-GRPO|98.3|97.3|94.8|100|84.5|89.6|
|**ELF-VLA**|**98.9**|**98.1**|**96.0**|**100**|**85.3**|**91.0**|


pendix 9.1): 

- **SFT (Baseline):** The base model trained solely with Supervised Finetuning. 

- **GRPO:** The SFT model was further finetuned using the conventional GRPO algorithm. 

- **GT-GRPO:** The SFT model finetuned on a response set augmented with Ground Truth (GT) trajectories, which are added directly. 

- **Rule-GRPO:** The SFT model finetuned on a response set augmented with new responses, which are regenerated based on feedback from predefined rules. 

- **ELF-VLA:** The SFT model finetuned on a response set augmented with new, refined responses, which are regenerated based on structured feedback from our teacher model. 

24838 


Figure 4. **Ratio of total-failure samples** measured during the RL training phase for GRPO, GT-GRPO, Rule-GRPO, and ELF-VLA. A total failure indicates all rollouts for a sample failed on a specific metric (PDMS below _s_ , NC of 0 and DAC of 0, respectively). 

Notably, ELF-VLA achieves the best overall performance. Our method outperforms the conventional GRPO method by 2.0 PDMS. This demonstrates that by introducing structured feedback and regenerating superior, indistribution trajectories, our approach helps the model resolve persistent failure issues. Furthermore, ELF-VLA surpasses GT-GRPO and Rule-GRPO by 1.8 and 1.4 PDMS, respectively. This highlights the distinct limitations of these two baselines. For GT-GRPO, the GT trajectories exhibit a significant distributional shift from the original VLAgenerated responses. The low likelihood of these GT responses makes the optimization difficult. For Rule-GRPO, the feedback from predefined rules has a limited impact on the model. This process is akin to simple self-refinement and lacks granular guidance, causing the model to fail to learn effective trajectory correction from such simplistic feedback. In contrast, ELF-VLA utilizes the teacher model’s extensive general knowledge to perform a deep, structured analysis of the original response. The VLA model receives this comprehensive feedback, which enables it to learn from its failures and refine the trajectory. This process results in a superior, more easily optimizable refined trajectory. 

**Total-Failure Ratio Analysis.** We analyze the failure rates during the RL training phase across these models, as shown in Fig. 4. Specifically, we measure the proportion of samples where all rolled-out trajectories fail simultaneously on key metrics: PDMS, DAC, and NC. As illustrated in the figure, while intermediate strategies like GT-GRPO and RuleGRPO help reduce failure ratios, ELF-VLA demonstrates the most significant improvements across all metrics. ELFVLA reduces the total-failure PDMS rate from 2.73% (for GRPO) to just 1.08%, with similarly strong reductions observed for NC and DAC. This result further validates that our method enables the model to learn from its mistakes, address the persistent failure problem, and ultimately en- 

Table 4. Comparison of high-level planning on NAVSIM. 

|Method|Speed Acc._↑_|Path Acc._↑_|Accuracy_↑_|
|---|---|---|---|
|Qwen2.5-VL-7B|37.8|61.3|19.1|
|InternVL3-8B|40.9|58.7|20.1|
|Qwen2.5-VL-32B|46.6|55.3|27.6|
|Qwen2.5-VL-72B|49.4|62.6|28.7|
|SFT|84.2|90.7|79.2|
|GRPO|84.3|90.8|79.3|
|GT-GRPO|83.5|90.5|78.4|
|Rule-GRPO|84.5|91.2|79.5|
|**ELF-VLA**|**85.8**|**92.5**|**80.3**|


Table 5. Ablation study on the number of training data in RL. _†_ : Randomly sampled. *: Curated as Sec. 3.3. 

|Num.|NC_↑_|DAC_↑_|TTC_↑_|CF_↑_|EP_↑_|PDMS_↑_|
|---|---|---|---|---|---|---|
|85k|98.5|96.8|95.3|100|83.4|89.1|
|24k_†_|98.4|96.8|95.2|100|83.1|88.9|
|24k*|**98.9**|**98.1**|**96.0**|**100**|**85.3**|**91.0**|


hance overall driving safety and robustness. **High-Level Planning Evaluation.** As shown in Tab. 4, our results highlight the clear advantage of ELF-VLA in highlevel planning. ELF-VLA achieves the best results in both longitudinal Speed Accuracy and lateral Path Accuracy, achieving the highest overall Planning Accuracy of 80.3%, 1.0% higher than conventional GRPO. Moreover, compared to open-source models, ELF-VLA outperforms the significantly larger Qwen2.5-VL-72B model by 51.6% in accuracy. This improvement stems from the teacher model providing refined meta actions, where the VLA model learns to internalize. This demonstrates that ELF-VLA can learn from failure cases to refine its high-level planning. 

### **4.3. Ablation Studies** 

**On GRPO with Training Data.** We investigate the impact of training data volume and composition for RL, as shown in Tab. 5. Using the full 85k dataset (89.1 PDMS) or a randomly sampled 24k subset (88.9 PDMS) both yield suboptimal results. In contrast, our curated 24k dataset (24k*), guided by Sec. 3.3, achieves the best performance of 91.0 PDMS. This suggests that the full 85k dataset is dominated by simple scenarios that provide limited learning signals, which weakens the overall gradient signal and leads to inefficient policy updates focused on already-mastered scenarios. Our curation strategy effectively distills the most valuable data. Combined with our feedback mechanism, this data allows for targeted training on these complex scenarios. This approach ultimately improves model performance and enhances training efficiency. 

**On GRPO with Feedback.** Tab. 6 analyzes our feedback components. We first vary the number of refinement responses, _k_ . Optimal performance (91.0 PDMS) is achieved 

24839 


Figure 5. **Visualization of trajectory refinement process by ELF-VLA on the NAVSIM dataset.** Visualization of the initial Wrong Trajectories (red), the Ground Truth (green), and the final Refined Trajectory (blue). A teacher-generated Feedback guides the refinement of a Wrong Trajectory into a Refined Trajectory. Colored text in the Feedback details the specific refinements that have been applied. 

Table 6. Ablation study on the number of refinement responses _k_ and the use of Policy Shaping (PS). 

|_k_|PS|NC_↑_|DAC_↑_|TTC_↑_|CF_↑_|EP_↑_|PDMS_↑_|
|---|---|---|---|---|---|---|---|
|4|✓|98.5|96.7|95.4|100|83.3|89.0|
|2|✓|98.2|97.5|94.3|100|84.9|89.7|
|1|✗|98.5|97.0|94.9|100|83.9|89.3|
|1|✓|**98.9**|**98.1**|**96.0**|**100**|**85.3**|**91.0**|


at _k_ = 1. Increasing _k_ degrades performance, dropping to 89.0 at _k_ = 4. This suggests that while a single targeted refinement is effective, multiple feedback-based responses may distract the policy. We also evaluate Policy Shaping (PS). Removing PS (at _k_ = 1) causes a significant 1.7% drop in PDMS from 91.0 to 89.3. This confirms PS is critical for preventing training collapse and formatting errors, ensuring the model can properly learn from high-advantage, low-probability refinement trajectories. 

### **4.4. Visualization of Refinement Process** 

Fig. 5 illustrates a qualitative example where ELF-VLA corrects a fault trajectory in a complex left-turn scenario. The initial fault trajectory (red curve) led to a potential collision, rooted in a significant misestimation of a key obstacle (predicted: 15.57m ahead, 8.11m left). Our teacher model provides structured feedback, precisely identifying this “Think Process” error and estimating the more accurate location (11.43m ahead, 4.11m left). Concurrently, it 

offers actionable corrections, such as adjustments to the target lateral position and longitudinal speed. Based on this feedback, the model generates the Refined Trajectory (blue curve). The corresponding “Key Obstacle Analysis” in the refined plan reflects this corrected perception, enabling the agent to plot a safer trajectory that successfully avoids the obstacle. More results can be found in Appendix 9.2. 

## **5. Conclusion** 

This paper proposes ELF-VLA, a framework for explicit learning from failures. Our approach augments the VLA policy with a powerful teacher model that produces structured diagnostic reports and identifies the underlying failure mode whenever a failure occurs. The policy then leverages this explicit, human-like feedback to synthesize a corrected, high-reward trajectory. By re-injecting these corrected samples into the RL training batch, ELF-VLA delivers targeted gradients that enable the policy to resolve challenging scenarios where unguided exploration rarely overcomes. 

The primary limitation of this method lies in its dependence on an external teacher model, which inherently bounds the student model’s performance by the teacher’s analytical capabilities. Furthermore, all experiments were conducted on the Navsim benchmark, a non-reactive simulation environment. Future work will involve exploring the role of different teacher models as well as performing closed-loop evaluations on more diverse datasets. 

24840 

## **6. Acknowledgments** 

This work was partially supported by the National Key R&D Program of China under Grant 2023YFE0205800 and 2024YFB2505803. 

## **References** 

- [1] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 5 

- [2] Wei Cao, Marcel Hallgarten, Tianyu Li, Daniel Dauner, Xunjiang Gu, Caojun Wang, Yakov Miron, Marco Aiello, Hongyang Li, Igor Gilitschenski, et al. Pseudo-simulation for autonomous driving. _arXiv preprint arXiv:2506.04218_ , 2025. 5, 3 

- [3] Angelica Chen, J´er´emy Scheurer, Jon Ander Campos, Tomasz Korbak, Jun Shern Chan, Samuel R Bowman, Kyunghyun Cho, and Ethan Perez. Learning from natural language feedback. _Transactions on machine learning research_ , 2024. 2 

- [4] Li Chen, Penghao Wu, Kashyap Chitta, Bernhard Jaeger, Andreas Geiger, and Hongyang Li. End-to-end autonomous driving: Challenges and frontiers. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2024. 1 

- [5] Haohan Chi, Huan-ang Gao, Ziming Liu, Jianing Liu, Chenyu Liu, Jinwei Li, Kaisen Yang, Yangcheng Yu, Zeda Wang, Wenyi Li, et al. Impromptu vla: Open weights and open data for driving vision-language-action models. _arXiv preprint arXiv:2505.23757_ , 2025. 3, 1 

- [6] Kashyap Chitta, Aditya Prakash, Bernhard Jaeger, Zehao Yu, Katrin Renz, and Andreas Geiger. Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. _IEEE transactions on pattern analysis and machine intelligence_ , 45(11):12878–12895, 2022. 6 

- [7] Daniel Dauner, Marcel Hallgarten, Tianyu Li, Xinshuo Weng, Zhiyu Huang, Zetong Yang, Hongyang Li, Igor Gilitschenski, Boris Ivanovic, Marco Pavone, et al. Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. _Advances in Neural Information Processing Systems_ , 37:28706–28719, 2024. 2, 4, 5, 3 

- [8] Wenhao Ding, Chejian Xu, Mansur Arief, Haohong Lin, Bo Li, and Ding Zhao. A survey on safety-critical driving scenario generation—a methodological perspective. _IEEE Transactions on Intelligent Transportation Systems_ , 24(7): 6971–6988, 2023. 1 

- [9] Xinpeng Ding, Jianhua Han, Hang Xu, Xiaodan Liang, Wei Zhang, and Xiaomeng Li. Holistic autonomous driving understanding by bird’s-eye-view injected multi-modal large models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 13668– 13677, 2024. 3, 1 

- [10] Haoyu Fu, Diankun Zhang, Zongchuang Zhao, Jianfeng Cui, Dingkang Liang, Chong Zhang, Dingyuan Zhang, Hongwei Xie, Bing Wang, and Xiang Bai. Orion: A holistic end-toend autonomous driving framework by vision-language in- 

structed action generation. _arXiv preprint arXiv:2503.19755_ , 2025. 2 

- [11] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 17853–17862, 2023. 1, 6 

- [12] Jyh-Jing Hwang, Runsheng Xu, Hubert Lin, Wei-Chih Hung, Jingwei Ji, Kristy Choi, Di Huang, Tong He, Paul Covington, Benjamin Sapp, et al. Emma: End-to-end multimodal model for autonomous driving. _arXiv preprint arXiv:2410.23262_ , 2024. 2 

- [13] Bo Jiang, Shaoyu Chen, Bencheng Liao, Xingyu Zhang, Wei Yin, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. Senna: Bridging large vision-language models and end-to-end autonomous driving. _arXiv preprint arXiv:2410.22313_ , 2024. 2 

- [14] Bo Jiang, Shaoyu Chen, Qian Zhang, Wenyu Liu, and Xinggang Wang. Alphadrive: Unleashing the power of vlms in autonomous driving via reinforcement learning and reasoning. _arXiv preprint arXiv:2503.07608_ , 2025. 2 

- [15] Sicong Jiang, Zilin Huang, Kangan Qian, Ziang Luo, Tianze Zhu, Yang Zhong, Yihong Tang, Menglin Kong, Yunlong Wang, Siwen Jiao, et al. A survey on vision-languageaction models for autonomous driving. _arXiv preprint arXiv:2506.24044_ , 2025. 1 

- [16] Yingyan Li, Shuyao Shang, Weisong Liu, Bing Zhan, Haochen Wang, Yuqi Wang, Yuntao Chen, Xiaoman Wang, Yasong An, Chufeng Tang, et al. Drivevla-w0: World models amplify data scaling law in autonomous driving. _arXiv preprint arXiv:2510.12796_ , 2025. 6 

- [17] Yue Li, Meng Tian, Dechang Zhu, Jiangtong Zhu, Zhenyu Lin, Zhiwei Xiong, and Xinhai Zhao. Drive-r1: Bridging reasoning and planning in vlms for autonomous driving with reinforcement learning. _arXiv preprint arXiv:2506.18234_ , 2025. 1, 2 

- [18] Yingyan Li, Yuqi Wang, Yang Liu, Jiawei He, Lue Fan, and Zhaoxiang Zhang. End-to-end driving with online trajectory evaluation via bev world model. _arXiv preprint arXiv:2504.01941_ , 2025. 6 

- [19] Yongkang Li, Kaixin Xiong, Xiangyu Guo, Fang Li, Sixu Yan, Gangwei Xu, Lijun Zhou, Long Chen, Haiyang Sun, Bing Wang, et al. Recogdrive: A reinforced cognitive framework for end-to-end autonomous driving. _arXiv preprint arXiv:2506.08052_ , 2025. 6, 1 

- [20] Zhenxin Li, Kailin Li, Shihao Wang, Shiyi Lan, Zhiding Yu, Yishen Ji, Zhiqi Li, Ziyue Zhu, Jan Kautz, Zuxuan Wu, et al. Hydra-mdp: End-to-end multimodal planning with multitarget hydra-distillation. _arXiv preprint arXiv:2406.06978_ , 2024. 6 

- [21] Zhenxin Li, Shihao Wang, Shiyi Lan, Zhiding Yu, Zuxuan Wu, and Jose M Alvarez. Hydra-next: Robust closed-loop driving with open-loop training. _arXiv preprint arXiv:2503.12030_ , 2025. 6 

- [22] Bencheng Liao, Shaoyu Chen, Haoran Yin, Bo Jiang, Cheng Wang, Sixu Yan, Xinbang Zhang, Xiangyu Li, Ying Zhang, Qian Zhang, et al. Diffusiondrive: Truncated diffusion model 

24841 

for end-to-end autonomous driving. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 12037–12047, 2025. 6 

- [23] Henry X Liu and Shuo Feng. Curse of rarity for autonomous vehicles. _nature communications_ , 15(1):4808, 2024. 1 

- [24] Xueyi Liu, Zuodong Zhong, Yuxin Guo, Yun-Fu Liu, Zhiguo Su, Qichao Zhang, Junli Wang, Yinfeng Gao, Yupeng Zheng, Qiao Lin, et al. Reasonplan: Unified scene prediction and decision reasoning for closed-loop autonomous driving. _arXiv preprint arXiv:2505.20024_ , 2025. 2 

- [25] Yuechen Luo, Fang Li, Shaoqing Xu, Zhiyi Lai, Lei Yang, Qimao Chen, Ziang Luo, Zixun Xie, Shengyin Jiang, Jiaxin Liu, et al. Adathinkdrive: Adaptive thinking via reinforcement learning for autonomous driving. _arXiv preprint arXiv:2509.13769_ , 2025. 1, 2 

- [26] Ziang Luo, Kangan Qian, Jiahua Wang, Yuechen Luo, Jinyu Miao, Zheng Fu, Yunlong Wang, Sicong Jiang, Zilin Huang, Yifei Hu, et al. Mtrdrive: Memory-tool synergistic reasoning for robust autonomous driving in corner cases. _arXiv preprint arXiv:2509.20843_ , 2025. 2 

- [27] Lu Ma, Hao Liang, Meiyi Qiang, Lexiang Tang, Xiaochen Ma, Zhen Hao Wong, Junbo Niu, Chengyu Shen, Runming He, Yanhao Li, et al. Learning what reinforcement learning can’t: Interleaved online fine-tuning for hardest questions. _arXiv preprint arXiv:2506.07527_ , 2025. 2 

- [28] Ana-Maria Marcu, Long Chen, Jan H¨unermann, Alice Karnsund, Benoit Hanotte, Prajwal Chidananda, Saurabh Nair, Vijay Badrinarayanan, Alex Kendall, Jamie Shotton, et al. Lingoqa: Visual question answering for autonomous driving. In _European Conference on Computer Vision_ , pages 252–269. Springer, 2024. 2, 3, 1 

- [29] Tianwen Qian, Jingjing Chen, Linhai Zhuo, Yang Jiao, and Yu-Gang Jiang. Nuscenes-qa: A multi-modal visual question answering benchmark for autonomous driving scenario. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , pages 4542–4550, 2024. 3, 1 

- [30] Zhijie Qiao, Haowei Li, Zhong Cao, and Henry X Liu. Lightemma: Lightweight end-to-end multimodal model for autonomous driving. _arXiv preprint arXiv:2505.00284_ , 2025. 2 

- [31] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 2 

varez. Omnidrive: A holistic vision-language dataset for autonomous driving with counterfactual reasoning. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 22442–22452, 2025. 2, 3, 1 

   - [35] Shuo Xing, Chengyuan Qian, Yuping Wang, Hongyuan Hua, Kexin Tian, Yang Zhou, and Zhengzhong Tu. Openemma: Open-source multimodal model for end-to-end autonomous driving. In _Proceedings of the Winter Conference on Applications of Computer Vision_ , pages 1001–1009, 2025. 2 

   - [36] Zebin Xing, Xingyu Zhang, Yang Hu, Bo Jiang, Tong He, Qian Zhang, Xiaoxiao Long, and Wei Yin. Goalflow: Goaldriven flow matching for multimodal trajectories generation in end-to-end autonomous driving. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1602–1611, 2025. 6 

   - [37] Jianhao Yan, Yafu Li, Zican Hu, Zhi Wang, Ganqu Cui, Xiaoye Qu, Yu Cheng, and Yue Zhang. Learning to reason under off-policy guidance. _arXiv preprint arXiv:2504.14945_ , 2025. 2, 5 

   - [38] Wenhao Yao, Zhenxin Li, Shiyi Lan, Zi Wang, Xinglong Sun, Jose M Alvarez, and Zuxuan Wu. Drivesuprim: Towards precise trajectory selection for end-to-end planning. _arXiv preprint arXiv:2506.06659_ , 2025. 6 

   - [39] Xiaoying Zhang, Hao Sun, Yipeng Zhang, Kaituo Feng, Chaochao Lu, Chao Yang, and Helen Meng. Critique-grpo: Advancing llm reasoning with natural language and numerical feedback. _arXiv preprint arXiv:2506.03106_ , 2025. 2 

   - [40] Rui Zhao, Qirui Yuan, Jinyu Li, Haofeng Hu, Yun Li, Chengyuan Zheng, and Fei Gao. Sce2drivex: A generalized mllm framework for scene-to-drive learning. _arXiv preprint arXiv:2502.14917_ , 2025. 2 

   - [41] Zewei Zhou, Tianhui Cai, Seth Z Zhao, Yun Zhang, Zhiyu Huang, Bolei Zhou, and Jiaqi Ma. Autovla: A visionlanguage-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. _arXiv preprint arXiv:2506.13757_ , 2025. 1, 2, 6 

   - [42] Jinguo Zhu, Weiyun Wang, Zhe Chen, Zhaoyang Liu, Shenglong Ye, Lixin Gu, Hao Tian, Yuchen Duan, Weijie Su, Jie Shao, et al. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models. _arXiv preprint arXiv:2504.10479_ , 2025. 5, 2 

- [32] Chonghao Sima, Katrin Renz, Kashyap Chitta, Li Chen, Hanxue Zhang, Chengen Xie, Jens Beißwenger, Ping Luo, Andreas Geiger, and Hongyang Li. Drivelm: Driving with graph visual question answering. In _European conference on computer vision_ , pages 256–274. Springer, 2024. 3, 1 

- [33] Xiaoyu Tian, Junru Gu, Bailin Li, Yicheng Liu, Yang Wang, Zhiyong Zhao, Kun Zhan, Peng Jia, Xianpeng Lang, and Hang Zhao. Drivevlm: The convergence of autonomous driving and large vision-language models. _arXiv preprint arXiv:2402.12289_ , 2024. 2 

- [34] Shihao Wang, Zhiding Yu, Xiaohui Jiang, Shiyi Lan, Min Shi, Nadine Chang, Jan Kautz, Ying Li, and Jose M Al- 

24842 

