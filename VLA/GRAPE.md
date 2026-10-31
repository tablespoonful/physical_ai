---
title: "GRAPE: Generalizing Robot Policy via Preference Alignment"
date: "2024-11-28"
authors: "Zijian Zhang; Kaiyuan Zheng; Zhaorun Chen; Joel Jang; Yi Li; Siwei Han"
venue: "ICRA 2026"
url: https://arxiv.org/abs/2411.19309
pdf: https://arxiv.org/pdf/2411.19309
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2411.19309)** / [論文ページ](https://arxiv.org/abs/2411.19309)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

**Zijian Zhang**<sup>* 1</sup> **Kaiyuan Zheng**<sup>* 2</sup> **Zhaorun Chen**<sup>* 3</sup> **Joel Jang**<sup>2</sup> **Yi Li**<sup>2</sup> **Siwei Han**<sup>1</sup> **Chaoqi Wang**<sup>3</sup> **Mingyu Ding**<sup>1</sup> **Dieter Fox**<sup>2</sup> **Huaxiu Yao**<sup>1</sup> 

# **Abstract** 

Despite the recent advancements of visionlanguage-action (VLA) models on a variety of robotics tasks, they suffer from critical issues such as poor generalizability to unseen tasks, due to their reliance on behavior cloning exclusively from successful rollouts. Furthermore, they are typically fine-tuned to replicate demonstrations collected by experts under different settings, thus introducing distribution bias and limiting their adaptability to diverse manipulation objectives, such as efficiency, safety, and task completion. To bridge this gap, we introduce **GRAPE** : **G** ene **ra** lizing Robot Policy via **P** r **e** ference Alignment. Specifically, GRAPE aligns VLAs on a trajectory level and implicitly models reward from both successful and failure trials to boost generalizability to diverse tasks. Moreover, GRAPE breaks down complex manipulation tasks to independent stages and automatically guides preference modeling through customized spatiotemporal constraints with keypoints proposed by a large vision-language model. Notably, these constraints are flexible and can be customized to align the model with varying objectives, such as safety, efficiency, or task success. We evaluate GRAPE across a diverse array of tasks in both real-world and simulated environments. Experimental results demonstrate that GRAPE enhances the performance of state-of-the-art VLA models, increasing success rates on in-domain and unseen manipulation tasks by 51.79% and 58.20%, respectively. Additionally, GRAPE can be aligned with various objectives, such as safety and efficiency, reducing collision rates by 37.44% and rollout step-length by 11.15%, respectively. 

> *Equal contribution 1UNC-Chapel Hill, Chapel Hill, NC, USA 

> 2University of Washington, Seattle, WA, USA 3University of Chicago, Chicago, IL, USA. Correspondence to: Huaxiu Yao _<_ huaxiu@cs.unc.edu _>_ . 


Figure 1: Comparison of GRAPE with SOTA VLA models fine-tuned on the same data across a large variety of generalization and in-domain tasks in both real-world and simulated environments. 

# **1. Introduction** 

The recent rapid proliferation of vision-language-action (VLA) models has streamlined general robotic manipulation tasks, demonstrating impressive capability across a range of tasks under controlled environmental variations (Black et al., 2024; Kim et al., 2024; Team et al., 2024; Brohan et al., 2023). However, these models face several critical challenges such as poor generalizability across new environments, objects, tasks, and semantic contexts (Kim et al., 2024). A significant factor contributing to this limitation is their reliance on _supervised fine-tuning_ (SFT), where VLAs simply imitate actions from successful rollouts via behavior cloning while not developing a holistic understanding of the task goal or potential failure patterns (Kumar et al., 2021). While reinforcement learning (RL) algorithms such as PPO (Schulman et al., 2017) have proved promising in enhancing their generalizability (Zhai et al., 2024), the high cost of gathering sufficient online trajectories and explicitly defining reward make them impractical for training VLA (Team et al., 2024). 

Furthermore, training VLAs to solely replicate expert behaviors often results in _behavior collapse_ (Kumar et al., 2024) where the planned trajectories are often suboptimal (Kim et al., 2024). This is because the SFT datasets are usually 

_Preprint_ 

1 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 


Figure 2: **Overview of GRAPE.** GRAPE first uses a VLM to decompose a manipulation task ( **top** ) into temporal stages and identify key spatial points for each subtask. Given user-specified alignment goals, it prompts a VLM to generate cost functions for each stage. During iterative preference optimization ( **bottom** ), offline trajectories are sampled from the base VLA model, scored using multi-stage cost, self-evaluation and task success indicators, and ranked to form preferences. GRAPE then optimizes the VLA models iteratively until convergence. 

uncurated and consist of offline demonstrations collected from experts that embed implicitly different values (e.g. task completion, safety, and cost-efficiency) that are not clearly defined within the data (O’Neill et al., 2023; Walke et al., 2023). Simply imitating these behaviors via SFT can potentially confuse the model and result in suboptimal trajectories that deviate from the actual objective of the demonstrations. Some approaches attempt to address this challenge by explicitly defining a set of objectives and solving them hierarchically (Huang et al., 2024). However, this approach incurs additional inference overhead and lacks scalability (Li et al., 2024b). 

To address these issues, we propose **GRAPE** : **G** ene **ra** lizing Robot Policy via **P** r **e** ference Alignment to alleviate the high cost of training VLAs with RL objective, while offering flexibility for aligning towards customized manipulation objectives. As shown in Figure 2, GRAPE introduces _trajectory-wise preference optimization_ (TPO) to align VLA policies on a trajectory level by implicitly modeling reward from both successful and failure trials, boosting generalizability to diverse tasks. To further alleviate the difficulty in ranking trajectories and providing preferences towards arbitrary alignment objectives, GRAPE proposes to decompose the complex manipulation tasks into multiple independent stages and adopt a large vision model to propose keypoints for each stage, each associated with a spatial-temporal constraint. Notably, these constraints are flexible and can be 

customized to align the model with varying manipulation objectives, such as task completion, robot-interaction safety, and cost-efficiency. We evaluate GRAPE across a wide range of real-world tasks and two simulated environments. Experimental results show that GRAPE outperforms stateof-the-art VLA models, improving success rates on both in-domain and unseen manipulation tasks by 51.79% and 58.20%, respectively. Moreover, GRAPE can be aligned to diverse objectives such as safety and efficiency, to further reduce collision rate by 37.44% and rollout step-length by 11.15%, respectively. 

# **2. Generalizing Robot Policy via Preference Alignment** 

## **2.1. Preliminaries** 

During inference, a VLA typically initializes with an task instruction _q_ , and at each timestep _t_ , it takes an environment observation _ot_ (usually an image) and outputs an action _at_ , where we can denote _πθ_ ( _ai|_ ( _oi, q_ )) as the action policy of a VLA parameterized by _θ_ . To complete the task, VLA iteratively interacts with the environment and obtains a trajectory _ζ_ = _{o_ 1 _, a_ 1 _, · · · , oT , aT |q}_ of length _T_ . Typically, VLAs are fine-tuned to imitate expert behaviors via SFT: 


2 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

where _D_ = _{_ ( _ζ_ 1 _, q_ 1) _, . . . ,_ ( _ζN , qN_ ) _}_ denotes the training set containing _N_ expert trajectories. Specifically, _L_ SFT enforces VLA to memorize the action associated with each observation sampled from a distribution P _D_ , resulting in poor generalizability to new task settings. It is worth to note that while we follow O’Neill et al. (2023); Brohan et al. (2023) and consider the step-wise policy based on the Markov decision process (MDP) assumption (Sutton, 2018), our approach can be easily adapted to both non-MDP case which takes past interaction histories (usually a video or a series of images) as state (Cheang et al., 2024) and diffusion policy (Chi et al., 2023) which generates multiple future steps all at once (Team et al., 2024). 

## **2.2. TPO: Trajectory-wise Preference Optimization** 

To improve generalization, we follow Schulman et al. (2017); Bai et al. (2022) and further fine-tune VLA policies via RL objective. Let _rϕ_ denote a reward function parameterized by _ϕ_ , we have 


where _β_ controls the deviation from the base reference policy _π_ ref trained via SFT in Eq. (1) and _π_ ( _ζ, q_ ) is the likelihood of policy _π_ generating the entire trajectory _ζ_ under instruction _q_ . Then we follow Rafailov et al. (2024) and derive the analytical reparameterization of the trajectory reward _r_ ( _ζ_ ) as: 


Similar to Rafailov et al. (2024), we adopt the Bradley-Terry (BT) (Bradley & Terry, 1952) model and model _rϕ_ from a set of trajectories ranked with preferences. Specifically, let _ζw_ and _ζl_ denotes the chosen and rejected trajectory starting from the same initial state, we can formulate the trajectory-wise reward modeling objective as: 


Then, we follow Rafailov et al. (2024) and substitute Eq. (3) into Eq. (4) and obtain the following _trajectory-wise preference optimization_ (TPO) loss _L_ TPO equivalent to Eq. (2): 


where we can further draw from MDP and decompose the likelihood of a trajectory _ζ_ into individual state-action pairs, i.e., _π_ ( _ζ, q_ ) =<sup>�</sup><sup>_T_</sup> _i_ =1<sup>_π_(</sup><sup>_ai|_(</sup><sup>_oi, q_)) and further obtain</sup> 


Then we can substitute Eq. (6) into Eq. (5) to obtain the TPO loss _L_ TPO in terms of step-wise state-action pairs. Our TPO loss Eq. (6) is beneficial as it: (1) aligns policy _πθ_ globally towards human preferences on a trajectory level while simply using step-wise rollouts collected by VLAs; (2) it stabilizes the policy and steers it towards the final goal by backpropagating the gradients throughout all the stateaction pairs along the trajectory; (3) it significantly boosts generalizability by learning from both successful and failed trajectories via a RL objective. Although Finn et al. (2016) indicates that expanding the size of the sampled trajectory can reduce the bias in reward modeling, it also increases the training costs. Thus while our method can be easily scaled up, we keep our discussion to the binary case where only one chosen/rejected trajectory is present. 

## **2.3. Guided-Cost Preference Generation** 

While given the TPO objective Eq. (5) we can align the policy towards arbitrary objectives defined through trajectories ranked by the corresponding preference, it incurs high costs as it requires human expertise and lengthy manual annotation. Thus to better scale up the preference synthesis towards arbitrary alignment objectives (e.g. task completion, safety, efficiency), we propose _Guided-Cost Preference Generation (GCPG)_ to automatically curate such preferences that integrate different alignment objectives. 

## 2.3.1. MULTI-STAGE TEMPORAL KEYPOINT CONSTRAINTS 

Building on insights from Huang et al. (2024), we address the complexity of specifying precise trajectory preferences for complex manipulation tasks by decomposing trajectories into temporal stages and assigning costs to quantify performance at each stage. Then, we aggregate these stagespecific costs to obtain a holistic evaluation for each trajectory. Specifically, we adopt a VLM-based stage decomposer _MD_ (detailed in Appendix A), to partition a trajectory _ζ_ into a sequence of **S** consecutive stages, formulated as 


After obtaining the stage decomposition, we further employ a vision-language model (e.g. DINOv2 (Oquab et al., 2023)) to identify keypoints that serve as reference metrics across each stage. Then we prompt a powerful LLM (Achiam et al., 2023) to propose cost functions (see examples in Appendix E.2.) for each stage that corresponds with the alignment objective, where lower cost indicates better objective compliance. Specifically, the cost _C_<sup>_Si_</sup> ( _{κSi}_ ) at stage _Si_ is calculated using its corresponding keypoints _{κSi}_ . 

Then to aggregate the costs for the entire trajectory, instead of summing each stage linearly, we apply an exponential 

3 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

**Algorithm 1** GRAPE Iterative Preference Optimization 

decay to capture the casual dependencies of each temporal stage (e.g. if a trajectory incurs high costs in preceding stages it is not expected to perform well subsequently), defined as the _external reward_ : 

- trajectory incurs high costs in preceding **Require:** Base VLA policy _πθ_ , a collection of task instruc- 

- expected to perform well subsequently), tions _Q_ = _{qi}_ , stage decomposer _MD_ , max iterations 

