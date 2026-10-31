---
title: "AutoDrive-R²: Incentivizing Reasoning and Self-Reflection Capacity for VLA Model in Autonomous Driving"
date: "2026"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2509.01944
pdf: https://arxiv.org/pdf/2509.01944
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2509.01944)** / [論文ページ](https://arxiv.org/abs/2509.01944)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Published as a conference paper at ICLR 2026 

# AUTODRIVE-R²: INCENTIVIZING REASONING AND SELF-REFLECTION CAPACITY FOR VLA MODEL IN AUTONOMOUS DRIVING 

**Zhenlong Yuan**<sup>**1**</sup><sup>_∗†_</sup> **, Chengxuan Qian**<sup>**1**</sup><sup>_∗_</sup> **, Jing Tang**<sup>**1**</sup> **, Rui Chen**<sup>**1**</sup> **, Zijian Song**<sup>**2**</sup> **, Lei Sun**<sup>1</sup><sup>_‡_</sup> , **Xiangxiang Chu**<sup>1</sup> , **Yujun Cai**<sup>3</sup> , **Dapeng Zhang**<sup>4§</sup> , **Shuo Li**<sup>5</sup> 

1 AMAP, Alibaba Group, 2 Sun Yat-sen University, 3 University of Queensland, 

4 Lanzhou University, 5 Case Western Reserve University 

- _∗_ Equal contribution _‡_ Project Lead § Corresponding Author 

## ABSTRACT 

Vision–Language–Action (VLA) models in autonomous driving systems have recently demonstrated transformative potential by integrating multimodal perception with decision-making capabilities. However, the interpretability and coherence of the decision process and the plausibility of action sequences remain largely underexplored. To address these issues, we propose AutoDrive-R², a novel VLA framework that enhances both reasoning and self-reflection capabilities of autonomous driving systems through chain-of-thought (CoT) processing and reinforcement learning (RL). Specifically, we first propose an innovative CoT dataset named nuScenesR²-6K for supervised fine-tuning, which effectively builds cognitive bridges between input information and output trajectories through a four-step logical chain with self-reflection for validation. Moreover, to maximize both reasoning and self-reflection during the RL stage, we further employ the Group Relative Policy Optimization algorithm within a physics-grounded reward framework that incorporates spatial alignment, vehicle dynamic, and temporal smoothness criteria to ensure reliable and realistic trajectory planning. Extensive evaluation results across both nuScenes and Waymo datasets demonstrates the state-of-theart performance and robust generalization capacity of our method. 


> _†_ Work done during the internship at AMAP, Alibaba Group. 

1 

Published as a conference paper at ICLR 2026 

## 1 INTRODUCTION 

Autonomous driving technologies have witnessed rapid advancements in recent years. These systems typically take sensor data as input and then output planning trajectories. Traditional pipelines (Kendall et al., 2019; Chen et al., 2021) usually adopt architectures with separate perception, mapping, prediction, and planning modules. Such design may suffer from two key limitations: error accumulation and lack joint optimization across components, leading to performance degradation. In contrast, modern methods (Hu et al., 2023; Jiang et al., 2023; Chen et al., 2024) unify these complex systems into a single end-to-end paradigm, which naturally offers three main benefits: system simplification, enhanced robustness, and alleviated error accumulation. 

However, these end-to-end methods primarily focus on trajectory planning while lacking the contextual reasoning necessary for complex driving scenarios. To address this limitation, recent works integrate Vision-Language Models (VLMs) into autonomous driving systems, leveraging their pretrained reasoning capabilities to enhance decision-making in challenging situations (Shao et al., 2024a; Wang et al., 2023; Tian et al., 2024). Unlike traditional approaches that train perceptionpolicy modules from scratch, VLM-based methods instead fine-tune pre-trained models by leveraging pre-training on millions of image-text pairs, enhancing vehicles to interpret dynamic traffic situations and develop sophisticated navigation strategies. Despite promising results, current VLMbased systems still struggle with consistently producing accurate planning outputs. 

Building upon VLMs, Vision-Language-Action models (VLA) further extend reasoning capabilities to final action prediction, enabling robots and autonomous vehicles to generate precise actions from visual inputs and textual instructions (Yang et al., 2025). This advancement has led to the adoption of similar action generation mechanisms in autonomous driving, with approaches like _π_ 0 (Black et al., 2024) inspiring the development of action tokenizer that produce precise planning trajectories (Zhou et al., 2025b). 

However, current VLA approaches in autonomous driving typically face two critical limitations that hinder their practical deployment: First, existing trajectory generation framework often produce physically infeasible outputs. Existing approaches that directly generate textual commands or waypoints via VLMs frequently produce physically-infeasible outputs and exhibit model collapse. While intermediate representations like meta-actions or latent action tokens have been proposed to mitigate these issues, these designs violate the end-to-end optimization principle and significantly increase model complexity overhead. Second, current systems demonstrate inadequate reasoning capabilities for complex driving scenarios. Since most methods employ simplistic reasoning strategies, they fail to account for both complicated road condition and vehicle kinematic constraints, resulting predicted trajectories significantly deviate from real-world requirements. These limitations underscore the critical need for a novel VLA framework that balances architectural simplicity, robust contextual understanding, and strict physical constraints. 

To overcome these challenges, we propose AutoDrive-R², a novel VLA framework that enhances both reasoning quality and physical feasibility through a two-stage training approach. Our key insight is that effective autonomous driving requires structured reasoning processes that can be systematically validated and refined. Specifically, to address the inadequacy of contextual reasoning for complex driving scenarios, we first construct nuScenesR²-6K, a chain-of-thought (CoT) dataset for supervised fine-tuning (SFT). nuScenesR²-6K is the first dataset in autonomous driving that stimulates both reasoning and self-reflection capabilities for VLA models. Unlike prior datasets, nuScenesR²-6K provides not only ground-truth trajectories but also the underlying reasoning and self-reflection steps, ensuring both the correctness and causal plausibility of driving behavior. 

Furthermore, to resolve the challenge of physically infeasible trajectory generation, we further develop a physics-grounded reward framework tailored to group relative policy optimization (GRPO) of autonomous driving tasks. By explicitly incorporating spatial alignment, vehicle dynamic and temporal smoothness constraints into consideration, our physics-grounded reward enables reinforcement learning to adapt to diverse driving scenarios and vehicle dynamics while maintaining physical feasibility and motion comfort. Comprehensive experiments on nuScenes and Waymo benchmarks demonstrate that AutoDrive-R² achieves state-of-the-art performance. Our key contributions are: 

- We introduce AutoDrive-R², a novel VLA framework that enables semantic reasoning with selfreflection step and trajectory planning from visual information and language instructions. 

2 

Published as a conference paper at ICLR 2026 


Figure 1: Pipeline of our method. We adopt a two-stage training process. The first stage introduces an innovative CoT dataset named nuScenesR²-6K for SFT. The nuScenesR²-6K adopts a four-step logical chain with self-reflection to generate valuable chain-of-thought data. The second stage proposes an novel physics-grounded reward framework for RL optimization, which incorporates spatial alignment, vehicle dynamic, and temporal smoothness for reliable trajectory planning. 

- We propose nuScenesR<sup>2</sup> -6K, an innovative CoT dataset adopting a four-step logic chain with self-reflection to help build foundational perception capabilities after SFT. 

- We propose a RL-based post-training method based on GRPO, which incorporates physicsgrounded rewards as constraint to refine planning trajectory for diverse scenes. 

## 2 METHODOLOGY 

**Overview.** In this section, we present an overview of AutoDrive-R². The target of trajectory planning task requires the model to forecast a vehicle’s future motion based on its historical sensor data and contextual information. Formally, given a sequence of historical vehicle states _H_ (including position, acceleration, velocity, steering angle, etc.) and its camera image _F_ , the model _M_ outputs predicted bird’s-eye view (BEV) trajectory coordinates _T_ over the next 3 seconds at 0.5-second intervals, defined as _T_ = _M_ ( _H, F_ ). 

As depicted in Fig. 2, our training process contains two stages. In stage one, we construct a highquality dataset nuScenesR<sup>2</sup> -6K for cold start to build cognitive bridges between input information and output trajectories through a four-step logical chain with self-reflection for validation. In stage two, we employ a physics-based reinforcement learning framework that integrates spatial alignment, vehicle dynamic and temporal smoothness to ensure physically feasible trajectory generation. 

### 2.1 LOGISTIC COT DATASET WITH SELF-REFLECTION 

The success of VLA models in autonomous driving critically depends on their ability to produce both interpretable reasoning and physically feasible actions. However, existing training approaches often fail to establish this dual requirement, leading to models that either lack explainable decisionmaking processes or generate unrealistic trajectories. To investigate this challenge, we initially explored direct reinforcement learning optimization for trajectory planning, following recent advances in reasoning-based RL (Guo et al., 2025). However, preliminary experiments revealed that models trained exclusively on RL exhibited significant degradation in trajectory planning compared to models pre-trained with SFT before RL. Therefore, we constructed a high-quality cold-start dataset named nuScenesR²-6K to cultivate the model’s foundational understanding of trajectory planning. 

3 

Published as a conference paper at ICLR 2026 

To this end, we constructed nuScenesR²-6K, a dataset of 6,000 image-trajectory pairs enriched with high-fidelity chain-of-thought (CoT) reasoning. The dataset was created through a meticulous "generate-then-validate" pipeline. First, we curated an initial pool of approximately 8,000 imagetrajectory pairs from the nuScenes training set. We then leveraged the Qwen2.5-VL-72B model to synthesize initial CoT reasoning sequences for these pairs. Crucially, to ensure data quality, we employed the closed-source Qwen-VL-Max model as an expert validator to score and review each generated chain. Chains containing factual errors or logical inconsistencies were systematically discarded. This rigorous filtering process yielded the final 6,000 high-fidelity samples for SFT. 

Moreover, we observe that many existing approaches rely on universal prompts for problem-toanswer reasoning, lacking structured guidance for rational analysis. While this strategy proves effective for simple tasks, it frequently fails when confronted with complex mathematical or logical problems. To address this limitation, our CoT prompt design systematically decomposes trajectory planning into three interdependent reasoning stages: 

- Image-Driven Analysis: Establishing foundational scene understanding (e.g., obstacle and lane localization, traffic sign detection) to anchor subsequent reasoning. 

- Physics-based Calculation: Leveraging kinematic equations (e.g., angular momentum conservation) to translate abstract observations into quantifiable predictions. 

- Contextual Logic Synthesis: Integrating domain-specific knowledge (e.g., intersection traffic rules) to ensure predictions align with real-world driving regulations. 

To further enhance robustness and the correctness of answers, we explicitly introduce a selfreflection phase as the fourth step, inspired by mathematical reasoning frameworks that validate conclusions through backward-checking. This allows the model to verify the coherence of its reasoning and correct potential contradictions. Our prompt implements a four-step logic chain: 

### **Observation → Calculation → Logic → Reflection,** 

which delivers both systematic and error-resilient reasoning. Ultimately, the nuScenesR²-6K dataset is adopted for supervised fine-tuning Qwen2-VL-7B model, thus yielding our stage-1 model. 

### 2.2 GROUP RELATIVE POLICY OPTIMIZATION (GRPO) 

We follow the GRPO algorithm (Jiang et al., 2025) to train the model. Unlike traditional approaches that rely on critic networks to estimate value functions, GRPO introduces a pairwise comparison mechanism among candidate response. This design not only simplifies the architecture but also reduces computational overhead during training. The methodology begins by generating _G_ distinct candidate responses _o_ = _{o_ 1 _, . . . , oG}_ for a given input question _q_ through policy sampling. For our specific task, we implement two rule-based verifiable reward functions to assess response quality: 

**Accuracy Reward** To better adapt to trajectory planning task, we define a physics-grounded accuracy rewards _racc_ which integrates spatial, kinematic, and temporal constraints for evaluation. Details are specified in the following section. 

**Format Reward** The format reward _racc_ enforces strict adherence to the required output format. The model must produce responses in the form: _"<think>thinking process here</think><answer>(x_ 1 _, y_ 1 _), ...,(xn, yn)</answer>"_ . A value of 1 is assigned if the format is correct, otherwise 0. In summary, the total reward for a response _oi_ is calculated as: _ri_ = _r_ acc<sup>_i_+</sup><sup>_r_</sup> format<sup>_i._To quantify the relative quality of all responses</sup><sup>_{r_1</sup><sup>_, . . . , rG}_, GRPO normalizes these</sup> scores by subtracting the group mean and dividing by the standard deviation. Consequently, the advantage for each response can be formulated by: 


where _Ai_ is the relative advantage of the _i_ -th answer. Then the optimization objective further incorporates a regularization term to ensure the updated policy _πθ_ remains close to the original reference 

4 

Published as a conference paper at ICLR 2026 

policy _π_ ref. This is achieved by adding a KL-divergence term _D_ KL( _· ∥·_ ) to the loss function: 


where _β_ acts as a hyperparameter to trade-off between exploration and stability during optimization. 

### 2.3 PHYSICS-GROUNDED ACCURACY REWARDS IN GRPO 

In autonomous driving, traditional reward function designs often focus solely on trajectory position error, while neglecting the complex constraints in geometric, dynamical, and temporal dimensions. To address this issue, we propose a physics-grounded reward framework that integrates spatial alignment, vehicle dynamics, and temporal continuity to comprehensively guide the model in generating safe, feasible, and comfortable driving strategies. This multi-dimensional approach not only ensures geometric accuracy but also explicitly incorporates the physical limitations of real-world vehicles and the perceptual requirements for motion smoothness, creating a holistic optimization objective. 

**Spatial Alignment: Balancing Global Maneuverability.** The foundation of any trajectory reward function lies in its ability to align predicted paths with target routes. We define a spatial accuracy term _r_ pos as the mean squared Euclidean distance between predicted and ground-truth coordinates: 


where _N_ denotes the number of time steps, _x_<sup>_i_</sup> _, y_<sup>_i_</sup> represent predicted coordinates at the _i_ -th time step, while _x_<sup>_i_</sup> gt<sup>_, y_</sup> gt<sup>_i_correspond to the ground-truth values. This formulation prioritizes global path ad-</sup> herence by penalizing deviations across all time steps, ensuring the vehicle remains on the intended route. However, focusing only on minimizing position error may produce physical-implausible results. For instance, strictly following the shortest path might bring about abrupt steering or acceleration, which not only violate vehicle kinematics but also compromise passenger comfort. To balance geometric precision with practical feasibility, we introduce additional constraints derived from vehicle dynamics. 

**Vehicle Dynamics: Bridging Perception and Control.** Autonomous driving systems must respect the real-world physical limitations, which are governed by steering kinematics and longitudinal dynamics. Ignoring them may result in trajectories that are impossible to execute (e.g., requiring infinite torque for abrupt steering changes) or uncomfortable for passengers. To ensure kinematic feasibility, we penalize deviations in steering angles through the following term _r_ ste: 


where _θ_<sup>_j_</sup> and _θgt_<sup>_j_respectively denotes the predicted and corresponding ground-truth steering angle</sup> at _j_ -th time step. Additionally, we address unphysical acceleration/braking patterns by introducing an additional velocity constraint term: 


where _v_<sup>_k_</sup> and _vgt_<sup>_j_respectivelyrepresentsthepredictedandcorrespondingground-truthvelocityat</sup> the _k_ -th time step. In summary, both _r_ ste and _r_ vel enforce compliance with vehicle-specific constraints, ensuring generated trajectories are both physically realizable and socially acceptable in 

5 

Published as a conference paper at ICLR 2026 

Table 1: Trajectory L2 errors and collision rates on the nuScenes dataset. 

|**Method**|**L**|**2 Err**|**or (m**|**)**_↓_|**Colli**|**sion**|**Rate (**|**%)**_↓_|
|---|---|---|---|---|---|---|---|---|
||1s|2s|3s|Avg.|1s|2s|3s|Avg.|
|_Open-source Generalist_|_Vision_|_Lang_|_uage_|_Model_|_s_||||
|Llama-3.2-11B-Vision (Touvron et al.,2023)|1.54|3.31|3.91|2.92|-|-|-|-|
|DeepSeek-VL2-16B (Liu et al.,2025)|0.66|1.68|2.92|1.75|-|-|-|-|
|LLaMA-3.2-11B-Vision (Touvron et al.,2023)|0.52|1.42|2.68|1.54|-|-|-|-|
|Qwen-2.5-VL-3B (Bai et al.,2025)|2.69|4.16|5.78|4.21|0.32|0.54|0.78|0.55|
|Qwen-2.5-VL-7B (Bai et al.,2025)|0.46|1.33|2.55|1.45|0.10|0.18|0.24|0.17|
|_Training-based Driving Spe_|_cialis_|_ts (Ex_|_isting_|_Metho_|_ds)_||||
|UniAD (Hu et al.,2023)|0.42|0.64|0.91|0.66|0.62|0.58|0.63|0.61|
|VAD (Jiang et al.,2023)|0.17|0.34|0.60|0.37|0.07|0.17|0.41|0.22|
|BEV-Planner (Li et al.,2024)|0.16|0.32|0.57|0.35|0.00|0.29|0.73|0.34|
|Ego-MLP (Zhai et al.,2023)|0.15|0.32|0.59|0.35|-|-|-|-|
|_Ours and Key Competitors (S_|_pecia_|_lized_|_Drivin_|_g Mod_|_els)_||||
|DriveVLM (Tian et al.,2024)|0.18|0.34|0.68|0.40|0.10|0.22|0.45|0.27|
|OmniDrive (Wang et al.,2024)|0.14|0.29|0.55|0.33|0.00|0.13|0.78|0.30|
|DriveVLM-Dual (Tian et al.,2024)|0.15|0.29|0.48|0.31|0.05|0.08|0.17|0.10|
|EMMA (Hwang et al.,2024)|0.14|0.29|0.54|0.32|-|-|-|-|
|EMMA+ (Hwang et al.,2024)|0.13|0.27|0.48|0.29|-|-|-|-|
|<br>Imprompt-VLA|0.13|0.27|0.53|0.30|-|-|-|-|
|**AutoDrive-R² 3B**|0.35|0.49|0.62|0.49|0.13|0.44|0.87|0.48|
|**AutoDrive-R² 7B**|0.13|0.19|0.25|0.19|0.00|0.07|0.12|0.07|


mixed traffic scenarios. These constraints explicitly bridge the gap between perception-driven planning and actuator-level control, ensuring that predicted trajectories align with the physical boundaries while maintaining ride quality. 

**Temporal Smoothness: Ensuring Navigation Reliability** Temporal discontinuities in trajectory predictions fundamentally undermine the reliability of autonomous driving systems. When steering or acceleration commands exhibit sudden jumps between time steps, the predicted trajectories may lose coherence, which further compromises the system’s ability to maintain stable, predictable motion patterns required for safe navigation. To address this, we introduce a temporal smoothness term _r_ tem that penalizes rapid variations in consecutive control signals: 


Such design ensures temporal coherence of predicted trajectories. By explicitly constraining the rate of change in both steering and velocity, the reward function filters out unstable oscillations that could destabilize the vehicle’s state estimation. This regularization effect strengthens the model’s ability to generalize across diverse driving scenarios while maintaining safety margins during execution. 

**Integrated Reward Function.** The final reward synthesizes all dimensions with learnable weights: 


Here, _λ_ pos _, λ_ ste _, λ_ vel _, λ_ tem are learnable coefficients that balance trade-offs between competing objectives. We set them all equal one in experiments. This holistic formulation ensures the model generates trajectories that are geometrically accurate, dynamically feasible, and temporally smooth, addressing the multifaceted challenges of autonomous driving. 

6 

Published as a conference paper at ICLR 2026 

## 3 EXPERIMENT 

### 3.1 EXPERIMENTAL SETTINGS 

**Datasets.** For training, we adopt nuScenesR<sup>2</sup> -6K dataset, which contains 6k image-trajectory sample pairs, each includes a front-view image and a 3-second trajectory planning with 0.5-second intervals. The Qwen2.5-VL-7B model is fine-tuned on these samples for SFT to establish foundational perception capabilities before RL. For evaluation, our method is tested on nuScenes and Waymo datasets, both offering comprehensive autonomous driving data. The nuScenes dataset contains 1,000 urban driving scenes with six synchronized camera views to support planning tasks. Waymo dataset includes 4,021 driving segments, capturing eight camera views and ego-vehicle trajectories. 

**Details.** We implement experiments on both Qwen2.5-VL-3B and Qwen2.5-VL-7B models. In both stages, the learning rate is set to 5e-7 with an accumulated total batch size of 8. The GRPO is configured with a maximum completion length of 4,096 tokens and samples 6 responses per input. For training, the reinforcement learning (RL) pipeline utilized the TRL framework, and was executed for a total of 750 training iterations and 1 epoch for 18 hours. 

**Evaluation Metrics.** We evaluate performance using both accuracy and safety metrics. For accuracy, we adopt the L2 distance (in meters) between the predicted and ground truth trajectories at 1s, 2s, and 3s, along with the average error. To assess safety, we also report the Collision Rate (%), which measures the frequency of collisions in the predicted paths. For all models, we utilize the official checkpoints and conduct evaluations under the same evaluation codes to ensure fairness. Note that the <mark>best</mark> and <mark>second-best</mark> results are highlighted in all tables. 

### 3.2 EVALUATION RESULTS 

**Results on nuScenes Datasets** Table 1 compares the prediction errors among our method and existing approaches on the nuScenes dataset. Notably, our approach consistently achieves the best performance across all time intervals, surpassing current leading methods such as EMMA+, which are trained on substantially larger internal datasets with 103k scenarios. In contrast, our training data consists of only 6k curated CoT samples for stage 1 and another 6k for stage 2, approximately 11.65% the size of EMMA+’s dataset. Furthermore, our model demonstrates significant improvements over Qwen2-VL-7B, reducing L2 errors by 86.9%, despite having less parameter. 

**Zero-shot performance on Waymo Datasets** Moreover, Tab. 2 demonstrates the robust zeroshot capabilities of our model. Specifically, our method respectively reduces L2 errors by 33.3% and 90.7% compared to the latest EMMA+ method and Qwen2-VL-72B baseline models. Overall, our model consistently delivers precise trajectory predictions across multiple datasets, establishing its state-of-the-art performance and generalization capability. 

Table 2: Trajectory L2 errors on Waymo. 

|**Method**||**L2 E**|**rror (**|**m)**_↓_|
|---|---|---|---|---|
||1s|2s|3s|Avg.|
|_Generalist VLMs_|_+ Spec_|_ialize_|_d Drivi_|_ng Models_|
|Qwen-2.5-VL-3B|2.98|5.05|7.38|5.14|
|Qwen-2.5-VL-7B|1.66|1.82|2.92|2.13|
|DriveVLM|0.17|0.34|0.75|0.42|
|EMMA|0.12|0.28|0.61|0.34|
|EMMA+|0.11|0.25|0.53|0.30|
|**AutoDrive-R² 3B**|0.23|0.36|0.51|0.37|
|**AutoDrive-R² 7B**|0.11|0.19|0.29|0.20|


**Model Size** In Tab. 1 and Tab. 2, we compare 3B EMMA+ <mark>0.11 0.25</mark> 0.53 <mark>0.30</mark> and 7B variants of Qwen2.5-VL within our two- **AutoDrive-R² 3B** 0.23 0.36 <mark>0.51</mark> 0.37 stage training framework to analyze impact of dif- **AutoDrive-R² 7B** <mark>0.11 0.19 0.29 0.20</mark> ferent model size. While the 7B model achieves superior performance with an average L2 error of 0.19m, the 3B version demonstrates a notable improvement than its baseline. The disparity highlights that larger models inherently capture more complex patterns, but the two-stage framework (SFT + GRPO) effectively compensates for the 3B model’s limited capacity by enforcing strict trajectory constraints and contextual logic synthesis. 

**Closed-loop Experiment** To evaluate our model’s practical decision-making, we conducted closedloop experiments on the NAVSIM benchmark. As detailed in Table 3, our method sets a new state-ofthe-art by outperforming all prior approaches across every metric. Specifically, our model achieves top scores in safety, with a Navigation Completion of 98.3 and Time-to-Collision of 95.6, while also excelling in driving quality by leading in Driving Agent Comfort (94.4) and Ego-Progress (81.6). 

7 

Published as a conference paper at ICLR 2026 


Figure 2: Qualitative comparison of trajectory planning performance across Qwen2.5-VL-7B, EMMA+, and our AutoDrive-R² on the nuScenes dataset. Note that blue lines denote predicted trajectories while green lines represent ground truth trajectories. 

The most significant advantage is observed in the Planner-Diverse Motion Score (PDMS), where our score of 90.3 surpasses the next-best competitor by over 6 points, showcasing superior humanlike planning. These comprehensive results confirm our model’s ability to translate its predictive accuracy into robust, safe, and efficient real-world driving actions. 

Table 3: Performance on the Closed-loop NAVSIM. 

|**Methods**|NC_↑_|DAC_↑_|TTC_↑_|Comfort_↑_|EP_↑_|PDMS_↑_|
|---|---|---|---|---|---|---|
|TransFuser (Chitta et al.,2022)|97.7|92.8|92.8|100|79.2|84.1|
|UniAD (Hu et al.,2023)|97.8|91.9|92.9|100|78.8|83.4|
|Para-Drive (Weng et al.,2024b)|97.9|92.4|93.0|99.8|79.3|84.0|
|**AutoDrive-R² 7B**|98.5|95.9|95.4|100|82.7|89.1|


**Visualization** In Fig. 2, we present a comparative analysis of our method against other approaches in the nuScenes dataset. Notably, Qwen2.5-VL-7B fails to generate accurate predictions in specific scenarios (e.g., (b) and (d)), whereas EMMA+ exhibits significant trajectory deviation. In contrast, our method consistently achieves more reliable and physically feasible trajectory planning under varying illumination environments and complex motion patterns. 

8 

Published as a conference paper at ICLR 2026 

### 3.3 ABLATION STUDIES 

**Training Stages** Drawing inspiration from DeepSeek-R1-Zero, we first attempt to train the model solely through RL. As shown in Tab. 4, the model purely trained on RL (7B + _RL_ ) underperforms that of SFT (7B + _SFT_ ) by 22.2% in average L2 error. We attribute this to model’s inability to establish structured reasoning chains, as RL struggles to explore the high-dimensional reasoning space required for multi-step calculations and contextual logic synthesis. This observation validates the necessity of our two-stage training. 

**Supervised Fine-tuning (** **_SFT_ )** In the first stage, the baseline Qwen2.5-VL-7B (7B) achieves an average L2 error of 1.45m, whereas the SFT model (7B + _SFT_ ) trained on the nuScenesR²-6K dataset reduces this to 0.27m, demonstrating an 81.4% improvement. This significant enhancement highlights the effectiveness of adopting SFT training in 

Table 4: Ablation studies of trajectory L2 errors on nuScenes dataset for validation. 

|**Method**|**L**|**2 Err**|**or (m**|**)**_↓_|
|---|---|---|---|---|
||1s|2s|3s|Avg.|
|Qwen2.5-VL-7B|0.46|1.33|2.55|1.45|
|Qwen2.5-VL-7B +_SFT_|0.17|0.27|0.36|0.27|
|Qwen2.5-VL-7B +_RL_|0.21|0.33|0.44|0.33|
|_SFT :_w/o. Four.|0.19|0.25|0.32|0.25|
|_SFT :_w/o. Self.|0.17|0.23|0.29|0.23|
|_RL :_w/o. _r_pos|0.32|0.53|0.72|0.53|
|_RL :_w/o. _r_ste|0.14|0.20|0.27|0.21|
|_RL :_w/o. _r_vel|0.15|0.21|0.29|0.22|
|_RL :_w/o. _r_tem|0.15|0.23|0.34|0.24|
|**AutoDrive-R² 7B**|0.13|0.19|0.25|0.19|


establishing foundational reasoning capabilities. Moreover, removing four-step reasoning structure (w/o. Four.) increases the error to 0.25m, indicating a 31.5% degradation compared to AutoDriveR². Similarly, eliminating self-reflection (w/o. Self.) results in 0.23m error, representing a 21.1% decline relative to AutoDrive-R². This emphasizes the interdependence of both four-step logical chain and self-reflection mechanism in constructing high-quality CoT dataset. 

**Reinforcement Learning (** **_RL_ )** In the second stage, we evaluate the contribution of individual reward components within the physics-grounded framework of AutoDrive-R². Specifically, spatial alignment is critical for maintaining global geometric path accuracy, as its removal (w/o. _r_ pos) increases the error to 0.53m, much higher than the full model. Moreover, steering angle regulation ensures kinematic feasibility by penalizing abrupt changes in steering adjustments, and its absence (w/o. _r_ ste) leads to a 10.5% degradation (0.21m). Additionally, velocity consistency constraints ensure adherence to target speed profiles by penalizing deviations in predicted velocity from groundtruth values, and their exclusion (w/o. _r_ vel) raises the error to 0.22m. Finally, temporal smoothness penalties suppress unstable control patterns by penalizing abrupt changes in steering and velocity across time steps, and their removal (w/o. _r_ tem) results in a 26.3% increase in error (0.24m). By integrating all four components into our physics-grounded reward, AutoDrive-R² achieves an optimal 0.19m L2 error, confirming the necessity of each element in achieving reliable trajectory planning. 

**Key Hyperparameters** In Tab. 5, We conduct a series of ablation studies to analyze the impact of key hyperparameters. First, for the reward weights ( _λ_ ), we find that uniform weights ( _λ_ = (1 _,_ 1 _,_ 1 _,_ 1)) achieve a lower average L2 error (0.19 m) compared to decaying weights (0.22 m). This indicates that all reward components are equally important for the learning process, leading us to adopt the uniform setting. Next, we analyze the KL-divergence coefficient _β_ . A value of _β_ = 0 _._ 04 achieves the best performance with a 0.19 m error. A smaller value ( _β_ = 0 _._ 02) results in a higher error (0.21 m), while a larger value ( _β_ = 0 _._ 06) also slightly degrades performance (0.20 m), likely by overly constraining the optimization. Finally, for the number of generations ( _G_ ), we observe performance improving as _G_ increases from 2 (0.23 m) to 6 (0.19 m). However, increasing _G_ further to 8 yields no additional benefit. Therefore, we set _G_ = 6 to balance performance and computation. 

Table 5: Ablations on key hyperparameters. 

|**Setting**|**L**|**2 Err**|**or (m)**|_↓_|
|---|---|---|---|---|
||1s|2s|3s|Avg.|
|_Reward_|_Weight_|_s (λ)_|||
|_λ_: (0_._4_,_0_._3_,_0_._2_,_0_._1)|0.15|0.22|0.29|0.22|
|<br>_λ_: (1_,_1_,_1_,_1)**(Ours)**|0.13|0.19|0.25|0.19|
|_KL-diverg_|_ence B_|_eta (β)_|||
|_β_ = 0_._02|0.14|0.21|0.27|0.21|
|_β_ = 0_._04**(Ours)**|0.13|0.19|0.25|0.19|
|_β_ = 0_._06|0.13|0.20|0.26|0.20|
|_Number of G_|_enerat_|_ions (_|_G)_||
|_G_= 2|0.16|0.23|0.31|0.23|
|_G_= 4|0.14|0.20|0.26|0.20|
|_G_= 6**(Ours)**|0.13|0.19|0.25|0.19|
|_G_= 8|0.13|0.19|0.25|0.19|


9 

Published as a conference paper at ICLR 2026 

## 4 RELATED WORK (EXTENDED VER. IN APPX. B) 

**Autonomous Driving** The evolution of autonomous driving systems has transitioned from modular architectures to end-to-end learning paradigms. Early works like UniAD (Hu et al., 2023) pioneered the integration of sub-tasks into a unified framework. Concurrently, other methods addressed core challenges in prediction and efficiency; for example, Flash (Antonello et al., 2022) focused on creating fast models for real-time application, while DiPA (Knittel et al., 2023) tackled the complex, multi-modal nature of agent interactions. These works highlighted the need for a holistic evaluation beyond simple L2 error, inspiring our new analyses on collision rate and closed-loop performance. Subsequent methods like Para-Drive (Weng et al., 2024a) and BEV-Planner (Li et al., 2024) continued to refine these integrated approaches. 

The advent of vision-language models (VLMs) has further transformed the field. DriveVLM (Tian et al., 2024) and DriveMLM (Wang et al., 2023) enabled systems to incorporate linguistic reasoning for decision-making and rationale generation. Alongside performance, explainability has become a critical concern. A systematic review in (Kuznietsov et al., 2024) provides a comprehensive overview of techniques for building trustworthy systems, while works like Interpretable Goal-based Prediction and Planning (Albrecht et al., 2021) explored generating explanations by making the model’s goals explicit. In contrast to these post-hoc or explicit-goal methods, our AutoDrive-R² introduces a novel form of _intrinsic_ explainability, representing a significant step towards inherently trustworthy AI for autonomous driving. 

**General VLMs** The development of general vision-language models (VLMs) has been driven by the success of large language models (LLMs) in understanding textual data. CLIP (Radford et al., 2021) established a foundational approach by aligning image and text features through contrastive learning, enabling zero-shot generalization. Building on this, BLIP (Li et al., 2022) and its successor BLIP2 (Li et al., 2023) refined multimodal alignment using contrastive and matching losses to improve contextual grounding. More recent models, such as LLaVA (Liu et al., 2023) and Qwen2.5VL (Bai et al., 2025), have integrated robust LLMs with vision encoders to enhance representation capabilities. The OmniGen2 (Wu et al., 2025) framework further advanced this by introducing dual decoding pathways for text and image generation, while DeepSeek-V3 (Liu et al., 2025) demonstrated efficient inference through a Mixture-of-Experts (MoE) architecture with auxiliary-loss-free load balancing. These advancements highlight the growing synergy between vision and language modalities in multimodal learning. 

**Reinforcement Learning for Post-Training** Reinforcement learning (RL) has emerged as a critical tool for refining model capabilities post-training. Techniques like Proximal Policy Optimization (PPO) (Schulman et al., 2017) have been instrumental in fine-tuning models for complex tasks, as seen in the optimization of GPT (Achiam et al., 2024). Direct Preference Optimization (DPO) (Rafailov et al., 2023) introduces a sampling-free parameterization for reward models, streamlining the fine-tuning process. Reward Fine-Tuning (RFT) (Yuan et al., 2023) has shown particular efficacy in mathematical reasoning, while Guided Reward Policy Optimization (GRPO) (Shao et al., 2024b) enables robust reasoning improvements without external toolkits. The DeepSeek-R1 (Guo et al., 2025) model exemplifies the application of GRPO, achieving state-ofthe-art results through physics-informed reward design. These methodologies underscore the importance of RL in aligning model outputs with real-world constraints and user preferences. 

## 5 CONCLUSION 

In this work, we propose AutoDrive-R², a novel VLA framework designed for reasoning-guided trajectory planning in autonomous driving. AutoDrive-R² effectively balances semantic understanding with real-world constraints through a two-stage training framework: (1) a SFT stage adopting the nuScenesR²-6K dataset, which employs a four-step CoT process to cultivate structured reasoning and self-reflection for validation, and (2) a RL stage leveraging GRPO training to refine trajectory planning under physics-grounded rewards. Experiments validate the effectiveness of AutoDrive-R², achieving SOTA performance on nuScenes (34.5% reduction vs. EMMA+) and Waymo (90.7% reduction vs. Qwen2.5-VL-7B), demonstrating strong zero-shot generalization. Future efforts will focus on multi-agent coordination and real-time sensor fusion integration to further improve adaptability in complicated environments. 

10 

Published as a conference paper at ICLR 2026 

## ETHICS STATEMENT 

Our research builds upon publicly available autonomous driving datasets, including nuScenes and Waymo, to construct the nuScenesR²-6K dataset. The manual annotation process focuses exclusively on labeling contextual reasoning chains and trajectory planning scenarios, ensuring no personally identifiable information (PII) is collected or inferred. The dataset is fully anonymized, emphasizing high-level environmental and traffic dynamics while safeguarding individual privacy. We advocate for the responsible application of AutoDrive-R², urging stakeholders to prioritize safety, fairness, and transparency in deployment. Specifically, we caution against misuse in surveillance or discriminatory decision-making, particularly in scenarios where autonomous systems could disproportionately impact vulnerable populations. All experiments adhere to rigorous academic standards, with a commitment to open science: we publicly share our dataset, code, and training protocols to enable independent verification, ethical scrutiny, and collaborative refinement. By fostering transparency and community engagement, we aim to ensure that advancements in autonomous driving align with societal values and regulatory frameworks. 

## REPRODUCIBILITY STATEMENT 

To ensure the full reproducibility of our findings, we have provided detailed implementation and methodological descriptions throughout the paper. The construction of the nuScenesR²-6K dataset, including its 6,000 manually annotated image-trajectory pairs and statistical properties, is described in Sec. 2.1 and Appendix D. The AutoDrive-R² framework, with its four-step reasoning process (Observation → Calculation → Logic → Reflection) and self-reflection validation mechanism, is thoroughly outlined in Sec. 2.2, where we also provide the structured input prompts used to generate chain-of-thought (CoT) data. Key components of the Group Relative Policy Optimization (GRPO) training algorithm, including the physics-grounded reward function, spatial alignment, vehicle dynamics, and temporal smoothness criteria, are detailed in Sec. 2.3 and Appendix C. To further facilitate replication, we will publicly release the nuScenesR²-6K dataset, pre-trained model checkpoints, and training code upon acceptance, adhering to open scientific principles. Additionally, all hyperparameters, evaluation protocols, and ablation study configurations are explicitly documented in Appendix A, ensuring transparent and rigorous experimental validation. 

11 

Published as a conference paper at ICLR 2026 

## REFERENCES 

- Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, and et al. Gpt-4 technical report, 2024. URL https://arxiv.org/abs/2303.08774. 

- Stefano V Albrecht, Cillian Brewitt, John Wilhelm, Balint Gyevnar, Francisco Eiras, Mihai Dobre, and Subramanian Ramamoorthy. Interpretable goal-based prediction and planning for autonomous driving. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 1043–1049. IEEE, 2021. 

- Morris Antonello, Mihai Dobre, Stefano V Albrecht, John Redford, and Subramanian Ramamoorthy. Flash: Fast and light motion prediction for autonomous driving with bayesian inverse planning and learned motion profiles. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 9829–9836. IEEE, 2022. 

- Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang, Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A visionlanguage-action flow model for general robot control, 2024. URL https://arxiv.org/ abs/2410.24164. 

- Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners, 2020. URL https://arxiv.org/abs/2005.14165. 

- Long Chen, Lukas Platinsky, Stefanie Speichert, Bła˙zej Osi´nski, Oliver Scheel, Yawei Ye, Hugo Grimmett, Luca Del Pero, and Peter Ondruska. What data do we need for training an av motion planner? In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 1066– 1072. IEEE, 2021. 

- Rui Chen, Lei Sun, Jing Tang, Geng Li, and Xiangxiang Chu. Finger: Content aware fine-grained evaluation with reasoning for ai-generated videos. _arXiv preprint arXiv:2504.10358_ , 2025. 

- Shaoyu Chen, Bo Jiang, Hao Gao, Bencheng Liao, Qing Xu, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. Vadv2: End-to-end vectorized autonomous driving via probabilistic planning, 2024. URL https://arxiv.org/abs/2402.13243. 

- Kashyap Chitta, Aditya Prakash, Bernhard Jaeger, Zehao Yu, Katrin Renz, and Andreas Geiger. Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. _IEEE transactions on pattern analysis and machine intelligence_ , 45(11):12878–12895, 2022. 

- Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, and et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning, 2025. URL https://arxiv.org/abs/2501.12948. 

- Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, Lewei Lu, Xiaosong Jia, Qiang Liu, Jifeng Dai, Yu Qiao, and Hongyang Li. Planning-oriented autonomous driving. In _2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 17853–17862, 2023. doi: 10.1109/CVPR52729.2023. 01712. 

12 

Published as a conference paper at ICLR 2026 

- Zhijian Huang, Chengjian Fen, Feng Yan, Baihui Xiao, Zequn Jie, Yujie Zhong, Xiaodan Liang, and Lin Ma. Drivemm: All-in-one large multimodal model for autonomous driving. _arXiv preprint arXiv:2412.07689_ , 2024. 

- Jyh-Jing Hwang, Runsheng Xu, Hubert Lin, Wei-Chih Hung, Jingwei Ji, Kristy Choi, Di Huang, Tong He, Paul Covington, Benjamin Sapp, et al. Emma: End-to-end multimodal model for autonomous driving. _arXiv preprint arXiv:2410.23262_ , 2024. 

- Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. In _2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ , pp. 8306–8316, 2023. doi: 10.1109/ICCV51070.2023.00766. 

- Bo Jiang, Shaoyu Chen, Qian Zhang, Wenyu Liu, and Xinggang Wang. Alphadrive: Unleashing the power of vlms in autonomous driving via reinforcement learning and reasoning, 2025. URL https://arxiv.org/abs/2503.07608. 

- Alex Kendall, Jeffrey Hawke, David Janz, Przemyslaw Mazur, Daniele Reda, John-Mark Allen, Vinh-Dieu Lam, Alex Bewley, and Amar Shah. Learning to drive in a day. In _2019 International Conference on Robotics and Automation (ICRA)_ , pp. 8248–8254. IEEE, 2019. 

- Anthony Knittel, Majd Hawasly, Stefano V Albrecht, John Redford, and Subramanian Ramamoorthy. Dipa: probabilistic multi-modal interactive prediction for autonomous driving. _IEEE Robotics and Automation Letters_ , 8(8):4887–4894, 2023. 

- Anton Kuznietsov, Balint Gyevnar, Cheng Wang, Steven Peters, and Stefano V Albrecht. Explainable ai for safe and trustworthy autonomous driving: A systematic review. _IEEE Transactions on Intelligent Transportation Systems_ , 2024. 

- Nathan Lambert. Reinforcement learning from human feedback, 2025. URL https://arxiv. org/abs/2504.12501. 

- Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. BLIP: Bootstrapping language-image pre-training for unified vision-language understanding and generation. In Kamalika Chaudhuri, Stefanie Jegelka, Le Song, Csaba Szepesvari, Gang Niu, and Sivan Sabato (eds.), _Proceedings of the 39th International Conference on Machine Learning_ , volume 162 of _Proceedings of Machine Learning Research_ , pp. 12888–12900. PMLR, 17–23 Jul 2022. URL https: //proceedings.mlr.press/v162/li22n.html. 

- Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. BLIP-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara Engelhardt, Sivan Sabato, and Jonathan Scarlett (eds.), _Proceedings of the 40th International Conference on Machine Learning_ , volume 202 of _Proceedings of Machine Learning Research_ , pp. 19730–19742. PMLR, 23–29 Jul 2023. URL https://proceedings.mlr.press/v202/li23q.html. 

- Zhiqi Li, Zhiding Yu, Shiyi Lan, Jiahan Li, Jan Kautz, Tong Lu, and Jose M. Alvarez. Is ego status all you need for open-loop end-to-end autonomous driving? In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 14864–14873, June 2024. 

- Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, and et al. Deepseek-v3 technical report, 2025. URL https: //arxiv.org/abs/2412.19437. 

- Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. In _NeurIPS_ , 2023. 

- Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. Learning transferable visual models from natural language supervision, 2021. URL https://arxiv.org/abs/2103.00020. 

13 

Published as a conference paper at ICLR 2026 

- Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea Finn. Direct preference optimization: Your language model is secretly a reward model. _Advances in Neural Information Processing Systems_ , 36:53728–53741, 2023. 

- John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms, 2017. URL https://arxiv.org/abs/1707.06347. 

- Hao Shao, Yuxuan Hu, Letian Wang, Guanglu Song, Steven L. Waslander, Yu Liu, and Hongsheng Li. Lmdrive: Closed-loop end-to-end driving with large language models. In _2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 15120–15130, 2024a. doi: 10.1109/CVPR52733.2024.01432. 

- Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Y Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024b. 

- Wenchao Sun, Xuewu Lin, Yining Shi, Chuang Zhang, Haoran Wu, and Sifa Zheng. Sparsedrive: End-to-end autonomous driving via sparse scene representation, 2024. URL https://arxiv. org/abs/2405.19620. 

- Xiaoyu Tian, Junru Gu, Bailin Li, Yicheng Liu, Yang Wang, Zhiyong Zhao, Kun Zhan, Peng Jia, Xianpeng Lang, and Hang Zhao. Drivevlm: The convergence of autonomous driving and large vision-language models, 2024. URL https://arxiv.org/abs/2402.12289. 

- Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, Aurelien Rodriguez, Armand Joulin, Edouard Grave, and Guillaume Lample. Llama: Open and efficient foundation language models, 2023. URL https://arxiv.org/abs/2302.13971. 

- Shihao Wang, Zhiding Yu, Xiaohui Jiang, Shiyi Lan, Min Shi, Nadine Chang, Jan Kautz, Ying Li, and Jose M Alvarez. Omnidrive: A holistic llm-agent framework for autonomous driving with 3d perception, reasoning and planning. _CoRR_ , 2024. 

- Wenhai Wang, Jiangwei Xie, ChuanYang Hu, Haoming Zou, Jianan Fan, Wenwen Tong, Yang Wen, Silei Wu, Hanming Deng, Zhiqi Li, Hao Tian, Lewei Lu, Xizhou Zhu, Xiaogang Wang, Yu Qiao, and Jifeng Dai. Drivemlm: Aligning multi-modal large language models with behavioral planning states for autonomous driving, 2023. URL https://arxiv.org/abs/2312.09245. 

- Xinshuo Weng, Boris Ivanovic, Yan Wang, Yue Wang, and Marco Pavone. Para-drive: Parallelized architecture for real-time autonomous driving. In _2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 15449–15458, 2024a. doi: 10.1109/CVPR52733.2024. 01463. 

- Xinshuo Weng, Boris Ivanovic, Yan Wang, Yue Wang, and Marco Pavone. Para-drive: Parallelized architecture for real-time autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 15449–15458, 2024b. 

- Chenyuan Wu, Pengfei Zheng, Ruiran Yan, Shitao Xiao, Xin Luo, Yueze Wang, Wanli Li, Xiyan Jiang, Yexin Liu, Junjie Zhou, Ze Liu, Ziyi Xia, Chaofan Li, Haoge Deng, Jiahao Wang, Kun Luo, Bo Zhang, Defu Lian, Xinlong Wang, Zhongyuan Wang, Tiejun Huang, and Zheng Liu. Omnigen2: Exploration to advanced multimodal generation, 2025. URL https://arxiv. org/abs/2506.18871. 

- Zhenhua Xu, Yujia Zhang, Enze Xie, Zhen Zhao, Yong Guo, Kwan-Yee K Wong, Zhenguo Li, and Hengshuang Zhao. Drivegpt4: Interpretable end-to-end autonomous driving via large language model. _IEEE Robotics and Automation Letters_ , 2024. 

- Zhenjie Yang, Yilin Chai, Xiaosong Jia, Qifeng Li, Yuqian Shao, Xuekai Zhu, Haisheng Su, and Junchi Yan. Drivemoe: Mixture-of-experts for vision-language-action model in end-to-end autonomous driving, 2025. URL https://arxiv.org/abs/2505.16278. 

14 

Published as a conference paper at ICLR 2026 

- Tengju Ye, Wei Jing, Chunyong Hu, Shikun Huang, Lingping Gao, Fangzhen Li, Jingke Wang, Ke Guo, Wencong Xiao, Weibo Mao, Hang Zheng, Kun Li, Junbo Chen, and Kaicheng Yu. Fusionad: Multi-modality fusion for prediction and planning tasks of autonomous driving, 2023. URL https://arxiv.org/abs/2308.01006. 

- Gokul Yenduri, Ramalingam M, Chemmalar Selvi G, Supriya Y, Gautam Srivastava, Praveen Kumar Reddy Maddikunta, Deepti Raj G, Rutvij H Jhaveri, Prabadevi B, Weizheng Wang, Athanasios V. Vasilakos, and Thippa Reddy Gadekallu. Generative pre-trained transformer: A comprehensive review on enabling technologies, potential applications, emerging challenges, and future directions, 2023. URL https://arxiv.org/abs/2305.10435. 

- Zheng Yuan, Hongyi Yuan, Chengpeng Li, Guanting Dong, Keming Lu, Chuanqi Tan, Chang Zhou, and Jingren Zhou. Scaling relationship on learning mathematical reasoning with large language models, 2023. URL https://arxiv.org/abs/2308.01825. 

- Jiang-Tian Zhai, Ze Feng, Jinhao Du, Yongqiang Mao, Jiang-Jiang Liu, Zichang Tan, Yifu Zhang, Xiaoqing Ye, and Jingdong Wang. Rethinking the open-loop evaluation of end-to-end autonomous driving in nuscenes, 2023. URL https://arxiv.org/abs/2305.10430. 

- Xingcheng Zhou, Xuyuan Han, Feng Yang, Yunpu Ma, and Alois C. Knoll. Opendrivevla: Towards end-to-end autonomous driving with large vision language action model, 2025a. URL https: //arxiv.org/abs/2503.23463. 

- Zewei Zhou, Tianhui Cai, Seth Z. Zhao, Yun Zhang, Zhiyu Huang, Bolei Zhou, and Jiaqi Ma. Autovla: A vision-language-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning, 2025b. URL https://arxiv.org/abs/2506.13757. 

- Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and Mohamed Elhoseiny. Minigpt-4: Enhancing vision-language understanding with advanced large language models. _arXiv preprint arXiv:2304.10592_ , 2023. 

15 

Published as a conference paper at ICLR 2026 

## APPENDIX 

In this appendix, we provide more details, related work, tool library, and discussions for a comprehensive evaluation and understanding of our method. Detailed contents are as follows: 

|**A**|**Experiment**|**16**|
|---|---|---|
|A|.1<br>More Hyperparameter Configurations . . . . . . . . . . . . . . . .|. . . . . . . . .<br>16|
|A|.2<br>More Visualization Results<br>. . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>16|
|A|.3<br>"Aha Moment" . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>16|
|**B**|**Related Work**|**18**|
|B|.1<br>Autonomous Driving<br>. . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>18|
|B|.2<br>General VLMs . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>18|
|B|.3<br>Reinforcement Learning for Post-Training<br>. . . . . . . . . . . . .|. . . . . . . . .<br>19|
|**C**|**Vehicle Kinematics in Physics-Grounded Rewards**|**19**|
|**D**|**Detailed Prompts to Generate CoT Data**|**20**|
|**E**|**LLM clarification**|**21**|


## A EXPERIMENT 

### A.1 MORE HYPERPARAMETER CONFIGURATIONS 

Our method is implemented on a machine with an Intel(R) Xeon(R) Platinum 8480+ and eight 8 NVIDIA H20 GPUs with 90G memory. The training process ran for 750 epochs without freezing the vision transformer (ViT) backbone, and the number of generation is set to 6 in GRPO algorithm. 

### A.2 MORE VISUALIZATION RESULTS 

**Fig. 3** provides additional visualization results in trajectory planning tasks between our AutoDriveR² and other methods on the nuScenes dataset. Notably, our method consistently outperforms other approaches in predicting both reliable and physically-feasible trajectories, demonstrating the stateof-the-art performance of our proposed method. 

To further illustrate the advantages of our structured reasoning process, we present two representative comparisons in **Fig. 6 and Fig. 7** . These visualizations explicitly contrast the four-stage CoT reasoning (AutoDrive-R²) with the single-step reasoning of Qwen2.5-VL-7B. As can be seen, the Qwen2.5-VL model predicts a trajectory that deviates from the lane marking due to its simplified reasoning approach. The model’s single-stage analysis fails to account for the vehicle’s kinematic constraints and results in an unrealistic leftward drift. In contrast, AutoDrive-R²’s four-stage process systematically validates its predictions. These examples demonstrate how our structured CoT framework enables systematic error detection and correction, resulting in trajectories that are both geometrically accurate and physically feasible. The integration of physics-grounded rewards in the GRPO stage further ensures these corrections align with real-world driving constraints. 

### A.3 "AHA MOMENT" 

A compelling insight observed during the development of AutoDrive-R² is the emergence of a **“reasoning self-correction moment”** , where the model systematically identifies and resolves contradictions in its initial trajectory planning. 

This reasoning self-correction moment demonstrates AutoDrive-R²’s ability to re-examine its own assumptions and refine predictions through structured self-validation. As shown in **Fig. 5** , similar 

16 

Published as a conference paper at ICLR 2026 


Figure 3: Qualitative comparison of trajectory planning performance across Qwen2.5-VL-7B, EMMA+, and our AutoDrive-R² on the nuScenes dataset. Note that blue lines denote predicted trajectories while green lines represent ground truth trajectories. 


Figure 4: "Aha Moment" of our AutoDrive-R² on the nuScenes dataset. 


Figure 5: "Aha Moment" of our AutoDrive-R² on the nuScenes dataset. 

17 

Published as a conference paper at ICLR 2026 

behavior is observed during trajectory planning tasks: the model exhibits an emergent capacity to detect inconsistencies in its motion modeling and resolve them via iterative recalculations. 

_Let me think, the vehicle’s current velocity (5.64m/s) and negative acceleration suggest it’s already slowing, but stopping within 3s requires sustained deceleration of 1.0m/s², feasible given history._ 

_Wait, I’m re-examining the right edge of the frame and notice the continuous white lane line curves smoothly rightward beyond 5m, not ending abruptly. Oh, I see, the embankment isn’t a dead end; it’s roadside topography, and the road itself continues along the curve. The cones and sign mark a narrowing, not closure._ 

This autonomous reasoning process, characterized by four-stage self-reflection, is a hallmark of AutoDrive-R²’s training pipeline. The integration of physics-grounded rewards in the GRPO stage ensures that even minor corrections (e.g., adjusting lateral offsets or deceleration rates) are validated against real-world constraints. 

## B RELATED WORK 

### B.1 AUTONOMOUS DRIVING 

In recent years, autonomous driving has evolved from traditional modular pipelines—comprising detection, online mapping, prediction, and planning—toward end-to-end learning-based approaches (Hu et al., 2023; Jiang et al., 2023; Sun et al., 2024). UniAD (Hu et al., 2023) was the first to integrate all sub-tasks into a cascaded model, achieving significant improvements over traditional modular approaches. Some methods (Jiang et al., 2023; Ye et al., 2023; Chen et al., 2024) extract bird’s-eye view features and predict planning trajectories via multiple stages of interaction modeling. Para-Drive (Weng et al., 2024a) explores the design space of modular end-to-end autonomous driving stacks to significantly enhance both accuracy and inference speed. Additionally, Ego-MLP and BEV-Planner (Zhai et al., 2023; Li et al., 2024) investigate the role of ego-vehicle state and empirically validate its influence through experimental results. 

With the emergence of vision-language models (VLMs), researchers have increasingly integrated both large language models (LLMs) and VLMs into autonomous driving to enhance overall system performance. Several approaches (Xu et al., 2024; Shao et al., 2024a) incorporate pretrained LLMs to generate driving actions along with interpretable textual explanations. Furthermore, DriveVLM (Tian et al., 2024) incorporates specialized reasoning modules to improve situational understanding, while DriveMM (Huang et al., 2024) processes multi-view video and image inputs to enhance generalization in vehicle control. DriveMLM (Wang et al., 2023) introduces a behavior planning module to generate optimal driving decisions with accompanying rationales. 

Moreover, the recent success of vision-language-action (VLA) models in robotics offers a new perspective for autonomous driving. DriveMoE (Yang et al., 2025) builds on the embodied AI framework _π_ 0 (Black et al., 2024) and introduces Action-MoE by training routing networks to activate expert modules for diverse driving behaviors. Furthermore, OpenDriveVLA (Zhou et al., 2025a) proposes an agent-environment-ego interaction model for precise trajectory planning. AutoVLA (Zhou et al., 2025b) directly predicts semantic reasoning and trajectory plans from visual inputs and language prompts. 

### B.2 GENERAL VLMS 

In recent years, the success of large language models (LLMs) (Yenduri et al., 2023; Brown et al., 2020; Touvron et al., 2023) has motivated researchers to extend them into vision-language models (VLMs) (Radford et al., 2021; Zhu et al., 2023), which integrate textual and visual data for richer multimodal representation. CLIP (Radford et al., 2021), a pioneering work, combines image and text features using an image encoder and a text encoder to predict correct pairings of image-text examples via a zero-shot learning strategy. Similarly, BLIP (Li et al., 2022) and BLIP-2 (Li et al., 2023) are trained using an image-text contrastive (ITC) loss to align vision and language representations, along with an image-text matching (ITM) loss to distinguish between positive and negative image-text pairs, thereby enhancing visual representation grounded in textual context. Inspired 

18 

Published as a conference paper at ICLR 2026 

by these methods, many VLMs—such as LLaVA (Liu et al., 2023) and Qwen2.5VL (Bai et al., 2025)—further enhance the robustness and representation capabilities of pretrained vision encoders by integrating a large language model as the text encoder (e.g., LLaMA (Touvron et al., 2023)). OmniGen2 (Wu et al., 2025) represents another notable VLM, employing two distinct decoding pathways for text and image modalities with unshared parameters and a decoupled image tokenizer. Notably, DeepSeek-V3 (Liu et al., 2025) introduces a robust Mixture-of-Experts (MoE) language model that employs an auxiliary-loss-free strategy for load balancing, achieving both efficient and cost-effective inference. 

### B.3 REINFORCEMENT LEARNING FOR POST-TRAINING 

Reinforcement learning (RL) has been widely adopted in large language models, and researchers have found that reinforcement learning from human feedback (RLHF) (Lambert, 2025) can significantly enhance their reasoning capabilities. Among these methods, Proximal Policy Optimization (PPO) (Schulman et al., 2017) was initially used in simulated robotic locomotion and Atari game environments, and later employed by OpenAI to fine-tune GPT (Achiam et al., 2024), resulting in substantial improvements in text generation tasks. Unlike conventional RLHF methods, direct Preference Optimization (DPO) introduces a new reward model parameterization that eliminates the need for sampling during fine-tuning (Rafailov et al., 2023). Reward Fine-Tuning (RFT) (Yuan et al., 2023) is another RL-based approach that demonstrates strong performance in mathematical reasoning tasks. Furthermore, Guided Reward Policy Optimization (GRPO) (Shao et al., 2024b) effectively improves the reasoning capabilities of LLMs without relying on external toolkits or voting mechanisms. DeepSeek-R1 (Guo et al., 2025), for example, leverages GRPO to fine-tune its model and achieves superior performance compared to existing methods. Inspired by these approaches, recent work (Chen et al., 2025) adopts similar fine-tuning strategies to enhance the reasoning capabilities of language and multimodal models. 

## C VEHICLE KINEMATICS IN PHYSICS-GROUNDED REWARDS 

The physical constraints of autonomous driving systems are deeply rooted in vehicle kinematics and passenger comfort principles. Vehicle kinematics governs the relationship between steering geometry, tire friction, and acceleration limits, ensuring that predicted trajectories adhere to the physical capabilities of the vehicle. For instance, abrupt steering adjustments can violate the minimum turning radius determined by the vehicle’s wheelbase _L_ and maximum steering angle _δ_ max. The minimum turning radius _R_ min is defined as 


where _L_ is the distance between the front and rear axles (wheelbase), and _δ_ max is the maximum achievable steering angle of the front wheels. Any trajectory requiring a tighter turn than _R_ min would be physically infeasible, leading to tire slippage or loss of control. Additionally, lateral acceleration _ac_ during cornering must satisfy 


where _v_ is the vehicle speed, _R_ is the turning radius, _µ_ is the tire-road friction coefficient (typically _µ ≈_ 0 _._ 8), and _g_ is gravitational acceleration (9 _._ 81 m/s<sup>2</sup> ). Exceeding this threshold results in unsafe side-slip, particularly on low-friction surfaces like wet or icy roads. Beyond kinematic feasibility, passenger comfort is critically tied to smooth motion dynamics. Sudden changes in acceleration, known as jerk _j_ ( _t_ ), directly impact rider experience. Jerk is defined as 


where _a_ ( _t_ ) is the instantaneous acceleration. Human tolerance for jerk is generally below 2 _._ 5 m/s<sup>3</sup> , and abrupt steering or acceleration adjustments (e.g., _θj − θj−_ 1 or _vk − vk−_ 1) can induce discomfort jerky motions. Furthermore, rapid maneuvers amplify vibrations in the vehicle suspension system, modeled as a second-order differential equation: 


19 

Published as a conference paper at ICLR 2026 

where _m_ is the sprung mass (mass supported by the suspension), _c_ is the damping coefficient, _k_ is the spring stiffness, _x_ is the vertical displacement of the suspension, and _F_ ( _t_ ) is external forces (e.g., centrifugal force during sharp turns). Excessive _F_ ( _t_ ) due to abrupt motions overwhelms the suspension, increasing perceived jolts and reducing ride quality. 

These principles are directly addressed in the physics-grounded reward framework. By penalizing abrupt changes in steering angle and velocity through temporal smoothness terms _r_ tem, the method ensures that trajectories remain within the vehicle’s kinematic limits while minimizing jerk and vibration. This approach aligns with the experimental validation in the main text, where removing _r_ tem led to a 26.3% increase in trajectory error, underscoring the necessity of balancing geometric accuracy with physical and physiological constraints. 

## D DETAILED PROMPTS TO GENERATE COT DATA 

During the supervised fine-tuning (SFT) stage of AutoDrive-R², we designed a structured input prompt to generate high-quality chain-of-thought (CoT) data for the nuScenesR²-6K datasets. The prompt template is as follows: 

<mark>### Prompt: You are given an image, a driving-related question, and its answer. Generate a four-stage reasoning process with explicit mathematical modeling and self-validation. Engage in an internal dialogue using expressions such as ’let me think’, ’wait’, ’Hmm’, ’oh, I see’, ’let’ s break it down’, etc, or other natural language thought expressions. It’s encouraged to include self-reflection or verification in the reasoning process.</mark> 

<mark>### Input Format: - System Instructions: {original_task} - Past Vehicle Status: {original_information} - Prediction Task: {original_problem} - Answer: {original_solution} ### Output Format: ### 1. Visual Analysis "Image analysis results: - Vehicle’s intended direction: Left turn (steering wheel angle: \theta rad) - Obstacles ahead: *</mark><sup><mark>Cardetectedahead(movingright/left/straight)</mark></sup> <mark>*</mark><sup><mark>Pedestriancrossingroad(left/rightside)</mark></sup> <mark>- Traffic signal: signal_status detected (red / green / yellow)" ### 2. Motion Modeling "Using historical data in Past Vehicle Status with N time points:</mark> _<mark>t</mark>_ 1 <mark>: [</mark> _<mark>x</mark>_ <mark>=</mark> _<mark>x</mark>_ 1 _<mark>, y</mark>_ <mark>=</mark> _<mark>y</mark>_ 1 <mark>]</mark> _<mark>, v</mark>_ <mark>=</mark> _<mark>v</mark>_ 1 _<mark>m/s, a</mark>_ <mark>= (</mark> _<mark>a</mark> x_ 1 _<mark>, a</mark> y_ 1 <mark>)</mark> _<mark>m/s</mark>_<sup>2</sup> _<mark>t</mark>_ 2 <mark>: [</mark> _<mark>x</mark>_ <mark>=</mark> _<mark>x</mark>_ 2 _<mark>, y</mark>_ <mark>=</mark> _<mark>y</mark>_ 2 <mark>]</mark> _<mark>, v</mark>_ <mark>=</mark> _<mark>v</mark>_ 2 _<mark>m/s, a</mark>_ <mark>= (</mark> _<mark>a</mark> x_ 2 _<mark>, a</mark> y_ 2 <mark>)</mark> _<mark>m/s</mark>_<sup>2</sup> <mark>...</mark> _<mark>t</mark> n_ <mark>: [</mark> _<mark>x</mark>_ <mark>=</mark> _<mark>x</mark> n_ _<mark>, y</mark>_ <mark>=</mark> _<mark>y</mark> n_ <mark>]</mark> _<mark>, v</mark>_ <mark>=</mark> _<mark>v</mark> n_ _<mark>m/s, a</mark>_ <mark>= (</mark> _<mark>a</mark> xn_ _<mark>, a</mark> yn_ <mark>)</mark> _<mark>m/s</mark>_<sup>2</sup> <mark>Calculations: - Average acceleration:</mark> _<mark>a</mark> xavg_ <mark>= (</mark><sup><mark>�</mark></sup> _<mark>a</mark> xi_ <mark>)</mark> _<mark>/N</mark>_ <mark>=</mark> _<mark>a</mark> xavg_ _<mark>m/s</mark>_<sup>2</sup> _<mark>a</mark> yavg_ <mark>= (</mark><sup><mark>�</mark></sup> _<mark>a</mark> yi_ <mark>)</mark> _<mark>/N</mark>_ <mark>=</mark> _<mark>a</mark> yavg_ _<mark>m/s</mark>_<sup>2</sup> <mark>- Velocity prediction:</mark> _<mark>v</mark> x_ <mark>=</mark> _<mark>v</mark> n_ <mark>+</mark> _<mark>a</mark> xavg_ _<mark>× δ</mark> t_ <mark>=</mark> _<mark>v</mark> t_ 0 <mark>+</mark> _<mark>a</mark> xavg_ _<mark>× δ</mark> t_ _<mark>v</mark> y_ <mark>=</mark> _<mark>v</mark> n_ <mark>+</mark> _<mark>a</mark> yavg_ _<mark>× δ</mark> t_ <mark>=</mark> _<mark>v</mark> t_ 0 <mark>+</mark> _<mark>a</mark> yavg_ _<mark>× δ</mark> t_ <mark>- Position prediction:</mark> _<mark>x</mark>_ <mark>(</mark> _<mark>t</mark>_ <mark>+ 1) =</mark> _<mark>x</mark> n_ <mark>+</mark> _<mark>v</mark> x_ _<mark>× δ</mark> t_ <mark>+ 0</mark> _<mark>.</mark>_ <mark>5</mark> _<mark>× a</mark> xavg_ _<mark>× δ</mark> t_<sup>2</sup> _<mark>y</mark>_ <mark>(</mark> _<mark>t</mark>_ <mark>+ 1) =</mark> _<mark>y</mark> n_ <mark>+</mark> _<mark>v</mark> y_ _<mark>× δ</mark> t_ <mark>+ 0</mark> _<mark>.</mark>_ <mark>5</mark> _<mark>× a</mark> yavg_ _<mark>× δ</mark> t_<sup>2</sup> <mark>- Lateral offset:</mark> _<mark>δ</mark> y_ <mark>=</mark> _<mark>v × tan</mark>_ <mark>(</mark> _<mark>θ</mark>_ <mark>) =</mark> _<mark>v</mark> t_ 0 _<mark>× tan</mark>_ <mark>(</mark> _<mark>θ</mark>_ <mark>)</mark> 

20 

Published as a conference paper at ICLR 2026 

<mark>### 3. Logical Deductions "Safety check: - If following this trajectory, will the vehicle: *</mark><sup><mark>Runaredlight?</mark></sup><sup>_<mark>→</mark>_</sup><sup><mark>yes/no</mark></sup> <mark>*</mark><sup><mark>Collidewithcarahead?</mark></sup><sup>_<mark>→</mark>_</sup><sup><mark>yes/no</mark></sup> <mark>*</mark><sup><mark>Hitpedestriancrossing?</mark></sup><sup>_<mark>→</mark>_</sup><sup><mark>yes/no</mark></sup> 

<mark>- Conclusion: recommended_action (e.g., ’Stop immediately’, ’Reduce speed to 5m/s’)"</mark> 

<mark>### 4. Self-Reflection Validation "Validation: - Assumption check:</mark> 

<mark>*</mark><sup><mark>Predictedposition(x=x_pred,y=y_pred)requiresaveragespeedofvm</mark></sup> <mark>/s</mark> 

<mark>*</mark><sup><mark>Isthisspeedachievablewithvehicle’saccelerationhistory?</mark></sup><sup>_<mark>→</mark>_</sup><sup><mark>yes/</mark></sup> <mark>no - Adjustment:</mark> 

<mark>*</mark><sup><mark>Ifnotfeasible</mark></sup><sup>_<mark>→</mark>_</sup><sup><mark>Modifytrajectorybyreducingspeedorincreasing</mark></sup> <mark>stopping distance"</mark> 

This structured prompt ensures nuScenesR²-6K dataset contains diverse and causally plausible reasoning process, which are critical for cultivating the model’s foundational perception and planning capabilities before RL fine-tuning. 

## E LLM CLARIFICATION 

We clarify the role of Large Language Models (LLMs) in the preparation of this manuscript. Specifically, LLMs were employed to refine the language, grammar, and overall readability of the text. This involved tasks such as correcting grammatical errors, improving sentence structure, and enhancing the flow of the narrative to ensure clarity and precision in scientific communication. It is critical to emphasize that all core scientific contributions, including the formulation of the research problem, the development of the AutoDrive-R² framework, the creation of the nuScenesR²-6K dataset, the design of the two-stage training methodology combining chain-of-thought reasoning and Group Relative Policy Optimization (GRPO) with physics-grounded rewards, and the comprehensive experimental analysis on nuScenes and Waymo benchmarks, are the result of the authors’ independent work. The LLM was strictly utilized as a linguistic tool and did not contribute to the conceptualization, implementation, or evaluation of the proposed methods. All intellectual property, including the theoretical foundations, algorithmic innovations, and empirical validations, originates solely from the human authors. 

21 

Published as a conference paper at ICLR 2026 


Figure 6: Visualization comparison between Qwen2.5-VL-7B and AutoDrive-R² on nuScenes. 


Figure 7: Visualization comparison between Qwen2.5-VL-7B and AutoDrive-R² on nuScenes. 

22 

