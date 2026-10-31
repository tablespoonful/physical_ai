---
title: "Efficient Reinforcement Learning by Guiding World Models with Non-Curated Data"
date: "2025-02-26"
authors: "Yi Zhao; Aidan Scannell; Wenshuai Zhao; Yuxin Hou; Tianyu Cui; Le Chen"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2502.19544
pdf: https://arxiv.org/pdf/2502.19544
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2502.19544)** / [論文ページ](https://arxiv.org/abs/2502.19544)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Published as a conference paper at ICLR 2026 

# EFFICIENT REINFORCEMENT LEARNING BY GUIDING WORLD MODELS WITH NON-CURATED DATA 

**Yi Zhao**<sup>_†_1</sup> **Aidan Scannell**<sup>1</sup><sup>_,_2</sup> **Wenshuai Zhao**<sup>1</sup><sup>_,_3</sup> **Yuxin Hou**<sup>4</sup> **Tianyu Cui**<sup>1</sup><sup>_,_5</sup> **Le Chen**<sup>6</sup> **Dieter B¨uchler**<sup>6</sup><sup>_,_7</sup><sup>_,_8</sup><sup>_,_9</sup> **Arno Solin**<sup>1</sup><sup>_,_3</sup> **Juho Kannala**<sup>1</sup><sup>_,_10</sup> **Joni Pajarinen**<sup>1</sup> 1Aalto University 2University of Edinburgh 3ELLIS Institute Finland 4Deep Render 5Imperial College London 6Max Planck Institute for Intelligent Systems 7CIFAR AI Chair 8University of Alberta 9Alberta Machine Intelligence Institute (Amii) 10University of Oulu 

### ABSTRACT 

Leveraging offline data is a promising way to improve the sample efficiency of online reinforcement learning (RL). This paper expands the pool of usable data for offline-to-online RL by leveraging abundant non-curated data that is reward-free, of mixed quality, and collected across multiple embodiments. Although learning a world model appears promising for utilizing such data, we find that naive finetuning fails to accelerate RL training on many tasks. Through careful investigation, we attribute this failure to the distributional shift between offline and online data during fine-tuning. To address this issue and effectively use the offline data, we propose two techniques: _i)_ experience rehearsal and _ii)_ execution guidance. With these modifications, the non-curated offline data substantially improves RL’s sample efficiency. Under limited sample budgets, our method achieves nearly twice the aggregate score of learning-from-scratch baselines across 72 visuomotor tasks spanning 6 embodiments. On challenging tasks such as locomotion and robotic manipulation, it outperforms prior methods that utilize offline data by a decent margin. 

### 1 INTRODUCTION 

Leveraging offline data offers a promising way to improve the sample efficiency of reinforcement learning (RL). Prior work has focused primarily on utilizing curated offline data labeled with rewards (Levine et al., 2020; Kumar et al., 2020; Fujimoto & Gu, 2021; Kumar et al., 2023), which is expensive and laborious to obtain. For instance, leveraging offline datasets for new robotic manipulation tasks requires retrospectively annotating image-based data with rewards. We instead propose expanding the pool of usable offline data by utilizing abundant non-curated data that is reward-free, of mixed quality, and collected across multiple embodiments. This leads to our main research question: 

#### _How can we effectively leverage non-curated offline data for efficient RL?_ 

Typical offline-to-online RL methods (Lee et al., 2022; Zhao et al., 2022; Yu & Zhang, 2023; Nakamoto et al., 2024; Nair et al., 2020) fail to utilize non-curated offline data due to their assumption of structured data with rewards. While pre-training visual encoders (Schwarzer et al., 2021; Nair et al., 2022; Parisi et al., 2022; Xiao et al., 2022; Yang & Nachum, 2021; Shang et al., 2024) is a common approach to utilize non-curated offline datasets, it fails to fully leverage the rich information, such as dynamics models, informative states, and action priors for policy learning. On the other hand, learning world models from offline data appears promising for utilizing the non-curated dataset. However, prior work has explored world model training primarily in settings with known rewards (Lu et al., 2023; Rafailov et al., 2023; Hansen et al., 2024) or expert demonstrations (Zhu et al., 2024a; Zhou et al., 2024; Gao et al., 2025) or focused solely on visual prediction (Zheng et al., 2024; Zhu et al., 2024b). Recent approaches (Seo et al., 2022; Wu et al., 2024; 2025) have developed novel architectures for world model pre-training using in-the-wild action-free data, but paid limited 

> _†_ Correspondence to yi.zhao@aalto.fi. Code and datasets: https://github.com/zhaoyi11/ncrl. 

1 

Published as a conference paper at ICLR 2026 


Figure 1: **Overview of NCRL (Non-curated offline data for efficient RL).** NCRL leverages noncurated offline data—reward-free, mixed-quality, and multi-embodiment—to enable efficient RL. It uses this data to pretrain a task-agnostic world model, and then, during fine-tuning, to reduce distributional shift and guide exploration through experience rehearsal and execution guidance. 

attention to the fine-tuning process. As a result, despite being trained on massive datasets, these methods show only marginal improvements over training-from-scratch baselines. Additionally, due to the computational costs of RL experiments, previous work (Wu et al., 2024; 2025) evaluated only on a small set of tasks, leaving the effectiveness of the learned world model unclear on broader tasks. In contrast, we extensively evaluate our method on 72 visuomotor control tasks spanning both locomotion and robotic manipulation, demonstrating consistent improvements over existing approaches. 

Through experiments, we observe that naively fine-tuning a world model fails to improve RL’s sample efficiency on many tasks. With careful investigation, we identify the root cause as a distributional shift between offline data used for pre-training and online data used for RL fine-tuning. Specifically, when the offline data distribution does not sufficiently cover the data distribution of downstream tasks, the pre-trained world models struggle to benefit policy learning due to this distribution mismatch, shown in Fig. 2. Building on these insights, we propose using non-curated offline data in _both_ pre-training and fine-tuning stages, in contrast to previous methods that only consider the offline data for world model pre-training (Wu et al., 2025; Yuan et al., 2022; Rajeswar et al., 2023). To this end, we propose a pipeline named Non-curated offline data for efficient RL (NCRL). In the pre-training stage, NCRL learns a task-agnostic world model from non-curated offline data that is reward-free, mix-quality and task-agnostic. In the fine-tuning stage, NCRL reuses this data through _experience rehearsal_ and _execution guidance_ to mitigate distributional shift by retrieving task-relevant trajectories and to prompt exploration by steering the agent toward regions where the world model has high confidence. 

Equipped with our proposed techniques, NCRL demonstrates strong performance across a diverse set of tasks. Specifically, under a limited sample budget (150k samples), NCRL achieves almost double the aggregate score of learning-from-scratch baselines (DrQ-v2 and DreamerV3), while matching their performance achieved with larger sample budgets. On representative challenging tasks, NCRL outperforms baselines that leverage offline data as well as state-of-the-art methods using pre-trained world models by a significant margin. Additionally, without any modifications, we show that NCRL improves task adaptation, enabling agents to efficiently adapt their skills to new tasks. To summarize, our contributions are: 

> **C1** We propose a more realistic setting for leveraging offline data that consists of reward-free and mixed-quality multi-embodiment data. 

2 

Published as a conference paper at ICLR 2026 

Table 1: Comparison with different policy learning methods that leverage offline data. 

||**Offline RL**|**Off2On RL**|**RLPD**|**MT Offline RL**|**NCRL (ours)**|
|---|---|---|---|---|---|
|Reward-free offline data|✗|✗|✗|✗|✓|
|Non-expert offline data|✓|✓|✓|✓|✓|
|X-embodiment offline data|✗|✗|✗|✓|✓|
|Continual improvement|✗|✓|✓|✗|✓|
|Training stability|✗|✗|✓|✗|✓|


- **C2** We demonstrate that naive world model fine-tuning fails on many tasks due to distributional shift between pre-training and fine-tuning data. 

- **C3** We propose two techniques, experience rehearsal and execution guidance, to mitigate the distributional gap and encourage exploration during RL fine-tuning. 

- **C4** We present NCRL, which leverages non-curated offline data in both pre-training and finetuning stages and clearly outperforms existing approaches across a diverse set of tasks. 

### 2 RELATED WORK 

In this section, we review RL methods that leverage offline data in different ways. See Sec. C for extended discussion and Table 1 for a comparison. 

**RL with task-specific offline datasets** Offline RL trains agents purely from offline data by constraining divergence from behavior policies (Kumar et al., 2020; Fujimoto & Gu, 2021; Kumar et al., 2019; Wu et al., 2019; Kostrikov et al., 2021; 2022; Uchendu et al., 2023), but performance depends heavily on dataset quality (Yarats et al., 2022). Offline-to-online RL (Lee et al., 2022; Zhao et al., 2022; Yu & Zhang, 2023; Nair et al., 2020; Rafailov et al., 2023) addresses this by fine-tuning the agent via interaction with the environment. MOTO (Rafailov et al., 2023) proposes a model-based offline-to-online RL method with reward-labeled data, but requires model-based value expansion, policy regularization, and controlling epistemic uncertainty to conduct stable online RL training. Recent work (Ball et al., 2023; Li et al., 2023) demonstrates promising results by leveraging offline data, but it still assumes reward-labeled offline data or relies on near-expert data of the target tasks (Li et al., 2023), while we focus on a more general setting assuming reward-free, mixed-quality and task-agnostic offline data. 

**RL with multi-task offline datasets** Recent work has explored multi-task offline RL (Kumar et al., 2023; Hansen et al., 2024; Julian et al., 2020; Kalashnikov et al., 2021; Yu et al., 2021), but requires known rewards. PWM (Georgiev et al., 2024) trains a world model for multi-task RL but is limited to state-based inputs and reward-labeled data. To handle unknown rewards, approaches like human labeling (Cabi et al., 2020; Singh et al., 2019), inverse RL (Ng et al., 2000; Abbeel & Ng, 2004), or generative adversarial imitation learning (Ho & Ermon, 2016) can be used, though these require human labor or expert demonstrations. Yu et al. (2022) assigns zero rewards to unlabeled data, which introduces additional bias. Apart from these, there is a line of work that focuses on representation learning or dynamics model training from in-the-wild data (Schwarzer et al., 2021; Parisi et al., 2022; Yang & Nachum, 2021; Yuan et al., 2022; Stooke et al., 2021; Shah & Kumar, 2021; Wang et al., 2022; Sun et al., 2023; Ze et al., 2023; Ghosh et al., 2023; Wu et al., 2025; 2023) but fails to utilize rich information in the dataset at the fine-tuning stage. 

### 3 METHODS 

In this section, we detail our two-stage approach, which consists of _(i)_ world model pre-training, which learns a multi-task & embodiment world model, given offline data, which rather importantly, includes reward-free and mixed-quality data, and _(ii)_ RL-based fine-tuning which leverages the pretrained world model, non-curated offline data, and online interaction in an offline-to-online fashion. See Fig. 1 for the overview and Alg. 1 for the full algorithm. 

3 

Published as a conference paper at ICLR 2026 

#### 3.1 PROBLEM SETUP 

In this paper, we assume the agent has access to a non-curated but in-domain offline dataset _D_ off with three key characteristics: _(i)_ trajectories lack reward labels _rt_<sup>_i_,</sup><sup>_(ii)_data quality is mixed, and</sup><sup>_(iii)_data</sup> comes from multiple embodiments. During fine-tuning, the agent interacts with the environment to collect labeled trajectories _τ_ on<sup>_i_=</sup><sup>_{oi_</sup> _t_<sup>_, ai_</sup> _t_<sup>_, r_</sup> _t_<sup>_i}T_</sup> _t_ =1<sup>andstorestheminanonlinedataset</sup><sup>_D_on=</sup> _{τ_ on<sup>_i}N_</sup> _i_ =1<sup>on.Ourgoalistolearnahigh-performancepolicybyleveragingboth</sup><sup>_D_offand</sup><sup>_D_onwhile</sup> minimizing the required online interactions _N_ on. 