- _external reward_ : _K_ , reward weights _{λ_ 1 _, λ_ 2 _, λ_ 3 _}_ , stage-wise keypoints **S** _{κSi}_ cost functions _{Cj_<sup>_Si}_and thresholds</sup><sup>_{τ S_</sup> _j_<sup>_i}_</sup> 

- _R_ ext( _ζ_ ) = � _e_<sup>_−CSi_(</sup><sup>_{κSi }_)</sup> (8) **Ensure:** policy _π_<sup>_∗_</sup> aligned towards customized objective _i_ =1 1: **for** _k_ = 1 _, . . . , K_ **do** 2: Sample trajectories _D_<sup>_k_</sup> = _{ζi}_<sup>_M_</sup> _i_ =1<sup>using</sup><sup>_πθ_with</sup><sup>_Q_</sup> 

- aggregates the individual costs and sub3: **for** trajectory _ζ ∈D_<sup>_k_</sup> **do** 

where Eq. (8) aggregates the individual costs and subobjectives from each stage to tackle the curse of dimensionality and effectively adhere to the customized alignment. 

- 4: Decompose _ζ_ into multiple stages _S {_ Eq. (7) _}_ 5: Compute the cost for each stage _CSi_ 6: Calculate external reward _R_ ext( _ζ_ ) _{_ Eq. (8) _}_ 7: Compute policy self-reward _R_ self( _ζ_ ) _{_ Eq. (10) _}_ 8: Examine task success _I_ success( _ζ_ ) _{_ Eq. (11) _}_ 9: Aggregate GCPG reward _R_ GCPG( _ζ_ ) _{_ Eq. (9) _}_ 

- 10: **end for** 11: Rank _D_<sup>_k_</sup> by their _R_ GCPG( _ζ_ ) rewards 

## 2.3.2. GUIDED-COST PREFERENCE GENERATION 

To further improve the stability and optimality of the preference synthesis, we draw inspirations from selfrewarding (Zhou et al., 2024b) and determine that _a more optimal trajectory should be confirmed by both the external judge (as in Eq. (8)) and the model itself_ . Thus we incorporate two additional rewards and obtain the GCPG reward: 

- 12: Pair _{ζw, ζl}_ from top- _m_ and bottom- _m_ trajectories 13: Update _πθ_ using TPO loss _{_ Eq. (5) _}_ 14: **end for** 


where _R_ self( _ζ_ ) is the self-evaluated score provided by _π_ , which equals the log-likelihood of generating trajectory _ζ_ : 


and _I_ success( _ζ_ ) is a binary indicator function that indicates whether the trajectory _ζ_ successfully completes the task: 


where _λ_ are the weight parameters that adjust the importance of each reward. Intuitively, Eq. (10) can be seen as a dense approximation of the sparse signal provided by Eq. (11), which are further calibrated by Eq. (8) to obtain a holistic evaluation of the trajectory that accounts for both its optimality and degree of alignment to a customized objective specified through the external reward in Eq. (8). 

## **2.4. Iterative Preference Optimization** 

After generating the preference, we then discuss our iterative preference optimization strategy. Inspired by the practices of on-policy RL (Schulman et al., 2017) which often yield more optimal policy than off-policy training, we iteratively fine-tune the SFT VLA model via TPO with trajectories collected online. For example, during the _k_<sup>th</sup> iteration, we (1) first sample numerous trajectories for a variety of tasks and obtain _D_<sup>_k_</sup> ; (2) then we calculate the costs for each trajectory using Eq. (9) and rank these trajectories accordingly per task; (3) we pair the top- _m_ and bottom- _m_ trajectories 

with each other for each task, and obtain _m_<sup>2</sup> chosen-rejected trajectory pairs; (4) then we fine-tune the same sampling policy with TPO via Eq. (5) and obtain an updated policy. We iterate this process for _K_ times and obtain the final model aligned with the target objective. We detail the GRAPE iterative preference optimization procedure in Algorithm 1. 

# **3. Experiment** 

In this section, we evaluate GRAPE’s performance in both real and simulated environments, addressing four key questions: (1) Does GRAPE improve the VLA model’s performance relative to SFT-based baseline models? (2) How effective are guided-cost preference selection and iterative preference optimization in enhancing the model’s performance? (3) What is the individual contribution of each reward component to overall model performance? (4) Can GRAPE support flexible alignment with different alignment objectives? 

## **3.1. Experimental Setups** 

**Implementation Details.** We employ OpenVLA (Kim et al., 2024) as the backbone model, using LoRA fine-tuning with the AdamW optimizer for both supervised and preference fine-tuning. In the supervised fine-tuning stage, we use a learning rate of 4 _×_ 10<sup>_−_5</sup> with a batch size of 16. For preference fine-tuning, we apply a learning rate of 2 _×_ 10<sup>_−_5</sup> with the same batch size. Further details on the training process and datasets are available in Appendices A and B. 

**Baseline Models.** We first compare GRAPE with two leading robot learning models known for their strong perfor- 

4 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 


Figure 3: Comparison of GRAPE with OpenVLA and Octo fine-tuned on the same data on the Simpler-Env environment. We report the in-domain performance, which includes four tasks and three generalization evaluations ( _subject_ , _physical_ , and _semantic_ ), where each incorporates multiple tasks. 

mance in robot control tasks. The first model, Octo (Team et al., 2024), is a large transformer-based policy model. The second, OpenVLA (Kim et al., 2024), is a 7B VLA model. Both models were supervised fine-tuned using the same dataset sampled from corresponding environments. We denote the supervised fine-tuned models as Octo-SFT and OpenVLA-SFT, respectively. In addition, we compare GRAPE, which utilizes trajectory-wise preference optimization, with the original step-wise direct preference optimization, denoted as OpenVLA-DPO, which is directly trained to optimize preferences defined at each step. 

## **3.2. Evaluation in Simulation Environment** 

**Evaluation Setup.** Follow Kim et al. (2024), we evaluate GRAPE’s performance in two robot simulation environments: Simpler-Env (Li et al., 2024a) and LIBERO (Liu et al., 2023). In Simpler-Env, we evaluate the model’s indomain performance as well as its generalization across three aspects: subject (generalize to unseen objects), physical (generalize to unseen object sizes/shapes), and semantic (generalize to unseen instructions) generalization. In LIBERO, we test our model on four tasks: LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-Long. All tasks are in-domain tasks. Additional details about the experimental setup are provided in Appendix C.2. 

**Results.** We use the success rate across all tasks in SimpleEnv and LIBERO as our primary evaluation metric, while we also record the grasping rate in Simpler-Env. The results of Simple-Env and LIBERO are reported in Figure 3 and Figure 4, respectively. According to the results, GRAPE outperforms Octo-SFT and OpenVLA-SFT in Simpler-Env by an average of 131.72% and 46.10%, respectively, and in LIBERO by an average of 8.53% and 7.36%, respectively. Additional results are provided in Appendix D. This outcome aligns with our expectations, as learning from preference comparisons enhances alignment with trajectory completion, thereby improving performance. Moreover, while GRAPE significantly boosts in-domain performance, 


