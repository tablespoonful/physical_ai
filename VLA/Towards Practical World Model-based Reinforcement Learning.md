---
title: "Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models"
date: "2026-03-21"
authors: "Zhilong Zhang; Haoxiang Ren; Yihao Sun; Yifei Sheng; Haonan Wang; Haoxin Lin"
venue: "ICML 2026"
url: https://arxiv.org/abs/2603.20607
pdf: https://arxiv.org/pdf/2603.20607
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.20607)** / [論文ページ](https://arxiv.org/abs/2603.20607)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

**Zhilong Zhang**<sup>1 2 *</sup> **Haoxiang Ren**<sup>2 *</sup> **Yihao Sun**<sup>3 4 *</sup> **Yifei Sheng**<sup>1 2</sup> **Haonan Wang**<sup>1 2</sup> **Zhichao Wu**<sup>1 2</sup> **Haoxin Lin**<sup>1 2</sup> **Pierre-Luc Bacon**<sup>3 4</sup> **Yang Yu**<sup>1 2</sup><sup>_†_</sup> 

# **Abstract** 

Well-pretrained Vision-Language-Action (VLA) models show strong generalization for robotic control, but finetuning them with reinforcement learning (RL) is constrained by the high cost and safety risks of real-world interaction. Training VLA models in interactive world models avoids these issues but introduces several challenges, including pixel-level world modeling, multi-view consistency, and compounding errors under sparse rewards. Building on recent advances across large multimodal models and model-based RL, we propose VLA-MBPO, a practical framework to tackle these problems in VLA finetuning. Our approach has three key design choices: (i) adapting unified multimodal models (UMMs) for data-efficient world modeling; (ii) an interleaved view decoding mechanism to enforce multi-view consistency; and (iii) chunk-level branched rollout to mitigate error compounding. Theoretical analysis and experiments across simulation and real-world tasks demonstrate that VLA-MBPO significantly improves policy performance and sample efficiency, underscoring its robustness and scalability for real-world robotic deployment. 

# **1. Introduction** 

The emergence of Vision-Language-Action (VLA) models represents a significant advancement in robotic control, primarily attributable to their enhanced generalization capabilities (Kim et al., 2024; Intelligence et al., 2025b). By integrating the expansive world knowledge and reasoning 

*Equal contribution 1National Key Laboratory for Novel Software Technology, Nanjing University, Nanjing, China<sup>2</sup> School of Artificial Intelligence, Nanjing University, Nanjing, China<sup>3</sup> Mila - Quebec AI Institute<sup>4</sup> Universite de Montr´ eal.´ Correspondence to: Yang Yu _<_ yuy@nju.edu.cn _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

ability of Vision-Language Models (VLM) with extensive pretraining on vast robotics datasets, VLA models can effectively learn and execute a diverse range of tasks across varied robotic embodiments (Deng et al., 2025b; Intelligence et al., 2025b; Bjorck et al., 2025). 

Previously, finetuning VLA models typically relies on imitation learning (IL), particularly Behavior Cloning (BC), where the model learns a policy by minimizing the discrepancy between the model and expert actions (Ghosh et al., 2024; Kim et al., 2024; 2025; Intelligence et al., 2025b). However, it is well-known that BC is constrained by the limited generalizability and the high cost of collecting large amounts of expert demonstrations (Xu et al., 2020; Rajaraman et al., 2020; Xu et al., 2024). Meanwhile, reinforcement learning (RL) is the standard approach that learns from environmental interactions, thereby achieving stronger generalization with fewer demonstrations (Chen et al., 2025b; Liu et al., 2025; Zang et al., 2025; Li et al., 2025b). However, applying RL in real-world settings remains challenging, as it typically requires numerous interactions with the environment, making it prohibitively expensive, potentially unsafe, and hard to scale (Zhang et al., 2025; Xiao et al., 2025; Zhang et al., 2026). 

To enable RL training for VLAs while addressing its limitations in real-world settings, a promising approach is to use world models as simulated environments. This allows agents to learn entirely in imagined spaces, avoiding the high costs and safety risks associated with real-world interaction. Only a few prior studies (Zhang et al., 2024; Zhu et al., 2025) and technical reports (Li et al., 2025a; Fei et al., 2025) have explored this direction, however, applying world models to VLA training still presents several fundamental challenges. First, VLAs rely on visual inputs, requiring world models to generate pixel-level future frames and reward signals that generalize well from limited offline data. While some methods finetune pretrained video models as world models, these models suffer from low inference efficiency and cannot directly predict reward signals (Xiao et al., 2025; Zhu et al., 2025). Second, many robotic tasks, especially fine-grained manipulation, rely on multi-view visual inputs, which demand consistent and coherent pre- 

1 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 


_Figure 1._ The framework illustration of VLA-MBPO, comprising (A) a UMM-based world model with interleaved view decoding for multi-view observation and reward prediction, and (B) a stable and scalable policy update algorithm with chunked-level branch rollout. (C) illustration of both simulated and real-world task designs in our work. 

dictions across views (Guo et al., 2025; Qian et al., 2025). Furthermore, model-based learning is inherently susceptible to compounding model errors (Janner et al., 2019; Yu et al., 2020; Xu et al., 2020), and this issue is significantly amplified in VLA settings due to sparse reward signals, where small modeling inaccuracies can lead to opposite reward outcomes and severely misguide policy learning. Together, these challenges make it nontrivial to directly apply existing model-based RL methods to VLA finetuning. 

In this work, we propose a practical world model-based RL framework that explicitly addresses these challenges. To enable sample-efficient and generalizable pixel-space world modeling, we use a _pretrained unified multimodal model (UMM)_ as the backbone of our world model (Deng et al., 2025a; Cui et al., 2025; Sun et al., 2025), allowing joint prediction of visual dynamics and rewards without expensive video rollouts. To support consistent multi-view generation required for precise control, we introduce the _interleaved view decoding_ technique that enforces cross-view consistency while preserving view-specific details. Finally, to mitigate compounding model errors under sparse rewards, we employ _chunk-level branched rollout_ that limits error accumulation for policy optimization (Park et al., 2025). Together, these components form a cohesive world modelbased RL approach tailored for VLA finetuning (VLAMBPO), enabling effective reinforcement learning with limited real-world interactions, as illustrated in Figure 1. 

To validate VLA-MBPO, we provide a theoretical analysis of the reduced value gap alongside experiments in simulated and real-world tasks. Overall, our results demonstrate that VLA-MBPO substantially improves policy generalization 

and data efficiency. Crucially, our approach yields this good performance using a universal set of hyperparameters, paving the way for more reliable and scalable deployment of VLA models in real-world robotic applications. 

# **2. Preliminaries** 

**Language-Conditioned Markov Decision Process.** We formulate the language-conditioned robot control task as an infinite-horizon Language-conditioned Markov Decision Process (L-MDP) _M_ = ( _S, A, L, T, r, γ_ ) (Puterman, 1990; 2014). The state space _S_ consists of visual observations, and _L_ denotes the set of language instructions. The action space _A_ consists of low-level control commands (e.g., joint positions or end-effector poses). The transition function _T_ : _S × A →_ ∆( _S_ ) specifies the distribution over the next state given the current state and the executed action. The reward function _r_ : _S ×L →{_ 0 _,_ 1 _}_ assigns a binary reward based on the visual observation and the task instruction. The objective of L-MDP is to learn a language-conditioned policy _π_ ( _at|st, l_ ) that maximizes the expected discounted return _V_ ( _π_ ) = E _π_ [<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γtr_(</sup><sup>_st, l_)] under any task instruc-</sup> tion. Recently, most VLAs employ action chunking technique (Fu et al., 2024), where the policy outputs a sequence of _k_ consecutive actions ˜ _at_ = ( _at, at_ +1 _, · · · , at_ + _k−_ 1). 

**Proximal Policy Optimization.** We optimize the policy _πθ_ using Proximal Policy Optimization (PPO) (Schulman et al., 2017). PPO aims to maximize a clipped surrogate objective _L_ ( _θ_ ) to constrain policy updates and limit the divergence between _πθ_ and the behavior policy _πθ_ old that collected the 

2 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

data. This objective function is computed by: 


where _ρt_ ( _θ_ ) = _ππθθ_ old( _a_ ( _at|ts|st,tl,l_ <u>))</u><sup>is the likelihood ratio.To esti-</sup> 

mate the advantage _A_<sup>ˆ</sup> _t_ , PPO employ Generalized Advantage Estimation (GAE) (Schulman et al., 2015): 


Here _Vϕ_ ( _s, l_ ) is the language-conditioned value function parameterized by _ϕ_ , _γ_ is the discount factor, and _λ_ controls the bias–variance trade-off in the advantage estimation. 

# **3. Addressing Practical Challenges in World Model-based RL for VLAs** 

Applying model-based reinforcement learning (MBRL) for VLA models poses several challenges that arise from pixellevel modeling, multi-view generation, and compounding errors under sparse rewards. We organize this section around these challenges and describe how each design choice addresses a specific problem. We first focus on challenges in dynamics and reward modeling in the VLA domain (Section 3.1), and then tackle compounding errors exacerbated by sparse rewards during policy learning (Section 3.2). Together, these components form a cohesive and practical world model-based RL framework for VLA (Section 3.3). 

## **3.1. Challenges in World Modeling for VLAs** 


_Figure 2._ Frame-skipping scheme in UMM-based World Model. 

Unlike conventional MBRL settings that rely on lowdimensional states or latent rollouts (Janner et al., 2019; Hafner et al., 2023; Hansen et al., 2024), world models for VLAs require (i) high-fidelity pixel-based generation since VLAs typically take origin images as inputs for visual perception, (ii) consistent multi-view generation for finegrained control, and (iii) accurate semantic understanding ability for reward modeling. However, training such pixelspace world models from scratch is notoriously data-hungry and prone to overfitting in offline settings. 

Prior work typically finetunes separate large video models and vision–language models for dynamics and reward modeling, respectively (Zhu et al., 2025). While effective, this two-model design introduces complexity and engineering overhead. In contrast, inspired by recent advances (Deng et al., 2025a; Sun et al., 2025), we adopt unified multimodal models (UMMs) as a streamlined alternative, enabling joint prediction of future observations and rewards within a single model. Moreover, by directly modeling dynamics without generating intermediate frames, UMMs improve rollout efficiency compared to video world models (Figure 2). However, since UMMs are not originally tailored for VLA settings, additional adaptations are required. 

**Extending UMMs to Action Spaces.** UMM-based world models typically operate over vision and language modalities (Sun et al., 2025), whereas VLA agents introduce an additional low-level action modality. To support UMMs in handling low-level action inputs, we follow Goyal et al. (2025) to represent actions as integer tokens by discretizing continuous action values into a fixed range (e.g., [0,256]) and mapping them to the UMM vocabulary. The UMM is then tasked with generating the next observation and reward based on the text-based action chunks. This process is formalized by the conditional probability _st_ + _k ∼ Tθ_ ( _·|st,_ ˜ _at_ ) for the next observation, where ˜ _at_ represents a _k × d_ token sequence, with _k_ being the chunk size and _d_ the number of action dimensions. Moreover, we define the chunk-level reward as _rθ_ ( _st_ + _k, l_ ) =<sup>�</sup><sup>_k_</sup> _i_ =1<sup>_γi−_1</sup><sup>_r_(</sup><sup>_st_+</sup><sup>_i, l_), where</sup><sup>_γ_is the</sup> discount factor and _r_ ( _st_ + _i, l_ ) denotes the reward at step _t_ + _i_ under task instruction _l_ . This design requires no architectural or vocabulary modification, preserving the pretrained capabilities of UMMs. In our implementation, we adopt Bagel (Deng et al., 2025a) as the base model. 

**Interleaved View Decoding.** Fine-grained manipulation often requires reasoning over multiple camera views, as a single viewpoint is insufficient to fully capture object geometry, occlusions, and contact dynamics. This introduces an additional challenge for world modeling: in addition to predicting visually plausible future observations, the world model must maintain cross-view consistency for downstream policy learning. Directly extending UMMs to multi-view inputs often results in view-specific artifacts, which can degrade control performance, even when local predictions are accurate. To address this challenge, we propose a _interleaved view decoding_ strategy that explicitly enforces consistency across multiple camera views. In most VLA models, the input consists of both head-view (or top-view) camera images _s_<sup>_h_</sup> and wrist-camera images _s_<sup>_w_</sup> , forming the combined input _s_ = [ _s_<sup>_h_</sup> _, s_<sup>_w_</sup> ]. Here, the head-view captures global scene information, while the wrist-view provides fine-grained but partially observable details. To model this, we decompose 

3 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

the state transitions as: 


Empirically, we find that this way is better than independent generation of each view in Section 5.1, which ensures that both global and fine-grained information are effectively integrated, maintaining consistency between views. This decomposition can be implemented easily with interleaved decoding in UMMs with attention matrix in Figure 10. 

## **3.2. Challenges in Compounding Model Errors under Sparse Rewards** 

Compounding errors are a fundamental challenge in MBRL, as inaccuracies in world model predictions accumulate over long rollouts and can severely mislead policy optimization. In VLA settings, this issue is further exacerbated by sparse reward structures commonly encountered in manipulation tasks, where small prediction errors may result in qualitatively different outcomes and even opposite reward signals. Such error amplification renders naive full-horizon rollout strategies unreliable. 

To mitigate this issue, we employ the _chunk-level branched rollout_ , a technique used in state-based simple tasks (Park et al., 2025) but has not been validated in pixel-based VLA finetuning. Instead of rolling out full-horizon trajectories starting from the initial state _s_ 0, we initiate rollouts from any observation within the offline dataset with much smaller rollout horizon. Furthermore, since our world model operates at the chunk level, we can further reduce the effective rollout horizon by a factor of 1 _/k_ , where _k_ is the chunk size. By combining these two strategies, we shorten the rollout length by a large margin, thereby enhancing the efficiency and stability of policy optimization. 

## **3.3. VLA-MBPO: Practical World Model-based RL Framework for VLA Models** 

We present **VLA-MBPO** , a practical world model-based RL framework for VLA models, which integrates the three components mentioned above to facilitate VLA reinforcement learning, as illustrated in Figure 1. Our algorithm consists of three phases: 1) data collection with the VLA model; 2) world model finetuning with collected data; 3) policy optimization with RL in the world model. For policy optimization, we adopt _Flow-Noise_ (Chen et al., 2025a), a simple variant of PPO for flow matching-based policy learning. During the RL process, we append an MLP-based value head to the VLA model for value prediction (Chen et al., 2025a). Here, the advantage under _n_ branched rollout 

