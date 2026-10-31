---
title: "Towards Long-Lived Robots: Continual Learning VLA Models via Reinforcement Fine-Tuning"
date: "2026-02-11"
authors: "Yuan Liu; Haoran Li; Shuai Tian; Yuxing Qin; Yuhui Chen; Yupeng Zheng"
venue: "RSS 2026"
url: https://arxiv.org/abs/2602.10503
pdf: https://arxiv.org/pdf/2602.10503
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.10503)** / [論文ページ](https://arxiv.org/abs/2602.10503)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Towards Long-Lived Robots: Continual Learning VLA Models via Reinforcement Fine-Tuning 

Yuan Liu<sup>1,2†</sup> , Haoran Li<sup>1,3,4 �</sup> , Shuai Tian<sup>1,3</sup> , Yuxing Qin<sup>1,3</sup> , Yuhui Chen<sup>1,3</sup> , Yupeng Zheng<sup>1,3</sup> , 

Yongzhen Huang<sup>2</sup> , Dongbin Zhao<sup>1,3,4</sup> 

> 1SKL-MAIS, Institute of Automation, Chinese Academy of Sciences (CASIA), Beijing, China 

   - 2School of Artificial Intelligence, Beijing Normal University, Beijing, China 

- 3School of Artificial Intelligence, University of Chinese Academy of Sciences, Beijing, China 

> 4Beijing Academy of Artificial Intelligence, Beijing, China 


Fig. 1: **Overview of VLA post-training.** This phase involves single-stage multi-task adaptation and incremental continual learning. Addressing the substantial data dependence and susceptibility to catastrophic forgetting inherent in SFT, we introduce LifeLong-RFT, which combines on-policy RL with the multi-dimensional process reward mechanism. 

**_Abstract_ —Pretrained on large-scale and diverse datasets, VLA models demonstrate strong generalization and adaptability as general-purpose robotic policies. However, Supervised FineTuning (SFT), which serves as the primary mechanism for adapting VLAs to downstream domains, requires substantial amounts of task-specific data and is prone to catastrophic forgetting. To address these limitations, we propose LifeLong-RFT, a simple yet effective Reinforcement Fine-Tuning (RFT) strategy for VLA models independent of online environmental feedback and pretrained reward models. By integrating chunking-level on-policy reinforcement learning with the proposed multi-dimensional process reward mechanism, LifeLong-RFT quantifies the heterogeneous contributions of intermediate action chunks across three dimensions to facilitate policy optimization. Specifically, (1) the Quantized Action Consistency Reward (QACR) ensures** 

**accurate action prediction within the discrete action space; (2) the Continuous Trajectory Alignment Reward (CTAR) aligns decoded continuous action chunks with reference trajectories to ensure precise control; (3) the Format Compliance Reward (FCR) guarantees the structural validity of outputs. Comprehensive experiments across SimplerEnv, LIBERO, and real-world tasks demonstrate that LifeLong-RFT exhibits strong performance in multi-task learning. Furthermore, for continual learning on the LIBERO benchmark, our method achieves a 22% gain in average success rate over SFT, while effectively adapting to new tasks using only 20% of the training data. Overall, our method provides a promising post-training paradigm for VLAs. The project page is available at https://yuan-liu-lifelong-rft.github.io.** 

### I. INTRODUCTION 

Vision-Language-Action (VLA) models trained on largescale datasets are progressively emerging as a pivotal approach 

> † Work done during an internship at CASIA. � Corresponding author. 

for achieving generalist robot policies [6, 7, 25, 13]. Despite these advances, adapting VLA models to new tasks via supervised fine-tuning (SFT) remains challenging, as illustrated in Fig. 1. First, SFT typically requires a substantial amount of task-specific data, limiting the ability of VLA models to rapidly adapt in low-data or few-shot settings. Second, SFT often leads to catastrophic forgetting, where learning new skills degrades previously acquired knowledge. These issues prevent the SFT from supporting the evolution of VLA into long-lived agents capable of continually acquiring new skills. 

These two challenges are not independent [64]: improving data-efficient adaptation often exacerbates forgetting, while preserving prior knowledge restricts effective learning from limited new data. Achieving an effective balance between plasticity and stability is essential for robots to learn from limited data without erasing prior knowledge. In earlier work based on specialized models, this trade-off was widely viewed as intrinsic [50], motivating solutions based on task-specific adapters or handcrafted features [32, 43, 68, 51]. With the emergence of foundation models, representations learned from massive and diverse datasets exhibit substantially improved transferability, reshaping the plasticity–stability dilemma yet not eliminating it [54]. While such representations significantly reduce the data requirements for learning new tasks, directly applying SFT still results in severe catastrophic forgetting [47]. Consequently, continual learning techniques developed for specialized models are often reused to mitigate forgetting in foundation models [67, 69, 61]. However, these techniques struggle to scale to VLA settings involving both massive tasks and a high-capacity parameterization. 

In contrast to SFT, which learns from the annotated datasets, recent advances in large language models suggest that onpolicy reinforcement learning (RL), which updates the model using samples drawn from its current distribution, can exhibit stronger robustness to forgetting [60, 11, 31]. This observation raises an important question for robotics: _can onpolicy reinforcement learning be leveraged to enable continual adaptation of VLA foundation models, supporting their evolution into long-lived agents?_ A central challenge in answering this question lies in designing efficient, reliable, and scalable reward signals for reinforcement fine-tuning of VLA models. 

Existing approaches to reinforcement fine-tuning VLA models rely primarily on two categories of reward signals. The first uses environment-provided ground-truth rewards [42, 36, 63, 48, 12], which are typically available only in simulation and depend on privileged information. Such methods face significant barriers in real-world deployment due to the sim-toreal gap and the difficulty of computing rewards without access to privileged state. The second category employs model-based reward estimation, such as predicting task success [62, 46, 15, 75], task progress [45, 17, 74, 34], or distance-based dense rewards [19, 24, 16, 25, 20]. However, inaccuracies and generalization errors in reward models make these approaches highly vulnerable to reward hacking [18]. Moreover, both categories require extensive interaction with an environment—whether simulators [36, 42], world models [80, 25], or 

real robots [15, 53]—resulting in prohibitively high training costs when scaling to large task sets. Importantly, existing methods predominantly optimize performance on the finetuning tasks themselves, while largely neglecting the continual learning properties required for long-lived VLA agents. 

In this work, we propose a simple yet effective posttraining paradigm for VLA models named **LifeLong-RFT** . By designing a multi-dimensional process reward mechanism, we enable chunking-level on-policy reinforcement fine-tuning without requiring interaction with the environment. Specifically, we decompose this mechanism into three dimensions to provide comprehensive rewards. First, we introduce the **Q** uantized **A** ction **C** onsistency **R** eward (QACR). Given that VLAs are built upon VLM backbones to generate discrete action tokens, QACR ensures precise prediction within the quantized action space by measuring the consistency between predicted and target tokens. Second, we design the **C** ontinuous **T** rajectory **A** lignment **R** eward (CTAR). While QACR ensures accuracy within the quantized action space, physical execution necessitates alignment with continuous trajectories. To this end, CTAR utilizes decoded action chunks to compute chunking-level rewards based on spatial deviations from reference trajectories, incentivizing the model to explore optimal motions. Third, we introduce the **F** ormat **C** ompliance **R** eward (FCR). Due to the generative diversity of VLA backbones, the model is prone to producing structurally invalid outputs ( _e.g._ , mismatched action dimensions and inconsistent prediction horizons). To mitigate this instability, the FCR functions as a binary reward that promotes adherence to valid formats, ensuring action executability and enhancing inference efficiency. 

Our main contributions are summarized as follows: 

1) We propose **LifeLong-RFT** , a post-training strategy that integrates chunking-level on-policy reinforcement learning with the multi-dimensional process reward. This approach enables VLAs to continually master new tasks with limited demonstrations while preserving original capabilities. 

2) The multi-dimensional process reward mechanism comprises the **Q** uantized **A** ction **C** onsistency **R** eward (QACR), the **C** ontinuous **T** rajectory **A** lignment **R** eward (CTAR), and the **F** ormat **C** ompliance **R** eward (FCR), quantifying the heterogeneous contributions of intermediate action chunks across three dimensions to facilitate policy optimization. 

3) Comprehensive experiments across both simulated and real-world tasks demonstrate LifeLong-RFT’s superior performance in multi-task learning. Notably, for continual learning on LIBERO, our method achieves a 22% improvement in average success rate over SFT, facilitating efficient adaptation to novel tasks with only 20% of the training data. 

### II. RELATED WORK 

### _A. Vision-Language-Action Models_ 

Representing a paradigm shift, VLA models diverge from the traditional hierarchical architecture in favor of an end-toend learning approach, directly mapping multimodal perceptual inputs to robot control actions [8, 82]. Generally, these models can be categorized into two streams based on their 

action representations: Discrete Action Models [55, 33, 56, 29, 27] and Continuous Action Models [30, 7, 65, 23, 78]. Discrete Action Models typically utilize VLM backbones [1, 4] to generate discrete action tokens autoregressively for executing manipulation tasks. In contrast, Continuous Action Models explore the integration of diffusion policies [65, 14] or flow matching [6] with VLMs to directly output continuous actions, achieving dexterous control. Building on these architectures, current models typically leverage large-scale pretraining to acquire manipulation priors, followed by SFT to adapt to specific downstream tasks. Nevertheless, despite demonstrating promising performance, this SFT-based post-training paradigm remains limited by the need for substantial amounts of taskspecific data and is prone to catastrophic forgetting. 

