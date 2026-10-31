---
title: "Reinforcement Learning for Large Model: A Survey"
date: "2025-08-11"
authors: "Weijia Wu; Chen Gao; Joya Chen; Kevin Qinghong Lin; Qingwei Meng; Yiming Zhang"
url: https://arxiv.org/abs/2508.08189
pdf: https://arxiv.org/pdf/2508.08189
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2508.08189)** / [論文ページ](https://arxiv.org/abs/2508.08189)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

**1** 

# Reinforcement Learning for Large Model: A Survey 

Weijia Wu<sup>1</sup> , Chen Gao<sup>1</sup> , Joya Chen<sup>1</sup> , Kevin Qinghong Lin<sup>1</sup> , Qingwei Meng<sup>2</sup> , Yiming Zhang<sup>3</sup> 

, Yuke Qiu<sup>2</sup> , Hong Zhou<sup>2</sup> , Mike Zheng Shou<sup>1</sup><sup>_‡_</sup> 

1National University of Singapore 

2Zhejiang University 

3The Chinese University of Hong Kong 

**Abstract** —Recent advances at the intersection of reinforcement learning (RL) and visual intelligence have enabled agents that not only perceive complex visual scenes but also reason, generate, and act within them. This survey offers a critical and up-to-date synthesis of the field. We first formalize visual RL problems and trace the evolution of policy-optimization strategies from RLHF to verifiable reward paradigms, and from Proximal Policy Optimization to Group Relative Policy Optimization. We then organize more than 250 representative works into four thematic pillars: multi-modal large language models, visual generation, unified model frameworks, and vision-language-action models. For each pillar we examine algorithmic design, reward engineering, benchmark progress, and we distill trends such as curriculum-driven training, preference-aligned diffusion, and unified reward modeling. Finally, we review evaluation protocols spanning set-level fidelity, sample-level preference, and state-level stability, and we identify open challenges that include sample efficiency, generalization, and safe deployment. Our goal is to provide researchers and practitioners with a coherent map of the rapidly expanding landscape of visual RL and to highlight promising directions for future inquiry. Resources are available at: Visual RL. 

**Index Terms** —Reinforcement Learning, Multimodal Model, Survey, Visual Generation. 

✦ 

## **CONTENTS** 

|||3.4|Vision Language Action Models . . . . .|9|
|---|---|---|---|---|
||||3.4.1<br>GUI Automation . . . . . . . .|9|
|2|||3.4.2<br>Visual Navigation . . . . . . .|10|
|2|||3.4.3<br>Visual Manipulation . . . . . .|10|
|2<br>|**4**|**Metrics **|**and Benchmarks**|10|
|3<br>||4.1|Formalizing Metric Granularity . . . . .|11|
|3<br>||4.2|Evaluation of Multi-Modal Large Lan-||
|4|||guage Models . . . . . . . . . . . . . . .|12|
|||4.3|Evaluation of Visual Generation Models|12|
|4<br>||4.4|Evaluation of Unified Models . . . . . .|12|
|5<br>||4.5|Evaluation of Vision Language Action||
|5|||Models . . . . . . . . . . . . . . . . . . .|13|
|6||4.6|Benchmarks . . . . . . . . . . . . . . . .|13|
||**5**|**Challen**|**ges and Future Works**|14|
|6<br>||5.1|Effective Reasoning: Balancing Depth||
|6<br>|||and Efficiency . . . . . . . . . . . . . . .|14|
|6<br>||5.2|Long-Horizon RL in VLA<br>. . . . . . . .|14|
|7<br>||5.3|RL for Thinking with Vision . . . . . . .|14|
|7<br>||5.4|Reward Model Design for Visual Gener-||
|8<br>8|||<br>ation<br>. . . . . . . . . . . . . . . . . . . .|14|
|8|**6**|**Conclus**|**ion**|14|
|8|||||
|9|**Ref**|**erences**||15|


### **Introduction** 

- **2 Preliminary: Reinforcement Learning in LLM** 2 2.1 Notation and Problem Formulation . . . 2 2.2 Alignment Paradigms . . . . . . . . . . 3 2.2.1 RL from Human Feedback . . 3 2.2.2 Direct Preference Optimization 4 2.2.3 Reinforcement Learning with Verifiable Rewards . . . . . . . 4 

- 2.3 Policy-Optimization Algorithms . . . . . 5 2.3.1 Proximal Policy Optimization 5 2.3.2 Group Relative Policy Optimization . . . . . . . . . . . . 6 

- **3 Reinforcement Learning in Vision** 6 3.1 Multi-Modal Large Language Models . 6 3.1.1 Conventional RL-based MLLMs 6 3.1.2 Spatial and 3D Perception . . 7 3.1.3 Image Reasoning . . . . . . . 7 3.1.4 Video Reasoning . . . . . . . . 8 

- 3.2 Visual Generation . . . . . . . . . . . . . 8 3.2.1 Image Generation . . . . . . . 8 3.2.2 Video Generation . . . . . . . 8 3.2.3 3D Generation . . . . . . . . . 9 3.2.4 Reward Design and Preference Modeling for Visual Generation . . . . . . . . . . . . . 9 

- 3.3 Unified Model . . . . . . . . . . . . . . . 9 3.3.1 Unified RL . . . . . . . . . . . 9 3.3.2 Task specific RL . . . . . . . . 9 

_Corresponding author (_<sup>_‡_</sup> _) : Mike Zheng Shou (mikeshou@nus.edu.sg)._ 

2 

## **1 INTRODUCTION** 

Reinforcement Learning (RL) has achieved remarkable successes in the field of Large Language Models (LLMs) [1], [2], most notably through paradigms like Reinforcement Learning from Human Feedback (RLHF) [3] and innovative frameworks such as DeepSeek-R1 [4]. These methodologies have significantly enhanced the capabilities of LLMs, aligning generated outputs closely with human preferences and enabling nuanced, complex reasoning and interaction capabilities previously unattainable through supervised learning alone. 

In recent years, inspired by these remarkable achievements from LLM, there has been an explosive interest in extending the RL methodologies that proved successful for LLMs to multimodal large models, including VisionLanguage Models (VLM) [5], [6], [7], Vision-Language-Action models (VLA) [8], [9], [10], [11], diffusion-based visual generation models [12], [13], [14], and unified multimodal frameworks [15], [16], [17], as shown in Figure 1. Multimodal models such as Gemini 2.5 [18] have leveraged RL to align visual-textual reasoning processes and produce outputs with higher semantic coherence and alignment with human judgments. Concurrently, VLA models integrating vision and language with action-oriented outputs have adopted RL to optimize complex sequential decision-making processes in interactive environments, significantly improving taskspecific performance in GUI automation [11], [19], robotic manipulation [8], and embodied navigation [20]. The rapid advancement of diffusion-based generative models has further spurred this RL-driven innovation wave. Works like ImageReward [21] have introduced reinforcement learning to enhance the semantic alignment and visual quality of generative outputs, refining diffusion-based generation through iterative feedback mechanisms derived from human preferences or automated reward critics. Moreover, unified models that blend multiple tasks, _i.e.,_ understanding, and generation, into single architectures [15], [22] have increasingly relied on RLdriven fine-tuning, achieving generalization and task transfer previously considered challenging. Despite the substantial progress in integrating reinforcement learning with multimodal large language models, several core challenges remain. These include stabilizing policy optimization under complex reward signals, managing high-dimensional and diverse visual inputs, and designing scalable reward functions that support long-horizon decision-making. Addressing these challenges necessitates methodological innovations in both algorithmic design and evaluation protocols. 

In this survey, we present a comprehensive synthesis of recent advances in visual reinforcement learning within the context of multimodal large models, with a focus on the surge of research activity since 2024. We begin by revisiting foundational RL successes in language models, such as RLHF [3] and DeepSeek-R1 [4], which have laid the groundwork for multimodal adaptation. Subsequently, we discuss how these strategies have evolved in the visual domain, categorizing over 200 representative works into four key domains: (i) 

multimodal large language models, (ii) visual generation, (iii) unified RL frameworks, and (iv) vision-language-action agents, as shown in Figure 1. Within each category, we analyze key developments in algorithmic formulations, reward modeling, and benchmarking methodologies. Finally, we identify open challenges and future directions, highlighting the need for more efficient multimodal reasoning, robust long-horizon learning strategies for VLA tasks, and scalable, high-fidelity reward signals tailored to visual generation. Through this comprehensive overview, we offer a structured overview of visual reinforcement learning to support future research and practical deployment in this rapidly evolving field. 

Our key contributions are as follows: 

- We provide a systematic and up-to-date survey of over 200 visual reinforcement learning studies, encompassing MLLMs, visual generation, unified models, and visionlanguage-action agents. 

- We analyze advances in policy optimization, reward modeling, and benchmarking across subfields, revealing key challenges and future directions: such as reward design in visual generation and the lack of intermediate supervision in reasoning and VLA tasks. 

- We introduce a principled taxonomy of Visual RL methods based on metric granularity and reward supervision, including three reward paradigms for image generation. This framework clarifies the design trade-offs across domains and offers actionable insights for selecting and developing RL strategies. 

## **2 PRELIMINARY: REINFORCEMENT LEARNING IN LLM** 

This section lays the foundation for the RL of multi-modal models. We first formalize the notation (§2.1), casting text and image generation as a Markov Decision Process. Next, we examine three alignment paradigms (§2.2): _RL from Human Feedback_ (RLHF), _Group-Relative Policy Optimization_ (GRPO), and _Reinforcement Learning with Verifiable Rewards_ (RLVR), each aligning policies via human preferences or deterministic checks. Finally, §2.3 reviews the core policy gradient methods (PPO, GRPO) and their adaptations to visual reasoning and generation. 

### **2.1 Notation and Problem Formulation** 

We cast text- or image-generation as an episodic Markov decision process. We treat the user _prompt p_ as the **initial state** _s_ 0 = _p_ . At timestep _t_ , the state is the prompt plus all previously generated actions: 


A _continuation_ is the full action sequence _{a_ 1 _, . . . , aT }_ , where each token _at ∈A_ is sampled autoregressively from the policy: 


In words, the prompt anchors the state sequence, and each new action is chosen in the context of that prompt and the tokens already produced. 

3 


Fig. 1: **Timeline of Representative Visual Reinforcement Learning Models.** The figure presents a chronological overview of key Visual RL models from 2023 to 2025, organized into four tracks: Multimodal LLM, Visual Generation, Unified Models, and VLA Models. 

A fixed reference model ( _e.g.,_ the supervised fine-tuned checkpoint) is denoted _π_ ref. Human preferences are distilled into a scalar reward model _Rϕ_ ( _p, y_ ), replacing the reward from the unknown environment. We write _ρt_ ( _θ_ ) = _πθ_ ( _at | st_ )� _πθ_ old( _at | st_ ) for the importance ratio between new and behavior policies. _A_<sup>ˆ</sup> _t_ is used to denote the advantage estimate. PPO reduces the variance of _A_<sup>ˆ</sup> _t_ with a learned critic _V_<sup>ˆ</sup> _ψ_ , whereas GRPO replaces the critic by a _group-relative_ baseline computed from a set _O_ = _{ai}i_<sup>_G_</sup> =1<sup>of continuations</sup> that share the same prompt. All two algorithms add a KL regulariser KL� _πθ_ ( _·| p_ ) _∥π_ ref( _·| p_ )� weighted by _β_ to keep the updated policy close to the reference. Unless stated otherwise, expectations E[ _·_ ] are over prompts _p ∼D_ and continuations drawn from the specified policy. 

### **2.2 Alignment Paradigms** 

### _2.2.1 RL from Human Feedback_ 

RLHF [3] extends the underlying MDP with _pairwise preference data_ curated from human annotators. Each preference example is a triple ( _p, y_ A _, y_ B), where _p_ is the prompt (or state sequence) and ( _y_ A _, y_ B) are two candidate continuations (trajectories, images, _etc._ ); the label _y ∈{_ 0 _,_ 1 _}_ records which continuation is preferred, as shown in Figure 2. 

**Reward-model learning.** A scalar reward model _Rϕ_ is trained to reproduce the pairwise ordering via a 

Bradley–Terry likelihood: 


where _σ_ ( _·_ ) is the logistic function. After convergence, _Rϕ_ provides a _dense, differentiable_ proxy for human preference. 

**Policy optimization.** The policy _πθ_ is finally fine-tuned by maximizing (i) the learned reward, (ii) a KL penalty that keeps the policy close to the supervised-fine-tuned baseline _π_ SFT, and (iii) an _optional_ log-likelihood regulariser on the original pre-training distribution, as introduced in InstructGPT [3]<sup>1</sup> : 


In practice, the first two terms are optimised with KLregularised PPO over minibatches of sampled continuations, while the third term adds the pre-training gradients (“PPOptx” in [3]) to mitigate performance regressions on the original corpus. 

**Three-stage recipe.** Most modern RLHF pipelines follow the three-stage recipe, as shown in Figure 2 (a). Step 1: Collect 

1. The coefficients _β_ and _γ_ respectively control the strength of the KL penalty and the pre-training log-likelihood term. Setting _γ_ =0 recovers the standard PPO objective. 

4 

TABLE 1: **Glossary of Symbols for Visual Reinforcement Learning.** It consolidates the notation that recurs across Sections §2.1–§2.3, with the rightmost column pointing to each appearance of the symbol. 

|**Symbol**|**Alias**|**Meaning**|**Appears in**|
|---|---|---|---|
|_p_|prompt|User prompt (initial state)|§2.1, §2.2.1, §2.3.1, §2.3.2|
|_at_|action|Token / pixel patch / diffusion noise at step_t_|§2.1, Eq. (8), §2.3.2|
|_y_|traj|Full continuation(_a_1_, . . . , aT_)|§2.1, §2.2.1, §2.2.3|
|_yi_|continuation|_i_-th continuation in a GRPO group|§2.1, §2.3.2|
|_st_|state|Prompt plus previously generated actions|§2.1, §2.3.1, §2.3.2|
|_πθ_|policy|Trainable model (current parameters)|§2.1, §2.2.1, §2.2.2, §2.3.1, §2.3.2|
|_πθ_old|behaviour policy|Frozen policy that produced current batch|Eq. (10), §2.3.2|
|_π_SFT|SFT baseline|Supervised-fine-tuned checkpoint|§2.2.1, §2.3.1|
|_π_ref|reference|Policy used in KL regulariser|§2.1, §2.3.1, §2.3.2|
|_ρt_|ratio|Importance weight_πθ/πθ_old|Eq. (10), §2.3.2|
|_Vψ_<br>|critic|Value network predicting future return|§2.3.1|
|ˆ<br>_At_<br>|advantage|GAE advantage (token-level)|Eq. (9), §2.3.1|
|ˆ<br>_Ai,t_|group adv.|Group-normalised advantage (GRPO)|Eq. (12), §2.3.2|
|_O_ =_{at}_<sup>_G_</sup><br>1|group|Set of_G_continuations for one prompt at_t_timestep|§2.1, §2.3.2|
|_G_|group size|Number of continuations per prompt|§2.1, §2.3.2|
|_rϕ_(_st, at_)|token reward|Immediate reward from frozen preference model|§2.3.1|
|_ri_|token reward|Reward of the_i_-th continuation in group|§2.3.2|
|mean(_·_)|mean|Group reward mean in GRPO|§2.3.2|
|std(_·_)|std|Group reward standard deviation in GRPO|§2.3.2|
|_Rϕ_(_p, y_)|RM|Sequence-level reward model (RLHF)|§2.2.1|
|_ϵ_|clip|PPO clipping threshold|Eq. (10), §2.3.2|
|_β_|KL weight|Weight balancing KL vs. reward|Eq. (8), §2.2.1, §2.3.2|
|KL(_·∥·_)|KL|Divergence between policy and reference|§2.2.1, §2.3.1, §2.3.2|
|_D_KL(_p_)|est. KL|Token-average KL estimator in GRPO|Eq. (13)|


demonstration data, and train a supervised policy; Step 2: Collect comparison data, and train a reward model; Step 3: Optimize a policy _πθ_ against the reward model using PPO. The paradigm was _pioneered_ by Christiano et al., [23], who trained Atari and robotic agents from pairwise human preferences. Ouyang et al., [3] later _scaled_ the recipe to large language models (InstructGPT) by coupling preference modeling with PPO. For vision, reward models such as ImageReward [21] and Human Preference Score (HPS) [24] supply dense aesthetic signals that guide text-to-image diffusion and related tasks. 

where the log-odds gap is: 


The logistic function _σ_ ( _z_ ) = 1 _/_ (1 + _e_<sup>_−z_</sup> ) turns the gap into a binary-classification loss; training proceeds with standard maximum-likelihood gradients, no reward model, value network, or importance sampling is required. 

### _2.2.2 Direct Preference Optimization_ 

Direct Preference Optimisation (DPO) [2] takes exactly the _same_ pairwise-preference data as RLHF but removes the intermediate reward-model and RL loop. Instead, it derives a _closed-form, supervised_ objective that implicitly enforces a KL constraint to a frozen reference policy _π_ ref, as shown in Figure 2 (b). 

**Closed-form objective.** For every prompt _p_ annotators rank two continuations � _y_ A _, y_ B� and order them so that _y_ A is the preferred continuation (“winner”) and _y_ B the nonpreferred one (“loser”). Thus the dataset consists of triples ( _p, y_ A _, y_ B) _∼D_ . Let _π_ ref be a frozen reference policy (e.g., the SFT checkpoint) and let _β >_ 0 be a temperature hyperparameter. DPO minimizes: 


_2.2.3 Reinforcement Learning with Verifiable Rewards_ Reinforcement Learning with Verifiable Rewards (RLVR) eliminates the subjectivity and data-collection cost of RLHF by replacing pairwise human preferences with _deterministic, programmatically checkable_ reward signals _v_ : ( _p, y_ ) _�→ {_ 0 _,_ 1 _, . . . , K}_ . Typical examples include `pass` _/_ `fail` unit tests for code synthesis, exact-match answers in mathematics, IoU/DICE thresholds for segmentation, or formal outputformat validators ( _e.g.,_ LeetCode compiler). Because the reward is generated _online_ by execution or metric evaluation, RLVR removes both (i) the reward-model training stage of RLHF and (ii) the contrastive surrogate loss of DPO, while still enabling substantial policy improvements beyond supervised learning [4], [25], [26], as shown in Figure 2 (c). 

**Verifiable reward.** For a prompt (state) _p_ and a sampled continuation _y_ , a verifier returns: 


_e.g.,_ “ `pass` ” if the generated program solves all hidden tests. The same idea applies to vision: a generated mask that 

5 


Fig. 2: **Three Alignment Paradigms for Reinforcement Learning.** (a) RLHF learns a reward model from human preference data and optimizes the policy via PPO. (b) DPO removes the reward model and directly optimizes a contrastive objective against a frozen reference. (c) RLVR replaces subjective preferences with deterministic verifiable signals and trains the policy using GRPO. 

attains IoU _≥_ 0 _._ 9 with ground truth, or an image whose CLIP similarity exceeds a hard threshold can be awarded _r_ = 1. Current most RLVR systems ( _e.g.,_ DeepSeekMath, Deepseek-R1) adopt GRPO [25] (see Equ. 12) and standard KL regularization to train the policy model. 

RLVR therefore follows a concise two-stage pipeline. Step 1: Supervised policy pre-training on demonstrations _{_ ( _p, y_ ) _}_ , producing the initial _π_ SFT. Step 2: RL fine-tuning with GRPO/PPO against the on-the-fly verifiable reward _v_ ( _p, y_ ), optionally mixing in a small percentage of teacher-forced SFT updates to stabilise training. 

### **2.3 Policy-Optimization Algorithms** 

### _2.3.1 Proximal Policy Optimization_ 

Proximal Policy Optimization (PPO) [27] is a first order trust region method that updates the policy _πθ_ while _staying close to the previous policy πθ_ old at every step, as shown in Figure 3 (a). In text- or image-generation problems we treat a prompt _p_ as the initial state _s_ 0 and the continuation _{a_ 1 _, . . . , aT }_ as the trajectory. Define the importance-sampling ratio _ρt_ ( _θ_ ) and immediate reward _rϕ_ : 

- **Importance–sampling ratio** 


Fig. 3: **Two Representative Policy Optimization Algorithms for LLM.** PPO (a) uses a learned value model _Vψ_ for advantage estimation and injects the KL penalty at each token. GRPO (b) removes the value model, computes groupnormalized advantages _A_<sup>ˆ</sup> _i,t_ across _G_ continuations, and applies an explicit prompt-level KL penalty. 

which re-weights the gradient estimate from the behavior policy to the updated policy. 

- **Immediate reward** _rϕ_ ( _st, at_ ), provided by a _frozen_ reward model _rϕ_ that has been pre-trained to approximate human preference. 

- **Value baseline** _Vψ_ ( _st_ ), produced by a _learned_ value network _Vψ_ that regresses the expected discounted return from state _st_ . 

6 

With the KL-regularised reward between the policy model and reference model, _rt_<sup>PPO</sup> can be defined: 


where the KL term(latter item) keeps the updated policy _πθ_ from drifting too far from the frozen reference _π_ ref. _β_ balances exploration (via KL proximity to the frozen reference model _π_ ref) against exploitation of the reward model. A larger _β_ implies stricter proximity and thus safer but potentially slower learning. Then the generalized advantage estimator (GAE) [28] produces _A_<sup>ˆ</sup> _t_ : 


where GAE computes advantage values by exponentially weighting multi-step reward estimates, providing a smooth trade-off between low-variance learning and high-variance Monte Carlo returns. 

The surrogate objective maximized by PPO is then: 


where the hyper-parameter _ϵ ∈_ (0 _,_ 1) controls the width of the trust region. Accurate and low-variance _A_<sup>ˆ</sup> _t_ estimates are therefore critical, they direct each policy update and ultimately determine the stability and sample efficiency of PPO. 

### _2.3.2 Group Relative Policy Optimization_ 

Group Relative Policy Optimisation (GRPO) [25] extends PPO by discarding the learned value (critic) network and replacing it with a _group-relative_ baseline computed from multiple outputs sampled for the same prompt. This design markedly reduces memory consumption while aligning the advantage estimator with the comparison-based reward model, as shown in Figure 3 (b). 

**Group Relative Baseline.** For each prompt _p_ , we sample a group of _G_ full continuations _a_ 1 _, . . . , aG ∼ πθ_ ( _· | p_ ), where each continuation _a·,t_ = ( _a_ 1 _,t, . . . , aG,t_ ) is a sequence of tokens indexed by timestep _t_ . The frozen reward model _rϕ_ ( _p, ai,t_ ) then assigns a scalar score to each token _ai,t_ conditioned on the prompt. These sequence level rewards are then normalized across the group to compute a grouprelative advantage signal: 


where mean( _·_ ) and std( _·_ ) denote the mean and standard deviation functions used to compute the group relative advantage. The same _A_<sup>ˆ</sup> _i_ is reused for every token _ai,t_ in the continuation, producing the clipped surrogate: 


where _ρi,t_ = _πθ_ ( _ai,t | si,t_ )� _πθ_ old( _ai,t | si,t_ ) _._ The explicit KL penalty _D_ KL( _·_ ) keeps _πθ_ near the reference _π_ ref, while the 

group-relative advantage _A_<sup>ˆ</sup> _i_ replaces the value baseline _Vψ_ , roughly halving memory and compute yet retaining a lowvariance learning signal. 

**Prompt-level KL estimator.** Instead of injecting a tokenwise penalty into the reward (as PPO does with _β_ log _π_<sup>_<u>π</u>_</sup> ref<sup>_<u>θ</u>_),</sup> GRPO adds a _separate_ prompt-level regulariser. With the _G_ sampled continuations we form an unbiased token-average estimate: 


which measures how far the current policy drifts from the frozen reference _π_ ref over the _whole_ continuation. 

Relative to PPO in Equ. (10), GRPO introduces two key improvements: _1) Eliminates the value (critic) network._ Variance reduction is achieved by a _group-relative_ baseline, leading to lower memory footprint and fewer hyper-parameters. _2) Separates the KL loss channel._ The KL divergence is optimized as an explicit regulariser rather than folded into the advantage, yielding a transparent trade-off between reward maximization and reference anchoring. 