with chunk size _k_ is defined as: 


The Flow-Noise estimates the log likelihood term in the PPO policy loss as follows: 


where _A_ = ( **A**<sup>0</sup> _, ...,_ **A**<sup>1</sup> ) is denoising sequence of an action chunk. The complete algorithm is shown in Algorithm 1. 

## **Algorithm 1** VLA-MBPO 

- 1: **Require:** Initialized VLA Model _{πϕ, Vϕ}_ , initialized World Model _{Tθ, rθ}_ , initialized the replay buffer _D_ . 

- 2: **Data collection:** Run _πϕ_ in real environments to collect data and add them to _D_ . 

- 3: **World model fine-tuning:** Fine-tune _{Tθ, rθ}_ on _D_ . 

- 4: **Policy optimization in WM:** 

- 5: **for** _j_ = 1 **to** _N_ RL ~~i~~ ter<sup>**do**</sup> 

- 6: Sample starting states _{st}_<sup>_M_</sup> from buffer _D_ . 

- 7: Generate chunk-level branched rollouts by _Tθ, rθ_ . 

- 8: Run _Flow-Noise_ to update _{πϕ, Vϕ}_ on these synthetic data. 

- 9: **end for** 

Our method can be viewed as an instance of offline modelbased reinforcement learning (MBRL), but it differs from prior offline MBRL approaches in several key aspects. First, unlike traditional methods using conservative regularization to mitigate model bias (Yu et al., 2020; Sun et al., 2023; Lin et al., 2025), our approach omits such mechanisms as the finetuned UMM-World achieves sufficient accuracy to render them unnecessary. Second, unlike recent actionchunking-based offline MBRL method (Park et al., 2025), our method is built upon PPO framework and therefore does not rely on additional designs like rejection sampling and Q models, significantly reducing the system complexity. Driven by these two advantages, **our method maintains a single set of hyperparameters across all tasks** (Table 5), which enhances its practical utility and simplifies deployment in real-world scenarios. 

# **4. Theoretical Analysis** 

In this section, we first analyze how previous world modelbased RL methods suffer from severe compounding model error in Section 4.1. Then we show a theoretical result of how VLA-MBPO mitigates these errors in Section 4.2. 

4 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

## **4.1. Value Gap of World Model-based RL** 

Previous world model-based RL for VLA methods evaluate the chunk-level policy in the step-level world model with full-horizon rollouts (Xiao et al., 2025; Zhu et al., 2025). 

**Theorem 4.1** (Value Gap of Chunk-level Policy with Step-level World Model) **.** _Given a chunk-level policy π_<sup>_k_</sup> _with a chunk size k, and a step-level world model T_<sup>ˆ</sup> _. Assume that ϵ_<sup>_k_</sup> _π_ = max _s D_ TV � _πD_<sup>_k_(˜</sup><sup>_a|s_)</sup><sup>_∥πk_(˜</sup><sup>_a|s_)</sup> � _and ϵm_ = max _t_ E _s∼Dt_ � _D_ TV � _T_ ( _s_<sup>_′_</sup> _|s, a_ ) _∥T_<sup>ˆ</sup> ( _s_<sup>_′_</sup> _|s, a_ )�� _. Then, the value gap of policy π_<sup>_k_</sup> _under the true environment and the learned world model is bounded by:_ 


_Proof._ See Appendix B. 

As shown in Theorem 4.1, the value gap is influenced by two components: (a) **Policy error** _ϵ_<sup>_k_</sup> _π_<sup>:the divergence between</sup> the current policy _π_<sup>_k_</sup> and the behavior policy _πD_<sup>_k_,with</sup> _<u>γ</u>_<sup>_k_</sup> dependency _O_ . (b) **Model error** _ϵm_ : the � (1 _−γ_ )(1 _−γ_<sup>_k_</sup> ) � discrepancy between true dynamics _T_ and learned model _T_<sup>ˆ</sup> , _kγ_<sup>_k_</sup> which also significantly scales as _O_ . � (1 _−γ_ )(1 _−γ_<sup>_k_</sup> ) � 

The value gap grows quadratically with the task horizon due to the compounding errors, resulting in big value errors in long-horizon tasks. For large VLA models, we typically control policy divergence _ϵ_<sup>_k_</sup> _π_<sup>byreducingtheupdatestep</sup> size or adding a KL constraint. However, world model error _ϵm_ is more challenging to control during RL training, as it is largely dependent on the high-quality pretraining. Consequently, even small model inaccuracies can accumulate over long rollouts, leading to significant distortions in value estimates and misleading policy optimization. 

## **4.2. Reduced Value Gap of VLA-MBPO** 

Here, we demonstrate how VLA-MBPO reduces compounding errors by employing a chunk-level branched rollouts in a chunk-wise world model. 

