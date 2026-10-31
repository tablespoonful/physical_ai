---
title: "LongNav-R1: Horizon-Adaptive Multi-Turn RL for Long-Horizon VLA Navigation"
date: "2026-02-12"
authors: "Yue Hu; Avery Xi; Qixin Xiao; Seth Isaacson; Henry X. Liu; Ram Vasudevan"
venue: "RSS 2026"
url: https://arxiv.org/abs/2602.12351
pdf: https://arxiv.org/pdf/2602.12351
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.12351)** / [論文ページ](https://arxiv.org/abs/2602.12351)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# LongNav-R1: Horizon-Adaptive Multi-Turn RL for Long-Horizon VLA Navigation 

Yue Hu<sup>1</sup> , Avery Xi<sup>1</sup> , Qixin Xiao<sup>1</sup> , Seth Isaacson<sup>1</sup> , Henry X. Liu<sup>1</sup> , Ram Vasudevan<sup>1</sup> , Maani Ghaffari<sup>1</sup> 

> 1 University of Michigan, Ann Arbor 

{huyu,axi,qxiaocs,sethgi,henryliu,ramv,maanigj}@umich.edu 


Fig. 1: LongNav-R1 formulates the navigation process as a multi-turn conversation between the VLA policy and the embodied environment. This end-to-end multi-turn RL framework enables the VLA policy to optimize multi-step decision-making based on cumulative, sequential outcomes. 

**_Abstract_ —This paper develops LongNav-R1, an end-to-end multi-turn reinforcement learning (RL) framework designed to optimize Visual-Language-Action (VLA) models for long-horizon navigation. Unlike existing single-turn paradigm, LongNav-R1 reformulates the navigation decision process as a continuous multiturn conversation between the VLA policy and the embodied environment. This multi-turn RL framework offers two distinct advantages: i) it enables the agent to reason about the causal effects of historical interactions and sequential future outcomes; and ii) it allows the model to learn directly from online interactions, fostering diverse trajectory generation and avoiding the behavioral rigidity often imposed by human demonstrations. Furthermore, we introduce Horizon-Adaptive Policy Optimization. This mechanism explicitly accounts for varying horizon lengths during advantage estimation, facilitating accurate temporal credit assignment over extended sequences. Consequently, the agent develops diverse navigation behaviors and resists collapse during long-horizon tasks. Experiments on object navigation benchmarks validate the framework’s efficacy: With 4,000 rollout trajectories, LongNav-R1 boosts the Qwen3-VL-2B success rate from 64.3% to 73.0%. These results demonstrate superior sample efficiency and significantly outperform state-of-the-art methods. The model’s generalizability and robustness are further validated by its zero-shot performance** 

**in long-horizon real-world navigation settings. All source code is open-sourced at https://github.com/UMich-CURLY/LongNav-R1.** 

## I. INTRODUCTION 

Navigation is a fundamental capability for intelligent embodied agents, serving as the cornerstone for robots to assist humans in physical environments. Historically, navigation systems relied on modular pipelines [53, 2, 7, 74, 36] involving separate perception [29], mapping [76, 64], and planning [20, 62, 63] components. However, recent progress has shifted toward endto-end Vision-Language-Action (VLA) models [71, 70, 49]. These models leverage large-scale pre-training to enable general semantic navigation, allowing agents to interpret complex visual cues and linguistic commands directly into actions. 

Despite these advancements, current navigation approaches remain far from achieving human-level performance, particularly in long-horizon tasks. This is because existing state-ofthe-art methods [71, 70, 28, 49] adopt a single-turn imitation learning paradigm, which reduces navigation to a sequence of isolated action predictions based on immediate local context. 


Fig. 2: Comparison of single-turn SFT and multi-turn RL. 

This formulation introduces two critical deficiencies: first, it lacks causal reasoning by treating steps independently, thereby overlooking the sequential dependencies where early-stage exploration serves as a prerequisite for late-stage, goal-directed efficiency. Second, it leads to behavioral rigidity by strictly imitating expert trajectories instead of optimizing for goal success. Consequently, the agent becomes myopic and brittle, incapable of recovering from errors or adapting to distribution shifts. 

To bridge this gap, this paper proposes LongNav-R1, an end-to-end framework that reformulates navigation as a multiturn Reinforcement Learning (RL) process. Unlike the singleturn paradigm, LongNav-R1 treats the navigation task as a continuous conversation between the VLA policy and the physical environment. This multi-turn formulation offers two key advantages. First, it provides the model with comprehensive state and objective awareness, allowing it to learn the causal relationship between current actions and distant rewards. Second, by learning directly from online interactions, the agent is encouraged to explore diverse trajectories, thereby overcoming the rigidity of human demonstrations and improving robustness against environmental stochasticity. 

While multi-turn RL offers a promising framework for longhorizon VLA navigation, its deployment is bottlenecked by the challenge of temporal credit assignment, as the relative contribution of each turn to the final objective varies significantly over time. While actor-critic methods like PPO [41] manage this via learned value functions, they incur prohibitive computational overhead during long-horizon training. Conversely, efficient critic-free methods from the LLM domain, such as GRPO [42] and REINFORCE++ [19], are optimized for single-turn tasks with outcome-level rewards and fail to capture the evolving temporal statistics inherent in multi-step robotic decisionmaking. 

To address this bottleneck, we introduce Horizon-Adaptive Policy Optimization (HAPO), a framework for critic-free advantage estimation. HAPO eliminates the need for a separate value network by regressing a baseline directly from the local rollout buffer via kernel regression. Drawing inspiration from variance reduction techniques in verifiable RL [68], we introduce a general formulation that unifies the advantage estimation of critic-free methods with the value function approximation of actor-critic architectures. Under this formulation, existing optimization heuristics such as GRPO and REINFORCE++ emerge as special cases determined by specific kernel choices. By explicitly designing a temporal kernel function, HAPO enables the derived baseline to capture the reward’s temporal 

dynamics of long-horizon navigation, offering the temporal precision of a critic without the associated computational overhead. HAPO enables optimizing VLA models for the varying sequence lengths inherent in long-horizon robotic tasks. 

To validate the effectiveness of LongNav-R1 and HAPO, we conducted three key evaluations. First, we validated LongNav-R1 across real-world settings and four widely-used simulation benchmarks. Despite being trained on only six object categories in HM3D V1 [37], LongNav-R1 successfully localizes unseen objects in zero-shot real-world scenarios and outperforms previous SOTA methods on HM3D V1 [37], V2 [59], MP3D [23] and OVON [65], demonstrating robust generalizability. Second, we conducted ablation studies on core components. Results indicate that multi-turn RL contributes a substantial improvement of 8.7% on success rate compared to SFT, while HAPO is critical for unlocking long-horizon navigation, boosting success rates from 0% to 15.4%. Third, we demonstrated that LongNav-R1 yields highly sample-efficient agents. The success rate of a Qwen3-VL-2B backbone increased from 0.51% to 73.0% using only 34k trajectories, outperforming SFT baselines trained on millions of data. 

To summarize, the primary contributions of this paper are: 

- (i) We propose LongNav-R1, a end-to-end multi-turn reinforcement learning framework that optimizes the VLA policy for multi-step navigation. 

- (ii) We introduce HAPO, a critic-free advantage estimation framework that facilitates precise temporal credit assignment, allowing large VLA models to improve multi-step decision-making without the significant computational burden of auxiliary critic networks. 

- (iii) We provide a comprehensive experimental validation of LongNav-R1 in real-world and diverse navigation benchmarks, demonstrating that LongNav-R1 significantly outperforms existing methods. 

II. RELATED WORKS 

**Semantic navigation.** Semantic navigation requires agents to navigate to the specific target in unseen environments based on human instructions. There are two representative tasks that involve both visual information and language instructions: Object Goal Navigation [10, 37, 59, 8] and Vision-and-Language Navigation [4, 24, 25]. Early methods [51, 33, 61, 31, 32] largely focused on acquiring task-specific skills via imitation learning [38, 39] or RL [9, 16, 13, 69]. While these methods can achieve strong performance in trained environments, they often suffer from poor generalization due to domain gaps. Recently, the field has shifted toward leveraging the generalization capabilities of Large-Language Models (LLMs) and VisionLanguage Models (VLMs) to improve multi-task navigation. These approaches [22, 34, 44, 5, 45, 6, 14, 27, 66, 75, 30, 21, 62, 71, 70, 28] offer greater flexibility and adaptability in novel environments, but often lack optimized task execution and navigation efficiency, resulting in inferior performance. In contrast, our method trains a VLA model end-to-end with navigation objective, offering both task-aware efficiency and generalization capability. 

**Large language model for embodied navigation.** Large language models have been introduced into robotic navigation due to their generalization capabilities in understanding and planning. Current research follows two primary trajectories. The first utilizes off-the-shelf LLMs and VLMs in a zeroshot fashion. These methods employ LLMs and VLMs as high-level policies to identify landmarks [67, 66] and select frontiers [30, 30, 21, 62]. The second trajectory [70, 71, 49] involves fine-tuning VLMs as end-to-end VLA models that directly generate actions via Supervised Fine-Tuning (SFT). However, SFT-based methods are often bottlenecked by the need for exhaustive expert demonstrations and are susceptible to the domain drift inherent in behavior cloning. To overcome these limitations, we train our VLA model using end-to-end RL, which facilitates the discovery of diverse navigation skills and enhances final navigation performance. 

**Reinforcement learning for large language model.** Reinforcement learning has become a crucial post-training technique for large language models, facilitating alignment with human preferences [35] and significantly bolstering reasoning capabilities [6]. While these advancements have primarily been applied to web search [50, 54] and tool-use [47, 55, 48], adapting these benefits to embodied navigation remains an open challenge. A pioneering effort, Nav-R1 [28], adopts the DeepSeek-R1 paradigm [17] by generating navigation action sequences in a single turn and training the VLA model via GRPO [42]. However, embodied navigation is inherently a multi-turn decision-making process involving hundreds of steps; a single-turn formulation fails to capture its sequential and long-horizon nature. To address this, we propose an end-to-end, multi-turn RL framework for VLA models. Furthermore, rather than directly adopting standard advantage estimations from GRPO [42], REINFORCE++ [19], or RLOO [1], we introduce horizon-adaptive advantage estimation. This technique stabilizes interaction-adaptive optimization and improves longhorizon decision-making performance in embodied navigation. 

