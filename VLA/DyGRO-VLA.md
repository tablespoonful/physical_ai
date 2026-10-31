---
title: "DyGRO-VLA: Cross-Task Scaling of Vision-Language-Action Models via Dynamic Grouped Residual Optimization"
date: "2026-05-17"
authors: "Sixu Lin; Yunpeng Qing; Litao Liu; Ming Zhou; Ruixing Jin; Xiaoyi Fan"
venue: "ICML 2026"
url: https://arxiv.org/abs/2605.17486
pdf: https://arxiv.org/pdf/2605.17486
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.17486)** / [論文ページ](https://arxiv.org/abs/2605.17486)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 

**Sixu Lin**<sup>1 2</sup> **Yunpeng Qing**<sup>3</sup> **Litao Liu**<sup>4</sup> **Ming Zhou**<sup>5</sup> **Ruixing Jin**<sup>1</sup> **Xiaoyi Fan**<sup>2</sup> **Guiliang Liu**<sup>1 6</sup><sup>_†_</sup> 

## **Abstract** 

Recent progress in Reinforcement Learning (RL) provides a principled approach to optimizing Vision-Language-Action (VLA) models, facilitating a shift from trajectory imitation to active learning in the task environment. Despite improvements in control precision, most RL optimizers remain task-specific, which reduces VLA models from generalist controllers to policies that overfit to a narrow set of tasks. In this study, we conduct an in-depth analysis of this phenomenon and highlight the importance of cross-task feature representations for improving the generalizability of VLA models. Motivated by this finding, we introduce DyGRO-VLA, a two-stage optimization framework that 1) effectively captures cross-task latent representations based on information-theoretic principles, and 2) dynamically refines policy optimization via a mixture-ofRL-residuals. DyGRO-VLA enables the RL optimizer to exploit task-relevant latent information while strategically mitigating adverse interference on the learned representations throughout the optimization process. We evaluate our approach on LIBERO, RoboTwin2 benchmarks, and further validate it on real world, demonstrating consistent improvements over strong baselines under multitask training and distribution shift. Our project page is available at DyGRO-VLA. 

## **1. Introduction** 

Under the rapid development of large-scale foundation models, Vision-Language-Action (VLA) models have emerged 

> _†_ Corresponding author. 1School of Data Science, The Chinese University of Hong Kong (Shenzhen)<sup>2</sup> Jiangxing Intelligence Technology Inc.<sup>3</sup> Zhejiang University<sup>4</sup> Rutgers UniversityNew Brunswick 5Shanghai AI Laboratory 6Shenzhen Loop Area Institute. Correspondence to: Guiliang Liu _<_ liuguiliang@cuhk.edu.cn _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

as a promising paradigm for generalist robot manipulation policy by unifying perception, language understanding, and action control (Ma et al., 2024). Compared with lightweight task-specific policies (Chi et al., 2023; Zhao et al., 2023), VLAs typically offer stronger semantic grounding and better multi-task transfer, largely due to their higher representational capacity and the ability to reuse shared structure across heterogeneous tasks. As a result, VLAs are widely viewed as an important step toward general-purpose robots that can solve diverse real-world tasks with a unified model (Black et al., 2024; Intelligence et al., 2025). 

Despite these advances, training a high-performing generalist policy solely from offline demonstrations remains challenging. Compared to datasets for language modeling and visual understanding, robotic datasets are relatively small, less diverse, and costly to collect (Xing et al., 2025), especially for long-tail scenarios that are less likely to be encountered in practice. To mitigate the data scarcity issues, recent studies incorporate online Reinforcement Learning (RL) to optimize VLA in the post-training (Chen et al., 2025b; Lu et al., 2025; Li et al., 2025a; Zang et al., 2025). 

While RL-based optimization can effectively improve success rates on individual dexterous manipulation tasks (Luo et al., 2024; 2025), these gains often come at the expense of losing cross-task scalability. Our in-depth study reveals that as the number of tasks increases, the performance of RL optimization degrades substantially (see Figure 2). In some cases, it even harms the original VLA model that was pre-trained on offline data (see Figure 1). We find that this failure mode arises because the RL optimizer can distort the shared representation learned during pretraining, effectively isolating task-specific experience and reducing cross-task knowledge sharing (see Figure 3). This distortion leads to catastrophic forgetting and weakens cross-task adaptation. Therefore, balancing the trade-off between dexterity and generalizability remains a significant open challenge. 

To address this challenge, we propose Dynamic Grouped Residual Optimization (DyGRO), a cross-task optimizer for VLA models. Specifically, DyGRO-VLA follows a twostage optimization paradigm with the following objectives: 

1) _Learning shared representations across tasks._ DyGRO- 

1 

**DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 

VLA follows the Information Bottleneck (IB) principle (Tishby et al., 1999) to extract action-relevant features from visual observations and robot states. By preserving useful information for guiding robot motion while discarding nuisance factors (e.g., background clutter and lighting variations), these features can be more effectively shared across tasks. Practically, to make IB learning computationally tractable, we derive a variational lower bound tailored to offline robot behavior modeling and use it to jointly train the feature representation and action prediction models. 

2) _Finetuning with Mixture-of-RL-Residuals (MoRR)._ To optimize the policy without disrupting the shared cross-task representation, we design the RL policy to predict a residual as refinements of the prediction from the action model (Johannink et al., 2019). However, classic residual learning is typically tailored to a single task. To generalize across a variety of tasks, we strategically combine residual refinements from a mixture of RL policies, where the mixture weights are determined by a dynamic routing mechanism. Consequently, while each policy only specializes in a subset of tasks, the router can adaptively select and compose them to produce the most effective refinement for the current tasks. To implement MoRR, we introduce a task-embedding method that provides task information to the router, based on which we design an online training scheme that jointly updates the RL residual policies and the routing model. 

To validate the effectiveness of DyGRO-VLA, we conduct extensive experiments across diverse multi-task manipulation benchmarks, including LIBERO (Liu et al., 2023) and RoboTwin2 (Chen et al., 2025a). Across all settings, DyGRO-VLA consistently outperforms state-ofthe-art baselines, achieving the highest average success rate of 97.1% on LIBERO, an absolute gain of +4.4% over its offline base model—and demonstrating substantial improvements on the most challenging LIBERO-Long suite (+9.8%). Furthermore, in real-world evaluations on RoboTwin2, DyGRO-VLA attains the best overall success in simulation (79.2%) and surpasses RFT baselines under Sim2Real transfer, particularly on complex bimanual and long-horizon tasks. These results highlight DyGRO-VLA as a scalable and robust solution for efficient multi-task reinforcement fine-tuning and real-world robotic manipulation. 

## **2. Related Work** 

**Multi-task Learning.** A central challenge in multi-task learning is the interference among task gradients, which can hinder optimization efficiency. Prior work has sought to mitigate this issue through sample- or task-level reweighting strategies (Peng et al., 2023). Broadly, existing approaches fall into two categories: (1) designing reweighting schemes to balance the relative contributions of different tasks (Sener & Koltun, 2018; Parisotto et al., 2015; Yu et al., 2020), and 

(2) adjusting per-task gradient directions to reduce conflicts and encourage cooperative learning (Yu et al., 2020; Liu et al., 2021; Chen et al., 2020; Wang et al., 2020; Bohn et al., 2024). More recently, token-level MoE routing methods have also been proposed to address gradient conflicts at finer granularity (Yang et al., 2024). (Yang et al., 2020; Huang et al., 2024; Kong et al., 2025; Wu et al., 2025) utilize routing strategy to resolve multi-task gradient conflicts. 