### _B. Reinforcement Fine-tuning for VLA Models_ 

To further enhance the robustness and self-refinement capabilities of VLAs, recent research increasingly explores reinforcement fine-tuning strategies. Current strategies primarily comprise three paradigms: simulation-based, real-world-based, and world model-driven approaches. Simulation-based methods [48, 73, 36, 45, 17] benefit from large-scale parallelization, significantly enhancing sample efficiency, and leverage privileged states to construct dense rewards. However, constrained by the sim-to-real gap, these approaches face challenges in deployment within the physical world. Real-world-based strategies [15, 22, 72, 76] effectively enhance model generalization through online adaptation to physical environments. Nevertheless, such methods often involve prohibitive human costs and struggle with the acquisition of rewards. Notably, frontier research [25, 20, 37, 70, 28] employs world models for VLA reinforcement fine-tuning. By leveraging the capability of future state prediction, this approach provides dense reward signals for policy optimization. However, the inherent prediction errors of world models increase the susceptibility of VLAs to reward hacking. Overall, these methods necessitate extensive environmental interaction, limiting their scalability due to high training costs. 

### _C. Continual Learning in Robotics_ 

Continual learning in robotics aims to construct generalist policies capable of adapting to dynamic environmental changes [2, 3] while retaining existing capabilities. Several studies [49, 43, 32, 68, 38, 57, 71] address forgetting by allocating specific parameters to each new learning phase. Additionally, alternative approaches depend on task decomposition via clustering or multistage learning [67, 81, 51]. With the advent of VLAs, recent research focuses on enabling their continual adaptation. Along this line, MergeVLA [21] introduces a model-merging paradigm, aiming to achieve efficient skill expansion by resolving parameter conflicts during the fusion of multi-expert models. On the other hand, Stellar VLA [69] constructs a knowledge-driven continual imitation learning framework, effectively mitigating catastrophic forgetting. In contrast to the aforementioned methods, we integrate on-policy reinforcement learning with the proposed multi-dimensional 

process reward mechanism to effectively adapt to new tasks while retaining previously learned knowledge. 

### III. PROBLEM FORMULATION AND PRELIMINARIES 

**VLA and Post-Training.** The goal of VLA modeling is to learn a general-purpose robotic policy _πθ_ ( **a** _|o, l_ ) _,_ which maps observations _o_ and natural language instructions _l_ to robot actions **a** . In practice, a VLA model is first _pretrained_ on large-scale and diverse datasets to acquire rich semantic understanding and transferable representations. The pretrained parameters _θ_ are then _post-trained_ using task-specific data to adapt the action outputs **a** to the target robot embodiment and downstream tasks. 

**Continual Learning.** SFT remains the primary approach for post-training VLA models. However, SFT primarily optimizes performance on the tasks present in the current training dataset, while largely overlooking the degradation of previously acquired capabilities. In real-world settings, a long-lived agent is expected to acquire new skills while retaining the skills learned earlier, a requirement commonly referred to as continual learning. Formally, this involves an agent learning from a sequence of tasks _{Tk}_<sup>_∞_</sup> _k_ =1<sup>,whereeachtask</sup><sup>_Tk_is</sup> associated with _N_ expert demonstrations _{τk_<sup>_n}_</sup> _n_<sup>_N_</sup> =1<sup>.Unlikea</sup> single adaptation stage, which assumes concurrent access to all task data, CL necessitates continuous knowledge acquisition under the constraint of limited access to historical data. 

**On-Policy Reinforcement Learning.** While SFT can efficiently improve performance on the currently targeted tasks, it often leads to rapid degradation of previously acquired capabilities, a phenomenon commonly known as catastrophic forgetting. In contrast, recent findings [60, 11, 31] in LLMs suggest that on-policy reinforcement learning exhibits stronger resistance to forgetting. Unlike SFT, which relies on fixed annotated datasets, on-policy reinforcement learning updates the policy using self-generated answers and optimizes the expected return over these answers. 

### IV. METHOD 

To support the evolution of VLAs into long-lived agents capable of continually acquiring new skills, we propose LifeLong-RFT, a reinforcement fine-tuning strategy illustrated in Fig. 2. This strategy integrates chunking-level on-policy reinforcement learning with the proposed multi-dimensional process reward mechanism, which quantifies the heterogeneous contributions of intermediate action chunks across three dimensions without requiring environment interaction. 

### _A. Chunking-Level On-Policy Reinforcement Learning_ 

Most existing on-policy RL approaches [42, 36, 63, 12] for VLA post-training optimize model parameters by collecting full trajectories and relying on environment-provided rewards. While such methods can achieve strong performance, they require extensive interaction with the environment during training, leading to high training costs and limiting scalability to large-scale and multi-task settings. To eliminate the need for environment interaction, we adopt a simple alternative: instead 


Fig. 2: **Overview of the proposed LifeLong-RFT.** This strategy integrates the chunking-level on-policy reinforcement learning algorithm with the multi-dimensional process reward mechanism to facilitate policy optimization. 

of evaluating actions along complete trajectories, we evaluate each action chunk sampled by the VLA model independently, thereby removing the dependency on environment interaction. In this work, we employ Group Relative Policy Optimization (GRPO) [59]. In contrast to conventional algorithms such as PPO [58], which rely on an explicit critic network, GRPO estimates advantages via group-wise comparisons of sampled outputs, thereby considerably reducing computational overhead. Specifically, for each observation _o_ and instruction _l_ , a group of _G_ action outputs _{_ **a** _i}_<sup>_G_</sup> _i_ =1<sup>isfirstsampledfromthe</sup> old policy _πθ_ old( **a** _|o, l_ ). Then, corresponding rewards _{ri}_<sup>_G_</sup> _i_ =1 are computed via task-specific reward functions. Based on the mean and standard deviation of intra-group rewards, the relative advantage _Ai_ for each output is computed as follows: 


Given the advantage _Ai_ , the policy parameters _θ_ are optimized by maximizing the following objective: 


where _B_ denotes the dataset of expert demonstrations, each comprising an observation _o_ and a language instruction _l_ . To stabilize the training process, clip constrains the policy _πθ_ <u>(</u> **a** _i|o,l_ <u>)</u> probability ratio, _πθ_ old ( **a** _i|o,l_ )<sup>, within [1</sup><sup>_−ϵ,_1+</sup><sup>_ϵ_]. Furthermore,</sup> 

_γ_ modulates the strength of the KL divergence regularization term _DKL_ [ _πθ||π_ ref], effectively preventing the new policy _πθ_ from deviating excessively from the reference policy _π_ ref. Building upon this formulation, the construction of an efficient and verifiable reward _ri_ becomes the key to optimization. 

### _B. Multi-Dimensional Process Reward_ 

To effectively guide the on-policy reinforcement learning process without requiring environment interaction, we design the multi-dimensional process reward mechanism. This mechanism decomposes the assessment of action chunks into three complementary dimensions, bridging discrete token generation and continuous robotic control. In this section, we detail the designs of the three dimension-specific rewards. 

_1) Quantized Action Consistency Reward:_ Built upon VLM backbones, contemporary VLAs [26, 29, 55] interpret language instructions and multi-modal observations to generate action tokens. This paradigm necessitates designing a specialized reward function to assess the consistency between generated tokens and the ground truth, facilitating accurate prediction within the quantized action space. For this purpose, we propose the Quantized Action Consistency Reward (QACR) function, as shown in Algorithm 1. 

First, we perform a format check on the model generations to verify their compliance with the predefined specifications of the action tokenizer Fast+ [55] ( _i.e._ , the action chunk size and action dimension). Only validated generations proceed to the subsequent consistency assessment stage, while those failing the verification receive a reward of zero. Second, we compute the consistency reward by position-wise matching between the predicted action token sequence **a** = _{au}_<sup>_U_</sup> _u_ =1<sup>anditsground-</sup> 


where I(( _·_ ) is the indicator function that returns 1 when the predicted action token _aℓℓ_ matches the ground-truth _a_ ˜ _ℓ_ , and 0 otherwise. Additionally, the term “valid” indicates that the predicted sequence satisfies the decoding requirements of the Fast+ tokenizer. Based on this formulation, QACR provides a robust assessment for sequence consistency. 

to pose deviation. **(2)** To incentivize precise gripper actuation, we employ a binary reward _rt_<sup>grip</sup> . This reward is defined as an indicator function I( _·_ ) that assigns a value of 1 when the predicted gripper state **y** _t_<sup>grip</sup> matches the ground truth **y** ˜ _t_<sup>grip</sup> , and 0 otherwise. **(3)** Finally, the normalized CTAR is computed by averaging the weighted combination of pose and grip rewards over the action chunk size _H_ , formally defined as: 

_2) Continuous Trajectory Alignment Reward:_ While QACR ensures accuracy within the quantized action space, physical execution necessitates alignment with continuous trajectories. To address this, we introduce the Continuous Trajectory Alignment Reward (CTAR). This mechanism assesses the spatial alignment between decoded continuous action chunks and reference trajectories, providing dense feedback to facilitate dexterous manipulation. The implementation of this reward function is outlined in Algorithm 2. 


