---
title: "$λ$-Reachability: Geometric-Horizon Safety Bellman Equations for Humanoid Safety"
date: "2026-06-14"
authors: "Rui Chen; Shangtao Li; Yifan Sun; Changliu Liu"
url: https://arxiv.org/abs/2606.16022
pdf: https://arxiv.org/pdf/2606.16022
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.16022)** / [論文ページ](https://arxiv.org/abs/2606.16022)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# _λ_ **-Reachability: Geometric-Horizon Safety Bellman Equations for Humanoid Safety** 

### **Rui Chen** 

Robotics Institute Carnegie Mellon University United States ruic3@andrew.cmu.edu 

**Shangtao Li** Mechanical Engineering Carnegie Mellon University United States shangtal@andrew.cmu.edu 

### **Yifan Sun** 

Robotics Institute Carnegie Mellon University United States yifansu@andrew.cmu.edu 

**Changliu Liu** Robotics Institute Carnegie Mellon University United States cliu6@andrew.cmu.edu 


Figure 1: Safety value inference on hardware. A safety value _V_<sup>_π_</sup> is learned to predict the state-wise worstover-future safety signal _ℓ_ , which models collision avoidance in task (a,c) and stable locomotion in task (b,d). The frame _t_<sup>ˆ</sup> unsafe when _V_<sup>_π_</sup> predicts the first non-recoverable state (orange) and frame _t_ unsafe when the actual unsafe condition occurs (red) are both marked. The gap between _t_<sup>ˆ</sup> unsafe and _t_ unsafe is the predictive horizon of _V_<sup>_π_</sup> for unsafe states. The headlight turns red at _t_<sup>ˆ</sup> unsafe when _V_<sup>_π_</sup> predicts future safety violations. 

**Abstract:** We introduce _λ-Reachability_ , a scalable approach to Hamilton–Jacobi safety analysis for high-dimensional robotic systems. Unlike prior discounted formulations that rely on fixed one-step Bellman updates, _λ_ -Reachability employs a _stochastic multi-step estimator_ of the safety value, using a geometrically distributed rollout horizon together with a randomly absorbed terminal. Conceptually analogous to TD( _λ_ ), _λ_ -Reachability interpolates between local self-consistency updates and long-horizon max-over-trajectory safety targets via an interpretable horizon-control parameter. Unlike TD( _λ_ ), where the terminal value is always incorporated in learning targets, the terminal safety value in _λ_ -Reachability is only used at a probability controlled by parameter _δ_ . We formally show that for _δ <_ 1, the update induces a contraction mapping that allows temporal-difference learning; as _λ →_ 1, the estimator recovers the undiscounted reachability objective. We apply _λ_ -Reachability to high-dimensional safety learning problems with both simulated and real humanoid robots under balance and collision avoidance constraints. Experimental results demonstrate that _λ_ -Reachability significantly improves both safe-set boundary classification and safety margin estimation compared to single-step temporal-difference baselines. 

**Keywords:** Reachability Analysis, Reinforcement Learning, Humanoids 

## **1 Introduction** 

Robots operating in the real world must reason about _persistent_ safety: whether a policy will ever violate constraints, and how close it is to doing so. A common formalization uses an instantaneous safety signal, with its positivity indicating a violation, and defines a policy’s safety value as the worst future signal. Hence, the safety value certifies safety for all future time, with the sign indicating whether persistent safety is reachable and the magnitude acting as a safety margin. This worst-overtime notion is widely used as the foundational quantity for safety assessment [1]. 

Based on the safety assessment, a wide range of work focuses on _safe control_ : producing actions that comply with safety constraints. Safe set algorithms (SSA) [2, 3] and control barrier functions (CBF) [4, 5] provide an optimization-based framework to enforce forward invariance within a safe set while retaining task performance. Hamilton-Jacobi (HJ) reachability-based methods [6, 1] recover the safety value by solving a variational inequality via dynamic programming. Those safe control approaches have been applied to real-world applications such as quadruped navigation [7, 8], collaborative manipulation [9], and autonomous driving [10]. To ultimately achieve safe control, the correctness of the safety value—both the sign indicating safety and the magnitude encoding safety margin—is an essential prerequisite, as it directly quantifies the safety performance. Only with accurate safety values, one is able to derive appropriate safe control operations, such as activating failure-recovery policies based on safety margins [11] and applying safe control constraints based on value gradients [12, 8]. Hence, this work focuses on acquiring accurate safety values for policies as a critical step in safety analysis and control. 

Prior work that explicitly _synthesizes_ or _learns_ the underlying safety value with formal structure is often limited to relatively low-dimensional state descriptions. Safety Index Synthesis constructs a safety index by solving sum-of-squares (SOS) programs [13, 12, 14], but SOS formulations rely on semi-definite optimization whose size grows rapidly with state dimension and polynomial degree, leading to poor scalability [15]. Neural CBF learning methods aim to fit barrier functions from data [16], but unlike SOS- or PDE-based constructions whose constraints hold by design, learned neural barrier functions must satisfy barrier inequalities over a continuous state space; since training typically enforces these conditions only on sampled states, additional verification is required to establish safety guarantees [17, 18]. Similarly, HJ reachability computes a viscosity solution of the HJ (variational inequality) PDEs on a grid. However, standard solvers suffer from the curse of dimensionality—memory and computation scale exponentially with state dimension [19, 20]. These limitations are calling for new methods to learn safety value functions that can operate directly in high-dimensional robotic and perceptual representations. 

To address the issue of high dimensionality, several works reformulate safety problems through _discounted_ safety Bellman operators that admit contraction properties. This enables the use of reinforcement learning techniques, such as TD/Q-learning with function approximation [21, 22], to learn safety values from data. Ganai et al. [23] learns reachability estimators to support safe policy optimization, while Ganai et al. [1] summarizes the growing connections between HJ reachability and reinforcement learning. Notably, all existing works build on the safety Bellman equation with a one-step bootstrapped value target. In high-dimensional settings with rich perception (e.g., height maps) and complex environment dynamics, one-step bootstrapping can be unstable since approximation errors can be propagated through noisy transitions. The value learning can also be slow, since future safety information propagates by only one step per update. To avoid these drawbacks, one may consider removing bootstrapping entirely and learning from Monte Carlo-style targets instead. However, that requires full task trajectories, which can be costly to collect in high-dimensional realworld environments. It is also desirable to learn safety values while the system is in operation, instead of waiting for full rollouts which defers learning. In summary, we aim to efficiently learn safety value functions that accurately identify feasible boundaries and estimate safety margins, even from partial trajectory data. 

Motivated by these challenges, we propose _λ-Reachability_ , a TD( _λ_ )-style approach [24] for safety value learning that replaces sensitive one-step backups with a geometric mixture of multi-step max 

2 

targets. By sampling a random rollout horizon and backing up the maximum observed safety signal over that horizon, _λ_ -Reachability interpolates smoothly between short-horizon bootstrapping and Monte Carlo max targets, while providing an explicit knob ( _λ_ ) that controls the effective lookahead horizon. Instead of deterministically bootstrapping from the current safety value estimate, we do so only with a probability _δ_<sup>_n_</sup> that decreases as the look-ahead horizon _n_ extends. We formally prove that the resulting stochastic multi-step safety Bellman equation induces a contraction mapping when _δ <_ 1, thereby allowing temporal-difference solutions and recovering the undiscounted safety value in expectation as _λ →_ 1. We also interpret our approach as a connection between CBF and HJ-based approaches in terms of safety value learning. Finally, _λ_ -Reachability is applied to high-dimensional robotic tasks using perceptual observations to recover safety values for balance and collision-avoidance constraints. Results in both simulations and on physical hardware show improved boundary and margin accuracy compared to one-step baselines. 

## **2 Background** 

### **2.1 Safety Value Functions for Control Policies** 

Let _x ∈X_ be the system state and _u ∈U_ the control. During operation, the system should never enter unsafe states such as collisions and off-balance poses. We assume that such a constraint is specified through a _safety signal ℓ_ : _X →_ R, which defines a safe set we wish the system to stay in _XS_ := _{x ∈X | ℓ_ ( _x_ ) _≤_ 0 _}._ Given a control policy _π_ : _X →U_ , let _τx_<sup>_π_denote the infinite-horizon</sup> state trajectory induced by _π_ starting from _x_ . If _ℓ_ ( _τx_<sup>_π_(</sup><sup>_t_))</sup><sup>_≤_0forall</sup><sup>_t_,</sup><sup>_τ_</sup> _x_<sup>_π_issafeandthepolicy</sup> induces a forward invariant set [13] within _XS_ . This work aims to synthesize a safety value function _V_<sup>_π_</sup> : _X →_ R that quantifies the future safety performance of _π_ for any _x ∈X_ , defined as 


It follows that _{x | V_<sup>_π_</sup> ( _x_ ) _≤_ 0 _}_ is a forward invariant set within _XS_ . By definition, (1) also satisfies the _safety Bellman equation_ : 


### **2.2 The Discounted Safety Bellman Equation** 

Exact synthesis of the value function (1) has proven intractable for higher dimension problems either by Sum-of-Square programming [25, 13] or solving Hamilton- Jacobi-Bellman variational inequality [1]. Unlike standard reward-based Bellman equations, (2) does not induce a contraction mapping, which makes it unsuitable to derive a learning target directly [21]. To address this issue, Fisac et al. [21] introduces a _γ_ -discounted formulation of the safety objective. For a discount factor _γ ∈_ (0 _,_ 1), the _discounted safety Bellman equation_ is defined as 


where _γ_ can be interpreted as an episode continuing probability. This equation induces a contraction mapping under the supremum norm and admits a unique fixed point. Moreover, as _γ →_ 1, the solution _V_<sup>_π_</sup> to (3) recovers the original undiscounted safety value in (1). Concretely, the learning is carried out by regressing _V_<sup>_π_</sup> ( _xt_ ) towards sampled targets _yt_ : 


where _k_ is the training step and _α_ is the learning rate. The target _yt_ is given by 


with _γ_ annealed to 1 during training. Hence, (3) is suitable for being used with temporal-difference techniques to provide a tractable way to synthesize safety value functions [21]. 

3 

## **3 Stochastic Multi-step Safety Bellman Equation** 

### **3.1 Unifying Max Backups with Variable Horizon** 

Notice that the original safety objective in (1) is defined over an infinite horizon, whereas the update rule in (4) relies on a one-step bootstrap target at the successor state _xt_ +1. As a result, the regression target _yt_ is strongly influenced by the current approximation of _V_<sup>_π_</sup> ( _xt_ +1), which is typically inaccurate during early stages of training. This induces substantial bias in the learning signal and can lead to error propagation through repeated bootstrapping. Moreover, such myopic updates are inefficient at propagating safety information backward in time when unsafe events occur many steps after _t_ . Similar limitations of one-step updates are well documented in the reinforcement learning literature for classic one-step temporal-difference (TD) methods [24]. 

At the opposite end of the spectrum, Monte-Carlo methods avoid bootstrapping altogether by constructing targets directly from fully observed trajectories. In the context of safety value learning, this corresponds to the target _yt_ = max _{ℓt, ℓt_ +1 _, . . . , ℓT }_ where _T_ denotes the terminal time step. Monte-Carlo targets are unbiased with respect to the infinite-horizon objective (1) and provide accurate supervision when full trajectories are available. However, they typically exhibit high variance, require complete rollouts, and cannot always be computed until termination. These properties make Monte-Carlo supervision impractical for high-dimensional systems and incompatible with online learning settings, where only partial trajectory segments may be accessible. 

Motivated by the complementary strengths and weaknesses of one-step bootstrapping and MonteCarlo evaluation, our core contribution is to unify learning from max targets with different bootstrap horizons for safety value functions. Specifically, we propose a variant of safety Bellman equation with a geometric stopping horizon and stochastic terminal absorption. The equation smoothly interpolates between short-horizon bootstrapping and long-horizon Monte-Carlo supervision. Specifically, given state _xt_ , a continuation probability _λ ∈_ [0 _,_ 1) and a terminal survival constant _δ ∈_ [0 _,_ 1), we define the following _stochastic multi-step safety Bellman equation_ 


where the stochastic bootstrapped value is given by 


The stopping step _n ≥_ 1 follows a geometric distribution _n ∼_ Geom(1 _− λ_ ) given by 


The terminal survival event _s ∼_ Bernoulli( _δ_<sup>_n_</sup> ) bootstraps on the current value estimation with a probability that decreases as the horizon grows. _v_ term is a lower bound of _ℓ_ so that when _s_ = 0, the bootstrapped value at _t_ + _n_ is effectively ignored. Importantly, although (6) does not explicitly include a discount factor, it induces a contraction mapping which allows temporal-difference approaches to converge to a fixed point. As _λ →_ 1, (6) also converges to the undiscounted objective (1). To show those, we first define the stochastic multi-step safety Bellman operator 


We then present the theoretical results as follows. See Appendix A for proof. 

**Theorem 1** (Contraction Mapping) **.** _The stochastic multi-step safety Bellman equation induces a contraction mapping under the supremum norm for λ ∈_ [0 _,_ 1) _and δ ∈_ [0 _,_ 1) _. Namely, for V, V_<sup>˜</sup> : _X →_ R _, there exists a constant ρ ∈_ [0 _,_ 1) _such that ∥Tλ,δ_ [ _V_ ] _− Tλ,δ_ [ _V_<sup>˜</sup> ] _∥∞ ≤ ρ∥V − V_<sup>˜</sup> _∥∞._ **Proposition 1** (Value Approximation) **.** _In the limit of λ →_ 1 _, the fixed-point solution to_ (6) _converges to the undiscounted safety value_ (1) _._ 

Hence, (6) has a unique fixed-point (by Theorem 1) which solves the objective (1) as _λ →_ 1 (by Proposition 1). These properties justify the learning of _V_<sup>_π_</sup> by regression towards 


4 

which is a stochastic multi-step estimator that integrates safety signals observed along the trajectory segment while retaining the ability to bootstrap from the current value approximation at the stopping state. We refer to this learning procedure as _λ-Reachability_ , in analogy to TD( _λ_ ) methods for cumulative rewards. Notably, the bootstrap horizon _n_ above is unbounded, whereas in practice we only have access to finite-length policy rollouts. Hence, for practical implementation, we instead sample _n_ from a truncated geometric distribution. See Appendix B for full training implementations. 

### **3.2 Interpretations** 

**Explicit Safety Horizon.** The expected stopping length is E[ _n_ ] = 1 _−_ <u>1</u> _λ_<sup>which increases monoton-</sup> ically as _λ →_ 1. _λ_ provides an explicit mechanism for tuning the safety horizon: smaller values emphasize near-term safety, while larger values aggressively propagate long-horizon safety information. This control can be particularly useful when different notions of safety prediction are needed. 

**Relation to Discounted Safety Bellman.** Two properties must hold to allow temporal-difference learning: (i) a unique fixed point induced by a contraction for training stability and (ii) consistency with the true safety value for value approximation accuracy. While both (3) and (6) satisfy these conditions, they differ fundamentally in how contraction is induced. The discounted Bellman induces contraction via explicit value discounts (3), requiring _γ <_ 1. Meanwhile, accurate value approximation is achieved in the limit _γ →_ 1 [21]. Hence, the training stability and approximation accuracy are inherently coupled. In contrast, _λ_ -Reachability (6) incorporates the bootstrapped value with probability _δ_<sup>_n_</sup> , inducing a contraction mapping as long as _δ <_ 1. The value approximation accuracy is determined by a different parameter _λ_ . Such decoupling allows one to improve value accuracy by annealing _λ_ to 1, while maintaining contraction and training stability by _δ <_ 1. 

**Relation to CBF and HJ.** For safety value learning, CBF–based approaches [16] directly exploit invariance labels that encode infinite-horizon safety, consistent with (1). These methods learn the persistent safety, but do not explicitly model how safety information propagates across timesteps. In contrast, HJ reachability approaches [1] rely on one-step self-consistency conditions (2) and propagate safety information through bootstrapping. While effective, purely local updates can be slow in high-dimensional settings. In this regard, _λ_ -Reachability unifies these two paradigms via observing future safety signals with a stochastic look-ahead horizon, and interpolating between global invariance supervision and local HJ consistency. From (6), one can recover CBF learning by fixing _s_ = 0 and using trajectory-specific horizons _n_ , and recover HJ learning by fixing _s_ = 1 and _n_ = 1. 

## **4 Experiments** 

### **4.1 Tasks** 

**1) Policy training.** Given a task, we first train a policy _π_ using task-specific objectives (e.g., velocity tracking). Note that a safety value can be learned for an arbitrary policy. 

