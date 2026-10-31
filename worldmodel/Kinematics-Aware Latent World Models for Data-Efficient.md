---
title: "Kinematics-Aware Latent World Models for Data-Efficient Autonomous Driving"
date: "2026-03-07"
authors: "Jiazhuo Li; Linjiang Cao; Qi Liu; Xi Xiong"
url: https://arxiv.org/abs/2603.07264
pdf: https://arxiv.org/pdf/2603.07264
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.07264)** / [論文ページ](https://arxiv.org/abs/2603.07264)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Kinematics-Aware Latent World Models for Data-Efficient Autonomous Driving** 

Jiazhuo Li, Linjiang Cao, Qi Liu, and Xi Xiong 

**_Abstract_ — Data-efficient learning remains a central challenge in autonomous driving due to the high cost and safety risks of large-scale real-world interaction. Although world-model-based reinforcement learning enables policy optimization through latent imagination, existing approaches often lack explicit mechanisms to encode spatial and kinematic structure essential for driving tasks. In this work, we build upon the Recurrent State-Space Model (RSSM) and propose a kinematics-aware latent world model framework for autonomous driving. Vehicle kinematic information is incorporated into the observation encoder to ground latent transitions in physically meaningful motion dynamics, while geometry-aware supervision regularizes the RSSM latent state to capture task-relevant spatial structure beyond pixel reconstruction. The resulting structured latent dynamics improve long-horizon imagination fidelity and stabilize policy optimization. Experiments in a driving simulation benchmark demonstrate consistent gains over both model-free and pixel-based world-model baselines in terms of sample efficiency and driving performance. Ablation studies further verify that the proposed design enhances spatial representation quality within the latent space. These results suggest that integrating kinematic grounding into RSSM-based world models provides a scalable and physically grounded paradigm for autonomous driving policy learning.** 

## I. INTRODUCTION 

Despite rapid progress in autonomous driving, achieving reliable decision-making in long-tail and safety-critical scenarios remains a fundamental challenge [1]. Although recent systems demonstrate strong performance within restricted operational domains, failures still occur under distribution shift, including rare road user behaviors and extreme environmental conditions [2]. Reinforcement learning (RL) provides a principled framework for sequential decision-making through interaction-driven optimization [3]. However, its application to autonomous driving is severely constrained by data efficiency. Learning robust driving policies typically requires massive environment interactions, yet large-scale real-world data collection is costly, time-consuming, and potentially unsafe. While high-fidelity simulators reduce safety risks, they remain computationally expensive, often requiring millions of interaction steps for policy convergence. This interaction bottleneck fundamentally limits the scalability of pure model-free RL in complex driving environments. 

To address the interaction bottleneck, world models (WM) learn compact latent representations of environment dynamics, enabling policy optimization through imagination rollouts instead of repeated real-environment interaction. By internalizing transition dynamics in latent space, WMs 

J. Li, L. Cao, Q. Liu and X. Xiong are with the Key Laboratory of Road and Traffic Engineering, Ministry of Education, Tongji University, Shanghai, China, emails: 2534457@tongji.edu.cn, 2431743@tongji.edu.cn, liu ~~q~~ i@tongji.edu.cn, xi ~~x~~ iong@tongji.edu.cn. 

significantly improve sample efficiency and support longhorizon reasoning. Building on this paradigm, we propose a task-relevant world-model framework tailored for autonomous driving. Unlike purely generative latent modeling, our approach explicitly aligns latent dynamics with spatial and kinematic structures critical for driving tasks. Visual observations are fused with vehicle kinematic states to construct a kinematics-grounded latent representation of the driving scene, while structured spatial supervision regularizes latent transitions toward geometrically consistent and driving-relevant semantics. Policy learning is then performed via imagination rollouts in the structured latent space, enabling data-efficient and dynamically coherent decisionmaking with reduced reliance on real-environment interaction. 

Existing approaches to autonomous driving decisionmaking broadly fall into several paradigms. Model-based control has long served as a foundation, where optimizationbased methods such as model predictive control (MPC) explicitly exploit system dynamics and constraints for trajectory planning and tracking [4]. In contrast, model-free RL learns policies directly from interaction data, with algorithms such as Proximal Policy Optimization (PPO) [5] and Soft Actor-Critic (SAC) [6] enabling stable policy optimization. Bridging control and learning, planning with learned dynamics integrates neural networks with search or modelbased rollouts [7], [8]. To further improve data efficiency, WM learn compact latent representations of environment dynamics, supporting planning or imagination-based policy optimization. Representative approaches include PlaNet and Dreamer [9]–[11], which perform behavior learning via latent imagination, as well as large-scale generative world models for interactive environment synthesis [12]. Building on these advances, world-model-based methods have been applied to autonomous driving. Prior works enhance robustness through semantic masking or representation alignment between raw observations and privileged features [13], [14]. However, existing approaches primarily focus on representation filtering or generative modeling, without explicitly constraining latent dynamics to maintain geometrically consistent and physically grounded structures essential for closed-loop vehicle control. 

Motivated by these observations, we build upon the Recurrent State-Space Model (RSSM) [11] and propose a task-relevant world-model framework that explicitly enforces spatial and kinematic consistency in latent dynamics for autonomous driving. Rather than treating latent representations as purely generative abstractions, our approach aligns the latent transition with driving-relevant spatial structure. Specifically, we introduce two complementary mechanisms. 

First, low-dimensional vehicle kinematic states obtained from onboard sensing are incorporated into the observation encoder to ground latent transitions in physically meaningful motion dynamics. Second, structured spatial supervision is imposed through auxiliary prediction heads that estimate lane-relative geometry and neighboring vehicle states. The resulting gradients regularize the RSSM latent dynamics to preserve geometrically coherent and interaction-aware representations, thereby shaping the world model toward task-critical spatial structure. 

The contributions of this paper are summarized as follows: 

- 1) We propose a kinematics-grounded world-model framework for autonomous driving that explicitly aligns latent dynamics with decision-critical spatial and motion structure. 