**Reinforcement Learning for Vision-Language-Action Models.** Recent studies demonstrate that reinforcement finetuning can significantly improve VLA performance in manipulation tasks (Huang et al., 2025; Liu et al., 2025; Chen et al., 2025b; Guo et al., 2025; Tan et al., 2025; Li et al., 2025a; Zang et al., 2025). (Liu et al., 2025) analyzes the generalization benefits brought by RL to VLAs, while (Chen et al., 2025b) successfully deploys reinforced fine-tuning in real-world sparse-reward settings, showcasing effective adaptation in challenging robotic scenarios. In addition, (Guo et al., 2025) proposes an iterative learning paradigm that stabilizes training and improves efficiency. Different from these works, our method emphasizes the _scalability_ of VLA post-training. While prior approaches focus on task-level performance gains or real-world adaptation, we argue that RL should preserve the intrinsic generalization ability of large VLAs, fundamentally distinguishing them from lightweight, task-specific models. 

## **3. Problem Formulation** 

In this section, we discuss the problem of cross-task finetuning of VLA policies using RL methods and formulate the key challenges with empirical evidence. 

**Multi-task Reinforcement Learning.** We consider solving a distribution of tasks _ζ ∼ p_ ( _ζ_ ) with a single policy _π_ . In this setting, each task induces a POMDP _M_<sup>_ζ_</sup> = ( _S_<sup>_ζ_</sup> _, A, P_<sup>_ζ_</sup> _, R_<sup>_ζ_</sup> _, O_<sup>_ζ_</sup> _, ρ_<sup>_ζ_</sup> _, γ_ ). A task begins at an initial state _s_ 0 _∼ ρ_<sup>_ζ_</sup> . At each timestep _t_ , the agent receives an observation _ot ∈O_<sup>_ζ_</sup> composed of RGB images, robot proprioceptive information, and a natural language instruction. The agent then selects an action _at ∈A_ from the shared primitive action space, receives a reward _rt ∼ R_<sup>_ζ_</sup> , and transitions to the next state _st_ +1 following the transition function _P_<sup>_ζ_</sup> . For brevity, we assume sparse rewards for robotic control: the agent receives a success reward of +1 upon task completion. The objective of the policy _π_ is to maximize the expected discounted return across the task distribution: 


Striving for temporal abstraction, we implement _π_ ( **a** _t | ot_ ) as _action chunking_ policy (Zhao et al., 2023; Huang et al., 2025; Li et al., 2025b). An action chunk is defined as **a** _t_ = _at_ : _t_ + _h−_ 1 _∈A_<sup>_h_</sup> . 

2 

**DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 


_Figure 1._ Catastrophic Forget- _Figure 2._ Multi-Task Conting. RFT may improve the flict. As the number of tasks trained tasks but leads to inincreases, RFT becomes unstacreasing performance drops on ble and increasingly ineffective. other tasks. 

**Catastrophic Forgetting in Cross-Tasks Adaptation.** Developing scalable and general-purpose VLA models is a central objective in embodied robotic control (Black et al., 2024; Shi et al., 2025; Intelligence et al., 2025). Although recent advances in reinforcement learning (RL) optimization have substantially improved the dexterity and task success rates of VLA policies (Li et al., 2025a; Lu et al., 2025), these models often remain highly task-specific. In particular, such RL optimizers tend to overfit to individual tasks and consequently struggle to retain prior knowledge in continual multi-task learning settings. 

For empirical evidence, we test on LIBERO (Liu et al., 2023) benchmark. We conduct empirical analysis using the VLA model introduced in Section 4.1. As shown in Figure 1, when training a VLA on LIBERO-Spatial, we observe that performance on unrelated tasks in LIBERO-Object rapidly declines as training progresses. The success rate drops significantly, indicating that specialization on spatial tasks erodes the model’s capacity to handle object-centric tasks. 

Delving into the phenomenon of catastrophic forgetting, we observe that a fundamental prerequisite for the scalability of VLA models is the development of a shared feature space capable of encoding useful information across diverse tasks. However, during fine-tuning on a specific task, the RL agent often distorts this shared representation by isolating its representation of its experience from others. As shown in Figure 3, single-task RFT drives the tuned task’s representations to form an isolated cluster, indicating a drift away from the shared feature space and reduced alignment with other similar tasks. It eventually results in a deterioration of VLA’s cross-task competencies. 

**Rethinking RL Post-training for VLA.** Revisiting the objective of VLA models, the ultimate goal is to learn a generalist control policy capable of performing effectively across diverse tasks. In practice, the variations among these tasks, including differences in time horizons, the number and types of target objects, and the visual, physical, and dynamic properties of the environments, are substantial (Kroemer et al., 2021; Kawaharazuka et al., 2025). Given the 


_Figure 3._ **t-SNE visualization of the shared feature space on LIBERO.** We embed representations from 40 tasks (10 samples per task) before and after single-task RFT. 

inherently task-driven nature of RL optimizers, they are prone to overfitting to specific tasks and forgetting previously learned ones, as discussed above. This tendency naturally introduces a trade-off between achieving high task success rates and maintaining cross-task scalability. This trade-off poses a significant challenge for the direct application of RL optimizers in VLA models. To study this effect, we perform RL post-training with a classic actor–critic algorithm, Soft Actor-Critic (SAC) (Haarnoja et al., 2018). We evaluate three multi-task regimes (3 random seeds): (i) a single task from the LIBERO Spatial suite, (ii) 10 tasks from LIBERO Spatial, and (iii) 20 tasks from LIBERO Spatial and LIBERO Goal. As illustrated in Figure 2, the average success rate becomes increasingly unstable as the number of tasks grows during RL post-training. In particular, when trained on 10 tasks, only marginal improvements are observed, whereas with 20 tasks, the average success rate declines sharply, underscoring the limitations of current multi-task RL optimizers. 

In this study, unlike prior works (Chen et al., 2025b; Lu et al., 2025; Li et al., 2025a) that focus on how RL optimizes the performance of individual tasks (i.e., for each task _ζ_ , max E _Mζ_ [<sup>�</sup> _t_<sup>_∞_</sup> =0<sup>_γtrt_]), we examine the collective</sup> success rates of tasks as a group (i.e., for all _ζ ∼ p_ ( _ζ_ ), max _|ζ_<sup><u>1</u></sup> _|_ � _ζ_<sup>E</sup><sup>_M_</sup> _ζ_<sup>[�</sup> _t_<sup>_∞_</sup> =0<sup>_γtrt_])andintroduceanovelRL</sup> framework that effectively addresses the trade-off between accuracy and scalability in VLA post-training. 

## **4. DyGRO-VLA** 

To achieve scalable cross-task performance, we propose DyGRO-VLA, a RL optimization framework for VLA models. Similar to recent VLA post-training methods (Lu et al., 2025; Li et al., 2025a;b), DyGRO-VLA follows an _offline pretraining_ -to- _online fine-tuning_ paradigm. However, unlike prior works targeting individual task performance, DyGRO-VLA seeks to generalize across multiple tasks by 1) learning shared representations in pretraining and 2) optimizing the performance all tasks concurrently during post-training. 

3 

**DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 


_Figure 4._ **Method pipeline.** DyGRO-VLA follows a two-stage training recipe. **1) Offline stage:** we train the VLA backbone to predict actions while learning a compact latent representation via an information-bottleneck (IB) objective. **2) Online stage:** we freeze the VLA backbone and optimize the residual MoE in online multi-task settings, serving as a residual compensation module on top of the base model to further improve overall multi-task ability and generalization. 

### **4.1. Offline Pre-Training for Cross-Task Representation** 

The goal of pretraining is to learn a cross-task latent representation _p_ ( _z | o_ ) that not only captures essential information from the observation _o_ but also facilitates the learning of the action model _π_ ( _a | z_ ) across diverse tasks. 

**Latent Feature Extraction.** DyGRO-VLA implements _p_ ( _z | o_ ) using a VLM backbone coupled with a fusion module to encode exteroception from sensors and commands, and to fuse these features with proprioceptive information. 

At each time step _t_ , the backbone processes images from both wrist and third-view cameras **_X_** _t_ together with an instruction _Lt_ . Visual observations are encoded using DINOv2 (Oquab et al., 2024) and SigLIP (Zhai et al., 2023), and subsequently fused with tokenized language representations through a Qwen2.5-0.5B LLM (Team, 2024), yielding a sequence of hidden states. These hidden states are then partitioned into _conditioning tokens h_<sup>cond</sup> _t_ and _action tokens h_<sup>act</sup> _t_<sup>, where</sup><sup>_h_cond</sup> _t integrate_ vision and language. 