## III. PROBLEM FORMULATION 

This section establishes the mathematical formulation for robotic navigation using a VLA policy. We first introduce the navigation objective and frame the multi-step navigation decision process as a multi-turn conversation. Then we define a multi-turn RL formulation tailored for VLAs. Building on this foundation, we introduce critic-free horizon-adaptive policy optimization to optimize VLA for long-horizon objective. 

_A. Navigation task objective_ 

We address the task of general robotic navigation in unknown environments. In this setting, an agent is provided with a open instruction _I_ , describing either a target object or a sequence of steps, and iteratively perceives and interacts with the environment to locate the goal. At each time step _t_ , the agent receives an observation _vt_ and constructs a state _st_ . Action selection is governed by a parameterized policy _πθ_ conditioned on the current state _st_ : 


An episode terminates when the agent invokes a ‘stop’ action. Success is defined as reaching the target’s vicinity within a fixed step budget. Our objective is to optimize _πθ_ to maximize both navigation efficiency and success rate. 

## _B. Multi-turn RL formulation of VLA policy_ 

To solve the general navigation tasks, we utilize recent advances in large foundation models to optimize a VLA policy under the navigation objective. Given that navigation is a long-horizon process often spanning hundreds of steps, we frame the task as a multi-turn conversation between the VLA policy and its embodied environment. We model actions autoregressively, conditioned on the global instruction _I_ , history _{v_ 1: _t−_ 1 _, a_ 1: _t−_ 1 _}_ , and current observation _vt_ : 


This multi-turn RL framework offers two advantages. First, it enables KV cache reuse, significantly enhancing computational efficiency during training and inference. The history _{v_ 1: _t−_ 1 _, a_ 1: _t−_ 1 _}_ is saved in cache and only need to compute new observation. This optimization is critical for long-horizon navigation, which involves hundreds of steps and generates hundreds of thousands of visual tokens. Second, the sequential nature of our formulation allows the model to explicitly account for the causal dependencies of prior interactions. By attributing the final trajectory outcome to individual actions, we improve both learning efficiency and performance on long-horizon tasks. **Comparison with existing VLA policies.** In contrast to UniNavid [71] and Nav-R1 [28], which adopt a singleturn paradigm, our multi-turn paradigm explicitly models the sequence effects. These prior works predict actions and optimize at the step-level, failing to capture the sequential nature of navigation. Furthermore, while StreamVLN [49] utilizes a multi-turn structure, it relies on SFT. Consequently, it suffers from the severe distribution shift issues inherent to behavior cloning and lacks a mechanism to directly optimize for the final, long-term success of the navigation task. 

## _C. Horizon-adaptive policy optimization_ 

To optimize VLA policies for long-horizon navigation, we propose Horizon-Adaptive Policy Optimization (HAPO). While recent advancements such as REINFORCE++ [19] and GRPO [42] have demonstrated efficacy in LLM training, their applicability is constrained by a reliance on single-turn paradigms and sparse, outcome-level rewards. By treating all time steps uniformly, these frameworks fail to capture the temporal dynamics of robotic navigation. In reality, moments like critical turns are far more determinative of success than routine straight-line movements. HAPO addresses this temporal credit assignment challenge by employing a kernel-based advantage estimator that uses step-level dense rewards, allowing the model to explicitly weigh contributions across varying horizons. HAPO has two phases: i) formulating advantage estimation as a generalized non-parametric value estimation framework via kernel regression, and ii) introducing a temporal kernel design to enable horizon-adaptive advantage estimation. 


Fig. 3: The overall pipeline of LongNav-R1. The framework optimizes the VLA policy through a three-stage iterative process: i) collecting long-horizon trajectories via multi-turn interactive rollout; ii) computing action-level advantages using the proposed horizon-adaptive estimator; and iii) updating the VLA model via the aggregated optimization objective. 

**General kernel-based advantage estimation.** Following the theoretical framework established in [68], we model critic-free baselines as non-parametric value function approximations. Unlike parametric critics that approximate values over the global state space, non-parametric critic-free methods perform local regression based strictly on the current rollout buffer. The key idea is to formalize value estimation as a kernel regression problem over the rollout buffer, which induces a generalized framework for advantage estimation, capable of adapting to diverse task objectives through specialized kernel designs. 

Specifically, let _B_ = _{τ_<sup>_i_</sup> _}_<sup>_B_</sup> _i_ =1<sup>denoteabufferofcomplete</sup> rollout trajectories _τ_<sup>_i_</sup> = _{_ ( _s_<sup>_i_</sup> _t_<sup>_, ai_</sup> _t_<sup>_, r_</sup> _t_<sup>_i_)</sup><sup>_}T_</sup> _t_ =1<sup>.Foreachaction</sup><sup>_a_</sup> _t_<sup>_i_</sup> at timestep _t_ in trajectory _τ_<sup>_i_</sup> , the advantage _A_<sup>_i_</sup> _t_<sup>isdefinedas</sup> 


where _G_<sup>_i_</sup> _t_<sup>isthereturnwithdiscountfactor</sup><sup>_γ_,and</sup><sup>_V_</sup> _B_<sup>_K_(</sup><sup>_·_)</sup> denotes a kernel-based baseline. Specifically, the baseline is computed via leave-one-out kernel regression: 


where _f_ ( _·_ ) is a feature mapping and _K_ ( _·, ·_ ) is a similarity kernel defined in the feature space. The leave-one-out construction _j̸_ = _i_ excludes samples from the current trajectory to avoid self-bias and ensure unbiased estimation. This formulation subsumes a broad class of critic-free advantage estimators 

through appropriate choices of the kernel _K_ and feature representation _f_ , enabling task-dependent value estimation without learning a parametric critic. For instance, in scenarios governed by temporal dynamics, a time-aware kernel can be employed to capture sequential dependencies; conversely, in environments where geometric configuration is paramount, a spatial-aware kernel is more appropriate for modeling structural regularities. Explicitly integrating these state features yields significantly more accurate value estimates. 

**Temporal-aware kernel design.** To explicitly account for the sequential structure of navigation, HAPO introduces a time-aware kernel. We account for the temporal dynamics by explicitly defining the discrete time step as the feature, _f_ ( _s_<sup>_t_</sup> _i_<sup>) =</sup> _−_<sup>_<u>|x−x′|</u>_2</sup> _t_ , and employ a Gaussian kernel _K_ ( _x, x_<sup>_′_</sup> ) = exp � 2 _σ_<sup>2</sup> � with bandwidth _σ_ , to provide temporal smoothing for the value estimates. By applying this formulation, HAPO regresses a baseline that is strictly specific to the current horizon of the episode. This enables the advantage estimator to adapt to the shifting reward distributions inherent in navigation, effectively distinguishing between the high-variance exploration phase (early horizon) and the high-precision target acquisition phase (late horizon). 

**Comparison with REINFORCE++.** HAPO provides a general advantage estimation framework while existing methods such as REINFORCE++ emerges as special cases. Specifically, REINFORCE++ corresponds to the use of a constant kernel _K_ ( _·, ·_ ) = 1 with features defined only at the final outcome state. Under this setting, the value estimate reduces to the mean final reward of the rollout buffer: _VB_<sup>_K_(</sup><sup>_s_</sup> _T_<sup>_i_)=</sup> _B_ <u>1</u> � _Bj_ =1<sup>_G_</sup> _T_<sup>_j_.</sup> This implies that the entire batch shares a uniform baseline, 

effectively assigning the same value to all actions across all time steps. It introduces significant bias by disregarding the varying step-specific contributions to the final return, a critical oversight in long-horizon navigation tasks. 

## IV. LONGNAV-R1: MULTI-TURN NAVIGATION FRAMEWORK 

This section provides a comprehensive overview of our proposed pipeline, illustrated in Fig. 3. We begin by detailing the interactive VLA rollout within embodied environments in section IV-A, including state encoding, token pruning, and action prediction. Subsequently, we describe our horizonadaptive advantage estimation in section IV-B, which processes rollout trajectories to provide dense advantages for long-horizon navigation tasks. Finally, we describe our training strategy in section IV-C, which enables scalable and efficient VLA optimization through SFT warm-up phase followed by multiturn RL training. 

## _A. Interactive VLA rollout_ 

**State encoding.** State encoding transforms the multi-modal trajectory history into a sequence of tokens to provide global context for action prediction. Specifically, at each time step _t_ , we process the observation-action pair in two stages: i) visual and action encoding. The current visual observation _vt_ is processed by a vision encoder **E** to extract latent features (visual tokens) **x** _t_ . Simultaneously, the previous action _at−_ 1 is embedded into a textual token **e** _t_ via the tokenizer **D** ( _·_ ): 


**Online token pruning.** We filter redundant visual tokens before updating the state. Since navigation tasks are inherently longhorizon, often involving hundreds of steps, a single trajectory can generate hundreds of thousands of visual tokens. This massive volume creates significant computational overhead. To enhance representation efficiency, we introduce online token pruning at each rollout step. The key idea is to retain only informative visual tokens, defined as those exhibiting low feature similarity to the historical context. 

Let _{_ **k** 1: _t−_ 1 _,_ **v** 1: _t−_ 1 _}_ be the cached keys and values from the historical trajectory. We compute a binary selection mask **m** _t ∈{_ 0 _,_ 1 _}_<sup>_M_</sup> , where an element is set to 1 only if the token’s maximum similarity to the history falls below a predefined threshold _δ_ (indicating novel information). The retained sparse visual tokens **f** _t_ are computed as: 


Here, _M_ denotes the number of visual tokens in the current observation, and I( _·_ ) is the indicator function. Only the nonzero (informative) tokens are preserved. Consequently, the sparse state _st_ at time step _t_ is updated to include the history cache, the new sparse visual tokens, and the action token: 