## **3 REINFORCEMENT LEARNING IN VISION** 

### **3.1 Multi-Modal Large Language Models** 

We categorize the works into four coherent groups, each defined by shared RL-driven objectives and internal reasoning mechanisms. 

### _3.1.1 Conventional RL-based MLLMs_ 

We refer to _conventional RL-based MLLMs_ as approaches that apply reinforcement learning primarily to _align_ a vision–language backbone with _verifiable, task-level rewards_ , without explicitly modeling multi-step chain-of-thought reasoning. Typical works RePIC [29], GoalLadder [30], DriveR1 [31] and VLM-R1 [32] replace preference models with _deterministic validators_ ( _e.g.,_ exact-match, IoU, BLEU) and optimize the policy by GRPO/PPO variants under a KL regulariser. This design yields stable value-free training, improves zero-shot robustness on captioning, grounding and autonomous-driving benchmarks, and substantially reduces the annotation cost typically incurred by supervised finetuning. 

Recent extensions demonstrate the flexibility of this paradigm. GRPO-CARE [33] introduces consistency-aware group normalization to mitigate reward variance, while Q-Ponder [34] adds a pondering controller. From a data perspective, MoDoMoDo formulates a multi-domain mixture optimization that predicts reward distributions and selects optimal curricula [35]; V-Triune further unifies perception and reasoning tasks within a single triple-objective pipeline, empirically validating that rule-based RL scales to diverse visual signals [36]. Collectively, these studies indicate that (i) verifiable rewards can serve as a low-cost alternative to human feedback, (ii) group-relative objectives offer higher training stability than token-level PPO on heterogeneous visual tasks, and (iii) curriculum or data-mixture scheduling is emerging as a key ingredient for broad generalization. 

7 


Fig. 4: **Overall taxonomy of reinforcement-learning research in vision.** The chart groups existing work by high-level domain (MLLMs, visual generation, unified models, and vision-language action agents) and then by finer-grained tasks, illustrating representative papers for each branch. 

### _3.1.2 Spatial and 3D Perception_ 

**2D perception.** Perception centric works applies RL to sharpen object detection, segmentation and grounding without engaging in lengthy chain–of–thought reasoning. OmniR1 [54] introduces a two-system (global–local) GRPO pipeline that verifies predictions via rule-based metrics, yielding notable improvements on region-level benchmarks and emotion-recognition tasks. DIP-R1 [55] further decomposes perception into step-wise “inspect _→_ observe _→_ act” cycles, where each stage receives deterministic IoU or countingbased rewards to boost fine-grained detection. PerceptionR1 [59] revisits the effect of GRPO on a spectrum of detection and OCR datasets. Complementing these, VisRL [60] frames intention-guided focus selection as an RL sub-policy, eliminating expensive region labels and consistently outperforming supervised strong baselines on visual grounding tasks. 

**3D perception.** Beyond 2-D, several studies leverage RL to align multimodal models with physically consistent 3- D layouts. MetaSpatial [56] employs rendered depth/IoU rewards to refine spatial reasoning for AR/VR scene generation, whereas Scene-R1 [58] couples video-grounded snippet selection with a two-stage grounding policy to learn 3-D scene structure without point-level supervision. At molecular scale, BindGPT [57] treats atom placement as sequential actions and uses binding-affinity estimators as verifiable rewards, demonstrating the scalability of perception-focused RL to 3-D biochemical design. Collec- 

tively, these approaches underscore a common recipe: (i) formulate detection/segmentation/3-D alignment as Markov decision problems, (ii) craft deterministic spatial rewards ( _e.g.,_ IoU, depth consistency, binding energy), and (iii) finetune pretrained VLM backbones via GRPO/PPO for stable perception enhancement—thereby differentiating themselves from reasoning-oriented RL variants. 

### _3.1.3 Image Reasoning_ 

Thinking about Images methods enhance multimodal reasoning by _verbalising_ observations of a static picture before producing an answer, but the visual content itself is not modified during inference. By contrast, Thinking with Images elevates the picture to an _active, external workspace_ : models iteratively _generate, crop, highlight, sketch or insert explicit visual annotations_ as tokens in their chain-of-thought, thereby aligning linguistic logic with grounded visual evidence. 

**Think about Image** . Early think about image works for spatial VQA employs view-consistent or transformationinvariant objectives, such as SVQA-R1 [65] and STARR1 [69]. VL-GenRM [66] and RACRO [67] refine preference data or caption rewards to curb hallucinations. Benchmarkoriented efforts such as EasyARC [68] offer procedurally generated, fully verifiable tasks that suit outcome-based reinforcement learning. To mitigate shortcut reliance and improve generality, Visionary-R1 [70] enforces image interpretation before reasoning, whereas UniVG-R1 [71] unifies referring, captioning, and detection by coupling a grounding 

8 

corpus with GRPO fine-tuning. Extensions such as EchoInkR1 [72] further enrich visual reasoning by integrating audio–visual synchrony under GRPO optimization. Meanwhile, curriculum-driven frameworks—WeThink, G1, GThinker, and Observe-R1 progressively increase task complexity or introduce re-thinking cues ( _e.g.,_ difficulty ladders, multimodal format constraints) to cultivate deeper and more structured reasoning capabilities in MLLMs. These methods show that language only RL with well-designed visual correctness rewards significantly improves model accuracy, robustness, and out-of-distribution performance. 

**Think with Image.** Early think with image works grounds reasoning via discrete _region–level_ operations: GRIT [82] interleaves bounding-box tokens with language and trains under GRPO to maximize both answer correctness and box fidelity, while VILASR [83] generalizes this idea to multi-view and video settings, enforcing cross-view spatial consistency. Ground-R1 [85] and BRPO [84] adopt twostage pipelines that first highlight evidence regions (via IoU-based or reflection rewards) before verbal reasoning. A complementary thread explores pixel-space or sequencelevel manipulation. Visual Planning [81] replaces text chains with imagined image roll-outs rewarded by downstream task success; Pixel Reasoner [86] augments the action space with crop, erase and paint primitives and balances exploration through curiosity-driven rewards, whereas DeepEyes [6] shows that end-to-end RL can spontaneously induce such visual thinking behaviours. Finally, TACO [87] introduces a think–answer consistency objective that resamples long visual–verbal chains until their intermediate edits align with the final answer. Together, these systems demonstrate that explicitly generating or editing visual artefacts during reasoning optimized via GRPO or R1-style outcome RL—yields more faithful, interpretable and robust image understanding than language only approaches. 

### _3.1.4 Video Reasoning_ 

Video reasoning extends the capabilities of MLLMs to process temporal dynamics, requiring not only spatial perception but also sequential understanding and causal inference. Recent works in this domain have proposed diverse approaches to tackle complex reasoning over video inputs. For instance, VQ-Insight [95] introduces a hierarchical reward design and self-consistency voting mechanism tailored to the question–answering process over long videos. TW-GRPO [96] combines token wise credit assignment with GRPO-style optimization to improve fine-grained temporal alignment between textual reasoning and video evidence. Meanwhile, several R1-style frameworks have been developed to unlock video understanding in complex real-world or egocentric settings. EgoVLM [97] and VAU-R1 [98] focus on egocentric video reasoning with visual memory and utility-based rewards. DeepVideo-R [99] integrates dense video encodings and external reward functions to supervise long-horizon reasoning. TimeMaster [100] explicitly structures temporal abstraction and reasoning via curriculum learning, while VideoR1 [101] proposes a scalable RL framework for videobased QA tasks across multiple domains. Collectively, these works highlight the importance of aligning temporal representations with language trajectories through reinforcement 

learning, paving the way for robust and generalizable video reasoning agents. 

### **3.2 Visual Generation** 

### _3.2.1 Image Generation_ 

RL for image generation models departs from the language counterpart in both _action space_ continuous diffusion steps or prompt refinements and _reward design_ , which must capture perceptual quality, text–image alignment, and subject fidelity. A first family learns an explicit _visual reward model_ : ImageReward [21] supplies human-preference scores that drive policy-gradient fine-tuning of diffusion backbones in DiffPPO [132], Dpok [116], and FocusDiff [115]. A second line bypasses reward modelling by optimising _pairwise or unary preferences_ : DDPO [13], DiffusionDPO [122], DiffusionKTO [123], and DiffusionRPO [124] treat denoising trajectories as MDPs and apply R1/GRPO updates to maximise comparative human feedback. Beyond alignment, works such as PrefPaint [118], Parrot [126], and RLRF [119] craft multi-objective or render-and-compare rewards to refine aesthetics, diversity, or vector graphics. RL has also been used to inject _reasoning and prompt adaptation_ : ReasonGenR1 [114], GoT-R1 [120] and RePrompt [129] first generate textual plans or improved prompts, then reinforce the generator for coherent scene synthesis. Finally, personalisation methods—DPG-T2I [127], RPO [128], and B<sup>2</sup> -DiffuRL [131] optimize rewards that measure subject fidelity under scarce reference images. Collectively, these studies show that RL, armed with perceptual or preference-based rewards, can steer diffusion models toward higher realism, stronger prompt faithfulness, controllable layout, and user-specific appearance capabilities difficult to achieve with likelihood training alone. 

### _3.2.2 Video Generation_ 

Applying RL to video generation introduces challenges absent in images: rewards must capture _temporal coherence_ , _motion naturalness_ , and _text–video alignment_ across hundreds of frames. Early work such as InstructVideo [144] repurposed image scorers and applied PPO to refine short clips, whereas VideoRM [147] and VideoReward [141] learn dedicated preference models that grade entire sequences for smoothness, consistency and prompt faithfulness. Building on GRPO/R1, DanceGRPO [138] shows that group-normalized returns stabilize long-horizon optimization and boost aesthetic and alignment scores across diffusion and flow backbones. 

Beyond preference alignment, specialized rewards tackle domain-specific goals. GAPO [143] exploits gap-aware ranking to fine-tune anime videos; Phys-AR [140] penalizes violations of physics to yield plausible trajectories; and InfLVG [139] trains an inference-time policy that retains only context tokens beneficial for multi-scene coherence. Auxiliary critics further facilitate training: VideoScore [145] and Gradeo [146] offer explainable, multi-factor scores, while TeViR [142] feeds imagined video roll-outs as dense rewards to downstream control agents. Collectively, these studies demonstrate that carefully crafted sequence level rewards and group-relative policy updates are key to producing temporally consistent, semantically aligned, and physically plausible videos capabilities difficult to obtain with likelihood training alone. 

9 

### _3.2.3 3D Generation_ 

RL for 3D generation differs from 2D and video tasks as rewards operate on _volumetric structures_ or _rendered views_ , often requiring expensive render-and-compare loops. DreamCS [148] pioneers this paradigm by framing text-tomesh synthesis as a Markov decision process: a diffusion backbone proposes coarse shapes, then a policy refines vertex positions under a reward that jointly measures silhouette IoU, CLIP text-mesh alignment, and mesh smoothness. On the reward side, DreamReward [149] introduces a large-scale human preference dataset of rendered 3-D assets and trains a geometry-aware critic that scores prompts, renders, and latent SDFs; the learned signal enables stable PPO fine-tuning of existing text-to-shape models. 

A complementary line adopts direct preference optimization. DreamDPO [14] extends DPO to NeRF and mesh diffusion models by sampling paired 3D outputs and maximizing the margin dictated by human comparisons, achieving superior prompt fidelity without an explicit value network. Finally, Nabla-R2D3 [150] tackles _interactive scene editing_ : the agent sequentially adds, deletes, or transforms objects in a 3D scene; reward is computed via real-time rasterized views and task-specific validators ( _e.g.,_ occupancy, spatial relations). Group-relative policy optimization (R2D3) stabilizes training despite sparse feedback. Together, these studies demonstrate that RL, equipped with geometry-aware or render-based rewards, provides an effective mechanism for controlling structural integrity, text alignment, and interactive editability capabilities that standard likelihood or score-distillation objectives struggle to capture in the 3D domain. 

### _3.2.4 Reward Design and Preference Modeling for Visual Generation_ 

As shown in Figure 5, the reward design in RL-based visual generation can broadly be divided into three paradigms: (a) Human-Centric Preference Optimization (using human feedback or learned reward models for video alignment and fidelity). Representative works include ImageReward [21], which pioneered large-scale text-to-image reward modeling from human comparisons and provided a critic for diffusion fine-tuning. Dpok [116] and DiffPPO [132] adapted PPO with KL regularization and human aesthetic scores to enhance alignment and fidelity. Extending these ideas to video, VideoRM [147] and VideoReward [141] trained reward models on large-scale human (and GPT-assisted) video comparisons, enabling RL fine-tuning of text-to-video generation. (b) Multimodal Reasoning-Based Evaluation (using a question-answering or reasoning module to score consistency between videos and textual descriptions). For example, LLaVA-Reward [134] leverages a large VLM to evaluate images across multiple dimensions including alignment, fidelity, and safety, providing a multi-faceted reward signal that better approximates human judgment. and (c) Metric-Driven Objective Optimization (directly optimizing quantitative metrics like FID or IoU for quality). 

### **3.3 Unified Model** 

Task specific RL maximizes a reward tied to a _single_ objective, whereas _Unified RL_ optimizes a _shared_ policy and reward across multiple vision–language tasks ( _e.g.,_ understanding and generation). 

### _3.3.1 Unified RL_ 

Unlike task specific pipelines that attach RL to a single downstream objective, _Unified RL_ methods optimize a **shared policy** across heterogeneous multimodal tasks under a _single_ reinforcement signal. The central idea is to merge understanding and generation trajectories into one training loop typically using Group-Relative or R1-style methods. 

UniRL [15] exemplifies this paradigm: a visual autoregressive backbone is first instruction-tuned, then jointly finetuned on VQA, captioning and image generation with a blended reward measuring textual correctness, CLIP-based alignment, and aesthetic quality. CoRL [22] pushes the idea further by alternating “co-understanding” and “cogeneration” batches within the same GRPO step. To address inefficiency in dense token spaces, SelfTok [17] discretises multi-modal actions into a self-evolving token set and demonstrates that a single RL head can govern retrieval, grounding, and synthesis with minimal extra parameters. Finally, HermesFlow [151] couples an autoregressive text module with a rectified flow image decoder under one crosstask reward, illustrating that diffusion-style and languagestyle policies can be harmonized through unified reinforcement updates. Together, these works suggest that sharing a common RL objective across tasks not only reduces training cost but also encourages emergent cross modal generalization unavailable to isolated, task specific fine-tuning. 