Consistent with QACR, we first conduct format verification on the predicted action token sequence **a** = _{au}_<sup>_U_</sup> _u_ =1<sup>.Only</sup> sequences that pass this verification proceed to the subsequent reward calculation, while invalid ones are directly assigned a zero reward. Subsequently, we utilize the Fast+ [55] tokenizer to decode the predicted action tokens into the continuous action chunk **y** , comprising a sequence of _H_ actions. For the action chunk **y** , the action vector **y** _t_ at each time step consists of a pose component **y** _t_<sup>pose</sup> and a gripper component **y** _t_<sup>grip</sup> . Here, **y** _t_<sup>pose</sup> represents the end-effector pose (or joint angles) of the robot at step _t_ , while **y** _t_<sup>grip</sup> indicates the gripper’s open-close state. Based on this, we decompose the calculation of CTAR into the following steps: **(1)** To encourage precise pose alignment, we formulate the pose reward _rt_<sup>pose</sup> as an exponentially decaying function of the error relative to the ground truth. Specifically, we compute the normalized L1 distance _dt_ between the predicted pose vector **y** _t_<sup>pose</sup> and the ground truth **y** ˜ _t_<sup>pose</sup> . Based on this error, we apply an exponential decay function exp( _−α · dt_ ) to convert it into a reward signal, where the hyperparameter _α_ regulates the sensitivity 

where the hyperparameter _β ∈_ [0 _,_ 1] modulates the relative importance of the pose reward _rt_<sup>pose</sup> and the gripper reward _rt_<sup>grip</sup> at each time step _t_ . In conclusion, the CTAR function establishes a dense reward mechanism by quantifying the prediction discrepancies in both robot poses and gripper states. 

_3) Format Compliance Reward:_ While QACR and CTAR focus on optimizing prediction accuracy and control precision, their effectiveness is dependent on the structural validity of the generated outputs. Specifically, the predicted sequences must adhere to the specified action dimensions and action chunk size. To this end, we propose the Format Compliance Reward (FCR) to guide the model in generating structurally well-formed token sequences. 

Concretely, we employ the Fast+ tokenizer to verify the compliance of the generated token sequence with the required output shape. Accordingly, we define the FCR as a binary reward function that returns 1 if the validation passes and 0 

TABLE I: Multi-Task learning performance on SimplerEnv. 

||**Training**||**Widow**|**X (Visual Ma**|**tching)**||**Google **|**Robot (V**|**isual Matchi**|**ng)**|
|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|||||||||||
||**Strategy**|**Put Carrot**<br>**on Plate**|**Stack**<br>**Blocks**|**Put Spoon**<br>**on Towel**|**Put Eggplant**<br>**in Basket**|**Avg**|**Pick Coke**<br>**Can**|**Move**<br>**Near**|**Open/Close**<br>**Drawer**|**Avg**|
|**_Continuous Action Models_**|||||||||||
|Octo-Base [65]|SFT|8.3|0.0|12.5|43.1|16.0|17.0|4.2|22.7|16.8|
|RoboVLM [41]|SFT|25.0|12.5|29.2|58.3|31.3|77.3|61.7|43.5|63.4|
|GR00T N1.5 [52]|SFT|–|–|–|–|–|69.3|68.7|35.8|52.4|
|_π_0 [6]|SFT|**58.8**|21.3|63.3|79.2|55.7|72.7|65.3|38.3|58.7|
|ThinkAct [23]|SFT + RFT|37.5|8.7|58.3|70.8|43.8|92.0|72.4|50.0|71.5|
|NORA-1.5 [25]|SFT|–|–|–|–|–|92.8|78.7|62.2|77.9|
|NORA-1.5 [25] (DPO)|SFT+RFT|–|–|–|–|–|94.0|**88.0**|**66.4**|**82.8**|
|**_Discrete Action Models_**|||||||||||
|TraceVLA [79]|SFT|–|–|–|–|–|28.0|53.7|57.0|42.0|
|RT-1-X [8]|SFT|4.2|0.0|0.0|0.0|1.1|56.7|31.7|59.7|53.4|
|OpenVLA [29]|SFT|0.0|0.0|0.0|4.1|1.0|16.3|46.2|35.6|27.7|
|SpatialVLA [56]|SFT|25.0|29.2|16.7|**100.0**|42.7|86.0|77.9|57.4|73.7|
|_π_0-FAST [55]|SFT|22.0|**83.0**|29.0|48.0|45.5|75.3|67.5|42.6|61.9|
|NORA-1.5-FAST [25]|SFT|–|–|–|–|–|88.6|86.4|41.2|72.1|
|NORA-Long [26] (Baseline)|SFT|46.0|60.3|80.2|75.7|65.5|86.0|82.3|56.0|74.7|
|**NORA-Long** [26]|**RFT (Ours)**|50.2|64.4|**84.3**|77.0|**69.0**|**94.0**|84.7|58.5|79.1|
|**∆**|–|+4.2|+4.1|+4.1|+1.3|**+3.5**|+8.0|+2.4|+2.5|+**4.4**|


otherwise. The specific formulation is defined as: 


where the condition “valid” indicates that the model output adheres to the predefined output format, enabling the Fast+ tokenizer to decode it into a continuous action chunk. By explicitly incentivizing the model to acquire structurally valid output patterns, this reward establishes the necessary prerequisites for effective trajectory exploration. 

Finally, we synthesize QACR, CTAR, and FCR to formulate the multi-dimensional process reward as follows: 


where _ω ∈_ [0 _,_ 1] governs the trade-off between discrete action consistency and continuous trajectory alignment, and _λ_ scales the significance of structural format compliance. 

### V. EXPERIMENTS 

In this section, we investigate the performance of LifeLongRFT through comprehensive experiments in both simulation and real-world settings. We first present the implementation details of the method, then detail the experimental configurations and results for both multi-task and continual learning. 

### _A. Implementation Details_ 

In our experiments, we adopt NORA-Long [26] as the base VLA model, which utilizes the Fast+ [55] tokenizer for action representation. During the reinforcement fine-tuning phase, the model undergoes full-parameter optimization. Specifically, we set the rollout group size for GRPO to 8 and employ the AdamW [44] optimizer with a learning rate of 1 _×_ 10<sup>_−_6</sup> . For the CTAR configuration, the hyperparameters _α_ and _β_ are set to 5 and 0.8, respectively. Finally, the multi-dimensional 

process reward is formulated as a weighted combination of rewards across three dimensions, with weighting coefficients _ω_ = 0 _._ 7 and _λ_ = 0 _._ 1. All experiments are conducted on 8 NVIDIA H20 GPUs. 

### _B. Multi-Task Learning Experiments_ 

### _1) Experimental Setup:_ 

_a) Training Settings:_ To evaluate multi-task learning in simulation, we utilize SimplerEnv [39] and LIBERO [40]. For SimplerEnv, we train the model on BridgeData V2 [66] for WidowX and Fractal [8] for Google Robot. For LIBERO, we fine-tune the model for each task suite ( _i.e._ , Object, Spatial, Goal, and Long), utilizing all 10 tasks with third-person and wrist inputs. Moreover, we conduct experiments within realworld environments on the Franka robot, as shown in Fig. 3. Concretely, we jointly train the model using 40 demonstrations each for the first three tasks, and 50 for the last. 

_b) Evaluation Protocols:_ In SimplerEnv, we evaluate the model’s performance on the WidowX and Google Robot platforms under the Visual Matching setting. To ensure robust evaluation, each task is repeated over 24 trials under diverse initial object poses and environmental configurations. For LIBERO, we evaluate the model on each task suite with 500 trials. Additionally, in real-world experiments, we perform 20 trials per task. Across all the above experiments, we report the average success rate (SR) as the evaluation metric. 

_2) Performance on Simulation:_ In Table I, LifeLong-RFT consistently improves the performance of the SFT baseline across diverse evaluation scenarios, achieving average success rate improvements of 3.5% on WidowX and 4.4% on the Google Robot. Moreover, results in Table II show that our method surpasses all competing continuous and discrete action models, achieving a superior average success rate of 95.6%. 

_3) Performance on Real-World:_ Beyond simulation, we also conducted real-world experiments. Table III demonstrates 


Fig. 3: **Overview of real-world experimental tasks:** Pick & Place (Banana, Bread), Pull Drawer, and Hang Chinese Knot. 

TABLE II: Multi-Task learning performance on LIBERO. 

