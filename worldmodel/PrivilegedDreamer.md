---
title: "PrivilegedDreamer: Explicit Imagination of Privileged Information for Rapid Adaptation of Learned Policies"
date: "2025-02-17"
authors: "Morgan Byrd; Jackson Crandell; Mili Das; Jessica Inman; Robert Wright; Sehoon Ha"
url: https://arxiv.org/abs/2502.11377
pdf: https://arxiv.org/pdf/2502.11377
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2502.11377)** / [論文ページ](https://arxiv.org/abs/2502.11377)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **PrivilegedDreamer: Explicit Imagination of Privileged Information for Rapid Adaptation of Learned Policies** 

Morgan Byrd<sup>1</sup><sup>_∗_</sup> , Jackson Crandell<sup>1</sup> , Mili Das<sup>1</sup> , Jessica Inman<sup>2</sup> , Robert Wright<sup>2</sup> , and Sehoon Ha<sup>1</sup> 

**_Abstract_ — Numerous real-world control problems involve dynamics and objectives affected by unobservable hidden parameters, ranging from autonomous driving to robotic manipulation, which cause performance degradation during sim-to-real transfer. To represent these kinds of domains, we adopt hiddenparameter Markov decision processes (HIP-MDPs), which model sequential decision problems where hidden variables parameterize transition and reward functions. Existing approaches, such as domain randomization, domain adaptation, and meta-learning, simply treat the effect of hidden parameters as additional variance and often struggle to effectively handle HIP-MDP problems, especially when the rewards are parameterized by hidden variables. We introduce PrivilegedDreamer, a model-based reinforcement learning framework that extends the existing model-based approach by incorporating an explicit parameter estimation module. PrivilegedDreamer features its novel dual recurrent architecture that explicitly estimates hidden parameters from limited historical data and enables us to condition the model, actor, and critic networks on these estimated parameters. Our empirical analysis on five diverse HIP-MDP tasks demonstrates that PrivilegedDreamer outperforms state-of-the-art model-based, model-free, and domain adaptation learning algorithms. Additionally, we conduct ablation studies to justify the inclusion of each component in the proposed architecture.** 

## I. INTRODUCTION 

Markov decision processes (MDPs) have been powerful mathematical frameworks for modeling a spectrum of sequential decision scenarios, from computer games to intricate autonomous driving systems; however, they often assume fixed transition or reward functions. In many real-world domains, there exist hidden-parameter MDPs (HIP-MDPs) [1] that are characterized by the presence of hidden or uncertain parameters playing significant roles in their dynamics or reward functions. For instance, autonomous driving must handle diverse vehicles with distinctive dynamic attributes and properties to achieve a better driving experience, while the agricultural industry must account for variations in produce weight for sorting. Consequently, research endeavors have explored diverse approaches, including domain randomization [2], domain adaptation [3], and meta-learning [4], to address these challenges effectively. 

We approach these HIP-MDP problems using modelbased reinforcement learning because a world model holds significant promise in efficiently capturing dynamic behaviors characterized by hidden parameters, ultimately resulting 

> This work was supported by the GTRI Graduate Student Researcher Fellowship Program and NSF Award No. 2339076 

> 1Georgia Institute of Technology, Atlanta, GA, 30308, USA 

> 2Georgia Tech Research Institute, Atlanta, GA, 30308, USA 

> *Correspondence to abyrd45@gatech.edu 

in improved policy learning. Particularly, we establish our framework based on Dreamer [5], which has been effective in solving multiple classes of problems, including DeepMind Control Suite [6], Atari [7], and robotic control [8]. Our initial hypothesis was that the Dreamer framework could capture parameterized dynamics accurately by conditioning the model on latent variables, leading to better performance at the end of learning. However, Dreamer is designed to predict action-conditioned dynamics in the observation space and does not consider the effect of hidden parameters. 

This paper presents PrivilegedDreamer to solve HIPMDPs via explicit prediction of hidden parameters. Our key intuition is that a recurrent state-space model (RSSM) of model-based RL must be explicitly conditioned on hidden parameters to capture the subtle changes in dynamics or rewards. However, a HIP-MDP assumes that hidden variables are not available to agents. Therefore, we introduce an explicit module to estimate hidden parameters from a history of state variables via a long short-term memory (LSTM) network, which can be effectively trained by minimizing an additional reconstruction loss. This dual recurrent architecture allows accurate estimation of hidden parameters from a short amount of history. The estimated hidden parameters are also fed into the transition model, actor, and critic networks to condition their adaptive behaviors on these hidden parameters. 

We evaluate our method in five HIP-MDP environments, two of which also have hidden-parameter-conditioned reward functions. We compare our method against several state-of-the-art baselines, including model-based (DreamerV2 [7]), model-free (Soft Actor Critic [9] and Proximal Policy Optimization [10]), and domain adaptation (Rapid Motor Adaptation [11]) algorithms. Our PrivilegedDreamer achieves a 41% higher average reward over these five tasks and demonstrates remarkably better performance on the HIP-MDPs with parameterized reward functions. We further analyze the behaviors of the learned policies to investigate how rapid estimation of hidden parameters affects the final performance and also to justify the design decisions of the framework. Finally, we outline a few interesting future research directions. 

## II. RELATED WORK 

## _A. World Models_ 

Model-based RL improves sample efficiency over modelfree RL by learning an approximate model for the transition dynamics of the environment, allowing for policy training 

without interacting with the environment itself. However, obtaining accurate world models is not straightforward because the learned model can easily accumulate errors exponentially over time. To alleviate this issue, [12] designs ensembles of stochastic dynamics models to attempt to incorporate uncertainty. The Dreamer architecture [5], [7], [13] learns a model of the environment via reconstructing the input from a latent space using the recurrent state-space model (RSSM). The RSSM incorporates the Gated Recurrent Unit (GRU) network [14] and the Variational Autoencoder (VAE) [15] for modeling. With this generative world model, the policy is trained with imagined trajectories in this learned latent space. [16] and [17] leverage the Transformer architecture [18] to autoregressively model the world dynamics and similarly train the policy in latent imagination. Our work is built on top of the Dreamer architecture, but the idea of explicit modeling of hidden parameters has the potential to be combined with other architectures. 

## _B. Randomized Approaches without Explicit Modeling_ 

One of the most popular approaches to deal with uncertain or parameterized dynamics is domain randomization (DR), which aims to improve the robustness of a policy by exposing the agent to randomized environments. It has been effective in many applications, including manipulation [19], [2], [20], [21], locomotion [3], [22], autonomous driving [23], and indoor drone flying [24]. Domain randomization has also shown great success in deploying trained policies on actual robots, such as performing sim-to-real transfer for a quadrupedal robot in [22] and improving performance for a robotic manipulator in [19]. [25] and [26] both incorporate DR for increased robustness in a world model setting. While DR is highly effective in many situations, it tends to lead to an overly conservative policy that is suboptimal for challenging problems with a wide range of transition or reward functions. 

## _C. Domain Adaptation_ 

Since incorporating additional observations is often beneficial [27], another common strategy for dealing with variable environments is to incorporate the hidden environmental parameters into the policy for adaptation. This privileged information of the hidden parameters can be exploited during training, but at test time, system identification must occur online. For model-free RL, researchers typically train a universal policy conditioned on hidden parameters and estimate them at test time by identifying directly from a history of observations [28], [11], [29]. Another option is to improve state estimation while training in diverse environments, which similarly allows for adaptation without needing to perform explicit system identification [30]. For model-based RL, the problem of handling variable physics conditions is handled in multiple ways. A few research groups [31], [32] propose using meta-learning to rapidly adapt to environmental changes online. [33] uses a graph-based meta RL technique to handle changing dynamics. [34] used data augmentation in offline RL to get zero-shot dynamics generalization. The most 

applicable methods for our work are those that use a learned encoder to estimate a context vector that attempts to capture the environmental information. Then, this context vector is used for conditioning the policy and forward prediction, as in [35], [36], [37], [38]. 

## III. PRIVILEGEDDREAMER: ADAPTATION VIA EXPLICIT IMAGINATION 

## _A. Background_ 

_1) Hidden-parameter MDP:_ A Markov decision process (MDP) formalizes a sequential decision problem, which is defined as a tuple ( _S, A, T, R, p_ 0), where _S_ is the state space, _A_ is the action space, _T_ is the transition function, _R_ is the reward function, and _p_ 0 is the initial state distribution. For our work, we consider the hidden-parameter MDP (HIP-MDP), which generalizes the MDP by conditioning the transition function _T_ and/or the reward function _R_ on an additional hidden latent variable _ω_ sampled from a distribution _pω_ [1]. Without losing generality, _ω_ can be a scalar or a vector. In the setting of continuous control, which is the primary focus of this work, this latent variable represents physical quantities, such as mass or friction, that govern the dynamics but are not observable in the state space. 