Note that at the initial step, with the KV cache and action history empty, the model’s state is derived from the task 

instruction _I_ and the first observation. Subsequently, the state is maintained via the KV cache, which encodes the full history of actions and observations. 

**Action prediction.** Given the encoded state representation, the agent predicts the optimal next action to advance toward the goal. By encapsulating the full history of observations and actions, the state allows the agent to reason about the causal effects of past decisions and maintain global context, crucial for preventing redundant exploration and enabling targeted search. In the VLA framework, action generation is cast as next-token prediction. At each timestep _t_ , the policy outputs a categorical distribution over the vocabulary, from which the action token is sampled: 


Here, _πθ_ denotes the probability distribution derived from the VLA’s softmax-normalized logits, and _|D|_ represents the vocabulary size. While this work focuses on a discrete action space where each command corresponds to a single token, the framework is readily extensible to continuous control via action quantization or tokenization strategies. 

Upon predicting action _at_ , the agent executes it within the embodied environment, prompting a state transition, a reward _rt_ and a new observation _vt_ +1. This sequential rollout iterates until a termination condition, either a stop action or the maximum horizon _T_ is met, yielding the complete trajectory _τ_ = _{_ ( _s_ 1 _, a_ 1 _, r_ 1) _,_ ( _s_ 2 _, a_ 2 _, r_ 2) _, . . . ,_ ( _sT , aT , rT_ ) _}_ . This loop allows the agent to continuously update its state and refine its decision-making to satisfy the navigation instruction. 

## _B. Horizon-adaptive advantage estimation_ 

To optimize VLA policies within long-horizon, multi-turn settings, we implement HAPO solution proposed in sec. III-C for navigation task. The key idea of HAPO is the regression of a temporal-aware baseline via kernel regression over the rollout buffer. This enables accurate advantage estimation that accounts for temporal dynamics. Given full trajectories in the rollout buffer, we compute advantages for every timestep to provide dense process feedback for the VLA policy learning with three main steps. 

**Return estimation.** Given a full trajectory _τ_<sup>_i_</sup> _∈B_ , we compute the empirical returns at _t_ -th step _G_<sup>_i_</sup> _t_<sup>=�</sup><sup>_|_</sup> _t_<sup>_τ′_</sup> =<sup>_i|_</sup> _t_<sup>_γt′−trt_using</sup> a predefined discount factor _γ_ . For the navigation task, we define the step-level reward _rt_ based on the geodesic distance to the goal, providing a dense proxy for incremental progress. We calibrate the discount factor _γ_ to modulate the effective temporal horizon based on environmental semantic density. In indoor settings, high semantic density induces complex, highfrequency temporal dynamics; we therefore restrict the horizon to mitigate variance and maintain a high signal-to-noise ratio. Conversely, sparse outdoor environments exhibit low-frequency temporal dynamics, allowing a larger _γ_ to capture long-range dependencies without signal degradation. 

**Kernel-based baseline.** We regress a non-parametric baseline by applying a temporal kernel function across the rollout buffer. To mitigate the high variance inherent in long-horizon tasks, 

a critic-free baseline based on Gaussian smoothing. where _A_<sup>norm</sup> _t_<sup>_,i_</sup> denotes the normalized advantage, computed returns in proximal timestamps, HAPO constructs via global batch normalization to enhance training stability. baseline at each horizon scale. The baseline _Vtt_<sup>_i_for</sup> Following REINFORCE++ [19], the transformation is defined<sup>calculatedas</sup> as: _A_<sup>norm</sup> _t_<sup>_,i_</sup> =<sup>_A_</sup> _<u>t</u>_<sup>_i−_</sup> std<sup>mean</sup> ( _A|_<sup><u>(</u></sup> _A_<sup>_A_</sup> _∈B_<sup>_<u>|A</u>_</sup> )<sup>_∈B_</sup><sup><u>)</u></sup> + _ϵ_ , where _ϵ_ is a small constant <u>�</u> _Bj̸_ = _i_ <u>�</u> _|tτ_<sup>_′_</sup> =1 _j |_<sup>exp</sup> <u>�</u> _−_<sup>_<u>|t−</u>_</sup> 2 _σ_<sup>_t_2</sup><sup>_′|_2</sup> <u>�</u> _G_<sup>_j_</sup> _t_<sup>_′_</sup> for numerical stability. And _ρ_<sup>_i_</sup> _t_<sup>=</sup><sup>_πθ_(</sup><sup>_a_</sup> _t_<sup>_i|Ii_)</sup><sup>_/π_ref(</sup><sup>_a_</sup> _t_<sup>_i|Ii_) denotes</sup> _Vt_<sup>_i_=</sup> (9) the importance sampling ratio. The hyperparameters _ϵl_ , _ϵh_ and <u>�</u> _Bj̸_ = _i_ <u>�</u> _|tτ_<sup>_′_</sup> =1 _j |_<sup>exp</sup> <u>�</u> _−_<sup>_<u>|t−</u>_</sup> 2 _σ_<sup>_t_2</sup><sup>_′|_2</sup> <u>�</u> _β_ serve to constrain the gradient range and policy update magnitude, respectively, ensuring stable optimization by preventing represents the rollout buffer and _σ_ is the bandwidth large architectural shifts during learning. The reference model controlling the temporal smoothing window. The _π_ ref and KL loss _D_ KL are used for regularization to make bandwidth is calibrated to the environment’s temporal the training more stable. We also use the entropy masking Note that, while standard long-horizon tasks suffer trick in [12]. Note that, comparing to REINFORCE++, our from high variance due to noisy trajectories, our non-parametric advantage estimator moves beyond simple batch averages to a kernel regression effectively reduces this variance with temporal time-aware baseline, enabling more precise credit assignment. window. This allows the policy to better manage stochastic dynamics and **advantage estimation.** The advantage at each timestep rectify errors accumulated during the imitation phase, ensuring is computed as the residual between the return and the temporal robustness over long execution horizons. 

we utilize a critic-free baseline based on Gaussian smoothing. By grouping returns in proximal timestamps, HAPO constructs a stable baseline at each horizon scale. The baseline _Vtt_<sup>_i_for</sup> state _s_<sup>_i_</sup> _t_<sup>iscalculatedas</sup> 

where _B_ represents the rollout buffer and _σ_ is the bandwidth parameter controlling the temporal smoothing window. The kernel bandwidth is calibrated to the environment’s temporal dynamics. Note that, while standard long-horizon tasks suffer from high variance due to noisy trajectories, our non-parametric kernel regression effectively reduces this variance with temporal smoothing window. 

**Dense advantage estimation.** The advantage at each timestep is computed as the residual between the return and the temporal baseline: _A_<sup>_i_</sup> _t_<sup>=</sup><sup>_Gi_</sup> _t_<sup>_−V_</sup> _t_<sup>_i_.Bycalculatingdenseadvantage</sup> signals at each timestamp, HAPO provides the VLA policy with informative process signals. This allows the model to learn complex navigation dynamics and maintain a precise correspondence between visual-linguistic inputs and sequential actions. This approach significantly enhances sampling efficiency and training stability compared to standard outcomereward critic-free methods that lack temporal awareness. 

## V. EXPERIMENTS 

## _A. Experimental setup_ 

We conduct experiments to evaluate LongNav-R1 on three specific aspects: i) How does LongNav-R1 perform compared to existing state-of-the-arts (SOTA)? ii) Does LongNav-R1 improve long-horizon decision-making capacity for VLA? iii) Is the key design of our method effective? 

**Benchmarks.** To evaluate our general-purpose navigation method, we conduct extensive experiments on object-goal and open-vocabulary tasks across four benchmarks: HM3D V1 [37], V2 [59], MP3D [8], and HM3D-OVON [65]. Unlike previous baselines that often prioritize either efficiency or open-vocabulary capabilities on limited subsets, we provide a comprehensive comparison across diverse baselines. **Evaluation metrics.** We report two metrics including _success rate (SR)_ and _success rate weighted by path length (SPL)_ [3]. SR is the core metric of object-goal navigation task, representing the success rate of navigation episodes. SPL measures the ability of the agent to find the optimal path. If success, SPL =<sup>optimal</sup> path<sup><u>p</u></sup> length<sup>athlength</sup> , otherwise SPL = 0. Higher is better for both metrics. 

## _C. Training strategy_ 

We utilize an off-the-shelf VLM [60] as our backbone. Since generic VLMs lack embodied navigation priors, we first employ a warm-start phase using imitation learning (IL) on human demonstrations [38]. Subsequently, we transition the agent to an Online RL phase, optimizing the policy via our HAPO. **Balanced IL Warm-up.** In this phase, we utilize teacher forcing to bootstrap the VLA policy with fundamental navigation behaviors. We process the full trajectory sequence in a single forward pass, computing gradients exclusively on the generated action tokens. The objective is to minimize the standard negative log-likelihood: 


**Implementation details.** For real-world, an Orbbec Femto Bolt sensor is mounted approximately 1m off the ground. To mitigate the sim-to-real gap, the real-world RGB camera is calibrated to approximate the intrinsics of the simulated camera used during training. For simulation, we follow the standard settings [37]. The camera of the agent is 0 _._ 88 _m_ above the ground. The camera outputs 640 _×_ 480 RGB images. The success distance threshold is set as 1m, and the step budget is 500. The discrete action set includes MOVE FORWARD (0.25m), TURN LEFT/RIGHT (30°), and STOP. Ablations are conducted on randomly sampled 200 episodes. For the VLA policy training, we start with a Qwen-3-VL-2B [60] as base. **Computation resource.** Both SFT and RL stages were trained on 4 A100 GPUs (72 GPUh per stage). For consistency, efficiency metrics were benchmarked on a single A100. In real-world experiments, an A100 server handles inference, with ROS managing observation and action communication. 

where _I_<sup>_i_</sup> represents the _i_ -th instruction in the each batch with size _B_ . This supervised pre-training instills essential search strategies, such as panoramic scanning and collision avoidance. However, naive IL induces a strong length bias, particularly affecting the ‘stop’ action; agents tend to terminate episodes near the average length of training trajectories regardless of goal proximity. 