- 2) We introduce kinematic grounding and geometryaware spatial regularization into RSSM-based latent transition learning, guiding the latent dynamics toward physically meaningful and interaction-aware representations. 

- 3) We empirically demonstrate significant improvements in data efficiency and driving performance, together with enhanced prediction accuracy and imagination fidelity of the learned latent dynamics. 

The remainder of this paper is organized as follows. Section II explains our modeling problems and the preliminary knowledge. Section III details our proposed framework. Section IV introduces the experimental setup and analyzes the results. Section V concludes the paper and discusses future directions. 

## II. PRELIMINARIES 

This section describes the problem we studied and preliminary knowledge of world models. In real-world driving, an ego vehicle cannot access the complete and exact state of the environment, such as the precise intentions of other drivers or occluded road regions. Instead, it must rely solely on its onboard sensors, which provide partial and noisy observations. We model the autonomous driving task as a Partially Observable Markov Decision Process (POMDP). The POMDP is defined by the tuple ( _S, A, O, T , G, R, γ_ ), where _S_ represents the true but unobservable environment state. _A_ is the action space consisting of continuous steering and throttle/brake commands **a** _t_ = ( _a_ steer _, a_ throttle) _∈_ [ _−_ 1 _,_ 1]<sup>2</sup> . _O_ is the observation space. At each time step _t_ , the ego vehicle receives an observation **o** _t_ composed of two modalities: 


where _It ∈_ R<sup>_H×W ×_3</sup> is an image from a front-facing camera, and **v** _t ∈_ R<sup>5</sup> is a vector of vehicle physics, including speed, steering angle, previous actions and yaw rate. Both of them can be directly obtained through raw sensors or physical calculations. _T_ ( _s_<sup>_′_</sup> _| s, a_ ) : _S × A × S →_ [0 _,_ 1] defines the conditional transition probability distribution over next states. _G_ ( _o | s, a_ ) : _S × A × O →_ [0 _,_ 1] defines the probability of observing given state and action. _R_ : _S × A →_ R is the reward function balancing progress, 

