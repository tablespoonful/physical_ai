---
title: "Inference Time Policy Optimization for Offline RL with Differentiable World Models"
date: "2026-03-23"
authors: "Rohan Deb; Stephen J. Wright; Arindam Banerjee"
url: https://arxiv.org/abs/2603.22430
pdf: https://arxiv.org/pdf/2603.22430
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.22430)** / [論文ページ](https://arxiv.org/abs/2603.22430)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Inference Time Policy Optimization for Offline RL with Differentiable World Models 

**Rohan Deb Steven J. Wright** Siebel School of Computing and Data Science Department of Computer Sciences University of Illinois Urbana-Champaign University of Wisconsin Madison rd22@illinois.edu sjwright2@wisc.edu 

### **Arindam Banerjee** 

Siebel School of Computing and Data Science 

University of Illinois Urbana-Champaign 

arindamb@illinois.edu 

#### **Abstract** 

Offline Reinforcement Learning (RL) learns optimal policies from fixed datasets, training a policy once and deploying it at inference time without further refinement. Inspired by model predictive control (MPC), we introduce an inference time adaptation framework that utilizes a pretrained policy along with a learned world model. While existing world model and diffusion-planning methods use learned dynamics to generate imagined trajectories during training, or to sample candidate plans at inference time, they do not use inference-time information to _optimize_ the policy parameters on the fly. In contrast, our design is a Differentiable World Model (DWM) pipeline that enables end-to-end gradient computation through imagined rollouts for _inference time policy optimization_ (ITPO). We evaluate our algorithm on D4RL continuous-control benchmarks (MuJoCo locomotion tasks and AntMaze), and show that exploiting inference-time information to optimize the policy parameters yields consistent gains over strong offline RL baselines. Inference-time adaptation, however, is expensive: rollout generation and backpropagation dominate per-step compute. We study this tradeoff explicitly, showing that a suitable tilted version of one-step MeanFlow sampler recovers much of the gains at a fraction of the cost. 

## **1 Introduction** 

Offline reinforcement learning learns a policy in a Markov decision process from a fixed dataset of previously collected trajectories, without any additional interaction with the environment [Levine et al., 2020, Prudencio et al., 2022, Ernst et al., 2005, Fujimoto et al., 2019b]. This setting arises naturally in domains where data is abundant but online interaction is constrained [Levine et al., 2020, Fujimoto et al., 2019b, Liu et al., 2020]. Examples include modern recommender and advertising systems, which operate on massive logs of user interactions [Xiao and Wang, 2023, Afsar et al., 2022, Cai et al., 2017, Zhao et al., 2021]; healthcare and other safety-critical decision problems, which cannot permit exploratory actions [Gottesman et al., 2019, Yu et al., 2021a, Fatemi et al., 2022]; robotics and control, which may be limited by real-world cost, wear, and safety [Kober et al., 2013, Zhou et al., 2022, Venkataraman et al., 2024]; and autonomous driving and navigation, which rely typically on recorded datasets rather than unrestricted on-policy exploration [Kiran et al., 2022, Shi et al., 2021, Shah et al., 2023]. 

1 

The core challenge of offline RL is to optimize reward while avoiding actions that are unsupported by the data distribution [Lange et al., 2012, Levine et al., 2020]. Offline RL algorithms address this challenge by shaping either the policy or the value-learning objective. Behavior Regularized Actor Critic (BRAC) approaches keep the learned policy close to the dataset behavior [Fujimoto and Gu, 2021, Tarasov et al., 2023b]; Conservative Q Learning (CQL) penalizes high Q-values on unlikely actions to reduce overestimation under dataset shift [Kumar et al., 2020]; and in-sample or implicit methods avoid querying out-of-distribution actions (e.g., IQL) [Kostrikov et al., 2022]. Separately, motivated by generative models’ success, recent work replaces parametric policies with generative ones to capture multi-modal behavior. These include sequence-modeling policies such as Decision Transformer that predict actions conditioned on return [Chen et al., 2021] and diffusion or flow-based policies such Decision Diffuser [Janner et al., 2022a] and Flow Q learning [Park et al., 2025] that generate actions or trajectories by iterative denoising or flow dynamics. For a more detailed discussion on related works, see Appendix A. 

Existing offline RL methods typically produce a single policy trained on the offline dataset and then deploy it _as-is_ at inference time. These methods do not explicitly exploit inference-time information about the particular states encountered by the agent beyond using it as the input to the pre-trained policy. Recent work on large language models and reasoning suggests that additional inference-time computation can improve performance on a given test instance. For example, self-consistency and search-based reasoning methods use extra computation at inference time to refine or select among candidate outputs [Wang et al., 2023, Yao et al., 2023, Muennighoff et al., 2025], while more recent work has begun to explore reinforcement-learning-based approaches for inference-time improvement [Hou et al., 2025, Zuo et al., 2025]. This motivates the question: whether, in offline RL, additional inference-time computation can similarly improve the performance of an agent. 

In offline RL, realizing this idea requires identifying what form of inference-time computation can actually improve the deployed policy. An offline learner returns a pre-trained policy _πψ_ and an associated critic _Qϕ_ , intended to approximate the optimal policy and _Q_ -values. When the policy is deployed without further adaptation, performance depends on how accurate these approximations are in the states and actions _encountered at inference time_ , and accurate _Q_ estimation is itself challenging for two reasons. First, the _Q_ -value is intrinsically difficult to estimate because it represents a long-horizon quantity: it aggregates future rewards over many steps starting from a given state-action pair. Second, in offline RL the critic must approximate the _Q_ -value of the _optimal_ policy, even though the available data might be generated by a different behavior policy. Beyond the difficulty of _Q_ -estimation, the deployed policy is itself information-limited: it is the best policy extractable from the offline dataset under the chosen learning objective. Inference-time gains must therefore come from _new information_ that was not available during offline training: the particular state _st_ that the agent encounters at deployment. The information becomes useful only if it can be coupled with a model of the consequences of acting from _st_ , allowing the agent to look ahead from this specific state and refine its decision based on what would happen next. 

In the Markovian model, the one-step transition dynamics _P_ ( _s_<sup>_′_</sup> _| s, a_ ) and reward function _r_ ( _s, a_ ) are _local objects_ : they depend only on the current state-action pair, rather than on long-horizon estimates, and are independent of whatever policy is being deployed. This fact motivates a different approach: learn world models of _P_ and _r_ from offline data and use these learned functions at inference time to formulate policy. The link between _P_ and _r_ and a corresponding optimal policy is provided by Model Predictive Control (MPC) [Camacho and Bordons, 2007, Rawlings et al., 2017]. Conventional MPC optimizes action sequences over rolled-out short-horizon trajectories defined by the function _P_ , thus implicitly generating a policy. We use MPC in a different way, using information gathered from the rollout simulations to update the parameters 

2 

that define our policy, and not to merely find the best action sequence. In this way, the initial policy learned from the offline data is updated continuously during deployment as new information is gathered about the system. See Figure 1 for a visual overview and Section 4 for a detailed description of our method. We now outline our main contributions. 

1. We introduce _MPC with a Differentiable World Model_ (MPCwDWM), an inference-time adaptation framework for offline RL. The world model consists of a learned generative state-transition sampler, a reward model, and a terminal-value function, all differentiable in the policy parameters (Section 3). 

2. Building on this pipeline, we perform inference-time _policy-parameter_ updates by backpropagating through imagined rollouts to refine the baseline policy before each action. This contrasts with prior MPC and gradient-based-planning methods that optimize action sequences while leaving the policy fixed (Section 4). 

3. We evaluate on D4RL continuous-control benchmarks [Fu et al., 2020] (18 MuJoCo locomotion and 6 AntMaze datasets), showing consistent gains over strong offline RL baselines (Section 5). 

4. To address the compute requirements of diffusion unrolling and BPTT, we propose _FlowMPC_ , a one-step MeanFlow variant of the transition sampler that recovers much of the gain at a fraction of the compute (Section 6). 

**Comparison with existing World Model based Offline RL methods.** Although world models (including diffusion-based world models) have been used in _offline_ RL, they are typically leveraged in two ways. Some methods [Kidambi et al., 2020, Yu et al., 2020, 2021b, Ding et al., 2024] use the learned dynamics primarily during _training_ , generating imagined rollouts from the offline dataset to construct additional targets or synthetic experience for policy and value learning, including diffusion world models that model multi-step futures without step-by-step rollout. Other methods use a generative model at _inference time_ to produce candidates for future optimal state trajectories via sampling (often with guidance via return-conditioning), and then select an action by executing the first action of a sampled plan, without adapting the underlying policy parameters during inference [Ajay et al., 2023, Janner et al., 2022a, Ki et al., 2025, Yun et al., 2024]. In contrast, our method uses the current observed state to _adapt the policy parameters at inference time_ by backpropagating through a differentiable world model over imagined finite-horizon rollouts. 

**Comparison with MPC-based methods.** Although MPC has been combined with learned dynamics in several recent works, these methods either operate online with environment interaction or perform gradientfree planning over action sequences. Latent-world-model methods such as Dreamer [Hafner et al., 2020, 2021, 2025] and TD-MPC [Hansen et al., 2022, 2024] train jointly with online interaction; the former uses the model only at training time, while the latter performs gradient-free MPPI in the latent space at deployment. Gradient-based and embedded differentiable MPC methods [V et al., 2023, Romero et al., 2025] optimize action sequences or cost-function parameters rather than the policy itself. Diffusion-based MPC methods such as D-MPC [Zhou et al., 2024] sample candidate action sequences from a learned diffusion proposal and select the best by gradient-free random shooting under a multi-step diffusion dynamics model. In contrast, our method operates purely on offline data and uses the current observed state to _adapt the policy parameters at inference time_ by backpropagating through a differentiable world model over imagined finite-horizon rollouts. A detailed methodological comparison against each of these is provided in Appendix E. 

3 

## **2 Preliminaries** 

We consider a discounted Markov decision process (MDP) specified by the tuple _M_ = _⟨S, A, P, d_ 0 _, r, γ⟩_ , where _S_ and _A_ are the state and action spaces, _P_ ( _s_<sup>_′_</sup> _| s, a_ ) is the transition kernel, _d_ 0 is the initial state distribution, _r_ ( _s, a_ ) is the reward function, and _γ ∈_ [0 _,_ 1) is the discount factor. A stochastic policy _π_ ( _a | s_ ) induces a distribution over trajectories _τ_ = ( _s_ 0 _, a_ 0 _, r_ 0 _, s_ 1 _, a_ 1 _, r_ 1 _, . . ._ ) with density _p_<sup>_π_</sup> ( _τ_ ) = _d_ 0( _s_ 0)<sup>�</sup> _t≥_ 0<sup>_π_(</sup><sup>_at| st_)</sup><sup>_P_(</sup><sup>_st_+1</sup><sup>_| st, at_) and discounted return</sup><sup>_R_(</sup><sup>_τ_)=�</sup> _t_<sup>_∞_</sup> =0<sup>_γtr_(</sup><sup>_st, at_)</sup><sup>_._The RL objective</sup> is to find a return-maximizing policy within a policy class Π, _π_<sup>_⋆_</sup> _∈_ argmax _π∈_ Π E _τ ∼p_<sup>_π_</sup> [ _R_ ( _τ_ )] _._ 

**Temporal-difference learning.** TD methods approximate the optimal action-value function _Q_<sup>_⋆_</sup> ( _s, a_ ) = E _τ ∼pπ_<sup>_⋆_</sup> [ _R_ ( _τ_ ) _| s_ 0 = _s, a_ 0 = _a_ ] with a parameterized critic _Qϕ_ by minimizing a Bellman error on the data 


where _Qϕ_ ¯ denotes a target network whose parameters _ϕ_<sup>¯</sup> are a slowly updated copy of _ϕ_ . For continuous action spaces, the maximization is typically implemented via a parameterized actor _πψ_ ( _a | s_ ), leading to a policy objective of the form _J_ ( _ψ_ ) := E _s∼D, a∼πψ_ ( _·|s_ )[ _Qϕ_ ( _s, a_ )] _._ 

**Offline RL and distribution shift.** Offline RL learns a policy from a fixed dataset without additional environment interactions. We assume access to a static dataset of transitions _D_ = _{_ ( _st, at, rt, st_ +1) _}_<sup>_N_</sup> _t_ =1 collected by an unknown behavior policy _µ_ . A core difficulty is that naively applying TD learning and policy improvement can drive the learned policy _πψ_ toward state-action regions that are weakly represented in _D_ , i.e., the induced discounted state-action occupancy measure _d_<sup>_πψ_</sup> moves away from _d_<sup>_µ_</sup> , where _d_<sup>_π_</sup> ( _s, a_ ) := (1 _− γ_ )<sup>�</sup> _t≥_ 0<sup>_γt_Pr</sup><sup>_τ∼pπ_(</sup><sup>_st_=</sup><sup>_s,at_=</sup><sup>_a_).ManyofflineRLmethodsaddressthisdistributionshiftby</sup> enforcing an explicit constraint, either at the policy level _D_ ( _πψ_ ( _· | s_ ) _∥ µ_ ( _· | s_ )) _≤ ε,_ or at the occupancy level _D_ ( _d_<sup>_πψ_</sup> _∥ d_<sup>_µ_</sup> ) _≤ ε,_ where _D_ is a divergence or discrepancy measure. Such constrained formulations often introduce additional algorithmic heuristics to obtain stable and competitive performance in practice. 

## **3 Components of the World Model** 

Our algorithm at inference time requires sampling next state samples conditioned on the current state action pair, and differentiating those samples with respect to the conditioning variables. We refer to any model with this sample plus gradient interface as a differentiable generative world model (DiffGenWM), and in this work we implement it using a conditional generative model. In addition to the DiffGenWM module, our world model includes a differentiable reward model and a terminal value function given by the critic of a pretrained policy. Concretely, we build a world model using the offline dataset of trajectories _D_ = _{_ ( _st, at, rt, st_ +1) _}_<sup>_N_</sup> _t_ =1<sup>,</sup> consisting of (1) a _differentiable diffusion sampler fθ_ to simulate the transition dynamics, (2) a reward model _rξ_ to learn the reward of a given state action pair and, (3) pretrained policy _πψ_ and the corresponding pretrained critic value _Qϕ_ . 

### **3.1 Differentiable Diffusion Sampler** 

We learn a parametric, differentiable sampler _st_ +1 = _fθ_ ( _st, at, εt_ ) _, εt ∼ p_ 0 _,_ that represents a conditional distribution _pθ_ ( _st_ +1 _| st, at_ ) over next states, with all stochasticity isolated in _εt_ via reparameterization. Here, _differentiable_ means in ( _st, at_ ) for fixed _εt_ , not in _θ_ . We train _fθ_ on the offline dataset _D_ = _{_ ( _st, at, rt, st_ +1) _}_<sup>_N_</sup> _t_ =1<sup>as a conditional diffusion model [Ho et al., 2020].</sup> 

4 

**Forward process.** Given a horizon _K_ and a schedule _{αk}_<sup>_K_</sup> _k_ =1<sup>_⊂_(0</sup><sup>_,_1) with</sup><sup>_α_¯</sup><sup>_k_:=</sup><sup><u>�</u></sup><sup>_k_</sup> _j_ =1<sup>_αj_, we corrupt</sup> _st_ +1 via a Gaussian Markov chain whose closed-form marginal at level _k_ is _s_<sup>(</sup> _t_ +1<sup>_k_)=</sup><sup>_~~√~~_</sup> _<u>α</u>_ <u>¯</u> _k st_ +1 +<sup>_~~√~~_</sup> 1 _− α_ ¯ _k ϵ_ , where _ϵ ∼N_ (0 _, I_ ). 


**Training objective.** We minimize the standard conditional denoising loss 


with _s_<sup>(</sup><sup>_k_)</sup> _t_ +1<sup>given by the forward marginal above.The trained</sup><sup>_fθ_serves as a learned, differentiable one-step</sup> dynamics simulator; see Appendix B.1 for the full construction, including the explicit initialization and reverse-step maps. 

### **3.2 Reward model** 

In addition to the transition model, we learn a parametric reward predictor from the same offline data. We parameterize the reward predictor as a function _rξ_ : _S × A →_ R, which maps a state–action pair ( _st, at_ ) to a scalar reward estimate. Given an offline dataset of transitions _D_ = _{_ ( _st, at, rt, st_ +1) _}_<sup>_N_</sup> _t_ =1<sup>, we fit</sup><sup>_rξ_by</sup> supervised regression on observed rewards, minimizing the loss function 


After training, _rξ_ serves as a differentiable reward oracle that can be queried at arbitrary ( _s, a_ ) pairs produced by downstream planning or policy optimization, and can be combined with the learned diffusion transition model to form multi-step return objectives. 

### **3.3 Policy and Terminal Value** 

Given an offline dataset _D_ = _{_ ( _st, at, rt, st_ +1) _}_<sup>_N_</sup> _t_ =1<sup>, we learn a parametric stochastic policy</sup><sup>_πψ_(</sup><sup>_a | s_) and a</sup> parametric action-value function _Qϕ_ ( _s, a_ ) via a BC-regularized actor-critic, in the spirit of BRAC [Tarasov et al., 2023a, Wu et al., 2019]. The critic minimizes a one-step temporal-difference loss with target network _Qϕ_ ¯, 


The actor maximizes value under _Qϕ_ while staying close to the dataset behavior via a behavior-cloning term that increases the likelihood of dataset actions under _πψ_ , 


where _λ >_ 0 controls the strength of the regularization. In practice, _Qϕ_ ¯ is maintained as a slowly updated copy of _Qϕ_ to stabilize the bootstrapped target in _LQ_ ( _ϕ_ ). 

5 

Figure 1: Inference-time MPC with a diffusion world model. An offline dataset trains (i) a diffusion sampler _fθ_ , (ii) a reward model _rξ_ , and (iii) a policy _πψ_ and terminal critic _Qϕ_ . At state _st_ , we unroll _M_ imagined rollouts via ˜ _ah_ = _πψ_ (˜ _sh_ ) and _s_ ˜ _h_ +1 = _fθ_ (˜ _sh,_ ˜ _ah, εt_ + _h_ ), score them with predicted rewards plus a terminal value, and backpropagate through the rollout to update _ψ_ before executing the first action. Green: forward rollout; Brown: gradient flow. 


## **4 MPC with Differentiable World Model** 

We now describe our receding-horizon model predictive control (MPC) procedure that uses the learned diffusion world model as a differentiable simulator. The world model is given by the reparameterized transition map _st_ +1 = _fθ_ ( _st, at, εt_ ) _, εt ∼ p_ 0( _ε_ ), where _fθ_ denotes the reverse diffusion sampler unrolled as a computation graph. We combine this dynamics model with a learned reward predictor _rξ_ ( _s, a_ ) and a learned terminal critic _Qϕ_ ( _s, a_ ). The critic provides a terminal value for truncated rollouts, while _rξ_ supplies the immediate reward along imagined trajectories at inference time. Without loss of generality, we assume _πψ_ is deterministic for the remainder of this section. 

**Receding-horizon Objective:** At a real environment state _st_ , MPC optimizes a horizon- _H_ objective over imagined trajectories generated by _fθ_ . Given a fixed noise sequence _εt_ : _t_ + _H−_ 1 = ( _εt, . . . , εt_ + _H−_ 1) define the imagined rollout recursively by _s_ ˜0 = _st, a_ ˜ _j_ = _πψ_ (˜ _sj_ ) _, s_ ˜ _j_ +1 = _fθ_ (˜ _sj,_ ˜ _aj, εt_ + _j_ ), where _j_ = 0 _, . . . , H −_ 1. We evaluate the finite-horizon return by summing predicted stage rewards and adding a terminal value given by the critic: 


6 

**Algorithm 1** Model Predictive Control with Differentiable World Model (MPCwDWM) 

**Require:** Diffusion sampler _fθ_ , noise _{ε_<sup>(</sup> _t_ :<sup>_i_</sup> _t_<sup>)</sup> + _H−_ 1<sup>_}_</sup> _i_<sup>_M_</sup> =1<sup>reward model</sup><sup>_rξ_, terminal critic</sup><sup>_Qϕ_, policy</sup><sup>_πψ_, horizon</sup> _H_ , particles _M_ , inner steps _E_ , step size _η_ , discount _γ_ . 1: **for** _t_ = 1 _,_ 2 _,_ 3 _. . . , T_ **do** 2: Observe environment state _st_ 3: **for** _e_ = 1 _,_ 2 _, . . . , E_ **do** 4: _J ←_ 0, _s_ ˜<sup>(</sup> 0<sup>_i_)</sup> _← st ∀ i ∈{_ 1 _,_ 2 _, . . . , M }_ 5: **for** _j_ = 0 _,_ 1 _, . . . , H −_ 1 **do** 6: **for** _i_ = 1 _,_ 2 _, . . . , M_ **do** 7: _a_ ˜<sup>(</sup> _j_<sup>_i_)</sup> _← πψ_ (˜ _s_<sup>(</sup> _j_<sup>_i_))</sup> _▷_ Action for imagined rollout 8: **end for** 9: _J ← J_ + _M_<sup><u>1</u></sup> � _Mi_ =1<sup>_γj rξ_(˜</sup><sup>_s_(</sup> _j_<sup>_i_)</sup><sup>_,_˜</sup><sup>_a_(</sup> _j_<sup>_i_))</sup> 10: **for** _i_ = 1 _,_ 2 _, . . . , M_ **do** 11: _s_ ˜<sup>(</sup> _j_<sup>_i_</sup> +1<sup>)</sup><sup>_←fθ_(˜</sup><sup>_s_(</sup> _j_<sup>_i_)</sup><sup>_,_˜</sup><sup>_a_(</sup> _j_<sup>_i_)</sup><sup>_, ε_(</sup> _t_ +<sup>_i_)</sup> _j_<sup>)</sup> _▷_ Next state 12: **end for** 13: **end for** 14: _J ← J_ + _M_<sup><u>1</u></sup> � _Mi_ =1<sup>_γH Qϕ_(˜</sup><sup>_s_(</sup> _H_<sup>_i_)</sup><sup>_, πψ_(˜</sup><sup>_s_(</sup> _H_<sup>_i_)))</sup> 15: _ψ ← ψ_ + _η ∇ψJ ▷_ Policy Update 16: **end for** 17: Execute _at ← πψ_ ( _st_ ) and observe ( _rt, st_ +1) 18: **end for** 

We then define the MPC objective as the expectation of this return over diffusion noise: 


**Monte Carlo Approximation:** We approximate the objective _Jt_ ( _ψ_ ) with _M_ i.i.d. noise sequences _{ε_<sup>(</sup> _t_ :<sup>_m_</sup> _t_ +<sup>)</sup> _H−_ 1<sup>_}_</sup> _m_<sup>_M_</sup> =1<sup>,</sup> where _ε_<sup>(</sup> _t_ :<sup>_m_</sup> _t_ +<sup>)</sup> _H−_ 1<sup>_∼p_0.For each</sup><sup>_m_, generate an imagined rollout</sup><sup>_{s_˜(</sup> _j_<sup>_m_)</sup> _,_ ˜ _a_<sup>(</sup> _j_<sup>_m_)</sup> _}_<sup>_H_</sup> _j_ =0<sup>:</sup> 


The Monte Carlo estimator is 

**Gradient-based optimization:** At time _t_ , we perform _E_ steps of gradient ascent on _J_<sup>�</sup> _t_ ( _ψ_ ) while holding _fθ_ , _rξ_ , and _Qϕ_ fixed: _ψ ← ψ_ + _η ∇ψJ_<sup>�</sup> _t_ ( _ψ_ ), where _η >_ 0 is the step size. After the inner loop, MPC executes the first action in the real environment _at_ = _πψ_ ( _st_ ), observes ( _rt, st_ +1), and repeats the procedure at the next state _st_ +1. See Figure 1 for a visual overview and Algorithm 1 for detailed steps. For a closed-form gradient recursion for our setup see Appendix B.2. 

7 

|Dataset|TD3+BC|IQL<br>**half**|CQL<br>**cheetah**|ReBRAC|`DiffMPC`|
|---|---|---|---|---|---|
|medium|54_._7_±_0_._9|50_._0_±_0_._2|46_._9_±_0_._4|65_._87_±_1_._3|**70.05**_±_1_._8|
|expert|93_._4_±_0_._4|95_._5_±_2_._1|97_._3_±_1_._1|105_._22_±_0_._92|**106.14**_±_2_._1|
|medium-expert|89_._1_±_5_._6|92_._7_±_2_._8|95_._0_±_1_._4|100_._29_±_8_._2|**105.35**_±_1_._8|
|medium-replay|45_._0_±_1_._1|42_._1_±_3_._6|45_._3_±_0_._3|50_._21_±_0_._7|**59.89**_±_1_._2|
|full-replay|75_._0_±_2_._5|75_._0_±_0_._7|76_._9_±_0_._9|82_._19_±_0_._9|**85.149**_±_0_._9|
|||**ho**|**pper**|||
|medium|60_._9_±_7_._6|65_._2_±_4_._2|61_._9_±_6_._4|102_._05_±_0_._9|**103.38**_±_0_._35|
|expert|**109.6**_±_3_._7|108_._8_±_3_._1|106_._5_±_9_._1|104_._73_±_6_._94|105_._06_±_5_._02|
|medium-expert|87_._8_±_10_._5|85_._5_±_29_._7|96_._9_±_15_._1|105_._70_±_8_._3|**107.42**_±_5_._30|
|medium-replay|55_._1_±_31_._7|89_._6_±_13_._2|86_._3_±_7_._3|95_._82_±_7_._9|**103.14**_±_0_._45|
|full-replay|97_._9_±_17_._5|104_._4_±_10_._8|101_._9_±_0_._6|107_._49_±_0_._4|**108.77**_±_0_._6434|
|||**wal**|**ker2d**|||
|medium|77_._7_±_2_._9|80_._7_±_3_._4|79_._5_±_3_._2|84_._78_±_1_._8|**88.91**_±_0_._6|
|expert|110_._0_±_0_._6|96_._9_±_32_._3|109_._3_±_0_._1|112_._15_±_0_._2|**116.65**_±_0_._41|
|medium-expert|110_._4_±_0_._6|112_._1_±_0_._5|109_._1_±_0_._2|111_._81_±_0_._3|**115.76**_±_1_._04|
|medium-replay|68_._0_±_19_._2|75_._4_±_9_._3|76_._8_±_10_._0|80_._67_±_5_._8|**95.87**_±_1_._19|
|full-replay|90_._3_±_5_._4|97_._5_±_1_._4|94_._2_±_1_._9|100_._16_±_8_._8|**105.76**_±_2_._91|
|Average|81_._7|84_._8|85_._6|93_._9|**98.5**|


Table 1: Average normalized score over the final evaluation and ten unseen training seeds on Gym-MuJoCo tasks. TD3+BC, IQL, and CQL scores are taken from [Tarasov et al., 2023a]. We ran ReBRAC and `DiffMPC` with ReBRAC as the pre-trained policy. The symbol _±_ represents the standard deviation across seeds. 

## **5 Experiments** 

**Datasets.** We evaluate our algorithm on the D4RL benchmark [Fu et al., 2020], focusing on continuouscontrol domains where offline learning and long-horizon credit assignment are challenging. Our main results cover Gym MuJoCo locomotion datasets (15 tasks spanning medium, expert, medium-expert, medium-replay, and full-replay settings across all three environments HalfCheetah, Hopper, and Walker2d). We also consider all AntMaze datasets (6 tasks spanning maze, maze-diverse, medium-play, medium-diverse, large-play, and large-diverse). 

**Baselines.** We compare against strong offline RL baselines that are widely used on D4RL locomotion. These include TD3+BC [Fujimoto and Gu, 2021], which adds behavior cloning regularization to a TD3 actor update; IQL [Kostrikov et al., 2022], which performs offline policy improvement via value-weighted regression without explicit behavior constraints; CQL [Kumar et al., 2020], which trains a conservative critic by penalizing high values on out-of-distribution actions; and ReBRAC [Tarasov et al., 2023b], which revisits behavior-regularized actor-critic with practical improvements and strong performance. 

8 

**Experimental details.** Our approach has an offline training stage and an inference-time adaptation stage. We first train a policy _πψ_ and critic _Qϕ_ on the offline dataset using ReBRAC [Tarasov et al., 2023b]. We then train a diffusion transition model _fθ_ on dataset transitions and a reward predictor _rξ_ on dataset rewards using supervised learning. Since the inference-time adaptation differentiates through the diffusion sampler, we refer to this instantiation of our method as `DiffMPC` . Training details and results for both models are deferred to Appendix C. 

To train the ReBRAC policy we follow the hyper-parameter choices from [Tarasov et al., 2023a]. We tune the inference time parameters on a single training seed (different from the evaluation seeds). For a detailed description and hyperparameter choices see Appendix C 

|Task Name|ReBRAC|`DiffMPC`|
|---|---|---|
|antmaze-umaze|**99.0**_±_3_._0|**99.0**_±_3_._0|
|umaze-diverse|89_._0_±_7_._0|**90.0**_±_6_._3|
|medium-play|86_._7_±_11_._5|**94.4**_±_6_._8|
|medium-diverse|83_._0_±_10_._1|**94.0**_±_8_._0|
|large-play|59_._0_±_25_._5|**67.0**_±_26_._1|
|large-diverse|51_._0_±_27_._0|**66.0**_±_30_._4|
|Average|77_._62|**85.07**|


Table 2: Average normalized score on ten unseen seeds on **AntMaze** . _±_ represents the standard deviation across seeds. 

**Results.** Across D4RL [Fu et al., 2020] continuous-control tasks, `DiffMPC` outperforms existing strong offline RL baselines (see Table 1). It achieves average normalized scores of 98 _._ 5 on Gym MuJoCo (vs. ReBRAC 93 _._ 9). On all datasets, our method `DiffMPC` improves the performance from the pre-trained ReBRAC policy, showing that inference time adaptation of the policy brings statistical benefits. We also compare `DiffMPC` with the pre-trained ReBRAC (outperforms TD3+BC, IQL, CQL and SAC-RND in [Tarasov et al., 2023a]) on D4RL Antmaze task in Table 2 and show that inference time adaptation improves the performance. Our method acheives an average score of 85 _._ 07 on AntMaze (vs. ReBRAC 77 _._ 62), with the largest gains on hard AntMaze variants (large-play 59 _→_ 67, large-diverse 51 _→_ 66). 

**Generative Model Baselines.** We also compare against generative model based approaches to Offline RL. Decision Transformer (DT) casts offline RL as return conditioned sequence modeling and predicts actions with a Transformer conditioned on the desired return and history Chen et al. [2021]. Trajectory Transformer (TT) models trajectories as sequences and plans by decoding high reward trajectories under the learned sequence model Janner et al. [2021]. MOPO learns a dynamics model from offline data and optimizes a policy in the learned model while penalizing rewards using model uncertainty to discourage exploiting model errors Yu et al. [2020]. MOReL constructs a pessimistic surrogate MDP that transitions to an absorbing state in regions where the model is unreliable, then learns a policy within this conservative MDP Kidambi et al. [2020]. MBOP performs model predictive planning in a learned dynamics model while constraining candidate action sequences with a behavior prior and extending the horizon with a value estimate Argenson and Dulac-Arnold [2021]. Finally, Diffuser learns a diffusion model over trajectories and plans by iterative denoising with flexible conditioning, so sampling corresponds to generating high reward behavior consistent with the constraints Janner et al. [2022a]. Since prior generative-model baselines report MuJoCo results on a subset of D4RL tasks, we use the same evaluation subset for a direct comparison. Table 3 shows that `DiffMPC` consistently outperforms prior generative model based offline RL approaches across all environments. In particular, `DiffMPC` achieves the best average score of 94 _._ 4, outperforming Diffuser at 77 _._ 5. 

**MPC-based baselines.** We also compare against recent MPC-based approaches for continuous control. TD-MPC and TD-MPC2 use learned latent dynamics together with Model Predictive Path Integral (MPPI) control: at each step, candidate action sequences are sampled, rolled out through the latent dynamics, scored using reward and terminal value estimates, and iteratively refined into a sampling distribution from which 

9 

|Dataset|DT|TT|MOPO|MOReL|MBOP|Diffuser|`DiffMPC`|
|---|---|---|---|---|---|---|---|
||||**H**|**alfCheetah**||||
|medium-expert|86.8|95.0|63.3|53.3|**105.9**|88_._9_±_0_._3|105_._35_±_1_._8|
|medium|42.6|46.9|42.3|42.1|44.6|42_._8_±_0_._3|**70.05**_±_1_._8|
|medium-replay|36.6|41.9|53.1|40.2|42.3|37_._7_±_0_._5|**59.89**_±_1_._2|
|||||**Hopper**||||
|medium-expert|107.6|**110.0**|23.7|108.7|55.1|103_._3_±_1_._3|107_._420_±_5_._30|
|medium|67.6|61.1|28.0|95.4|48.8|74_._3_±_1_._4|**103.38**_±_0_._35|
|medium-replay|82.7|91.5|67.5|93.6|12.4|93_._6_±_0_._4|**103.14**_±_0_._45|
|||||**Walker2d**||||
|medium-expert|108.1|101.9|44.6|95.6|70.2|106_._9_±_0_._2|**115.76**_±_1_._04|
|medium|74.0|79.0|17.8|77.8|41.0|79_._6_±_0_._55|**88.91**_±_0_._6|
|medium-replay|66.6|82.6|39.0|49.8|9.7|70_._6_±_1_._6|**95.87**_±_1_._19|
|Average|74.7|78.9|42.1|72.9|47.8|77.5|**94.4**|


Table 3: Normalized scores on D4RL MuJoCo tasks. DT, TT, MOPO, MOReL, MBOP, and Diffuser values are taken from Janner et al. [2022b]. The symbol _±_ represents the standard deviation across the seeds. 

the first action is executed [Hansen et al., 2022, 2024]. These methods are developed for online control, where the replay buffer is populated by ongoing environment interaction; we provide a detailed comparison with these latent-space MPC methods, together with TD-MPC2 result tables on D4RL Gym-MuJoCo, in Appendix E.1. We further compare against gradient-based optimization of action sequences through learned differentiable rollouts [V et al., 2023]; Appendix E.2 gives the detailed design-space comparison and the full action-update ablation. In both cases, `DiffMPC` outperforms the corresponding baselines on offline D4RL Gym-MuJoCo datasets. 

Finally, we compare against D-MPC, a diffusion-based MPC method that trains a diffusion action proposal and a diffusion dynamics model from offline data, then performs gradient-free MPC by random shooting over sampled action sequences [Zhou et al., 2024]. D-MPC improves over prior model-based MPC baselines such as MBOP, but on the locomotion subset in its original comparison, its average score remains below other offline RL baselines (which `DiffMPC` outperforms). Unlike D-MPC, which selects the best sampled open-loop action sequence, `DiffMPC` updates the pa- 

|Task Name|D-MPC|`DiffMPC`|
|---|---|---|
|halfcheetah medium|46_._00_±_0_._17|**70.05**_±_1_._8|
|hopper medium|61_._24_±_2_._30|**103.38**_±_0_._35|
|walker2d medium|76_._21_±_2_._67|**88.91**_±_0_._6|
|halfcheetah medium-replay|41_._12_±_0_._31|**59.89**_±_1_._2|
|hopper medium-replay|92_._49_±_2_._23|**103.14**_±_0_._45|
|walker2d medium-replay|78_._81_±_4_._19|**95.87**_±_1_._19|
|Average|65_._98|**86.87**|


Table 4: Average normalized score on ten unseen seeds. _±_ represents the standard deviation across seeds. 

10 

rameters of a pretrained policy by backpropagating through differentiable imagined rollouts inside the MPC loop. The detailed comparison is given in Appendix E.3, Since D-MPC reports MuJoCo results on a subset of D4RL tasks, we use the same evaluation subset for a direct comparison. Table 4 shows that `DiffMPC` achieves an average normalized score of 86 _._ 87, compared with 65 _._ 98 for D-MPC, and improves over D-MPC on all six tasks. 

**Ablation.** We conduct extensive ablations on the key hyperparameters of `DiffMPC` : planning horizon _H_ , inner gradient steps _E_ , step size _η_ , DDIM sampling steps _K_ , and the number of Monte Carlo particles _M_ , across all Gym-MuJoCo datasets (Appendix D). The method is robust across a wide range: moderate horizons ( _H ∈{_ 5 _,_ 10 _}_ ) and a single inner step ( _E_ = 1) recover most of the gains from inference-time adaptation at modest cost, while _M_ has negligible effect within _{_ 512 _,_ 1024 _,_ 4096 _}_ . Larger _E_ and _η_ yield further improvements on stable environments such as Walker2d, but can amplify model and value errors on termination-sensitive tasks like Hopper, consistent with known failure modes of offline RL under aggressive policy updates. The DDIM ablation shows diminishing returns from additional denoising steps on most datasets, motivating the one-step MeanFlow sampler in Section 6. We additionally validate `DiffMPC` with SAC-RND as the pre-trained policy, where it improves the average normalized score from 84 _._ 08 to 93 _._ 00 (Appendix D.6). 

## **6 Inference-Time Compute and One-Step World Model** 

|_H_|Zero-shot (ms/step)|DiffMPC (ms/step)|
|---|---|---|
|1|0_._409_±_0_._053|48_._42_±_0_._98|
|2|0_._409_±_0_._053|84_._76_±_1_._76|
|5|0_._409_±_0_._053|194_._96_±_14_._51|


|_K_|Zero-shot (ms/step)|DiffMPC (ms/step)|
|---|---|---|
|1|0_._390_±_0_._049|57_._36_±_1_._51|
|5|0_._390_±_0_._049|121_._86_±_11_._37|
|10|0_._390_±_0_._049|198_._77_±_24_._64|


Table 5: Per-step wall-clock time on Hopper while sweeping planning horizon _H_ (DDIM denoising steps _K_ = 10, inner gradient steps _E_ = 1, one episode of 1000 steps, mean _±_ std). 

Table 6: Per-step wall-clock time on Hopper while sweeping DDIM steps _K_ (planning horizon _H_ = 5, inner gradient steps _E_ = 1, one episode of 1000 steps, mean _±_ std). 

A practical limitation of `DiffMPC` is the cost of iterative diffusion sampling: each imagined transition requires _K_ sequential denoising steps, and inference-time MPC issues many such queries per step. Tables 5 and 6 quantify this overhead on Hopper full-replay. The zero-shot ReBRAC policy selects an action in roughly 0 _._ 4 ms, whereas `DiffMPC` at _H_ = 5, _K_ = 10 takes nearly 200 ms per step, almost three orders of magnitude slower. Both the planning horizon and the number of denoising steps contribute roughly linearly to this cost: increasing _H_ from 1 to 5 raises latency from 48 to 195 ms, and increasing _K_ from 1 to 10 raises it from 57 to 199 ms. Since _K_ multiplies the cost of every world-model call inside the rollout, it is the more attractive axis to improve. 

This motivates collapsing the _K_ -step denoising chain into a single forward pass. We replace the diffusion sampler with a one-step _MeanFlow_ model [Geng et al., 2025], which maps ( _st, at, ϵt_ ) to _st_ +1 in a single forward pass while remaining differentiable. To offset the loss of expressiveness from collapsing many denoising steps into one, we additionally train the world model under a _policy-tilted_ objective that upweights state–action pairs likely under a strong pretrained policy, focusing capacity on the regions the deployed controller actually queries. We call the resulting method `FlowMPC` . 

11 

On the D4RL Gym-MuJoCo suite, `FlowMPC` improves the average normalized score over the ReBRAC initialization from 94 _._ 93 to 97 _._ 87, with gains on all 15 datasets. The improvements are largest on the mediumquality datasets where there is the most room for inference-time policy refinement (e.g., halfcheetah-medium 65 _._ 42 _→_ 70 _._ 06, walker2d-medium 84 _._ 79 _→_ 88 _._ 59, halfcheetah-medium-replay 50 _._ 78 _→_ 56 _._ 51), while remaining competitive with `DiffMPC` across most regimes. At the same time, `FlowMPC` reduces per-transition forward latency by roughly 8 _×_ at _K_ = 10 and total forward+backward time by 15–75 _×_ as _K_ grows. Full derivations of the MeanFlow training objective, the policy-tilted scheme, and complete benchmark and latency results are deferred to Appendix F. 

**Scaling the planning horizon.** A second limitation of `DiffMPC` is that inference-time MPC cost scales linearly with horizon _H_ . The natural fix is to replace the autoregressive rollout with a _trajectory-level_ generator producing ( _st_ +1 _, . . . , st_ + _H_ ) in one forward pass, conditioned on the current state and policy. Several recent works pursue this (though not at inference time): Rigter et al. [2024] train a diffusion model for on-policy trajectories via policy-gradient guidance, Jackson et al. [2024] use policy-guided diffusion under a regularized target, and Ajay et al. [2023] cast offline decision-making as conditional trajectory generation with classifier-free return guidance. The challenge in our setting is that _πψ_ is updated at inference time, so the generator must produce rollouts consistent with the _current πψ_ without autoregressive unrolling. Possible approaches: policy-gradient guidance during sampling (à la PolyGRAD), or periodic fine-tuning of the generator with policy scores via RL-based methods [Black et al., 2024] or adjoint matching [Domingo-Enrich et al., 2025]. We view this as a promising path to amortize the per-step cost of long-horizon `DiffMPC` , and leave a thorough exploration to future work. 

Our primary goal in this work is to demonstrate the statistical benefits of inference-time policy optimization with differentiable world models. We take initial steps toward reducing its computational cost, through FlowMPC and the discussion of trajectory-level generation above, and leave a more thorough investigation to future work. 

## **7 Conclusion** 

We introduced an inference-time adaptation framework for offline RL that refines a pretrained policy on the fly using the current state and a learned differentiable world model. The core design is a Differentiable World Model pipeline that supports end-to-end gradient computation through imagined finite-horizon rollouts, enabling direct optimization of policy parameters at deployment via a surrogate objective combining predicted rewards and a terminal critic. Our diffusion instantiation, `DiffMPC` , yields consistent gains over strong offline RL baselines across D4RL Gym MuJoCo and AntMaze. Recognizing that iterative diffusion sampling is the dominant inference-time cost, we proposed `FlowMPC` , a one-step MeanFlow variant trained under a policy-tilted objective, which recovers most of the gains at a fraction of the wall-clock cost. Together, these results show that inference-time computation, properly amortized, is a practical lever for offline RL. Promising directions for future work include trajectory-level generative world models that produce finitehorizon futures in a single pass, evaluations using generative policies (eg. Flow Q-Learning [Park et al., 2025]), and offline-to-online extensions with periodic world-model updates to improve robustness under distribution shift. 

12 

## **References** 

- M. M. Afsar, T. Crump, and B. Far. Reinforcement learning based recommender systems: A survey. _ACM Computing Surveys_ , 2022. 

- A. Ajay, Y. Du, A. Gupta, J. B. Tenenbaum, T. Jaakkola, and P. Agrawal. Is conditional generative modeling all you need for decision-making? In _International Conference on Learning Representations (ICLR)_ , 2023. arXiv:2211.15657. 

- A. Antos, R. Munos, and C. Szepesvári. Fitted q-iteration in continuous action-space mdps. In _Advances in Neural Information Processing Systems_ , 2007. URL https://papers.nips.cc/paper/ 3233-fitted-q-iteration-in-continuous-action-space-mdps. 

- A. Argenson and G. Dulac-Arnold. Model-based offline planning. In _International Conference on Learning Representations (ICLR)_ , 2021. doi: 10.48550/arXiv.2008.05556. URL https://openreview.net/ forum?id=OMNB1G5xzd4. 

- K. Black, M. Janner, Y. Du, I. Kostrikov, and S. Levine. Training diffusion models with reinforcement learning. In _International Conference on Learning Representations (ICLR)_ , 2024. URL https:// arxiv.org/abs/2305.13301. 

- D. Brandfonbrener, W. F. Whitney, R. Ranganath, and J. Bruna. Offline rl without off-policy evaluation. In _Advances in Neural Information Processing Systems_ , volume 34, pages 4933–4946, 2021. 

- H. Cai, K. Ren, W. Zhang, K. Malialis, J. Wang, Y. Yu, and D. Guo. Real-time bidding by reinforcement learning in display advertising. In _Proceedings of the Tenth ACM International Conference on Web Search and Data Mining_ , pages 661–670, 2017. 

- E. F. Camacho and C. Bordons. _Model Predictive Control_ . Springer, London, 2 edition, 2007. doi: 10.1007/978-0-85729-398-5. 

- L. Chen, K. Lu, A. Rajeswaran, K. Lee, A. Grover, M. Laskin, P. Abbeel, A. Srinivas, and I. Mordatch. Decision transformer: Reinforcement learning via sequence modeling. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2021. 

- M. P. Deisenroth and C. E. Rasmussen. PILCO: A model-based and data-efficient approach to policy search. In _Proceedings of the 28th International Conference on Machine Learning (ICML)_ , pages 465–472, 2011. 

- Z. Ding, A. Zhang, Y. Tian, and Q. Zheng. Diffusion world model: Future modeling beyond step-by-step rollout for offline reinforcement learning. _arXiv preprint arXiv:2402.03570_ , 2024. 

- C. Domingo-Enrich, M. Drozdzal, B. Karrer, and R. T. Q. Chen. Adjoint matching: Fine-tuning flow and diffusion generative models with memoryless stochastic optimal control. In _International Conference on Learning Representations (ICLR)_ , 2025. URL https://arxiv.org/abs/2409.08861. 

- S. Emmons, B. Eysenbach, I. Kostrikov, and S. Levine. Rvs: What is essential for offline rl via supervised learning?, 2021. URL https://arxiv.org/abs/2112.10751. 

- D. Ernst, P. Geurts, and L. Wehenkel. Tree-based batch mode reinforcement learning. _Journal of Machine Learning Research_ , 6:503–556, 2005. 

- M. Fatemi, A. Benz, A. Carnicelli, and M. Ghassemi. Semi-markov offline reinforcement learning for 

13 

healthcare. In _Proceedings of the 2nd Machine Learning for Health Symposium_ , volume 174 of _Proceedings of Machine Learning Research_ , pages 299–315, 2022. 

- J. Fu, A. Kumar, O. Nachum, G. Tucker, and S. Levine. D4rl: Datasets for deep data-driven reinforcement learning, 2020. 

- S. Fujimoto and S. S. Gu. A minimalist approach to offline reinforcement learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2021. 

- S. Fujimoto, D. Meger, and D. Precup. Off-policy deep reinforcement learning without exploration. In _Proceedings of the 36th International Conference on Machine Learning (ICML)_ , volume 97 of _Proceedings of Machine Learning Research_ , pages 2052–2062. PMLR, 2019a. URL https://proceedings. mlr.press/v97/fujimoto19a.html. 

- S. Fujimoto, D. Meger, and D. Precup. Off-policy deep reinforcement learning without exploration. In _Proceedings of the 36th International Conference on Machine Learning_ , volume 97 of _Proceedings of Machine Learning Research_ , pages 2052–2062, 2019b. 

- Z. Geng, M. Deng, X. Bai, J. Z. Kolter, and K. He. Mean flows for one-step generative modeling, 2025. URL https://arxiv.org/abs/2505.13447. 

- O. Gottesman, F. Johansson, J. Meier, M. Denton, D. Lee, S. Srinivasan, L. Zhang, Y. Ding, S. Wihl, X. Peng, J. Yao, I. Lage, C. Mosch, L. H. Sonabend, R. Ranganath, L. A. Celi, and F. Doshi-Velez. Guidelines for reinforcement learning in healthcare. _Nature Medicine_ , 25(1):16–18, 2019. 

- D. Hafner, T. Lillicrap, I. Fischer, R. Villegas, D. Ha, H. Lee, and J. Davidson. Learning latent dynamics for planning from pixels. In _Proceedings of the 36th International Conference on Machine Learning (ICML)_ , pages 2555–2565, 2019. 

- D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi. Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations (ICLR)_ , 2020. 

- D. Hafner, T. Lillicrap, M. Norouzi, and J. Ba. Mastering Atari with discrete world models. In _International Conference on Learning Representations (ICLR)_ , 2021. 

- D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap. Mastering diverse control tasks through world models. _Nature_ , 640(8059):647–653, 2025. doi: 10.1038/s41586-025-08744-2. 

- N. Hansen, X. Wang, and H. Su. Temporal difference learning for model predictive control. In _Proceedings of the 39th International Conference on Machine Learning (ICML)_ , pages 8387–8406, 2022. 

- N. Hansen, H. Su, and X. Wang. TD-MPC2: Scalable, robust world models for continuous control. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- N. Heess, G. Wayne, D. Silver, T. Lillicrap, T. Erez, and Y. Tassa. Learning continuous control policies by stochastic value gradients. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 28, 2015. 

- J. Ho, A. Jain, and P. Abbeel. Denoising diffusion probabilistic models. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 33, pages 6840–6851, 2020. 

- Z. Hou, X. Lv, R. Lu, J. Zhang, Y. Li, Z. Yao, J. Li, J. Tang, and Y. Dong. T1: Advancing language model reasoning through reinforcement learning and inference scaling. In A. Singh, M. Fazel, D. Hsu, 

14 

S. Lacoste-Julien, F. Berkenkamp, T. Maharaj, K. Wagstaff, and J. Zhu, editors, _Proceedings of the 42nd International Conference on Machine Learning_ , volume 267 of _Proceedings of Machine Learning Research_ , pages 23976–24003. PMLR, 13–19 Jul 2025. URL https://proceedings.mlr.press/v267/ hou25e.html. 

- M. T. Jackson, M. T. Matthews, C. Lu, B. Ellis, S. Whiteson, and J. N. Foerster. Policy-guided diffusion. In _Reinforcement Learning Conference (RLC)_ , 2024. URL https://arxiv.org/abs/2404.06356. 

- M. Janner, Q. Li, and S. Levine. Offline reinforcement learning as one big sequence modeling problem. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 34, pages 1273–1286, 2021. doi: 10.48550/arXiv.2106.02039. URL https://papers.neurips.cc/paper_files/paper/ 2021/hash/099fe6b0b444c23836c4a5d07346082b-Abstract.html. 

- M. Janner, Y. Du, J. B. Tenenbaum, and S. Levine. Planning with diffusion for flexible behavior synthesis. In _International Conference on Machine Learning (ICML)_ , 2022a. 

- M. Janner, Y. Du, J. B. Tenenbaum, and S. Levine. Planning with diffusion for flexible behavior synthesis. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2022b. 

- N. Jiang and L. Li. Doubly robust off-policy value evaluation for reinforcement learning. In _Proceedings of The 33rd International Conference on Machine Learning_ , volume 48 of _Proceedings of Machine Learning Research_ , pages 652–661. PMLR, 2016. URL https://proceedings.mlr.press/ v48/jiang16.html. 

- D. Ki, J. Oh, S.-W. Shim, and B.-J. Lee. Prior-guided diffusion planning for offline reinforcement learning. _arXiv preprint arXiv:2505.10881_ , 2025. 

- R. Kidambi, A. Rajeswaran, P. Netrapalli, and T. Joachims. Morel: Model-based offline reinforcement learning. _arXiv preprint arXiv:2005.05951_ , 2020. 

- B. R. Kiran, I. Sobh, V. Talpaert, P. Mannion, A. A. A. Sallab, S. Yogamani, and P. Pérez. Deep reinforcement learning for autonomous driving: A survey. _IEEE Transactions on Intelligent Transportation Systems_ , 23 (6):4909–4926, 2022. 

- J. Kober, J. A. Bagnell, and J. Peters. Reinforcement learning in robotics: A survey. _The International Journal of Robotics Research_ , 32(11):1238–1274, 2013. 

- I. Kostrikov, A. Nair, and S. Levine. Offline reinforcement learning with implicit q-learning. In _International Conference on Learning Representations (ICLR)_ , 2022. 

- A. Kumar, J. Fu, G. Tucker, and S. Levine. Stabilizing off-policy q-learning via bootstrapping error reduction. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2019. doi: 10.48550/arXiv.1906.00949. URL https://papers.nips.cc/paper/2019/hash/ 2f4d86d9b4d1d7c0b8b6d81e2a9c3f2b-Abstract.html. 

- A. Kumar, A. Zhou, G. Tucker, and S. Levine. Conservative q-learning for offline reinforcement learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2020. 

- M. G. Lagoudakis and R. Parr. Least-squares policy iteration. _Journal of Machine Learning Research_ , 4: 1107–1149, 2003. URL https://www.jmlr.org/papers/v4/lagoudakis03a.html. 

15 

- S. Lange, T. Gabel, and M. Riedmiller. Batch reinforcement learning. In M. Wiering and M. van Otterlo, editors, _Reinforcement Learning: State-of-the-Art_ . Springer, 2012. 

- J. Lee, W. Jeon, B. Lee, J. Pineau, and K.-E. Kim. Optidice: Offline policy optimization via stationary distribution correction estimation. In _Proceedings of the 38th International Conference on Machine Learning_ , volume 139 of _Proceedings of Machine Learning Research_ , pages 6120–6130. PMLR, 2021. URL https://proceedings.mlr.press/v139/lee21f.html. 

- S. Levine, A. Kumar, G. Tucker, and J. Fu. Offline reinforcement learning: Tutorial, review, and perspectives on open problems. _arXiv preprint arXiv:2005.01643_ , 2020. 

- Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, and M. Le. Flow matching for generative modeling, 2022. URL https://arxiv.org/abs/2210.02747. 

- X. Liu, C. Gong, and Q. Liu. Flow straight and fast: Learning to generate and transfer data with rectified flow, 2022. URL https://arxiv.org/abs/2209.03003. 

- Y. Liu, A. Swaminathan, A. Agarwal, and E. Brunskill. Provably good batch reinforcement learning without great exploration. In _Advances in Neural Information Processing Systems_ , volume 33, pages 1264–1274, 2020. 

- N. Muennighoff, Z. Yang, W. Shi, X. L. Li, L. Fei-Fei, H. Hajishirzi, L. Zettlemoyer, P. Liang, E. Candès, and T. Hashimoto. s1: Simple test-time scaling. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , 2025. URL https://aclanthology.org/2025.emnlp-main. 1025/. 

- R. Munos and C. Szepesvári. Finite-time bounds for fitted value iteration. _Journal of Machine Learning Research_ , 9:815–857, 2008. URL https://www.jmlr.org/papers/v9/munos08a.html. 

- A. Nair, M. Dalal, A. Gupta, and S. Levine. Awac: Accelerating online reinforcement learning with offline datasets. In _International Conference on Learning Representations (ICLR)_ , 2021. doi: 10.48550/arXiv. 2006.09359. URL https://openreview.net/forum?id=OJiM1R3jAtZ. 

- S. Park, Q. Li, and S. Levine. Flow q-learning. In _Proceedings of the 42nd International Conference on Machine Learning_ , volume 267 of _Proceedings of Machine Learning Research_ , pages 48104–48127. PMLR, 2025. 

- X. B. Peng, A. Kumar, G. Zhang, and S. Levine. Advantage-weighted regression: Simple and scalable off-policy reinforcement learning, 2019. URL https://arxiv.org/abs/1910.00177. 

- R. F. Prudencio, M. R. O. A. Maximo, and E. L. Colombini. A survey on offline reinforcement learning: Taxonomy, review, and open problems. _IEEE Transactions on Neural Networks and Learning Systems_ , 2022. 

- J. B. Rawlings, D. Q. Mayne, and M. Diehl. _Model Predictive Control: Theory, Computation, and Design_ . Nob Hill Publishing, Madison, WI, 2 edition, 2017. 2nd edition. Available at: https://sites. engineering.ucsb.edu/~jbraw/mpc/. 

- M. Riedmiller. Neural fitted q iteration - first experiences with a data efficient neural reinforcement learning method. In J. Gama, R. Camacho, P. Brazdil, A. Jorge, and L. Torgo, editors, _Proceedings of the Sixteenth European Conference on Machine Learning (ECML 2005)_ , volume 3720 of _Lecture Notes in Computer_ 

16 

_Science_ , pages 317–328. Springer, 2005. URL http://www.ni.uos.de/fileadmin/user_ upload/publications/riedmiller.ecml2005.official.pdf. 

- M. Rigter, J. Yamada, and I. Posner. World models via policy-guided trajectory diffusion. _Transactions on Machine Learning Research_ , 2024. URL https://arxiv.org/abs/2312.08533. 

- A. Romero, E. Aljalbout, Y. Song, and D. Scaramuzza. Actor–critic model predictive control: Differentiable optimization meets reinforcement learning for agile flight. _IEEE Transactions on Robotics_ , 2025. doi: 10.1109/TRO.2025.3644945. 

- D. Shah, A. Bhorkar, H. Leen, I. Kostrikov, N. Rhinehart, and S. Levine. Offline reinforcement learning for visual navigation. In _Proceedings of The 6th Conference on Robot Learning_ , volume 205 of _Proceedings of Machine Learning Research_ , pages 44–54, 2023. 

- T. Shi, Y. Li, Y. Liu, and H. Wang. Offline reinforcement learning for autonomous driving with safety and exploration enhancement. _arXiv preprint arXiv:2110.07067_ , 2021. 

- D. Tarasov, V. Kurenkov, A. Nikulin, and S. Kolesnikov. Revisiting the minimalist approach to offline reinforcement learning. _arXiv preprint arXiv:2305.09836_ , 2023a. doi: 10.48550/arXiv.2305.09836. 

- D. Tarasov, V. Kurenkov, A. Nikulin, and S. Kolesnikov. Revisiting the minimalist approach to offline reinforcement learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2023b. 

- P. Thomas and E. Brunskill. Data-efficient off-policy policy evaluation for reinforcement learning. In _Proceedings of The 33rd International Conference on Machine Learning_ , volume 48 of _Proceedings of Machine Learning Research_ , pages 2139–2148. PMLR, 2016. URL https://proceedings.mlr. press/v48/thomasa16.html. 

- J. S. V, S. Jalagam, Y. LeCun, and V. Sobal. Gradient-based planning with world models. _arXiv preprint arXiv:2312.17227_ , 2023. 

- S. Venkataraman, Y. Wang, Z. Wang, N. R. T. Chintalapati, Z. Erickson, and D. Held. Real-world offline reinforcement learning from vision-language model feedback. _arXiv preprint arXiv:2411.05273_ , 2024. 

- X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang, A. Chowdhery, and D. Zhou. Self-consistency improves chain of thought reasoning in language models. In _The Eleventh International Conference on Learning Representations_ , 2023. URL https://openreview.net/forum?id=1PL1NIMMrw. 

- Z. Wang, A. Novikov, K. Zolna, J. T. Springenberg, S. Reed, B. Shahriari, N. Siegel, J. Merel, C. Gulcehre, N. Heess, and N. de Freitas. Critic regularized regression, 2020. URL https://arxiv.org/abs/ 2006.15134. 

- Z. Wang, J. J. Hunt, and M. Zhou. Diffusion policies as an expressive policy class for offline reinforcement learning, 2022. URL https://arxiv.org/abs/2208.06193. 

- Y. Wu, G. Tucker, and O. Nachum. Behavior regularized offline reinforcement learning. _arXiv preprint arXiv:1911.11361_ , 2019. doi: 10.48550/arXiv.1911.11361. 

- T. Xiao and D. Wang. A general offline reinforcement learning framework for interactive recommendation. _arXiv preprint arXiv:2310.00678_ , 2023. 

- S. Yao, D. Yu, J. Zhao, I. Shafran, T. L. Griffiths, Y. Cao, and K. R. Narasimhan. Tree of thoughts: Deliberate 

17 

problem solving with large language models. In _Advances in Neural Information Processing Systems_ , 2023. URL https://openreview.net/forum?id=5Xc1ecxO1h. 

- C. Yu, J. Liu, and S. Nemati. Reinforcement learning in healthcare: A survey. _ACM Computing Surveys_ , 55 (1):1–36, 2021a. 

- T. Yu, G. Thomas, L. Yu, S. Ermon, J. Zou, S. Levine, C. Finn, and T. Ma. Mopo: Model-based offline policy optimization. _arXiv preprint arXiv:2005.13239_ , 2020. 

- T. Yu, A. Kumar, R. Rafailov, A. Rajeswaran, S. Levine, and C. Finn. Combo: Conservative offline model-based policy optimization. _arXiv preprint arXiv:2102.08363_ , 2021b. 

- T. Yun, S. Yun, J. Lee, and J. Park. Guided trajectory generation with diffusion models for offline model-based optimization. _arXiv preprint arXiv:2407.01624_ , 2024. 

- X. Zhao, C. Gu, H. Zhang, X. Yang, X. Liu, H. Liu, and J. Tang. Dear: Deep reinforcement learning for online advertising impression in recommender systems. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 35, pages 750–758, 2021. 

- G. Zhou, L. Ke, S. Srinivasa, A. Gupta, A. Rajeswaran, and V. Kumar. Real world offline reinforcement learning with realistic data source. _arXiv preprint arXiv:2210.06479_ , 2022. 

- G. Zhou, S. Swaminathan, R. V. Raju, J. S. Guntupalli, W. Lehrach, J. Ortiz, A. Dedieu, M. Lázaro-Gredilla, and K. Murphy. Diffusion model predictive control. _Transactions on Machine Learning Research_ , 2024. URL https://openreview.net/forum?id=pvtgffHtJm. 

- Y. Zuo, K. Zhang, L. Sheng, S. Qu, G. Cui, X. Zhu, H. Li, Y. Zhang, X. Long, E. Hua, B. Qi, Y. Sun, Z. Ma, L. Yuan, N. Ding, and B. Zhou. Ttrl: Test-time reinforcement learning. In _Advances in Neural Information Processing Systems_ , 2025. URL https://openreview.net/forum?id=VuVhgEiu20. 

18 

## **A Related Works** 

**Offline reinforcement learning.** Offline reinforcement learning studies how to learn a high return policy from a fixed dataset while mitigating distribution shift between the learned policy and the logged behavior Lange et al. [2012], Levine et al. [2020]. A large family of methods constrains policy improvement to remain close to actions supported by the dataset, either by explicitly regularizing the learned policy toward behavior cloning or by limiting the space of candidate actions used for value based updates Wu et al. [2019], Fujimoto et al. [2019a], Kumar et al. [2019], Fujimoto and Gu [2021], Tarasov et al. [2023b]. Another family focuses on conservative value estimation to reduce overestimation when evaluating actions that are unlikely under the dataset, with CQL penalizing high values assigned to low density actions Kumar et al. [2020]. Complementary approaches avoid explicit out of distribution action maximization during policy improvement by extracting policies from value functions using implicit or advantage weighted updates, as in IQL and AWAC Kostrikov et al. [2022], Nair et al. [2021]. Across these lines, the shared objective is to maximize return while ensuring that learning and improvement remain grounded in the support of the offline data. 

**Batch reinforcement learning and approximate dynamic programming.** Offline RL is closely related to earlier work on _batch_ reinforcement learning and approximate dynamic programming, where policies are learned from logged transition tuples without additional interaction. Classical fitted value-iteration style methods include tree-based fitted Q-iteration [Ernst et al., 2005] and least-squares policy iteration [Lagoudakis and Parr, 2003], along with neural fitted Q-iteration (NFQ) as an early neural approach [Riedmiller, 2005]. These methods clarified the basic promise of learning from static data and the practical dependence on function approximation, dataset coverage, and policy evaluation quality; for broader background, see the batch RL chapter by Lange et al. [2012] and the modern offline RL tutorial by Levine et al. [2020]. 

**Coverage, distribution shift, and off-policy evaluation.** A recurring theme since early approximate dynamic programming is that learning from a fixed dataset hinges on how well the data covers the state– action regions needed by the learned policy. Analyses of fitted value iteration make this dependence explicit through approximation and sampling error terms that are amplified by distribution shift across Bellman backups [Munos and Szepesvári, 2008, Antos et al., 2007]. In parallel, the offline setting is tightly connected to off-policy evaluation (OPE), which estimates the performance of a target policy from data generated by different behavior policies. Doubly robust estimators [Jiang and Li, 2016] and subsequent refinements aimed at variance control and model-based mixing [Thomas and Brunskill, 2016] highlight the statistical difficulty of evaluating and optimizing policies under mismatch, which later offline RL methods address implicitly through regularization or pessimism. 

**Deep model-free offline RL.** With deep function approximation, naïve off-policy actor–critic can fail offline due to extrapolation error on actions that are weakly supported by the dataset, which is then compounded by bootstrapping [Kumar et al., 2019, Fujimoto et al., 2019b]. Many practical algorithms can be viewed as enforcing _policy support constraints_ during improvement. Behavior-regularized actor–critic [Wu et al., 2019] and advantage-weighted updates [Peng et al., 2019] bias learning toward dataset actions, while criticregularized regression [Wang et al., 2020] fits policies via weighted regression modulated by value estimates. A particularly influential baseline is TD3+BC, which augments an online actor update with a behavior cloning term and careful normalization [Fujimoto and Gu, 2021]. Another line seeks _pessimism_ in value estimation: Conservative Q-Learning (CQL) explicitly lowers Q-values for out-of-distribution actions [Kumar et al., 2020], and Implicit Q-Learning (IQL) avoids explicit maximization over unseen actions by combining 

19 

expectile value regression with advantage-weighted policy updates [Kostrikov et al., 2022]. Density-ratio and stationary-distribution correction viewpoints also motivate offline policy optimization; for example, Lee et al. [2021] estimate distribution corrections to optimize policies from fixed data. 

**Model-based offline RL.** Model-based offline RL learns a dynamics model from logged data and uses model rollouts for planning or for generating additional training targets, but must guard against _model exploitation_ when rollouts drift out of support. MOPO penalizes uncertainty to discourage out-of-distribution model rollouts [Yu et al., 2020], MOReL constructs pessimistic MDP variants to avoid unreliable regions [Kidambi et al., 2020], and COMBO combines model rollouts with conservative value regularization [Yu et al., 2021b]. Planning-first formulations such as MBOP emphasize using learned models and short-horizon planning as the primary control mechanism under offline training [Argenson and Dulac-Arnold, 2021]. Collectively, these works frame a core tradeoff between using model-based lookahead to improve decisions and controlling error accumulation from imperfect learned dynamics. 

**Offline RL as sequence modeling and generative policy classes.** A complementary direction casts offline RL as conditional sequence modeling, learning to output actions from trajectory context rather than performing Bellman backups. Decision Transformer [Chen et al., 2021] conditions on desired returns, while Trajectory Transformer treats trajectories as token sequences for planning and action selection [Janner et al., 2021]. More recently, Emmons et al. [2021] study when supervised learning alone can suffice for strong offline performance, emphasizing choices of conditioning information and model capacity. Separately, generative modeling has been used to enlarge policy classes while retaining dataset support; diffusion-based policy representations such as Diffusion-QL [Wang et al., 2022] and diffusion planners [Janner et al., 2022a] demonstrate strong performance but typically require iterative sampling at inference. 

## **B Diffusion Sampler and Rollout Gradients** 

### **B.1 Differentiable Diffusion Sampler** 

Our objective is to learn a parametric differentiable diffusion sampler that conditioned on a given state-action pair _st, at_ at time _t_ and sampled noise _ϵt_ generates the next state _st_ +1 as follows: _st_ +1 = _fθ_ ( _st, at, εt_ ) _, εt ∼ p_ 0( _ε_ ). Here _fθ_ is the _reverse diffusion sampler_ , written as a deterministic computation graph, and _εt_ is a collection of Gaussian random variables used in the generation process. Equivalently, the diffusion model specifies a conditional distribution over next states, _pθ_ ( _st_ +1 _| st, at_ ), together with a reparameterized sampling procedure _st_ +1 = _fθ_ ( _st, at, εt_ ) whose randomness is isolated in _εt_ . 

We learn _pθ_ ( _st_ +1 _| st, at_ ) from an offline dataset of transitions _D_ = _{_ ( _st, at, rt, st_ +1) _}_<sup>_N_</sup> _t_ =1<sup>_._The diffusion</sup> model is trained to represent the conditional law of _st_ +1 given ( _st, at_ ) by introducing a _forward noising process_ on _st_ +1 and a learned _reverse denoising process_ that inverts this noising when conditioned on ( _st, at_ ). At sampling time, the reverse process induces the map _fθ_ . 

**Forward process:** Fix a diffusion horizon _K ∈_ N and a variance schedule _{αk}_<sup>_K_</sup> _k_ =1<sup>_⊂_(0</sup><sup>_,_1).For each</sup> transition tuple ( _st, at, st_ +1) _∈D_ , define a Markovian forward process that progressively corrupts the next state as follows: 


20 

Let _α_ ¯ _k_ :=<sup>�</sup><sup>_k_</sup> _j_ =1<sup>_αj_.This choice implies a closed-form marginal for any noise level</sup><sup>_k_given by</sup><sup>_q_</sup> � _s_<sup>(</sup> _t_ +1<sup>_k_)</sup><sup>_|_</sup> _st_ +1� = _N_ � _~~√~~_ _<u>α</u>_ <u>¯</u> _k st_ +1 _,_ (1 _− α_ ¯ _k_ ) _I_ �. In particular, one can write a reparameterized sample from the marginal as 


**Conditional reverse process:** The reverse process aims to sample _st_ +1 conditioned on ( _st, at_ ) by iteratively denoising from a Gaussian reference distribution at level _K_ . Let the conditioning be _ct_ := ( _st, at_ ) _._ At sampling time, initialize from a base noise variable _s_<sup>(</sup> _t_ +1<sup>_K_)</sup><sup>_∼N_(0</sup><sup>_, I_), and apply a learned reverse transition</sup> for _k ∈_ [ _K −_ 1] using _s_<sup>(</sup> _t_ +1<sup>_k−_1)</sup> = _~~√~~_ <u>1</u> _<u>αk</u>_ � _s_<sup>(</sup> _t_ +1<sup>_k_)</sup><sup>_−_(1</sup><sup>_−αk_) ˆ</sup><sup>_ϵθ_</sup> � _s_<sup>(</sup> _t_ +1<sup>_k_)</sup><sup>_, k, ct_</sup> �<sup>�</sup> + _σkzk−_ 1 _, zk−_ 1 _∼N_ (0 _, I_ ) _._ Here _ϵ_ ˆ _θ_ ( _·, k, ct_ ) is a parametric predictor of the noise component at level _k_ , and _{σk}_ specifies the reverse-process variance. The final denoised sample is _s_<sup>(0)</sup> _t_ +1<sup>_∼pθ_(</sup><sup>_·|st, at_),andwedefinethereversesampler</sup><sup>_fθ_by</sup> collecting all Gaussian random variables used by the reverse procedure into _εt_ := ( _zK, zK−_ 1 _, . . . , z_ 0), so that the sampled next state can be written as _s_<sup>(0)</sup> _t_ +1<sup>=</sup><sup>_fθ_(</sup><sup>_st, at, εt_).We define the initialization map</sup><sup>_gK_: R</sup><sup>_d→_R</sup><sup>_d_</sup> and the reverse-step map _hk_ : R<sup>_d_</sup> _×_ R<sup>_d_</sup> _×_ R<sup>_m_</sup> _×_ R<sup>_d_</sup> _→_ R<sup>_d_</sup> by 


so that _s_<sup>(</sup> _t_ +1<sup>_k−_1)=</sup><sup>_hk_(</sup><sup>_s_(</sup> _t_ +1<sup>_k_)</sup><sup>_, st, at, zk−_1) and</sup><sup>_s_(</sup> _t_ +1<sup>_K_)=</sup><sup>_gK_(</sup><sup>_zK_).</sup> 

**Deterministic computation graph for fixed noise.** For any fixed realization of _εt_ , the mapping ( _st, at_ ) _�→ s_<sup>(0)</sup> _t_ +1<sup>isadeterministiccompositionof(i)linearoperations,(ii)evaluationsofthedenoiser</sup><sup>_ϵ_ˆ</sup><sup>_θ_(</sup><sup>_·, k, ct_)at</sup> each reverse step, and (iii) additive terms determined by the fixed Gaussian draws. Consequently, _fθ_ is a differentiable computation graph in its inputs ( _st, at_ ) for fixed _εt_ . 

**Learning objective:** We train ˆ _ϵθ_ to invert the forward corruption of _st_ +1, conditioned on ( _st, at_ ). Using the marginal reparameterization at a randomly chosen diffusion level _k_ , we form _s_<sup>(</sup> _t_ +1<sup>_k_)=</sup><sup>_~~√~~_</sup> _<u>α</u>_ <u>¯</u> _k st_ +1 + _~~√~~_ 1 _− α_ ¯ _k ϵ, ϵ ∼N_ (0 _, I_ ), and minimize the conditional noise-prediction error 


Intuitively, this objective teaches the denoiser to recover the injected Gaussian noise at arbitrary noise levels while leveraging ( _st, at_ ) as side information. After training, the resulting reverse process defines a conditional generative model _pθ_ ( _st_ +1 _| st, at_ ), and its sampling procedure is precisely the transition map _st_ +1 = _fθ_ ( _st, at, εt_ ) _, εt ∼ p_ 0( _ε_ ), which we treat as a learned, differentiable simulator of one-step dynamics. 

### **B.2 Gradient recursion through diffusion rollouts** 

Recall that given a fixed noise sequence _εt_ : _t_ + _H−_ 1 = ( _εt, . . . , εt_ + _H−_ 1) define the imagined rollout recursively by 


21 

The next theorem states a compact Jacobian recursion for the gradient of the per-noise objective _L_ ( _ψ_ ; _εt_ : _t_ + _H−_ 1) under the rollout dynamics in (2). Define the rollout Jacobians, for _j_ = 0 _, . . . , H −_ 1, 


Let _Gj_ := _∇ψs_ ˜ _j_ and _Dj_ := _∇ψa_ ˜ _j_ . Then _G_ 0 = 0 and, for _j_ = 0 _, . . . , H −_ 1, 


Further define the gradient of the reward and the critic as: 


**Theorem B.1** ( **Gradient recursion** ) **.** _Fix a time t, a horizon H, and a noise sequence εt_ : _t_ + _H−_ 1 _, and let {_ (˜ _sj,_ ˜ _aj_ ) _}_<sup>_H_</sup> _j_ =0<sup>_be defined by_(2)</sup><sup>_.Assume πψis differentiable in ψ and its state input, and fθ, rξ, and Qϕ_</sup> _are differentiable in their state and action arguments._ 

_Then the gradient of the per-noise return is_ 


_Moreover, if fθ is implemented by a reverse diffusion recursion as given by_ (1) _then_ 


_where AK_ = 0 _, BK_ = 0 _, and for k_ = _K, . . . ,_ 1 _,_ 


_with all partial derivatives evaluated at_ ( _u, s, a, z_ ) = ( _s_<sup>(</sup><sup>_k_)</sup> _, s, a, zk−_ 1) _._ 

_Proof._ We fix a time _t_ , horizon _H_ , and a noise sequence _εt_ : _t_ + _H−_ 1. All quantities below are defined along the imagined rollout (2). Since the noise is fixed, the rollout is deterministic, hence the gradient _∇ψL_ ( _ψ_ ; _εt_ : _t_ + _H−_ 1) is obtained by repeated application of the chain rule. 

1. **Sensitivity recursions:** Recall the rollout recursion (2): 


22 

Define the state and action sensitivities 


Since ˜ _s_ 0 = _st_ does not depend on _ψ_ , we have 


For each _h_ , the action is ˜ _ah_ = _πψ_ (˜ _sh_ ). By the chain rule, 


Introduce the policy Jacobians (as in the theorem statement) 


Substituting (7) into (6) yields 


For each _h ∈{_ 0 _, . . . , H −_ 1 _}_ , the next state is ˜ _sh_ +1 = _fθ_ (˜ _sh,_ ˜ _ah, εt_ + _h_ ). Differentiating with respect to _ψ_ and applying the chain rule gives 


Introduce the world-model Jacobians (as in the theorem statement) 


Substituting (10) into (9) yields 


Equations (5), (8), and (11) are exactly the sensitivity recursions stated in Theorem B.1. 

2. **Gradient of the per-noise return** 

Recall the per-noise return definition: 


Fix _h ∈{_ 0 _, . . . , H −_ 1 _}_ and define the stage reward _rh_ := _rξ_ (˜ _sh,_ ˜ _ah_ ). By the chain rule, 


Introduce the shorthand 


23 

Then (13) becomes 


Define the terminal action ˜ _aH_ := _πψ_ (˜ _sH_ ) and the terminal value _VT_ := _Qϕ_ (˜ _sH ,_ ˜ _aH_ ). By the chain rule, 


Introduce the terminal derivatives 


Then (16) becomes 


Here _DH_ is defined exactly as in (4), and can be expanded via the same policy sensitivity identity (8) with _h_ = _H_ : 


Differentiating (12) and applying (15) and (18) gives 


which is the gradient expression stated in Theorem B.1. 

3. **Jacobian Recursion:** Next we derive and prove the Jacobian recursions for _∇afθ_ ( _s, a, ε_ ) and _∇sfθ_ ( _s, a, ε_ ) under the reverse diffusion implementation (1). 

Fix ( _s, a_ ) and a noise pack _ε_ = ( _zK, zK−_ 1 _, . . . , z_ 0). Let _{s_<sup>(</sup><sup>_k_)</sup> _}_<sup>_K_</sup> _k_ =0<sup>be generated by</sup> 


Assume _gK_ is independent of ( _s, a_ ) and each _hk_ ( _u, s, a, z_ ) is differentiable in ( _u, s, a_ ). Define the diffusion-depth sensitivities 


Since _s_<sup>(</sup><sup>_K_)</sup> = _gK_ ( _zK_ ) and _gK_ does not depend on ( _s, a_ ), 


24 

Fix _k ∈{_ 1 _, . . . , K}_ and write (22) as 


Differentiate (26) with respect to _a_ and apply the chain rule: 


where the partial derivatives are evaluated at 


Differentiating (26) with respect to _s_ gives 


with the same evaluation point (28). 

**Iterating to obtain** _∇afθ_ **and** _∇sfθ_ **.** Starting from (25) and iterating (27)–(29) for _k_ = _K, K −_ 1 _, . . . ,_ 1 yields _A_ 0 and _B_ 0. Since _fθ_ ( _s, a, ε_ ) = _s_<sup>(0)</sup> by (23), 


## **C Additional Experimental Details** 

### **C.1 World Model** 

**Diffusion Sampler:** We train a conditional DDPM dynamics model to predict _st_ +1 from ( _st, at_ ) on offline D4RL MuJoCo datasets (Hopper, HalfCheetah, and Walker2d, using standard v2 splits). States and next states are standardized with dataset mean/std (with a small _ϵ_ for numerical stability), while actions are left unnormalized, and training minimizes the _ϵ_ -prediction mean-squared error objective. The denoiser is an MLP with time-embedding dimension 128, hidden size 512, and 4 layers, using _T_ = 200 diffusion steps and a linear _β_ -schedule from 10<sup>_−_4</sup> to 2 _×_ 10<sup>_−_2</sup> . Optimization uses AdamW (learning rate 3 _×_ 10<sup>_−_4</sup> , weight decay 0), batch size 2048, gradient clipping at 1 _._ 0, exponential moving average (EMA) of parameters with decay 0 _._ 999 and is trained for 200k steps. 

**Reward Model:** We train a reward model _rθ_ ( _s, a_ ) as an MLP on D4RL transitions, where the input is the concatenated state-action vector [ _s, a_ ] and the output is a scalar immediate reward prediction. The network uses hidden width 512 with 4 layers total (3 hidden layers plus a final linear output layer). States are normalized using dataset statistics while actions are left unnormalized, and training minimizes MSE with AdamW (learning rate 3 _×_ 10<sup>_−_4</sup> , batch size 2048) for 200k steps with gradient clipping at 1 _._ 0. We checkpoint every 20k steps and run periodic online validation every 5k steps. 

We report the predictive performance of the offline trained diffusion dynamics model and the offline trained reward model across D4RL MuJoCo datasets. Figure 2 shows the diffusion model prediction RMSE across 

25 


Figure 2: One-step state prediction RMSE of diffusion models across training steps (20k–200k) on mediumreplay datasets. RMSE decreases with training for all three environments (halfcheetah, hopper, walker2d), with shaded regions showing standard error over 1000 transitions. 


Figure 3: Reward prediction RMSE of reward models across training steps (20k–200k) on medium-replay datasets. All environments show decreasing RMSE with training. Shaded regions indicate standard error over 1000 transitions. 

training steps, and Figure 3 reports the reward model prediction RMSE across training steps. For final performance, Table 7 reports both diffusion model accuracy, measured by one-step RMSE, and reward model accuracy, measured by reward prediction RMSE, with uncertainty reported as standard error. For the diffusion model, the one-step RMSE is computed using Monte Carlo samples and normalized by the number of transitions. Overall, both models achieve low error on most datasets. 

**Policy and Critic Value:** ReBRAC is a TD3+BC-style offline RL algorithm that uses three-hidden-layer actor and critic networks with hidden dimension 256 and ReLU activations. The critic applies LayerNorm between hidden layers, and both the actor and critic are trained with behavior-regularization penalties whose coefficients are tuned separately. For D4RL Gym-MuJoCo tasks, ReBRAC uses Adam with batch size 1024, learning rate 10<sup>_−_3</sup> for all networks, target update rate _τ_ = 5 _×_ 10<sup>_−_3</sup> , and discount factor _γ_ = 0 _._ 99. The main tuned hyperparameters are the actor and critic regularization coefficients _β_ 1 and _β_ 2. We follow the hyperparameter choices from Tarasov et al. [2023a]. 

26 

|Task|Diffusion one-step RMSE (_±_SE)|Reward RMSE (_±_SE)|
|---|---|---|
|halfcheetah-random|0.2318_±_0.000010|0.0477_±_0.0016|
|halfcheetah-medium|0.5494_±_0.000014|0.1292_±_0.0034|
|halfcheetah-expert|1.3065_±_0.000026|0.2763_±_0.0076|
|halfcheetah-medium-expert|0.5972_±_0.000013|0.1622_±_0.0045|
|halfcheetah-medium-replay|0.3996_±_0.000014|0.0918_±_0.0027|
|halfcheetah-full-replay|0.4739_±_0.000014|0.1164_±_0.0033|
|hopper-random|0.1268_±_0.004497|0.0082_±_0.0003|
|hopper-medium|0.0784_±_0.001281|0.0720_±_0.0030|
|hopper-expert|0.1375_±_0.000755|0.1415_±_0.0058|
|hopper-medium-expert|0.1678_±_0.000710|0.0789_±_0.0033|
|hopper-medium-replay|0.1008_±_0.000764|0.0192_±_0.0005|
|hopper-full-replay|0.1178_±_0.002514|0.0208_±_0.0005|
|walker2d-random|0.6591_±_0.009463|0.0244_±_0.0008|
|walker2d-medium|1.4068_±_0.005905|0.0779_±_0.0020|
|walker2d-expert|3.3412_±_0.014321|0.4902_±_0.0123|
|walker2d-medium-expert|1.5566_±_0.026789|0.1060_±_0.0031|
|walker2d-medium-replay|1.1100_±_0.002611|0.0459_±_0.0013|
|walker2d-full-replay|1.2560_±_0.009531|0.0578_±_0.0022|
|Average|0.7565_±_0.000031|0.1092_±_0.0271|


Table 7: Diffusion one-step RMSE and reward prediction RMSE (mean _±_ standard error) on D4RL MuJoCo datasets. 

### **C.2 Inference time Parameters** 

The inference time parameters for our method are: Horizon Length ( _H_ ), Inner Gradient Steps ( _E_ ), Step size ( _η_ ), and number of particles _M_ . We tune them on a single different seed, which is different from the 10 evaluation seeds. We tune the planning horizon _H ∈{_ 0 _,_ 1 _,_ 2 _,_ 5 _,_ 10 _}_ , the number of inner gradient steps _E ∈{_ 1 _,_ 2 _}_ , and the number of particles _M ∈{_ 2048 _,_ 4096 _,_ 8192 _}_ . For HalfCheetah and Walker2d, we tune the inner step size _η ∈{_ 5 _×_ 10<sup>_−_7</sup> _,_ 5 _×_ 10<sup>_−_6</sup> _,_ 5 _×_ 10<sup>_−_5</sup> _,_ 5 _×_ 10<sup>_−_4</sup> _}_ and for Hopper, _η ∈{_ 5 _×_ 10<sup>_−_8</sup> _,_ 5 _×_ 10<sup>_−_7</sup> _,_ 5 _×_ 10<sup>_−_6</sup> _,_ 1 _×_ 10<sup>_−_5</sup> _,_ 1 _×_ 10<sup>_−_4</sup> _}_ . We keep the DDIM denoising steps _K_ = 10. The choices for each dataset is given below. 

## **D Ablation Studies** 

### **D.1 Horizon Length** 

We conduct ablation studies to understand the effect of the planning horizon _H_ on the performance of `DiffMPC` . Recall that _H_ controls the number of steps over which imagined rollouts are unrolled before the terminal critic _Qϕ_ is applied. 

**Effect of Planning Horizon** _H_ **.** We sweep _H ∈{_ 1 _,_ 2 _,_ 5 _,_ 10 _,_ 20 _}_ across all 18 Gym-MuJoCo datasets and report normalized scores in Tables 9–11. 

27 

Table 8: Hyperparameters for DiffMPC across D4RL datasets. _H_ : horizon length, _E_ : inner gradient steps, _η_ : step size, _M_ : number of particles. 

|Dataset|_H_|_E_|_η_|_M_|
|---|---|---|---|---|
||_halfc_<br>|_heet_<br>|_ah_<br>||
|medium|5|1|5_×_10<sup>_−_4</sup><br>|8,192|
|expert|2|1|5_×_10<sup>_−_6</sup>|4,096|
|medium-expert|5|1|5_×_10<sup>_−_5</sup>|8,192|
|medium-replay|5|1|5_×_10<sup>_−_4</sup><br>|8,192|
|full-replay|5|1|5_×_10<sup>_−_4</sup>|4,096|
||_ho_<br>|_pper_<br>|||
|medium|2|1|5_×_10<sup>_−_5</sup>|8,192|
|expert|1|1|5_×_10<sup>_−_8</sup>|8,192|
|medium-expert|2|1|1_×_10<sup>_−_6</sup>|8,192|
|medium-replay|5|1|1_×_10<sup>_−_4</sup>|4,096|
|full-replay|5|1|1_×_10<sup>_−_4</sup>|4,096|
||_wal_<br>|_ker2_<br>|_d_<br>||
|medium|5|1|5_×_10<sup>_−_5</sup>|4,096|
|expert|5|1|5_×_10<sup>_−_5</sup>|8,192|
|medium-expert|10|1|5_×_10<sup>_−_5</sup>|8,192|
|medium-replay|5|1|5_×_10<sup>_−_5</sup>|8,192|
|full-replay|5|1|5_×_10<sup>_−_5</sup>|8,192|


Several consistent patterns emerge across environments and datasets. First, even a short horizon of _H_ = 1 or _H_ = 2 is sometimes sufficient to recover the gains from inference-time adaptation, suggesting that the immediate one-step gradient signal through the world model provides useful policy improvement. This is particularly visible in the Walker2d family of tasks, where normalized scores improve monotonically or near-monotonically with _H_ (e.g., walker2d-expert improves from 112 _._ 94 at _H_ = 1 to 113 _._ 74 at _H_ = 20, and walker2d-medium-expert from 111 _._ 71 to 112 _._ 77). 

Second, moderate horizons ( _H_ = 5 or _H_ = 10) tend to perform well across most datasets without incurring instability. Longer horizons ( _H_ = 20) occasionally exhibit higher variance or slight degradation, likely due to compounding model errors over longer imagined rollouts. This is most apparent in the hopper-expert task, where the standard deviation grows substantially at _H_ = 20 (94 _._ 03 _±_ 18 _._ 46) compared to shorter horizons. 

Third, on tasks where the pre-trained ReBRAC policy is already near-optimal or the dataset is uninformative (e.g., random datasets such as halfcheetah-random, hopper-random, walker2d-random), inference-time adaptation provides little to no gain across all horizons, consistent with our main results where we observed no improvement on these tasks. 

Fourth, on full-replay and medium-replay datasets, where the offline data covers a wider range of behaviors, the gains from increasing _H_ tend to be more stable, as the world model trained on richer data yields more reliable multi-step predictions. 

28 

Overall, the ablation confirms that inference-time adaptation is robust across a broad range of horizon choices, with _H ∈{_ 5 _,_ 10 _}_ offering a good balance between performance and computational cost. Since each additional horizon step requires an extra forward pass through the diffusion sampler and reward model, as well as additional backpropagation through the computation graph, practitioners operating under strict latency constraints may prefer smaller _H_ with minimal loss. 

|Dataset|_H_ = 1|_H_ = 2|_H_ = 5|_H_ = 10|_H_ = 20|
|---|---|---|---|---|---|
|random|33_._66_±_0_._19|33_._60_±_0_._32|33_._76_±_0_._19|**34**_._**39**_±_0_._23|34_._23_±_0_._34|
|medium|68_._27_±_0_._58|65_._52_±_8_._85|**68**_._**97**_±_0_._68|68_._88_±_0_._66|68_._77_±_0_._73|
|medium-replay|51_._13_±_0_._85|51_._03_±_0_._56|**51**_._**68**_±_0_._66|51_._43_±_0_._94|51_._48_±_0_._67|
|medium-expert|**106**_._**68**_±_0_._84|106_._13_±_1_._31|102_._36_±_10_._22|105_._79_±_0_._62|106_._05_±_0_._43|
|expert|105_._54_±_0_._53|104_._87_±_1_._84|106_._06_±_0_._36|105_._80_±_0_._46|**106**_._**67**_±_0_._36|
|full-replay|83_._78_±_0_._36|84_._40_±_0_._30|**85**_._**15**_±_0_._41|84_._27_±_0_._49|82_._51_±_0_._48|


Table 9: Effect of planning horizon _H_ on `DiffMPC` for HalfCheetah datasets. Normalized scores (mean _±_ std) on D4RL. Best score per row is in bold. 

|Dataset|_H_ = 1|_H_ = 2|_H_ = 5|_H_ = 10|_H_ = 20|
|---|---|---|---|---|---|
|random|9_._01_±_1_._14|8_._87_±_1_._27|8_._99_±_1_._12|9_._04_±_1_._22|**9**_._**48**_±_1_._22|
|medium-replay|101_._68_±_0_._44|101_._83_±_0_._31|101_._68_±_0_._41|93_._44_±_24_._63|**101**_._**96**_±_0_._42|
|medium-expert|112_._47_±_1_._25|106_._48_±_13_._37|112_._99_±_1_._07|**113**_._**54**_±_1_._14|109_._38_±_12_._93|
|full-replay|108_._01_±_0_._09|108_._02_±_0_._13|108_._06_±_0_._12|108_._38_±_0_._10|**108**_._**61**_±_0_._09|
|expert|107_._70_±_13_._12|**110**_._**36**_±_9_._51|101_._86_±_17_._29|98_._34_±_19_._36|94_._03_±_18_._46|


Table 10: Effect of planning horizon _H_ on `DiffMPC` for Hopper datasets. Normalized scores (mean _±_ std) on D4RL. Best score per row is in bold. 

|Dataset|_H_ = 1|_H_ = 2|_H_ = 5|_H_ = 10|_H_ = 20|
|---|---|---|---|---|---|
|random|**21**_._**96**_±_0_._01|**21**_._**96**_±_0_._02|**21**_._**96**_±_0_._01|**21**_._**96**_±_0_._02|**21**_._**96**_±_0_._02|
|medium|85_._75_±_0_._60|81_._83_±_12_._87|83_._01_±_10_._20|**86**_._**52**_±_0_._45|84_._98_±_5_._96|
|medium-replay|76_._46_±_22_._93|86_._36_±_7_._68|76_._35_±_25_._69|**87**_._**99**_±_3_._86|78_._86_±_18_._54|
|medium-expert|111_._71_±_0_._11|111_._76_±_0_._09|112_._04_±_0_._07|112_._30_±_0_._08|**112**_._**77**_±_0_._06|
|full-replay|104_._00_±_0_._34|104_._54_±_0_._76|104_._50_±_0_._65|**104**_._**74**_±_0_._54|104_._20_±_0_._29|
|expert|112_._94_±_0_._05|112_._93_±_0_._08|113_._15_±_0_._04|113_._41_±_0_._07|**113**_._**74**_±_0_._08|


Table 11: Effect of planning horizon _H_ on `DiffMPC` for Walker2d datasets. Normalized scores (mean _±_ std) on D4RL. Best score per row is in bold. 

### **D.2 Effect of Inner Gradient Steps** 

We next study the effect of the number of inner gradient steps _E_ taken on _J_<sup>�</sup> _t_ ( _ψ_ ) at each real environment state, before executing the next action. Larger _E_ allows more aggressive policy adaptation per step, but also 

29 

increases the computational cost linearly and risks overfitting the policy to the imagined trajectories of a single state _st_ . We sweep _E ∈{_ 1 _,_ 2 _,_ 3 _,_ 4 _,_ 5 _}_ . Results are reported in Tables 12–14. 

The ablation reveals a clear environment-dependent pattern. On the Walker2d tasks, normalized scores improve monotonically with _E_ in nearly every dataset (e.g., walker2d-expert from 112 _._ 99 at _E_ = 1 to 114 _._ 59 at _E_ = 5, walker2d-medium-expert from 111 _._ 76 to 113 _._ 02, walker2d-medium from 82 _._ 27 to 87 _._ 56). This indicates that the policy benefits from repeated gradient refinement on the same imagined rollout objective, and that the world model is sufficiently accurate on Walker2d that additional inner steps do not introduce harmful drift. A similar but milder trend appears on the HalfCheetah full-replay and expert datasets. 

In contrast, the Hopper environment exhibits markedly different behavior. On hopper-medium-replay, performance degrades sharply and monotonically as _E_ increases, falling from 101 _._ 92 at _E_ = 1 to 52 _._ 78 at _E_ = 5, with standard deviations growing to nearly 40. A similar instability appears on hopper-expert, where scores are highest at _E_ = 1 and become noisier at larger _E_ . We attribute this to the interaction between repeated policy optimization and Hopper’s termination-sensitive locomotion dynamics: Hopper episodes terminate when the agent becomes unhealthy, i.e., when the hopper falls or topples over. Thus, small policy-induced trajectory deviations can produce large return changes. More broadly, repeated optimization against imperfect offline model/value estimates can amplify estimation error and move the policy toward out-of-distribution actions, which is a central failure mode in offline RL [Kumar et al., 2020, Brandfonbrener et al., 2021]. 

On HalfCheetah-random, increasing _E_ also leads to a steady decline in performance (33 _._ 58 _→_ 29 _._ 75), which is consistent with the observation from the _H_ ablation that random datasets do not benefit from inference-time adaptation: in the absence of useful policy improvement signal, additional gradient steps simply move the policy away from a reasonable initialization. 

Overall, _E_ = 1 is a safe default that captures most of the benefit at minimal cost on every environment, while _E ∈{_ 3 _,_ 4 _,_ 5 _}_ can yield additional gains on stable environments such as Walker2d and on some HalfCheetah datasets. These results suggest that the optimal _E_ is environment-specific and should be tuned with awareness of the underlying dynamics’ sensitivity to policy perturbations. 

|Dataset|_E_ = 1|_E_ = 2|_E_ = 3|_E_ = 4|_E_ = 5|
|---|---|---|---|---|---|
|random|**33**_._**58**_±_0_._16|32_._44_±_0_._23|31_._14_±_0_._17|30_._33_±_0_._17|29_._75_±_0_._21|
|medium|**68**_._**89**_±_0_._90|68_._74_±_0_._61|68_._51_±_0_._61|68_._34_±_0_._64|67_._98_±_0_._87|
|medium-replay|51_._20_±_0_._57|52_._22_±_0_._76|52_._14_±_0_._73|49_._99_±_5_._87|**52**_._**87**_±_0_._61|
|medium-expert|106_._43_±_0_._49|**106**_._**79**_±_0_._81|106_._40_±_0_._72|106_._40_±_0_._35|106_._57_±_0_._35|
|expert|105_._38_±_0_._67|105_._41_±_0_._87|105_._63_±_0_._86|**106**_._**00**_±_0_._41|105_._65_±_0_._54|
|full-replay|84_._28_±_0_._53|85_._23_±_0_._29|85_._80_±_0_._64|85_._91_±_0_._47|**86**_._**00**_±_0_._27|


Table 12: Effect of inner gradient steps _E_ on `DiffMPC` for HalfCheetah datasets. Normalized scores (mean _±_ std) on D4RL. Best score per row is in bold. 

### **D.3 Effect of Inner Step Size** 

We next study the effect of the inner-loop step size _η_ used in the gradient updates _ψ ← ψ_ + _η∇ψJ_<sup>�</sup> _t_ ( _ψ_ ). A larger _η_ allows the policy to move further per inner step at inference time, which can accelerate adaptation 

30 

|Dataset|_E_ = 1|_E_ = 2|_E_ = 3|_E_ = 4|_E_ = 5|
|---|---|---|---|---|---|
|random|8_._69_±_1_._04|8_._85_±_1_._22|9_._28_±_1_._25|8_._69_±_1_._11|**9**_._**72**_±_1_._23|
|medium-replay|**101**_._**92**_±_0_._28|93_._32_±_24_._50|77_._18_±_37_._39|62_._08_±_39_._72|52_._78_±_40_._01|
|medium-expert|110_._52_±_3_._70|113_._20_±_1_._24|106_._48_±_20_._95|107_._89_±_16_._97|**113**_._**38**_±_0_._88|
|full-replay|108_._10_±_0_._12|108_._09_±_0_._11|108_._24_±_0_._09|108_._25_±_0_._14|**108**_._**35**_±_0_._10|
|expert|**109**_._**74**_±_6_._38|95_._33_±_17_._45|99_._35_±_19_._71|106_._80_±_13_._17|98_._08_±_18_._41|


Table 13: Effect of inner gradient steps _E_ on `DiffMPC` for Hopper datasets. Normalized scores (mean _±_ std) on D4RL. Best score per row is in bold. 

|Dataset|_E_ = 1|_E_ = 2|_E_ = 3|_E_ = 4|_E_ = 5|
|---|---|---|---|---|---|
|random|**21**_._**97**_±_0_._01|21_._96_±_0_._01|21_._96_±_0_._02|21_._96_±_0_._01|21_._96_±_0_._02|
|medium|82_._27_±_13_._94|86_._05_±_0_._32|86_._93_±_0_._35|87_._35_±_0_._31|**87**_._**56**_±_0_._33|
|medium-replay|**89**_._**27**_±_1_._74|80_._26_±_25_._37|85_._85_±_11_._75|66_._77_±_37_._12|81_._34_±_26_._05|
|medium-expert|111_._76_±_0_._07|112_._21_±_0_._06|112_._57_±_0_._07|112_._81_±_0_._07|**113**_._**02**_±_0_._07|
|full-replay|104_._18_±_0_._88|104_._41_±_0_._19|104_._79_±_0_._36|**105**_._**24**_±_0_._50|**105**_._**24**_±_0_._54|
|expert|112_._99_±_0_._11|113_._50_±_0_._08|113_._85_±_0_._09|114_._19_±_0_._12|**114**_._**59**_±_0_._16|


Table 14: Effect of inner gradient steps _E_ on `DiffMPC` for Walker2d datasets. Normalized scores (mean _±_ std) on D4RL. Best score per row is in bold. 

but also risks overshooting and pushing the policy into regions where the world model becomes unreliable. We sweep _η ∈{_ 5 _×_ 10<sup>_−_7</sup> _,_ 5 _×_ 10<sup>_−_6</sup> _,_ 5 _×_ 10<sup>_−_5</sup> _}_ . Results are reported in Tables 15–17. 

The ablation reveals a strong environment-dependent pattern that mirrors what we observed for the inner gradient steps _E_ . On the Walker2d tasks, performance improves nearly monotonically with larger _η_ across every non-random dataset (e.g., walker2d-expert from 112 _._ 49 at _η_ = 5 _×_ 10<sup>_−_7</sup> to 115 _._ 40 at _η_ = 5 _×_ 10<sup>_−_5</sup> , walker2d-medium-replay from 59 _._ 48 to 79 _._ 00, walker2d-medium-expert from 111 _._ 42 to 113 _._ 17). This indicates that the Walker2d world model is sufficiently accurate that larger gradient steps translate directly into better policies without inducing harmful drift. 

On HalfCheetah, the picture is more mixed. Datasets with broad coverage (full-replay, medium-replay) benefit from the largest step size, while expert and random datasets degrade as _η_ grows. The most extreme case is halfcheetah-random, where the score drops from 34 _._ 31 at _η_ = 5 _×_ 10<sup>_−_7</sup> to 27 _._ 60 at _η_ = 5 _×_ 10<sup>_−_5</sup> . Halfcheetah-expert exhibits a similar monotonic decrease (106 _._ 70 _→_ 103 _._ 54), with the largest _η_ also introducing substantial variance. 

The Hopper environment again shows the most pronounced instability under aggressive adaptation. On hopper-medium-replay, the largest step size collapses performance from 101 _._ 75 at _η_ = 5 _×_ 10<sup>_−_6</sup> to 61 _._ 12 at _η_ = 5 _×_ 10<sup>_−_5</sup> , with the standard deviation jumping above 40. This parallels the failure mode observed in the _E_ ablation on the same dataset, and reinforces the interpretation that Hopper’s narrow stable manifold makes it unusually sensitive to large policy perturbations. 

Overall, the optimal _η_ is environment-specific: _η_ = 5 _×_ 10<sup>_−_5</sup> is preferable on Walker2d and on HalfCheetah 

31 

datasets with broad coverage, while smaller step sizes around _η_ = 5 _×_ 10<sup>_−_7</sup> to 5 _×_ 10<sup>_−_6</sup> are safer on Hopper and on near-optimal policies. A practical default of _η_ = 5 _×_ 10<sup>_−_6</sup> provides a reasonable trade-off, performing close to the best on most datasets while avoiding the catastrophic instability seen at the largest step size on Hopper. 

|Dataset|_η_ = 5_×_10<sup>_−_7</sup>|_η_ = 5_×_10<sup>_−_6</sup>|_η_ = 5_×_10<sup>_−_5</sup>|
|---|---|---|---|
|random|**34**_._**31**_±_0_._09|33_._60_±_0_._19|27_._60_±_0_._16|
|medium|68_._65_±_1_._03|**69**_._**03**_±_0_._81|66_._55_±_0_._60|
|medium-replay|50_._96_±_0_._74|51_._38_±_0_._85|**52**_._**53**_±_0_._62|
|medium-expert|106_._05_±_0_._25|105_._81_±_2_._41|**106**_._**23**_±_0_._26|
|expert|**106**_._**70**_±_0_._34|105_._66_±_0_._41|103_._54_±_8_._21|
|full-replay|82_._46_±_0_._47|84_._31_±_0_._39|**86**_._**04**_±_0_._34|


Table 15: Effect of inner step size _η_ on `DiffMPC` for HalfCheetah datasets. Normalized scores (mean _±_ std) on D4RL. Best score per row is in bold. 

|Dataset|_η_ = 5_×_10<sup>_−_7</sup>|_η_ = 5_×_10<sup>_−_6</sup>|_η_ = 5_×_10<sup>_−_5</sup>|
|---|---|---|---|
|random|**9**_._**00**_±_1_._24|8_._45_±_0_._73|8_._40_±_0_._69|
|medium-replay|100_._35_±_3_._65|**101**_._**75**_±_0_._52|61_._12_±_41_._11|
|medium-expert|**112**_._**54**_±_1_._08|112_._14_±_0_._90|112_._35_±_0_._46|
|full-replay|108_._13_±_0_._13|107_._98_±_0_._10|**108**_._**46**_±_0_._08|
|expert|99_._50_±_20_._18|98_._88_±_18_._66|**100**_._**53**_±_18_._66|


Table 16: Effect of inner step size _η_ on `DiffMPC` for Hopper datasets. Normalized scores (mean _±_ std) on D4RL. Best score per row is in bold. 

|Dataset|_η_ = 5_×_10<sup>_−_7</sup>|_η_ = 5_×_10<sup>_−_6</sup>|_η_ = 5_×_10<sup>_−_5</sup>|
|---|---|---|---|
|random|**21**_._**96**_±_0_._02|**21**_._**96**_±_0_._01|**21**_._**96**_±_0_._01|
|medium|77_._06_±_17_._66|86_._01_±_0_._46|**87**_._**99**_±_0_._95|
|medium-replay|59_._48_±_32_._73|71_._06_±_29_._41|**79**_._**00**_±_27_._66|
|medium-expert|111_._42_±_0_._12|111_._74_±_0_._08|**113**_._**17**_±_0_._12|
|full-replay|103_._97_±_0_._51|104_._60_±_1_._39|**105**_._**94**_±_0_._71|
|expert|112_._49_±_0_._06|112_._97_±_0_._08|**115**_._**40**_±_0_._13|


Table 17: Effect of inner step size _η_ on `DiffMPC` for Walker2d datasets. Normalized scores (mean _±_ std) on D4RL. Best score per row is in bold. 

### **D.4 Effect of DDIM Sampling Steps** 

We next study the effect of the number of DDIM sampling steps _K_ used when unrolling the diffusion world model _fθ_ at inference time. Recall from Section 3 that each call to _fθ_ requires _K_ sequential reverse-diffusion steps to produce a single next-state sample. Larger _K_ produces samples that more faithfully match the trained conditional distribution _pθ_ ( _st_ +1 _| st, at_ ), but linearly increases both the cost of each forward rollout and the depth of the computation graph through which gradients are backpropagated. We sweep _K ∈{_ 1 _,_ 2 _,_ 5 _,_ 10 _,_ 20 _}_ 

32 

across all 18 Gym-MuJoCo datasets, with the remaining hyperparameters fixed at their best per-dataset values from the previous ablations. Results are reported in Tables 18–20. 

The picture that emerges from these tables depends on the dataset. On HalfCheetah, the choice of _K_ has a small effect on most datasets: halfcheetah-medium ranges between 68 _._ 67 and 69 _._ 12, and halfcheetahmedium-replay between 51 _._ 19 and 51 _._ 56, with differences on the order of one standard deviation. The Walker2d expert and medium-expert tasks behave similarly, varying by only a few tenths of a point across the full range of _K_ . On these datasets, a small number of denoising steps appears to be enough for inference-time optimization, although larger _K_ can still help at the margin. 

Other datasets benefit from larger _K_ . Halfcheetah-full-replay improves from 82 _._ 90 at _K_ = 1 to 84 _._ 46 at _K_ = 20, and hopper-full-replay and walker2d-full-replay show the same trend. We attribute this to the fact that broader-coverage datasets train more expressive diffusion models whose multi-step denoising procedure captures finer-grained dynamics that a one-step sample may miss. 

Walker2d-medium and walker2d-medium-replay go the other way and degrade with larger _K_ . On walker2dmedium, scores fall from 86 _._ 09 at _K_ = 1 to 81 _._ 04 at _K_ = 20, with growing variance. We hypothesize that the deeper diffusion computation graph at large _K_ produces noisier or less stable gradient signals during the policy update, partially offsetting the benefits of more accurate samples. 

Hopper shows the largest swings across _K_ , particularly on hopper-medium-expert and hopper-expert, where individual _K_ values can shift by several points with large standard deviations. This matches our earlier observations that Hopper is unusually sensitive to perturbations in the inference-time pipeline, and it suggests that _K_ needs to be tuned more carefully here than elsewhere. 

Overall, _K ∈{_ 1 _,_ 2 _}_ is competitive on many datasets at much lower cost, while _K_ = 10 tends to work better on the full-replay datasets where extra sampling fidelity helps. This trade-off motivates the one-step MeanFlow sampler in Section 6: where extra denoising steps give diminishing returns, distilling the diffusion process into a single evaluation recovers most of the benefit at a fraction of the cost, and we can fall back to multi-step sampling on the datasets where it actually pays off. 

|Dataset|_K_ = 1|_K_ = 2|_K_ = 5|_K_ = 10|_K_ = 20|
|---|---|---|---|---|---|
|random|**34**_._**02**_±_0_._20|33_._92_±_0_._17|33_._57_±_0_._22|33_._60_±_0_._20|33_._57_±_0_._08|
|medium|68_._74_±_0_._56|68_._67_±_0_._81|68_._76_±_0_._49|**69**_._**12**_±_0_._66|68_._70_±_0_._56|
|medium-replay|51_._41_±_0_._40|51_._19_±_0_._84|**51**_._**56**_±_0_._44|**51**_._**56**_±_0_._97|51_._21_±_0_._96|
|medium-expert|105_._61_±_0_._18|105_._75_±_0_._33|106_._03_±_0_._84|104_._65_±_5_._25|**106**_._**53**_±_0_._58|
|expert|104_._49_±_0_._19|104_._58_±_0_._37|**105**_._**53**_±_0_._62|105_._19_±_0_._70|104_._67_±_2_._24|
|full-replay|82_._90_±_0_._42|82_._87_±_0_._47|84_._31_±_0_._34|84_._35_±_0_._38|**84**_._**46**_±_0_._28|


Table 18: Effect of DDIM sampling steps _K_ on `DiffMPC` for HalfCheetah datasets. Normalized scores (mean _±_ std) on D4RL. Best score per row is in bold. 

### **D.5 Effect of Number of Particles** 

We finally study the effect of the number of Monte Carlo particles _M_ used to estimate the MPC objective _J_ � _t_ ( _ψ_ ) at inference time. Recall that _M_ controls the number of i.i.d. noise sequences over which we average the imagined-rollout return; larger _M_ reduces the variance of the gradient estimator. Since the _M_ particles are 

33 

|Dataset|_K_ = 1|_K_ = 2|_K_ = 5|_K_ = 10|_K_ = 20|
|---|---|---|---|---|---|
|random|8_._58_±_1_._09|**9**_._**32**_±_1_._22|8_._60_±_1_._03|9_._21_±_1_._26|8_._37_±_0_._82|
|medium-replay|101_._75_±_0_._45|85_._73_±_33_._10|101_._48_±_0_._51|101_._85_±_0_._31|**102**_._**05**_±_0_._45|
|medium-expert|113_._22_±_2_._39|108_._44_±_14_._94|111_._06_±_4_._33|108_._92_±_14_._62|**113**_._**66**_±_0_._91|
|full-replay|107_._92_±_0_._17|107_._87_±_0_._20|108_._04_±_0_._17|108_._00_±_0_._09|**108**_._**09**_±_0_._12|
|expert|**111**_._**19**_±_5_._36|99_._62_±_21_._08|106_._35_±_12_._65|105_._80_±_11_._82|100_._79_±_12_._62|


Table 19: Effect of DDIM sampling steps _K_ on `DiffMPC` for Hopper datasets. Normalized scores (mean _±_ std) on D4RL. Best score per row is in bold. 

|Dataset|_K_ = 1|_K_ = 2|_K_ = 5|_K_ = 10|_K_ = 20|
|---|---|---|---|---|---|
|random|21_._96_±_0_._01|21_._96_±_0_._01|21_._96_±_0_._02|**21**_._**97**_±_0_._01|21_._96_±_0_._02|
|medium|**86**_._**09**_±_1_._13|85_._52_±_0_._99|85_._24_±_5_._28|81_._95_±_12_._75|81_._04_±_15_._06|
|medium-replay|71_._60_±_32_._72|84_._44_±_5_._33|**89**_._**03**_±_2_._19|78_._78_±_22_._03|73_._33_±_19_._42|
|medium-expert|111_._71_±_0_._07|111_._75_±_0_._07|111_._74_±_0_._06|**111**_._**77**_±_0_._11|111_._72_±_0_._10|
|full-replay|103_._57_±_0_._35|103_._60_±_0_._32|104_._24_±_0_._76|104_._10_±_0_._57|**104**_._**40**_±_0_._87|
|expert|112_._71_±_0_._07|112_._71_±_0_._08|112_._95_±_0_._05|112_._97_±_0_._07|**112**_._**98**_±_0_._11|


Table 20: Effect of DDIM sampling steps _K_ on `DiffMPC` for Walker2d datasets. Normalized scores (mean _±_ std) on D4RL. Best score per row is in bold. 

independent and processed in parallel, the wall-clock cost of increasing _M_ is largely absorbed by hardware parallelism, and the practically relevant question is not whether larger _M_ is faster but whether `DiffMPC` is robust across reasonable choices. We sweep _M ∈{_ 512 _,_ 1024 _,_ 4096 _}_ across all 18 Gym-MuJoCo datasets, with the remaining hyperparameters fixed at their best per-dataset values from the previous ablations. Results are reported in Tables 21–23. 

The ablation confirms that `DiffMPC` is stable across this range of _M_ . On nearly every dataset, the difference between the smallest and largest _M_ is well within the noise of a single run: HalfCheetah scores vary by less than one point across the entire range on every dataset, and the Walker2d expert and medium-expert tasks differ by less than 0 _._ 5 points across all three _M_ values. This indicates that the gradient estimator is well-behaved at _M_ = 512 and that further variance reduction provides only marginal change to the resulting policy. 

The takeaway is that _M_ is not a parameter that requires careful tuning within this range. Any choice in _{_ 512 _,_ 1024 _,_ 4096 _}_ produces qualitatively similar performance, and practitioners can default to whatever value fits comfortably within their available parallel compute budget without expecting significant changes to the final policy. 

### **D.6 Pre-trained policy: SAC-RND** 

We also evaluate `DiffMPC` using SAC-RND as the pre-trained policy. SAC-RND combines soft actor-critic with a random-network-distillation exploration bonus, where the prediction error of a learned network against a fixed random target network provides an intrinsic reward during policy training. We follow the 

34 

|Dataset|_M_ = 512|_M_ = 1024|_M_ = 4096|
|---|---|---|---|
|random|**34**_._**27**_±_0_._16|34_._22_±_0_._31|33_._61_±_0_._14|
|medium|**68**_._**89**_±_0_._64|68_._72_±_0_._56|68_._50_±_0_._75|
|medium-replay|51_._21_±_0_._63|51_._19_±_0_._63|**51**_._**69**_±_0_._69|
|medium-expert|106_._05_±_0_._23|106_._11_±_0_._29|**106**_._**88**_±_0_._24|
|expert|**106**_._**45**_±_0_._28|106_._09_±_0_._23|105_._77_±_0_._39|
|full-replay|82_._65_±_0_._50|82_._88_±_0_._52|**84**_._**32**_±_0_._30|


Table 21: Effect of number of particles _M_ on `DiffMPC` for HalfCheetah datasets. Normalized scores (mean _±_ std) on D4RL. Best score per row is in bold. 

|Dataset|_M_ = 512|_M_ = 1024|_M_ = 4096|
|---|---|---|---|
|random|8_._61_±_0_._83|8_._75_±_1_._03|**8**_._**77**_±_0_._94|
|medium-replay|**100**_._**22**_±_4_._75|99_._14_±_10_._27|99_._90_±_4_._98|
|medium-expert|110_._15_±_7_._17|**112**_._**75**_±_1_._02|112_._74_±_1_._28|
|full-replay|**108**_._**11**_±_0_._14|108_._05_±_0_._16|108_._04_±_0_._14|
|expert|100_._47_±_16_._44|**102**_._**28**_±_15_._09|101_._30_±_17_._34|


Table 22: Effect of number of particles _M_ on `DiffMPC` for Hopper datasets. Normalized scores (mean _±_ std) on D4RL. Best score per row is in bold. 

|Dataset|_M_ = 512|_M_ = 1024|_M_ = 4096|
|---|---|---|---|
|random|**21**_._**97**_±_0_._01|21_._96_±_0_._02|21_._96_±_0_._02|
|medium|85_._70_±_0_._44|83_._67_±_5_._29|**86**_._**19**_±_0_._68|
|medium-replay|77_._21_±_14_._71|74_._87_±_24_._18|**79**_._**78**_±_17_._78|
|medium-expert|111_._45_±_0_._09|111_._46_±_0_._09|**111**_._**75**_±_0_._07|
|full-replay|**103**_._**81**_±_0_._80|103_._58_±_0_._52|103_._74_±_0_._61|
|expert|112_._61_±_0_._10|112_._68_±_0_._07|**113**_._**03**_±_0_._10|


Table 23: Effect of number of particles _M_ on `DiffMPC` for Walker2d datasets. Normalized scores (mean _±_ std) on D4RL. Best score per row is in bold. 

35 

hyperparameter choices from the original SAC-RND paper and apply our inference-time optimization starting from the resulting pre-trained SAC-RND policy. Table 24 reports the normalized D4RL score of SAC-RND and `DiffMPC` , averaged over 10 evaluation episodes. 

|Dataset<br>|SAC-RND (zero-shot<br>halfcheetah<br>|)<br>`DiffMPC`<br>|
|---|---|---|
|medium|62_._90_±_0_._31|69_._40_±_0_._48|
|medium-replay|47_._78_±_1_._16|65_._95_±_0_._86|
|medium-expert|105_._99_±_0_._17|107_._46_±_0_._16|
|full-replay|82_._03_±_0_._42|81_._29_±_0_._23|
|expert|46_._96_±_48_._83|64_._49_±_50_._78|
||hopper||
|medium|99_._70_±_0_._28|100_._83_±_0_._26|
|medium-replay|100_._51_±_1_._16|102_._21_±_0_._17|
|medium-expert|110_._53_±_0_._17|110_._55_±_0_._26|
|full-replay|77_._41_±_17_._96|103_._32_±_14_._29|
|expert|110_._64_±_0_._31|110_._74_±_0_._34|
||walker2d||
|medium|91_._35_±_2_._32|92_._74_±_0_._83|
|medium-replay|84_._05_±_2_._03|89_._85_±_1_._66|
|medium-expert|94_._85_±_12_._08|108_._56_±_0_._12|
|full-replay|104_._77_±_0_._10|105_._50_±_0_._13|
|expert|41_._50_±_17_._07|82_._03_±_31_._84|
|Average|84_._08|**93.00**|


## Table 24: Average normalized score over the final evaluation on ten episodes on Gym-MuJoCo tasks. The symbol _±_ represents the standard deviation across episodes. **E Additional Comparison with MPC approaches** 

### **E.1 Latent-space world models for continuous control** 

The use of learned dynamics for policy improvement has a long history. PILCO [Deisenroth and Rasmussen, 2011] fit Gaussian-process dynamics and computed analytic policy gradients via belief-state propagation. Stochastic Value Gradients [Heess et al., 2015] extended this to neural dynamics by reparameterizing stochastic transitions and backpropagating through finite-horizon rollouts. PlaNet [Hafner et al., 2019] introduced a recurrent state-space model and performed cross-entropy planning in the latent space. Two design axes emerge from this literature: _what kind of latent dynamics to learn_ , and _how to use it to act_ . Two families have come to dominate continuous control along these axes. 

**Dreamer family.** Dreamer [Hafner et al., 2020] couples a recurrent latent dynamics model with an actor and critic trained on imagined latent rollouts; the actor is updated by backpropagating return gradients through the unrolled dynamics. DreamerV2 [Hafner et al., 2021] introduced categorical latents, and DreamerV3 [Hafner 

36 

et al., 2025] demonstrated robust performance across DMControl, Atari, Crafter, and Minecraft under fixed hyperparameters. The defining feature is _training-time use of the model_ : the deployed actor is feedforward and the model is not consulted at inference. 

**TD-MPC family.** TD-MPC [Hansen et al., 2022] takes the opposite stance. It learns a Task-Oriented Latent Dynamics model jointly with reward, value, and a policy prior via TD learning, then performs gradient-free MPPI in the latent space at inference, with the learned policy as a warm-start. The terminal value bootstraps beyond the planning horizon. TD-MPC2 [Hansen et al., 2024] scales this to 104 continuous-control tasks across DMControl, Meta-World, ManiSkill2, and MyoSuite under a single hyperparameter setting. The defining feature is _inference-time planning_ : the model is consulted on every step, with substantial per-step compute (TD-MPC2’s MPPI predicts _∼_ 9 _,_ 200 latent states per action) traded for state-conditioned decision making. 

**Contrast with our work.** Our setting differs along three axes, summarized in Table 25. First, _inferencetime parameter refinement_ : Dreamer optimizes actor parameters at training time and deploys a static actor; TD-MPC optimizes action sequences at inference time but leaves the underlying policy unchanged. We optimize _policy parameters_ at inference time via gradient steps through the rollout, so the deployed policy itself adapts in response to the observed state. Second, _offline regime_ : both Dreamer and TD-MPC train via environment interaction with jointly learned dynamics, value, and policy components; we operate purely on a fixed offline dataset with a pretrained policy and critic. Third, _generative state-space dynamics_ : Dreamer’s RSSM and TD-MPC’s TOLD are deterministic predictors in compact latent spaces, trained jointly with reward and value; our transition model is a conditional generative model in explicit state space (diffusion, with a one-step MeanFlow variant in Section 6), trained in isolation by maximum-likelihood objectives. The Dreamer-vs-TD-MPC progression is itself evidence that inference-time use of a world model can outperform training-time-only use at the cost of additional deployment compute. We extend this design philosophy to offline RL and replace gradient-free MPPI over action sequences with gradient-based refinement of policy parameters. 

||**Dreamer family**|**TD-MPC family**|**Ours**|
|---|---|---|---|
|When is the model used?|Training|Inference|Inference|
|What is optimized?|Actor parameters|Action sequences|Policy parameters|
|How is it optimized?|Gradient (BPTT)|Gradient-free (MPPI)|Gradient (BPTT)|
|Setting|Online|Online|Offline|
|Dynamics|Latent (RSSM)|Latent (TOLD)|Explicit (generative)|
|Deployment cost|Single forward pass|MPPI search|Inner-loop gradient updates|


Table 25: Design-space comparison between the Dreamer family, the TD-MPC family, and our approach. 

TD-MPC2 outperforms DreamerV3 on average across the 104-task suite, with the largest gains on hard high-dimensional locomotion and manipulation tasks. As TD-MPC2 represents the stronger of the two families and the closest analogue to our inference-time-planning approach, we use it as the representative latent-world-model baseline in our empirical comparison. 

**Empirical comparison with TD-MPC2.** We train TD-MPC2 [Hansen et al., 2024] on each D4RL GymMuJoCo dataset using the official implementation, with the offline transitions supplied as the replay buffer. 

37 

We additionally train an offline-adapted variant of TD-MPC2 in which there is an added behavior-cloning (BC) loss on the policy: besides the usual TD-MPC2 objective, the actor is explicitly trained to match the dataset actions. This extra term pulls updates toward behavior-supported actions, reducing out-of-distribution policy drift during offline training and typically making learning more stable on fixed datasets. Table 26 reports both final and best normalized scores for the two variants. Neither variant approaches the performance of standard offline RL baselines (Section 5): TD-MPC2 is designed for the online sample-efficient regime in which the replay buffer is grown by ongoing environment interaction, and removing this interaction, whether by simply repurposing the online recipe or by an offline adaptation, substantially degrades performance. 

||**TD-M**|**PC2**|**TD-MPC2 (offli**|**lne with BC loss)**|
|---|---|---|---|---|
|**Dataset**|**Final**|**Best**|**Final**|**Best**|
|halfcheetah-random|4_._13_±_1_._17|17_._71_±_0_._51|12_._75_±_1_._93|16_._04_±_0_._77|
|halfcheetah-medium|0_._72_±_1_._56|2_._60_±_0_._17|2_._88_±_0_._63|3_._34_±_0_._74|
|halfcheetah-medium-replay|7_._01_±_0_._64|10_._79_±_0_._94|6_._41_±_0_._15|13_._96_±_0_._31|
|halfcheetah-medium-expert|1_._67_±_0_._74|2_._78_±_0_._38|1_._35_±_0_._81|3_._32_±_0_._72|
|halfcheetah-expert|_−_1_._71_±_0_._53|_−_0_._40_±_0_._96|_−_1_._79_±_0_._75|0_._32_±_0_._22|
|halfcheetah-full-replay|4_._56_±_0_._58|7_._68_±_1_._00|6_._25_±_0_._51|10_._57_±_0_._11|
|hopper-random|3_._66_±_1_._48|8_._21_±_0_._30|1_._35_±_0_._48|7_._86_±_0_._48|
|hopper-medium|1_._32_±_0_._41|1_._86_±_0_._40|1_._51_±_0_._18|1_._97_±_0_._52|
|hopper-medium-replay|1_._80_±_0_._52|3_._81_±_0_._47|2_._71_±_0_._21|5_._17_±_1_._38|
|hopper-medium-expert|0_._78_±_0_._06|1_._32_±_0_._35|0_._84_±_0_._05|2_._35_±_1_._30|
|hopper-expert|0_._72_±_0_._02|1_._43_±_0_._49|0_._73_±_0_._08|1_._73_±_0_._45|
|hopper-full-replay|4_._18_±_2_._35|5_._20_±_1_._15|3_._77_±_1_._99|7_._74_±_1_._02|
|walker2d-random|2_._93_±_1_._96|9_._59_±_4_._01|4_._82_±_0_._77|7_._50_±_1_._37|
|walker2d-medium|0_._55_±_0_._30|8_._02_±_6_._28|0_._28_±_0_._29|6_._35_±_3_._38|
|walker2d-medium-replay|4_._52_±_1_._89|7_._93_±_0_._52|2_._26_±_0_._75|8_._07_±_0_._27|
|walker2d-medium-expert|_−_0_._11_±_0_._09|0_._58_±_0_._23|0_._13_±_0_._26|2_._42_±_0_._51|
|walker2d-expert|_−_0_._14_±_0_._02|0_._03_±_0_._18|_−_0_._17_±_0_._06|_−_0_._09_±_0_._03|
|walker2d-full-replay|4_._02_±_1_._72|13_._40_±_1_._70|5_._20_±_4_._15|20_._09_±_2_._61|


Table 26: TD-MPC2 normalized scores on D4RL Gym-MuJoCo. Mean _±_ standard deviation across three seed. Final score is the score at the end of training; best score is the highest score over the course of training. 

### **E.2 Gradient-based and embedded differentiable MPC** 

A complementary line of work uses gradient-based optimization through differentiable dynamics inside an MPC loop, either by backpropagating through learned rollouts or by embedding a differentiable MPC solver 

38 

as a layer in a policy network. We discuss two representative methods. 

**Gradient-based planning with world models.** V et al. [2023] use gradient descent through a learned differentiable world model as an alternative to gradient-free trajectory optimization (CEM, MPPI) for visual model predictive control. At each environment step, they backpropagate the predicted return from an _H_ -step rollout under the learned dynamics back to the action sequence and update the actions via gradient ascent. The dynamics is a Dreamer-style latent world model. They evaluate in the online, sample-efficient regime on visual control benchmarks and report performance on par with or superior to gradient-free MPC and pure policy-based methods. They also propose a hybrid variant in which a policy network produces an initial action sequence which is then refined by gradient-based MPC. 

**Actor-Critic Model Predictive Control.** Romero et al. [2025] embed a differentiable MPC solver as the final layer of an actor network in an actor-critic RL framework. The MPC layer uses an _analytic_ dynamics model (a quadrotor model) together with a learned cost-map network that maps observations to the MPC’s cost-function parameters. Gradients flow end-to-end through the MPC solver into the cost-map network during training, and at deployment the same MPC solver produces actions on every environment step. The method is evaluated on agile quadrotor racing in simulation and on a real platform, and is shown to improve out-of-distribution behavior, robustness to dynamics perturbations, and sample efficiency relative to standard actor-critic baselines. 

**Comparison with our work.** Our setting differs along three axes, summarized in Table 27. First, _what is optimized_ : V et al. [2023] optimize an open-loop action sequence at each step (or a policy-initialized refinement of one); Romero et al. [2025] optimize the cost-map network parameters end-to-end through a differentiable MPC layer at training time, with the MPC solver itself producing actions at inference; we optimize the _policy parameters ψ_ via gradient steps through the rollout at inference time. Second, _dynamics class_ : V et al. [2023] use a learned deterministic latent model, Romero et al. [2025] use known analytic dynamics, and we use a learned conditional generative model in explicit state space (diffusion in our main results, single-step MeanFlow in Section 6). Third, _problem setting_ : both prior works operate online; we operate purely on a fixed offline dataset with a pretrained policy and critic, and the inference-time update is the only mechanism by which the deployed policy can improve. 

||**Jyothir et al.**|**Romero et al.**|**Ours**|
|---|---|---|---|
|What is optimized?|Action sequences|Cost-map parameters|Policy parameters|
|How is it optimized?|Gradient (BPTT)|Gradient through MPC<br>solver|Gradient (BPTT)|
|When?|Inference|Training and inference|Inference|
|Dynamics|Learned latent|Analytic|Learned generative|
|Setting|Online|Online|Offline|
|Domain|Visual control|Quadrotor flight|D4RL benchmarks|


Table 27: Design-space comparison between gradient-based / embedded differentiable MPC methods and our approach. 

39 

|Dataset<br>|Grad-MPC<br>**halfcheetah**<br>|`DiffMPC`<br>|
|---|---|---|
|medium|68_._26_±_0_._63|**69.14**_±_1_._17|
|expert|107_._81_±_0_._58|**107.82**_±_0_._60|
|medium-expert|102_._41_±_1_._23|**106.28**_±_1_._63|
|medium-replay|51_._32_±_0_._60|**63.45**_±_0_._59|
|full-replay|82_._37_±_0_._28|**85.69**_±_0_._24|
||**hopper**||
|medium|102_._33_±_0_._25|**103.39**_±_0_._08|
|expert|110_._20_±_6_._08|**113.06**_±_2_._03|
|medium-expert|**112.87**_±_1_._62|110_._68_±_17_._30|
|medium-replay|101_._27_±_0_._34|**103.17**_±_0_._15|
|full-replay|107_._13_±_0_._14|**108.26**_±_0_._10|
||**walker2d**||
|medium|86_._63_±_0_._96|**88.99**_±_0_._60|
|expert|112_._54_±_0_._12|**116.53**_±_0_._16|
|medium-expert|112_._20_±_0_._05|**117.32**_±_0_._73|
|medium-replay|78_._72_±_19_._90|**94.49**_±_0_._86|
|full-replay|104_._37_±_0_._93|**106.69**_±_0_._75|
|Average|94_._30|**99.66**|


Table 28: Average normalized score over the final evaluation and ten episodes on Gym-MuJoCo tasks. The symbol _±_ represents the standard deviation across episodes. 

**Empirical comparison.** Among the two prior methods, only V et al. [2023] is directly applicable to our setting: Romero et al. [2025] requires a known analytic dynamics model, which is unavailable on D4RL benchmarks where we only have access to an offline dataset. We therefore compare against an offline adaptation of V et al. [2023], which we refer to as Grad-MPC: at each environment step, we backpropagate the imagined return through our learned diffusion world model to update an open-loop action sequence via gradient ascent, keeping all other components (world model, critic, horizon, number of inner steps) identical to `DiffMPC` . Table 28 reports the resulting normalized scores. `DiffMPC` outperforms Action Update on 14 of 15 datasets and improves the average normalized score from 94 _._ 30 to 99 _._ 66. The gap is most pronounced on datasets with broad coverage and on Walker2d (e.g., walker2d-medium-expert improves from 112 _._ 20 to 117 _._ 32, halfcheetah-medium-replay from 51 _._ 32 to 63 _._ 45). We attribute this gap to the difference in what is being optimized: updating policy parameters _ψ_ amortizes the inference-time gradient signal across states and exploits the inductive bias of the pretrained policy, whereas optimizing a fresh open-loop action sequence at every step discards this structure and is more vulnerable to compounding world-model errors over the planning horizon. 

40 

### **E.3 Diffusion-based MPC** 

A closely related thread uses diffusion models for MPC, but with a fundamentally different role for the generative components. We discuss the most prominent recent example. 

**Diffusion Model Predictive Control.** Zhou et al. [2024] propose D-MPC, an online MPC method built on two diffusion models trained on offline data: a multi-step _action proposal_ that generates candidate action sequences over a horizon _F_ , and a multi-step _dynamics model_ that predicts the corresponding state trajectories. At each environment step, candidate action sequences are sampled from the action proposal, scored by predicted return under the dynamics model, and the best sequence is selected via a sampling-based planner (a variant of random shooting). Only the first action is executed before the procedure repeats. They evaluate on D4RL Gym-MuJoCo and report substantial gains over single-step model-based planning baselines such as MBOP, attributing the improvement to multi-step trajectory-level modeling that mitigates compounding error. 

**Contrast with our work.** D-MPC and our method both use diffusion models inside an MPC loop, but the role of the diffusion model and the optimization mechanism differ along the axes summarized in Table 29. First, _what is optimized_ : D-MPC selects the best _action sequence_ from candidates sampled by a learned diffusion action proposal; we update the _policy parameters ψ_ of a pretrained behavior policy via gradient steps through the rollout. Second, _how it is optimized_ : D-MPC is gradient-free, scoring sampled trajectories under the dynamics model; we backpropagate through the entire rollout to obtain gradients with respect to _ψ_ . Third, _dynamics structure_ : D-MPC’s diffusion model is multi-step and trajectory-level, predicting _F_ future states in a single forward pass; ours is single-step ( _st_ +1 given _st, at_ ), with the rollout assembled by repeated application. Fourth, _generative components_ : D-MPC trains two diffusion models (action proposal and dynamics); we train a single generative dynamics model and rely on a separately trained behavior policy for actions. For ease of reference, we reproduce the empirical comparison against D-MPC on D4RL datasets from Section 5 in Table 30. 

||**Zhou et al.**|**Ours**|
|---|---|---|
|What is optimized?|Action sequence (best<br>candidate)|Policy parameters|
|How is it optimized?|Gradient-free (random shooting)|Gradient (BPTT)|
|Dynamics|Multi-step trajectory diffusion|One-step transition diffusion|
|Action source|Learned diffusion proposal|Pretrained behavior policy|


Table 29: Design-space comparison between D-MPC and our approach. 

## **F FlowMPC: One step Model** 

Inference-time policy optimization can improve performance over purely offline-trained policies, but it brings this issue of deployment speed to the forefront. The inner loop requires many model evaluations per environment step, and diffusion-based transition models are especially costly because each simulated transition requires iterative denoising [Ho et al., 2020]. As a result, iterative sampling becomes a dominant 

41 

|Task Name|D-MPC|`DiffMPC`|
|---|---|---|
|halfcheetah medium|46_._00_±_0_._17|**70.05**_±_1_._8|
|hopper medium|61_._24_±_2_._30|**103.38**_±_0_._35|
|walker2d medium|76_._21_±_2_._67|**88.91**_±_0_._6|
|halfcheetah medium-replay|41_._12_±_0_._31|**59.89**_±_1_._2|
|hopper medium-replay|92_._49_±_2_._23|**103.14**_±_0_._45|
|walker2d medium-replay|78_._81_±_4_._19|**95.87**_±_1_._19|
|Average|65_._98|**86.87**|


Table 30: Average normalized score on ten unseen seeds. _±_ represents the standard deviation across seeds. 

latency bottleneck in real-time control settings. There is a strong need for faster generative dynamics for differentiable planning. 

One way to reduce this deployment cost is to replace iterative diffusion sampling with a _single-step_ generative model. Mean-flow [Geng et al., 2025] dynamics provide such a mechanism: the model maps a state-action pair to the next-state prediction in one forward pass, cutting per-transition latency at inference. This is especially attractive in inference-time MPC loops, where each environment step may require many simulated transitions and wall-clock time scales directly with the number of denoising steps. The main drawback is statistical: single-step models are typically less expressive than multi-step diffusion samplers and can incur higher prediction error on complex, multimodal transition distributions, and under rollout these errors compound. To mitigate this, we bias world-model training toward state-action regions that are likely under a strong pretrained policy, so that capacity is spent where the deployed controller will actually query the model. 

### **F.1 Mean-Flow Models** 

Mean-flow models [Geng et al., 2025] provide a framework for _one-step_ generation by modeling an _average_ velocity field, rather than the _instantaneous_ velocity used in standard Flow Matching [Lipman et al., 2022]. We follow the common continuous-time transport view, where a latent variable _zt ∈_ R<sup>_d_</sup> evolves over _t ∈_ [0 _,_ 1] to map between a data distribution and a simple prior. Let _x ∼ p_ data denote a data sample and _ϵ ∼ p_ prior denote a prior sample (typically _N_ (0 _, I_ )). A simple probability path used in rectified-flow style constructions [Liu et al., 2022] is the linear interpolation 


Along such paths, Flow Matching learns an instantaneous velocity field _v_ ( _zt, t_ ) that defines an ODE 


so that generation can be performed by numerically solving the ODE from _t_ = 1 to _t_ = 0 starting at _z_ 1 = _ϵ_ . 

**Average velocity.** Mean-flow models instead define the _average velocity_ between two time points _r < t_ as [Geng et al., 2025] 


42 

This quantity is aligned with the displacement along the trajectory: _zr_ = _zt −_ ( _t − r_ ) _u_ ( _zt, r, t_ ). 

If a neural network _uθ_ accurately predicts _u_ ( _·, r, t_ ), then sampling can avoid numerical integration. In particular, _one-step_ sampling is obtained by drawing _z_ 1 = _ϵ ∼ p_ prior and setting 


**MeanFlow Identity and Training Objective.** Direct supervision of _u_ ( _zt, r, t_ ) is intractable because it is defined by a time integral. Geng et al. [2025] derive an identity relating average and instantaneous velocities: 


where _dt_<sup>_<u>d</u>_is the total derivative along the trajectory.Expanding the total derivative gives</sup> 


This yields a tractable training target by replacing _v_ ( _zt, t_ ) with the usual conditional velocity used in Flow Matching. For the linear path above, a standard conditional velocity is _v_ cond = _ϵ − x_ [Lipman et al., 2022, Liu et al., 2022]. MeanFlow training fits _uθ_ by regressing to the identity-based target: 


with expectations over _x ∼ p_ data, _ϵ ∼ p_ prior, and a sampling scheme for ( _r, t_ ) with 0 _≤ r < t ≤_ 1. In our world-model setting, _x_ corresponds to the next state (or state increment), and both _uθ_ and the conditional velocity are parameterized _conditionally_ on the current state–action pair. 

### **F.2 One-Step Mean-Flow Dynamics for World Modeling** 

We learn a conditional, differentiable transition sampler for next-state generation. Given ( _st, at_ ), we generate _st_ +1 via a reparameterized map 


so that rollout sampling is a single forward pass and gradients with respect to ( _st, at_ ) are available. 

**MeanFlow sampler.** We instantiate _fθ_ using a one-step MeanFlow model [Geng et al., 2025]. The model learns an _average-velocity_ field _uθ_ ( _·, r, t_ ; _s, a_ ) and uses the MeanFlow sampling _zr_ = _zt −_ ( _t − r_ ) _u_ ( _zt, r, t_ ). In the one-step case with ( _r, t_ ) = (0 _,_ 1) and _z_ 1 = _ϵ_ , generation is _z_ 0 = _ϵ − uθ_ ( _ϵ,_ 0 _,_ 1). We therefore define the conditional transition sampler as 


**Training from offline transitions.** We train on _D_ = _{_ ( _st, at, rt, st_ +1) _}_ by treating _x_ = _st_ +1 as the data sample. We draw _ϵ ∼ p_ 0 and times 0 _≤ r < t ≤_ 1, and form the linear interpolation _z_ = (1 _− t_ ) _x_ + _tϵ_ . For this path, the conditional velocity is _v_ = _ϵ − x_ [Lipman et al., 2022]. MeanFlow fits _uθ_ by enforcing the MeanFlow identity [Geng et al., 2025] through the regression target 


43 

where the total derivative along the path is _dt_<sup>_<u>d</u>uθ_=</sup><sup>_v ∂zuθ_+</sup><sup>_∂tuθ_(implemented as a Jacobian-vector product).</sup> The training loss is 


where sg( _·_ ) denotes stop-gradient. 

### **F.3 Policy-Tilted Flow World Models** 

A one-step world model trades compute for statistical error: it is fast to sample, but rollout quality depends on where the model is accurate. Since inference-time planning queries transitions induced by the deployed controller, we train the world model under a _tilted_ distribution that emphasizes state–action regions likely under a strong pretrained policy _πψ_ pre. 

**Tilted training objective.** Let _ℓθ_ ( _s, a, s_<sup>_′_</sup> ) denote the per-transition MeanFlow loss from the previous subsection (the contribution inside _L_ MF( _θ_ )) for a transition ( _s, a, s_<sup>_′_</sup> ) _∈D_ . We train the transition model by minimizing the weighted risk 


where the normalized tilt weight is 

and _η ≥_ 0 controls the tilt strength (with _η_ = 0 recovering uniform training). In practice, the denominator is estimated by the minibatch mean so that the average weight in each minibatch is 1. 

The weight _w_ ¯ _η_ ( _s, a_ ) increases for dataset transitions whose actions have higher likelihood under _πψ_ pre( _· | s_ ). This concentrates model capacity on state–action regions that dominate imagined rollouts at deployment, improving rollout fidelity in the MPC loop and mitigating the statistical error introduced by using a one-step MeanFlow transition model. 

### **F.4 Experiments** 

**Benchmarks and evaluation.** We evaluate on the D4RL Gym-MuJoCo locomotion suite [Fu et al., 2020] across HalfCheetah, Hopper, and Walker2d, using the standard v2 datasets in five regimes (medium, expert, medium-expert, medium-replay, full-replay), for a total of 15 tasks. We report D4RL normalized scores computed from episode returns. Each reported value is the mean and standard deviation over 10 evaluation seeds. 

**Methods compared.** ReBRAC is the offline-trained initialization policy [Tarasov et al., 2023a] and is the zero shot performance. `FlowMPC` is our method, which replaces diffusion transition sampling with a one-step MeanFlow transition model and trains the world model with policy-tilted weighting. 

44 

|Task Name|Zero Shot|`FlowMPC`|
|---|---|---|
|halfcheetah-medium|65_._42_±_1_._76|**70.06**_±_1_._9|
|halfcheetah-expert|105_._33_±_3_._21|**106.96**_±_1_._486|
|halfcheetah-medium-expert|103_._79_±_2_._8|**109.89**_±_0_._89|
|halfcheetah-medium-replay|50_._78_±_0_._56|**56.51**_±_5_._5|
|halfcheetah-full-replay|82_._38_±_1_._32|**85.89**_±_0_._95|
|hopper-medium|102_._25_±_0_._23|**103.07**_±_0_._65|
|hopper-expert|100_._74_±_14_._9|**101.21**_±_17_._2|
|hopper-medium-expert|107_._48_±_4_._5|**107.78**_±_3_._06|
|hopper-medium-replay|98_._65_±_5_._15|**102.60**_±_0_._59|
|hopper-full-replay|107_._49_±_0_._74|**108.36**_±_0_._55|
|walker2d-medium|84_._79_±_1_._52|**88.59**_±_1_._2|
|walker2d-expert|112_._19_±_0_._31|**116.44**_±_0_._42|
|walker2d-medium-expert|111_._65_±_0_._46|**115.01**_±_1_._09|
|walker2d-medium-replay|83_._86_±_7_._38|**90.92**_±_4_._2|
|walker2d-full-replay|101_._11_±_3_._9|**104.76**_±_1_._12|
|Average|94_._93|**97.87**|


Table 31: Average normalized score over the final evaluation and ten unseen training seeds on Gym-MuJoCo tasks, excluding random datasets. The symbol _±_ represents the standard deviation across the seeds. 

**Inference-time policy improvement.** Both `DiffMPC` and `FlowMPC` refine the deployed controller at test time. At each environment step, they generate imagined forward rollouts under a learned differentiable transition model, score trajectories using learned rewards and a terminal critic term, and take a small number of gradient steps through the rollout computation graph before executing the resulting action. The key difference is the transition sampler: `DiffMPC` uses a conditional diffusion model with _K_ reverse denoising steps per transition, while `FlowMPC` uses a single-step MeanFlow sampler. 

**Main results on D4RL.** Table 31 summarizes performance on all tasks. `FlowMPC` improves over the ReBRAC initialization on average (83.91 vs. 81.14) and matches or exceeds MPCwDWM on several HalfCheetah regimes. MPCwDWM attains the best average score (85.18), but it relies on iterative diffusion sampling at inference time which is far more expensive. 

**Inference-time compute and latency.** Tables 32 and 33 measure the cost of a single transition evaluation and the corresponding forward+backward cost used in inference-time optimization. Across environments, one-step MeanFlow reduces the forward-pass cost by about 8 _×_ relative to a _K_ = 10 diffusion sampler, with the gap widening linearly as the number of diffusion denoising steps increases. The same trend holds for end-to-end differentiation: MeanFlow reduces total (forward+backward) time by roughly 15 _×_ at _K_ = 10 and by more than 70 _×_ at _K_ = 50. These measurements quantify the bottleneck addressed by `FlowMPC` : rollout generation and differentiation dominate deployment-time compute, and replacing iterative denoising with a one-step sampler yields large, predictable latency reductions. 

45 

|Diffusion Steps|Diffusion (ms)|MeanFlow (ms)|Speedup|
|---|---|---|---|
||<br>**HalfChee**|<br>**tah**||
|10|1_._0200_±_0_._0019|0_._1177_±_0_._0017|8_._67x|
|20|2_._0184_±_0_._0019|0_._1177_±_0_._0017|17_._15x|
|30|3_._0852_±_0_._0008|0_._1177_±_0_._0017|26_._21x|
|40|4_._0280_±_0_._0011|0_._1177_±_0_._0017|34_._22x|
|50|5_._0487_±_0_._0072|0_._1177_±_0_._0017|42_._89x|
||**Hoppe**|**r**||
|10|1_._0211_±_0_._0017|0_._1213_±_0_._0018|8_._42x|
|20|2_._0214_±_0_._0017|0_._1213_±_0_._0018|16_._66x|
|30|3_._0788_±_0_._0010|0_._1213_±_0_._0018|25_._38x|
|40|4_._0237_±_0_._0038|0_._1213_±_0_._0018|33_._17x|
|50|5_._0508_±_0_._0017|0_._1213_±_0_._0018|41_._64x|
||**Walker2**|**d**||
|10|1_._0252_±_0_._0017|0_._1182_±_0_._0019|8_._67x|
|20|2_._0225_±_0_._0018|0_._1182_±_0_._0019|17_._11x|
|30|3_._0796_±_0_._0016|0_._1182_±_0_._0019|26_._05x|
|40|4_._0387_±_0_._0027|0_._1182_±_0_._0019|34_._17x|
|50|5_._0597_±_0_._0007|0_._1182_±_0_._0019|42_._81x|


Table 32: Forward-pass latency comparison between diffusion and MeanFlow on D4RL random datasets (5 runs per measurement). Horizon _H_ = 1, batch size _N_ = 2048. Action dimension: HalfCheetah = 6, Hopper = 3, Walker2d = 6. MeanFlow uses a single step while diffusion uses the number of denoising steps shown. Values report mean _±_ standard deviation in milliseconds. 

46 

|Diffusion Steps|Diffusion Total (ms)|MeanFlow Total (ms)|Speedup|
|---|---|---|---|
||<br>**HalfChe**|<br>**etah**||
|10|3_._2964_±_0_._0011|0_._2184_±_0_._0010|15_._09x|
|20|6_._5419_±_0_._0019|0_._2184_±_0_._0010|29_._95x|
|30|9_._8108_±_0_._0016|0_._2184_±_0_._0010|44_._92x|
|40|13_._0628_±_0_._0009|0_._2184_±_0_._0010|59_._81x|
|50|16_._3602_±_0_._0011|0_._2184_±_0_._0010|74_._91x|
||**Hoppe**|**r**||
|10|3_._3223_±_0_._0012|0_._2261_±_0_._0012|14_._69x|
|20|6_._5865_±_0_._0003|0_._2261_±_0_._0012|29_._13x|
|30|9_._8816_±_0_._0019|0_._2261_±_0_._0012|43_._70x|
|40|13_._1673_±_0_._0006|0_._2261_±_0_._0012|58_._24x|
|50|16_._4745_±_0_._0021|0_._2261_±_0_._0012|72_._86x|
||**Walker**|**2d**||
|10|3_._2956_±_0_._0014|0_._2182_±_0_._0008|15_._10x|
|20|6_._5398_±_0_._0003|0_._2182_±_0_._0008|29_._97x|
|30|9_._8225_±_0_._0022|0_._2182_±_0_._0008|45_._02x|
|40|13_._0738_±_0_._0014|0_._2182_±_0_._0008|59_._92x|
|50|16_._3534_±_0_._0007|0_._2182_±_0_._0008|74_._95x|


Table 33: Total gradient backpropagation time comparison between diffusion and MeanFlow on D4RL random datasets (5 runs). Horizon _H_ = 1, batch size _N_ = 2048. Action dimension: HalfCheetah = 6, Hopper = 3, Walker2d = 6. MeanFlow uses one step while diffusion uses the number of denoising steps shown. Values report mean _±_ standard deviation in milliseconds. 

47 

## **G Broader impacts** 

This work is foundational methods research on offline reinforcement learning, evaluated on standard simulated continuous-control benchmarks (D4RL MuJoCo and AntMaze) rather than on a deployed system. On the positive side, offline RL with inference-time adaptation is motivated by settings where online interaction is costly or unsafe (e.g., healthcare, robotics, autonomous driving, recommender systems), and improving the reliability of policies extracted from fixed datasets can reduce the need for risky exploration in such domains. On the negative side, the same techniques could in principle be applied to high-stakes decision-making systems where errors have real consequences; inference-time policy updates also make the deployed policy state-dependent and harder to audit than a fixed pretrained policy, which could complicate verification in safety-critical applications. We do not release any new datasets or pretrained models that pose elevated misuse risk beyond what is already available through D4RL and standard offline RL baselines, and we view careful domain-specific validation, uncertainty quantification, and human oversight as appropriate mitigations before any real-world deployment. 

48 