|**Method**|**Training**<br>||**LIBER**|**O**||**Avg**|
|---|---|---|---|---|---|---|
||**Strategy**|**Object **|**Spatial **|**Goal **|**Long**||
|**_Continuous Action Models_**|||||||
|Octo-Base [65]|SFT|85.7|78.9|84.6|51.1|75.1|
|GR00T N1 [5]|SFT|97.6|94.4|93.0|90.6|93.9|
|_π_0[6]|SFT|98.8|96.8|95.8|85.2|94.2|
|OpenVLA-OFT [30]|SFT|98.1|96.9|95.5|**91.1**|95.4|
|ThinkAct [23]|SFT + RFT|91.4|88.3|87.1|70.9|84.4|
|VLA-RFT [37]|SFT + RFT|94.4|94.4|95.4|80.2|91.1|
|NORA-1.5 [25]|SFT|96.4|97.3|94.5|89.6|94.5|
|NORA-1.5 [25] (DPO)|SFT + RFT|96.0|98.0|95.4|90.5|95.0|
|**_Discrete Action Models_**|||||||
|TraceVLA [79]|SFT|85.2|84.6|75.1|54.1|74.8|
|OpenVLA [29]|SFT|88.4|84.7|79.2|53.7|76.5|
|SpatialVLA [56]|SFT|89.9|88.2|78.6|55.5|78.1|
|CoT-VLA [77]|SFT|91.6|87.5|87.6|69.0|83.9|
|WorldVLA [9]|SFT|96.2|87.6|83.4|60.0|79.1|
|_π_0-Fast [55]|SFT|96.8|96.4|88.6|60.2|85.5|
|MolmoAct-7B-D [33]|SFT|95.4|87.0|87.6|77.2|86.6|
|TGRPO [17]|SFT + RFT|92.2|90.4|81.0|59.2|80.7|
|NORA-Long [26] (Baseline)|SFT|97.5|96.4|91.0|82.4|91.8|
|**NORA-Long**[26]|**RFT (Ours)**|**99.2**|**98.2**|**95.8**|89.0|**95.6**|
|**∆**|–|+1.7|+1.8|+4.8|+6.6|**+3.8**|


that our method consistently outperforms all competing methods across four tasks. Specifically, when employing NORALong as the backbone, LifeLong-RFT achieves an average success rate improvement of 8.7% over the SFT baseline. Notably, for the dexterous task “Hang Chinese Knot”, this method outperforms the SFT baseline by 15%. 

### _C. Continual Learning Experiments_ 

### _1) Experimental Setup:_ 

_a) Training Settings:_ We utilize LIBERO [40] to conduct experiments within simulated environments. Following LOTUS [67], the training process consists of a base task stage and a lifelong learning stage. For each task suite, we conduct the base task stage training using its first six tasks, each comprising 50 demonstrations. Subsequently, the lifelong learning stage focuses on incremental learning for the remaining four tasks. In this stage, each new task consists of only 10 demonstrations, while 5 demonstrations per previously learned task are retained for Experience Replay (ER) [10, 35]. Overall, a complete experimental cycle comprises one base learning step and four sequential lifelong learning steps. Additionally, 

TABLE III: Multi-Task learning performance on real-world. 

|**Task Split**|**_π_0** [6]|**OpenVLA** [29]|**N**|**ORA-Long** [|25]|
|---|---|---|---|---|---|
||SFT|SFT|SFT|**RFT (Ours)**|**∆**|
|Pick Banana|90.0|75.0|85.0|90.0|+5.0|
|Pick Bread|75.0|70.0|75.0|85.0|+10.0|
|Pull Drawer|95.0|85.0|95.0|100.0|+5.0|
|Hang Chinese Knot|65.0|55.0|60.0|75.0|+15.0|
|**Overall**|81.3|71.3|78.8|**87.5**|**+8.7**|


for real-world experiments, we sequentially train the model on four tasks as illustrated in Fig. 3, utilizing 20 demonstrations for each new task and retaining 5 for each previous task. 

_b) Evaluation Protocols:_ We utilize three metrics [40] to assess the model’s continual learning capabilities: Forward Transfer (FWT), Negative Backward Transfer (NBT), and Area Under the Success Rate Curve (AUC). All three metrics are derived from the task success rate. Specifically, a higher FWT indicates improved adaptation to new tasks; a lower NBT implies effective mitigation of catastrophic forgetting of previously learned tasks; and a higher AUC reflects better average success rates across all evaluated tasks. Given that the model sequentially learns over _K_ tasks _{Tk}_<sup>_K_</sup> _k_ =1<sup>,let</sup><sup>_sk,j_</sup> denote the agent’s success rate on task _j_ after learning the first _k_ tasks. These three metrics are defined as follows: _sk,k_ <u>NBT</u> _<u>k</u>_ = FWT =<sup>�</sup> _k∈_ [ _K_ ] _K_<sup>,NBT=�</sup> _k∈_ [ _K_ ] _K_<sup>,NBT</sup><sup>_k_</sup> <u>1</u> = <u>AUC</u> _<u>k</u> K−k_ � _Kq_ = _k_ +1<sup>(</sup><sup>_sk,k−sq,k_),andAUC</sup> � _k∈_ [ _K_ ] _K_<sup>,</sup> AUC _k_ = _K−_ <u>1</u> _k_ +1<sup>(</sup><sup>_sk,k_+�</sup><sup>_K_</sup> _q_ = _k_ +1<sup>_sq,k_). In our experiments, we</sup> evaluate policies on all learned tasks, conducting 50 episodes for LIBERO and 20 episodes for real-world experiments. 

_2) Performance on Simulation:_ First, we evaluate LifeLong-RFT on LIBERO to validate its continual learning capabilities. We compare against models [81, 67, 71] trained with behavioral cloning (BC) loss. Additionally, we assess large-scale VLAs [6, 29, 30, 26] optimized by SFT. As shown in Table IV, our method consistently outperforms other methods across all task suites. Notably, on LIBERO-Goal, LifeLong-RFT demonstrates significant superiority, achieving a substantial gain of 35.9 in AUC over the SFT baseline. 

_3) Performance on Real-World:_ Furthermore, we assess real-world continual learning performance. As presented in Table V, our method shows a substantial improvement of 23.7 in FWT over the SFT baseline, significantly outperforming the other two models. Furthermore, the approach yields an 

TABLE IV: Continual learning performance on LIBERO. 

|**Task Split**|**Metrics**|**BUDS** [81]|**LOTUS** [67]|**SPECI** [71]|**_π_0** [6]|**OpenVLA** [29]|**OpenVLA-OFT** [30]||**NORA-Long** [|26]|
|---|---|---|---|---|---|---|---|---|---|---|
|||BC|BC|BC|SFT|SFT|SFT|SFT|**RFT (Ours)**|**∆**|
||FWT (_↑_)|52.0|74.0|83.0|73.0|59.4|89.8|84.8|96.0|+11.2|
|LIBERO-Object|NBT (_↓_)|21.0|11.0|10.0|16.2|17.9|3.1|6.8|1.5|-5.3|
||**AUC** (_↑_)|47.0|65.0|78.0|59.3|45.1|87.4|79.7|**94.8**|**+15.1**|
||FWT (_↑_)|–|–|67.0|74.4|64.2|88.6|82.8|94.0|+11.2|
|LIBERO-Spatial|NBT (_↓_)|–|–|6.0|23.7|17.6|9.4|14.0|3.7|-10.3|
||**AUC** (_↑_)|–|–|66.0|55.5|50.8|81.7|71.7|**91.2**|**+19.5**|
|LIBERO-Goal|FWT (_↑_)|50.0|61.0|74.0|74.6|58.6|90.2|72.8|92.4|+19.6|
||NBT (_↓_)|39.0|30.0|20.0|23.9|5.8|13.8|25.2|3.1|-22.1|
||**AUC** (_↑_)|42.0|56.0|65.0|56.3|53.5|79.2|54.4|**90.3**|**+35.9**|
||FWT (_↑_)|–|–|58.0|53.8|32.0|64.0|61.0|74.2|+13.2|
|LIBERO-Long|NBT (_↓_)|–|–|21.0|14.2|14.1|31.4|17.3|12.8|-4.5|
||**AUC** (_↑_)|–|–|46.0|42.5|20.8|38.7|47.3|**64.5**|**+17.2**|


TABLE V: Continual learning performance on real-world. 

|**Task Split**|**Metrics**|**_π_0**[6]|**OpenVLA**[29]|**N**|**ORA-Long**|[26]<br>|
|---|---|---|---|---|---|---|
|||SFT|SFT|SFT|**RFT (Ours)**|<br>**∆**|
||FWT (_↑_)|58.8|46.3|56.3|80.0|+23.7|
|Real-World|NBT (_↓_)|16.3|17.8|18.3|6.1|-12.2|
||**AUC**(_↑_)|47.9|35.1|44.2|**75.9**|**+31.7**|


TABLE VI: Ablation of the multi-dimensional process reward. 

|**Settings**|**Ob**|**ject**|**Spa**|**tial**|**G**|**oal**|**Lo**|**ng**|**A**|**vg**|
|---|---|---|---|---|---|---|---|---|---|---|
||**SR**|**∆**|**SR**|**∆**|**SR**|**∆**|**SR**|**∆**|**SR**|**∆**|
|w/o QACR|97.0|-2.2|96.4|-1.8|92.2|-3.6|85.6|-3.4|92.8|-2.8|
|w/o CTAR|8.0|**-91.2**|6.2|**-92.0**|2.4|**-93.4**|2.0|**-87.0**|4.7|**-90.9**|
|w/o FCR|98.0|-1.2|96.2|-2.0|93.2|-2.6|84.6|-4.4|93.0|-2.6|
|**RFT (Ours)**|**99.2**|**-**|**98.2**|**-**|**95.8**|**-**|**89.0**|**-**|**95.6**|**-**|


NBT of only 6.1, demonstrating a strong capability to preserve performance on learned tasks. Overall, the model fine-tuned with LifeLong-RFT achieves an average success rate of 75.9% across the learning cycle, exhibiting robust continual learning. 