**Online multi-turn RL training.** Following the warm-up, the agent enters the multi-turn RL stage. Here, the objective is to maximize the expected cumulative reward over the full horizon: 


TABLE I: **Comparison on object goal navigation.** LongNavR1 outperforms previous SOTAs across different metrics on object goal navigation benchmark HM3D V1 [37], V2 [59] and MP3D [8]. 

|**Method**|**Ob**|**servatio**|**ns**|**HM3**|**D V1**|**HM3**|**D V2**|**M**|**P3D**|
|---|---|---|---|---|---|---|---|---|---|
||Odom.|Depth|RGB|SR_↑_|SPL_↑_|SR_↑_|SPL_↑_|SR_↑_|SPL_↑_|
|CoWs [15]<br>|✓<br>|✓<br>|✓<br>|-<br>|-<br>|-|-|||
|DD-PPO [51]|✓|✓|✓|27.9|14.2|-|-|-|-|
|ESC [75]|✓|✓|✓|39.2|22.3|-|-|28.7|14.2|
|Habitat-Web [38]|✓|✓|✓|41.5|16.0|-|-|31.6|8.5|
|VoroNav [53]|✓|✓|✓|42.0|26.0|-|-|-|-|
|L3MVN [66]|✓|✓|✓|50.4|23.1|-|-|34.9|14.5|
|OpenFMNav [26]|✓|✓|✓|52.5|24.1|-|-|37.2|15.7|
|VLFM [64]|✓|✓|✓|52.5|30.4|-|-|36.4|17.5|
|GAMap [21]|✓|✓|✓|53.1|26.0|-|-|-|-|
|SG-Nav [62]|✓|✓|✓|54.0|24.9|-|-|40.2|16.0|
|UniGoal [63]|✓|✓|✓|54.5|25.1|-|-|41.0|16.4|
|InstructNav [30]|✓|✓|✓|58.0|20.9|-|-|-|-|
|SGM [72]|✓|✓|✓|-|-|60.2|30.8|37.7|14.7|
|BeliefMapNav [76]|✓|✓|✓|61.4|30.6|-|-|37.3|17.6|
|SGImagineNav [20]|✓|✓|✓|65.4|30.0|-|-|-|-|
|ImagineNav [73]|✓||✓|53.0|23.8|-|-|-|-|
|ProcTHOR [13]|✓||✓|54.4|31.8|-|-|-|-|
|OVRL [58]|✓||✓|62.0|26.8|-|-|28.6|7.4|
|OVRL-v2 [57]|✓||✓|64.7|28.1|-|-|-|-|
|PIRLNav-IL [39]|✓||✓|64.1|27.1|52.0|20.6|-|-|
|PIRLNav-RL [39]|✓||✓|70.4|34.1|61.9|27.9|-|-|
|ZSON [31]|||✓|25.5|12.6|-|-|15.3|4.8|
|PixNav [7]|||✓|37.9|20.5|-|-|-|-|
|PSL [43]|||✓|42.4|19.2|-|-|18.9|6.4|
|UniNavid [71]|||✓|73.7|37.1|-|-|-|-|
|**LongNav-R1**|||✓|**76.0**|**44.3**|**83.7**|**43.4**|**63.0**|**30.2**|


TABLE II: **Comparison on open-vocabulary object goal navigation.** Zero-shot LongNav-R1 outperforms previous SOTAs across different metrics on OVON [65]. ZS denotes zero-shot. **LongNav-R1** is trained only on HM3D without fine-tuning on the OVON. Val-Seen-Syn is the Val-Seen-Synonyms split. 

|Method|**ZS**|**Val-**|**Seen**|**Val-Se**|**en-Syn**|**Val-U**|**nseen**|
|---|---|---|---|---|---|---|---|
|||SR_↑_|SPL_↑_|SR_↑_|SPL_↑_|SR_↑_|SPL_↑_|
|BC|✗|11.1|4.5|9.9|3.8|5.4|1.9|
|DAgger [40]|✗|11.1|4.5|9.9|3.8|5.4|1.9|
|RL [41]|✗|18.1|9.4|15.0|7.4|10.2|4.7|
|BCRL [46]|✗|39.2|18.7|27.8|11.7|18.6|7.5|
|DAgRL [11]|✗|41.3|21.2|29.4|14.4|18.3|7.9|
|VLFM [64]|✓|35.2|18.6|32.4|17.3|35.2|19.6|
|DAgRL+OD [65]|✗|38.5|21.1|39.0|21.4|37.1|19.8|
|Uni-NaVid [71]|✗|41.3|21.1|43.9|21.8|39.5|19.8|
|MTU3D [77]|✗|55.0|23.6|45.0|14.7|40.8|12.1|
|Nav-R1 [28]|✗|58.4|26.3|48.1|23.1|42.2|20.1|
|**LongNav-R1**|✓|**59.2**|**32.1**|**58.7**|**28.3**|**53.8**|**22.8**|


_B. Comparison with SOTAs_ 

**LongNav-R1 outperforms previous SOTAs on object-goal navigation benchmarks: HM3D V1, V2, and MP3D.** Tab. I compares LongNav-R1 against state-of-the-art object navigation methods using various observation modalities, including odometry, depth, and RGB. LongNav-R1 consistently outperforms existing baselines across all datasets, improving success rates to **76.0** %, **83.7** %, and **63.0** % on HM3D V1, V2, and MP3D, respectively. We also observe that: i) LongNav-R1 (using RGB-only) surpasses methods that rely on full odometry and RGBD sensor setups. This demonstrates the effectiveness of our approach and suggests strong generalizability to real-world 

TABLE III: **Compare to existing large-scale learning strategies for VLAs.** Results are reported on OVON Val-Unseen. 

|Method|Turn|Learning|GPUh|SR_↑_|SPL_↑_|
|---|---|---|---|---|---|
|UniNavid [71]|Single-turn|Imitation learning|1400|39.5|19.8|
|Nav-R1 [28]|Single-turn|Critic-free RL|-|42.2|20.1|
|StreamVLN [49]<br>|Multi-turn<br>|Imitation learning<br>|1500<br>|11.4<br>|9.4<br>|
|SFT [35]|Multi-turn|Imitation learning|72|45.5|19.9|
|**LongNav-R1**|Multi-turn|Critic-free RL|144|53.8|22.8|


Fig. 4: RL demonstrates high efficiency, improving performance by 30% with 4k iterations. Evolution of success rate and path efficiency during training. The training pipeline consists of two phases: an initial SFT phase followed by a RL phase. 

scenarios, where odometry and depth sensors are often noisy or range-limited. We attribute this robustness to the informative navigation cues provided by large model priors and the spatial understanding enriched by multi-turn causal reasoning; and ii) LongNav-R1 outperforms the prior end-to-end VLA model UniNavid [71] on path efficiency by **7.2** %. This superior efficiency stems from our RL training, which enables the agent to learn diverse behaviors to solve the navigation objective. In contrast, UniNavid uses SFT imitation learning, which is limited by the strict mimicry of human demonstrations and struggles to adapt efficiently to unseen testing environments. **LongNav-R1 outperforms previous SOTAs on the openvocabulary object-goal navigation benchmark: HM3DOVON.** Tab. II compares LongNav-R1 against several stateof-the-art open-vocabulary object navigation methods. To validate the generalization ability of LongNav-R1, we trained exclusively on HM3D and evaluated on all other benchmarks via direct inference. LongNav-R1 demonstrates strong generalization: without any fine-tuning, it achieves SOTA. We also observe that: i) LongNav-R1 significantly surpasses traditional transformer-based RL methods by about 30%, such as RL [41], BCRL [46], and DAgRL [11]. This highlights the potential of using pretrained large models as policies for robotic tasks; ii) LongNav-R1 outperforms the single-turn RL baseline, NavR1 [28]. We attribute this to our multi-turn RL approach, which better captures sequential dependencies and long-term navigation objectives. 

**Evaluation against other large-scale learning strategies for VLAs.** We benchmarked against SOTA VLAs (UniNavid, Nav-R1) and RL baselines (REINFORCE++). LongNav-R1 excels across turn types and learning setups (critic-free RL and imitation learning). i) It surpasses multi-turn (StreamVLN, SFT) by overcoming behavior cloning’s distribution shift and fostering better generalization, while StreamVLN fails to 

TABLE IV: **Effectiveness of multi-turn reinforcement learning.** Performance across different horizon length (steps). The physical distances are 12.5m (50 steps) and 50m (200 steps) 

|**Training Strategy**<br>**Ov**|**erall**|_<_|**50**|**50 - **|**200**|_>_|**200**|
|---|---|---|---|---|---|---|---|
|SR_↑_|SPL_↑_|SR_↑_|SPL_↑_|SR_↑_|SPL_↑_|SR_↑_|SPL_↑_|
|No Training [60]<br>0.51|0.50|1.9|1.8|0.0|0.0|0.0|0.0|
|SFT [35]<br>64.3|33.0|74.1|38.9|64.7|32.8|0.0|0.0|
|REINFORCE++ [19] 47.4|26.0|68.0|37.0|42.5|23.5|0.0|0.0|
|**HAPO (**_σ_ =_∞_**)**<br>71.6|40.4|82.7|47.3|72.2|40.5|0.0|0.0|
|**HAPO (**_σ_ = 30**)**<br>73.0|44.3|86.2|53.2|69.9|41.7|15.4|9.4|
|(a) Baseline: Kernel|_t_||(b|) Val|Err:|Kern|el _t_|


Fig. 5: We compare two HAPO variants, using different kernel sizes _σ_ . Subplot (a) displays the returns in a batch buffer alongside the regressed baselines, while (b) illustrates the value estimation errors. 

Fig. 6: Ablation of _σ_ and _γ_ . TABLE V: Feature. 


generalize. ii) Lacking existing critic-based RL for navigation VLAs, we reimplement PPO, however it collapses from value-head optimization complexities. LongNav-R1’s critic-free estimator removes this need, achieving superior performance and computational efficiency. 