_2) Dreamer:_ For our model, we build upon the DreamerV2 model of [7]. DreamerV2 uses a recurrent state-space model (RSSM) to model dynamics and rewards. This RSSM takes as input the state _xt_ and the action _at_ to compute a deterministic recurrent state _ht_ = _fφ_ ( _ht−_ 1 _, zt−_ 1 _, at−_ 1) using a GRU _fφ_ and a sampled stochastic state _zt ∼ qφ_ ( _zt |ht , xt_ ) using an encoder _qφ_ . The transition predictor _z_ ˆ _t ∼ pφ_ ( _z_ ˆ _t |ht_ ) computes an estimate _z_ ˆ _t_ of the stochastic state using only the deterministic state _ht_ , which is necessary during training in imagination as _xt_ is not available. The combination of the deterministic and stochastic states is used as a representation to reconstruct the state _x_ ˆ _t ∼ pφ_ ( _x_ ˆ _t |ht , zt_ ), predict the reward _r_ ˆ _t ∼ pφ_ ( _r_ ˆ _t |ht , zt_ ), and predict the discount factor _γ_ ˆ _t ∼ pφ_ ( _γ_ ˆ _t |ht , zt_ ). 

For policy learning, Dreamer adopts an actor-critic network, which is trained via imagined rollouts. For each imagination step _t_ , the latent variable _z_ ˆ _t_ is predicted using only the world model, the action is sampled from the stochastic actor: _at ∼ πθ_ ( _at |z_ ˆ _t_ ), and the value function is estimated as: _vψ ≈_ E _pφ ,pθ_ [∑ _γ_<sup>_τ−t_</sup> _r_ ˆ _τ_ ], where _r_ ˆ _t_ is computed from the reward predictor above. The actor is trained to maximize predicted discounted rewards over a fixed time horizon _H_ . The critic aims to accurately predict the value from a given latent state. The actor and critic losses are: 


