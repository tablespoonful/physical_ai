---
title: "Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination"
date: "2026-05-06"
authors: "Jonathan Spieler; Sven Behnke"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2605.04568
pdf: https://arxiv.org/pdf/2605.04568
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.04568)** / [論文ページ](https://arxiv.org/abs/2605.04568)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

**Jonathan Spieler**<sup>1</sup> **Sven Behnke**<sup>1</sup> 

# **Abstract** 

State-of-the-art model-based Reinforcement Learning (RL) approaches either use gradientfree, population-based methods for planning, learned policy networks, or a combination of policy networks and planning. Hybrid approaches that combine Model Predictive Control (MPC) with a learned model and a policy prior to leverage the advantages of both paradigms have shown promising results. However, these approaches typically rely on gradient-free optimization methods, which can be computationally expensive for high-dimensional control tasks. While gradient-based methods are a promising alternative, recent works have empirically shown that gradient-based methods often perform worse than their gradient-free counterparts. We propose Dream-MPC, a novel approach that generates few candidate trajectories from a rolled-out policy and optimizes each trajectory by gradient ascent using a learned world model, uncertainty regularization and amortization of optimization iterations over time by reusing previously optimized actions. Our results on 24 continuous control tasks show that Dream-MPC can significantly improve the performance of the underlying policy and can outperform gradient-free MPC and state-of-theart baselines. Code and videos are available at https://dream-mpc.github.io. 

# **1. Introduction** 

Reinforcement Learning has achieved promising results in recent years and demonstrated its potential for robotics (Wu et al., 2023; Lancaster et al., 2024; Seo et al., 2025). 

1Autonomous Intelligent Systems, Computer Science Institute VI - Intelligent Systems and Robotics, Center for Robotics and the Lamarr Institute for Machine Learning and Artificial Intelligence, University of Bonn, Germany. Correspondence to: Jonathan Spieler _<_ spieler@ais.uni-bonn.de _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 


_Figure 1._ **Aggregate performance metrics.** Optimality gap, interquartile median (IQM), mean and median normalized scores with 95% confidence intervals of different methods. Notably, Dream-MPC with a strong policy achieves the best results. 

However, model-free methods often struggle with sample efficiency and generalization, especially in complex and highdimensional environments (Byravan et al., 2022). Modelbased RL, on the other hand, can be more sample-efficient and can generalize better, but requires an accurate model of the environment (Xiao et al., 2019). There has been growing interest in world models that are learned from data and can be used for decision-making (Sutton, 1991; Ha & Schmidhuber, 2018). Many recent works (Hafner et al., 2019; Hansen et al., 2022; 2024; Srinivas et al., 2018) use a learned world model for planning through imaginary rollouts with MPC (Richalet et al., 1978; Cutler & Ramaker, 1979) and rely on gradient-free, sampling-based methods such as the Cross Entropy Method (CEM) (Rubinstein, 1997) or Model Predictive Path Integral (MPPI) (Williams et al., 2015; 2017) for trajectory optimization. Although sampling-based MPC methods can be parallelized using Graphics Processing Units (GPUs), their implementation on embedded systems can be challenging due to the limited computational resources. In addition, planning with sampling-based methods is highly inefficient or even intractable in high-dimensional spaces, which might limit their applicability to real-world robotics tasks (Xie et al., 2021). 

In contrast, fully amortized methods such as Dreamer (Hafner et al., 2020) learn a purely reactive policy via imaginary rollouts. Inference for the learned policy is computationally less expensive than the search procedure using CEM, but amortized policies often lack generalization (Byravan et al., 2022). Since the learned world models are differentiable, it is natural to propose gradient-based meth- 

1 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

ods for trajectory optimization because they can be more efficient than gradient-free, sampling-based methods. Instead of sampling many action sequences and evaluating them as done by CEM, gradients backpropagated through the model can be used to guide the optimization procedure (Bharadhwaj et al., 2020). When the action dimension increases, there is an exponential growth in search space for CEM, while there is only a small increase in computational load for gradient descent, i.e., an additional gradient dimension (Bharadhwaj et al., 2020). While few works propose to combine gradient-based optimization with world models, the empirical results observed are worse than for their gradient-free counterparts (Bharadhwaj et al., 2020; S V et al., 2023; Zhou et al., 2025). 

We propose Dream-MPC, a novel method which combines gradient-based MPC with a learned policy network and world model that can significantly improve the performance of the policy and even outperform its gradient-free equivalent and state-of-the-art methods. Our method incorporates uncertainty directly into the optimization objective and amortizes optimization iterations over time to further improve performance and computational efficiency compared to previous approaches. We evaluate our method empirically on various tasks from different domains, including high-dimensional tasks and tasks with visual observations, as well as for different model-based RL algorithms with distinct types of world models and when using gradient-based MPC during training. 

In summary, our contributions are as follows: 

- We propose Dream-MPC, a gradient-based MPC method, which uses a learned world model for predicting future states and costs and achieves state-of-the-art performance on continuous control tasks. 

- Dream-MPC can outperform gradient-free MPC methods, while showing improvements in computational efficiency compared to gradient-free, sampling-based MPC methods. 

- We overcome limitations of prior gradient-based MPC methods by introducing uncertainty regularization and action reuse and evaluate our method extensively on different environments and settings. 

# **2. Related Work** 

**Model-based RL.** Model-based RL tries to learn a model of the environment that can be used to predict the outcome of actions and plan accordingly (Sutton, 1991). World models are considered a central component of human thinking and decision-making processes (Sutton, 1991; Ha & Schmidhuber, 2018; LeCun, 2022). While some approaches to 

world modelling show promising results and are able to generalize to different domains, they are mostly focused on representation learning and not or only partially cover the planning aspect. The combination of elements of planning and search (especially Monte Carlo Tree Search) with deep reinforcement learning has shown remarkable successes in game domains (Silver et al., 2016; 2017a). Most recent model-based RL approaches use the learned world model for planning through imaginary rollouts (Srinivas et al., 2018; Micheli et al., 2023; Hansen et al., 2024; Hafner et al., 2025; Mosbach et al., 2025). However, the performance of these approaches depends heavily on the quality of the learned world model (Talvitie, 2014) and often suffers from the compounding error problem (Asadi et al., 2019). 

**MPC and RL.** State-of-the-art approaches, such as those from the Dreamer family (Hafner et al., 2020; 2021; 2025), use a policy network to predict the actions directly. While policy networks have shown remarkable success for robotics applications, the world model and value function are typically only utilized during training, and the policy is then frozen during inference. This procedure leads to a reactive policy, which can be considered as offline planning and limits the generalization capabilities (Byravan et al., 2022). To address this limitation, recent works such as TD-MPC (Hansen et al., 2022; 2024), POLO (Lowrey et al., 2019) or PlaNet (Hafner et al., 2019) combine model-based RL with online planning through MPC to leverage the benefits of both paradigms. Typically, MPC is performed using gradient-free, sampling-based methods such as CEM or MPPI. Although, the results obtained empirically are often good, for each time step, hundreds or thousands of different action alternatives are sampled and evaluated, which increases the computational effort and renders these approaches only partly suitable for real-time applications. 

**Gradient-based Planning.** The idea of gradient-based planning has been around for decades (Kelley, 1960) and typically refers to backpropagating gradients of a cost function with respect to actions to iteratively optimize a sequence of actions by gradient descent. While early works relied on known analytic forms of environment dynamics, more recent works revisited the idea with learned approximate models of the environment (Srinivas et al., 2018; Silver et al., 2017b; Henaff et al., 2018). However, there are only few works that have been able to successfully perform gradientbased planning and these approaches are usually limited since they either require expert demonstrations (Srinivas et al., 2018) or cannot scale to more challenging robotics tasks (Henaff et al., 2018). Works such as (Bharadhwaj et al., 2020) and (S V et al., 2023) use a Gaussian as a proposal distribution for gradient-based optimization. Typically, a more informative proposal is used for MPC to warm-start the optimization procedure, for example a policy network. Prior works which combine policy models and MPC mostly use 

2 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 


_Figure 2._ **Overview of the proposed approach.** Dream-MPC optimizes action sequences rolled out from a policy network _π_ in latent space _z_ with gradient-based MPC. _N_ candidate trajectories are sampled from the policy prior and optimized for _I_ iterations using gradient ascent to maximize the objective _J_ . The first action from the candidate trajectory with the highest value of _J_ is applied to the environment, and the procedure is repeated for the next time step. The policy network and world model are shared across candidates and time steps. 

the policy model to generate a trajectory, which is then optimized using gradient-free methods (Byravan et al., 2022; Mansard et al., 2018; Hamrick et al., 2021; Argenson & Dulac-Arnold, 2021; Morgan et al., 2021). Since the learned world models are usually differentiable, also gradient-based methods have been proposed for optimizing the trajectory proposal from a policy model (S V et al., 2023). However, gradient-based optimization methods perform worse in their experiments compared to their gradient-free counterparts. The reasons are attributed to problems with the gradients, but are not analyzed in detail. 

Note that while the general idea of combining policy networks with MPC itself is not new, previously proposed methods have only been applied to few and relatively simple tasks without systematically evaluating their performance. To the best of our knowledge, we are the first to achieve a gradient-based MPC method with a learned world model that can outperform its gradient-free equivalent and state-ofthe-art baselines by introducing uncertainty regularization and reusing previously planned actions. We also evaluate the performance of gradient-based MPC for a broad variety of environments, including state- and image-based observations and different types of world models. In order to place our work in context with previous work, we provide a summary over the main differences between Dream-MPC and Policy+Grad-MPC (S V et al., 2023) in Section F. 

# **3. Preliminaries** 

**Reinforcement Learning** can be formulated as an infinitehorizon Markov Decision Process (MDP) with continuous 

action and state spaces, which can be defined as a tuple _⟨S, A, T , R, γ⟩_ , where _S_ and _A_ are the state and action spaces, _T_ : _S × A →S_ is the transition or dynamics function, _R_ : _S × A →_ R is the reward function and _γ_ is a discount factor. The goal is to obtain a policy _π_ : _S →A_ , which maximizes the expected discounted sum of rewards, i.e., the return E _π_ [<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γtrt_],where</sup><sup>_rt_=</sup><sup>_R_(</sup><sup>_st, π_(</sup><sup>_st_)).</sup> Model-based RL learns a model of the environment, often referred to as world model, which is then used for selecting actions and deriving a policy by planning with the learned model. 

**Model Predictive Control** is a well-known method for trajectory optimization, which minimizes a cost function over a finite horizon while taking the system dynamics and constraints into account. The optimization problem is solved at each time step, using the current state as initial condition and the predicted future states. The solution provides the optimal action sequence for the next few time steps with respect to the predicted costs. Thus, MPC generates a locally optimal sequence of actions up to the prediction horizon _H_ by solving the following optimization problem: 


The learned model is used to estimate the return of a candidate trajectory (Negenborn et al., 2005). Since solving Eq. (1) leads to a locally optimal solution and is not guaranteed to solve the general RL problem outlined before, most state-of-the-art methods learn value functions to bootstrap return estimates beyond the horizon _H_ . 

3 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

# **4. Dream-MPC: Gradient-Based Model Predictive Control** 

We propose Dream-MPC, which uses gradient ascent to optimize action sequences sampled from a policy network in an MPC-like manner. The idea is shown in Fig. 2. Since gradient ascent is prone to getting stuck at local optima, we propose to generate few candidate trajectories by sampling from a stochastic policy network. Instead of sampling thousands of trajectories from a Gaussian distribution like CEM, we only consider few trajectories based on the policy. Namely, for each time step _t_ , the algorithm creates _N_ initial action sequences by performing an imaginary rollout of a stochastic policy _πθ_ in latent space _z_ using a learned latent dynamics model _d_ : 


In case of a deterministic policy we add small perturbations to the initial action sequence sampled from the policy to generate _N_ candidate trajectories. The learned world model predicts the following latent states as well as the rewards _r_ ˆ for each state and the terminal values _q_ ˆ. Each trajectory is then refined using gradient ascent with step size _α_ to maximize the respective expected return, which is estimated using the predictions from the world model. The first action of the candidate trajectory with the highest expected return is applied, and the planning procedure is repeated in the next time step. Sampling from a policy provides a warm-start through proposing a decent initial solution for the optimization, which has been shown to be essential for the performance of gradient-free (Hansen et al., 2022) and gradient-based optimization methods (Parmas et al., 2018). Our method allows for combining the benefits of both, fully amortized methods using reactive policies and fully online planning, namely improved generalization while reducing computational costs. In contrast to naively sampling random action sequences, which do not leverage any knowledge of the optimization problem, our approach uses gradients backpropagated through the learned world model to efficiently guide the optimization. 

Since we optimize actions over a receding horizon, but only apply the first action at each time step, we propose to amortize optimization iterations over time by reusing corresponding optimized actions from previous time steps to initialize actions as a mixture of previously optimized action ˜ _a_ and policy actions ˆ _a_ : 


where _ρ_ is the reuse coefficient, which controls the influence of the previously optimized actions. For the action at time step _t_ + _H_ , there is no previously planned action. Thus, 

we initialize the planned action by the same value as the planned action of the previous time step. 

For our experiments, we integrate our method into TDMPC2 (Hansen et al., 2024), a model-based RL algorithm, which performs local trajectory optimization using MPPI in the latent space of a learned world model. Instead of learning a dynamics model using a reconstruction objective, TD-MPC2 implicitly learns a control-centric world model from environment interactions using a combination of jointembedding prediction, reward prediction, and TD-learning without decoding observations. The TD-MPC2 architecture consists of following five learned components: 

|Encoder:|_zt_ =_h_(_st_)_,_|
|---|---|
|Latent dynamics:|_zt_+1 =_d_(_zt, at_)_,_|
|Reward:|ˆ_rt_ =_R_(_zt, at_)_,_|
|Terminal value:|ˆ_qt_ =_Q_(_zt, at_)_,_|
|Policy prior:|ˆ_at ∼πθ_(_zt_)_,_|


where _s_ and _a_ are the states and actions, and _z_ is the latent representation. Since we only consider single-task experiments in this work, we omit the learnable task embedding used for multi-task world models. 

The policy prior _πθ_ serves to guide the sampling-based MPPI trajectory optimizer in TD-MPC2 as well as our gradient-based method. TD-MPC2 maintains a replay buffer _B_ during online interaction, which is used to iteratively update the world model and collect new environment data by planning with the learned model. Please refer to Section C for details on the model training, architecture and MPPI planning procedure. We replace the MPPI planner by our gradient-based MPC method. Our gradient-based MPC algorithm is summarized in Alg. 1. The MPC procedure requires _N × I × H_ evaluations of the world model at each time step, which equals 512 _×_ 6 _×_ 3 = 9216 for MPPI while our method uses significantly less model evaluations, i.e., only 5 _×_ 1 _×_ 3 = 15. Note that while we use TD-MPC2 for our experiments, our method can also be integrated into other model-based reinforcement learning approaches such as Dreamer (Hafner et al., 2020) or DINO-WM (Zhou et al., 2025). We provide additional results for Dream-MPC with Dreamer in Section 5.4. 

We further integrate our method into BMPC (Wang et al., 2025), which builds on TD-MPC2 and learns a policy _πθ_ by imitating an MPC expert _π_ MPC and at the same time uses the policy to guide the MPC optimization process. The results of Wang et al. (2025) show that this bootstrapping approach can improve sample efficiency and asymptotic performance, especially for high-dimensional tasks. We use BMPC since it provides a higher quality policy compared to TD-MPC2, where the performance gap between the policy network and the MPC procedure is quite large as shown in Section D.3. For more details on BMPC, please refer to Section C.2. 

4 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

## **Algorithm 1 Dream-MPC** 

**Input:** Encoder _h_ ( _s_ ), dynamics model _d_ ( _z, a_ ), reward model _R_ ( _z, a_ ), value function model _Q_ ( _z, a_ ), policy prior _πθ_ ( _z_ ), current state _st_ , planning horizon _H_ , optimization iterations _I_ , candidates per iteration _N_ , action optimization rate _α_ Encode state into latent representation _zt ← h_ ( _st_ ). Sample _N_ action sequences by rolling out the policy _πθ_ with the latent dynamics model _d_ . Initialize candidate action sequences _at_ : _t_ + _H_ via Eq. (3). **for** optimization iteration _i_ = 1 _,_ 2 _, . . . I_ **do for** candidate action sequence _n_ = 1 _,_ 2 _, . . . N_ **do for** rollout step _τ_ = _t . . . t_ + _H −_ 1 **do** Predict reward ˆ _rτ_<sup>(</sup><sup>_n_)</sup> = _R_ ( _zτ , aτ_ ). Predict uncertainty _uτ_<sup>(</sup><sup>_n_)</sup> via Eq. (4). Predict next latent state _zτ_<sup>(</sup><sup>_n_</sup> +1<sup>)</sup><sup>_←d_(</sup><sup>_zτ, aτ_).</sup> **end for** Predict terminal value _q_ ˆ _t_<sup>(</sup> +<sup>_n_)</sup> _H_<sup>=</sup><sup>_Q_(</sup><sup>_zt_+</sup><sup>_H, at_+</sup><sup>_H_).</sup> Compute MPC objective _J_<sup>(</sup><sup>_n_)</sup> using ˆ _r_ , _q_ ˆ and _u_ via Eq. (5). Optimize action sequence via _a_<sup>(</sup> _t_ :<sup>_n_</sup> _t_<sup>)</sup> + _H ← at_ : _t_ + _H_ + _α∇aJ_<sup>(</sup><sup>_n_)</sup> . **end for end for return** First optimized action _a_<sup>(</sup> _t_<sup>_k_)</sup> with _k_ = arg max _n{J_<sup>(</sup><sup>_n_)</sup> _}n_<sup>_N_</sup> =1<sup>.</sup> 

requires to specify a coefficient that weighs both aspects, we found it sufficient in our experiments to set _λ_ unc = 0 _._ 01. We use the same hyperparameters as the underlying base methods and also the same set of hyperparameters across all tasks. The parameters specific to our MPC method are listed in Tab. 10. We also conduct experiments in which we use this uncertainty regularization for TD-MPC2 and BMPC and include the results in Section D.3. 

# **5. Experiments** 

We evaluate our method on a set of 24 diverse continuous control tasks from the DeepMind Control Suite (Tassa et al., 2020), HumanoidBench (Sferrazza et al., 2024) and MetaWorld (Yu et al., 2019) covering a wide range of task difficulties including high-dimensional state and action spaces, sparse rewards, complex locomotion, and manipulation. Additionally, we also include results for six DeepMind Control tasks with visual observations. For details on the environments, please refer to Section B. 

## **5.1. Comparison to Baselines** 

We compare our method to following state-of-the-art baselines commonly used for continuous control tasks: 

The world model may be queried on unseen state-action pairs during planning, i.e., when estimating returns of candidate trajectories. This can lead to extrapolation errors even if we have learned a good value function (Feng et al., 2023). Recent work (Lin et al., 2026) has shown that TDMPC2 suffers from value overestimation. To address this, we propose to regularize the planning procedure by penalizing trajectories with a large uncertainty and by balancing estimated returns and (epistemic) model uncertainty when evaluating candidate trajectories. Therefore, we estimate the (epistemic) uncertainty of a trajectory as proposed by Hansen et al. (2024) for offline RL and multi-task world models: 


where _q_ ˆ _m_ is the predicted value from Q-function _m_ from an ensemble of _M_ Q-functions. The regularization strength at each time step is scaled based on the magnitude of the mean value predictions for a given latent state to account for different tasks without requiring task-specific coefficients. 

The planning objective is then redefined as: 


where _λ_ unc is a task-agnostic coefficient that balances return maximization and uncertainty minimization. While this 

- Soft-Actor-Critic (SAC) (Haarnoja et al., 2018), a model-free RL method which uses a maximum entropy objective for policy learning, 

- Dreamer-v3 (Hafner et al., 2025), a model-based RL method which learns a policy network using rollouts from a generative world model, 

- TD-MPC2 (Hansen et al., 2024), a model-based RL method which uses policy-guided MPPI for action selection, and 

- BMPC (Wang et al., 2025), an extension of TD-MPC2 which uses imitation learning of the MPC planner for policy learning. 

We first evaluate the performance of Dream-MPC when replacing the MPPI planner by our proposed gradient-based MPC planner at test time using (pre-)trained TD-MPC2 and BMPC models, respectively. For more details on the baselines refer to Section C. We report performance metrics across all 24 tasks using the _rliable_ package provided by Agarwal et al. (2021) to evaluate the performance of our method. Specifically, we report the optimality gap, median, interquartile median (IQM), and mean normalized scores as well as the performance profile curves with 95% confidence intervals based on the evaluation scores of trained BMPC agents in Figs. 1 and 3. Confidence intervals are estimated using the percentile bootstrap with stratified sampling as 

5 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 


_Figure 3._ **Performance profiles.** Score distributions across all tasks, which provides insights into the variance of the performance. Detailed results are included in Tabs. 11 to 13. 

recommended by Agarwal et al. (2021). For a comparison across different score scales of all tasks, we normalize DeepMind Control Suite scores by dividing by 1000, and HumanoidBench scores as proposed in Lee et al. (2025): 


where we use the random and target success scores provided by the authors. Please refer to Lee et al. (2025) for more details. Meta-World scores are left as they are since the success rates are already values between zero and one. The detailed evaluation results for all environments are shown in Tabs. 11 to 13. Our gradient-based MPC method can improve the performance of the policy network and outperforms MPPI when using BMPC as a basis. Combined with BMPC, Dream-MPC improves the IQM by 26.7% and the mean by 20.5% compared to BMPC, outperforming all baselines. 

While Dream-MPC can also significantly improve the performance of the underlying policy for TD-MPC2 by 144.7% (IQM) and 43.4% (mean), it cannot consistently match the performance of MPPI because for TD-MPC2 there is a large gap between the performance of the policy only and with MPPI as shown in Tab. 1. The detailed results for each environment are shown in Tabs. 14 to 16. We find that having a good policy is important because it leads to better value estimates, which are crucial for gradient-based MPC. This fact favours MPPI, which has a higher diversity of the initial solutions due to the sampling procedure. While we can further improve the performance of Dream-MPC with TD-MPC2 as a basis, for example by increasing the number of optimization iterations, this also increases computational costs. It therefore highlights the importance of a good initial solution to warm-start the MPC optimization process, especially for high-dimensional problems. 

_Table 1._ **Mean scores per domain.** Performance comparison of different TD-MPC2 variants on different benchmarks. 

|**Benchmark**|**TD-MPC2**|**TD-MPC2**<br>**(policy only)**|**Dream-MPC**<br>**(TD-MPC2)**|
|---|---|---|---|
|DeepMind Control|657_±_225|367_±_247|433_±_259|
|HumanoidBench|761_±_1617|224_±_505|379_±_897|
|Meta-World|0.67_±_0.33|0.38_±_0.35|0.62_±_0.31|


## **5.2. Visual Observations** 

Additionally, we evaluate the performance of our method using image-based observations to demonstrate that our method also works well in these settings. The results are shown in Tab. 2. We find that our method can also improve the performance of the underlying policy and even outperforms MPPI for visual observations. 

_Table 2._ **Visual observations.** Performance comparison of different BMPC variants on tasks from the DeepMind Control Suite using image-based observations. 

|**Environment**|**BMPC**|**BMPC**<br>**(policy only)**|**Dream-MPC**<br>**(BMPC)**|
|---|---|---|---|
|Acrobot Swingup|287_±_45|**292**_±_**18**|288_±_31|
|Cartpole Swingup Sparse|709_±_120|625_±_283|**725**_±_**141**|
|Cheetah Run|609_±_23|597_±_45|**643**_±_**9**|
|Hopper Hop|253_±_11|264_±_6|**275**_±_**3**|
|Quadruped Walk|427_±_78|402_±_44|**435**_±_**76**|
|Walker Run|740_±_15|740_±_6|**762**_±_**6**|


The results are the mean episode returns and standard deviations for three random seeds and ten test episodes. **Best** and <u>second best</u> results are highlighted. 

## **5.3. Training with Gradient-based MPC** 

In addition to analyzing our gradient-based MPC method only during inference, we also evaluate its performance when it is already being used during training. Therefore, we use TD-MPC2 as a basis without imitation learning because we hypothesize that the bootstrapping approach of BMPC might lead to unstable training and premature convergence, especially since we have only few candidate trajectories. While combining gradient-based MPC with imitation learning is an interesting research direction, we leave this for future work. Fig. 4 shows the learning curves of BMPC, TD-MPC2 and of Dream-MPC for four different environments. Overall, our gradient-based MPC planner can match the performance of TD-MPC2’s MPPI planner. While for simpler control problems Dream-MPC can even outperform TD-MPC2 and match BMPC, we find that for high-dimensional problems our method performs slightly worse. The lower asymptotic performance of gradient-based MPC results from premature convergence due to less exploration compared to MPPI, which is used by TD-MPC2 and BMPC. We discuss this in more detail in Section G. 

6 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 


_Figure 4._ **Learning curves for four tasks from the DeepMind Control Suite, Meta-World and HumanoidBench.** The line represents the mean episodic return and the shaded area the 95% confidence interval across 3 seeds. 

## **5.4. Integration into Dreamer** 

We also find improvements in sample-efficiency and asymptotic performance when integrating our method into Dreamer, which is shown in Fig. 13. Our evaluation results shown in Tab. 3 further demonstrate that Dream-MPC outperforms all baselines including its gradient-free equivalents and both previously proposed Grad-MPC variants. Implementation details and additional experiments are included in Section E. 

_Table 3._ **Performance comparison of different algorithms.** 

|**Method**|**Acrobot**<br>**Swingup**|**Cheetah**<br>**Run**|**Hopper**<br>**Hop**|**Walker**<br>**Run**|
|---|---|---|---|---|
|SAC+AE|7_±_19|495_±_100|86_±_75|453_±_69|
|PlaNet|7_±_18|535_±_70|1_±_4|228_±_149|
|Dreamer|134_±_91|751_±_111|182_±_43|575_±_33|
|Grad-MPC|7_±_18|438_±_81|3_±_5|382_±_35|
|Policy+Grad-MPC|144_±_7|591_±_131|158_±_47|556_±_33|
|CEM+policy|12_±_26|674_±_20|43_±_42|**638**_±_**21**|
|Dream-MPC (Dreamer)|**147**_±_**101**|**836**_±_**49**|**298**_±_**86**|632_±_52|


The results are the mean episode returns and standard deviations for three random seeds and ten test episodes. **Best** and <u>second best</u> results are highlighted. 

## **5.5. Ablation Study** 

We perform ablations to evaluate our design choices and provide insights into which components are crucial to successfully perform gradient-based MPC. Using a high-quality policy prior to warm-start the MPC optimization is particularly important for high-dimensional problems, as shown in Tab. 4. Together with reusing previously optimized actions, warm-starting reduces computational costs. 

We replace the policy prior by a Gaussian distribution to highlight the importance of a good initial proposal distribution to warm-start the MPC process and use the same number of candidate trajectories as MPPI, i.e., 512. For a fair comparison, we compensate for the less informative prior by increasing the number of optimization iterations to five, which, depending on the environment, leads to an increase in inference time by a factor of about five to ten 

_Table 4._ **Dream-MPC ablations.** We compare the performance of different variants using trained BMPC models. 

|**Method**|**Acrobot**<br>**Swingup**|**Humanoid**<br>**Run**|**Button Press**|**Reach**|
|---|---|---|---|---|
|Dream-MPC (BMPC)|**596**_±_**50**|**531**_±_**38**|0.67_±_0.47|**4348**_±_**215**|
|w/o MPC (policy-only|) 564_±_52|458_±_15|**1.00**_±_**0.00**|2117_±_309|
|w/o policy prior|554_±_21|7_±_4|0.70_±_0.22|842_±_239|
|w/o gradient ascent|579_±_43|496_±_25|0.97_±_0.05|2362_±_323|
|w/o uncertainty reg.|583_±_58|524_±_39|**1.00**_±_**0.00**|4239_±_232|


The results are the mean episode returns and standard deviations for three random seeds and ten test episodes. **Best** and <u>second best</u> results are highlighted. 

compared to Dream-MPC. We further find that uncertainty regularization and amortization of optimization iterations by reuse of previous planned actions are especially important when using gradient-based MPC during training, as illustrated in Fig. 5a. Fig. 5b shows a sensitivity analysis of the uncertainty regularization and action reuse coefficients, emphasizing that Dream-MPC is quite robust to the choice of these parameters. We also conduct experiments in which we use this uncertainty regularization for TD-MPC2 and BMPC and include the results in Section D.3. The results indicate that for BMPC, the performance slightly improves – except for HumanoidBench – while for TD-MPC2, the uncertainty regularization leads to a performance decrease for all three domains. The smaller benefits of our proposed uncertainty regularization reported in Tab. 4 result from smaller value approximation errors for BMPC as discussed in Section G. Additionally, we provide an analysis of the planner gradients when integrating our method into Dreamer in Section E.2, which suggests that Dream-MPC is more robust compared to the previously proposed Grad-MPC. 

We further evaluate the performance of fully trained BMPC agents with gradient-based MPC when varying the number of candidates, the number of optimization iterations, and the planning horizon. The results for Acrobot Swingup, Humanoid Run and Slide are shown in Fig. 12. All other hyperparameters are fixed to their default value when varying one. While we use a single set of hyperparameters across all environments, algorithms, and for state-based and visual ob- 

7 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 


_Figure 5._ **Ablations.** (a) Performance of different Dream-MPC (TD-MPC2) variants demonstrating the importance of each design choice. (b) Performance of Dream-MPC (TD-MPC2) with different uncertainty regularization and action reuse coefficients. The line represents the mean episodic return and the shaded area the 95% confidence interval across 3 seeds. 

servations, we find that dynamically adjusting the planning parameters can help to further improve performance. The parameter sweep also shows that increasing the horizon and the number of optimization iterations does not necessarily always increase the performance further, but can also impair the performance for some environments, which may result from an inaccurate model, especially when using a longer prediction horizon than the one used for training the model. 

_Table 5._ **Inference times of different methods for Acrobot Swingup.** Mean and standard deviation for three random seeds and ten test episodes per seed. 

|**Method**|**Inference time**|
|---|---|
|BMPC|18.77_±_0.11 ms|
|Dream-MPC (BMPC)|**18.15**_±_**0.12 ms**|
|TD-MPC2|20.83_±_0.14 ms|


## **5.6. Inference Time** 

We benchmark inference times of the different methods on a single Nvidia GeForce RTX 4090 GPU. The results in Tab. 5 show that Dream-MPC is about as fast as MPPI for lower dimensional problems, potentially enabling its usage for real-world robotics applications, which require high control frequencies. Although the inference time increases for high-dimensional problems, our method is still significantly faster than Grad-MPC (S V et al., 2023) for example, which samples hundreds of action sequences from a Gaussian and optimizes each candidate solution for multiple iterations by using gradient ascent. The corresponding inference times are shown in Tab. 17. 

# **6. Conclusion** 

We propose Dream-MPC, a novel method for gradient-based planning with a learned policy network and world model, which incorporates amortization of optimization iterations over time and uncertainty to overcome the limitations of previously proposed gradient-based MPC methods, namely worse performance compared to their gradient-free equivalents and high computational costs while also achieving state-of-the-art performance. We empirically evaluate our method on a broad set of diverse tasks from different domains, including visual observations, to demonstrate its effectiveness. Overall, our results highlight that gradientbased trajectory optimization with a learned world model has the potential to significantly improve the performance of model-based RL algorithms. 

8 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

# **Acknowledgements** 

This work was funded by German Research Foundation (DFG) grant BE 2556/16-2 (Research Unit FOR 2535 Anticipating Human Behavior) and by the Federal Ministry of Research, Technology and Space of Germany (BMFTR) within the WestAI - AI Service Center West, grant no. 16IS22094A and within the Robotics Institute Germany, grant no. 16ME0999. Computational resources were provided by the German AI Service Center WestAI. 

# **Impact Statement** 

This paper presents work whose goal is to advance the field of machine learning by introducing Dream-MPC, a gradientbased MPC method for planning with world models. This advancement is particularly relevant for domains such as robotics or autonomous systems, where both prediction and planning are important for safe interaction with the environment. Thus, the deployment of such a technology to real systems requires careful consideration of ethical and safetyrelevant aspects such as out-of-distribution generalization or a lack of transparency in the decision-making process. 

- Cutler, C. R. and Ramaker, B. Dynamic matrix control - A computer control algorithm. _IEEE Transactions on Automatic Control_ , 17:72, 1979. 

- Feng, Y., Hansen, N., Xiong, Z., Rajagopalan, C., and Wang, X. Finetuning offline world models in the real world. In _7th Conference on Robot Learning (CoRL)_ , 2023. 

- Georgiev, I., Giridhar, V., Hansen, N., and Garg, A. PWM: Policy learning with multi-task world models. In _13th International Conference on Learning Representations (ICLR)_ , 2025. 

- Ha, D. and Schmidhuber, J. World models, 2018. URL http://arxiv.org/abs/1803.10122. 

- Haarnoja, T., Zhou, A., Abbeel, P., and Levine, S. Soft Actor-Critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In _35th International Conference on Machine Learning (ICML)_ , 2018. 

- Hafner, D., Lillicrap, T., Fischer, I., Villegas, R., Ha, D., Lee, H., and Davidson, J. Learning latent dynamics for planning from pixels. In _36th International Conference on Machine Learning (ICML)_ , 2019. 

# **References** 

- Agarwal, R., Schwarzer, M., Castro, P. S., Courville, A. C., and Bellemare, M. Deep reinforcement learning at the edge of the statistical precipice. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2021. 

- Argenson, A. and Dulac-Arnold, G. Model-based offline planning. In _9th International Conference on Learning Representations (ICLR)_ , 2021. 

- Asadi, K., Misra, D., Kim, S., and Littman, M. L. Combating the compounding-error problem with a multistep model, 2019. URL http://arxiv.org/abs/ 1905.13320. 

- Bharadhwaj, H., Xie, K., and Shkurti, F. Model-predictive control via cross-entropy and gradient-based optimization. In _2nd Annual Conference on Learning for Dynamics and Control (L4DC)_ , 2020. 

- Byravan, A., Hasenclever, L., Trochim, P., Mirza, M., Ialongo, A. D., Tassa, Y., Springenberg, J. T., Abdolmaleki, A., Heess, N., Merel, J., and Riedmiller, M. A. Evaluating model-based planning and planner amortization for continuous control. In _10th International Conference on Learning Representations (ICLR)_ , 2022. 

- Clavera, I., Rothfuss, J., Schulman, J., Fujita, Y., Asfour, T., and Abbeel, P. Model-based reinforcement learning via meta-policy optimization. In _2nd Conference on Robot Learning (CoRL)_ , 2018. 

- Hafner, D., Lillicrap, T. P., Ba, J., and Norouzi, M. Dream to control: Learning behaviors by latent imagination. In _8th International Conference on Learning Representations (ICLR)_ , 2020. 

- Hafner, D., Lillicrap, T. P., Norouzi, M., and Ba, J. Mastering Atari with discrete world models. In _9th International Conference on Learning Representations (ICLR)_ , 2021. 

- Hafner, D., Pasukonis, J., Ba, J., and Lillicrap, T. Mastering diverse control tasks through world models. _Nature_ , 640: 647–653, 2025. 

- Hamrick, J. B., Friesen, A. L., Behbahani, F. M. P., Guez, A., Viola, F., Witherspoon, S., Anthony, T., Buesing, L. H., Velickovic, P., and Weber, T. On the role of planning in model-based deep reinforcement learning. In _9th International Conference on Learning Representations (ICLR)_ , 2021. 

- Hansen, N., Su, H., and Wang, X. Temporal difference learning for model predictive control. In _39th International Conference on Machine Learning (ICML)_ , 2022. 

- Hansen, N., Su, H., and Wang, X. TD-MPC2: Scalable, robust world models for continuous control. In _12th International Conference on Learning Representations (ICLR)_ , 2024. 

- Henaff, M., Whitney, W. F., and LeCun, Y. Model-based planning with discrete and continuous actions, 2018. URL http://arxiv.org/abs/1705.07177. 

9 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

- Hubert, T., Schrittwieser, J., Antonoglou, I., Barekatain, M., Schmitt, S., and Silver, D. Learning and planning in complex action spaces. In _38th International Conference on Machine Learning (ICML)_ , 2021. 

- Kelley, H. J. Gradient theory of optimal flight paths. _ARS Journal_ , 30(10):947–954, 1960. 

- Kingma, D. P. and Ba, J. Adam: A method for stochastic optimization. In _3rd International Conference on Learning Representations (ICLR)_ , 2015. 

- Lancaster, P., Hansen, N., Rajeswaran, A., and Kumar, V. MoDem-V2: Visuo-motor world models for real-world robot manipulation. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2024. 

- LeCun, Y. A path towards autonomous machine intelligence version 0.9.2, 2022-06-27, 2022. URL https: //openreview.net/pdf?id=BZ5a1r-kVsf. 

- Lee, H., Lee, Y., Seno, T., Kim, D., Stone, P., and Choo, J. Hyperspherical normalization for scalable deep reinforcement learning. In _42nd International Conference on Machine Learning (ICML)_ , 2025. 

- Lin, H., Wang, P., Schneider, J., and Shi, G. TD-M(PC)<sup>2</sup> : Improving temporal difference MPC through policy constraint. In _8th Annual Conference on Learning for Dynamics and Control (L4DC)_ , 2026. 

- Lowrey, K., Rajeswaran, A., Kakade, S. M., Todorov, E., and Mordatch, I. Plan online, learn offline: Efficient learning and exploration via model-based control. In _7th International Conference on Learning Representations (ICLR)_ , 2019. 

- Mansard, N., DelPrete, A., Geisert, M., Tonneau, S., and Stasse, O. Using a memory of motion to efficiently warmstart a nonlinear predictive controller. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2018. 

- Micheli, V., Alonso, E., and Fleuret, F. Transformers are sample-efficient world models. In _11th International Conference on Learning Representations (ICLR)_ , 2023. 

- Morgan, A. S., Nandha, D., Chalvatzaki, G., D’Eramo, C., Dollar, A. M., and Peters, J. Model predictive actor-critic: Accelerating robot skill acquisition with deep reinforcement learning. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2021. 

- Mosbach, M., Ewertz, J. N., Villar-Corrales, A., and Behnke, S. SOLD: Slot object-centric latent dynamics models for relational manipulation learning from pixels. In _42nd International Conference on Machine Learning (ICML)_ , 2025. 

- Negenborn, R. R., De Schutter, B., Wiering, M. A., and Hellendoorn, H. Learning-based model predictive control for Markov decision processes. In _16th IFAC World Congress_ , 2005. 

- Parmas, P., Rasmussen, C. E., Peters, J., and Doya, K. PIPPS: Flexible model-based policy search robust to the curse of chaos. In _35th International Conference on Machine Learning (ICML)_ , 2018. 

- Parmas, P., Seno, T., and Aoki, Y. Model-based reinforcement learning with scalable composite policy gradient estimators. In _40th International Conference on Machine Learning (ICML)_ , 2023. 

- Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J., Chanan, G., Killeen, T., Lin, Z., Gimelshein, N., Antiga, L., Desmaison, A., Kopf, A., Yang, E., DeVito, Z., Raison, M., Tejani, A., Chilamkurthy, S., Steiner, B., Fang, L., Bai, J., and Chintala, S. PyTorch: An imperative style, high-performance deep learning library. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2019. 

- Richalet, J., Rault, A., Testud, J., and Papon, J. Model predictive heuristic control. _Automatica_ , 14(5):413–428, 1978. 

- Rubinstein, R. Y. Optimization of computer simulation models with rare events. _European Journal of Operational Research_ , 99(1):89–112, 1997. 

- S V, J., Jalagam, S., LeCun, Y., and Sobal, V. Gradientbased planning with world models, 2023. URL http: //arxiv.org/abs/2312.17227. 

- Seo, Y., Sferrazza, C., Chen, J., Shi, G., Duan, R., and Abbeel, P. Learning sim-to-real humanoid locomotion in 15 minutes. 2025. URL https://arxiv.org/ abs/2512.01996. 

- Sferrazza, C., Huang, D.-M., Lin, X., Lee, Y., and Abbeel, P. HumanoidBench: Simulated humanoid benchmark for whole-body locomotion and manipulation. In _Robotics: Science and Systems Conference (RSS)_ , 2024. 

- Silver, D., Huang, A., Maddison, C. J., Guez, A., Sifre, L., Van Den Driessche, G., Schrittwieser, J., Antonoglou, I., Panneershelvam, V., Lanctot, M., Dieleman, S., Grewe, D., Nham, J., Kalchbrenner, N., Sutskever, I., Lillicrap, T., Leach, M., Kavukcuoglu, K., Graepel, T., and Hassabis, D. Mastering the game of Go with deep neural networks and tree search. _Nature_ , 529(7587):484–489, 2016. 

- Silver, D., Schrittwieser, J., Simonyan, K., Antonoglou, I., Huang, A., Guez, A., Hubert, T., Baker, L., Lai, M., Bolton, A., Chen, Y., Lillicrap, T., Hui, F., Sifre, L., Van Den Driessche, G., Graepel, T., and Hassabis, D. Mastering the game of Go without human knowledge. _Nature_ , 550(7676):354–359, 2017a. 

10 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

- Silver, D., van Hasselt, H., Hessel, M., Schaul, T., Guez, A., Harley, T., Dulac-Arnold, G., Reichert, D., Rabinowitz, N., Barreto, A., and Degris, T. The predictron: End-to-end learning and planning. In _34th International Conference on Machine Learning (ICML)_ , 2017b. 

- Srinivas, A., Jabri, A., Abbeel, P., Levine, S., and Finn, C. Universal planning networks: Learning generalizable representations for visuomotor control. In _35th International Conference on Machine Learning (ICML)_ , 2018. 

- Suh, H. J., Simchowitz, M., Zhang, K., and Tedrake, R. Do differentiable simulators give better policy gradients? In _39th International Conference on Machine Learning (ICML)_ , 2022. 

- Sutton, R. S. Dyna, an integrated architecture for learning, planning, and reacting. _ACM SIGART Bulletin_ , 2(4): 160–163, 1991. 

   - Yarats, D., Zhang, A., Kostrikov, I., Amos, B., Pineau, J., and Fergus, R. Improving sample efficiency in model-free reinforcement learning from images. In _AAAI Conference on Artificial Intelligence_ , 2021. 

   - Yarats, D., Fergus, R., Lazaric, A., and Pinto, L. Mastering visual continuous control: Improved data-augmented reinforcement learning. In _10th International Conference on Learning Representations (ICLR)_ , 2022. 

   - Yu, T., Quillen, D., He, Z., Julian, R., Hausman, K., Finn, C., and Levine, S. Meta-World: A benchmark and evaluation for multi-task and meta reinforcement learning. In _3rd Conference on Robot Learning (CoRL)_ , 2019. 

   - Zhou, G., Pan, H., LeCun, Y., and Pinto, L. DINO-WM: World models on pre-trained visual features enable zeroshot planning. In _42nd International Conference on Machine Learning (ICML)_ , 2025. 

- Talvitie, E. Model regularization for stable sample rollouts. In _30th Conference on Uncertainty in Artificial Intelligence (UAI)_ , 2014. 

- Tassa, Y., Tunyasuvunakool, S., Muldal, A., Doron, Y., Trochim, P., Liu, S., Bohez, S., Merel, J., Erez, T., Lillicrap, T., and Heess, N. dm ~~c~~ ontrol: Software and tasks for continuous control. _Software Impacts_ , 6, 2020. 

- Wang, Y., Guo, H., Wang, S., Qian, L., and Lan, X. Bootstrapped model predictive control. In _13th International Conference on Learning Representations (ICLR)_ , 2025. 

- Williams, G., Aldrich, A., and Theodorou, E. A. Model predictive path integral control using covariance variable importance sampling. 2015. URL http://arxiv. org/abs/1509.01149. 

- Williams, G., Wagener, N., Goldfain, B., Drews, P., Rehg, J. M., Boots, B., and Theodorou, E. A. Information theoretic MPC for model-based reinforcement learning. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2017. 

- Wu, P., Escontrela, A., Hafner, D., Abbeel, P., and Goldberg, K. DayDreamer: World models for physical robot learning. In _6th Conference on Robot Learning (CoRL)_ , 2023. 

- Xiao, C., Wu, Y., Ma, C., Schuurmans, D., and Muller, M.¨ Learning to combat compounding-error in model-based reinforcement learning, 2019. URL https://arxiv. org/abs/1912.11206. 

- Xie, K., Bharadhwaj, H., Hafner, D., Garg, A., and Shkurti, F. Latent skill planning for exploration and transfer. In _9th International Conference on Learning Representations (ICLR)_ , 2021. 

11 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

# **A. Limitations and Future Work** 

**Fixed optimization parameters.** Our experiments suggest that it may be beneficial to dynamically adapt the optimization parameters such as the action optimization step size and number of iterations to further improve the performance, especially for high-dimensional problems. 

**Policy prior.** We find that gradient-based MPC requires a high-quality policy prior for efficient planning, which may not always be available. This can potentially be addressed by more sophisticated planning architectures. 

**Future work.** As our current approach is applied to single-task problems, it would also be interesting to extend it to multi-task world models to evaluate its potential in this setting. 

# **B. Environment Details** 

We evaluate our method on a total of 24 continuous control tasks from three different domains: eight environments from the Deep Mind Control suite, including four high-dimensional locomotion tasks, eight environments from HumanoidBench, and eight environments from Meta-World. All three domains are infinite-horizon continuous control environments for which we use a fixed episode length, an action repeat of 2 for the DeepMind Control Suite and Meta-World and 1 for HumanoidBench, and no termination conditions. We follow the success definition of Hansen et al. (2024). This section provides an overview and details for all tasks considered, including their observation and action dimensions. 


_Figure 6._ **DeepMind Control Suite benchmarking domains (Tassa et al., 2020).** 

_Table 6._ **Overview of DeepMind Control Suite tasks.** Classification is based on Hubert et al. (2021); Yarats et al. (2022) 

|**Task**|**Difficulty**|**Reward**|**dim(**_S_**)**|**dim(**_A_**)**|
|---|---|---|---|---|
|Acrobot Swingup|hard|dense|6|1|
|Cartpole Swingup Sparse|easy|sparse|5|1|
|Dog Run|hard|dense|223|38|
|Dog Walk|hard|dense|223|38|
|Fish Swim|medium|dense|24|5|
|Hopper Hop|medium|dense|15|4|
|Humanoid Run|hard|dense|67|24|
|Humanoid Walk|hard|dense|67|24|


12 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

We consider following eight tasks from Meta-World: 

- Assembly: Pick up a nut and place it onto a peg (peg and nut positions are randomized), 

- Button Press: Press a button (button positions are randomized), 

- Disassemble: Remove a nut from a peg (peg and nut positions are randomized), 

- Lever Pull: Pull a lever down 90 degrees (lever positions are randomized), 

- Pick Place Wall: Pick a puck, bypass a wall and place the puck (puck and goal positions are randomized), 

- Push Back: Push the puck to a goal (puck and goal positions are randomized), 

- Shelf Place: Pick and place a puck onto a shelf (puck and shelf positions are randomized), 

- Window Open: Push and open a window (window positions are randomized). 

All tasks from Meta-World share the same embodiment, observation space (dim( _S_ ) = 39) and action space (dim( _A_ ) = 4). Please refer to Yu et al. (2019) for the definitions of the reward functions and success metrics used in the Meta-World tasks. 


_Figure 7._ **Meta-World manipulation tasks.** We consider eight different tasks from the Meta-World Benchmark. 

We further consider following eight tasks from the twelve benchmarking locomotion tasks of HumanoidBench: 

- Balance Hard: Balance on the unstable board while the spherical pivot beneath the board does move, 

- Balance Simple: Balance on the unstable board while the spherical pivot beneath the board does not move, 

- Hurdle: Keep forward velocity close to 5 m/s while successfully overcoming hurdles, 

- Maze: Reach the goal position in a maze by taking multiple turns at the intersections, 

- Reach: Reach a randomly initialized 3D point with the left hand, 

- Run: Run forward at a speed of 5 m/s, 

- Slide: Walk over an iterating sequence of upward and downward slides at 1 m/s, 

- Stair: Traverse an iterating sequence of upward and downward stairs at 1 m/s. 

## Visualizations of the tasks are shown in Fig. 8. 

The benchmark uses the Unitree H1 with two dexterous hands. The observation and action spaces, and degrees of freedom of the robot system with the dexterous hands are summarized in Tab. 7. 

13 

### **Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 


_Figure 8._ **HumanoidBench locomotion tasks.** We consider eight tasks from the HumanoidBench locomotion benchmark that cover a wide variety of interactions and difficulties. This figure illustrates an initial state for each task. 

_Table 7._ **Humanoid robot specifications with two hands.** 

|**Parameter**|**Value**|
|---|---|
|Observation space|151|
|Action space|61|
|DoF (body)|25|
|DoF (hands)|50|


# **C. Implementation Details** 

**TD-MPC2 implementation.** We use the official implementation of TD-MPC2 available at https://github.com/ nicklashansen/tdmpc2, and use the default hyperparameters suggested by the authors. A complete list of hyperparameters is provided in Tab. 8. Details on TD-MPC2 can be found in Section C.1. For the experiments with (pre-)trained models, we use the models provided by Hansen et al. (2024) for the DeepMind Control Suite and Meta-World, except for Cartpole Swingup Sparse, Dog Run, Dog Walk, Humanoid Run and Humanoid Walk because some checkpoints cannot be loaded after code restructuring<sup>1</sup> . Thus, we train new models from scratch for these tasks as well as for HumanoidBench. 

**BMPC implementation.** We use the official implementation of BMPC from https://github.com/ wertyuilife2/bmpc, and use the default hyperparameters suggested by the authors. Since the code is based on the official TD-MPC2 codebase and incorporates both algorithms, we use this implementation as a basis for our method. Details on BMPC are provided in Section C.2. We train all BMPC models from scratch. 

**Dreamer-v3 baseline implementation.** We use the official implementation of Dreamer-v3 available at https:// github.com/danijar/dreamerv3. We follow the decision of Hansen et al. (2024) and use the authors’ suggested hyperparameters for proprioceptive control (DeepMind Control Suite). Please refer to Hafner et al. (2025) and Hansen et al. (2024) for a complete list of hyperparameters and implementation details. 

> 1cf. https://github.com/nicklashansen/tdmpc2/issues/23 

14 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

**SAC baseline implementation.** We use the SAC implementation from https://github.com/denisyarats/ pytorch_sac as in the TD-MPC (Hansen et al., 2022) paper, and use the hyperparameters suggested by the authors. Please refer to their paper for a complete list of hyperparameters. 

## **C.1. TD-MPC2** 

**Architectural details.** All components of TD-MPC2 are implemented as multi-layer perceptrons (MLPs). The encoder _h_ contains a variable number of layers (2 _−_ 5), depending on the architecture size; all other components are 3-layer MLPs. Intermediate layers consist of a linear layer followed by LayerNorm and a Mish activation function. The latent representation is normalized as a simplicial embedding. _Q_ -functions additionally use Dropout. We summarize the TD-MPC2 architecture for the 5M parameter base (default for online RL) model size using PyTorch-like notation: 

Encoder parameters: 167,936 Dynamics parameters: 843,264 Reward parameters: 631,397 Policy parameters: 582,668 Q parameters: 3,156,985 Task parameters: 7,680 Total parameters: 5,389,930 

Architecture: TD-MPC2 base 5M( (task_embedding): Embedding(T, 96, max_norm=1) (encoder): ModuleDict( (state): Sequential( (0): NormedLinear(in_features=S+T, out_features=256, act=Mish) (1): NormedLinear(in_features=256, out_features=512, act=SimNorm) ) ) (dynamics): Sequential( (0): NormedLinear(in_features=512+T+A, out_features=512, act=Mish) (1): NormedLinear(in_features=512, out_features=512, act=Mish) (2): NormedLinear(in_features=512, out_features=512, act=SimNorm) ) (reward): Sequential( (0): NormedLinear(in_features=512+T+A, out_features=512, act=Mish) (1): NormedLinear(in_features=512, out_features=512, act=Mish) (2): Linear(in_features=512, out_features=101,) ) (pi): Sequential( (0): NormedLinear(in_features=512+T, out_features=512, act=Mish) (1): NormedLinear(in_features=512, out_features=512, act=Mish) (2): Linear(in_features=512, out_features=2A, bias=True) ) (Qs): Vectorized ModuleList( (0-4): 5 x Sequential( (0): NormedLinear(in_features=512+T+A, out_features=512, dropout=0.01, act=Mish) (1): NormedLinear(in_features=512, out_features=512, act=Mish) (2): Linear(in_features=512, out_features=101, bias=True) ) ) 

where S is the input dimensionality, T is the number of tasks, and A is the action space. We exclude the task embedding T from single-task experiments. The exact parameter counts listed above are for S= 39, T= 80, and A= 6. Since we only perform single-task experiments in this work, all models contain around 5M parameters for TD-MPC2. 

**Policy-guided MPC.** TD-MPC2 uses Model Predictive Path Integral (MPPI) (Williams et al., 2015; 2017) for local trajectory optimization, which is a gradient-free, sampling-based MPC method. MPPI iteratively samples action sequences ( _at, at_ +1 _, . . . , at_ + _H_ ) of length _H_ from _N_ ( _µ, σ_<sup>2</sup> ), evaluates their expected return by rolling out latent trajectories with the model, and updates the parameters _µ, σ_ of a time-dependent multivariate Gaussian with diagonal covariance based on a weighted average such that the expected return is maximized. This iterative optimization procedure is repeated for a fixed number of iterations and the first action _at ∼N_ ( _µ_<sup>_∗_</sup> _t_<sup>_, σ_</sup> _t_<sup>_∗_) is applied to the environment.TD-MPC2 augments the sampling</sup> procedure with samples from the policy prior _πθ_ and warm-starts the optimization procedure by initializing ( _µ, σ_ ) as the solution of the previous step shifted by one to improve performance. Please refer to Hansen et al. (2022) for more details. 

**— Appendices continue on next page —** 

15 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

_Table 8._ **TD-MPC2 hyperparameters.** We use the same hyperparameters across all tasks. Certain hyperparameters are set automatically using heuristics. 

|**Hyperparameter**|**Value**|
|---|---|
|**Planning**||
|Horizon (_H_)|3|
|Iterations|6 (+2if_∥A∥≥_20)|
|Population size|512|
|Policy prior samples|24|
|Number of elites|64|
|Minimum std.|0_._05|
|Maximum std.|2|
|Temperature|0_._5|
|Momentum|No|
|**Policy prior**||
|Log std. min.|_−_10|
|Log std. max.|2|
|**Replay buffer**||
|Capacity|1_,_000_,_000|
|Sampling|Uniform|
|**Architecture (5M)**||
|Encoder dim|256|
|MLP dim|512|
|Latent state dim|512|
|Task embedding dim|96|
|Task embedding norm|1|
|Activation|LayerNorm + Mish|
|_Q_-function dropout rate|1%|
|Number of_Q_-functions|5|
|Number of reward/value bins|101|
|SimNorm dim (_V_)|8|
|SimNorm temperature (_τ_)|1|
|**Optimization**||
|Update-to-data ratio|1|
|Batch size|256|
|Joint-embedding coef.|20|
|<br>Reward prediction coef.|0_._1|
|<br>Value prediction coef.|0_._1|
|Temporal coef. (_λ_)|0_._5|
|_Q_-fn. momentum coef.|0_._99|
|Policy prior entropy coef.|1_×_10<sup>_−_4</sup>|
|<br>Policy prior loss norm.|Moving(5%_,_95%)percentiles|
|Optimizer|Adam (Kingma & Ba, 2015)|
|Learning rate|<br>3_×_10<sup>_−_4</sup>|
|Encoder learning rate|1_×_10<sup>_−_4</sup>|
|<br>Gradient clip norm|20|
|Discount factor|Heuristic|
|Seed steps|Heuristic|


16 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

## **C.2. BMPC** 

**Architectural details.** The main architectural difference of BMPC to TD-MPC2 is that it uses two _V_ -functions instead of five _Q_ -functions: 

V parameters: 1,256,650 

Total parameters: 3,489,595 

Architecture: Difference BMPC to TD-MPC2 ( (Vs): Vectorized ModuleList( (0-1): 2 x Sequential( (0): NormedLinear(in_features=512+T, out_features=512, dropout=0.01, act=Mish) (1): NormedLinear(in_features=512, out_features=512, act=Mish) (2): Linear(in_features=512, out_features=101, bias=True) ) ) 

**Policy learning.** The policy is learned using the following objective: 


where _H_ is the entropy, KL is the Kullback-Leibler divergence, **z** 0: _H_ are latent vectors rolled out using the models _h_ and _d_ , and _β_ and _λ_ are hyperparameters for loss balancing and temporal weighting, respectively. The KL loss is normalized using moving percentiles _S_ , which are commonly used to stabilize training. 

**Model-based TD-learning.** Since BMPC does not use a SAC-style max-Q approach for policy improvement, the authors decide to learn a state value function _Vϕ_ instead of a state-action value function _Qϕ_ . The value network is learned by minimizing the cross-entropy loss with respect to the discretized n-step TD-target _V_<sup>ˆ</sup> computed by using the latest model, policy, and target value network: 


where _N_ is the TD horizon, **z** 0: _H_ are latent vectors rolled out through the models _h_ and _d_ . _V_<sup>ˆ</sup> is the TD-target computed using the model _d, R_ and the policy _πθ_ in an on-policy manner. The authors use a fixed value of _N_ = 1 to keep compounding errors small. 

**Lazy reanalyze.** BMPC stores imitation targets in the replay buffer and uses lazy reanalyze to avoid costly replanning for all samples during every update to compute the policy objective. For every _k_ -th network update, _b_ samples are drawn from the batch and used to get new imitation targets, i.e., the mean and standard deviation of the action distribution _πt_ = _π_ MPC( _·|h_ ( **s** _t_ ) _, πθ_ ) by replanning. These targets _πt_ are then placed back into the replay buffer. Since the replanning is performed independently of the training process, the replay buffer can be approximately seen as an expert dataset and used to sample state-action pairs from it for supervised learning. During replanning, additional noise is added to the policy prior to increase exploration in MPC planning. Thus, the resulting surrogate policy objective with lazy reanalyze can be defined as: 


where _πt_ is the expert action distribution from the replay buffer. 

**— Appendices continue on next page —** 

17 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

_Table 9._ **BMPC hyperparameters.** We use the same hyperparameters for all tasks. All other hyperparameters are the default TD-MPC2 values. 

|**Hyperparameter**|**Value**|
|---|---|
|**Planning**||
|Horizon|3|
|Replanning horizon|3|
|Lazy reanalyze interval (_k_)|10|
|Lazy reanalyze batch size (_b_)|20|
|**Policy prior**||
|Log std. min.|_−_3|
|Log std. max.|1|
|Log std. min. (replanning)|_−_2|
|Log std. max. (replanning)|1|
|**Architecture**||
|Number of_V_-functions|2|
|**Optimization**||
|Batch size|256|
|TD horizon (_N_)|1<br>|
|Policy prior entropy coef.|1_×_10<sup>_−_4</sup>|


## **C.3. Dream-MPC** 

The hyperparameters specific to our method are listed in Tab. 10. 

_Table 10._ **Dream-MPC planning hyperparameters.** We use the same set of hyperparameters for all tasks. All other hyperparameters are the default TD-MPC2 and BMPC values respectively. 

|**Hyperparameter**|**Value**|
|---|---|
|Iterations_I_|1|
|Policy prior samples_N_|5|
|Optimization step size_α_|0_._1|
|Action reuse coefficient_ρ_|0_._1|
|Uncertainty regularization coefficient_λ_unc|0_._01|


# **D. Additional Results** 

In this section, we provide results for Dream-MPC when varying the computational budget, the learning curves for all baselines as well as detailed evaluation results for all environments. 

## **D.1. Learning Curves** 

Figs. 9 to 11 show the episode returns and the success rates as a function of environment steps, respectively. 

## **— Appendices continue on next page —** 

18 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 


_Figure 9._ **Learning curves for the DeepMind Control Suite.** The line represents the mean episodic return and the shaded area the 95% confidence interval across 3 seeds. 


_Figure 10._ **Learning curves for Meta-World.** The line represents the mean episodic return and the shaded area the 95% confidence interval across 3 seeds. 


_Figure 11._ **Learning curves for HumanoidBench.** The line represents the mean episodic return and the shaded area the 95% confidence interval across 3 seeds. 

19 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

## **D.2. Detailed Evaluation Results** 

We provide detailed results for all environments in Tabs. 11 to 13. We find that having a good policy is important because it leads to better value estimates, which are crucial for gradient-based MPC. While Dream-MPC can improve the performance of the policy for TD-MPC2, it cannot consistently match the performance of MPPI. Since the performance of the policy is quite weak as shown in Tabs. 14 to 16, this fact favours MPPI, which has a higher diversity of the initial solutions due to the sampling procedure. While we can further improve the performance of Dream-MPC with TD-MPC2 as a basis, for example by increasing the number of optimization iterations, this also increases computational costs. This highlights the importance of a good initial solution to warm-start the MPC optimization process, especially for high-dimensional problems. 

_Table 11._ **DeepMind Control Suite evaluation results of different algorithms.** 

|**Task**|**SAC**|**Dreamer-v3**|**TD-MPC2**|**BMPC**|**Dream-MPC**<br>**(TD-MPC2)**|**Dream-MPC**<br>**(BMPC)**|
|---|---|---|---|---|---|---|
|Acrobot Swingup|176_±_21|372_±_141|595_±_34|587_±_25|590_±_40|**596**_±_**50**|
|Cartpole Swingup Sparse|788_±_10|538_±_325|848_±_0|837_±_14|847_±_3|**849**_±_**1**|
|Fish Swim|657_±_110|729_±_98|786_±_8|804_±_17|764_±_56|**816**_±_**11**|
|Hopper Hop|287_±_15|198_±_111|**493**_±_**47**|404_±_39|307_±_38|423_±_54|
|Dog Run|15_±_6|26_±_7|358_±_228|678_±_27|115_±_72|**703**_±_**19**|
|Dog Walk|42_±_33|47_±_20|933_±_10|937_±_4|389_±_22|**946**_±_**7**|
|Humanoid Run|83_±_43|1_±_1|344_±_60|528_±_29|110_±_10|**531**_±_**38**|
|Humanoid Walk|364_±_95|2_±_1|899_±_10|917_±_6|338_±_63|**937**_±_**4**|
|**Mean**|302_±_269|239_±_261|657_±_225|711_±_181|433_±_259|**725**_±_**181**|


The results are the mean episode returns and standard deviations for three random seeds and ten test episodes. **Best** and second best results are highlighted. 

_Table 12._ **Meta-World evaluation results of different algorithms.** 

|**Task**|**SAC**|**Dreamer-v3**|**TD-MPC2**|**BMPC**|**Dream-MPC**<br>**(TD-MPC2)**|**Dream-MPC**<br>**(BMPC)**|
|---|---|---|---|---|---|---|
|Assembly|0.0_±_0.0|0.0_±_0.0|1.0_±_0.0|1.0_±_0.0|1.0_±_0.0|**1.0**_±_**0.0**|
|Button Press|0.27_±_0.31|0.61_±_0.02|0.33_±_0.47|0.33_±_0.47|0.33_±_0.47|**0.67**_±_**0.47**|
|Disassemble|0.03_±_0.05|0.27_±_0.23|0.67_±_0.47|1.0_±_0.0|0.67_±_0.47|**1.0**_±_**0.0**|
|Lever Pull|0.03_±_0.05|0.52_±_0.1|0.0_±_0.0|0.67_±_0.47|0.0_±_0.0|**0.67**_±_**0.47**|
|Pick Place Wall|0.0_±_0.0|0.21_±_0.24|**1.0**_±_**0.0**|0.0_±_0.0|0.67_±_0.47|0.67_±_0.47|
|Push Back|0.67_±_0.47|0.32_±_0.23|0.67_±_0.47|0.33_±_0.47|**0.67**_±_**0.47**|0.33_±_0.47|
|Shelf Place|0.0_±_0.0|0.27_±_0.21|0.67_±_0.47|0.67_±_0.47|1.0_±_0.0|**1.0**_±_**0.0**|
|Window Open|1.0_±_0.0|0.48_±_0.09|1.0_±_0.0|0.67_±_0.47|0.67_±_0.47|**1.0**_±_**0.0**|
|**Mean**|0.25_±_0.36|0.33_±_0.18|0.67_±_0.33|0.58_±_0.32|0.62_±_0.31|**0.79**_±_**0.23**|


The results are the mean episode successes and standard deviations for three random seeds and ten test episodes. **Best** and second best results are highlighted. 

_Table 13._ **HumanoidBench evaluation results of different algorithms.** 

|**Task**|**SAC**|**Dreamer-v3**|**TD-MPC2**|**BMPC**|**Dream-MPC**<br>**(TD-MPC2)**|**Dream-MPC**<br>**(BMPC)**|
|---|---|---|---|---|---|---|
|Balance Hard|55_±_3|28_±_12|**92**_±_**12**|81_±_12|45_±_10|82_±_12|
|Balance Simple|70_±_10|39_±_14|240_±_37|489_±_84|47_±_14|**654**_±_**89**|
|Hurdle|5_±_3|13_±_5|78_±_24|120_±_43|12_±_1|**249**_±_**34**|
|Maze|140_±_7|110_±_4|169_±_47|**349**_±_**2**|120_±_8|266_±_33|
|Reach|2048_±_212|2151_±_1038|**5037**_±_**1436**|4125_±_324|2751_±_444|4348_±_215|
|Run|8_±_3|11_±_5|136_±_110|139_±_81|10_±_7|**302**_±_**11**|
|Slide|11_±_5|56_±_29|237_±_54|442_±_36|16_±_3|**632**_±_**114**|
|Stair|15_±_15|35_±_17|100_±_18|403_±_145|30_±_6|**456**_±_**145**|
|**Mean**|294_±_664|305_±_698|761_±_1617|769_±_1277|379_±_897|**874**_±_**1326**|


The results are the mean episode returns and standard deviations for three random seeds and ten test episodes. **Best** and second best results are highlighted. 

20 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

## **D.3. Detailed TD-MPC2 and BMPC Results** 

We include full results of TD-MPC2 and BMPC for all environments in Tabs. 14 to 16, including the performance of using the underlying policy network only. We also conduct experiments in which we apply the test-time regularization defined in Eq. (4) with a regularization coefficient of _λ_ unc = 0 _._ 01 to TD-MPC2 and BMPC. While the regularization can improve the performance of BMPC in some cases, it causes a significant performance decrease for TD-MPC2, especially for high-dimensional problems. 

_Table 14._ **DeepMind Control Suite evaluation results of different TD-MPC2 and BMPC variants.** 

|**Environment**|**TD-MPC2**|**TD-MPC2**<br>**(policy only)**|**TD-MPC2 (w/ test-time**<br>**regularization)**|**BMPC**|**BMPC (policy**<br>**only)**|**BMPC (w/ test-time**<br>**regularization)**|
|---|---|---|---|---|---|---|
|Acrobot Swingup|**595**_±_**34**|551_±_21|594_±_32|587_±_25|564_±_52|573_±_11|
|Cartpole Swingup Sparse|848_±_0|760_±_114|848_±_0|837_±_14|**848**_±_**1**|845_±_3|
|Fish Swim|786_±_8|645_±_83|783_±_13|804_±_17|**804**_±_**14**|776_±_9|
|Hopper Hop|**493**_±_**47**|383_±_154|465_±_79|404_±_39|445_±_106|440_±_87|
|Dog Run|358_±_228|89_±_52|376_±_231|678_±_27|670_±_13|**678**_±_**23**|
|Dog Walk|933_±_10|298_±_20|926_±_9|937_±_4|930_±_5|**940**_±_**4**|
|Humanoid Run|344_±_60|65_±_2|345_±_55|**528**_±_**29**|458_±_15|514_±_31|
|Humanoid Walk|899_±_10|142_±_36|881_±_9|917_±_6|930_±_7|**931**_±_**3**|
|**Mean**|657_±_225|367_±_247|652_±_221|711_±_181|706_±_187|**712**_±_**179**|


The results are the mean episode returns and standard deviations for three random seeds and ten test episodes. **Best** and second best results are highlighted. 

_Table 15._ **Meta-World evaluation results of different TD-MPC2 and BMPC variants.** 

|**Environment**|**TD-MPC2**|**TD-MPC2**<br>**(policy only)**|**TD-MPC2 (w/ test-time**<br>**regularization)**|**BMPC**|**BMPC (policy**<br>**only)**|**BMPC (w/ test-time**<br>**regularization)**|
|---|---|---|---|---|---|---|
|Assembly|1.0_±_0.0|1.0_±_0.0|0.67_±_0.47|1.0_±_0.0|1.0_±_0.0|**1.0**_±_**0.0**|
|Button Press|0.33_±_0.47|0.0_±_0.0|0.67_±_0.47|0.33_±_0.47|**1.0**_±_**0.0**|0.33_±_0.47|
|Disassemble|0.67_±_0.47|0.67_±_0.47|0.67_±_0.47|1.0_±_0.0|0.67_±_0.47|**1.0**_±_**0.0**|
|Lever Pull|0.0_±_0.0|0.0_±_0.0|0.0_±_0.0|0.67_±_0.47|**1.0**_±_**0.0**|0.67_±_0.47|
|Pick Place Wall|**1.0**_±_**0.0**|0.0_±_0.0|0.33_±_0.47|0.0_±_0.0|0.67_±_0.47|0.33_±_0.47|
|Push Back|0.67_±_0.47|0.33_±_0.47|**0.67**_±_**0.47**|0.33_±_0.47|0.33_±_0.47|0.33_±_0.47|
|Shelf Place|0.67_±_0.47|0.67_±_0.47|1.0_±_0.0|0.67_±_0.47|1.0_±_0.0|**1.0**_±_**0.0**|
|Window Open|1.0_±_0.0|0.33_±_0.47|1.0_±_0.0|0.67_±_0.47|**1.0**_±_**0.0**|0.67_±_0.47|
|**Mean**|0.67_±_0.33|0.38_±_0.35|0.62_±_0.31|0.58_±_0.32|**0.83**_±_**0.24**|0.67_±_0.29|


The results are the mean episode returns and standard deviations for three random seeds and ten test episodes. **Best** and second best results are highlighted. 

_Table 16._ **HumanoidBench evaluation results of different TD-MPC2 and BMPC variants.** 

|**Environment**|**TD-MPC2**|**TD-MPC2**<br>**(policy only)**|**TD-MPC2 (w/ test-time**<br>**regularization)**|**BMPC**|**BMPC (policy**<br>**only)**|**BMPC (w/ test-time**<br>**regularization)**|
|---|---|---|---|---|---|---|
|Balance Hard|92_±_12|34_±_3|**94**_±_**22**|81_±_12|78_±_8|80_±_9|
|Balance Simple|240_±_37|33_±_16|208_±_34|489_±_84|414_±_45|**778**_±_**77**|
|Hurdle|78_±_24|14_±_3|73_±_27|120_±_43|147_±_40|**175**_±_**51**|
|Maze|169_±_47|111_±_3|115_±_4|**349**_±_**2**|121_±_7|347_±_4|
|Reach|**5037**_±_**1436**|1558_±_368|399_±_208|4125_±_324|2117_±_309|2279_±_376|
|Run|136_±_110|8_±_4|99_±_72|139_±_81|91_±_25|**222**_±_**56**|
|Slide|237_±_54|14_±_2|248_±_77|442_±_36|250_±_26|**553**_±_**100**|
|Stair|100_±_18|24_±_8|91_±_23|403_±_145|208_±_46|**432**_±_**199**|
|**Mean**|761_±_1617|224_±_505|166_±_106|**769**_±_**1277**|428_±_646|608_±_665|


The results are the mean episode returns and standard deviations for three random seeds and ten test episodes. **Best** and second best results are highlighted. 

**— Appendices continue on next page —** 

21 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

## **D.4. Planner Sweep** 

Fig. 12 shows the performance of trained BMPC agents with Dream-MPC at test time when varying the number of candidates, horizon and number of optimization iterations. When varying one hyperparameter, the others are fixed to their default value. 


_Figure 12._ **Parameter sweep.** Performance of trained BMPC agents with Dream-MPC at test time when varying the number of candidates, horizon and number of optimization iterations. When varying one hyperparameter, the others are fixed to their default value. We also include the performance of the learned policy _πθ_ and the default values of one iteration, a horizon of three and five candidate trajectories. 

# **E. Integration into Dreamer** 

We further integrate our base method (without uncertainty regularization) into Dreamer (Hafner et al., 2020) to show that it also works with other model-based RL algorithms. Dreamer learns a latent dynamics model, often referred to as a world model, consisting of the following components: 

- Representation model: _pθ_ ( _st|st−_ 1 _, at−_ 1 _, ot_ ) 

- Transition model: _qθ_ ( _st|st−_ 1 _, at−_ 1) 

- Reward model: _qθ_ ( _rt|st_ ) 

- Observation model (only used as an additional learning signal): _qθ_ ( _ot|st_ ) 

All components are jointly optimized to increase the variational lower bound (ELBO), including reconstruction terms for observations and rewards as well as a KL regularizer: 


where 


22 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

The expected values are calculated based on the dataset and representation model. Please refer to Hafner et al. (2020) for the derivation of the variational bound. 

Following the original Dreamer implementation, we estimate state values using _Vλ_ , an exponentially-weighted average of the reward estimates for a different number of steps beyond the horizon with the learned value model to balance bias and variance: 


For each time step _t_ , Dream-MPC creates an initial sequence of actions by performing an imaginary rollout of the policy _πϕ_ and generates _N_ candidate trajectories adding small perturbations to the initial action sequence: 


The imaginary rollout is done by encoding observations and actions into latent space using the representation model _pθ_ and repeatedly calling the one-step transition model _qθ_ to generate a sequence of predicted states _{sτ }_<sup>_t_</sup> _τ_<sup>+</sup> =<sup>_H_</sup> _t_ +1<sup>+1for each candidate</sup> trajectory. 


We integrate our gradient-based MPC method into Dreamer as shown in Alg. 2. 

**Algorithm 2 Dream-MPC integration into Dreamer Input:** Representation model _pθ_ ( _st|st−_ 1 _, at−_ 1 _, ot_ ), transition model _qθ_ ( _st|st−_ 1 _, at−_ 1), reward model _qθ_ ( _rt|st_ ), value function model _vψ_ ( _st_ ), policy model _πϕ_ ( _at|st_ ), exploration noise _p_ ( _ϵ_ ), action repeat _R_ , seed episodes _S_ , collect interval _C_ , batch size _B_ , chunk length _L_ , learning rate _η_ Initialize dataset _D_ with _S_ random seed episodes. Initialize model parameters _θ, ϕ, ψ_ randomly. **while** not converged **do for** update step _s_ = 1 _..C_ **do** Draw sequences _{_ ( _ot, at, rt_ )<sup>_L_</sup> _t_ =<sup>+</sup> _k_<sup>_k}_</sup> _i_<sup>_B_</sup> =1<sup>_∼D_uniformly at random from the dataset.</sup> Compute loss _L_ ( _θ_ ) from Eq. (10). Update model parameters _θ ← θ − η∇θL_ ( _θ_ ). Imagine trajectories _{_ ( _sτ , aτ_ ) _}τ_<sup>_t_+</sup> =<sup>_H_</sup> _t_<sup>from each</sup><sup>_st_.</sup> Predict rewards E [ _qθ_ ( _rτ |sτ_ )] and values _vψ_ ( _sτ_ ). Compute value estimates _Vλ_ ( _sτ_ ) via Eq. (14). Update _ϕ ← ϕ_ + _η∇ϕ_ � _tτ_ += _Ht_<sup>_Vλ_(</sup><sup>_sτ_).</sup> Update _ψ ← ψ − η∇ψ_ � _tτ_ += _Ht_ <u>12</u><sup>_||vψ_(</sup><sup>_sτ_)</sup><sup>_−Vλ_(</sup><sup>_sτ_)</sup><sup>_||_2.</sup> **end for** _o_ 1 _←_ env.reset() **for** time step _t_ = 1 _.._ [ _R_<sup>_<u>T</u>_]</sup><sup>**do**</sup> Infer current state _st ∼ pθ_ ( _st|st−_ 1 _, at−_ 1 _, ot_ ) from the history. _at ←_ planner( _st_ ), see Alg. 3 for details. Add exploration noise _ϵ ∼ p_ ( _ϵ_ ) to the action. **for** action repeat _k_ = 1 _..R_ **do** _rt_<sup>_k, ok_</sup> _t_ +1<sup>_←_env.step(</sup><sup>_a_</sup> _t_<sup>)</sup> **end for** _rt, ot_ +1 _←_<sup>�</sup><sup>_R_</sup> _k_ =1<sup>_r_</sup> _t_<sup>_k, oR_</sup> _t_ +1 **end for** _D ←D ∪{_ ( _ot, at, rt_ )<sup>_T_</sup> _t_ =1<sup>_}_</sup> 

### **end while** 

23 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

## **Algorithm 3 Dream-MPC planner for Dreamer** 

**Input:** Representation model _pθ_ ( _st|st−_ 1 _, at−_ 1 _, ot_ ), transition model _qθ_ ( _st|st−_ 1 _, at−_ 1), reward model _qθ_ ( _rt|st_ ), value function model _vψ_ ( _st_ ), policy model _πϕ_ ( _at|st_ ), planning horizon _H_ , optimization iterations _I_ , candidates per iteration _J_ , action noise _σa_<sup>2, action</sup> optimization rate _α_ 


## **E.1. Experiments** 

We evaluate our method on four different environments from the DeepMind Control Suite and compare our method with PlaNet (Hafner et al., 2019), Dreamer (Hafner et al., 2020), SAC+AE (Yarats et al., 2021), a variant of the model-free Soft Actor Critic (SAC) (Haarnoja et al., 2018) algorithm for image-based observations and the Policy+Grad-MPC method proposed in (S V et al., 2023). Note that Policy+Grad-MPC and Dream-MPC both share the general idea of using a policy 


_Figure 13._ **Learning curves for four tasks from the DeepMind Control Suite.** The line represents the mean episodic return and the shaded area the 95% confidence interval across 3 seeds. 

network to warm-start gradient-based MPC. We provide a summary of the main differences in Section F. All experiments are performed with only RGB visual observations with a resolution of 64 _×_ 64. 

We evaluate the performance of our method when enabling planning already during training. The learning curves are shown in Fig. 13 and the evaluation results are presented in Tab. 3. We find that our method can not only outperform the baselines, but also that planning during training can improve the sample efficiency without leading to premature convergence. In contrast to PlaNet (CEM) and Grad-MPC, which both use 1000 _×_ 10 _×_ 12 = 120 000 evaluations of the world model at each time step, our method only requires 5 _×_ 1 _×_ 15 = 75 evaluations. These results are not only promising since Dreamer uses a recurrent dynamics model and a relatively long planning horizon, but also in particular for Acrobot Swingup, which is a non-linear system with chaotic dynamics. All aspects usually affect gradient quality negatively, especially since first order gradient estimators can accumulate significant variance over long-horizon rollouts, which makes them in particular ineffective in chaotic systems (Suh et al., 2022). 

We benchmark inference times of the different methods on a single Nvidia GeForce RTX 4090 GPU. The results in Tab. 17 show that Dream-MPC is significantly faster as Grad-MPC, which uses a much higher number of candidate trajectories. While Policy+Grad-MPC is faster than Dream-MPC due to using a horizon of one, the overall performance is worse compared to using the policy only because such a myopic optimization is most likely unsuitable for many problems. Note 

24 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

that at the moment a batched version of one operation in the recurrent world model is missing in PyTorch, which slows the parallelized gradient computation down. While this can potentially be further improved, it affects all gradient-based MPC methods in the same way, thus leading to a fair comparison. 

_Table 17._ **Inference times of different methods for Acrobot Swingup.** Mean and standard deviation for three random seeds and ten test episodes per seed. 

|**Method**|**Inference time**|
|---|---|
|PlaNet|31.10_±_0.65 ms|
|Grad-MPC|195.75_±_1.33 ms|
|Policy+Grad-MPC|23.16_±_0.55 ms|
|Dream-MPC (Dreamer)|44.86_±_0.60 ms|


## **E.2. Gradient Analysis** 

We evaluate the planner gradients of Grad-MPC and of our method for the ground truth dynamics (simulator) and the learned dynamics model for different planning horizons on the Pendulum-v1 environment with state observations. As Fig. 14 shows, the magnitudes of the gradients are in reasonable orders when using the ground truth dynamics. While the variance increases for longer horizons and might also do for more complex problems, the gradients do not explode or vanish in this case. However, the variance increases significantly for longer planning horizons when using the learned dynamics model. In contrast to Grad-MPC, the variance increases much less for Dream-MPC and although relatively large remains bounded, suggesting that the performance issues of gradient-based planning should not solely be attributed to issues with the gradients caused by the architecture of the world model. Our work shows that there are more aspects that need to be considered such as the quality of the initial proposal for MPC and the learned world model, advocating that further research on gradient-based planning is needed. 


_Figure 14._ **Planner gradients of Grad-MPC and Dream-MPC.** For different planning horizons on the Pendulum-v1 environment using the ground truth (simulator) and learned dynamics model respectively and state observations. The values are represented by their mean and standard deviation for three different random seeds. The default hyperparameters provided in Tab. 18 are used unless otherwise specified. 

As pointed out in Parmas et al. (2023), simply evaluating the gradient quality based on variance alone is insufficient. Thus, we follow the proposal of the authors and analyze the gradients using their Expected Signal-to-Noise Ratio (ESNR), which is defined as 


25 

### **Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 


_Figure 15._ **Expected Signal-to-Noise Ratio (ESNR) of the planner gradients of Grad-MPC and Dream-MPC.** Calculated via Eq. (17) for different planning horizons on the Pendulum-v1 environment using the ground truth (simulator) and learned dynamics model respectively and state observations. The values are represented by their mean and standard deviation for three different random seeds. The default hyperparameters provided in Tab. 18 are used unless otherwise specified. 

where _R_ =<sup>�</sup><sup>_t_</sup> _τ_<sup>+</sup> =<sup>_H_</sup> _t_ +1<sup>+1</sup><sup>_rτ_is the return, i.e., the undiscounted sum of rewards.</sup> 

Fig. 15 shows the ESNRs of Grad-MPC and Dream-MPC using the ground truth dynamics or learned dynamics model. While the ESNR remains stable when using the ground truth dynamics, especially for longer horizons the ESNR drops when using the learned model. Recent findings (Georgiev et al., 2025) suggest that learned models can improve ESNR compared to using the ground truth dynamics for some problems, indicating the possibility of further improvement. While the ESNR significantly suffers for horizons greater than ten for Grad-MPC using the learned dynamics model, the ESNR for Dream-MPC remains much more stable for increasing horizons. Together with the variance which increases but does not explode, this suggests that our method is more robust compared to Grad-MPC. 

## **E.3. Model Exploitation** 

We further analyze the problem of model exploitation, a general challenge in model-based reinforcement learning, where policies tend to exploit inaccuracies in high-capacity dynamics models, potentially leading to poor real-world performance despite high predicted returns (Clavera et al., 2018). Since our method optimizes actions to maximize expected returns, we rely on accurate predictions. Fig. 16 shows the mean difference between the actual returns and the predicted returns of a trained policy on the Acrobot Swingup task in for three different seeds and ten test episodes per seed. 

We find that the differences are quite small, which indicates that the policy may not exploit the learned model. This is probably because the prediction horizon is sufficiently short and MPC may also help to compensate for model inaccuracies by replanning at each step. While the models for other environments might not necessarily be as accurate as for Acrobot Swingup, we empirically find that the learned model tends to estimate the reward quite accurately. Using an ensemble of models to consider uncertainty as for TD-MPC2 can further help to reduce model exploitation. 

**— Appendices continue on next page —** 

26 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 


_(a)_ Mean difference between actual and predicted returns and standard deviation for three different seeds and ten test episodes per seed. 


_(b)_ Actual and predicted return for five exemplary evaluation episodes. 

_Figure 16._ **Analysis of predicted returns over the number of environment steps for Acrobot Swingup.** 

## **E.4. Implementation Details** 

We use PyTorch (Paszke et al., 2019) implementations of SAC+AE<sup>2</sup> , PlaNet and Dreamer<sup>3</sup> that are distributed under MIT license and also base the implementations of Grad-MPC and of our method on the latter. The hyperparameters are listed in Tab. 18. 

We use the default hyperparameters for SAC+AE as described in Yarats et al. (2021), except for the action repeat, which we set to two for a fair comparison. 

## **— Appendices continue on next page —** 

> 2https://github.com/denisyarats/pytorch_sac_ae 

> 3https://github.com/yusukeurakami/dreamer-pytorch 

27 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

_Table 18._ **Hyperparameters and their values used for the experiments.** 

|**Algorithm**|**Hyperparameter**|**Value**|
|---|---|---|
||Optimizer|Adam (Kingma & Ba, 2015)|
||Max. episode length|1000|
||Action repeat|2|
||Experience size|1000000|
||Embedding size|1024|
||Hidden size|200|
||Belief size|200|
||State size|30|
|All|Exploration noise|0.3|
||Seed episodes|5|
||Collect interval|100|
||Batch size|50|
||Overshooting distance|0|
||Overshooting KL beta|0|
||Overshooting reward scale|0|
||Global KL beta|0|
||Free nats|3|
||Bit depth|5|
|Dreamer & Dream-MPC|Planning horizon|15|
||Activation function|ReLU / ELU|
||Model learning rate|6e-4|
||Actor learning rate|8e-5|
|Dreamer Dream-MPC|Critic learning rate|8e-5|
|,<br>& Polic+Grad-MPC|Adam epsilon|1e-7|
|y|Grad clip norm|100|
||Discount factor|0.99|
||Horizon discount factor|0.95|
||Action optimization rate|0.1|
||Action noise|0.2|
|Dream-MPC|Action reuse coefficient|0.1|
||Candidates|5|
||Optimization iterations|1|
||Activation function|ReLU|
||Candidates|1000|
||Elite candidates|100|
|Grad-MPC & PlaNet|Optimization iterations|10|
||Grad clip norm|1000|
||Model learning rate|1e-3|
||Adam epsilon|1e-4|
||<br>Planning horizon|12|
|Grad-MPC|Action optimization rate|0.05|
||Action optimization rate|0.05|
|Policy+Grad-MPC|Optimization iterations|10|
||Planning horizon|1|


28 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

# **F. Summary of Differences to Policy+Grad-MPC** 

We summarize the main differences between Dream-MPC and the Policy+Grad-MPC method proposed in S V et al. (2023) as follows: 

- **Trajectory optimization.** While the general idea of using a policy to initialize gradient-based MPC is shared by both methods, there are important differences. Dream-MPC uses not just a single trajectory but samples few trajectories from the policy and optimizes each trajectory independently. Additionally, rollout and optimization is performed using longer horizons than just a horizon of one, which is used by Policy+Grad-MPC. While these values can be parameterized, they have a significant impact on the behavior and performance of the optimization. For example, using a horizon of one time step leads to a myopic optimization, which is unsuitable for most problems as outlined in Section E. Longer rollouts with learned world models are also more challenging due to imperfect models as shown in Section E.2. 

- **Uncertainty regularization.** We propose to incorporate uncertainty regularization into the MPC objective, which we find to be particularly important for high-dimensional problems. 

- **Action reuse.** We further propose to reuse previously optimized actions instead of completely discarding them to reduce the number of optimization iterations and improve computational efficiency. 

- **Extensive experiments and thorough ablations.** Grad-MPC (S V et al., 2023) provides only limited experimental results and lacks in-depth implementation details. While it shows that gradient-based MPC with a policy network is promising for two sparse-reward tasks from the DeepMind Control Suite, it does not provide a full evaluation of the method in diverse settings such as different benchmarks, different world models or types of observations, nor does it address high-dimensional problems, efficiency of gradient-based MPC or analyzes why the performance of gradientbased MPC is usually worse, compared to gradient-free methods. In contrast, Dream-MPC offers a comprehensive set of experiments that systematically analyze the performance of our method across a wide range of conditions, providing new insights into its applicability and efficiency to enable further research. 

- **Training with gradient-based MPC.** We also evaluate Dream-MPC when enabling gradient-based MPC already during training and not just during inference. In contrast, Policy+Grad-MPC is only evaluated using pretrained Dreamer models. Our results show that our method is also competitive to gradient-free MPC methods such as MPPI in this setting. In contrast, our experiments with Policy+Grad-MPC showed that it prematurely converges due to the horizon of just one time step. 

- **Different world models.** We integrate our method into different types of world models, i.e., Dreamer (generative) and TD-MPC2 (implicit, control-centric) to show that our method is not targeted to a specific world model architecture while Policy+Grad-MPC only evaluates their method using Dreamer. 

- **Implementation.** Furthermore, we were not able to reproduce the results shown in S V et al. (2023) with the given information because it lacks in-depth implementation details and there is no official implementation available. In contrast, we provide implementation details and open-source our implementation so that future work can replicate and build upon. 

**— Appendices continue on next page —** 

29 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

# **G. Analysis of Dream-MPC’s Performance on Dog Run** 

As shown in Fig. 4, Dream-MPC (TD-MPC2) achieves a lower asymptotic performance when using gradient-based MPC during training compared to BMPC or TD-MPC2 for high-dimensional problems, such as Dog Run. To understand why Dream-MPC performs worse than MPPI for Dog Run when being used during training, we empirically analyze the quality of the used TD-MPC2/BMPC world model for Dog Run and how it affects overall performance of MPC. 

## **G.1. Value Estimation** 

Recent work (Lin et al., 2026) has shown that TD-MPC2 suffers from value overestimation, particularly for high-dimensional tasks. The reasons are attributed to a policy mismatch: since the actions optimized by MPC are used to interact with the environment, the resulting training distribution corresponds to the MPC policy rather than that of the policy prior network. We follow the approach proposed by the authors and estimate values using the average discounted return for 100 evaluation episodes. The value approximation errors for BMPC, TD-MPC2 and Dream-MPC (TD-MPC2) are shown in Fig. 17. For BMPC, we use five Q-networks in all following experiments instead of two V-networks to isolate potential confounding effects arising from using V-networks instead. 


_Figure 17._ **Value estimations for Dog Run.** The lines represent the mean values and the shaded areas the 95% confidence interval across 3 seeds. 

Similar to Lin et al. (2026), we find that for high-dimensional problems, such as Dog Run, TD-MPC2 tends to overestimate the values, although the gap is in our case smaller and also changes from an overestimation in the beginning to an underestimation at the end of the training. While this suggests that the underlying mechanisms might be more complex than a systematic overestimation and that further research on this is required, it emphasizes that in general calibrated value estimates are needed for policy learning and MPC. 

The bootstrapping mechanism of BMPC mitigates the distribution mismatch, which is indicated by lower value estimation errors and improved training stability. While the value estimation errors for TD-MPC2 without MPC are also small, the overall performance is worse and suggests that the value function has not seen state-action pairs, which would lead to a high reward. We discuss this in more detail in Section G.2. While gradient-based MPC constrains the policy mismatch by staying closer to the nominal policy distribution, it is prone to local optima, which can impair asymptotic performance, especially for high-dimensional problems. 

Next, we want to evaluate how much value estimation errors affect the overall performance during inference. Fig. 18 shows the connections between the episode return _G_ and the estimated absolute value approximation error _eq_ (Fig. 18a), between _G_ and the episode mean variance of the predicted Q-values _q_ ˆstd (Fig. 18b) as well as between _q_ ˆstd and _eq_ (Fig. 18c), respectively. Errors are binned into quartiles. We find that regardless of whether the policy, MPPI or gradient-based MPC is used, a lower episode return corresponds to a higher absolute value error. This is also reflected by the Spearman correlation coefficients reported in Tab. 19 and emphasizes that accurate value estimates are in general important for all considered methods. 

We further find that there is a connection between the episode return and the variance of the predicted Q-values _q_ ˆstd as shown in Fig. 18b and by the Spearman coefficients. This indicates that episodes with a higher critic ensemble disagreement have much lower returns, suggesting that uncertainty is a good indicator for poor performance. Furthermore, there is a weaker correlation between _q_ ˆstd and _eq_ , which suggests that higher uncertainty also tends to be accompanied by larger value estimation errors. Although the correlation is not as strong as for the return, this indicates that uncertainty is meaningfully aligned with value function errors, and also confirms empirically the importance of taking uncertainty into account. 

30 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

_Table 19._ **Spearman correlation coefficients for Dog Run using BMPC with 5 Q-networks.** We omit p-values since they are all much smaller than 0.05. 

|**Method**|**Metric**|**Outcome**|**Spearman Coefficient**|
|---|---|---|---|
||ˆ_q_std|_G_|-0.93|
|Policy|_eq_|_G_|-0.74|
||ˆ_q_std|_eq_|0.68|
||ˆ_q_std|_G_|-0.88|
|MPPI|_eq_|_G_|-0.66|
||ˆ_q_std|_eq_|0.68|
||ˆ_q_std|_G_|-0.80|
|Dream-MPC|_eq_|_G_|-0.59|
||ˆ_q_std|_eq_|0.46|


_Figure 18._ **Effects of value approximation errors.** Analysis for BMPC on Dog Run. (a) Absolute value error vs. episode return. (b) Mean variance of predicted Q-values vs. episode return. (c) Mean variance of predicted Q-values vs. absolute value error. 

31 

**Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination** 

While correlations are consistent when using the policy only, with MPPI and with gradient-based MPC, their strength varies. There is a trend suggesting that the correlations are slightly weaker with MPC, and gradient-based MPC showing even weaker correlations than MPPI. We hypothesize that the replanning of MPC allows for mitigating errors and that gradient-based MPC is less affected from model errors since the actions are closer to the nominal policy actions, which reduces the chance of out-of-distribution queries of the world model. This property makes gradient-based MPC potentially promising for offline RL, where the state-action coverage is limited. 

## **G.2. Policy Mismatch** 

We further perform an experiment, where we analyze and compare the estimated values of BMPC with TD-MPC2. First, we use the much stronger policy of BMPC to evaluate whether the Q-networks of TD-MPC2, which was trained without MPC, can accurately estimate the values for good actions, although they have potentially not been seen or explored during training. 

We find that BMPC slightly overestimates the values as shown in Fig. 19, but is quite accurate for trajectories corresponding to higher returns. TD-MPC2 trained without MPC in contrast significantly underestimates the values and basically predicts the same value for all episodes, indicating that the model has not seen state-action pairs leading to higher returns during training. 

Next, we repeat this experiment, but use TD-MPC2, which was trained with MPPI to analyze whether the sampling-based MPC leads to improved exploration that helps to correct wrong value estimates. While TD-MPC2 still underestimates the values, the errors are much smaller, and it is specifically quite accurate for regions corresponding to lower returns. This suggests that sampling-based MPC can help to partially mitigate value approximation errors due to improved exploration during training and further highlights the importance of the policy and value functions being aligned to each other. Even if we have a well-performing policy, the world model needs to provide accurate predictions for the actions from the policy. 

MPPI as a sampling-based MPC method benefits from a higher diversity across the candidate solution, which encourages exploration and thus improves training stability. The MPPI planner used in TD-MPC2 and BMPC uses a large number of random samples in addition to the policy prior samples, which help to explore underestimated or uncovered regions. Gradient-based MPC in contrast is prone to converging to local optima. Nevertheless, Dream-MPC performs surprisingly well and at least slightly improves compared to using only the policy prior, but is not able to match the performance of MPPI for high-dimensional problems when used during training. BMPC achieves the best performance, potentially because of a correction of the policy mismatch due to the bootstrapping mechanism in combination with carefully made design decisions to avoid premature convergence to local optima. BMPC adds an entropy loss to the policy learning objective and adds exploration in its lazy reanalyze mechanism to avoid premature convergence to local optima. We believe that this can potentially also help to further improve gradient-based MPC, but leave this for future work. 


_Figure 19._ **Value estimation comparison for BMPC policy on Dog Run.** 

32 