**Training statistics analysis.** Fig. 4 shows the evolution of success rate and path efficiency throughout the training process, which consists of an initial SFT phase followed by RL. We see that: i) during the warm-up stage, SFT facilitates rapid early learning, elevating performance from 0 to 64.3%; however, it encounters a bottleneck at approximately 30k iterations, where further data scaling yields diminishing returns; and ii) in contrast, the RL phase successfully breaks this plateau, demonstrating superior efficiency by improving performance by 8.7% within only 4k iterations. This is attributed to the multi-turn design, which enables the model to learn from hundreds of decision-making points per sample, and the use of on-policy rollouts, which allow for effective error correction and behavioral refinement. 

## _C. Ablation studies_ 

**Effectiveness of multi-turn reinforcement learning.** Tab. IV compares two HAPO variants against various training strategies, including zero-shot (no training), SFT [35], and REINFORCE++ [19]. Specifically, REINFORCE++ uses sparse binary outcome rewards (1/0 for success/failure), while HAPO incorporates step-wise distance-to-goal rewards. We see that: i) both HAPO variants outperform all other training strategies; and ii) RL with dense rewards outperforms SFT, whereas RL with sparse rewards does not. This demonstrates the importance of dense reward shaping in multi-horizon robotics tasks. 

**Effectiveness of horizon-adaptive advantage estimation.** Fig. 5 and Tab. IV compares HAPO variants, using different bandwidth sizes _σ_ . We visualize the estimated baseline and the value estimation error of a randomly sampled batch buffer in subplots (a) and (b). The value estimation error is the average difference between the real return and the regressed baseline at each step. HAPO with restricted temporal window outperforms infinite-window (uniform) baseline. We see that: i) HAPO with _σ_ = 30 can achieve smaller estimation error compared to _σ_ = _∞_ ; ii) this reduced estimation error directly correlates with improved performance, as evidenced in Tab. IV. This highlights the necessity of temporal-adaptive advantage estimation, as simple uniform dense estimation fails to account for the complex temporal dynamics inherent in robotic navigation. **Ablation on kernel bandwidth** _σ_ **and discount factor** _γ_ **, see Fig. 6.** We see that an intermediate temporal window ( _σ_ = 30 _, γ_ = 0 _._ 95) yields optimal performance. This balance is critical because increasing temporal window via higher _γ_ prevents short-sighted policies by encouraging long-term predictions, yet setting it too high makes return values unpredictable. Increasing temporal window via higher _σ_ prevents the baseline from overfitting to local returns, but an excessively large _σ_ eliminates horizon awareness. We optimize this configuration via value-error analysis on an offline rollout dataset (Fig. 4 in main paper). This kernel regression is computationally efficient and strongly correlates with final model performance. Moreover, this technique can be extended to automated bandwidth tuning using an online rollout buffer. 

**Stronger justification for timestep feature design, see Tab. V** . HAPO is a flexible framework capable of accommodating different factors via feature switching. Specifically, HAPO’s timestep feature outperforms per-trajectory and distance metrics. The reasons are: i) HAPO reduces per-trajectory bias (similar to REINFORCE++ v.s GRPO), ensuring generalized navigation over instance-specific overfitting; ii) distance fails to credit critical in-place actions (turning to unlock regions). This is reflected in the data: elapsed timesteps maintain a higher correlation with returns (0 _._ 24) than distance-to-goal (0 _._ 09). **Clearer explanation for value-error analysis, see Tab. VI.** i) Navigation success requires minimizing accumulated value error across all elapsed timesteps. ii) Thus, longer horizons (>200 steps) yield larger accumulated errors and lower performance than shorter ones (<200 steps). iii) For >200 steps, HAPO (30) sustains lower error and outperforms the _∞_ -baseline, while 

TABLE VII: Computation analysis. 

|Turns|**Infe**|**rence Time **|**(s)**|**Me**|**mory **|**Cost **|**(GB)**|
|---|---|---|---|---|---|---|---|
||50|100<br>200|400|50|100|200|400|
|**LongNav-R1**|0.12|0.15<br>0.19|0.23|6.25|7.34|9.33|11.62|
|TA|BLE|VIII: Abl|ation|of p|runi|ng.||
|Pruni|ng (_δ_)|Speed (s)|Me|m (G|B)|SR_↑_||
|0%|(1.0)|0.203||15.6||53.1||
|20%|(0.97)|0.172||13.7||56.5||
|35%|(0.95)|0.168||11.8||54.4||
|45%|(0.93)|0.141||10.8||52.4||
|50%|(0.92)|0.132||10.4||45.6||
|63%|(0.90)|0.118||8.9||25.8||
|80%|(0.85)|0.089||7.3||0.0||


both perform identically for <200 steps. iv) The peak variations (<200) in Tab. III (main paper) arise from fine-grained binning across unbalanced intervals (<50, 50-200). 

**Computation analysis.** Tab. VII compares the computational overhead of LongNav-R1 in terms of inference latency and memory consumption. We see that while inference time scales with the horizon, LongNav-R1 remains highly performant, requiring only 0.23 s to process a 400-step sequence. Achieving about 5 FPS, the model can be deployed in practical real-world environments. This is attributed to two architectural advantages: the multi-turn setup, which enables KV cache reuse to avoid redundant processing of past observations, and online token pruning, which restricts attention mechanisms to only the most informative new tokens. 

**Effectiveness of online pruning.** Tab. VIII shows that increasing the pruning ratio consistently improves speed and reduces memory usage, navigation accuracy follows an inverted-U trend. Performance suffers at both extremes: unpruned models quickly exceed memory limits in long tasks (peak memory), while overpruning discards essential data. ii) We demonstrate superior efficiency compared to baselines (StreamVLN requires 24GB memory and 0.37s). Moreover, performance drops after 150 steps (37.5m) due to the training focus on nearby targets and context-heavy degradation at 60k tokens, see Fig.6. _D. Case study_ 

**Qualitative analysis of SFT and LongNav-R1.** Fig. 7 visualizes the navigation process of SFT and LongNav-R1 as they search for a sofa. We see that: i) despite the challenge of a distant, cross-floor goal, LongNav-R1 successfully and efficiently reaches the target while SFT fails; and ii) LongNavR1 natively handles cross-floor transitions, a task where modular designs often struggle, enhancing its adaptability in real-world environments. 

**Visualization of LongNav-R1 in real-world deployment.** Fig. 8 visualizes the navigation process of LongNav-R1 as it searches for an elevator, an unseen object category, in a real-world office environment. For the hardware mobile base, we adopt the mobile base design from TidyBot++ [52], omitting the manipulator. Equipped with LongNav-R1, the robot successfully locates the target, demonstrating zero-shot real-world effectiveness of the navigation policy. 


Fig. 7: Visualization of the navigation process in habitat. Blue and green lines represent the optimal and inferred trajectories. 


Fig. 8: Visualization of the navigation process in **real-world** . The robot successfully navigates to an elevator, an unseen category. Displayed trajectories are approximate for visualization. 

## VI. DISCUSSION 

**Generalize to tasks lacking geometric proxies.** i) We want to clarify that HAPO is not constrained to dense geometric proxies. As a versatile, critic-free framework for long-horizon tasks, it accommodates diverse factors via feature switching and natively supports sparse reward (producing the REINFORCE++ in Tab. IV); ii) HAPO’s strong sim-to-real generalization, evidenced by its superior zero-shot performance in real-world demo, makes it highly feasible to get these priors in simulation before deploying in real world. 

## VII. CONCLUSION 

**Conclusion.** In this paper, we provide a recipe for training endto-end VLA policies for long-horizon navigation using multiturn reinforcement learning and horizon-adaptive policy optimization. By utilizing a critic-free advantage estimation, HAPO effectively manages dense rewards and sequential decisionmaking without the prohibitive computational overhead of an auxiliary critic model, a key advantage when scaling large models. Our model, LongNav-R1, achieves state-of-the-art results across four simulation benchmarks and demonstrates robustness in real-world deployment. 

**Limitation and future works.** A current limitation is that our online token pruning retains the full KV cache to maintain causal consistency. To mitigate memory bottlenecks in extremehorizon tasks, future work will explore selective KV cache eviction and spatially aware global memory mechanisms. Beyond navigation, we aim to extend this framework to diverse applications, such as mobile manipulation, and incorporate world models for real-world multi-turn reinforcement learning. 

## REFERENCES 

- [1] Arash Ahmadian, Chris Cremer, Matthias Gallé, Marzieh Fadaee, Julia Kreutzer, Olivier Pietquin, Ahmet Üstün, and Sara Hooker. Back to basics: Revisiting reinforce-style optimization for learning from human feedback in llms. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 12248–12267, 2024. 

- [2] Dong An, Hanqing Wang, Wenguan Wang, Zun Wang, Yan Huang, Keji He, and Liang Wang. Etpnav: Evolving topological planning for vision-language navigation in continuous environments. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2024. 

- [3] Peter Anderson, Angel Chang, Devendra Singh Chaplot, Alexey Dosovitskiy, Saurabh Gupta, Vladlen Koltun, Jana Kosecka, Jitendra Malik, Roozbeh Mottaghi, Manolis Savva, and Amir R. Zamir. On evaluation of embodied navigation agents. _arXiv preprint arXiv:1807.06757_ , 2018. doi: 10.48550/arXiv.1807. 06757. 

- [4] Peter Anderson, Qi Wu, Damien Teney, Jake Bruce, Mark Johnson, Niko Sünderhauf, Ian Reid, Stephen Gould, and Anton Van Den Hengel. Vision-and-language navigation: Interpreting visually-grounded navigation instructions in real environments. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2018. 

- [5] Anthropic. Claude ai. https://claude.ai, 2023. Accessed: 202505-05. 