**Theorem 4.2** (Value Gap of Chunk-level Policy with Chunk-level World Model and Branched Rollouts) **.** _Given an offline dataset D and a chunk-level policy π_<sup>_k_</sup> _with a chunk size k. Suppose that policy π_<sup>_k_</sup> _is evaluated via n-chunks branched rollouts in the chunk-level world model T_ ˆ<sup>_k_</sup> ( _s_<sup>_′_</sup> _|s,_ ˜ _a_ ) _. Assume that ϵ_<sup>_k_</sup> _π_ = max _s D_ TV� _πD_<sup>_k_(˜</sup><sup>_a|s_)</sup><sup>_∥πk_(˜</sup><sup>_a|s_)</sup> � _and ϵ_<sup>_k,n_</sup> _m_ = max _t≤n_ E _s∼dπkt,s_ 0 _∼D_ � _D_ TV � _T_<sup>_k_</sup> ( _s_<sup>_′_</sup> _|s,_ ˜ _a_ ) _∥T_<sup>ˆ</sup><sup>_k_</sup> ( _s_<sup>_′_</sup> _|s,_ ˜ _a_ )�� _. Then the value gap of policy π_<sup>_k_</sup> _under the true environment_ 

_and the learned world model is bounded by:_ 


_Proof._ See Appendix B. 

Theorem 4.2 highlights how VLA-MBPO limits the value gap between the true environment and the learned world model via chunk-level world models and branched rollouts. By restricting the length of the rollouts and breaking the task into chunks, both the policy and model errors are mitigated compared to previous methods. Specifically, the policy er- <u>(</u> _<u>γ</u>_<sup>_k_</sup> <u>)</u><sup>_n_+1</sup> ror dependency is bounded by _O_ while the � (1 _−γ_ )(1 _−γ_<sup>_k_</sup> ) <u>�</u> model error dependency is bounded by _O_ � 1 _−nγ_ �. We observe that as _n_ increases, while the dependency on model error increases linearly, the influence of policy error diminishes exponentially. This suggests that by appropriately selecting the branched-rollout chunks _n_ , we can significantly alleviate this value gap. 

**Simple Case Study.** Consider a scenario where the discount factor _γ_ = 0 _._ 99 and the chunk size _k_ = 10, which are typical choices in VLA-RL tasks. In such cases, previous world model-based VLA-RL methods suffer from a value gap of approximately 4183 _ϵ_<sup>_k_</sup> _π_<sup>+ 18916</sup><sup>_ϵm_.In contrast, if we</sup> use VLA-MBPO with branched rollouts of length _n_ = 2, the value gap is considerably smaller, approximately 1710 _ϵ_<sup>_k_</sup> _π_<sup>+</sup> 400 _ϵ_<sup>_k,n_</sup> _m_<sup>, demonstrating the effectiveness of the VLA-MBPO</sup> in mitigating error compounding. 

# **5. Experiments** 

We conduct extensive experiments on both simulated and real-world robotic tasks to answer these questions. **Q1** : How does our UMM-based world model (UMM-World) perform on multi-view dynamics modeling and reward prediction? (Section 5.1) **Q2** : How does VLA-MBPO perform in simulation tasks? (Section 5.2) **Q3** : How does VLA-MBPO perform in real-world tasks? (Section 5.3) **Q4** : How sensitive is VLA-MBPO to key hyperparameters and design choices? (Section 5.4) 

## **5.1. World Model Evaluation** 

**Benchmark.** We conduct our evaluation on the _Object_ task suite in LIBERO (Liu et al., 2023), a manipulation benchmark that contains 10 distinct tasks with diverse object instances. We use a dataset comprised of 50 trajectories per task for training, and report evaluation results on a held-out test set of 10 trajectories per task. The evaluation protocol involves rolling out 40 steps across 100 held-out test trajec- 

5 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

_Table 1._ Performance comparison of various world models across multiple metrics, including dynamics and reward model evaluations. 

||||**D**|**ynamics M**|**odel**|||**Reward**|**Model**|
|---|---|---|---|---|---|---|---|---|---|
|**Model**||**Head View**|||**Wrist View**||**Inf. Time**_↓_|**ACC**_↑_|**F1**_↑_|
||**LPIPS**_↓_|**PSNR**_↑_|**SSIM**_↑_|**LPIPS**_↓_|**PSNR**_↑_|**SSIM**_↑_||||
|Ctrl-World|0.150|21.95|0.882|0.435|13.87|0.680|21|–|–|
|Qwen3-VL-8B|–|–|–|–|–|–|–|97.0|0.841|
|**UMM-World**|**0.094**|**23.29**|**0.906**|**0.254**|**18.76**|**0.751**|10|98.4|**0.861**|
|-_w/o IVD_|0.116|21.71|0.895|0.454|13.38|0.559|**8**|**98.5**|0.799|
|-_w/o PT_|0.281|19.26|0.756|0.579|12.80|0.499|10|94.5|0.496|


tories. We report evaluation results for both head and wrist views to rigorously assess long-term consistency. 

**Baselines.** We quantitatively compare our model against two distinct baselines: (1) _Ctrl-World_ (Guo et al., 2025), a video generation model that excels at dynamics synthesis with multi-view consistency but lacks the semantic grounding for intrinsic reward prediction; and (2) _Qwen3-VL_ (Bai et al., 2025), a VLM capable of precise reward reasoning but unable to predict visual dynamics. Moreover, to validate our model design, we evaluate two ablations: 1) _w/o Interleaved View Decoding (IVD)_ , where views are generated in parallel rather than interleaved, isolating the impact of our decoding strategy on multi-view consistency. 2) _w/o Pretrained (PT)_ , where UMM-World is randomly initialized. We quantitatively evaluate all models from dynamics prediction, inference speed and reward prediction perspectives. 

**Task Results.** As presented in Table 1, UMM-World demonstrates superior performance across nearly all metrics. Not only does it outperforms the video world model baseline on the prediction fidelity of both head and wrist views, but also achieves a 2 _×_ faster inference speed owing to the frameskipping scheme. When it comes to reward prediction, our model also matches the specialist Qwen3-VL-8B. We credit these substantial gains to two key innovations: _Interleaved View Decoding_ and _Unified Pretraining_ . Ablation studies confirm that removing either component leads to a severe degradation in both dynamics modeling and reward prediction performance. We also present some qualitative results of UMM-World in Figure 4 and Figure 11. 

## **5.2. Simulation Task Experiments** 

**Benchmark.** We evaluate VLA-MBPO on LIBERO (Liu et al., 2023), a widely adopted benchmark consisting of four task suites: _Spatial_ , _Object_ , _Goal_ , and _Long_ , designed to assess capabilities ranging from visual grounding to longhorizon planning. The offline dataset is constructed by collecting 50 episodes per task, where the behavior policy is obtained via _π_ 0 _._ 5 with one-shot SFT. We measure performance by average success rate over 50 evaluation episodes 

per task across all 10 tasks in each suite. 

**Baselines.** We compare VLA-MBPO against four baselines: (1) _π_ 0 _._ 5 (SFT): the VLA model ( _π_ 0 _._ 5) prior to any RL; (2) _BC_ (WM): a BC baseline trained on successful trajectories generated by world models; (3) an online RL baseline _πRL_ (Chen et al., 2025a) under an equivalent real-world interaction budget; and (4) _IDQL_ (Hansen-Estruch et al., 2023): an offline model-free RL algorithm for flow-matching policies. 

_Table 2._ Performance comparison on LIBERO benchmark. 

|**Model**||**LI**|**BERO**|||
|---|---|---|---|---|---|
||**Spatial**|**Object**|**Goal**|**Long**|**Avg**|
||One-T|rajectory|SFT|||
|_π_0_._5(SFT)|78.2|88.6|85.8|54.6|76.8|
|BC (WM)|80.6|89.8|85.0|48.6|76.0|
|_πRL_|86.0|92.4|90.8|61.2|82.6|
|IDQL|79.0|92.4|86.4|52.2|77.5|
|**VLA-MBPO**|**87.8**|**96.6**|**92.8**|**66.8**|**85.9**|
|∆|+9.6|+8.0|+6.8|+12.2|+9.1|


**Task Results.** As shown in Table 2, VLA-MBPO achieves consistent and substantial performance gains over all baselines across every suite of the LIBERO benchmark. It attains the highest average success rate, improving the initial SFT policy by +9.1. Notably, the most pronounced improvement occurs on the _LIBERO-Long_ suite, which comprises the most challenging long-horizon tasks. Under an identical real-world data budget, VLA-MBPO substantially outperforms both offline and online RL methods on this suite, highlighting its superior sample efficiency and effectiveness in solving complex manipulation tasks. 

**Generalizable Credit Assignment.** We visualize the learning dynamics of the value model on unseen full-horizon trajectories in Figure 3. We find that despite training with short branched rollouts, our value model progressively aligns with ground-truth returns through learning cross-chunk temporal dependencies and value consistency, thereby achieving coherent long-horizon value estimates that accurately reflect trajectory outcomes. We posit that this stitching capability is the fundamental mechanism enabling VLA-MBPO 

6 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 


_Figure 3._ The learning dynamics of value models. The blue lines represent the ground-truth return, while the orange lines represent the return estimated by the value model. 

to achieve significant policy improvement using only shorthorizon model-based rollouts. 

## **5.3. Real-world Task Experiments** 

Transitioning from simulation to the physical world introduces significant challenges, including complex non-rigid dynamics, sensor noise, and unmodeled environmental factors. In this section, we explore whether VLA-MBPO can improve performance of VLAs in the real-world scenarios. 

