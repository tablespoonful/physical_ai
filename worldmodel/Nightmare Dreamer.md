---
title: "Nightmare Dreamer: Dreaming About Unsafe States And Planning Ahead"
date: "2026-01-08"
authors: "Oluwatosin Oseni; Shengjie Wang; Jun Zhu; Micah Corah"
url: https://arxiv.org/abs/2601.04686
pdf: https://arxiv.org/pdf/2601.04686
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.04686)** / [論文ページ](https://arxiv.org/abs/2601.04686)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Nightmare Dreamer: Dreaming About Unsafe States And Planning Ahead 

Oluwatosin Oseni<sup>_∗_1</sup> , Shengjie Wang<sup>_∗_2</sup> , Jun Zhu<sup>2</sup> , and Micah Corah<sup>1</sup> 

> 1Colorado School of Mines 2Tsinghua University 

> _∗_ Equal contribution. Corresponding author: oluwatosin_oseni@mines.edu 

**_Abstract_ —Reinforcement Learning (RL) has shown remarkable success in real-world applications, particularly in robotics control. However, RL adoption remains limited due to insufficient safety guarantees. We introduce** **_Nightmare Dreamer_ , a modelbased Safe RL algorithm that addresses safety concerns by leveraging a learned world model to predict potential safety violations and plan actions accordingly.** **_Nightmare Dreamer_ achieves nearly zero safety violations while maximizing rewards.** **_Nightmare Dreamer_ outperforms model-free baselines on Safety Gymnasium tasks using only image observations, achieving nearly a 20x improvement in efficiency.** 

## I. INTRODUCTION 

Reinforcement Learning (RL) has shown impressive success across various domains, from surpassing human performance in games like Go [24], to champion-level drone racing [19], and advanced robotic tasks like catching dynamic objects with dexterous hands [20]. Recent model-based RL methods, such as DreamerV3 [15], further extend these capabilities—enabling robots to learn locomotion in hours and solving complex tasks like Minecraft diamond collection. Notably, RL has also demonstrated real-world impact in areas like plasma control for nuclear fusion [8] and autonomous navigation of stratospheric balloons [4]. 

Despite these successes, deployment of RL in real-world applications remains limited due to fundamental safety concerns. The exploratory nature of RL algorithms can lead agents to adopt dangerous or harmful behaviors during training, posing unacceptable risks in safety-critical environments [9]. 

This challenge is notable when deploying RL agents in environments where they interact with or operate around humans, such as autonomous vehicles, robotic assistants, or industrial control systems. Safe Reinforcement Learning (SafeRL) addresses these concerns by formulating the learning problem as a Constrained Markov Decision Process (CMDP) [2], where agents must maximize rewards while satisfying explicit safety constraints. Current approaches primarily rely on two methodologies: Lagrangian-based methods known as the primal-dual method [5] that use dual optimization to balance rewards and constraints with algorithms like PPO-Lag and TRPO-Lag [21], and primal methods that attempt to apply the cost constraints with clever design of the objective functions as well as updating the policy without much use of dual variables [26, 6]. State-of-art Model-free approaches like CPO [1] and PPO-Lagrangian [21], while theoretically sound, suffer from sample inefficiency and struggle to maintain safety guarantees throughout training, particularly in high-dimensional visual 

environments. Conversely, model-based methods often fail to fully exploit the predictive capabilities of learned world models for proactive safety planning, limiting their effectiveness in preventing future constraint violations. To address these limitations, we introduce _Nightmare Dreamer_ , a model-based SafeRL algorithm that leverages learned world models to predict potential safety violations and plan actions accordingly. Our key innovation lies in the integration of dual specialized actors—a control actor optimized for reward maximization and a safe actor focused on constraint satisfaction—with an online planning algorithm that switches between policies based on predicted future costs. Unlike existing approaches that treat safety as a reactive constraint, _Nightmare Dreamer_ proactively “dreams” about unsafe future states and takes preventive action. Our main contributions are threefold: 

- 1) A bi-actor architecture that separates reward optimization from safety constraint satisfaction, enabling more effective multi-objective learning; 

- 2) A predictive safety planning mechanism that uses world model rollouts to anticipate constraint violations; 

- 3) Demonstration that discriminator-based regularization can achieve stable training and superior performance compared to traditional behaviour cloning approaches. 

Experimental evaluation on Safety Gymnasium benchmarks demonstrates that _Nightmare Dreamer_ achieves nearly zero safety violations while maintaining competitive reward performance. Moreover, _Nightmare Dreamer_ demonstrates strong sample efficiency, surpassing baseline performance with as little as 1/20 of the interaction steps. 