- [6] Xiao Bi, Deli Chen, Guanting Chen, Shanhuang Chen, Damai Dai, Chengqi Deng, Honghui Ding, Kai Dong, Qiushi Du, Zhe Fu, Huazuo Gao, Kaige Gao, Wenjun Gao, Ruiqi Ge, Kang Guan, Daya Guo, Jianzhong Guo, Guangbo Hao, Zhewen Hao, Ying He, Wenjie Hu, Panpan Huang, Erhang Li, Guowei Li, Jiashi Li, Yao Li, Y. K. Li, Wenfeng Liang, Fangyun Lin, A. X. Liu, Bo Liu, Wen Liu, Xiaodong Liu, Xin Liu, Yiyuan Liu, Haoyu Lu, Shanghao Lu, Fuli Luo, Shirong Ma, Xiaotao Nie, Tian Pei, Yishi Piao, Junjie Qiu, Hui Qu, Tongzheng Ren, Zehui Ren, Chong Ruan, Zhangli Sha, Zhihong Shao, Junxiao Song, Xuecheng Su, Jingxiang Sun, Yaofeng Sun, Minghui Tang, Bingxuan Wang, Peiyi Wang, Shiyu Wang, Yaohui Wang, Yongji Wang, Tong Wu, Y. Wu, Xin Xie, Zhenda Xie, Ziwei Xie, Yiliang Xiong, Hanwei Xu, R. X. Xu, Yanhong Xu, Dejian Yang, Yuxiang You, Shuiping Yu, Xingkai Yu, B. Zhang, Haowei Zhang, Lecong Zhang, Liyue Zhang, Mingchuan Zhang, Minghua Zhang, Wentao Zhang, Yichao Zhang, Chenggang Zhao, Yao Zhao, Shangyan Zhou, Shunfeng Zhou, Qihao Zhu, and Yuheng Zou. Deepseek llm: Scaling open-source language models with longtermism. _arXiv preprint arXiv:2401.02954_ , 2024. 

- [7] Wenzhe Cai, Siyuan Huang, Guangran Cheng, Yuxing Long, Peng Gao, Changyin Sun, and Hao Dong. Bridging zero-shot object navigation and foundation models through pixel-guided navigation skill. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5228–5234. IEEE, 2024. 

- [8] Angel X. Chang, Angela Dai, Thomas A. Funkhouser, Maciej Halber, Matthias Nießner, Manolis Savva, Shuran Song, Andy Zeng, and Yinda Zhang. Matterport3d: Learning from rgb-d data in indoor environments. _2017 International Conference on 3D Vision (3DV)_ , pages 667–676, 2017. 

- [9] Matthew Chang, Arjun Gupta, and Saurabh Gupta. Semantic visual navigation by watching youtube videos. _Advances in Neural Information Processing Systems_ , 33:4283–4294, 2020. 

- [10] Devendra Singh Chaplot, Dhiraj Prakashchand Gandhi, Abhinav Gupta, and Russ R Salakhutdinov. Object goal navigation using goal-oriented semantic exploration. _Advances in Neural Information Processing Systems_ , 33:4247–4258, 2020. 

- [11] Howard Chen, Alane Suhr, Dipendra Misra, Noah Snavely, and Yoav Artzi. Touchdown: Natural language navigation and spatial reasoning in visual street environments. In _Proceedings of_ 

_the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 12538–12547, 2019. 

- [12] Ganqu Cui, Yuchen Zhang, Jiacheng Chen, Lifan Yuan, Zhi Wang, Yuxin Zuo, Haozhan Li, Yuchen Fan, Huayu Chen, Weize Chen, et al. The entropy mechanism of reinforcement learning for reasoning language models. _arXiv preprint arXiv:2505.22617_ , 2025. 

- [13] Matt Deitke, Eli VanderBilt, Alvaro Herrasti, Luca Weihs, Kiana Ehsani, Jordi Salvador, Winson Han, Eric Kolve, Aniruddha Kembhavi, and Roozbeh Mottaghi. Procthor: Large-scale embodied ai using procedural generation. _Advances in Neural Information Processing Systems_ , 35:5982–5994, 2022. 

- [14] A. Dubey et al. The llama 3 herd of models. _arXiv preprint arXiv:2407.21783_ , 2024. 

- [15] Samir Yitzhak Gadre, Mitchell Wortsman, Gabriel Ilharco, Ludwig Schmidt, and Shuran Song. Cows on pasture: Baselines and benchmarks for language-driven zero-shot object navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 23171–23181, 2023. 

- [16] Nandiraju Gireesh, DA Sasi Kiran, Snehasis Banerjee, Mohan Sridharan, Brojeshwar Bhowmick, and Madhava Krishna. Object goal navigation using data regularized q-learning. In _2022 IEEE 18th International Conference on Automation Science and Engineering (CASE)_ , pages 1092–1097. IEEE, 2022. 

- [17] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ , 2025. 

- [18] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models, 2021. URL https://arxiv.org/abs/2106.09685. 

- [19] Jian Hu. Reinforce++: A simple and efficient approach for aligning large language models. _arXiv preprint arXiv:2501.03262_ , 2025. 

- [20] Yue Hu, Junzhe Wu, Ruihan Xu, Hang Liu, Avery Xi, Henry X Liu, Ram Vasudevan, and Maani Ghaffari. Imaginative world modeling with scene graphs for embodied agent navigation. _arXiv preprint arXiv:2508.06990_ , 2025. 

- [21] Hao Huang, Yu Hao, Congcong Wen, Anthony Tzes, Yi Fang, et al. Gamap: Zero-shot object goal navigation with multi-scale geometric-affordance guidance. _Advances in Neural Information Processing Systems_ , 37:39386–39408, 2024. 

- [22] Apoorv Khandelwal, Luca Weihs, Roozbeh Mottaghi, and Aniruddha Kembhavi. Simple but effective: Clip embeddings for embodied ai. _2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 14809–14818, 2021. 

- [23] Mukul Khanna, Yongsen Mao, Hanxiao Jiang, Sanjay Haresh, Brennan Schacklett, Dhruv Batra, Alexander Clegg, Eric Undersander, Angel X. Chang, and Manolis Savva. Habitat synthetic scenes dataset (hssd-200): An analysis of 3d scene scale and realism tradeoffs for objectgoal navigation. _2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 16384–16393, 2023. 

- [24] Jacob Krantz, Erik Wijmans, Arjun Majundar, Dhruv Batra, and Stefan Lee. Beyond the nav-graph: Vision and language navigation in continuous environments. In _European Conference on Computer Vision (ECCV)_ , 2020. 

- [25] Alexander Ku, Peter Anderson, Roma Patel, Eugene Ie, and Jason Baldridge. Room-across-room: Multilingual vision-andlanguage navigation with dense spatiotemporal grounding. In _Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)_ , 2020. 

- [26] Yuxuan Kuang, Hai Lin, and Meng Jiang. OpenFMNav: Towards open-set zero-shot object navigation via vision-language foundation models. In _Findings of the Association for Computational_ 

_Linguistics (NAACL)_ , pages 338–351, 2024. 

- [27] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning, 2023. 

- [28] Qingxiang Liu, Ting Huang, Zeyu Zhang, and Hao Tang. Nav-r1: Reasoning and navigation in embodied scenes. _arXiv preprint arXiv:2509.10884_ , 2025. 

- [29] Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Qing Jiang, Chunyuan Li, Jianwei Yang, Hang Su, et al. Grounding dino: Marrying dino with grounded pre-training for open-set object detection. In _European Conference on Computer Vision_ , pages 38–55. Springer, 2024. 

- [30] Yuxing Long, Wenzhe Cai, Hongchen Wang, Guanqi Zhan, and Hao Dong. Instructnav: Zero-shot system for generic instruction navigation in unexplored environment. In _Conference on Robot Learning_ , 2024. 

- [31] Arjun Majumdar, Gunjan Aggarwal, Bhavika Devnani, Judy Hoffman, and Dhruv Batra. Zson: Zero-shot object-goal navigation using multimodal goal embeddings. _Advances in Neural Information Processing Systems_ , 35:32340–32352, 2022. 

- [32] Oleksandr Maksymets, Vincent Cartillier, Aaron Gokaslan, Erik Wijmans, Wojciech Galuba, Stefan Lee, and Dhruv Batra. Thda: Treasure hunt data augmentation for semantic navigation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 15374–15383, 2021. 

- [33] Arsalan Mousavian, Alexander Toshev, Marek Fišer, Jana Košecká, Ayzaan Wahid, and James Davidson. Visual representations for semantic target driven navigation. In _2019 International Conference on Robotics and Automation (ICRA)_ , pages 8846–8852. IEEE, 2019. 

- [34] OpenAI. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- [35] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback. _Advances in neural information processing systems_ , 35:27730–27744, 2022. 

- [36] Yanyuan Qiao, Wenqi Lyu, Hui Wang, Zixu Wang, Zerui Li, Yuanyuan Zhang, Mingkui Tan, and Qi Wu. Open-nav: Exploring zero-shot vision-and-language navigation in continuous environment with open-source llms. _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6710– 6717, 2024. 

- [37] Santhosh Kumar Ramakrishnan, Aaron Gokaslan, Erik Wijmans, Oleksandr Maksymets, Alexander Clegg, John M Turner, Eric Undersander, Wojciech Galuba, Andrew Westbury, Angel X Chang, Manolis Savva, Yili Zhao, and Dhruv Batra. Habitatmatterport 3d dataset (HM3d): 1000 large-scale 3d environments for embodied AI. In _Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track_ , 2021. 

- [38] Ram Ramrakhya, Eric Undersander, Dhruv Batra, and Abhishek Das. Habitat-web: Learning embodied object-search strategies from human demonstrations at scale. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 5173–5183, June 2022. 

- [39] Ram Ramrakhya, Dhruv Batra, Erik Wijmans, and Abhishek Das. Pirlnav: Pretraining with imitation and rl finetuning for objectnav. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 17896–17906, 2023. 

- [40] Stéphane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , pages 627–635. JMLR Workshop and Conference Proceedings, 2011. 

- [41] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. 

_arXiv preprint arXiv:1707.06347_ , 2017. 

- [42] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 

- [43] Xinyu Sun, Lizhao Liu, Hongyan Zhi, Ronghe Qiu, and Junwei Liang. Prioritized semantic learning for zero-shot instance navigation. In _European Conference on Computer Vision_ , pages 161–178. Springer, 2024. 