#### 3.2 MULTI-EMBODIMENT WORLD MODEL PRE-TRAINING 

During pre-training, rather than training separate models per task as in previous work (Hafner et al., 2020; 2021; 2023), we train one world model per benchmark and demonstrate that a single multitask & embodiment world model can effectively leverage non-curated data. 

Since our primary goal is enabling RL agents to use non-curated offline data rather than proposing a new architecture, we adopt the widely-used recurrent state space model (RSSM) (Hafner et al., 2019) with several modifications: _(i)_ removal of task-related losses, _(ii)_ zero-padding of actions to unify dimensions across embodiments, and _(iii)_ scaling the model to 280M parameters. With these changes, we show that RSSMs can successfully learn the dynamics of multiple embodiments and can be fine-tuned for various tasks. 

Our first stage pre-trains the following components: 

Sequence model : _ht_ = _fθ_ ( _ht−_ 1 _, zt−_ 1 _, at−_ 1) Encoder : _zt ∼ qθ_ ( _zt | ht, ot_ ) Dynamics predictor : _z_ ˆ _t ∼ pθ_ (ˆ _zt | ht_ ) Decoder : _o_ ˆ _t ∼ dθ_ (ˆ _ot | ht, zt_ ) _._ 

The models _fθ_ , _qθ_ , _pθ_ and _dθ_ are jointly optimized by minimizing: 


where _β_ 1 _, β_ 2 _, β_ 3 are weights of each term. _L_ pred minimizes reconstruction error, _L_ dyn enables the sequence model and dynamics predictor to predict future latent states, and _L_ rep encourages the representation to be more predictable. They are given as: 


where sg represents the stop-gradient operator and KL( _p∥q_ ) is the KL divergence. 

While there is room to improve world model pre-training through recent self-supervised methods (Eysenbach et al., 2023) or advanced architectures (Vaswani et al., 2017; Gu et al., 2022; Mereu et al., 2025), such improvements are orthogonal to our method and left for future work. 

#### 3.3 RL-BASED FINE-TUNING WITH REHEARSAL AND GUIDANCE 

In our fine-tuning stage, the agent interacts with the environment to collect new data _τ_ on<sup>_i_=</sup><sup>_{oi_</sup> _t_<sup>_, ai_</sup> _t_<sup>_, r_</sup> _t_<sup>_i}T_</sup> _t_ =0<sup>.</sup> This data is used to learn a reward function _r_ ˆ _t ∼ rθ_ (ˆ _rt | ht, zt_ ) via supervised learning while fine-tuning the world model with Eq. (1). For simplicity, we denote the concatenation of _ht_ and _zt_ as _st_ = [ _ht, zt_ ] and use _s_ ˆ _t_ = [ _ht,_ ˆ _zt_ ] when the latent state is predicted by the dynamics predictor _pθ_ . The actor and critic are trained using imagined trajectories _τ_ ˆ<sup>_i_</sup> = _{s_ ˆ<sup>_i_</sup> _t_<sup>_, ai_</sup> _t_<sup>_}T_</sup> _t_ =0<sup>generated by rolling out the policy</sup><sup>_πϕ_(</sup><sup>_a | s_) with the sequence model</sup><sup>_fθ_and the</sup> dynamics predictor _pθ_ . The rollouts are initialized from states _p_ 0( _s_ ) sampled from the replay buffer. The critic _vϕ_ ( _Vt_<sup>_λ| st_) learns to approximate the distribution over the</sup><sup>_λ_-return</sup><sup>_V_</sup> _t_<sup>_λ_, calculated as:</sup> 


4 

Published as a conference paper at ICLR 2026 


Figure 2: **Visualization of Distribution Mismatch. Left:** At the early stage of fine-tuning, there is a distribution shift between offline data used for world model pre-training and online data used for RL fine-tuning, which hurts performance. **Middle:** Experience rehearsal mitigates the distributional shift issue. **Right:** Quantitatively, at the early stage of fine-tuning, experience rehearsal reduces the Wasserstein distance between the online data and both the offline and expert data. 

where _vt_<sup>_λ_=E[</sup><sup>_vϕ_(</sup><sup>_· | st_)]denotesth</sup><sup>~~ee~~xpectationofthevaluedistributionpredictedbythecritic.</sup> The value function _vϕ_ is trained by maximizing the log likelihood of the target _λ_ -return, while the actor _πϕ_ is optimized to maximize the _λ_ -return by backpropagating gradients through the actions and latent states of the imagined trajectories: 


**Why Fine-Tuning a World Model Alone is Not Enough?** While previous methods typically discard non-curated offline data during fine-tuning (Wu et al., 2025; Rajeswar et al., 2023; Wu et al., 2023), we find that relying solely on a pre-trained world model often fails, particularly on hard-exploration tasks. To understand why, we analyze the Shelf Place task from Meta-World (Yu et al., 2020) as an illustrative task by visualizing the distributions of offline data _D_ off used for world model pre-training and online data _D_ on collected during early RL training in Fig. 2. The t-SNE plot in Fig. 2 (left) reveals a distribution mismatch between _D_ off and _D_ on, leading to three key issues: _(i)_ The world model’s accuracy can degrade if a significant distributional shift exists between the offline and online data. This degradation is particularly pronounced when the offline data distribution is narrow, which may create a substantial state-space gap. _(ii)_ For hard exploration tasks, the agent struggles to reach high-reward regions, causing the world model to be fine-tuned on a narrow online data distribution and leading to catastrophic forgetting. _(iii)_ The policy update in Eq. (4) relies on imagined trajectories ˜ _τ_ = _p_ 0( _s_ )<sup>�</sup><sup>_H_</sup> _t_ =0<sup>_−_1</sup><sup>_πϕ_(</sup><sup>_at | st_)</sup><sup>_pθ_(</sup><sup>_st_+1</sup><sup>_| st, at_),</sup> where _p_ 0( _s_ ) is sampled from _D_ on. A narrow _p_ 0( _s_ ) limits the world model to rollout promising trajectories for policy updates. To address these challenges, we introduce two key components: _i)_ experience rehearsal, which mitigates distributional shift by retrieving task-relevant trajectories from non-curated datasets (Fig. 2 middle, right), and _ii)_ execution guidance, which encourages exploration by steering the agent toward regions where the world model has high confidence. 

**Experience Rehearsal** Prior works like RLPD (Ball et al., 2023) and ExPLORe (Li et al., 2023) have shown that replaying offline data can boost RL training. However, these methods use small, well-structured offline datasets. In our setting, directly replaying non-curated offline data is infeasible since our datasets are _∼_ 100× larger and contain diverse tasks and embodiments. 

We propose retrieving task-relevant trajectories _D_ retrieved = _{τ_ retrieved<sup>_i}_</sup> _i_<sup>_N_</sup> =1<sup>from the non-curated of-</sup> fline data based on neural feature distance between online samples and offline trajectories. This filters out irrelevant trajectories, creating a small task-relevant dataset. Specifically, we compute: 


where e _θ_ is the encoder learned during world model pre-training, and _o_ on and _o_ off are initial observations from trajectories in the online buffer and offline dataset, respectively. For efficient search to get the top-k similar trajectories, we pre-compute key-value pairs mapping trajectory IDs to neural 

> 1We follow the policy update described in the first version of the paper (https://arxiv.org/abs/2301.04104v1) and Dreamer v2 (Hafner et al., 2021). 

5 

Published as a conference paper at ICLR 2026 


Figure 3: **Left:** Quantitative comparison across 72 diverse tasks from Meta-World (Yu et al., 2020) and DMControl (Tassa et al., 2018) with the same sample budget (150k). See Sec. I for full results. **Right:** Learning curves on representative challenging locomotion and robotic manipulation tasks. NCRL consistently outperforms state-of-the-art methods that leverage offline data by a decent margin. We plot the mean and corresponding 95% confidence interval. 

features and use Faiss (Douze et al., 2024), enabling retrieval in seconds. The retrieval precision can be found in Sec. A.3. 

The retrieved data is replayed during fine-tuning, so-called experience rehearsal. The retrieved data serves three purposes, as shown in Fig. 1. First, it prevents catastrophic forgetting by continuing to train the world model on relevant pre-training data, particularly important for hard exploration tasks with narrow online data distributions. Second, it augments the initial state distribution _p_ 0( _s_ ) during model rollout, enabling the world model to rollout promising trajectories for policy learning. Third, as described below, it enables learning a policy prior for execution guidance. In Sec. B.1, we explain that experience retrieval reduces distribution shift during online fine-tuning. We further demonstrate that experience retrieval acts as a regularizer, helping to prevent catastrophic forgetting during the fine-tuning process. Unlike RLPD and ExPLORe, we do not use this data to learn a Q-function, eliminating the need for reward labels. 

**Execution Guidance via Prior Actors** Standard RL training initializes the replay buffer with random actions and collects new data through environment interaction using the training policy. However, offline data often contains valuable information like near-expert trajectories and diverse state-action coverage that should be utilized during fine-tuning. Additionally, distribution shift between offline and online data can degrade pre-trained model weights, making it important to guide the online data collection toward the offline distribution at the early training stage. 

To achieve this, we train a prior policy _π_ bc via behavioral cloning on the retrieved offline data _D_ retrieved. During online data collection, we alternate between this prior policy _π_ bc and the RL policy _πϕ_ according to a pre-defined schedule. Specifically, at the start of each episode, we probabilistically select whether to use _π_ bc. If _π_ bc is selected, we randomly choose a starting timestep _t_ bc and duration _H_ during which _π_ bc is active, with _πϕ_ used for the remaining timesteps. In Sec. B.2, we theoretically show that, assuming _π_ bc outperforms _πϕ_ in the early stage of training, using a mixed policy composed of _π_ bc and _πϕ_ leads to improved policy performance. 

While this approach shares similarities with JSRL (Uchendu et al., 2023), our method differs in three key aspects: _i)_ we leverage non-curated rather than task-specific offline data, _ii)_ we demonstrate the benefits of a model-based approach over JSRL’s model-free framework, and _iii)_ we randomly switch between policies mid-episode rather than only using _π_ bc at episode start. The complete algorithm and theoretical analysis can be found in Sec. H and Sec. B, respectively. 

### 4 EXPERIMENTS 

In the experiments, we aim to answer the following questions: 

6 

Published as a conference paper at ICLR 2026 

- **Q1** How does NCRL compare to state-of-the-art methods that leverage offline data and trainfrom-scratch baselines in terms of sample efficiency and final performance? 

- **Q2** How does NCRL compare to other leading model-based approaches that utilize offline data? 

- **Q3** How effectively does NCRL adapt to new tasks in a continual learning setting? We further conduct detailed ablation studies to evaluate our method. 

**Tasks** We evaluate our method on _pixel_ -based continuous control tasks from DMControl (Tassa et al., 2018) and Meta-World (Yu et al., 2020). The chosen tasks include both locomotion and manipulation tasks covering different challenges in RL, including high-dimensional observations, hard exploration, and complex dynamics. We use three random seeds for each task. 

**Dataset** Our dataset consists of data from two benchmarks: DMControl and Meta-World, visualized in Sec. K. For DMControl, we include 10k trajectories covering 5 embodiments collected by _unsupervised RL agents_ (Rajeswar et al., 2023; Pathak et al., 2017), trained via curiosity without task-related information. These trajectories vary in competence and coverage. As the unsupervised RL agents are trained to maximize the agent’s curiosity rather than a specific reward signal, the dataset for DMControl does not contain expert trajectories for a specific task (e.g., Walk, Run etc.) For Meta-World, we collect mixed-quality 50k trajectories across 50 tasks using TDMPCv2 agents (Hansen et al., 2024) by injecting Gaussian noise with _σ_ up to 2.0, which intentionally corrupts the policies and produces trajectories of varying success and quality. In practice, such a mixture of successful, partially successful, and failed behaviors can naturally arise from, for instance, noisy or partial human demonstrations collected through teleoperation. In Fig. 9, we assess the dataset quality via imitation learning, showing unsatisfactory performance. This emphasizes the mixed-quality property of the dataset. When combined with the DMControl data, our complete offline dataset comprises 60k trajectories (10M state-action pairs) across 6 embodiments. 