safety, and rule compliance, while _γ ∈_ [0 _,_ 1] is the discount factor. The agent’s objective is to learn a policy _π_ ( _at|o≤t_ ) that maximizes the expected cumulative discounted reward: 


Due to partial observability in driving, the true transition dynamics _T_ are unknown. To address this challenge, worldmodel-based reinforcement learning approximates belief dynamics using a learned latent representation. Instead of explicitly maintaining a probability distribution over environment states, the agent learns a compact latent variable _s_ ˆ _t ∈S_ latent that summarizes past information. 

The world model usually includes the following components: a representation model _p_ (ˆ _st | s_ ˆ _t−_ 1 _, at−_ 1 _, ot_ ) that maps high-dimensional observations into a compact latent state; a latent transition model _p_ (ˆ _st_ +1 _| s_ ˆ _t, at_ ) that predicts future latent states; an observation model that reconstructs or predicts observations _p_ (ˆ _ot | s_ ˆ _t_ ); and a reward model _p_ (ˆ _rt | s_ ˆ _t, at_ ) for value estimation. In some tasks, there also has a continue model _p_ (ˆ _ct | s_ ˆ _t, at_ ) that predicts termination signal. Through this learned latent dynamics model, the agent can perform imagination rollouts entirely in latent space, enabling policy optimization without requiring real environment interaction at every step. 

## III. THE KINEMATICS-AWARE LATENT WORLD MODELS 

This section provides a detailed introduction to our proposed kinematics aware world model, which integrates multi-modal encoding, RSSM-based dynamics with drivingspecific supervision, and latent-space policy learning to enable data-efficient training with explicit driving semantics. 

## _A. Multi-modal Encoding_ 

To address the limitations of pure image input, we propose an enhanced input representation that fuses image features with 5-dimensional vehicle physical information. These physical states can be accurately and efficiently obtained from onboard sensors (e.g., IMU, odometry), offering a reliable and low-cost alternative to inferring them from pixels. 

Specifically, the image encoder processes the front-facing camera image _It_ through a convolutional neural network (CNN): _f_ img = CNN( _It_ ; _θ_ img). The physics encoder processes the normalized vehicle physics vector _vt_ through a multilayer perceptron (MLP): _f_ phys = MLP( _vt_ ; _θ_ phys). Finally, the visual and physics features are concatenated to form the unified observation embedding: 


By incorporating this information explicitly, the world model does not have to infer dynamics solely from visual observations, allowing it to focus on learning environmental dynamics and interactions. 

## _B. Latent Dynamics Modeling_ 

The encoded observations embedding is then fed into a Recurrent State-Space Model (RSSM) [11]. At each time step, the model maintains a deterministic hidden state _ht_ that summarizes past information, and a stochastic state _zt_ that captures uncertainty. The transition is defined as: 


where _fθ_ is a recurrent neural network. _zt_ is sampled from the posterior distribution during training, and prior distribution during inference. ( _ht, zt_ ) together form the latent state. 

The basic world model loss consists of prediction loss and KL regularization loss: 


where _L_ pred _,t_ includes the negative log-likelihood of observation reconstruction _−_ ln _pθ_ (ˆ _ot | ht, zt_ ), reward prediction _−_ ln _pθ_ (ˆ _rt | ht, zt_ ), and termination signal prediction _−_ ln _pθ_ (ˆ _ct | ht, zt_ ). The _L_ KL _,t_ = _D_ KL( _qθ_ ( _zt | ht, et_ ) _∥ pθ_ (ˆ _zt | ht_ )) is the KL divergence between the posterior and prior distribution, constraining the encoder to avoid extracting irrelevant information from observations and enhancing the consistency and predictability of the latent state. 