_B. Algorithm_ 

While the original DreamerV2 layout works effectively for many tasks, it falters in the HIP-MDP domain, especially 

in the case where the reward explicitly depends on the hidden latent variable. Even though the RSSM has memory to determine the underlying dynamics, prior works, such as [38], have shown that this hidden state information is poorly captured implicitly and must be learned explicitly. 

_1) Explicit Imagination via LSTM:_ To improve the estimation of hidden parameters, we incorporate an additional independent module for estimating the privileged information from the available state information. This dual recurrent architecture allows us to effectively estimate the important hidden parameters in the first layer and model other variables conditioned on this estimation in the second layer. Our estimation module _ω_ ˜ _t ∼ ηφ_ ( _ω_ ˜ _t |xt , at−_ 1) takes the state _xt_ and previous action _at−_ 1 as inputs and predicts the intermediate hidden parameter _ω_ ˜ _t_ . It is still parameterized by _φ_ because we treat it as part of the world model. The estimation module is comprised of an LSTM [39] followed by MLP layers that reshape the output to that of the privileged data. We use an LSTM because its recurrent architecture is more suitable to model subtle and non-linear relationships between state and hidden variables over time. However, the choice of the architecture was not significant to the performance. In our experience, LSTM and GRU demonstrated similar performance. 

Note that we use _ω_ ˜ _t_ to make the recurrent world model conditioned on the estimated hidden variable. For the actor and critic, we feed the value from the prediction head, _ω_ ˆ _t_ , which will be described in the next paragraph. 

_2) Improving Accuracy via Additional Prediction Head:_ We also added an additional prediction head _pφ_ ( _ω_ ˆ _t |ht , zt_ ), which is similar to the reward or state prediction heads. While the previous LSTM estimation _η_ predicts the intermediate parameter _ω_ ˜ _t_ to make the model conditioned on the hidden parameter, this additional prediction head offers two major improvements: 1) encouraging the RSSM state variables _ht_ and _zt_ to contain enough information about the hidden parameter and 2) improving the prediction accuracy. 

_3) Hidden Variable Loss:_ We design an additional loss to train the estimation module, which is similar to the other losses of the DreamerV2 architecture. We do not use the discount predictor from the original DreamerV2 architecture as all of our tests are done in environments with no early termination. We group the other Dreamer losses all under _LDreamer_ to highlight our differences. This makes the total loss for the world model: 


where the first additional loss term is to compute an intermediate estimate _ω_ ˜ for the hidden parameter _ω_ using the environment states _x_ and actions _a_ and the second term is the world model reconstruction loss for _ω_ ˆ based on the RSSM latent variables _h_ and _z_ . 

It is important to highlight that relying solely on this hidden parameter loss term is not sufficient. Theoretically, it 


Fig. 1: Architecture of PrivilegedDreamer. Compared to the default DreamerV2 model ( **top** ), our architecture ( **bottom** ) adopts an explicit parameter estimation model _η_ to predict the hidden parameters _ωt_ from a history of states. Then, the estimated parameters _ω_ ˜ _t_ are fed into the model to establish the explicit dependency. 

seems like the loss encourages the recurrent state variables _ht_ and _zt_ to encapsulate all relevant information and increase all the model, actor, and critic networks’ awareness of hidden parameters. However, in practice, this privileged information remains somewhat indirect to those networks. Consequently, this indirect access hinders their ability to capture subtle changes and results in suboptimal performance. 

_4) Hidden-parameter Conditioned Networks (ConditionedNet):_ Once we obtain the estimate of the hidden parameter _ωt_ , we feed this information to the networks. This idea of explicit connection has been suggested in different works in reinforcement learning, such as rapid motor adaptation (RMA) [11] or meta strategy optimization (MSO) [40]. Similarly, we augment the inputs of the representation model _zt_ , the critic network _vψ_ , and the actor network _πθ_ to encourage them to incorporate the estimated _ω_ ˜ _t_ and _ω_ ˆ _t_ . 