#### 4.1 NCRL IMPROVES SAMPLE EFFICIENCY ACROSS DIVERSE TASKS 

**Comparison with Methods that Leverage Offline Data** We compare NCRL against several state-of-the-art methods that leverage reward-free data to improve RL training: _(i)_ **R3M** (Nair et al., 2022), a visual representation pre-training approach that serves as our baseline for comparing pre-trained visual features using non-curated offline data. _(ii)_ **UDS-RLPD** (Yu et al., 2022; Ball et al., 2023), which assigns zero rewards to offline data and uses RLPD Ball et al. (2023) for policy training. _(iii)_ **ExPLORe** (Li et al., 2023), which labels offline data using UCB rewards. We enhance the original implementation with reward ensembles. _(iv)_ **JSRL-BC** (Uchendu et al., 2023), which collects online data using a mixture of the training policy and a behavior-cloned prior policy learned from offline data. As the compared baselines cannot handle multi-embodiment data like NCRL, we preprocess the offline data to only include task-relevant trajectories for them. Despite the baselines having access to better-structured data, NCRL still significantly outperforms all baselines across the tested tasks. See Sec. G for the details of baselines. 

Fig. 3 (right) shows comparison results with baselines. Our method outperforms _all_ compared baselines by a large margin. Compared to R3M, NCRL shows the importance of world model pretraining and reusing offline data during fine-tuning, versus representation learning alone. R3M fails to improve sample efficiency on most tasks, consistent with findings in Hansen et al. (2023). 

UDS and ExPLORe reuse offline data by labeling it with zero rewards and UCB rewards, respectively, and concatenating it with online data for off-policy updates. UDS shows only slightly better performance on Walker Run compared to R3M and JSRL-BC, demonstrating the ineffectiveness of zero-reward labeling. ExPLORe performs better on 2/3 locomotion tasks and shows progress on challenging manipulation tasks, but NCRL still significantly outperforms it, demonstrating the superiority of leveraging a pre-trained world model and properly reusing offline data during fine-tuning. 

NCRL also clearly outperforms JSRL-BC. JSRL-BC’s performance heavily depends on the offline data distribution. While JSRL-BC can perform well when a good prior actor can be extracted from offline data, it struggles with non-expert trajectories, showing only marginal improvements over other baselines on the Cheetah Run Hard, Assembly, and Shelf Place tasks. In contrast, NCRL effectively leverages non-expert offline data. For example, on Quadruped Walk, NCRL benefits from exploratory offline data, enabling pixel-based control within just 100 trials. 

7 

Published as a conference paper at ICLR 2026 


Figure 4: Comparison with other world model pre-training methods. NCRL outperforms stateof-the-art model-based methods without relying on techniques used in iVideoGPT, such as reward shaping and demonstration-based replay buffer initialization. 


Figure 5: NCRL enables fast task adaptation. We train an RL agent to control an Ant robot from DMControl to complete a series of tasks incrementally. NCRL significantly outperforms the widely used baseline PackNet by properly leveraging non-curated offline data. 

**Comparison with Training-from-Scratch Methods** We compare NCRL with two widely used training-from-scratch baselines: **DrQ-v2** and **DreamerV3** , representing model-free and model-based approaches, respectively. Fig. 3 (left) and Sec. I show comparison results on 22 locomotion and 50 robotic manipulation tasks with pixel inputs from DMControl and Meta-World benchmarks. With 150k online samples, NCRL achieves higher aggregate scores compared to DrQ-v2 and DreamerV3, matching their performance obtained with 3.3-6.7 _×_ more samples (500k for DMControl, 1M for Meta-World). Furthermore, NCRL achieves promising performance on hard exploration tasks where learning-from-scratch baselines fail, such as challenging Meta-World manipulation tasks and hard DMControl tasks. 

**Comparison with Other Model-Based Methods** While most multi-task/multi-embodiment world models focus on visual prediction (Zheng et al., 2024; Zhu et al., 2024b) or imitation learning (Zhu et al., 2024a; Zhou et al., 2024), some works like Seo et al. (2022), Wu et al. (2024), and iVideoGPT (Wu et al., 2025) investigate world model pre-training with in-the-wild data for RL. These methods typically focus on designing novel or scalable model architectures to leverage the offline data, but lack mechanisms to better leverage offline data during RL fine-tuning. Furthermore, due to the cost of RL training, these methods are usually evaluated on limited task sets, making the effectiveness of the pre-trained world model unclear on diverse tasks. 

Figure 4 compares our method with world model pre-training approaches. The baseline results are from the iVideoGPT paper to get the best reported results in the original paper. We further compare iVideoGPT in an aligned setting in Sec. A.2. Despite extensive pre-training on diverse manipulation data, iVideoGPT and pre-trained DreamerV3 show only marginal improvements over training-fromscratch baselines. In contrast, NCRL clearly accelerates RL training by properly leveraging noncurated offline data during both pre-training and fine-tuning. Notably, baselines in Fig. 4 use reward shaping and expert replay buffer pre-filling, while NCRL uses _none_ of these tricks yet achieves superior performance. This highlights that _(i)_ non-curated offline data contains useful information for RL fine-tuning, and _ii)_ NCRL can effectively leverage such data. Furthermore, NCRL could potentially be combined with iVideoGPT to leverage even more diverse offline data in future work. 

#### 4.2 NCRL ENABLES FAST TASK ADAPTATION 

We investigate NCRL’s benefits for continual task adaptation, where an agent must incrementally solve a sequence of tasks. While similar to continual reinforcement learning (CRL) or life-long RL (Parisi et al., 2019; Khetarpal et al., 2022), we use a simplified setting with a limited task set. 

8 

Published as a conference paper at ICLR 2026 


Figure 6: Ablation study on key components. “P” represents world model pre-training, “ER” means experience rehearsal, and “G” represents execution guidance. The combination of a pre-trained taskagnostic world model with retrieval-based experience rehearsal and execution guidance boosts RL performance across diverse tasks. 

Figure 7: Comparison of execution guidance versus uncertainty-based reward labeling. NCRL demonstrates the effectiveness of using execution guidance over uncertainty-based reward labeling on challenging robotic manipulation tasks. 

Note that CRL has a broad scope; assumptions and experiment setups vary among methods, making it difficult to set up a fair comparison with other methods. Rather than proposing a state-of-the-art CRL method, we aim to demonstrate that NCRL offers an effective approach to leverage previous data that also fits the CRL setting. 

**Setup & Baselines** We set our continual adaptation experiment based on the Quadruped robot from DMControl. Specifically, the agent sequentially learns stand, walk, run, jump, roll, and roll fast tasks with 300K environment steps per task. To have a fair comparison, i.e., having comparable model parameters and eliminating the potential effects from pre-training on other tasks, we pre-train a small world model only on the Quadruped domain. During training, the agent can access all previous experiences and model weights. We compare against a widely used baseline PackNet (Mallya & Lazebnik, 2018), which iteratively prunes actor parameters while preserving important weights to remember previous skills. For each new task, PackNet fine-tunes the actor model via iterative pruning while randomly reinitializing the critic model since rewards are not shared among tasks. 

**Results** Figure 5 shows NCRL significantly outperforms PackNet, enabling adaptation within 100 trials per task. With limited samples, PackNet achieves only 20–60% of NCRL’s episodic returns. We attribute NCRL’s superior performance to its ability to leverage the diverse offline data through both world model pre-training and fine-tuning with experience rehearsal and execution guidance. 

#### 4.3 ABLATIONS 

**Role of Each Component** We now analyze each component’s contribution using the same set of tasks from Sec. 4.1. As shown in Fig. 6, world model pre-training shows promising results when the offline data consists of diverse trajectories, such as data collected by exploratory agents (Walker Run), while it fails to work well when the offline data distribution is relatively narrow as in the Meta-World tasks. We found that experience rehearsal and execution guidance stabilize training and improve performance on hard exploration tasks like Cheetah Run Hard and challenging manipulation tasks from Meta-World. This addresses _(i)_ world model pre-training alone, failing to fully leverage rich state and action information from the non-curated offline data and _(ii)_ distributional shift between offline and online data during fine-tuning hurts the learning. The proposed retrieval-based experience rehearsal and execution guidance help utilize offline data and accelerate exploration, which together enable NCRL to achieve strong performance on a wide range of tasks. 

9 

Published as a conference paper at ICLR 2026 

**Comparison with Uncertainty-Aware Reward Function** To leverage reward-free offline data, ExPLORe (Li et al., 2023) proposes to label offline data with uncertaintybased rewards. To demonstrate the effectiveness of NCRL, we compare it with uncertainty-based rewards. Specifically, instead of using execution guidance, we use Optimistic Thompson Sampling (OTS) (Hu et al., 2023b) to label the imagined trajectories via model rollout. As shown in Fig. 7, our method outperforms the variant using OTS on hard exploration tasks, Assembly and Stick Pull, by a large margin, showing the effectiveness of using execution guidance. 


Figure 8: Impact of fine-tuning different world model components. 

**Comparison of Fine-Tuning Different Components** We ferent world model components. now investigate the role of different components in the world model during fine-tuning. We use the Quadruped Walk task as a representative task for the investigation. As shown in Fig. 8, the encoder, decoder, and latent dynamics play important roles during fine-tuning. Fine-tuning the full world model yields the best performance on the tested task. The full world model is fine-tuned by default in our experiments. 

### 5 CONCLUSION 

We propose NCRL, a simple yet efficient approach to leverage ample non-curated offline datasets consisting of reward-free, mixed-quality data collected across multiple embodiments. NCRL pretrains a task-agnostic world model on the non-curated data and adapts to downstream tasks via RL. We show that naive fine-tuning of world models fails to accelerate RL training due to distributional shift and propose two techniques – experience rehearsal and execution guidance – to mitigate this issue. Equipped with these techniques, we demonstrate that world models pre-trained on non-curated data are able to boost RL’s sample efficiency across a broader range of locomotion and robotic manipulation tasks. We compared NCRL against a wide set of baselines, including two widely used training-from-scratch methods, five methods that utilize offline data, and one continual learning method. Our NCRL consistently delivers strong performance over these baselines. Extensive ablation studies reveal the effectiveness of the proposed techniques. While promising, NCRL can be improved in multiple ways: extending to real-world applications, leveraging in-the-wild offline data, and exploring novel world model architectures. 

#### ETHICS STATEMENT 

This paper contributes to the field of reinforcement learning (RL), with potential applications including robotics and autonomous machines. While our methods hold promise for advancing technology, they could also be applied in ways that raise ethical concerns, such as in autonomous machines exploring the world and making decisions on their own. However, the specific societal impacts of our work are broad and varied, and we believe a detailed discussion of potential negative uses is beyond the scope of this paper. We encourage a broader dialogue on the ethical use of RL technology and its regulation to prevent misuse. 

#### REPRODUCIBILITY STATEMENT 

To facilitate reproducibility, we provide implementation descriptions in Sec. G, report computational requirements in Sec. F, present the complete algorithm in Sec. H, and specify key hyperparameters in Sec. J. Code and datasets are in https://github.com/zhaoyi11/ncrl. 

#### ACKNOWLEDGMENTS 

We acknowledge CSC – IT Center for Science, Finland, for awarding this project access to the LUMI supercomputer, owned by the EuroHPC Joint Undertaking, hosted by CSC (Finland) and the LUMI consortium through CSC. We acknowledge the computational resources provided by the Aalto Science-IT project. We acknowledge funding from the Research Council of Finland (353138, 362407, 352788, 357301, 339730). Aidan Scannell and Wenshuai Zhao were supported by the Research Council of Finland, Flagship program Finnish Center for Artificial Intelligence (FCAI). 

