---
title: "Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning"
date: "2026-03-02"
authors: "Shaohuai Liu; Weirui Ye; Yilun Du; Le Xie"
url: https://arxiv.org/abs/2603.01452
pdf: https://arxiv.org/pdf/2603.01452
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.01452)** / [論文ページ](https://arxiv.org/abs/2603.01452)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning** 

**Shaohuai Liu**<sup>1*</sup> **Weirui Ye**<sup>2*</sup> **Yilun Du**<sup>3</sup><sup>_†_</sup> Texas A&M University MIT Harvard University liushaohuai5@tamu.edu ywr@csail.mit.edu ydu@seas.harvard.edu 

**Le Xie**<sup>3</sup><sup>_†_</sup> Harvard University xie@seas.harvard.edu 

*Equal contribution _†_ Equal advising 

# **Abstract** 

Developing generalist robots capable of mastering diverse skills remains a central challenge in embodied AI. While recent progress emphasizes scaling model parameters and offline datasets, such approaches are limited in robotics, where learning requires active interaction. We argue that effective online learning should scale the _number of tasks_ , rather than the number of samples per task. This regime reveals a structural advantage of modelbased reinforcement learning (MBRL). Because physical dynamics are invariant across tasks, a shared world model can aggregate multi-task experience to learn robust, task-agnostic representations. In contrast, model-free methods suffer from gradient interference when tasks demand conflicting actions in similar states. Task diversity therefore acts as a regularizer for MBRL, improving dynamics learning and sample efficiency. We instantiate this idea with **EfficientZero-Multitask (EZ-M)** , a sample-efficient multi-task MBRL algorithm for online learning. Evaluated on **HumanoidBench** , a challenging whole-body control benchmark, EZ-M achieves state-of-the-art performance with significantly higher sample efficiency than strong baselines, without extreme parameter scaling. These results establish task scaling as a critical axis for scalable robotic learning. The project website is available here. 

# **1. Introduction** 

Generalist agents capable of robust generalization and adaptation remain a central objective in embodied AI research. Inspired by the success of Large Language Models (LLMs), recent trends in robotics have largely prioritized the Foundation Model paradigm—scaling model parameters and aggregating massive offline datasets (Reed et al., 2022; Brohan et al., 2022; Kim et al., 2024; Black et al., 2024; 


_Figure 1._ **Normalized task-average scores on HumanoidBenchHard** . EZ-M matches and surpasses the strong baselines with environment interactions limited to 1 million. All runs are with 3 random seeds. EZ-M significantly outperforms all baselines. 

O’Neill et al., 2024). While effective for broad task coverage, this approach faces a fundamental limitation unique to robotics: unlike passive text generation, embodied intelligence requires active interaction with physical environments. Relying solely on offline data limits an agent’s ability to correct errors, adapt to dynamic changes, and refine behaviors through feedback. Consequently, scaling online learning—improving the efficiency and efficacy of active interaction—is as critical as scaling offline data. 

We propose that effective online learning requires scaling the breadth of tasks, a paradigm we term online task scaling, rather than merely increasing sample counts per task. This shift exposes a critical structural advantage for ModelBased Reinforcement Learning (MBRL). While Model-Free (MF) policies often suffer from gradient interference when distinct tasks demand conflicting actions in similar states, MBRL focuses on learning the underlying transition dynamics. Since physical laws are task-invariant, a shared world model aggregates diverse multi-task data to refine its understanding of the environment. In this context, task diversity serves as a dynamics regularizer: it prevents the model from overfitting to the narrow state distributions of single tasks, 

1 

**Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning** 

ensuring the learned physics generalize globally. Consequently, MBRL effectively converts multi-task scaling into robust representation learning. 

In this work, we introduce EfficientZero-Multitask (EZ-M), a sample-efficient multi-task RL algorithm building upon the EfficientZero architecture (Ye et al., 2021). EZ-M incorporates targeted architectural modifications and consistency regularization to effectively exploit dynamics invariance in online settings. We evaluate our approach on HumanoidBench (Sferrazza et al., 2024), a high-dimensional domain where modeling complex contact-rich dynamics constitutes the primary bottleneck. 

Our empirical results demonstrate that EZ-M not only achieves State-of-the-Art (SoTA) performance but also exhibits distinct positive transfer properties: whereas ModelFree (MF) baselines degrade or plateau as task cardinality increases, EZ-M leverages task diversity to improve sample efficiency. This suggests a scalable trajectory for robotic learning: apart from relying exclusively on large-scale offline datasets, we envision a regime of massive parallel online learning, where diverse tasks synergize to construct a unified, generalized world model. And our primary contributions are as follows: 

- We propose EfficientZero-Multitask (EZ-M), extending the sample efficiency of MBRL to the multi-task online setting via novel consistency mechanisms that mitigate negative interference between tasks. 

- We provide a theoretical analysis formalizing the structural advantage of MBRL. We show that while MF objectives suffer from gradient conflict in multi-task settings, MBRL benefits from dynamics invariance, yielding asymptotically superior sample efficiency as the number of tasks increases. 

- We achieve State-of-the-Art performance on the comprehensive HumanoidBench, demonstrating that online task scaling in MBRL offers a viable pathway for highdimensional robotic control. 

# **2. Related Work** 

**Humanoid Control** . Humanoid control remains a rigorous benchmark due to under-actuation and contact complexity. While prior work spans imitation-based tracking (Peng et al., 2018) and adversarial RL (Peng et al., 2021), often leveraging GPU-accelerated simulation (Makoviychuk et al., 2021), comprehensive benchmarks like HumanoidBench (Sferrazza et al., 2024) highlight persistent challenges in stability and sample efficiency for online learning. 

**Multi-Task Learning.** To mitigate challenges like gradient interference (Yu et al., 2020) and heterogeneous re- 

ward scales (Hessel et al., 2019), prior work employs techniques ranging from gradient projection (Yu et al., 2020; Chen et al., 2018) to distillation (Teh et al., 2017). Parallel efforts leverage high-capacity Vision-Language-Action (VLA) models (Kim et al., 2024), applying supervised learning or offline RL to massive teleoperation datasets (O’Neill et al., 2024) to achieve generalization. Diverging from these resource-intensive paradigms, we prioritize **sampleefficient online learning** . Rather than relying on massive model scaling or pre-collected datasets, we utilize a compact shared dynamics model for MBRL. We demonstrate that structural regularization in dynamics and value learning can effectively substitute for sheer scale, enabling stable, task-scalable online RL within a limited parameter budget. 

**Model-Based RL.** Prior work establishes the efficacy of planning via learned dynamics, ranging from experience augmentation (Sutton, 1991) and latent rollouts (Hafner et al., 2019; 2023) to search-based trajectory selection (Hansen et al., 2022; Ye et al., 2021) and value re-estimation (Schrittwieser et al., 2020; Wang et al., 2025). Recent advances further integrate diffusion models (Hafner et al., 2025). However, these innovations primarily target single-task performance. The limited multi-task MBRL literature restricts itself to MPC approaches (Hansen et al., 2023; 2025), leaving the potential of MCTS for online multi-task learning unexplored. 

# **3. Preliminaries** 

**Multi-Task Reinforcement Learning** (MTRL) aims to train a single agent over a set of tasks _T_ . Each task _τ ∈T_ introduces an MDP _Mτ_ = ( _Sτ , Aτ , Pτ , rτ , γ_ ) with shared discount factor _γ_ but task-dependent state = space _Sτ_ , action space _Aτ_ , state transition _sτ,t_ +1 _Pτ_ ( _sτ,t, aτ,t_ ), and reward function _rτ_ . We learn a task-conditioned policy _πθ_ ( _a|s, τ_ ) maximizing the expected return averaged over _T_ , mathematically defined as _J_ ( _θ_ ) = E _τ ∈T_ �E _πθ_ ( _·|s,τ_ ) � _t≥_ 0<sup>_γtrτ_(</sup><sup>_sτ,t, aτ,t_)</sup> � Compared to single-task RL, MTRL must fit heterogeneous learning signals with a shared representation, which can cause gradient conflicts, negative transfer, and instability, especially for shared critics under different reward/value scales. Practical training typically mixes experience from multiple tasks via task-balanced sampling and task conditioning, while controlling cross-task interference through normalization or other stabilization techniques. 

**Monte Carlo Tree Search and Gumbel Search** are two tree search technologies used in MuZero series and EfficientZero series for producing improved policy and filtered actions. MCTS (Coulom, 2006; Kocsis & Szepesvari´ , 2006) and grows a search tree by iteratively expanding new nodes on leaves and recursively updating the values of nodes on 

2 

**Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning** 

the dive path. It dives along the path with node descents that have the highest upper confidence bound scores (Auer et al., 2002). MCTS produces an improved policy using the visit count distribution of the root descents and a filtered action that is most visited. Therefore, MCTS typically requires considerable node expansions to generate stable, improved policies, and the inability to parallelize also leads to computational efficiency issues (Ye et al., 2022). In contrast, Gumbel search (Danihelka et al., 2022) utilizes Gumbel sample-without-replacement (Kool et al., 2019) and sequential halving (Karnin et al., 2013) to iteratively dichotomize action spaces. It replaces count-based UCB for node selection with Gumbel scores, which are more reliant on value estimations. The benefits of these modifications are not only reduced node expansion, but more importantly, guarantee policy improvements. 

# **4. Methods** 

To train an RL agent across multiple tasks, the algorithm is supposed to satisfy: (1) scale with the number of tasks increases; (2) be adaptive to task-varying observation and action spaces; (3) be robust to task-varying reward and value scales; (4) be computationally efficient in terms of both training and inference. EZ-M is built upon the success of EfficientZero-v2, which proved to be sample and computation-efficient across tasks with visual/proprio inputs and continuous/discrete actions. We extend EfficientZerov2 to the online, multi-task RL, with improved designs that stabilize multi-task learning as listed below. Our methods could be summarized in Fig.2. 

## **4.1. Model, Search and Learning** 

**Model components** . EZ-M learns to plan over action candidates in a hidden state space by jointly conducting temporal consistency modeling, categorical reward/value prediction, and real/imagined TD-learning. In contrast to the methods like Dreamer series (Hafner et al., 2019; 2020; 2023) trained to reconstruct the original input, EZ-M didn’t employ the reconstruction loss and kept the model learning to be control objective concentrated. Different from EfficientZero-v2, EZ-M uses a separate reward prediction path identical to state transition prediction rather than connecting a reward prediction head after the next state prediction _rt_ = _R_ ( _ht_ +1). To avoid the interference of task-varying action dimensions and scales, an action encoder projects actions from different tasks into the same action embedding space to stabilize tasksharing model training. Specifically, the EZ-M architecture consists of six learned sub-networks: 


where _τ_ denotes the task identifier and _t_ represents the time step. The variables _hτ,t_ and _uτ,t_ correspond to the latent state representation and action embedding derived from the raw state _sτ,t_ and action _aτ,t_ , respectively. The dynamics network _G_ autoregressively predicts the subsequent latent state _h_<sup>ˆ</sup> _τ,t_ +1, while _r_ ˆ _τ,t_ and _v_ ˆ _τ,t_ estimate the immediate reward and value function. 

**Search with model priors** . We use the above model outputs as prior information to guide the tree search, and apply Gumbel Trick (Danihelka et al., 2022; Wang et al., 2024). 

At the root node, we calculate the Gumbel score _g_ ( _a_ ) of each root descent with action _a_ using model outputs, where 


where _σ_ is a monotonous function following (Danihelka et al., 2022). _{s, a}_ represents all state-action sets of the search tree with the limited node expansion budget, following the predictions of the dynamic network and policy network. _H_ represents the length of each dive trajectory during node expansion. _q_ ˆ( _a_ ) is the visit count-average of bootstrapped value estimation along the dive paths, normalized to [0,1] using min-max. Sequential Halving (Karnin et al., 2013) is applied to iteratively dichotomize the root action candidate set after equally expanding the remaining descents, defined as 


Then it will finally produce a filtered action _A_ and an improved policy _π_ via 


At non-root nodes, the action selection follows the proposed policy _p_ to avoid unexpected exploration noises finally introduced to root value estimations. This result in a principle that visit count matches policy prior. 

**Policy learning** . In contrast to max-Q policy gradient applied in actor-critic model-based RL algorithms (Hansen et al., 2022; 2023), we use supervised learning that let the policy head output _p_ to mimic the improved policy _π_ generated from the tree search. A key concern here is that EZ series are state-value based, thus it is not natural to apply max-Q learning. A related work demonstrates such distillation of improved policy can lead to improved performance in TD-MPC framework (Wang et al., 2025). 

3 

**Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning** 


_Figure 2._ **Overview of EfficientZero-Multitask (EZ-M)** . **Green** arrows and notations represent model inference and predictions. **Black** notations and bold arrows indicate target/grounded values and transitions. (A) **Task-sharing model architecture** . EZ-M uses a shared model to predict policy, value, and reward while training multiple tasks, with each component conditioned by task embeddings. (B) **Balanced data collection** . Rollout workers sample tasks with a balanced schedule and execute the corresponding task policy to interact with the environment. This prevents learning collapse from data imbalance and maintains diverse task coverage over time. (C) **Multi-task rollout learning** . For each sampled trajectory segment, the model is unrolled in latent space conditioned on the task index to produce ˆ _rτ,k_ , _v_ ˆ _τ,k_ , and _p_ ˆ _τ,k_ along the imagined rollout. Supervision comes from grounded transitions ( _aτ,k, rτ,k_ ) and reanalyzed targets ( _πτ,k, vτ,k_ ), where cross-entropy loss enables a single network to learn consistent predictions across tasks. **Blue** dashed lines represents temporal consistency and path consistency. (D) **Distributed implementation** . Data collection (Rollout) feeds trajectories into task-independent replay buffers, while Reanalyze periodically recomputes search-based targets with the latest model. The learner consumes reanalyzed batches to update parameters and broadcasts updated weights back to rollout/reanalyze workers for scalable asynchronous training. 

We uses full reanalyze, applying tree search on each sampled states from the experience replay, to generate the target policy since EZ-M follows the off-policy RL setting. To be specific, the improved policy _π_ consists of sampled action candidate set _A_ , their corresponding Gumbel scores _g_ , and a filtered action _A_ . We found that a simple Maximum Likelihood Estimation (MLE) loss, defined as 


produces more stable performance in practice, especially in tasks with high dimensional action spaces. 

**Reward prediction** . Accurately predicting environmental rewards under the situation that reward scales vary significantly with tasks is a critical challenge in multi-task modelbased RL. Similar problems of task-varying Q-value scales induced by heterogeneous reward scales have placed obstacles in multi-task model free RL (Hessel et al., 2019; Nauman et al., 2025). In contrast to applying complex reward normalization methods like those work, we rather solely uses categorical modeling in reward prediction (Schrittwieser et al., 2020) without normalization or parameter scaling. (Bellemare et al., 2017) also reports cross entropy loss over categorical modeling produces more balanced gradients and loss scales since the classification loss is not sensitive to scale changes. 

**Value learning** . Learning to predict value precisely is critical to our off-policy, value-based RL algorithm. Therefore, we applied a bunch of improvements on value prediction. We keep to use categorical modeling in value estimation since we didn’t use reward normalization, and it’s proved to be effective in predicting task-varying values in multi-task actor-critic RL(Nauman et al., 2025). We also use value ensemble proposed in (Hansen et al., 2023) to stablize value prediction and alleviate overestimation. Multiple value heads also bring a improvement in mixed value targets proposed in (Wang et al., 2024), which uses model-based value estimation, the root bootstrapped values of reanalyze tree search, on stale transitions sampled from the replay buffer. (Wang et al., 2024) uses a rule-based method on determining when to use model-based targets and what is stale transition. We can derive the value predicting variance with the multiple value estimations, previously used for designing intrinsic reward and increasing exploration (Osband et al., 2016; Pathak et al., 2017), and now we use the value variance as the weight balance between TD targets and model-based targets, defined as _v_ mix = _αv_ td +(1 _− α_ ) _v_ <u>model, where the weight co-</u> efficient _α_ = (Var(ˆ _v_ ) _−_ Var( _v_ ˆ)) _/_ (Var(ˆ _v_ ) _−_ Var( _v_ ˆ)). Var(ˆ _v_ ) and Var( _v_ ˆ) are the empirical maximum and minimum value variance. As the value variance goes higher, particularly in those fresh transitions, it is supposed to rely more on 

4 

**Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning** 

the TD-targets. The variance on those stale transitions is comparatively low, so we can use more model-based targets. 

**Temporal Consistency on Latent States** . To stabilize multi-step rollouts and mitigate representation drift during imagination, we impose a temporal consistency regularization on the latent space. Intuitively, this constraint enforces alignment between the predicted latent state (generated by the dynamics) and the encoded latent state (derived directly from the corresponding future observation). By encouraging these two pathways to converge, we ensure that imagined trajectories remain anchored to the representation induced by real data. Concretely, we minimize the projection distance (e.g., negative cosine similarity (Chen & He, 2021)) between the predicted transition and the target representation, utilizing a stop-gradient on the target to prevent collapse. This regularization is critical for multi-task learning, as it prevents the dynamics model from diverging under the distribution shifts introduced by diverse task mixing. 

**Base training objective** . In summary, we formulate the overall training objective as the sum of the reward prediction loss, the policy (or search-improved policy) loss, the value prediction loss, and the latent consistency regularization over _K_ unrolled steps: 


where _rk, πk, vk_ denote the training targets at unroll step _k_ (e.g., bootstrapped _n_ -step reward/value targets and the search policy target), and _r_ ˆ _k, pk,_ ˆ _vk_ are the corresponding network predictions. The term _L_ SimSiam( _·_ ) collects temporal consistency regularization on latent dynamics/representation. This unified objective allows EZ-M to learn a task-conditioned world model and planner-aligned policy/value predictions end-to-end from replayed trajectories, while maintaining stable latent rollouts that are crucial for effective planning. 

## **4.2. Path Consistency** 

A critical limitation in the loss design of Wang et al. (2024) is that reward and value predictors are trained via independent supervision, lacking explicit constraints for mutual consistency along imagined rollouts. Consequently, the learned value ˆ _v_ ( _hk_ ) often diverges from its recursive decomposition _r_ ˆ( _hk, uk_ ) + _γv_ ˆ( _hk_ +1). This discrepancy accumulates over rollout steps, leading to compounding estimation errors during tree search. In the multi-task setting, this inconsistency is further exacerbated, as the shared model must simultaneously generalize across heterogeneous task dynamics and varying reward scales. 

To address this issue, we incorporate a path-consistency 

regularizer to stabilize multi-task value learning under heterogeneous reward scales, inspired by (Farquhar et al., 2021). For a task _τ_ , given a _K_ -step trajectory segment ( _sk, ak, rk, sk_ +1)<sup>_K_</sup> _k_ =0<sup>_−_1sampled from the corresponding re-</sup> play buffer, we minimize the following objective 


The stop-gradient operator sg( _·_ ) prevents destabilizing target coupling between reward and value learning, since the path consistency loss will never update the reward prediction network. It is a satisfying property, as the network can concentrate on the challenging reward prediction across tasks. The final training objective could be formulated as a summation over tasks: 


## **4.3. Multi-Task Design Choices** 

**Learnable task embedding** . To accommodate EZ-M in multi-task learning, we introduce a learnable task embedding to explicitly condition all major components of the agent on the task identity (Hansen et al., 2023). Concretely, each task index is mapped to a trainable vector that is injected into the representation/dynamics/prediction modules via concatenation. This design provides a lightweight mechanism for task-specific specialization while keeping the majority of parameters shared, which is especially important when tasks exhibit distinct transition or similar patterns. In practice, the embedding enables the network to form task-aware latent states and value/reward predictions without requiring separate heads per task, and it also offers a clean interface for extending to new tasks by learning new embeddings while reusing the shared backbone. 

**Action masking and observation padding** . Multi-task environments often differ in action space size, and observation dimensionality in proprio control, which can break a single unified network interface. We address this by using action masking and observation padding to standardize inputs/outputs across tasks. For actions, we maintain a global action space and apply a per-task binary mask to invalidate illegal actions during both policy evaluation and planning. For observations, we pad task-specific observations with all-zero tensors to a fixed maximum dimension. This simple unification avoids ad-hoc architecture branching, preserves vectorized training, and ensures that differences across tasks are handled explicitly and safely (invalid actions are never selected, and padded inputs do not leak spurious signals). 

**Independent Experience Replay.** To mitigate task imbalance and minimize negative transfer arising from heterogeneous data distributions, we employ an independent 

5 

**Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning** 

experience replay strategy. In standard monolithic buffers, tasks with higher reward magnitudes or easier dynamics often dominate the prioritized sampling mechanism. In contrast, we maintain a dedicated replay buffer for each task, enabling explicit control over the inter-task sampling ratio. This decoupling ensures that complex or sparse-reward tasks are not marginalized by dominant ones. Furthermore, this design streamlines the architecture: sampling homogeneous batches facilitates consistent task conditioning and simplifies the management of task-specific action masks. 

# **5. Theoretical Analysis** 

We formalize the structural advantage of Model-Based RL (MBRL) for online task scaling. We show that while ModelFree (MF) baselines suffer from low gradient similarities across relevant tasks in Fig.3, EZ-M leverages task diversity as a dynamics regularizer, leading to superior asymptotic sample efficiency. 

## **5.1. Problem Formulation** 

Consider a multi-task setting _T_ = _{τ_ 1 _, . . . , τK}_ sharing a physical environment. We define the global state space _S_ and action space _A_ as the union of reachable states and actions across all tasks (or a shared latent manifold). While individual tasks may utilize subsets of these spaces, the physical transition dynamics _P_ ( _s_<sup>_′_</sup> _|s, a_ ) remain stationary. Each task _τk_ is defined by a unique reward function _rk_ ( _s, a_ ). In EZ-M, we map these to a shared latent space via _h_ = _H_ ( _s_ ) and _u_ = _U_ ( _a_ ). 

no conflicting objectives. While distinct tasks may require contradictory actions in the same state (e.g., Task A requires “turning left” vs. Task B requires “turning right”), the physical consequence of any action remains objective and independent of task intent. Thus, task diversity effectively acts as a regularizer, forcing the representation to capture the causal structure of the environment rather than task-specific correlations. 

## **5.3. Sample Complexity Analysis** 

Let _d_ dyn and _d_ rew denote the sample complexity to learn the transition dynamics and a single reward function. 

**Assumption 1 (Dynamics Dominance).** In highdimensional robotic control, learning the physical dynamics is significantly more sample-intensive than learning a taskspecific reward: _d_ dyn _≫ d_ rew. 

_Remark:_ This is consistent with theoretical findings in reward-free exploration (Jin et al., 2020; Agarwal et al., 2020), which establish that learning the transition operator governs the minimax sample complexity (scaling with _O_ ( _S_<sup>2</sup> _A_ )), whereas reward estimation is comparatively cheap (scaling with _O_ ( _SA_ )). 

**Theorem 5.3** ( **Asymptotic Task Scaling Efficiency** ) **.** _Let NMF and NMB denote the total sample complexity to master K tasks. Under worst-case interference for MF and shared dynamics for MB, the per-task sample complexity satisfies:_ 


## **5.2. Interference vs. Invariance** 

**Proposition 5.1** ( **Gradient Interference in MF** (Yu et al., 2020)) **.** _Let θ be the shared parameters of a model-free policy. If optimal policies for distinct tasks τi, τj require disjoint actions in the same latent state, the expected cosine similarity of their gradients is negative:_ 


_Remark:_ In standard MF-MTL, this necessitates gradient projection (e.g., PCGrad) or massive parameter scaling to disentangle conflicting task subspaces. 

**Lemma 5.2** ( **Dynamics Invariance** ) **.** _The physical transition dynamics P are invariant across T . Therefore, there exists a unique optimal parameter set ϕ_<sup>_∗_</sup> _for the dynamics model Gϕ that minimizes the prediction error for all tasks simultaneously:_ 


_Remark:_ Unlike policy learning, dynamics learning presents 

_Proof._ Model-free agents implicitly entangle dynamics and reward learning. Due to gradient interference (Proposition 5.1), they fail to share structural knowledge effectively, solving each control problem as an independent instance: _N_ MF _∝ K_ ( _d_ dyn + _d_ rew). In contrast, EZ-M decouples these processes. The invariant dynamics _G_ are learned once (Lemma 5.2). For any additional task _k >_ 1, the agent leverages the mature world model and only incurs the cost of learning the reward head. Thus, _N_ MB _≈_ 1 _·d_ dyn + _K ·d_ rew. Dividing by _K_ and taking the limit yields the result. 

# **6. Experiments** 

In this section, we outline the experiments that evaluate our proposed EZ-M approach. The experiments are designed to answer the following questions: (1) How does the performance of EZ-M compare to mainstream baselines? (2) How does model performance change with the number of tasks trained simultaneously? (3) How do world model components share knowledge between tasks? (4) What is the necessity of proposed methods, such as path consistency, task embedding, and independent experience replay? The 

6 

**Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning** 

answers to these questions are listed in the following subsections, and more details and curves of our experiment can be found in Appendix.A. 

## **6.1. Experimental settings** 

**Benchmarks** . We evaluate EZ-M on HumanoidBench (Sferrazza et al., 2024), a challenging suite for whole-body humanoid control that requires coordinating dozens of degrees of freedom under contact-rich dynamics. Compared to standard locomotion benchmarks like DMControl (Tassa et al., 2018) saturated with baselines, HumanoidBench involves difficult tasks like stair, hurdle, and maze that still remain a considerable gap to be solved. Following (Nauman et al., 2025), we consider two difficulty tiers, **Medium** and **Hard** . Medium uses the H1-* setting (no hand control) with 9 locomotion tasks: stand, walk, run, stair, crawl, slide, pole, hurdle, and maze. Hard uses H1hand-* (with hand control) with 14 tasks: the same 9 locomotion tasks plus sit-simple, sit-hard, balance-simple, balance-hard, and reach. Environment steps of both settings are limited to 1 million. The action-repeat is not applied. 

**Baselines.** We compare EZ-M against established baselines spanning single-task (ST) and multi-task (MT) regimes, as well as model-free (MF) and model-based (MB) approaches. Key baselines include **TD-MPC2** (ST, MB) (Hansen et al., 2023), **DreamerV3** (ST, MB) (Hafner et al., 2023), **MHSAC** (MT, MF) (Yang et al., 2020), and **BRC** (MT, MF) (Nauman et al., 2025). Baseline scores are sourced directly from published results where available; otherwise, we report results obtained from re-evaluating official code. Notably, BRC relies on a massive 1B-parameter model to achieve its performance. In contrast, EZ-M utilizes a compact architecture with only 16M parameters, demonstrating that structured world models can achieve superior sample efficiency without brute-force parameter scaling. 

**Evaluation Metrics.** To assess aggregate performance, we report normalized scores calculated as detailed in Appendix B. Additionally, we provide full training curves plotting original returns against environment steps in Figure 6 and Figure 7 (Appendix A). 

## **6.2. Performance Analysis & Knowledge Sharing** 

EZ-M achieves state-of-the-art (SoTA) performance on the challenging HumanoidBench suite. As illustrated in Figure 6, EZ-M demonstrates superior sample efficiency across the 9 medium-difficulty tasks compared to baselines. Furthermore, it maintains this dominance in the higherdimensional regime, outperforming competitors on the 14 contact-rich H1Hand tasks (Figure 7). Quantitatively, EZ-M effectively solves or achieves SoTA results in 7 out of 9 tasks in the Medium setting (Table 1) and 10 out of 14 tasks in the Hard setting (Figure 7), highlighting its robustness in 

complex control domains. 

**Gradient Similarity Analysis.** To investigate the underlying mechanisms, we analyze inter-task gradient similarity, comparing EZ-M’s World Model components (Dynamics, Reward, Policy/Value) against BRC’s Actor/Critic. We select ( _h1-walk_ , _h1-run_ ) as a _related_ pair and ( _h1-walk_ , _h1crawl_ ) as a _distantly related_ one. As shown in Figure 3, EZ-M consistently maintains high similarity for the related pair (darker orange lines) while keeping it low for the distant one (lighter orange lines). It indicates that EZ-M effectively exploits positive transfer while mitigating interference. In contrast, BRC exhibits consistently lower similarity even for related tasks, suggesting that the model-based architecture facilitates superior knowledge transfer via shared dynamics. 

**Failure Case Analysis.** While EZ-M dominates in locomotion and dynamic manipulation tasks, we observe a performance gap in stationary tasks like _sit-hard_ compared to BRC (Table 2). We hypothesize that the intricate self-contact dynamics in sitting poses are harder for the world model to predict accurately, leaving room for future improvements in contact modeling. 

**Computational Efficiency.** Despite the inherent overhead of MCTS planning, EZ-M maintains high efficiency through an asynchronous distributed architecture (Ye et al., 2021) that decouples rollout generation from model optimization. For the Medium task suite, EZ-M requires approximately **10 hours** on 2 NVIDIA A40 GPUs. In contrast, the strongest baseline, BRC, requires more than **40 hours** on a single A40 GPU to reach the same step count. These results demonstrate that EZ-M’s parallelized design effectively offsets its planning costs, yielding a significantly faster research turnaround than sequential model-free baselines. 

## **6.3. Performance scaling with the number of tasks** 

We further investigate the scaling properties of EZ-M with respect to the number of concurrent tasks. We evaluate training configurations with task cardinalities of _N ∈{_ 1 _,_ 4 _,_ 9 _}_ , where _N_ = 1 serves as the Single-Task baseline. For the _N_ = 4 setting, we partition the tasks into two disjoint subsets: _{h1-stand_ , _h1-walk_ , _h1-run_ , _h1-stair}_ and _{h1-crawl_ , _h1-pole_ , _h1-slide_ , _h1-hurdle}_ . To strictly isolate the benefit of multi-task scaling, we report the average performance on these 8 tasks across all settings. As illustrated in Figure 4, EZ-M exhibits a positive scaling law: performance consistently improves with the number of tasks given the same total environment step budget. This trend empirically validates the efficacy of multi-task online RL as a mechanism for amplifying sample efficiency. 

7 

**Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning** 


_Figure 3._ **Gradient similarities over training process** . We compare the gradient similarities on different model modules between BRC and EZ-M. We choose two task pairs, ( _h1-walk_ , _h1-run_ ) and ( _h1-walk_ , _h1-crawl_ ), representing _relevant_ and _irrelevant_ tasks, respectively. _dyn_ , _rew_ , and _vp_ represent the dynamics, reward, and value-policy model in EZ-M. **(Left)** We validate that the gradient similarities between the relevant task pair are higher than the irrelevant across the training process, indicating positive knowledge transfer. **(Right)** We showcase that EZ-M modules have higher gradient similarities than BRC modules in the relevant task pair. Curves are slightly smoothed for better visualization. 


_Figure 4._ **Performance scale with the number of tasks.** _y_ -axis denotes the task-average, normalized episodic return and _x_ -axis represents number of tasks in training simultaneously. We use 3 different random seeds and report 95% confidence intervals. 


_Figure 5._ **Ablations on model components.** _y_ -axis denotes the task-average, normalized episodic return and _x_ -axis represents different settings. _−_ represents removing a component. _TE_ represents task embedding. _Dyn_ , _Rew_ , _VP_ , _Rep_ represent the dynamics, reward, value-policy, representation model, respectively. - _Dyn_ - _Rew_ - _VP_ _~~T~~ E_ indicates removing the task embedding on dynamics, reward, and value-policy models. _IER_ represents independent experience replay. _PathCons_ is the path consistency loss. We use 3 different random seeds and report 95% confidence intervals. 

## **6.4. Ablation study** 

Finally, we perform ablation studies to isolate the individual contributions of the core mechanisms introduced in EZ-M: Path Consistency (PC) loss, Independent Experience Replay (IER), and Task Embeddings. Given the architectural depth of world models, we additionally investigate the optimal injection points for task conditioning. All experiments are conducted on the HumanoidBench-Medium setting with a 1M step budget. As illustrated in Figure 5, **Independent Experience Replay** emerges as the most critical component; its removal leads to the most severe performance degradation, underscoring its role in mitigating data imbalance. The **Path Consistency loss** also provides substantial gains by enforcing alignment between reward and value predictions. Furthermore, our structural analysis confirms that task embeddings are indispensable, particularly when conditioning the Dynamics and Reward models to capture task-specific physics and objectives. 

# **7. Discussion** 

In this work, we demonstrated the efficacy of ModelBased Reinforcement Learning for scaling online multi-task robotic control. Our results on HumanoidBench validate that task scaling serves as a powerful regularizer: by leveraging invariant physical dynamics, EZ-M converts diverse multi-task data into robust representations, achieving sample efficiency superior to model-free baselines. This confirms that shared world models effectively bridge distinct behaviors while mitigating the gradient interference that plagues policy-centric approaches. Limitations remain regarding the computational overhead of tree search, which may pose latency challenges for high-frequency real-world deployment. Additionally, our framework assumes a shared physical embodiment; transfer efficacy may diminish across tasks with disjoint dynamics or heterogeneous morpholo- 

8 

**Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning** 

gies. Future work will focus on (1) distilling the planner into a lightweight policy for real-time inference, and (2) integrating language-conditioned goals to extend EZ-M toward open-ended instruction following. 

# **References** 

- Agarwal, A., Kakade, S., Krishnamurthy, A., and Sun, W. Flambe: Structural complexity and representation learning of low rank mdps. _Advances in neural information processing systems_ , 33:20095–20107, 2020. 

- Auer, P., Cesa-Bianchi, N., and Fischer, P. Finite-time analysis of the multiarmed bandit problem. _Machine learning_ , 47(2):235–256, 2002. 

- Bellemare, M. G., Dabney, W., and Munos, R. A distributional perspective on reinforcement learning. In _International conference on machine learning_ , pp. 449–458. PMLR, 2017. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. corr, abs/2410.24164, 2024. doi: 10.48550. _arXiv preprint ARXIV.2410.24164_ , 2024. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Chen, X. and He, K. Exploring simple siamese representation learning. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 15750–15758, 2021. 

- Chen, Z., Badrinarayanan, V., Lee, C.-Y., and Rabinovich, A. Gradnorm: Gradient normalization for adaptive loss balancing in deep multitask networks. In _International conference on machine learning_ , pp. 794–803. PMLR, 2018. 

- Coulom, R. Efficient selectivity and backup operators in monte-carlo tree search. In _International conference on computers and games_ , pp. 72–83. Springer, 2006. 

- Danihelka, I., Guez, A., Schrittwieser, J., and Silver, D. Policy improvement by planning with gumbel. In _International Conference on Learning Representations_ , 2022. 

- Farquhar, G., Baumli, K., Marinho, Z., Filos, A., Hessel, M., van Hasselt, H. P., and Silver, D. Self-consistent models and values. _Advances in Neural Information Processing Systems_ , 34:1111–1125, 2021. 

- Hafner, D., Lillicrap, T., Ba, J., and Norouzi, M. Dream to control: Learning behaviors by latent imagination. _arXiv preprint arXiv:1912.01603_ , 2019. 

- Hafner, D., Lillicrap, T., Norouzi, M., and Ba, J. Mastering atari with discrete world models. _arXiv preprint arXiv:2010.02193_ , 2020. 

- Hafner, D., Pasukonis, J., Ba, J., and Lillicrap, T. Mastering diverse domains through world models, 2024. _URL https://arxiv. org/abs/2301.04104_ , 2023. 

- Hafner, D., Yan, W., and Lillicrap, T. Training agents inside of scalable world models. _arXiv preprint arXiv:2509.24527_ , 2025. 

- Hansen, N., Wang, X., and Su, H. Temporal difference learning for model predictive control. _arXiv preprint arXiv:2203.04955_ , 2022. 

- Hansen, N., Su, H., and Wang, X. Td-mpc2: Scalable, robust world models for continuous control. _arXiv preprint arXiv:2310.16828_ , 2023. 

- Hansen, N., Su, H., and Wang, X. Learning massively multitask world models for continuous control. _arXiv preprint arXiv:2511.19584_ , 2025. 

- Hessel, M., Soyer, H., Espeholt, L., Czarnecki, W., Schmitt, S., and Van Hasselt, H. Multi-task deep reinforcement learning with popart. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 33, pp. 3796–3803, 2019. 

- Jin, C., Krishnamurthy, A., Simchowitz, M., and Yu, T. Reward-free exploration for reinforcement learning. In _International Conference on Machine Learning_ , pp. 4870– 4879. PMLR, 2020. 

- Karnin, Z., Koren, T., and Somekh, O. Almost optimal exploration in multi-armed bandits. In _International conference on machine learning_ , pp. 1238–1246. PMLR, 2013. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-language-action model, 2024. _URL https://arxiv. org/abs/2406.09246_ , 2024. 

- Kocsis, L. and Szepesvari,´ C. Bandit based monte-carlo planning. In _European conference on machine learning_ , pp. 282–293. Springer, 2006. 

- Kool, W., Van Hoof, H., and Welling, M. Stochastic beams and where to find them: The gumbel-top-k trick for sampling sequences without replacement. In _International conference on machine learning_ , pp. 3499–3508. PMLR, 2019. 

- Makoviychuk, V., Wawrzyniak, L., Guo, Y., Lu, M., Storey, K., Macklin, M., Hoeller, D., Rudin, N., Allshire, A., 

9 

**Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning** 

Handa, A., et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- Nauman, M., Cygan, M., Sferrazza, C., Kumar, A., and Abbeel, P. Bigger, regularized, categorical: High-capacity value functions are efficient multi-task learners. _arXiv preprint arXiv:2505.23150_ , 2025. 

- Osband, I., Blundell, C., Pritzel, A., and Van Roy, B. Deep exploration via bootstrapped dqn. _Advances in neural information processing systems_ , 29, 2016. 

- O’Neill, A., Rehman, A., Maddukuri, A., Gupta, A., Padalkar, A., Lee, A., Pooley, A., Gupta, A., Mandlekar, A., Jain, A., et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 6892–6903. IEEE, 2024. 

- Pathak, D., Agrawal, P., Efros, A. A., and Darrell, T. Curiosity-driven exploration by self-supervised prediction. In _International conference on machine learning_ , pp. 2778–2787. PMLR, 2017. 

- Peng, X. B., Abbeel, P., Levine, S., and Van de Panne, M. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- Peng, X. B., Ma, Z., Abbeel, P., Levine, S., and Kanazawa, A. Amp: Adversarial motion priors for stylized physicsbased character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 

A., et al. Deepmind control suite. _arXiv preprint arXiv:1801.00690_ , 2018. 

   - Teh, Y., Bapst, V., Czarnecki, W. M., Quan, J., Kirkpatrick, J., Hadsell, R., Heess, N., and Pascanu, R. Distral: Robust multitask reinforcement learning. _Advances in neural information processing systems_ , 30, 2017. 

   - Wang, S., Liu, S., Ye, W., You, J., and Gao, Y. Efficientzero v2: Mastering discrete and continuous control with limited data. _arXiv preprint arXiv:2403.00564_ , 2024. 

   - Wang, Y., Guo, H., Wang, S., Qian, L., and Lan, X. Bootstrapped model predictive control. _arXiv preprint arXiv:2503.18871_ , 2025. 

   - Yang, R., Xu, H., Wu, Y., and Wang, X. Multi-task reinforcement learning with soft modularization. _Advances in Neural Information Processing Systems_ , 33:4767–4777, 2020. 

   - Ye, W., Liu, S., Kurutach, T., Abbeel, P., and Gao, Y. Mastering atari games with limited data. _Advances in neural information processing systems_ , 34:25476–25488, 2021. 

   - Ye, W., Abbeel, P., and Gao, Y. Spending thinking time wisely: Accelerating mcts with virtual expansions. _Advances in Neural Information Processing Systems_ , 35: 12211–12224, 2022. 

   - Yu, T., Kumar, S., Gupta, A., Levine, S., Hausman, K., and Finn, C. Gradient surgery for multi-task learning. _Advances in neural information processing systems_ , 33: 5824–5836, 2020. 

- Reed, S., Zolna, K., Parisotto, E., Colmenarejo, S. G., Novikov, A., Barth-Maron, G., Gimenez, M., Sulsky, Y., Kay, J., Springenberg, J. T., et al. A generalist agent. _arXiv preprint arXiv:2205.06175_ , 2022. 

- Schrittwieser, J., Antonoglou, I., Hubert, T., Simonyan, K., Sifre, L., Schmitt, S., Guez, A., Lockhart, E., Hassabis, D., Graepel, T., et al. Mastering atari, go, chess and shogi by planning with a learned model. _Nature_ , 588(7839): 604–609, 2020. 

- Sferrazza, C., Huang, D.-M., Lin, X., Lee, Y., and Abbeel, P. Humanoidbench: Simulated humanoid benchmark for whole-body locomotion and manipulation. _arXiv preprint arXiv:2403.10506_ , 2024. 

- Sutton, R. S. Dyna, an integrated architecture for learning, planning, and reacting. _ACM Sigart Bulletin_ , 2(4):160– 163, 1991. 

- Tassa, Y., Doron, Y., Muldal, A., Erez, T., Li, Y., Casas, D. d. L., Budden, D., Abdolmaleki, A., Merel, J., Lefrancq, 

10 

**Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning** 

# **A. Training Curves** 

Fig. 6 and Fig. 7 report the training dynamics on the Medium and Hard task suites, respectively. We plot the evaluation return against environment steps, where each curve is aggregated over multiple random seeds (with shaded regions indicating the variability across runs). These plots complement the main paper summary by revealing both learning speed and stability throughout training. 


_Figure 6._ **Unnormalized curves on HumanoidBench-Medium benchmark.** _y_ -axis denotes the episodic return and _x_ -axis represents environment interactions per million. All experiments use 3 different random seeds. We report 95% confidence intervals. 


_Figure 7._ **Unnormalized curves on HumanoidBench-Hard benchmark.** _y_ -axis denotes the episodic return and _x_ -axis represents environment interactions per million. All experiments use 3 different random seeds. We report 95% confidence intervals. 

11 

**Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning** 

# **B. Score Normalization & Table Performance** 

We normalize episode returns using the following equation: 


The random score and success score of each task could be found in Table.1 and 2. 

_Table 1._ **Scores for HumanoidBench-Medium (1M) tasks.** We **bold** the results surpass the success score or achieve the SoTA. 

|Task|Random|Success|MHSAC|TD-MPC2|BRC|BRC-ST|EZ-M(ours)|
|---|---|---|---|---|---|---|---|
|h1-stand|10.545|800.0|74.904|**810.688**|**829.358**|**841.246**|**806.034**|
|h1-walk|2.377|700.0|29.352|**814.249**|**844.784**|**858.926**|**802.969**|
|h1-run|2.020|700.0|17.434|**778.845**|**772.299**|439.246|**775.867**|
|h1-stair|3.112|700.0|25.421|**497.040**|474.852|322.088|459.234|
|h1-crawl|272.658|700.0|449.088|**963.360**|**949.326**|**971.295**|**830.971**|
|h1-slide|3.191|700.0|29.004|334.359|**831.837**|578.478|577.740|
|h1-pole|20.090|700.0|93.175|**744.285**|**897.267**|**869.307**|**878.993**|
|h1-hurdle|2.214|700.0|19.038|387.131|232.031|99.793|**542.286**|
|h1-maze|106.441|1200.0|251.297|311.648|354.939|344.027|**380.795**|


_Table 2._ Scores for HumanoidBench-Hard (1M) tasks. We **bold** the results surpass the success score or achieve the SoTA. 

|Task|Random|Success|DreamerV3|TD-MPC2|BRC|BRC-ST|EZ-M(ours)|
|---|---|---|---|---|---|---|---|
|h1hand-stand|11.973|800.0|40.938|196.511|**840.061**|315.990|**891.780**|
|h1hand-walk|2.505|700.0|19.819|234.061|515.383|**771.471**|**919.960**|
|h1hand-run|1.927|700.0|6.580|32.551|171.790|44.512|**818.397**|
|h1hand-stair|3.161|700.0|16.193|46.537|188.810|64.864|**380.349**|
|h1hand-crawl|278.868|800.0|261.801|**897.086**|735.992|**849.207**|644.386|
|h1hand-slide|3.142|700.0|20.625|89.454|313.723|148.877|**535.404**|
|h1hand-pole|19.721|700.0|48.306|98.703|512.936|386.245|**841.353**|
|h1hand-hurdle|2.371|700.0|6.381|38.890|108.067|46.112|**405.686**|
|h1hand-maze|106.233|1200.0|116.332|133.406|358.803|342.268|**380.642**|
|h1hand-sit<br>~~s~~imple|10.768|750.0|47.866|612.656|**926.804**|**843.850**|**814.762**|
|h1hand-sit<br>~~h~~ard|2.477|750.0|15.589|139.181|**805.502**|605.966|304.836|
|h1hand-balance<br>~~s~~imple|10.170|800.0|12.615|26.401|91.749|**101.260**|98.004|
|h1hand-balance<br>~~h~~ard|10.032|800.0|13.110|29.886|**72.918**|72.199|57.565|
|h1hand-reach|-50.024|12000.0|894.156|3610.454|3895.343|3729.537|**5353.093**|


12 

**Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning** 

# **C. Hyperparameters & Model architecture** 

Table 3 summarizes the key hyperparameters used in our experiments. Unless otherwise specified, we keep the same hyperparameter configuration across all tasks to ensure a fair comparison and to reduce per-environment tuning. 

Table 4 details the network architecture used by EZ-M on HumanoidBench-Hard. The model follows a modular design with a shared representation backbone, a task-embedding conditioning, and separate dynamics/reward/value/policy prediction components. We adopt lightweight MLP backbones with LayerNorm and residual blocks for stable optimization, while using discrete-support heads (51 bins) for reward and value prediction to improve learning signal quality. Overall, the full network contains only **16M** parameters, which is orders of magnitude smaller than the **BRC** baseline with a **1B** -scale model, highlighting the parameter-efficiency of our approach. 

_Table 3._ Key hyperparameters used in HumanoidBench experiments 

|**Hyperparameter**|**Value**|
|---|---|
|Environment|HumanoidBench|
|Discount factor_γ_|0.99|
|Unroll steps|5|
|TD steps|5|
|Batch size|512|
|Replay buffer size|1_×_10<sup>6 </sup>(Medium) /2_×_10<sup>6 </sup>(Hard)|
|Training steps|2_×_10<sup>5 </sup>(Medium) /6_×_10<sup>5 </sup>(Hard)|
|Network hidden dimension|512|
|Task embedding dimension|128|
|Task embedding usage|Rep / Dyn / Rew / Policy-Value|
|Number of res blocks|3|
|MCTS simulations|32|
|Top actions|16|
|Sampled actions|16|
|Optimizer|Adam|
|Learning rate|1_×_10<sup>_−_4</sup>|
|Weight decay|2_×_10<sup>_−_5</sup>|


_Table 4._ EfficientZero network architecture (for HumanoidBench-Hard). 

|Module|Architecture|
|---|---|
|Representation_fθ_|MLP(305_→_512) + LN + Tanh; 3_×_ResBlock(512)|
|Task embedding|Embedding(14, 128), max<br>~~n~~orm=1|
|Dynamics_gθ_|LN(701); MLP(701_→_512_→_512); 3_×_ResBlock(512)|
|Reward head_rθ_|act-MLP(189_→_64)+LN+Tanh;<br>dyn trunk: LN(704)+MLP(704_→_512_→_512)+3_×_ResBlock(512);<br>rew: [Linear(512_→_512)+BN+ReLU]_×_2; Linear(512_→_51)|
|Value heads_vθ_|trunk dim=640; 3_×_ResBlock(640);<br>5 heads: [Linear(640_→_512)+Dropout+BN+ReLU]_×_2; Linear(512_→_51)|
|Policy head_πθ_|[Linear(640_→_512)+BN+ReLU]_×_2; Linear(512_→_122)|
|Projection|Linear(512_→_1024)+LN+ReLU; Linear(1024_→_1024)+LN+ReLU;<br>Linear(1024_→_512)+LN|
|Proj. head|Linear(512_→_1024)+LN+ReLU; Linear(1024_→_512)|
|**Total params**|**16M**|


13 