### _D. Ablation Studies_ 

_1) Effectiveness of Multi-Dimensional Process Reward:_ To verify the effectiveness of multi-dimensional process reward, we conduct multi-task learning experiments on LIBERO. The first row of Table VI indicates that removing QACR leads to a 2.8% average performance drop across the four task suites, confirming its necessity for accurate quantized action prediction. The second row further underscores the critical role of CTAR, where its exclusion leads to a 90.9% performance drop, resulting in the model being nearly incapable of task completion. Additionally, the third row shows that FCR is critical for guaranteeing the structural validity of the output. Particularly in LIBERO-Long, the absence of FCR leads to a 4.4% degradation. Overall, each reward component exhibits consistent effectiveness, enhancing overall performance. 

_2) Efficiency of New Task Adaptation:_ To assess the adaptation efficiency of LifeLong-RFT in acquiring new tasks, we conduct experiments across the four task suites of the LIBERO benchmark. Specifically, we first train the model on the initial six tasks of each suite via multi-task learning. Subsequently, 


Fig. 4: Adaptation efficiency on representative new tasks. 

we select a representative task from the remaining four unseen tasks in each suite to evaluate the model’s efficiency for new task adaptation. In Fig. 4, LifeLong-RFT shows superior adaptation efficiency compared to SFT. On the “Pick Orange Juice” task, it achieves 100% success using merely 5 demonstrations, whereas SFT reaches 98% even when trained with 50. Similarly, for the “Pick Bowl” task, LifeLong-RFT matches the performance of the SFT baseline trained on 50 demonstrations using only 5, and improves to 100% success with just 10. In addition to few-shot scenarios, our approach sustains its advantage with the full set of demonstrations: it surpasses SFT by 30% on the “Put Wine Bottle” task and exhibits superior performance on the long-horizon task “Put Alphabet Soup and Cream Cheese”. 

### VI. CONCLUSION AND FUTURE OUTLOOK 

In this work, we introduce LifeLong-RFT, a reinforcement fine-tuning strategy to overcome the extensive data requirements and catastrophic forgetting associated with SFT. Unlike existing methods, our method integrates the chunking-level onpolicy RL with the multi-dimensional process reward mechanism to achieve efficient new task adaptation while preserving 

pre-existing knowledge. Specifically, this mechanism employs Quantized Action Consistency Reward, Continuous Trajectory Alignment Reward, and Format Compliance Reward to quantify the heterogeneous contributions of action chunks across three dimensions, independent of environmental feedback and pre-trained reward models. Comprehensive experiments indicate that LifeLong-RFT consistently surpasses SFT-based methods in both multi-task and continual learning. 

**Limitations & Future Work.** This work primarily focuses on discrete action models, yet their performance falls short of the levels achieved by continuous action models. Future research extending the LifeLong-RFT training strategy to continuous action models will significantly accelerate the transition of VLAs from laboratory research to industrial applications. 

### VII. ACKNOWLEDGMENTS 

This work was supported by the New Generation Artificial Intelligence-National Science and Technology Major Project 2025ZD0122902; in part by the National Natural Science Foundation of China (NSFC) under Grants 62136008 and 62293545; the Beijing Major Science and Technology Project under Contract no. Z251100008125023; the Suzhou Innovation and Entrepreneurship Leading Talents Programme – Innovation Leading Talent in Universities and Research Institutes under Grant ZXL2025310; and the Beijing Academy of Artificial Intelligence (BAAI). 

### REFERENCES 

- [1] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 

- [2] Jacob Beck, Risto Vuorio, Evan Zheran Liu, Zheng Xiong, Luisa Zintgraf, Chelsea Finn, and Shimon Whiteson. A survey of meta-reinforcement learning. _arXiv preprint arXiv:2301.08028_ , 2023. 

- [3] Jacob Beck, Risto Vuorio, Evan Zheran Liu, Zheng Xiong, Luisa Zintgraf, Chelsea Finn, and Shimon Whiteson. A tutorial on meta-reinforcement learning. _Foundations and Trends in Machine Learning_ , 18(2-3):224–384, 2025. 

- [4] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- [5] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [6] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A visionlanguage-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [7] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, brian ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. $ _\_ pi _<u>{</u>_ 0.5 _}_ $: a vision-languageaction model with open-world generalization. In _9th Annual Conference on Robot Learning_ , 2025. 