10 

Published as a conference paper at ICLR 2026 

### REFERENCES 

- Pieter Abbeel and Andrew Y Ng. Apprenticeship learning via inverse reinforcement learning. In _International Conference on Machine Learning (ICML)_ , 2004. 

- Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, et al. Cosmos world foundation model platform for physical ai. In _arXiv preprint arXiv:2501.03575_ , 2025. 

- Eloi Alonso, Adam Jelley, Vincent Micheli, Anssi Kanervisto, Amos Storkey, Tim Pearce, and Franc¸ois Fleuret. Diffusion for world modeling: Visual details matter in atari. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 

- OpenAI: Marcin Andrychowicz, Bowen Baker, Maciek Chociej, Rafal Jozefowicz, Bob McGrew, Jakub Pachocki, Arthur Petron, Matthias Plappert, Glenn Powell, Alex Ray, et al. Learning dexterous in-hand manipulation. _The International Journal of Robotics Research (IJRR)_ , 2020. 

- Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E Hinton. Layer normalization. _arXiv preprint arXiv:1607.06450_ , 2016. 

- Philip J Ball, Laura Smith, Ilya Kostrikov, and Sergey Levine. Efficient online reinforcement learning with offline data. _International Conference on Machine Learning (ICML)_ , 2023. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. RT-2: vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning (CoRL)_ , 2023a. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. RT-1: Robotics transformer for real-world control at scale. _Robotics: Science and Systems (RSS)_ , 2023b. 

- Yuri Burda, Harrison Edwards, Amos Storkey, and Oleg Klimov. Exploration by random network distillation. _International Conference on Learning Representations_ , 2019. 

- Serkan Cabi, Sergio G´omez Colmenarejo, Alexander Novikov, Ksenia Konyushkova, Scott Reed, Rae Jeong, Konrad Zolna, Yusuf Aytar, David Budden, Mel Vecerik, et al. Scaling data-driven robotics with reward sketching and batch reinforcement learning. In _Robotics: Science and Systems (RSS)_ , 2020. 

- Matthijs Douze, Alexandr Guzhva, Chengqi Deng, Jeff Johnson, Gergely Szilvasy, PierreEmmanuel Mazar´e, Maria Lomeli, Lucas Hosseini, and Herv´e J´egou. The faiss library. _arXiv preprint arXiv:2401.08281_ , 2024. 

- Benjamin Eysenbach, Abhishek Gupta, Julian Ibarz, and Sergey Levine. Diversity is all you need: Learning skills without a reward function. In _International Conference on Learning Representations (ICLR)_ , 2019. 

- Benjamin Eysenbach, Vivek Myers, Sergey Levine, and Ruslan Salakhutdinov. Contrastive representations make planning easy. In _Advances in Neural Information Processing Systems Workshop (NeurIPS Workshop)_ , 2023. 

- Scott Fujimoto and Shixiang Shane Gu. A minimalist approach to offline reinforcement learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2021. 

- Chongkai Gao, Haozhuo Zhang, Zhixuan Xu, Zhehao Cai, and Lin Shao. FLIP: Flow-centric generative planning for general-purpose manipulation tasks. _International Conference on Learning Representations (ICLR)_ , 2025. 

- Ignat Georgiev, Varun Giridhar, Nicklas Hansen, and Animesh Garg. PWM: Policy learning with large world models. _arXiv preprint arXiv:2407.02466_ , 2024. 

- Dibya Ghosh, Chethan Anand Bhateja, and Sergey Levine. Reinforcement learning from passive data via latent intentions. In _International Conference on Machine Learning (ICML)_ , 2023. 

11 

Published as a conference paper at ICLR 2026 

- Albert Gu, Karan Goel, and Christopher R´e. Efficiently modeling long sequences with structured state spaces. _International Conference on Learning Representations (ICLR)_ , 2022. 

- David Ha and J¨urgen Schmidhuber. Recurrent world models facilitate policy evolution. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2018. 

- Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _International Conference on Machine Learning (ICML)_ , 2019. 

- Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. _International Conference on Learning Representations (ICLR)_ , 2020. 

- Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. _International Conference on Learning Representations (ICLR)_ , 2021. 

- Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- Nicklas Hansen, Zhecheng Yuan, Yanjie Ze, Tongzhou Mu, Aravind Rajeswaran, Hao Su, Huazhe Xu, and Xiaolong Wang. On pre-training for visuo-motor control: Revisiting a learning-fromscratch baseline. In _International Conference on Machine Learning (ICML)_ , 2023. 

- Nicklas Hansen, Hao Su, and Xiaolong Wang. TD-MPC2: Scalable, robust world models for continuous control. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- Jonathan Ho and Stefano Ermon. Generative adversarial imitation learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2016. 

- Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. GAIA-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023a. 

- Bingshan Hu, Tianyue H Zhang, Nidhi Hegde, and Mark Schmidt. Optimistic thompson samplingbased algorithms for episodic reinforcement learning. In _Uncertainty in Artificial Intelligence (UAI)_ , 2023b. 

- Ryan Julian, Benjamin Swanson, Gaurav S Sukhatme, Sergey Levine, Chelsea Finn, and Karol Hausman. Never stop learning: The effectiveness of fine-tuning in robotic reinforcement learning. In _Conference on Robot Learning (CoRL)_ , 2020. 

- Sham Kakade and John Langford. Approximately optimal approximate reinforcement learning. In _International Conference on Machine Learning (ICML)_ , 2002. 

- Dmitry Kalashnikov, Jacob Varley, Yevgen Chebotar, Benjamin Swanson, Rico Jonschkowski, Chelsea Finn, Sergey Levine, and Karol Hausman. MT-OPT: Continuous multi-task robotic reinforcement learning at scale. _arXiv preprint arXiv:2104.08212_ , 2021. 

- Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. DROID: A large-scale in-the-wild robot manipulation dataset. In _Robotics: Science and Systems (RSS)_ , 2024. 

- Khimya Khetarpal, Matthew Riemer, Irina Rish, and Doina Precup. Towards continual reinforcement learning: A review and perspectives. _Journal of Artificial Intelligence Research_ , 2022. 

- Ilya Kostrikov, Rob Fergus, Jonathan Tompson, and Ofir Nachum. Offline reinforcement learning with fisher divergence critic regularization. In _International Conference on Machine Learning (ICML)_ , 2021. 

- Ilya Kostrikov, Ashvin Nair, and Sergey Levine. Offline reinforcement learning with implicit q- learning. _International Conference on Learning Representations (ICLR)_ , 2022. 

12 

Published as a conference paper at ICLR 2026 

- Aviral Kumar, Justin Fu, Matthew Soh, George Tucker, and Sergey Levine. Stabilizing off-policy q-learning via bootstrapping error reduction. _Advances in Neural Information Processing Systems (NeurIPS)_ , 2019. 

- Aviral Kumar, Aurick Zhou, George Tucker, and Sergey Levine. Conservative q-learning for offline reinforcement learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2020. 

- Aviral Kumar, Anikait Singh, Frederik Ebert, Mitsuhiko Nakamoto, Yanlai Yang, Chelsea Finn, and Sergey Levine. Pre-training for robots: Offline rl enables learning new tasks from a handful of trials. In _Robotics: Science and Systems (RSS)_ , 2023. 

- Michael Laskin, Denis Yarats, Hao Liu, Kimin Lee, Albert Zhan, Kevin Lu, Catherine Cang, Lerrel Pinto, and Pieter Abbeel. URLB: Unsupervised reinforcement learning benchmark. _Neural Information Processing Systems Track on Datasets and Benchmarks_ , 2021. 

- Yann LeCun, Yoshua Bengio, et al. Convolutional networks for images, speech, and time series. _The Handbook of Brain Theory and Neural Networks_ , 1995. 

- Seunghyun Lee, Younggyo Seo, Kimin Lee, Pieter Abbeel, and Jinwoo Shin. Offline-to-online reinforcement learning via balanced replay and pessimistic q-ensemble. In _Conference on Robot Learning (CoRL)_ , 2022. 

- Sergey Levine, Aviral Kumar, George Tucker, and Justin Fu. Offline reinforcement learning: Tutorial, review, and perspectives on open problems. _arXiv preprint arXiv:2005.01643_ , 2020. 

- Qiyang Li, Jason Zhang, Dibya Ghosh, Amy Zhang, and Sergey Levine. Accelerating exploration with unlabeled prior data. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2023. 

- Hao Liu and Pieter Abbeel. Behavior from the void: Unsupervised active pre-training. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2021a. 

- Hao Liu and Pieter Abbeel. APS: Active pretraining with successor features. In _International Conference on Machine Learning (ICML)_ , 2021b. 

- Cong Lu, Philip J Ball, Tim GJ Rudner, Jack Parker-Holder, Michael A Osborne, and Yee Whye Teh. Challenges and opportunities in offline reinforcement learning from visual observations. _Transactions on Machine Learning Research (TMLR)_ , 2023. 

- Arun Mallya and Svetlana Lazebnik. PackNet: Adding multiple tasks to a single network by iterative pruning. In _Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2018. 

- Pietro Mazzaglia, Tim Verbelen, Bart Dhoedt, Alexandre Lacoste, and Sai Rajeswar. Choreographer: Learning and adapting skills in imagination. In _International Conference on Learning Representations (ICLR)_ , 2023. 

- Riccardo Mereu, Aidan Scannell, Yuxin Hou, Yi Zhao, Aditya Jitta, Antonio Dominguez, Luigi Acerbi, Amos Storkey, and Paul Chang. Generative world modelling for humanoids: 1X world model challenge technical report. _arxiv preprint arXiv:2510.07092_ , 2025. 

- Vincent Micheli, Eloi Alonso, and Franc¸ois Fleuret. Transformers are sample-efficient world models. In _International Conference on Learning Representations (ICLR)_ , 2023. 

- Ashvin Nair, Abhishek Gupta, Murtaza Dalal, and Sergey Levine. AWAC: Accelerating online reinforcement learning with offline datasets. _arXiv preprint arXiv:2006.09359_ , 2020. 

- Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3M: A universal visual representation for robot manipulation. In _Conference on Robot Learning (CoRL)_ , 2022. 

- Mitsuhiko Nakamoto, Simon Zhai, Anikait Singh, Max Sobol Mark, Yi Ma, Chelsea Finn, Aviral Kumar, and Sergey Levine. Cal-QL: Calibrated offline rl pre-training for efficient online finetuning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 

13 

Published as a conference paper at ICLR 2026 

- Andrew Y Ng, Stuart Russell, et al. Algorithms for inverse reinforcement learning. In _International Conference on Machine Learning (ICML)_ , 2000. 

- Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, et al. Open X- Embodiment: Robotic learning datasets and rt-x models. In _International Conference on Robotics and Automation (ICRA)_ , 2023. 

- German I Parisi, Ronald Kemker, Jose L Part, Christopher Kanan, and Stefan Wermter. Continual lifelong learning with neural networks: A review. _Neural Networks_ , 2019. 

- Simone Parisi, Aravind Rajeswaran, Senthil Purushwalkam, and Abhinav Gupta. The unsurprising effectiveness of pre-trained vision models for control. In _International Conference on Machine Learning (ICML)_ , 2022. 

- Deepak Pathak, Pulkit Agrawal, Alexei A Efros, and Trevor Darrell. Curiosity-driven exploration by self-supervised prediction. In _International Conference on Machine Learning (ICML)_ , 2017. 

- Deepak Pathak, Dhiraj Gandhi, and Abhinav Gupta. Self-supervised exploration via disagreement. In _International Conference on Machine Learning (ICML)_ , 2019. 

- Tim Pearce, Tabish Rashid, Dave Bignell, Raluca Georgescu, Sam Devlin, and Katja Hofmann. Scaling laws for pre-training agents and world models. _arXiv preprint arXiv:2411.04434_ , 2024. 