**Experiment Setup.** As shown in Figure 9, we design five real-world tasks across two robotic platforms. On the bimanual robot **Arx-X5** , a) _Plug Cable_ requires sub-centimeter precision to insert a cable into a 3-mm socket, while b) _Fold Towel_ assesses bimanual manipulation of deformable objects. On the whole-body robot **Galaxy-R1** , c) _Pick Cup_ and d) _Insert Pen_ evaluate whole-body manipulation with disturbed robot poses and camera viewpoints, and e) _Wipe Board_ tests mobile whole-body control under partial observability. For each task, we collect expert demonstrations via human teleoperation, with approximately 50 trajectories for Arx-X5 tasks and 100 trajectories for Galaxy-R1 tasks, and perform SFT for _π_ 0 _._ 5. We then collect 50 rollouts per task using _π_ 0 _._ 5 (SFT) for subsequent VLA-MBPO training. Evaluation is conducted on 50 trajectories per task: 30 _seen_ and 20 _unseen_ , where the latter include novel objects, backgrounds, and spatial configurations. Additional details are provided in Appendix C. 

**Task Results.** As shown in Figure 5, VLA-MBPO delivers consistent performance gains across both robotic platforms, validating its robustness in physical environments where dynamics are inherently stochastic. On Arx-X5, gains in _Fold Towel_ confirm effective modeling of deformable-object dynamics, while improved _Plug Cable_ performance highlights success in fine-grained, contact-rich manipulation. On Galaxy-R1, VLA-MBPO excels in high-DoF wholebody control, notably in _Wipe Board_ task with severe partial observability. Strong results on both seen and unseen conditions further validate its real-world generalization. 

## **5.4. Ablation Study** 

While the main results highlight the effectiveness of VLAMBPO, we now explore the influence of two key factors: the a) _rollouts scheme_ , and b) _generated sample size_ . We conduct all ablation studies on _LIBERO-Long_ suite. 

_Table 3._ Results of different rollouts scheme for VLA-MBPO. 

|||**LIBERO**|**Long**|
|---|---|---|---|
|**Rollouts Scheme**|Bran|ched Rollout|Full Horizon|
||**1**|**2**<br>**4**||
|**VLA-MBPO**|63.9|**66.8**<br>62.9|52.8|


**Rollouts Scheme.** We analyze the impact of different rollout lengths for VLA-MBPO, as shown in Table 3. The results consistently demonstrate that VLA-MBPO improves policy performance across various rollout horizons. However, there is a tradeoff: shorter rollouts (length=1 chunk) restrict exploration and complicate trajectory stitching, while excessively long horizons (length=4 chunks) lead to the unreliable trajectory generation. Both of these factors limit the potential for performance gains. Furthermore, using full-horizon rollouts in long-horizon tasks results in significant performance degradation due to intolerable compounding model errors. 

**Imagined Sample Size.** We analyze the policy performance across different generated sample sizes per iteration as shown in Figure 6. VLA-MBPO demonstrates a consistently monotonic improvement in success rate with increasing sample size. As the generated sample size grows, the value estimations become more accurate, which reduces biases in policy gradients and results in more stable policy improvements. This underscores the potential of VLA-MBPO to tackle more complex and diverse multitask learning challenges, offering a scalable and practical approach for world model-based RL for VLAs. 

# **6. Related Works** 

**Reinforcement Learning for VLA Models.** Recent research has increasingly focused on adapting reinforcement learning to fine-tune VLA models for embodied control. Li et al. (2025b) and Liu et al. (2025) adapt standard on-policy algorithms (Schulman et al., 2017) to fine-tune next-token prediction VLA models (Kim et al., 2024; 2025) and other work like _π_ RL (Chen et al., 2025a) extends online fine-tuning to flow matching policies (Black et al., 2024; Intelligence et al., 2025c). However, regardless of the backbone, the prohibitively high sample complexity of online interaction restricts their applicability in real-world scenarios. To circumvent these costs, Offline RL has been applied to finetuning VLA. _π_ 0.6<sup>_∗_(Intelligence et al., 2025a) improves VLA</sup> policies via advantage-conditioned policy optimization over 

7 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 


_Figure 4._ Qualitative visualization results of UMM-World. 


_Figure 6._ Results of different sample size for VLA-MBPO. 

heterogeneous offline data. Reinbot (Zhang et al., 2025) enables offline policy optimization by predicting dense returns from static datasets. Despite their data efficiency, these methods operate purely on static datasets without modeling environment dynamics, limiting their ability to simulate consequences or recover from out-of-distribution states. 

**Model-based Reinforcement Learning.** Model-based reinforcement learning improves sample efficiency by learning environment dynamics to augment experience with imagined transitions (Janner et al., 2019; Lin et al., 2023) or to enable planning (Chua et al., 2018). This paradigm has also been extended to offline RL by generating synthetic data beyond static datasets (Yu et al., 2020; Sun et al., 2023; Lin et al., 2025; 2026; Wu et al., 2026). A central challenge in MBRL is _compounding error_ , where small prediction errors accumulate over rollout horizons. MBPO (Janner et al., 2019) mitigates error by performing short branched 

rollouts, and MOPO (Yu et al., 2020) and MOBILE (Sun et al., 2023) further penalize policy optimization in regions with high uncertainty to prevent exploitation of inaccurate dynamics. More recently, Park et al. (2025) propose an action-chunked dynamics model that predicts future states from action sequences, though it remains limited to lowdimensional state spaces and relies on a complex design for conservative Q-learning. In high-dimensional visual control and VLA settings, Zhu et al. (2025); Xiao et al. (2025); Li et al. (2025a) make important progress, but their reliance on full-horizon rollouts leaves them vulnerable to compounding errors, limiting their applicability to long-horizon and complex tasks. 

# **7. Conclusion** 

In this paper, we present VLA-MBPO, a practical world model-based RL framework for training VLA models. By integrating a UMM-based backbone, interleaved view decoding for multi-view consistency, and chunk-level branched rollout to mitigate error compounding, VLAMBPO significantly enhances policy improvement and sample efficiency. These advancements enables a more practical and scalable post-training method for VLA models, pave a way for more reliable real-world deployment. 

**Limitations.** Despite the higher inference efficiency of UMM-World compared to video models, the sample generation phase still requires large computational resources, as detailed in Appendix F. Additionally, since the UMM model used in our framework was not pretrained on action-labeled robotic data, VLA-MBPO still requires a small amount data to finetune the world model when applied to downstream tasks. A promising direction for future work is to enhance the pretraining process, enabling the world model to achieve one-shot or even zero-shot generalization. 

8 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

# **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none of which we feel must be specifically highlighted here. 

# **Acknowledgements** 

This work was supported by the Yangtze River Delta Science and Technology Innovation Community Joint Research Program 2024CSJZN00302, the National Natural Science Foundation of China under Grants 62495090 and 62495093, the Natural Science Foundation of Jiangsu under Grants BK20243039, the “111 Center” (No. B26023), and the Fundamental and Interdisciplinary Disciplines Breakthrough Plan of the Ministry of Education of China (No. JYB2025XDXM118). 

# **References** 

- Bai, S., Cai, Y., Chen, R., Chen, K., Chen, X., Cheng, Z., Deng, L., Ding, W., Gao, C., Ge, C., Ge, W., Guo, Z., Huang, Q., Huang, J., Huang, F., Hui, B., Jiang, S., Li, Z., Li, M., Li, M., Li, K., Lin, Z., Lin, J., Liu, X., Liu, J., Liu, C., Liu, Y., Liu, D., Liu, S., Lu, D., Luo, R., Lv, C., Men, R., Meng, L., Ren, X., Ren, X., Song, S., Sun, Y., Tang, J., Tu, J., Wan, J., Wang, P., Wang, P., Wang, Q., Wang, Y., Xie, T., Xu, Y., Xu, H., Xu, J., Yang, Z., Yang, M., Yang, J., Yang, A., Yu, B., Zhang, F., Zhang, H., Zhang, X., Zheng, B., Zhong, H., Zhou, J., Zhou, F., Zhou, J., Zhu, Y., and Zhu, K. Qwen3-vl technical report. _CoRR_ , 2025. 

- Bjorck, J., Castaneda, F., Cherniadev, N., Da, X., Ding, R.,˜ Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L. X., Tanner, J., Vuong, Q., Walling, A., Wang, H., and Zhilinsky, U. _π_ 0: A vision-language-action flow model for general robot control. _CoRR_ , 2024. 

- Chen, K., Liu, Z., Zhang, T., Guo, Z., Xu, S., Lin, H., Zang, H., Zhang, Q., Yu, Z., Fan, G., Huang, T., Wang, Y., and Yu, C. _πRL_ : Online RL fine-tuning for flow-based vision-language-action models. _CoRR_ , 2025a. 

- Chen, Y., Tian, S., Liu, S., Zhou, Y., Li, H., and Zhao, D. Conrft: A reinforced fine-tuning method for vla models via consistency policy. _arXiv preprint arXiv:2502.05450_ , 2025b. 

- Chua, K., Calandra, R., McAllister, R., and Levine, S. Deep reinforcement learning in a handful of trials using probabilistic dynamics models. In _Thirty-second Annual Conference on Neural Information Processing Systems (NeurIPS’18), Montr´eal, Canada_ , 2018. 

- Cui, Y., Chen, H., Deng, H., Huang, X., Li, X., Liu, J., Liu, Y., Luo, Z., Wang, J., Wang, W., et al. Emu3. 5: Native multimodal models are world learners. _arXiv preprint arXiv:2510.26583_ , 2025. 

- Deng, C., Zhu, D., Li, K., Gou, C., Li, F., Wang, Z., Zhong, S., Yu, W., Nie, X., Song, Z., Guang, S., and Fan, H. Emerging properties in unified multimodal pretraining. _CoRR_ , 2025a. 

- Deng, S., Yan, M., Wei, S., Ma, H., Yang, Y., Chen, J., Zhang, Z., Yang, T., Zhang, X., Zhang, W., et al. Graspvla: a grasping foundation model pre-trained on billion-scale synthetic action data. _arXiv preprint arXiv:2505.03233_ , 2025b. 