## _C. Driving-Specific Supervision Heads_ 

Relying solely on pixel reconstruction often neglects structured semantic information and cannot guarantee geometric consistency required for long-horizon interaction prediction, as critical driving elements such as lane boundaries and surrounding vehicles occupy only a small fraction of the visual input. We extend the output heads of the basic world model by adding two task-specific detection heads. The gradients of these two new heads are backpropagated to the world model, guiding the latent state to explicitly focus on key driving scene information. 

A Lane Detection Head is designed to predict key lanerelated information from the latent state, which are three critical indicators for lane keeping in autonomous driving: 


where _d_<sup>ˆ</sup> left, _d_<sup>ˆ</sup> right are distances to left and right lane boundaries, and ∆<sup>ˆ</sup> heading is the heading angle difference relative to the lane. 

A Vehicle Detection Head is designed to predict the key information of surrounding vehicles from the latent state, which is critical for collision avoidance: 


specifically, the head predicts a 12-dimensional vector representing the states of up to three surrounding vehicles, with 

each vehicle characterized by four attributes: the relative positions and relative speed along the ego vehicle’s longitudinal and lateral axes. 

It is worth noting that these signals are used only during training as auxiliary supervision and does not need to be provided during testing. We normalize all target values to eliminate dimensional heterogeneity across outputs. Both heads employ symlog MSE loss: 


where symlog( _x_ ) = sign( _x_ ) ln( _|x|_ + 1). The total training loss _L_ total of the world model is then defined as: 


Fig. 1. World Model Learning. The network encodes multi-modal inputs into latent states and decodes multiple task-specific outputs including reconstruction, prediction, and driving-aware supervision signals. 

## _D. Actor-Critic learning_ 

Same as DreamerV3 [11], we train an actor network _π_ ( _a | ϕ_ ) and critic network _V_ ( _ϕ_ ) using imagined trajectories: The critic estimates state values using _λ_ -returns: 


with the _λ_ -return defined as: 


where _γ_ is the discount factor, _λ ∈_ [0 _,_ 1] is the trace decay parameter, _rτ_ is the immediate reward, _vψ_ ( _sτ_ +1) is the bootstrap value estimate from the target network, and _H_ denotes the length of imagined trajectories. Intuitively, _λ_ -return considers cumulative rewards within finite-length imagined trajectories, while using _vψ_ ( _sn_ ) at the endpoint to approximate future returns infinitely far ahead, thereby providing a global value estimate for each state. 

We adopt the dynamics gradient mode, which directly maximizes the value function along the imagined trajectory. 

The actor loss is defined as the negative expected advantage, weighted by the cumulative product of discounts and continuation probabilities: 


where _wτ_ = _γ_<sup>_τ−t_�</sup><sup>_τ_</sup> _k_ =<sup>_−_</sup> _t_<sup>1</sup><sup>_ck_isthecumulativeweight,</sup><sup>_ck_is</sup> the predicted continuation probability from the continuation head. 


**Algorithm 1** Kinematics-Aware World Model **Require:** environment, initial policy, hyperparameters **Ensure:** trained policy 

- 1: Initialize replay buffer _D_ 

- 2: Initialize world model parameters _θ_ , actor parameters _ϕ_ , critic parameters _ψ_ 

- 3: Prefill _D_ with random actions 

- 4: **for** each iteration _k_ = 1 _, . . . , K_ **do** 

- 5: Sample batch _{_ ( _ot, at, rt_ ) _}_<sup>_T_</sup> _t_ =1<sup>from</sup><sup>_D_</sup> 

- 6: / World model learning 

- 7: Encode **e** _t ←_ CONCAT (CNN( _It_ ; _θ_ img) _,_ MLP( **v** _t_ ; _θ_ phys)) 8: Compute posterior and prior states via RSSM 

- 9: Compute losses: _L_ basic _, L_ lane _, L_ nbr 