- Rafael Rafailov, Kyle Beltran Hatch, Victor Kolev, John D Martin, Mariano Phielipp, and Chelsea Finn. MOTO: Offline pre-training to online fine-tuning for model-based robot learning. In _Conference on Robot Learning (CoRL)_ , 2023. 

- Sai Rajeswar, Pietro Mazzaglia, Tim Verbelen, Alexandre Pich´e, Bart Dhoedt, Aaron Courville, and Alexandre Lacoste. Mastering the unsupervised reinforcement learning benchmark from pixels. In _International Conference on Machine Learning (ICML)_ , 2023. 

- Scott Reed, Konrad Zolna, Emilio Parisotto, Sergio Gomez Colmenarejo, Alexander Novikov, Gabriel Barth-Maron, Mai Gimenez, Yury Sulsky, Jackie Kay, Jost Tobias Springenberg, et al. A generalist agent. _Transactions on Machine Learning Research (TMLR)_ , 2022. 

- Aidan Scannell, Mohammadreza Nakhaei, Kalle Kujanp¨a¨a, Yi Zhao, Kevin Luck, Arno Solin, and Joni Pajarinen. Discrete codebook world models for continuous control. In _International Conference on Learning Representations (ICLR)_ , 2025. 

- Max Schwarzer, Nitarshan Rajkumar, Michael Noukhovitch, Ankesh Anand, Laurent Charlin, R Devon Hjelm, Philip Bachman, and Aaron C Courville. Pretraining representations for data-efficient reinforcement learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2021. 

- Ramanan Sekar, Oleh Rybkin, Kostas Daniilidis, Pieter Abbeel, Danijar Hafner, and Deepak Pathak. Planning to explore via self-supervised world models. In _International Conference on Machine Learning (ICML)_ , 2020. 

- Younggyo Seo, Kimin Lee, Stephen L James, and Pieter Abbeel. Reinforcement learning with action-free pre-training from videos. In _International Conference on Machine Learning_ , pp. 19561–19579. PMLR, 2022. 

- Rutav Shah and Vikash Kumar. RRL: Resnet as representation for reinforcement learning. In _International Conference on Machine Learning (ICML)_ , 2021. 

- Jinghuan Shang, Karl Schmeckpeper, Brandon B May, Maria Vittoria Minniti, Tarik Kelestemur, David Watkins, and Laura Herlant. Theia: Distilling diverse vision foundation models for robot learning. In _Conference on Robot Learning (CoRL)_ , 2024. 

- Avi Singh, Larry Yang, Kristian Hartikainen, Chelsea Finn, and Sergey Levine. End-to-end robotic reinforcement learning without reward engineering. _Robotics: Science and Systems (RSS)_ , 2019. 

- Adam Stooke, Kimin Lee, Pieter Abbeel, and Michael Laskin. Decoupling representation learning from reinforcement learning. In _International Conference on Machine Learning (ICML)_ , 2021. 

14 

Published as a conference paper at ICLR 2026 

- Yanchao Sun, Shuang Ma, Ratnesh Madaan, Rogerio Bonatti, Furong Huang, and Ashish Kapoor. SMART: Self-supervised multi-task pretraining with control transformers. In _International Conference on Learning Representations_ , 2023. 

- Yuval Tassa, Yotam Doron, Alistair Muldal, Tom Erez, Yazhe Li, Diego de Las Casas, David Budden, Abbas Abdolmaleki, Josh Merel, Andrew Lefrancq, et al. Deepmind control suite. _arXiv preprint arXiv:1801.00690_ , 2018. 

- Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _Robotics: Science and Systems (RSS)_ , 2024. 

- Ikechukwu Uchendu, Ted Xiao, Yao Lu, Banghua Zhu, Mengyuan Yan, Jos´ephine Simon, Matthew Bennice, Chuyuan Fu, Cong Ma, Jiantao Jiao, et al. Jump-start reinforcement learning. In _International Conference on Machine Learning (ICML)_ , 2023. 

- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. _Advances in Neural Information Processing Systems (NeurIPS)_ , 2017. 

- Oriol Vinyals, Igor Babuschkin, Wojciech M Czarnecki, Micha¨el Mathieu, Andrew Dudzik, Junyoung Chung, David H Choi, Richard Powell, Timo Ewalds, Petko Georgiev, et al. Grandmaster level in starcraft ii using multi-agent reinforcement learning. _Nature_ , 2019. 

- Che Wang, Xufang Luo, Keith Ross, and Dongsheng Li. VRL3: A data-driven framework for visual deep reinforcement learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2022. 

- Jialong Wu, Haoyu Ma, Chaoyi Deng, and Mingsheng Long. Pre-training contextualized world models with in-the-wild videos for reinforcement learning. _Advances in Neural Information Processing Systems_ , 36:39719–39743, 2023. 

- Jialong Wu, Haoyu Ma, Chaoyi Deng, and Mingsheng Long. Pre-training contextualized world models with in-the-wild videos for reinforcement learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 

- Jialong Wu, Shaofeng Yin, Ningya Feng, Xu He, Dong Li, Jianye Hao, and Mingsheng Long. iVideoGPT: Interactive videogpts are scalable world models. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 

- Yifan Wu, George Tucker, and Ofir Nachum. Behavior regularized offline reinforcement learning. _arXiv preprint arXiv:1911.11361_ , 2019. 

- Tete Xiao, Ilija Radosavovic, Trevor Darrell, and Jitendra Malik. Masked visual pre-training for motor control. _arXiv preprint arXiv:2203.06173_ , 2022. 

- Yingchen Xu, Jack Parker-Holder, Aldo Pacchiano, Philip Ball, Oleh Rybkin, S Roberts, Tim Rockt¨aschel, and Edward Grefenstette. Learning general world models in a handful of reward-free deployments. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2022. 

- Mengjiao Yang and Ofir Nachum. Representation matters: Offline pretraining for sequential decision making. In _International Conference on Machine Learning (ICML)_ , 2021. 

- Denis Yarats, Rob Fergus, Alessandro Lazaric, and Lerrel Pinto. Reinforcement learning with prototypical representations. In _International Conference on Machine Learning (ICML)_ , 2021. 

- Denis Yarats, David Brandfonbrener, Hao Liu, Michael Laskin, Pieter Abbeel, Alessandro Lazaric, and Lerrel Pinto. Don’t change the algorithm, change the data: Exploratory data for offline reinforcement learning. _arXiv preprint arXiv:2201.13425_ , 2022. 

- Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Meta-World: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on Robot Learning (CoRL)_ , 2020. 

15 

Published as a conference paper at ICLR 2026 

- Tianhe Yu, Aviral Kumar, Yevgen Chebotar, Karol Hausman, Sergey Levine, and Chelsea Finn. Conservative data sharing for multi-task offline reinforcement learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2021. 

- Tianhe Yu, Aviral Kumar, Yevgen Chebotar, Karol Hausman, Chelsea Finn, and Sergey Levine. How to leverage unlabeled data in offline reinforcement learning. In _International Conference on Machine Learning (ICML)_ , 2022. 

- Zishun Yu and Xinhua Zhang. Actor-critic alignment for offline-to-online reinforcement learning. In _International Conference on Machine Learning (ICML)_ , 2023. 

- Zhecheng Yuan, Zhengrong Xue, Bo Yuan, Xueqian Wang, Yi Wu, Yang Gao, and Huazhe Xu. Pretrained image encoder for generalizable visual reinforcement learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2022. 

- Yanjie Ze, Nicklas Hansen, Yinbo Chen, Mohit Jain, and Xiaolong Wang. Visual reinforcement learning with self-supervised 3d representations. _Robotics and Automation Letters_ , 2023. 

- Yi Zhao, Rinu Boney, Alexander Ilin, Juho Kannala, and Joni Pajarinen. Adaptive behavior cloning regularization for stable offline-to-online reinforcement learning. _arXiv preprint arXiv:2210.13846_ , 2022. 

- Yi Zhao, Le Chen, Jan Schneider, Quankai Gao, Juho Kannala, Bernhard Sch¨olkopf, Joni Pajarinen, and Dieter B¨uchler. RP1M: A large-scale motion dataset for piano playing with bi-manual dexterous robot hands. _Conference on Robot Learning (CoRL)_ , 2024. 

- Zangwei Zheng, Xiangyu Peng, Tianji Yang, Chenhui Shen, Shenggui Li, Hongxin Liu, Yukun Zhou, Tianyi Li, and Yang You. Open-Sora: Democratizing efficient video production for all. _arXiv preprint arXiv:2412.20404_ , 2024. 

- Siyuan Zhou, Yilun Du, Jiaben Chen, Yandong Li, Dit-Yan Yeung, and Chuang Gan. RoboDreamer: Learning compositional world models for robot imagination. _International Conference on Machine Learning (ICML)_ , 2024. 

- Fangqi Zhu, Hongtao Wu, Song Guo, Yuxiao Liu, Chilam Cheang, and Tao Kong. IRASim: Learning interactive real-robot action simulators. _arXiv preprint arXiv:2406.14540_ , 2024a. 

- Zheng Zhu, Xiaofeng Wang, Wangbo Zhao, Chen Min, Nianchen Deng, Min Dou, Yuqi Wang, Botian Shi, Kai Wang, Chi Zhang, et al. Is sora a world simulator? a comprehensive survey on general world models and beyond. _IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)_ , 2024b. 

16 

Published as a conference paper at ICLR 2026 

## **Appendices** 

|**A **|**More Results**|**18**|
|---|---|---|
|**B**|**Theoretical Analysis**|**21**|
|**C **|**More Related Work**|**23**|
|**D **|**Limitations**|**24**|
|**E**|**Disclosure of LLMs Usage**|**24**|
|**F**|**Compute Resources**|**24**|
|**G **|**Implementation Details**|**24**|
|**H **|**Algorithm**|**27**|
|**I**|**Full Results**|**28**|
|**J**|**Hyperparameters**|**34**|
|**K **|**Task Visualization**|**35**|


17 

Published as a conference paper at ICLR 2026 

### A MORE RESULTS 

#### A.1 COMPARISON WITH IMITATION LEARNING BASELINE 

To demonstrate the mixed-quality property of the non-curated dataset, we compare NCRL with Diffusion Policy, a widely used imitation learning approach by modeling the agent with diffusion models. From Fig. 9, we can see that due to the dataset consisting of non-expert data, the diffusion policy fails to demonstrate satisfactory results, while NCRL can effectively utilize the offline data. 


Figure 9: Comparison with Diffusion Policy. NCRL can effectively handle non-curated offline data while the imitation learning baseline fails. 

#### A.2 COMPARISON WITH IVIDEOGPT 

#### **Comparison in an Aligned Setting** 

In Fig. 4, we compare our method against the original iVideoGPT results (Wu et al., 2025). Their experimental setups differ than ours in several ways: _i)_ iVideoGPT modifies the reward function to assign high rewards to successful episodes and _ii)_ pre-fills the replay buffer with a few demonstrations to ease exploration. In addition, iVideoGPT is pre-trained on X-embodiment datasets (O’Neill et al., 2023), whereas our method uses data from the same domain as the downstream tasks. 


Figure 10: Comparison with aligned iVideoGPT. 

To control for these differences, we run an additional set of experiments. Specifically, we finetune iVideoGPT on our dataset, initialize the policy with behavior cloning, and remove both reward shaping and demonstration pre-filling. We refer to this variant as iVideoGPT-align. We compare iVideoGPT-align with our NCRL after training with 200k environment steps Fig. 10, NCRL still outperforms iVideoGPT-align with a decent margin. 

**Full Results of Comparison with iVideoGPT** We compare with other model-based approaches on tasks used in iVideoGPT (Wu et al., 2025). We show that NCRL outperforms the baselines without using reward shaping and pre-filling the replay buffer with demonstrations. This highlights that although non-curated, the offline data can clearly boost RL training, and NCRL can effectively use the information in the data. 