### _3.3.2 Task specific RL_ 

In contrast to the unified approaches of §3.3.1, task-specific RL confines the reward signal to a single downstream objective, optimizing one functional head while leaving other capabilities untouched. VARGPT-v1.1 [154] exemplifies this strategy: although the underlying visual autoregressive model can handle both understanding and generation, its RL stage targets _only_ visual generation with DPO. Similarly, Emu3 [16] introduces RL exclusively to polish its image generation branch, which leveraging pair wise human preferences. For the multimodal understanding abilities of model ( _e.g.,_ captioning, VQA), the work just train this part by task specific fine-tuning alone. 

### **3.4 Vision Language Action Models** 

### _3.4.1 GUI Automation_ 

Modern GUI RL research frames screen understanding and action prediction as a vision–language decision process, then employs rule-based or preference rewards to close the perception–action loop. On desktop and web interfaces, GUI-R1 [10] introduces an R1-style rule set that maps click success, text entry, and scroll validity to dense rewards. UI-R1 [156] adds GRPO with a novel action-specific KL term to stabilize longhorizon plans, while SE-GUI [11] applies self-evolutionary filtering to distil high-fidelity trajectories. Focusing on trajectory reuse, UIShift [157] formulates an inverse dynamics objective that lets MLLM learn actions from unlabeled GUI pairs and then refines them via RL. Complementary preference-based frameworks include LPO [162] that rewards spatial proximity for precise clicks. ProgRM [159] injects program-level logical checks, and RUIG [164] leverages instruction grounding with reinforcement signals. Tool-specific 

10 


Fig. 5: **Three reward paradigms for RL-based image generation.** (a) Human-Centric Preference Optimization: aligns outputs with human aesthetic scores (HPS [24], ImageReward [21]); (b) Multimodal Reasoning-Based Evaluation: scores images via multimodal reasoning consistency (UnifiedReward [152], PARM [187]); (c) Metric-Driven Objective Optimization: minimizes task-specific quantitative metrics such as FID and IoU. 

baselines such as Ui-tars [163] offer larger action vocabularies yet still rely on rule-driven RL for robust execution. 

Mobile scenarios introduce latency and on-device constraints. AgentCPM-GUI [158] compresses the action space and conducts GRPO fine-tuning. MobileGUI-RL [19] advances this line via online RL with task-level rewards to improve exploration under limited memory, and MobileR1 [160] extends interactive multi-turn RL to correct error cascades during long tasks. At inference, GTA1 [161] samples multiple action candidates and employs a judge model to pick the best, effectively trading compute for higher success rates. Additional, light-weight models such as Appvlm [165] demonstrate that modest-sized MLLM, after GRPO finetuning, can control smartphone apps with competitive precision. To adaptively reduce the thinking length, the TON [188] proposes a thought-dropout solution during supervised fine-tuning stage, then GRPO skill adaptivley skip unnecessary reasoning process for efficiently thinking. 

Collectively, these studies show that GUI agents benefit from rule-verifiable rewards, group-normalzsed policy updates, and preference-guided localization, achieving rapid progress toward reliable, cross-platform automation. 

### _3.4.2 Visual Navigation_ 

RL-driven visual navigation research now couples large vision–language models with embodied control, employing group-normalized or time-decayed returns to maintain longhorizon stability. OctoNav-R1 [168] exploits a hybrid RL pipeline with a “think-before-action” ability for VLA model, then translate egocentric frames into low-level actions. Focusing on dataset efficiency, VLN-R1 [170] builds an end-to-end navigator and introduces a time-decayed reward to handle continuous trajectories. At the system level, Flare [171] demonstrates that fine-tuning a multi-task robotics policy with large-scale RL in simulation can generalize to realworld household tasks. Complementary advances include More [169], which augments omni-directional inputs with memory-guided policy distillation, and RAPID [20], which 

integrates pose priors for faster convergence in unseen layouts. These works show that using temporal rewards, memory sampling, and environment priors with GRPO/PPO helps VLA agents navigate more reliably and efficiently. 

### _3.4.3 Visual Manipulation_ 

Visual manipulation tasks ( _e.g.,_ object relocation, tool use, and multi-step rearrangement) require fine-grained perception and long-horizon planning. Recent works [175], [176] integrate reinforcement learning with vision–language models to enhance generalization, interactivity, and policy consistency. TGRPO [175] introduces a task-grounded reward formulation and group normalized updates to stabilize training for open-ended object manipulation. RFTF [176] applies rule-based rewards to support interactive table top tasks and emphasizes training with minimal human supervision. Meanwhile, RLVLA [177] and VLA-RL [8] explore curriculum-based or progressive reinforcement learning for VLM-based robot agents, achieving high success rates across diverse rearrangement environments. 

Building on this, ConRFT [178] and iRe-VLA [179] introduce consistency-aware and instruction-refinement strategies respectively, using RL to align visual predictions with physical interaction outcomes. RIPT-VLA focuses on interactive prompting during manipulation, bridging LLM planning and low-level control through reinforced feedback [9]. Finally, ReinBot [180] leverages multimodal rollouts and preferencebased updates to improve real-world manipulation robustness [180]. Collectively, these studies highlight the role of vision-language reasoning, structured reward design, and RL-based refinement in advancing embodied manipulation under complex, language-conditioned settings. 

## **4 METRICS AND BENCHMARKS** 

Evaluating visual reinforcement learning (RL) with large models requires both traditional RL metrics [234], [235] and new ones designed for complex, open-ended outputs. Metrics 

11 

TABLE 2: **Overview of evaluation metrics in large-model visual RL.** Each task family is broken down into Task Metrics (RL-free external benchmarks), Reward Metrics (how the learning signal is computed), and Model-state Metrics (diagnostics tracked during optimization). 

|**Task Family**|**Task Metric**_M_set<br>(RL-free benchmarks / scores)|**Reward / Advantage Estimation**_M_samp<br>(scoring & preference signals)|**Model-state Metric**_M_<sup>_t_</sup><br>state<br>(training diagnostics)|
|---|---|---|---|
|**Multimodal**<br>**LLMs/ VLMs**|•**Comprehensive Evaluation**:_e.g.,_<br>MME [189], SEED-Bench [190], VQA<br>v2 [191], MMBench [192].<br>•**OCR**:_e.g.,_ TextVQA [193],<br>OCR-VQA [194], OCRBench [195].<br>•**Mathematical**:_e.g.,_ MathVista [196].<br>•**Documentation**:_e.g.,_ ChartQA [196],<br>DocVQA [197], InfoVQA [198].<br>•**Multilingual**:_e.g.,_ CMMMU [199],<br>CMMU [200].<br>_. . ._|•**Reward from Human Preference**:_e.g.,_<br>InstructGPT [3], LLaVA-RLHF [201].<br>•**Verifiable Rewards**: Deepseekmath [25],<br>IoU [202], CodeRL [203].<br>•**Reward from Model Preference**:_e.g.,_<br>CriticGPT [204].<br>_. . ._|•**Output length monitoring**:_e.g.,_ DPO [2].<br>•**KL-divergence**:_e.g.,_ InstructGPT [3].<br>_. . ._|
|**Visual**<br>**Generation**<br>(Image / Video /<br>3D)|•**Image Fidelity & Diversity**:_e.g.,_<br>FID [205], Inception Score (IS) [206].<br>•**Pixel-level Reconstruction**:_e.g.,_<br>PSNR [207], SSIM [207].<br>•**Semantic Alignment**:_e.g.,_ Geneval [208],<br>T2I-CompBench [209], CLIP Score [210],<br>Frechet CLIP Distance [211].<br>•**Video Fidelity & Diversity**:_e.g.,_<br>FVD [212], Video IS [213].<br>_. . ._|•**Reward from Human Preference**:_e.g.,_<br>ImageReward [21], HPS [24], HPS V2 [24],<br>Pick-a-pic [214], VideoReward [141],<br>RichHF-18K [215].<br>•**Verifiable Rewards**:_e.g.,_<br>MotionPrompt [216], DSPO [217],<br>Instructrl4pix [218].<br>•**Reward from Model Preference**:_e.g.,_<br>VideoPrefer [147], PARM [219].<br>_. . ._|•**Denoising Trajectory Diagnostics**:_e.g.,_<br>VARD [220], Inversion-DPO [221].<br>•**KL-divergence**:_e.g.,_ DDPO [13],<br>VARD [220].<br>_. . ._|
|**Unified Models**|•**Generation–oriented Task Metrics**:_e.g.,_<br>GenEval [208], DPG-Bench [222],<br>ParaPrompts [223].<br>•**Understanding–oriented Task**<br>**Metrics**:_e.g.,_MME [189], POPE [224].<br>_. . ._|•**Unified Rewards**:_e.g.,_UniRL [15],<br>CoRL [22].<br>•**Task-specific Rewards**:_e.g.,_Vargpt-v1.<br>1 [154], Emu3 [16].<br>_. . ._|•**Generation–Understanding**<br>**Imbalance**:_e.g.,_UniRL [15].<br>•**KL-divergence**:_e.g.,_HermesFlow [151]<br>_. . ._|
|**Vision-Language**<br>**Action Agents**<br>(GUI /<br>Navigation /<br>Manip.)|•**GUI Action Accuracy (offline)**:_e.g.,_<br>ScreenSpot [225], ScreenSpot-Pro [226],<br>Ui-vision [227].<br>•**Task Success rate (online):**_e.g.,_<br>Webarena [228], Osworld [229], Windows<br>agent arena [230].<br>•**Model-based Evaluation:**_e.g.,_<br>Agentrewardbench [231], Webworld [232],<br>Digirl [233].<br>•**Reward from Human Preference**:_e.g.,_<br>RFTF [176].<br>•**Navigation Success & SPL:**<br>_. . ._|•**Rule-based Success (binary) (IoU, Action**<br>**Accuracy):**_e.g.,_UI-R1 [156], ARPO [167],<br>VLA-RL [8].<br>•**Model Preference Critic:**_e.g.,_<br>ProgRM [159].<br>•**Dense Shaping (distance or**<br>**coverage):**_e.g.,_LPO [162], Gui-r1 [10].<br>_. . ._|•**Action trajectory length:**_e.g.,_<br>Osworld [229].<br>•**KL penalty for policy stability**:_e.g.,_<br>GUI-R1 [10], UI-R1 [156].<br>•**Output length monitoring:**_e.g.,_<br>UI-R1 [156]._. . ._|


like cumulative return and task success rate are still useful especially in tasks involving agents and environments but they are increasingly combined with preference-based evaluations. In this section, we discuss metrics and benchmarks across four major application areas of large-model RL. 

### **4.1 Formalizing Metric Granularity** 

Let _P_ test = _{ p_ 1 _, . . . , pD}_ denote a fixed set of _prompts_ (inputs) and let a generative policy _πθ_ ( _y | p_ ) produce an _output y_ (text, image, video, _etc._ ) conditioned on each prompt _p ∈P_ test. As shown in Figuer 6, we distinguish three granularities of evaluation: 

**Task Metric** _M_ set **(Set-level).** As illustrated in Fig. 6 (a), set-level metrics evaluate the generative policy _πθ_ over the full prompt set _P_ test, by comparing the distribution of generated outputs _Y_ gen = _{πθ_ ( _· | pi_ ) _}i_<sup>_D_</sup> =1<sup>to a reference set of</sup> ground-truth outputs _Y_ gt = _{y_ gt<sup>_i}_</sup> _i_<sup>_D_</sup> =1<sup>. When the evaluation</sup> function operates _without access to ground-truth outputs_ such as CLIPScore [236], we define: 


where _M_ samp( _y, p_ ) denotes a sample-level reward function applied to each generated output. By contrast, many classical vision metrics do rely on reference outputs such as IoU [202]. For these cases, set-level evaluation is defined as: 


where each ground-truth output _y_ gt<sup>_i_denotes</sup><sup>_i_-thground</sup> truth from the reference set. 

**Reward/Advantage metric** _M_ samp **(Sample-level).** As illustrated in Fig. 6 (b), reward and advantage metrics _M_ samp operate at the granularity of individual input-output pairs, forming the backbone of reinforcement learning in generative settings. Given a prompt _pi_ , the policy _πθ_ generates a sample _y_ gen<sup>_i_,whichisthenscoredby</sup><sup>_M_samp(</sup><sup>_y_</sup> gen<sup>_i, pi_)to</sup> compute a scalar reward or advantage signal. This feedback is used to optimize the policy via reinforcement learning ( _e.g.,_ PPO [27], DPO [2]). In preference-based learning, the sample-level metric is often learned from human or GPT-4 comparisons [3], [201], or automatically derived via scoring models like CLIPScore [236], or ImageReward [21]. When rewards are reference-dependent (e.g., using PSNR [207] or 

12 


Fig. 6: **Metric Granularity in Visual RL.** (a) Set-level metric _M_ set: one score over the whole prompt set, used for final evaluation ( _e.g.,_ FID). (b) Sample-level metric _M_ samp: peroutput rewards that train the policy (RLHF, DPO). (c) State-level metric _M_<sup>_t_</sup> state<sup>:training-timesignalslikeKLor</sup> length drift, used to monitor stability. Notation: _pi_ , _y_ gen<sup>_i_,</sup><sup>_y_</sup> gt<sup>_i_</sup> denote the prompt, the generated output, and ground truth, respectively. _πθ_ 0 and _πθt_ refer to the 0-th and _t_ -th policy model. _Rϕ_ ( _·_ ) denotes the reward model. 

IoU [202]), _M_ samp compares the generated output _y_ gen<sup>_i_to a</sup> ground-truth output _y_ gt<sup>_i_. Formally, the reward signal can be</sup> expressed as: 


depending on whether the reward model _Rϕ_ operates with or without access to ground-truth outputs. In practice, the per-sample scores are transformed into step-wise advantages _A_ ˆ _i,t_ (where _t_ indexes generation steps). These advantages directly drive policy updates, enabling reward shaping and exploration control at the level of individual outputs. 

**State-level Metric** _M_<sup>_t_</sup> state<sup>**.**AsdepictedinFig.6(c),</sup> state-level metrics monitor the _training dynamics_ of the current policy _πθt_ at iteration _t_ . A common choice is the KL divergence to a frozen reference policy _πθ_ 0 : 


Other diagnostics include _output-length drift_ for autoregressive models and _DDIM step-trace variance_ for diffusion models. By tracking _M_<sup>_t_</sup> state<sup>duringoptimisation,practitioners</sup> detect reward hacking, mode collapse, or excessive policy shift before these issues degrade final performance. 

### **4.2 Evaluation of Multi-Modal Large Language Models** 

**Task Metric.** As summarized in Table 2, MLLM are first judged on _external, RL-free benchmarks_ . General reasoning 

suites such as MME [189], SEED-BENCH [190] and MMBENCH [192] measure factual QA, commonsense and multistep chain-of-thought across images. Domain-specific subsets probe OCR (TextVQA [193]), mathematics (MathVista [196]), documents (ChartQA [196]) and multilingual grounding (CMMMU [199]). 

**Reward Metric.** During training, each generated answer is scored with a sample-level reward _M_ samp. Three sources dominate current practice. (i) _Human-preference rewards_ are learned from large RLHF corpora _e.g.,_ InstructGPT [3] and LLaVA-RLHF [201], and give dense feedback that closely matches user judgements. (ii) _Verifiable rewards_ arise when a sub-task admits deterministic checks, such as unit-test pass rate in CodeRL [203] or symbolic exactness in DeepSeekMath [25]; they are noise-free but limited in scope. (iii) _Modelpreference rewards_ replace humans with a stronger frozen critic, _e.g.,_ CriticGPT [204], delivering scalable but potentially biased supervision. The chosen reward is converted to advantages _A_<sup>ˆ</sup> _i,t_ and optimized via PPO, GRPO or DPO. 

**Model-State Metric.** Beyond external scores, practitioners track light-weight diagnostics _M_<sup>_t_</sup> state<sup>throughout RL updates.</sup> Two lightweight diagnostics are widely adopted: (i) _Output length drift_ , the deviation of answer length from the SFT baseline large drift foreshadows verbosity or repetition [2]; (ii) _KL divergence_ between the current policy _πθt_ and frozen SFT reference _πθ_ 0 , as used in InstructGPT [3]. 

### **4.3 Evaluation of Visual Generation Models** 

**Task Metric.** As listed in Table 2, final quality is judged on standard, RL–free benchmarks that target complementary axes. Image fidelity & diversity is measured by FID and Inception Score, while pixel-level reconstruction tasks (superresolution, inpainting) use PSNR or SSIM. For prompt alignment, CLIP Score and Frechet CLIP Distance quantify´ semantic correctness; video models additionally report FVD or Video IS to capture temporal coherence. 

**Reward Metric.** During RL fine-tuning, each generated image or video receives a sample-level reward _M_ samp. Human-preference rewards, _e.g.,_ ImageReward [21] and HPS [24] supply dense signals that correlate well with aesthetic appeal. When a deterministic checker exists, authors turn to _verifiable rewards_ : MotionPrompt [216] and DSPO [217] use optical-flow, object masks that can be evaluated without humans. A third route relies on model preference rewards, where a stronger frozen critic ( _e.g.,_ VideoPrefer [147] or PARM [219]) scores samples, enabling scalable DPO/PPO training. 

**Model-State Metric.** Two light diagnostics track training stability. (i) Denoising trajectory statistics: VARD [220] and Inversion DPO [221] record per-step noise predictions or DDIM traces; pathological spikes reveal early collapse. (ii) KL divergence between the current diffusion policy and its frozen base ( _πθt ∥ πθ_ 0 ), popularized by DDPO [13] and reused in VARD. 

### **4.4 Evaluation of Unified Models** 

**Task Metric.** Two benchmark families are widely adopted. _Generation-oriented suites_ such as GenEval [208], DPGBench [222], and ParaPrompts [223] focus on prompt-faithful generation, testing multi-object composition, style control, 

13 

and long-caption adherence. Conversely, understandingoriented benchmarks (MME [189], POPE [224]) measure grounding, reasoning and hallucination detection from the same backbone. 

**Reward Metric.** Recent work explores two design philosophies for training signals. _Unified rewards_ ( _e.g.,_ UniRL [15], CoRL [22]) blend multiple objectives textual correctness, CLIP alignment, aesthetic quality—into a single scalar that drives one shared policy across tasks. In contrast, taskspecific rewards keep the generator and understanding heads separate, applying RL only to the generation branch as in VARGPT-V1.1 [154] or Emu3 [16]. The former promotes crossmodal transfer, while the latter preserves the stability of perception modules. 

**Model-State Metric.** Unified models additionally track fine-grained diagnostics during RL. UniRL [15] proposes a generation–understanding imbalance score the absolute gap between batch-level rewards on the two task families to prevent one modality from dominating the update. HermesFlow [151] monitors the KL divergence between the current shared policy _πθt_ and its supervised baseline _πθ_ 0 on _both_ generation and understanding prompts, serving as an early-warning signal for policy collapse. These statelevel curves _M_<sup>_t_</sup> state<sup>allow practitioners to stop or re-weight</sup> training before external task scores degrade. 