Upon completing the encoding stage, the fusion module initializes a set of learnable action-query tokens _qt_<sup>_a_and</sup> fuses them with _h_<sup>cond</sup> _t_ , _h_<sup>act</sup> _t_<sup>, and the proprioceptive input</sup><sup>_pt_</sup> to produce _h_<sup>fuse</sup> _t_ (Wang et al., 2025). Appendix A.1 covers the details. 

**Learning Task-Sharing Representation.** To effectively extract task-sharing features _z_ ˜ _T_ from the fused latent features _h_<sup>fuse</sup> _t_ , DyGRO-VLA designs the learning objective based on the principle of Information Bottleneck (IB) (Tishby et al., 1999) and designs the learning objective as follows: 


where the probabilistic model _pθ_ ( _z|o_ ) first extracts _h_<sup>fuse</sup> _t_ from _o_ and then transforms it into _z_ ˜ _T_ . In essence, IB principle formalizes representation learning as a trade-off between _compression_ and _task relevance_ . Given an input observation _O_ and a latent representation _Z_ , the IB framework seeks a stochastic encoder that retains information useful for downstream robot action prediction, such as spatial and morphological features of the target object, while discarding nuisance factors such as background and lighting conditions. This is achieved by maximizing _I_ ( _Z_ ; _A_ ) ( _I_ denotes the mutual information between two variables) while minimizing _I_ ( _O_ ; _Z_ ), weighted by _λ_ IB . 

However, quantifying mutual information directly is intractable for high-dimensional inputs. Therefore, we employ a variational approximation to derive a lower bound of Objective 2 and propose the following objective: 

**Proposition 4.1** (Variational Information Bottleneck for Ac- 

4 

**DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 

tion Regression) **.** _Let Z be a latent representation produced by an encoder pθ_ ( _z|o_ ) _, and let πθ_ ( _a|z_ ) _denote a probabilistic action decoder. Then, maximizing the IB objective (2) is equivalent to minimizing the following loss term:_ 


_where 1) Tψ_ : _O × Z →_ R _denotes a neural critic, and 2) POZ and POPZ denote the joint distribution of O and Z, as well as the product of their marginals._ 

Appendix B shows the proof. In practice, we estimate the E _POZ_ [ _Tψ_ ( _o, z_ )] using paired samples in each mini-batch, and approximate sampling from the product of marginals _POPZ_ by randomly permuting _z_ within the same mini-batch (pairing _oi_ with _zπ_ ( _i_ ) for a permutation _π_ ) (Belghazi et al., 2018). For stability, we reuse the same permutation within each optimization step. 

Finally, to enable accurate action prediction, we parameterize the policy _πθ_ ( _a | z_ ) using the action head architecture from prior work (Kim et al., 2025). Given the fused latent representation _z ∈Z_ , the action head maps it to continuous control commands and outputs an action chunk of horizon _h_ for execution. Formally, the base policy is a mapping _πθ_<sup>base</sup> : _Z →A_<sup>_h_</sup> . 

Accordingly, the maximum likelihood term in objective (3) can be approximated by regressing vector fields of fixed conditional probability path. 

By combining _πθ_<sup>base</sup> ( **_a_** _| z_ ) and _pθ_ ( _z | o_ ), we obtain a shared base policy trained on offline demonstrations to acquire general multi-task competence. 

### **4.2. Online Finetuning via Mixture of RL Residuals** 

Upon learning the task-sharing representation _pθ_ ( _z | o_ ), we proceed to optimize the action prediction model _πθ_<sup>base</sup> ( **_a_** _| z_ ) using an RL optimizer. However, as discussed in Section 3, although prior RL fine-tuning methods enhance the VLA’s dexterity on individual tasks, these improvements come at the cost of distorting the learned task-sharing representation. Such distortion compromises the VLA model’s ability to scale effectively across multiple tasks. 

To address the trade-off between control dexterity and crosstask scalability, DyGRO-VLA employs a dynamic Mixtureof-RL-Residuals (MoRR) for multi-task RL optimization. 

**Learning Task Embeddings.** DyGRO-VLA learns multiple RL policies and leverages their combination to optimize task performance. A key prerequisite for this process is determining which policies should be involved to handle a given task. To this end, we develop a task embedding denoted as _z_ ˜ _T_ . Notably, unlike the latent representation 

_pθ_ ( _z | o_ ), which primarily captures decision-relevant patterns, the task embedding _z_ ˜ _T_ is designed to encode taskidentification patterns. During training, task IDs are used only as supervision to shape the embedding space, while the router is conditioned on _z_ ˜ _T_ rather than directly consuming explicit environment labels (e.g., task IDs, names, or object categories). This design encourages the task embedding to capture semantic task features and allows DyGRO-VLA to select appropriate experts from the learned routing space at inference time. 

Inspired by contrastive learning (Oord et al., 2018; Wu et al., 2025), we design the following loss function: 


where _N_ is the number of training tasks, _eζ_ = Emb( _ζ_ ) denotes the learnable task prototype associated with task ID _ζ_ , _τ_ is a temperature hyperparameter, and sim( **a** _,_ **b** ) = **a**<sup>_⊤_</sup> **b** is the similarity function. In practice, the MoE router is conditioned on the task embedding _z_ ˜ _T_ , while the task prototypes _eζ_ are only used during contrastive training to shape the embedding space and are not directly involved in routing decisions. 

**Mixture of Residuals with Dynamic Routing.** Based on the task embeddings , DyGRO-VLA utilizes a Mixture-ofExperts (MoE) module (Jacobs et al., 1991; Shazeer et al., 2017) to refine the action chunk across multiple tasks. 

Specifically, given a task embedding _z_ ˜ _T_ , a router _h_ ( _·_ ) produces gating logits over _N_ residual experts _{πi_<sup>∆</sup><sup>_}N_</sup> _i_ =1<sup>and</sup> activates only the top- _m_ of them. The corresponding gating weights are then used to combine the outputs of the selected experts as follows: 


where 1) _{ωi_ (˜ _zT_ ) _}_<sup>_m_</sup> _i_ =1<sup>arethetop</sup><sup>_m_gatingweightspre-</sup> dicted by the router and 2) ˜ **_a_** _i_ is the residual chunk predicted by the _i_ -th expert, conditioned on the latent features _z_ and the base action chunk **_a_** base (predicted the pre-trained policy _πθ_<sup>base</sup> ). This residual parameterization preserves the base policy as a strong prior while enabling specialized experts to perform targeted corrections. 

**Learning the Residual RL Policies.** Unlike prior residualpolicy methods that attach an external residual controller to a frozen base policy (Xiao et al., 2025b; Yuan et al., 2024), we integrate a residual MoE into the base architecture by conditioning each expert on the same VLM latent representation used by the base action head. This avoids introducing a separate perception encoder for the residual branch, improving compute efficiency and reducing redundant re-encoding. 

5 

**DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 

The RL loss of residual policy is formulated as: 


where 1) _πψ,θ_ denotes the augmented policy that merges the predicted action refinement ∆ **a** (Eq. (5)) with action samples from the base policy _πθ_<sup>base</sup> ( _a | z_ ) such that _∀_ **_a_** _∼ πψ,θ,_ **_a_** = ∆ **_a_** + **_a_** base ; and 2) _Qθk_ ( _st,_ **_a_** _t_ ) denotes the _k_ -th critic in a _K_ -ensemble of action-value functions, parameterized by _θk_ . The critic objective is detailed in Appendix A.2. To mitigate routing instability and prevent expert collapse in the MoE policy, we regularize the gating distribution to encourage balanced expert utilization. Let _ω_ ˆ _n ∈_ ∆<sup>_N−_1</sup> denote the predicted router distribution for the _n_<sup>_th_</sup> task embedding _z_ ˜ _T,n_ during training, and let _ω_ ˆavg = _B_ <u>1</u> � _Bn_ =1<sup>_ω_ˆ</sup><sup>_n_</sup> be the mini-batch average ( _B_ is the minibatch size). We introduce an entropy-based load-balancing regularizer as: 


