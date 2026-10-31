---
title: "Occupancy Reward Shaping: Improving Credit Assignment for Offline Goal-Conditioned Reinforcement Learning"
date: "2026-04-22"
authors: "Aravind Venugopal; Jiayu Chen; Xudong Wu; Chongyi Zheng; Benjamin Eysenbach; Jeff Schneider"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2604.20627
pdf: https://arxiv.org/pdf/2604.20627
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.20627)** / [論文ページ](https://arxiv.org/abs/2604.20627)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Published as a conference paper at ICLR 2026 

## OCCUPANCY REWARD SHAPING: IMPROVING CREDIT ASSIGNMENT IN OFFLINE GOAL-CONDITIONED REINFORCEMENT LEARNING 

|**Aravind Venugopal**<sup>_∗_</sup><br>Carnegie Mellon University|**Jiayu Chen**<br>The University of Hong Kong,<br>INFIFORCE Intelligent Technology|**Xudong Wu**<br>The University of Hong Kong|
|---|---|---|
|**Chongyi Zheng**|**Benjamin Eysenbach**|**Jeff Schneider**|
|Princeton University|Princeton University|Carnegie Mellon University|


### ABSTRACT 

The temporal lag between actions and their long-term consequences makes credit assignment a challenge when learning goal-directed behaviors from data. Generative world models capture the distribution of future states an agent may visit, indicating that they have captured temporal information. How can that temporal information be extracted to perform credit assignment? In this paper, we formalize how the temporal information stored in world models encodes the underlying geometry of the world. Leveraging optimal transport, we extract this geometry from a learned model of the occupancy measure into a reward function that captures goal-reaching information. Our resulting method, **Occupancy Reward Shaping (ORS)** , largely mitigates the problem of credit assignment in sparse reward settings. ORS provably does not alter the optimal policy, yet empirically improves performance by 2 _._ 2 _×_ across 13 diverse long-horizon locomotion and manipulation tasks. Moreover, we demonstrate the effectiveness of ORS in the real world for controlling nuclear fusion on 3 Tokamak control tasks. 

Code: https://github.com/aravindvenu7/occupancy ~~r~~ eward ~~s~~ haping 

Website: https://github.com/aravindvenu7.github.io/website/ors/ 

### 1 INTRODUCTION 

Reinforcement learning (RL) is fundamentally tied to credit assignment because effectively reasoning about the long-term consequences of actions is crucial to learn diverse goalreaching behaviors from data. Although goal-conditioned reinforcement learning (GCRL) offers a simple, domainagnostic and scalable framework for RL from large offline datasets (Liu et al., 2022a; Yang et al., 2023), GCRL agents trained with sparse rewards struggle with credit assignment (Eysenbach et al., 2022; Ding et al., 2019; Wang et al., 2023a; Park et al., 2024a). Therefore, the design of welldefined and meaningful reward functions, called reward shaping (Ng et al., 1999) is a promising solution to address the credit assignment challenge (Yu et al., 2025). 

While manual reward design for each goal is infeasible, existing work relies on learning local temporal distance estimators from offline data (Hartikainen et al., 2019) and using them to build semi/non-parametric graphs (Savinov et al., 2018; Mezghani et al., 2023) and indirectly infer temporal information for credit assignment. These approaches run the risk of 


Figure 1: Average relative success rate (task-normalized) on 7 challenging OGBench tasks (Park et al., 2024a). Higher is better; 100.% matches the best algorithm per task. Our method, ORS, performs best, improving over the best baseline by 31%. 

> 1Corresponding author: avenugo2@andrew.cmu.edu 

1 

Published as a conference paper at ICLR 2026 


Figure 2: ORS learns the occupancy measure (distribution of future states) and extracts goal-reaching information into a reward function such that states with future states closer to goal have higher rewards. 

scaling poorly with task complexity as composing local infor- 

mation to infer global temporal dependencies often leads to compounding errors. So, _can we learn reward functions that accurately and directly capture long-term temporal dependencies and goalreaching information present in offline data?_ 

Generative world models (Janner et al., 2020b; Schramm & Boularias, 2024; Farebrother et al., 2025) have shown a remarkable ability to capture the multi-modal distribution of future states an agent may visit, i.e., the occupancy measure. This suggests that they must inherently possess the ability to reason about long-term temporal effects of actions by encoding the geometry of the environment. Nonetheless, it remains unclear how to extract such temporal information from a learned world model and leverage it for credit assignment. 

In this paper, we formalize how world models encode world geometry. Specifically, using tools for optimal transport, we show that long-term temporal dependencies can be explicitly recovered from the velocity field of a learned occupancy model trained with flow matching (Liu et al., 2022b; Lipman et al., 2022). Building on this insight, we propose **Occupancy Reward Shaping** (ORS), a reward-shaping method that extracts global goal-reaching information from the dataset occupancy measure into a scalar reward while provably preserving the optimal policy. We demonstrate that ORS significantly enhances performance, improving **2** _._ **2** _×_ over its sparse-reward base algorithm and achieving **24%-248%** improvements over state-of-the-art methods on 13 challenging locomotion and manipulation tasks from OGBench (Park et al., 2024a). Furthermore, ORS consistently outperforms baselines on 3 tasks that involve controlling actuators in a nuclear fusion reactor called a Tokamak (Char et al., 2023), showing its utility in complex, real-world systems. 

### 2 RELATED WORK 

**Offline GCRL.** Offline GCRL has been a long-standing area of research in RL (Kaelbling, 1993; Schaul et al., 2015), stemming from a necessity to build innovative algorithms taking advantage of its rich metric structures, probabilistic goal-reaching interpretations and sub-goal compositionality. As a result, diverse types of algorithms exist in offline GCRL based on behavioral cloning (Yang et al., 2022; Hejna et al., 2023), actor-critic methods (Haarnoja et al., 2018; Kostrikov et al., 2021), hind-sight goal relabeling (Andrychowicz et al., 2017) as well as more specialized approaches based on metric learning (Wang et al., 2023a; Reichlin et al., 2024; Park et al., 2024c), contrastive reinforcement learning (Eysenbach et al., 2022), dual RL (Ma et al., 2022; Sikchi et al., 2023b) and hierarchical RL (Chane-Sane et al., 2021; Park et al., 2023; Zhou & Kao, 2025). 

Hierarchical RL methods (Chane-Sane et al., 2021; Park et al., 2023) address the challenges posed by long-horizon, sparse-reward tasks with a two-level policy structure where the high level policy predicts sub-goals that a low-level policy learns to reach. Methods such as Ahn et al. (2025) address this challenge by learning an n-step critic (De Asis et al., 2018) to effectively reduce the temporal horizon. Our approach addresses this challenge using reward shaping for effective credit assignment, making ORS complementary to the methods discussed above. 

2 

Published as a conference paper at ICLR 2026 

**Reward Shaping.** The idea of using reward shaping to facilitate learning dates back to early RL research and applications (Saksida et al., 1997; Randløv & Alstrøm, 1998). In their canonical work, Ng et al. (1999) proposes potential-based reward shaping (PBRS) that preserves the optimal policy under shaped rewards. Potential functions have been learned using expert demonstrations (Brys et al., 2015; Kang et al., 2018), transitions (Harutyunyan et al., 2015), uncertainty (Li et al., 2025) or with discriminators to be used as exploration bonuses (Durugkar et al., 2021). Another line of research does not follow PBRS and considers reward shaping as a bonus for exploration (Pathak et al., 2017; Mguni et al., 2021; Wang et al., 2023b; Agarwal et al., 2023; Ma et al., 2024; Zheng et al., 2024) and as curriculum learning (Andrychowicz et al., 2017; Eysenbach et al., 2022; Zheng et al., 2023). 

Hartikainen et al. (2019) estimates local temporal distance to provide a dense reward for credit assignment in online GCRL. We address the challenge of learning shaped rewards for credit assignment in Offline GCRL. The closest work to ours, Mezghani et al. (2023), uses both a local reward computed with a local temporal distance classifier and a “global” reward computed using shortest path search on a graph constructed using the local distance classifier. While graph-based methods scale poorly with task complexity, we learn a single reward function capable of directly encoding global, long-horizon goal-reaching information for credit assignment by leveraging the occupancy measure. Our experiments show the effectiveness of ORS over prior state-of-the-art work. 

### 3 BACKGROUND 

#### 3.1 NOTATION 

**Goal-Conditioned Reinforcement Learning:** We consider an infinite-horizon controlled Markov Process (a MDP (Puterman, 2014) without rewards) defined by ( _S, A, µ, p, γ_ ) with state space _S_ and action space _A_ . _p_ : _S × A × S →_ R denotes the transition function while _µ_ denotes the initial state distribution. The discount factor is denoted by _γ ∈_ (0 _,_ 1). A policy _π_ ( _a|s_ ): _S×A →_ R is a probability distribution mapping states to actions. Each policy induces a conditional state-action occupancy distribution _d_<sup>_π_</sup> ( _s_<sup>+</sup> _| s, a_ ) over future states _s_<sup>+</sup> : _d_<sup>_π_</sup> ( _s_<sup>+</sup> _| s, a_ ) = (1 _− γ_ )<sup>�</sup><sup>_∞_</sup> ∆ _t_ =1<sup>_γ_∆</sup><sup>_t−_1 P(</sup><sup>_st_+∆</sup><sup>_t_=</sup> _s_<sup>+</sup> _| s, a, π_ ), which we refer to as the occupancy measure for simplicity. 

The objective of GCRL is to reach any goal, _g ∈S_ , from another state _s ∈S_ in the minimum number of steps. A goal-conditioned policy _π_ ( _a|s, g_ ): _S × S × A →_ R maps states and goals to actions. Formally, the aim is to learn the optimal shortest-path policy _π_<sup>_∗_</sup> ( _a|s, g_ ) that maximizes E _τ ∼p_ ( _τ |g_ ) � _∞t_ =0<sup>_γtδg_(</sup><sup>_st_)where</sup><sup>_t_isthetimestep,</sup><sup>_p_(</sup><sup>_τ|g_)=</sup><sup>_µ_(</sup><sup>_s_0)</sup><sup>_π_(</sup><sup>_a_0</sup><sup>_|s_0</sup><sup>_, g_)</sup><sup>_p_(</sup><sup>_s_1</sup><sup>_|_</sup> _s_ 0 _, a_ 0) _· · · p_ ( _si | si−_ 1 _, ai−_ 1) _· · ·_ and _δg_ is a Dirac delta at goal _g_ . Such a policy reaches _g_ in the minimum number of steps. In this paper, we focus on offline GCRL. In particular, agents cannot interact with the environment for learning but have access to an offline dataset of trajectories _D_ , where each trajectory is _τ_ = ( _s_ 0 _, a_ 0 _, s_ 1 _, a_ 1 _, . . . ,_ ; _, sT_ ). We denote the dataset behavioral policy by _πD_ ( _a | s_ ) and the dataset occupancy measure corresponding to _πD_ by _d_<sup>_πD_</sup> ( _s_<sup>+</sup> _| s, a_ ). 

**Flow Matching:** Flow matching aims to learn to sample from a distribution _p_ **data** , given a finite number of samples _x_<sup>(1)</sup> _, ..., x_<sup>(</sup><sup>_N_)</sup> _∈_ **R**<sup>_d_</sup> drawn from _p_ **data** . Flow matching transforms a base distribution _p_ 0, which is typically a simple Isotropic Gaussian _N_ (0 _,_ **Id** ) at time _t_ = 0 to the target data distribution _p_ **data** ( _x_ ) at _t_ = 1. This transformation is defined by a velocity field _vθ_ ( _t, x_ ): [0 _,_ 1] _×_ **R**<sup>_d_</sup> _→_ **R**<sup>_d_</sup> , parameterized by a neural network and having a corresponding flow _ψθ_ ( _t, x_ ): [0 _,_ 1] _×_ **R**<sup>_d_</sup> _→_ **R**<sup>_d_</sup> which is a unique solution to the Ordinary Differential Equation (ODE) _dtd_<sup>_ψθ_(</sup><sup>_t, x_) =</sup><sup>_vθ_</sup> � _t, ψθ_ ( _t, x_ ))�. The velocity field is trained to minimize: 


where Unif([0 _,_ 1]) denotes uniform sampling between 0 and 1 and _xt_ = (1 _− t_ ) _x_ 0 + _t x_ 1 is the linear interpolation between _x_ 0 and _x_ 1. On convergence, _vθ_ ( _t, xt_ ) learns the velocity field which transforms samples from _p_ 0 to samples from _p_ **data** by numerically integrating the ODE. In this paper, following Lipman et al. (2024); Park et al. (2025), we use linear interpolation between base and target distributions and uniform time sampling. As in Park et al. (2025), we find that the Euler method is sufficient for solving the ODE. 

3 

Published as a conference paper at ICLR 2026 

#### 3.2 MOTIVATION 