## II. RELATED WORK 

Safety will play a vital role in potential everyday adoption of RL. SafeRL seeks to address this challenge by maximizing an objective function (reward) while simultaneously maintaining safety constraints (cost) below a predefined safety budget. 

**Constrained Policy Optimization (CPO)** [1], a primal method, was the first state-of-the-art policy gradient algorithm to solve the CMDP problem. CPO performs two policy updates: first, updating the policy in the direction of objective optimization (similar to Trust Region Policy Optimization (TRPO) [22]), followed by projecting the policy back into the constraint set. While CPO may outperform primal-dual methods on some tasks and converge to the safety bound, it is computationally intensive due to being a second-order method involving inversion of high-dimensional Hessians [27]. 

**Primal-dual methods** such as PPO-Lagrangian and TRPOLagrangian [21] are the standard approach for CMDP problems. These methods apply Lagrangian duality in SafeRL and have achieved considerabe success. However, primaldual methods remain challenging to apply due to parameter sensitivity in the learning rate of the Lagrangian multiplier. 

**Model-based Vision-only Safe RL** Model-based methods have historically outperformed model-free approaches due to their superior sample efficiency. LAMBDA [3] added safe planning capabilities to DreamerV1 [13], but suffers from the same suboptimal performance due to its base algorithm, DreamerV1, compared to its later improvement, DreamerV2. Safe SLAC [16] achieves comparable performance to LAMBDA, yet does not fully exploit the world model’s safety augmentation potential, bypassing imaginary rollouts that could enhance safe policy learning. Safe Dreamer [17], an adaptation of DreamerV3, combines Lagrangian methods with online planning to achieve strong performance. However, their planning is computationally intensive at inference time. 

## III. PRELIMINARY 

Safe RL tries to solve the Constrained RL problem known as Constrained Markov Decision Processes (CMDP)[2], an extension of MPD in classical RL. The CMDP can be represented in a tuple _M_ = ( _S, A, R, C,_ P _, µ, γ_ ). _S_ refers to the state space; _A_ refers to the action space; _R_ ( _r|s, a_ ) refers to the reward obtained by the agent in state s after taking action _a_ ; _C_ ( _c|s, a_ ) refer to cost which will be subject to a constraint; P( _s_<sup>_′_</sup> _|s, a_ ) is the transition probability of going to state _s_<sup>_′_</sup> from state s taking action a while receiving _R_ ( _r|s, a_ ) and _C_ ( _c|s, a_ ), _µ_ : _S →_ [0 _,_ 1] is the starting state distribution, and finally _γ ∈_ [0 _,_ 1) is the reward discount factor. We define a parametrized policy _πθ_ ( _a|s_ ) to maximize the cumulative discounted reward defined in the objective function below: 


In SafeRL, we aim to learn a policy that maximises the above objective while satisfying the constraint: 


In other words, we maintain cumulative discounted cost below a threshold known as the safety budget _b_ . We formulate the SafeRL problem as finding the optimal policy that satisfies: 


_Nightmare Dreamer_ learns a world model based on the work of Hafner et al. [12], adopting the Recurrent StateSpace Model. The world model components are parametrized by _ϵ_ and learns the world dynamics. Following the partialobservability framework of RL problems, our model takes _∼_ in the current camera image and the observation _ot_ 

_p_ ( _ot|ht, zt_ ). Then, without access to the real state, our model computes an internal state _ht, zt_ to learn the world dynamics as well as to predict future observations, rewards, and costs: 


We define the loss function, parametrized by _ϵ_ , below: 


We take a multi-agent Actor-Critic Model-based RL approach to tackle the SafeRL problem. We train a Control and Safe Actor and a Reward and Cost Critic in pairs and aim to optimize their respective policy and value functions separately. To optimize both Policy functions, we utilize the learned world model and perform trajectory rollouts under each policy. The rollouts involve sampling a real observation stored from a previous environment interaction and, with the learned dynamics, imagining future states by applying the sampled action from the actors for _H_ horizon steps. However, during environmental interaction, we switch between the Control and Safe actor to ensure safety. 

## _A. Control Actor and Safe Actor_ 

In our framework, we define two actor types. The Control actor, parametrized by _ϕ_ , executes action _ac_ sampled by _πϕ_ ( _a|s_ ) that maximizes future expected reward. On the other hand, the safe actor, parametrized by _ρ_ , aims to find an action _as_ sampled by policy _πρ_ ( _a|s_ ) that satisfies the cost constraint. Both actors are implemented as Multi-layer Perceptron (MLP) networks and employ the Exponential Linear Unit (ELU) activation function [7]. Action predictions are modeled using a truncated normal distribution. 