- Fei, S., Wang, S., Ji, L., Li, A., Zhang, S., Liu, L., Hou, J., Gong, J., Zhao, X., and Qiu, X. Srpo: Self-referential policy optimization for vision-language-action models. _arXiv preprint arXiv:2511.15605_ , 2025. 

- Fu, Z., Zhao, T. Z., and Finn, C. Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. _arXiv preprint arXiv:2401.02117_ , 2024. 

- Ghosh, D., Walke, H. R., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., Luo, J., Tan, Y. L., Chen, L. Y., Vuong, Q., Xiao, T., Sanketi, P. R., Sadigh, D., Finn, C., and Levine, S. Octo: An opensource generalist robot policy. In _Robotics: Science and Systems XX (RSS’24), Delft, Netherlands_ , 2024. 

- Goyal, A., Hadfield, H., Yang, X., Blukis, V., and Ramos, F. Vla-0: Building state-of-the-art vlas with zero modification. _arXiv preprint arXiv:2510.13054_ , 2025. 

- Guo, Y., Shi, L. X., Chen, J., and Finn, C. Ctrl-world: A controllable generative world model for robot manipulation. _CoRR_ , 2025. 

- Hafner, D., Pasukonis, J., Ba, J., and Lillicrap, T. P. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- Hansen, N., Su, H., and Wang, X. TD-MPC2: scalable, robust world models for continuous control. In _The Twelfth International Conference on Learning Representations (ICLR’24), Vienna, Austria_ , 2024. 

- Hansen-Estruch, P., Kostrikov, I., Janner, M., Kuba, J. G., and Levine, S. IDQL: implicit q-learning as an actor-critic method with diffusion policies. _CoRR_ , 2023. 

9 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

- Intelligence, P., Amin, A., Aniceto, R., Balakrishna, A., Black, K., Conley, K., Connors, G., Darpinian, J., Dhabalia, K., DiCarlo, J., Driess, D., Equi, M., Esmail, A., Fang, Y., Finn, C., Glossop, C., Godden, T., Goryachev, I., Groom, L., Hancock, H., Hausman, K., Hussein, G., Ichter, B., Jakubczak, S., Jen, R., Jones, T., Katz, B., Ke, L., Kuchi, C., Lamb, M., LeBlanc, D., Levine, S., Li-Bell, A., Lu, Y., Mano, V., Mothukuri, M., Nair, S., Pertsch, K., Ren, A. Z., Sharma, C., Shi, L. X., Smith, L., Springenberg, J. T., Stachowicz, K., Stoeckle, W., Swerdlow, A., Tanner, J., Torne, M., Vuong, Q., Walling, A., Wang, H., Williams, B., Yoo, S., Yu, L., Zhilinsky, U., and Zhou, Z. _π_<sup>_∗_</sup> 0 _._ 6: a VLA that learns from experience. _CoRR_ , 2025a. 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Galliker, M. Y., Ghosh, D., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., LeBlanc, D., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Ren, A. Z., Shi, L. X., Smith, L., Springenberg, J. T., Stachowicz, K., Tanner, J., Vuong, Q., Walke, H., Walling, A., Wang, H., Yu, L., and Zhilinsky, U. _π_ 0 _._ 5: a visionlanguage-action model with open-world generalization. _CoRR_ , 2025b. 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Galliker, M. Y., Ghosh, D., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., LeBlanc, D., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Ren, A. Z., Shi, L. X., Smith, L., Springenberg, J. T., Stachowicz, K., Tanner, J., Vuong, Q., Walke, H., Walling, A., Wang, H., Yu, L., and Zhilinsky, U. _π_ 0.5: a visionlanguage-action model with open-world generalization. _CoRR_ , 2025c. 

- Janner, M., Fu, J., Zhang, M., and Levine, S. When to trust your model: Model-based policy optimization. In _Thirty-third Annual Conference on Neural Information Processing Systems (NeurIPS’19), Vancouver, Canada_ , 2019. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E. P., Sanketi, P. R., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake, R., Sadigh, D., Levine, S., Liang, P., and Finn, C. Openvla: An open-source vision-language-action model. In _8th Annual Conference on Robot Learning (CoRL’24), Munich, Germany_ , 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _CoRR_ , 2025. 

- Langley, P. Crafting papers on machine learning. In _Seventeenth International Conference on Machine Learning (ICML’00), Stanford, USA_ , 2000. 

- Li, H., Ding, P., Suo, R., Wang, Y., Ge, Z., Zang, D., Yu, K., Sun, M., Zhang, H., Wang, D., et al. Vla-rft: Vision-language-action reinforcement fine-tuning with verified rewards in world simulators. _arXiv preprint arXiv:2510.00406_ , 2025a. 

- Li, H., Zuo, Y., Yu, J., Zhang, Y., Yang, Z., Zhang, K., Zhu, X., Zhang, Y., Chen, T., Cui, G., Wang, D., Luo, D., Fan, Y., Sun, Y., Zeng, J., Pang, J., Zhang, S., Wang, Y., Mu, Y., Zhou, B., and Ding, N. Simplevla-rl: Scaling VLA training via reinforcement learning. _CoRR_ , 2025b. 

- Lin, H., Sun, Y., Zhang, J., and Yu, Y. Model-based reinforcement learning with multi-step plan value estimation. In _26th European Conference on Artificial Intelligence (ECAI’23), Krak´ow, Poland_ , 2023. 

- Lin, H., Xu, Y.-Y., Sun, Y., Zhang, Z., Li, Y.-C., Jia, C., Ye, J., Zhang, J., and Yu, Y. Any-step dynamics model improves future predictions for online and offline reinforcement learning. In _The Thirteenth International Conference on Learning Representations (ICLR’25), Singapore_ , 2025. 

- Lin, H., Xiao, S., Li, Y.-C., Zhang, Z., Sun, Y., Jia, C., and Yu, Y. ADM-v2: Pursuing full-horizon roll-out in dynamics models for offline policy learning and evaluation. In _The Fourteenth International Conference on Learning Representations (ICLR’26), Rio de Janeiro, Brazil_ , 2026. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. In _Thirty-seventh Annual Conference on Neural Information Processing Systems (NeurIPS’23), New Orleans, USA_ , 2023. 

- Liu, J., Gao, F., Wei, B., Chen, X., Liao, Q., Wu, Y., Yu, C., and Wang, Y. What can RL bring to VLA generalization? an empirical study. _CoRR_ , 2025. 

- Park, K., Park, S., Lee, Y., and Levine, S. Scalable offline model-based RL with action chunks. _CoRR_ , 2025. 

- Puterman, M. L. Markov decision processes. _Handbooks in operations research and management science_ , 1990. 

- Puterman, M. L. _Markov decision processes: discrete stochastic dynamic programming_ . John Wiley & Sons, 2014. 

- Qian, Z., Chi, X., Li, Y., Wang, S., Qin, Z., Ju, X., Han, S., and Zhang, S. Wristworld: Generating wrist-views via 4d world models for robotic manipulation. _arXiv preprint arXiv:2510.07313_ , 2025. 

- Rajaraman, N., Yang, L. F., Jiao, J., and Ramchandran, K. Toward the fundamental limits of imitation learning. In _Thirty-fourth Annual Conference on Neural Information Processing Systems (NeurIPS’20), Virtual Event_ , 2020. 

10 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

- Schulman, J., Moritz, P., Levine, S., Jordan, M., and Abbeel, P. High-dimensional continuous control using generalized advantage estimation. _arXiv preprint arXiv:1506.02438_ , 2015. 

- Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and Klimov, O. Proximal policy optimization algorithms. _CoRR_ , 2017. 

- Sun, Y., Zhang, J., Jia, C., Lin, H., Ye, J., and Yu, Y. ModelBellman inconsistency for model-based offline reinforcement learning. In _40th International Conference on Machine Learning (ICML’23), Honolulu, USA_ , 2023. 

- Sun, Y., Zhang, Z., Yu, Y., and Bacon, P.-L. Planning with unified multimodal models. _arXiv preprint arXiv:2509.23014_ , 2025. 

   - Zhang, Z., Chen, R., Ye, J., Sun, Y., Wang, P., Pang, J., Li, K., Liu, T., Lin, H., Yu, Y., et al. Whale: Towards generalizable and scalable world models for embodied decisionmaking. _arXiv preprint arXiv:2411.05619_ , 2024. 

   - Zhang, Z., Mei, Y., Du, X., Cao, H., Wang, H., Min, P., Wang, C., Chen, P., Xin, C., Wang, Y., Luo, W., Sun, Y., Wang, Y., Yuan, L., Wang, G., and Yu, Y. Hierarchical value-decomposed offline reinforcement learning for whole-body control. In _The Fourteenth International Conference on Learning Representations_ , 2026. URL https://openreview.net/forum? id=eSkDNIGbcd. 

   - Zhu, F., Yan, Z., Hong, Z., Shou, Q., Ma, X., and Guo, S. WMPO: world model-based policy optimization for vision-language-action models. _CoRR_ , 2025. 

- Wu, Z., Ye, J., Zhang, Z., Sun, Y., Lin, H., Ren, H., Luo, J., Yuan, L., and Yu, Y. Speedup patch: Learning a plugand-play policy to accelerate embodied manipulation. In _ICLR 2026 the 2nd Workshop on World Models: Understanding, Modelling and Scaling_ , 2026. URL https: //openreview.net/forum?id=qcoPvvhlXg. 

- Xiao, J., Yang, Y., Chang, X., Chen, R., Xiong, F., Xu, M., Zheng, W., and Zhang, Q. World-env: Leveraging world model as a virtual environment for VLA post-training. _CoRR_ , 2025. 