In this section, we motivate our method by examining why credit assignment becomes a challenge when using sparse rewards. We do so by analyzing the learning dynamics of the goal-conditioned value function _V_ ( _s, g_ ) the GCRL policy _π_ ( _a|s, g_ ) must maximize. Given a goal g, initial state _s_ 0, the optimal policy _π_<sup>_∗_</sup> ( _a_<sup>_∗_</sup> _|s, g_ ), and the optimal trajectory _τ_<sup>_∗_</sup> = _{s_ 0 _, s_ 1 _, ..., sT_ = _g}_ induced by _π_<sup>_∗_</sup> , the optimal value function is monotonically non-decreasing along _τ_<sup>_∗_</sup> : _∀si, sj ∈ τ_<sup>_∗_</sup> _, V_<sup>_∗_</sup> ( _sj, g_ ) _≥ V_<sup>_∗_</sup> ( _si, g_ ) _⇐⇒ j ≥ i_ . However, non-monotonicity often arises in practice due to sampling or approximation errors (Park et al., 2023; Ahn et al., 2025). 

High non-monotonicity in _V_<sup>ˆ</sup> ( _s, g_ ) can cause the policy to get stuck in sub-optimal regions of the state space, especially when _g_ is distant from _s_ . We hypothesize that in long-horizon tasks, under sparse rewards, credit assignment becomes a challenge because _V_<sup>ˆ</sup> ( _s, g_ ) exhibits high nonmonotonicity, leading to poor policies. 

We now evaluate this hypothesis empirically using expert trajectories, each with a different length and a unique goal, on the sparse-reward **antmaze-giantnavigate** task from OGBench (Park et al., 2024a) used in Ahn et al. (2025). Trajectories are visualized in Appendix B.4. We analytically compute _V_<sup>ˆ</sup> ( _s, g_ ) as the discounted sum of rewards. By injecting multiplicative noise with variance _σv_<sup>2,wesimulateer-</sup> rors in value estimation: _V_<sup>ˆ</sup> ( _s, g_ ) _← r_ ( _s, a_<sup>_∗_</sup> _, g_ ) + _γ ∗_ � _V_ ˆ ( _s′, g_ ) + _ϵ ∗ V_ ˆ ( _s′, g_ )�, _ϵ ∼N_ (0 _, σv_<sup>2),with</sup> _γ_ = 0 _._ 99. We evaluate the quality of _V_<sup>ˆ</sup> ( _s_<sup>_′_</sup> _, g_ ) using _δV_ , the value non-monotonicity error, computed as the proportion of states along an expert trajectory where _V_<sup>ˆ</sup> ( _st_ +1 _, g_ ) _< V_<sup>ˆ</sup> ( _st, g_ ). 


Figure 3: Average _δV_ ( **y-axis** ) over 5 expert trajectories on **antmaze-giant-navigate** as a function of _σv_ ( **x-axis** ). _δV_ increases with _σv_ , denoting increasingly more noisy and non-monotonic _V_ ˆ ( ( _s, g_ ) under sparse rewards. under sparse rewards. 

Figure 3 plots average _δV_ over varying _σv_<sup>2while</sup> _V_ ˆ ( ( _s, g_ ) under sparse rewards. under sparse rewards. Fig. 4 plots _V_<sup>ˆ</sup> ( _s, g_ ) over 5 trajectories for _σv_ = 0 _._ 0005. The results indicate that under sparse rewards, _δV_ is high even under small _σv_ and increases with _σv_ and task horizon. This motivates the central question we aim to address: 

_How do we design reward functions that encode long-horizon temporal structure and thereby mitigate value non-monotonicity with effective credit assignment, leading to performative policies?_ 

### 4 OCCUPANCY REWARD SHAPING FOR OFFLINE GCRL 

First, we detail how we learn a generative model of the occupancy measure (Sec. 4.1). In Sec.4.2, we then show exactly how the occupancy measure encodes state geometry (Prop.1). This allows us to extract goal-reaching temporal information from the learned occupancy model into a reward-shaping term (Prop.2). We show that these “occupancyshaped” rewards preserve the optimal goal-reaching policy (Sec.4.3) and finally, we summarize our method in Sec.4.4. 

#### 4.1 LEARNING THE OCCUPANCY MEASURE 

The state-action conditioned occupancy measure over future states of the dataset policy _πD_ has the following recursive form (Sutton, 1995; Janner et al., 2020a; Schramm & Boularias, 2024): 


Figure 4: _V_ ˆ ( _s, g_ ) ( **y-axis** ) with sparse rewards vs time ( **x-axis** ) over 5 expert trajectories (each line a trajectory) from **antmaze-giant-navigate** . _V_ ˆ ( _s, g_ ) becomes increasingly noisy as we move away from goal towards the start of a trajectory (moving left on x-axis) even under small _σv_ . 

4 

Published as a conference paper at ICLR 2026 


This recursive form, reminiscent of temporal difference learning, allows learning _d_<sup>_πD_</sup> ( _s_<sup>+</sup> _| s, a_ ) parameterized by _θ_ as a mixture over two components: **1.** the transition function and **2.** a target _d_<sup>_πD_</sup> ( _s_<sup>+</sup> _| s_<sup>_′_</sup> _, a_<sup>_′_</sup> ) over subsequent future states under _πD_ (parameterized by _θ−_ , a time-delayed version of _θ_ ). This approach naturally stitches together future states under intersecting trajectories in _D_ . To accurately represent the multi-modality inherent in _d_<sup>_πD_</sup> and to enable efficient computation of the ORS reward function (explained in Sec. 4.2), we learn _d_<sup>_πD_</sup> using a flow matching model with the following loss (Farebrother et al., 2025) : 


where _Lnext_ ( _θ_ ) is the standard flow matching loss over the transition function and _Lfuture_ ( _θ_ ) regresses the velocity field _vθ_ ( _t, s, a, xt_ ) towards a bootstrapped estimate of the velocity field of _d_<sup>_π_</sup> _θ−_<sup>_D_(</sup><sup>_s_+</sup><sup>_|s′, a′_) represented by</sup><sup>_vθ−_(</sup><sup>_t, s′, a′, xt_).</sup><sup>**sg**represents the stop-gradient operation.</sup> 

#### 4.2 EXTRACTING TEMPORAL INFORMATION FROM THE OCCUPANCY MEASURE 

We now establish a precise connection between the occupancy measure and state space geometry. **Definition 1** (Shortest-path distance and level sets) **.** _Let step_<sup>_∗_</sup> ( _s, g_ ) _denote the minimum number of steps required to reach goal g from any state s_ ; _∀_ ( _s, g_ ) _∈D. We define the level sets:_ 


_Clearly, S_ 0 = _{g}. Under deterministic dynamics, for any s ∈Sk with k ≥_ 1 _, there exists an action a_<sup>_∗_</sup> _at state s such that the next-state distribution satisfies p_ ( _· | s, a_<sup>_∗_</sup> ) _⊆Sk−_ 1 _._ 

This characterization of distance from goal allows us to quantify how the occupancy measure encodes geometry in terms of the squared _Wasserstein-2 distance_ between _d_<sup>_πD_</sup> and _δg_ : 

**Proposition 1** (informal) **.** _Under suitable assumptions on goal reachability, dynamics, and dataset coverage, for all_ ( _s, a, g_ ) _∈D, the average squared Wasserstein-2 distance_ 


_is monotonically increasing with respect to the shortest-path layer index k. In particular, for a fixed goal g and any k ≥_ 1 _, if s_ 1 _∈Sk−_ 1 _and s_ 2 _∈Sk, then_ 


_Moreover, for any state–goal pair_ ( _s, g_ ) _, the squared Wasserstein-2 distance is minimized by the optimal action:_ 


The assumptions and proof are provided in Appendix A.3 and Appendix A.4. This formulation captures not only _how far_ the center of mass of _d_<sup>_πD_</sup> ( _s_<sup>+</sup> _| s, a_ )) is from _g_ , but also _how spread out d_<sup>_πD_</sup> ( _s_<sup>+</sup> _| s, a_ )) is with respect to _g_ : if state _A_ and state _B_ are both 5 transitions away from _g_ but _A_ has more future states that are farther away from the goal than _B_ , _W_ 2<sup>2(; ) will be lower for state</sup><sup>_B_.</sup> 

Intuitively, this means that by defining a reward _r_<sup>_W_</sup> ( _s, a, g_ ) = _−W_ 2<sup>2(</sup><sup>_δg, dπD_(</sup><sup>_s_+</sup><sup>_|s, a_)),wecan</sup> extract the state-space geometry as goal-reaching temporal information into a scalar value that is 

5 

Published as a conference paper at ICLR 2026 

**Algorithm 1:** Occupancy Reward Shaping. **Input:** Occupancy model _d_<sup>_π_</sup> _θ_<sup>_D_, reward function</sup><sup>_r_</sup> _ψ_<sup>_W_, learning rate</sup><sup>_η_</sup> // Training the occupancy model: **1 for** _each iteration t_ = 1 _to N_ **do 2** Sample ( _s, a, s_<sup>+</sup> ) _∼D_ ; **3** Compute _Lpretrain_ ( _θ_ ) (Eq. 8) and update _θ ← θ − η∇θLpretrain_ ( _θ_ ); **4 end 5 for** _each iteration t_ = 1 _to N_ **do 6** Sample ( _s, a, s_<sup>_′_</sup> _, a_<sup>_′_</sup> ) _∼D_ ; **7** Compute _Lflow_ ( _θ_ ) (Eq. 3) and update _θ ← θ − η∇θLflow_ ( _θ_ ); **8 end** // Training the reward function: **9 for** _each iteration t_ = 1 _to N_ **do 10** Sample ( _s, a, g_ ) _∼D_ ; **11** Compute _Lrew_ ( _ψ_ ) (Eq. 5) and update _ψ ← ψ − η∇ψLrew_ ( _ψ_ ); **12 end** 

higher for states with _s_<sup>+</sup> closer to _g_ under _D_ . Unlike prior works (Mezghani et al., 2023; Hartikainen et al., 2019), this reward-shaping term will directly capture global long-horizon information about goal-reachability. What remains is to compute _W_ 2<sup>2(</sup><sup>_δg, dπD_(</sup><sup>_s_+</sup><sup>_|s, a_)).While exact compu-</sup> tation involves an intractable integral, we show how to estimate _r_<sup>_W_</sup> ( _s, a, g_ ) using the velocity field corresponding to _d_<sup>_π_</sup> _θ_<sup>_D_(</sup><sup>_s_+</sup><sup>_| s, a_)):</sup> 

**Proposition 2.** _The squared Wasserstein-2 distance between δg and d_<sup>_πD_</sup> ( _s_<sup>+</sup> _| s, a_ ) _is upper bounded, up to a multiplicative constant C >_ 0 _, by the mean squared error of the associated velocity field corresponding to d_<sup>_πD_</sup> ( _s_<sup>+</sup> _| s, a_ ) _and the target velocity corresponding to δg:_ 


_where xt_ = _tx_ 1 + (1 _− t_ ) _x_ 0 _._ 

where _v_ ( _t, s, a, xt_ ) is the velocity field corresponding to _d_<sup>_πD_</sup> ( _s_<sup>+</sup> _|s, a_ ) at time _t_ . The proof is in Appendix A.5. As mentioned in Sec. 4.1, this further justifies our choice of using a flow matching model to learn _d_<sup>_πD_</sup> . Using the learned _d_<sup>_π_</sup> _θ_<sup>_D_</sup> from Sec. 4.1, we can now learn _r_<sup>_W_</sup> ( _s, a, g_ ) using a neural network _ψ_ . Notably, this does not involve running an ODE solver for multiple time-steps: 


#### 4.3 ORS PRESERVES THE OPTIMAL POLICY 

It remains unclear whether using _rW_ from Sec.4.2, one can learn the same optimal policy as with sparse rewards, as it is estimated using the _dataset occupancy measure d_<sup>_πD_</sup> . 

**Theorem 1.** _Under suitable assumptions on goal reachability, dynamics, and dataset coverage, the greedy goal-conditioned policy:_ 


_where Q_<sup>_∗_</sup> ( _s, a, g_ ) _denotes the optimal action-value function induced by the reward r_<sup>_W_</sup> ( _s, a, g_ ) _, coincides with the optimal shortest-path policy π_<sup>_∗_</sup> ( _a | s, g_ ) _._ 

Please refer to Appendix A.6 for the proof. ORS thus enables efficient use of the rich goal-reaching information present in the dataset occupancy measure without having to estimate the new occupancy measure at each intermediate policy improvement step. 

6 

Published as a conference paper at ICLR 2026 

#### 4.4 METHOD SUMMARY 

ORS has 3 stages: **1.** Train the flow matching occupancy model _d_<sup>_π_</sup> _θ_<sup>_D_</sup> using Eq. 3; **2.** Train the reward function _rψ_<sup>_W_using Eq. 5; and</sup><sup>**3.**Train a goal-conditioned policy using any offline GCRL algorithm</sup> that uses a TD-learning critic. Stages 1 and 2 that involve learning _d_<sup>_π_</sup> _θ_<sup>_D_</sup> and _rψ_<sup>_W_are summarized in</sup> Alg. 1. Details on architecture and hyperparameters are provided in Appendix B.6. 

### 5 EXPERIMENTS 

In this section, we present an extensive empirical analysis of ORS across a variety of challenging long-horizon offline GCRL tasks. We then conduct detailed analyses and ablations to dissect key design choices underlying our algorithm. 