## _B. Planning Ahead of Risks_ 

Obstacle avoidance is a fundamental concept in robotics and planning. We pursue a similar approach (pseudo-code in Alg. 1) by leveraging the learned world model. Starting from the current observation and state embedding, we perform rollouts under the Control Policy _πϕ_ ( _a|s_ ) in the latent space. This allows us to predict the potential cost violation if we continue to act under the Control policy. If the cost violation exceeds a threshold (safety budget _b_ ), we simply perform action selection by sampling from the safe policy _πρ_ ( _a|s_ ) and 


Fig. 1: Action selection during environment interaction: The blue game pad signifies the action from the Controller, while the red game pad refers to an action from from the Safe Actor. 

sample from the Control policy _πϕ_ ( _a|s_ ) otherwise. We provide the action selection equation below: 


where _C_ at time step _t_ is predicted from the agent’s observation (Posterior), and the consequent Costs are predicted using rollouts from the learned model (Prior) without access to the observation. Figure 1 illustrates this action selection process. 

## _C. Control & Safe Actors Learning_ 

In our approach, we train two policies, a Control policy and a Safe policy. To train the Control policy, which actors aim to find a set of parameters that maximize the objective (Reward). We achieve this by directly maximizing the target Value function (gradient ascent) wrt the Control Policy, which is given by: 


Where the value function _vξ_ aims to maximise the sum of discounted rewards. Finally, we obtain the following loss function for the Control policy parametrized by _ϕ_ [14]: 


The entropy regulariser term ensures policy exploration. To perform policy improvement, we perform rollouts under the Control policy by sampling states from the buffer and performing H horizon steps from the sampled initial states. The rollouts (Imagination) involves starting from some initial state and, with the learned model (Transition Model), computing all recurring states given an Action. 

_1) Safe Actor Learning and Lagrangian Formulation:_ The Primal-dual method [5], also known as the Lagrangian method, is the most common approach to the Multi-objective CMDP problem [21]. The Lagrangian formulation balances our task objective with cost constraints and is given below: 


The Safe actor, parametrized by _ρ_ , aims to find a policy _πρ_ ( _a|s_ ) that solves the multi-objective optimization problem (8) and is given by: 


The first term aims to solve the cost constraint in (3) by directly minimizing the target value cost function wrt to the Safe Policy and is weighed by _λp_ , provided in (10). 

We achieve maximizing the control objective in 3 by **Behavior Cloning** the Control Policy _πϕ_ ( _a|s_ ) rather than direct reward maximization. This Multi-Objective loss function ensures the satisfaction of safety constraints while maintaining goal-directed behavior. 

To imitate the Control policy, we train a Discriminator network that learns to predict if an action is sampled from a Control or a Safe policy, given a current state. The discriminator outputs 0 for safe actions and 1 for control actions, and we maximize _−D_ ( _s, a_ ) wrt the Safe Policy to encourage control-like behavior. 

## **Algorithm 1:** Planning Ahead of Risks for Safe Action <u>Selection</u> 

**Input:** Current state _st_ , safety budget _bs_ **Output:** Action _at_ to execute Compute current cost _Ct_ ( _ht, zt, ot_ ) based on current observation; Initialize _C_ sum _← Ct_ ( _ht, zt, ot_ ); **for** _i ←_ 1 **to** _H_ **do** Predict next latent state using learned dynamics model; Estimate cost _Ct_ + _i_ for predicted state; _C_ sum _← C_ sum + _Ct_ + _i_ ; **end if** _C_ sum _> bs_ **then** _at ∼ πρ_ ( _a|st_ ) ; // Sample action from safe policy **else** _at ∼ πϕ_ ( _a|st_ ) ; // Sample action from Control policy **end return** _at_ ; 

_2) Lagrangian Method and Update:_ The learnable Lagrangian value _λp_ in Equ 9 is updated based with: 


where the Clip function ensures the Lagrangian value does not explode or become infinitesimal, and the online mean cost _Ck_ is defined as the moving average cost over the past _l_ = 

50 time steps. This online mean provides an estimate of the current performance of the agent that allows us to update the Lagrangian multiplier _λp_ appropriately. 

_3) Behavior Imitation via Action Discrimination:_ Discriminators are often used with adversarial networks and GANs [11] to perform image generation. We use a Discriminator term to ensure our safe policy selects actions that maximise the reward by mimicking the control policy. Our experiments show that direct Discriminator optimization provides superior regularization and generalization compared to standard behavior cloning methods like KL loss or log probability. The discriminator estimates the log likelihood of predicting if an action is sampled from the Control policy or a safe policy given a current state _st_ : 