- [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- [9] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 

- [10] Arslan Chaudhry, Marcus Rohrbach, Mohamed Elhoseiny, Thalaiyasingam Ajanthan, Puneet K Dokania, Philip HS Torr, and Marc’Aurelio Ranzato. On tiny episodic memories in continual learning. _arXiv preprint arXiv:1902.10486_ , 2019. 

- [11] Howard Chen, Noam Razin, Karthik Narasimhan, and Danqi Chen. Retaining by doing: The role of onpolicy data in mitigating forgetting. _arXiv preprint arXiv:2510.18874_ , 2025. 

- [12] Kang Chen, Zhihao Liu, Tonghe Zhang, Zhen Guo, Si Xu, Hao Lin, Hongzhi Zang, Quanlu Zhang, Zhaofei Yu, Guoliang Fan, et al. _π_ rl: Online rl fine-tuning for flow-based vision-language-action models. _arXiv preprint arXiv:2510.25889_ , 2025. 

- [13] Yaran Chen, Wenbo Cui, Yuanwen Chen, Mining Tan, Xinyao Zhang, Jinrui Liu, Haoran Li, Dongbin Zhao, and He Wang. Robogpt: An llm-based long-term decisionmaking embodied agent for instruction following tasks. _IEEE Transactions on Cognitive and Developmental Systems_ , 17(5):1163–1174, 2025. 

- [14] Yuhui Chen, Haoran Li, and Dongbin Zhao. Boosting continuous control with consistency policy. In _Proceedings of the 23rd International Conference on Autonomous Agents and Multiagent Systems_ , AAMAS ’24, page 335–344, Richland, SC, 2024. 

- [15] Yuhui Chen, Shuai Tian, Shugao Liu, Yingting Zhou, Haoran Li, and Dongbin Zhao. ConRFT: A reinforced fine-tuning method for vla models via consistency policy. In _Robotics: Science and Systems, RSS_ , 2025. 

- [16] Yuhui Chen, Haoran Li, Zhennan Jiang, Haowei Wen, and Dongbin Zhao. Tevir: Text-to-video reward with diffusion models for efficient reinforcement learning. _IEEE Transactions on Systems, Man, and Cybernetics:_ 

_Systems_ , 56(2):893–905, 2026. 

- [17] Zengjue Chen, Runliang Niu, He Kong, Qi Wang, Qianli Xing, and Zipei Fan. Tgrpo: Fine-tuning visionlanguage-action model via trajectory-wise group relative policy optimization. _arXiv preprint arXiv:2506.08440_ , 2025. 

- [18] Paul F Christiano, Jan Leike, Tom Brown, Miljan Martic, Shane Legg, and Dario Amodei. Deep reinforcement learning from human preferences. _Advances in neural information processing systems_ , 30, 2017. 

- [19] Alejandro Escontrela, Ademi Adeniji, Wilson Yan, Ajay Jain, Xue Bin Peng, Ken Goldberg, Youngwoon Lee, Danijar Hafner, and Pieter Abbeel. Video prediction models as rewards for reinforcement learning. _Advances in Neural Information Processing Systems_ , 36:68760– 68783, 2023. 

- [20] Senyu Fei, Siyin Wang, Li Ji, Ao Li, Shiduo Zhang, Liming Liu, Jinlong Hou, Jingjing Gong, Xianzhong Zhao, and Xipeng Qiu. Srpo: Self-referential policy optimization for vision-language-action models. _arXiv preprint arXiv:2511.15605_ , 2025. 

- [21] Yuxia Fu, Zhizhen Zhang, Yuqi Zhang, Zijian Wang, Zi Huang, and Yadan Luo. Mergevla: Cross-skill model merging toward a generalist vision-languageaction agent. _arXiv preprint arXiv:2511.18810_ , 2025. 

- [22] Yanjiang Guo, Jianke Zhang, Xiaoyu Chen, Xiang Ji, Yen-Jen Wang, Yucheng Hu, and Jianyu Chen. Improving vision-language-action model with online reinforcement learning. _arXiv preprint arXiv:2501.16664_ , 2025. 

- [23] Chi-Pin Huang, Yueh-Hua Wu, Min-Hung Chen, YuChiang Frank Wang, and Fu-En Yang. Thinkact: Visionlanguage-action reasoning via reinforced visual latent planning. _arXiv preprint arXiv:2507.16815_ , 2025. 

- [24] Tao Huang, Guangqi Jiang, Yanjie Ze, and Huazhe Xu. Diffusion reward: Learning rewards via conditional video diffusion. In _European Conference on Computer Vision_ , pages 478–495. Springer, 2024. 

- [25] Chia-Yu Hung, Navonil Majumder, Haoyuan Deng, Liu Renhang, Yankang Ang, Amir Zadeh, Chuan Li, Dorien Herremans, Ziwei Wang, and Soujanya Poria. Nora-1.5: A vision-language-action model trained using world model-and action-based preference rewards. _arXiv preprint arXiv:2511.14659_ , 2025. 

- [26] Chia-Yu Hung, Qi Sun, Pengfei Hong, Amir Zadeh, Chuan Li, U Tan, Navonil Majumder, Soujanya Poria, et al. Nora: A small open-sourced generalist vision language action model for embodied tasks. _arXiv preprint arXiv:2504.19854_ , 2025. 

- [27] Yuheng Ji, Huajie Tan, Jiayu Shi, Xiaoshuai Hao, Yuan Zhang, Hengyuan Zhang, Pengwei Wang, Mengdi Zhao, Yao Mu, Pengju An, et al. Robobrain: A unified brain model for robotic manipulation from abstract to concrete. _arXiv preprint arXiv:2502.21257_ , 2025. 

- [28] Zhennan Jiang, Kai Liu, Yuxin Qin, Shuai Tian, Yupeng Zheng, Mingcai Zhou, Chao Yu, Haoran Li, and Dongbin Zhao. World4rl: Diffusion world models for 

   - policy refinement with reinforcement learning for robotic manipulation. _arXiv preprint arXiv:2509.19080_ , 2025. 

- [29] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [30] Moo Jin Kim, Chelsea Finn, and Percy Liang. Finetuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- [31] Song Lai, Haohan Zhao, Rong Feng, Changyi Ma, Wenzhuo Liu, Hongbo Zhao, Xi Lin, Dong Yi, Qingfu Zhang, Hongbin Liu, et al. Reinforcement fine-tuning naturally mitigates forgetting in continual post-training. _arXiv preprint arXiv:2507.05386_ , 2025. 

- [32] Daehee Lee, Minjong Yoo, Woo Kyung Kim, Wonje Choi, and Honguk Woo. Incremental learning of retrievable skills for efficient continual task adaptation. _Advances in Neural Information Processing Systems_ , 37: 17286–17312, 2024. 

- [33] Jason Lee, Jiafei Duan, Haoquan Fang, Yuquan Deng, Shuo Liu, Boyang Li, Bohan Fang, Jieyu Zhang, Yi Ru Wang, Sangho Lee, et al. Molmoact: Action reasoning models that can reason in space. _arXiv preprint arXiv:2508.07917_ , 2025. 

- [34] Tony Lee, Andrew Wagenmaker, Karl Pertsch, Percy Liang, Sergey Levine, and Chelsea Finn. Roboreward: General-purpose vision-language reward models for robotics. _arXiv preprint arXiv:2601.00675_ , 2026. 

- [35] Haoran Li, Zhennan Jiang, Yuhui Chen, and Dongbin Zhao. Generalizing consistency policy to visual rl with prioritized proximal experience regularization. _Advances in Neural Information Processing Systems_ , 37:109672– 109700, 2024. 

- [36] Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang, Tianxing Chen, Ganqu Cui, et al. Simplevla-rl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ , 2025. 

- [37] Hengtao Li, Pengxiang Ding, Runze Suo, Yihao Wang, Zirui Ge, Dongyuan Zang, Kexian Yu, Mingyang Sun, Hongyin Zhang, Donglin Wang, et al. Vla-rft: Visionlanguage-action reinforcement fine-tuning with verified rewards in world simulators. _arXiv preprint arXiv:2510.00406_ , 2025. 

- [38] Xilai Li, Yingbo Zhou, Tianfu Wu, Richard Socher, and Caiming Xiong. Learn to grow: A continual structure learning framework for overcoming catastrophic forgetting. In _International conference on machine learning_ , pages 3925–3934. PMLR, 2019. 

- [39] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- [40] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang 

Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776– 44791, 2023. 

- [41] Huaping Liu, Xinghang Li, Peiyan Li, Minghuan Liu, Dong Wang, Jirong Liu, Bingyi Kang, Xiao Ma, Tao Kong, and Hanbo Zhang. Towards generalist robot policies: What matters in building vision-language-action models. 2025. 

- [42] Jijia Liu, Feng Gao, Bingwen Wei, Xinlei Chen, Qingmin Liao, Yi Wu, Chao Yu, and Yu Wang. What can rl bring to vla generalization? an empirical study. _arXiv preprint arXiv:2505.19789_ , 2025. 

- [43] Zuxin Liu, Jesse Zhang, Kavosh Asadi, Yao Liu, Ding Zhao, Shoham Sabach, and Rasool Fakoor. Tail: Taskspecific adapters for imitation learning with large pretrained models. _arXiv preprint arXiv:2310.05905_ , 2023. 

- [44] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. _arXiv preprint arXiv:1711.05101_ , 2017. 

- [45] Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, and Ziwei Wang. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning. _arXiv preprint arXiv:2505.18719_ , 2025. 

- [46] Jianlan Luo, Charles Xu, Jeffrey Wu, and Sergey Levine. Precise and dexterous robotic manipulation via humanin-the-loop reinforcement learning. _Science Robotics_ , 10 (105):eads5033, 2025. 

- [47] Yun Luo, Zhen Yang, Fandong Meng, Yafu Li, Jie Zhou, and Yue Zhang. An empirical study of catastrophic forgetting in large language models during continual fine-tuning. _IEEE Transactions on Audio, Speech and Language Processing_ , 2025. 

- [48] Mingyang Lyu, Yinqian Sun, Erliang Lin, Huangrui Li, Ruolin Chen, Feifei Zhao, and Yi Zeng. Reinforcement fine-tuning of flow-matching policies for vision-language-action models. _arXiv preprint arXiv:2510.09976_ , 2025. 

- [49] Arun Mallya and Svetlana Lazebnik. Packnet: Adding multiple tasks to a single network by iterative pruning. In _Proceedings of the IEEE conference on Computer Vision and Pattern Recognition_ , pages 7765–7773, 2018. 

- [50] M Anwar Ma’sum, Mahardhika Pratama, and Igor Skrjanc. Latest advancements towards catastrophic forgetting under data scarcity: A comprehensive survey on few-shot class incremental learning. _arXiv preprint arXiv:2502.08181_ , 2025. 

- [51] Yuan Meng, Zhenshan Bing, Xiangtong Yao, Kejia Chen, Kai Huang, Yang Gao, Fuchun Sun, and Alois Knoll. Preserving and combining knowledge in robotic lifelong reinforcement learning. _Nature Machine Intelligence_ , 7 (2):256–269, 2025. 

- [52] NVIDIA Isaac Robotics Team. Gr00t n1.5: An upgraded foundation model for humanoid robots. https://research. nvidia.com/labs/gear/gr00t-n1 <u>5/,</u> 2025. 

- [53] Mingjie Pan, Siyuan Feng, Qinglin Zhang, Xinchen Li, Jianheng Song, Chendi Qu, Yi Wang, Chuankang Li, Ziyu Xiong, Zhi Chen, et al. Sop: A scalable online post-training system for vision-language-action models. _arXiv preprint arXiv:2601.03044_ , 2026. 

- [54] Keon-Hee Park, Kyungwoo Song, and Gyeong-Moon Park. Pre-trained vision and language transformers are few-shot incremental learners. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 23881–23890, 2024. 

- [55] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- [56] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- [57] Dushyant Rao, Francesco Visin, Andrei Rusu, Razvan Pascanu, Yee Whye Teh, and Raia Hadsell. Continual unsupervised representation learning. _Advances in neural information processing systems_ , 32, 2019. 

- [58] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [59] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 

- [60] Idan Shenfeld, Jyothish Pari, and Pulkit Agrawal. Rl’s razor: Why online reinforcement learning forgets less. _arXiv preprint arXiv:2509.04259_ , 2025. 

- [61] Mingchen Song, Xiang Deng, Guoqiang Zhong, Qi Lv, Jia Wan, Yinchuan Li, Jianye Hao, and Weili Guan. Fewshot vision-language action-incremental policy learning. _arXiv preprint arXiv:2504.15517_ , 2025. 

- [62] Sumedh Sontakke, Jesse Zhang, S´eb Arnold, Karl Pertsch, Erdem Bıyık, Dorsa Sadigh, Chelsea Finn, and Laurent Itti. Roboclip: One demonstration is enough to learn robot policies. _Advances in Neural Information Processing Systems_ , 36:55681–55693, 2023. 

- [63] Shuhan Tan, Kairan Dou, Yue Zhao, and Philipp Kr¨ahenb¨uhl. Interactive post-training for vision-language-action models. _arXiv preprint arXiv:2505.17016_ , 2025. 

- [64] Xiaoyu Tao, Xiaopeng Hong, Xinyuan Chang, Songlin Dong, Xing Wei, and Yihong Gong. Few-shot classincremental learning. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 12183–12192, 2020. 

- [65] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An 

open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [66] Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pages 1723– 1736. PMLR, 2023. 

- [67] Weikang Wan, Yifeng Zhu, Rutav Shah, and Yuke Zhu. Lotus: Continual imitation learning for robot manipulation through unsupervised skill discovery. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 537–544. IEEE, 2024. 

- [68] Yixiao Wang, Yifei Zhang, Mingxiao Huo, Ran Tian, Xiang Zhang, Yichen Xie, Chenfeng Xu, Pengliang Ji, Wei Zhan, Mingyu Ding, et al. Sparse diffusion policy: A sparse, reusable, and flexible policy for robot learning. _arXiv preprint arXiv:2407.01531_ , 2024. 

- [69] Yuxuan Wu, Guangming Wang, Zhiheng Yang, Maoqing Yao, Brian Sheil, and Hesheng Wang. Continually evolving skill knowledge in vision language action model. _arXiv preprint arXiv:2511.18085_ , 2025. 

- [70] Junjin Xiao, Yandan Yang, Xinyuan Chang, Ronghan Chen, Feng Xiong, Mu Xu, Wei-Shi Zheng, and Qing Zhang. World-env: Leveraging world model as a virtual environment for vla post-training. _arXiv preprint arXiv:2509.24948_ , 2025. 

In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713, 2025. 

   - [78] Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, et al. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-languageaction model. _arXiv preprint arXiv:2510.10274_ , 2025. 

   - [79] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daum´e III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ , 2024. 

   - [80] Fangqi Zhu, Zhengyang Yan, Zicong Hong, Quanxin Shou, Xiao Ma, and Song Guo. WMPO: world modelbased policy optimization for vision-language-action models. _arXiv preprint arXiv:2511.09515_ , 2025. 

   - [81] Yifeng Zhu, Peter Stone, and Yuke Zhu. Bottom-up skill discovery from unsegmented demonstrations for long-horizon robot manipulation. _IEEE Robotics and Automation Letters_ , 7(2):4126–4133, 2022. 

   - [82] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-languageaction models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 

- [71] Jingkai Xu and Xiangli Nie. Speci: Skill prompts based hierarchical continual imitation learning for robot manipulation. _arXiv preprint arXiv:2504.15561_ , 2025. 

- [72] Xiu Yuan, Tongzhou Mu, Stone Tao, Yunhao Fang, Mengke Zhang, and Hao Su. Policy decorator: Modelagnostic online refinement for large policy model. _arXiv preprint arXiv:2412.13630_ , 2024. 

- [73] Hongzhi Zang, Mingjie Wei, Si Xu, Yongji Wu, Zhen Guo, Yuanqing Wang, Hao Lin, Liangzhi Shi, Yuqing Xie, Zhexuan Xu, et al. Rlinf-vla: A unified and efficient framework for vla+ rl training. _arXiv preprint arXiv:2510.06710_ , 2025. 

- [74] Shaopeng Zhai, Qi Zhang, Tianyi Zhang, Fuxian Huang, Haoran Zhang, Ming Zhou, Shengzhe Zhang, Litao Liu, Sixu Lin, and Jiangmiao Pang. A vision-languageaction-critic model for robotic real-world reinforcement learning. _arXiv preprint arXiv:2509.15937_ , 2025. 

- [75] Jiahui Zhang, Ze Huang, Chun Gu, Zipei Ma, and Li Zhang. Reinforcing action policies by prophesying. _arXiv preprint arXiv:2511.20633_ , 2025. 

- [76] Jiahui Zhang, Yusen Luo, Abrar Anwar, Sumedh Anand Sontakke, Joseph J Lim, Jesse Thomason, Erdem Biyik, and Jesse Zhang. Rewind: Language-guided rewards teach robot policies without new demonstrations. _arXiv preprint arXiv:2505.10911_ , 2025. 

- [77] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chainof-thought reasoning for vision-language-action models. 

## **Towards Long-Lived Robots: Continual Learning VLA Models via Reinforcement Fine-Tuning** 

## Supplementary Material 

APPENDIX 

### _A. Training Details_ 

In this section, we detail the training settings for multi-task learning and continual learning in both simulation ( _i.e._ , SimplerEnv [39] and LIBERO [40]) and real-world environments. 

_1) Multi-Task Learning:_ The training settings for multi-task learning on SimplerEnv are detailed in Table VII. Notably, the WidowX setup utilizes a global batch size of 512 for 30 epochs, whereas the Google Robot employs a batch size of 1024 for 40 epochs. Apart from these specific adjustments, the remaining hyperparameters are kept consistent, highlighting the cross-platform robustness of our approach. 