- 10: Update _θ_ by minimizing total loss 

- 11: / Behavior learning in imagination 

- 12: Sample start states from posterior 

- 13: Generate imagined trajectory of length _H_ using actor and RSSM prior 

- 14: Compute _λ_ -returns and advantages 

- 15: Update critic _ψ_ via regression to targets 

Fig. 2. Actor-Critic Learning. Imagined trajectories generated by the world model enable policy optimization in latent space. The actor predicts actions _π_ ( _a | ϕ_ ) while the critic estimates values _V_ ( _ϕ_ ) via _λ_ -returns, allowing gradient-based updates without real environment interaction. 

- 16: Update actor _ϕ_ via dynamics gradient 

- 17: / Environment interaction (parallel) 

- 18: Rollout policy in environments for _N_ steps, adding to _D_ 

19: **end for** 

## _E. Reward Design_ 

The reward function _R_ in our driving task is composed of four components that balance progress, safety, and rule compliance: 

The forward distance reward _R_ 1 encourages making progress along the lane centerline: 


where _st_ is the longitudinal projection of the vehicle onto the lane centerline, and **1** pos indicates correct driving direction. The speed reward _R_ 2 encourages maintaining an appropriate speed: 


where _v_ is the current speed and _v_ max = 80 km _/_ h. 

The lane center offset penalty _R_ 3 penalizes deviation from the lane center: 


where _yt_ denotes lateral offset and _w_ lane is lane width. 

The termination reward/punishment _R_ 4 provides a sparse terminal reward for completing the route or penalty for violations: 


The total reward for each timestep is: 


## IV. NUMERICAL RESULTS 

This section provides a detailed introduction to our experimental setup, model configuration, comparative experiment, ablation study and analysis of related results. 

## _A. Experimental Setup_ 

Our experiments are conducted in the MetaDrive [15] autonomous driving simulation environment. The map we selected featuring multi-lane roads, moderate traffic density, and a mix of straight and curved segments, ensuring the task is sufficiently challenging while remaining tractable. 

Key environment parameters include a straight and curve map string, traffic density of 0.1, action repeat of 20, image resolution of 120 _×_ 80 pixels, time limit of 6000 environment steps, forward distance reward _βd_ = 1 _._ 0, speed reward _βc_ = 0 _._ 1, center offset penalty _βc_ = 1 _._ 0, crash and out of road penalty _p_ crash _, p_ out = 40 _._ 0. 

## _B. Model Configurations_ 

The world model follows the DreamerV3 architecture with the enhancements described in Section 3. The CNN encoder and decoder employ a depth of 32, kernel size of 4, minimum resolution of 4, and SiLU activations. The MLP consists of 2 layers with 256 units, SiLU activations, and layer normalization. The RSSM uses a deterministic state size of 512, stochastic state size of 32 _×_ 32, and recurrent depth of 1. Both actor and critic networks are configured with 2 layers of 512 units and layer normalization. 

We use a batch size of 16 sequences, each of length 64. The learning rate is set to 1 _×_ 10<sup>_−_4</sup> . Optimization is 

performed using Adam. The imagination horizon is set to _H_ = 15 steps. For GAE, we use discount factors _γ_ = 0 _._ 997 and _λ_ = 0 _._ 95. The KL regularization applies free bits of 1 _._ 0, with dynamics scale of 0 _._ 5 and representation scale of 0 _._ 1. All models are trained for 1.6 million environment steps (equivalent to 80,000 interactive steps due to action repeat 20). 

## _C. Comparative Experiments_ 

To demonstrate sample efficiency, we compare our framework against a standard model-free baseline: PPO implemented in Stable-Baselines3. PPO uses the same observation data, encoder and Actor Critic architecture of the same scale, and the same Metadrive configuration. PPO trains for 300000 agent steps with default hyperparameters: learning rate 2 _._ 5 _×_ 10<sup>_−_4</sup> , _n_ steps = 256, batch size 64, and 10 epochs per update. 