where _ϵ_ is a small constant for numerical stability. The _sparse_ mixture weights _ωi_ ( _·_ ) used in Eq. (5) are obtained by selecting top- _m ω_ ˆ _i_ followed by renormalization. Minimizing _L_ LB is equivalent to maximizing the entropy of the routing probabilities, thereby preventing collapse to a single residual policy. We add _L_ LB to the policy objective. Therefore, the overall training objective of MoRR policy is: 

_Lπ_ ( _ψ_ ) = _L_ RL( _ψ_ ) + _λ_ CL _L_ CL( _ψ_ ) + _λ_ LB _L_ LB( _ψ_ ) _,_ (8) where _λ_ CL and _λ_ LB control the weights of the corresponding loss terms. 

**Difficulty-Aware Sampling.** Inspired by (Lu et al., 2025; Florensa et al., 2017; 2018), we bias task sampling toward under-solved tasks. Specifically, given the empirical success rate sr _j_ of task _ζj_ , we define _P_ ( _ζj_ ) _∝_ exp� max(0 _, target −_ sr _j_ ) _/τ_ �, which increases the sampling probability only when sr _j < target_ and saturates otherwise. This asymmetric design focuses training on partially solvable yet still challenging tasks while retaining minimal exposure to mastered tasks. 

**Practical Implementation.** In practice, we maintain two replay buffers: an offline buffer _D_ offline and an online buffer _D_ online. Following RLPD-style sampling (Ball et al., 2023), we uniformly mix offline and online transitions for each gradient update. To ensure stable initialization of online residual RL, we warm up both the critic and policy prior to online interaction, as in Cal-QL (Nakamoto et al., 2023). We further use BC regularization (Fujimoto & Gu, 2021) and an advantage-filtered actor update (Nair et al., 2020) to stabilize residual policy learning. Pseudocode are provided in Appendix D. 

## **5. Experiments** 

### **5.1. Experiments Settings.** 

**Benchmark.** 1) LIBERO (Liu et al., 2023) is a lifelong learning benchmark with five suites spanning 130 tasks. _LIBERO-Spatial_ evaluates spatial generalization by varying object placements; _LIBERO-Object_ tests object generalization by placing different objects into a box; _LIBERO-Goal_ measures diverse operations in a fixed environment; and _LIBERO-Long_ contains ten long-horizon tasks across varied scenes. 2) RoboTwin2.0 (Chen et al., 2025a) is a dual-arm manipulation benchmark designed for cross-embodiment evaluation. We select four representative tasks to assess real-world transfer performance and practical deployability. 

**Baseline.** To assess each model’s multi-task capability, we train all baseline methods on a unified training set formed by mixing data from all four suites with full shot data. To evaluate scalability and efficiency across model scales, we consider both generalist large VLA models and light-weight multi-task policies. Specifically, we include five recent large-scale VLA baselines reported in Table 1, including Octo (Team et al., 2024), OpenVLA (Kim et al., 2024), SpatialVLA (Qu et al., 2025), _π_ 0-FAST* (Pertsch et al., 2025), and _π_ 0 (Black et al., 2024). These models are finetuned from their released pretrained checkpoint when applicable. In addition, we evaluate two representative lightweight baselines, Diffusion Policy (Chi et al., 2023) and MTACT (Bharadhwaj et al., 2023). All baselines are trained under the same mixed-suite protocol for a fair comparison. To provide an initial sanity check for our approach, we also train the base DyGRO-VLA policy using supervised finetuning (SFT) under the same setting. Following common practice, we adopt LoRA (Hu et al., 2022) with rank 64 for this SFT baseline. 

### **5.2. Main Results** 

**Results Analysis.** Table 1 reports success rates under the 4-suite co-training setting, evaluated on each LIBERO suite. Overall, DyGRO-VLA achieves leading or comparable performance across all suites. Compared with the offline SFT base model, our reinforcement fine-tuning consistently improves Spatial, Object, and Goal performance, and yields a clear average gain (92.7% _→_ 97.1%). Notably, the largest improvement appears on the most challenging suite, _LIBERO-Long_ , where success increases from 85.2% to 95.0%, indicating substantially enhanced long-horizon robustness. DyGRO-VLA remains competitive with prior multi-task VLA models under the same multi-task protocol. 

**Reinforcement Fine-Tuning (RFT) Baseline Comparisons.** We evaluate DyGRO-VLA against representative RFT baselines on _LIBERO-Long_ (Table 2) to characterize post-training performance. Since most prior RFT methods 

6 

**DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 

_Table 1._ **LIBERO.** Success rate (%) on LIBERO Benchmark. **Best** results are in **bold** and **second-best** results are underlined. 

|**Method**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|
|**Multi-task SFT Models**||||||
|Diffusion Policy (From Scratch) (Chi et al.,2023)|59.6|73.8|51.6|41.0|56.5|
|MT-ACT (From Scratch) (Bharadhwaj et al.,2023)|50.2|72.0|60.2|50.2|58.2|
|Octo (Team et al.,2024)|78.7|85.5|84.2|51.0|74.9|
|OpenVLA (Kim et al.,2024)|82.1|87.3|77.4|51.8|74.7|
|SpatialVLA (Qu et al.,2025)|88.2|89.9|78.6|55.5|78.1|
|_π_0-FAST* (Pertsch et al.,2025)|96.4|96.8|88.6|60.2|85.5|
|_π_0 (Black et al.,2024)|**98.0**|96.8|94.4|88.4|94.4|
|DyGRO-VLA (SFT)|95.4|96.0|93.8|85.0|92.6|
|**Multi-task RFT Models**||||||
|DyGRO-VLA (Offline)|95.6|96.0|94.0|85.2|92.7|
|**DyGRO-VLA**|97.6|**98.6**|**97.2**|**95.0**|**97.1**|
|∆|**+2.0**|**+2.6**|**+3.2**|**+9.8**|**+4.4**|


_Table 2._ **RFT Comparisons.** Success rate (%) on LIBERO-Long. 

|**Method**|**LIBERO-Long**|
|---|---|
|TGRPO (Chen et al.,2025c)|59.2|
|GRAPE (Zhang et al.,2024)|57.2|
|VLA-RL (Lu et al.,2025)|59.8|
|World-Env (Xiao et al.,2025a)|57.8|
|RIPT-VLA (Tan et al.,2025)|93.8|
|SimpleVLA-RL (Li et al.,2025a)|91.7|
|RLinf (Zang et al.,2025)|94.0|
|**DyGRO-VLA**|**95.2**|


are tailored to single-task or single-suite training and are not readily applicable to joint co-training across all four LIBERO suites, a direct four-suite comparison would be confounded by mismatched training assumptions. We therefore adopt a suite-wise evaluation protocol and report results consistently across suites. The results show DyGRO-VLA achieves the best performance with a success rate of 95.2%. 

**Conflict Mitigation via Dynamic Grouping.** We analyze gradient conflicts using four representative tasks with contrasting interaction semantics, consisting of two _Open_ tasks and two _Close_ tasks (Open I/II, Close I/II). We quantify inter-task interference via pairwise cosine similarity of pertask gradients (Yu et al., 2020), comparing a single MLP residual head against our MoRR. As shown in Figure 5, gradients are positively aligned within the _Open_ and _Close_ pairs, but exhibit negative correlations across _Open↔Close_ , indicating strong interference under a shared MLP head. MoRR reduces these negative similarities while maintaining within-group alignment, suggesting that MoE routing with dynamic grouping effectively mitigates cross-task conflicts. 

### **5.3. Ablation Study** 

**Expert Number Ablation.** To verify whether scaling the MoRR improves multi-task performance, we vary the number of experts and report results in Table 4. Increasing 