Figure 4: Comparison of GRAPE with OpenVLA and Octo fine-tuned on the same data on the LIBERO environment. We report the performance on four types of LIBERO tasks. 

it also enhances the generalizability of VLA policies on OOD tasks by aligning task completion at the trajectory level. Furthermore, GRAPE outperforms OpenVLA-DPO in both environments, achieving an average improvement of 33.14%, demonstrating the effectiveness of trajectory-wise preference optimization due to learning from both success and failure from a global trajectory level without low-level step-wise noises. 

## **3.3. Evaluation in Real-World Robot Environment** 

**Evaluation Setup.** We conducted 300 real-world experiments across 30 tasks to evaluate the generalization capabilities of GRAPE. The evaluation focus on in-distribution evaluation and five out-of-distribution generalization types: visual, subject, action, semantic, and language grounding generalizations. Here, visual generalization assesses the ability to adapt to new visual environments; subject generalization evaluates the recognition and handling of unfamiliar objects; action generalization measures performance across diverse actions; semantic generalization evaluates responses to prompts with similar meanings; and language grounding generalization gauges comprehension of spatial directions. Detailed experimental setup are provided in Appendix C.1 and illustrated in Figure 5. 

**Results.** In the real-world experiment, GRAPE significantly outperforms other models across a variety of tasks. Notably, in in-domain tasks, GRAPE achieves a success rate of 67.5%, which is a 17.5% improvement over OpenVLADPO’s 50%, OpenVLA-SFT’s 45% and substantially higher than Octo-SFT’s 20%. Additionally, in visual generalization tasks, GRAPE demonstrates higher adaptability with a success rate of 56%. In the more challenging action generalization tasks, although OpenVLA-SFT shows modest performance, GRAPE still outperforms OpenVLA-SFT, indicating its potential in understanding various actions and executing commands based on language. Considering tasks across all categories, GRAPE’s total average success rate is 50.3%, marking a 11% improvement over OpenVLADPO’s 39.3%, OpenVLA-SFT’s 32.3% and significantly 

5 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 


Figure 5: Comparison of GRAPE with OpenVLA and Octo fine-tuned on the same data on the real-world environment. We report the in-domain performance, which includes four tasks and five generalization evaluations ( _visual_ , _subject_ , _action_ , _semantic_ , and _language grounding_ ), where each incorporates multiple tasks. We also report the average performance across all tasks. 

Figure 6: Performance of GRAPE during iterative preference optimization via TPO. We demonstrate the average success rate for each iteration across in-domain tasks and three types of generation tasks ( _subject_ , _physical_ , _semantics_ ). 

ahead of Octo-SFT’s 5.7%. This performance highlights (1) GRAPE’s effectiveness and adaptability in handling complex and variable task environments and (2) validates the effectiveness of trajectory-wise preference optimization in learning from global success and failure patterns when compared to OpenVLA-DPO. 

## **3.4. Ablation Study of Reward Model** 

In this section, we conduct an ablation study to analyze the contribution of each reward component in Eq. (9) to the final performance: the external objective-aligned reward _R_ ext( _ζ_ ), the self-evaluated reward _R_ self( _ζ_ ), and the success indicator _I_ success( _ζ_ ). Additionally, we perform a separate ablation study to emphasize the importance of utilizing the entire reward score for preference selection. This approach is compared against a method that randomly selects one successful trajectory as the preferred trajectory and one failed trajectory as the rejected trajectory. The results in the Simpler-Env environment are reported in Table 1. 

The results indicate that: (1) incorporating the full reward score Eq. (9) for preference ranking significantly enhances performance compared to random selection based 

on success alone; (2) all reward components contribute to model performance. These findings align with our expectations. Specifically, _R_ self( _ζ_ ) enhances the robustness of the GRAPE by encouraging it to select trajectories with higher generation probabilities. In parallel, _R_ ext( _ζ_ ) guides the model toward learning specific behaviors, such as safety and efficiency. Finally, _I_ success( _ζ_ ) serves as a critical indicator, steering the model to prioritize successful trajectories. 

## **3.5. Analysis of Iterative Preference Optimization** 

In this section, we analyze the iterative preference optimization performance. We conduct the experiments on the Simpler-Env environment and report the results with respect to the training iterations in Figure 6. Here, SFT means the supervised fine-tuned OpenVLA model before preference optimization. In our experiments, GRAPE achieves 17.5%, 9.0%, 15.0%, 21.0% improvements in in-domain performance, subject generalization, physical generalization and semantic generation, respectively. The findings suggest that GRAPE progressively enhances model performance across iterations, showcasing its ability to enhance the quality of generated preference data and achieve better 

6 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

Table 1: Ablation study of reward score. Here, Random w/ _I_ success refers to randomly selecting one successful trajectory as the chosen trajectory and one failed trajectory as the rejected trajectory, _R_ self( _ζ_ ) is the self-evaluated score provided by the log-likelihood of generating trajectory _ζ_ , _R_ ext( _ζ_ ) represents objective-aligned multi-stage reward defined in Eq. (8), _I_ success( _ζ_ ) is a binary indicator function that indicates whether the trajectory _ζ_ successfully completes the task. 

||**In-do**<br>Grasp|**main**<br>Success|**Subje**<br>Grasp|**ct Gen.**<br>Success|**Physic**<br>Grasp|**al Gen.**<br>Success|**Semant**<br>Grasp|**ics Gen.**<br>Success|**Ave**<br>Grasp|**rage**<br>Success|
|---|---|---|---|---|---|---|---|---|---|---|
|Random w/_I_success|62.00%|35.50%|60.33%|33.00%|44.00%|33.50%|54.50%|36.50%|55.21%|34.63%|
|w/o_R_self(_ζ_)|66.50%|38.00%|62.33%|37.00%|51.25%|36.75%|68.00%|42.50%|62.02%|38.56%|
|w/o_R_ext(_ζ_)|63.50%|37.50%|61.00%|34.33%|48.50%|35.50%|62.50%|40.00%|58.88%|36.83%|
|w/o_I_success|58.50%|32.00%|59.67%|34.67%|42.25%|31.75%|58.50%|39.00%|54.73%|34.36%|
|GRAPE|**71.00%**|**43.00%**|**62.67%**|**40.67%**|**63.50%**|**41.75%**|**72.00%**|**47.00%**|**67.29%**|**43.11%**|


Table 2: Results with respect to different objectives. GRAPE-Safety, GRAPE-Efficiency, GRAPE-TC are models trained with safety, efficiency, task completion objectives, respectively. Here, we use collision rate (CR), step length (SL), success rate (SR) to evaluate the safety, efficiency and task completion capabilities. 

|Method|**R**|**eal-Wor**|**ld**|**Si**|**mulati**|**on**|
|---|---|---|---|---|---|---|
||CR_↓_|SL_↓_|SR_↑_|CR_↓_|SL_↓_|SR_↑_|
|OpenVLA-SFT|53.33|142.32|34.61|66.50|72.68|27.50|
|GRAPE-Safety|**29.84**|146.11|54.31|**46.00**|74.49|37.00|
|GRAPE-Efficiency|58.45|**125.79**|51.67|57.50|**64.92**|38.50|
|GRAPE-TC|38.60|131.66|**58.46**|59.50|70.24|**42.50**|


generalization. Notably, the magnitude of improvement diminishes over time, aligning with our expectations as the model approaches convergence. 

## **3.6. Analysis of Different Alignment Objectives** 

## 3.6.1. QUANTITATIVE ANALYSIS 

After demonstrating the effectiveness of GRAPE in improving the generalization of the VLA model (measured by success rate), we further investigate its potential to align the model with flexible objectives, such as efficiency and safety. Revisiting Eq. (8), we observe that adjusting the threshold parameters can guide the model to prioritize specific objectives by influencing trajectory preference selection. In this study, we focus on two new alignment objectives: safety and efficiency. Safety aims to minimize collisions between the robot and objects, while efficiency seeks to reduce the average number of steps required for the robot to complete a task. To achieve these objectives, we set a lower threshold for collision costs to emphasize safety and a lower threshold for path costs to prioritize efficiency. These modified settings are then applied to the original real-world and simulation evaluations. We train models to align with the safety and efficiency objectives, referring to these models as GRAPESafety and GRAPE-Efficiency, respectively (see detailed experimental setup in Appendix C.2). 

The results are reported in Table 2, where we use collision rates, step lengths, and success rates to evaluate safety, efficiency and generalization capabilities, respectively. According to Table 2, the GRAPE-Safety and GRAPE-Efficiency have better performance on collision rate and step length respectively, meanwhile maintain a comparable success rate, compared with OpenVLA-SFT. The results indicate that GRAPE can be easily adapted to account for flexible alignment objectives such as safety, efficiency by adjusting the multi-stage cost functions accordingly, while incurring minimal drop in task success rate. 

## 3.6.2. CASE STUDY 

We further demonstrate a case study in Figure 7 to analyze GRAPE’s adaptability towards different alignment objectives. Specifically, we consider a safety-critical _pickup_ task where an obstacle is placed between the object and the target. Specifically, OpenVLA-SFT fails to complete the task without preference alignment. However, we can see that while GRAPE aligned towards task completion (on the secondrow of Figure 7) can effectively pick up and place the object, it also collides with the obstacle, due to the policy is aligned to aggressively boost task success without explicitly addressing safety concerns. On the contrary, GRAPE-safety learns to avoid colliding with the obstacle while efficiently completing the task. Both Table 2 and Figure 7 indicates that by simply tweaking the cost function, GRAPE can effectively adapt to different objectives. More cases and detailed safety evaluation tasks could be found in Appendix E.1. 