The results in Figure 3 indicate that the world-model-based framework exhibits a relatively faster convergence rate. It reaches a stable high return (nearing 200) in just 80,000 real-environment steps. In contrast, PPO requires 300000 interaction steps to converge to a level below 150 scores. 


Fig. 3. A comparison between our model with PPO. The solid lines represent the averaged return, while the shaded area indicates the variability around the mean. 

## _D. Ablation Studies_ 

We conducted a series of ablation experiments, and the results are presented in Figure 4 and Table I. Our ablation study compares four model variants: ImgOnly, a baseline using solely images with reward and continuation heads; Img+Head, which adds lane and neighbor detection heads to image input; and Img+Head+Phys, our full framework integrating both multi-modal inputs and five supervision heads. Table I also includes an experiment where the reward and continuation heads were removed. 

The result indicate that adding the lane/neighbor heads to the image-only model improved the mean return (MR) by 9 _._ 7% and the success rate (SR) by 16 percentage points. After further incorporating physical information as input, MR 


Fig. 4. Training curves of model variants in the ablation study. ImgOnly (green) uses images input alone; Img+Head (blue) adds lane and neighbor supervision heads; Img+Head+Phys (orange) further incorporates vehicle physics as input. 

continued to improve by 12 _._ 2%, with a total improvement of 23 _._ 1%. In addition, the reward and continuation heads played a crucial role in our experiment, and the performance of the model would significantly decline if they were removed. 

These results validate that driving-specific supervision and multi-modal inputs are both critical, with their combination yielding synergistic improvements in driving performance. 

TABLE I 

ABLATION STUDY RESULTS 

|**Inp**|**ut**||**Heads**||**Metr**|**ics**|
|---|---|---|---|---|---|---|
|**Image**|Phys|Decoder|Rwd/Cont|Lane/Neigh|MR|SR|
|✓|_×_|✓|✓|_×_|176.5|0.17|
|✓|_×_|✓|✓|✓|193.6|0.33|
|✓|✓|✓|_×_|✓|172.6|0.18|
|✓|✓|✓|✓|✓|217.2|0.49|


## _E. Synthetic Scenarios_ 

We compare the imagination quality of different model variants. As illustrated in Figure 5, the world model trained with only image input (ImgOnly) generates physically inconsistent rollouts. For example, when the ego car is preparing to overtake, the position of the preceding vehicle becomes blurred and undergoes abrupt, unrealistic shifts. In lanechanging scenarios, the model frequently confuses yellow solid lines with white dashed lines. In contrast, the combination of vehicle kinematics and auxiliary supervision effectively alleviates these problems. The imagined trajectories now maintain stable and physically plausible states for surrounding vehicles during interactions, and correctly preserve the color and type of lane markings during maneuvers, demonstrating improved physical grounding and semantic consistency in the latent space. 

## V. CONCLUSIONS 

This paper presents a task-relevant world-model framework for autonomous driving that improves latent repre- 


Fig. 5. Comparison of imagination quality across model variants. Top row: ImgOnly generates physically inconsistent rollouts with blurred vehicle positions (left) and confused lane markings (right). Bottom row: Img+Head+Phys produces stable, physically plausible predictions with correct semantic preservation of surrounding vehicles and lane markings. 

sentation learning through structured spatial supervision and kinematics-aware input. The proposed approach encourages the world model to capture driving-relevant spatial semantics instead of relying solely on visual reconstruction objectives. Simulation experiments demonstrate improved sample efficiency, faster convergence, and superior driving performance compared to baselines of the world-model only images and a model-free PPO agent, highlighting the benefits of explicitly structured supervision for safety-critical driving tasks. 

Future work will focus on tighter integration of vehicle dynamics and world models to improve physical consistency in latent imagination. We also plan to extend the framework to offline learning settings, leveraging large-scale driving datasets to enhance data efficiency and safety. In addition, scaling the approach to multi-agent scenarios will be an important direction for modeling interactive traffic behaviors in complex environments. 