## _D. Critics Learning_ 

The reward and cost critics are trained to predict future discounted reward and cost, respectively, given the states from the imagination rollouts, similar to the actors. The Critics are MLP networks and use ELU activation functions that output a distribution of the critic estimation. We found that this helps address the sparse nature of the cost from the environment. 

Leveraging the learned model allows us to predict the sparse cost in the environment. We compute the future discounted sum of both Cost and reward using the generalized _λ_ target values [23, 25]. using the same setup for DreamerV2 for both the Cost and Reward Value functions. 

The loss functions are thus formulated to maximize the loglikelihood of predicting the value function from the _λ_ target values. 

## VI. EXPERIMENTAL SETUP AND RESULTS 

_Nightmare Dreamer_ was trained on Safety Gymnasium, a Safe Policy Optimization Benchmark (SafePO) for Safe RL [18]. This benchmark is an extension of the now-discontinued Safety Gym previously maintained by OpenAI [10]. 

## _A. Task Description_ 

Safety Gymnasium provides several environments; we focus on the circle environment. There are 3 circle tasks with progressively difficult constraints (Fig. 2). All involve the agent moving around in a circle, but the agent incurs a cost of 1 for every step while outside a constraint boundary. There are also several agents with different control complexities (Fig. 2). 

## _B. Results_ 

Figure 3 shows experimental results of our algorithm on SafePointCircle and SafeCarCircle compared to SOTA SafeRL algorithms from the SafePo benchmark. We observe promising results, with Nightmare converging to optimal reward and cost faster than benchmark algorithms. The dashed line indicates the safety budget that cost values must remain below. Nightmare stays below this budget while achieving near-zero cost. Due to Nightmare’s computational requirements, we compare 


Fig. 3: Safety Circle 1 Reward and Cost Performance Comparison with Benchmark algorithms 

1e6 environmental interactions against 1e7 for benchmark methods. We compare our approach to SOTA model-free algorithms that are more computationally efficient than our approach but significantly less sample efficient, similar to the Safe-Dreamer [17] evaluation. 

## VII. CONCLUSION 

We introduced _Nightmare Dreamer_ , a model-based safe RL algorithm that achieves zero constraint violations while maximizing rewards from visual inputs. Our method trains two specialized actors—control and safe—using a learned world model, with a planning mechanism that switches between policies based on predicted future costs. Our key innovations is discriminator-based policy regularization approach. Experiments on Safety Gymnasium’s Circle task demonstrate faster convergence to safe policies compared to model-free baselines. While currently validated on Circle tasks, the framework provides a foundation for extending model-based safe RL to more complex environments. In the future, we hope to adapt _Nightmare Dreamer_ to other tasks and to perform tests with real-world robots and constraints and with comparison to other model-based Safe RL methods. 

## REFERENCES 

- [1] Joshua Achiam, David Held, Aviv Tamar, and Pieter Abbeel. Constrained policy optimization, 2017. URL https://arxiv.org/abs/1705.10528. 

- [2] Eitan Altman. Constrained markov decision processes. 1999. URL https://api.semanticscholar.org/CorpusID: 14906227. 

- [3] Yarden As, Ilnura Usmanova, Sebastian Curi, and Andreas Krause. Constrained policy optimization via bayesian world models, 2022. URL https://arxiv.org/abs/ 2201.09802. 

- [4] Marc G Bellemare, Salvatore Candido, Pablo Samuel Castro, Jun Gong, Marlos C Machado, Subhodeep Moitra, Sameera S Ponda, and Ziyu Wang. Autonomous navigation of stratospheric balloons using reinforcement learning. _Nature_ , 588(7836):77–82, 2020. 

- [5] D P Bertsekas. Nonlinear programming. _Journal of the Operational Research Society_ , 48(3):334–334, 1997. doi: 10.1057/palgrave.jors.2600425. URL https://doi.org/10. 1057/palgrave.jors.2600425. 

- [6] Shicong Cen, Chen Cheng, Yuxin Chen, Yuting Wei, and Yuejie Chi. Fast global convergence of natural policy gradient methods with entropy regularization, 2021. URL https://arxiv.org/abs/2007.06558. 

- [7] Djork-Arn´e Clevert, Thomas Unterthiner, and Sepp Hochreiter. Fast and accurate deep network learning by exponential linear units (elus), 2016. 