TABLE VII: Multi-Task learning settings on SimplerEnv. 

|**Hyperparameter**<br>**WidowX**<br>**Google Robot**|
|---|
|**_Platform-Specific Settings_**|
|Global Batch Size<br>512<br>1024<br>Epochs<br>30<br>40|
|**_Shared Settings_**|
|Learning Rate<br>1_×_10<sup>_−_6</sup>|
|Optimizer<br>AdamW [44]|
|Group Size<br>8|
|Temperature<br>0.8|
|(_α, β, ω, λ, γ_)<br>(5_,_0_._8_,_0_._7_,_0_._1_,_0_._001)|


Table VIII details the hyperparameter settings for multi-task learning on LIBERO. Specifically, for the long-horizon task suite LIBERO-Long, we set the global batch size to 256 and train for 35 epochs. The remaining three task suites share a unified parameter configuration with 15 training epochs. 

epochs, while all other parameters remain consistent with the simulation experiments. 

TABLE IX: Multi-Task learning settings on real-world tasks. 

|**Hyperparameter**|**Real-World**|
|---|---|
|**_Shared Settings_**||
|Global Batch Size|128|
|Epochs|20|
|Learning Rate|1_×_10<sup>_−_6</sup>|
|Optimizer|AdamW [44]|
|Group Size|8|
|Temperature|0.8|
|(_α, β, ω, λ, γ_)|(5_,_0_._8_,_0_._7_,_0_._1_,_0_._001)|


_2) Continual Learning:_ **(1)** The continual learning protocol in LIBERO consists of an initial base task stage and a subsequent lifelong learning stage. For the base task stage, the training parameters remain consistent with Table VIII, while the configurations for the four task suites in the lifelong learning stage are presented in Table X. Given that the lifelong learning stage utilizes limited demonstrations to learn new tasks, we set the global batch size to 32 and train for 10 epochs. **(2)** The real-world continual learning experiment includes only the lifelong learning stage, requiring the model to learn four tasks sequentially. As demonstrated in Table X, the training configurations remain consistent with LIBERO. 

TABLE X: Continual learning settings for LIBERO and realworld experiments. 

|**Hyperparameter**|**LIBERO / Real-World**|
|---|---|
|**_Shared Settings_**||
|Global Batch Size|32|
|Epochs|10|
|Learning Rate|1_×_10<sup>_−_6</sup>|
|Optimizer|AdamW [44]|
|Group Size|8|
|Temperature|0.8|
|(_α, β, ω, λ, γ_)|(5_,_0_._8_,_0_._7_,_0_._1_,_0_._001)|


TABLE VIII: Multi-Task learning settings on LIBERO. 

### _B. Additional Experimental Results and Analysis_ 

|**Hyperparameter**<br>**Ob**|**ject / Spatial / Goal**|**Long**|
|---|---|---|
|**_Task-Specific Settings_**|||
|Global Batch Size|128|256|
|Epochs|15|35|
|**_Shared Settings_**|||
|Learning Rate|1_×_10<sup>_−_6</sup>||
|Optimizer|AdamW [44]||
|Group Size|8||
|Temperature<br>|0.8<br>||
|(_α, β, ω, λ, γ_)|(5_,_0_._8_,_0_._7_,_0_._1_,_0_._00|1)|


For the four real-world tasks on the Franka robot, totaling 170 demonstrations, the training parameters are provided in Table IX. We set the global batch size to 128 and train for 20 

_1) Detailed Continual Learning Results:_ To comprehensively analyze the continual learning effectiveness of LifeLong-RFT, we report detailed results for the model on all learned tasks at each training phase. As shown in Table XI, our method exhibits strong performance in adapting to new tasks and retaining prior knowledge. Notably, following the training of Task 8 in the LIBERO-Goal suite, the model exhibits performance improvements on previously learned tasks ( _i.e._ , Tasks 2, 3, and 7), demonstrating strong backward transfer capabilities. However, within the long-horizon LIBERO-Long suite, it exhibits suboptimal performance on certain tasks (such as Task 7 at 36% and Task 9 at 34%) with limited demonstrations. This underscores a challenge worthy of further exploration in future work. 

TABLE XI: Detailed continual learning results on four LIBERO task suites (Object, Spatial, Goal, and Long). 