# **4. Related Works** 

**Vision-Language-Action Models.** Previous robot learning works (Huang et al., 2024; Li et al., 2024b; Chen et al., 2024c; Mu et al., 2024a; Huang et al., 2023; Liang et al., 2023a; Mu et al., 2024b) typically take a hierarchical planning strategy. For example, Code as Policies (Liang et al., 2023a) and EmbodiedGPT (Mu et al., 2024b) use LLMs and VLMs to generate high-level action plans, then rely on a low-level controller for local trajectories. However, such models suffer from limited low-level skills and are hard to 

7 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 


Figure 7: Comparison of GRAPE aligned via _safety_ objective (GRAPE-Safety) with GRAPE aligned via _task-completion_ (GRAPE-TC) objective and OpenVLA-SFT. Specifically, we assess their performance on a safety-critical task with the instruction: _pick up the white box and place into the black pot_ . 

generalize to everyday tasks. VLAs tend to scale up lowlevel tasks by incorporating VLM as backbones and directly generating actions within the model. They generally achieve action planning via two mainstream approaches: (1) Discretizing the action space (Kim et al., 2024; Brohan et al., 2023; 2022), as in OpenVLA (Kim et al., 2024), preserves the autoregressive language decoding objective by truncating actions into a small set of _action tokens_ . However, this introduces errors, leading some methods (Black et al., 2024) to adopt newer structures (Zhou et al., 2024a) that integrate diffusion heads for action prediction, avoiding discretization. (2) Diffusion models (Chi et al., 2023; Xian et al., 2023; Janner et al., 2022; Liang et al., 2023b; Ajay et al., 2023), such as Diffusion Policy (Chi et al., 2023), serve as the action head, generating a sequence of future actions through iterative denoising instead of stepwise action generation. 

While these models vary in structure, they are consistently supervised-trained on successful rollouts via behavior cloning, which can hardly be generalized to unseen manipulation tasks. However, our GRAPE first aligns VLA policies on a trajectory level via trial and error, effectively boosting generalizability and customizability. 

**Reinforcement Learning and Preference Optimization.** 

Reinforcement learning (RL) (Christiano et al., 2017; Ziegler et al., 2019; Schulman et al., 2017) plays a pivotal role in the post-training of foundation models (Dubey et al., 2024; Achiam et al., 2023; Chen et al., 2024d;a; Fan et al., 2024; Yang et al., 2024; Chen et al., 2024b; Wang et al., 2025), which has been extensively leveraged to align the pre-trained FMs to comply with human values embedded through preference data. In the meantime, RL has also shown tremendous success in training policies for robotics tasks (Chen et al., 2024c; Wang et al., 2024b; Chen et al., 2021; 2022; Zhu et al., 2019; Wu et al., 2024). While it is 

intuitively beneficial to post-align VLA via RL, few prior works have reported such success, mainly due to that (1) manipulation objectives are usually diverse and complex, making the reward hard to define analytically (Finn et al., 2016); (2) while such reward can be modeled from human preferences, annotating such preferences in robotics manipulation tasks are usually lengthy (Walke et al., 2023); (3) the imperfect numerical differentiation of rewards usually leads RL algorithms such as PPO (Schulman et al., 2017) to collapse (Bus¸oniu et al., 2018). However, various recent works (Rafailov et al., 2024; Wang et al., 2024a) have successfully aligned the policy via RL without explicit reward modeling. Inspired, GRAPE aligns the policy by contrasting trajectories with each other, avoiding issues in rewarding modeling. Besides, we introduce an automatic preference synthesis pipeline that easily scales with diverse manipulation tasks and adapts to different alignment objectives. 

# **5. Conclusion** 

In this work, we addressed the critical challenges faced by vision-language-action (VLA) models, including limited generalizability and adaptability to diverse manipulation objectives. We proposed GRAPE, which aligns VLA policies on a trajectory level. GRAPE enhances generalizability by learning from both successful and failed trials, offering flexibility in aligning with objectives such as safety, efficiency, and task success through customized spatiotemporal constraints. Experimental results demonstrated significant improvements, with GRAPE enhancing success rates on both in-domain and unseen tasks while enabling flexible alignment on different objectives. Moreover, we have demonstrated the potential of GRAPE to align VLA with customized objectives, effectively resulting in an improvement of lower collision rate and average step lengths. 

8 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

# **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

# **References** 

- Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I., Aleman, F. L., Almeida, D., Altenschmidt, J., Altman, S., Anadkat, S., et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- Ajay, A., Du, Y., Gupta, A., Tenenbaum, J. B., Jaakkola, T. S., and Agrawal, P. Is conditional generative modeling all you need for decision making? In _The Eleventh International Conference on Learning Representations_ , 2023. 

- Bai, Y., Jones, A., Ndousse, K., Askell, A., Chen, A., DasSarma, N., Drain, D., Fort, S., Ganguli, D., Henighan, T., et al. Training a helpful and harmless assistant with reinforcement learning from human feedback. _arXiv preprint arXiv:2204.05862_ , 2022. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Bradley, R. A. and Terry, M. E. Rank analysis of incomplete block designs: I. the method of paired comparisons. _Biometrika_ , 39(3/4):324–345, 1952. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., Ding, T., Driess, D., Dubey, A., Finn, C., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 

- Bus¸oniu, L., De Bruin, T., Tolic, D., Kober, J., and Palunko,´ I. Reinforcement learning for control: Performance, stability, and deep approximators. _Annual Reviews in Control_ , 46:8–28, 2018. 

- Cheang, C.-L., Chen, G., Jing, Y., Kong, T., Li, H., Li, Y., Liu, Y., Wu, H., Xu, J., Yang, Y., et al. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ , 2024. 

- Chen, L., Lu, K., Rajeswaran, A., Lee, K., Grover, A., Laskin, M., Abbeel, P., Srinivas, A., and Mordatch, I. Decision transformer: Reinforcement learning via sequence modeling. _Advances in neural information processing systems_ , 34:15084–15097, 2021. 

- Chen, Y., Wu, T., Wang, S., Feng, X., Jiang, J., Lu, Z., McAleer, S., Dong, H., Zhu, S.-C., and Yang, Y. Towards human-level bimanual dexterous manipulation with reinforcement learning. _Advances in Neural Information Processing Systems_ , 35:5150–5163, 2022. 

- Chen, Z., Du, Y., Wen, Z., Zhou, Y., Cui, C., Weng, Z., Tu, H., Wang, C., Tong, Z., Huang, Q., et al. Mjbench: Is your multimodal reward model really a good judge for text-to-image generation? _arXiv preprint arXiv:2407.04842_ , 2024a. 

- Chen, Z., Pinto, F., Pan, M., and Li, B. Safewatch: An efficient safety-policy following video guardrail model with transparent explanations. _arXiv preprint arXiv:2412.06878_ , 2024b. 

- Chen, Z., Zhao, Z., He, T., Chen, B., Zhao, X., Gong, L., and Liu, C. Safe reinforcement learning via hierarchical adaptive chance-constraint safeguards. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2024c. 

- Chen, Z., Zhao, Z., Zhu, Z., Zhang, R., Li, X., Raj, B., and Yao, H. Autoprm: Automating procedural supervision for multi-step reasoning via controllable question decomposition. _arXiv preprint arXiv:2402.11452_ , 2024d. 

- Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., and Song, S. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , pp. 02783649241273668, 2023. 

- Christiano, P. F., Leike, J., Brown, T., Martic, M., Legg, S., and Amodei, D. Deep reinforcement learning from human preferences. _Advances in neural information processing systems_ , 30, 2017. 

- Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle, A., Letman, A., Mathur, A., Schelten, A., Yang, A., Fan, A., et al. The llama 3 herd of models. _arXiv preprint arXiv:2407.21783_ , 2024. 

- Fan, Y., Watkins, O., Du, Y., Liu, H., Ryu, M., Boutilier, C., Abbeel, P., Ghavamzadeh, M., Lee, K., and Lee, K. Reinforcement learning for fine-tuning text-to-image diffusion models. _Advances in Neural Information Processing Systems_ , 36, 2024. 

9 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

- Finn, C., Levine, S., and Abbeel, P. Guided cost learning: Deep inverse optimal control via policy optimization. In _International conference on machine learning_ , pp. 49–58. PMLR, 2016. 

- Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., and Chen, W. LoRA: Low-rank adaptation of large language models. In _International Conference on Learning Representations_ , 2022. URL https:// openreview.net/forum?id=nZeVKeeFYf9. 

- Huang, W., Wang, C., Zhang, R., Li, Y., Wu, J., and Fei-Fei, L. Voxposer: Composable 3d value maps for robotic manipulation with language models. _arXiv preprint arXiv:2307.05973_ , 2023. 

- Huang, W., Wang, C., Li, Y., Zhang, R., and Fei-Fei, L. Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation. _arXiv preprint arXiv:2409.01652_ , 2024. 

- Janner, M., Du, Y., Tenenbaum, J., and Levine, S. Planning with diffusion for flexible behavior synthesis. In _International Conference on Machine Learning_ , pp. 9902–9915. PMLR, 2022. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Kumar, A., Hong, J., Singh, A., and Levine, S. Should i run offline reinforcement learning or behavioral cloning? In _International Conference on Learning Representations_ , 2021. 