### **4.5 Evaluation of Vision Language Action Models** 

**Task Metric.** In GUI Automation task, there are multiple benchmarks could be classified into online or offline scenarios. For _offline_ setting, it mainly have grounding and navigation parts. For grounding, mainly check whether the click action fail into the target button; For navigation, it requires model to predict current action conditioned on oracle past history, this mainly dependent on whether the action class (click or type) are correctly predicted per step. For _online_ setting, it is more challenging, because it requires the model to fully perform multi-step execution which is long procedural then check whether the final outcome meet the task requirement. Such long procedural setups will produce sparse signal in term of model evalation. 

**Reward Metric.** For reward modeling, most offline RL methods borrow the metric from task metric like IoU, while come to the online environment, due to the sparsity of task success rate, which present significant challenges for end-toend multi-turn RL training [167] i.e., lack of training efficency, lack of informativeness, step-level reward is proposed to address this issue, such as developing a reward or critic models [232], [233]. 

**Model-State Metric.** To fully understand the model behavior beyond task success rate, trajectory length being an important metric as it can reflect how efficient model can address the task. A smart agent should be able to resolve the task with minimal steps. This pose challenges for agents with advanced planning ability. 

### **4.6 Benchmarks** 

A variety of new benchmarks explicitly support RL-based training and evaluation in the visual domain (see Table 3). For **MLLM** , recent datasets target complex multi-hop reasoning 

and alignment with human preferences. For example, SEEDBench-R1 [237] introduces a hierarchical egocentric video question-answering benchmark with 50k training questions and a human-verified validation set. Long Video RL [242] scales up multi-step reasoning on long videos: it provides 52k QA pairs with detailed reasoning annotations. Another recent benchmark, Ego-R1 Bench [241], focuses on ultralong (week-long) egocentric videos; an RL-trained “chainof-tool-thought” agent must invoke perception tools in 7 sequential steps on average to answer each query, illustrating the use of step-wise reasoning accuracy as a core challenge. In the image domain, VisuLogic [239] contains 1 _,_ 000 carefully crafted visual reasoning puzzles ( _e.g.,_ spatial and logic problems) to evaluate pure vision-centric reasoning, and most models perform only slightly above random on this benchmark. 

Benchmarks for **visual generation** tasks predominantly supply human preference data that serve as reward models for policy optimization. Datasets like ImageReward [21] and HPS v1 & v2 [24], [24] collect human-ranked pairs of text-toimage outputs, allowing one to train a scalar reward function that scores generations. Such reward models have been used to refine text-to-image diffusion models via RLHF, aligning outputs with human aesthetic preferences. Similarly, Picka-Pic [214] and VideoReward [141]extend this to broader user preferences (motion smoothness, text alignment). Some benchmarks also facilitate robust evaluation of generative RL agents on generalization. T2I-CompBench [209] is a textto-image compositionality test set that requires correctly binding novel combinations of attributes and object relations – a measure of compositional generalization often used to assess RL-trained generators. Likewise, domain-specific benchmarks define verifiable success criteria as rewards: StarVector [262] provides SVG code-generation tasks with a strict shape-matching reward, and AnimeReward [143] targets consistency in animated video generations with multi-dimensional human preference scores (image-video coherence, character consistency, etc.). 

For **vision–language action** agents, numerous benchmarks provide expert trajectories and simulated environments with clear reward signals for policy training and robust evaluation. Many are centered on GUI and web interaction tasks, where success can be unambiguously measured. For instance, GUI-R1-3K [10] compiles 3 _,_ 000+ GUI manipulation trajectories across Windows, Linux, macOS, Android, and web platforms. It introduces an “R1-style” dense reward scheme mapping each correct action ( _e.g.,_ clicking the right button, entering correct text, a valid scroll) to positive feedback, providing step-wise reinforcement that guides an agent through multi-step UI tasks. Building on this, SE-GUI [11] curates 3k high-quality GUI examples with grounded instructions and bounding-box annotations, which are used to train agents with a self-imitation RL strategy. Evaluation-focused suites like UI-R1 [156] define a fixed set of unseen tasks ( _e.g.,_ 136 mobile GUI tasks spanning click, scroll, swipe, text-input actions) to test generalization of learned policies. Meanwhile, web interaction benchmarks such as Mind2Web [263] offer 2,000 tasks on real websites with a binary success/failure reward for completing each task. Some datasets emphasize exact match and reproducibility: AITZ [264] (Android Interaction w/ CoAT 

14 

reasoning) logs 18k screen-action pairs with corresponding tool-assisted rationales, and uses an exact action match reward to ensure precise adherence to instructions. On the other hand, broader benchmarks like OmniAct [265] and GUICoURS [266] target generalist agent capabilities across diverse domains. OmniAct integrates nearly 10k scripted desktop and web tasks into a single environment, while GUICoURS combines multimodal resources (10M OCR observations, 67k navigation demonstrations) spanning GUI, web, and chat interfaces. The reward structures in these benchmarks are carefully crafted, from rule-based metrics to preference scores, to guide policy learning and reflect task goals. They enable visual RL agents to learn from meaningful feedback and be evaluated not just on task success, but also on alignment with human reasoning and performance on complex, long-horizon decisions. 

## **5 CHALLENGES AND FUTURE WORKS** 

### **5.1 Effective Reasoning: Balancing Depth and Efficiency** 

A recurrent challenge in visual RL is reasoning calibration: excessively long chains of visual or verbal thoughts incur latency and compounding errors, whereas overly aggressive pruning discards salient cues. We foresee two research thrusts. ( **i** ) _Adaptive horizon policies_ : train a termination critic that jointly optimizes answer quality and computational cost; curriculum-based reward shaping can gradually penalize redundant steps while preserving informative ones. ( **ii** ) _Meta-reasoning and few-shot self-evaluation_ : incorporate a lightweight evaluator that critiques partial chains ( _e.g.,_ via frozen vision–language models) and decides whether further thinking is worthwhile. Future benchmarks should therefore report both success rate and reasoning efficiency metrics (average steps, FLOPs, latency), encouraging algorithms that achieve high accuracy with just-enough deliberation rather than maximal cogitation. 

### **5.2 Long-Horizon RL in VLA** 

Long-horizon vision–language agents (VLA) must execute dozens of atomic actions ( _e.g.,_ clicks, drags, text edits) before any end-task reward is observed. Existing works such as OS-World [273] and ARPO [167] therefore fall back on sparse reward for each click and a binary task success flag yet empirical results suggest that even GRPO yields limited gains under such supervision. Future research should (i) _discover intrinsic sub-goals_ : segment trajectories via statechange detection or language-conditioned clustering, then assign dense rewards to sub-goal completions; (ii) _learn affordance critics_ : train contrastive vision–language models to score how much an action reduces the distance to the verbal goal, providing shaped feedback without manual labels; (iii) _hierarchical or option-based RL_ : couple a high-level language planner that proposes semantic sub-tasks with a low-level policy fine-tuned by off-policy RL or decision transformers; 

### **5.3 RL for Thinking with Vision** 

Recent works for visual planning, such as Chain-of-Focus [7] and Openthinkimg [91] all treat the picture as an external workspace: the agent may crop, sketch, highlight or insert 

visual tokens before emitting the next language token. While early prototypes rely on supervised heuristics for these spatial actions, moving to reinforcement learning exposes four open problems. **(i) Action-space design.** Cropping or doodling is naturally continuous ( _x, y, w, h, . . ._ ) yet RL libraries and GPU memories favor small discrete sets. Hybrid schemes that learn a differentiable proposal policy and then refine coordinates via policy gradient fine-tuning, as hinted by BRPO [84] and VRAG-RL [88], remain largely unexplored. **(ii) Credit assignment.** Most benchmarks only reward the final task success ( _e.g.,_ answer correctness in VILASR [83]); the whole visual chain-of-thought shares a single sparse scalar. Future work should mine step-wise proxy rewards, _e.g.,_ CLIP similarity increase after a crop, or entropy drop in a learned belief state—to enable bootstrapped or hierarchical RL. **(iii) Data efficiency.** Sketching or inserting patches triggers extra forward passes through the vision encoder, making naive on-policy RL prohibitively expensive. Relabeling (DeepEyes [6]) and model-based imagination (Pixel Reasoner [86]) point to sample-efficient alternatives, but principled replay and uncertainty-aware planners for visual actions are still missing. Therefore, future directions include: learning structured visual skills (crop, zoom, draw) via skill-prior RL; devising cross-modal reward shaping that scores each edit by how much it simplifies the remaining reasoning; and curating benchmarks whose metrics expose not just final accuracy. 

### **5.4 Reward Model Design for Visual Generation** 

A central obstacle for reinforcement-learning–based visual generation is the lack of a scalable and faithful reward function. Widely used handcrafted metrics such as FID [205] offer a convenient numerical signal, yet correlate only weakly with human judgments of aesthetics, semantic fidelity, or temporal coherence, especially when the task extends beyond single-frame images. Recent learned critics, such as ImageReward [21] and HPS [24] for images, and VideoReward [141] for videos to bridge this gap by training on pairwise human-preference data, but each model targets a narrow modality and captures only a slice of perceptual quality ( _e.g.,_ prompt alignment or visual appeal). As a result, policies optimized with PPO or GRPO often exploit loopholes in a single scalar signal, producing high-contrast artifacts, repetitive textures, or physically implausible motion that “game” the critic without improving real user satisfaction. The challenge, therefore, is to design reward models that (i) integrate complementary low-level signals (consistency, physics, geometry) with high-level human preferences, (ii) generalize across images, video and 3-D scenes, and (iii) remain robust against reward hacking while being cheap enough to update continually as user tastes evolve. 

## **6 CONCLUSION** 

Visual reinforcement learning has transitioned from isolated proof-of-concepts to a vibrant research frontier that bridges vision, language, and action. Our review shows that modern progress is driven by three converging forces: (i) scalable reward supervision, moving from labour-intensive RLHF to group-relative and verifiable-signal pipelines; (ii) unified 

15 

architectures, where a single policy is jointly optimised for perception, reasoning, and generation; and (iii) ever-richer benchmarks, which measure not only task success but also alignment with human preference and policy stability. 

Yet significant challenges remain. First, data and compute efficiency are pressing: current methods often require orders of magnitude more samples than supervised counterparts. Second, robust generalization across domains, viewpoints, and embodiment settings is still limited. Third, reward design for long-horizon, open-world tasks lacks principled guidance, risking reward hacking, and unsafe behaviors. Finally, evaluation standards must evolve to capture real-world utility, ethical alignment, and energy footprint. Addressing these issues will likely involve tighter integration of modelbased planning, self-supervised visual pre-training, adaptive curricula, and safety-aware optimization. 

In summary, visual RL stands poised to transform how intelligent systems perceive and interact with their surroundings. By unifying methodological insights and charting unresolved questions, this survey aims to serve as both a reference and a catalyst for the next wave of research toward sample-efficient, reliable, and socially aligned visual decisionmaking agents. 

## **REFERENCES** 

- [1] A. Jaech, A. Kalai, A. Lerer, A. Richardson, A. El-Kishky, A. Low, A. Helyar, A. Madry, A. Beutel, A. Carney _et al._ , “Openai o1 system card,” _arXiv preprint arXiv:2412.16720_ , 2024. 

- [2] R. Rafailov, A. Sharma, E. Mitchell, C. D. Manning, S. Ermon, and C. Finn, “Direct preference optimization: Your language model is secretly a reward model,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 53 728–53 741, 2023. 

- [3] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray _et al._ , “Training language models to follow instructions with human feedback,” _Advances in neural information processing systems_ , vol. 35, pp. 27 730–27 744, 2022. 

- [4] D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi _et al._ , “Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning,” _arXiv preprint arXiv:2501.12948_ , 2025. 

- [5] G. Zhou, P. Qiu, C. Chen, J. Wang, Z. Yang, J. Xu, and M. Qiu, “Reinforced mllm: A survey on rl-based reasoning in multimodal large language models,” _arXiv preprint arXiv:2504.21277_ , 2025. 

- [6] Z. Zheng, M. Yang, J. Hong, C. Zhao, G. Xu, L. Yang, C. Shen, and X. Yu, “Deepeyes: Incentivizing” thinking with images” via reinforcement learning,” _arXiv preprint arXiv:2505.14362_ , 2025. 

- [7] X. Zhang, Z. Gao, B. Zhang, P. Li, X. Zhang, Y. Liu, T. Yuan, Y. Wu, Y. Jia, S.-C. Zhu _et al._ , “Chain-of-focus: Adaptive visual search and zooming for multimodal reasoning via rl,” _arXiv preprint arXiv:2505.15436_ , 2025. 

- [8] G. Lu, W. Guo, C. Zhang, Y. Zhou, H. Jiang, Z. Gao, Y. Tang, and Z. Wang, “Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning,” _arXiv preprint arXiv:2505.18719_ , 2025. 

- [9] S. Tan, K. Dou, Y. Zhao, and P. Krahenb¨ uhl,¨ “Interactive post-training for vision-language-action models,” _arXiv preprint arXiv:2505.17016_ , 2025. 

- [10] R. Luo, L. Wang, W. He, and X. Xia, “Gui-r1: A generalist r1style vision-language action model for gui agents,” _arXiv preprint arXiv:2504.10458_ , 2025. 

- [11] X. Yuan, J. Zhang, K. Li, Z. Cai, L. Yao, J. Chen, E. Wang, Q. Hou, J. Chen, P.-T. Jiang _et al._ , “Enhancing visual grounding for gui agents via self-evolutionary reinforcement learning,” _arXiv preprint arXiv:2505.12370_ , 2025. 

- [12] Y. Fan, O. Watkins, Y. Du, H. Liu, M. Ryu, C. Boutilier, P. Abbeel, M. Ghavamzadeh, K. Lee, and K. Lee, “Reinforcement learning for fine-tuning text-to-image diffusion models,” in _Thirty-seventh Conference on Neural Information Processing Systems (NeurIPS) 2023_ . Neural Information Processing Systems Foundation, 2023. 

- [13] K. Black, M. Janner, Y. Du, I. Kostrikov, and S. Levine, “Training diffusion models with reinforcement learning,” 2023. 

- [14] Z. Zhou, X. Xia, F. Ma, H. Fan, Y. Yang, and T.-S. Chua, “Dreamdpo: Aligning text-to-3d generation with human preferences via direct preference optimization,” _arXiv preprint arXiv:2502.04370_ , 2025. 

- [15] W. Mao, Z. Yang, and M. Z. Shou, “Unirl: Self-improving unified multimodal models via supervised and reinforcement learning,” _arXiv preprint arXiv:2505.23380_ , 2025. 

- [16] X. Wang, X. Zhang, Z. Luo, Q. Sun, Y. Cui, J. Wang, F. Zhang, Y. Wang, Z. Li, Q. Yu _et al._ , “Emu3: Next-token prediction is all you need,” _arXiv preprint arXiv:2409.18869_ , 2024. 

- [17] B. Wang, Z. Yue, F. Zhang, S. Chen, L. Bi, J. Zhang, X. Song, K. Yanting Chan, J. Pan, W. Wu _et al._ , “Discrete visual tokens of autoregression, by diffusion, and for reasoning,” _arXiv e-prints_ , pp. arXiv–2505, 2025. 

- [18] G. DeepMind, “Gemini 2.5,” https://deepmind.google/ technologies/gemini/, 2025, accessed: 2025-08-09. 

- [19] Y. Shi, W. Yu, Z. Li, Y. Wang, H. Zhang, N. Liu, H. Mi, and D. Yu, “Mobilegui-rl: Advancing mobile gui agent through reinforcement learning in online environment,” _arXiv preprint arXiv:2507.05720_ , 2025. 

- [20] M. Kim, G. Bae, J. Lee, W. Shin, C. Kim, M.-Y. Choi, H. Shin, and H. Oh, “Rapid: Robust and agile planner using inverse reinforcement learning for vision-based drone navigation,” _arXiv preprint arXiv:2502.02054_ , 2025. 

- [21] J. Xu, X. Liu, Y. Wu, Y. Tong, Q. Li, M. Ding, J. Tang, and Y. Dong, “Imagereward: Learning and evaluating human preferences for text-to-image generation,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 15 903–15 935, 2023. 

- [22] J. Jiang, C. Si, J. Luo, H. Zhang, and C. Ma, “Co-reinforcement learning for unified multimodal understanding and generation,” _arXiv preprint arXiv:2505.17534_ , 2025. 

- [23] P. F. Christiano, J. Leike, T. Brown, M. Martic, S. Legg, and D. Amodei, “Deep reinforcement learning from human preferences,” _Advances in neural information processing systems_ , vol. 30, 2017. 

- [24] X. Wu, K. Sun, F. Zhu, R. Zhao, and H. Li, “Human preference score: Better aligning text-to-image models with human preference,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2023, pp. 2096–2105. 

- [25] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu _et al._ , “Deepseekmath: Pushing the limits of mathematical reasoning in open language models,” _arXiv preprint arXiv:2402.03300_ , 2024. 

- [26] N. Lambert, J. Morrison, V. Pyatkin, S. Huang, H. Ivison, F. Brahman, L. J. V. Miranda, A. Liu, N. Dziri, S. Lyu _et al._ , “T _\_ ” ulu 3: Pushing frontiers in open language model post-training,” _arXiv preprint arXiv:2411.15124_ , 2024. 

- [27] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [28] J. Schulman, P. Moritz, S. Levine, M. Jordan, and P. Abbeel, “Highdimensional continuous control using generalized advantage estimation,” _arXiv preprint arXiv:1506.02438_ , 2015. 

- [29] Y. Oh, J. Mok, D. Chung, J. Shin, S. Park, J. Barthelemy, and S. Yoon, “Repic: Reinforced post-training for personalizing multi-modal language models,” _arXiv preprint arXiv:2506.18369_ , 2025. 

- [30] A. Zakharov and S. Whiteson, “Goalladder: Incremental goal discovery with vision-language models,” _arXiv preprint arXiv:2506.16396_ , 2025. 

- [31] Y. Li, M. Tian, D. Zhu, J. Zhu, Z. Lin, Z. Xiong, and X. Zhao, “Driver1: Bridging reasoning and planning in vlms for autonomous driving with reinforcement learning,” _arXiv preprint arXiv:2506.18234_ , 2025. 

- [32] H. Shen, P. Liu, J. Li, C. Fang, Y. Ma, J. Liao, Q. Shen, Z. Zhang, K. Zhao, Q. Zhang _et al._ , “Vlm-r1: A stable and generalizable r1-style large vision-language model,” _arXiv preprint arXiv:2504.07615_ , 2025. 

- [33] Y. Chen, Y. Ge, R. Wang, Y. Ge, J. Cheng, Y. Shan, and X. Liu, “Grpocare: Consistency-aware reinforcement learning for multimodal reasoning,” _arXiv preprint arXiv:2506.16141_ , 2025. 

