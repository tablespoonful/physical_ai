---
title: "Dreamer-SAC: Off-Policy Learning in Latent World Models for Sample-Efficient Autonomous Driving"
date: "2026-08-11"
authors: "Jiazhuo Li; Linjiang Cao; Qi Liu; Xi Xiong"
url: https://arxiv.org/abs/2608.10386
pdf: https://arxiv.org/pdf/2608.10386
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2608.10386)** / [論文ページ](https://arxiv.org/abs/2608.10386)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Dreamer-SAC: Off-Policy Learning in Latent World Models for Sample-Efficient Autonomous Driving** 

**Jiazhuo Li Linjiang Cao Qi Liu Xi Xiong**<sup>_∗_</sup> Tongji University `2534457@tongji.edu.cn` , `2431743@tongji.edu.cn` , `liu_qi@tongji.edu.cn` , `xi_xiong@tongji.edu.cn` 

## **Abstract** 

Sample-efficient reinforcement learning for autonomous driving is often limited by the trade-off between data efficiency and model bias. While world models reduce the reliance on costly environment interactions, policy optimization over learned dynamics remains sensitive to prediction errors. This paper proposes the DreamerSAC framework, which integrates a recurrent state-space world model with an off-policy soft actor-critic algorithm trained directly in latent space. The framework uses a combination of real interactions and short-horizon generated trajectories with n-step target estimation and multi-objective supervision. Evaluated in autonomous driving scenarios with objectives encompassing driving efficiency and safety, the proposed framework consistently outperforms representative reinforcement learning baselines, including DreamerV3, SAC, and PPO, while achieving improved performance with substantially fewer real environment interactions. Experiments reveal an inverted-U relationship between rollout horizon and policy performance, where short-horizon latent rollouts achieve the best trade-off between additional training signals and accumulated model bias. Furthermore, n-step target estimation demonstrates more effectiveness over one-step temporal-difference targets in exploiting predicted experience for value learning. 

## **1 Introduction** 

Autonomous driving is a core enabling technology for next-generation intelligent transportation systems, with the potential to reduce traffic fatalities, alleviate congestion, and improve mobility accessibility [1]. Autonomous vehicles are required to make continuous sequential decisions in complex and uncertain traffic environments involving dynamic interactions with surrounding road users. However, the large-scale deployment of reliable autonomous driving decision systems remains challenging. A primary bottleneck lies in the prohibitive cost of safety validation, as ensuring reliable performance under long-tail and safety-critical scenarios, such as collisions, unexpected cut-ins, and complex interactions, requires extensive driving experience. Real-world testing not only incurs substantial economic costs but also introduces potential risks to public road safety [2]. Reinforcement learning (RL) provides a promising data-driven framework for sequential decisionmaking [3], enabling autonomous agents to learn sophisticated driving policies through environmental interaction rather than relying solely on manually designed decision rules. Despite its potential, the practical application of RL to autonomous driving remains severely constrained by its limited sample efficiency, as achieving reliable policies typically requires large amounts of interaction data [4]. 

Model-based reinforcement learning (MBRL) has recently attracted considerable attention as a promising solution to this problem. Instead of interacting with the environment for every policy update, MBRL learns a predictive world model that approximates environment dynamics and generates 

> _∗_ Corresponding author. 

trajectories for policy optimization. By replacing expensive environment interactions with latentspace rollouts, world models substantially improve data efficiency while maintaining competitive control performance [5]. Building on this paradigm, this paper proposes a model-based RL framework tailored for autonomous driving. Our method integrates world models with off-policy RL, enabling the agent to learn policies through both real and rolled-out interactions. This maximizes data utilization while mitigating the impact of model bias. 

Existing approaches to autonomous driving decision making have evolved through several paradigms. Early systems relied predominantly on rule-based methods, such as finite state machines, behavior trees, and handcrafted heuristics for scenario decomposition and maneuver selection [6, 7]. While interpretable and deterministic, these methods struggle to generalize to the combinatorial complexity of real-world traffic interactions and require extensive manual engineering to scale. Optimization-based techniques—notably model predictive control (MPC)—were subsequently introduced to explicitly exploit vehicle dynamics and constraints for trajectory planning and tracking [8]. However, the reliance on manually designed cost functions and simplified dynamic models limits their adaptability in highly interactive or uncertain environments. The emergence of deep learning enabled a paradigm shift toward data-driven policy learning. Imitation learning (IL), particularly behavior cloning, learns driving policies directly from expert demonstrations by mapping raw sensor inputs to control commands [9]. Although effective for capturing human-like driving styles, IL fundamentally suffers from covariate shift and compounding errors when the learned policy deviates from the expert state distribution [10]. Reinforcement learning (RL) offers an alternative by enabling agents to discover policies through trial-and-error interaction, thereby optimizing long-term performance beyond expert demonstrations. Model-free RL algorithms, such as Proximal Policy Optimization (PPO) [11] and Soft Actor-Critic (SAC) [12], have achieved remarkable success in continuous control tasks. To improve sample efficiency, model-based methods learn predictive dynamics models that generate synthetic rollouts, reducing reliance on costly real interactions. Early work such as Model-Based Policy Optimization (MBPO) [13] demonstrated that short-horizon rollouts from an ensemble of probabilistic dynamics models can effectively augment real data for off-policy SAC training. However, MBPO operates directly in the original state space using explicit dynamics models, limiting its applicability to high-dimensional visual observations common in autonomous driving. To overcome this, latent world models learn compact representations of environment dynamics, enabling planning and policy optimization entirely in a compressed latent space [14, 15]. Among recent approaches, the Dreamer family has demonstrated remarkable success across continuous-control benchmarks by learning a Recurrent State-Space Model (RSSM) that captures latent dynamics [16]. The learned latent representation enables planning and policy learning entirely in latent space, avoiding costly pixel-level reconstruction during policy optimization. 

Several works have adapted latent world models to autonomous driving: Gao et al. enhanced robustness through semantic masked world models [17], while Yang et al. explored representation alignment between raw observations and privileged features [18]. However, these approaches primarily focus on improving the representation quality of the world model itself, rather than reconsidering the policy optimization paradigm within the latent space. Most of these methods employ on-policy actor-critic optimization strategies, limiting the agent to training within the “imagined” world and lacking the ability to learn directly from real-world data. Unlike real transitions, predicted trajectories inevitably suffer from accumulated prediction errors [19], causing model bias that increases rapidly with rollout horizon, which will affect the policy’s assessment of safety-critical driving scenarios (such as collisions). 

To address these challenges, this paper proposes a Dreamer-SAC framework that combines latent world models with off-policy reinforcement learning through short-horizon rollouts and mixed replay optimization. Instead of relying exclusively on predicted trajectories, the proposed framework continuously updates the world model using real interaction data while generating short latent rollouts from posterior RSSM states. Real transitions are optimized using conventional one-step temporaldifference targets, whereas predicted trajectories adopt n-step targets to better exploit long-term reward information within the rollout horizon. Both data sources are jointly used for critic and actor optimization, allowing SAC to benefit from model-generated experience while limiting the adverse effects of long-horizon model bias. 

The main contributions of this work are summarized as follows: 

2 

1. A model-based off-policy reinforcement learning framework is proposed by integrating Soft Actor-Critic into the Recurrent State-Space Model, enabling autonomous driving policies to efficiently exploit model-generated rollouts. 

2. A hybrid real and model-generated experience learning strategy is developed to improve policy reliability by combining real transitions and latent rollouts with different value estimation schemes, thereby enhancing data utilization while mitigating the impact of model prediction errors. 

3. Comprehensive experiments demonstrate the superiority of the proposed framework over representative reinforcement learning baselines and reveal an inverted-U relationship between rollout horizon and performance, indicating that short-horizon rollouts provide the optimal balance between learning benefits and model bias. 

## **2 Preliminaries** 

This section introduces the problem we study, as well as background knowledge regarding world models and Soft Actor-Critic. 

### **2.1 Problem Definition** 

In real-world driving, an ego vehicle cannot access the complete and exact state of the environment, such as the precise intentions of other drivers or occluded road regions. Instead, it must rely solely on its onboard sensors, which provide partial and noisy observations. We model the autonomous driving task as a Partially Observable Markov Decision Process (POMDP) [20]. The POMDP is defined by the tuple ( _S, A, O, T ,_ Ω _, R, γ_ ), where _S_ represents the true but unobservable environment state. _A_ is the action space consisting of continuous steering and throttle/brake commands **a** _t_ = ( _a_ steer _, a_ throttle) _∈_ [ _−_ 1 _,_ 1]<sup>2</sup> . _O_ is the observation space. At each time step _t_ , the ego vehicle receives an observation **o** _t_ composed of two modalities: 


where _It ∈_ R<sup>_H×W ×_3</sup> is an image from a front-facing camera, and **v** _t ∈_ R<sup>125</sup> is a vector of vehicle observation, including LiDAR and own-state information. Both of them can be directly obtained through raw sensors or physical calculations. _T_ ( _s_<sup>_′_</sup> _| s, a_ ) : _S×A×S →_ [0 _,_ 1] defines the conditional transition probability distribution over next states. Ω( _o | s, a_ ) : _S × A × O →_ [0 _,_ 1] defines the probability of observing given state and action. _R_ : _S × A →_ R is the reward function balancing safety and efficiency, while _γ ∈_ [0 _,_ 1] is the discount factor. The agent’s objective is to learn a policy _π_ ( _at|o≤t_ ) that maximizes the expected cumulative discounted reward: 


### **2.2 Latent World Models** 

Model-based reinforcement learning improves sample efficiency by learning a predictive model of environment dynamics and generating trajectories for policy optimization. Instead of directly predicting future observations in the high-dimensional image space, latent world models first compress observations into a compact latent representation ˆ _st ∈S_ latent and perform transition prediction entirely in the latent space. This substantially reduces computational cost while preserving information relevant for control. 

The world model consists of the following components: 


3 

The representation model maps high-dimensional observations into a compact latent state, compressing raw sensor inputs while preserving task-relevant information. The transition model predicts future latent states given the current state and action, forming the core of the learned dynamics. The observation model reconstructs observations from the latent state, providing a self-supervised reconstruction signal. The reward model predicts immediate rewards for value estimation. In our tasks, a separate continue model predicts the termination signal, helping the agent identify episode boundaries. Through the learned latent dynamics model, the agent can generate latent rollouts by predicting future states, rewards, and termination signals in the latent space. These model-generated trajectories provide additional training experiences for policy optimization and reduce the reliance on direct environment interactions. 

### **2.3 Soft Actor-Critic** 

Soft Actor-Critic (SAC) [12] is an off-policy actor-critic algorithm that optimizes both expected return and policy entropy, encouraging efficient exploration while maintaining stable learning. SAC solves the maximum entropy objective: 


where _ρπ_ denotes the state-action marginal induced by policy _π_ , _γ ∈_ [0 _,_ 1) is the discount factor, and _α_ controls the trade-off between reward maximization and the entropy term _H_ , which encourages exploration. The critic is trained using the soft Bellman target: 


where two independent _Q_ -networks are employed to alleviate overestimation bias. The policy is optimized by minimizing the actor loss: 


where _D_ is the replay buffer and the temperature parameter _α_ is automatically adjusted to maintain a target policy entropy. Compared with on-policy policy-gradient methods, SAC achieves substantially higher sample efficiency through experience replay and stable value estimation, making it well suited for latent model-based reinforcement learning. 

## **3 Method** 

This section introduces the Dreamer-SAC framework. As shown in Figure 1, real driving experiences collected from the environment are stored in a replay buffer and used to train the RSSM world model, which learns compact latent representations and predicts observations, multi-objective rewards, and termination signals. Starting from real latent states, the current policy performs short-horizon rollouts in the learned latent dynamics. The generated trajectories are combined with real experiences to train the SAC agent, where real data adopts one-step temporal-difference targets and model-generated data uses multi-step returns. By integrating real and predicted experiences within an off-policy learning framework, the proposed method improves data efficiency while reducing the model bias associated with purely model-generated policy optimization. 

### **3.1 Multi-modal Encoding** 

The observation at each timestep consists of two modalities: a front-facing camera image _It ∈_ R<sup>_H×W ×_3</sup> providing rich visual context of the road environment, and a vector **v** _t ∈_ R<sup>125</sup> comprising LiDAR range measurements and ego-vehicle state information. The LiDAR component captures 120 range readings over a 50-meter sensing radius, while the ego-state component encodes the vehicle’s speed, steering angle, previous actions and yaw rate. 

The image modality is processed by a convolutional neural network (CNN): _f_ img = CNN( _It_ ; _θ_ img), progressively downsampling spatial resolution while expanding channel depth. The resulting feature 

4 


Figure 1: Overview of the proposed Dreamer-SAC framework. The RSSM encodes multimodal observations into a compact latent state; latent rollouts are generated from posterior states and jointly used with real transitions to optimize the SAC policy. 

maps are flattened into a compact image embedding. The vector modality is processed by a multilayer perceptron (MLP): _f_ phys = MLP( _vt_ ; _θ_ vec). Both embeddings are then concatenated to form the encoded observation: 


### **3.2 Latent Dynamics Modeling** 

The encoded observations embedding is then fed into a Recurrent State-Space Model (RSSM) [16]. At each time step, the model maintains a deterministic hidden state _ht_ that summarizes past information, and a stochastic state _zt_ that captures uncertainty. The transition is defined as: 


where _fθ_ is a recurrent neural network. _zt_ is sampled from the posterior _q_ ( _zt | ht, et_ ) when real observations are available, and from the prior _p_ ( _zt | ht_ ) during latent rollouts where no observation exists. ( _ht, zt_ ) together form the latent state. 

The basic world model loss consists of prediction loss and KL regularization loss: 


where _L_ pred _,t_ includes the negative log-likelihood of observation reconstruction _−_ ln _pθ_ ( _ot | ht, zt_ ), reward prediction _−_ ln _pθ_ ( _rt | ht, zt, at_ ), and termination signal prediction _−_ ln _pθ_ ( _ct | ht, zt, at_ ). The _L_ KL _,t_ = _D_ KL� _qθ_ ( _zt | ht, et_ ) _∥ pθ_ (ˆ _zt | ht_ )� is the KL divergence between the posterior and prior distribution, constraining the encoder to avoid extracting irrelevant information from observations and enhancing the consistency and predictability of the latent state. 

### **3.3 Multi-objective Reward** 

Autonomous driving is inherently a multi-objective decision-making problem, where safe and efficient driving behaviors must be optimized simultaneously. The reward function consists of the following three parts: 

5 

The driving efficiency reward _R_ eff encouraging forward progress and maintaining appropriate speed: 


where _xt_ is the longitudinal projection of the vehicle onto the lane centerline, _v_ is the current speed, _v_ max is the expected maximum speed, and **1** pos indicates correct driving direction. 

The lane center offset penalty _R_ lane penalizes deviation from the lane center: 


where _yt_ denotes lateral offset and _w_ lane is lane width. 

The termination reward/punishment _R_ term provides a sparse terminal reward for completing the route or penalty for violations: 


The total reward for each timestep is: 


Instead of learning a single reward predictor, we employ three independent prediction heads. The efficiency reward _R_ eff and lane-center reward _R_ lane are continuous and are optimized using mean squared error (MSE) loss. In contrast, the terminal reward _R_ term is sparse and discrete. A symlogdiscretized categorical distribution is used to model _R_ term, which better captures the uncertainty of terminal events by representing predictions as a probability distribution over discrete bins. 

The overall reward prediction loss is defined as: 


where _L_ CE denotes the cross-entropy loss for the symlog-discretized categorical prediction, and _λi_ are weighting coefficients balancing the contribution of each reward component. Therefore, the reward prediction term in the world model loss (Equation 13) is replaced by _L_ reward (Equation 18). 

### **3.4 Off-policy Learning** 

In Dreamer-style methods, the actor-critic is trained on-policy: each update requires fresh trajectories generated by the current policy, which is why these methods rely exclusively on model-generated rollouts and cannot reuse previously collected real transitions, as those were produced by earlier policies. In contrast, off-policy reinforcement learning imposes no such restriction on the datagenerating policy. This allows the agent to simultaneously exploit stored real transitions and freshly generated latent rollouts, enabling more efficient reuse of expensive real-world samples while still benefiting from model-generated experiences. 

### **3.4.1 Hybrid Real and Model-Generated Replay** 

The proposed hybrid replay mechanism operates as follows. For each training iteration, a batch of trajectory segments is first sampled from the real replay buffer, _Dr_ = _{_ ( _ot, at, rt, · · ·_ ) _}_ . These real trajectories serve two purposes. First, they are used to optimize the RSSM world model through representation learning. Second, the posterior latent states inferred from each real transition are used as initialization points for latent rollouts. Starting from every posterior state, the world model rolls forward for a fixed rollout horizon _H_ using the current SAC policy, generating transitions _Di_ . The SAC agent is then updated using the union of real and model-generated experiences, _D_ = _Dr ∪Di_ . 

Since rollout is performed from every sampled real transition, the number of predicted transitions is directly determined by the rollout horizon _H_ . Consequently, the ratio between real and predicted samples automatically becomes 1 : _H_ . Unlike previous methods that manually tune the proportion of predicted data, the proposed strategy introduces no additional hyperparameter. Increasing the rollout horizon naturally increases the amount of model-generated supervision, reflecting greater reliance on the learned world model. 

6 

Moreover, predicted trajectories are discarded immediately after policy optimization. At the next iteration, new predicted samples are regenerated using the latest RSSM and SAC policy. This online regeneration avoids repeatedly training on outdated predictions and reduces the influence of model errors accumulated during previous optimization stages. 

### **3.4.2 Multi-step Bootstrapping** 

Real transitions correspond to actual environment interactions and therefore employ the standard one-step SAC target, 


where _ct ∈{_ 0 _,_ 1 _}_ is the continuation flag, which zeroes out the bootstrap term after collision, out-of-road, or successful arrival. In contrast, predicted trajectories are generated entirely inside the learned world model and contain future rewards that are immediately available after rollout. Therefore, instead of discarding these additional rewards, we exploit the complete rollout horizon by constructing an _n_ -step target, 


where _at_ + _N ∼ πϕ_ ( _· | st_ + _N_ ), _N_ equals the remaining length of the rollout, and _ct_ + _j_ is from the RSSM continue predictor. Compared with one-step TD learning, the proposed target propagates long-horizon reward information to the critic while reducing bootstrap variance inside predicted trajectories. Algorithm 1 summarizes the complete training procedure. 

**Algorithm 1** Dreamer-SAC: Hybrid World Model with Off-policy Policy Optimization 

1: **Input:** World model _M_ , actor _π_ , critics _Q_ 1 _, Q_ 2, real replay buffer _D_ , rollout horizon _H_ 2: Initialize _M, π, Q_ 1 _, Q_ 2 3: **while** training **do** 4: Collect one transition from the environment and store it in _D_ 5: Sample batch _{_ ( _ot, at, rt_ ) _}_<sup>_T_</sup> _t_ =1<sup>from</sup><sup>_D_</sup> 6: Update RSSM by minimizing _L_ WM = _L_ KL + _L_ obs + _L_ reward + _L_ cont 7: Initialize predicted buffer _D_<sup>ˆ</sup> _←∅_ 8: **for all** posterior latent state _st_ **do** 9: _s ←_ sg( _st_ ) _▷_ Stop gradient 10: **for** _k_ = 1 **to** _H_ **do** 11: Sample action _ak ∼ π_ ( _s_ ) 12: Predict ( _s_<sup>_′_</sup> _, r, c_ ) using RSSM 13: Store transition ( _s, a, r, c, s_<sup>_′_</sup> ) into _D_<sup>ˆ</sup> 14: _s ← s_<sup>_′_</sup> 15: **end for** 

16: **end for** 

17: Update critics using real samples with 1-step TD targets and predicted samples with _n_ -step targets 18: Update actor by SAC objective 

- 19: Update entropy coefficient _α_ 20: Soft-update target critics 21: Discard _D_<sup>ˆ</sup> 22: **end while** 

## **4 Experiments** 

This section provides a detailed introduction to our experimental setup, model configuration, comparative experiment, ablation study and analysis of related results. 

7 

### **4.1 Experimental Setup** 

We evaluate the proposed framework on the MetaDrive simulator [21], a high-fidelity autonomous driving platform that provides diverse road geometries and dynamic traffic interactions. The experiments are conducted on the BIG_BLOCK_SEQUENCE-CC scenario, which consists of a multi-lane highway segment with consecutive curved sections. The vehicle itself needs to continuously adjust its steering as the road curvature changes, while maintaining safe interaction with surrounding vehicles. 

Key environment parameters include traffic density of 0.1 (Approximately 30 vehicles per kilometer), 10 distinct training scenarios and 50 distinct testing scenarios. Each episode terminates immediately upon collision or out-of-road. Each episode runs for up to 300 decision steps, with each decision step corresponding to 20 simulation frames. The action space is [ _−_ 1 _,_ 1]<sup>2</sup> for continuous steering and throttle/brake control. Observations consist of an RGB camera image (84 _×_ 84 _×_ 3) and a 125-dimensional vector (120 LiDAR rays at 50 m range plus 5 ego-vehicle state variables). Collision and out-of-road penalty _pcrash, pout_ = 40 _._ 0, successful arrival bonus _rsuccess_ = 10 _._ 0. Reward coefficients _βd_ = 1 _._ 0, _βs_ = 0 _._ 1, _βc_ = 1 _._ 0. 


Figure 2: MetaDrive driving scenario with multimodal observations. 

### **4.1.1 Model Configurations** 

The world model is implemented based on the recurrent state-space model (RSSM) architecture. The image encoder consists of four convolutional layers with channel sizes of 32, 64, 128, and 256, respectively, using kernel size 4, stride 2, layer normalization, and SiLU activations. The vector observation encoder employs a two-layer MLP with 256 hidden units, layer normalization, and SiLU activations. The RSSM contains a deterministic recurrent state of 256 dimensions and a discrete stochastic state with 32 categorical variables and 32 classes per variable. The resulting latent feature dimension is 1280. The decoder, reward prediction heads, and continuation prediction head are optimized jointly with the RSSM to learn predictive latent representations. 

The SAC policy module operates directly on RSSM latent features. The actor and twin critic networks consist of two fully connected layers with 256 hidden units, layer normalization, and SiLU activations. The critic networks use independent parameters and are updated with soft target networks using a Polyak coefficient of 0.005. The entropy coefficient is automatically adjusted during training with a target entropy of _−_ 2. 

All networks are optimized using the Adam optimizer. The world model is trained with sequences of batch size 16 and sequence length 32, using a learning rate of 1 _×_ 10<sup>_−_4</sup> . The SAC actor and critic are optimized with a learning rate of 3 _×_ 10<sup>_−_4</sup> . The rollout horizon is set to _H_ = 5 steps, where predicted trajectories are generated from posterior RSSM states and combined with real transitions for off-policy learning. The discount factor is _γ_ = 0 _._ 99. Training is performed for 40,000 environment interaction steps. The overall model contains approximately 13 million trainable parameters, including the world model, SAC policy, and value networks. 

8 

### **4.2 Comparative Experiments** 

To evaluate the effectiveness of the proposed Dreamer-SAC framework, we compare it with three representative reinforcement learning baselines. All methods are evaluated under identical driving environments, including the same MetaDrive configuration, sensor inputs, training scenarios, and network capacity. For fair comparison, all actor-critic networks adopt the same architecture with two hidden layers of 256 units. 

_•_ **DreamerV3:** DreamerV3 [16] represents latent world-model-based on-policy learning, which learns a RSSM from interaction data and trains an actor-critic agent entirely on predicted latent rollouts generated by the learned model. The actor is updated via REINFORCE with an advantage estimate computed from predicted returns, while the critic predicts state values using a symlog-discretized distribution. 

_•_ **SAC:** Soft Actor-Critic is an off-policy maximum-entropy RL algorithm that jointly optimizes expected return and policy entropy. It employs twin Q-networks to mitigate overestimation bias, a replay buffer for sample reuse, and automatic entropy temperature tuning. 

_•_ **PPO:** Proximal Policy Optimization is an on-policy policy-gradient method that constrains policy updates via a clipped surrogate objective, balancing sample efficiency with training stability. PPO collects trajectories using the current policy, computes advantage estimates via generalized advantage estimation, and performs multiple epochs of minibatch updates on each collected batch before discarding it. 


Figure 3: Training return comparison of Dreamer-SAC against DreamerV3, SAC, and PPO baselines. 

Figure 3 shows the comparison curves of training return convergence. The proposed DreamerSAC achieves the highest final performance, reaching an average return of 371.4. In comparison, DreamerV3 achieves an average return of 189.2 and exhibits relatively high variance. The SAC curve is relatively stable, converging at 134.5. PPO employs online learning, resulting in low data efficiency and a slow-rising curve, reaching a score of 65.5. These results validate the effectiveness of integrating latent world models with off-policy policy optimization for autonomous driving tasks. 

### **4.2.1 Generalization Evaluation** 

To further evaluate the generalization capability and long-horizon driving performance, we conduct additional experiments on a substantially longer road network, whose length is approximately three times that of the training environment. All methods are evaluated under 50 independent trials with unseen random seeds, and all indicators are taken as the average of these 50 experiments. 

We measure five driving metrics, including collision frequency, out-of-road frequency, average speed, average travel distance, and maximum travel distance. Collision frequency and out-of-road frequency are normalized by the total driven distance: 


9 

where _N_ collision and _N_ out denote the number of collision and out-of-road events, respectively, and _D_ total represents the total traveled distance in kilometers. 

The results are summarized in Table 1. Dreamer-SAC achieves the lowest collision frequency (1.56/km) and out-of-road frequency (1.37/km), while also obtaining the longest average travel distance (320.8 m) and maximum travel distance (951.6 m). Compared with DreamerV3, SAC, and PPO, Dreamer-SAC demonstrates substantially improved long-horizon driving reliability, indicating that the integration of latent prediction with off-policy learning leads to more robust decision-making beyond the training scenarios. 

Table 1: Generalization performance on extended road networks. 

|**Method**|**Collision**|**Out-of-road**|**Avg Speed**|**Avg Dist**|**Max Dist**|
|---|---|---|---|---|---|
||**(/km)**|**(/km)**|**(km/h)**|**(m)**|**(m)**|
|Dreamer-SAC|**1.56**|**1.37**|25.5|**320.8**|**951.6**|
|DreamerV3|2.88|1.76|**39.7**|215.5|515.2|
|SAC|1.68|8.85|28.0|95.0|348.0|
|PPO|3.72|4.03|25.1|129.1|369.6|


An interesting observation is that DreamerV3 achieves the highest average speed (39.7 km/h) but suffers from higher collision frequency and shorter travel distance. This indicates that training exclusively with predicted experiences may amplify model bias, where safety-critical transitions are inaccurately represented in the learned dynamics. Consequently, the policy may exploit inaccuracies in the predicted environment and adopt overly aggressive behaviors, such as maintaining higher speeds and performing frequent overtaking maneuvers, which improves short-term reward accumulation but compromises long-term driving reliability. 

In contrast, Dreamer-SAC employs a dual-network architecture and learns a more conservative and reliable driving strategy by continuously incorporating real experiences during policy optimization. When encountering slower vehicles, the agent tends to follow the preceding vehicle and reduce speed when necessary rather than aggressively performing risky maneuvers. Although the average speed is lower than DreamerV3, this behavior significantly improves survival distance and reduces safety violations, which is particularly important for autonomous driving applications. 

### **4.3 Effect of Rollout Horizon** 

The rollout horizon _H_ determines not only the rollout length of the learned world model but also the proportion of predicted samples used for policy optimization. We evaluate its influence by varying _H_ from 0 to 20 while keeping all other training configurations unchanged. As shown in Figure 4, the performance exhibits a clear inverted-U trend. Without rollouts ( _H_ = 0), the agent fails to learn meaningful driving behavior and achieves an average return of only _−_ 2 _._ 6. Increasing the horizon significantly improves performance, reaching the best result at _H_ = 5 with an average return of 371.4. However, further increasing the horizon leads to gradual degradation, with returns decreasing to 285.6 at _H_ = 20. 


Figure 4: Training return as a function of the rollout horizon _H_ , showing an inverted-U trend with optimal performance at _H_ = 5. 

10 

The poor performance without rollouts indicates that directly optimizing SAC in the learned latent space using only real samples is insufficient during early training. Since the RSSM representation and policy are optimized separately, the initial critic receives limited and unstable decision-related information. As a result, the policy tends to converge to a conservative failure mode, where the vehicle remains stationary to avoid collision penalties. Introducing short-horizon rollouts provides additional on-policy samples generated by the current policy and world model, allowing the critic to continuously evaluate newly explored behaviors and avoiding the negative feedback loop caused by insufficient exploration. 


Figure 5: Q-value mean, Q-value standard deviation, and world model loss across different rollout horizons. 

The additional training statistics, illustrated in Figure 5, provide further insights into this phenomenon. The average predicted Q-value increases with larger horizons, and the Q-value variance also becomes larger, suggesting that the critic obtains stronger action discrimination but also becomes increasingly optimistic. In particular, although _H_ = 20 achieves the highest Q-value estimates, its final return is lower than that of _H_ = 5, revealing a mismatch between value estimation and actual driving performance. 

The world model loss also increases with longer rollout horizons. This does not indicate worse world model learning; instead, it reflects that longer rollouts expose the model to more diverse states generated by imperfect policies. In contrast, the extremely low loss at _H_ = 0 is mainly caused by the degenerated stationary policy, where the model only needs to reconstruct limited static observations. These results demonstrate that the rollout horizon introduces a fundamental trade-off between data augmentation and model bias: short rollouts provide reliable synthetic experiences and improve exploration, whereas excessive rollouts amplify prediction errors and lead to overestimated value functions. Therefore, _H_ = 5 provides the optimal balance between additional training signals and model reliability in our autonomous driving setting. 

### **4.4 Ablation study** 

We conduct ablation studies to investigate the contribution of each major component in the proposed framework. Specifically, we analyze the effects of real experience integration, multi-objective world model learning, temporal-difference target design, and stochastic latent representation. The complete results are summarized in Table 2, where return is the average return of 50 trajectories. 

**Effect of real and predicted data combination.** We first evaluate whether real experiences are necessary when training SAC with predicted trajectories. As shown in Table 2, removing real samples decreases performance for both short and long horizon rollout settings. With _H_ = 1, training solely on predicted data (A1) achieves limited performance, while incorporating real transitions (A2) leads to clear improvement. A similar trend is observed for _H_ = 5 (A3 vs. A4), although the performance gap becomes smaller because longer rollouts generate more synthetic samples. These results demonstrate that real experiences provide essential grounding signals, while predicted trajectories effectively improve data efficiency by augmenting the training distribution. 

**Effect of multi-objective world model learning.** We further investigate the influence of different RSSM supervision signals by selectively detaching the gradient flow from individual prediction heads. Detaching the observation reconstruction gradient causes a severe performance degradation (A5), 

11 

Table 2: Ablation study results across experiment configurations. 

|**ID**|_H_|**Real Data**|**Gradient Heads**|**TD Target**|**Return**|
|---|---|---|---|---|---|
|A1|1|✗|decoder+reward+cont|1-step|167.3|
|A2|1|✓|decoder+reward+cont|1-step|226.2|
|A3|5|✓|decoder+reward+cont|_n_-step|**371.4**|
|A4|5|✗|decoder+reward+cont|_n_-step|347.5|
|A5|5|✓|reward+cont|_n_-step|_−_5.6|
|A6|5|✓|decoder only|_n_-step|280.8|
|A7|5|✓|decoder+reward+cont|1-step|331.6|
|A8|5|✓|decoder+reward+cont|_n_-step|303.4|


_Note._ A8 uses a continuous Gaussian stochastic latent state; all others use discrete latents. ✓ = enabled, ✗ = disabled. 

indicating that reconstruction provides an essential regularization signal for learning meaningful latent representations. Although the reward and continuation prediction tasks directly relate to control objectives, their gradients alone are insufficient to maintain a useful representation space. In contrast, detaching reward and continuation gradients while retaining only the reconstruction signal results in moderate performance degradation (A6), suggesting that task-oriented prediction gradients provide additional guidance by encouraging the latent dynamics to preserve decision-relevant information. 

**Effect of temporal target estimation.** We compare the proposed _n_ -step targets for predicted trajectories (A3) with conventional one-step TD targets (A7). The results show that n-step targets achieve better performance, demonstrating that latent rollouts contain useful future information beyond immediate transitions. By propagating rewards over multiple predicted steps, the critic can obtain more informative value estimates and better exploit the learned dynamics. 

**Effect of stochastic latent representation.** Finally, we compare the default discrete stochastic latent representation (A3) with a continuous Gaussian latent variable (A8). Replacing the discrete latent state with a continuous Gaussian distribution reduces the final performance, suggesting that the discrete stochastic representation provides a more expressive and stable latent space for modeling complex driving dynamics. This observation is consistent with previous findings that categorical latent states can better capture multi-modal future transitions in partially observable environments. 

### **4.5 Analysis of Model Bias in Rollouts** 

To investigate how model bias accumulates during rollouts, we perform a trajectory-level comparison between real and predicted transitions. Specifically, we randomly sample 512 trajectories from the replay buffer and initialize rollouts from the same real states. The world model then generates latent rollouts using exactly the same action sequences as those executed in the real environment. This enables a step-wise comparison between predicted and real trajectories without introducing policy distribution mismatch. 

Figure 6 presents the discrepancy between real and predicted trajectories in terms of latent representation similarity, reward prediction error, and reward distribution. The cosine similarity between real and predicted hidden states gradually decreases from 0.438 at the first predicted step to 0.371 after five steps. This indicates that the latent dynamics remain consistent with the real environment in short horizons but gradually accumulate prediction errors during longer rollouts. 

Similarly, the reward prediction error increases with rollout depth. The mean absolute error grows from 0.855 at the first step to 3.698 at the fifth step, representing more than a four-fold increase. Meanwhile, the variance of the predicted rewards is increasing, indicating that uncertainty grows as the rollout process extends. 

Further analysis of reward distributions reveals that the world model accurately captures frequent driving rewards around zero, which correspond to normal lane-following and vehicle-control behaviors. However, discrepancies emerge in sparse negative reward regions. The predicted distribution assigns higher probability to extreme negative rewards, indicating that the world model tends to overestimate the occurrence of safety-critical failures such as collisions or off-road events. This conservative prediction behavior results from the difficulty of accurately modeling rare transition events with limited real interactions. 

12 


Figure 6: Comparison between real and predicted trajectories: latent representation similarity, reward prediction error, and reward distribution over rollout depth. 

These results demonstrate that latent rollouts provide reliable short-term experience augmentation, while prediction errors gradually accumulate with longer rollouts. This explains the observed tradeoff between rollout horizon and policy performance: moderate horizons improve data efficiency by providing additional training signals, whereas excessive rollouts introduce biased value estimation and limit policy optimization. 

## **5 Conclusion** 

This paper proposed Dreamer-SAC, a model-based off-policy reinforcement learning framework for autonomous driving that combines the data efficiency of latent world models with the stability and experience reuse capability of off-policy learning. Unlike conventional Dreamer-style approaches that optimize policies solely using model-generated rollouts, the proposed framework jointly leverages real driving experiences and latent rollouts through SAC optimization. By generating short-horizon rollouts from real trajectory states and incorporating n-step target estimation, Dreamer-SAC improves policy learning while reducing the adverse effects of accumulated model errors. Experiments conducted in the MetaDrive autonomous driving environment demonstrate that the proposed approach consistently outperforms representative reinforcement learning baselines, including DreamerV3, SAC, and PPO. Further ablation studies verify the importance of real experience integration, multi-objective RSSM learning, and n-step target estimation. The results also reveal an inverted-U relationship between rollout horizon and policy performance, indicating that short-horizon rollouts provide an effective balance between additional training signals and model bias. 

Future work will focus on developing adaptive rollout strategies that dynamically adjust rollout length according to model reliability and uncertainty. In addition, evaluating the proposed framework with larger-scale real-world driving datasets and more diverse traffic scenarios will be essential for further improving the practicality and generalization capability of model-based reinforcement learning for autonomous vehicles. 

13 

## **References** 

- [1] Daniel J Fagnant and Kara Kockelman. Preparing a nation for autonomous vehicles: opportunities, barriers and policy recommendations. _Transportation Research Part A: Policy and Practice_ , 77:167–181, 2015. 

- [2] Riccardo Donà and Biagio Ciuffo. Virtual testing of automated driving systems: A survey on validation methods. _IEEE Access_ , 10:40149–40169, 2022. 

- [3] B Ravi Kiran, Ibrahim Sobh, Victor Talpaert, Patrick Mannion, Ahmad A Al Sallab, Senthil Yogamani, and Patrick Pérez. Deep reinforcement learning for autonomous driving: A survey. _IEEE Transactions on Intelligent Transportation Systems_ , 23(6):4909–4926, 2021. 

- [4] Rui Zhao, Yun Li, Yuze Fan, Fei Gao, Manabu Tsukada, and Zhenhai Gao. A survey on recent advancements in autonomous driving using deep reinforcement learning: Applications, challenges, and solutions. _IEEE Transactions on Intelligent Transportation Systems_ , 25(12): 19365–19398, 2024. 

- [5] Tianhao Feng, Wenyi Wang, and Yi Yang. A survey of world models for autonomous driving. _arXiv preprint arXiv:2501.11260_ , 2025. 

- [6] David Gonzalez, Joshué Pérez, Vicente Milanés, and Fawzi Nashashibi. A review of motion planning techniques for automated vehicles. _IEEE Transactions on Intelligent Transportation Systems_ , 17(4):1135–1145, 2016. 

- [7] Wilko Schwarting, Javier Alonso-Mora, and Daniela Rus. Planning and decision-making for autonomous vehicles. _Annual Review of Control, Robotics, and Autonomous Systems_ , 1: 187–210, 2018. 

- [8] Paolo Falcone, Francesco Borrelli, Jahan Asgari, Hongtei Eric Tseng, and Davor Hrovat. Predictive active steering control for autonomous vehicle systems. _IEEE Transactions on Control Systems Technology_ , 15(3):566–580, 2007. 

- [9] Luc Le Mero, Dewei Yi, Mehrdad Dianati, and Alexandros Mouzakitis. A survey on imitation learning techniques for end-to-end autonomous vehicles. _IEEE Transactions on Intelligent Transportation Systems_ , 23(9):14128–14147, 2022. 

- [10] Felipe Codevilla, Matthias Müller, Antonio López, Vladlen Koltun, and Alexey Dosovitskiy. End-to-end driving via conditional imitation learning. In _2018 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 1–9. IEEE, 2018. 

- [11] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [12] Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor. In _International Conference on Machine Learning_ , pages 1861–1870, 2018. 

- [13] Michael Janner, Justin Fu, Marvin Zhang, and Sergey Levine. When to trust your model: Model-based policy optimization. In _Advances in Neural Information Processing Systems_ , volume 32, 2019. 

- [14] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _International Conference on Machine Learning_ , pages 2555–2565. PMLR, 2019. 

- [15] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. _arXiv preprint arXiv:1912.01603_ , 2019. 

- [16] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse control tasks through world models. _Nature_ , 640(8059):647–653, 2025. 

14 

- [17] Zeyu Gao, Yao Mu, Chen Chen, Jingliang Duan, Ping Luo, Yanfeng Lu, and Shengbo Eben Li. Enhance sample efficiency and robustness of end-to-end urban autonomous driving via semantic masked world model. _IEEE Transactions on Intelligent Transportation Systems_ , 25 (10):13067–13079, 2024. 

- [18] Zhenjie Yang, Xiaosong Jia, Qifeng Li, Xue Yang, Maoqing Yao, and Junchi Yan. Raw2drive: Reinforcement learning with aligned world models for end-to-end autonomous driving (in carla v2). _arXiv preprint arXiv:2505.16394_ , 2025. 

- [19] Nathan Lambert, Brandon Amos, Omry Yadan, and Roberto Calandra. The challenges of exploration for model-based reinforcement learning. _arXiv preprint arXiv:2008.06036_ , 2020. 

- [20] Leslie Pack Kaelbling, Michael L Littman, and Anthony R Cassandra. Planning and acting in partially observable stochastic domains. _Artificial Intelligence_ , 101(1-2):99–134, 1998. 

- [21] Quanyi Li, Zhenghao Peng, Lan Feng, Qihang Zhang, Zhenghai Xue, and Bolei Zhou. Metadrive: Composing diverse driving scenarios for generalizable reinforcement learning. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 45(3):3461–3475, 2022. 

15 