_5) Additional Proprioceptive State as Inputs:_ In our experience, it is beneficial to provide the estimated state information as additional inputs to the actor and critic networks. We hypothesize that this may be because the most recent state information _xt_ is highly relevant for our continuous control tasks. On the other hand, the RSSM states _ht_ and _zt_ are indirect and more suitable for establishing long-term plans. _6) Summary:_ On top of DreamerV2, Our PrivilegedDreamer includes the following components: 

Recurrent hidden parameter predictor: _ω_ ˜ _t ∼ ηφ_ ( _ω_ ˜ _t |ht , zt_ ) HIP-conditioned representation model: _zt ∼ qφ_ ( _zt |ht , xt , ω_ ˜ _t_ ) HIP prediction head: _ω_ ˆ _t ∼ pφ_ ( _ω_ ˆ _t |ht , zt_ ) HIP-conditioned critic: _vt ∼ vψ_ ( _vt |ht , zt , xt , ω_ ˆ _t_ ) HIP-conditioned actor: _a_ ˆ _t ∼ πθ_ ( _at |ht , zt , xt , ω_ ˆ _t_ ) 

We omit the unchanged components from DreamerV2, such as input and reward predictors, for brevity. A schematic 


Walker 


Pendulum 


Throwing 


Kuka Sorting Pointmass 

Fig. 2: Five HIP-MDP tasks used in our experiments. 

of the model architecture used for training the world model itself can be seen in Fig. 1. This setup trains the encoder network, decoder network, and the latent feature components _z_ and _h_ . The estimation module _η_ that initially estimates the value of _ω_ ˜ _t_ is also trained here. 

When training the policy, we start with a seed state sampled from the replay buffer and then proceed in imagination only, as in the original DreamerV2. Via this setup, the actor and critic networks are trained to maximize the estimated discounted sum of rewards in imagination using a fixed world model. 

However, the key difference from DreamerV2 is that both the actor and critic networks take the estimated parameter _ω_ ˆ _t_ from the prediction head as an additional input, as well as the reconstructed state _x_ ˆ _t_ . Because learning the parameter estimation is much faster than learning the world model, this new connection works almost the same as providing the groundtruth hidden parameter for the majority of the learning time. We will examine this behavior in the discussion section. 

## IV. EXPERIMENTS 

We evaluate PrivilegedDreamer on several HIP-MDP problems to answer the following research questions: 

- 1) Can our PrivilegedDreamer solve HIP-MDP problems more effectively than the baseline RL and domain adaptation algorithms? 

- 2) Can the estimation network accurately find groundtruth hidden parameters? 

- 3) What are the impacts of the HIP reconstruction loss and HIP-conditioned policy? 

## _A. HIP-MDP Tasks_ 

We evaluate our model on a variety of continuous control tasks from the DeepMind Control (DMC) Suite [6], along with some tasks developed in MuJoCo [41]. All tasks involve operating in a continuous control environment with varying physics. The tasks are as follows: 

- DMC Walker Run - Make the Walker run as fast as possible in 2D, where the contact friction is variable. 

- DMC Pendulum Swingup - Swing a pendulum to an upright position, where the pendulum mass is variable. 

- Throwing - Control a paddle to throw a ball into a goal, where the ball mass is variable. 

- Kuka Sorting - Move an object to a desired location using a Kuka Iiwa manipulator arm, where the object 

mass is variable and the target location depends on the mass: heavier objects to the left and lighter objects to the right. The target trajectory is defined via the RL policy and is tracked by the Kuka arm using operational space control [42]. 

- DMC Pointmass - Move the point mass to the target location, where the x and y motors are randomly scaled. The target location depends on the motor scaling: away from the center for high motor scaling and towards the center for lower motor scaling. 

When we design these tasks, we start by simply introducing randomization to the existing two tasks, DMC Walker Run and DMC Pendulum Swingup. Then, we purposely design the last two tasks, Kuka Sorting and DMC Pointmass, to incorporate a reward function that depends on their hidden parameters. Throwing also implicitly necessitates a policy for identifying the ball’s mass and adjusting its trajectory. However, its reward function is not explicitly parameterized. 

All the environments are visualized in Fig. 2 and their randomization ranges are summarized in Table I. 

## _B. Baseline Algorithms_ 

The baseline algorithms that we compare against are as follows: 

- DreamerV2 : original DreamerV2 model proposed by [7]. 

- Proximal Policy Optimization (PPO): model-free, onpolicy learning algorithm proposed by [10] using the implementation from [43]. 

- Soft Actor Critic (SAC): model-free, off-policy learning algorithm proposed by [9] using the implementation from [44]. 

- Rapid Motor Adaptation (RMA): model-free domain adaptation algorithm proposed by [11], which estimates hidden parameters from a history of states and actions. We train an expert PPO policy with _ω_ as input and compare to the student RMA policy, which is trained with supervised learning to match _ω_ using a history of previous states. 