**2) Policy rollout.** Given _π_ , we collect a set of finite-length rollouts _{τ_<sup>_π_</sup> _}_ from the safety value learning environment. To collect unsafe scenarios, we sample a random event that perturbs the robot towards unsafe regions at the start of each episode. If the episode ends in a safe state, the robot is assumed to remain safe with a sufficiently trained policy. This enables us to label infinite-horizon safety metrics (i.e., signs and safety margins) from finite trajectories for evaluation. In practice, such an assumption may not hold, making safety labels empirical estimates that can be biased. 

**3) Safety labeling.** For each state _xt ∈ τ_<sup>_π_</sup> , we first compute the safety signal _ℓ_ ( _x_ ). Then, we define the forward-invariance indicator _ct_ ≜ **1** _{ℓ_ ( _xk_ ) _≤_ 0 _, ∀k ≥ t}_ . Since rollouts are finite, _ct_ serves as the best available estimate of forward invariance, rather than the true infinite-horizon label. Second, we define the empirical safety value _V_<sup>¯</sup><sup>_π_</sup> ( _xt_ ) ≜ max _k≥t ℓ_ ( _xk_ ). The resulting dataset is _D_ ≜ _{_ ( _xt, ℓt, ct, V_<sup>¯</sup><sup>_π_</sup> ( _xt_ )) _}t_ . Tasks used in this work are defined below. See Figure 2 for visualizations. 