- Kumar, A., Zhuang, V., Agarwal, R., Su, Y., Co-Reyes, J. D., Singh, A., Baumli, K., Iqbal, S., Bishop, C., Roelofs, R., et al. Training language models to self-correct via reinforcement learning. _arXiv preprint arXiv:2409.12917_ , 2024. 

- Li, X., Hsu, K., Gu, J., Pertsch, K., Mees, O., Walke, H. R., Fu, C., Lunawat, I., Sieh, I., Kirmani, S., Levine, S., Wu, J., Finn, C., Su, H., Vuong, Q., and Xiao, T. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024a. 

- Li, Y., Deng, Y., Zhang, J., Jang, J., Memmel, M., Garrett, C. R., Ramos, F., Fox, D., Li, A., Gupta, A., and Goyal, A. HAMSTER: Hierarchical action models for open-world robot manipulation. In _1st Workshop on X-Embodiment Robot Learning_ , 2024b. URL https: //openreview.net/forum?id=yF3UekSJus. 

- Liang, J., Huang, W., Xia, F., Xu, P., Hausman, K., Ichter, B., Florence, P., and Zeng, A. Code as policies: Language model programs for embodied control. In _2023 IEEE_ 

_International Conference on Robotics and Automation (ICRA)_ , pp. 9493–9500. IEEE, 2023a. 

- Liang, Z., Mu, Y., Ding, M., Ni, F., Tomizuka, M., and Luo, P. Adaptdiffuser: Diffusion models as adaptive self-evolving planners. In _International Conference on Machine Learning_ , pp. 20725–20745. PMLR, 2023b. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _arXiv preprint arXiv:2306.03310_ , 2023. 

- Mu, Y., Chen, J., Zhang, Q.-L., Chen, S., Yu, Q., Chongjian, G., Chen, R., Liang, Z., Hu, M., Tao, C., et al. Robocodex: Multimodal code generation for robotic behavior synthesis. In _Forty-first International Conference on Machine Learning_ , 2024a. 

- Mu, Y., Zhang, Q., Hu, M., Wang, W., Ding, M., Jin, J., Wang, B., Dai, J., Qiao, Y., and Luo, P. Embodiedgpt: Vision-language pre-training via embodied chain of thought. _Advances in Neural Information Processing Systems_ , 36, 2024b. 

- O’Neill, A., Rehman, A., Gupta, A., Maddukuri, A., Gupta, A., Padalkar, A., Lee, A., Pooley, A., Gupta, A., Mandlekar, A., et al. Open x-embodiment: Robotic learning datasets and rt-x models. _arXiv preprint arXiv:2310.08864_ , 2023. 

- Oquab, M., Darcet, T., Moutakanni, T., Vo, H., Szafraniec, M., Khalidov, V., Fernandez, P., Haziza, D., Massa, F., ElNouby, A., et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 

- Oquab, M., Darcet, T., Moutakanni, T., Vo, H., Szafraniec, M., Khalidov, V., Fernandez, P., Haziza, D., Massa, F., El-Nouby, A., Assran, M., Ballas, N., Galuba, W., Howes, R., Huang, P.-Y., Li, S.-W., Misra, I., Rabbat, M., Sharma, V., Synnaeve, G., Xu, H., Jegou, H., Mairal, J., Labatut, P., Joulin, A., and Bojanowski, P. Dinov2: Learning robust visual features without supervision, 2024. URL https://arxiv.org/abs/2304.07193. 

- Rafailov, R., Sharma, A., Mitchell, E., Manning, C. D., Ermon, S., and Finn, C. Direct preference optimization: Your language model is secretly a reward model. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- Ravi, N., Gabeur, V., Hu, Y.-T., Hu, R., Ryali, C., Ma, T., Khedr, H., Radle,¨ R., Rolland, C., Gustafson, L., Mintun, E., Pan, J., Alwala, K. V., Carion, N., Wu, C.-Y., Girshick, R., Dollar,´ P., and Feichtenhofer, C. Sam 2: Segment anything in images and videos. _arXiv_ 

10 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

_preprint arXiv:2408.00714_ , 2024. URL https:// arxiv.org/abs/2408.00714. 

- Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and Klimov, O. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- Sutton, R. S. Reinforcement learning: An introduction. _A Bradford Book_ , 2018. 

- Team, O. M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- Walke, H. R., Black, K., Zhao, T. Z., Vuong, Q., Zheng, C., Hansen-Estruch, P., He, A. W., Myers, V., Kim, M. J., Du, M., et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pp. 1723–1736. PMLR, 2023. 

- Wang, C., Zhao, Z., Zhu, C., Sankararaman, K. A., Valko, M., Cao, X., Chen, Z., Khabsa, M., Chen, Y., Ma, H., et al. Preference optimization with multi-sample comparisons. _arXiv preprint arXiv:2410.12138_ , 2024a. 

- Wang, C., Zhao, Z., Jiang, Y., Chen, Z., Zhu, C., Chen, Y., Liu, J., Zhang, L., Fan, X., Ma, H., et al. Beyond reward hacking: Causal rewards for large language model alignment. _arXiv preprint arXiv:2501.09620_ , 2025. 

   - Zhai, Y., Bai, H., Lin, Z., Pan, J., Tong, S., Zhou, Y., Suhr, A., Xie, S., LeCun, Y., Ma, Y., et al. Fine-tuning large vision-language models as decision-making agents via reinforcement learning. _arXiv preprint arXiv:2405.10292_ , 2024. 

   - Zhou, C., Yu, L., Babu, A., Tirumala, K., Yasunaga, M., Shamis, L., Kahn, J., Ma, X., Zettlemoyer, L., and Levy, O. Transfusion: Predict the next token and diffuse images with one multi-modal model. _arXiv preprint arXiv:2408.11039_ , 2024a. 

   - Zhou, Y., Fan, Z., Cheng, D., Yang, S., Chen, Z., Cui, C., Wang, X., Li, Y., Zhang, L., and Yao, H. Calibrated self-rewarding vision language models. _arXiv preprint arXiv:2405.14622_ , 2024b. 

   - Zhu, H., Gupta, A., Rajeswaran, A., Levine, S., and Kumar, V. Dexterous manipulation with deep reinforcement learning: Efficient, general, and low-cost. In _2019 International Conference on Robotics and Automation (ICRA)_ , pp. 3651–3657. IEEE, 2019. 

   - Ziegler, D. M., Stiennon, N., Wu, J., Brown, T. B., Radford, A., Amodei, D., Christiano, P., and Irving, G. Fine-tuning language models from human preferences. _arXiv preprint arXiv:1909.08593_ , 2019. 

- Wang, S., Chen, Z., Zhao, Z., Mao, C., Zhou, Y., He, J., and Hu, A. S. EscIRL: Evolving self-contrastive IRL for trajectory prediction in autonomous driving. In _8th Annual Conference on Robot Learning_ , 2024b. URL https: //openreview.net/forum?id=1IzW0aniyg. 

- Wu, T., Gan, Y., Wu, M., Cheng, J., Yang, Y., Zhu, Y., and Dong, H. Unidexfpm: Universal dexterous functional pregrasp manipulation via diffusion policy. _arXiv preprint arXiv:2403.12421_ , 2024. 

- Xian, Z., Gkanatsios, N., Gervet, T., Ke, T.-W., and Fragkiadaki, K. Chaineddiffuser: Unifying trajectory diffusion and keypose prediction for robotic manipulation. In _7th Annual Conference on Robot Learning_ , 2023. 

- Yang, Z., Teng, J., Zheng, W., Ding, M., Huang, S., Xu, J., Yang, Y., Hong, W., Zhang, X., Feng, G., et al. Cogvideox: Text-to-video diffusion models with an expert transformer. _arXiv preprint arXiv:2408.06072_ , 2024. 

- Ye, S., Jang, J., Jeon, B., Joo, S., Yang, J., Peng, B., Mandlekar, A., Tan, R., Chao, Y.-W., Lin, B. Y., et al. Latent action pretraining from videos. _arXiv preprint arXiv:2410.11758_ , 2024. 

11 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

# **A. Additional Description of GRAPE and Hyperparameter Settings** 

**Customized Cost Generation.** In our real-world experiments, we first input image-text pairs containing prompts and initial states into the Vision-Language Model (VLM) Hamster (Li et al., 2024b). Using the stage information and stage points generated by Hamster, we segmented the collected trajectories. This helps analyze complex task sequences more precisely, giving detailed attention to each stage. And we utilized Grounded-SAM (Ravi et al., 2024) or methods combining SAM (Ravi et al., 2024) and DinoV2 (Oquab et al., 2024) to extract key point information from the images. These key points, combined with our self-collected trajectory data, enable us to refine the execution steps and path planning of tasks based on the stage information generated by the Hamster model. For example, for a simple pick-and-place task, we can decompose it into multiple explicit stages: Grasp the grape, Move the grape onto the plate, Place the grape on the plate. 

To generate detailed operational information and cost functions for each stage, we utilized GPT-4o (Achiam et al., 2023) with customized prompts. This approach makes stage planning more precise and efficient, allowing us to meet specific task requirements and constraints. Furthermore, we enhanced our method by incorporating various task-specific constraints, including: **Collision constraints:** Ensuring the robot avoids collisions with obstacles. **Path constraints:** Optimizing the efficiency and safety of the robot’s movement path. By adopting this strategy, we achieve greater flexibility and specificity in task planning, and better adapting to different task scenarios. 