- [44] Gemini Team, Petko Georgiev, Ving Ian Lei, Ryan Burnell, Libin Bai, Anmol Gulati, Garrett Tanzer, Damien Vincent, Zhufeng Pan, Shibo Wang, et al. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. _arXiv preprint arXiv:2403.05530_ , 2024. 

- [45] Gemini Robotics Team. Gemini robotics: Bringing ai into the physical world. _ArXiv_ , abs/2503.20020, 2025. 

- [46] Xin Wang, Qiuyuan Huang, Asli Celikyilmaz, Jianfeng Gao, Dinghan Shen, Yuan-Fang Wang, William Yang Wang, and Lei Zhang. Reinforced cross-modal matching and self-supervised imitation learning for vision-language navigation. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 6629–6638, 2019. 

- [47] Yiping Wang, Qing Yang, Zhiyuan Zeng, Liliang Ren, Liyuan Liu, Baolin Peng, Hao Cheng, Xuehai He, Kuan Wang, Jianfeng Gao, et al. Reinforcement learning for reasoning in large language models with one training example. _arXiv preprint arXiv:2504.20571_ , 2025. 

- [48] Zihan Wang, Kangrui Wang, Qineng Wang, Pingyue Zhang, Linjie Li, Zhengyuan Yang, Xing Jin, Kefan Yu, Minh Nhat Nguyen, Licheng Liu, et al. Ragen: Understanding self-evolution in llm agents via multi-turn reinforcement learning. _arXiv preprint arXiv:2504.20073_ , 2025. 

- [49] Meng Wei, Chenyang Wan, Xiqian Yu, Tai Wang, Yuqiang Yang, Xiaohan Mao, Chenming Zhu, Wenzhe Cai, Hanqing Wang, Yilun Chen, Xihui Liu, and Jiangmiao Pang. StreamVLN: Streaming vision-and-language navigation via SlowFast context modeling. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2026. 

- [50] Zhepei Wei, Wenlin Yao, Yao Liu, Weizhi Zhang, Qin Lu, Liang Qiu, Changlong Yu, Puyang Xu, Chao Zhang, Bing Yin, Hyokun Yun, and Lihong Li. WebAgent-R1: Training web agents via end-to-end multi-turn reinforcement learning. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing (EMNLP)_ , pages 7909–7928, 2025. 

- [51] Erik Wijmans, Abhishek Kadian, Ari S. Morcos, Stefan Lee, Irfan Essa, Devi Parikh, Manolis Savva, and Dhruv Batra. Ddppo: Learning near-perfect pointgoal navigators from 2.5 billion frames. In _International Conference on Learning Representations_ , 2019. 

- [52] Jimmy Wu, William Chong, Robert Holmberg, Aaditya Prasad, Yihuai Gao, Oussama Khatib, Shuran Song, Szymon Rusinkiewicz, and Jeannette Bohg. Tidybot++: An open-source holonomic mobile manipulator for robot learning. In _Conference on Robot Learning_ , 2024. 

- [53] Pengying Wu, Yao Mu, Bin Wu, Yi Hou, Ji Ma, Shanghang Zhang, and Chang Liu. Voronav: Voronoi-based zero-shot object navigation with large language model. In _International Conference on Machine Learning_ , 2024. 

- [54] Zhiheng Xi, Jixuan Huang, Chenyang Liao, Baodai Huang, Honglin Guo, Jiaqi Liu, Rui Zheng, Junjie Ye, Jiazheng Zhang, Wenxiang Chen, Tao Gui, Qi Zhang, and Xuanjing Huang. AgentGym-RL: Training LLM agents for long-horizon decision making through multi-turn reinforcement learning. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2026. 

- [55] Zhenghai Xue, Longtao Zheng, Qian Liu, Yingru Li, Xiaosen 

- Zheng, Zejun Ma, and Bo An. SimpleTIR: End-to-end reinforcement learning for multi-turn tool-integrated reasoning. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2026. 

- [56] Karmesh Yadav, Santhosh Kumar Ramakrishnan, John Turner, Aaron Gokaslan, Oleksandr Maksymets, Rishabh Jain, Ram Ramrakhya, Angel X Chang, Alexander Clegg, Manolis Savva, Eric Undersander, Devendra Singh Chaplot, and Dhruv Batra. Habitat challenge 2022. https://aihabitat.org/challenge/2022/, 2022. 

- [57] Karmesh Yadav, Arjun Majumdar, Ram Ramrakhya, Naoki Yokoyama, Alexei Baevski, Zsolt Kira, Oleksandr Maksymets, and Dhruv Batra. Ovrl-v2: A simple state-of-art baseline for imagenav and objectnav. _arXiv preprint arXiv:2303.07798_ , 2023. 

- [58] Karmesh Yadav, Ram Ramrakhya, Arjun Majumdar, VincentPierre Berges, Sachit Kuhar, Dhruv Batra, Alexei Baevski, and Oleksandr Maksymets. Offline visual representation learning for embodied navigation. In _Workshop on Reincarnating Reinforcement Learning at ICLR 2023_ , 2023. 

- [59] Karmesh Yadav, Ram Ramrakhya, Santhosh Kumar Ramakrishnan, Theo Gervet, John Turner, Aaron Gokaslan, Noah Maestre, Angel Xuan Chang, Dhruv Batra, Manolis Savva, et al. Habitatmatterport 3d semantics dataset. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 4927–4936, 2023. 

- [60] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ , 2025. 

- [61] Wei Yang, Xiaolong Wang, Ali Farhadi, Abhinav Gupta, and Roozbeh Mottaghi. Visual semantic navigation using scene priors. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2019. 

- [62] Hang Yin, Xiuwei Xu, Zhenyu Wu, Jie Zhou, and Jiwen Lu. Sgnav: Online 3d scene graph prompting for llm-based zero-shot object navigation. _Advances in Neural Information Processing Systems_ , 37:5285–5307, 2024. 

- [63] Hang Yin, Xiuwei Xu, Linqing Zhao, Ziwei Wang, Jie Zhou, and Jiwen Lu. Unigoal: Towards universal zero-shot goal-oriented navigation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 19057–19066, 2025. 

_on Robot Learning_ , 2024. 

   - [70] Jiazhao Zhang, Kunyu Wang, Rongtao Xu, Gengze Zhou, Yicong Hong, Xiaomeng Fang, Qi Wu, Zhizheng Zhang, and He Wang. Navid: Video-based vlm plans the next step for vision-andlanguage navigation. _Robotics: Science and Systems_ , 2024. 

   - [71] Jiazhao Zhang, Kunyu Wang, Shaoan Wang, Minghan Li, Haoran Liu, Songlin Wei, Zhongyuan Wang, Zhizheng Zhang, and He Wang. Uni-navid: A video-based vision-language-action model for unifying embodied navigation tasks. _Robotics: Science and Systems_ , 2025. 

   - [72] Sixian Zhang, Xinyao Yu, Xinhang Song, Xiaohan Wang, and Shuqiang Jiang. Imagine before go: Self-supervised generative map for object goal navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 16414–16425, 2024. 

   - [73] Xinxin Zhao, Wenzhe Cai, Likun Tang, and Teng Wang. ImagineNav: Prompting vision-language models as embodied navigator through scene imagination. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2025. 

   - [74] Gengze Zhou, Yicong Hong, and Qi Wu. Navgpt: Explicit reasoning in vision-and-language navigation with large language models. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pages 7641–7649, 2024. 

   - [75] Kaiwen Zhou, Kaizhi Zheng, Connor Pryor, Yilin Shen, Hongxia Jin, Lise Getoor, and Xin Eric Wang. Esc: Exploration with soft commonsense constraints for zero-shot object navigation. In _International Conference on Machine Learning_ , pages 42829– 42842. PMLR, 2023. 

   - [76] Zibo Zhou, Yue Hu, Lingkai Zhang, Zonglin Li, and Siheng Chen. BeliefMapNav: 3D voxel-based belief map for zero-shot object navigation. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 38, 2025. 

   - [77] Ziyu Zhu, Xilin Wang, Yixuan Li, Zhuofan Zhang, Xiaojian Ma, Yixin Chen, Baoxiong Jia, Wei Liang, Qian Yu, Zhidong Deng, et al. Move to understand a 3d scene: Bridging visual grounding and exploration for efficient and versatile embodied navigation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 8120–8132, 2025. 

- [64] Naoki Yokoyama, Sehoon Ha, Dhruv Batra, Jiuguang Wang, and Bernadette Bucher. Vlfm: Vision-language frontier maps for zero-shot semantic navigation. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 42–48. IEEE, 2024. 

- [65] Naoki Yokoyama, Ram Ramrakhya, Abhishek Das, Dhruv Batra, and Sehoon Ha. Hm3d-ovon: A dataset and benchmark for open-vocabulary object goal navigation. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 5543–5550. IEEE, 2024. 

- [66] Bangguo Yu, Hamidreza Kasaei, and Ming Cao. L3mvn: Leveraging large language models for visual target navigation. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 3554–3560. IEEE, 2023. 

- [67] Bangguo Yu, Yuzhen Liu, Lei Han, Hamidreza Kasaei, Tingguang Li, and Ming Cao. Vln-game: Vision-language equilibrium search for zero-shot semantic navigation. _IEEE Transactions on Robotics_ , 42:1824–1839, 2024. 

- [68] Guanning Zeng, Zhaoyi Zhou, Daman Arora, and Andrea Zanette. Shrinking the variance: Shrinkage baselines for reinforcement learning with verifiable rewards. _arXiv preprint arXiv:2511.03710_ , 2025. 

- [69] Kuo-Hao Zeng, Zichen Zhang, Kiana Ehsani, Rose Hendrix, Jordi Salvador, Alvaro Herrasti, Ross Girshick, Aniruddha Kembhavi, and Luca Weihs. Poliformer: Scaling on-policy rl with transformers results in masterful navigators. In _Conference_ 

## VIII. APPENDIX 

## _A. SFT implementation details_ 