We selected our baselines to cover all the state-of-theart in model-based/model-free, on-policy/off-policy, and domain randomization/adaptation algorithms. All models were trained for 2 million timesteps in each environment randomized as specified in Table I. 

|**Task**|**Physics Randomization Target**|**Range**|**Reward**|
|---|---|---|---|
|Walker Run|Contact Friction|[0.05 - 4.5]|Fixed|
|Pendulum Swingup|Mass Scaling Factor of Pendulum|[0.1 - 2.0]|Fixed|
|Throwing|Mass Scaling Factor of Ball|[0.2 - 1.0]|Fixed|
|Kuka Sorting|Mass Scaling Factor of Object|[0.2 - 1.0]|Parameterized|
|Pointmass|X/Y Motor Scaling Factor|X [1 - 2]<br>Y [1 - 2]|Parameterized|


TABLE I: Parameter randomization applied for each task. 

|**Method**|**Walker**|**Pendulum**|**Throwing**|**So**|**rting**|**Pointmass**|**Mean**|
|---|---|---|---|---|---|---|---|
|PrivilegedDreamer|**766.20** _±_ **20.19**|**563.14** _±_ **147.44**|788.59 _±_ 45.66|**554.65**|_±_ **26.25**|**670.23** _±_ **13.93**|**668.56** _±_ **70.87**|
|DreamerV2 + Decoder + ConditionedNet|576.89 _±_ 96.68|329.80 _±_ 37.10|785.78 _±_ 64.18|180.85|_±_ 46.55|492.77 _±_ 17.82|473.22 _±_ 58.87|
|DreamerV2 + Decoder|671.85 _±_ 10.46|259.84 _±_ 26.08|707.51 _±_ 20.63|87.74|_±_ 43.24|480.96 _±_ 29.91|441.58 _±_ 28.21|
|DreamerV2 [7]|715.57 _±_ 39.95|289.43 _±_ 214.12|706.09 _±_ 26.24|167.61|_±_ 33.38|488.41 _±_ 3.60|473.42 _±_ 99.26|
|SAC [9]|475.22 _±_ 13.02|454.67 _±_ 268.98|**945.65** _±_ **17.02**|74.85|_±_ 88.03|393.49 _±_ 210.47|468.78 _±_ 158.03|
|PPO [10]|79.73<br>_±_ 10.95|470.04 _±_ 324.05|707.03 _±_ 115.63|229.93|_±_ 181.12|545.86 _±_ 72.22|406.52 _±_ 176.93|
|RMA [11]|75.28<br>_±_ 11.31|516.83 _±_ 386.43|624.57 _±_ 118.70|82.33|_±_ 416.57|545.31 _±_ 357.86|368.86 _±_ 305.00|


TABLE II: Model performance after 2 million timesteps of training. Our PrivilegedDreamer achieves better results particularly in the HIP-MDP problems with parameterized rewards, Kuka Sorting and Pointmass. 


Fig. 3: Learning curves for all tasks. PrivilegedDreamer shows the best performance against all the baseline algorithms, except for the throwing task which requires a very long horizon prediction. 

To validate our design choices, we further evaluate the following intermediate versions of the algorithm. 

- Dreamer + Decoder: This version only trains a decoder _ω_ ˆ _t ∼ pφ_ ( _ω_ ˆ _t |ht , zt_ ) by minimizing the hidden variable loss without an estimation module _η_ . Also, _ω_ ˆ _t_ is not provided to the actor and critic and _ht_ and _zt_ are expected to contain all the information about the hidden parameter _ωt_ . 

- Dreamer + Decoder + ConditionedNet: This version is similar to the previous Dreamer + Decoder, but the estimated _ω_ ˆ _t_ is given to the actor and critic networks. 

Note that the proposed PrivilegedDreamer can be viewed as the combination of Dreamer, an external estimation module, 

and conditioned networks trained with the hidden variable loss (PrivilegedDreamer = Dreamer + ExternalEstimation + Decoder + ConditionedNet). 

## _C. Evaluation_ 

_a) Performance:_ To evaluate the effectiveness of the proposed method, we first compare the learning curves and the final performance of all the learned models. Learning curves for all models are shown in Figure 3, where the means and standard deviations are computed over three random seeds. Since RMA is trained in a supervised fashion using an expert policy and is not trained using on-policy environment interactions, we do not have a comparable learning curve, so we display the average performance as a horizontal line for comparison. Table II shows the average reward over 100 runs for each seed. We also report the average performance over five tasks in both Figure 3 and Table II. 