**G1FLAT** . We train a locomotion policy _π_ for a Unitree G1 humanoid robot with 37 DoF in a flat environment with velocity-tracking goals. In this task, we consider a safety signal _ℓ_ flat to indicate the balance status, defined by both root height and body orientation. 

5 


Figure 2: Humanoid safety value tasks. The safety signal _ℓ_ is indicated by the ball color, with green indicating safe states ( _ℓ ≤−_ 0 _._ 5), yellow indicating near violations ( _ℓ ∈_ ( _−_ 0 _._ 5 _,_ 0]), and red indicating safety violations ( _ℓ>_ 0). The predicted safety value _V_ is indicated by the higher ball with the same color coding. 


Figure 3: Training curves for safety value functions in different safety tasks. The top row shows the sample value error _eV_ during training, while the bottom row shows the invariant state classification accuracy. 

**G1ROUGH** . This task replaces the flat ground in G1Flat with rough terrains with slopes and stairs with scan points as additional input. Other settings remain the same. 

**G1COLLISION** . This task builds on G1FLAT and introduces dynamic obstacles that the robot must avoid while navigating. To calculate the safety signal _ℓ_ collision, we introduce a distance component _ℓ_ dist = min _{_ max _{_ ( _d_ min _− d_ ) _/d_ min _, −_ 1 _},_ 0 _}_ and a contact component _ℓ_ contact = 1 if the ball hits the robot and _−_ 1 otherwise. Hence, we have _ℓ_ collision = max _{ℓ_ flat _, ℓ_ dist _, ℓ_ contact _}_ . 

See Appendix C for full environment setup, policy training, and data collection details. 

### **4.2 Ablations and Baselines** 

_λ_ -Reachability is trained by regressing towards the geometric-horizon targets (10) by minimizing 


via gradient descent with a learning rate of _α_ = 1 _e −_ 3 for 2000 steps. _λ_ is set to 0 _._ 99. To examine the effect of _λ_ value, we deploy ablations by setting alternative _λ_ values in _{_ 0 _._ 95 _,_ 0 _._ 5 _,_ 0 _._ 0 _}_ . We also compare _λ_ to other baselines that recover the safety value (1). 

**Discounted Policy Evaluation (DPE)** . DPE [21] recovers _V_<sup>_π_</sup> by regressing towards the discounted safety Bellman target (3). The discount factor _γ_ is initialized to 0 _._ 5 and annealed to 1 _._ 0 during training. This serves as the main baseline which _λ_ -Reachability builds on. 

**Supervised (SV)** . SV fits the estimated safety value _V_<sup>¯</sup><sup>_π_</sup> ( _xt_ ). This represents the optimum in highly controlled tasks. In general, it is difficult to identify “events” and segment trajectories into finite episodes that capture infinite-horizon safety. Labels from partial trajectories would be biased. Hence, SV is considered a miracle baseline for evaluation only, rather than a practical method. 

6 

Table 1: Inference results (mean _±_ std) in simulation. Supervised is marked as the miracle baseline. Best values among non-miracle methods are shown in bold. 

|||G1FLAT|||G1ROUGH||G|1COLLISION||
|---|---|---|---|---|---|---|---|---|---|
|**Method**|_r_temp (%)|_e_V|_r_FPR (%)|_r_temp (%)|_e_V|_r_FPR (%)|_r_temp (%)|_e_V|_r_FPR (%)|
|_λ_(ours)|**99.98**_±_**0.21**|**0.09**_±_**0.19**|**0.21**|**97.92**_±_**9.24**|**0.08**_±_**0.22**|**6.49**|**99.40**_±_**4.79**|0.13_±_0.23|**6.12**|
|_λ_(0_._95)|99.97_±_0.29|0.11_±_0.23|0.38|96.43_±_11.34|0.09_±_0.25|9.23|98.63_±_5.96|**0.12**_±_**0.20**|9.15|
|_λ_(0_._5)|56.52_±_20.39|0.71_±_1.23|31.91|52.40_±_27.65|0.27_±_0.64|45.45|44.80_±_18.28|0.16_±_0.33|48.02|
|_λ_(0_._0)|26.39_±_14.09|1.00_±_1.65|47.42|21.97_±_19.06|0.39_±_0.88|60.17|23.85_±_14.53|0.18_±_0.38|59.63|
|DPE|22.05_±_12.30|1.04_±_1.70|49.31|21.94_±_16.66|0.40_±_0.89|59.68|22.61_±_14.50|0.18_±_0.37|60.47|
|Supervised|99.99_±_0.33|0.05_±_0.13|0.09|99.35_±_6.29|0.09_±_0.17|2.71|99.72_±_2.60|0.14_±_0.27|2.05|


### **4.3 Metrics** 

For each state, the safety value function _V_<sup>_π_</sup> should correctly reveal both (a) whether the system will stay safe and (b) the current safety margin. When applied as a safety monitor, _V_<sup>_π_</sup> should alarm about future unsafe states as early as possible. That leads to the following metrics. 

**Temporal Recall** _r_ temp is the ratio of the predictive horizon for unsafe states over the maximal possible horizon: _r_ temp = E _τ π_ [max(0 _, t_ unsafe _− t_<sup>ˆ</sup> unsafe) _/_ ( _t_ unsafe _− t_ 0)] where _t_ unsafe, _t_<sup>ˆ</sup> unsafe are the earliest timestep when _ℓ_ , _V_<sup>_π_</sup> ( _xt_ ) _≥_ 0. _r_ temp = 1 indicates the optimal value. 

**Sample Value Error** _e_ V is the mean squared error _e_ V = E _xt∼τ_<sup>_π_</sup> _|V_<sup>_π_</sup> ( _xt_ ) _− V_<sup>¯</sup><sup>_π_</sup> ( _xt_ ) _|_<sup>2</sup> . 

**Sample False Positive Rate** _r_ FPR indicates the chances that _V_<sup>_π_</sup> misclassifies a non-invariant state _r_ FPR = _p_ ( _V_<sup>_π_</sup> ( _xt_ ) _≤_ 0 _| ct_ = 0). 

### **4.4 Quantitative Results in Simulation** 