**SFT Data Curation.** To bootstrap the VLM for the navigation objective, we perform Supervised Fine-Tuning (SFT) utilizing human demonstrations from the Habitat-Web dataset [38]. To ensure training efficiency and accommodate GPU memory limitations, we truncated the raw human trajectory data at 500 steps. We then evaluated various sampling strategies to effectively utilize the data. From Fig. 9, we can see that the dominant trajectory length is approximately 100 steps. Experimentally, we see that naive random sampling from this distribution introduces a significant “stop bias,” causing the model to overfit to premature episode termination. Consequently, scaling randomly sampled data leads to performance degradation; as shown in Tab. IX, the Success rate drops from 55.5% at 4k samples to 46.5% at 30k samples, despite improvements in Success weighted by Path Length. 

To mitigate this, we implement a Uniform Sampling strategy that equalizes trajectory selection across lengths ranging from 0 to 400 steps. This approach balances the state-action space, ensuring robust policy learning across varying trajectory complexities. As demonstrated in Tab. IX, uniform curation prevents convergence on sub-optimal stop behaviors and effectively leverages larger datasets. At the 30k data scale, the uniform configuration achieves a peak Success rate of 64.3% and a Success SPL of 57.0, representing a 17.8% absolute increase in success over the random baseline. 

TABLE IX: Effectiveness of SFT data curation. 

|**Sampling**|**Data**|**Success**|**SPL**|**Success SPL**|
|---|---|---|---|---|
|Random|4k|55.5|25.0|45.0|
|Random|10k|49.5|25.6|51.8|
|Random|30k|46.5|24.7|53.1|
|Uniform|10k|53.0|27.6|52.0|
|Uniform|30k|64.3|33.0|57.0|


**SFT training.** We use Qwen3-VL 2B Instruct [60] as the base model and employ LoRA [18] for parameter efficient SFT fine tuning. LoRA adapters with configuration _{r_ = 128 _, α_ = 256 _,_ dropout = 0 _._ 05 _}_ are attached to all linear blocks of the language model, while the vision encoder is left frozen. 

We train with an initial learning rate of 3 _×_ 10<sup>_−_5</sup> and a linear decaying schedule. We configure the AdamW optimizer with the standard hyperparameters _{β_ 1 = 0 _._ 9 _, β_ 2 = 0 _._ 999 _}_ . Gradient checkpointing along with our visual token sparsification enables bfloat16 training on full trajectories up to 400 steps long, without need for quantization or model parallelism. Training completes in 18 hours on 2 H100 GPUs. 

## _B. RL implementation details_ 

**Environment Setup.** Our RL training uses the 80 scene training split from the 2022 Habitat ObjectNav challenge [56]. We use the dense shaped reward _rt_ ( _at, st_ ) = _−_ ∆geo_dist _−_ 0 _._ 01 and terminal reward _rT_ = 2 _._ 5 _·_ SPL standard to habitat ObjectNav tasks [51]. The RGB observations and cylindrical agent form 

factor are likewise habitat ObjectNav defaults. We set the maximal environment steps per episode to 350 to reduce computational cost. 

**Multi-turn RL framework.** We implement a synchronous RL framework similar to DD-PPO [51], where experience collection is followed by training with gradient synchronization via torch DDP. However, instead of using a preemption threshold as in DD-PPO, we enable each worker to collect multiple trajectories per cycle using an asynchronous dispatch loop that pairs each VLM instance with dedicated Habitat Sim workers, amortizing the computation cost from episode length variability. Specifically, we dispatch episodes to any idle workers until the number of dispatches equals the rollout buffer size. This improvement allows us to use every single collected experience instead of discarding incomplete trajectories. Furthermore, VLM idle time is minimized as each VLM continuously runs episodes until the number of completed and running episodes equals the rollout buffer size. 

**Multi-turn RL training.** To stabilize the RL training with limited computation resource, we use a rollout buffer size of 16 but retain the most recent 256 trajectories for HAPO advantage estimation. This design decision trades trajectory staleness when estimating baselines for reduced variance. 

We employ the dual clip PPO training objective in combination with ClipCov [12] to prevent entropy collapse. The PPO objective is configured with _{γ_ = 0 _._ 95 _,_ clip_ratio_high = 0 _._ 28 _,_ clip_ratio_low = 0 _._ 2 _}_ . ClipCov is configured with the standard hyperparameters _{_ clip_cov_ub = 5 _,_ clip_cov_lb = 1 _,_ clip_cov_ratio = 0 _._ 0002 _}_ . We further regularize the policy with a KL divergence constraint. Since we train with LoRA adapters, disabling the adapters gives us the SFT tuned base model, which we use as the reference model. Since the habitat navigation action space is much smaller than typical large language model vocabulary size, we are able to calculate the full KL divergence instead of using KL estimators typically used in LLM/LVLM reinforcement learning. We use kl_coeff = 0 _._ 001 to weigh the KL divergence from the SFT model. 

Our RL policy was trained for 18 hours on 4 A100 GPUs, experiencing approximately 4000 episodes. Due to the need to accommodate long trajectories, each GPU runs a single VLM instance with batch size 1 during both rollout collection and training. Since the vast majority of trajectories are short enough to occupy less than half the GPU VRAM, we anticipate future performance gains by implementing dynamic batching. 

## _C. Online token pruning algorithm_ 

Our online visual token pruning strategy is consistent across both SFT and RL phases and is fully causal, allowing for efficient single-pass trajectory training. This approach enables the entire trajectory to be processed in one forward and backward pass, significantly boosting training efficiency. 

## _D. Generalization analysis_ 

To validate the generalization ability of LongNav-R1, we trained exclusively on HM3D and evaluated on all other benchmarks via direct inference. Although trained on only 


Fig. 9: Visualization of SFT trajectory data distribution. (a) is the overall human demonstration data, (b) is the randomly sampled data distribution, and (c) is our uniformly sampled data distribution. 

TABLE X: Object categories of HM3D V1 [37], V2 [59], MP3D [8] and HM3D-OVON [65]. 

|**Dataset **|**Object **|**Category**|
|---|---|---|
|HM3D|6|Bed, sofa, tv_monitor, plant, chair, toilet|
|MP3D|21|Bed, sofa, tv_monitor, plant, chair, toilet,<br>cabinet, chest_of_drawers, table, picture, sink,<br>stool, towel, cushion, shower, bathtub, counter,<br>fireplace, gym_equipment, seating, clothes|
|||Bed, plant, chair, toilet, air_conditioner, amplifier,<br>antique_clock, antique_telephone, appliance,<br>arcade_game, archway, armchair, artwork,<br>baby_changing_station, backpack, backrest,<br>backsplash, bag, balcony_railing, balustrade,<br>banner, bar, bar_cabinet, bar_chair, barbecue,<br>basket, bath_cabinet, bath_sink, bath_towel,<br>bathrobe, bathroom_accessory, bathroom_cabinet,|
|OVON|379|. . .,<br>stage, stair, staircase_handrail, staircase_trim,<br>stairs_railing, stand, statue, stereo_set,<br>stone_support_structure, stool, storage,<br>storage_cabinet, storage_space, stove,<br>stovetop, sunbed, support_beam, swivel_chair,<br>table, table_stand, tablecloth, tank, telephone,<br>telescope, tent, throw_blanket, tile, toilet, tool,<br>towel, toy, trampoline, trashcan, tray,<br>treadmill, tv, tv_stand, umbrella, urinal,<br>vase, water_fountain, water_heater, water_tank,<br>window, window_curtain, window_frame,<br>window_shade, window_shutter, wine_cabinet,<br>wood, workstation, worktop, wreath|


achieves high performance on unseen categories that are even semantically distant from the training set, such as fireplace, piano, flag, cooker. This demonstrates that LongNav-R1 has learned generalizable navigation capabilities rather than merely memorizing object shortcuts. 

## _E. Long-horizon analysis_ 

Fig. 11, 12, 13 and 14 shows the navigation process with increasing steps, ranging from 81 to 354 steps. LongNav-R1 demonstrates the ability to locate distant targets by sustaining long-horizon exploration and avoiding repetitive trajectories. 

We identify the representative long horizon trajectory examples in 12, 13 and 14 by filtering for episodes where the oracle horizon (2 times the steps taken by shortest path oracle) is greater than 200 steps. In these challenging episodes where long term consistency is required to reach the goal, LongNavR1 retains effective active perception strategies such as peeking and panoramic scanning, enabling it to capitalize on promising regions and avoid dead ends. 

6 target types in HM3D, LongNav-R1 generalizes to MP3D and OVON, handling 21 and 371 object categories, respectively. Tab X details these categories, highlighting the extensive diversity in OVON. Fig 10 reports the performance (Success Rate and SPL) across object categories in HM3D (V1/V2), MP3D, and OVON. We can see that: i) for MP3D, there is no significant performance gap between the 6 trained categories and the unseen categories; and ii) for OVON, the model 


Fig. 11: Visualization of navigation episode. The agent successfully navigates across rooms for 81 steps to locate the target bed. It starts on the balcony, travels indoors to the dining room, and discovers the bed in a nearby bedroom. 


Fig. 12: Visualization of a long-horizon navigation episode. The agent successfully navigates across floors for 185 steps to locate the target tv monitor. Starting at the second floor, agent travels across a corridor to check that no tv is present in the study or bathroom. It then travels downstairs, traverses the dining room, and finds the tv in the adjacent living room. 


Fig. 13: Visualization of a long-horizon navigation episode. The agent successfully navigates across floors for 239 steps to locate the target toilet. The agent explores the first floor thoroughly, then climbs to the second floor. It peeks into a bedroom without entering, and moves on to find the bathroom containing the toilet. 


Fig. 14: Visualization of a long-horizon navigation episode. The agent successfully explores the oblong first floor for 354 steps to locate the target toilet. The agent begins near the house entrance and proceeds down the entrance corridor. It crosses through the kitchen, turns to peek into the living room without entering, and turns back to continue though the kitchen and into the adjacent laundry room. Finally, it finds the toilet in the bathroom connected to the laundry room. 