Overall, the proposed PrivilegedDreamer achieves the best average reward over five tasks. It shows a significant performance improvement over the second best model, vanilla DreamerV2, in both standard DeepMind Control Suite tasks (Walker, Pointmass, Pendulum) as well as tasks we created ourselves (Sorting, Throwing). Performance margins are generally larger in the Sorting and DMC Pointmass tasks, where PrivilegedDreamer is the **only model** tested that does appreciably better than random. This is likely because the reward for these tasks explicitly depends on _ω_ and DreamerV2 only implicitly adapts its behaviors to the hidden parameters. This indicates that the novel architecture of PrivilegedDreamer is effective for solving HIP-MDPs, particularly when the reward function is parameterized. We suspect that RMA and PPO do especially poorly on the Walker task because the 2 million timestep training limit is insufficient for on-policy algorithms. Similarly, we suspect that the small training size affects the ability of RMA to effectively adapt, and that it would be more competitive with our method with a larger training dataset, which our method does not need due to its better sample efficiency. 


Fig. 4: Hidden parameter reconstruction error during learning. PrivilegedDreamer shows the best accuracy. 

One notable outlier is the great performance of SAC on the Throwing task. We suspect that the nature of the problem makes it difficult for model-based RL algorithms, both PrivilegedDreamer and DreamerV2. Moreover, in this task, a policy only has a few steps to estimate its hidden parameters and predict the ball’s trajectory, which can easily accumulate model errors over a long time horizon. On the other hand, SAC, a model-free RL algorithm, efficiently modifies its behaviors in a model-free fashion without estimating a ball trajectory. The on-policy model-free algorithms, PPO and RMA, are not sample-efficient enough to achieve good performance within two million steps. 

_b) Hidden Parameter Estimation:_ PrivilegedDreamer is based on the assumption that estimating hidden parameters is crucial for solving HIP-MDPs. Fig. 4 and Fig. 5 show the effectiveness of our model in reconstructing the hidden parameters and estimating them online. Fig. 4 illustrates the reconstruction errors during the learning process for the Pendulum, Throwing, and Pointmass tasks. In all cases, our PrivilegedDreamer exhibits faster convergence, typically within less than 0 _._ 5 million environmental steps, resulting in more consistent learning curves. Additionally, Fig. 5 displays the real-time estimation of hidden parameters during episodes. Our model accurately predicts these parameters within just a few steps, enhancing the performance of the final policies. These findings justify the effectiveness of an external LSTM-based hidden-parameter estimation module. 

## _D. Ablation Studies_ 

Comparing our full PrivilegedDreamer model to the ablations, we see that our model is superior and each component is necessary for optimal performance. From Fig. 4, we see that our full model is significantly better at reconstructing the hidden variable _ω_ than Dreamer + Decoder + ConditionedNet, which is already better than Dreamer + Decoder. With this low reconstruction error, online estimation of _ω_ is very effective, as shown in Fig. 5, which shows that our method rapidly converges within 5% of the real value, while the ablated versions take longer to converge to a lower quality estimate. Specifically, our agents find near-correct hidden parameters at the beginning of the episodes within a few environmental steps in all scenarios, while the other baselines take more than 500 steps (Dreamer+Decoder+ConditionedNet in Pointmass) or converge to wrong values (Dreamer+Decoder in Pendulum and Pointmass). Using this high quality estimate of _ω_ within our 


Fig. 5: Online parameter estimation within an episode. The two estimated values for the Pointmass model are shown in separate plots to improve readability. PrivilegedDreamer was able to estimate hidden parameters more effectively than the other baselines. 

ConditionedNet, Fig. 3 and Table II demonstrate that our method greatly outperforms the ablations. This validates our hypothesis that incorporating a good estimate of _ω_ into the world model and policy networks improves the performance of a RL policy operating in an environment with variable _ω_ . 

## V. CONCLUSION 

This paper presents a novel architecture for solving problems where the dynamics are dictated by hidden parameters. We model these problems with Hidden-parameter Markov decision processes (HIP-MDPs) and solve them using modelbased reinforcement learning. We introduce a new model PrivilegedDreamer, based on the DreamerV2 world model, that handles the HIP-MDP problem via explicit prediction of these hidden variables. Our key invention consists of an external recurrent module to estimate these hidden variables to provide them as inputs to the world model itself. We evaluate our model on five HIP-MDP tasks, including both DeepMind Control Suite tasks and manually created tasks, where the reward explicitly depends on the hidden parameter. We find our model significantly outperforms the DreamerV2 model, as well as the other baselines we tested against. 

Our research opens up several intriguing agendas for future investigation. Firstly, this paper has concentrated our efforts on studying hidden parameter estimation within proprioceptive control problems, intentionally deferring the exploration of visual control problems like Atari games or vision-based robot control for future works. We believe that the same principle of explicitly modeling hidden parameters can be effectively applied to these visual control challenges with minor adjustments to the neural network architectures. Furthermore, we plan to investigate more complex robotic control problems, such as legged locomotion [8], where real-world dynamics may be too sensitive to be precisely replicated by any of the hidden parameters. In such cases, we anticipate the need to devise better approximation methods. Lastly, we plan to delve into multi-agent scenarios in which these hidden parameters have an impact on the AI behavior of other agents. These subsequent research directions hold promise in extending the scope and impact of the original paper. 