- Xu, T., Li, Z., and Yu, Y. Error bounds of imitating policies and environments. In _Thirty-fourth Annual Conference on Neural Information Processing Systems (NeurIPS’20), Virtual Event_ , 2020. 

- Xu, T., Zhang, Z., Chen, R., Sun, Y., and Yu, Y. Provably and practically efficient adversarial imitation learning with general function approximation. _Advances in Neural Information Processing Systems_ , 37:66108–66146, 2024. 

- Yu, T., Thomas, G., Yu, L., Ermon, S., Zou, J. Y., Levine, S., Finn, C., and Ma, T. MOPO: model-based offline policy optimization. In _Thirty-fourth Annual Conference on Neural Information Processing Systems (NeurIPS’20), Virtual Event_ , 2020. 

- Zang, H., Wei, M., Xu, S., Wu, Y., Guo, Z., Wang, Y., Lin, H., Shi, L., Xie, Y., Xu, Z., et al. Rlinf-vla: A unified and efficient framework for vla+ rl training. _arXiv preprint arXiv:2510.06710_ , 2025. 

- Zhang, H., Zhuang, Z., Zhao, H., Ding, P., Lu, H., and Wang, D. Reinbot: Amplifying robot visual-language manipulation with reinforcement learning. In _Forty-second International Conference on Machine Learning (ICML’25), Vancouver, Canada_ , 2025. 

11 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

# **A. Useful Lemmas** 

**Lemma A.1** (Total Variation Distance for Joint Distributions) **.** _Let_ P1( _x, y_ ) = P1( _x_ ) P1( _y|x_ ) _and_ P2( _x, y_ ) = P2( _x_ ) P2( _y|x_ ) _be two joint probability distributions over_ ( _x, y_ ) _. Then the total variation distance between_ P1 _and_ P2 _satisfies_ 


_Proof._ Recall that the total variation distance between two distributions _µ_ and _ν_ is defined as _D_ TV( _µ, ν_ ) =<sup><u>1</u></sup> 2 � _|dµ − dν|_ . Applying this to the joint distributions P1 and P2, we have 


**Lemma A.2** (Total Variation Bound for Rollout State Distributions) **.** _Let_ P1 _and_ P2 _be two stochastic processes over states {st}t≥_ 0 _that share the same initial state distribution, i.e.,_ P1( _s_ 0) = P2( _s_ 0) _. Suppose that the expected total variation distance between their transition kernels satisfies_ max _t_ E _s∼_ P _t_ 1<sup>(</sup><sup>_s_)</sup> � _D_ TV�P1( _s_<sup>_′_</sup> _|s_ ) _∥_ P2( _s_<sup>_′_</sup> _|s_ )�� _≤ δ. Then, the total variation distance between the marginal state distributions at time t is bounded as_ 


_Proof._ We proceed by induction on _t_ . For _t_ = 0, we have P1( _s_ 0) = P2( _s_ 0) by assumption, so _D_ TV(P1( _s_ 0) _∥_ P2( _s_ 0)) = 0 _≤_ 0 _· δ_ , which establishes the base case. 

Assume the claim holds for some _t −_ 1 _≥_ 0, i.e., 


We now bound the distance at step _n_ . By the law of total probability, the marginal densities satisfy 


The total variation distance is then 


12 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

By the assumption, the first term is at most _δ_ , and by the induction hypothesis, the second term is at most ( _n −_ 1) _δ_ . Therefore, 


This completes the induction step. Hence, for all _n ≥_ 0, 


**Lemma A.3** (Value Divergence, Chunk-Level Policy, Chunk-Level World Model) **.** _Let k ∈_ N<sup>+</sup> _be the output chunk size of policies. Consider two stochastic k-steps policies π_ 1<sup>_kandπ_</sup> 2<sup>_k,whereeachpolicyselectsanactionsequence_</sup> _a_ ˜ _t_ = _at_ : _t_ + _k−_ 1 _given state st. Suppose that policy π_ 1<sup>_kand π_</sup> 2<sup>_kare evaluated in the chunk-level world model T k_</sup> 1<sup>(</sup><sup>_s′|s,_˜</sup><sup>_a_)</sup><sup>_and_</sup> _T_ 2<sup>_k_(</sup><sup>_s′|s,_˜</sup><sup>_a_)</sup><sup>_respectively.Assume the reward per-step satisfies r_(</sup><sup>_st, at_)</sup><sup>_∈_[0</sup><sup>_, r_max]</sup><sup>_, and define the k-steps total variation_</sup> _divergence between the policies as ϵ_<sup>_k_</sup> _π_<sup>:= max</sup><sup>_sD_TV</sup> � _π_ 1<sup>_k_(˜</sup><sup>_a|s_)</sup><sup>_∥π_</sup> 2<sup>_k_(˜</sup><sup>_a|s_)</sup> � _. Likewise, the dynamics divergence is bounded by ϵ_<sup>_k_</sup> _m_<sup>= max</sup><sup>_t_E</sup> _s∼dπt_ 1<sup>_k_</sup> � _D_ TV � _T_ 1<sup>_k_(</sup><sup>_s′|s,_˜</sup><sup>_a_)</sup><sup>_∥T_</sup> 2<sup>_k_(</sup><sup>_s′|s,_˜</sup><sup>_a_)</sup> �� _. Then the value gap of two policies is bounded by_ 


_Proof._ We reformulate the problem as a _temporally-extended MDP M_<sup>_k_</sup> = ( _S, A_<sup>_k_</sup> _, T,_<sup>˜</sup> ˜ _r, γ_<sup>_k_</sup> ), where: 

- The state space _S_ is unchanged. 

- The action space is chunk-level _A_<sup>_k_</sup> , with ˜ _a_ = _a_ 0: _k−_ 1 _∈A_<sup>_k_</sup> . 

- The transition kernel _T_<sup>_k_</sup> ( _s_<sup>_′_</sup> _| s,_ ˜ _a_ ) denotes the probability of reaching state _s_<sup>_′_</sup> after executing the _k_ -steps action sequence ˜ _a_ from state _s_ . 

- The reward _r_ ˜( _s,_ ˜ _a_ ) :=<sup>�</sup><sup>_k_</sup> _i_ =0<sup>_−_1</sup><sup>_γir_(</sup><sup>_si, ai_)isthe</sup><sup>_γ_-discountedsumwithinthechunk.Since</sup><sup>_r_(</sup><sup>_s, a_)</sup><sup>_∈_[0</sup><sup>_, r_max],the</sup> 1 _−γ_<sup>_k_</sup> 

- chunk reward is bounded by ˜ _r_ max = _r_ max 1 _−γ_<sup>.</sup> 

- The discount factor between macro-steps is _γ_<sup>_k_</sup> . 

Crucially, the expected return of any _k_ -steps policy is identical under the original MDP and its temporally-extended variant. Let _d_<sup>_π_</sup> _t_<sup>_k_</sup> denote the state-action density of policy _π_<sup>_k_</sup> at the timestep _t_ and _d_<sup>_πk_</sup> = (1 _− γ_<sup>_k_</sup> )<sup><u>�</u></sup><sup>_∞_</sup> _t_ =0<sup>(</sup><sup>_γk_)</sup><sup>_td_</sup> _t_<sup>_πk_</sup> is the overall discounted occupancy measure, such that _V_ ( _π_<sup>_k_</sup> ) = � _r_<sup>_k_</sup> ( _s,_ ˜ _a_ )<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>(</sup><sup>_γk_)</sup><sup>_td_</sup> _t_<sup>_πk_(</sup><sup>_s,_˜</sup><sup>_a_)</sup><sup>_dsda_˜ =</sup> 1 _−_ <u>1</u> _γ_<sup>_k_</sup> � _r_<sup>_k_</sup> ( _s,_ ˜ _a_ ) _d_<sup>_πk_</sup> ( _s,_ ˜ _a_ ) _dsda_ ˜, then we have 


By Lemma A.1, we have 


**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

The first term is exactly _ϵ_<sup>_k_</sup> _π_<sup>.For the second term, we have</sup> 


By Lemma A.2, we have 


Finally, we have 

**Lemma A.4** (Value Divergence, Chunk-level Policy, Chunk-level World Model, Branched Rollout) **.** _Let k ∈_ N<sup>+</sup> _be the output chunk size of policies. Consider two stochastic k-step policies π_ 1<sup>_kandπ_</sup> 2<sup>_k,whereeachpolicyse-_</sup> _lects an action sequence a_ ˜ _t_ = _at_ : _t_ + _k−_ 1 _given state st. Suppose that policy π_ 1<sup>_kandπ_</sup> 2<sup>_kareevaluatedinthe_</sup> _chunk-level world model T_ 1<sup>_k_(</sup><sup>_s′|s,_˜</sup><sup>_a_)</sup><sup>_andT k_</sup> 2<sup>(</sup><sup>_s′|s,_˜</sup><sup>_a_)</sup><sup>_respectively._</sup> _Assume we run a branched rollout of length n with chunk size k. Before the branch (”pre” branch), we assume that the expected total variation divergence of dynamics is bounded as_ max _t_ E _s∼dπt_ 1<sup>_k_</sup> _D_ TV � _T_ 1<sup>_k,pre_</sup> ( _s_<sup>_′_</sup> _|s,_ ˜ _a_ ) _∥T_ 2<sup>_k,pre_</sup> ( _s_<sup>_′_</sup> _|s,_ ˜ _a_ )� _≤ ϵ_<sup>_k,_</sup> _m_<sup>_pre_</sup> _and after the branch as_ max _t_ E _s∼dπt_ 1<sup>_k_</sup> _D_ TV � _T_ 1<sup>_k,post_</sup> ( _s_<sup>_′_</sup> _|s,_ ˜ _a_ ) _∥T_ 2<sup>_k,post_</sup> ( _s_<sup>_′_</sup> _|s,_ ˜ _a_ )� _≤ ϵ_<sup>_post_</sup> _m_<sup>_.Likewise, the policy divergence is bounded pre-branch and_</sup> _post-branch by ϵ_<sup>_k,_</sup> _π_<sup>_pre_</sup> _and ϵ_<sup>_k,_</sup> _π_<sup>_post_</sup> _, respectively. Then, the value gap of policy π_ 1<sup>_kand π_</sup> 2<sup>_kis bounded as:_</sup> 