We summarize the training results in Figure 3 and present evaluations in Table 1. See Appendix C for implementation details. Notably, G1FLAT is already a challenging safety value learning problem, with substantially higher state dimensionality than prior benchmarks [13, 1]. G1ROUGH further increases the complexity through height-map perception, while G1COLLISION is challenging in safety reasoning with multiple constraints. 

**Baselines** . From Figure 3, we see that _λ_ -Reachability quickly reduces the safety value prediction error and improves the invariance classification accuracy. The performance converges to that of the miracle baseline, showing that _λ_ -Reachability is able to learn near-optimal safety value even with partial trajectories. On the other hand, discounted policy evaluation (DPE) has trouble in improving both metrics. Since DPE relies on fixed one-step updates (3), the propagation of unsafe events can be slow and cause inefficient learning in high-dimensional tasks. The above gap is also pronounced in Table 1 where _λ_ -Reachability shows significant advantage over DPE in early warning of impending safety violations, accurate safety margins and rare false positives. With those, _λ_ -Reachability validates as an efficient and reliable approach to high-dimensional safety value learning. 

**Ablations** . From both Figure 3 and Table 1, we see that the choice of _λ_ has a major impact on the performance. With _λ_ = 0 _._ 99, _λ_ -Reachability achieves near-optimal safety learning across all tasks, matching the performance of the miracle baseline. As _λ_ decreases, the expected bootstrap horizon drops according to Section 3.2, e.g., 20 steps at _λ_ = 0 _._ 95 and 2 steps at _λ_ = 0 _._ 5. That quickly degrades the performance until it matches the performance of DPE at _λ_ = 0. This agrees with the fact that with _λ_ = 0, the horizon sampling (8) becomes deterministic and always samples 1, effectively reducing the target (10) to the one-step baseline (5) with _γ_ = 1. Hence, we confirm that local bootstrapping cannot reliably propagate future safety violations, especially when safetyrelevant events occur far from the current state. 

### **4.5 Hardware Experiments** 

We perform G1FLAT and G1COLLISION tasks on a real Unitree G1 humanoid. _V_<sup>_π_</sup> is learned in simulation and applied to physical rollout data. To perturb the safety signal, we push the robot 

7 

Table 2: Hardware inference results (mean _±_ std) on real G1FLAT and G1COLLISION tasks. 

|||G1FLAT||G|1COLLISION||
|---|---|---|---|---|---|---|
|**Method**|_r_temp (%)|_e_V|_r_FPR (%)|_r_temp (%)|_e_V|_r_FPR (%)|
|_λ_(ours)|80.91_±_4.96|**0.19**_±_**0.15**|20.31|**73.59**_±_**9.20**|0.48_±_0.25|**30.54**|
|_λ_(0_._95)|82.24_±_10.15|0.21_±_0.16|20.31|72.09_±_9.13|**0.47**_±_**0.25**|31.83|
|_λ_(0_._5)|**84.26**_±_**11.78**|0.24_±_0.14|**18.77**|48.78_±_27.09|0.58_±_0.33|48.35|
|_λ_(0_._0)|74.25_±_22.35|0.26_±_0.19|31.80|41.29_±_23.66|0.66_±_0.39|53.99|
|DPE|62.07_±_19.42|0.44_±_0.32|45.21|13.52_±_6.97|0.75_±_0.52|72.20|
|Supervised|84.42_±_13.26|0.27_±_0.26|19.92|79.63_±_9.67|0.48_±_0.33|23.21|


in G1FLAT and throw balls at the robot in G1COLLISION where the robot and ball are tracked using a mocap system. We summarize results in Table 2. _λ_ -Reachability stably outperforms the DPE baseline, and matches the performance of the miracle baseline with proper hyperparameters. Results on the G1COLLISION task show trends similar to those in the previous section. For G1FLAT, however, _λ_ -Reachability with high _λ_ values shows less advantage, with top scores at _λ_ = 0 _._ 5. One potential cause is that _V_<sup>_π_</sup> in G1FLAT relies entirely on noisy, real proprioceptive signals. _λ_ trained in simulation with longer bootstrap horizons (i.e., larger _λ_ ) relies on predictable future trajectories, which are rare in practice. _λ_ with shorter horizons leans more on the near-term signal and is more robust under distribution shift. In G1COLLISION, although the same noises exist, the safety values largely depend on the obstacle, whose trajectories are smooth and predictable thanks to the mocap system. See Appendix C for training details and Appendix D for additional results. 

## **5 Limitations** 

We identify two aspects where future work would benefit. First, safety value learning requires infinite-horizon trajectories to be sampled, since the horizon is essentially unbounded (see (8)). In practice, however, policy rollouts are finite with truncated horizon sampling (see (13)). Hence, practical _λ_ learning can be biased. It is thus beneficial to derive a max-horizon-dependent term as future work to quantify the learning bias with truncated bootstrap horizons. Another aspect regards the tradeoff between bias and robustness. As shown previously, noisy real data can introduce distributional shifts that degrade the performance of long-horizon _λ_ values. On the other hand, the solution to (6) is unbiased only when _λ_ anneals to 1. Consequently, _λ_ values closer to 1 reduce bias while making the learned value less robust against noisy online input. A principled approach to the bias-robustness tradeoff would be beneficial for applying _λ_ in general conditions. 

## **6 Discussions and Conclusions** 

In this paper, we proposed _λ_ -Reachability, a safety value learning approach that solves the safety Bellman equation using a geometric mixture of multi-step max backups. _λ_ -Reachability induces both a contraction mapping and unbiased safety value approximation under mild conditions, enabling scalable and efficient temporal-difference learning approaches. Experiments across multiple value learning problems demonstrate that _λ_ -Reachability consistently outperforms the baseline, addressing the issue of slow information propagation inherent to one-step bootstrapping in highdimensional settings. Although this work focuses on policy evaluation and does not derive a control policy, it can be directly integrated into existing reinforcement learning frameworks to enable safetyaware learning. For instance, _λ_ -Reachability can replace value learning in actor–critic methods (e.g., TD3, SAC), yielding actor updates that explicitly maximize safety. This improves upon prior actor– critic-based safety approaches such as [9], in which value functions need only be correct up to a partial order. Crucially, safety-maximizing actor-critics rely on accurate value scales to determine the feasibility of actions and will therefore benefit from the accurate safety margins of _λ_ . Similarly, _λ_ can be used in policy optimization (e.g., TRPO, PPO) by replacing value targets with geometrichorizon max targets (10), similar to [21]. Hence, while _λ_ -Reachability focuses on policy evaluation, it provides a principled approach to learning high-dimensional safety values, which is beneficial across a broad class of safe policy learning problems. 

8 

## **References** 

- [1] M. Ganai, S. Gao, and S. L. Herbert. Hamilton-jacobi reachability in reinforcement learning: A survey. _IEEE Open Journal of Control Systems_ , 3:310–324, 2024. 

- [2] C. Liu and M. Tomizuka. Control in a safe set: Addressing safety in human-robot interactions. In _Dynamic Systems and Control Conference_ , volume 46209. American Society of Mechanical Engineers, 2014. 

- [3] R. Liu, R. Chen, and C. Liu. Safe interactive industrial robots using jerk-based safe set algorithm. _arXiv preprint arXiv:2204.03038_ , 2022. 

- [4] A. D. Ames, S. Coogan, M. Egerstedt, G. Notomista, K. Sreenath, and P. Tabuada. Control barrier functions: Theory and applications. In _2019 18th European Control Conference (ECC)_ , 2019. doi:10.23919/ECC.2019.8796030. 

- [5] H. Wang, J. Peng, J. Xu, F. Zhang, and Y. Wang. High-order control barrier functions-based optimization control for time-varying nonlinear systems with full-state constraints: A dynamic sub-safe set approach. _International Journal of Robust and Nonlinear Control_ , 33(8):4490– 4503, 2023. 

- [6] J. F. Fisac, A. K. Akametalu, M. N. Zeilinger, S. Kaynama, J. Gillula, and C. J. Tomlin. A general safety framework for learning-based control in uncertain robotic systems. _IEEE Transactions on Automatic Control_ , 64(7):2737–2752, 2019. doi:10.1109/TAC.2018.2876389. 