REFERENCES 

- [1] F. Doshi-Velez and G. Konidaris, “Hidden parameter markov decision processes: A semiparametric regression approach for discovering latent task parametrizations,” vol. 2016-January. International Joint Conferences on Artificial Intelligence, 2016, pp. 1432–1440. 

- [2] J. Tobin, R. Fong, A. Ray, J. Schneider, W. Zaremba, and P. Abbeel, “Domain randomization for transferring deep neural networks from simulation to the real world,” 3 2017. [Online]. Available: http://arxiv.org/abs/1703.06907 

- [3] X. B. Peng, E. Coumans, T. Zhang, T.-W. E. Lee, J. Tan, and S. Levine, “Learning agile robotic locomotion skills by imitating animals,” in _Robotics: Science and Systems_ , 07 2020. 

- [4] J. X. Wang, Z. Kurth-Nelson, D. Tirumala, H. Soyer, J. Z. Leibo, R. Munos, C. Blundell, D. Kumaran, and M. Botvinick, “Learning to reinforcement learn.” 

- [5] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Dream to control: Learning behaviors by latent imagination,” 12 2019. [Online]. Available: http://arxiv.org/abs/1912.01603 

- [6] Y. Tassa, Y. Doron, A. Muldal, T. Erez, Y. Li, D. de Las Casas, D. Budden, A. Abdolmaleki, J. Merel, A. Lefrancq, T. Lillicrap, and M. Riedmiller, “Deepmind control suite,” 1 2018. [Online]. Available: http://arxiv.org/abs/1801.00690 

- [7] D. Hafner, T. Lillicrap, M. Norouzi, and J. Ba, “Mastering atari with discrete world models,” 10 2020. [Online]. Available: http://arxiv.org/abs/2010.02193 

- [8] P. Wu, A. Escontrela, D. Hafner, K. Goldberg, and P. Abbeel, “Daydreamer: World models for physical robot learning,” 6 2022. [Online]. Available: http://arxiv.org/abs/2206.14176 

- [9] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, “Soft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor,” 2018. 

- [10] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” 7 2017. [Online]. Available: http://arxiv.org/abs/1707.06347 

- [11] A. Kumar, Z. Fu, D. Pathak, and J. Malik, “Rma: Rapid motor adaptation for legged robots,” 2021. 

- [12] K. Chua, R. Calandra, R. McAllister, and S. Levine, “Deep reinforcement learning in a handful of trials using probabilistic dynamics models,” 5 2018. [Online]. Available: http://arxiv.org/abs/ 1805.12114 

- [13] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap, “Mastering diverse domains through world models,” 1 2023. [Online]. Available: http://arxiv.org/abs/2301.04104 

- [14] K. Cho, B. van Merrienboer, D. Bahdanau, and Y. Bengio, “On the properties of neural machine translation: Encoder-decoder approaches,” 9 2014. [Online]. Available: http://arxiv.org/abs/1409. 1259 

- [15] D. P. Kingma and M. Welling, “Auto-encoding variational bayes,” 12 2013. [Online]. Available: http://arxiv.org/abs/1312.6114 

- [16] J. Robine, M. H¨oftmann, T. Uelwer, and S. Harmeling, “Transformerbased world models are happy with 100k interactions,” 3 2023. [Online]. Available: http://arxiv.org/abs/2303.07109 

- [17] V. Micheli, E. Alonso, and F. Fleuret, “Transformers are sampleefficient world models,” 9 2022. [Online]. Available: http://arxiv.org/ abs/2209.00588 

- [18] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, “Attention is all you need,” 6 2017. [Online]. Available: http://arxiv.org/abs/1706.03762 

- [19] X. B. Peng, M. Andrychowicz, W. Zaremba, and P. Abbeel, “Sim-toreal transfer of robotic control with dynamics randomization,” 2018. 

- [20] F. Zhang, J. Leitner, M. Milford, and P. Corke, “Modular deep q networks for sim-to-real transfer of visuo-motor policies,” 10 2016. [Online]. Available: http://arxiv.org/abs/1610.06781 