|**Task Split**||||**L**|**IBER**|**O-Obje**|**ct**|||||||**LIB**|**ERO**|**-Spati**|**al**||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**T-1**|**T-2**|**T-3**|**T-4**|**T-5**|**T-6**|**T-7**|**T-8**|**T-9**|**T-10**|**T-1**|**T-2**|**T-3**|**T-4**|**T-5**|**T-6**|**T-7**|**T-8**|**T-9**|**T-10**|
|**_Base Task Stag_**|**_e_**||||||||||||||||||||
|Base Task 1-6|100%|100%|100%|98%|98%|100%|–|–|–|–|90%|100%|98%|98%|96%|84%|–|–|–|–|
|**_LifeLong Lear_**|**_ning St_**|**_age_**|||||||||||||||||||
|New Task 7|92%|96%|98%|96%|98%|100%|96%|–|–|–|94%|92%|98%|84%|94%|96%|100%|–|–|–|
|New Task 8|98%|100%|94%|98%|96%|100%|100%|82%|–|–|100%|97%|100%|94%|86%|92%|98%|90%|–|–|
|New Task 9|96%|96%|96%|86%|96%|100%|98%|92%|96%|–|70%|80%|98%|92%|92%|88%|96%|94%|90%|–|
|**New Task 10**|94%|100%|100%|96%|96%|94%|100%|76%|92%|90%|78%|98%|98%|88%<br>|88%|92%|80%|62%|92%|94%|
|**Task Split**|||||**LIBER**|**O-Goa**|**l**|||||||**LIB**|**ERO**|**-Lon**|**g**||||
||**T-1**|**T-2**|**T-3**|**T-4**|**T-5**|**T-6**|**T-7**|**T-8**|**T-9**|**T-10**|**T-1**|**T-2**|**T-3**|**T-4**|**T-5**|**T-6**|**T-7**|**T-8**|**T-9**|**T-10**|
|**_Base Task Stag_**|**_e_**||||||||||||||||||||
|Base Task 1-6|100%|98%|94%|86%|94%|96%|–|–|–|–|78%|86%|92%|96%|88%|92%|–|–|–|–|
|**_LifeLong Lear_**|**_ning St_**|**_age_**|||||||||||||||||||
|New Task 7|90%|90%|86%|88%|98%|94%|72%|–|–|–|58%|78%|74%|94%|44%|86%|36%|–|–|–|
|New Task 8|88%|96%|90%|76%|96%|90%|80%|100%|–|–|52%|70%|60%|84%|30%|80%|44%|82%|–|–|
|New Task 9|94%|94%|98%|80%|94%|96%|82%|98%|100%|–|60%|70%|82%|88%|44%|94%|50%|80%|34%|–|
|**New Task 10**|86%|100%|92%|80%|98%|90%|78%|96%|86%|84%|58%|80%|70%|82%<br>|38%|88%|38%|76%|18%|58%|


TABLE XII: Detailed continual learning results in real-world experiments. 

|**Task Split**|**Pick Banana **|**Pick Bread **|**Pull Drawer **|**Hang Chinese Knot**|
|---|---|---|---|---|
|**_LifeLong Le_**|**_arning Stage_**||||
|New Task 1|85%|–|–|–|
|New Task 2|80%|75%|–|–|
|New Task 3|70%|65%|100%|–|
|**New Task 4**|70%|70%|95%|60%|


Additionally, Table XII details the evaluation results of the real-world experiments. In particular, our method achieves a 100% success rate on the Pull Drawer task with only 20 demonstrations, demonstrating its superior plasticity and stability. Nevertheless, for the deformable task (Hang Chinese Knot), the success rate remains at 60%, suggesting the need for further improvement. 

_2) Further Analysis of Continual Learning:_ To further validate the effectiveness of LifeLong-RFT in learning extended task sequences, we conduct lifelong learning experiments across 10 tasks on the LIBERO-Goal suite. Specifically, the training for each new task utilizes only 10 demonstrations, with 5 demonstrations per previous task preserved for experience replay. As demonstrated in Table XIII, despite the dual challenges of an increasing number of new tasks and limited training samples, our method exhibits strong adaptability to new tasks ( _e.g._ , achieving a 100% success rate on Task 8) while maintaining stability on prior knowledge. 

### _C. Analysis of Reward Combinations within the MultiDimensional Process Reward_ 

To evaluate the impact of reward combination weights within the multi-dimensional process reward, we conduct multi-task learning experiments on LIBERO-Goal, performing a detailed parameter sensitivity analysis of _ω_ and _λ_ . As shown in Fig. 5 (a), the model maintains comparable performance 

TABLE XIII: Continual learning performance on LIBEROGoal during the lifelong learning stage. 

|**Task Split**|**T-1**|**T-2**|**T-3**|**T-4**|**T-5**|**T-6**|**T-7**|**T-8**|**T-9 **|**T-10**|
|---|---|---|---|---|---|---|---|---|---|---|
|**_LifeLong Lear_**|**_ning _**|**_Stage_**|||||||||
|New Task 1|48%|–|–|–|–|–|–|–|–|–|
|New Task 2|44%|76%|–|–|–|–|–|–|–|–|
|New Task 3|30%|48%|94%|–|–|–|–|–|–|–|
|New Task 4|54%|56%|96%|86%|–|–|–|–|–|–|
|New Task 5|48%|56%|98%|82%|98%|–|–|–|–|–|
|New Task 6|38%|74%|88%|76%|72%|90%|–|–|–|–|
|New Task 7|40%|72%|54%|78%|76%|76%|54%|–|–|–|
|New Task 8|44%|76%|68%|62%|80%|72%|60%|100%|–|–|
|New Task 9|26%|84%|88%|74%|96%|86%|60%|100%|96%|–|
|**New Task 10**|34%|76%|88%|70%|94%|80%|64%|100%|98%|70%|


with _ω_ values of 0.1, 0.3, and 0.7. Specifically, when _ω_ increases to 0.9, the weight of CTAR ( _i.e._ , 1 _− ω_ = 0 _._ 1) within the total reward significantly decreases, diminishing its guidance for model exploration and leading to a drop in the average success rate to 90.0%. Furthermore, the influence of the FCR-weighting hyperparameter _λ_ on model performance is illustrated in Fig. 5 (b). Experimental results demonstrate that our method also exhibits strong robustness to variations in this parameter. In particular, we set _λ_ to 0.1, achieving optimal model performance. 

### _D. Visualization of Training Process_ 

To intuitively demonstrate the effectiveness of our proposed rewards during the reinforcement fine-tuning phase, Fig. 6 presents the multi-task learning dynamics on LIBERO-Goal. As shown in Fig. 6 (a), the multi-dimensional process reward, comprising QACR, CTAR, and FCR, exhibits a continuous growth trend during training, confirming that it achieves synergistic optimization of the policy across multiple dimensions. Furthermore, Fig. 6 (b) and (c) illustrate that QACR and CTAR maintain consistent growth, indicating that they effectively 


Fig. 5: Ablation study on the reward combination weights. 

incentivize the model to achieve precise manipulation. 


Fig. 6: Representative reward curves during the training phase. The visualizations illustrate the training evolution of (a) the Multi-Dimensional Process Reward, (b) QACR, and (c) CTAR. 

### _E. Generalization across Discrete Action Models_ 

To further validate the generalization of our approach across different discrete VLA models, we conduct comprehensive experiments built upon RoboBrain-X0 [27]. Table XIV demonstrates that LifeLong-RFT exhibits significant superiority across all four task suites. Specifically, on LIBEROSpatial, our approach yields a 12.2% improvement in FWT and a 13.3% reduction in NBT, demonstrating its capacity to efficiently acquire new skills while preserving previously learned knowledge. 

### _F. Real-World Case Studies_ 

To qualitatively analyze the performance of our method in real-world experiments, this section presents representative examples of execution across four tasks. 

_1) Pick Banana:_ As illustrated in Fig. 7, the task requires the model to accurately identify and grasp the banana from a cluttered scene containing various fruits, and subsequently place it stably into the blue plate. Notably, our method effectively overcomes interference from distractor objects and robustly completes the pick-and-place task. 

_2) Pick Bread:_ Fig. 8 demonstrates a representative execution of the Pick Bread task. The core challenge of this task lies in the precise insertion of the bread into the narrow toaster slot. The illustrated examples indicate that the model fine-tuned with LifeLong-RFT exhibits strong fine-grained manipulation capabilities, successfully completing this task. 

_3) Pull Drawer:_ As shown in Fig. 9, the Pull Drawer task involves interacting with an articulated object, requiring the model to accurately grasp the handle and pull the drawer. The primary difficulty stems from the requirement for strict coordination between the end-effector and the drawer’s linear motion to avoid jamming. Specifically, our approach demonstrates robust manipulation in constrained environments. 

_4) Hang Chinese Knot:_ Fig. 10 illustrates the execution of the Hang Chinese Knot task, which centers on manipulating a deformable object. The goal is to grasp the knot from the table and suspend it onto a cabinet-mounted hook. This task necessitates superior fine-grained manipulation skills, enabling the model to execute the hanging operation while adapting to the dynamic deformations of the Chinese knot. While our method demonstrates significant effectiveness, it also exhibits certain limitations, offering directions for future research. 

TABLE XIV: Continual learning performance of RoboBrainX0 on LIBERO. 

|**Task Split**|**Metrics**||**RoboBrain-**|**X0**|
|---|---|---|---|---|
|||SFT|**RFT (Ours)**|**∆**|
||FWT (_↑_)|86.6|94.0|+7.4|
|LIBERO-Object|NBT (_↓_)|16.1|1.5|-14.6|
||**AUC** (_↑_)|74.7|**92.4**|**+17.7**|
||FWT (_↑_)|80.4|92.6|+12.2|
|LIBERO-Spatial|NBT (_↓_)|21.0|7.7|-13.3|
||**AUC** (_↑_)|64.5|**86.9**|**+22.4**|
||FWT (_↑_)|68.8|84.0|+15.2|
|LIBERO-Goal|NBT (_↓_)|16.0|13.1|-2.9|
||**AUC** (_↑_)|56.5|**73.8**|**+17.3**|
||FWT (_↑_)|62.8|64.4|+1.6|
|LIBERO-Long|NBT (_↓_)|28.1|15.5|-12.6|
||**AUC** (_↑_)|40.8|**52.0**|**+11.2**|


Fig. 7: A representative execution of the _Pick Banana_ task. 


Fig. 8: A representative execution of the _Pick Bread_ task. 


Fig. 9: A representative execution of the _Pull Drawer_ task. 


Fig. 10: A representative execution of the _Hang Chinese Knot_ task. 