- [7] K.-C. Hsu, A. Z. Ren, D. P. Nguyen, A. Majumdar, and J. F. Fisac. Sim-to-lab-to-real: Safe reinforcement learning with shielding and generalization guarantees. _Artificial Intelligence_ , 314:103811, 2023. 

- [8] K. S. Yun, R. Chen, C. Dunaway, J. M. Dolan, and C. Liu. Safe control of quadruped in varying dynamics via safety index adaptation. _arXiv preprint arXiv:2409.09882_ , 2024. 

- [9] R. Pandya, C. Liu, and A. V. Bajcsy. Robots that learn to safely influence via predictioninformed reach-avoid dynamic games. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. doi:10.1109/ICRA55743.2025.11128803. URL https:// arxiv.org/abs/2409.12153. arXiv:2409.12153. 

- [10] K. Leung, E. Schmerling, M. Zhang, M. Chen, J. Talbot, J. C. Gerdes, and M. Pavone. On infusing reachability-based safety assurance within planning frameworks for human–robot vehicle interactions. _The International Journal of Robotics Research_ , 39(10-11):1326–1345, 2020. 

- [11] T. He, C. Zhang, W. Xiao, G. He, C. Liu, and G. Shi. Agile but safe: Learning collision-free high-speed legged locomotion. _arXiv preprint arXiv:2401.17583_ , 2024. 

- [12] R. Chen, W. Zhao, R. Liu, W. Zhang, and C. Liu. Real-time safety index adaptation for parameter-varying systems via determinant gradient ascend. _arXiv preprint_ , 2023. 

- [13] R. Chen, W. Zhao, and C. Liu. Safety index synthesis with state-dependent control space. _arXiv preprint_ , 2023. 

- [14] W. Zhao, T. He, T. Wei, S. Liu, and C. Liu. Safety index synthesis via sum-of-squares programming, 2022. URL https://arxiv.org/abs/2209.09134. Also appears in ACC 2023 (doi:10.23919/ACC55779.2023.10156463). 

- [15] A. A. Ahmadi and A. Majumdar. Dsos and sdsos optimization: more tractable alternatives to sum of squares and semidefinite optimization. _SIAM Journal on Applied Algebra and Geometry_ , 3(2):193–230, 2019. 

9 

- [16] L. Lindemann, A. Robey, D. V. Dimarogonas, S. Tu, N. Matni, and R. Tedrake. Learning hybrid control barrier functions from data. In _Proceedings of the 4th Conference on Robot Learning_ , volume 155 of _Proceedings of Machine Learning Research_ , 2021. URL https: //proceedings.mlr.press/v155/lindemann21a.html. 

- [17] T. Vertovec and A. Clark. Scalable verification of neural control barrier functions using linear bound propagation. _arXiv preprint_ , 2025. 

- [18] H. Zhang, Z. Qin, S. Gao, and A. Clark. Seev: Efficient and sound neural network verification for safety-critical barrier certificates, 2024. URL https://arxiv.org/abs/2410. 20326. 

- [19] S. Bansal, M. Chen, S. Herbert, and C. J. Tomlin. Hamilton-jacobi reachability: A brief overview and recent advances. In _2017 IEEE 56th Annual Conference on Decision and Control (CDC)_ , 2017. doi:10.1109/CDC.2017.8263977. arXiv:1709.07523. 

- [20] J. Darbon and S. Osher. Algorithms for overcoming the curse of dimensionality for certain hamilton–jacobi equations arising in control theory and elsewhere, 2016. URL https:// arxiv.org/abs/1605.01799. 

- [21] J. F. Fisac, N. F. Lugovoy, V. Rubies-Royo, S. Ghosh, and C. J. Tomlin. Bridging hamiltonjacobi safety analysis and reinforcement learning. In _2019 International Conference on Robotics and Automation (ICRA)_ , pages 8550–8556. IEEE, 2019. 

- [22] K.-C. Hsu, V. Rubies-Royo, C. J. Tomlin, and J. F. Fisac. Safety and liveness guarantees through reach-avoid reinforcement learning. In _Proceedings of Robotics: Science and Systems_ , 2021. doi:10.15607/RSS.2021.XVII.077. URL https://www. roboticsproceedings.org/rss17/p077.pdf. 

- [23] M. Ganai, Z. Gong, C. Yu, S. Herbert, and S. Gao. Iterative reachability estimation for safe reinforcement learning. In _Advances in Neural Information Processing Systems_ , 2023. URL https://papers.nips.cc/paper_files/paper/2023/file/ dca63f2650fe9e88956c1b68440b8ee9-Paper-Conference.pdf. 

- [24] R. S. Sutton. Learning to predict by the methods of temporal differences. _Machine Learning_ , 3(1):9–44, 1988. doi:10.1023/A:1022633531479. 

- [25] W. Zhao, T. He, T. Wei, S. Liu, and C. Liu. Safety index synthesis via sum-of-squares programming. In _ACC_ , pages 732–737. IEEE, 2023. 

- [26] S. Fujimoto, H. Hoof, and D. Meger. Addressing function approximation error in actor-critic methods. In _International conference on machine learning_ , pages 1587–1596. PMLR, 2018. 

10 

## **A Proof of Contraction Mapping** 

**Theorem 2** (Contraction Mapping) **.** _The stochastic multi-step safety Bellman equation induces a contraction mapping under the supremum norm for λ ∈_ [0 _,_ 1) _and δ ∈_ [0 _,_ 1) _. Namely, for V, V_<sup>˜</sup> : _X →_ R _, there exists a constant ρ ∈_ [0 _,_ 1) _such that ∥Tλ,δ_ [ _V_ ] _− Tλ,δ_ [ _V_<sup>˜</sup> ] _∥∞ ≤ ρ∥V − V_<sup>˜</sup> _∥∞._ 

_Proof._ For brevity, let _m_<sup>(</sup> _t_<sup>_n_)</sup> := max _t≤k≤t_ + _n−_ 1 _ℓk_ . Let _Vt ≡ V_ ( _xt_ ) and expand the terminal sampling, we have 


Then, _∀xt ∈X_ , 


Hence, we have _∥Tλ,δ_ [ _V_ ] _− Tλ,δ_ [ _V_<sup>˜</sup> ] _∥∞ ≤_ E _n|xt_ [ _δ_<sup>_n_</sup> ] _∥V − V_<sup>˜</sup> _∥∞_ . The contraction factor is indeed _ρ_ = E _n|xt_ [ _δ_<sup>_n_</sup> ] _∈_ [0 _,_ 1). 

11 

## **B** _λ_ **-Reachability Implementation** 

### **B.1 Practical Implementations** 

**Truncated Geometric Distribution.** In practice, trajectories are finite and only a limited number of future states are available for each anchor time step. Sampling from an untruncated geometric distribution would therefore place non-negligible probability mass on horizons beyond the available data, implicitly biasing updates toward terminal states. To address this issue, we sample the bootstrap horizon from a truncated geometric distribution with finite support and renormalized probabilities, 


where _T_ denotes the terminal time of the trajectory. This truncation preserves the geometric structure of the stopping distribution while ensuring that all sampled horizons are feasible given the available data. 

**Value Initialization.** Safety signals _ℓ_ ( _x_ ) are non-positive within the safe set, and the reachability update relies on a max operator over future safety values. As a consequence, initializing the value function with overly pessimistic (positive) values can lead to self-reinforcing errors, whereby spurious unsafe predictions are repeatedly propagated backward through bootstrapping. To prevent this failure mode, we initialize the value function conservatively as 


which guarantees that early bootstrapped targets are dominated by observed safety signals rather than inaccurate value estimates. This initialization bias is gradually corrected as unsafe events are encountered during training. In practice, we assign _V_ 0<sup>_π_(</sup><sup>_x_) to a constant which is by design a lower</sup> bound of _ℓ_ . 