_Figure 5._ **Gradient Conflicts.** _Figure 6._ **Online Training** Pairwise cosine similarity be- **Strategy Ablation.** Success tween per-task gradients. Red rate versus online fine-tuning indicates aligned gradients (syniterations for different strateergy) and blue indicates conflictgies. Curves are averaged over ing gradients. 3 seeds; the dashed line denotes the offline base model. 

experts consistently boosts success: a single expert already reaches 93.4 average success, 4 experts improve to 97.0 with gains across all suites, and 8 experts achieve the best overall average performance (97.1 avg.), topping _Spatial_ and _Goal_ while tying the best _Long_ result. Notably, the largest gain is on long-horizon tasks, suggesting that additional experts enable better specialization and mitigate cross-task interference. 

**Component Ablation.** To assess the impact of each component in DyGRO-VLA, we perform a component-wise ablation (Tab. 5) by removing one term at a time while keeping all other settings fixed. Removing IB leads to a consistent drop in performance (97 _._ 1 _→_ 96 _._ 8), indicating that IB provides a reliable regularization benefit. Additionally, removing the InfoNCE-based contrastive learning objective leads to a pronounced degradation across suites, most notably on Long (95 _._ 0 _→_ 90 _._ 4), reducing the overall average to 94 _._ 3, which underscores the role of discriminative task embeddings for stable routing and multi-task generalization. Disabling difficulty-aware sampling also reduces performance (97 _._ 1 _→_ 96 _._ 4). Overall, the full model performs best, and these components contribute complementary gains. 

7 

**DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 

_Table 3._ **RoboTwin2.** Success rate (%) on RoboTwin2 Benchmark. **Best** results are in **bold** and **second-best** results are underlined. 

|Method|Beat Bl|ock Hammer|Pick D|ual Bottles|Stack B|owls Two|Place E|mpty Cup|Av|g.|
|---|---|---|---|---|---|---|---|---|---|---|
||Sim|Real|Sim|Real|Sim|Real|Sim|Real|Sim|Real|
|OpenVLA-oft (SFT) (Kim et al.,2025)|54.0|15.0|32.0|25.0|88.0|70.0|50.0|60.0|56.0|42.5|
|OpenVLA-oft (RFT) (Li et al.,2025a)|71.9|**30.0**|54.0|**40.0**|**92.0**|**90.0**|96.1|60.0|78.5|55.0|
|DyGRO-VLA|**72.2**|**30.0**|**57.0**|**40.0**|90.4|**90.0**|**97.0**|**70.0**|**79.2**|**57.5**|


_Table 4._ **Expert Number Ablation.** Success rate (%) on LIBERO. 

|Method|Spatial|Object|Goal|Long|Avg.|
|---|---|---|---|---|---|
|DyGRO-VLA (1)|95.2|96.4|93.6|88.2|93.4|
|DyGRO-VLA (4)|97.4|**98.8**|96.8|95.0|97.0|
|DyGRO-VLA (8)|**97.6**|98.6|**97.2**|**95.0**|**97.1**|


_Table 5._ **Online Training Ablation.** Success rate (%) on LIBERO. 

|Method|Spatial|Object|Goal|Long|Avg.|
|---|---|---|---|---|---|
|DyGRO-VLA|**97.6**|**98.6**|**97.2**|**95.0**|**97.1**|
|w/o IB Objective|97.4|98.2|97.0|94.6|96.8|
|w/o CL Objective|95.2|97.2|94.2|90.4|94.3|
|w/o DA Sampling|97.4|98.4|97.0|93.0|96.4|


**Online Training Strategy Ablation.** To examine the effect of online fine-tuning strategies, we conduct an ablation in which all methods are initialized from the same offline base model and evaluated over 3 seeds (Fig. 6). DyGRO-VLA achieves the highest success rate and the most stable improvement. In comparison, _Standard Residual RL_ exhibits large oscillations and ends with noticeably lower performance. Freezing the VLM in _VLM (Freeze) + Action Expert_ yields stable but modest gains, indicating limited adaptation capacity. Finally, _VLM (LoRA) + Action Expert_ exhibits severe performance collapse, indicating that directly updating the backbone under large-scale multi-task online RL can substantially destabilize optimization. 

### **5.4. Real-world Experiments** 


**Real-World Settings.** We deploy our VLA model for real-world validation using a single Intel RealSense camera mounted in a head (top-down) view. DyGRO-VLA is trained in simulation and transferred to the real robot via a Sim2Real pipeline. Specifically, we follow the Sim2Real protocol of SimpleVLA-RL (Li et al., 2025a), applying domain randomization in simulation and transferring the resulting policy to the real world. We evaluate on four representative RoboTwin tasks: _Beat Block Hammer_ , _Pick Dual Bottles_ , _Stack Bowls Two_ , and _Place Empty Cup_ . We compare against OpenVLA-OFT (SFT) (Kim et al., 2025) and an RFT variant of OpenVLA-OFT trained with SimpleVLARL. All real-world evaluations use 20 trials per task, while simulation results follow the RoboTwin2 benchmark evaluation protocol. 

**Results Analysis.** Our experiment results in Table 3 show that DyGRO-VLA achieves the best overall performance in simulation (79.2%) and matches or surpasses RFT baselines under Sim2Real transfer. In particular, DyGRO-VLA improves real-world success on _Pick Dual Bottles_ and _Place Empty Cup_ , while remaining competitive on _Stack Bowls Two_ . These results validate the practical applicability of our method for deploying simulation-trained VLA policies in real-world settings. 

### **5.5. Limitation** 

DyGRO-VLA has three main limitations: 1) _Online training sensitivity_ : The online stage requires environment interaction and is sensitive to reward sparsity and hyperparameter tuning, which limits stability and sample efficiency. _2) Task dependency in routing_ : The routing mechanism relies on task embeddings trained with known task identities, reducing effectiveness in settings with ambiguous or unlabeled task boundaries. _3) Limited real-world evaluation_ : Current validation covers only a few tasks and a specific Sim2Real setup; broader testing across diverse tasks, embodiments, and sensing conditions is needed to assess generalization. 

## **6. Conclusion** 

We investigate the scalability challenge of RL post-training for vision–language–action models, where multi-task online optimization can induce cross-task interference and catastrophic forgetting. To address this, we propose DyGROVLA, a two-stage framework that learns task-sharing representations from offline demonstrations and refines be- 

_Figure 7._ Real-world Platform for robotic manipulation. 

8 

**DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 

havior online via dynamically routed residual RL experts. Across LIBERO, RoboTwin2, and real-world Sim2Real experiments, DyGRO-VLA improves multi-task performance and robustness over strong baselines, with notable gains on challenging tasks. These results highlight the value of preserving shared representations and using dynamic residual modularization for scalable VLA post-training. An important direction of future work is extending DyGRO-VLA to mobile manipulation tasks that involve locomotion tasks before manipulating objects. 

## **Impact Statement** 

This work aims to advance the field of machine learning and robotics by improving the efficiency and generalization of VLA models through Dynamic Grouped Residual Optimization (DyGRO). The proposed method could accelerate progress toward generalist robotic systems capable of performing a wider range of real-world tasks with greater adaptability and data efficiency. 

Potential positive societal impacts include improved accessibility to automation, safer human-robot collaboration, and reduced data collection costs for robotic training. However, as with all advances in general-purpose AI and robotics, there are ethical considerations related to the potential misuse of autonomous systems, labor displacement in automation-sensitive industries, and biases originating from training data. We encourage future research to address these issues through transparent data practices, fairness-aware policy learning, and human-centered deployment standards. 

## **Acknowledgments** 

This work is supported in part by Shenzhen Science and Technology Program under grant KJZD20240903104008012, Shenzhen Science and Technology Program under grant ZDCY20250901113000001, CUHK-CUHK(SZ)-GDSTC Joint Collaboration Fund No. 2025A0505000053, and GuangDong Key Laboratory of Big Data Computing (2021B1212040002). 

## **References** 