- [34] Z. Cai, J. Zhang, X. Yuan, P. Jiang, W. Chen, B. Tang, L. Yao, Q. Wang, J. Chen, and B. Li, “Q-ponder: A unified training pipeline for reasoning-based visual quality assessment,” _arXiv preprint arXiv:2506.05384_ , 2025. 

- [35] Y. Liang, J. Qiu, W. Ding, Z. Liu, J. Tompkin, M. Xu, M. Xia, Z. Tu, L. Shi, and J. Zhu, “Modomodo: Multi-domain data 

16 

   - mixtures for multimodal llm reinforcement learning,” _arXiv preprint arXiv:2505.24871_ , 2025. 

- [36] Y. Ma, L. Du, X. Shen, S. Chen, P. Li, Q. Ren, L. Ma, Y. Dai, P. Liu, and J. Yan, “One rl to see them all: Visual triple unified reinforcement learning,” _arXiv preprint arXiv:2505.18129_ , 2025. 

- [37] Y. Zhan, Y. Zhu, S. Zheng, H. Zhao, F. Yang, M. Tang, and J. Wang, “Vision-r1: Evolving human-free alignment in large vision-language models via vision-guided reinforcement learning,” _arXiv preprint arXiv:2503.18013_ , 2025. 

- [38] Z. Xiao, J. Koo, S. Ouyang, J. Hernandez, Y. Meng, and V. Ordonez, “Proxythinker: Test-time guidance through small visual reasoners,” _arXiv preprint arXiv:2505.24872_ , 2025. 

- [39] Z. Wang, J. Zhu, B. Tang, Z. Li, F. Xiong, J. Yu, and M. B. Blaschko, “Jigsaw-r1: A study of rule-based visual reinforcement learning with jigsaw puzzles,” _arXiv preprint arXiv:2505.23590_ , 2025. 

- [40] Z. Wan, Z. Dou, C. Liu, Y. Zhang, D. Cui, Q. Zhao, H. Shen, J. Xiong, Y. Xin, Y. Jiang _et al._ , “Srpo: Enhancing multimodal llm reasoning via reflection-aware reinforcement learning,” _arXiv preprint arXiv:2506.01713_ , 2025. 

- [41] Y. Yang, X. He, H. Pan, X. Jiang, Y. Deng, X. Yang, H. Lu, D. Yin, F. Rao, M. Zhu _et al._ , “R1-onevision: Advancing generalized multimodal reasoning through cross-modal formalization,” _arXiv preprint arXiv:2503.10615_ , 2025. 

- [42] H. Tan, Y. Ji, X. Hao, M. Lin, P. Wang, Z. Wang, and S. Zhang, “Reason-rft: Reinforcement fine-tuning for visual reasoning,” _arXiv preprint arXiv:2503.20752_ , 2025. 

- [43] M. Zhu, Y. Tian, H. Chen, C. Zhou, Q. Guo, Y. Liu, M. Yang, and C. Shen, “Segagent: Exploring pixel understanding capabilities in mllms by imitating human annotator trajectories,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 3686–3696. 

- [44] T. Wu, J. Zou, J. Liang, L. Zhang, and K. Ma, “Visualquality-r1: Reasoning-induced image quality assessment via reinforcement learning to rank,” _arXiv preprint arXiv:2505.14460_ , 2025. 

- [45] B. Zhang, H. Li, T. Zhang, C. Yan, J. Cai, X. Jiang, and Y. Hao, “Improving the reasoning of multi-image grounding in mllms via reinforcement learning,” _arXiv preprint arXiv:2507.00748_ , 2025. 

- [46] C. Shen, W. Wei, X. Qu, and Y. Cheng, “Satori-r1: Incentivizing multimodal reasoning with spatial grounding and verifiable rewards,” _arXiv preprint arXiv:2505.19094_ , 2025. 

- [47] P. Wang, Y. Wei, Y. Peng, X. Wang, W. Qiu, W. Shen, T. Xie, J. Pei, J. Zhang, Y. Hao _et al._ , “Skywork r1v2: Multimodal hybrid reinforcement learning for reasoning,” _arXiv preprint arXiv:2504.16656_ , 2025. 

- [48] H. Yang, Y. Zhou, W. Han, and J. Shen, “Self-rewarding large vision-language models for optimizing prompts in text-to-image generation,” _arXiv preprint arXiv:2505.16763_ , 2025. 

- [49] Q. Chang, Z. Zhang, P. Hu, J. Du, J. Ma, Y. Pan, J. Zhang, Q. Liu, and J. Gao, “Thor: Tool-integrated hierarchical optimization via rl for mathematical reasoning,” _arXiv preprint arXiv:2509.13761_ , 2025. 

- [50] L. Xing, X. Dong, Y. Zang, Y. Cao, J. Liang, Q. Huang, J. Wang, F. Wu, and D. Lin, “Caprl: Stimulating dense image caption capabilities via reinforcement learning,” _arXiv preprint arXiv:2509.22647_ , 2025. 

- [51] L. Zhu, B. Ouyang, Y. Zhang, T. Cheng, R. Hu, H. Shen, L. Ran, X. Chen, L. Yu, W. Liu _et al._ , “Lens: Learning to segment anything with unified reinforced reasoning,” _arXiv preprint arXiv:2508.14153_ , 2025. 

- [52] J. Xiong, Y. Wang, W. Zhao, C. Liu, B. Yin, W. Zhou, and H. Li, “Docr1: Evidence page-guided grpo for multi-page document understanding,” _arXiv preprint arXiv:2508.07313_ , 2025. 

- [53] A. Masry, A. Puri, M. Hashemi, J. A. Rodriguez, M. Thakkar, K. Mahajan, V. Yadav, S. T. Madhusudhan, A. Piche, D. Bahdanau´ _et al._ , “Bigcharts-r1: Enhanced chart reasoning with visual reinforcement finetuning,” _arXiv preprint arXiv:2508.09804_ , 2025. 

- [54] H. Zhong, M. Zhu, Z. Du, Z. Huang, C. Zhao, M. Liu, W. Wang, H. Chen, and C. Shen, “Omni-r1: Reinforcement learning for omnimodal reasoning via two-system collaboration,” _arXiv preprint arXiv:2505.20256_ , 2025. 

- [55] S. Park, H. Kim, J. Kim, S. Kim, and Y. M. Ro, “Dip-r1: Deep inspection and perception with rl looking through and understanding complex scenes,” _arXiv preprint arXiv:2505.23179_ , 2025. 

- [56] Z. Pan and H. Liu, “Metaspatial: Reinforcing 3d spatial reasoning in vlms for the metaverse,” _arXiv preprint arXiv:2503.18470_ , 2025. 

- [57] A. Zholus, M. Kuznetsov, R. Schutski, R. Shayakhmetov, D. Polykovskiy, S. Chandar, and A. Zhavoronkov, “Bindgpt: 

A scalable framework for 3d molecular design via language modeling and reinforcement learning,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 39, no. 24, 2025, pp. 26 083– 26 091. 

- [58] Z. Yuan, S. Jiang, C.-M. Feng, Y. Zhang, S. Cui, Z. Li, and N. Zhao, “Scene-r1: Video-grounded large language models for 3d scene reasoning without 3d annotations,” _arXiv preprint arXiv:2506.17545_ , 2025. 

- [59] E. Yu, K. Lin, L. Zhao, J. Yin, Y. Wei, Y. Peng, H. Wei, J. Sun, C. Han, Z. Ge _et al._ , “Perception-r1: Pioneering perception policy with reinforcement learning,” _arXiv preprint arXiv:2504.07954_ , 2025. 

- [60] Z. Chen, X. Luo, and D. Li, “Visrl: Intention-driven visual perception via reinforced reasoning,” _arXiv preprint arXiv:2503.07523_ , 2025. 

- [61] X. Wang, Z. Yang, C. Feng, Y. Liang, Y. Zhou, X. Liu, Z. Zang, M. Li, C.-C. Lin, K. Lin _et al._ , “Vicrit: A verifiable reinforcement learning proxy task for visual perception in vlms,” _arXiv preprint arXiv:2506.10128_ , 2025. 

- [62] Y. Liu, T. Qu, Z. Zhong, B. Peng, S. Liu, B. Yu, and J. Jia, “Visionreasoner: Unified visual perception and reasoning via reinforcement learning,” _arXiv preprint arXiv:2505.12081_ , 2025. 

- [63] G. Sarch, S. Saha, N. Khandelwal, A. Jain, M. J. Tarr, A. Kumar, and K. Fragkiadaki, “Grounded reinforcement learning for visual reasoning,” _arXiv preprint arXiv:2505.23678_ , 2025. 

- [64] Z. Liu, Z. Sun, Y. Zang, X. Dong, Y. Cao, H. Duan, D. Lin, and J. Wang, “Visual-rft: Visual reinforcement fine-tuning,” _arXiv preprint arXiv:2503.01785_ , 2025. 

- [65] P. Wang and H. Ling, “Svqa-r1: Reinforcing spatial reasoning in mllms via view-consistent reward optimization,” _arXiv preprint arXiv:2506.01371_ , 2025. 

- [66] J. Zhang, K. Miao, R. Pi, Z. Wang, R. Liu, R. Pan, and T. Zhang, “Vlgenrm: Enhancing vision-language verification via vision experts and iterative training,” _arXiv preprint arXiv:2506.13888_ , 2025. 

- [67] Y. Gou, K. Chen, Z. Liu, L. Hong, X. Jin, Z. Li, J. T. Kwok, and Y. Zhang, “Perceptual decoupling for scalable multi-modal reasoning via reward-optimized captioning,” _arXiv preprint arXiv:2506.04559_ , 2025. 

- [68] M. Unsal and A. Akkus, “Easyarc: Evaluating vision language models on true visual reasoning,” _arXiv preprint arXiv:2506.11595_ , 2025. 

- [69] Z. Li, Z. Ma, M. Li, S. Li, Y. Rong, T. Xu, Z. Zhang, D. Zhao, and W. Huang, “Star-r1: Spacial transformation reasoning by reinforcing multimodal llms,” _arXiv preprint arXiv:2505.15804_ , 2025. 

- [70] J. Xia, Y. Zang, P. Gao, Y. Li, and K. Zhou, “Visionary-r1: Mitigating shortcuts in visual reasoning with reinforcement learning,” _arXiv preprint arXiv:2505.14677_ , 2025. 

- [71] S. Bai, M. Li, Y. Liu, J. Tang, H. Zhang, L. Sun, X. Chu, and Y. Tang, “Univg-r1: Reasoning guided universal visual grounding with reinforcement learning,” _arXiv preprint arXiv:2505.14231_ , 2025. 

- [72] Z. Xing, X. Hu, C.-W. Fu, W. Wang, J. Dai, and P.-A. Heng, “Echoink-r1: Exploring audio-visual reasoning in multimodal llms via reinforcement learning,” _arXiv preprint arXiv:2505.04623_ , 2025. 

- [73] J. Yang, F. Ma, Z. Wang, D. Yin, K. Rong, F. Rao, and R. Zhang, “Wethink: Toward general-purpose vision-language reasoning via reinforcement learning,” _arXiv preprint arXiv:2506.07905_ , 2025. 

- [74] L. Chen, H. Gao, T. Liu, Z. Huang, F. Sung, X. Zhou, Y. Wu, and B. Chang, “G1: Bootstrapping perception and reasoning abilities of vision-language model via reinforcement learning,” _arXiv preprint arXiv:2505.13426_ , 2025. 

- [75] Y. Zhan, Z. Wu, Y. Zhu, R. Xue, R. Luo, Z. Chen, C. Zhang, Y. Li, Z. He, Z. Yang _et al._ , “Gthinker: Towards general multimodal reasoning via cue-guided rethinking,” _arXiv preprint arXiv:2506.01078_ , 2025. 

- [76] Z. Guo, M. Hong, and T. Jin, “Observe-r1: Unlocking reasoning abilities of mllms with dynamic progressive reinforcement learning,” _arXiv preprint arXiv:2505.12432_ , 2025. 

- [77] F. Meng, L. Du, Z. Liu, Z. Zhou, Q. Lu, D. Fu, T. Han, B. Shi, W. Wang, J. He _et al._ , “Mm-eureka: Exploring the frontiers of multimodal reasoning with rule-based reinforcement learning,” _arXiv preprint arXiv:2503.07365_ , 2025. 

- [78] T. Xiao, X. Xu, Z. Huang, H. Gao, Q. Liu, Q. Liu, and E. Chen, “Advancing multimodal reasoning capabilities of multimodal large language models via visual perception reward,” _arXiv preprint arXiv:2506.07218_ , 2025. 

- [79] L.-C.-T. Xiaomi, “Mimo-vl technical report,” 2025. [Online]. Available: https://arxiv.org/abs/2506.03569 

17 

- [80] J. Li, S. Ju, Y. Su, H. Li, and Y. Shen, “Enhancing llms’ reasoningintensive multimedia search capabilities through fine-tuning and reinforcement learning,” _arXiv preprint arXiv:2505.18831_ , 2025. 

- [81] Y. Xu, C. Li, H. Zhou, X. Wan, C. Zhang, A. Korhonen, and I. Vulic,´ “Visual planning: Let’s think only with images,” _arXiv preprint arXiv:2505.11409_ , 2025. 

- [82] Y. Fan, X. He, D. Yang, K. Zheng, C.-C. Kuo, Y. Zheng, S. J. Narayanaraju, X. Guan, and X. E. Wang, “Grit: Teaching mllms to think with images,” _arXiv preprint arXiv:2505.15879_ , 2025. 

- [83] J. Wu, J. Guan, K. Feng, Q. Liu, S. Wu, L. Wang, W. Wu, and T. Tan, “Reinforcing spatial reasoning in vision-language models with interwoven thinking and visual drawing,” _arXiv preprint arXiv:2506.09965_ , 2025. 

- [84] X. Chu, X. Chen, G. Wang, Z. Tan, K. Huang, W. Lv, T. Mo, and W. Li, “Qwen look again: Guiding vision-language reasoning models to re-attention visual information,” _arXiv preprint arXiv:2505.23558_ , 2025. 

- [85] M. Cao, H. Zhao, C. Zhang, X. Chang, I. Reid, and X. Liang, “Ground-r1: Incentivizing grounded visual reasoning via reinforcement learning,” _arXiv preprint arXiv:2505.20272_ , 2025. 

- [86] A. Su, H. Wang, W. Ren, F. Lin, and W. Chen, “Pixel reasoner: Incentivizing pixel-space reasoning with curiosity-driven reinforcement learning,” _arXiv preprint arXiv:2505.15966_ , 2025. 

- [87] Z. Kan, Y. Liu, K. Yin, X. Jiang, X. Li, H. Cao, Y. Liu, D. Jiang, X. Sun, Q. Liao _et al._ , “Taco: Think-answer consistency for optimized longchain reasoning and efficient data learning via reinforcement learning in lvlms,” _arXiv preprint arXiv:2505.20777_ , 2025. 

- [88] Q. Wang, R. Ding, Y. Zeng, Z. Chen, L. Chen, S. Wang, P. Xie, F. Huang, and F. Zhao, “Vrag-rl: Empower vision-perceptionbased rag for visually rich information understanding via iterative reasoning with reinforcement learning,” _arXiv preprint arXiv:2505.22019_ , 2025. 

- [89] Z. Huang, Y. Ji, A. S. Rajan, Z. Cai, W. Xiao, J. Hu, and Y. J. Lee, “Visualtoolagent (vista): A reinforcement learning framework for visual tool selection,” _arXiv preprint arXiv:2505.20289_ , 2025. 

- [90] E. Chern, Z. Hu, S. Chern, S. Kou, J. Su, Y. Ma, Z. Deng, and P. Liu, “Thinking with generated images,” _arXiv preprint arXiv:2505.22525_ , 2025. 

- [91] Z. Su, L. Li, M. Song, Y. Hao, Z. Yang, J. Zhang, G. Chen, J. Gu, J. Li, X. Qu _et al._ , “Openthinkimg: Learning to think with images via visual tool reinforcement learning,” _arXiv preprint arXiv:2505.08617_ , 2025. 

- [92] M. Zhu, H. Zhong, C. Zhao, Z. Du, Z. Huang, M. Liu, H. Chen, C. Zou, J. Chen, M. Yang _et al._ , “Active-o3: Empowering multimodal large language models with active perception via grpo,” _arXiv preprint arXiv:2505.21457_ , 2025. 

- [93] Y. Chen, Y. Shen, W. Huang, S. Zhou, Q. Lin, X. Cai, Z. Yu, J. Bu, B. Shi, and Y. Qiao, “Learning only with images: Visual reinforcement learning with reasoning, rendering, and visual feedback,” _arXiv preprint arXiv:2507.20766_ , 2025. 

- [94] S. Yang, J. Li, X. Lai, B. Yu, H. Zhao, and J. Jia, “Visionthink: Smart and efficient vision language model via reinforcement learning,” _arXiv preprint arXiv:2507.13348_ , 2025. 

- [95] X. Zhang, W. Li, S. Zhao, J. Li, L. Zhang, and J. Zhang, “Vq-insight: Teaching vlms for ai-generated video quality understanding via progressive visual reinforcement learning,” _arXiv preprint arXiv:2506.18564_ , 2025. 

- [96] J. Dang, J. Wu, T. Wang, X. Lin, N. Zhu, H. Chen, W.-S. Zheng, M. Wang, and T.-S. Chua, “Reinforcing video reasoning with focused thinking,” _arXiv preprint arXiv:2505.24718_ , 2025. 

- [97] A. Vinod, S. Pandit, A. Vavre, and L. Liu, “Egovlm: Policy optimization for egocentric video understanding,” _arXiv preprint arXiv:2506.03097_ , 2025. 

- [98] L. Zhu, Q. Chen, X. Shen, and X. Cun, “Vau-r1: Advancing video anomaly understanding via reinforcement fine-tuning,” _arXiv preprint arXiv:2505.23504_ , 2025. 

- [99] J. Park, J. Na, J. Kim, and H. J. Kim, “Deepvideo-r1: Video reinforcement fine-tuning via difficulty-aware regressive grpo,” _arXiv preprint arXiv:2506.07464_ , 2025. 

- [100] J. Zhang, L. Feng, X. Guo, Y. Wu, Y. Dong, and D. Xu, “Timemaster: Training time-series multimodal llms to reason via reinforcement learning,” _arXiv preprint arXiv:2506.13705_ , 2025. 

- [101] K. Feng, K. Gong, B. Li, Z. Guo, Y. Wang, T. Peng, B. Wang, and X. Yue, “Video-r1: Reinforcing video reasoning in mllms,” _arXiv: 2503.21776_ , 2025. 

- [102] X. Li, Z. Yan, D. Meng, L. Dong, X. Zeng, Y. He, Y. Wang, Y. Qiao, Y. Wang, and L. Wang, “Videochat-r1: Enhancing spatio- 

temporal perception via reinforcement fine-tuning,” _arXiv preprint arXiv:2504.06958_ , 2025. 

- [103] H. Li, S. Han, Y. Liao, J. Luo, J. Gao, S. Yan, and S. Liu, “Reinforcement learning tuning for videollms: Reward design and data efficiency,” _arXiv preprint arXiv:2506.01908_ , 2025. 