**Iterative Preference Optimization.** For Iterative Preference Optimization, we first utilize the fine-tuned VLA model for online data sampling. For each task, we sample _Nt_ trajectories to facilitate further selection. To simplify the experimental setup, we set _Nt_ = 5 for each task, which has been found to perform effectively in practice. 

After sampling, each trajectory is automatically labeled using the GCPG reward, as defined in Eq. (9). Based on the distribution of _R_ self, _R_ ext, and _I_ success observed in preliminary experiments, we set _λ_ 1 = 0 _._ 01, _λ_ 2 = 0 _._ 01, and _λ_ 3 = 2. These values ensure that _R_ self, _R_ ext, and _I_ success contribute comparably to the final reward value. Subsequent experiments validate the reasonableness of these parameter choices. Using the GCPG reward assigned to each trajectory, we identify the trajectory with the highest reward as _yw_ and the trajectory with the lowest reward as _yl_ for each task. This selection process enables the construction of the TPO Dataset, _Dtraj_ , for TPO training. 

For the TPO training process, we employ LoRA (Hu et al., 2022) and the AdamW optimizer, setting the learning rate to 2 _×_ 10<sup>_−_5</sup> and the batch size to 16. The model is trained for a single epoch before being utilized for iterative online sampling. During iterative online sampling, the experimental settings remain consistent with the aforementioned descriptions. 

# **B. Detail Experiment Datasets** 

In this section, we describe the datasets collected for supervised fine-tuning (referred to as the SFT dataset) and preference alignment (referred to as the TPO dataset). 

## **B.1. Real-World Dataset** 

**SFT Dataset.** In our real-world robot experiments, we use a robotic platform composed of a Franka robotic arm and a Robotiq gripper for data collection. To ensure consistency in data collection and evaluation, all operations are performed in the same experimental environment. 

During data collection, we gathered a dataset of 220 instances of pick and place tasks involving common objects such as bananas, corn, milk, and salt. Additionally, we collected data on 50 instances of tasks involving pressing buttons of different colors. Since the number of objects used for the button-pressing tasks is limited, we introduced background noise and interfering objects during the testing phase to create unseen scenarios. 

To further enhance the capabilities of OpenVLA in handling different actions, we also collected data on 50 instances of knock down tasks. These diverse task datasets help improve the model’s generalization ability in processing different types of actions. 

**TPO Dataset.** In the real-world experiments, we utilized a model fine-tuned on the real-world SFT dataset via OpenVLA for trajectory sampling. Each task was conducted five times. In the TPO dataset, we experimented with 15 different tasks, including 10 pick and place tasks, 3 push button tasks, and 2 knock down tasks, accumulating a total of 75 data entries. After a selection process, we derived a preference dataset consisting of 30 trajectories. 

12 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

## **B.2. Simulation Datasets** 

**SFT Dataset:** For Simpler-Env, the SFT dataset comprises 100 trajectories, amounting to approximately 2,900 transitions. These rollouts are generated from Simpler-Env using Octo, following the methodology described in Ye et al. (2024). For LIBERO, it is worth noting that we neither collect new data nor fine-tune the OpenVLA model. Instead, we directly utilize the OpenVLA-SFT model provided by the OpenVLA team, which significantly streamlines the pipeline. 

**TPO Dataset.** In the case of Simpler-Env, trajectories are sampled for each task using the OpenVLA-SFT model, with five trials conducted per task. This process yields a TPO dataset consisting of 80 trajectories. For LIBERO, OpenVLA-SFT models (one model per task) are employed to sample data across four tasks in LIBERO. For each task, five trajectories are sampled for each sub-task, resulting in a TPO dataset comprising a total of 20 trajectories. 

# **C. Detailed Experiment Settings and Additional Result** 

## **C.1. Real-World** 

## C.1.1. REAL-WORLD EXPERIMENT SETUP 

In real-world experiment, we used the Franka robot arm, which is known for its precision and flexibility. However, we encountered a problem with the original Franka gripper, which was not long enough, limiting our ability to handle some of the tasks, resulting in inefficient completion and a high failure rate. To solve this problem, we decided to replace the original Franka grippers with Robotiq grippers, which are not only longer, but also provide more grip and flexibility, which greatly improves the efficiency and success rate of the tasks. 

The purpose of this experiment was to assess the cross-task generalization capabilities of OpenVLA under the GRAPE framework and to compare its performance with several baseline models. Considering the generally poor zero-shot generalization performance of most VLA models, we performed supervised fine-tuning using the comprehensive rollout dataset _Dr_ collected from real scenes to construct a fine-tuned model. The selection of baseline models included those adjusted with domain-specific data, as well as the Octo model, RVT-2 model, and OpenVLA-SFT model. 

## C.1.2. REAL-WORLD TASKS 

As shown in Figure 5, we performed a comprehensive evaluation on a real machine for several tasks. These tasks cover five different generalization scenarios: Visual Generalization, Subject Generalization, Action Generalization, Semantics Generalization, and Language Grounding. Specifically, for each generalization scenario, we set the following tasks: 

- **Visual Generalization** includes 8 tasks, e.g., pick up the GRAPE and put it in the black bowl, with noise objects and noisy backgrounds. Some tasks have only noisy backgrounds. 

- **Subject Generalization** includes 4 tasks, e.g., pick up the K and put it in the black bowl. 

- **Action Generalization** includes 7 tasks, e.g., fold the green towel from right to left . 

- **Semantics Generalization** includes 4 tasks, e.g., stack carrot and put it on the blue plates. 

- **Language Grounding** includes 3 tasks, e.g., pick up left object to left plate. 

We conducted experiments on 30 total different tasks, attempting each task ten times, totaling 300 executions. To ensure fairness in the evaluation, we maintained the same starting position in each model test. Additionally, we matched the image resolution when training all models and used exactly the same initial object positions in all evaluations. We set specific success criteria for each task. For example, in the pick-and-place task, a successful grasp is defined as successfully grasping the target object. In the push-button and knock-down tasks, a successful grasp is defined as correctly approaching and manipulating the target object. Overall task success is defined as the object being accurately placed at the target location, successfully knocked down, or the target button being successfully pressed. Due to the strictness of these criteria, some models found it difficult to achieve success in specific tasks. 

13 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

Table 3: Comparison of GRAPE models in diffierent iteration rounds. We assess their performance in in-domain tasks and three kinds of generalization evaluations. Each task’s performance is evaluated on the overall grasp rate and success rate. 

||**In-do**<br>Grasp|**main**<br>Success|**Subjec**<br>Grasp|**t Gen.**<br>Success|**Physica**<br>Grasp|**l Gen.**<br>Success|**Semant**<br>Grasp|**ics Gen.**<br>Success|**Ave**<br>Grasp|**rage**<br>Success|
|---|---|---|---|---|---|---|---|---|---|---|
|Iter-1|71.00%|43.00%|62.67%|**40.67**%|63.50%|41.75%|72.00%|47.00%|67.29%|43.11%|
|Iter-2|74.00%|45.00%|64.33%|40.33%|65.75%|44.25%|**76.00%**|**49.50%**|70.02%|44.77%|
|Iter-3|**74.50%**|**45.50%**|**64.67%**|**40.67%**|**66.00%**|**44.50%**|**76.00%**|49.00%|**70.29%**|**44.92%**|


## **C.2. Simulation Experiments** 

## C.2.1. SIMPLER-ENV 

We utilize Simpler-Env (Li et al., 2024a) as the experimental environment in our study. SIMPLER (Li et al., 2024a) (Simulated Manipulation Policy Evaluation for Real Robot Setups) is a collection of simulated environments created to assess robot manipulation policies in a way that closely reflects real-world scenarios. By leveraging simulated environments, SIMPLER effectively serves as a practical alternative to real-world testing, which is often costly, time-consuming, and challenging to replicate. 

**Simpler-Env Tasks.** In our paper, we use four in-domain tasks from WidowX robot in Simpler-Env. We also design three kinds of generalization tasks in Simpler-Env. These tasks are described below: 

## **In-Domain Tasks Shown in Fig. 3:** 

1. Put Carrot on Plate: The robot is positioned in front of a platform with a plate and a carrot. The robot’s goal is to grasp the carrot and put it onto the plate. 

2. Put Eggplant in basket: The robot is positioned in front of a sink with a basket and a Eggplant. The robot’s goal is to grasp the Eggplant and put it in the basket. 

3. Stack Green Cube on Yellow Cube: The robot is positioned in front of a platform with a green cube and a yellow cube. The robot’s goal is to grasp the green cube and stack it on the yellow cube. 

4. Put Spoon on towel: The robot is positioned in front of a platform with a spoon and a towel. The robot’s goal is to grasp the spoon and put it on the towel. 

## **Three Kinds of Generalization Tasks Shown in Fig. 3:** 

1. Subject Generalization: The robot is positioned in front of a platform, similar to the environment in in-domain tasks. But the robot’s goal is to grasp some new objects(i.e. pepsi can, coke can, sprite can) and put it onto the plate. 

2. Physical Generalization: The robot is positioned in front of a platform, similar to the environment in in-domain tasks. But the robot’s goal is to grasp some original objects with different sizes and collision boxes, then put it onto the plate. 

3. Semantics Generalization: The robot is positioned in front of a platform, similar to the environment in in-domain tasks. And the instruction is similar to in-domain tasks, too. But the instruction has been modified by GPT-4o (Achiam et al., 2023) while maintaining its original meaning. 

## C.2.2. LIBERO 