- Ball, P. J., Smith, L., Kostrikov, I., and Levine, S. Efficient online reinforcement learning with offline data. In _International Conference on Machine Learning_ , pp. 1577–1594. PMLR, 2023. 

- Belghazi, M. I., Baratin, A., Rajeshwar, S., Ozair, S., Bengio, Y., Courville, A., and Hjelm, D. Mutual information neural estimation. In _International conference on machine learning_ , pp. 531–540. PMLR, 2018. 

- Bharadhwaj, H., Vakil, J., Sharma, M., Gupta, A., Tulsiani, 

S., and Kumar, V. Roboagent: Towards sample efficient robot manipulation with semantic augmentations and action chunking. _arxiv_ , 2023. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. pi0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Bohn, C., Freeman, I., Tercan, H., and Meisen, T. Task weighting through gradient projection for multitask learning. In _International Conference on Neural Information Processing_ , pp. 317–331. Springer, 2024. 

- Chen, T., Chen, Z., Chen, B., Cai, Z., Liu, Y., Li, Z., Liang, Q., Lin, X., Ge, Y., Gu, Z., et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025a. 

- Chen, Y., Tian, S., Liu, S., Zhou, Y., Li, H., and Zhao, D. Conrft: A reinforced fine-tuning method for vla models via consistency policy. _arXiv preprint arXiv:2502.05450_ , 2025b. 

- Chen, Z., Ngiam, J., Huang, Y., Luong, T., Kretzschmar, H., Chai, Y., and Anguelov, D. Just pick a sign: Optimizing deep multitask models with gradient sign dropout. _Advances in Neural Information Processing Systems_ , 33: 2039–2050, 2020. 

- Chen, Z., Niu, R., Kong, H., Wang, Q., Xing, Q., and Fan, Z. Tgrpo: Fine-tuning vision-language-action model via trajectory-wise group relative policy optimization. _arXiv preprint arXiv:2506.08440_ , 2025c. 

- Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., and Song, S. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , pp. 02783649241273668, 2023. 

- Florensa, C., Held, D., Wulfmeier, M., Zhang, M., and Abbeel, P. Reverse curriculum generation for reinforcement learning. In _Conference on robot learning_ , pp. 482– 495. PMLR, 2017. 

- Florensa, C., Held, D., Geng, X., and Abbeel, P. Automatic goal generation for reinforcement learning agents. In _International conference on machine learning_ , pp. 1515– 1528. PMLR, 2018. 

- Fu, Y., Zhang, Z., Zhang, Y., Wang, Z., Huang, Z., and Luo, Y. Mergevla: Cross-skill model merging toward a generalist vision-language-action agent. _arXiv preprint arXiv:2511.18810_ , 2025. 

9 

**DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 

- Fujimoto, S. and Gu, S. S. A minimalist approach to offline reinforcement learning. _Advances in neural information processing systems_ , 34:20132–20145, 2021. 

- Guo, Y., Zhang, J., Chen, X., Ji, X., Wang, Y.-J., Hu, Y., and Chen, J. Improving vision-language-action model with online reinforcement learning. _arXiv preprint arXiv:2501.16664_ , 2025. 

- Haarnoja, T., Zhou, A., Abbeel, P., and Levine, S. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In _International conference on machine learning_ , pp. 1861–1870. Pmlr, 2018. 

- Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen, W., et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. 

- Huang, D., Fang, Z., Zhang, T., Li, Y., Zhao, L., and Xia, C. Co-rft: Efficient fine-tuning of vision-language-action models through chunked offline reinforcement learning. _arXiv preprint arXiv:2508.02219_ , 2025. 

- Huang, S., Zhang, Z., Liang, T., Xu, Y., Kou, Z., Lu, C., Xu, G., Xue, Z., and Xu, H. Mentor: Mixture-of-experts network with task-oriented perturbation for visual reinforcement learning. _arXiv preprint arXiv:2410.14972_ , 2024. 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- Jacobs, R. A., Jordan, M. I., Nowlan, S. J., and Hinton, G. E. Adaptive mixtures of local experts. _Neural computation_ , 3(1):79–87, 1991. 

- Johannink, T., Bahl, S., Nair, A., Luo, J., Kumar, A., Loskyll, M., Ojea, J. A., Solowjow, E., and Levine, S. Residual reinforcement learning for robot control. In _2019 international conference on robotics and automation (ICRA)_ , pp. 6023–6029. IEEE, 2019. 

- Kawaharazuka, K., Oh, J., Yamada, J., Posner, I., and Zhu, Y. Vision-language-action models for robotics: A review towards real-world applications. _IEEE Access_ , 2025. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- Kong, Y., Ma, G., Zhao, Q., Wang, H., Shen, L., Wang, X., and Tao, D. Mastering massive multi-task reinforcement learning via mixture-of-expert decision transformer. _arXiv preprint arXiv:2505.24378_ , 2025. 

- Kroemer, O., Niekum, S., and Konidaris, G. A review of robot learning for manipulation: Challenges, representations, and algorithms. _Journal of machine learning research_ , 22(30):1–82, 2021. 

- Li, H., Zuo, Y., Yu, J., Zhang, Y., Yang, Z., Zhang, K., Zhu, X., Zhang, Y., Chen, T., Cui, G., et al. Simplevla-rl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ , 2025a. 

- Li, Q., Zhou, Z., and Levine, S. Reinforcement learning with action chunking. _arXiv preprint arXiv:2507.07969_ , 2025b. 

- Liu, B., Liu, X., Jin, X., Stone, P., and Liu, Q. Conflictaverse gradient descent for multi-task learning. _Advances in Neural Information Processing Systems_ , 34:18878– 18890, 2021. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- Liu, J., Gao, F., Wei, B., Chen, X., Liao, Q., Wu, Y., Yu, C., and Wang, Y. What can rl bring to vla generalization? an empirical study. _arXiv preprint arXiv:2505.19789_ , 2025. 

- Lu, G., Guo, W., Zhang, C., Zhou, Y., Jiang, H., Gao, Z., Tang, Y., and Wang, Z. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning. _arXiv preprint arXiv:2505.18719_ , 2025. 

- Luo, J., Hu, Z., Xu, C., Tan, Y. L., Berg, J., Sharma, A., Schaal, S., Finn, C., Gupta, A., and Levine, S. Serl: A software suite for sample-efficient robotic reinforcement learning. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 16961–16969. IEEE, 2024. 

- Luo, J., Xu, C., Wu, J., and Levine, S. Precise and dexterous robotic manipulation via human-in-the-loop reinforcement learning. _Science Robotics_ , 10(105):eads5033, 2025. 

- Ma, Y., Song, Z., Zhuang, Y., Hao, J., and King, I. A survey on vision-language-action models for embodied ai. _arXiv preprint arXiv:2405.14093_ , 2024. 

- Nair, A., Gupta, A., Dalal, M., and Levine, S. Awac: Accelerating online reinforcement learning with offline datasets. _arXiv preprint arXiv:2006.09359_ , 2020. 

10 

**DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 

- Nakamoto, M., Zhai, S., Singh, A., Sobol Mark, M., Ma, Y., Finn, C., Kumar, A., and Levine, S. Cal-ql: Calibrated offline rl pre-training for efficient online fine-tuning. _Advances in Neural Information Processing Systems_ , 36: 62244–62269, 2023. 

- Oord, A. v. d., Li, Y., and Vinyals, O. Representation learning with contrastive predictive coding. _arXiv preprint arXiv:1807.03748_ , 2018. 

- Oquab, M., Darcet, T., Moutakanni, T., Vo, H., Szafraniec, M., Khalidov, V., Fernandez, P., Haziza, D., Massa, F., ElNouby, A., et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2024. 

- Parisotto, E., Ba, J. L., and Salakhutdinov, R. Actor-mimic: Deep multitask and transfer reinforcement learning. _arXiv preprint arXiv:1511.06342_ , 2015. 