- [21] S. James, A. J. Davison, and E. Johns, “Transferring end-to-end visuomotor control from simulation to real world for a multi-stage task,” 7 2017. [Online]. Available: http://arxiv.org/abs/1707.02267 

   - [24] F. Sadeghi and S. Levine, “Cad 2 rl: Real single-image flight without a single real image.” [Online]. Available: https://youtu.be/ nXBWmzFrj5s 

   - [25] M. Rigter, M. Jiang, and I. Posner, “Reward-free curricula for training robust world models,” _International Conference on Learning Representations_ , 2024. 

   - [26] J. Yamada, M. Rigter, J. Collins, and I. Posner, “Twist: Teacherstudent world model distillation for efficient sim-to-real transfer,” _arXiv preprint arXiv:2311.03622_ , 2023. 

   - [27] J. T. Kim and S. Ha, “Observation space matters: Benchmark and optimization algorithm,” _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 1527–1534, 2020. 

   - [28] W. Yu, J. Tan, C. K. Liu, and G. Turk, “Preparing for the unknown: Learning a universal policy with online system identification,” 2 2017. [Online]. Available: http://arxiv.org/abs/1702.02453 

   - [29] I. M. A. Nahrendra, B. Yu, and H. Myung, “Dreamwaq: Learning robust quadrupedal locomotion with implicit terrain imagination via deep reinforcement learning,” 1 2023. [Online]. Available: http://arxiv.org/abs/2301.10602 

   - [30] G. Ji, J. Mun, H. Kim, and J. Hwangbo, “Concurrent training of a control policy and a state estimator for dynamic and robust legged locomotion,” _IEEE Robotics and Automation Letters_ , vol. 7, 2022. 

   - [31] A. Nagabandi, I. Clavera, S. Liu, R. S. Fearing, P. Abbeel, S. Levine, and C. Finn, “Learning to adapt in dynamic, real-world environments through meta-reinforcement learning,” 3 2018. [Online]. Available: http://arxiv.org/abs/1803.11347 

   - [32] S. Sæmundsson, K. Hofmann, and M. P. Deisenroth, “Meta reinforcement learning with latent variable gaussian processes,” 3 2018. [Online]. Available: http://arxiv.org/abs/1803.07551 

   - [33] Q. Wang and H. van Hoof, “Model-based meta reinforcement learning using graph structured surrogate models,” 2 2021. [Online]. Available: http://arxiv.org/abs/2102.08291 

   - [34] P. J. Ball, C. Lu, J. Parker-Holder, and S. Roberts, “Augmented world models facilitate zero-shot dynamics generalization from a single offline environment,” 4 2021. [Online]. Available: http: //arxiv.org/abs/2104.05632 

   - [35] J. Wang, Y. Mu, D. Li, Q. Zhang, D. Zhao, Y. Zhuang, P. Luo, B. Wang, and J. Hao, “Prototypical contextaware dynamics generalization for high-dimensional modelbased reinforcement learning,” 11 2022. [Online]. Available: http://arxiv.org/abs/2211.12774 

   - [36] K. Lee, Y. Seo, S. Lee, H. Lee, and J. Shin, “Context-aware dynamics model for generalization in model-based reinforcement learning,” 5 2020. [Online]. Available: http://arxiv.org/abs/2005.06800 

   - [37] B. Huang, F. Feng, C. Lu, S. Magliacane, and K. Zhang, “Adarl: What, where, and how to adapt in transfer reinforcement learning,” 7 2021. [Online]. Available: http://arxiv.org/abs/2107.02729 

   - [38] Y. Seo, K. Lee, I. Clavera, T. Kurutach, J. Shin, and P. Abbeel, “Trajectory-wise multiple choice learning for dynamics generalization in reinforcement learning,” 10 2020. [Online]. Available: http: //arxiv.org/abs/2010.13303 

   - [39] S. Hochreiter and J. Schmidhuber, “Long short-term memory.” 

   - [40] W. Yu, J. Tan, Y. Bai, E. Coumans, and S. Ha, “Learning fast adaptation with meta strategy optimization,” 2020. 

   - [41] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control,” 2012. 

   - [42] O. Khatib, “A unified approach for motion and force control of robot manipulators: The operational space formulation,” _IEEE Journal on Robotics and Automation_ , vol. 3, no. 1, pp. 43–53, 1987. 

   - [43] A. Raffin, A. Hill, A. Gleave, A. Kanervisto, M. Ernestus, and N. Dormann, “Stable-baselines3: Reliable reinforcement learning implementations,” _Journal of Machine Learning Research_ , vol. 22, no. 268, pp. 1–8, 2021. [Online]. Available: http://jmlr.org/papers/ v22/20-1364.html 

   - [44] D. Yarats and I. Kostrikov, “Soft actor-critic (sac) implementation in pytorch,” https://github.com/denisyarats/pytorch ~~s~~ ac, 2020. 

- [22] J. Tan, T. Zhang, E. Coumans, A. Iscen, Y. Bai, D. Hafner, S. Bohez, and V. Vanhoucke, “Sim-to-real: Learning agile locomotion for quadruped robots,” 4 2018. [Online]. Available: http://arxiv.org/abs/ 1804.10332 

- [23] J. Tremblay, A. Prakash, D. Acuna, M. Brophy, V. Jampani, C. Anil, T. To, E. Cameracci, S. Boochoon, and S. Birchfield, “Training deep networks with synthetic data: Bridging the reality gap by domain randomization,” 4 2018. [Online]. Available: http://arxiv.org/abs/1804.06516 