We further utilize LIBERO (Liu et al., 2023) as the experimental environment in our study. LIBERO (LIfelong learning BEnchmark on RObot manipulation tasks) includes a set of 130 language-conditioned robot manipulation tasks inspired by human activities, organized into four distinct suites. Each suite is crafted to examine distribution shifts in object types, spatial arrangements of objects, task goals, or a combination of these factors. LIBERO is built to be scalable, extendable, and specifically tailored for advancing research in lifelong learning for robotic manipulation. 

**LIBERO tasks** In our paper, we use four in-domain tasks from LIBERO, which are shown in Fig. 4. These tasks is described below: 

14 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

- **LIBERO-Spatial** includes the same set of objects arranged in various layouts, testing the model’s ability to understand spatial relationships. 

- **LIBERO-Object** features consistent scene layouts with varying objects, evaluating the model’s ability to understand different object types. 

- **LIBERO-Goal** includes of the same objects and layouts but different task goals, testing the model’s knowledge of different task-oriented behaviors. 

- **LIBERO-10** consists of long-horizon tasks with diverse objects, layouts, and tasks. 

Eash task mentioned above has 10 sub-tasks, with similar task instructions and scenes. Here are some cases from various LIBERO tasks: 

- Open the top drawer of the cabinet and put the bowl in it. 

- Pick up the book and place it to the right of the caddy. 

- Turn on the stove and put the frying pan on it. 

- Stack the right bowl on the left bowl and place them in the tray. 

# **D. Additional Real-World and Simulation Results** 

We provide additional results in Table 4 , Table 5, and Figure 12 with detailed task description. Each table has in-domain tasks and several kinds of generalization evaluations. These experiments are conducted across Octo-SFT, OpenVLA-SFT and GRAPE. 

# **E. Case Study** 

## **E.1. Case Study of Real-World Generation Tasks** 

We provide an illustration for each specific task included in the suite evaluation for _in-domain_ tasks in Figure 8 and for each type of generation task, including _subject generalization_ in Figure 9, _language grounding_ in Figure 13, _visual generalization_ in Figure 10, _action generalization_ in Figure 11, and _semantic generalization_ in Figure 12. Specifically, we demonstrate the initial and final states of GRAPE in handling each of these challenging tasks, as detailed in the corresponding captions. In addition, we include a safety task to demonstrate how GRAPE adheres to safety requirements once aligned with safety constrains. 

15 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 


Figure 8: Illustrations of real-world tasks that we evaluated for _in-domain capabilities_ , where we report the detailed results in Table 4. 4.. Specifically, we demonstrate the initial and final state of GRAPE in handling each of the four challenging tasks detailed in the captions. 

Figure 9: Illustrations of real-world tasks that we evaluated for _subject generation_ , where we report the detailed results in Table 4. Specifically, we demonstrate the initial and final state of GRAPE in handling each of the four challenging tasks detailed in the captions. 

16 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 


Figure 10: Illustrations of real-world tasks that we evaluated for _visual generation_ , where we report the detailed results in Table 4. Specifically, we demonstrate the initial and final state of GRAPE in handling each of the eight challenging tasks detailed in the captions. 

17 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 


Figure 11: Illustrations of real-world tasks that we evaluated for _action generation_ , where we report the detailed results in Table 4. Specifically, we demonstrate the initial and final state of GRAPE in handling each of the seven challenging tasks detailed in the captions. 

18 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 


Figure 12: Illustrations of real-world tasks that we evaluated for _semantic generation_ , where we report the detailed results in Table 4. 4.. Specifically, we demonstrate the initial and final state of GRAPE in handling each of the four challenging tasks detailed in the captions. 

Figure 13: Illustrations of real-world tasks that we evaluated for _language generation_ , where we report the detailed results in Table 4. Specifically, we demonstrate the initial and final state of GRAPE in handling each of the five challenging tasks detailed in the captions. 

19 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 


Figure 14: Illustrations of real-world tasks used for safety evaluation, extending the tasks presented in Figure 7. The figure shows key frames from GRAPE’s trajectory in two challenging scenarios. Due to the lack of safety reward alignment, the OpenVLA-SFT approach fails, while GRAPE-Safety successfully navigates obstacles and completes the task once the safety rewards are properly aligned. 

20 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

Table 4: We present the performance of various action policy on real-world robotic manipulation tasks categorized by different types of generalization. The tasks include in-domain, visual generalization with and without noise, subject generalization, action generalization, semantics generalization, and language grounding. Each task’s performance is evaluated based on the number of successful grasps and the overall success rate, comparing results from Octo-SFT, OpenVLA-SFT, OpenVLA-DPO, and GRAPE. Average success rates are calculated for each generalization category to demonstrate the effectiveness of the tested models under different conditions. 

|**Generalization**|**Task**|**Octo**|**-SFT**|**OpenV**|**LA-SFT**|**OpenV**|**LA-DPO**|**GR**|**APE**|
|---|---|---|---|---|---|---|---|---|---|
|||Grasp|Success|Grasp|Success|Grasp|Success|Grasp|Success|
||pick up the corn and put it in the black bowl|3|3|2|2|5|3|8|7|
||pick up the banana and put it in the black bowl|2|0|6|6|8|6|9|7|
|In-domain|pick up the milk and put it in the white bowl|4|2|10|8|8|8|9|9|
||pick up the salt bottle and put it in the white bowl|4|3|4|2|5|3|6|4|
||Average|32.5%|20%|55%|45%|65%|50%|**80%**|**67.5%**|
||pick up the corn and put it in the black bowl|2|1|6|3|6|4|6|6|
||pick up the banana and put it in the black bowl|0|0|3|2|4|1|4|1|
|Visual Generalization|pick up the milk and put it in the white bowl|4|0|4|4|6|6|9|7|
|(w/o noise background)|pick up the salt bottle and put it in the white bowl|2|2|6|5|6|6|8|8|
||pick up the GRAPE and put it in the black bowl|0|0|6|5|8|5|8|6|
||Average|16%|6%|50%|38%|60%|44%|**70%**|**56%**|
||pick up the GRAPE and put it in the black bowl|1|0|4|2|5|3|6|4|
|Visual Generalization|pick up the milk and put it in the white bowl|2|1|7|5|6|4|5|4|
|(w/o noise background and object)|pick up the salt bottle and put it in the white bowl|0|0|2|2|6|5|8|8|
||Average|10%|3.3%|43.3%|30%|56.7%|40%|**63.3%**|**53.3%**|
||pick up the chips and put it in the red bowl|4|0|2|2|4|3|6|5|
||pick up the K and put it in the black bowl|2|0|4|4|6|5|7|6|
|Subject Generalization)|pick up the box juice and put it in the yellow plate|2|0|8|3|8|5|8|6|
||pick up the Fanta can and put it in the white bowl|2|2|4|1|5|2|6|4|
||Average|25%|5%|45%|25%|57.5%|37.5%|**67.5%**|**52.5%**|
||push down the blue button|1|0|4|4|6|4|6|6|
||push down the green button|1|0|6|4|7|5|4|4|
||push yellow the button|2|2|6|3|7|4|8|5|
|Action Generalization|knock down the green bottle|3|1|2|2|3|2|4|2|
||knock down the popcorn|0|0|4|2|4|3|4|3|
||fold the green towel from right to left|1|0|2|1|3|1|4|2|
||fold the white towel from left to right|1|0|3|1|4|2|4|3|
||Average|12.9%|4.3%|38.6%|24.3%|**48.6%**|30%|**48.6%**|**35.7%**|
||take green pepper and place it in the black bowl|0|0|10|6|9|7|10|8|
||move icecream and put it in the red bowl|0|0|6|4|5|4|4|4|
|Semantics Generalization|stack carrot and put it on the blue plates|0|0|8|8|6|5|6|6|
||Lift GRAPE and place it in the black bowl|0|0|2|0|3|2|2|2|
||Average|0%|0%|**65%**|45%|57.5%|45%|55%|**50%**|
||pick up left object to left plate|0|0|4|0|5|1|5|2|
||<br>push down right button|0|0|6|2|6|5|8|7|
|Language Grounding|<br>pick up right object to right plate|0|0|4|4|5|4|6|5|
||Average|0%|0%|46.7%|20%|53.3%|33.3%|**63.3%**|**46.7%**|
|Total Average||14.3%|5.7%|48.3%|32.3%|56.3%|39.3%|**62.6%**|**50.3%**|


21 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

Table 5: We compared the performance of Octo-SFT, OpenVLA-SFT, and GRAPE across various robotic tasks within in-domain, subject, physical, and semantics generalization categories. It shows grasp percentages and success rates for each task, illustrating how each VLA performs under different generalizations. 