_Proof._ We again utilize the temporally-extended MDP _M_<sup>_k_</sup> = ( _S, A_<sup>_k_</sup> _, T,_<sup>˜</sup> ˜ _r, γ_<sup>_k_</sup> ). In this view, a branched rollout of length _n_ chunks starting from _s ∼ d_<sup>_π_</sup> 1<sup>_k_</sup> corresponds to a standard trajectory in _M_<sup>_k_</sup> with discount factor _γ_<sup>_k_</sup> , but truncated or branched. 

14 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

Similar to Equation 15 and Equation 17, we obtain 


For _t ≤ n_ , by Lemma A.1 and Lemma A.2, we have _D_ TV � _d_<sup>_π_</sup> _t_ 1<sup>_k_(</sup><sup>_s,_˜</sup><sup>_a_)</sup><sup>_∥d_</sup> _t_<sup>_π_</sup> 2<sup>_k_(</sup><sup>_s,_˜</sup><sup>_a_)</sup> � _≤ D_ TV � _d_<sup>_π_</sup> _t_ 1<sup>_k_(</sup><sup>_s_)</sup><sup>_∥d_</sup> _t_<sup>_π_</sup> 2<sup>_k_(</sup><sup>_s_)</sup> � +max _s D_ TV� _π_ 1<sup>_k_(˜</sup><sup>_a|s_)</sup><sup>_∥π_</sup> 2<sup>_k_(˜</sup><sup>_a|s_)</sup> � _≤ t_ ( _ϵ_<sup>_k,_</sup> _m_<sup>post</sup> + _ϵ_<sup>_k,_</sup> _π_<sup>post</sup> )+ _ϵ_<sup>_k,_</sup> _π_<sup>post</sup> (22) 

And for _t ≥ n_ we have 


Combined the results above, we have 


Simplify the inequality above, finally we have 

# **B. Theoretical Analysis** 

**Theorem B.1** (Value Gap, Chunk-Level Policy, Step-Level World Model) **.** _Given an offline dataset D and a chunk size k ∈_ N<sup>+</sup> _, where the policy selects an action sequence_ ˜ _at_ = _at_ : _t_ + _k−_ 1 _given state st. Assume the reward per-step satisfies r_ ( _st, at_ ) _∈_ [0 _, r_ max] _, and define the k-step total variation divergence between the policy π_<sup>_k_</sup> _and the behavior policy πD_<sup>_k_</sup> _is bounded by ϵ_<sup>_k_</sup> _π_<sup>=max</sup><sup>_sD_TV</sup> � _πD_<sup>_k_(˜</sup><sup>_a|s_)</sup><sup>_∥πk_(˜</sup><sup>_a|s_)</sup> � _. Let ϵm_ = max _t_ E _s∼Dt_ � _D_ TV � _T_ ( _s_<sup>_′_</sup> _|s, a_ ) _∥T_<sup>ˆ</sup> ( _s_<sup>_′_</sup> _|s, a_ )�� _denote the expected total variation divergence of learned dynamics T_<sup>ˆ</sup> _. Then, the value gap of policy π_<sup>_k_</sup> _under the true environment and the learned world model is bounded by:_ 


### **Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

_Proof._ We decompose the value gap as follows: 


For _L_ 1, we apply Lemma A.3 with zero dynamics divergence and obtain 


For _L_ 2, we notice that the chunk-level divergence _ϵ_<sup>_k_</sup> _m_<sup>=max</sup><sup>_t_E</sup> _s∼dπt_ 1<sup>_k_</sup> � _D_ TV � _T_<sup>_k_</sup> ( _s_<sup>_′_</sup> _|s,_ ˜ _a_ ) _∥T_<sup>ˆ</sup><sup>_k_</sup> ( _s_<sup>_′_</sup> _|s,_ ˜ _a_ )�� of step-level world models _T_ and _T_<sup>ˆ</sup> is bounded by _kϵm_ , then we apply Lemma A.3 again and obtain 


Finally, combined with the _L_ 1 and _L_ 2 we have we have 

**Theorem B.2** (Value Gap, Chunk-level Policy, Chunk-level World Model, Branched Rollout) **.** _Given an offline dataset D and chunk size k ∈_ N<sup>+</sup> _, where the policy selects an action sequence a_ ˜ = _at_ : _t_ + _k−_ 1 _given state st. Suppose that policy π_<sup>_k_</sup> _is evaluated via n-chunks branched rollout in the chunk-level world model T_<sup>ˆ</sup><sup>_k_</sup> ( _s_<sup>_′_</sup> _|s,_ ˜ _a_ ) _. Assume the reward per-step satisfies r_ ( _st, at_ ) _∈_ [0 _, r_ max] _, and define the k-steps total variation divergence between the policies as ϵ_<sup>_k_</sup> _π_<sup>=</sup> max _s D_ TV� _πD_<sup>_k_(˜</sup><sup>_a|s_)</sup><sup>_∥πk_(˜</sup><sup>_a|s_)</sup> � _. Moreover, assume that the expected total variation divergence of dynamics_ **_on the current policy branched rollout_** _is defined as ϵ_<sup>_k,n_</sup> _m_<sup>= max</sup><sup>_t≤n_E</sup> _s∼d_<sup>_πk_</sup> _t,s_ 0 _∼D_ � _D_ TV � _T_<sup>_k_</sup> ( _s_<sup>_′_</sup> _|s,_ ˜ _a_ ) _∥T_<sup>ˆ</sup><sup>_k_</sup> ( _s_<sup>_′_</sup> _|s,_ ˜ _a_ )�� _. Then the value gap of policy π_<sup>_k_</sup> _under the true environment and the learned world model is bounded by:_ 


_Proof._ We define _V_<sup>ˆ</sup> ( _πD_<sup>_k, πk_)branchas the value of which executes the</sup><sup>_π_</sup> _D_<sup>_k_under the true dynamics until the branch point,</sup> then executes _π_<sup>_k_</sup> under the true dynamics for _n_ -chunks. Then we decompose the value gap as follows: 


For _L_ 1, we notice that this term only suffers from error before the branch begins, and we use Lemma B.2 with _ϵπ_<sup>_k,_pre</sup> _≤ ϵ_<sup>_k_</sup> _π_ and set all other errors to 0, then we have 


For _L_ 2, it incorporates model error under the policy _π_<sup>_k_</sup> incurred after the branch. Again we use Lemma B.2 with _ϵ_<sup>_k_</sup> _m_<sup>_′_set all</sup> other errors to 0, we obtain 


**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

Adding _L_ 1 and _L_ 2, we have 


# **C. Real-World Experiments** 

## **C.1. Hardware Setup** 

We evaluate our method on two distinct real-world robotic platforms: the Arx-X5 bimanual robot (left) and the Galaxy-R1 whole-body robot (right) as shown in figure 7. 


_Figure 7._ An illustration of real-world robots. 

**Galaxy-R1 System** The Galaxy-R1 is a high-dimensional whole-body robot featuring a 21-DoF kinematic structure, comprising dual 7-DoF arms, a 4-DoF torso, and a 3-DoF mobile base. It is equipped with a ZED 2i stereo camera (head) and two Intel RealSense D435i cameras (wrists), utilizing Galaxea G1 parallel grippers for manipulation. Data collection is performed via the JoyLo teleoperation system, which integrates 3D-printable links and Dynamixel actuators with Joy-Con controllers; the control loop operates at 100 Hz, with data synchronized and recorded at 10 Hz. 

**Arx-X5 System** The Arx-X5 is a bimanual platform with a dual-arm configuration totaling 14 DoF. Its perception suite consists of three Intel RealSense D435i RGB-D cameras providing multi-view feedback. For data collection, we employ a master-slave teleoperation setup, where two handheld master arms directly control the robot’s follower arms. The system operates at a control frequency of 15 Hz, which is sufficient for the quasi-static manipulation tasks utilized in our experiments. 

**Real-world Assets.** We present the comprehensive set of physical assets employed in our experiments in Figure 8. The left panel displays the seen objects that were accessible to the robot during the training phase, while the right panel introduces the unseen objects. 

**Task Illustration.** As illustrated in Figure 9, our evaluation suite encompasses five distinct tasks designed to test precision, deformable object manipulation, and whole-body coordination: (a) **Plug In** : A high-precision task requiring the robot to align and insert a plug into a power strip socket. (b) **Fold Towel** : A long-horizon deformable object task. Conditioned on a language prompt, the robot selects the correct towel from two options, drags it to the workspace center, performs an initial bimanual fold by grasping the top corners, executes a second fold by coordinating a left-hand hold with a right-hand grasp, 

17 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 


_Figure 8._ An illustration of real world assets. 

and finally positions the folded towel. (c) **Insert Pen** : Requires fine motor skills to pick up a pen from the table and insert it into a narrow pen holder. (d) **Pick Cup** : A pick-and-place task where the robot grasps a cup and precisely deposits it onto a target plate. (e) **Wipe Board** : A whole-body mobile manipulation task requiring the robot to execute a 90<sup>_◦_</sup> base rotation, navigate towards a whiteboard, and raise its end-effector to erase specific visual targets. 