**Stabilizing Training.** We adopt several stabilization techniques from value-based learning to improve robustness under bootstrapped max backups. First, we use a slowly-updated target network to compute bootstrap values in (10). Concretely, we maintain two online critics _Vθ_<sup>_π_</sup> 1<sup>_, V_</sup> _θ_<sup>_π_</sup> 2<sup>and their cor-</sup> responding target networks _Vθ_ ¯<sup>_−_</sup> 1<sup>_, V_</sup> _θ_ ¯<sup>_−_</sup> 2<sup>.Following the clipped target idea in double-Q methods [26],</sup> we compute the bootstrap term conservatively as 


and use _V_ boot<sup>_−_(</sup><sup>_xt_+</sup><sup>_n_)inplaceof</sup><sup>_Vπ_(</sup><sup>_xt_+</sup><sup>_n_)in(10).Bothonlinecriticsregresstothesametarget,</sup> which substantially reduces the propagation of spurious over-estimation through the max operator. Target networks are updated via Polyak averaging, _θ_<sup>¯</sup> _←_ (1 _− τ_ ) _θ_<sup>¯</sup> + _τθ_ . 

12 

### **B.2** _λ_ **-Reachability Training Procedures** 


13 

## **C Implementation Details** 

We present the implementation details of the entire pipeline used to train and evaluate safety value functions for the G1FLAT, G1ROUGH, and G1COLLISION tasks both in simulation and on physical hardware. For each task, we keep the humanoid modeling consistent across policy training, rollout collection, safety value learning, and safety value inference. For simulation inference, all stages are performed in simulation. For hardware inference, all stages except the safety value inference are done in simulation. Adaptations are made to accommodate the absence of certain hardware observations, for example, link-obstacle contact signals. 

All training and inference steps are performed on a single workstation equipped with an NVIDIA RTX 4090 (24 GB) GPU, running PyTorch 2.7.0+cu128, Python 3.11, IsaacLab 0.46, and rsl ~~r~~ l. 

### **C.1 Robot Policy Training** 

We first describe the environment setup and training details for acquiring the robot policy _π_ . 

### **C.1.1 Policy Training for Safety Value Inference in Simulation** 

For simulation experiments in Section 4.4, we use a Unitree G1 humanoid robot with 34 DoF. The observation spaces for all three tasks are listed in Table 3. 

Table 3: Observation composition for the simulation policies. All entries are single-frame dimensions (no history stacking). The critic shares the actor’s observation group <u>(symmetric actor–critic).</u> 

|Observation segment|G1FLAT|G1ROUGH|G1COLLISION|
|---|---|---|---|
|Base linear velocity**v** _∈_R<sup>3</sup>|3|3|3|
|Base angular velocity**_ω_** _∈_R<sup>3</sup><br>|3|3|3|
|Projected gravity**g** _∈_R<sup>3</sup>|3|3|3|
|Velocity command**c**_∈_R<sup>3</sup>|3|3|3|
|Joint positions**q**_∈_R<sup>37</sup>|37|37|37|
|Joint velocities ˙**q**_∈_R<sup>37</sup>|37|37|37|
|Last action**a**_∈_R<sup>37</sup>|37|37|37|
|Height scan**s**scan _∈_R<sup>187 </sup>(17_×_11grid,0_._1m)<br>|—|187|—|
|Ball position in base frame**p**ball _∈_R<sup>3</sup><br>|—|—|3|
|Ball velocity in base frame**v**ball _∈_R<sup>3</sup>|—|—|3|
|Total observation dimension|123|310|129|


In G1FLAT and G1ROUGH, the safety signal is defined as 


The robot is considered to be safe and balanced if (a) its root height _h_ root is higher than the threshold _h_ min = 0 _._ 2 _m_ and (b) the deviation _ψg_ between the root Z axis and gravity is at most _ψ_ max = _π/_ 4. _h_<sup>_∗_</sup> root<sup>= 0</sup><sup>_._65</sup><sup>_m_is the default standing root height.</sup> 

In G1COLLISION, a lightweight ball (50 _g_ , 10 _cm_ radius) is spawned every 3 to 5 seconds and launched toward the humanoid robot. The ball spawns at a random position at [2 _m,_ 5 _m_ ] from the robot, at heights between [0 _._ 1 _m,_ 1 _._ 2 _m_ ], and is given an initial velocity of [3 _m/s,_ 6 _m/s_ ] aimed at the robot’s torso at 0 _._ 8 _m_ height with gravity compensation to follow a ballistic arc. 

Rewards used for training _π_ are summarized in Table 4. 

The policy _π_ for all tasks is an MLP with feed-forward layers with ELU activations and a Gaussian action head (initial scalar standard deviation 1 _._ 0, no observation normalization). The hidden sizes are [256 _,_ 128 _,_ 128] for G1FLAT and G1COLLISION and [512 _,_ 256 _,_ 128] for G1ROUGH; the output dimension matches the action space (37), and joint-position targets are recovered as **q**<sup>target</sup> = **q**<sup>def</sup> + 0 _._ 5 **a** (scale 0 _._ 5, default-offset on, no action clipping). The policy is trained with PPO for 1000 steps with 2048 parallel agents in IsaacLab. Hyperparameter used are listed in Table 5. 

14 

Table 4: Reward composition for the simulation PPO policies. A dash (—) means the term is not used for that task. For G1COLLISION the ball-related terms are curriculum-gated, becoming active only after iteration 500; episodes terminate at 20 s or on illegal torso ~~l~~ ink contact ( _>_ 1 N), with ball impacts above 0 _._ 4 m excluded from termination. 

|Term|Formula|G1FLAT|G1ROUGH|G1COLLISION|
|---|---|---|---|---|
|Lin. vel. tracking|exp(_−∥_**v**_xy −_**c**_xy∥_<sup>2</sup>_/σ_<sup>2</sup>)<br>_σ_=0_._5|1_._0|1_._0|1_._0|
|Ang. vel. tracking|exp(_−_(_ωz −cωz_)<sup>2</sup>_/σ_<sup>2</sup>)<br>_σ_=0_._5|1_._0|2_._0|1_._0|
|_z_-velocity penalty|_v_<sup>2</sup><br>_z_|_−_0_._2|0|_−_0_._2|
|Roll/pitch penalty|_∥_**_ω_**_xy∥_<sup>2</sup>|_−_0_._05|—|_−_0_._05|
|Joint torques|_∥_**_τ_**_∥_<sup>2</sup>|_−_2_×_10<sup>_−_6</sup>|_−_1_._5_×_10<sup>_−_7</sup>|_−_2_×_10<sup>_−_6</sup>|
|Joint accelerations|_∥_¨**q**_∥_<sup>2</sup>|_−_1_×_10<sup>_−_7</sup>|_−_1_._25_×_10<sup>_−_7</sup>|_−_1_×_10<sup>_−_7</sup>|
|Action rate|_∥_**a**_t −_**a**_t−_1_∥_<sup>2</sup>|_−_0_._005|_−_0_._005|_−_0_._005|
|Feet air-time bonus|�<br>_f_<sup>(</sup><sup>_t_air</sup><br>_f_<br>_−_<sup>¯</sup>_t_)**1**[first contact]<br>¯_t_=0_._4s|0_._75|0_._25|0_._75|
|Feet slide|�<br>_f_<sup>_∥_</sup><sup>**v**</sup><sup>_f∥_</sup><sup>**1**[contact]</sup>|_−_0_._1|_−_0_._1|_−_0_._1|
|Flat orientation|_∥_**g**_xy∥_<sup>2</sup>|_−_1_._0|_−_1_._0|_−_1_._0|
|Joint-position limits|�<br>_j_ <sup>max(0</sup><sup>_, qj −q_max</sup><br>_j_<br>)<br>+ max(0_, q_<sup>min</sup><br>_j_<br>_−qj_)|_−_1_._0|_−_1_._0|_−_1_._0|
|Undesired contacts|<br><br><br>�<br>_b_ <sup>**1**[</sup><sup>_∥_</sup><sup>**f**</sup><sup>_b∥>_ 1 N]</sup><br>(torso/arms)|_−_1_._0|—|_−_1_._0|
|Termination|**1**[episode terminates]|_−_200|_−_200|_−_200|
|Joint deviation (hip)|�<br>_j∈_hip<sup>(</sup><sup>_qj −q_def</sup><br>_j_<br>)<sup>2</sup>|—|_−_0_._1|—|
|Joint deviation (arms)|�<br>_j∈_arms<sup>(</sup><sup>_qj −q_def</sup><br>_j_<br>)<sup>2</sup>|—|_−_0_._1|—|
|Joint deviation (fingers)|�<br>_j∈_fingers<sup>(</sup><sup>_qj −q_def</sup><br>_j_<br>)<sup>2</sup>|—|_−_0_._05|—|
|Joint deviation (torso)|i<br>(_q_torso_−q_<sup>def</sup><br>torso<sup>)2</sup>|—|_−_0_._1|—|
|Ball proximity|exp(_−d_<sup>2</sup><br>ball<sup>_/σ_2),</sup><sup>_σ_=2</sup><sup>_._0 m</sup>|—|—|_−_5_._0|
|Ball collision|**1**[_∥_**f**ball_∥>_0_._1N]|—|—|_−_1_._0|