- [104] S. Tao, J. Li, Y. Yan, J. Zhang, Y. Gao, H. Li, S. Xun, Y. Fan, H. Chen, J. He _et al._ , “Moss-chatv: Reinforcement learning with process reasoning reward for video temporal reasoning,” _arXiv preprint arXiv:2509.21113_ , 2025. 

- [105] Y. Li, J. Cheng, S. Jia, H. Kuang, S. Jiao, Q. Hou, and M.-M. Cheng, “Tempsamp-r1: Effective temporal sampling with reinforcement fine-tuning for video llms,” _arXiv preprint arXiv:2509.18056_ , 2025. 

- [106] Y. Xie, T. Chen, Z. Ge, and L. Ni, “Video-mtr: Reinforced multiturn reasoning for long video understanding,” _arXiv preprint arXiv:2508.20478_ , 2025. 

- [107] H. Zhang, X. Gu, J. Li, C. Ma, S. Bai, C. Zhang, B. Zhang, Z. Zhou, D. He, and Y. Tang, “Thinking with videos: Multimodal toolaugmented reinforcement learning for long video reasoning,” _arXiv preprint arXiv:2508.04416_ , 2025. 

- [108] N. Dufour, L. Degeorge, A. Ghosh, V. Kalogeiton, and D. Picard, “Miro: Multi-reward conditioned pretraining improves t2i quality and efficiency,” _arXiv preprint arXiv:2510.25897_ , 2025. 

- [109] Y. Luo, P. Du, B. Li, S. Du, T. Zhang, Y. Chang, K. Wu, K. Gai, and X. Wang, “Sample by step, optimize by chunk: Chunk-level grpo for text-to-image generation,” _arXiv preprint arXiv:2510.21583_ , 2025. 

- [110] Y. Gong, X. Wang, J. Wu, S. Wang, Y. Wang, and X. Wu, “Onereward: Unified mask-guided image generation via multitask human preference learning,” _arXiv preprint arXiv:2508.21066_ , 2025. 

- [111] S. Wu, M. Huang, Y. Cheng, W. Wu, J. Tian, Y. Luo, F. Ding, and Q. He, “Uso: Unified style and subject-driven generation via disentangled and reward learning,” _arXiv preprint arXiv:2508.18966_ , 2025. 

- [112] Y. Wang, Z. Li, Y. Zang, Y. Zhou, J. Bu, C. Wang, Q. Lu, C. Jin, and J. Wang, “Pref-grpo: Pairwise preference reward-based grpo for stable text-to-image reinforcement learning,” _arXiv preprint arXiv:2508.20751_ , 2025. 

- [113] X. He, S. Fu, Y. Zhao, W. Li, J. Yang, D. Yin, F. Rao, and B. Zhang, “Tempflow-grpo: When timing matters for grpo in flow models,” _arXiv preprint arXiv:2508.04324_ , 2025. 

- [114] Y. Zhang, Y. Li, Y. Yang, R. Wang, Y. Yang, D. Qi, J. Bao, D. Chen, C. Luo, and L. Qiu, “Reasongen-r1: Cot for autoregressive image generation models through sft and rl,” _arXiv preprint arXiv:2505.24875_ , 2025. 

- [115] K. Pan, W. Bu, Y. Wu, Y. Wu, K. Shen, Y. Li, H. Zhao, J. Li, S. Tang, and Y. Zhuang, “Focusdiff: Advancing fine-grained text-image alignment for autoregressive visual generation through rl,” _arXiv preprint arXiv:2506.05501_ , 2025. 

- [116] Y. Fan, O. Watkins, Y. Du, H. Liu, M. Ryu, C. Boutilier, P. Abbeel, M. Ghavamzadeh, K. Lee, and K. Lee, “Dpok: Reinforcement learning for fine-tuning text-to-image diffusion models,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 79 858–79 885, 2023. 

- [117] S. Gupta, C. Ahuja, T.-Y. Lin, S. D. Roy, H. Oosterhuis, M. de Rijke, and S. N. Shukla, “A simple and effective reinforcement learning method for text-to-image diffusion fine-tuning,” _arXiv preprint arXiv:2503.00897_ , 2025. 

- [118] K. Liu, Z. Zhu, C. Li, H. Liu, H. Zeng, and J. Hou, “Prefpaint: Aligning image inpainting diffusion model with human preference,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 30 554–30 589, 2024. 

- [119] J. A. Rodriguez, H. Zhang, A. Puri, A. Feizi, R. Pramanik, P. Wichmann, A. Mondal, M. R. Samsami, R. Awal, P. Taslakian _et al._ , “Rendering-aware reinforcement learning for vector graphics generation,” _arXiv preprint arXiv:2505.20793_ , 2025. 

- [120] C. Duan, R. Fang, Y. Wang, K. Wang, L. Huang, X. Zeng, H. Li, and X. Liu, “Got-r1: Unleashing reasoning capability of mllm for visual generation with reinforcement learning,” _arXiv preprint arXiv:2505.17022_ , 2025. 

- [121] Z. Hu, F. Zhang, and K. Kuang, “D-fusion: Direct preference optimization for aligning diffusion models with visually consistent samples,” _arXiv preprint arXiv:2505.22002_ , 2025. 

- [122] B. Wallace, M. Dang, R. Rafailov, L. Zhou, A. Lou, S. Purushwalkam, S. Ermon, C. Xiong, S. Joty, and N. Naik, “Diffusion model alignment using direct preference optimization,” in _Pro-_ 

18 

_ceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 8228–8238. 

- [123] S. Li, K. Kallidromitis, A. Gokul, Y. Kato, and K. Kozuka, “Aligning diffusion models by optimizing human utility,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 24 897–24 925, 2024. 

- [124] Y. Gu, Z. Wang, Y. Yin, Y. Xie, and M. Zhou, “Diffusion-rpo: Aligning diffusion models through relative preference optimization,” _arXiv preprint arXiv:2406.06382_ , 2024. 

- [125] Z. Miao, J. Wang, Z. Wang, Z. Yang, L. Wang, Q. Qiu, and Z. Liu, “Training diffusion models towards diverse image generation with reinforcement learning,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 10 844–10 853. 

- [126] S. H. Lee, Y. Li, J. Ke, I. Yoo, H. Zhang, J. Yu, Q. Wang, F. Deng, G. Entis, J. He _et al._ , “Parrot: Pareto-optimal multi-reward reinforcement learning framework for text-to-image generation,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 462–478. 

- [127] F. Wei, W. Zeng, Z. Li, D. Yin, L. Duan, and W. Li, “Powerful and flexible: Personalized text-to-image generation via reinforcement learning,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 394–410. 

- [128] Y. Miao, W. Loh, S. Kothawade, P. Poupart, A. Rashwan, and Y. Li, “Subject-driven text-to-image generation via preferencebased reinforcement learning,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 123 563–123 591, 2024. 

- [129] M. Wu, L. Wang, P. Zhao, F. Yang, J. Zhang, J. Liu, Y. Zhan, W. Han, H. Sun, J. Ji _et al._ , “Reprompt: Reasoning-augmented reprompting for text-to-image generation via reinforcement learning,” _arXiv preprint arXiv:2505.17540_ , 2025. 

- [130] O. Oertell, J. D. Chang, Y. Zhang, K. Brantley, and W. Sun, “Rl for consistency models: Reward guided text-to-image generation with fast inference,” in _Reinforcement Learning Conference_ , 2024. 

- [131] Z. Hu, F. Zhang, L. Chen, K. Kuang, J. Li, K. Gao, J. Xiao, X. Wang, and W. Zhu, “Towards better alignment: Training diffusion models with reinforcement learning against sparse rewards,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 23 604–23 614. 

- [132] Z. Xiao, P. Jiang, M. Zhou, J. Zhang, Z. Huang, and J. Yang, “Diffppo: Reinforcement learning fine-tuning of diffusion models for text-to-image generation,” in _2024 International Conference on Neuromorphic Computing (ICNC)_ . IEEE, 2024, pp. 1–5. 

- [133] J. Wang, Z. Tian, X. Wang, X. Zhang, W. Huang, Z. Wu, and Y.-G. Jiang, “Simplear: Pushing the frontier of autoregressive visual generation through pretraining, sft, and rl,” _arXiv preprint arXiv:2504.11455_ , 2025. 

- [134] S. Zhou, R. Zhang, H. Zhu, B. Kveton, Y. Zhou, J. Gu, J. Chen, and C. Chen, “Multimodal llms as customized reward models for text-to-image generation,” 2025. [Online]. Available: https://arxiv.org/abs/2507.21391 

- [135] J. Liu, G. Liu, J. Liang, Y. Li, J. Liu, X. Wang, P. Wan, D. Zhang, and W. Ouyang, “Flow-grpo: Training flow matching models via online rl,” _arXiv preprint arXiv:2505.05470_ , 2025. 

- [136] M. Gallici and H. S. d. O. Borde, “Fine-tuning next-scale visual autoregressive models with group relative policy optimization,” _arXiv preprint arXiv:2505.23331_ , 2025. 

- [137] C. Chen, A. Wang, H. Wu, L. Liao, W. Sun, Q. Yan, and W. Lin, “Enhancing diffusion models with text-encoder reinforcement learning,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 182–198. 

- [138] Z. Xue, J. Wu, Y. Gao, F. Kong, L. Zhu, M. Chen, Z. Liu, W. Liu, Q. Guo, W. Huang _et al._ , “Dancegrpo: Unleashing grpo on visual generation,” _arXiv preprint arXiv:2505.07818_ , 2025. 

- [139] X. Fang, L. Ma, Z. Chen, M. Zhou, and G.-j. Qi, “Inflvg: Reinforce inference-time consistent long video generation with grpo,” _arXiv preprint arXiv:2505.17574_ , 2025. 

- [140] W. Lin, L. Jia, W. Hu, K. Pan, Z. Yue, W. Zhao, J. Chen, F. Wu, and H. Zhang, “Reasoning physical video generation with diffusion timestep tokens via reinforcement learning,” _arXiv preprint arXiv:2504.15932_ , 2025. 

- [141] J. Liu, G. Liu, J. Liang, Z. Yuan, X. Liu, M. Zheng, X. Wu, Q. Wang, W. Qin, M. Xia _et al._ , “Improving video generation with human feedback,” _arXiv preprint arXiv:2501.13918_ , 2025. 

- [142] Y. Chen, H. Li, Z. Jiang, H. Wen, and D. Zhao, “Tevir: Text-to-video reward with diffusion models for efficient reinforcement learning,” _arXiv preprint arXiv:2505.19769_ , 2025. 

- [143] B. Zhu, Y. Jiang, B. Xu, S. Yang, M. Yin, Y. Wu, H. Sun, and Z. Wu, “Aligning anime video generation with human feedback,” _arXiv preprint arXiv:2504.10044_ , 2025. 

- [144] H. Yuan, S. Zhang, X. Wang, Y. Wei, T. Feng, Y. Pan, Y. Zhang, Z. Liu, S. Albanie, and D. Ni, “Instructvideo: Instructing video diffusion models with human feedback,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 6463–6474. 

- [145] X. He, D. Jiang, G. Zhang, M. Ku, A. Soni, S. Siu, H. Chen, A. Chandra, Z. Jiang, A. Arulraj _et al._ , “Videoscore: Building automatic metrics to simulate fine-grained human feedback for video generation,” _arXiv preprint arXiv:2406.15252_ , 2024. 

- [146] Z. Mou, B. Xia, Z. Huang, W. Yang, and J. Jia, “Gradeo: Towards human-like evaluation for text-to-video generation via multi-step reasoning,” _arXiv preprint arXiv:2503.02341_ , 2025. 

- [147] X. Wu, S. Huang, G. Wang, J. Xiong, and F. Wei, “Boosting text-tovideo generative model with mllms feedback,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 139 444–139 469, 2024. 

- [148] X. Zou, R. Xia, H. Wang, and P. Zhou, “Dreamcs: Geometry-aware text-to-3d generation with unpaired 3d reward supervision,” _arXiv preprint arXiv:2506.09814_ , 2025. 

- [149] J. Ye, F. Liu, Q. Li, Z. Wang, Y. Wang, X. Wang, Y. Duan, and J. Zhu, “Dreamreward: Text-to-3d generation with human preference,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 259– 276. 

- [150] Q. Liu, Z. Liu, D. Zhang, and K. Jia, “Nabla-r2d3: Effective and efficient 3d diffusion alignment with 2d rewards,” _arXiv preprint arXiv:2506.15684_ , 2025. 

- [151] L. Yang, X. Zhang, Y. Tian, C. Shang, M. Xu, W. Zhang, and B. Cui, “Hermesflow: Seamlessly closing the gap in multimodal understanding and generation,” _arXiv preprint arXiv:2502.12148_ , 2025. 

- [152] Y. Wang, Y. Zang, H. Li, C. Jin, and J. Wang, “Unified reward model for multimodal understanding and generation,” _arXiv preprint arXiv:2503.05236_ , 2025. 

- [153] Y. Wang, Z. Li, Y. Zang, C. Wang, Q. Lu, C. Jin, and J. Wang, “Unified multimodal chain-of-thought reward model through reinforcement fine-tuning,” _arXiv preprint arXiv:2505.03318_ , 2025. 

- [154] X. Zhuang, Y. Xie, Y. Deng, D. Yang, L. Liang, J. Ru, Y. Yin, and Y. Zou, “Vargpt-v1. 1: Improve visual autoregressive large unified model via iterative instruction tuning and reinforcement learning,” _arXiv preprint arXiv:2504.02949_ , 2025. 

- [155] Z. Geng, Y. Wang, Y. Ma, C. Li, Y. Rao, S. Gu, Z. Zhong, Q. Lu, H. Hu, X. Zhang _et al._ , “X-omni: Reinforcement learning makes discrete autoregressive image generative models great again,” _arXiv preprint arXiv:2507.22058_ , 2025. 

- [156] Z. Lu, Y. Chai, Y. Guo, X. Yin, L. Liu, H. Wang, H. Xiao, S. Ren, G. Xiong, and H. Li, “Ui-r1: Enhancing efficient action prediction of gui agents by reinforcement learning,” _arXiv preprint arXiv:2503.21620_ , 2025. 

- [157] L. Gao, L. Zhang, and M. Xu, “Uishift: Enhancing vlm-based gui agents through self-supervised reinforcement learning,” _arXiv preprint arXiv:2505.12493_ , 2025. 

- [158] Z. Zhang, Y. Lu, Y. Fu, Y. Huo, S. Yang, Y. Wu, H. Si, X. Cong, H. Chen, Y. Lin _et al._ , “Agentcpm-gui: Building mobile-use agents with reinforcement fine-tuning,” _arXiv preprint arXiv:2506.01391_ , 2025. 

- [159] D. Zhang, S. Zhang, Z. Yang, Z. Zhu, Z. Zhao, R. Cao, L. Chen, and K. Yu, “Progrm: Build better gui agents with progress rewards,” _arXiv preprint arXiv:2505.18121_ , 2025. 

- [160] J. Gu, Q. Ai, Y. Wang, P. Bu, J. Xing, Z. Zhu, W. Jiang, Z. Wang, Y. Zhao, M.-L. Zhang _et al._ , “Mobile-r1: Towards interactive reinforcement learning for vlm-based mobile agent via task-level rewards,” _arXiv preprint arXiv:2506.20332_ , 2025. 

- [161] Y. Yang, D. Li, Y. Dai, Y. Yang, Z. Luo, Z. Zhao, Z. Hu, J. Huang, A. Saha, Z. Chen _et al._ , “Gta1: Gui test-time scaling agent,” _arXiv preprint arXiv:2507.05791_ , 2025. 

- [162] J. Tang, Y. Xia, Y.-F. Wu, Y. Hu, Y. Chen, Q.-G. Chen, X. Xu, X. Wu, H. Lu, Y. Ma _et al._ , “Lpo: Towards accurate gui agent interaction via location preference optimization,” _arXiv preprint arXiv:2506.09373_ , 2025. 

- [163] Y. Qin, Y. Ye, J. Fang, H. Wang, S. Liang, S. Tian, J. Zhang, J. Li, Y. Li, S. Huang _et al._ , “Ui-tars: Pioneering automated gui interaction with native agents,” _arXiv preprint arXiv:2501.12326_ , 2025. 

- [164] Z. Zhang, W. Xie, X. Zhang, and Y. Lu, “Reinforced ui instruction grounding: Towards a generic ui task automation api,” _arXiv preprint arXiv:2310.04716_ , 2023. 

19 

- [165] G. Papoudakis, T. Coste, Z. Wu, J. Hao, J. Wang, and K. Shao, “Appvlm: A lightweight vision language model for online app control,” _arXiv preprint arXiv:2502.06395_ , 2025. 

- [166] H. Bai, Y. Zhou, J. Pan, M. Cemri, A. Suhr, S. Levine, and A. Kumar, “Digirl: Training in-the-wild device-control agents with autonomous reinforcement learning,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 12 461–12 495, 2024. 

- [167] F. Lu, Z. Zhong, S. Liu, C.-W. Fu, and J. Jia, “Arpo: End-to-end policy optimization for gui agents with experience replay,” _arXiv preprint arXiv:2505.16282_ , 2025. 

- [168] C. Gao, L. Jin, X. Peng, J. Zhang, Y. Deng, A. Li, H. Wang, and S. Liu, “Octonav: Towards generalist embodied navigation,” _arXiv preprint arXiv:2506.09839_ , 2025. 

- [169] H. Zhao, W. Song, D. Wang, X. Tong, P. Ding, X. Cheng, and Z. Ge, “More: Unlocking scalability in reinforcement learning for quadruped vision-language-action models,” _arXiv preprint arXiv:2503.08007_ , 2025. 

- [170] Z. Qi, Z. Zhang, Y. Yu, J. Wang, and H. Zhao, “Vln-r1: Visionlanguage navigation via reinforcement fine-tuning,” _arXiv preprint arXiv:2506.17221_ , 2025. 

- [171] J. Hu, R. Hendrix, A. Farhadi, A. Kembhavi, R. Mart´ın-Mart´ın, P. Stone, K.-H. Zeng, and K. Ehsani, “Flare: Achieving masterful and adaptive robot policies with large-scale reinforcement learning fine-tuning,” _arXiv preprint arXiv:2409.16578_ , 2024. 

- [172] A. Jiang, Y. Gao, Y. Wang, Z. Sun, S. Wang, Y. Heng, H. Sun, S. Tang, L. Zhu, J. Chai _et al._ , “Irl-vla: Training an vision-language-action policy via reward world model,” _arXiv preprint arXiv:2508.06571_ , 2025. 

- [173] B. Zhao, Z. Wang, J. Fang, C. Gao, F. Man, J. Cui, X. Wang, X. Chen, Y. Li, and W. Zhu, “Embodied-r: Collaborative framework for activating embodied spatial reasoning in foundation models via reinforcement learning,” _arXiv preprint arXiv:2504.12680_ , 2025. 

- [174] A. Eftekhar, K.-H. Zeng, J. Duan, A. Farhadi, A. Kembhavi, and R. Krishna, “Selective visual representations improve convergence and generalization for embodied ai,” _arXiv preprint arXiv:2311.04193_ , 2023. 