**Data Collection and Policy Evaluation** For all tasks, our data collection strategy involves an initial phase of humanteleoperated expert demonstrations for Supervised Fine-Tuning (SFT), followed by a mix of expert and autonomous self-collected data for Reinforcement Learning (RL). Evaluation of each tasks comprises 50 trials divided into 30 seen and 20 unseen socket configurations The specific protocols for each task are as follows: • **Plug In:** The SFT dataset consists of 50 expert trajectories. For RL, we augment this with 50 self-collected on-policy trajectories. The test scenarios are specifically designed to probe the policy’s spatial generalization capabilities in high-precision alignment scenarios. 

- **Fold Towel:** We collect 60 expert trajectories for SFT, covering 3 distinct towel colors (20 trajectories each). The RL dataset combines these expert data with 50 self-collected trajectories. The evaluation protocol tests robustness against background shifts, instruction variations, and novel towel instances, assessing the model’s fundamental understanding of deformable object dynamics. 

- **Insert Pen:** The SFT phase utilizes 100 expert trajectories, while the RL phase adds 50 self-collected trajectories. We conduct evaluation focusing on high-dimensional spatial understanding, specifically examining the policy’s ability to handle object generalization and severe viewpoint disturbances during fine manipulation. 

- **Pick Cup:** Similar to the pen task, we use 100 expert trajectories for SFT and add 50 self-collected trajectories for RL. The 50 evaluation trials are designed to test visual generalization under active camera motion, specifically assessing stability when the torso and mobile base introduce significant viewpoint perturbations. 

- **Wipe Board:** We employ 100 expert trajectories for SFT and supplement this with 50 self-collected trajectories for RL. The evaluation targets robustness under partial observability and high compounding errors arising from navigation. It further tests generalization across stain variations, including color, position, and quantity. 

18 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 


_Figure 9._ An illustration of real world tasks. We test VLA-MBPO on bimanual and whole-body robots. 

19 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

# **D. Implementation Details** 

**Causal Attention Mask Implementation** Figure 10 illustrates the design of our unified causal attention mask, which governs the information flow between multi-modal tokens during training. The sequence integrates visual observations, action sequences and text instructions. The token sequence consists of ViT and VAE features. ViT represents high-level semantic features extracted by the vision encoder to provide semantic grounding, while VAE denotes the compressed latent codes used for high-fidelity image reconstruction. The sequence is further structured by control tokens such as ”Action Chunk” (representing the robot’s discrete control signals) and task-specific prompts. We present 

**Prompt Engineering** To align the model’s generation with specific task requirements, we utilize structured text prompts for both world model and reward model prediction. The exact prompt templates are detailed below. 

- **World Model Prompt.** We instruct the model to act as a physical simulator. The input integrates the history of observations with a discrete action sequence, where the action sequence is normalized into integer arrays representing joint positions and gripper states for each timestep (e.g., [111, 113, ...]). 

   - _“You are now acting as a_ **_world model_** _that simulates robot manipulation task execution. Your task is to predict the_ **_next frame of visual observation_** _, given the following inputs: (1) Multiple current observation images from the robot’s cameras (head and wrist); (2) An action sequence describing the manipulation to execute; (3) Optionally, the next frame from the head camera (for predicting wrist camera views). You will receive images from different camera viewpoints and need to predict the next frame according to the provided action sequence and instruction.”_ 

Following this system instruction, the model receives the action chunk and the specific generation command, for example: "... Step 9: [124, 34, 127, 133, 241, 129, 0]. Predict next head camera view according to the current observation and action." 

- **Reward Model Prompt.** For the reward model, we leverage a pre-trained VLM as a success detector. We enforce a strict binary output format (Yes or No). 

   - _“You are a vision-language model with advanced reasoning abilities. Your task is to carefully observe the image and determine whether the task is successfully completed._ 

**_Environment description:_** _You are observing a robot workspace from the LIBERO dataset. The robot can manipulate objects (pick, place, arrange) in the scene._ 

**_Guidelines:_** _Carefully examine the state of objects. Check if the goal state matches the task description. Consider spatial arrangement._ 

**_Response format:_** _Answer with ”Yes.” if the task is successfully completed. Answer with ”No.” if the task is not yet completed or failed. Your response must be either ”Yes.” or ”No.” without additional explanation._ 

**_Task:_** _Determine whether the task: [Task Description] is successfully completed.”_ 

**Hyperparameters.** We present the detailed training hyperparameters for the UMM-World and the downstream policy optimization in Table 4 and Table 5. Respectively. A key advantage of our framework is its stability and ease of tuning; as evidenced in Table 5, the majority of hyperparameters remain constant across all task suites. The primary adaptation required is scaling the Sample Size (and the corresponding Update to data steps) for long horizon tasks. 

_Table 4._ Hyperparameters for UMM-World. 

|**Parameters**|**Value**|
|---|---|
|lr|2e_−_5|
|Cross entropy weight|0.01|
|MSE weight|1.0|
|Max latent size|64|
|Timestep shift|4|
|Cfg interval|[0.4, 1.0]|
|Text scale|6|
|Image scale|2|


20 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 


_Figure 10._ **Causal Mask in UMM World Model during training** . VAE and ViT denote VAE features and ViT features, respectively. _t_ is the noise timestep and _t_ = 0 means no noise. 

21 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

_Table 5._ Hyperparameters for RL. 

|**Parameters**||**Liber**|**o**||**Real-World**|
|---|---|---|---|---|---|
||**Spatial**|**Object**|**Goal**|**Long**||
|Sample size|512|512|512|1280|512|
|Batch size|512|512|512|512|512|
|Rollout chunk|2|2|2|2|2|
|Actor lr|5e_−_6|5e_−_6|5e_−_6|5e_−_6|5e_−_6|
|Critic lr|1e_−_4|1e_−_4|1e_−_4|1e_−_4|1e_−_4|
|Reward discount rate_γ_|0.99|0.99|0.99|0.99|0.99|
|GAE_λ_|0.95|0.95|0.95|0.95|0.95|
|Clip ratio_ϵ_|0.1|0.1|0.1|0.1|0.1|
|Action chunk_H_|10|10|10|10|10|
|Denoise steps|3|3|3|3|3|
|Noise level|0.5|0.5|0.5|0.5|0.5|
|Update to data|20|20|20|50|20|


_Figure 11._ Qualitative comparison of UMM-World prediction against Ground Truth across both simulated (LIBERO) and real-world tasks. 

22 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

# **E. Additional Results** 

## **E.1. World Model Generation Visualization** 

**Visualization Analysis** Figure 11 provides a qualitative comparison between the generated trajectories of UMM-World and the ground truth. The visualization is organized with the initial observation in the leftmost column, followed by the predicted sequence spanning 20 steps for simulated tasks and 40 steps for real-world scenarios. 


_Figure 12._ An illustration showing spatial consistency of UMM-World generation. 

**Case Study** Figure 12 illustrates UMM-World’s internal coherence through two distinct qualitative examples spanning two consecutive 20-step chunks. In the left deformable object included task, the model exhibits strong geometric consistency. Although the predicted head view diverges from the ground truth regarding the right hand’s position, the generated wrist view aligns with the predicted head view rather than the ground truth. This confirms that our interleaved decoding strategy enforces strict spatial coherence, ensuring the body posture remains consistent across viewpoints. The right example highlights the model’s adherence to physical laws. While the ground truth shows the robot erasing the entire word in the first chunk, the model predicts a variation where the letter E’ remains un-erased. Crucially, both the generated head and wrist views consistently depict this incomplete’ state. This demonstrates that the model maintains a unified physical reality—correctly reflecting the remaining ink across all sensors—rather than simply memorizing the expert’s outcome. 

## **E.2. Failure Case Analysis** 

1. **Partially Observable.** As illustrated in Figure 13, we analyze UMM-World’s failure cases from inherent partial observability in embodied control. The left panel demonstrates a failure during the arm lifting phase in the _Wipe Board_ task. As the manipulator moves out of the head camera’s field of view, the model fails to render the arm in the predicted head view. Although the wrist camera provides local visual feedback, the model struggles to infer the global arm posture solely from these local cues without explicit kinematic history in the main view, leading to a disappearance of the robot arm in the generated future.The right panel depicts a failure during the navigation phase involving significant viewpoint changes. When the robot rotates its base to face the whiteboard, the target object enters the field of view for the first time. Since this region was never present in the condition observations, the world model cannot hallucinate the correct geometric structure and texture of the unseen environment from nothing. 


_Figure 13._ An illustration of failure case caused of partial observability. 

2. **Large Physical Movements.** As shown in Figure 14, we observe generation failures when the target sequence involves excessive physical movement or state changes. The left panel illustrates a _Wipe Board_ sequence characterized by significant end-effector displacement. Due to the difficulty of modeling such large-scale motion in a single shot, the 

23 

**Towards Practical World Model-based Reinforcement Learning for Vision-Language-Action Models** 

model suffers from motion collapse; instead of capturing the extensive trajectory, it conservatively predicts minimal change, resulting in a generated arm that appears nearly static despite the actual dynamic motion. Similarly, in the _Fold Towel_ task (right panel), the sequence encompasses drastic configuration changes inherent to interacting with deformable objects. The complexity and stochasticity of these large-scale non-rigid transitions prove difficult to bridge accurately. Consequently, the model succumbs to hallucination, generating physically implausible towel configurations rather than correctly tracking the substantial deformation process. 


_Figure 14._ An illustration of failure cases caused by large prediction horizon. 

# **F. Computational Resources** 

All experiments were conducted on 8 NVIDIA H100 GPUs. The computational cost for UMM-World training on the collected dataset requires approximately 7-8 hours. The computational cost for policy optimization typically completes in approximately 4-6 hours under the standard interaction budget. 

24 