**_Tasks:_** For our empirical analysis, we primarily use OGBench (Park et al., 2024a), a benchmark specifically built for evaluating offline GCRL algorithms. We choose OGBench over older benchmarks such as Fu et al. (2020); Tarasov et al. (2023) for its task diversity, challenging long-horizon sparse-reward tasks that are unsaturated as of 2025, and comprehensive multi-goal evaluation. 

OGBench tasks are broadly categorized into 4 types: maze navigation, cube manipulation, puzzle manipulation, and scene tasks. We select tasks with varying levels of task complexity and planning horizon. from OGBench to be representative of these 4 categories. Within each category, we include tasks of varying complexity (e.g., cube-double and cube-triple) and varying dataset quality (e.g., cube-triple-play and cube-triple-noisy). We provide a detailed explanation of tasks in Appendix B.1. 

To demonstrate effectiveness in real-world settings, we evaluate ORS on actuator control tasks in a nuclear fusion reactor called a Tokamak. We use raw sensor and actuator data collected from the DIII-D tokamak located in San Diego, CA, USA. ORS controls 4 actuators that influence evolution of plasma in the Tokamak, a system characterized by highly non-linear, stochastic dynamics and complex physics. We evaluate over 3 separate tasks, each tracking a certain scalar or profile state variable: _βN_ (normalized ratio between plasma pressure and magnetic pressure), Electron density and Ion rotation. These quantities critically influence plasma stability and overall power output required for commercially viable nuclear fusion. Please refer to Appendix B.2 for further details. 

**_Baselines:_** We compare ORS against a set of representative baselines. These include Goal Conditioned Behavioral Cloning ( **GCBC** ) (Ghosh et al., 2019); Goal-Conditioned Implicit Q Learning ( **GCIQL** ) (Kostrikov et al., 2021) and Goal-Conditioned Implicit Value Learning ( **GCIVL** ) (Park et al., 2023) which approximate value functions using expectile regression (Newey & Powell, 1987) and recover policies using behavior-constrained deterministic policy gradient (DDPG + BC) and advantage-weighted regression (AWR), respectively (Park et al., 2024b). Quasimetric RL ( **QRL** ) (Wang et al., 2023a) learns a specialized quasimetric goal-conditioned value function with a dual objective. Contrastive RL ( **CRL** ) (Eysenbach et al., 2022) fits a Monte Carlo goal-conditioned value function using contrastive learning and extracts a greedy policy from it. 

We also compare ORS to several methods designed for long-horizon, sparse-reward settings. **GoFresh** (Mezghani et al., 2023) learns a shaped reward as a sum of a local reward from a temporal distance classifier between states and a global reward computed by shortest-path search on a graph constructed with the local distance classifier. **SMORE** (Sikchi et al., 2023a) is an occupancymatching method that uses dual RL to learn unnormalized densities that reflect the distance to goal. 

Hierarchical Implicit Q Learning ( **HIQL** ) (Park et al., 2023) trains a low-level policy to reach goals sampled from a high-level policy, both trained via a single GCIVL-style value function. Subgoal Advantage-Weighted Policy Bootstrapping ( **SAW** ) (Zhou & Kao, 2025) improves over HIQl by training a non-hierarchical goal-conditioned policy by bootstrapping on subgoal-conditioned policies with advantage-weighted importance sampling. **n-step GCIQL** and **GCIQL-OTA** use different techniques to learn a GCIQL critic using n-step TD learning (De Asis et al., 2018; Ahn et al., 2025). These baselines ensure a standalone comparison of our method against two key strategies to horizon reduction in RL. Both ORS and Go-Fresh use GCIQL with a Gaussian policy, owing to its popularity and simplicity and to ensure fair comparison. We build on the codebase of OGBench and make use of the official implementation for Go-Fresh. All algorithms use hindsight relabeling (Kaelbling, 

7 

Published as a conference paper at ICLR 2026 

Table 1: ORS vs baselines: Overall average (binary) success rate (%) across the 5 testtime goals over 8 seeds per task per algorithm. We report the 95% bootstrapped C.I. size after the ± sign. 

|**Dataset**|**GCBC**|**GC-IVL**|**QRL**|**CRL**|**GC-IQL**|**Go-Fresh**|**ORS (ours)**|
|---|---|---|---|---|---|---|---|
|antmaze-large-navigate|25_±_3|18_±_3|64_±_18|**90**_±_**4**|34_±_4|**88**_±_**3**|**88**_±_**7**|
|antmaze-giant-navigate|0_±_0|0_±_0|9_±_4|39_±_8|0_±_0|30_±_10|**56**_±_**9**|
|cube-double-play|1_±_1|36_±_3|1_±_0|10_±_2|**40**_±_**5**|17_±_6|**45**_±_**7**|
|cube-triple-play|0_±_0|1_±_1|0_±_0|6_±_3|7_±_3|18_±_5|**37**_±_**8**|
|puzzle-4x4-play|0_±_0|13_±_2|0_±_0|0_±_0|26_±_3|**74**_±_**6**|**70**_±_**5**|
|puzzle-4x5-play|0_±_0|7_±_1|0_±_0|1_±_0|14_±_1|**20**_±_**1**|**20**_±_**0**|
|puzzle-4x6-play|0_±_0|10_±_2|0_±_0|4_±_1|12_±_1|17_±_4|**20**_±_**2**|
|scene-play|5_±_1|42_±_4|5_±_1|19_±_2|51_±_4|56_±_10|**80**_±_**4**|
|antmaze-large-explore|0_±_0|8_±_6|0_±_0|0_±_0|1_±_1|**38**_±_**10**|22_±_7|
|cube-triple-noisy|1_±_1|9_±_1|1_±_0|3_±_1|2_±_1|5_±_4|**22**_±_**7**|
|puzzle-4x4-noisy|0_±_0|20_±_3|0_±_0|0_±_0|29_±_7|**50**_±_**5**|**56**_±_**7**|
|puzzle-4x6-noisy|0_±_0|17_±_2|0_±_0|6_±_3|**18**_±_**2**|**19**_±_**4**|**19**_±_**1**|
|scene-noisy|1_±_1|26_±_5|9_±_1|1_±_1|26_±_2|34_±_5|**40**_±_**5**|
|**Mean**|2.5|15.9|6.9|13.7|20.0|35.8|**44.2**|


1993; Andrychowicz et al., 2017). Appendix B.3-B.8 provides additional information on baselines, hyperparameters used and wall-clock time. 

#### 5.1 RESULTS 

Performance on OGBench is measured by average (binary) success rates on 5 test-time goals of each task. We train algorithms to convergence and average the results over **8 seeds** . We list the number of training iterations per task in Appendix B.5. Performance on Tokamak tasks is measured as the cumulative reward per episode, where reward is the L2 distance between the goal variables to track and the actual achieved quantities. On Tokamak tasks, we evaluate on 10 test-time goals over **4 seeds** . We discuss the results below: 