## REFERENCES 

- [1] A. Kuznietsov, B. Gyevnar, C. Wang, S. Peters, and S. V. Albrecht, “Explainable ai for safe and trustworthy autonomous driving: A systematic review,” _IEEE Transactions on Intelligent Transportation Systems_ , vol. 25, no. 12, pp. 19 342–19 364, 2024. 

   - [9] D. Hafner, T. Lillicrap, I. Fischer, R. Villegas, D. Ha, H. Lee, and J. Davidson, “Learning latent dynamics for planning from pixels,” in _International conference on machine learning_ . PMLR, 2019, pp. 2555–2565. 

   - [10] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Dream to control: Learning behaviors by latent imagination,” _arXiv preprint arXiv:1912.01603_ , 2019. 

   - [11] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap, “Mastering diverse control tasks through world models,” _Nature_ , vol. 640, no. 8059, pp. 647–653, 2025. 

   - [12] J. Bruce, M. D. Dennis, A. Edwards, J. Parker-Holder, Y. Shi, E. Hughes, M. Lai, A. Mavalankar, R. Steigerwald, C. Apps _et al._ , “Genie: Generative interactive environments,” in _Forty-first International Conference on Machine Learning_ , 2024. 

   - [13] Z. Gao, Y. Mu, C. Chen, J. Duan, P. Luo, Y. Lu, and S. E. Li, “Enhance sample efficiency and robustness of end-to-end urban autonomous driving via semantic masked world model,” _IEEE Transactions on Intelligent Transportation Systems_ , vol. 25, no. 10, pp. 13 067–13 079, 2024. 

   - [14] Z. Yang, X. Jia, Q. Li, X. Yang, M. Yao, and J. Yan, “Raw2drive: Reinforcement learning with aligned world models for end-to-end autonomous driving (in carla v2),” _arXiv preprint arXiv:2505.16394_ , 2025. 

   - [15] Q. Li, Z. Peng, L. Feng, Q. Zhang, Z. Xue, and B. Zhou, “Metadrive: Composing diverse driving scenarios for generalizable reinforcement learning,” _IEEE transactions on pattern analysis and machine intelligence_ , vol. 45, no. 3, pp. 3461–3475, 2022. 

- [2] R. Xu, H. Lin, W. Jeon, H. Feng, Y. Zou, L. Sun, J. Gorman, E. Tolstaya, S. Tang, B. White _et al._ , “Wod-e2e: Waymo open dataset for end-to-end driving in challenging long-tail scenarios,” _arXiv preprint arXiv:2510.26125_ , 2025. 

- [3] R. Zhao, Y. Li, Y. Fan, F. Gao, M. Tsukada, and Z. Gao, “A survey on recent advancements in autonomous driving using deep reinforcement learning: Applications, challenges, and solutions,” _IEEE Transactions on Intelligent Transportation Systems_ , vol. 25, no. 12, pp. 19 365– 19 398, 2024. 

- [4] P. Falcone, F. Borrelli, J. Asgari, H. E. Tseng, and D. Hrovat, “Predictive active steering control for autonomous vehicle systems,” _IEEE Transactions on control systems technology_ , vol. 15, no. 3, pp. 566–580, 2007. 

- [5] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [6] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, “Soft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor,” in _International conference on machine learning_ , 2018, pp. 1861–1870. 

- [7] D. Silver, A. Huang, C. J. Maddison, A. Guez, L. Sifre, G. Van Den Driessche, J. Schrittwieser, I. Antonoglou, V. Panneershelvam, M. Lanctot _et al._ , “Mastering the game of go with deep neural networks and tree search,” _nature_ , vol. 529, no. 7587, pp. 484–489, 2016. 

- [8] D. Ha and J. Schmidhuber, “Recurrent world models facilitate policy evolution,” _Advances in neural information processing systems_ , vol. 31, 2018. 