#### A.3 EXPERIENCE RETRIEVAL PERFORMANCE 

In Sec. 3.3, we adopt a simple criterion to retrieve task-relevant trajectories from the non-curated dataset. We evaluate retrieval performance in Table 2, reporting precision at the top-250 and top- 

18 

Published as a conference paper at ICLR 2026 


Figure 11: Comparison with model-based approaches for leveraging offline data. 

500 retrieved trajectories. Our method achieves consistently high precision. For the Door Open task, some retrieved trajectories overlap with related tasks (Door Close, Door Lock, Door Unlock), but we find that RL training remains effective across all 72 evaluated tasks. A likely reason is that most RL training data is collected online, with policy and value functions updated from imaginary data generated by model rollouts, which mitigates the impact of occasional task-irrelevant trajectories. We expect future work to explore more advanced retrieval strategies for improved robustness. 

<u>Table 2: Precision results across tasks.</u> 

|**Tasks**|**Quadruped Run**|**Assembly**|**Shelf Place**|**Door Open**|
|---|---|---|---|---|
|Precision@250|100%|100%|100%|84%|
|Precision@500|100%|100%|100%|68%|


#### A.4 MORE ABLATION STUDIES 

**Hyperparameter Sensitivity** In execution guidance, we randomly sample both the starting timestep _t_ start and duration _H_ . Unlike JSRL (Uchendu et al., 2023), our approach eliminates expensive tuning for these hyperparameters and demonstrates robust performance. In this stage, we only introduce one hyperparameter to probabilistically decide whether to use _π_ BC based on a linear annealing schedule. We show that in Fig. 12, our method is not sensitive to this annealing schedule, showing robustness in a wide range of possible schedules. 


Figure 12: Our method is less sensitive to the choice of the execution guidance annealing schedule. 

**Role of Each Component** We show inter-quartile mean (IQM) and optimality gap for the ablation study of the role of each proposed component in Fig. 13. Together with the retrieval-based experience rehearsal and execution guidance, a pre-trained task-agnostic world model boosts RL performance on a wide range of tasks. 

**Impact of Retrieved Data** In Fig. 14, we evaluate the impact of retrieved data on the agent’s performance to assess the robustness of NCRL with respect to the quality of the retrieved dataset. As shown in the experiments on three challenging MetaWorld manipulation tasks, we progressively replaced the retrieved task-relevant trajectories with 0%, 25%, 50%, 75%, and 100% trajectories that lie far from the target task in the latent space. We observed that our method remains robust even as the quality of the retrieved data degrades. 

19 

Published as a conference paper at ICLR 2026 


Figure 13: Ablation study on the role of each component. “P” represents world model pretraining, “ER” means experience rehearsal, and “G” represents execution guidance. Together with the proposed retrieval-based experience rehearsal and execution guidance, world model pre-training boosts RL performance on a wide range of tasks. 


Figure 14: Comparison with injecting different ratios of task-irrelevant offline data. Our method remains robust even as the quality of the retrieved data degrades. 

#### A.5 MODEL SIZE OF DREAMERV3 

In Sec. I, we compare NCRL with the DreamerV3 baseline under a commonly used but relatively small model-size configuration. Although DreamerV3 has shown performance gains on more challenging domains such as Craft and DMLab when using larger models, these benefits are less pronounced in the settings examined in this work (DMControl and MetaWorld). Indeed, DreamerV3 itself uses a relatively small model for DMControl tasks Hafner et al. (2023). To ensure a fair comparison, we additionally evaluated DreamerV3 using the same model size as NCRL. As shown in Fig. 15, increasing the model size improves DreamerV3’s performance on Walker Run but degrades performance on Quadruped Walk. However, NCRL consistently outperforms the DreamerV3 baseline across different model sizes. 


Figure 15: Comparison of DreamerV3 under different model size configurations. NCRL consistently outperforms both variants. 

#### A.6 PERFORMANCE ON CHALLENGING METAWORLD TASKS 

In Sec. I, although NCRL solves most MetaWorld tasks with satisfactory performance, a few tasks still exhibit relatively low success rates with 150k environment steps. These tasks typically involve long horizons, small objects of interest, or strict success criteria. We have already shown three of these challenging tasks in Fig. 3, showing increased success rates with a larger training budget. 

20 

Published as a conference paper at ICLR 2026 

We now include additional experiments on other selected tasks using an increased training budget in Fig. 16. We found that, for most tasks, the success rate improves as the training budget increases. 


Figure 16: Improved success rate on MetaWorld tasks as the training budget increases. 

### B THEORETICAL ANALYSIS 

In this section, we give a theoretical analysis of the main conclusions in our paper. 

B.1 PROOF OF THE BENEFITS OF EXPERIENCE RETRIEVAL 

**Proposition 1.** _Experience retrieval reduces distribution shift during online fine-tuning, compared to using the full offline dataset directly, in the sense that_ 


_Proof._ Let _p_ off( _s_ ), _p_ on( _s_ ), and _p_ retrieved( _s_ ) denote the state distributions of the non-curated offline dataset _D_ off, the online dataset _D_ on, and the retrieved dataset _D_ retrieved _⊂D_ off, respectively. We simplify the notation as 


Since _D_ retrieved _⊂D_ off, the distribution _p_ off( _s_ ) can be expressed as a mixture distribution: 


_<u>|D</u>_ retrieved _<u>|</u>_ where _p_ rest( _s_ ) is the distribution over the remaining offline data, and _α_ = _|D_ off _|_ denotes the fraction of samples in the retrieved dataset. 

The expected total variation for the mixture distribution decomposes as: 


Assume that _D_ retrieved is constructed by selecting states such that _∥s_ retrieved _−s_ on _∥ < ϵ_ , for some small _ϵ >_ 0. Consequently, states in _D_ rest satisfy _∥s_ rest _− s_ on _∥≥ ϵ_ . This construction implies the following bounds: 


for some _ϵ_<sup>_′_</sup> _>_ 0. Therefore, it follows that 


Substituting into Equation equation 7 yields: 


Thus, the expected total variation between the retrieved data and online data is strictly smaller than that between the full offline data and online data. 

21 

Published as a conference paper at ICLR 2026 

**Explanation.** Experience retrieval helps prevent catastrophic forgetting during online fine-tuning. **Definition B.1** (Catastrophic Forgetting due to Data Distribution Shift) **.** Catastrophic forgetting occurs when a neural network, after training on a new data distribution, experiences a significant performance drop on previously learned tasks due to the overwriting of representations from earlier distributions, caused by biased parameter updates towards the new distribution. 

_Proof._ Following the previous notations, let _D_ on and _D_ retrieved denote the online dataset and the retrieved offline dataset, respectively. The objective in Eq. (1) can be written as: 

_L_ mixed( _θ_ ) = _L_ on( _θ_ ) + _λ · L_ retrieved( _θ_ ) 


Assuming the _λ_ is a monotonic function of _α_ =<sup>_<u>|D</u>_retrieved</sup><sup>_<u>|</u>_</sup> and _λ >_ 0, since _D_ retrieved _⊂D_ off, the term _|D_ off _| L_ retrieved( _θ_ ) acts as a regularizer during online updates, constraining parameter changes on _D_ on in a way that preserves performance on the retrieved offline distribution _p_ retrieved. This mitigates the risk of catastrophic forgetting by anchoring the model to previously seen data. 

B.2 PROOF OF IMPROVED PERFORMANCE WITH EXECUTION GUIDANCE 

**Proposition 2** (Performance Improvement via Execution Guidance) **.** _Let π_<sup>_e_</sup> _denote an exploration policy and π_<sup>_g_</sup> _a guide policy obtained via imitation learning. Let ε_ = max _s |_ E _a∼πg_ ( _·|s_ )[ _Aπ_<sup>_e_</sup> ( _s, a_ )] _|. Let π_ ˜ _be a mixed policy (execution guidance) derived from π_<sup>_e_</sup> _and π_<sup>_g_</sup> _, defined as:_ 


_Then, the performance of the mixed policy π_ ˜ _exceeds that of the exploration policy π_<sup>_e_</sup> _by at least:_ 


_where γ ∈_ [0 _,_ 1) _is the discount factor._ 

_Proof._ The proof follows directly from Theorem 4.1 in Kakade & Langford (2002): we just need to replace _π_<sup>_′_</sup> in Kakade & Langford (2002) with _π_<sup>_g_</sup> and _π_ in Kakade & Langford (2002) with _π_<sup>_e_</sup> . According to (Kakade & Langford, 2002) an example can be provided where this bound is tight. 

This establishes that the performance improvement of the mixed policy ˜ _π_ over the exploration policy _π_<sup>_e_</sup> is positive when the expected policy improvement of the guidance policy over the execution policy _Es∼dπe_ [<sup>�</sup> _a_<sup>_πg_(</sup><sup>_·|s_)</sup><sup>_Aπe_(</sup><sup>_st, a_)] is larger than the term</sup><sup>_−_2(1</sup><sup>_−γ_)</sup><sup>_ε_(</sup> 1 _−_ <u>1</u> _γ_<sup>_−_</sup> 1 _−γ_ (11 _−α_ )<sup>) which</sup> results from the distribution shift due to using the guidance policy instead of only the execution policy. 

Moreover, according to Corallary 4.2 in Kakade & Langford (2002), when _Es∼dπe_ [<sup>�</sup> _a_<sup>_πg_(</sup><sup>_·|s_)</sup><sup>_Aπe_(</sup><sup>_st, a_)]</sup><sup>_≥_0andwhenthemaximalimmediaterewardispositive,we</sup> can always choose _α_ such that the performance improvement is positive (see Kakade & Langford (2002) for details). 

22 

Published as a conference paper at ICLR 2026 

### C MORE RELATED WORK 

In this section, we give a more detailed related work review. 

**RL with task-specific offline datasets** Leveraging offline data is a promising direction to improve sample efficiency in RL. One representative approach is offline RL, which trains agents using offline data without environment interaction. These methods typically constrain the distance between learned and behavior policies in different ways (Kumar et al., 2020; Fujimoto & Gu, 2021; Kumar et al., 2019; Wu et al., 2019; Kostrikov et al., 2021; 2022; Uchendu et al., 2023). However, policy performance is highly dependent on dataset quality (Yarats et al., 2022). To enable continued improvement, offline-to-online RL methods (Lee et al., 2022; Zhao et al., 2022; Yu & Zhang, 2023; Nair et al., 2020; Rafailov et al., 2023) were developed, which fine-tune policies trained with offline RL by interacting with environments. MOTO (Rafailov et al., 2023) proposes a model-based offline-to-online RL method with reward-labeled data, and requires model-based value expansion, policy regularization, and controlling epistemic uncertainty, while our method leverages reward-free and multi-embodiment data and requires none of the techniques proposed by MOTO. 

Typical offline-to-online RL face training instability challenges (Lee et al., 2022; Lu et al., 2023). To mitigate this issue, RLPD (Ball et al., 2023) is proposed and demonstrates strong performance by simply concatenating offline and online data, but requires reward-labeled task-specific offline data and does not address multi-embodiment scenarios. ExPLORe (Li et al., 2023) labels reward-free offline data using approximated upper confidence bounds (UCB) to solve hard exploration tasks, but relies on near-expert data for the target tasks, while we consider a more general setting with non-curated data. 

**RL with multi-task offline datasets** Recent work has explored multi-task offline RL (Kumar et al., 2023; Hansen et al., 2024; Julian et al., 2020; Kalashnikov et al., 2021; Yu et al., 2021), but requires known rewards. PWM (Georgiev et al., 2024) and TDMPC-v2 (Hansen et al., 2024) train world models for multi-task RL but are limited to state-based inputs and reward-labeled data. To handle unknown rewards, approaches like human labeling (Cabi et al., 2020; Singh et al., 2019), inverse RL (Ng et al., 2000; Abbeel & Ng, 2004), or generative adversarial imitation learning (Ho & Ermon, 2016) can be used, though these require human labor or expert demonstrations. Yu et al. (2022) assigns zero rewards to unlabeled data, which introduces additional bias. Apart from these, there is a line of work that focuses on representation learning from in-the-wild data (Schwarzer et al., 2021; Parisi et al., 2022; Yang & Nachum, 2021; Yuan et al., 2022; Stooke et al., 2021; Shah & Kumar, 2021; Wang et al., 2022; Sun et al., 2023; Ze et al., 2023; Ghosh et al., 2023) but fails to utilize rich information in the dataset, such as dynamics. 