Table 5: PPO hyperparameters for the simulation policies. All three tasks use the same algorithmic settings; only the network width and the number of training iterations vary per task. For all simulation tasks the actor and the critic consume the _same_ observation group <u>(symmetric actor–critic).</u> 

|Optimiser<br>|Adam, lr1_×_10<sup>_−_3</sup>, adaptive schedule (target KL0_._01)<br>|
|---|---|
|Discount_γ_, GAE_λ_GAE|0_._99, 0_._95|
|PPO clip / value-loss coef / entropy coef|0_._2/1_._0/0_._008|
|Epochs per update / minibatches per update|5/4|
|Steps per environment per rollout|24|
|Parallel environments|4096|
|Max gradient norm|1_._0|
|Iterations (G1FLAT/ G1ROUGH/ G1COLLISION)|1500/3000/1500|
|Random seed|42|
|Actor / critic observations|symmetric (no privileged terms)|


### **C.1.2 Policy Training for Safety Value Inference in the Real World** 

For hardware experiments in Section 4.5, we use a Unitree G1 humanoid robot with 29 DoF to be consistent with the physical platform we have access to. The environment setup for G1FLAT and G1COLLISION is shown below. 

**Observation space.** For deployment the observation history is stacked over the last 5 control steps (history length 5, control rate 50 Hz). Table 6 lists the per-frame composition and the resulting actor/critic dimensions. The actor uses only sensors that are also available on the physical platform (no base linear velocity), while the critic additionally observes **v** _∈_ R<sup>3</sup> per frame: an _asymmetric_ actor–critic. 

15 

Table 6: Observation composition for the 29-DoF hardware policies. The critic additionally consumes the base linear velocity **v** per frame (privileged) and is therefore 3 dimensions per frame larger than the actor. 

|Observation segment (per frame)|G1FLAT|G1COLLISION|
|---|---|---|
|Base angular velocity**_ω_** _∈_R<sup>3</sup>|3|3|
|Projected gravity**g** _∈_R<sup>3</sup><br>|3|3|
|Velocity command**c**_∈_R<sup>3</sup>|3|3|
|Joint positions**q**_∈_R<sup>29</sup>|29|29|
|Joint velocities ˙**q**_∈_R<sup>29</sup><br>|29|29|
|Last action**a**_∈_R<sup>29</sup>|29|29|
|Ball position in base frame**p**ball _∈_R<sup>3</sup><br>|—|3|
|Ball velocity in base frame**v**ball _∈_R<sup>3</sup>|—|3|
|Per-frame dimension|96|102|
|Actor observation (5-frame stack)|480|510|
|Critic observation (actor +**v**/frame)|495|525|


**Rewards.** Table 7 lists the reward terms used for training the two hardware policies. G1COLLISION (HW) is warm-started from the deployed G1FLAT (HW) baseline; the only additions in the avoidance policy are the three ball-related terms. 

Table 7: Reward composition for the 29-DoF hardware policies. A dash (—) denotes a term not used for that task. Termination conditions: time-out (20 s), base height _<_ 0 _._ 2 m, or projected-gravity tilt _>_ 0 _._ 8 rad. 

|Term|Formula|G1FLAT(HW)<br>G|1COLLISION(HW)|
|---|---|---|---|
|Lin. vel. tracking|exp(_−∥_**v**_xy −_**c**_xy∥_<sup>2</sup>_/σ_<sup>2</sup>)<br>_σ_=0_._5|1_._0|1_._0|
|Ang. vel. tracking|exp(_−_(_ωz −cωz_)<sup>2</sup>_/σ_<sup>2</sup>)<br>_σ_=0_._5|0_._5|0_._5|
|Alive bonus|1per step|0_._15|0_._15|
|Flat orientation|_∥_**g**_xy∥_<sup>2</sup>|_−_5_._0|_−_5_._0|
|Joint-position limits|�<br>_j_ <sup>max(0</sup><sup>_, qj −q_max</sup><br>_j_<br>)<br>+ max(0_, q_<sup>min</sup><br>_j_<br>_−qj_)|_−_5_._0|_−_5_._0|
|Undesired contacts|�<br>_b_ <sup>**1**[</sup><sup>_∥_</sup><sup>**f**</sup><sup>_b∥>_ 1 N] (excl. ankles)</sup>|_−_1_._0|_−_1_._0|
|Feet slide|�<br>_f_<sup>_∥_</sup><sup>**v**</sup><sup>_f∥_</sup><sup>**1**[contact]</sup>|_−_0_._2|_−_0_._2|
|Joint deviation (arms)|�<br>_j∈_arms<sup>(</sup><sup>_qj −q_def</sup><br>_j_<br>)<sup>2</sup>|_−_0_._1|_−_0_._1|
|Joint deviation (waist)|�<br>_j∈_waist<sup>(</sup><sup>_qj −q_def</sup><br>_j_<br>)<sup>2</sup>|_−_1_._0|_−_1_._0|
|Joint deviation (hip yaw/roll)|�<br>_j∈_hip<sup>(</sup><sup>_qj −q_def</sup><br>_j_<br>)<sup>2</sup>|_−_1_._0|_−_1_._0|
|_z_-velocity penalty|_v_<sup>2</sup><br>_z_|_−_2_._0|_−_2_._0|
|Roll/pitch penalty|_∥_**_ω_**_xy∥_<sup>2</sup>|_−_0_._05|_−_0_._05|
|Joint velocity|_∥_˙**q**_∥_<sup>2</sup>|_−_10<sup>_−_3</sup>|_−_10<sup>_−_3</sup>|
|Joint acceleration|_∥_¨**q**_∥_<sup>2</sup>|_−_2_._5_×_10<sup>_−_7</sup>|_−_2_._5_×_10<sup>_−_7</sup>|
|Action rate|_∥_**a**_t −_**a**_t−_1_∥_<sup>2</sup>|_−_0_._05|_−_0_._05|
|Energy (Unitree)|�<br>_j _<sup>_τj_ ˙</sup><sup>_qj_</sup>|_−_2_×_10<sup>_−_5</sup>|_−_2_×_10<sup>_−_5</sup>|
|Base height|(_h_base_−_0_._78)<sup>2</sup>|_−_10_._0|_−_10_._0|
|Feet gait (Unitree)|period0_._8s, offset[0_,_0_._5],<br>threshold0_._55|0_._5|0_._5|
|Feet clearance (swing)|�<br>_f_<sup>(</sup><sup>_hf −_0</sup><sup>_._1)2</sup><sup>**1**[swing]</sup>|1_._0|1_._0|
|Ball proximity|exp(_−d_<sup>2</sup><br>ball<sup>_/σ_2),</sup><sup>_σ_=2</sup><sup>_._0 m</sup>|—|_−_5_._0|
|Ball collision|**1**[_∥_**f**ball_∥>_0_._1N]|—|_−_20_._0|
|Ball approaching|max(0_, −_<sup>˙</sup>_d_ball)_·_ **1**[_d_ball _≤_2m]|—|_−_2_._0|