|**Generalization**|**Task**|**Octo**<br>Grasp|**-SFT**<br>Success|**OpenVL**<br>Grasp|**A-SFT**<br>Success|**OpenV**<br>Grasp|**LA-DPO**<br>Success|**GR**<br>Grasp|**APE**<br>Success|
|---|---|---|---|---|---|---|---|---|---|
||put the carrot on the plate|32.00%|16.00%|36.00%|30.00%|46.00%|36.00%|**68.00%**|**48.00%**|
||put the eggplant in the basket|70.00%|44.00%|58.00%|32.00%|70.00%|36.00%|**84.00%**|**48.00%**|
|In-domain|stack the green cube on the yellow cube|52.00%|0.00%|56.00%|20.00%|52.00%|26.00%|**76.00%**|**40.00%**|
||put the spoon on the towel|54.00%|**36.00%**|52.00%|28.00%|52.00%|30.00%|**56.00%**|34.00%|
||Average|52.00%|24.00%|50.50%|28.00%|55.00%|32.00%|**71.00%**|**43.00%**|
||put the coke can on the towel|24.00%|14.00%|60.00%|**38.00%**|66.00%|36.00%|**78.00%**|32.00%|
|Subject Generalization|put the pepsi can on the towel|28.00%|16.00%|58.00%|38.00%|60.00%|42.00%|**64.00%**|**50.00%**|
|(unseen objects)|put the sprite can on the towel|24.00%|12.00%|**62.00%**|22.00%|58.00%|26.00%|46.00%|**40.00%**|
||Average|25.33%|14.00%|60.00%|32.67%|61.33%|34.66%|**62.67%**|**40.67%**|
||put the carrot on the plate(size:0.5)|38.00%|22.00%|56.00%|38.00%|60.00%|46.00%|**78.00%**|**64.00%**|
||put the carrot on the plate(size:1.1)|26.00%|12.00%|32.00%|24.00%|42.00%|30.00%|**64.00%**|**42.00%**|
||put the carrot on the plate(wider collision box)|28.00%|16.00%|34.00%|26.00%|46.00%|32.00%|**62.00%**|**42.00%**|
|Phil Gliti|put the carrot on the plate(longer collision box)|32.00%|14.00%|38.00%|30.00%|50.00%|36.00%|**66.00%**|**48.00%**|
|ysca enerazaon<br>|put the spoon on the towel(size:0.5)|62.00%|38.00%|66.00%|**40.00%**|66.00%|38.00%|**72.00%**|38.00%|
|(unseen object sizes/shapes)|put the spoon on the towel(size:1.1)|52.00%|**32.00%**|50.00%|28.00%|**58.00%**|**32.00%**|56.00%|30.00%|
||put the spoon on the towel(wider collision box)|48.00%|30.00%|44.00%|24.00%|46.00%|28.00%|**50.00%**|**32.00%**|
||put the spoon on the towel(longer collision box)|56.00%|36.00%|54.00%|26.00%|54.00%|28.00%|**60.00%**|**38.00%**|
||Average|42.75%|25.00%|46.75%|29.50%|52.75%|33.75%|**63.50%**|**41.75%**|
||put the vegetable on the plate|16.00%|6.00%|32.00%|28.00%|40.00%|32.00%|**66.00%**|**48.00%**|
|Semantics Generalization|move the eggplant into the basket|18.00%|8.00%|50.00%|30.00%|56.00%|34.00%|**78.00%**|**44.00%**|
|(unseen instructions)|put the green cube onto the yellow cube|32.00%|6.00%|62.00%|26.00%|74.00%|42.00%|**88.00%**|**60.00%**|
||place the spoon onto the towel|42.00%|26.00%|48.00%|28.00%|48.00%|30.00%|**56.00%**|**36.00%**|
||Average|27.00%|11.50%|48.00%|28.00%|54.50%|34.50%|**72.00%**|**47.00%**|
|Total average||36.77%|18.63%|51.44%|29.54%|55.90%|33.73%|**67.29%**|**43.11%**|


22 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

## **E.2. Case Study of Multi-stage Cost Functions** 

We demonstrate some case studies of the multi-stage cost functions generated using our proposed pipeline given different alignment objectives. 

## E.2.1. TASK COMPLETION 

## **Cost Functions for Task Completion Alignment** 

# The task involves picking up the grape and placing it in the black bowl. # The stages involved are: # 1. Grasp grape # 2. Move grape to black bowl # 3. Drop grape in black bowl num_stages = 3 ### stage 1: Grasp grape def stage1_target_constraint1(end_effector, keypoints): """Align the end-effector with the grape’s center.""" grape_center = keypoints[0] target_cost = np.linalg.norm(end_effector - grape_center) return target_cost ### stage 2: Move grape to black bowl def stage2_target_constraint1(end_effector, keypoints): """Calculate the relative distance between grape and black bowl.""" black_bowl_center = keypoints[1]# Assuming keypoint 1 is the black bowl target_cost = np.linalg.norm(end_effector - black_bowl_center) return target_cost ### stage 3: Drop grape in black bowl def stage3_target_constraint1(end_effector, keypoints): """Ensure the grape rests in the black bowl.""" black_bowl_center = keypoints[1] target_cost = np.linalg.norm(end_effector - black_bowl_center) return target_cost 

## E.2.2. SAFETY 

## **Cost Functions for Cost-Efficiency Alignment** 

# The task involves picking up the grape and placing it in the black bowl. # The stages involved are: # 1. Grasp grape # 2. Move grape to black bowl # 3. Drop grape in black bowl 

23 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

num_stages = 3 ### stage 1: Grasp grape def stage1_collision_constraint1(end_effector, keypoints): """Approach the grape from above to avoid collision.""" grape_center = keypoints[0] collision_cost = 0 if end_effector[1] > grape_center[1] else 1 return collision_cost ### stage 2: Move grape to black bowl def stage2_collision_constraint1(end_effector, keypoints): """Ensure the grape is aligned above the black bowl.""" obstacles = keypoints[2:]#Assuming keypoints[2:] are obstacles threshold = 0.1 # Minimum allowable clearance collision_cost = sum( max(0, threshold - np.linalg.norm(end_effector - obstacle)) for obstacle in obstacles ) return collision_cost ### stage 3: Drop grape in black bowl def stage3_collision_constraint1(end_effector, keypoints): """Approach the grape from above to avoid collision.""" black_bowl_center = keypoints[1] collision_cost = 0 if end_effector[1] > black_bowl_center[1] else 1 return collision_cost 

## E.2.3. COST-EFFICIENCY 

## **Cost Functions for Safety Alignment** 

# The task involves picking up the grape and placing it in the black bowl. # The stages involved are: # 1. Grasp grape # 2. Move grape to black bowl # 3. Drop grape in black bowl num_stages = 3 ### stage 1: Grasp grape def stage1_path_constraint1(end_effector, keypoints): """Align the end-effector with the grape’s center.""" grape_center = keypoints[0] 

24 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

distance = np.linalg.norm(end_effector - grape_center) step_size = 0.01 # Assuming a small step size path_cost = int(distance / step_size) return path_cost ### stage 2: Move grape to black bowl def stage2_path_constraint1(end_effector, keypoints): """Calculate the relative distance between grape and black bowl.""" black_bowl_center = keypoints[1]# Assuming keypoint 1 is the black bowl distance = np.linalg.norm(end_effector - black_bowl_center) step_size = 0.01 # Assuming a small step size path_cost = int(distance / step_size) return path_cost ### stage 3: Drop grape in black bowl def stage3_path_constraint1(end_effector, keypoints): """Ensure the grape rests in the black bowl.""" black_bowl_center = keypoints[1] distance = np.linalg.norm(end_effector - black_bowl_center) step_size = 0.01 # Assuming a small step size path_cost = int(distance / step_size) return path_cost 

25 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

## **Prompt Template for Multi-stage Cost Proposal** 

**USER** : **Instructions** 

The image shows a robot stage point in a workspace, each point in the diagram represents the point of the stage split: 

- Stage ~~p~~ oint ~~0~~ : Represents the initial position of the carrot. 

- Stage ~~p~~ oint ~~1~~ : Represents the intermediate position above the carrot for grasping. 

Determine how many stages are involved in the task. Grasping must be an independent stage. Some examples: 

1. TASK: PUT THE CARROT ON THE PLATE 

## **Stages:** 

- **Grasp carrot** 

- **Move carrot to plate** 

- **Drop carrot on plate** 

## **Stage 1: Grasp carrot** 

- **Path constraints** : 

   - Align the end-effector with the carrot’s center. 

- **Collision constraints** : 

   - The end-effector must approach the carrot from above to avoid collision. 

## **Stage 2: Move carrot to plate** 

- **Path constraints** : 

   - Calculate the relative distance between carrot and plate. 

- **Collision constraints** : 

   - The carrot is aligned above the plate. 

## **Stage 3: Drop carrot on plate** 

- **Path constraints** : 

   - The carrot must rest on the plate. 

   - The carrot should not bounce out of the basket. 

- **Collision constraints** : 

   - The end-effector must approach the carrot from above to avoid collision. 

## **Note:** 

- Sum all Path constraints cost the path_cost variable. 

- Sum all Grasp constraints cost the grasp_cost variable. 

- Sum all Collision constraints cost the collision_cost variable. 

- Each constraint function takes an end-effector point and a set of keypoints as input, returning a numerical cost. The constraint is satisfied if this cost is zero or less. 

- Define any number of path constraints per stage, but avoid using ”if” statements in the functions. 

- Avoid using path constraints when manipulating deformable objects (e.g., towels). 

- Input format: 

   - end_effector: np.array of shape (3,) representing the end-effector position. 

   - keypoints: np.array of shape (K, 3) representing the keypoints positions. 

- Use Python and NumPy functions freely in constraint functions. 

- Use pairs of keypoints to create vectors if needed. 

- Keypoints are indexed starting from 0, matching their order in the keypoints array. 

26 

**GRAPE: Generalizing Robot Policy via Preference Alignment** 

**Structure your output in a single Python code block as follows:** 

# ... num_stages = ? ### stage 1 path constraints (if any) def stage1_path_constraint1(end_effector, keypoints): """Put your explanation here.""" ... return path_cost # Add more constraints if needed ... ### stage 1 collision constraints (if any) def stage1_collision_constraint1(end_effector, keypoints): """Put your explanation here.""" ... return collision_cost # Add more constraints if needed ... # Repeat for more stages ... 

**Query** Query Task: ” _{_ instruction _}_ ” Query Image: 

27 