Recent studies (Seo et al., 2022; Wu et al., 2025; 2023) explore world model pre-training with actionfree data, focusing on world model architecture design to utilize the action-free data. However, we demonstrate that naive fine-tuning of pre-trained world models fails on challenging tasks, while our method, incorporating experience rehearsal and execution guidance, significantly improves RL performance across 72 tasks. 

**Unsupervised RL** In unsupervised RL, an agent explores the environment based on intrinsic motivations, and the models’ parameters are initialized during this self-motivated exploration stage, aiming for fast downstream task learning (Rajeswar et al., 2023; Pathak et al., 2017; Burda et al., 2019; Eysenbach et al., 2019; Pathak et al., 2019; Liu & Abbeel, 2021a; Sekar et al., 2020; Liu & Abbeel, 2021b; Yarats et al., 2021; Laskin et al., 2021; Mazzaglia et al., 2023; Xu et al., 2022). Our problem setting differs from unsupervised RL in several ways: i) Unsupervised RL interacts with the environment actively while we leverage _static_ offline datasets, ii) unsupervised RL gives a specific focus on designing different intrinsic rewards, while our setting focuses on improving sample efficiency by leveraging unlabeled datasets. 

**Generalist Agents** RL methods usually perform well on a single task (Vinyals et al., 2019; Andrychowicz et al., 2020), however, this contrasts with humans who can perform multiple tasks well. Recent works have proposed generalist agents that master a diverse set of tasks with a single agent (Reed et al., 2022; Brohan et al., 2023b; Team et al., 2024; Zhao et al., 2024). These methods typically resort to scalable models and large datasets and are trained via imitation learning (Brohan et al., 2023b;a; O’Neill et al., 2023; Khazatsky et al., 2024). In contrast, we train a task-agonistic world model and use it to boost RL performance for multiple tasks and embodiments. 

23 

Published as a conference paper at ICLR 2026 

**World models** World models learn to predict future observations or states based on historical information. World models have been widely investigated in online model-based RL (Hafner et al., 2020; Ha & Schmidhuber, 2018; Micheli et al., 2023; Alonso et al., 2024; Scannell et al., 2025). Recently, the community has started investigating scaling world models (Ha & Schmidhuber, 2018), for example, Hu et al. (2023a); Pearce et al. (2024); Wu et al. (2025); Agarwal et al. (2025); Mereu et al. (2025) train world models with Diffusion Models or Transformers. However, these models are usually trained on demonstration data. In contrast, we explore the offline-to-online RL setting – closely fitting the pre-train and then fine-tune paradigm – and we focus on leveraging reward-free and multi-embodiment data to increase the amount of available data for pre-training. We further identify the distributional shift issue when fine-tuning the pre-trained world model and mitigate the issue by proposing experience rehearsal and execution guidance. 

### D LIMITATIONS 

Although demonstrating strong performance on a diverse set of tasks, our method has the following limitations. _1)_ The world model architecture used in our paper is the recurrent state space model. This model is built upon RNN, which can be limited for scaling. This can be mitigated by using a Transformer and a diffusion-based world model. However, we note that the main conclusion of this paper should still be valid. _2)_ We do not thoroughly discuss the generalization ability of the pre-trained world model. With DMControl tasks, our method shows a promising trend in generalizing to unseen tasks. However, generalization to new embodiments or novel configurations is still challenging, which requires even diverse training data. _3)_ The non-curated offline data used in our paper, although lifting several key assumptions in previous offline-to-online RL, is still in-domain data, i.e., our current method is not able to leverage the vast in-the-wild data. A promising direction is to combine in-the-wild data for pre-training as in (Wu et al., 2025) and the domain-specific “in-house” data (as used in our paper) for post-training. _4)_ We only conduct experiments in the simulator. Considering the sample efficiency of our proposed method, it could be promising to conduct experiments on real-world applications. 

### E DISCLOSURE OF LLMS USAGE 

Large Language Models (LLMs) were used to assist word choice, improving grammar as well as proof checking in Sec. B. LLMs were also used in compressing the Related Work section due to page limits. The Related Work section was initially written by authors without using LLMs and the compressed text was subsequently revised by the authors. The main draft was written by authors without using LLMs. The ideas were formalized independently of LLMs assistance. 

### F COMPUTE RESOURCES 

We conduct all experiments on clusters equipped with AMD MI250X GPUs, 64-core AMD EPYC “Trento” CPUs, and 64 GBs DDR4 memory. For pre-training, it takes _∼_ 48 GPU hours for 150k steps. For fine-tuning, it tasks _∼_ 8 GPU hours per run for 150K environment steps. Note that due to AMD GPUs not supporting hardware rendering, the training time should be longer than using Nvidia GPUs. To reproduce the NCRL’s results in Fig. 3, it roughly takes 8 h * 72 tasks * 3 seeds = 1728 GPU hours. 

### G IMPLEMENTATION DETAILS 

#### G.1 BEHAVIOR CLONING 

The Behavior Cloning methods used in both the execution guidance of NCRL and JSRL-BC are the same. We use a four-layer convolutional neural network (LeCun et al., 1995) with kernel depth [32, 64, 128, 256] following a three-layer MLPs with LayerNorm (Ba et al., 2016) after all linear layers. 

We list the adopted encoder and actor architectures for reference. 

24 

Published as a conference paper at ICLR 2026 

1 <mark>class Encoder(nn.Module):</mark> 2 <mark>def __init__(self, obs_shape):</mark> 3 <mark>super().__init__()</mark> 4 <mark>assert obs_shape == (9, 64, 64), f’obs_shape is {(obs_shape)}, but expect (9, 64, 64)’ # inputs shape</mark> 5 6 <mark>self.repr_dim = (32 * 8) * 2 * 2</mark> 7 <mark>_input_channel = 9</mark> 8 9 <mark>self.convnet = nn.Sequential(</mark> 10 <mark>nn.Conv2d(_input_channel, 32, 4, stride=2), # [B, 32, 31, 31]</mark> 11 <mark>nn.ELU(),</mark> 12 <mark>nn.Conv2d(32, 32*2, 4, stride=2), #[B, 64, 14, 14]</mark> 13 <mark>nn.ELU(),</mark> 14 <mark>nn.Conv2d(32*2, 32*4, 4, stride=2), #[B, 128, 6, 6]</mark> 15 <mark>nn.ELU(),</mark> 16 <mark>nn.Conv2d(32*4, 32*8, 4, stride=2), #[B, 256, 2, 2]</mark> 17 <mark>nn.ELU())</mark> 18 <mark>self.apply(utils.weight_init)</mark> 19 20 <mark>def forward(self, obs):</mark> 21 <mark>B, C, H, W = obs.shape</mark> 22 23 <mark>obs = obs / 255.0 - 0.5</mark> 24 <mark>h = self.convnet(obs)</mark> 25 <mark># reshape to [B, -1]</mark> 26 <mark>h = h.view(B, -1)</mark> 27 <mark>return h</mark> 

1 <mark>class Actor(nn.Module):</mark> 2 <mark>def __init__(self, repr_dim, action_shape, feature_dim=50, hidden_dim =1024):</mark> 3 <mark>super().__init__()</mark> 4 <mark>self.trunk = nn.Sequential(nn.Linear(repr_dim, feature_dim),</mark> 5 <mark>nn.LayerNorm(feature_dim), nn.Tanh())</mark> 6 7 <mark>self.policy = nn.Sequential(nn.Linear(feature_dim, hidden_dim),</mark> 8 <mark>nn.LayerNorm(hidden_dim), nn.ELU(),</mark> 9 <mark>nn.Linear(hidden_dim, hidden_dim),</mark> 10 <mark>nn.LayerNorm(hidden_dim), nn.ELU(),</mark> 11 <mark>nn.Linear(hidden_dim, action_shape[0]))</mark> 12 13 <mark>self.apply(utils.weight_init)</mark> 14 15 <mark>def forward(self, obs, std):</mark> 16 <mark>h = self.trunk(obs)</mark> 17 <mark>return self.policy(h)</mark> 

#### G.2 JSRL+BC 

Jump-start RL (Uchendu et al., 2023) is proposed as an offline-to-online RL method. It includes two policies, a prior policy _πθ_ 1( _a|s_ ) and a behavior policy _πθ_ 2( _a|s_ ), where the prior policy is trained via offline RL methods and the behavior policy is updated during the online learning stage. However, offline RL requires the offline dataset to include rewards for the target task. To extract behavior policy from the offline dataset, we use the BC agent described above as the prior policy. During online training, in each episode, we randomly sample the rollout horizon _h_ of the prior policy from a pre-defined array np.arange(0, 101, 10). We then execute the prior policy for _h_ steps and switch to the behavior policy until the end of an episode. 

25 

Published as a conference paper at ICLR 2026 

#### G.3 EXPLORE 

For the ExPLORe baseline, we follow the original training code<sup>2</sup> . We sweep over several design choices: i) kernel size of the linear layer used in the RND and reward models: [256 (default), 512]; ii) initial temperature value: [0.1 (default), 1.0]; iii) whether to use LayerNorm Layer (no by default); iv) learning rate: [1e-4, 3e-4 (default)]. However, we fail to obtain satisfactory performance. There are several potential reasons: i) the parameters used in the ExPLORe paper are tuned specifically to their setting, where manipulation tasks and near-expert trajectories are used; ii) the coefficient term of the RND value needs to be tuned carefully for different tasks and the reward should also be properly normalized. 

To achieve reasonable performance and eliminate the performance gap caused by implementationlevel details, we make the following modifications: i) we replace the RND module with ensembles to calculate uncertainty; ii) the reward function shares the latent space with the actor and critic. 

> 2Source code of ExPLORe https://github.com/facebookresearch/ExPLORe 

26 

Published as a conference paper at ICLR 2026 

### H ALGORITHM 

The full algorithm is described in Alg. 1. 