- Peng, X., Chang, C., Wang, F.-Y., and Li, L. Robust multitask learning with sample gradient similarity. _IEEE Transactions on Systems, Man, and Cybernetics: Systems_ , 54(1):497–506, 2023. 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., and Levine, S. Fast: Efficient action tokenization for vision-language-action models. In _Robotics: Science and Systems (RSS)_ , 2025. 

- Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., Wang, Z., Gu, J., Zhao, B., Wang, D., and Li, X. Spatialvla: Exploring spatial representations for visual-language-action model. In _Robotics: Science and Systems (RSS)_ , 2025. 

- Sener, O. and Koltun, V. Multi-task learning as multiobjective optimization. _Advances in neural information processing systems_ , 31, 2018. 

- Shazeer, N., Mirhoseini, A., Maziarz, K., Davis, A., Le, Q., Hinton, G., and Dean, J. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. _arXiv preprint arXiv:1701.06538_ , 2017. 

- Shi, L. X., Ichter, B., Equi, M., Ke, L., Pertsch, K., Vuong, Q., Tanner, J., Walling, A., Wang, H., Fusai, N., et al. Hi robot: Open-ended instruction following with hierarchical vision-language-action models. _arXiv preprint arXiv:2502.19417_ , 2025. 

- Tan, S., Dou, K., Zhao, Y., and Krahenb¨ uhl, P.¨ Interactive post-training for vision-language-action models. _arXiv preprint arXiv:2505.17016_ , 2025. 

- Team, O. M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- Team, Q. Qwen2 technical report. _arXiv preprint arXiv:2407.10671_ , 2, 2024. 

- Tishby, N., Pereira, F. C., and Bialek, W. The information bottleneck method. _arXiv preprint physics/0004057_ , 1999. 

- Wang, Y., Ding, P., Li, L., Cui, C., Ge, Z., Tong, X., Song, W., Zhao, H., Zhao, W., Hou, P., et al. Vla-adapter: An effective paradigm for tiny-scale vision-language-action model. _arXiv preprint arXiv:2509.09372_ , 2025. 

- Wang, Z., Tsvetkov, Y., Firat, O., and Cao, Y. Gradient vaccine: Investigating and improving multi-task optimization in massively multilingual models. _arXiv preprint arXiv:2010.05874_ , 2020. 

- Wu, W., Liu, F., Li, H., Hu, Z., Dong, D., Chen, C., and Wang, Z. Mixture-of-experts meets in-context reinforcement learning. _arXiv preprint arXiv:2506.05426_ , 2025. 

- Xiao, J., Yang, Y., Chang, X., Chen, R., Xiong, F., Xu, M., Zheng, W.-S., and Zhang, Q. World-env: Leveraging world model as a virtual environment for vla post-training. _arXiv preprint arXiv:2509.24948_ , 2025a. 

- Xiao, W., Lin, H., Peng, A., Xue, H., He, T., Xie, Y., Hu, F., Wu, J., Luo, Z., Fan, L., et al. Self-improving visionlanguage-action models with data generation via residual rl. _arXiv preprint arXiv:2511.00091_ , 2025b. 

- Xing, Y., Luo, X., Xie, J., Gao, L., Shen, H. T., and Song, J. Shortcut learning in generalist robot policies: The role of dataset diversity and fragmentation. In _Conference on Robot Learning, CoRL_ , pp. 3239–3266, 2025. 

- Yang, L., Shen, D., Cai, C., Yang, F., Gao, T., Zhang, D., and Li, X. Solving token gradient conflict in mixture-ofexperts for large vision-language model. _arXiv preprint arXiv:2406.19905_ , 2024. 

- Yang, R., Xu, H., Wu, Y., and Wang, X. Multi-task reinforcement learning with soft modularization. _Advances in Neural Information Processing Systems_ , 33:4767–4777, 2020. 

- Yu, T., Kumar, S., Gupta, A., Levine, S., Hausman, K., and Finn, C. Gradient surgery for multi-task learning. _Advances in neural information processing systems_ , 33: 5824–5836, 2020. 

- Yuan, X., Mu, T., Tao, S., Fang, Y., Zhang, M., and Su, H. Policy decorator: Model-agnostic online refinement for large policy model. _arXiv preprint arXiv:2412.13630_ , 2024. 

- Zang, H., Wei, M., Xu, S., Wu, Y., Guo, Z., Wang, Y., Lin, H., Shi, L., Xie, Y., Xu, Z., et al. Rlinf-vla: A unified and 

11 

**DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 

efficient framework for vla+ rl training. _arXiv preprint arXiv:2510.06710_ , 2025. 

- Zhai, X., Mustafa, B., Kolesnikov, A., and Beyer, L. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 11975–11986, 2023. 

- Zhang, Z., Zheng, K., Chen, Z., Jang, J., Li, Y., Han, S., Wang, C., Ding, M., Fox, D., and Yao, H. Grape: Generalizing robot policy via preference alignment. _arXiv preprint arXiv:2411.19309_ , 2024. 

- Zhao, T. Z., Kumar, V., Levine, S., and Finn, C. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

12 

**DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 

## **A. DyGRO-VLA** 

### **A.1. Fusion Module** 

Following prior work (Wang et al., 2025; Fu et al., 2025), each Fusion layer performs multi-head attention with the action query _qt_<sup>_a_and keys/values from three sources:(1)</sup><sup>_q_</sup> _t_<sup>_a_itself, (2) the concatenation of the action hidden state</sup><sup>_h_act</sup> _t_ and proprioceptive tokens _h_<sup>pro</sup> _t_ = Enc( _pt_ ), and (3) the conditioning representation _h_<sup>cond</sup> _t_ . A learnable scalar gate dynamically reweights the contribution of the conditioning branch, allowing the model to adaptively integrate task-relevant contextual information. 

### **A.2. Residual RL** 

**Residual MoE.** We parameterize the action distribution with an std model that predicts the standard deviation _σθ_ , while the Residual MoE provides the mean _µθ_ . This formulation defines a factorized Gaussian policy _πθ_ ( **a** _| s_ ) = _N_ ( _µθ_ ( _s_ ) _,_ diag( _σθ_<sup>2(</sup><sup>_s_))), which enables stochastic actions during RL exploration and optimization.</sup> 

**Residual Action Space.** When refining the base policy with a residual policy, we aim to keep the trajectory close to the original to avoid failure, which means the residual policy should make subtle adjustments. To control this, we bound the output within a specific range. We use the tanh function and mapping the residual action with a hyperparameter _α_ , ensuring it stays within ( _−α, α_ ). 

**Offline-to-Online Critic Objective.** Our critic for residual RL is a lightweight ResMLP with attention pooling. Following Cal-QL (Nakamoto et al., 2023), we maintain an ensemble of _K_ critics _{Qθi}_<sup>_K_</sup> _i_ =1<sup>and optimize them with an</sup><sup>_h_-step Bellman</sup> regression term together with a Cal-QL calibration regularizer: 


**Target ensemble and conservative aggregation.** For stable target estimation, we maintain a slowly-updated target ensemble _{Q_<sup>¯</sup> _θ_ ¯ _j }j_<sup>_K_</sup> =1<sup>and define the aggregated target critic as</sup> 


which yields the backup operator _B_<sup>_π_</sup> _Q_<sup>¯</sup> min. 

_h_ **-step (chunk) Bellman regression.** Each critic is trained by regressing to the shared target: 


The corresponding _h_ -step Bellman backup is 


where the _h_ -step return is 


**Cal-QL calibration regularizer.** To enable a smooth transition from offline data to online rollouts, we apply the Cal-QL calibration regularizer to each ensemble member, encouraging high value on policy actions while remaining anchored to dataset actions: 


Here **a** _t_ = _at_ : _t_ + _h−_ 1 denotes an action chunk and _π_ ( **a** _| s_ ) is the chunk-level policy. We approximate _V_<sup>_µ_</sup> ( _st_ ) using Monte Carlo returns from the offline dataset. 

13 

**DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 

## **B. Proof** 