**_How effective is ORS?_** ORS achieves the best performance on most tasks, with especially large gains on more complex domains. Table 1 summarizes results over 12 offline locomotion and manipulation datasets, where ***-play/*-navigate** denote noisy expert datasets and ***-noisy/*-explore** denote highly sub-optimal datasets (Park et al., 2024a). ORS achieves a **2** _._ **2** _×_ **improvement in performance on average** over its base algorithm GCIQL that uses sparse rewards. While we see that GCIQL/GCIVL struggle on locomotion and QRL/CRL struggle on manipulation, ORS consistently outperforms these baselines on both domains. ORS outperforms Go-Fresh on the majority of tasks, demonstrating the effectiveness of occupancy-based reward shaping over graph-based reward shaping, especially in complex tasks such as **antmaze-giant-navigate** and **cube-triple-play** that are characterized by long horizons upto 2000 steps long (Park et al., 2024a). We also see that ORS remains effective even under highly sub-optimal data in the ***-noisy/*-explore** datasets. Notably, only ORS and Go-Fresh produce non-zero performance on **antmaze-large-explore** . Although GoFresh outperforms ORS on this task, we hypothesize that this could be because the additional local rewards used by Go-Fresh are effective in such a task. 

**_How does ORS compare to other strategies for long-horizon, sparse-reward offline GCRL?_** On average, ORS outperforms the next-best method GO-Fresh by 24% and achieves 2.2 _×_ and 1.9 _×_ high performance than hierarchical (HIQL) and n-step return approaches(GCIQL-OTA), respectively. From Table 2, we see that while hierarchical or policy-bootstrapped-based methods like HIQL and SAW are effective on antmaze locomotion but struggle on manipulation tasks. SMORE is largely ineffective with a mean performance of just 2.8% while n-step return methods perform poorly on noisy datasets. In contrast, the strong performance of ORS with a simple non-hierarchical policy underscores the effectiveness of its occupancy-based reward shaping. 

**_Is ORS effective in real-world tasks?_** We now examine the ability of ORS to track goals by controlling actuators in real-world Tokamak control tasks. Table 3 compares ORS with baselines specifically designed for long-horizon, sparse-reward offline GCRL. While HIQL and SAW perform relatively well for rotation control, they perform poorly on other tasks. While SMORE performs poorly 

8 

Published as a conference paper at ICLR 2026 

overall, both n-step GCIQL and GCIQL-OTA perform well on density control but show poor performance on other tasks. GO-Fresh performs poorly overall on all tasks; we believe this is because graph-based reward shaping is ineffective in tasks with stochastic dynamics. ORS consistently achieves best performance across the Tokamak control, highlighting its effectiveness in complex real-world tasks. 


Figure 5: **Left:** ORS leads to _lower average value non-monotonicity δV_ at lower noise levels ( _σv_ ) over expert trajectories compared to using sparse rewards or just using _V_<sup>ˆ</sup> ( _, g_ ) = _rW_ ( _s, g_ ); **Center:** ORS induces _less noisy estimates_ of _V_<sup>ˆ</sup> ( _s, g_ ) over expert trajectories even for long horizons; and **Right:** ORS rewards over 5000 state-action pairs (denoted as dots) for a single fixed goal (denoted as **x** ) _smoothly decay in magnitude_ with temporal distance from goal. All plots in this figure are computed over **antmaze-giant-navigate** . 

**_How does ORS influence value learning?_** We analyze how ORS influences the learning dynamics of the induced value function on **antmaze-giant-navigate** _by improving credit assignment_ . Following the setup in Sec. 3.2, we analytically compute _V_<sup>ˆ</sup> ( _s, g_ ) induced by ORS rewards under varying noise levels _σv_ . Figure 5 **(left)** reports how the average _δV_ varies with _σv_ for sparse rewards, ORS, and a variant that directly uses _V_<sup>ˆ</sup> ( _s, g_ ) = _r_<sup>_W_</sup> ( _s, g_ ). Relative to sparse rewards, ORS exhibits _δV_ that is an order of magnitude smaller at lower noise levels. We plot the approximate value function _V_<sup>ˆ</sup> ( _s, g_ ) induced by ORS over the same 5 trajectories in Sec. 3.2 in Fig. 5 **(center)** , showing estimates that are much less noisy than sparse-reward _V_<sup>ˆ</sup> ( _s, g_ ) over long horizons. 

Finally, Figure 5 **(right)** plots ORS rewards for a fixed goal over 5000 uniformly sampled stateaction pairs, each state displayed in the figure by its x-y position in the maze. ORS reward magnitudes decay smoothly with increasing temporal distance from goal, with dark dots corresponding to states (eg. ends of trajectories) very distant from goal. 

**_How do different design choices affect ORS?_** We now examine some key design choices behind ORS. First, we compare ORS with a baseline called L2 that computes the uses L2 distance to goal for reward shaping. Table 4 shows that L2 rewards are ineffective and can hurt performance as shown by GCIQL with L2 rewards performing worse than sparse-reward GCIQL. 

Table 2: ORS vs long-horizon sparse-reward offline GCRL strategies on OGBench tasks: Overall average (binary) success rate (%) across the 5 test time goals over 8 seeds per task per algorithm. We report the 95% bootstrapped C.I. size after the ± sign. 

|**Dataset**|**HIQL**|**SAW**|**SMORE**|**n-step GCIQL**|**GCIQL-OTA**|**Go-Fresh**|**ORS (ours)**|
|---|---|---|---|---|---|---|---|
|antmaze-large-navigate|**91**_±_**2**|86_±_5|22_±_5|53_±_9|90_±_4|88_±_3|88_±_7|
|antmaze-giant-navigate|**72**_±_**7**|48_±_9|1_±_1|1_±_1|26_±_5|30_±_10|56_±_9|
|cube-double-play|6_±_2|**40**_±_**7**|2_±_2|4_±_3|3_±_2|17_±_6|**45**_±_**7**|
|cube-triple-play|3_±_2|6_±_6|0_±_0|1_±_1|2_±_2|18_±_5|**37**_±_**8**|
|puzzle-4x4-play|7_±_2|17_±_12|0_±_0|46_±_5|**85**_±_**4**|74_±_6|70_±_5|
|puzzle-4x5-play|8_±_4|8_±_4|0_±_0|5_±_2|19_±_1|**20**_±_**1**|**20**_±_**0**|
|puzzle-4x6-play|3_±_1|8_±_4|0_±_0|14_±_3|15_±_3|17_±_4|**20**_±_**2**|
|scene-play|38_±_3|63_±_6|8_±_2|26_±_7|42_±_7|56_±_10|**80**_±_**4**|
|antmaze-large-explore|0_±_0|15_±_8|0_±_0|0_±_0|0_±_0|**38**_±_**10**|22_±_7|
|cube-triple-noisy|2_±_1|0_±_0|1_±_1|2_±_1|2_±_1|5_±_4|**22**_±_**7**|
|puzzle-4x4-noisy|3_±_3|3_±_3|0_±_0|0_±_0|0_±_0|**50**_±_**5**|**56**_±_**7**|
|puzzle-4x6-noisy|2_±_1|8_±_6|0_±_0|12_±_6|15_±_3|**19**_±_**4**|**19**_±_**1**|
|scene-noisy|25_±_4|33_±_6|3_±_2|2_±_2|3_±_2|34_±_5|**40**_±_**5**|
|**Mean**|20.0|25.8|2.8|12.7|23.2|35.8|**44.2**|


9 

Published as a conference paper at ICLR 2026 

Table 3: ORS vs long-horizon sparse-reward offline GCRL strategies on 3 challenging Tokamak control tasks: Overall average cumulative return across 10 testtime goals over 4 seeds per task per algorithm. We report the 95% bootstrapped C.I. size after the ± sign. 

|**Task**|**HIQL**|**SAW**|**SMORE**|**n-step GCIQL**|**GCIQL-OTA**|**GO-Fresh**|**ORS**|
|---|---|---|---|---|---|---|---|
|Tokamak_βN_|**-45.26**_±_**3.83 **|**-51.39**_±_**8.16**|_−_56_._06_±_12_._71|_−_88_._7_±_44_._3|_−_67_._73_±_9_._73|**-48.20**_±_**11.72 **|**-44.76**_±_**8.42**|
|Tokamak density|_−_49_._8_±_7_._5|_−_44_._0_±_2_._3|_−_54_._0_±_10_._8|**-25.6**_±_**4.1**|**-27.1**_±_**2.5**|_−_38_._6_±_12_._6|**-26.9**_±_**6.6**|
|Tokamak rotation|_−_24_._4_±_1_._3|_−_26_._4_±_5_._1|_−_28_._5_±_6_._7|_−_57_._4_±_46_._6|_−_30_._1_±_6_._9|_−_28_._9_±_7_._4|**-22.4**_±_**0.6**|


Next, we ablate over design choices of the ORS reward function and _Q_ - function by comparing ORS against a version that uses state-only rewards _rW_ ( _s, g_ ) named ORS-s and a variant that uses the reward function itself as 

|**Dataset**|**ORS**|**L2**|**GCIQL**|
|---|---|---|---|
|antmaze-giant-navigate|56_±_9|3_±_2|0_±_0|
|cube-triple-play|37_±_8|3_±_1|7_±_3|


Table 4: ORS vs L2 rewards 

the _Q_ -function, i.e., _Q_ ( _s, a, g_ ) = _rW_ ( _s, a, g_ ) named ORS-r. We keep the base algorithm the same. 


Figure 6: ORS **vs** ORS-s **vs** ORS-r over 5 testtime goals and 8 seeds on **scene-play** (error bars show 95% bootstrapped CI) 

In experiments on the manipulation task **scene-play** in Fig. 6, ORS performs best, showing the importance of learning a _Q_ -function that is a cumulative sum over _rW_ ( _s, a, g_ ), especially when the task involves stitching over trajectories to learn the optimal _Q_<sup>_∗_</sup> . We hypothesize that the poor performance of ORS-r is due to noisy estimates of the _Q_ function, as evidenced by our analysis in Fig. 5. 

We also ablate the performance of ORS over varying values of the expectile parameter _κ_ of GCIQL which is crucially linked to the density of rewards (Kostrikov et al., 2021). The results in Table 5 show higher performance at lower _κ_ in locomotion 

tasks. We hypothesize that this is due to the rich learning signal from dense rewards of ORS. In manipulation tasks, as task complexity increases, the _κ_ at which we get best performance increases. 

|6<br>CONCLUSION|**Dataset**<br>_κ_**=0.6**|_κ_**=0.75**|_κ_**=0.9**|
|---|---|---|---|
||antmaze-giant-navigate<br>56_±_9<br><br>|15_±_6|1_±_1|
|In this paper, we show how generative|puzzle-4x4-play<br>70_±_5<br><br>|40_±_4<br>|21_±_3<br>|
|<br>world models implicitly capture world<br>geometry and introduce Occupancy Re-<br>ward Shaping, a novel reward-shaping<br>method for offline GCRL that utilizes a|scene-play<br>70_±_5<br>cube-triple-play<br>4_±_3<br>Table 5: Performance of ORS over|80_±_4<br>27_±_12<br>varying v|71_±_7<br>37_±_8<br>alues of_κ_.|
|generative occupancy model to extract global<br>ward function. Unlike prior work that relies <br>complexity and enables learning performative<br>plement on top of existing GCRL algorithms<br>tasks, including real-world Tokamak control.|goal-reaching information into<br> on graph-building, ORS scale<br>policies over diverse datasets. <br>and achieves state-of-the-art re|a goal-c<br>s effectiv<br> ORS is<br>sults ove|onditioned re-<br>ely with task<br>simple to im-<br>r challenging|


**Limitations.** Reward shaping methods, by virtue of being sample-based, are less effective in longhorizon tasks with highly combinatorial state spaces and very few ways to achieve task success (e.g. a large multi-step combination lock puzzle). In such regimes, particularly in the offline setting, even ORS rewards may provide limited signal since the occupancy measure has a high Wasserstein distance from goal for almost all states. This challenge could potentially be addressed by learning an occupancy measure over a filtered set of “useful” future states and by augmenting the ORS reward with local rewards that capture short-range state dependencies. 

#### ACKNOWLEDGEMENTS 

We would like to thank Grace Liu and Mahsa Bastankhah for reviewing the paper. This material is based upon work supported in part by the U.S. Department of Energy, Office of Fusion Energy 

10 

Published as a conference paper at ICLR 2026 

Sciences, under Award DE-SC0024544 and on work supported by the National Science Foundation under Award No. 2441665. Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation. 

**LLM usage:** We used LLMs to aid in LaTeX formatting while writing the paper. 

**Reproducibility Statement:** We make our code available on Github. To ensure reliable comparison, each RL algorithm is evaluated over 8 random seeds and 95% bootstrapped CIs are reported as error bars in tables and plots. Additional information on baselines is provided in Appendix B.2B.6. We state this information in Sec. 5.1 of the main paper. All proofs are in Appendix A and assumptions are stated in Appendix A.3. We state this in Sec. 4.2 of the main paper. 

### REFERENCES 

- Joseph Abbate, Rory Conlin, and Egemen Kolemen. Data-driven profile prediction for diii-d. _Nuclear Fusion_ , 61(4):046027, 2021. 

- Siddhant Agarwal, Ishan Durugkar, Peter Stone, and Amy Zhang. f-policy gradients: A general framework for goal-conditioned rl using f-divergences. _Advances in Neural Information Processing Systems_ , 36:12100–12123, 2023. 

- Hongjoon Ahn, Heewoong Choi, Jisu Han, and Taesup Moon. Option-aware temporally abstracted value for offline goal-conditioned reinforcement learning. _arXiv preprint arXiv:2505.12737_ , 2025. 

- Marcin Andrychowicz, Filip Wolski, Alex Ray, Jonas Schneider, Rachel Fong, Peter Welinder, Bob McGrew, Josh Tobin, OpenAI Pieter Abbeel, and Wojciech Zaremba. Hindsight experience replay. _Advances in neural information processing systems_ , 30, 2017. 

- Tim Brys, Anna Harutyunyan, Halit Bener Suay, Sonia Chernova, Matthew E Taylor, and Ann Now´e. Reinforcement learning from demonstration through shaping. In _IJCAI_ , pp. 3352–3358, 2015. 

- Elliot Chane-Sane, Cordelia Schmid, and Ivan Laptev. Goal-conditioned reinforcement learning with imagined subgoals. In _International conference on machine learning_ , pp. 1430–1440. PMLR, 2021. 

- Ian Char, Joseph Abbate, L´aszl´o Bard´oczi, Mark Boyer, Youngseog Chung, Rory Conlin, Keith Erickson, Viraj Mehta, Nathan Richner, Egemen Kolemen, et al. Offline model-based reinforcement learning for tokamak control. In _Learning for Dynamics and Control Conference_ , pp. 1357–1372. PMLR, 2023. 

- Ian Char, Youngseog Chung, Joseph Abbate, Egemen Kolemen, and Jeff Schneider. Full shot predictions for the diii-d tokamak via deep recurrent networks. _arXiv preprint arXiv:2404.12416_ , 2024. 

- Kristopher De Asis, J Hernandez-Garcia, G Holland, and Richard Sutton. Multi-step reinforcement learning: A unifying algorithm. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 32, 2018. 

- Yiming Ding, Carlos Florensa, Pieter Abbeel, and Mariano Phielipp. Goal-conditioned imitation learning. _Advances in neural information processing systems_ , 32, 2019. 

- Ishan Durugkar, Mauricio Tec, Scott Niekum, and Peter Stone. Adversarial intrinsic motivation for reinforcement learning. _Advances in Neural Information Processing Systems_ , 34:8622–8636, 2021. 

- Benjamin Eysenbach, Tianjun Zhang, Sergey Levine, and Russ R Salakhutdinov. Contrastive learning as goal-conditioned reinforcement learning. _Advances in Neural Information Processing Systems_ , 35:35603–35620, 2022. 

11 

Published as a conference paper at ICLR 2026 

- Jesse Farebrother, Matteo Pirotta, Andrea Tirinzoni, R´emi Munos, Alessandro Lazaric, and Ahmed Touati. Temporal difference flows. _arXiv preprint arXiv:2503.09817_ , 2025. 

- Justin Fu, Aviral Kumar, Ofir Nachum, George Tucker, and Sergey Levine. D4rl: Datasets for deep data-driven reinforcement learning. _arXiv preprint arXiv:2004.07219_ , 2020. 

- Scott Fujimoto and Shixiang Shane Gu. A minimalist approach to offline reinforcement learning. _Advances in neural information processing systems_ , 34:20132–20145, 2021. 

- Dibya Ghosh, Abhishek Gupta, Justin Fu, Ashwin Reddy, Coline Devin, Benjamin Eysenbach, and Sergey Levine. Learning to reach goals without reinforcement learning. 2019. 

- Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In _International conference on machine learning_ , pp. 1861–1870. Pmlr, 2018. 

- Kristian Hartikainen, Xinyang Geng, Tuomas Haarnoja, and Sergey Levine. Dynamical distance learning for semi-supervised and unsupervised skill discovery. _arXiv preprint arXiv:1907.08225_ , 2019. 

- Kristian Hartikainen, Xinyang Geng, Tuomas Haarnoja, and Sergey Levine. Dynamical distance learning for semi-supervised and unsupervised skill discovery, 2020. URL https://arxiv. org/abs/1907.08225. 

- Anna Harutyunyan, Sam Devlin, Peter Vrancx, and Ann Now´e. Expressing arbitrary reward functions as potential-based advice. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 29, 2015. 

- Joey Hejna, Jensen Gao, and Dorsa Sadigh. Distance weighted supervised learning for offline interaction data. In _International Conference on Machine Learning_ , pp. 12882–12906. PMLR, 2023. 

- Dan Hendrycks and Kevin Gimpel. Gaussian error linear units (gelus). _arXiv preprint arXiv:1606.08415_ , 2016. 

- Michael Janner, Igor Mordatch, and Sergey Levine. Gamma-models: Generative temporal difference learning for infinite-horizon prediction. _Advances in neural information processing systems_ , 33: 1724–1735, 2020a. 

- Michael Janner, Igor Mordatch, and Sergey Levine. Generative temporal difference learning for infinite-horizon prediction. _arXiv preprint arXiv:2010.14496_ , 2020b. 

- Zhengyao Jiang, Tianjun Zhang, Michael Janner, Yueying Li, Tim Rockt¨aschel, Edward Grefenstette, and Yuandong Tian. Efficient planning in a compact latent action space. _arXiv preprint arXiv:2208.10291_ , 2022. 

- Leslie Pack Kaelbling. Learning to achieve goals. In _IJCAI_ , volume 2, pp. 1094–8, 1993. 

- Bingyi Kang, Zequn Jie, and Jiashi Feng. Policy optimization with demonstrations. In _International conference on machine learning_ , pp. 2469–2478. PMLR, 2018. 

- Diederik P Kingma and Jimmy Ba. Adam: A method for stochastic optimization. _arXiv preprint arXiv:1412.6980_ , 2014. 

- Ilya Kostrikov, Ashvin Nair, and Sergey Levine. Offline reinforcement learning with implicit q- learning. _arXiv preprint arXiv:2110.06169_ , 2021. 

- Mingxuan Li, Junzhe Zhang, and Elias Bareinboim. Automatic reward shaping from confounded offline data. _arXiv preprint arXiv:2505.11478_ , 2025. 

- Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- Yaron Lipman, Marton Havasi, Peter Holderrieth, Neta Shaul, Matt Le, Brian Karrer, Ricky TQ Chen, David Lopez-Paz, Heli Ben-Hamu, and Itai Gat. Flow matching guide and code. _arXiv preprint arXiv:2412.06264_ , 2024. 

12 

Published as a conference paper at ICLR 2026 

- Minghuan Liu, Menghui Zhu, and Weinan Zhang. Goal-conditioned reinforcement learning: Problems and solutions. _arXiv preprint arXiv:2201.08299_ , 2022a. 

- Xingchao Liu, Chengyue Gong, and Qiang Liu. Flow straight and fast: Learning to generate and transfer data with rectified flow. _arXiv preprint arXiv:2209.03003_ , 2022b. 

- Lei Lv, Yunfei Li, Yu Luo, Fuchun Sun, Tao Kong, Jiafeng Xu, and Xiao Ma. Flow-based policy for online reinforcement learning. _arXiv preprint arXiv:2506.12811_ , 2025. 

- Haozhe Ma, Zhengding Luo, Thanh Vinh Vo, Kuankuan Sima, and Tze-Yun Leong. Highly efficient self-adaptive reward shaping for reinforcement learning. _arXiv preprint arXiv:2408.03029_ , 2024. 

- Jason Yecheng Ma, Jason Yan, Dinesh Jayaraman, and Osbert Bastani. Offline goal-conditioned reinforcement learning via _f_ -advantage regression. _Advances in neural information processing systems_ , 35:310–323, 2022. 

- Marlos C Machado, Andre Barreto, Doina Precup, and Michael Bowling. Temporal abstraction in reinforcement learning with the successor representation. _Journal of machine learning research_ , 24(80):1–69, 2023. 

- Lina Mezghani, Sainbayar Sukhbaatar, Piotr Bojanowski, Alessandro Lazaric, and Karteek Alahari. Learning goal-conditioned policies offline with self-supervised reward shaping. In _Conference on robot learning_ , pp. 1401–1410. PMLR, 2023. 

- David Mguni, Jianhong Wang, Taher Jafferjee, Nicolas Perez-Nieves, Wenbin Song, Yaodong Yang, Feifei Tong, Hui Chen, Jiangcheng Zhu, Yali Du, et al. Learning to shape rewards using a game of switching controls. _arXiv preprint arXiv:2103.09159_ , 2021. 

- Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Andrei A Rusu, Joel Veness, Marc G Bellemare, Alex Graves, Martin Riedmiller, Andreas K Fidjeland, Georg Ostrovski, et al. Human-level control through deep reinforcement learning. _nature_ , 518(7540):529–533, 2015. 

- Whitney K Newey and James L Powell. Asymmetric least squares estimation and testing. _Econometrica: Journal of the Econometric Society_ , pp. 819–847, 1987. 

- Andrew Y Ng, Daishi Harada, and Stuart Russell. Policy invariance under reward transformations: Theory and application to reward shaping. In _Icml_ , volume 99, pp. 278–287. Citeseer, 1999. 

- Seohong Park, Dibya Ghosh, Benjamin Eysenbach, and Sergey Levine. Hiql: Offline goalconditioned rl with latent states as actions. _Advances in Neural Information Processing Systems_ , 36:34866–34891, 2023. 

- Seohong Park, Kevin Frans, Benjamin Eysenbach, and Sergey Levine. Ogbench: Benchmarking offline goal-conditioned rl. _arXiv preprint arXiv:2410.20092_ , 2024a. 

- Seohong Park, Kevin Frans, Sergey Levine, and Aviral Kumar. Is value learning really the main bottleneck in offline rl? _Advances in Neural Information Processing Systems_ , 37:79029–79056, 2024b. 

- Seohong Park, Tobias Kreiman, and Sergey Levine. Foundation policies with hilbert representations. _arXiv preprint arXiv:2402.15567_ , 2024c. 

- Seohong Park, Qiyang Li, and Sergey Levine. Flow q-learning. _arXiv preprint arXiv:2502.02538_ , 2025. 

- Deepak Pathak, Pulkit Agrawal, Alexei A Efros, and Trevor Darrell. Curiosity-driven exploration by self-supervised prediction. In _International conference on machine learning_ , pp. 2778–2787. PMLR, 2017. 

- Martin L Puterman. _Markov decision processes: discrete stochastic dynamic programming_ . John Wiley & Sons, 2014. 

- Jette Randløv and Preben Alstrøm. Learning to drive a bicycle using reinforcement learning and shaping. In _ICML_ , volume 98, pp. 463–471, 1998. 

13 

Published as a conference paper at ICLR 2026 

- Alfredo Reichlin, Miguel Vasco, Hang Yin, and Danica Kragic. Learning goal-conditioned policies from sub-optimal offline data via metric learning. _arXiv preprint arXiv:2402.10820_ , 2024. 

- Lisa M Saksida, Scott M Raymond, and David S Touretzky. Shaping robot behavior using principles from instrumental conditioning. _Robotics and Autonomous Systems_ , 22(3-4):231–249, 1997. 

- Nikolay Savinov, Alexey Dosovitskiy, and Vladlen Koltun. Semi-parametric topological memory for navigation. _arXiv preprint arXiv:1803.00653_ , 2018. 

- Tom Schaul, Daniel Horgan, Karol Gregor, and David Silver. Universal value function approximators. In _International conference on machine learning_ , pp. 1312–1320. PMLR, 2015. 

- Liam Schramm and Abdeslam Boularias. Bellman diffusion models. _arXiv preprint arXiv:2407.12163_ , 2024. 

- Harshit Sikchi, Rohan Chitnis, Ahmed Touati, Alborz Geramifard, Amy Zhang, and Scott Niekum. Score models for offline goal-conditioned reinforcement learning. In _The Twelfth International Conference on Learning Representations_ , 2023a. 

- Harshit Sikchi, Qinqing Zheng, Amy Zhang, and Scott Niekum. Dual rl: Unification and new methods for reinforcement and imitation learning. _arXiv preprint arXiv:2302.08560_ , 2023b. 

- Richard S Sutton. Td models: Modeling the world at a mixture of time scales. In _Machine learning proceedings 1995_ , pp. 531–539. Elsevier, 1995. 

- Denis Tarasov, Vladislav Kurenkov, Alexander Nikulin, and Sergey Kolesnikov. Revisiting the minimalist approach to offline reinforcement learning. _Advances in Neural Information Processing Systems_ , 36:11592–11620, 2023. 

- Michael L Walker, Peter De Vries, Federico Felici, and Eugenio Schuster. Introduction to tokamak plasma control. In _2020 American Control Conference (ACC)_ , pp. 2901–2918. IEEE, 2020. 

- Tongzhou Wang, Antonio Torralba, Phillip Isola, and Amy Zhang. Optimal goal-reaching reinforcement learning via quasimetric learning. In _International Conference on Machine Learning_ , pp. 36411–36430. PMLR, 2023a. 

- Yiming Wang, Ming Yang, Renzhi Dong, Binbin Sun, Furui Liu, et al. Efficient potential-based exploration in reinforcement learning using inverse dynamic bisimulation metric. _Advances in Neural Information Processing Systems_ , 36:38786–38797, 2023b. 

- Rui Yang, Yiming Lu, Wenzhe Li, Hao Sun, Meng Fang, Yali Du, Xiu Li, Lei Han, and Chongjie Zhang. Rethinking goal-conditioned supervised learning and its connection to offline rl. _arXiv preprint arXiv:2202.04478_ , 2022. 

- Rui Yang, Lin Yong, Xiaoteng Ma, Hao Hu, Chongjie Zhang, and Tong Zhang. What is essential for unseen goal generalization of offline goal-conditioned rl? In _International Conference on Machine Learning_ , pp. 39543–39571. PMLR, 2023. 

- Rui Yu, Shenghua Wan, Yucen Wang, Chen-Xiao Gao, Le Gan, Zongzhang Zhang, and DeChuan Zhan. Reward models in deep reinforcement learning: A survey. _arXiv preprint arXiv:2506.15421_ , 2025. 

- Wenhao Zhan, Baihe Huang, Audrey Huang, Nan Jiang, and Jason Lee. Offline reinforcement learning with realizability and single-policy concentrability. In _Conference on Learning Theory_ , pp. 2730–2775. PMLR, 2022. 

- Chongyi Zheng, Ruslan Salakhutdinov, and Benjamin Eysenbach. Contrastive difference predictive coding. _arXiv preprint arXiv:2310.20141_ , 2023. 

- Chongyi Zheng, Jens Tuyls, Joanne Peng, and Benjamin Eysenbach. Can a misl fly? analysis and ingredients for mutual information skill learning. _arXiv preprint arXiv:2412.08021_ , 2024. 

- John L Zhou and Jonathan C Kao. Flattening hierarchies with policy bootstrapping. _arXiv preprint arXiv:2505.14975_ , 2025. 

14 

Published as a conference paper at ICLR 2026 

# **Appendices** 

### A PROOFS 

We introduce notation in Sec. A.1. We then provide common setup used for all proofs in Sec. A.2. We introduce the assumptions used in Sec. A.3. Sec. A.4, A.5 and A.6 provide the proofs for Proposition1, Proposition2 and Theorem1, respectively. 

- A.1 NOTATION 

   - **Shortest-path distance** : We use step<sup>_∗_</sup> ( _s, g_ ) to denote the minimum number of steps to reach _g_ from _s_ . We define level sets: 


Clearly, _S_ 0 = _{g}_ . Under deterministic dynamics, there exists an action _a_<sup>_∗_</sup> at state _s_ such that _p_ ( _. | s, a_<sup>_∗_</sup> ) _∈Sk−_ 1 whenever _s ∈Sk_ , _k ≥_ 1. 

- A.2 COMMON SETUP FOR PROOFS 

The squared Wasserstein-2 distance between two probability measures _µ_ and _ν_ is defined as: 


where Λ( _µ, ν_ ) is the set of all joint measures with marginals _µ_ and _ν_ . 

We consider the special case where one measure is a Dirac delta, _µ_ = _δg_ , located at a single point _g_ . In this case, any valid transport plan must move all mass from the point _g_ . This removes the need for optimization, as the transport plan is uniquely determined to be the product measure Λ( _x, y_ ) = _δg_ ( _x_ ) _ν_ ( _y_ ). 

Substituting this unique plan into the definition yields: 


The result is the expected squared Euclidean distance from the point _g_ to the distribution _ν_ . 

By replacing the general measure _ν_ with the specific transition probability _d_<sup>_πD_</sup> ( _s_<sup>+</sup> _| s, a_ ) and renaming the integration variable, we obtain the final form: 


With this setup, we now define 


Then 


Recall the expanded form of _d_<sup>_π_</sup> : 


Now, substitute into the definition of _M_<sup>_π_</sup> as an integral, and under the assumption of deterministic dynamics: 


15 

Published as a conference paper at ICLR 2026 

Using the linearity of the integral, we decompose the above expression into two terms: 


It is notable that _M_<sup>_πD_</sup> ( _s, a, g_ ) resembles a squared goal-conditioned Wasserstein-2 distance analogue of the successor representation (Machado et al., 2023). 

We also define the state-only version _M_<sup>_πD_</sup> ( _s, g_ ) = E _a∼πD_ ( _.|s_ ) _M_<sup>_πD_</sup> ( _s, a, g_ ) 

#### A.3 ASSUMPTIONS 

This section lists the assumptions we use to develop our proofs: 

**Assumption A.1** (Deterministic dynamics) **.** _We assume that the environment dynamics are deterministic: For any state s ∈S and action a ∈A, the state transition probability p_ ( _s_<sup>_′_</sup> _| s, a_ ) _is a point mass distribution, concentrated on the unique successor state f_ ( _s, a_ ) _. That is,_ 


**Remark A.1.** _This is a common assumption made for the sake of analytical tractability in foundational reinforcement learning theory. It allows for a clear analysis of the core properties of value functions and policies without the complexities introduced by stochasticity. This assumption serves as a standard basis for theoretical analysis in related work, for instance, in Hartikainen et al. (2020)._ 

**Assumption A.2** (One-step reachability) **.** 


**Remark A.2.** _This assumption is inherent to the definition of a well-posed shortest-path problem. It simply formalizes that the goal is reachable and a shortest path exists from all relevant states._ **Assumption A.3.** _The potential function_ Φ( _s, g_ ) _is strongly monotonic with respect to the shortestpath distance step_<sup>_∗_</sup> ( _s, g_ ) _. For any two states sa, sb, if step_<sup>_∗_</sup> ( _sa, g_ ) _≤ step_<sup>_∗_</sup> ( _sb, g_ ) _, then_ 


_Furthermore, for any k ≥_ 1 _, if s_ 1 _∈ Sk−_ 1 _and s_ 2 _∈ Sk, there exists a constant_ ∆Φ _>_ 0 _such that_ 


**Remark A.3.** _This assumption ensures that the signal provided by the Wasserstein distance is strong and informative, providing a non-trivial cost increase when moving away from the goal._ 

**Assumption A.4** (Layer monotonicity of _πD_ ) **.** _We assume the offline policy πD is consistent with the shortest-path layer structure. For any k ≥_ 1 _, if s_ 1 _∈ Sk−_ 1 _and s_ 2 _∈ Sk, their successors under πD, s_<sup>_′_</sup> 1<sup>=</sup><sup>_f_(</sup><sup>_s_1</sup><sup>_, πD_(</sup><sup>_s_1))</sup><sup>_and s′_</sup> 2<sup>=</sup><sup>_f_(</sup><sup>_s_2</sup><sup>_, πD_(</sup><sup>_s_2))</sup><sup>_must maintain their relative layer ordering.That_</sup> _is,_ 


**Remark A.4.** _Assumption A.4 is a condition on the quality of the offline data, which is a standard requirement for obtaining theoretical guarantees in the offline RL setting (Zhan et al., 2022)._ 

16 

Published as a conference paper at ICLR 2026 

A.4 MONOTONICITY OF GOAL-CONDITIONED REWARD FUNCTION (PROPOSITION 1) 

**Proposition.** _Under suitable assumptions on goal reachability, dynamics, and dataset coverage, for all_ ( _s, a, g_ ) _∈D, the average squared Wasserstein-2 distance_ 


_is monotonically increasing with respect to the shortest-path layer index k. In particular, for a fixed goal g and any k ≥_ 1 _, if s_ 1 _∈Sk−_ 1 _and s_ 2 _∈Sk, then_ 


_Moreover, for any state–goal pair_ ( _s, g_ ) _, the squared Wasserstein-2 distance is minimized by the optimal action:_ 


We prove the proposition in two parts: We first prove that the average _W_ 2<sup>2distanceismonotoni-</sup> cally decreasing in shortest-path distance to goal and then show that _W_ 2<sup>2(</sup><sup>_δg, dπD_(</sup><sup>_s_+</sup><sup>_|s, a∗_))</sup><sup>_≤_</sup> _W_ 2<sup>2(</sup><sup>_δg, dπD_(</sup><sup>_s_+</sup><sup>_| s, a_)) for any (</sup><sup>_s, a, g_).Recall that we define the shortest-path distance in terms of</sup> the layer index _k_ and show that _W_ 2<sup>2(</sup><sup>_δg, dπD_(</sup><sup>_s_+</sup><sup>_|s, a_))=</sup><sup>_M πD_(</sup><sup>_s, a, g_) in Sec. A.2.We can now</sup> re-write the first part of the proposition as: 

**1** (Layer Monotonicity of _M_<sup>_πD_</sup> ) **.** _Under Assumptions A.1, A.3 and A.4, the function M_<sup>_πD_</sup> _is monotonically increasing with respect to the shortest-path layer index k. For goal g and any k ≥_ 1 _, if s_ 1 _∈ Sk−_ 1 _and s_ 2 _∈ Sk, we have:_ 


It is important to note that the indices _k_ here are such that _k_ = 0 refers to the goal state, i.e. index _k −_ 1 defines a state closer to goal than index _k_ . 

_Proof._ Let us define the Bellman operator _T_<sup>_πD_</sup> which maps a function _M_ to a new function _T_<sup>_πD_</sup> _M_ : 


We prove this statement by analyzing the properties of the Bellman evaluation operator _T_<sup>_πD_</sup> associated with the policy _πD_ . 

The function _M_<sup>_πD_</sup> is the unique fixed point of this operator, satisfying _M_<sup>_πD_</sup> = _T_<sup>_πD_</sup> ( _M_<sup>_πD_</sup> ). The existence and uniqueness of this fixed point, and the convergence of value iteration ( _Mi_ +1 = _T_<sup>_πD_</sup> _Mi_ ) to it from any starting function _M_ 0, is guaranteed by the Banach Fixed-Point Theorem. This is because the operator _T_<sup>_πD_</sup> is a _contraction mapping_ due to the discount factor _γ <_ 1. 

To show this, we take any two functions _Ma, Mb_ and measure the distance between their outputs under the supremum norm _∥Ma − Mb∥∞_ = max _s |Ma_ ( _s_ ) _− Mb_ ( _s_ ) _|_ : 

_∥T_<sup>_πD_</sup> _Ma − T_<sup>_πD_</sup> _Mb∥∞_ = max _s_ ��(1 _− γ_ )Φ( _s′, g_ ) + _γMa_ ( _s′, g_ ) _−_ �(1 _− γ_ )Φ( _s_<sup>_′_</sup> _, g_ ) + _γMb_ ( _s_<sup>_′_</sup> _, g_ )��� = max _γ|Ma_ ( _s_<sup>_′_</sup> _, g_ ) _− Mb_ ( _s_<sup>_′_</sup> _, g_ ) _|_ where _s_<sup>_′_</sup> = _f_ ( _s, πD_ ( _s_ )) _s ≤ γ_ max _z∈S_<sup>_|Ma_(</sup><sup>_z, g_)</sup><sup>_−Mb_(</sup><sup>_z, g_)</sup><sup>_|_</sup> = _γ∥Ma − Mb∥∞._ 

Since _γ <_ 1, the operator is a contraction. Therefore, the sequence converges to the unique fixed point _M_<sup>_πD_</sup> . 

Now, we prove that the operator _T_<sup>_πD_</sup> preserves the property of monotonicity. Let _M_ be an arbitrary function that is monotonically increasing with respect to the layer index _k_ . We must show that the resulting function _T_<sup>_πD_</sup> _M_ is also monotonic. 

Let _s_ 1 _∈ Sk−_ 1 and _s_ 2 _∈ Sk_ . Let their successors be _s_<sup>_′_</sup> 1<sup>=</sup><sup>_f_(</sup><sup>_s_1</sup><sup>_, πD_(</sup><sup>_s_1)) and</sup><sup>_s′_</sup> 2<sup>=</sup><sup>_f_(</sup><sup>_s_2</sup><sup>_, πD_(</sup><sup>_s_2)).</sup> We want to show that ( _T_<sup>_πD_</sup> _M_ )( _s_ 1 _, g_ ) _≤_ ( _T_<sup>_πD_</sup> _M_ )( _s_ 2 _, g_ ). 

17 

Published as a conference paper at ICLR 2026 

Consider the difference: 

( _T_<sup>_πD_</sup> _M_ )( _s_ 2 _, g_ ) _−_ ( _T_<sup>_πD_</sup> _M_ )( _s_ 1 _, g_ ) = (1 _− γ_ )[Φ( _s_<sup>_′_</sup> 2<sup>_, g_)</sup><sup>_−_Φ(</sup><sup>_s′_</sup> 1<sup>_, g_)] +</sup><sup>_γ_[</sup><sup>_M_(</sup><sup>_s′_</sup> 2<sup>_, g_)</sup><sup>_−M_(</sup><sup>_s′_</sup> 1<sup>_, g_)]</sup><sup>_._</sup> 

By Assumption A.4, we have step<sup>_∗_</sup> ( _s_<sup>_′_</sup> 1<sup>_, g_)</sup><sup>_≤_step</sup><sup>_∗_(</sup><sup>_s′_</sup> 2<sup>_, g_).Nowweanalyzethetwotermsinthe</sup> difference: 

- By Assumption A.3, the condition step<sup>_∗_</sup> ( _s_<sup>_′_</sup> 1<sup>_, g_)</sup><sup>_≤_step</sup><sup>_∗_(</sup><sup>_s′_</sup> 2<sup>_, g_)directlyimpliesthat</sup> [Φ( _s_<sup>_′_</sup> 1<sup>_, g_)</sup><sup>_≤_Φ(</sup><sup>_s′_</sup> 2<sup>_, g_)].The first term [Φ(</sup><sup>_s′_</sup> 2<sup>_, g_)</sup><sup>_−_Φ(</sup><sup>_s′_</sup> 1<sup>_, g_)] is non-negative.</sup> 

- By our premise for this step, the function _M_ is monotonic. Since _d_<sup>_∗_</sup> ( _s_<sup>_′_</sup> 1<sup>_, g_)</sup><sup>_≤d∗_(</sup><sup>_s′_</sup> 2<sup>_, g_), it</sup> follows that _M_ ( _s_<sup>_′_</sup> 1<sup>_, g_)</sup><sup>_≤M_(</sup><sup>_s′_</sup> 2<sup>_, g_).Thus,the second term [</sup><sup>_M_(</sup><sup>_s′_</sup> 2<sup>_, g_)</sup><sup>_−M_(</sup><sup>_s′_</sup> 1<sup>_, g_)] is also</sup> non-negative. 

Since both terms are non-negative, their sum is non-negative, and thus ( _T_<sup>_πD_</sup> _M_ )( _s_ 1 _, g_ ) _≤_ ( _T_<sup>_πD_</sup> _M_ )( _s_ 2 _, g_ ). This proves that the operator _T_<sup>_πD_</sup> preserves monotonicity. 

The value iteration process starts with an initial value function _M_ 0( _s_ ) = 0 for all _s_ . The zero function is trivially monotonic. Since the operator _T_<sup>_πD_</sup> preserves monotonicity, the entire sequence of value functions _{M_ 0 _, M_ 1 _, M_ 2 _, . . . }_ generated by _Mi_ +1 = _T_<sup>_πD_</sup> _Mi_ consists of monotonic functions. The final value function _M_<sup>_πD_</sup> is the limit of this sequence, and the limit of a sequence of monotonic functions is also monotonic. 

Therefore, _M_<sup>_πD_</sup> is monotonically increasing with respect to the layer index _k_ . 

It follows that average _W_ 2<sup>2distance E</sup> _a∼πD_ ( _·|s_ )<sup>_W_2</sup> 2<sup>(</sup><sup>_δg, dπD_(</sup><sup>_s_+</sup><sup>_| s, a_)) is monotonically decreasing</sup> in shortest-path distance towards goal _g_ . 

We now prove the second part. Similar to part 1, we can re-write in terms of _M_<sup>_πD_</sup> as follows: **2** (Optimal actions under _M_<sup>_πD_</sup> ( _s, a, g_ )) **.** _Under Assumptions A.1-A.4 and the layer monotonicity of M_<sup>_πD_</sup> _, for any state s ∈ Sk with k ≥_ 1 _, any optimal, shortest-path-inducing, action a_<sup>_∗_</sup> _∼ π_<sup>_∗_</sup> ( _.|s, g_ ) _, and any non-optimal action abad, the function M_<sup>_πD_</sup> _is strictly smaller for the shortest-path action. That is,_ 


For Term 1, since _s_<sup>_∗_</sup> _∈ Sk−_ 1 and _sbad ∈ Sj_ with _j ≥ k_ , by Assumption A.3, we have Φ( _sbad, g_ ) _≥_ Φ( _s_<sup>_∗_</sup> _, g_ ) + ∆Φ. Thus, Term 1 is strictly positive and bounded below by (1 _− γ_ )∆Φ _>_ 0. 

For Term 2, since _s_<sup>_∗_</sup> _∈ Sk−_ 1 and _sbad ∈ Sj_ with _j ≥ k_ , by Lemma 1, we have _M_<sup>_πD_</sup> ( _s_<sup>_∗_</sup> _, g_ ) _≤ M_<sup>_πD_</sup> ( _sbad, g_ ). Thus, Term 2 is non-negative. 

The sum of a strictly positive term and a non-negative term is strictly positive. Therefore, ∆ _M >_ 0. It follows that _r_<sup>_W_</sup> ( _s, a_<sup>_∗_</sup> _, g_ ) _> r_<sup>_W_</sup> ( _s, abad, g_ ) or equivalently, _r_<sup>_W_</sup> ( _s, a_<sup>_∗_</sup> _, g_ ) _≥ r_<sup>_W_</sup> ( _s, a, g_ ), where _a_ can be any action in _D_ at state _s_ , which concludes the proof. 

#### A.5 ESTIMATING SQUARED WASSERSTEIN-2 DISTANCE (PROPOSITION 2) 

**Proposition.** _The squared Wasserstein-2 distance between δg and d_<sup>_πD_</sup> ( _s_<sup>+</sup> _| s, a_ ) _is upper bounded, up to a multiplicative constant C >_ 0 _, by the mean squared error of the associated velocity field corresponding to d_<sup>_πD_</sup> ( _s_<sup>+</sup> _| s, a_ ) _and the target velocity corresponding to δg:_ 


18 

Published as a conference paper at ICLR 2026 

_where xt_ = _tx_ 1 + (1 _− t_ ) _x_ 0 _._ 

We note that _x_ 1 _− x_ 0 gives us the velocity at ( _x_ 0 _, x_ 1), where _x_ 1 = _g_ . We start from the definition of squared Wasserstein-2 distance in Sec. A.2. In our case, _µ_ corresponds to _δg_ and _ν_ corresponds to _d_<sup>_π_</sup> _θ_<sup>_D_(</sup><sup>_s_+</sup><sup>_|s, a_).As</sup><sup>_µ_=</sup><sup>_δg_, a point mass centered at</sup><sup>_g_, the transport plan is uniquely determined</sup> to be the product measure _λ_ ( _x, s_<sup>+</sup> ) = _δg_ ( _x_ ) _d_<sup>_π_</sup> _θ_<sup>_D_(</sup><sup>_s_+</sup><sup>_|s, a_)(Sec.A.2).Foragiven(</sup><sup>_s, a, g_),the</sup> inequality follows from Lemma 1 of Lv et al. (2025) by Gronwall’s inequality: 


A.6 OPTIMALITY OF ORS POLICY (PROOF OF THEOREM 1) 

**Theorem.** _Under suitable assumptions on goal reachability, dynamics, and dataset coverage, the greedy goal-conditioned policy:_ 


_where Q_<sup>_∗_</sup> ( _s, a, g_ ) _denotes the optimal action-value function induced by the reward r_<sup>_W_</sup> ( _s, a, g_ ) _, coincides with the optimal shortest-path policy π_<sup>_∗_</sup> ( _a | s, g_ ) _._ 

The optimal action-value function, _Q_<sup>_∗_</sup> ( _s, a, g_ ), for the reward _r_<sup>_W_</sup> ( _s, a, g_ ) is the unique fixed point of the Bellman optimality operator: 


The corresponding optimal state-value function is _V_<sup>_∗_</sup> ( _s, g_ ) = max _a′ Q_<sup>_∗_</sup> ( _s, a_<sup>_′_</sup> _, g_ ). _π_<sup>_greedy_</sup> is the policy that greedily maximizes _Q_<sup>_∗_</sup> ( _s, a, g_ ): 


**Lemma A.1** (Layer-wise Monotonicity of the Optimal Value Function _V_<sup>_∗_</sup> ) **.** _Under Assumptions A.1-A.4 and layer monotonicity of M_<sup>_πD_</sup> _(Sec. A.4), the value function of the optimal shortestpath policy, V_<sup>_∗_</sup> ( _s, g_ ) _, is strictly monotonically non-decreasing with the shortest-path layer index (i.e., the value is strictly higher for states closer to the goal). For any k ≥_ 1 _, if s_ 1 _∈ Sk−_ 1 _and s_ 2 _∈ Sk, we have:_ 


_Consequently, it holds that V_<sup>_∗_</sup> ( _s_ 2 _, g_ ) _< V_<sup>_∗_</sup> ( _s_ 1 _, g_ ) _._ 

_Proof._ Let _π_<sup>_∗_</sup> denote the optimal shortest-path policy. For the sake of clarity, we write that for any state _s_ and goal _g_ , let _a_<sup>_∗_</sup> ( _s_ ) = _π_<sup>_∗_</sup> ( _a_<sup>_∗_</sup> _|s, g_ ). We first establish the difference in the one-step cost for taking a shortest-path action from two adjacent layers. 

Let _sa ∈ Sj−_ 1 and _sb ∈ Sj_ for any _j ≥_ 1. Let their successors under _π_<sup>_∗_</sup> be _sa_<sup>_′_=</sup><sup>_f_(</sup><sup>_sa, a∗_(</sup><sup>_sa_))</sup><sup>_∈_</sup> _Sj−_ 2 and _s_<sup>_′_</sup> _b_<sup>=</sup><sup>_f_(</sup><sup>_sb, a∗_(</sup><sup>_sb_))</sup><sup>_∈Sj−_1.Consider the difference in their one-step costs:</sup> 


By Assumption 3 (Strong Monotonicity of Φ), since _s_<sup>_′_</sup> _a_<sup>_∈Sj−_2and</sup><sup>_s′_</sup> _b_<sup>_∈Sj−_1, we have [Φ(</sup><sup>_s_</sup> _b_<sup>_′, g_)</sup><sup>_−_</sup> Φ( _s_<sup>_′_</sup> _a_<sup>_, g_)]</sup><sup>_≥_∆Φ.By Lemma 1 (Layer Monotonicity of</sup><sup>_M πD_), since</sup><sup>_s′_</sup> _a_<sup>_∈Sj−_2and</sup><sup>_s′_</sup> _b_<sup>_∈Sj−_1, we</sup> have [ _M_<sup>_πD_</sup> ( _s_<sup>_′_</sup> _b_<sup>_, g_)</sup><sup>_−M πD_(</sup><sup>_s_</sup> _a_<sup>_′, g_)]</sup><sup>_≥_0.Therefore,wehavealowerboundonthesingle-stepcost</sup> difference: 

_M_<sup>_πD_</sup> ( _sb, a_<sup>_∗_</sup> ( _sb_ ) _, g_ ) _− M_<sup>_πD_</sup> ( _sa, a_<sup>_∗_</sup> ( _sa_ ) _, g_ ) _≥_ (1 _− γ_ )∆Φ _._ 

19 

Published as a conference paper at ICLR 2026 

Now, let’s consider the two shortest-path trajectories starting from _s_ 1 _∈ Sk−_ 1 and _s_ 2 _∈ Sk_ . Let _τ_ 1<sup>_∗_=(</sup><sup>_s_1</sup><sup>_,_0</sup><sup>_, s_1</sup><sup>_,_1</sup><sup>_, . . . , s_1</sup><sup>_,k−_1=</sup><sup>_g_)bethetrajectorystartingfrom</sup><sup>_s_1</sup><sup>_,_0=</sup><sup>_s_1.</sup> Let _τ_ 2<sup>_∗_=</sup> ( _s_ 2 _,_ 0 _, s_ 2 _,_ 1 _, . . . , s_ 2 _,k_ = _g_ ) be the trajectory starting from _s_ 2 _,_ 0 = _s_ 2. By definition of the shortest-path policy, we have _s_ 1 _,t ∈ Sk−_ 1 _−t_ and _s_ 2 _,t ∈ Sk−t_ for _t ∈_ [0 _, k −_ 1]. 

The value functions are the sum of discounted negative costs: 


Let’s analyze the difference _V_<sup>_∗_</sup> ( _s_ 1 _, g_ ) _− V_<sup>_∗_</sup> ( _s_ 2 _, g_ ): 


For each term in the summation (for _t ∈_ [0 _, k −_ 2]), we have _s_ 1 _,t ∈ Sk−_ 1 _−t_ and _s_ 2 _,t ∈ Sk−t_ . Applying our single-step cost difference result, we get: 


The last term for the _τ_ 2<sup>_∗_trajectory is</sup><sup>_M πD_(</sup><sup>_s_2</sup><sup>_,k−_1</sup><sup>_, a∗_(</sup><sup>_s_2</sup><sup>_,k−_1)</sup><sup>_, g_).Since</sup><sup>_s_2</sup><sup>_,k−_1</sup><sup>_∈S_1, its successor</sup> is _g ∈ S_ 0. We know _M_<sup>_πD_</sup> _≥_ 0. So we can lower bound the entire difference: 


Since _k ≥_ 1 and _γ ∈_ (0 _,_ 1), the term (1 _− γ_<sup>_k−_1</sup> ) is strictly positive. As ∆Φ _>_ 0, the entire lower bound is strictly positive. This completes the proof. 

**Theorem A.1** (Equivalence of the Q-learning Optimum and the Shortest Path) **.** _Under Assumptions A.1-A.4 and noting that r_<sup>_W_</sup> ( _s, a_<sup>_∗_</sup> _, g_ ) _> r_<sup>_W_</sup> ( _s, abad, g_ ) _(Sec A.4), the greedy policy with respect to Q_<sup>_∗_</sup> _is the optimal shortest-path policy π_<sup>_∗_</sup> _._ 

_Proof._ We must show that for any state ( _s, g_ ), the shortest-path action _a_<sup>_∗_</sup> = _π_<sup>_∗_</sup> ( _.|s, g_ ) is the unique maximizer of the action-value function _Q_<sup>_∗_</sup> ( _s, a, g_ ) and is therefore, the same action chosen by _π_<sup>_greedy_</sup> ( _. | s, g_ ). That is, for any non-shortest-path action _abad̸_ = _a_<sup>_∗_</sup> : 


Let’s analyze the difference ∆ _Q_ = _Q_<sup>_∗_</sup> ( _s, a_<sup>_∗_</sup> _, g_ ) _− Q_<sup>_∗_</sup> ( _s, abad, g_ ). Let the successor states be _s_<sup>_∗_</sup> = _f_ ( _s, a_<sup>_∗_</sup> ) and _sbad_ = _f_ ( _s, abad_ ). 


20 

Published as a conference paper at ICLR 2026 

We will now analyze the two terms of this expression. 

The first term, _M_<sup>_πD_</sup> ( _s, abad, g_ ) _− M_<sup>_πD_</sup> ( _s, a_<sup>_∗_</sup> _, g_ ), by part 2 of the proof in Sec. A.4, this term is guaranteed to be positive. 

We now analyze the second term, _γ_ [ _V_<sup>_∗_</sup> ( _s_<sup>_∗_</sup> _, g_ ) _− V_<sup>_∗_</sup> ( _s_ bad _, g_ )]. By definition, the successor state _s_<sup>_∗_</sup> lies in a layer closer to the goal than _s_ bad (i.e., _d_<sup>_∗_</sup> ( _s_<sup>_∗_</sup> _, g_ ) _< d_<sup>_∗_</sup> ( _s_ bad _, g_ )). It therefore follows directly from Lemma A.1 that 


Thus, the term � _V_<sup>_∗_</sup> ( _s_<sup>_∗_</sup> _, g_ ) _− V_<sup>_∗_</sup> ( _s_ bad _, g_ )� is strictly positive. 

The difference in Q-values, ∆ _Q_ , is the sum of a strictly positive term and a strictly positive term (Term 2). The sum is therefore strictly positive. 


This shows that for any state _s_ , the shortest-path action _a_<sup>_∗_</sup> _∼ π_<sup>_∗_</sup> ( _a|s, g_ ) is the unique greedy action with respect to _Q_<sup>_∗_</sup> . Therefore, the greedy policy with respect to _Q_<sup>_∗_</sup> must be the optimal shortest-path policy _π_<sup>_∗_</sup> . 

### B ADDITIONAL INFORMATION 

- B.1 OGBENCH TASKS 

   - **Antmaze datasets:** Antmaze involves controlling a quadruped Ant robot with 8 degrees of freedom (DoF) to reach a given goal location in the maze. The agent must learn both high-level navigation and low-level locomotion skills purely from offline data. We perform experiments on 3 types of challenging mazes: **antmaze-large-navigate** , **antmaze-giantnavigate** and **antmaze-large-explore** . 

**antmaze-giant** is twice the size of the large and same size as **antmaze-ultra** in (Jiang et al., 2022) designed to substantially challenge long-horizon planning capabilities. Both **antmaze-large-navigate** and **antmaze-giant-navigate** are collected with noisy expert SAC policies that repeatedly move towards randomly sampled goals (Park et al., 2024a). **antmaze-large-explore** features extremely low quality yet high coverage data consisting of random exploratory trajectories. 

- **Cube datasets:** The cube environments involve manipulation of cube blocks using a robot arm. We perform experiments on 2 cube-play datasets which are collected using a scripted policy that repeatedly picks a cube and places it in other random locations or on another cube: **cube-double-play** (2 cubes) and **cube-triple-play** (3 cubes). During evaluation, the agent is required to perform cube moving, stacking, swapping or permutations according to the provided goal configuration. This requires learning generalizable pick-and-place operations with multiple objects and stitching across unstructured data to achieve this. The task horizon also increases with the number of cubes. We also perform experiments on the **cube-triple-noisy** dataset which involves highly sub-optimal data with noisy transitions. 

- **Puzzle datasets:** These environments specifically test out the combinatorial generalization abilities of the agent (upto 2<sup>24</sup> puzzle configurations and a much larger state space due to robotic manipulation on the puzzle) under very long horizons. They require solving the Lights Out puzzle (Park et al., 2024a), which consists of a 2D grid with buttons in cells, where pressing buttons toggles the color the that button and buttons around it. The agent has to achieve an appropriate goal configuration of colors by pressing buttons by controlling a robot arm. We evaluate algorithms on play datasets of **puzzle-4x4** , **puzzle-4x5** and **puzzle4x6** ; and noisy datasets of **puzzle-4x4** and **puzzle-4x6** . These are particularly challenging tasks (Park et al., 2024a). 

- **Scene datasets:** The scene tasks challenge sequential, long-horizon planning. They involve manipulating diverse objects: a cube, a window, a drawer and two locks. **scene-play** features a dataset collected using a scripted policy that randomly interacts with the objects. At test-time, the agent has to arrange objects into a given goal configuration. These tasks can involve up to 8 sub-tasks e.g. unlock a drawer, then open it, then put a cube in it and close it again, etc. The agent must therefore be able to stitch together multiple skills to 

21 

Published as a conference paper at ICLR 2026 

achieve success. **scene-noisy** involves the same tasks but the dataset is of substantially lower quality. 


Figure 7: OGBench tasks. 

#### B.2 TOKAMAK TASKS 

A tokamak (Figure 8) is a scientific device that uses electro-magnetic fields to confine extremely hot ionized gas called plasma in a toroidal chamber, with the aim of achieving controlled nuclear fusion It is considered the most promising experimental design for achieving commercial nuclear fusion at scale, opening up avenues for nearly unlimited clean energy. 

We use a dataset of raw sensor and actuator data collected from the DIII-D tokamak located in San Diego, CA, USA. Each trajectory corresponds to one plasma discharge, with a control frequency of 25 ms. A control task corresponds to tracking certain state variables of the plasma through the duration of a discharge. While we were not able to get experiment time on the reactor on short notice, we evaluated each RL algorithm using rollouts from a thoroughly tested and accurately learned model of plasma dynamics (Char et al., 2023; 2024) as a proxy. Each RL algorithm was evaluated based on how closely it tracks a given goal state of the plasma. The reward at each timestep during evaluation corresponds to the L2 distance between the goal variables to track and the actual quantities achieved through control. 


Figure 8: Tokamak fusion reactor from (Walker et al., 2020). 

22 

Published as a conference paper at ICLR 2026 

We evaluated each algorithm over 10 goals. The offline dataset size was roughly 50k samples after data cleaning and processing. The state and action spaces are outlined in the following table: 

|**Category**|**Variables**|
|---|---|
|State Space|**Scalar States:** _βN_, Internal Inductance, Line Averaged Density,<br>Loop Voltage, Stored Energy<br>**Profile States:** Electron Density, Electron Temperature, Pressure,<br>Safety Factor, Ion Temperature, Ion Rotation|
|Action Space|Power Injected, Torque Injected, Total Deuterium Gas Injection, Total ECH Power|


Please refer to Abbate et al. (2021); Char et al. (2023; 2024) for detailed explanations of the specific variables and actuators. 

- B.3 ADDITIONAL INFORMATION ON BASELINES 

   - **For baselines provided in the OGBench (Park et al., 2024a) repository, we use the best hyperparameters provided in the paper. These include: GCBC, GCIVL, GCIQL, QRL, CRL and HIQL** . 

   - **GCIQL** : GCIQL is a goal-conditioned variant of Implicit Q Learning (Kostrikov et al., 2021) that fits the optimal _Q_<sup>_∗_</sup> using expectile regression (Newey & Powell, 1987). GCIQL learns _Q_ and _V_ as follows: 


Here, _Q_<sup>¯</sup> is the target Q function (Mnih et al., 2015), _κ_ is the expectile and _r_<sup>_W_</sup> ( _s, a, g_ ) is the ORS reward. For policy extraction, we use deterministic policy gradient with a behavioral regularization ( **DDPG + BC** ) (Fujimoto & Gu, 2021): 

_J_ DDPG+BC( _π_ ) = E( _s,a_ ) _∼pD_ ( _s,a_ ) _, g∼pD_ mixed<sup>(</sup><sup>_g|s_) [</sup><sup>_Q_(</sup><sup>_s, πµ_(</sup><sup>_s, g_)</sup><sup>_, g_) +</sup><sup>_α_log</sup><sup>_π_(</sup><sup>_a | s, g_)]</sup> 

where _π_<sup>_µ_</sup> ( _s, g_ ) = E _a∼π_ ( _a|s,g_ )[ _a_ ]. We use double-Q learning and normalize the Q values before policy extraction. 

- **Go-Fresh** (Mezghani et al., 2023): Go-Fresh involves 3 stages: Training the R-Net, a neural network that learns local temporal distances between states, using R-Net and R-Net embeddings to create a semi-parametric graph of the offline dataset and then training a policy. While training a policy, every 1000 iterations of training, Go-Fresh creates a new dataset where each tuple corresponds to a randomly sampled ( _s, g_ ) pair from the dataset. We noticed in initial experiments that even when Go-Fresh is trained using the same GCRL algorithm as ORS (GCIQL), overall success-rate was close to 0 across tasks. To ensure a fair and unbiased comparison, we modified the Go-Fresh codebase to have the same goal sampling strategy from OGBench (detailed in Appendix D of (Park et al., 2024a) and in the last item of this sub-section) used for all other baselines. This substantially improved performance and is required to produce non-negligible performance, as reported in Tables 1 and 2. 

Furthermore, noticing that Go-Fresh is tested on relatively simpler tasks compared to ours in their paper (Mezghani et al., 2023), we modify the following hyperparameters to account for the increased task difficulty, in addition to using best values for other hyperparameters: We used a memory capacity of 5000 on all tasks which we found to be sufficient (the graph building stage consistently produced a graph with less than 5000 nodes). We increased the R-Net size to an MLP of 64 units (we did not see an improvement in classification accuracy for large sizes) and used a local distance threshold _τ_ = 10 on all tasks. We also see that weighing the local reward by a factor of 5 before summing it with the global reward gave better performance. 

- **Goal sampling for all algorithms** : The same goal-sampling method was used for all baselines in this paper as well as ORS and all variations. Goals were sampled in three different ways according to probabilities from a categorical distribution defined as follows: 

23 

Published as a conference paper at ICLR 2026 

- _p_<sup>_D_</sup> cur<sup>(</sup><sup>_g|s_):Dirac delta distribution centered at the current state</sup><sup>_s_.</sup> 

- _p_<sup>_D_</sup> traj<sup>(</sup><sup>_g|s_):goal is sampled from future states of</sup><sup>_s_from the same trajectory with uni-</sup> form sampling. 

- _p_<sup>_D_</sup> rand<sup>(</sup><sup>_g|s_):goal is uniformly sampled from</sup><sup>_D_.</sup> 

We provide information on the specific values used in Sec. B.6 and B.7 and Table 6. 

- **n-step returns:** We implement two ways of doing n-step returns in the critic with sparse rewards (where _r_ ( _s, g_ ) = _−_ **1** ( _s̸_ = _g_ ) and _t_ is the MDP timestep): 

   1. **n-step GCIQL** : _Q_ ( _st, at, g_ ) =<sup>�</sup><sup>_t_</sup> _i_ =<sup>+</sup> _t_<sup>_n−_1</sup> _r_ ( _st_ + _i, g_ ) + _γ_<sup>_n_</sup> _Q_ ( _st_ + _n, π_ ( _at_ + _n|st_ + _n, g_ ) _, g_ ) 

   2. **GCIQL-OTA** (based on the core idea in (Ahn et al., 2025)): 

      - _Q_ ( _st, at, g_ ) = _−_ **1** ( _st_ + _n̸_ = _g_ ) + _γQ_ ( _st_ + _n, π_ ( _at_ + _n|st_ + _n, g_ ) _, g_ ) 

As evident, we use GCIQL as the base algorithm for n-step return algorithms. We provide the specific hyperparameters used for each task in Table 6. Please refer to Sec. B.7 for information on all other common hyperparameters. 

Table 6: Specific hyperparameters for best performance with **n-step GCIQL** and **GCIQL-OTA** 

|**Dataset**|_α_**(BC-coefficient)**|_κ_**(Expectile)**|**n**|_γ_|Actor (_p_<sup>_D_</sup><br>cur<sup>_,_</sup>|<sup>_pD_</sup><br>traj|<sup>_, pD_</sup><br>rand<sup>)</sup>|
|---|---|---|---|---|---|---|---|
|puzzle-4x6-play|1.0|0.9|25|0.995|(0,|1, 0)||
|cube-triple-play|3.0|0.9|50|0.995|(0,|1, 0)||
|antmaze-large-navigate|0.3|0.9|50|0.995|(0,|1, 0)||
|antmaze-giant-navigate|0.3|0.9|50|0.995|(0,|1, 0)||
|puzzle-4x6-noisy|0.03|0.9|25|0.995|(0,|1, 0)||
|cube-triple-noisy|0.03|0.9|50|0.995|(0,|1, 0)||
|antmaze-large-explore|0.01|0.9|50|0.995|(0,|0, 1)||


24 

Published as a conference paper at ICLR 2026 

- B.4 TRAJECTORY VISUALIZATIONS: ANALYSED TRAJECTORIES 


Figure 9: Expert trajectories of varying lengths on **antmaze-giant-navigate** used for analysis in Sec. 3.2 and Sec. 5.1. The green dot represents the starting position and the star represents the goal. 

#### B.5 TRAINING ITERATIONS 

Table 7: Training iterations per task. All algorithms are trained for the same number of iterations. 

|**Dataset**|**Training Iterations**|
|---|---|
|cube-double-play|1M|
|puzzle-4x4-play|1M|
|scene-play|1M|
|puzzle-4x5-play|1M|
|puzzle-4x6-play|1M|
|cube-triple-play|2M|
|antmaze-large-navigate|3M|
|antmaze-giant-navigate|6M|
|puzzle-4x4-noisy|1M|
|scene-noisy|1M|
|puzzle-4x6-noisy|1M|
|cube-triple-noisy|1M|
|antmaze-large-explore|6M|


#### B.6 OCCUPANCY AND REWARD MODEL HYPERPARAMETERS 

Table 8: Occupancy and reward-model hyperparameters. 

|**Hyperparameter**|**Value**|
|---|---|
|Gradient steps|2M|
|Optimizer|Adam (Kingma & Ba,2014)|
|Learning rate|0.0003|
|Batch size|256|
|Architecture|MLP|
|MLP size|_{_512, 512, 512, 512_}_|
|Nonlinearity|GELU (Hendrycks & Gimpel,2016)|
|Layer normalization|True|
|Target net update rate (occupancy model)|0.005|
|Discount factor_γ_ (occupancy model)|0.99|
|Flow steps<br><br><br>|22 (antmaze-giant-navigate), 55 (antmaze-large-navigate), 45 (other tasks)|
|Reward (_p_<sup>_D_</sup><br>cur<sup>_, pD_</sup><br>traj<sup>_, pD_</sup><br>rand<sup>) ratio for goal sampling</sup>|(0.2, 0.5, 0.3)|


We added a warm-start stage without bootstrapping to the occupancy model by training it to predict future states _s_<sup>+</sup> distributed according to a geometric distribution over trajectory timesteps _tτ ∼_ Geom(1 _− γ_ ) starting the current state _s_ : 


for the first 1M epochs and then training it using the bootstrapping loss in Sec. 4.1 for next next 1M epochs, however we did not see any consistent improvements from doing this. 

25 

Published as a conference paper at ICLR 2026 

#### B.7 POLICY TRAINING HYPERPARAMETERS 

We first list hyperparameters common to all algorithms in Table 9: 

Table 9: Common hyperparameters for policy training. 

|**Hyperparameter**|**Value**|
|---|---|
|Optimizer|Adam (Kingma & Ba,2014)|
|Learning rate|0.0003|
|Batch size|1024|
|Architecture|MLP|
|MLP size (Actor and Critic)|_{_512, 512, 512_}_|
|Nonlinearity|GELU (Hendrycks & Gimpel,2016)|
|Layer normalization|True|
|Target critic update rate|0.005|
|Critic (_p_<sup>_D_</sup><br>cur<sup>_, pD_</sup><br>traj<sup>_, pD_</sup><br>rand<sup>) ratio for goal sampling</sup>|(0.2, 0.5, 0.3)|


We then provide specific hyperparameters used for ORS and Go-Fresh (which use GCIQL as the base algorithm to train policies) in Table 10: 

Table 10: Specific hyperparameters for policy training: ORS and Go-Fresh 

|**Dataset**|_α_**(BC-coefficient)**|_κ_**(Expectile)**|_γ_|Actor (_p_<sup>_D_</sup><br>cur<sup>_, pD_</sup><br>traj<sup>_, pD_</sup><br>rand<sup>)</sup>|reward scaling for ORS (linear scaling_x_ : (_r/x_))|
|---|---|---|---|---|---|
|puzzle-4x4-play|0.6|0.6|0.99|(0, 1, 0)|0.75|
|puzzle-4x5-play|0.6|0.6|0.99|(0, 0.5, 0.5)|0.75|
|puzzle-4x6-play|0.6|0.9|0.99|(0, 0.5, 0.5)|0.25|
|cube-double-play|0.3|0.75|0.99|(0, 0.5, 0.5)|0.25|
|cube-triple-play|0.3|0.9|0.99|(0, 0.5, 0.5)|0.25|
|scene-play|0.3|0.75|0.99|(0, 0.5, 0.5)|0.75|
|antmaze-large-navigate|0.15|0.6|0.995|(0, 1, 0)|2.0|
|antmaze-giant-navigate|0.1|0.6|0.995|(0, 1, 0)|2.0|
|puzzle-4x4-noisy|0.05|0.6|0.99|(0, 1, 0)|0.25|
|puzzle-4x6-noisy|0.05|0.75|0.99|(0, 1, 0)|0.25|
|cube-triple-noisy|0.03|0.75|0.99|(0, 0.5, 0.5)|1.0|
|scene-noisy|0.1|0.75|0.99|<br>(0, 1, 0)|0.25|
|antmaze-large-explore|0.015|0.9|0.99|(0, 0.5, 0.5)|3.0|


#### B.8 WALL-CLOCK TIME 

The average wall-clock time per iteration is as follows: 

|Method|Component|Time per iteration (ms)|
|---|---|---|
||Occupancy model|14|
|ORS|Reward function|8|
||Policy training|6.5|
|GO-FRESH|R-NET training|9.5|
||Policy training|7.2|


GO-FRESH also has a graph computation time that ranges between 1.5-10 mins depending on the task and dataset. For default GCIQL, policy training takes 7.2 ms per iteration. All times were reported on a single NVIDIA RTX A6000 GPU. We typically see that reward function and occupancy model losses converge in around 500k iterations. R-Net training typically runs for 500k iterations. 

26 

Published as a conference paper at ICLR 2026 

While ORS does lead to a slightly higher computational overhead, it also leads to a 2.3 _×_ increase in performance over GCIQL, its base algorithm, and exhibits stronger performance than GO-FRESH on a variety of tasks. GO-FRESH requires training a distance classifier, training a graph memory and building a graph, each of which involves hyperparameter tuning for the size of the R-Net, number of edges in the graph, number of negative pairs for training the R-Net, distance threshold for the R-Net and careful weighing of local and global rewards during policy training. In contrast, ORS is simple to train, does not require storing a large graph in memory and is easy to tune. We agree that increasing the efficiency of ORS is an important direction for future work. 

27 