**Algorithm 1** Efficient RL by Guiding World Models with Non-Curated Offline Data **Require:** Non-curated offline data _D_ off, Online data _D_ on _←∅_ , Retrieval data _D_ retrieval _←∅_ World model _fθ, qθ, pθ, dθ_ Policy _πϕ_ RL, _πϕ_ BC, Value function _vϕ_ and Reward _rξ_ . _// Task-Agnostic World Model Pre-Training_ **for** num. pre-train steps **do** Randomly sample mini-batch _B_ off : _{ot, at, ot_ +1 _}_<sup>_T_</sup> _t_ =0<sup>from</sup><sup>_D_off.</sup> Update world model _fθ, qθ, pθ, dθ_ by minimizing Eq. (1) on sampled batch _B_ . **end for** _// Task-Specific Training // Experience Retrieval_ Collect one initial observation _o_<sup>0</sup> on<sup>from the environment.</sup> Compute the visual similarity between _o_ on and initial observations of trajectories _o_ off in _D_ off using Eq. (5). Select R trajectories according to Eq. (5) and fill _D_ retrieval. _// Behavior Cloning Policy Training_ **for** num. bc updates **do** Randomly sample mini-batch _B_ retrieval : _{ot, at}_<sup>_N_</sup> _t_ =0<sup>from</sup><sup>_D_retrieval.</sup> Update _πϕ_ BC by minimizing _− N_<sup><u>1</u></sup> � _Nt_ =0<sup>log</sup><sup>_πϕ_BC(</sup><sup>_at|ot_).</sup> **end for** _// Task-Specific RL Fine-Tuning_ **for** num. episodes **do** _// Collect Data_ Decide whether to use _πϕ_ BC according to the predefined schedule. **if** Select _πϕ_ BC **then** Randomly select the starting time step _k_ and the rollout horizon _H_ . **end if** _t ←_ 0 **while** _t ≤_ episode length **do** _at_ = _πϕBC_ ( _at|ot_ ) if Use _πϕ_ BC and _k ≤ t ≤ H_ else _at_ = _πϕRL_ ( _at|ot_ ). Interact with the environment using _at_ . Store _{ot, at, rt, ot_ +1 _}_ to _D_ on. _t ← t_ + 1 **end while** _// Update Models_ **for** num. grad steps **do** Randomly sample mini-batch _B_ on : _{ot, at, rt, ot_ +1 _}_<sup>_T_</sup> _t_ =0<sup>from</sup><sup>_Don_and</sup><sup>_B_retrieval</sup> : _{ot, at, rt, ot_ +1 _}_<sup>_T_</sup> _t_ =0<sup>from</sup><sup>_D_retrieval.</sup> Update world model _fθ, qθ, pθ, dθ_ by minimizing Eq. (1) on sampled batch _{B_ on _, B_ retrieval _}_ . Update _rξ_ by minimizing _− N_<sup><u>1</u></sup> � _Ni_ =0<sup>log</sup><sup>_pξ_(</sup><sup>_rt|st_) on</sup><sup>_B_on.</sup> ◁ _st_ = [ _ht, zt_ ] _// Update policy and value function_ Generate imaginary trajectories _τ_ ˜ = _{st, at, st_ +1 _}_<sup>_T_</sup> _t_ =0<sup>by rolling out</sup><sup>_hθ, pθ_with</sup><sup>_πϕ_</sup> RL<sup>.</sup> Update policy _πϕ_ RL and value function _vϕ_ with Eq. (4). **end for end for** 

27 

Published as a conference paper at ICLR 2026 

### I FULL RESULTS 

In Table 3 and Table 4, we list the success rate of 50 Meta-World benchmark tasks with pixel inputs. In Table 5, we list the episodic return of DMControl of 22 tasks. We compare NCRL at 150k samples with two widely used baselines DreamerV3 and DrQ-v2 at both 150k samples and 1M samples. We report the results over 5 random seeds for NCRL and 3 random seeds for DreamerV3 and DrQ-v2. The best results are marked with a bold font at 150k samples and the highest overall scores are marked with underline. The detailed result curves of both Meta-World and DMControl are shown in Fig. 17, Fig. 18, and Fig. 19. 

#### I.1 META-WORLD BENCHMARK 

Table 3: Success rate of Meta-World benchmark with pixel inputs. 

|Tasks|DreamerV3<br>@**1M**|DrQ-v2<br>@**1M**|DreamerV3<br>@**150k**|DrQ-v2<br>@**150k**|NCRL<br>@**150k**|
|---|---|---|---|---|---|
|Assembly|0.0|0.0|0.0|0.0|**0.44**|
|Basketball|0.0|0.97|0.0|0.0|**0.36**|
|Bin Picking|0.0|0.93|0.0|0.33|**0.84**|
|Box Close|0.13|0.9|0.0|0.0|**0.88**|
|Button Press|1.0|0.7|0.47|0.13|**0.76**|
|Button Press<br>Topdown|1.0|1.0|0.33|0.17|**1.0**|
|Button Press<br>Topdown Wall|1.0|1.0|0.73|0.63|**1.0**|
|Button Press Wall|1.0|1.0|0.93|0.77|**1.0**|
|Coffee Button|1.0|1.0|1.0|1.0|1.0|
|Coffee Pull|0.6|0.8|0.0|**0.6**|0.56|
|Coffee Push|0.67|0.77|0.13|0.2|**0.72**|
|Dial Turn|0.67|0.43|0.13|0.17|**0.65**|
|Disassemble|0.0|0.0|0.0|0.0|0.0|
|Door Close|-|-|-|-|1.0|
|Door Lock|1.0|0.93|0.6|**0.97**|0.96|
|Door Open|1.0|0.97|0.0|0.0|**0.92**|
|Door Unlock|1.0|1.0|**1.0**|0.63|0.92|
|Drawer Close|0.93|1.0|0.93|**1.0**|0.92|
|Drawer Open|0.67|0.33|0.13|0.33|**1.0**|
|Faucet Open|1.0|1.0|0.47|0.33|**1.0**|
|Faucet Close|0.87|1.0|**1.0**|**1.0**|0.92|
|Hammer|1.0|1.0|0.07|0.4|**1.0**|
|Hand Insert|0.07|0.57|0.0|0.1|**0.44**|
|Handle Press Side|1.0|1.0|1.0|1.0|**1.0**|
|Handle Press|1.0|1.0|0.93|0.97|**1.0**|
|Handle Pull Side|0.67|1.0|0.67|0.6|**1.0**|
|Handle Pull|0.67|0.6|0.33|0.6|**0.85**|
|Lever Pull|0.73|0.83|0.0|0.33|**0.72**|


More results see Table 4 

28 

Published as a conference paper at ICLR 2026 

Table 4: Success rate of Meta-World benchmark with pixel inputs (Cont.). 

|Tasks|DreamerV3<br>@**1M**|DrQ-v2<br>@**1M**|DreamerV3<br>@**150k**|DrQ-v2<br>@**150k**|NCRL (ours)<br>@**150k**|
|---|---|---|---|---|---|
|Peg Insert Side|1.0|1.0|0.0|0.27|**1.0**|
|Peg Unplug Side|0.93|0.9|**0.53**|0.5|0.48|
|Pick Out of Hole|0.0|0.27|0.0|0.0|**0.25**|
|Pick Place Wall|0.2|0.17|0.0|0.0|**0.64**|
|Pick Place|0.67|0.67|0.0|0.0|**0.20**|
|Plate Slide<br>Back Side|1.0|1.0|0.93|1.0|**1.0**|
|Plate Slide Back|1.0|1.0|0.8|0.97|**1.0**|
|Plate Slide Side|1.0|0.9|**0.73**|0.5|0.52|
|Plate Slide|1.0|1.0|0.93|**1.0**|0.95|
|Push Back|0.33|0.33|0.0|0.0|**0.32**|
|Push Wall|0.33|0.57|0.0|0.0|**0.84**|
|Push|0.26|0.93|0.0|0.13|**0.72**|
|Reach|0.87|0.73|**0.67**|0.43|0.40|
|Reach Wall|1.0|0.87|0.53|0.7|**0.80**|
|Shelf Place|0.4|0.43|0.0|0.0|**0.80**|
|Soccer|0.6|0.3|0.13|0.13|**0.16**|
|Stick Push|0.0|0.07|0.0|0.0|**0.64**|
|Stick Pull|0.0|0.33|0.0|0.0|**0.52**|
|Sweep Into|0.87|1.0|0.0|**0.87**|0.72|
|Sweep|0.0|0.73|0.0|0.3|**0.64**|
|Window Close|1.0|1.0|0.93|**1.0**|**1.0**|
|Window Open|1.0|0.97|0.6|**1.0**|0.96|
|**Mean**|0.656|0.753|0.360|0.430|**0.748**|
|**Medium**|0.870|0.900|0.130|0.330|**0.840**|


29 

Published as a conference paper at ICLR 2026 


Figure 17: Meta-World results. We report 5 seeds for NCRL and 3 seeds for DrQ-v2 and DreamerV3. 

30 

Published as a conference paper at ICLR 2026 


Figure 18: Meta-World results (Cont.). We report 5 seeds for NCRL and 3 seeds for DrQ-v2 and DreamerV3. 

31 

Published as a conference paper at ICLR 2026 

#### I.2 DMCONTROL BENCHMARK 

Table 5: Episodic return of DMControl benchmark with pixel inputs. 

|Tasks|DreamerV3<br>@**500k**|DrQ-v2<br>@**500k**|DreamerV3<br>@**150k**|DrQ-v2<br>@**150k**|NCRL(ours)<br>@**150k**|
|---|---|---|---|---|---|
|CartPole Balance|994.3|992.3|955.8|983.3|**995.0**|
|Acrobot Swingup|222.1|30.3|**85.2**|20.8|84.6|
|Acrobot Swingup<br>Sparse|2.5|1.17|1.7|1.5|**12.2**|
|Acrobot Swingup<br>Hard|-0.2|0.3|**2.0**|0.4|-17.1|
|Walker Stand|965.7|947.6|946.2|742.9|**974.1**|
|Walker Walk|949.2|797.8|808.9|280.1|**960.5**|
|Walker Run|616.6|299.3|224.4|143.0|**707.7**|
|Walker Backflip|293.6|96.7|128.2|91.7|**266.1**|
|Walker Walk<br>Backward|942.9|744.3|625.9|470.9|**887.6**|
|Walker Walk<br>Hard|-2.1|-9.5|-4.7|-17.1|**842.8**|
|Walker Run<br>Backward|363.8|246.0|229.4|167.4|**366.0**|
|Cheetah Run|843.7|338.1|**621.4**|251.2|543.8|
|Cheetah Run<br>Front|473.8|202.4|143.1|108.4|**317.6**|
|Cheetah Run<br>Back|657.4|294.4|407.6|171.2|**462.3**|
|Cheetah Run<br>Backwards|693.8|384.3|**626.6**|335.6|521.6|
|Cheetah Jump|597.0|535.6|200.8|251.8|**614.2**|
|Quadruped Walk|369.3|258.1|145.2|76.5|**855.6**|
|Quadruped Stand|746.0|442.2|227.2|318.9|**941.4**|
|Quadruped Run|328.1|296.5|183.0|102.8|**766.9**|
|Quadruped Jump|689.6|478.3|168.3|190.5|**820.2**|
|Quadruped Roll|663.9|446.0|207.9|126.2|**948.0**|
|Quadruped Roll<br>Fast|508.8|366.9|124.8|164.7|**758.9**|
|**Mean**|541.81|372.23|320.86|226.49|**617.73**|
|**Medium**|606.8|318.70|204.35|166.05|**733.3**|


32 

Published as a conference paper at ICLR 2026 


Figure 19: DMControl results. We report 5 seeds for NCRL and 3 seeds for DrQ-v2 and DreamerV3. 

33 

Published as a conference paper at ICLR 2026 

### J HYPERPARAMETERS 

In this section, we list important hyperparameters used in NCRL. 

Table 6: Hyperparameters used in NCRL. 

|**Hyperparameter**|**Value**|
|---|---|
|**Pre-training**||
|Stacked images|1|
|Pretrain steps|200,000|
|Batch size|16|
|Sequence length|64|
|Replay buffer capacity|Unlimited|
|Replay sampling strategy|Uniform|
|RSSM||
|Hidden dimension|12288|
|Deterministic dimension|1536|
|Stochastic dimension|32 * 96|
|Block number|8|
|Layer Norm|True|
|CNN channels|[96, 192, 384, 768]|
|Activation function|SiLU|
|Optimizer||
|Optimizer|Adam|
|Learning rate|1e-4|
|Weight decay|1e-6|
|<br>Eps|1e-5|
|Gradient clip|100|
|**Fine-tuning**||
|Warm-up frames|15000|
|Execution Guidance Schedule|linear(1,0,50000) for DMControl<br>linear(1,0,1,150000) for Meta-Wolrd|
|Action repeat|2|
|Offline data mix ratio|0.25|
|Discount|0.99|
|Discount lambda|0.95|
|MLPs|[512, 512, 512]|
|MLPs activation|SiLU|
|Actor critic learning rate|8e-5|
|Actor entropy coef|1e-4|
|Target critic update fraction|0.02|
|Imagine horizon|16|


34 

Published as a conference paper at ICLR 2026 

### K TASK VISUALIZATION 


Figure 20: Visualization of tasks from DMControl and Meta-World used in our paper. 

35 