- [8] Jonas Degrave, Federico Felici, Jonas Buchli, Michael Neunert, Brendan Tracey, Francesco Carpanese, Timo Ewalds, Roland Hafner, Abbas Abdolmaleki, Diego Casas, Craig Donner, Leslie Fritz, Cristian Galperti, Andrea Huber, James Keeling, Maria Tsimpoukelli, Jackie Kay, Antoine Merle, Jean-Marc Moret, and Martin Riedmiller. Magnetic control of tokamak plasmas through deep reinforcement learning. _Nature_ , 602:414–419, 02 2022. doi: 10.1038/s41586-021-04301-9. 

- [9] Shuo Feng, Haowei Sun, Xintao Yan, Haojie Zhu, Zhengxia Zou, Shengyin Shen, and Henry X Liu. Dense reinforcement learning for safety validation of autonomous vehicles. _Nature_ , 615(7953):620–627, 2023. 

- [10] Scott Fujimoto, Edoardo Conti, Mohammad Ghavamzadeh, and Joelle Pineau. Benchmarking batch deep reinforcement learning algorithms, 2019. URL https://arxiv.org/abs/1910.01708. 

- [11] Ian J. Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio. Generative adversarial networks, 2014. 

- [12] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels, 2019. URL https://arxiv.org/abs/1811.04551. 

- [13] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination, 2020. URL https://arxiv.org/abs/ 1912.01603. 

- [14] Danijar Hafner, Timothy P Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. In _International Conference on Learning Representations_ , 2021. URL https://openreview.net/ forum?id=0oabwyZbOu. 

- [15] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models, 2024. URL https://arxiv.org/abs/2301.04104. 

- [16] Yannick Hogewind, Thiago D. Simao, Tal Kachman, and Nils Jansen. Safe reinforcement learning from pixels using a stochastic latent representation, 2022. URL https://arxiv.org/abs/2210.01801. 

- [17] Weidong Huang, Jiaming Ji, Chunhe Xia, Borong Zhang, and Yaodong Yang. Safedreamer: Safe reinforcement learning with world models, 2024. URL https://arxiv. org/abs/2307.07176. 

- [18] Jiaming Ji, Borong Zhang, Jiayi Zhou, Xuehai Pan, Weidong Huang, Ruiyang Sun, Yiran Geng, Yifan Zhong, Juntao Dai, and Yaodong Yang. Safety-gymnasium: A unified safe reinforcement learning benchmark. _arXiv preprint arXiv:2310.12567_ , 2023. 

- [19] Elia Kaufmann, Leonard Bauersfeld, Antonio Loquercio, Matthias M¨uller, Vladlen Koltun, and Davide Scaramuzza. Champion-level drone racing using deep reinforcement learning. _Nature_ , 620(7976):982–987, 2023. 

- [20] Fengbo Lan, Shengjie Wang, Yunzhe Zhang, Haotian Xu, Oluwatosin Oseni, Ziye Zhang, Yang Gao, and Tao Zhang. Dexcatch: Learning to catch arbitrary objects with dexterous hands, 2024. URL https://arxiv.org/abs/ 2310.08809. 

- [21] Alex Ray, Joshua Achiam, and Dario Amodei. Benchmarking safe exploration in deep reinforcement learning. _arXiv preprint arXiv:1910.01708_ , 7(1):2, 2019. 

- [22] John Schulman, Sergey Levine, Philipp Moritz, Michael I. Jordan, and Pieter Abbeel. Trust region policy optimization, 2017. URL https://arxiv.org/abs/1502.05477. 

- [23] John Schulman, Philipp Moritz, Sergey Levine, Michael Jordan, and Pieter Abbeel. High-dimensional continuous control using generalized advantage estimation, 2018. 

- [24] David Silver, Julian Schrittwieser, Karen Simonyan, Ioannis Antonoglou, Aja Huang, Arthur Guez, Thomas Hubert, Lucas Baker, Matthew Lai, Adrian Bolton, et al. Mastering the game of go without human knowledge. _nature_ , 550(7676):354–359, 2017. 

- [25] Richard S Sutton and Andrew G Barto. _Reinforcement learning: An introduction_ . MIT press, 2018. 

- [26] Tengyu Xu, Yingbin Liang, and Guanghui Lan. Crpo: A new approach for safe reinforcement learning with convergence guarantee, 2021. URL https://arxiv.org/abs/ 2011.05869. 

- [27] Linrui Zhang, Li Shen, Long Yang, Shixiang Chen, Bo Yuan, Xueqian Wang, and Dacheng Tao. Penalized proximal policy optimization for safe reinforcement learning, 2022. URL https://arxiv.org/abs/2205.11814. 