- [175] Z. Chen, R. Niu, H. Kong, and Q. Wang, “Tgrpo: Fine-tuning vision-language-action model via trajectory-wise group relative policy optimization,” _arXiv preprint arXiv:2506.08440_ , 2025. 

- [176] J. Shu, Z. Lin, and Y. Wang, “Rftf: Reinforcement fine-tuning for embodied agents with temporal feedback,” _arXiv preprint arXiv:2505.19767_ , 2025. 

- [177] J. Liu, F. Gao, B. Wei, X. Chen, Q. Liao, Y. Wu, C. Yu, and Y. Wang, “What can rl bring to vla generalization? an empirical study,” _arXiv preprint arXiv:2505.19789_ , 2025. 

- [178] Y. Chen, S. Tian, S. Liu, Y. Zhou, H. Li, and D. Zhao, “Conrft: A reinforced fine-tuning method for vla models via consistency policy,” _arXiv preprint arXiv:2502.05450_ , 2025. 

- [179] Y. Guo, J. Zhang, X. Chen, X. Ji, Y.-J. Wang, Y. Hu, and J. Chen, “Improving vision-language-action model with online reinforcement learning,” _arXiv preprint arXiv:2501.16664_ , 2025. 

- [180] H. Zhang, Z. Zhuang, H. Zhao, P. Ding, H. Lu, and D. Wang, “Reinbot: Amplifying robot visual-language manipulation with reinforcement learning,” _arXiv preprint arXiv:2505.07395_ , 2025. 

- [181] L. Kang, X. Song, H. Zhou, Y. Qin, J. Yang, X. Liu, P. Torr, L. Bai, and Z. Yin, “Viki-r: Coordinating embodied multi-agent cooperation via reinforcement learning,” _arXiv preprint arXiv:2506.09049_ , 2025. 

- [182] D. Kim, S. Park, H. Jang, J. Shin, J. Kim, and Y. Seo, “Robotr1: Reinforcement learning for enhanced embodied reasoning in robotics,” _arXiv preprint arXiv:2506.00070_ , 2025. 

- [183] C. Xu, Q. Li, J. Luo, and S. Levine, “Rldg: Robotic generalist policy distillation via reinforcement learning,” _arXiv preprint arXiv:2412.09858_ , 2024. 

- [184] J. Luo, C. Xu, J. Wu, and S. Levine, “Precise and dexterous robotic manipulation via human-in-the-loop reinforcement learning,” _arXiv preprint arXiv:2410.21845_ , 2024. 

- [185] N. Hansen, Y. Lin, H. Su, X. Wang, V. Kumar, and A. Rajeswaran, “Modem: Accelerating visual model-based reinforcement learning with demonstrations,” _arXiv preprint arXiv:2212.05698_ , 2022. 

- [186] A. Zeng, S. Song, S. Welker, J. Lee, A. Rodriguez, and T. Funkhouser, “Learning synergies between pushing and grasping with self-supervised deep reinforcement learning,” in _2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2018, pp. 4238–4245. 

- [187] Z. Guo, R. Zhang, C. Tong, Z. Zhao, P. Gao, H. Li, and P.-A. Heng, “Can we generate images with cot? let’s verify and reinforce image generation step by step,” _arXiv preprint arXiv:2501.13926_ , 2025. 

- [188] J. Wang, K. Q. Lin, J. Cheng, and M. Z. Shou, “Think or not? selective reasoning via reinforcement learning for vision-language models,” _arXiv preprint arXiv:2505.16854_ , 2025. 

- [189] C. Fu, P. Chen, Y. Shen, Y. Qin, M. Zhang, X. Lin, J. Yang, X. Zheng, K. Li, X. Sun _et al._ , “Mme: A comprehensive evaluation benchmark for multimodal large language models,” _arXiv preprint arXiv:2306.13394_ , 2023. 

- [190] B. Li, Y. Ge, Y. Ge, G. Wang, R. Wang, R. Zhang, and Y. Shan, “Seed-bench: Benchmarking multimodal large language models,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 13 299–13 308. 

- [191] Y. Goyal, T. Khot, D. Summers-Stay, D. Batra, and D. Parikh, “Making the v in vqa matter: Elevating the role of image understanding in visual question answering,” in _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2017, pp. 6904–6913. 

- [192] Y. Liu, H. Duan, Y. Zhang, B. Li, S. Zhang, W. Zhao, Y. Yuan, J. Wang, C. He, Z. Liu _et al._ , “Mmbench: Is your multi-modal model an all-around player?” in _European conference on computer vision_ . Springer, 2024, pp. 216–233. 

- [193] A. Singh, V. Natarajan, M. Shah, Y. Jiang, X. Chen, D. Batra, D. Parikh, and M. Rohrbach, “Towards vqa models that can read,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2019, pp. 8317–8326. 

- [194] A. Mishra, S. Shekhar, A. K. Singh, and A. Chakraborty, “Ocr-vqa: Visual question answering by reading text in images,” in _2019 international conference on document analysis and recognition (ICDAR)_ . IEEE, 2019, pp. 947–952. 

- [195] Y. Liu, Z. Li, H. Li, W. Yu, M. Huang, D. Peng, M. Liu, M. Chen, C. Li, L. Jin _et al._ , “On the hidden mystery of ocr in large multimodal models,” _arXiv preprint arXiv:2305.07895_ , vol. 2, no. 5, p. 6, 2023. 

- [196] P. Lu, H. Bansal, T. Xia, J. Liu, C. Li, H. Hajishirzi, H. Cheng, K.-W. Chang, M. Galley, and J. Gao, “Mathvista: Evaluating mathematical reasoning of foundation models in visual contexts,” _arXiv preprint arXiv:2310.02255_ , 2023. 

- [197] M. Mathew, D. Karatzas, and C. Jawahar, “Docvqa: A dataset for vqa on document images,” in _Proceedings of the IEEE/CVF winter conference on applications of computer vision_ , 2021, pp. 2200–2209. 

- [198] M. Mathew, V. Bagal, R. Tito, D. Karatzas, E. Valveny, and C. Jawahar, “Infographicvqa,” in _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision_ , 2022, pp. 1697–1706. 

- [199] G. Zhang, X. Du, B. Chen, Y. Liang, T. Luo, T. Zheng, K. Zhu, Y. Cheng, C. Xu, S. Guo _et al._ , “Cmmmu: A chinese massive multidiscipline multimodal understanding benchmark,” _arXiv preprint arXiv:2401.11944_ , 2024. 

- [200] Z. He, X. Wu, P. Zhou, R. Xuan, G. Liu, X. Yang, Q. Zhu, and H. Huang, “Cmmu: A benchmark for chinese multi-modal multi-type question understanding and reasoning,” _arXiv preprint arXiv:2401.14011_ , 2024. 

- [201] Z. Sun, S. Shen, S. Cao, H. Liu, C. Li, Y. Shen, C. Gan, L.-Y. Gui, Y.-X. Wang, Y. Yang _et al._ , “Aligning large multimodal models with factually augmented rlhf,” _arXiv preprint arXiv:2309.14525_ , 2023. 

- [202] H. Rezatofighi, N. Tsoi, J. Gwak, A. Sadeghian, I. Reid, and S. Savarese, “Generalized intersection over union: A metric and a loss for bounding box regression,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2019, pp. 658– 666. 

- [203] H. Le, Y. Wang, A. D. Gotmare, S. Savarese, and S. C. H. Hoi, “Coderl: Mastering code generation through pretrained models and deep reinforcement learning,” _Advances in Neural Information Processing Systems_ , vol. 35, pp. 21 314–21 328, 2022. 

- [204] N. McAleese, R. M. Pokorny, J. F. C. Uribe, E. Nitishinskaya, M. Trebacz, and J. Leike, “Llm critics help catch llm bugs,” _arXiv preprint arXiv:2407.00215_ , 2024. 

- [205] M. Heusel, H. Ramsauer, T. Unterthiner, B. Nessler, and S. Hochreiter, “Gans trained by a two time-scale update rule converge to a local nash equilibrium,” _Advances in neural information processing systems_ , vol. 30, 2017. 

- [206] T. Salimans, I. Goodfellow, W. Zaremba, V. Cheung, A. Radford, and X. Chen, “Improved techniques for training gans,” _Advances in neural information processing systems_ , vol. 29, 2016. 

20 

- [207] Z. Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli, “Image quality assessment: from error visibility to structural similarity,” _IEEE transactions on image processing_ , vol. 13, no. 4, pp. 600–612, 2004. 

- [208] D. Ghosh, H. Hajishirzi, and L. Schmidt, “Geneval: An objectfocused framework for evaluating text-to-image alignment,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 52 132– 52 152, 2023. 

- [209] K. Huang, K. Sun, E. Xie, Z. Li, and X. Liu, “T2i-compbench: A comprehensive benchmark for open-world compositional textto-image generation,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 78 723–78 747, 2023. 

- [210] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark _et al._ , “Learning transferable visual models from natural language supervision,” in _International conference on machine learning_ . PmLR, 2021, pp. 8748–8763. 

- [211] E. Betzalel, C. Penso, A. Navon, and E. Fetaya, “A study on the evaluation of generative models,” _arXiv preprint arXiv:2206.10935_ , 2022. 

- [212] T. Unterthiner, S. Van Steenkiste, K. Kurach, R. Marinier, M. Michalski, and S. Gelly, “Fvd: A new metric for video generation,” 2019. 

- [213] M. Saito, S. Saito, M. Koyama, and S. Kobayashi, “Train sparsely, generate densely: Memory-efficient unsupervised training of highresolution temporal gan,” _International Journal of Computer Vision_ , vol. 128, no. 10, pp. 2586–2606, 2020. 

- [214] Y. Kirstain, A. Polyak, U. Singer, S. Matiana, J. Penna, and O. Levy, “Pick-a-pic: An open dataset of user preferences for text-to-image generation,” _Advances in neural information processing systems_ , vol. 36, pp. 36 652–36 663, 2023. 

- [215] Y. Liang, J. He, G. Li, P. Li, A. Klimovskiy, N. Carolan, J. Sun, J. Pont-Tuset, S. Young, F. Yang _et al._ , “Rich human feedback for text-to-image generation,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 19 401–19 411. 

- [216] H. Nam, J. Kim, D. Lee, and J. C. Ye, “Optical-flow guided prompt optimization for coherent video generation,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 7837–7846. 

- [217] M. Cai, S. Li, W. Li, X. Huang, H. Chen, J. Hu, and Y. Wang, “Dspo: Direct semantic preference optimization for real-world image super-resolution,” _arXiv preprint arXiv:2504.15176_ , 2025. 

- [218] T. Li, J. Liu, H. Chen, and Q. Liu, “Instructrl4pix: Training diffusion for image editing by reinforcement learning,” _arXiv preprint arXiv:2406.09973_ , 2024. 

- [219] R. Zhang, C. Tong, Z. Zhao, Z. Guo, H. Zhang, M. Zhang, J. Liu, P. Gao, and H. Li, “Let’s verify and reinforce image generation step by step,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 28 662–28 672. 

- [220] F. Dai, Z. Zhuang, Y. Huang, S. Huang, B. Liao, D. Wang, and F. Yuan, “Vard: Efficient and dense fine-tuning for diffusion models with value-based rl,” _arXiv preprint arXiv:2505.15791_ , 2025. 

- [221] Z. Li, Y. Li, C. Meng, Z. Liu, Y. Ling, S. Zhang, G. Yang, C. Yang, Z. Yang, and L. Sun, “Inversion-dpo: Precise and efficient posttraining for diffusion models,” _arXiv preprint arXiv:2507.11554_ , 2025. 

- [222] X. Hu, R. Wang, Y. Fang, B. Fu, P. Cheng, and G. Yu, “Ella: Equip diffusion models with llm for enhanced semantic alignment,” _arXiv preprint arXiv:2403.05135_ , 2024. 

- [223] W. Wu, Z. Li, Y. He, M. Z. Shou, C. Shen, L. Cheng, Y. Li, T. Gao, and D. Zhang, “Paragraph-to-image generation with informationenriched diffusion model,” _International Journal of Computer Vision_ , pp. 1–22, 2025. 

- [224] Y. Li, Y. Du, K. Zhou, J. Wang, W. X. Zhao, and J.-R. Wen, “Evaluating object hallucination in large vision-language models,” _arXiv preprint arXiv:2305.10355_ , 2023. 

- [225] K. Cheng, Q. Sun, Y. Chu, F. Xu, Y. Li, J. Zhang, and Z. Wu, “Seeclick: Harnessing gui grounding for advanced visual gui agents,” _arXiv preprint arXiv:2401.10935_ , 2024. 

- [226] K. Li, Z. Meng, H. Lin, Z. Luo, Y. Tian, J. Ma, Z. Huang, and T.-S. Chua, “Screenspot-pro: Gui grounding for professional highresolution computer use,” _arXiv preprint arXiv:2504.07981_ , 2025. 

- [227] S. Nayak, X. Jian, K. Q. Lin, J. A. Rodriguez, M. Kalsi, R. Awal, N. Chapados, M. T. Ozsu,<sup>¨</sup> A. Agrawal, D. Vazquez _et al._ , “Uivision: A desktop-centric gui benchmark for visual perception and interaction,” _arXiv preprint arXiv:2503.15661_ , 2025. 

- [228] S. Zhou, F. F. Xu, H. Zhu, X. Zhou, R. Lo, A. Sridhar, X. Cheng, T. Ou, Y. Bisk, D. Fried _et al._ , “Webarena: A realistic web environment for building autonomous agents,” _arXiv preprint arXiv:2307.13854_ , 2023. 

- [229] T. Xie, D. Zhang, J. Chen, X. Li, S. Zhao, R. Cao, T. J. Hua, Z. Cheng, D. Shin, F. Lei _et al._ , “Osworld: Benchmarking multimodal agents for open-ended tasks in real computer environments,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 52 040–52 094, 2024. 

- [230] R. Bonatti, D. Zhao, F. Bonacci, D. Dupont, S. Abdali, Y. Li, Y. Lu, J. Wagle, K. Koishida, A. Bucker _et al._ , “Windows agent arena: Evaluating multi-modal os agents at scale,” _arXiv preprint arXiv:2409.08264_ , 2024. 

