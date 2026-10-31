---
title: "SRPO: Self-Referential Policy Optimization for Vision-Language-Action Models"
date: "2025-11-19"
authors: "Senyu Fei; Siyin Wang; Li Ji; Ao Li; Shiduo Zhang; Liming Liu"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2511.15605
pdf: https://arxiv.org/pdf/2511.15605
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.15605)** / [論文ページ](https://arxiv.org/abs/2511.15605)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **SRPO: Self-Referential Policy Optimization for Vision-Language-Action Models** 

Senyu Fei<sup>2</sup><sup>_,_3</sup><sup>_,†_</sup> Siyin Wang<sup>1</sup><sup>_,_3</sup><sup>_,†_</sup> Li Ji<sup>1</sup><sup>_,_3</sup> Ao Li<sup>3</sup> Shiduo Zhang<sup>1</sup> Liming Liu<sup>3</sup> Jinlong Hou<sup>3</sup> Jingjing Gong<sup>3</sup><sup>_,_�</sup> Xianzhong Zhao<sup>2</sup> Xipeng Qiu<sup>1</sup><sup>_,_3</sup><sup>_,_�</sup> 1Fudan University 2Tongji University 3Shanghai Innovation Institute feisenyu@outlook.com {siyinwang20, xpqiu}@fudan.edu.cn jjgongjj@gmail.com 

## **Abstract** 

_Vision-Language-Action (VLA) models excel in robotic manipulation but are constrained by their heavy reliance on expert demonstrations, leading to demonstration bias and limiting performance. Reinforcement learning (RL) is a vital post-training strategy to overcome these limits, yet current VLA-RL methods, including group-based optimization approaches, are crippled by severe reward sparsity. Relying on binary success indicators wastes valuable information in failed trajectories, resulting in low training efficiency. To solve this, we propose Self-Referential Policy Optimization (SRPO), a novel VLA-RL framework. SRPO eliminates the need for external demonstrations or manual reward engineering by leveraging the model’s own successful trajectories, generated within the current training batch, as a selfreference. This allows us to assign a progress-wise reward to failed attempts. A core innovation is the use of Latent World Representations to measure behavioral progress robustly. Instead of relying on raw pixels or requiring domain-specific fine-tuning, we utilize the compressed, transferable encodings from a world model’s latent space. These representations naturally capture progress patterns across environments, enabling accurate, generalized trajectory comparison. Empirical evaluations on the LIBERO benchmark demonstrate SRPO’s efficiency and effectiveness. Starting from a supervised baseline with 48.9% success, SRPO achieves a new state-of-the-art success rate of 99.2% in just 200 RL steps, representing a 103% relative improvement without any extra supervision. Furthermore, SRPO shows substantial robustness, achieving a 167% performance improvement on the LIBERO-Plus benchmark._ 

## **1. Introduction** 

Vision-Language-Action (VLA) models [6, 23, 43, 59] have demonstrated remarkable capabilities in robotic manipula- 

> _†_ Joint First Authors, �Corresponding Authors. 


Figure 1. Overview of Self-Referential Policy Optimization (SRPO). SRPO addresses reward sparsity in Vision-LanguageAction reinforcement learning by leveraging (i) in-batch trajectories as a reference and (ii) latent world representation for modeling behavioral progress. Our method enhances model performance and training efficiency without requiring the external demonstrations or task-specific reward engineering of previous Process Reward Modeling (PRM) approaches. 

tion by leveraging large-scale pre-trained vision-language models. However, existing VLA systems rely heavily on expert demonstrations and tend to overfit small downstream datasets, resulting in a strong demonstration bias that prevents them from surpassing human performance [15, 55]. To address such limitations, many recent studies have shown that reinforcement learning (RL) is an effective post-training strategy that can substantially improve VLA performance, both in-distribution and out-of-distribution [19, 29, 31]. Among RL methods, group-based optimization approaches such as GRPO [37] have become particularly attractive, providing a simple yet highly effective learning paradigm for VLA fine-tuning [27, 41, 53]. 

Despite the remarkable progress in GRPO, it still suffers from sparsity challenges in reward signals [8, 10, 33]. This issue becomes particularly pronounced in VLA domains, as the computational cost of multi-turn trajectory rollouts is substantially higher and the inadequate utilization of information from failed trajectories significantly reduces training 

6718 

efficiency. While recent work has explored process supervision to provide denser feedback, these approaches typically depend on expert demonstrations or hand-crafted task decompositions to define intermediate progress milestones [12, 31], creating scalability limitations that contradict the goal of autonomous learning. 

To address the reward sparsity challenge, we propose self-referential learning, where the model’s own successful trajectories serve as reference standards to evaluate and guide failed attempts. While GRPO leverages outcome-only rewards for advantage estimation, our approach utilizes the entire trajectory batch more efficiently. This paradigm transforms the supervision problem from “how do we obtain expert labels” to “how do we extract progress-wise reward from our own successes”. 

A central challenge in this paradigm lies in quantitatively measuring the behavioral similarity between successful and failed trajectories to assess progress towards task completion. Since trajectories are represented solely by visual observations, we require a reward model capable of extracting global state information to measure progress. While world models offer a natural approach for modeling such dynamics [1, 2, 44], traditional pixel-level world models suffer from poor generalization across domains or typically require extensive task-specific fine-tuning [49]. We address this limitation by leveraging the latent representations learned by world models, which we find naturally capture transferable behavioral progress patterns across different environments. These latent world representations enable robust trajectory comparison without requiring precise environmental reconstruction or domain-specific training. 

Building on these insights, we propose Self-Referential Policy Optimization (SRPO), which seamlessly integrates self-referential learning into the RL training structure. During each training iteration, we identify successful trajectories within the batch and use them as behavioral references through world model latent representations, while failed trajectories receive progress-wise rewards based on their behavioral alignment with successful patterns. We opt for trajectory-level rewards over fine-grained reward shaping as overly detailed hand-crafted dense signals can lead the policy to converge toward suboptimal solutions [26, 40]. 

Empirical evaluation on the LIBERO [28] benchmark demonstrates the transformative impact of our approach. Starting from a supervised fine-tuned baseline with just one demonstration per task and a 48.9% success rate, SRPO reaches 99.2% success in merely 200 reinforcement learning steps, representing 103% relative improvement that establishes new state-of-the-art performance. Importantly, this RL improvement requires no additional expert demonstrations or manual reward engineering. Our method also shows substantial improvements in robustness on the LIBERO-Plus [15] benchmark, with 167% performance improvement. Our 

proposed reward demonstrates its effectiveness in both simulation and real-world experiments. 

Our contributions are threefold as follow: 

1. We propose SRPO, a novel VLA reinforcement learning framework that mitigates reward sparsity by using modelgenerated successful trajectories to provide progress-wise rewards for failed attempts, eliminating reliance on expert demonstration or task-specific engineering. 

2. We introduce a latent world representation-based progress-wise reward method that overcomes the generalization limitations and domain-specific training requirements of traditional pixel-level world models. 

3. Experimental results demonstrate that our method achieves state-of-the-art performance on the LIBERO benchmark and exhibits strong generalization capabilities on LIBERO-Plus, while eliminating the need for additional supervision during RL training, establishing a new paradigm for autonomous VLA learning. 

## **2. Related Work** 

### **2.1. Vision-Language-Action Models** 

The remarkable success of models trained on vast internetscale datasets has demonstrated the power of scaling laws, motivating the field to increasingly focus on VisionLanguage-Action (VLA) models for transferring these capabilities to embodied agents [6, 23, 24, 35, 45, 59]. Due to the limited generalization and domain adaptability of supervised post-training, the field is increasingly turning to Reinforcement Learning (RL) to encourage exploration and enhance overall robustness [27, 29, 31]. These studies have explored the distinct characteristics of RL compared to SFT, employing RL algorithms to train both autoregressive [41] and diffusion-based VLAs [11], while also developing several integrated training-and-inference frameworks. However, these approaches often suffer from sparse reward signals, which prevent effective utilization of information from failure trajectories and limit training efficiency. To address this, we propose a novel VLA-RL framework that leverages dense, zero-shot transferable rewards to enable highly efficient policy learning. 

### **2.2. Reinforcement Learning** 

The application of Reinforcement Learning (RL) to Large Language Models (LLMs) has evolved significantly [13, 16, 18, 22, 42, 50]. RLHF [3] successfully aligned models with human preferences using algorithms like PPO [36]. RLVR [48] replacing expensive human preferences with automatically verifiable rewards. GRPO [37] bypasses the need for a learned reward model by using programmatic rewards. Recent works have also attempted to enhance stability and efficiency in optimization [46, 51, 52]. Since task success serves as a naturally verifiable reward, numerous works in 

6719 


Figure 2. Overview of the SRPO method. During policy rollout, both successful and failed trajectories are collected in the Rollout Reference Set. For each trajectory, we employ a world model pre-trained on large-scale robotics video data [2] as an encoder to extract latent world representations. Behavioral similarity is modeled as the L2 distance between trajectory embeddings in this space to yield progress-wise rewards. These rewards are subsequently used for advantage estimation and policy optimization under KL regularization. 

the VLA domain have attempted to optimize policies using GRPO with binary (0/1) rewards [27, 29, 41, 53], while facing the challenge of sparse reward signals. As robotic trajectory rollouts are more time-consuming and resourceintensive, some works have begun to construct rewards using hand-crafted or task-specific priors [12, 31, 38]. However, such methods requiring expert demonstrations or prior information are difficult to scale in online RL settings that encourage autonomous learning. To this end, we introduce a self-referential approach leveraging task-agnostic latent world representation to provide progress-wise rewards, thus fully utilizing failure trajectory information to enhance learning efficiency. 

## **3. Methodology** 

bution over actions given the current observation _ot_ , goal description _l_ . 

**The environment function** _zt_ +1 _∼ E_ ( _·|zt, at_ ) defines the stochastic transition from the current environment state _zt_ to the next environment state _zt_ +1 given the action _at_ taken by the agent. 

**Trajectory Rollout** is the process of generating a sequence of observations and actions over time, starting from an initial environment state _z_ 0. The trajectory _{_ ( _z_ 0 _, o_ 0 _, a_ 0 _, z_ 1 _, o_ 1 _, a_ 1 _, . . . , zT , oT_ ) _}_ are generated by iteratively applying these functions: 


### **3.1. Problem Formulation and Key Components** 

Given the current observation _ot_ at time step _t_ , and a goal description _l_ , the agent takes an action _at_ according to a policy _πθ_ ( _at|ot, l_ ) parameterized by _θ_ and conditioned on a goal description _l_ . The agent then receives the next observation _ot_ +1 from the environment, so on and so forth, until finally receiving a terminal observation _oT_ . If the agent successfully completes the task specified by the goal description _l_ , it receives a positive reward; otherwise, it receives reward depending on how close it is to completing the task. The objective is to learn a policy that maximizes the reward received over time for a variety of goals **l** and the initial state of the environment **z** . 

**The observation function** is defined as _ot ← O_ ( _zt_ ), where _O_ is the observation function that maps the environment state _zt_ to the partial observation _ot_ received by the agent. 

**Action generation** is modeled by the policy function _πθ_ ( _at|ot, l_ ) which is the _θ_ parameterized probability distri- 

Note that the state of the environment _zt_ is not directly accessible to the agent; instead, the agent relies on the observation _ot_ derived from _zt_ through the observation function _O_ . 

**The Reward function** _R_ ( _z_ 0: _T , l_ ) evaluates how well the state trajectory is performing in achieving the goal specified by _l_ . This reward is usually provided by the environment at the end of the episode, based on whether the goal described by _l_ has been achieved. However, these rewards could be provided sparsely as 0 and 1, making it difficult for the agent to learn effective policies through traditional reinforcement learning methods. To address this, we adapt a world model to shape rewards _R_<sup>ˆ</sup> ( _o_ 0: _T , S_ ) for the failed trajectories to provide more informative feedback during training, where we described in detail in Section 3.2. 

### **3.2. World progress reward modeling** 

As have mentioned earlier, neither the states _z_ 0: _T_ nor the reward function _R_ ( _z_ 0: _T , l_ ) are directly accessible to the 

6720 

agent. There is only the sparse terminal reward signal provided at the end of each episode. We propose a world model-based task-agnostic reward shaping mechanism to provide progress-wise signals for unsuccessful rollout trajectories. The reward can be shaped as _R_<sup>ˆ</sup> ( _o_ 0: _T , S_ ), where _S_ = _o_<sup>(</sup> 0:<sup>_i_)</sup> _T_<sup>;</sup><sup>_R_(</sup><sup>_z_</sup> 0:<sup>(</sup><sup>_i_</sup> _T_<sup>)</sup><sup>_, l_) = 1</sup><sup>_,∀i_</sup> is the observation set of � � successful trajectories. 

First, we encode the observations of the unsuccessful trajectory and the successful reference trajectories, with a world-model encoder _W_ , 


We then cluster the representations of the successful trajectories using the DBSCAN algorithm [14] to obtain a set of representative centers. The distance to the closest center representation is then calculated; a smaller distance indicates a larger reward. 


Finally, the reward is calculated with 


where _ϕ_ ( _·_ ) is an activation function transforming the output to the range (0 _,_ 1), and _d_<sup>¯</sup> and _σd_ are the mean and standard deviation, respectively, of the calculated distance for all failed trajectories. 

### **3.3. Self-Referential Policy Optimization** 

We introduce _Self-Referential Policy Optimization_ (SRPO), a novel policy optimization framework for VLA models that leverages latent world representations to enable **selfreferential advantage estimation** on **trajectory level** . 

Following GRPO, the probability ratio, advantage and regularization terms are 


The clipped surrogate objective is 


The overall SRPO objective, which we aim to maximize, is given by the expectation of the _L_ CLIP( _θ_ ) function. This expectation is computed over time steps _t_ and sample IDs _i_ within the current training group, with an additional regularization term applied to the parameters _θ_ . 


for simplicity, the expectation over different tasks _l_ and initial state _z_ 0 have been omitted. The group statistics are derived from world progress rewards as follows: 


This self-referential approach enables the policy to learn from relative performance within trajectory groups, where rewards _R_<sup>ˆ</sup> _j_ are computed through our world progress reward model rather than traditional task-specific rewards. The KL divergence _D_ KL( _πθ ∥ π_ ref) term maintains policy stability. 

## **4. Experiments** 

Our experimental design addresses several fundamental research questions: **RQ1:** Can SRPO achieve state-of-theart performance on standard benchmarks? **RQ2:** Does the method possess strong generalization capabilities to adapt to unseen task scenarios? **RQ3:** Can the latent world modelingbased reward mechanism accurately assess task progress, and does it outperform both pixel-level approaches and conventional video encoding methods? **RQ4:** Can SRPO improve training efficiency? **RQ5:** Can SRPO motivate novel trajectory exploration? **RQ6:** Whether the reward shaping method can successfully transfer to real-world robotic systems without requiring domain-specific expert demonstrations? 

### **4.1. Experimental Setup** 

Main experiments are conducted on the LIBERO [28] benchmark, specifically on Goal, Spatial, Object and Long suites, each of which contains 10 tasks for evaluating a distinct model capability. To evaluate generalization robustness, we employ the **LIBERO-Plus** [15] benchmark that introduces seven dimensions of perturbations. 

**Models.** For simulation experiments, we utilize a modified version of OpenVLA enhanced with action chunking and parallel decoding, which we refer to as **OpenVLA*** in the following sections. OpenVLA*-One refers to base model with one-traj-per-task SFT, while OpenVLA*-Full refers to full-shot SFT. More details can be found in Appendix G.1. 

**Baseline Methods.** Our baseline selection includes: _SimpleVLA-RL_ [27], _RIPT-VLA_ [41] and _RLinf_ [53] trained with GRPO, _VLA-RL_ [31] with PPO, _GRAPE_ [56] 

6721 

Table 1. Performance comparison on LIBERO benchmark. We evaluate mainstream VLA foundation models and RL-based methods. OpenVLA* incorporates action chunking and parallel decoding on the basis of OpenVLA. Our approach, built upon one-shot SFT, achieves state-of-the-art results on LIBERO benchmark, with _↑_ indicating performance gains over the one-shot baseline. 

|**Model**||**L**|**IBERO**|||
|---|---|---|---|---|---|
||Spatial|Object|Goal|Long|Avg|
|OpenVLA [23]|84.7|88.4|79.2|53.7|76.5|
|Pi0+fast [35]|96.4|96.8|88.6|60.2|85.5|
|Pi0 [6]|96.8|98.8|95.8|85.2|94.2|
|FASTer [30]|98.0|99.4|98.6|95.4|97.9|
|SmolVLA [39]|93.0|94.0|91.0|77.0|88.8|
|WorldVLA [9]|85.6|89.0|82.6|59.0|79.1|
|NORA [21]|92.2|95.4|89.4|74.6|87.9|
|CoT-VLA [57]|87.5|91.6|87.6|69.0|81.1|
|UniVLA [7]|96.5|96.8|95.6|92.0|95.2|
|TraceVLA [58]|84.6|85.2|75.1|54.1|74.8|
|MolmoAct [25]|87.0|95.4|87.6|77.2|86.6|
|ThinkAct [20]|88.3|91.4|87.1|70.9|84.4|
|GR00T N1 [5]|94.4|97.6|93.0|90.6|93.9|
|3D-CAVLA [4]|98.2|99.8|98.2|96.1|98.1|
|OpenVLA-OFT [24]|96.2|98.3|96.2|90.7|95.3|
|OpenVLA*-Full|91.6|95.3|90.6|86.5|91.0|
|TGRPO [12]|90.4|92.2|81.0|59.2|80.7|
|GRAPE [56]|88.5|92.1|83.1|57.2|80.2|
|VLA-RL [31]|90.2|91.8|82.2|59.8|81.0|
|World-Env [49]|87.6|86.6|86.4|57.8|79.6|
|SimpleVLA-RL [27]|98.2|98.7|98.8|91.7|96.9|
|RIPT-VLA [41]|99.0|98.6|98.6|93.8|97.5|
|RLinf [53]|**99.4**|99.8|98.8|94.0|98.0|
|OpenVLA*-One|63.6|54.9|59.6|17.3|48.9|
|+ Offline SRPO|92.5|96.8|92.0|88.7|92.5|
||_↑_28.9|_↑_41.9|_↑_32.4|_↑_71.4|_↑_43.6|
|**+ Online SRPO**|98.8<br>|**100.0**<br>|**99.4**<br>|**98.6**<br>|**99.2**<br>|
||_↑_35.2|_↑_45.1|_↑_39.8|_↑_81.3|_↑_50.3|


learning post-training. To obtain shared latent world representations, we employ large-scale video-pretrained latent world model _V-JEPA 2_ . Training details and compute reports are provided in the Appendix F. 

### **4.2. Main Results** 

Main results are summarized in Table 1, demonstrating that our approach achieves state-of-the-art performance in terms of the overall average success rate across all four suites. The key findings are as follows: 

**(1) Effectiveness of Online Post-Training:** While the initial one-shot SFT baseline shows modest performance, SRPO significantly improves upon it, validating the efficacy of our online post-training paradigm in enhancing policy performance through environment interaction. 

**(2) Superiority in Reward Design:** Our method outperforms RL-based methods like SimpleVLA-RL and RLinf, which rely on sparse outcome rewards, highlighting the importance of process rewards that provide denser supervisory signals. Furthermore, it surpasses approaches using manually designed process rewards like TGRPO and , demonstrates that self-reference-based rewards, derived from pretrained world models, offer a more effective learning signal than task-specific alternatives that require heuristic stage partitioning and reward tuning. 

**(3) SOTA Performance with Limited Inputs:** Despite using only third-person visual observations and language instructions as input, our method outperforms several baselines that utilize additional modalities such as multiple camera views, proprioception [6, 24, 35, 39] and 3D data [4]. This demonstrates that SRPO can achieve state-of-the-art performance relying solely on visual inputs, highlighting its effectiveness and practical applicability. 

### **4.3. Generalization Performance** 

with trajectory-wise DPO, _TGRPO_ [12] with task-specific progress reward, _World-Env_ [49] utilizing world model as simulator. We also provide some imitation learning methods [4–7, 9, 20, 21, 23–25, 35, 39, 57, 58] as reference, although they have different information inputs or pre-training data. 

**Implementation Details.** In the scope of this work, we consider the observation _ot_ to be the third view image, and the _l_ to be a language description of the goal. The environment is a physics simulator that takes in the current state _zt_ (including object positions, velocities, etc.) and the action _at_ (e.g., end-effector commands) to produce the next state _zt_ +1. The architecture of our policy is based on a pre-trained Visual-Language-Action model, which integrates visual inputs and language descriptions to inform the agent’s actions. 

We leverage SiiRL [47] to develop our training framework. Our pipeline begins with supervised fine-tuning using a single demonstration per task from the official checkpoint, followed by our SRPO method for online reinforcement 

To assess SRPO’s generalization, we validate two key aspects: (1) whether SRPO training in LIBERO environments improves generalization over SFT, and (2) whether SRPO is more robust to perturbations than training on the precollected LIBERO-Plus dataset. The following key findings are summarized from Table 2: 

(1) **SRPO Overcomes the Diversity Limitation of OneShot SFT.** While the one-shot SFT baseline exhibits weak generalization due to limited trajectory diversity, SRPO posttraining enables it to surpass even the full-shot SFT policy. This is attributed to SRPO’s online interaction, which explores a broader range of trajectories than those contained in the static full-shot dataset. A detailed analysis of this trajectory diversity advantage is provided in Section 5.3. 

(2) **SRPO also Surpasses Full-Shot SFT in Perturbed Data Settings.** When trained in perturbed environments, our method not only exceeds the performance of the full-shot SFT baseline but also outperforms OpenVLA-OFT (utilizes 

6722 

Table 2. Robustness Evaluation on LIBERO-Plus Benchmark. OpenVLA-OFT+ refers to the OpenVLA-OFT model that has been trained on the LIBERO-Plus dataset. Our method, SRPO, applied to a one-shot SFT policy, not only significantly outperforms its base model but also surpasses the full-shot SFT baseline in all 7 dimensions, demonstrating superior generalization capability. The _↑_ indicates performance gains over the One-shot SFT base model. 

|**Setting**|**Model**|||**Perturbat**|**ion Dim**|**ensions**|||**Total**|
|---|---|---|---|---|---|---|---|---|---|
|||Camera|Robot-Init|Language|Light|Background|Noise|Layout||
||Pi0|13.8|6.0|58.8|85.0|81.4|79.0|68.9|53.6|
||Pi0+fast|65.1|21.6|61.0|73.2|73.2|74.4|68.8|61.6|
||UniVLA|1.8|46.2|69.6|69.0|81.0|21.2|31.9|42.9|
||WorldVLA|0.1|27.9|41.6|43.7|17.1|10.9|38.0|25.0|
|**t**|OpenVLA|0.8|3.5|23.0|8.1|34.8|15.2|28.5|15.6|
|**ho**|OpenVLA-OFT|56.4|31.9|79.5|88.7|93.3|75.8|74.2|69.6|
|**o-S**|OpenVLA-OFT_w|10.4|38.7|70.5|76.8|93.6|49.9|69.9|55.8|
|**er**|OpenVLA-OFT_m|55.6|21.7|81.0|92.7|91.0|78.6|68.7|67.9|
|**Z**|NORA-long|2.2|37.0|65.1|45.7|58.6|12.8|62.1|39.0|
||RIPT-VLA|55.2|31.2|77.6|88.4|91.6|73.5|74.2|68.4|
||OpenVLA*-Full|12.8|39.4|68.5|63.4|75.0|34.8|62.7|51.1|
||OpenVLA*-One|3.2|14.0|27.6|25.7|32.7|6.4|26.4|19.4|
||+ Online SRPO|17.1|51.0|81.8|70.4|88.9|35.3|72.4|59.6|
|||_↑_13.9|_↑_37.0|_↑_54.2|_↑_44.7|_↑_56.2|_↑_28.9|_↑_46.0|_↑_40.2|
|**ta**|OpenVLA-OFT+|92.8|30.3|85.8|94.9|93.9|89.3|77.6|79.5|
|**Da**|OpenVLA*-Full|69.4|49.6|66.3|88.2|88.5|78.7|70.3|73.0|
|**+**|OpenVLA*-One|12.8|23.0|30.0|42.0|49.6|23.3|34.5|30.7|
||+ Online SRPO|83.4|62.0|73.6|97.2|97.7|85.7|75.2|82.1|
|||_↑_70.6|_↑_39.0|_↑_43.6|_↑_55.2|_↑_48.1|_↑_62.4|_↑_40.7|_↑_51.4|


additional wrist image and proprioception) trained with fullshot SFT. This result underscores that the trajectory diversity afforded by SRPO plays a major role in improving generalization, compensating for and exceeding the advantage of more complex input modalities. 

## **5. Analysis** 

Table 3. Progress Reward Benchmark Results. Our method achieved a better level than the baseline in all 5 indicators. 

|**Method**|**SC**|**Mono**|**MMD**|**JS**|**SMD**|
|---|---|---|---|---|---|
|Pixel-level|0.125|0.498|0.274|0.548|2.100|
|ImageBind|0.957|0.837|0.356|0.408|18.111|
|SRPO (Ours)|**0.998**|**0.992**|**0.615**|**0.572**|**188.799**|


### **5.1. Can Latent World Representation Improve Reward Shaping?** 

We compare our approach against two alternative reward formulations: (1) pixel-level progress reward [48], which computes similarity based on pixel-wise features, and (2) ImageBind-based progress reward, derived from the generalpurpose vision embeddings model ImageBind [17]. 

**Qualitative Visualization.** We evaluate our progress reward approach on several tasks (e.g., placing a cup in a microwave, tidying a desk). As shown in Figure 3, our method produces smoother, more monotonic progress curves that better reflect task structure, especially for longhorizon tasks with repeated sub-tasks. In contrast, pixellevel and ImageBind-based methods generate fluctuating, non-monotonic progress signals. This improvement comes from embedding entire trajectories into a latent space that 

captures physical regularities, allowing for more accurate estimation about task progress. Further reward curves and success/failure trajectory examples are provided in Appendix B. 

**Quantitative Comparison.** We carefully selected 700 success trajectories progressing steadily towards the goal and 300 failure trajectories from multiple tasks in both simulation and real-world environment. We establish five metrics for evaluating progress rewards: _Spearman Correlation (SC)_ and _Monotonicity (Mono)_ are computed exclusively on success trajectories to measure the positive correlation with frame numbers and the trajectory’s monotonicity, respectively; _Maximum Mean Discrepancy (MMD)_ , _JS Divergence (JS)_ , and _Standardized Mean Difference (SMD)_ are statistical measures that quantify the distinguishability between 

6723 


Figure 3. Comparison of progress estimation methods in simulated (a-c) and real-world (d-f) environments. Our SRPO reward (a,d) provides monotonic and physically plausible progress estimation. Pixel-level rewards (b,e) show sensitivity to perceptual changes, while ImageBind rewards (c,f) exhibit erratic trends from jerky motions. 


Figure 4. Training performance comparison using different progress reward formulations. Our SRPO-based reward enables stable and efficient learning, consistently outperforming both baselines and achieving superior final performance. 

success and failure trajectories. For all five metrics, a higher value indicates better performance. As shown in Table 3, our method provides more reasonable progress rewards for intermediate failure states and better distinguishes between success and failure trajectories, thereby more effectively utilizing the failure trajectories. The detailed formulations of our bench are provided in Appendix A. 

**Training Effectiveness.** As shown in Figure 4, the pixellevel method exhibits notably slow convergence, suggesting that its reward signal provides insufficient guidance for effective policy optimization. While ImageBind demonstrates faster initial learning compared to the pixel-level approach, its performance plateaus around 85% without further improvement, indicating that the suboptimal progress estimation hinders the model’s ability to extract useful information from failure trajectories, ultimately causing training stagnation. We argue that the _pixel-level_ method is fundamentally 


Figure 5. Training efficiency comparison between SRPO and GRPO: (a) LIBERO-Long, (b) LIBERO-Object. 

limited because it relies solely on the final frame as and exhibites sensitivity to minor pixel changes, and general visual model like _ImageBind_ lacks the capability of understanding robotics-relevant physical concepts. Our experimental results confirm that effective progress estimation for VLAs requires rewards grounded in _world progress_ rather than simple perceptual similarity. 

### **5.2. Can SRPO Improve Training Efficiency?** 

Our results across the four suites are obtained using 79 steps (Spatial), 59 steps (Object), 103 steps (Goal), and 219 steps (Long), demonstrating significant advantages over SFT which requires tens of thousands of steps. Meanwhile, we compare the efficiency differences between SRPO and GRPO, as shown in Figure 5. The results clearly indicate that SRPO achieves a steeper efficiency slope than GRPO, especially for long-horizon tasks. Unlike GRPO, which essentially discards unsuccessful episodes, our self-referential framework can extract valuable learning signals from nearsuccessful trajectories by recognizing and rewarding the productive segments within them, thereby guiding the policy 

6724 

more efficiently towards the final goal. 

### **5.3. Can SRPO Motivate Novel Trajectory Exploration?** 


Figure 6. Action space comparison of end-effector trajectories between (a) full-shot supervised fine-tuning (SFT) and (b) SRPO online reinforcement learning (RL) policies. 

A fundamental limitation of imitation learning is its inherent constraint to the state-action distribution present in the demonstration data. To quantitatively assess whether SRPO enables the policy to transcend these limitations and explore beyond the demonstrator’s domain, we analyze the diversity of actions generated by the policy in _LIBERO-Spatial_ task suite. We performed rollouts on this suite using both the fullshot SFT weights and the RL fine-tuned weights, executing 10 trajectory episodes per task, with end-effector positions utilized as actions, which is visualize in Figure 6. 

The results demonstrate that the online RL-trained policy exhibits two key advantages over the SFT baseline in terms of action distribution: (1) it explores previously unreachable regions; and (2) it generates more dispersed trajectories, indicating the model’s propensity for spatial exploration rather than merely fitting to specific demonstration paths. More details are provided in Appendix. 

### **5.4. Can world progress rewarding modeling extend to real-world?** 

In this section, we investigate whether our proposed latent world progress rewarding method can effectively generalize to real-world robotic tasks. To this end, we conduct experiments with offline RL approach on five real-world manipulation tasks performed on an X-ARM 7 robot: _Put apple into the plate_ , _Put pear into the plate_ , _Folding towels_ , _Cleaning whiteboard_ and _Select Poker_ . 

For each task, we compare two state-of-the-art visionlanguage-action (VLA) policy backbones: _π_ 0 (a diffusionbased VLA model) and _π_ 0-FAST (an autoregressive VLA 


Figure 7. Real-world task success rates comparing supervised fine-tuning (SFT) baselines against our offline RL approach. Our method consistently improves performance across both diffusionbased ( _π_ 0) and autoregressive ( _π_ 0-FAST) VLA policies. 

enhanced with frequency-space tokenization). Both models are compared against standard supervised fine-tuning (SFT) baselines. 

Both the diffusion-based _π_ 0 and autoregressive _π_ 0-FAST models demonstrate substantial performance improvements when enhanced with our reward shaping method, with average gains of + **66** _._ **8** % and + **86** _._ **7** %, respectively. The most significant improvements are observed on tasks involving object placement and manipulation, underscoring the method’s efficacy in adapting to perceptual variations. These consistent and substantial improvements across diverse tasks and policy architectures confirm that progress-aware reward modeling effectively transfers to real-world robotic manipulation, enabling more efficient policy optimization through better credit assignment and progression-aware weighting. 

## **6. Conclusion** 

In this paper, we introduce Self-Referential Policy Optimization (SRPO), a novel VLA reinforcement learning approach leveraging task-agnostic latent world representation to provide progress-wise reward. By using self-referential learning, we eliminate reliance on expert demonstration or task-specific engineering, and develop an efficient VLA RL framework that can fully utilize the information provided by the failure trajectories, achieving significant improvements in both performance and efficiency compared to the existing methods. Further analysis demonstrates that our method improves reward shaping, motivates novel trajectory exploration, and the world progress reward modeling can be effectively applied to real-world robotic tasks. This work establishes a novel paradigm for efficient VLA reinforcement learning by demonstrating that pre-trained world model latent representations provide a powerful, generic substrate for progress assessment. 

6725 

## **Acknowledgements** 

This work was supported by the National Natural Science Foundation of China (No. 62521004). 

## **References** 

- [1] Arslan Ali, Junjie Bai, Maciej Bala, Yogesh Balaji, Aaron Blakeman, Tiffany Cai, Jiaxin Cao, Tianshi Cao, Elizabeth Cha, Yu-Wei Chao, et al. World simulation with video foundation models for physical ai. _arXiv preprint arXiv:2511.00062_ , 2025. 2, 4, 10 

- [2] Mido Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Matthew Muckley, Ammar Rizvi, Claire Roberts, Koustuv Sinha, Artem Zholus, et al. V-jepa 2: Selfsupervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 2, 3 

- [3] Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda Askell, Anna Chen, Nova DasSarma, Dawn Drain, Stanislav Fort, Deep Ganguli, Tom Henighan, et al. Training a helpful and harmless assistant with reinforcement learning from human feedback. _arXiv preprint arXiv:2204.05862_ , 2022. 2 

- [4] Vineet Bhat, Yu-Hsiang Lan, Prashanth Krishnamurthy, Ramesh Karri, and Farshad Khorrami. 3d cavla: Leveraging depth and 3d context to generalize vision language action models for unseen tasks. _arXiv preprint arXiv:2505.05800_ , 2025. 5 

- [5] Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 5 

- [6] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A visionlanguage-action flow model for general robot control. corr, abs/2410.24164, 2024. doi: 10.48550. _arXiv preprint ARXIV.2410.24164_ . 1, 2, 5 

- [7] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 5 

- [8] Meng Cao, Lei Shu, Lei Yu, Yun Zhu, Nevan Wichers, Yinxiao Liu, and Lei Meng. Enhancing reinforcement learning with dense rewards from language model critic. In _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ , pages 9119–9138, 2024. 1 

- [9] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 5 

- [10] Alex J Chan, Hao Sun, Samuel Holt, and Mihaela Van Der Schaar. Dense reward for free in reinforcement learning from human feedback. _arXiv preprint arXiv:2402.00782_ , 2024. 1 

- [11] Kang Chen, Zhihao Liu, Tonghe Zhang, Zhen Guo, Si Xu, Hao Lin, Hongzhi Zang, Quanlu Zhang, Zhaofei Yu, Guoliang 

Fan, et al. _π_ -rl: Online rl fine-tuning for flow-based visionlanguage-action models. _arXiv preprint arXiv:2510.25889_ , 2025. 2 

- [12] Zengjue Chen, Runliang Niu, He Kong, and Qi Wang. Tgrpo :fine-tuning vision-language-action model via trajectory-wise group relative policy optimization. _ArXiv_ , abs/2506.08440, 2025. 2, 3, 5 

- [13] Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit Dhillon, Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities. _arXiv preprint arXiv:2507.06261_ , 2025. 2 

- [14] Martin Ester, Hans-Peter Kriegel, Jörg Sander, Xiaowei Xu, et al. A density-based algorithm for discovering clusters in large spatial databases with noise. In _kdd_ , pages 226–231, 1996. 4 

- [15] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, et al. Libero-plus: In-depth robustness analysis of visionlanguage-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 1, 2, 4 

- [16] Zhaoye Fei, Li Ji, Siyin Wang, Junhao Shi, Jingjing Gong, and Xipeng Qiu. Unleashing embodied task planning ability in llms via reinforcement learning. _ArXiv_ , abs/2506.23127, 2025. 2 

- [17] Rohit Girdhar, Alaaeldin El-Nouby, Zhuang Liu, Mannat Singh, Kalyan Vasudev Alwala, Armand Joulin, and Ishan Misra. Imagebind: One embedding space to bind them all. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 15180–15190, 2023. 6 

- [18] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ , 2025. 2 

- [19] Yanjiang Guo, Jianke Zhang, Xiaoyu Chen, Xiang Ji, Yen-Jen Wang, Yucheng Hu, and Jianyu Chen. Improving visionlanguage-action model with online reinforcement learning. _arXiv preprint arXiv:2501.16664_ , 2025. 1 

- [20] Chi-Pin Huang, Yueh-Hua Wu, Min-Hung Chen, YuChiang Frank Wang, and Fu-En Yang. Thinkact: Visionlanguage-action reasoning via reinforced visual latent planning. _arXiv preprint arXiv:2507.16815_ , 2025. 5 

- [21] Chia-Yu Hung, Qi Sun, Pengfei Hong, Amir Zadeh, Chuan Li, U Tan, Navonil Majumder, Soujanya Poria, et al. Nora: A small open-sourced generalist vision language action model for embodied tasks. _arXiv preprint arXiv:2504.19854_ , 2025. 

   - 5 

- [22] Aaron Jaech, Adam Kalai, Adam Lerer, Adam Richardson, Ahmed El-Kishky, Aiden Low, Alec Helyar, Aleksander Madry, Alex Beutel, Alex Carney, et al. Openai o1 system card. _arXiv preprint arXiv:2412.16720_ , 2024. 2 

- [23] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag R. Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey 

6726 

Levine, Percy Liang, and Chelsea Finn. Openvla: An opensource vision-language-action model. _ArXiv_ , abs/2406.09246, 2024. 1, 2, 5 

- [24] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _ArXiv_ , abs/2502.19645, 2025. 2, 5 

- [25] Jason Lee, Jiafei Duan, Haoquan Fang, Yuquan Deng, Shuo Liu, Boyang Li, Bohan Fang, Jieyu Zhang, Yi Ru Wang, Sangho Lee, et al. Molmoact: Action reasoning models that can reason in space. _arXiv preprint arXiv:2508.07917_ , 2025. 5 

- [26] Sergey Levine. Sporks of agi, 2024. Substack blog post. 2 

- [27] Hao-Si Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang, Tianxing Chen, Ganqu Cui, Dehui Wang, Dingxiang Luo, Yuchen Fan, Youbang Sun, Jia Zeng, Jiangmiao Pang, Shanghang Zhang, Yu Wang, Yao Mu, Bowen Zhou, and Ning Ding. Simplevla-rl: Scaling vla training via reinforcement learning. _ArXiv_ , abs/2509.09674, 2025. 1, 2, 3, 4, 5 

- [28] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 2, 4 

- [29] Jijia Liu, Feng Gao, Bingwen Wei, Xinlei Chen, Qingmin Liao, Yi Wu, Chao Yu, and Yu Wang. What can rl bring to vla generalization? an empirical study. _arXiv preprint arXiv:2505.19789_ , 2025. 1, 2, 3 

- [30] Yicheng Liu, Shiduo Zhang, Zibin Dong, Baijun Ye, Tianyuan Yuan, Xiaopeng Yu, Linqi Yin, Chenhao Lu, Junhao Shi, Luca Jiang-Tao Yu, Liangtao Zheng, Jingjing Gong, Tao Jiang, Xipeng Qiu, and Hang Zhao. Faster: Toward powerful and efficient autoregressive vision–language–action models with learnable action tokenizer and block-wise decoding. https: //openreview.net/forum?id=k6nTUFoqeT, 2025. ICLR 2026 Conference submission. 5 

- [31] Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Hao Jiang, Zifeng Gao, Yansong Tang, and Ziwei Wang. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning. _ArXiv_ , abs/2505.18719, 2025. 1, 2, 3, 4, 5 

- [32] Yecheng Jason Ma, Joey Hejna, Chuyuan Fu, Dhruv Shah, Jacky Liang, Zhuo Xu, Sean Kirmani, Peng Xu, Danny Driess, Ted Xiao, et al. Vision language models are in-context value learners. In _The Thirteenth International Conference on Learning Representations_ , 2024. 6 

- [33] Tongzhou Mu, Minghua Liu, and Hao Su. Drs: Learning reusable dense rewards for multi-stage tasks. _arXiv preprint arXiv:2404.16779_ , 2024. 1 

- [34] Xue Bin Peng, Aviral Kumar, Grace Zhang, and Sergey Levine. Advantage-weighted regression: Simple and scalable off-policy reinforcement learning. _arXiv preprint arXiv:1910.00177_ , 2019. 4 

- [35] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. _ArXiv_ , abs/2501.09747, 2025. 2, 5 

- [36] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 2 

- [37] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 1, 2 

- [38] Junyang Shu, Zhiwei Lin, and Yongtao Wang. Rftf: Reinforcement fine-tuning for embodied agents with temporal feedback. _arXiv preprint arXiv:2505.19767_ , 2025. 3 

- [39] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 5 

- [40] Rich Sutton. The bitter lesson. http : / / www . incompleteideas.net/IncIdeas/BitterLesson.html, 2019. Accessed: 2025-11-12. 2 

- [41] Shuhan Tan, Kairan Dou, Yue Zhao, and Philipp Krähenbühl. Interactive post-training for vision-language-action models. _ArXiv_ , abs/2505.17016, 2025. 1, 2, 3, 4, 5 

- [42] Kimi Team, Angang Du, Bofei Gao, Bowei Xing, Changjiu Jiang, Cheng Chen, Cheng Li, Chenjun Xiao, Chenzhuang Du, Chonghua Liao, et al. Kimi k1. 5: Scaling reinforcement learning with llms. _arXiv preprint arXiv:2501.12599_ , 2025. 2 

- [43] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 1 

- [44] Siyin Wang, Zhaoye Fei, Qinyuan Cheng, Shiduo Zhang, Panpan Cai, Jinlan Fu, and Xipeng Qiu. World modeling makes a better planner: Dual preference optimization for embodied task planning. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 21518–21537, Vienna, Austria, 2025. Association for Computational Linguistics. 2 

- [45] Siyin Wang, Jinlan Fu, Feihong Liu, Xinzhe He, Huangxuan Wu, Junhao Shi, Kexin Huang, Zhaoye Fei, Jingjing Gong, Zuxuan Wu, Yugang Jiang, See-Kiong Ng, Tat-Seng Chua, and Xipeng Qiu. Roboomni: Proactive robot manipulation in omni-modal context. _ArXiv_ , abs/2510.23763, 2025. 2 

- [46] Shenzhi Wang, Le Yu, Chang Gao, Chujie Zheng, Shixuan Liu, Rui Lu, Kai Dang, Xionghui Chen, Jianxin Yang, Zhenru Zhang, et al. Beyond the 80/20 rule: High-entropy minority tokens drive effective reinforcement learning for llm reasoning. _arXiv preprint arXiv:2506.01939_ , 2025. 2 

- [47] Zhixin Wang, Tianyi Zhou, Liming Liu, Ao Li, Jiarui Hu, Dian Yang, Jinlong Hou, Siyuan Feng, Yuan Cheng, and Yuan Qi. Distflow: A fully distributed rl framework for scalable and efficient llm post-training, 2025. 5 

- [48] Xumeng Wen, Zihan Liu, Shun Zheng, Shengyu Ye, Zhirong Wu, Yang Wang, Zhijian Xu, Xiao Liang, Junjie Li, Ziming Miao, et al. Reinforcement learning with verifiable rewards implicitly incentivizes correct reasoning in base llms. _arXiv preprint arXiv:2506.14245_ , 2025. 2, 6 

6727 

- [49] Junjin Xiao, Yandan Yang, Xinyuan Chang, Ronghan Chen, Feng Xiong, Mu Xu, Wei-Shi Zheng, and Qing Zhang. Worldenv: Leveraging world model as a virtual environment for vla post-training. _arXiv preprint arXiv:2509.24948_ , 2025. 2, 5 

- [50] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ , 2025. 2 

- [51] Shihui Yang, Chengfeng Dou, Peidong Guo, Kai Lu, Qiang Ju, Fei Deng, and Rihui Xin. Dcpo: Dynamic clipping policy optimization. _arXiv preprint arXiv:2509.02333_ , 2025. 2 

Hausman, Keerthana Gopalakrishnan, Chuyuan Fu, Pete Florence, Chelsea Finn, Kumar Avinava Dubey, Danny Driess, Tianli Ding, Krzysztof Marcin Choromanski, Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah Brown, Anthony Brohan, Montserrat Gonzalez Arenas, and Kehang Han. RT-2: vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning, CoRL 2023, 6-9 November 2023, Atlanta, GA, USA_ , pages 2165– 2183. PMLR, 2023. 1, 2 

- [52] Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, Yu Yue, Weinan Dai, Tiantian Fan, Gaohong Liu, Lingjun Liu, et al. Dapo: An open-source llm reinforcement learning system at scale. _arXiv preprint arXiv:2503.14476_ , 2025. 2 

- [53] Hongzhi Zang, Mingjie Wei, Si Xu, Yongji Wu, Zhen Guo, Yuanqing Wang, Hao Lin, Liangzhi Shi, Yuqing Xie, Zhexuan Xu, et al. Rlinf-vla: A unified and efficient framework for vla+ rl training. _arXiv preprint arXiv:2510.06710_ , 2025. 1, 3, 4, 5 

- [54] Shaopeng Zhai, Qi Zhang, Tianyi Zhang, Fuxian Huang, Haoran Zhang, Ming Zhou, Shengzhe Zhang, Litao Liu, Sixu Lin, and Jiangmiao Pang. A vision-language-action-critic model for robotic real-world reinforcement learning. _arXiv preprint arXiv:2509.15937_ , 2025. 6 

- [55] Shiduo Zhang, Zhe Xu, Peiju Liu, Xiaopeng Yu, Yuan Li, Qinghui Gao, Zhaoye Fei, Zhangyue Yin, Zuxuan Wu, YuGang Jiang, et al. Vlabench: A large-scale benchmark for language-conditioned robotics manipulation with longhorizon reasoning tasks. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 11142– 11152, 2025. 1 

- [56] Zijian Zhang, Kaiyuan Zheng, Zhaorun Chen, Joel Jang, Yi Li, Siwei Han, Chaoqi Wang, Mingyu Ding, Dieter Fox, and Huaxiu Yao. Grape: Generalizing robot policy via preference alignment. _arXiv preprint arXiv:2411.19309_ , 2024. 4, 5 

- [57] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713, 2025. 5 

- [58] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daum’e, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatialtemporal awareness for generalist robotic policies. _ArXiv_ , abs/2412.10345, 2024. 5 

- [59] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong T. Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi, Grecia Salazar, Michael S. Ryoo, Krista Reymann, Kanishka Rao, Karl Pertsch, Igor Mordatch, Henryk Michalewski, Yao Lu, Sergey Levine, Lisa Lee, Tsang-Wei Edward Lee, Isabel Leal, Yuheng Kuang, Dmitry Kalashnikov, Ryan Julian, Nikhil J. Joshi, Alex Irpan, Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol 

6728 