**Proposition B.1** (Variational Information Bottleneck for Action Regression) **.** _Let Z be a latent representation produced by an encoder pθ_ ( _z|o_ ) _, and let πθ_ ( _a|z_ ) _denote a probabilistic action decoder. Then, maximizing the IB objective (2) is equivalent to:_ 


_where 1) Tψ_ : _O × Z →_ R _denotes a neural critic, and 2) POZ and POPZ denote the joint distribution of O and Z, as well as the product of their marginals._ 

_Proof._ Starting from the Information Bottleneck functional: 


- (1) holds because maximizing _I_ ( _Z_ ; _A_ ) _− βI_ ( _Z_ ; _O_ ) is equivalent to minimizing its negative. 

- (2) holds by substituting the definitions _I_ ( _Z_ ; _A_ ) = E[log _p_ ( _a|z_ )] _−_ E[log _p_ ( _a_ )] and _I_ ( _Z_ ; _O_ ) = _D_ KL( _POZ∥POPZ_ ), where the constant E[log _p_ ( _a_ )] is omitted since it is independent of _θ_ . 

- (3) holds by applying the Donsker–Varadhan (DV) representation of the KL divergence: 


This introduces the variational critic function _Tψ_ ( _o, z_ ). 

- (4) holds by absorbing the supremum into optimization over _ψ_ for notation consistency. The additive constant C encompasses all parameter-independent terms. 

- (5) holds by defining _I_ DV( _O_ ; _Z_ ) as the Donsker–Varadhan estimate of mutual information. Thus, the resulting loss corresponds to the trainable Information Bottleneck formulation: 


14 

**DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 


_Figure 8._ **Sim-to-real qualitative demonstrations of DyGRO-VLA on RoboTwin2.0.** The policy is trained in simulation and directly deployed in the real world. We show four real-world tasks: Beat Block Hammer, Pick Dual Bottles, Stack Bowls Two, and Place Empty Cup. 

## **C. Real-World Details** 

**Real-World Setups.** We deploy the training checkpoint zero-shot on the real robot without any real-world fine-tuning. We evaluate DyGRO-VLA on four real-world tasks from RoboTwin2.0: Beat Block Hammer, Pick Dual Bottles, Stack Bowls Two, and Place Empty Cup. These tasks cover diverse manipulation skills, including contact-rich tool-use, multi-object grasping, object stacking, and goal-conditioned placement. Beat Block Hammer requires accurate tool-object interaction, Pick Dual Bottles evaluates the ability to grasp multiple objects, Stack Bowls Two tests spatial alignment and stable placement, and Place Empty Cup examines pick-and-place generalization in real-world scenes. 

**Real-World Visualization.** As shown in Figure 8, our proposed multi-task training framework achieves effective zero-shot sim-to-real transfer. After being trained only in simulation, DyGRO-VLA can be directly deployed on the real robot without additional real-world data or fine-tuning. The qualitative results demonstrate that the learned multi-task policy generalizes to diverse real-world manipulation scenarios, including tool-use, dual-object picking, stacking, and object placement. 

## **D. Pseudocode** 

The pseudocode of DyGRO-VLA is provided in Algorithm 1. 

15 

**DyGRO-VLA: Cross-Task Scaling of Vision–Language–Action Models via Dynamic Grouped Residual Optimization** 

|**Algo**|**rithm 1 DyGRO-VLA:**IB Pretraining+ Online MoRR||
|---|---|---|
|**Req**<br>|**uire:** _D_demo_, E, T_; _h, N_on_, U_; _η_off_, ηπ, ηQ_; _λ_IB_, λ_CL_, λ_LB; _θ, ν, ϕ, ψ_<br>||
|**Ensu**|**re:** Executed chunk_at_ =_a_<sup>base</sup><br>_t_<br>+ ∆_at_||
|1: I|nitialize online replay buffer_D_on _←∅_||
|2: **S  l**|**tage I: Offline pretraining**||
|3: **f**|**or**_i_= 1**to**_N_off **do**||
|4:|Sample(_o, l, p, a_<sup>_⋆_</sup>)_∼D_demo||
|5:|Sample latent_z ∼pθ_(_z | o, l, p_)||
|6:|Predict base chunk_a_<sup>base</sup> _←π_<sup>base</sup><br>_θ_<br>(_· | z_)||
|7:|<br>_L_IB _←_DV-IB(_o, z_;_ν_)|// variational IB term|
|8:|_L_base _←L_BC(_a_<sup>base</sup>_, a_<sup>_⋆_</sup>) +_λ_IB_L_IB<br>||
|9:|(_θ, ν_)_←_(_θ, ν_)_−η_off_∇_(_θ,ν_)_L_base||
|10: **e**|**nd for**||
|11: F|reeze_θ_|// preserve task-sharing representation|
|12: **S   i**|**tage II: Online finetuning**||
|13: **f**|**or**_k_ = 1**to**_N_on**do**||
|14:|Reset_E_ and sample task identity_ζ ∼T_||
|15:|**Rollout**||
|16:|**while not done do**||
|17:|Observe(_ot, lt, pt_)||
|18:|(_zt,_˜_z_<sup>_T_</sup><br>_t_ <sup>)</sup><sup>_←_Enc</sup><sup>_θ_(</sup><sup>_ot, lt, pt_)</sup>|// latent + task embedding|
|19:|_a_<sup>base</sup><br>_t_<br>_←π_<sup>base</sup><br>_θ_<br>(_· | zt_)<br>||
|20:|_ωt ←_Top-_m_Softmax(Router_ϕ_(˜_z_<sup>_T_</sup><br>_t_ <sup>))</sup>||
|21:|**for**each expert_i_in top-_m_(_ωt_)**do**<br><br>||
|22:|Sample residual chunk˜_at,i ∼π_<sup>∆</sup><br>_i,ϕ_<sup>(</sup><sup>_· | zt, a_base</sup><br>_t_<br>)||
|23:|**end for**||
|24:|∆_at ←_<sup>�</sup><br>_i∈_top-_m_(_ωt_) <sup>_ωt,i_ ˜</sup><sup>_at,i_</sup><br>||
|25:|Execute chunk_at_ =_a_<sup>base</sup><br>_t_<br>+ ∆_at_for_h_steps, receive(_r_<sup>(</sup><sup>_h_)</sup><br>_t_<br>_, ot_+_h,_done)<br>||
|26:|(_zt_+_h,_˜_z_<sup>_T_</sup><br>_t_+_h_<sup>)</sup><sup>_←_Enc</sup><sup>_θ_(</sup><sup>_ot_+</sup><sup>_h, lt_+</sup><sup>_h, pt_+</sup><sup>_h_)</sup><br>||
|27:|Store(_zt,_˜_z_<sup>_T_</sup><br>_t _<sup>_, ζ, ωt,_ ∆</sup><sup>_at, r_(</sup><sup>_h_)</sup><br>_t_<br>_, zt_+_h,_done)into_D_on||
|28:|**end while**||
|29:|**Updates**||
|30:|**for**_u_= 1**to**_U_ **do**||
|31:|Sample minibatch_M ∼D_on||
|32:|_LQ ←L_TD_/_Cal-QL(_M_;_ψ, θ, ϕ_)||
|33:|_ψ ←ψ −ηQ ∇ψLQ_||
|34:|_L_RL _←L_actor(_M_;_ψ, θ, ϕ_)|// SAC-style on augmented policy|
|35:|_L_CL _←L_InfoNCE(_M_;_ϕ_)|// shape ˜_z_<sup>_T_</sup>|
|36:|<br>_L_LB _←L_load-balance(_M_;_ϕ_)<br><br>|<br>// prevent expert collapse|
|37:|_ϕ ←ϕ −ηπ ∇ϕ_<br>�<br>_L_RL+_λ_CL_L_CL+_λ_LB_L_LB<br>�||
|38:|**end for**||
|39: **e**|**nd for**||
|40: **r**|**eturn**_π_(_at | ot, lt, pt_) =_π_<sup>base</sup><br>_θ_<br>(_· | zt_) + ∆_at_||


16 