**PPO hyperparameters.** Table 8 lists the PPO settings for the hardware policies. Both tasks use a [512 _,_ 256 _,_ 128] MLP with ELU activations and a Gaussian action head (init scalar std 1 _._ 0). Compared to the simulation lineage, the hardware policies use (i) wider networks, (ii) an asymmetric actor–critic, (iii) a smaller action scale ( **q**<sup>target</sup> = **q**<sup>def</sup> + 0 _._ 25 **a** , vs. 0 _._ 5 in simulation), and (iv) 

16 

a richer domain randomisation regime (friction sampling, base-mass perturbation, and a periodic root-velocity push event) to bridge to hardware. 

Table 8: PPO hyperparameters for the 29-DoF hardware policies. 

|Hyperparameter|Value|
|---|---|
|Actor/critic hidden dimensions|[512_,_256_,_128]|
|Activation; action head|ELU; Gaussian, init scalar std1_._0|
|Observation normalisation<br>Optimiser|off (empirical normalisation on)<br>Adam, lr10<sup>_−_3</sup>,<br>adaptive schedule (target KL0_._01)|
|Discount_γ_, advantage_λ_GAE|0_._99, 0_._95|
|PPO clip / value-loss coef / entropy coef|0_._2/1_._0/0_._01|
|Epochs per update / minibatches per update|5/4|
|Steps per environment per rollout|24|
|Parallel envs (G1FLAT/ G1COLLISION)<br>Iterations (G1FLAT)|8192/4096<br>30 000<br>(deployed @6 000)|
|Iterations (G1COLLISION)|5 000<br>(deployed @4 999)|
|Warm start (G1COLLISION)|resume from deployed G1FLATbaseline|
|Observation history length|5frames|
|Actor / critic observations|**asymmetric**; critic adds**v** _∈_R<sup>3 </sup>per frame<br>friction_∈_[0_._3_,_1_._0];|
|Domain randomisation|base mass+[_−_1_,_3]kg;<br>push every5s,<br>_vx,y ∼U_[_−_0_._5_,_0_._5]m/s|
|Random seed|42|


**Sim-vs-hardware differences in PPO.** The hardware lineage diverges from the simulation lineage in four respects. _(i) Asymmetric actor–critic._ Because the base linear velocity **v** is not reliably observable on the deployed platform, it is withheld from the actor and provided only to the critic; the actor consumes 96 (G1FLAT) or 102 (G1COLLISION) dimensions per frame while the critic consumes 99 and 105, respectively. _(ii) Observation history._ Hardware observations are stacked over the last 5 frames (simulation uses single-frame observations). _(iii) Action scale._ Joint-position targets are recovered as **q**<sup>target</sup> = **q**<sup>def</sup> + 0 _._ 25 **a** on hardware versus 0 _._ 5 **a** in simulation, halving the action range to reduce abrupt commands. _(iv) Domain randomisation._ Friction is sampled in [0 _._ 3 _,_ 1 _._ 0], the torso mass is perturbed by [ _−_ 1 _,_ 3] kg, and a periodic root-velocity push event with _vx,y ∼U_ [ _−_ 0 _._ 5 _,_ 0 _._ 5] m/s is applied every 5 s; the simulation lineage uses no such randomisation. All other PPO settings (optimiser, _γ_ , _λ_ GAE, clip, value-loss/entropy coefficients, epochs and minibatches) are identical to the simulation policies. 

### **C.2 Data Collection for Safety Value Learning** 

With robot policy _π_ , the dataset _D_ for safety value learning is generated by evaluating _π_ in each simulation environment with 2048 agents for 1000 steps. For simulation inference tasks in Section 4.4, safety signals are labeled following Section 4.1. For hardware inference in Section 4.5, we label the safety signal for G1FLAT as _ℓ_ flat := _ℓ_ ori. The contact component _ℓ_ contact in the safety signal for G1COLLISION is synthesized as _ℓ_ contact := 1 _d_ ball _≤_ 0 _._ 3 _−_ 1 _d_ ball _>_ 0 _._ 3. 

### **C.3 Safety Value Learning** 

Using the dataset _D_ , we train the _λ_ -Reachability approach, its ablations, and baselines. All safety values are represented as neural networks with two hidden layers of width 256 and ReLU activations, mapping each task’s observation to a scalar value _V_<sup>_π_</sup> ( _x_ ) _∈_ R. The final linear layer is initialised with zero weights and bias _−_ 2, so that _V_<sup>_π_</sup> starts strongly safe everywhere. For _λ_ -Reachability 

17 

we instantiate two critics _Vθ_<sup>_π_</sup> 1<sup>,</sup><sup>_V_</sup> _θ_<sup>_π_</sup> 2<sup>withthisarchitectureandreporttheensemblemean</sup><sup>_Vπ_(</sup><sup>_x_)=</sup> <u>12�</u> _Vθ_<sup>_π_</sup> 1<sup>(</sup><sup>_x_) +</sup><sup>_V_</sup> _θ_<sup>_π_</sup> 2<sup>(</sup><sup>_x_)</sup> �; the baselines use a single critic with the same architecture. Training is done following Section 4.2. Full training parameters for _λ_ -Reachability and DPE are reported below. 

Table 9: Safety-value learning hyperparameters. The main columns report the configuration used for the hardware-inference lineage; values that change for the simulation-inference lineage are listed in the last column. For _λ_ -Reachability we additionally report ablations _λ ∈{_ 0 _._ 99 _,_ 0 _._ 95 _,_ 0 _._ 50 _,_ 0 _}_ in Section 4.4; the value shown here is the default ( _λ_ =0 _._ 99) used in all main results. 

|Hyperparameter|_λ_-Reachability|DPE|Sim-inference override|
|---|---|---|---|
|Critic ensemble|2<br>(clipped double-_Q_)|1|—|
|Horizon discount_λ_|0_._99(main)|annealed<br>0_._9_→_0_._99|—|
|Per-step survival_δ_|0_._99|—|—|
|Absorption value_v_term|_−_10<sup>6</sup>|—|—|
|Max bootstrap horizon_n_max|200|1<br>(one-step TD)|—|
|Hidden dims, activation|[256_,_256], ReLU|[256_,_256], ReLU|—|
|Optimiser, learning rate_α_|Adam,10<sup>_−_3</sup>|Adam,10<sup>_−_3</sup>|—|
|Batch size_B_|256|256|—|
|Target Polyak rate_τ_|0_._005|0_._05|_τ_=0_._05<br>(_λ_-reach)|
|Target update period|every step<br>regression|every10steps|every10steps<br>(_λ_-reach)|
|Loss|+lower-bound hinge<br>+monotonicity hinge<br>+sign BCE (_α_bce=5);<br>weights(1_,_1_,_1_,_1)|MSE on<br>(1_−λ_)_ℓ_<br>+_λ_max(_ℓ, V _<sup>_−_</sup>(_x_<sup>_′_</sup>))|hinge / BCE<br>weights_→_0|
|Total gradient steps|10 000|10 000|2 000|
|Evaluation cadence|every500steps|every500steps|—|
|Random seed|0|0|—|


### **C.4 Safety Value Inference** 

Simulation inference is performed by applying the learned _V_<sup>_π_</sup> to the same environments on which the rollout policy was trained, and computing metrics according to Section 4.3. For hardware inference, we collect real data from policy rollouts with artificially generated disturbances. To record observations for G1COLLISION, we use an Optitrack motion capture system to stream the poses of both the humanoid base and a ball, which serves as the dynamic obstacle. The relative position and velocity of the ball in the humanoid base frame are computed online as part of the observation for the safety value function. The safety values are applied to the collected trajectories and evaluated against labeled safety signals following Section 4.3. 

18 

## **D Hardware Experiment Results** 

In this section, we present additional hardware experimental results on G1FLAT and G1COLLISION, including video screenshots and plots of the safety signal _ℓ_ and the inferred safety value _V_<sup>_π_</sup> . In each plot, we mark the timestamp of the external events that perturb the robot towards unsafe regions and observe the first timestamp at which _λ_ -Reachability and the DPE baseline predict non-recoverable states, and the first timestamp of actual unsafe events. It is evident that _λ_ outperforms the baseline via earlier warning and more accurate value prediction. 


Figure 4: Additional hardware experiment results. 

19 