- [231] X. H. Lu,` A. Kazemnejad, N. Meade, A. Patel, D. Shin, A. Zambrano, K. Stanczak, P. Shaw, C. J. Pal, and S. Reddy, “Agentreward-´ bench: Evaluating automatic evaluations of web agent trajectories,” _arXiv preprint arXiv:2504.08942_ , 2025. 

- [232] H. Chae, N. Kim, K. T.-i. Ong, M. Gwak, G. Song, J. Kim, S. Kim, D. Lee, and J. Yeo, “Web agents with world models: Learning and leveraging environment dynamics in web navigation,” _arXiv preprint arXiv:2410.13232_ , 2024. 

- [233] H. Bai, Y. Zhou, J. Pan, M. Cemri, A. Suhr, S. Levine, and A. Kumar, “Digirl: Training in-the-wild device-control agents with autonomous reinforcement learning,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 12 461–12 495, 2024. 

- [234] S. Jordan, Y. Chandak, D. Cohen, M. Zhang, and P. Thomas, “Evaluating the performance of reinforcement learning algorithms,” in _International Conference on Machine Learning_ . PMLR, 2020, pp. 4962–4973. 

- [235] R. Agarwal, M. Schwarzer, P. S. Castro, A. C. Courville, and M. Bellemare, “Deep reinforcement learning at the edge of the statistical precipice,” _Advances in neural information processing systems_ , vol. 34, pp. 29 304–29 320, 2021. 

- [236] J. Hessel, A. Holtzman, M. Forbes, R. L. Bras, and Y. Choi, “Clipscore: A reference-free evaluation metric for image captioning,” _arXiv preprint arXiv:2104.08718_ , 2021. 

- [237] Y. Chen, Y. Ge, R. Wang, Y. Ge, L. Qiu, Y. Shan, and X. Liu, “Exploring the effect of reinforcement learning on video understanding: Insights from seed-bench-r1,” _arXiv preprint arXiv:2503.24376_ , 2025. 

- [238] J. Cheng, Y. Ge, T. Wang, Y. Ge, J. Liao, and Y. Shan, “Video-holmes: Can mllm think like holmes for complex video reasoning?” _arXiv preprint arXiv:2505.21374_ , 2025. 

- [239] W. Xu, J. Wang, W. Wang, Z. Chen, W. Zhou, A. Yang, L. Lu, H. Li, X. Wang, X. Zhu, W. Wang, J. Dai, and J. Zhu, “Visulogic: A benchmark for evaluating visual reasoning in multi-modal large language models,” _arXiv preprint arXiv:2504.15279_ , 2025. [Online]. Available: https://arxiv.org/abs/2504.15279 

- [240] H. Yao, Q. Yin, J. Zhang, M. Yang, Y. Wang, W. Wu, F. Su, L. Shen, M. Qiu, D. Tao, and J. Huang, “R1-sharevl: Incentivizing reasoning capability of multimodal large language models via share-grpo,” 2025. 

- [241] S. Tian, R. Wang, H. Guo, P. Wu, Y. Dong, X. Wang, J. Yang, H. Zhang, H. Zhu, and Z. Liu, “Ego-r1: Chain-of-tool-thought for ultra-long egocentric video reasoning,” 2025. 

- [242] Y. Chen, W. Huang, B. Shi, Q. Hu, H. Ye, L. Zhu, Z. Liu, P. Molchanov, J. Kautz, X. Qi _et al._ , “Scaling rl to long videos,” _arXiv preprint arXiv:2507.07966_ , 2025. 

- [243] H. Shao, S. Qian, H. Xiao, G. Song, Z. Zong, L. Wang, Y. Liu, and H. Li, “Visual cot: Unleashing chain-of-thought reasoning in multi-modal language models,” _arXiv preprint arXiv:2403.16999_ , 2024. 

- [244] Y. Wang, Z. Wang, B. Xu, Y. Du, K. Lin, Z. Xiao, Z. Yue, J. Ju, L. Zhang, D. Yang, X. Fang, Z. He, Z. Luo, W. Wang, J. Lin, J. Luan, and Q. Jin, “Time-r1: Post-training large vision language model for temporal video grounding,” _arXiv preprint arXiv:2503.13377_ , 2025. 

- [245] J. Yang, S. Yang, A. Gupta, R. Han, L. Fei-Fei, and S. Xie, “Thinking in Space: How Multimodal Large Language Models See, Remember and Recall Spaces,” _arXiv preprint arXiv:2412.14171_ , 2024. 

- [246] J. Yuan, T. Peng, Y. Jiang, Y. Lu, R. Zhang, K. Feng, C. Fu, T. Chen, L. Bai, B. Zhang _et al._ , “Mme-reasoning: A comprehensive benchmark for logical reasoning in mllms,” _arXiv preprint arXiv:2505.21327_ , 2025. 

- [247] K. Wang, J. Pan, L. Wei, A. Zhou, W. Shi, Z. Lu, H. Xiao, Y. Yang, H. Ren, M. Zhan, and H. Li, “Mathcoder- 

21 

   - VL: Bridging vision and code for enhanced multimodal mathematical reasoning,” in _The 63rd Annual Meeting of the Association for Computational Linguistics_ , 2025. [Online]. Available: https://openreview.net/forum?id=nuvtX1imAb 

- [248] P. Lu, H. Bansal, T. Xia, J. Liu, C. Li, H. Hajishirzi, H. Cheng, K.-W. Chang, M. Galley, and J. Gao, “Mathvista: Evaluating mathematical reasoning of foundation models in visual contexts,” in _International Conference on Learning Representations (ICLR)_ , 2024. 

- [249] R. Zhang, D. Jiang, Y. Zhang, H. Lin, Z. Guo, P. Qiu, A. Zhou, P. Lu, K.-W. Chang, P. Gao _et al._ , “Mathverse: Does your multimodal llm truly see the diagrams in visual math problems?” _arXiv preprint arXiv:2403.14624_ , 2024. 

- [250] Y. Hao, J. Gu, H. W. Wang, L. Li, Z. Yang, L. Wang, and Y. Cheng, “Can mllms reason in multimodality? emma: An enhanced multimodal reasoning benchmark,” _arXiv preprint arXiv:2501.05444_ , 2025. 

- [251] R. Qiao, Q. Tan, G. Dong, M. Wu, C. Sun, X. Song, Z. GongQue, S. Lei, Z. Wei, M. Zhang _et al._ , “We-math: Does your large multimodal model achieve human-like mathematical reasoning?” _arXiv preprint arXiv:2407.01284_ , 2024. 

- [252] C. Zou, X. Guo, R. Yang, J. Zhang, B. Hu, and H. Zhang, “Dynamath: A dynamic visual benchmark for evaluating mathematical reasoning robustness of vision language models,” 2024. 

- [253] H. Cai, Y. Yang, and W. Hu, “Mm-iq: Benchmarking human-like abstraction and reasoning in multimodal models,” _arXiv preprint arXiv:2502.00698_ , 2025. 

- [254] C. He, R. Luo, Y. Bai, S. Hu, Z. L. Thai, J. Shen, J. Hu, X. Han, Y. Huang, Y. Zhang, J. Liu, L. Qi, Z. Liu, and M. Sun, “Olympiadbench: A challenging benchmark for promoting agi with olympiadlevel bilingual multimodal scientific problems,” 2024. 

models to versatile gui agents,” _arXiv preprint arXiv:2406.11317_ , 2024. 

   - [267] X. Puig, E. Undersander, A. Szot, M. D. Cote, T.-Y. Yang, R. Partsey, R. Desai, A. W. Clegg, M. Hlavac, S. Y. Min _et al._ , “Habitat 3.0: A co-habitat for humans, avatars and robots,” _arXiv preprint arXiv:2310.13724_ , 2023. 

   - [268] J. Krantz, E. Wijmans, A. Majumdar, D. Batra, and S. Lee, “Beyond the nav-graph: Vision-and-language navigation in continuous environments,” in _European Conference on Computer Vision_ . Springer, 2020, pp. 104–120. 

   - [269] S. James, Z. Ma, D. R. Arrojo, and A. J. Davison, “Rlbench: The robot learning benchmark & learning environment,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 2, pp. 3019–3026, 2020. 

   - [270] S. Nasiriany, A. Maddukuri, L. Zhang, A. Parikh, A. Lo, A. Joshi, A. Mandlekar, and Y. Zhu, “Robocasa: Large-scale simulation of everyday tasks for generalist robots,” _arXiv preprint arXiv:2406.02523_ , 2024. 

   - [271] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “Libero: Benchmarking knowledge transfer for lifelong robot learning,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 44 776–44 791, 2023. 

   - [272] S. Zhang, Z. Xu, P. Liu, X. Yu, Y. Li, Q. Gao, Z. Fei, Z. Yin, Z. Wu, Y.-G. Jiang _et al._ , “Vlabench: A large-scale benchmark for languageconditioned robotics manipulation with long-horizon reasoning tasks,” _arXiv preprint arXiv:2412.18194_ , 2024. 

   - [273] R. Abhyankar, Q. Qi, and Y. Zhang, “Osworld-human: Benchmarking the efficiency of computer-use agents,” _arXiv preprint arXiv:2506.16042_ , 2025. 

- [255] J. Roberts, M. R. Taesiri, A. Sharma, A. Gupta, S. Roberts, I. Croitoru, S.-V. Bogolin, J. Tang, F. Langer, V. Raina _et al._ , “Zerobench: An impossible visual benchmark for contemporary large multimodal models,” _arXiv preprint arXiv:2502.09696_ , 2025. 

- [256] X. Yue, T. Zheng, Y. Ni, Y. Wang, K. Zhang, S. Tong, Y. Sun, B. Yu, G. Zhang, H. Sun, Y. Su, W. Chen, and G. Neubig, “Mmmupro: A more robust multi-discipline multimodal understanding benchmark,” _arXiv preprint arXiv:2409.02813_ , 2024. 

- [257] D. Jiang, R. Zhang, Z. Guo, Y. Li, Y. Qi, X. Chen, L. Wang, J. Jin, C. Guo, S. Yan _et al._ , “Mme-cot: Benchmarking chain-of-thought in large multimodal models for reasoning quality, robustness, and efficiency,” _arXiv preprint arXiv:2502.09621_ , 2025. 

- [258] Q. Yan, Y. Fan, H. Li, S. Jiang, Y. Zhao, X. Guan, C.-C. Kuo, and X. E. Wang, “Multimodal inconsistency reasoning (mmir): A new benchmark for multimodal reasoning models,” 2025. [Online]. Available: https://arxiv.org/abs/2502.16033 

- [259] J. Wang, Y. Ming, Z. Shi, V. Vineet, X. Wang, Y. Li, and N. Joshi, “Is a picture worth a thousand words? delving into spatial reasoning for vision language models,” in _The Thirty-Eighth Annual Conference on Neural Information Processing Systems_ , 2024. 

- [260] Q. Yang, S. Yao, W. Chen, S. Fu, D. Bai, J. Zhao, B. Sun, B. Yin, X. Wei, and J. Zhou, “Humanomniv2: From understanding to omni-modal reasoning with context,” _arXiv preprint arXiv:2506.21277_ , 2025. 

- [261] X. Wu, Y. Hao, K. Sun, Y. Chen, F. Zhu, R. Zhao, and H. Li, “Human preference score v2: A solid benchmark for evaluating human preferences of text-to-image synthesis,” _arXiv preprint arXiv:2306.09341_ , 2023. 

- [262] J. A. Rodriguez, A. Puri, S. Agarwal, I. H. Laradji, P. Rodriguez, S. Rajeswar, D. Vazquez, C. Pal, and M. Pedersoli, “Starvector: Generating scalable vector graphics code from images and text,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 16 175–16 186. 

- [263] X. Deng, Y. Gu, B. Zheng, S. Chen, S. Stevens, B. Wang, H. Sun, and Y. Su, “Mind2web: Towards a generalist agent for the web,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 28 091–28 114, 2023. 

- [264] J. Zhang, J. Wu, Y. Teng, M. Liao, N. Xu, X. Xiao, Z. Wei, and D. Tang, “Android in the zoo: Chain-of-action-thought for gui agents,” _arXiv preprint arXiv:2403.02713_ , 2024. 

- [265] R. Kapoor, Y. P. Butala, M. Russak, J. Y. Koh, K. Kamble, W. AlShikh, and R. Salakhutdinov, “Omniact: A dataset and benchmark for enabling multimodal generalist autonomous agents for desktop and web,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 161–178. 

- [266] W. Chen, J. Cui, J. Hu, Y. Qin, J. Fang, Y. Zhao, C. Wang, J. Liu, G. Chen, Y. Huo _et al._ , “Guicourse: From general vision language 

22 

TABLE 3: **Public benchmarks of MLLM most commonly used in visual RL.** Only benchmarks relevant to visual reinforcement learning are included (RL-focused training & evaluation); task-specific benchmarks, such as MME [189], are excluded from consideration. ‘Tr’ and ‘Te’ refer to the ‘Train’ and ‘Test’, respectively. 

|**Task family**|**Benchmark**|**Date**|**Tr/Te**|**Description**(benchmark info. and RL reward signal)|
|---|---|---|---|---|
||**SEED-Bench-R1**[237]<br>**Video-Holmes**[238]|Mar 2025<br>May 2025|Tr&Te<br>Te|Video-QA pairs with human-preference reward model (used in [237])<br>Human-ranked T2I pairs from diverse generation models (used in [238])|
||**VisuLogic**[239]<br>**R1-ShareVL**[240]|Apr 2025<br>May 2025|Tr&Te<br>Tr|Visual-reasoning QA set; exact-match reward enables RL fine-tuning (used in [239])<br>52 k MM-Eureka subset for Share-GRPO RL training (used in [240])|
||**Ego-R1**[241]<br>**Long-RL**[242]<br>|Jun 2025<br>Jul 2025<br>|Tr&Te<br>Tr&Te<br>|25 k CoTT egocentric traces enabling RL training for ultra-long video reasoning (used in [241])<br>104 K long-video QA pairs (GRPO accuracy / format reward) (used in [242])<br>|
||**VisCOT**[243]|Mar 2024|Tr&Te|438 k visual chain-of-thought traces with step-wise rewards for RL (used in [243])|
||**MMK12**[77]|Mar 2025|Tr&Te|<br>15.6 K multimodal math problems (rule-based accuracy / format rewards) (used in [77])|
||**Time-R1**[244]|Mar 2025|Tr&Te|2.5 K TimeRFT grounding spans (IoU reward) (used in [244])|
||**VSI-Bench**[245]|Dec 2024|Te|Spatial QA benchmark offering RL exact-match reward (used in [245])|
||**MME-**<br>**Reasoning**[246]|May 2025|Te|Logic QA benchmark (used in [246])|
||**K12-2M**[247]|May 2025|Tr|2 M multimodal math pairs for RL training (used in [247])|
|**Multimodal**|**MathVista**[248]|Oct 2023|Te|Visual-math QA benchmark; test-only RL exact-match reward (used in [248])|
|**LLMs / VLMs**|**MathVerse**[249]|Mar 2024|Te|Diagram-math QA benchmark; test-only RL exact-match reward (used in [249])|
||**EMMA**[250]|Jan 2025|Te|Robust multimodal reasoning benchmark challenging current MLLMs (used in [250])|
||**WeMath**[251]|Jul 2024|Te|<br>Multimodal math reasoning benchmark with diagrams (used in [251])|
||**DynaMATH**[252]<br>**MM-IQ**[253]|Oct 2024<br>Feb 2025|Te<br>Te|<br>Dynamic visual math reasoning robustness benchmark for VLMs (used in [252])<br>Human-like multimodal abstraction and reasoning benchmark (used in [253])|
||**OlympiadBench**[254]|Feb 2024|Te|Bilingual multimodal Olympiad-level scientific reasoning benchmark (used in [254])|
||**ZeroBench**[255]<br>|Feb 2025<br>|Te|near-impossible visual reasoning stress test for LMMs (used in [255])<br>|
||**MMMU-Pro**[256]<br>**MME-CoT**[257]<br>**MMIR**[258]|Sep 2024<br>Feb 2025<br>Feb 2025|Te<br>Te<br>Te|robust multidisciplinary multimodal understanding benchmark (used in [256])<br>Multimodal chain-of-thought reasoning benchmark dataset (used in [257])<br>Multimodal inconsistency reasoning benchmark dataset (used in [258])|
||**SpatialEval**[259]|Jun 2024|Te|Synthetic spatial reasoning benchmark for VLMs (used in [259])|
||**MMReason**[259]|Jun 2025|Te|Synthetic spatial reasoning benchmark for VLMs (used in [259])|
||**IntentBench**[260]|Jun 2025|Te|Omnimodal evaluation demands unified audio-visual comprehension (used in [260])|
||**ImageReward**[21]|Apr 2023|Tr&Te|Human-ranked pairs for T2I; reward model outputs scalar score (used in [129], [132], [134])|
||**HPS**[24]|Mar 2023|Tr&Te|Human-ranked T2I pairs from diverse generation models (used in [24])|
||**HPS V2**[261]|Jun 2023|Tr&Te|Human-ranked T2I pairs across diverse prompts, preference-based reward (used in [120], [124])|
||**Pick-a-Pic**[214]|May 2023|Tr&Te|User preferences for pairwise rankings over T2I generations (used in [122], [123], [124], [126])|
|**Visual**<br>**Generation**|**VideoReward**[141]|Jan 2025|Te|Human-ranked video pairs across quality, motion, and text alignment (used in [141])|
|(image/video/3D)|**T2I-CompBench**[209]|Jul 2023|Tr&Te|Compositional text-to-image dataset covering attributes and object relations. (used in [117],<br>[120])|
||**StarVector**[262]|Dec 2023|Tr&Te|SVG Code Generation Data, Match Reward (used in [119])|
||**AnimeReward**[143]|Apr 2025|Tr|Multi-dimensional (_e.g.,_character consisten) human preference anime videos (used in [143])|
||**VideoPrefer**[147]|Dec 2024|Tr|MLLM-annotated 135K video preference pairs (used in [147])|
||**GUI-R1-3K**[10]|Apr 2025|Tr&Te|GUI trajectories spanning Windows, Linux, macOS, Android, and Web platforms (used in [10])|
||**SE-GUI-3k**[11]|May 2025|Tr|3,018 examples (desktop / web / mobile) with instruction and bounding box (used in [11])|
||**UI-R1**[156]|May 2025|Tr|136 mobile GUI tasks covering 5 action types (click, scroll, swipe, text-input) (used in [11])|
||**CAGUI**[158]|Jun 2025|Te|55 K trajectories from 30 Chinese Android apps, 8 domains (used in [11])|
||**Mobile-R1**[160]|Jun 2025|Tr&Te|More than 500 online task trajectories from 28 Chinese as (used in [160])|
||<br>**Mind2web**[263]|<br>Jun 2023|Tr&Te|pp<br>2 k tasks on 137 real websites; success/fail reward for RL (used in [162], [263])|
|**Vision–Language**|<br>**AITZ**[264]|<br>Jun 2023|Tr&Te|<br>18,643 Android screen–action pairs with CoAT reasoning (used in [264])|
|**Action Agents**|<br>**Omniac**[265]|<br>Feb 2024|Tr&Te|<br>Desktop + web 9.8 k scripted tasks (used in [265])|
||**GUICours**[266]|Jun 2024|Tr&Te|<br>GUIEnv/Act/Chat datasets (10 M OCR + 67 k navigation) (used in [266])|
||**Habitat 3.0**[267]|Oct 2023|Tr&Te|Interactive embodied-AI scenes with humans and robots (used in [267])|
||**VLN-CE**[268]|Apr 2020|Tr&Te|Continuous embodied navigation dataset with language instructions (used in [268])|
||**Rlbench**[269]|Apr 2020|Tr&Te|Multi-task simulated robot manipulation benchmark dataset (used in [269])|
||<br>**RoboCasa**[270]|<br>Jun 2024|Tr|<br>Large-scale kitchen-task simulation for generalist robotics (used in [270])|
||**LIBERO**[271]|Jun 2023|Tr|<br>Lifelong robot learning benchmark with 100 manipulation tasks (used in [271])|
||**VLABench**[272]|Dec 2024|Tr&Te|<br>Long-horizon language-conditioned manipulation benchmark for robots (used in [272])|


23 

TABLE 4: **Public benchmarks of Visual Generation (image/video/3D) most commonly used in visual RL.** Only benchmarks relevant to visual reinforcement learning are included (RL-focused training & evaluation). ‘Tr’ and ‘Te’ refer to the ‘Train’ and ‘Test’, respectively. 

|**Benchmark**|**Date**|**Tr/Te**|**Description**(benchmark info. and RL reward signal)|
|---|---|---|---|
|**ImageReward**[21]|Apr 2023|Tr&Te|Human-ranked pairs for T2I; reward model outputs scalar score (used<br>in [129], [132], [134])|
|**HPS**[24]|Mar 2023|Tr&Te|Human-ranked T2I pairs from diverse generation models (used in [24])|
|**HPS V2**[261]|Jun 2023|Tr&Te|Human-ranked T2I pairs across diverse prompts, preference-based reward<br>(used in [120], [124])|
|**Pick-a-Pic**[214]|May 2023|Tr&Te|User preferences for pairwise rankings over T2I generations (used in [122],<br>[123], [124], [126])|
|**VideoReward**[141]|Jan 2025|Te|Human-ranked video pairs across quality, motion, and text alignment (used<br>in [141])|
|**T2I-CompBench**[209]|Jul 2023|Tr&Te|Compositional text-to-image dataset covering attributes and object relations.<br>(used in [117], [120])|
|**StarVector**[262]|Dec 2023|Tr&Te|SVG Code Generation Data, Match Reward (used in [119])|
|**AnimeReward**[143]|Apr 2025|Tr|Multi-dimensional (_e.g.,_character consisten) human preference anime videos<br>(used in [143])|
|**VideoPrefer**[147]|Dec 2024|Tr|MLLM-annotated 135K video preference pairs (used in [147])|


TABLE 5: **Public benchmarks of VLAs most commonly used in visual RL.** Only benchmarks relevant to visual reinforcement learning are included (RL-focused training & evaluation). ‘Tr’ and ‘Te’ refer to the ‘Train’ and ‘Test’, respectively. 

|**Benchmark**|**Date**|**Tr/Te**|**Description**(benchmark info. and RL reward signal)|
|---|---|---|---|
|**GUI-R1-3K**[10]|Apr 2025|Tr&Te|GUI trajectories spanning Windows, Linux, macOS, Android, and Web<br>platforms|
|**SE-GUI-3k**[11]|May 2025|Tr|3,018 examples (desktop / web / mobile) with instruction and bounding box|
|**UI-R1**[156]|May 2025|Tr|136 mobile GUI tasks covering 5 action types (click, scroll, swipe, text-input)|
|**CAGUI**[158]|Jun 2025|Te|55 K trajectories from 30 Chinese Android apps, 8 domains|
|**Mobile-R1**[160]|Jun 2025|Tr&Te|More than 500 online task trajectories from 28 Chinese apps|
|**Mind2web**[263]|Jun 2023|Tr&Te|2 k tasks on 137 real websites; success/fail reward for RL|
|**AITZ**[264]|Jun 2023|Tr&Te|18,643 Android screen–action pairs with CoAT reasoning|
|**Omniac**[265]|Feb 2024|Tr&Te|Desktop + web 9.8 k scripted tasks|
|**GUICours**[266]|Jun 2024|Tr&Te|GUIEnv/Act/Chat datasets (10 M OCR + 67 k navigation)|
|**Habitat**[267]|Oct 2023|Tr&Te|Interactive embodied-AI scenes with humans and robots|
|**VLN-CE**[268]|Apr 2020|Tr&Te|Continuous embodied navigation dataset with language instructions|
|**RLBench**[269]|Apr 2020|Tr&Te|Multi-task simulated robot manipulation benchmark dataset|
|**RoboCasa**[270]|Jun 2024|Tr|Large-scale kitchen-task simulation for generalist robotics|
|**LIBERO**[271]|Jun 2023|Tr|Lifelong robot learning benchmark with 100 manipulation tasks|
|**VLABench**[272]|Dec 2024|Tr&Te|Long-horizon language-conditioned manipulation benchmark for robots|


