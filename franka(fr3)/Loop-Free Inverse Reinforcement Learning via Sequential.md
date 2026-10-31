---
title: "Loop-Free Inverse Reinforcement Learning via Sequential Value Recovery with Q-Score Matching"
date: "2026-09-30"
authors: "Yang Chen; Yitan Zhang; Michael Witbrock; Shuyue Hu"
url: https://arxiv.org/abs/2609.38955
pdf: https://arxiv.org/pdf/2609.38955
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.38955)** / [論文ページ](https://arxiv.org/abs/2609.38955)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

## **Loop-Free Inverse Reinforcement Learning via Sequential Value Recovery with Q-Score Matching** 

**Yang Chen**<sup>1</sup><sup>_∗_</sup> **Yitan Zhang**<sup>2</sup><sup>_∗_</sup> **Michael J. Witbrock**<sup>2</sup> **Shuyue Hu**<sup>1</sup><sup>_†_</sup> 1 Shanghai Artificial Intelligence Laboratory 2 University of Auckland `chenyang4@pjlab.org.cn, yzhb332@aucklanduni.ac.nz, m.witbrock@auckland.ac.nz, hushuyue@pjlab.org.cn` 

### **Abstract** 

Inverse Reinforcement Learning (IRL) aims to recover a reward function that explains expert demonstrations. Existing IRL methods typically rely on a bi-level optimization procedure that alternates between reward learning and policy optimization, leading to substantial computational burden and training instability. In this work, we introduce a different route that eliminates policy optimization entirely by leveraging diffusion policies. Our key insight is that a diffusion policy encodes the action-gradient structure of the optimal soft Q function, enabling reward learning to be cast as a sequence of value recovery problems, thereby allowing us to bypass reward-policy loops inherent in prior IRL methods. Specifically, our method proceeds in three stages: (I) recovering the optimal soft Q function via action-gradient matching and estimating the corresponding soft value function (LogSumExp of Q values) in a way inspired by Gumbel regression; (II) calibrating these soft values by inferring a state-dependent offset; (III) extracting the reward by enforcing Bellman consistency. This leads to _Loop-Free Inverse Reinforcement Learning_ (LFIRL), a fully offline algorithm that operates in a simple, loop-free, and sequential manner. LFIRL is simple to implement and significantly improves training efficiency while maintaining strong reward recovery performance. Empirically, across Maze, Franka Kitchen, Adroit Hand Pen, and Push-T benchmarks, LFIRL achieves **2-3x** speedup over the fastest baselines, while matching or surpassing state-of-the-art methods in reward recovery quality.<sup>3</sup> 

### **1 Introduction** 

Inverse reinforcement learning (IRL) [27, 1] studies how to recover a reward function from expert demonstrations, with the goal of explaining expert behavior through an underlying optimization principle. It has become an important paradigm for reward design, behavior understanding, and transferable decision making [21, 34]. In practice, however, a major bottleneck in IRL is time efficiency due to the inherent _loop structure_ underlying many classic and modern approaches [1, 50, 9, 10, 47]: the alternating update of the reward function and the policy. This loop arises because most IRL methods generally cannot extract reward-supervision signals directly from demonstrations. Instead, the reward is usually learned through differentiating expert behavior from the learner behavior. This mutual dependence naturally leads to a classic _bi-level_ optimization process, where a reward function is updated by contrasting expert demonstrations with learner behavior, the learner policy is then updated under the updated reward, and this process is repeated until convergence. Such a looped training paradigm is computationally expensive, especially in high-dimensional tasks, and also makes 

> _∗_ Equal contribution. 

> _†_ Corresponding author. 

> 3The implementation is available at `https://github.com/NothingThrough/LFIRL` . 

40th Conference on Neural Information Processing Systems (NeurIPS 2026). 


Figure 1: Traditional inverse reinforcement learning alternates between reward learning and policy optimization, while our loop-free version trains each component once without a reward-policy loop. 

the overall training process harder to stabilize. This raises our central question: _can we design an IRL method without the reward-policy loop while still recovering a useful reward function?_ 

If we could extract reward-supervision signals directly from demonstrations, then reward recovery would no longer need to be mediated by a reward-policy loop. Intuitively, demonstrations already contain local information about which nearby actions are more or less preferable around expert behavior. _Diffusion policy_ methods [5, 30, 33] provide a natural way to represent this information. Built on the recently burgeoning diffusion models [17, 36], a diffusion policy represents expert action distribution by transforming noise into actions through an iterative refinement process: it learns the gradient of the action distribution’s _score function_ , _∇_ **a** log _π_<sup>_∗_</sup> ( **a** _|_ **s** ), that describes the direction in which actions should move towards expert ones, and iteratively optimizes wrt this gradient field via a series of stochastic steps. This score-based signal is exactly what we need to break the reward-policy loop. Specifically, in the commonly used maximum-entropy reinforcement learning [14] setting, this score function encodes information of the gradient of the expert’s optimal soft Q function wrt actions, i.e., _∇_ **a** log _π_<sup>_∗_</sup> ( **a** _|_ **s** ) = _∇_ **a** _Q_<sup>_∗_</sup> ( **a** _,_ **s** ). Therefore, by matching its action gradient, we can estimate an optimal soft Q function directly from demonstrations, without relying on the differential information from an iteratively updated learner policy. 

Based on this observation, we propose a new IRL algorithm that avoids the conventional reward-policy loops and instead recovers the reward in a _fully sequential_ manner (see Fig. 1). Concretely, it proceeds in three sequential stages: **(I)** This stage first recovers an optimal soft Q function by matching its action gradients to the score induced by a diffusion policy, where we use a Sobolev-style training mechanism [6] to favor expert actions over nearby perturbations; then estimates the corresponding soft value function (V = LogSumExp Q) in a way inspired by Gumbel regression [13] (Sec. 4.1). **(II)** For deriving calibrated value functions, the second stage infers a state-dependent offset function, appending which to the already estimated Q and V yields their more accurate estimates (Sec. 4.2). **(III)** The final stage recovers the reward function from the calibrated Q and V functions by enforcing Bellman consistency (Sec. 4.3). The entire pipeline is _fully offline_ , using only a static set of trajectories. We empirically demonstrate that our resulting algorithm matches or surpasses state-of-the-art IRL baselines in reward recovery while significantly reducing training time (Sec. 5). 

Our contributions are summarized as follows: 

1. We introduce diffusion policy to IRL and propose the **Loop-Free Inverse Reinforcement Learning (LFIRL)** algorithm. It is a **fully offline** IRL algorithm that **avoids the computationally expensive looped reward-policy updates** in conventional IRL methods by leveraging the diffusion policy to realize a sequential value recovery procedure. 

2. We conduct empirical studies on tasks including Maze, Franka Kitchen, Adroit Hand Pen, and Push-T, showing that our method matches or surpasses strong online and offline baselines in reward recovery while **improving training time efficiency by 2-3x** in most settings. 

### **2 Related Work** 

**Inverse reinforcement learning.** IRL has been studied since the early formulations of reward recovery and apprenticeship learning [1, 27, 31, 50, 51], and was later extended to deep-learning variants such as Guided Cost Learning [9]. More recent adversarial formulations remain a dominant route for IRL and imitation learning, but they typically rely on a _nested loop_ between reward/discriminator 

2 

learning and policy optimization, including GAIL [16], AIRL [10], DAC [22], and observation-only adversarial variants such as GAIfO [39]. A broader unifying view is provided by the momentmatching perspective of imitation learning [37], while empirical studies such as [29] further highlight the sensitivity of adversarial pipelines to design choices. Several recent methods reduce or modify this classical reward-policy loop: Maximum-Likelihood IRL [47] proposes a _single-loop_ update, ValueDICE [23] avoids a separate RL optimization procedure through off-policy distribution matching, IQ-Learn [12] and LS-IQ [2] learn implicit Q-function formulations, PIRO [4] stabilizes non-adversarial reward-policy learning through trust-region reward optimization. Other approaches modify the imitation or policy-search process in different ways, including Coherent Soft Imitation Learning [41], successor-feature matching [20], FILTER [38], and Hybrid IRL [32]. In contrast to both nested-loop methods and single-loop approaches that tightly entangle reward and policy learning, our method adopts a _fully staged, sequential_ IRL pipeline: it uses diffusion-derived local action-score information to recover soft values, and then recovers rewards. 

**Diffusion-Based Imitation Learning.** Diffusion models have rapidly become strong policy classes for imitation learning, especially in robotics and multimodal control. Diffusion Policy [5] models actions through a conditional denoising process and has become a standard baseline for visuomotor behavior cloning, while subsequent work extends diffusion-based imitation learning through goalconditioned policies [33], diffusion-augmented behavioral cloning [3], improved visual or selfsupervised representations [25, 46], and architectural scaling studies [7, 49]. A smaller line of work uses diffusion models more directly for reward learning, for example by extracting reward-like quantities from diffusion models [28], learning rewards from expert videos [19], leveraging score information for policy optimization [30], or integrating diffusion into adversarial imitation pipelines as the _discriminator_ such as DiffAIL [40], DRAIL [24], and DIFO [18]. Recent score-matchingbased imitation methods such as [42] likewise emphasize the value of diffusion-derived gradient information. Our method differs from these directions in that we use a diffusion policy only as a score estimator for local supervision of soft _Q_ -recovery, and then recover _V_ and _r_ sequentially, rather than using diffusion as the final policy class, extracting relative trajectory-level rewards from multiple diffusion models, or embedding diffusion inside an adversarial reward-policy loop. 

### **3 Preliminaries** 

A Markov decision process (MDP) is defined by the tuple ( _S, S⊥, A, P, γ, r_ ), where _S_ and _A_ denote the state and action spaces, _S⊥ ⊆S_ is a set of absorbing states, _P_ ( _·|_ **s** _,_ **a** ) is the transition kernel, _γ ∈_ (0 _,_ 1) is the discount factor, and _r_ : _S × A →_ R is the reward function. For any absorbing state **s** _⊥ ∈S⊥_ , we have _P_ ( **s** _⊥|_ **s** _⊥,_ **a** ) = 1 and _r_ ( **s** _⊥,_ **a** ) = 0 for all **a** _∈A_ , which describes cannever-escape states, e.g., completions or failures of a game. Let _π_ ( **a** _|_ **s** ) be a stochastic policy, and let _ρ_<sup>_π_</sup> ( **s** _,_ **a** ) := 1 _−_ <u>1</u> _γ_ � _∞t_ =0<sup>Pr(</sup><sup>**s**</sup><sup>_t_=</sup><sup>**s**</sup><sup>_,_</sup><sup>**a**</sup><sup>_t_=</sup><sup>**a**</sup><sup>_|π, P_) denote its induced state-action density.</sup> 

#### **3.1 Maximum-Entropy RL and IRL** 

The goal of classic RL is to find a policy to maximize the expected discounted long-term rewards E( **s** _,_ **a** ) _∼ρπ_ [ _r_ ( **s** _,_ **a** )]. We consider a generalized version of Maximum-entropy (MaxEnt) RL that augments the reward objective with the relative entropy _Hµ_ ( _π_ ) := E( **s** _,_ **a** ) _∼ρπ_ [ _−_ log<sup>_π_</sup> _µ_ (<sup><u>(</u></sup> **a**<sup>**a**</sup> _|_<sup>_<u>|</u>_</sup> **s**<sup>**s**</sup> )<sup><u>)</u>] between</sup> _π_ and a reference policy _µ_ : E( **s** _,_ **a** ) _∼ρπ_ [ _r_ ( **s** _,_ **a** )] + _ε Hµ_ ( _π_ ), where _ε >_ 0 is the temperature parameter. It recovers the standard MaxEnt RL [14] objective up to a constant when _µ_ is uniform. 

Under this formulation of MaxEnt RL, the optimal policy admits the energy-based form 


where the optimal soft value function _V_<sup>_∗_</sup> ( **s** ) and optimal soft action value function _Q_<sup>_∗_</sup> ( **s** _,_ **a** ) satisfy 


Note that the MaxEnt optimality condition in Eq. (1) implies the following relation, _π_<sup>_∗_</sup> ( **a** _|_ **s** ) _/µ_ ( **a** _|_ **s** ) and _Q_<sup>_∗_</sup> ( **a** _|_ **s** ) have the same gradient wrt actions, which we will leverage to build our method upon: 


3 

In MaxEnt inverse RL (MaxEnt IRL), the reward function is unknown, while a set of expert demonstrations _DE_ = _{τi}_<sup>_N_</sup> _i_ =1<sup>is observed, where each trajectory</sup><sup>_τ_= (</sup><sup>**s**0</sup><sup>_,_</sup><sup>**a**0</sup><sup>_,_</sup><sup>**s**1</sup><sup>_,_</sup><sup>**a**1</sup><sup>_, . . ._) is generated by</sup> an expert policy _πE_ . The goal is to recover a reward function under which _πE_ is optimal under the above MaxEnt RL framework, which can be interpreted by the following optimization problem: 


The min-max structure of Eq. (4) reveals an inherent _bi-level_ optimization procedure of many classic and modern IRL methods [16, 8, 10, 48]: the upper level updates the reward by contrasting expert behavior with the learner behavior induced by the current reward, while the lower level updates the learner’s imitation policy. Classic IRL methods typically implement this bi-level procedure as a computationally expensive _nested reward-policy loop_ because the lower level is a full RL procedure for computing an optimal policy. Some recent methods [47, 48] improve time efficiency by introducing a relatively cheap _single reward-policy loop_ , where the lower level conducts one or several steps of policy improvement. Although this bi-level optimization structure is well theoretically grounded [16, 47] and has been shown to be effective in applications [43, 11], its induced reward-policy loops introduce inevitable computational burden and instability to the optimization process. 

#### **3.2 Diffusion Models and Diffusion Policy** 

Diffusion models [17, 36] generate samples by modeling a _forward process_ that gradually adds noise to data and a _reverse process_ that iteratively removes this noise to recover data samples. _Diffusion policy_ methods use this idea for imitating expert behavior, where a policy _π_ ( _·|_ **s** _t_ ) is modeled as an action generation process: given an MDP time step _t_ , let _{_ **a**<sup>_k_</sup> _t_<sup>_}K_</sup> _k_ =0<sup>denote the latent action sequence</sup> indexed by the diffusion step _k_ , where **a**<sup>0</sup> _t_<sup>correspondstotheinitialaction(samplesfromexpert</sup> demonstrations) and larger _k_ corresponds to noisier ones. The forward process uses a variance schedule _{βk}_<sup>_K_</sup> _k_ =1<sup>with</sup><sup>_αk_:= 1</sup><sup>_−βk_,</sup><sup>_α_¯</sup><sup>_k_:= �</sup><sup>_k_</sup> _j_ =1<sup>_αj_, and Gaussian noise</sup><sup>**_ϵ_**</sup><sup>_∼N_(0</sup><sup>_, I_); the noisy</sup> action at step _k_ can be written in closed form as 


The reverse process trains a noise predictor **_ϵϕ_** by minimizing the following MSE loss: 


Training the noise predictor **_ϵ_** _ϕ_ can be interpreted as learning _∇_ **a** log _πE_ ( **a** _|_ **s** _t_ ), the so-called _score_ of a diffusion policy, which is a vector field indicating the direction to adjust a noisy action to increase its likelihood under the expert action distribution. In the idealized limit of exact denoising, it can be shown that _∇_ **a** log _πE_ ( **a** _|_ **s** _t_ ) _|_ **a** = **a** _kt_<sup>=</sup><sup>_−_</sup> _~~√~~_ 1 _−_ <u>1</u> _α_ ¯ _k_<sup>**_ϵϕ_**(</sup><sup>**a**</sup> _t_<sup>_k,_</sup><sup>**s**</sup><sup>_t, k_)=:</sup><sup>_g_</sup><sup>**_ϕ_**(</sup><sup>**a**</sup> _t_<sup>_k,_</sup><sup>**s**</sup><sup>_t, k_).Combining this with</sup> Eq. (3), under the condition that the expert policy is soft-optimal, i.e., _πE_ = _π_<sup>_∗_</sup> , we have 


Thus, a pretrained diffusion policy can provide the action-gradient supervision signal to recover the optimal soft Q function. We will utilize this property to design our method. To stay self-contained, detailed derivations of the identity relationship in Eq. (7) are given in Appendix A.1. 

### **4 Methods** 

In this section, we present **Loop-Free Inverse Reinforcement Learning (LFIRL)** , a fully offline IRL algorithm that avoids reward-policy loops in conventional IRL approaches. Instead, it proceeds in three sequential stages (see Fig. 1): **(I)** first recover a soft Q function from diffusion-policy using Sobolev training and recover the value function _V_ from the learned _Q_ in a way inspired by Gumbel regression; **(II)** then infer the state-dependent offset and calibrate the _Q_ and _V_ ; **(III)** finally recover the reward from the learned _Q_ and _V_ by enforcing Bellman consistency. 

#### **4.1 Stage I: Recover the Soft Q Function and Value function** 

In this stage, we recover the optimal soft Q function through _Sobolev Training_ [6, 35], which trains neural networks by jointly matching function values and their derivatives. In our formulation, the 

4 


Figure 2: Illustration of matching policy’s score on Push-T task, where the goal is to push the T-shaped block to the target pose. The red circle marks the agent’s current position (initially in the Start panel), and the dark dashed curves indicate two optimal routes to reach the correct position for pushing the block. The arrows depict the action-gradient field supervised by the diffusion policy’s score; the blue dots are perturbed actions whose Q values are constrained below that of the expert action by a margin, thereby providing anchoring information. 

score function of the diffusion policy provides direct supervision on action-gradients. Specifically, we train a Q-network _Q_<sup>ˆ</sup> **_ω_** ( **s** _,_ **a** ) such that its action-gradient matches the diffusion policy’s score after correcting for the reference policy. Concretely, we align _∇_ **a** _Q_<sup>ˆ</sup> **_ω_** ( **s** _,_ **a** ) _|_ **a** = **a** _k_ with _g_ **_ϕ_** ( **a**<sup>_k_</sup> _,_ **s** _, k_ ) _− ∇_ **a** log _µ_ ( **a** _|_ **s** ) _|_ **a** = **a** _k_ , where **a**<sup>_k_</sup> is obtained by adding noise to an expert action **a**<sup>0</sup> via Eq. (5). 

However, the derivation of value supervision is not straightforward, as the optimal Q values themselves are indeed what we seek for. To address this, we introduce an implicit form of value supervision by enforcing a small margin between the Q values of expert actions and those of their _locally_ perturbed counterparts. We do not impose this margin globally, in order to preserve action diversity, as multiple actions may be optimal under the same state. Intuitively, this margin-based constraint effectively regularizes the Q function, using expert actions as “anchor points” to shape a more precise function surface. These settings, illustrated with Push-T task in Fig. 2, lead to the following loss function for training _Q_<sup>ˆ</sup> **_ω_** ( **s** _,_ **a** ): 


where _ξ >_ 0 is an intended margin, _η_ ( _·|_ **a** ) denotes the neighborhood of action **a** , ReLU( _x_ ) := max _{_ 0 _, x}_ denotes the Rectified Linear Unit function, and _λ ≥_ 0 is a weighting coefficient. In practice, we can instantiate the reference policy _µ_ ( **a** _|_ **s** ) as a simple distribution (e.g., uniform over bounded actions or a Gaussian prior), whose score _∇_ **a** log _µ_ ( **a** _|_ **s** ) is tractable. 

After obtaining _Q_<sup>ˆ</sup> **_ω_** , we estimate the corresponding soft value function. However, direct computation of _V_<sup>ˆ</sup> ( **s** ) = _ε_ log � _A_<sup>exp( ˆ</sup><sup>_Q_</sup><sup>**_ω_**(</sup><sup>**s**</sup><sup>_,_</sup><sup>**a**)</sup><sup>_/ε_)</sup><sup>_dµ_(</sup><sup>**a**</sup><sup>_|_</sup><sup>**s**) is generally intractable in continuous action spaces.To</sup> address this, we reformulate the problem via an equivalent moment condition, drawing inspirations from _Gumbel regression_ in RL [13], which models action selection by perturbing Q values with Gumbel distribution noise [15] and leverages _Gumbel-Max Trick_ [15] to infer the value function as the expected stochastic maximum, yielding a LogSumExp form.the unique solution to E **a** _∼µ_ ( _·|_ **s** )[exp( _<u>Q</u>_ ˆ **_ω_** <u>(</u> **s** _<u>,</u>_ **a** _ε_ <u>)</u> _−V_ <u>(</u> **s** <u>)</u> )] = 1 _._ This characterization allows us to estimateSpecifically, the soft value _V_<sup>ˆ</sup> ( **s** ) is _V_ ˆ ( **s** ) without explicitly computing the LogSumExp. We then construct a convex surrogate whose first-order condition recovers the above moment constraint: 


This objective is strictly convex in _v_ and admits a unique minimizer, which coincides with the soft value _V_<sup>ˆ</sup> ( **s** ). The derivation is provided in Appendix A.2. In practice, we freeze _Q_<sup>ˆ</sup> **_ω_** and train a value 

5 

network _V_<sup>ˆ</sup> **_χ_** on a set of trajectories _DS_ sampled from _µ_ through the following empirical objective 


Notably, although this objective coincides with the Gumbel regression loss [13], our derivation does not rely on a stochastic model for Q values, as _Q_<sup>ˆ</sup> **_ω_** is fixed during training _V_<sup>ˆ</sup> **_χ_** ; instead, it follows directly from the deterministic characterization of the LogSumExp under the reference policy _µ_ . 

#### **4.2 Stage II: Infer the State-Dependent Offset and Calibrate Soft Values** 

The soft values recovered in Stage I are _uncalibrated_ , as the action-gradient matching determines only how soft values change wrt actions, but does not reflect their state-dependent factors. This fact can be formally explained by the following proposition, whose justification is given in Appendix A.3. **Proposition 1.** _Assume πE_ = _π_<sup>_∗_</sup> _and that the learned diffusion policy’s score is exact in the sense of Eq._ (7) _. For each state_ **s** _, if the action-gradient matching term in Eq._ (8) _is minimized exactly, then there exists a state-dependent function b_<sup>_∗_</sup> : _S →_ R _such that Q_<sup>_∗_</sup> ( **s** _,_ **a** ) = _Q_<sup>ˆ</sup> **_ω_** ( **s** _,_ **a** ) + _b_<sup>_∗_</sup> ( **s** ) _._ 

This reflects the ambiguity caused by _shift invariance_ : adding any _state-dependent offset b_ ( **s** ) leaves action-gradient unchanged, i.e., _∇_ **a** _Q_<sup>ˆ</sup> **_ω_** ( **s** _,_ **a** ) = _∇_ **a** � _Q_ ˆ **_ω_** ( **s** _,_ **a** ) + _b_ ( **s** )�, making _Q_<sup>ˆ</sup> **_ω_** identifiable only up to _b_ ( **s** ). We therefore introduce an offset network _b_ **_ψ_** : _S →_ R and define the calibrated soft Q function as _Q_ **_ω_** _,_ **_ψ_** ( **s** _,_ **a** ) := _Q_<sup>ˆ</sup> **_ω_** ( **s** _,_ **a** ) + _b_ **_ψ_** ( **s** ) and write the calibrated soft value function from Stage I as _V_<sup>ˆ</sup> **_χ_** ( **s** ) + _b_ **_ψ_** ( **s** ). A key challenge is that the offset _b_ **_ψ_** is not identifiable from action-gradient information. While penalizing _b_<sup>2</sup> **_ψ_**<sup>can fix the shift ambiguity by selecting the minimum-norm solution</sup> among all equivalent offsets, it ignores the transition structure and may yield solutions that violate Bellman consistency. Therefore, we regularize the _Bellman-implied reward_ , 

_δ_ **_ω_** _,_ **_χ_** _,_ **_ψ_** ( **s** _t,_ **a** _t,_ **s** _t_ +1) := _Q_<sup>ˆ</sup> **_ω_** ( **s** _t,_ **a** _t_ ) + _b_ **_ψ_** ( **s** _t_ ) _− γ_ � _V_ ˆ **_χ_** ( **s** _t_ +1) + _b_ **_ψ_** ( **s** _t_ +1)� _,_ (11) 

which couples _b_ **_ψ_** across consecutive states and enforces consistency with the underlying dynamics. Intuitively, minimizing the squared norm of _δ_ **_ω_** _,_ **_χ_** _,_ **_ψ_** penalizes inconsistent offset value shifts across transitions, encouraging the offset to vary coherently along trajectories. 

In addition, absorbing states provide direct supervision: for any **s** _⊥ ∈S⊥_ , we have _Q_<sup>_∗_</sup> ( **s** _⊥,_ **a** ) = 0 for all **a** .<sup>4</sup> Thus, the resulting objective is 


where _λb ≥_ 0 is a regularization coefficient, _Q_<sup>ˆ</sup> **_ω_** and _V_<sup>ˆ</sup> **_χ_** are fixed, and only _b_ **_ψ_** is updated. 

After calibrating the soft Q function, we re-estimate the value function using the calibrated _Q_ **_ω_** _,_ **_ψ_** . Specifically, we freeze _Q_ **_ω_** _,_ **_ψ_** and optimize the Gumbel regression objective again: 


This second value-fitting step is needed because the soft value function must be consistent with the offset-calibrated soft Q function. 

#### **4.3 Stage III: Recover the Reward Function** 

Given the calibrated soft Q function _Q_ **_ω_** _,_ **_ψ_** and value function _V_ **_χ_** _′_ , reward recovery reduces to enforcing Bellman consistency. For a transition ( **s** _t,_ **a** _t,_ **s** _t_ +1), we write the Bellman-implied reward target _r_ = _Q_ **_ω_** _,_ **_ψ_** ( **s** _t,_ **a** _t_ ) _− γV_ **_χ_** _′_ ( **s** _t_ +1) _._ We parameterize the reward by a network _r_ **_θ_** and learn it by minimizing Bellman residual errors. To stabilize training, we apply clipping and normalization: 


4This zero value is caused by the absorbing state itself, not by a particular action, so it is used to calibrate the state-dependent offset rather than to provide the action-level value supervision used in Stage I. 

6 

**Algorithm 1** Loop-Free Inverse Reinforcement Learning (LFIRL) 

|1: **Input:** Expert demonstrations_DE_; initialized networks <sup>ˆ</sup>_Q_**_ω_**,_b_**_ψ_**,_V_**_χ_**, and_r_**_θ_**; refer|ence policy_µ_.|
|---|---|
|2: Train a (or load a pre-trained) diffusion policy on_DE_. {**Stage I**}<br><sup>ˆ</sup>||
|3: Recover _Q_**_ω_**(**s**_,_**a**)on_DE_ via matching diffusion policy’s score.|▷Eq. (8)|
|4: Recover_V_**_χ_**(**s**)on_DS_ using Gumbel-regression-style value fitting.|▷Eq. (10)|
|5: Recover state-dependent offset_b_**_ψ_**(**s**)on_DE_ and_DS_. {**Stage II**}<br>|▷Eq. (12)|
|6: Calibrate <sup>ˆ</sup>_V_**_χ_**_′_(**s**)by the calibrated Q values <sup>ˆ</sup>_Q_**_ω_**+_b_**_ψ_**(**s**).|▷Eq. (13)|
|7: Recover_r_**_θ_** on_DE_ and_DS_ by minimizing Bellman residual errors. {**Stage III**}|▷Eq. (15)|
|8: **Output:** recovered reward function_r_**_θ_**.||


#### **4.4 Algorithm Summary** 

The complete procedure of the proposed Loop-Free IRL framework is summarized in Algorithm 1. In contrast to traditional IRL pipelines, our method eliminates the reward-policy loop entirely: each stage is executed only once in a sequential manner, and every component is trained solely on the frozen outputs produced by preceding stages. Importantly, the algorithm is _fully offline_ , as _DS_ is an offline dataset collected from the reference policy _µ_ . Consequently, training requires neither environment interactions nor rollouts from a learned dynamics model during training. Overall, this loop-free offline design substantially improves training efficiency, as will be demonstrated experimentally. 

### **5 Experiments** 

We evaluate LFIRL from two perspectives: **(1)** reward recovery quality and **(2)** training time efficiency. 

#### **5.1 Experimental Setup** 

We consider four different kinds of tasks (see Fig. 3): PointMaze with the UMaze, Medium, and Large settings; Franka Kitchen consists of four subtasks; Adroit Hand Pen; and the Push-T manipulation [5]. We compare against four classes of baselines: (1) _Non-Adversarial IRL_ baselines: IQ-Learn [12] and ML-IRL [47]; (2) the _Adversarial IRL_ baseline: AIRL [10]; (3) the _Offline IRL_ baseline: Offline ML-IRL [48], CLARE [45], and ValueDICE [23]; and (4) _Diffusion-based GAIL_ baselines: DRAIL [24] and DIFO [18]. All reported results are averaged over five random runs. All methods are trained with the same environment-step budget, and within each environment we use the same number of expert demonstrations for all methods. Full implementation details, including hyperparameters and network architectures, are in Appendix E.1. 

To evaluate reward recovery on PointMaze and Franka Kitchen, we train an SAC [14] policy on the recovered reward, and then evaluate this policy in the original environment. We report success rate on PointMaze and the mean number of completed subtasks on Franka Kitchen. Since our method is designed to recover a reward function rather than directly output a policy, this setting provides a task-level assessment of whether the recovered reward induces the intended behavior. For the higher-dimensional Adroit Hand Pen and Push-T environments, we instead evaluate reward quality through discrimination: we construct balanced sets of high-quality and low-quality trajectories, score them with each learned reward model, and report the resulting classification accuracy. We additionally compare the recovered and ground-truth rewards on the same state-action samples using Pearson’s and Spearman’s correlation coefficients; the results are presented in Sec. 5.4. To evaluate efficiency, we record the training time required by each method to consume the same number of trajectory throughput, with each method run independently and without parallelized competition for compute resources. In addition to the main comparison, we also report an offset-ablation study and a demonstration-reduction study; the corresponding results are provided in Sec. 5.5 and Sec. 5.6. 

#### **5.2 Reward Recovery** 

The main results are shown in Fig. 4. Overall, LFIRL recovers highly effective rewards and exhibits strong cross-task robustness. Across various tasks, the recovered reward consistently supports competitive downstream control and achieves the best or near-best final performance in most settings. 

7 


Figure 3: Illustrations of the evaluation tasks used in our experiments. 


Figure 4: Reward-recovery results on PointMaze and Franka Kitchen. We report success rate on PointMaze and average completed subtasks on Franka Kitchen. Since LFIRL recovers the reward only at the final stage, its result is shown as a fixed final score rather than a policy-learning curve. For online IRL methods, “steps” denotes environment interaction steps. For offline IRL methods, “steps” denotes the number of transitions sampled from the offline dataset during training. 

Even in cases where it does not attain the single best score, its performance remains highly competitive, indicating that the proposed sequential recovery pipeline yields stable and transferable reward signals. 

For the higher-dimensional Push-T and Adroit Hand Pen, we instead evaluate whether the recovered reward can distinguish high-quality trajectories from low-quality ones. The results are reported in Tab. 1. These results further support a consistent overall picture: the reward recovered by LFIRL captures meaningful behavioral differences and generalizes well across qualitatively different evaluation protocols, including both downstream control and trajectory discrimination. 

#### **5.3 Average Running Time** 

Tab. 2 reports the average running time under the same step budget. Overall, LFIRL substantially reduces the time cost of training. Across tasks, it is consistently the fastest method, typically achieving about a 2–3x reduction in runtime compared with the fastest baseline in each setting, and a roughly 2–5x reduction when loading a pre-trained diffusion policy. These results confirm that removing the reward-policy optimization loop brings not only pipeline simplicity, but also a substantial practical gain in time efficiency. 

#### **5.4 Correlation with Ground-Truth Rewards** 

The preceding evaluations assess whether a recovered reward supports the intended behavior or distinguishes trajectories of different quality. We further evaluate reward recovery directly by comparing each learned reward with the environment’s ground-truth reward on the same set of state-action samples. We report Pearson’s correlation coefficient (PCC), which measures linear association between the recovered and ground-truth reward values, and Spearman’s rank correlation coefficient (SCC), which measures agreement between their rankings. A higher PCC indicates that 

Table 1: Trajectory-quality classification accuracy (%) on Push-T and Adroit Hand Pen using reward networks recovered by different IRL algorithms. Results are reported as mean _±_ standard deviation over five runs. 

|**Task**|LFIRL|AIRL|IQ-Learn|DIFO|DRAIL|ML-IRL|Offline ML-IRL|CLARE|ValueDICE|
|---|---|---|---|---|---|---|---|---|---|
|Push-T|**74.17**_±_**1.96**|59.67_±_2.08|39.67_±_0.58|**79.00**_±_**1.00**|49.67_±_1.15|71.33_±_2.33|42.67_±_1.20|71.00_±_3.67|**78.67**_±_**2.52**|
|Pen|**97.17**_±_**2.75**|90.00_±_2.45|74.33_±_7.59|91.67_±_2.05|**98.33**_±_**0.94**|71.00_±_4.32|66.00_±_12.43|94.67_±_0.58|95.67_±_1.15|


8 

Table 2: Average running time (in hours). “Load D.P.” denotes LFIRL with a pre-trained diffusion policy, while “Train D.P.” denotes LFIRL including diffusion-policy training time. “T.R.” is short for “time reduction” and reports the relative time saved compared with the fastest baseline (marked with an underline). 

|**Task**||**Onli**|**ne meth**|**ods**||**Offl**|**line metho**|**l ds**||**LF**|**IRL**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||AIRL I|Q-Learn|DIFO D|RAIL|ML-IRL<br>|ML-IRL C|LARE Val|ueDICE<br>L|oad D.P. T.|R. (SpeedUp)|Train D.P.|T.R. (SpeedUp)|
|UMaze|1.38|6.88|2.47|1.70|9.76|3.09|5.86|4.66|0.28|79.7% (5x)|0.43|68.8% (3x)|
|Maze(M)|3.67|10.10|7.05|2.65|13.80|4.99|5.98|4.87|0.77|70.9% (3x)|1.07|59.6% (2x)|
|Maze(L)|6.88|10.88|7.73|3.05|13.33|5.52|6.67|5.17|1.42|53.4% (2x)|1.80|41.0% (2x)|
|Kitchen|9.55|13.72|7.40|3.33|18.42|6.83|7.80|5.91|1.52|54.4% (2x)|1.87|43.8% (2x)|
|Push-T|1.57|8.55|4.05|1.95|9.50|2.10|3.20|5.30|0.35|77.7% (4x)|0.62|60.5% (3x)|
|Pen|4.83|14.88|10.83|7.50|18.52|6.53|3.79|4.71|1.18|68.9% (3x)|1.71|54.9% (2x)|


Table 3: Direct comparison of recovered and ground-truth rewards on the same state-action samples. Each entry reports PCC / SCC; higher values indicate stronger linear association / rank agreement. Bold indicates the highest value for each metric in each task. 

|**Method**|**UMaze**<br>**PCC / SCC**|**Medium**<br>**PCC / SCC**|**Large**<br>**PCC / SCC**|**Kitchen**<br>**PCC / SCC**|**Push-T**<br>**PCC / SCC**|**Pen**<br>**PCC / SCC**|**Average**<br>**PCC / SCC**|
|---|---|---|---|---|---|---|---|
|LFIRL (Ours)|**0.83 / 0.91**|**0.76**/ 0.82|**0.84 / 0.87**|**0.67 / 0.81**|0.72 /**0.81**|**0.79 / 0.85**|**0.77 / 0.85**|
|AIRL|0.65 / 0.86|0.63 / 0.74|0.77 / 0.75|0.44 / 0.63|0.69 / 0.74|0.75 / 0.71|0.66 / 0.74|
|IQ-Learn|0.62 / 0.74|0.59 / 0.62|0.65 / 0.70|0.34 / 0.51|0.48 / 0.65|0.47 / 0.62|0.53 / 0.64|
|DIFO|0.69 / 0.79|0.53 / 0.67|0.68 / 0.81|0.61 / 0.77|**0.83**/ 0.79|0.71 / 0.72|0.68 / 0.76|
|DRAIL|0.67 / 0.71|0.74 /**0.84**|0.69 / 0.78|0.56 / 0.76|0.51 / 0.56|0.63 / 0.62|0.63 / 0.71|
|ML-IRL|0.78 / 0.75|0.67 / 0.72|0.64 / 0.71|0.63 / 0.69|0.66 / 0.73|0.78 / 0.69|0.69 / 0.72|
|Offline ML-IRL|0.49 / 0.52|0.47 / 0.58|0.42 / 0.62|0.45 / 0.54|0.45 / 0.53|0.53 / 0.43|0.47 / 0.54|
|CLARE|0.72 / 0.80|0.68 / 0.74|0.49 / 0.61|0.24 / 0.46|0.51 / 0.79|0.58 / 0.55|0.54 / 0.66|
|ValueDICE|0.72 / 0.81|0.61 / 0.79|0.74 / 0.71|0.53 / 0.56|0.65 / 0.76|0.57 / 0.63|0.64 / 0.71|


the recovered reward more closely follows the ground-truth reward’s linear variation across samples; a higher SCC indicates that it better preserves which samples receive higher or lower reward. These measures assess agreement in structure and ordering, respectively, without requiring the recovered reward to have exactly the same scale or offset as the ground-truth reward. 

As shown in Tab. 3, LFIRL obtains the highest PCC on five of the six tasks and the highest SCC on five of the six tasks. Thus, LFIRL’s consistently strong results indicate that the sequential recovery procedure preserves both the linear variation and relative ordering of the ground-truth reward across a range of environments. 

#### **5.5 Ablation Study** 

We conduct an ablation study to evaluate the contribution of the state-dependent offset _b_ ( **s** ) in LFIRL. The results are shown in Fig. 5. Overall, removing _b_ ( **s** ) consistently degrades performance across the evaluated tasks, showing that inferring the offset and calibrating soft values are important for recovering a well-aligned value structure. This result supports our analysis in Sec. 4.2: calibrating this offset is necessary for obtaining a reliable downstream reward. 


#### **5.6 Reduced-Data Experiments** 

We further study how LFIRL behaves when the number of expert demonstrations is reduced. The results are shown in Fig. 6, where we use the full dataset, one-half of the demonstrations, and one-quarter of the demonstrations. Overall, the performance of LFIRL decreases as the number of demonstrations becomes smaller. This trend is consistent with the design of our method: the first stage recovers the Q function from local supervision around expert actions, and the number of available expert state-action anchors directly affects how accurately this action-value structure can 

9 


Figure 6: Reduced-data experiments with the full, one-half, and one-quarter of the demonstrations. We report success rate on PointMaze, average completed subtasks on Franka Kitchen, and reward on Push-T and Pen. 

be reconstructed. When the demonstration set is reduced, anchor coverage becomes sparser, which weakens the quality of Q recovery and subsequently affects downstream value and reward recovery. Nevertheless, LFIRL remains competitive across the reduced-data settings. 

### **6 Discussion** 

**Source of the time efficiency gain.** The efficiency of LFIRL mainly comes from its linear training pipeline, not merely from using offline training framework. Offline IRL methods can still be slow if they keep a reward-policy loop, since reward updates repeatedly depend on policy or value optimization under the current reward, no matter if the policy interacts with the environment. Even methods that reduce this cost, such as IQ-Learn [12], may avoid training an explicit policy in discrete action spaces but still rely on value or policy quantities induced by the current reward-related objective. LFIRL removes this repeated coupling with each stage using the frozen output of previous stages, and this is why LFIRL remains much faster than offline IRL methods in Tab. 2. 

**Choice of generative models.** In fact, LFIRL uses a conditional _Denoising Diffusion Probabilistic Model_ [17] (DDPM)-based diffusion policy to provide the derivative signal for Q function recovery, following common practice in diffusion-based imitation learning methods. In principle, any stateconditioned generative model that can provide a reliable score, or an action-gradient signal, can be used as the source of derivative supervision in Stage I. In Appendix B.1, we instantiate a version based on _Flow Matching_ [26], another popular generative model paradigm. However, Appendix B.2 shows that, under the same number of training epochs, this variant gives weaker reward recovery. One possible reason is that the two pretraining objectives may have different convergence behavior under the same epoch budget. Conditional DDPM training directly optimizes denoising over multiple noise levels, which provides a strong and stable supervision signal for action refinement around expert demonstrations. Flow Matching instead learns a continuous transport vector field, whose action-generation quality can be more sensitive to integration accuracy, schedule design, and training budget. As a result, the pretrained diffusion policy is less accurate for giving the score signal used for Q function recovery, which then propagates to the final reward. 

### **7 Conclusion** 

We propose LFIRL, a novel staged IRL framework that removes the conventional reward-policy optimization loop by turning reward recovery into a sequence of value-recovery problems. Concretely, LFIRL first recovers an optimal Q function from diffusion-policy score signals and estimates the soft value function via Gumbel-regression-style value fitting. It then infers a state-dependent offset to calibrate the recovered soft values and re-estimates the value function using the calibrated Q function. Finally, it recovers the reward function by enforcing Bellman consistency. Experiments on PointMaze, Franka Kitchen, Adroit Hand Pen, and Push-T show that LFIRL matches or surpasses strong baselines in reward recovery while substantially reducing training time, achieving 2-3x efficiency gains in most settings. **Limitations.** The quality of the recovered Q function depends on sufficient local anchors around expert actions. When anchor coverage is sparse, the method may require more demonstrations to reconstruct the action-value structure accurately. **Future work** may explore broader classes of generative models beyond DDPM and Flow Matching for providing action-gradient supervision, and develop more sample-efficient ways to recover reliable value and reward information from limited expert demonstrations. 

10 

### **References** 

- [1] Pieter Abbeel and Andrew Y Ng. Apprenticeship learning via inverse reinforcement learning. In _Proceedings of the twenty-first international conference on Machine learning_ , page 1, 2004. 1, 2 

- [2] Firas Al-Hafez, Davide Tateo, Oleg Arenz, Guoping Zhao, and Jan Peters. Ls-iq: implicit reward regularization for inverse reinforcement learning. In _11th International Conference on Learning Representations, ICLR 2023_ , 2023. 3 

- [3] Shang-Fu Chen, Hsiang-Chun Wang, Ming-Hao Hsu, Chun-Mao Lai, and Shao-Hua Sun. Diffusion model-augmented behavioral cloning. In _Forty-first International Conference on Machine Learning_ , 2024. 3 

- [4] Yang Chen, Menglin Zou, Jiaqi Zhang, Yitan Zhang, Junyi Yang, Gael Gendron, Libo Zhang, Jiamou Liu, and Michael J. Witbrock. Trust region reward optimization and proximal inverse reward optimization algorithm. In _Advances in Neural Information Processing Systems_ , 2025. 3 

- [5] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11):1684–1704, 2025. 2, 3, 7, 19 

- [6] Wojciech M Czarnecki, Simon Osindero, Max Jaderberg, Grzegorz Swirszcz, and Razvan Pascanu. Sobolev training for neural networks. _Advances in neural information processing systems_ , 30, 2017. 2, 4 

- [7] Sudeep Dasari, Oier Mees, Sebastian Zhao, Mohan Kumar Srirama, and Sergey Levine. The ingredients for robotic diffusion transformers. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 15617–15625. IEEE, 2025. 3 

- [8] Chelsea Finn, Paul Christiano, Pieter Abbeel, and Sergey Levine. A connection between generative adversarial networks, inverse reinforcement learning, and energy-based models. _arXiv preprint arXiv:1611.03852_ , 2016. 4 

- [9] Chelsea Finn, Sergey Levine, and Pieter Abbeel. Guided cost learning: Deep inverse optimal control via policy optimization. In _International conference on machine learning_ , pages 49–58. PMLR, 2016. 1, 2 

- [10] Justin Fu, Katie Luo, and Sergey Levine. Learning robust rewards with adversarial inverse reinforcement learning. In _International Conference on Learning Representations_ , 2018. 1, 3, 4, 7 

- [11] Justin Fu, Anoop Korattikara, Sergey Levine, and Sergio Guadarrama. From language to goals: Inverse reinforcement learning for vision-based instruction following. In _International Conference on Learning Representations_ , 2023. 4 

- [12] Divyansh Garg, Shuvam Chakraborty, Chris Cundy, Jiaming Song, and Stefano Ermon. Iq-learn: Inverse soft-q learning for imitation. _Advances in Neural Information Processing Systems_ , 34:4028–4039, 2021. 3, 7, 10 

- [13] Divyansh Garg, Joey Hejna, Matthieu Geist, and Stefano Ermon. Extreme q-learning: Maxent rl without entropy. In _The Eleventh International Conference on Learning Representations_ , 2023. 2, 5, 6 

- [14] Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In _International conference on machine learning_ , pages 1861–1870. Pmlr, 2018. 2, 3, 7 

- [15] Tamir Hazan and Tommi Jaakkola. On the partition function and random maximum a-posteriori perturbations. In _Proceedings of the 29th International Conference on Machine Learning_ , pages 1667–1674, 2012. 5 

- [16] Jonathan Ho and Stefano Ermon. Generative adversarial imitation learning. _Advances in neural information processing systems_ , 29, 2016. 3, 4 

- [17] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. _Advances in neural information processing systems_ , 33:6840–6851, 2020. 2, 4, 10 

- [18] Bo-Ruei Huang, Chun-Kai Yang, Chun-Mao Lai, Dai-Jie Wu, and Shao-Hua Sun. Diffusion imitation from observation. _Advances in Neural Information Processing Systems_ , 37:137190–137217, 2024. 3, 7 

- [19] Tao Huang, Guangqi Jiang, Yanjie Ze, and Huazhe Xu. Diffusion reward: Learning rewards via conditional video diffusion. _European Conference on Computer Vision (ECCV)_ , 2024. 3 

11 

- [20] Arnav Kumar Jain, Harley Wiltzer, Jesse Farebrother, Irina Rish, Glen Berseth, and Sanjiban Choudhury. Non-adversarial inverse reinforcement learning via successor feature matching. In _The Thirteenth International Conference on Learning Representations_ , 2025. 3 

- [21] Mrinal Kalakrishnan, Peter Pastor, Ludovic Righetti, and Stefan Schaal. Learning objective functions for manipulation. In _2013 IEEE International Conference on Robotics and Automation_ , pages 1331–1336. IEEE, 2013. 1 

- [22] Ilya Kostrikov, Kumar Krishna Agrawal, Debidatta Dwibedi, Sergey Levine, and Jonathan Tompson. Discriminator-actor-critic: Addressing sample inefficiency and reward bias in adversarial imitation learning. In _International Conference on Learning Representations_ , 2019. 3 

- [23] Ilya Kostrikov, Ofir Nachum, and Jonathan Tompson. Imitation learning via off-policy distribution matching. _arXiv preprint arXiv:1912.05032_ , 2019. 3, 7 

- [24] Chun-Mao Lai, Hsiang-Chun Wang, Ping-Chun Hsieh, Yu-Chiang F Wang, Min-Hung Chen, and Shao-Hua Sun. Diffusion-reward adversarial imitation learning. _Advances in Neural Information Processing Systems_ , 37:95456–95487, 2024. 3, 7 

- [25] Xiang Li, Varun Belagali, Jinghuan Shang, and Michael S Ryoo. Crossway diffusion: Improving diffusionbased visuomotor policy via self-supervised learning. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 16841–16849. IEEE, 2024. 3 

- [26] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matthew Le. Flow matching for generative modeling. In _The Eleventh International Conference on Learning Representations_ , 2023. 10, 16 

- [27] Andrew Y Ng, Stuart Russell, et al. Algorithms for inverse reinforcement learning. In _Icml_ , volume 1, page 2, 2000. 1, 2 

- [28] Felipe Nuti, Tim Franzmeyer, and João F Henriques. Extracting reward functions from diffusion models. _Advances in Neural Information Processing Systems_ , 36:50196–50220, 2023. 3 

- [29] Manu Orsini, Anton Raichuk, Léonard Hussenot, Damien Vincent, Robert Dadashi, Sertan Girgin, Matthieu Geist, Olivier Bachem, Olivier Pietquin, and Marcin Andrychowicz. What matters for adversarial imitation learning? _Advances in Neural Information Processing Systems_ , 34:14656–14668, 2021. 3 

- [30] Michael Psenka, Alejandro Escontrela, Pieter Abbeel, and Yi Ma. Learning a diffusion model policy from rewards via q-score matching. In _Forty-first International Conference on Machine Learning_ , 2024. 2, 3 

- [31] Nathan D Ratliff, J Andrew Bagnell, and Martin A Zinkevich. Maximum margin planning. In _Proceedings of the 23rd international conference on Machine learning_ , pages 729–736, 2006. 2 

- [32] Juntao Ren, Gokul Swamy, Zhiwei Steven Wu, J Andrew Bagnell, and Sanjiban Choudhury. Hybrid inverse reinforcement learning. _arXiv preprint arXiv:2402.08848_ , 2024. 3 

- [33] Moritz Reuss, Maximilian Li, Xiaogang Jia, and Rudolf Lioutikov. Goal-conditioned imitation learning using score-based diffusion policies. _arXiv preprint arXiv:2304.02532_ , 2023. 2, 3 

- [34] Sahand Sharifzadeh, Ioannis Chiotellis, Rudolph Triebel, and Daniel Cremers. Learning to drive using inverse reinforcement learning and deep q-networks. _arXiv preprint arXiv:1612.03653_ , 2016. 1 

- [35] Hwijae Son, Jin Woo Jang, Woo Jin Han, and Hyung Ju Hwang. Sobolev training for physics informed neural networks. _arXiv preprint arXiv:2101.08932_ , 2021. 4 

- [36] Yang Song, Jascha Sohl-Dickstein, Diederik P Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole. Score-based generative modeling through stochastic differential equations. In _International Conference on Learning Representations_ , 2021. 2, 4 

- [37] Gokul Swamy, Sanjiban Choudhury, J Andrew Bagnell, and Steven Wu. Of moments and matching: A game-theoretic framework for closing the imitation gap. In _International Conference on Machine Learning_ , pages 10022–10032. PMLR, 2021. 3 

- [38] Gokul Swamy, David Wu, Sanjiban Choudhury, Drew Bagnell, and Steven Wu. Inverse reinforcement learning without reinforcement learning. In _International Conference on Machine Learning_ , pages 33299– 33318. PMLR, 2023. 3 

- [39] Faraz Torabi, Garrett Warnell, and Peter Stone. Generative adversarial imitation from observation. _arXiv preprint arXiv:1807.06158_ , 2018. 3 

12 

- [40] Bingzheng Wang, Guoqiang Wu, Teng Pang, Yan Zhang, and Yilong Yin. Diffail: Diffusion adversarial imitation learning. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pages 15447–15455, 2024. 3 

- [41] Joe Watson, Sandy Huang, and Nicolas Heess. Coherent soft imitation learning. _Advances in Neural Information Processing Systems_ , 36:14540–14583, 2023. 3 

- [42] Runzhe Wu, Yiding Chen, Gokul Swamy, Kianté Brantley, and Wen Sun. Diffusing states and matching scores: A new framework for imitation learning. In _The Thirteenth International Conference on Learning Representations_ , 2025. 3 

- [43] Zheng Wu, Liting Sun, Wei Zhan, Chenyu Yang, and Masayoshi Tomizuka. Efficient sampling-based maximum entropy inverse reinforcement learning with application to autonomous driving. _IEEE Robotics and Automation Letters_ , 5(4):5355–5362, 2020. 4 

- [44] Omar G. Younis, Rodrigo Perez-Vicente, John U. Balis, Will Dudley, Alex Davey, and Jordan K Terry. Minari, September 2024. URL `https://doi.org/10.5281/zenodo.13767625` . 19 

- [45] Sheng Yue, Guanbo Wang, Wei Shao, Zhaofeng Zhang, Sen Lin, Ju Ren, and Junshan Zhang. Clare: Conservative model-based reward learning for offline inverse reinforcement learning. In _11th International Conference on Learning Representations, ICLR 2023_ , 2023. 7 

- [46] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 3 

- [47] Siliang Zeng, Chenliang Li, Alfredo Garcia, and Mingyi Hong. Maximum-likelihood inverse reinforcement learning with finite-time guarantees. _Advances in Neural Information Processing Systems_ , 35:10122–10135, 2022. 1, 3, 4, 7 

- [48] Siliang Zeng, Chenliang Li, Alfredo Garcia, and Mingyi Hong. When demonstrations meet generative world models: A maximum likelihood framework for offline inverse reinforcement learning. _Advances in Neural Information Processing Systems_ , 36:65531–65565, 2023. 4, 7 

- [49] Minjie Zhu, Yichen Zhu, Jinming Li, Junjie Wen, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, Yaxin Peng, Feifei Feng, et al. Scaling diffusion policy in transformer to 1 billion parameters for robotic manipulation. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 10838– 10845. IEEE, 2025. 3 

- [50] Brian D Ziebart, Andrew L Maas, J Andrew Bagnell, Anind K Dey, et al. Maximum entropy inverse reinforcement learning. In _Aaai_ , volume 8, pages 1433–1438. Chicago, IL, USA, 2008. 1, 2 

- [51] Brian D Ziebart, J Andrew Bagnell, and Anind K Dey. Modeling interaction via the principle of maximum causal entropy. In _Proceedings of the 27th International Conference on Machine Learning_ , pages 1255– 1262, 2010. 2 

13 

# **Appendices** 

### **A Detailed Derivations** 

#### **A.1 Derivation of Diffusion Scores and Their Relation to Soft Q-Gradients** 

In this appendix, we derive the identities underlying Section 3. We use _t_ for the MDP time index and _k_ for the diffusion step. For a fixed state **s** _t_ , let **a**<sup>0</sup> _t_<sup>_∼πE_(</sup><sup>_· |_</sup><sup>**s**</sup><sup>_t_) denote a clean expert action, and let</sup> **a**<sup>_k_</sup> _t_<sup>denote its noisy version at diffusion step</sup><sup>_k_.</sup> 

The DDPM forward process is defined by 


This gives the closed-form marginal 

or equivalently, 

This is the same forward noising relation used in Eq. (5). 

For each fixed ( **s** _t, k_ ), let _pk_ ( **a** _|_ **s** _t_ ) denote the conditional density of noisy actions at diffusion step _k_ , induced by sampling **a**<sup>0</sup> _t_<sup>_∼πE_(</sup><sup>_· |_</sup><sup>**s**</sup><sup>_t_) and then applying Eq. (16).The score of this noisy action</sup> density is 


The diffusion policy is trained by the noise-prediction objective 


Using the Gaussian corruption in Eq. (16), the noisy-action score satisfies 


Therefore, the learned noise predictor induces the score estimator 

In the idealized limit of exact denoising, the approximation in Eq. (17) becomes exact for the noisy conditional density _pk_ ( **a** _|_ **s** _t_ ). 


Taking the action gradient gives 

which is Eq. (3). 

Combining the low-noise score approximation with Eq. (3), we obtain 


This is the identity used in Eq. (8): the diffusion-policy score, after subtracting the reference-policy score, provides the action-gradient supervision for recovering the soft _Q_ -function. 

14 

#### **A.2 Derivations for Stage I: Q-Recovery and Initial Value Fitting** 

In this subsection, we justify the first-stage recovery of the uncalibrated soft _Q_ -function and the initial value function. The key point is that matching action derivatives recovers the action-dependent geometry of _Q_<sup>_∗_</sup> , but cannot determine its state-dependent offset. 

We next justify the Gumbel-regression objective used to obtain the initial value estimate from the frozen _Q_<sup>ˆ</sup> **_ω_** . For a fixed state **s** and a fixed Q function _Q_<sup>�</sup> , define 


Differentiating with respect to _v_ gives 

The first-order condition is therefore 

Rearranging gives 

Moreover, 


so the minimizer is unique. 

In Stage I, we instantiate _Q_<sup>�</sup> as the frozen action value function _Q_<sup>ˆ</sup> **_ω_** . Replacing the expectation over _µ_ ( _· |_ **s** ) by actions gives 


This is Eq. (10). Since _Q_<sup>ˆ</sup> **_ω_** is fixed in this step, gradients are taken only with respect to **_χ_** . The resulting value network _V_<sup>ˆ</sup> **_χ_** is the initial value estimate used in Stage II for offset calibration. 

#### **A.3 Derivations for Stage II: Offset Calibration and Value Re-estimation** 

_Proof of Proposition 1._ Fix any state **s** and a connected action neighborhood on which the low-noise diffusion-score supervision is reliable. If the derivative-matching term in Eq. (8) is minimized exactly, then for every initial action point **a** in this neighborhood, 


where **a**<sup>_k_</sup> denotes the low-noise corrupted version of **a** . By Eq. (7), under the idealized assumptions that _πE_ = _π_<sup>_∗_</sup> and the diffusion score is exact, 


Thus, 


Since the gradients match only with respect to the action variable, the two functions can differ by a term that depends on the state but not on the action. Therefore, there exists a state-dependent function _b_<sup>_∗_</sup> : _S →_ R such that 


on the sampled action neighborhood. This proves Proposition 1. 

15 

### **B Flow-Matching Version of Diffusion Policy** 

#### **B.1 Flow-Matching Policy and Score Estimation** 

The main method uses a DDPM-based diffusion policy to provide the score estimator _gϕ_ ( **a** _t_<sup>_k,_</sup><sup>**s**</sup><sup>_t, k_).</sup> To keep the presentation concise, this subsection follows the simplified case that the reference policy _µ_ is uniform. In this case, _∇_ **a** log _µ_ ( **a** _|_ **s** ) = 0 inside the support, so the generative-model score can be directly used as the action-gradient signal for Stage I. This is not the only possible generative pretraining choice. A Flow-Matching-based model can also be used as a conditional action generator, and under a simple Gaussian interpolation path it can provide a score estimator that plays the same role in Stage I. This section explains this replacement. 

Flow Matching trains a time-dependent vector field that transports samples from a simple noise distribution to the data distribution [26]. In the policy setting, the data distribution is the expert action distribution conditioned on the current state. Let _u ∈_ [0 _,_ 1] denote the flow time, where _u_ = 0 corresponds to Gaussian noise and _u_ = 1 corresponds to expert actions. Given an expert pair ( **s** _t,_ **a** _t_ ) _∼DE_ and Gaussian noise **_ϵ_** _∼N_ (0 _, I_ ), the interpolation is defined as: 


Here, **a**<sup>_u_</sup> _t_<sup>is an intermediate noisy action along the path from noise to the expert action.The derivative</sup> of this path with respect to _u_ is 

_d du_<sup>**a**</sup> _t_<sup>_u_=</sup><sup>**a**</sup><sup>_t−_</sup><sup>**_ϵ_**</sup><sup>_._</sup> 

A Flow-Matching policy therefore learns a state-conditioned velocity field _vϕ_ ( **a** _t_<sup>_u,_</sup><sup>**s**</sup><sup>_t, u_)bythe</sup> regression objective 


After training, action generation can be performed by starting from Gaussian noise and integrating 


from _u_ = 0 to _u_ = 1. The resulting endpoint is used as an action sampled from the learned policy. 

For LFIRL, we need not only a sampling procedure, but also a score signal for action-gradient matching. Let _pu_ ( **a** _|_ **s** _t_ ) denote the conditional density of the intermediate action **a**<sup>_u_</sup> _t_<sup>at flow time</sup><sup>_u_.</sup> Its score is 


which indicates how an intermediate action should be adjusted to move toward higher-probability expert actions under state **s** _t_ . 

Under the interpolation defined in Eq. (19), this score can be estimated from the learned velocity field. If the learned velocity is exact, then at a fixed ( **a**<sup>_u_</sup> _t_<sup>_,_</sup><sup>**s**</sup><sup>_t, u_) it estimates the conditional mean of</sup> the path derivative, 


Combining this relation with the interpolation equation gives 


For the same Gaussian path, the score of _puu_ ( **a** _|_ **s** _t_ ) can be written in terms of this conditional noise can be written in terms of this conditional noise estimate. Thus, for _u <_ 1, we obtain the Flow-Matching score estimator, we obtain the Flow-Matching score estimator 

The expression is used for _u <_ 1; at _u_ = 1, the path reaches the expert action endpoint and the denominator vanishes. In practice, the analogue of the low-noise DDPM regime is to use flow times close to, but not exactly equal to, 1. 

This gives the connection needed by LFIRL. When _u_ is close to 1, the intermediate action **a**<sup>_u_</sup> _t_<sup>is close</sup> to the initial expert action. Therefore, _gϕ_<sup>FM</sup> ( **a**<sup>_u_</sup> _t_<sup>_,_</sup><sup>**s**</sup><sup>_t, u_) estimates the local score of the expert action</sup> distribution around that action. Thus, in the low-noise regime, Eq. (3) gives 


Therefore, a Flow-Matching-based diffusion policy can be used in Stage I by replacing the DDPM score estimator _gϕ_ ( **a** _t_<sup>_k,_</sup><sup>**s**</sup><sup>_t, k_) in Eq. (8) with</sup><sup>_g_</sup> _ϕ_<sup>FM</sup> ( **a**<sup>_u_</sup> _t_<sup>_,_</sup><sup>**s**</sup><sup>_t, u_).</sup> 

16 


Figure 7: Additional ablation comparing DDPM-based and Flow-Matching-based pretraining in LFIRL. The two variants use the same subsequent sequential reward-recovery pipeline, but differ in how the pretrained generative policy is obtained. Higher is better. 

#### **B.2 Additional Results: DDPM vs. Flow Matching Pretraining** 

In the main experiments, LFIRL uses a DDPM-based diffusion policy to provide the score signal for recovering the soft _Q_ -function. We also evaluate an alternative implementation in which the diffusionpolicy pretraining stage is replaced by a Flow Matching version, while keeping the remaining LFIRL pipeline unchanged. This comparison isolates the effect of the pretrained generative policy used to provide local action-gradient supervision. 

As shown in Fig. 7, under the same number of pretraining epochs, the Flow-Matching-based variant generally performs worse than the DDPM-based variant. This suggests that, in our setting, DDPM pretraining provides a more effective score signal for the subsequent _Q_ -recovery stage. Since LFIRL relies on the pretrained generative policy to supply local action-gradient information, a weaker pretraining stage can directly reduce the quality of the recovered _Q_ -function and subsequently degrade the final recovered reward. 

### **C Sensitivity to the Reference Policy** 

The reference policy _µ_ specifies the behavioral baseline relative to which the expert policy is interpreted. Under the reference-policy MaxEnt formulation, 


We examine how the choice of _µ_ affects LFIRL by comparing a uniform reference policy with a state-conditioned Gaussian reference policy. 

The two variants use the same expert demonstrations and LFIRL training configuration. The uniform variant uses a uniform distribution over the bounded action space, for which _∇_ **a** log _µ_ ( **a** _|_ **s** ) = 0 in the interior of its support. For the Gaussian variant, we initialize an SAC actor before LFIRL training and freeze it throughout the reward-recovery pipeline. The actor outputs the mean and standard deviation of a state-conditioned action distribution and is not fitted to the expert demonstrations. At each noisy action **a**<sup>_k_</sup> _t_<sup>, we evaluate the score of this frozen reference policy and use</sup> 


as the target for _ε_<sup>_−_1</sup> _∇_ **a** _Q_<sup>ˆ</sup> **_ω_** ( **s** _t,_ **a**<sup>_k_</sup> _t_<sup>).Actions used for soft-value estimation are also sampled from the</sup> same frozen reference policy. 

We evaluate these variants on MuJoCo tasks, where the expert demonstrations can be generated by stochastic sampling from pretrained SAC experts. This allows the reference-policy comparison to be conducted with a specified source of expert actions; the generating policy distributions of the robotic-manipulation datasets cannot be verified in the same way. Table 4 reports the resulting episodic returns. 

The choice of reference policy affects performance, and the direction of the effect depends on the task. The uniform variant performs better on Swimmer and Walker2d, whereas the Gaussian 

17 

Table 4: Sensitivity to the reference policy on MuJoCo tasks. Results are episodic returns, reported as mean _±_ standard deviation. The expert return is included for context. 

|**Environment**|**LFIRL-Uniform**|**LFIRL-Gaussian**|**Expert**|
|---|---|---|---|
|Swimmer-v5|284.56_±_27.64|208.42_±_7.25|315.55_±_1.38|
|Walker2d-v5|4933.41_±_52.79|4722.40_±_230.42|5861.18_±_73.99|
|Hopper-v5|3413.50_±_210.23|3868.04_±_79.58|4098.17_±_247.70|


Table 5: Sensitivity of PointMaze success rate to Stage-I hyperparameters. Each group varies one parameter while the remaining parameters are held at their default values. Bold indicates the highest result within each parameter group for each environment. 

||**Diffus**|**ion-noise m**|**agnitude**|**Value-an i**|**choring ci**|**oefficient**|**Inten**|**ded ma**|**rgin**|
|---|---|---|---|---|---|---|---|---|---|
|**Environment**|Low|Medium|High|_λ_= 0_._5|_λ_= 1|_λ_= 2|_ξ_ = 0_._5|_ξ_ = 1|_ξ_ = 2|
|UMaze|**0.98**|0.87|0.68|0.92|**0.98**|0.97|0.57|**0.98**|0.61|
|Medium|**0.39**|0.35|0.25|0.38|**0.39**|0.35|0.24|**0.39**|0.26|
|Large|**0.31**|0.29|0.25|0.26|0.31|**0.34**|0.18|**0.31**|0.24|


variant performs better on Hopper. LFIRL therefore is not invariant to _µ_ : changing the behavioral baseline changes the reward interpretation and can alter the recovered reward. Nevertheless, the Gaussian-reference variant remains effective, showing that the recovery procedure is not restricted to the uniform-reference simplification. 

This experiment assumes that the reference policy is specified. It does not infer _µ_ from expert demonstrations. In general, demonstrations alone do not uniquely separate an unknown reference policy from the reward without additional assumptions; jointly inferring the two is beyond the scope of this work. 

### **D Sensitivity to Stage-I Hyperparameters** 

LFIRL has several sequential recovery stages, but their hyperparameters need not have the same effect on performance. The value-recovery stage uses a Gumbel-regression-style objective, while the final reward-recovery stage enforces Bellman consistency. Here, we focus on three choices that directly affect the local _Q_ -recovery signal in Stage I: the magnitude of the diffusion noise, the value-anchoring coefficient _λ_ , and the intended margin _ξ_ in value anchoring. 

We vary one parameter at a time while holding the other two at their default settings: the low-noise schedule, _λ_ = 1, and _ξ_ = 1. The noise settings scale the coefficient<sup>_~~√~~_</sup> 1 _− α_ ¯ _k_ in the forward noising process by 1 _×_ , 4 _×_ , and 8 _×_ , respectively. Table 5 reports PointMaze success rates under these settings. 

**Diffusion-noise magnitude.** Performance decreases as the noise coefficient increases. Increasing _~~√~~_ 1 _− α_ ¯ _k_ moves noisy actions farther from the clean expert-action distribution, where the local approximation between the noisy-action score and the expert-policy score becomes less reliable. The decline is modest from low to medium noise on Medium and Large, but larger at high noise across all three environments. This supports using the low-noise schedule as the default for local _Q_ -gradient supervision. 

**Value-anchoring coefficient** _λ_ **.** Performance is comparatively stable between _λ_ = 1 and _λ_ = 2. Increasing _λ_ to 2 slightly improves Large while causing a small decrease on UMaze and Medium. Reducing it to 0 _._ 5 weakens the anchoring signal and lowers performance, particularly on Large. Thus, the method is less sensitive to this coefficient once anchoring is sufficiently strong, with _λ_ = 1 providing a stable choice across the three environments. 

**Intended margin** _ξ_ **.** The intended margin has the strongest effect among the three tested parameters. Both _ξ_ = 0 _._ 5 and _ξ_ = 2 underperform _ξ_ = 1 on every environment. A small margin provides 

18 

insufficient separation between expert actions and their perturbed neighbors. An excessively large margin demands larger local _Q_ differences and may conflict with gradient matching or suppress near-optimal actions. In these experiments, _ξ_ = 1 provides the most reliable balance across all three environments. 

Overall, these results identify the diffusion-noise magnitude and the anchoring margin as the more consequential Stage-I settings. The value-anchoring coefficient is less sensitive once it is large enough to provide effective anchoring. 

### **E Additional Experimental Details** 

#### **E.1 Implementation Details and Hyperparameter Setup** 

The overall training procedure of LFIRL is given in Alg. 1. Key network architecture and hyperparameter settings for each environment are summarized in Tab. 6 and Tab. 7. 

Table 6: Network architecture and hyperparameter setup for the PointMaze environments. 

||PointMaze_UMaze-v3|PointMaze_Medium-v3|PointMaze_Large-v3|
|---|---|---|---|
|Expert demonstrations|2000|2000|2000|
|Policy pretraining epochs|60|40|40|
|Q/_b_/V/_r_learning rate|3e-5|3e-5|3e-5|
|Stage passes(_Q, b, V, r_)|8/8/20/20|8/8/20/20|8/8/20/20|
|Q,_b_, V,_r_hidden layers|256, 256, 256, 256|256, 256, 256, 256|256, 256, 256, 256|
|IRL batch size|256|256|256|
|Discount factor_γ_|0.99|0.99|0.99|
|EMA coefficient_τ_|0.005|0.005|0.005|


Table 7: Network architecture and hyperparameter setup for the robotic manipulation environments. 

||FrankaKitchen-v1|gym_pusht/PushT-v0|AdroitHandPen-v1|
|---|---|---|---|
|Expert demonstrations|19|200|200|
|Policy pretraining epochs|20|200|40|
|Q/_b_/V/_r_learning rate|3e-5|3e-4|3e-5|
|Stage passes(_Q, b, V, r_)|8/8/20/20|40/40/100/100|40/40/100/100|
|Q,_b_, V,_r_hidden layers|256, 256, 256, 256|256, 256, 256, 256|256, 256, 256, 256|
|IRL batch size|256|256|256|
|Discount factor_γ_|0.99|0.99|0.99|
|EMA coefficient_τ_|0.005|0.005|0.005|


#### **E.2 Expert Demonstrations Sources** 

The sources of offline trajectory datasets for experts are provided in Tab. 8. In Maze and Kitchen tasks, we directly use the expert trajectories from the Minari Offline Reinforcement Learning datasets [44]. For the Push-T task, we use the expert trajectories from the dataset in Diffusion Policy [5]. 

Table 8: The sources of expert policies or demonstrations. 

|Task|Source||
|---|---|---|
|UMaze|`https:/`|`/minari.farama.org/datasets/D4RL/pointmaze/umaze-v2/`|
|Medium|`https:/`|`/minari.farama.org/datasets/D4RL/pointmaze/medium-v2/`|
|Large|`https:/`|`/minari.farama.org/datasets/D4RL/pointmaze/large-v2/`|
|Franka Kitchen|`https:/`|`/minari.farama.org/datasets/D4RL/kitchen/complete-v2/`|
|Push-T|`https:/`|`/diffusion-policy.cs.columbia.edu/data/training/pusht.zip`|
|Pen|`https:/`|`/minari.farama.org/datasets/D4RL/pen/expert-v2/`|


19 

#### **E.3 Hardware Information** 

Hardware specifications are provided in Tab. 9. 

Table 9: Hardware configuration used in experiments. 

|Hardware|Specifications|
|---|---|
|CPU|AMD EPYC 7713 64-Core Processor @ 2 GHz|
|GPU|NVIDIA A100-SXM4-80GB @ 1215 MHz|
|Memory|2 TB|


20 

