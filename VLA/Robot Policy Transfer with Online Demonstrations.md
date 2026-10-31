---
title: "Robot Policy Transfer with Online Demonstrations: An Active Reinforcement Learning Approach"
date: "2025"
venue: "ICRA 2025"
url: https://doi.org/10.1109/ICRA55743.2025.11127396
pdf: https://arxiv.org/pdf/2503.12993
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2503.12993)** / [論文ページ](https://doi.org/10.1109/ICRA55743.2025.11127396)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Robot Policy Transfer with Online Demonstrations: An Active Reinforcement Learning Approach** 

Muhan Hou<sup>1</sup> , Koen Hindriks<sup>1</sup> , A.E. Eiben<sup>1</sup> , Kim Baraka<sup>1</sup> 

**_Abstract_ — Transfer Learning (TL) is a powerful tool that enables robots to transfer learned policies across different environments, tasks, or embodiments. To further facilitate this process, efforts have been made to combine it with Learning from Demonstrations (LfD) for more flexible and efficient policy transfer. However, these approaches are almost exclusively limited to** **_offline demonstrations_ collected before policy transfer starts, which may suffer from the intrinsic issue of covariance shift brought by LfD and harm the performance of policy transfer. Meanwhile, extensive work in the learning-from-scratch setting has shown that** **_online demonstrations_ can effectively alleviate covariance shift and lead to better policy performance with improved sample efficiency. This work combines these insights to introduce** **_online demonstrations_ into a policy transfer setting. We present Policy Transfer with Online Demonstrations, an active LfD algorithm for policy transfer that can optimize the timing and content of queries for online episodic expert demonstrations under a limited demonstration budget. We evaluate our method in eight robotic scenarios, involving policy transfer across diverse environment characteristics, task objectives, and robotic embodiments, with the aim to transfer a trained policy from a source task to a related but different target task. The results show that our method significantly outperforms all baselines in terms of average success rate and sample efficiency, compared to two canonical LfD methods with offline demonstrations and one active LfD method with online demonstrations. Additionally, we conduct preliminary sim-to-real tests of the transferred policy on three transfer scenarios in the real-world environment, demonstrating the policy effectiveness on a real robot manipulator.** 

## I. INTRODUCTION 

Transfer Learning (TL) has recently become increasingly popular in the robotics community. Instead of learning from scratch, TL enables a robot to utilize prior knowledge (e.g., policy) of a source situation to improve learning in a related target situation [1]. This target situation may differ from the source in various aspects, such as environments [2], [3] (e.g., from simulation to real world), tasks [4] (e.g., grabbing a bottle to grabbing a mug), or even embodiments [5] (e.g., different robot arms). 

To facilitate policy transfer, efforts have been made to combine TL with Learning from Demonstrations (LfD). These demonstrations can be utilized to acquire prior skills of the source domain [6], [7], [8], [9], [10] and accelerate the policy transfer process to the target domain [11], [4]. However, almost all previous work relies on _offline demonstrations_ , which are collected before policy transfer starts. This can lead to the covariance shift [12], as the state distribution in the demonstrations differs from that of 

> 1All authors are with the Department of Computer Science, Vrije Universiteit (VU) Amsterdam, The Netherlands, and can be contacted at m.hou@vu.nl 

the ongoing robot policy. This issue can even be further exacerbated by discrepancies in task space between the source and target domains. And to adapt the demonstration distribution to the ongoing policy update, it requires information about the learning process, which is not available a prior and can only be obtained iteratively in an online manner. By contrast, extensive work [13], [14], [15] in the learning-from-scratch setting has shown that _online demonstrations_ , which are collected during the learning process, can effectively alleviate covariance shift and produce better policy performance. Furthermore, by querying for the most suitable demonstrations during the learning process, LfD with online demonstrations can achieve the same level of policy performance with much fewer demonstrations [16] and improve sample efficiency [15]. This can be of great importance especially when the number of demonstrations is constrained by time and financial costs (e.g., data collection from human demonstrators). Therefore, we extend this idea to the scenario of policy transfer and ask the question: _will online demonstrations benefit policy transfer, and how can we realize that?_ 

To this end, we present the first active LfD algorithm for policy transfer that leverages online demonstrations for transfer learning and show that online demonstrations _will_ indeed benefit policy transfer if designed properly. Our method extends the EARLY framework [17] to the transfer learning scenario and simultaneously optimizes the problems of _when_ to query and _what_ episodic demonstrations of the target task to query during the policy transfer process (see figure 1). More specifically, a query strategy module evaluates the trajectory-based uncertainty after each episodic roll-out of the robot policy for the target task. An adaptive threshold of uncertainty is then updated to determine whether a query will be requested. If so, the query strategy module outputs the initial state of one of the recent roll-outs that the robot is most uncertain about and queries an episodic expert demonstration starting from this initial state. We test our approach in 8 robot policy transfer scenarios, involving policy transfer across diverse environment characteristics, task objectives, and robotic embodiments . Compared to EARLY and two other canonical LfD baselines with offline demonstrations, our method achieves significantly higher success rate and sample efficiency in target tasks that the other baseline methods can hardly address. To summarize, our contributions are two-fold: 

- 1) We present an active LfD algorithm for robot policy transfer that effectively transfers policies from source to 


Fig. 1: Overview of our method. 

target tasks across diverse scenarios. 

- 2) We validate the effectiveness of our method through a set of robotic policy transfer scenarios, supported by extensive empirical results from simulations and preliminary sim-to-real experiments in real-world environments. 

## II. RELATED WORK 

**Policy Transfer with Demonstrations** Policy transfer aims to adapt a policy of a source domain to a target domain that is related but different from the source [1]. To further facilitate policy transfer, efforts have been made to introduce demonstrations into this process, either from the source domain or the target domain. When these demonstrations are from the source domain, they are commonly used to acquire prior skills of the source domain using different representations [6], [7], [8], [9], [10], whcih can be later fine-tuned for the taregt domain. Additionally, these source domain demonstrations can also be used to infer the dynamics difference between the target and source domain, the knowledge of which can be then utilized to adapt policy to the target domains [18]. And when these demonstrations are from target domain, they can be utilized to accelerate the policy transfer process [11], [4] and better transfer the robot policy from simulation to real-world environments [19]. However, almost all of these work only use offline demonstrations, which are collected prior to the policy transfer process. By contrast, extensive evidence has shown in the scenario of learning from scratch that online demonstrations can effectively improve sample efficiency and achieve better learning performance by providing the required demonstrations to the learning agent during the training process. Therefore, our work extends this idea to the scenario of policy transfer and presents an active LfD algorithm that queries online demonstrations, achieving better performance in policy transfer with improved sample effiency. 

**Interactive Learning from Demonstrations** . To alleviate the issue of covariance shift of conventional Learning from Demonstrations (LfD), efforts have been made to introduce interactive teaching inputs into the learning paradigm [20], [21]. Instead of using offline demonstrations that are collected before learning happens, interactive LfD collect teaching signals from demonstrators during the learning process. 

These teaching inputs can be in the form of evaluative feedback [22], [23], [24], [25], [26], state-action corrections [27], [28], [29], [30], and episodic demonstrations [15], [17], the timing and content of which can either be determined by the demonstrators themselves [12], [31] or actively requested by the learning agent [13], [14], [15], [17]. However, all of them are designed for the scenario of learning from scratch. Few have attempted to explore its potential in policy transfer, which is the main focus of our work. 

## III. BACKGROUND 

To leverage _online_ demonstrations for robot policy transfer, our work builds upon the Advantage Weighted ActorCritic (AWAC), an advanced off-policy LfD to update actorcritic models with _offline_ demonstrations. Furthermore, we optimize both the timing and content of online demonstration queries for _policy transfer_ by adapting the general paradigm for active LfD proposed in the EARLY framework [17] that was originally designed for the scenario of _learning from scratch_ . We thereby introduce the necessary background as follows. 

## _A. Advantage Weighted Actor-Critic_ 

Advantage Weighted Actor-Critic (AWAC) [32] is an advanced LfD algorithm that optimizes the policy and value function networks with offline demonstrations. It utilizes the Soft Actor-Critic (SAC) [33] as its underlying off-policy RL algorithm and updates its action-value function _Qϕ_ ( _s, a_ ) via: 


where 


And for the policy network _πθ_ , AWAC updates its parameters _θ_ via: 


where _β_ = _D ∪R_ is the combined replay buffer consisting of the demo buffer _D_ and self roll-out buffer _R_ . _λ_ is a hyperparameter and _A_<sup>_πθ_</sup> ( _s, a_ ) = _Q_<sup>_πθ_</sup> ( _s, a_ ) _− V_<sup>_πθ_</sup> ( _s_ ) is the advantage for the policy _πθ_ , which is used to bias the policy update to favor actions of larger estimated action-values. 

## _B. EARLY_ 

Episodic Active Reinforcement Learning from demonstration querY (EARLY) [17] is an active LfD algorithm that leverages online demonstrations for the scenario of learning from scratch. It decides _when_ to query and _what_ episodic expert demonstration to query by evaluating the uncertainty _u_ of an episodic roll-out _ξπ_<sup>_i_underpolicy</sup><sup>_π_with:</sup> 


After each episodic roll-out, EARLY will update a shifting history of uncertainty to generate an adaptive threshold to decide whether to query. Once deciding to query, it will request an episodic expert demonstration starting from a certain initial state chosen by the query strategy. Both policy roll-outs and expert demonstrations will be stored in the replay buffer, which will be used to update the actor and critic with SAC as the underlying off-policy RL algorithm. 

## IV. METHODOLOGY 

## _A. Problem Formulation_ 

We consider the scenario where there is a source task environment _ES_ and a target task environment _ET_ . Both environments are Markov Decision Processes (MDPs), denoted as _ES_ = _{S_<sup>_ES_</sup> _, A_<sup>_ES_</sup> _, r_<sup>_ES_</sup> _, P_<sup>_ES_</sup> _, ρ_<sup>_E_</sup> 0<sup>_S, γES}_and</sup><sup>_ET_=</sup> _{S_<sup>_ET_</sup> _, A_<sup>_ET_</sup> _, r_<sup>_ET_</sup> _, P_<sup>_ET_</sup> _, ρ_<sup>_E_</sup> 0<sup>_T, γET }_,where</sup><sup>_S_isthestate</sup> space, _A_ is the action space, _r_ : _S × A →_ R is the reward function, _P_ ( _st_ +1 _|st, at_ ) is the environment transition function, _ρ_ 0 is the initial state distribution, and _γ_ is the discount factor. 

For the source task _ES_ , we assume that the robot has access to the trained expert-level policy network _πθ_<sup>_ES_</sup> parametrized by _θ_ . For the target task _ET_ , the robot has access to _Nd_ episodic expert demonstrations = _ξk,demo_<sup>_ET_</sup> _{_ ( _s_<sup>_E_</sup> 0 _,k_<sup>_T, aE_</sup> 0 _,k_<sup>_T, r_</sup> 0<sup>_E_</sup> _,k_<sup>_T, sE_</sup> 1 _,k_<sup>_T_)</sup><sup>_, ...}_.Notethateach</sup> demonstration can be queried from an expert demonstrator and iteratively added to the demo buffer _D_ either before policy transfer starts (i.e., offline demonstrations) or during the training process (i.e., online demonstrations). The goal is to leverage these demonstrations to adapt the policy _πθ_<sup>_ES_</sup> of the source task _ES_ to the target task _ET_ such that the transferred policy _πθ_<sup>_ET_</sup> may = maximize the discounted target task reward _J_<sup>_ET_</sup> E _πθET ,sET_ 0 _∼ρET_ 0 �� _Lt_ =0 _ET −_ 1 � _γ_<sup>_ET_�</sup><sup>_t_</sup> _r_<sup>_ET_</sup> ( _st_<sup>_ET_</sup> _, πθ_<sup>_ET_</sup> ( _s_<sup>_E_</sup> _t_<sup>_T_</sup> ))� for an episode of the maximum length _L_<sup>_ET_</sup> . 

To simplify the problem, this work focuses on the scenario where the target and source task environments share the same state and action spaces but may differ in their transition dynamics _P_ and reward functions _r_ . Additionally, we assume that the policy networks for both the source and target tasks share the same neural network structure. 

**Algorithm 1** Policy Transfer with Online Demonstrations 

- **Input:** demonstration budget _Nd_ , max length of shifting history _Nh_ , ratio threshold _rquery_ 

- 1: Randomly initialize action-value network _Q_<sup>_E_</sup> _ϕ_<sup>_T_</sup> for the target task 

- 2: Initialize policy network _πθ_<sup>_ET_</sup> _← πθ_<sup>_ES_</sup> 3: Initialize self roll-out buffer _R_ and demo buffer _D_ 4: Initialize initial state history _H_ , roll-out uncertainty history _Hu_ 

- 5: Index of the adaptive threshold _idxthres ← int_ ( _Nh × rquery_ ) 

- 6: Queried demo number _nd ←_ 0 7: **for** iteration _i ∈{_ 1 _,_ 2 _, ...}_ **do** 8: roll out the policy _πθ_<sup>_ET_</sup> to get a trajectory _ξπ_<sup>_i_</sup> _θET_ 9: **for** step _t ∈ ξπ_<sup>_iET_</sup><sup>**do**</sup> 

- 10: update self roll-out buffer _R_ 11: update _Q_<sup>_E_</sup> _ϕ_<sup>_T_</sup> and _πθ_<sup>_ET_</sup> via (1) and (3) respectively 12: **end for** 13: calculate roll-out uncertainty _ui_ ( _ξπ_<sup>_iET_)via(4)</sup> 14: update _H_ and _Hu_ 15: **if** l _en_ ( _H_ ) _≥ Nh_ + 1 **then** 16: descendingly reorder _Hu_ into _Hu_<sup>_dsc_</sup> 17: adaptive threshold _uthres ← Hu_<sup>_dsc_</sup> [ _idxthres_ ] 18: **if** _ui > uthres_ and _nd < Nd_ **then** 19: _s_<sup>_E_</sup> 0 _,query_<sup>_T←_argmax</sup> _sET_ 0 _,j_<sup>_∈H Hu_</sup> 20: query a demo _ξk,demo_<sup>_ET_startingfrom</sup><sup>_s_</sup> 0<sup>_E_</sup> _,query_<sup>_T_</sup> 21: update demo buffer _D_ 22: update _Q_<sup>_E_</sup> _ϕ_<sup>_T_</sup> and _πθ_<sup>_ET_</sup> 23: _nd ← nd_ + 1 24: **end if** 25: remove the earliest element from _H_ and _Hu_ 26: **end if** 27: **end for** 

“demo-while-training” manner, where the robot actively decides the timing and contents of online expert demonstrations to query for better policy transfer performance. 

Starting from a trained policy _πθ_<sup>_ES_</sup> of the source task, our algorithm evaluates the uncertainty _u_ using (4) after each episodic roll-out in the target task and updates a shifting history _H_ of roll-out initial states and a shifting history _Hu_ of roll-out uncertainty. After the shifting history grows to its full length _Nh_ , the algorithm will generate an adaptive threshold _uthres_ of uncertainty to determine whether to query. If it decides to query, the algorithm will search the shifting history _H_ for the episodic roll-out that has the highest uncertainty, and query an expert demonstrator for an episodic demonstration _ξk,demo_<sup>_ET_inthetargettaskstarting</sup> from the same initial state as that of the most uncertain rollout. We summarize the pseudo-code as in Algorithm 1. 

## V. EXPERIMENTAL SETUP 

## _B. Policy Transfer With Online Demonstrations_ 

Aiming to better transfer the robot policy of a source task to a target task, we design an algorithm that learns in a 

## _A. Task Environments_ 

For source tasks, we choose two robotic tasks: _PandaPush_ and _PandaPickAndPlace_ as designed in [34]. For the task 


Fig. 2: Overview of all the source and target tasks. 

of _PandaPush_ , the Franka Emika manipulator, which is of 7 degrees of freedom, starts from a neutral pose and aims to push a 0 _._ 04m-sized cube across the table surface to a goal position randomly chosen from an area of 0 _._ 3m _×_ 0 _._ 3m. For the task of _PandaPickAndPlace_ , the Franka Emika manipulator starts from the same neutral pose and aims to pick up a cube positioned in an area of 0 _._ 3m _×_ 0 _._ 04m and place it at a pre-defined fixed position on the table surface. Both source tasks are situated in an environment without any obstacles on the table. Furthermore, both tasks are designed with sparse rewards, i.e., the robot receives a reward of +1000 only if the cube reaches the goal position, and a reward of _−_ 1 otherwise. 

For target tasks, we design 8 target tasks, as shown in Figure 2. More specifically, these target tasks can be divided into 3 general types of transfer learning scenarios, i.e., across different _environment characteristics_ (e.g., object size, object shape, friction factor), across different _task objectives_ (e.g., pushing or pick-and-place a cube while avoiding obstacles), and across different _robotic embodiments_ (e.g., transfer the policy from one robot arm to a different one). 

Across different environment characteristics, we design 4 target tasks: 

- _PushNewObjectShape_ : This task is similar to _PandaPush_ , but uses a coin-shaped object, which is a cylinder with a height of 0 _._ 01m and a radius of 0 _._ 02m. 

- _PushNewFriction_ : This task is similar to _PandaPush_ , but features a friction factor of 0 _._ 25, which is half the value used in _PandaPush_ . 

- _PnPNewObjectShape_ : This task is similar to _PandaPickAndPlace_ , but uses a cylinder-shaped object with a height of 0 _._ 04m and a radius of 0 _._ 02m 

- _PnPNewObjectSize_ : This task is similar to _PandaPickAndPlace_ , but uses a much smaller cube with a size of 0 _._ 02m. 

Across different task objectives, we designed 2 more target tasks: 

- _PushWithObstacle_ : This task is similar to _PandaPush_ , but the robot arm needs to push the cube to a fixed goal position without touching the obstacle. An episode will terminate with a reward of _−_ 1000 once the cube touches the obstacle. The initial position of the cube will be randomly chosen from a fixed area of 0 _._ 3m _×_ 0 _._ 04m. 

- _PnPWithObstacle_ . This task is similar to _PandaPickAndPlace_ , but the robot arm needs to pick and place the cube to a fixed goal position without touching the obstacle. An episode will terminate with a reward of _−_ 1000 once the cube runs into the obstacle. The initial position of the cube will be randomly chosen from a fixed area of 0 _._ 3m _×_ 0 _._ 04m. 

And across different robotic embodiments, we design 

another 2 target tasks: 

- _PushNewRobot_ : This task is similar to _PandaPush_ , but uses UR5 as the robot manipulator, which is of 6 degrees of freedom. Since we use the target 3D position of the end-effector as the action _at_ , switching to a new robot of a different number of degrees of freedom will not lead to the mismatch of action space between the source task and the target task. 

- _PnPNewRobot_ : This task is similar to _PandaPickAndPlace_ , but also uses UR5 as the manipulator instead of the Franka Emika manipulator. 

Based on these 8 target tasks, we define 8 corresponding scenarios for robot policy transfer. For PushNewObjectShape, PushNewFriction, PushWithObstacle, and PushNewRobot, we use PandaPush as the source task, resulting in 4 scenarios that we refer to as _Push2NewObjectShape_ , _Push2NewFriction_ , _Push2WithObstacle_ , and _Push2NewRobot_ . Similarly, we choose PandaPickAndPlace as the source task for PnPNewObjectShape, PnPNewObjectSize, PnPWithObstacle, and PnPNewRobot, resulting in another 4 scenarios we refer to as _PnP2NewObjectShape_ , _PnP2NewObjectSize_ , 


Fig. 3: Results of simulation experiments. 

## _PnP2WithObstacle_ , and _PnP2NewRobot_ . 

## _B. Demonstration Collection_ 

For each of the 8 scenarios for policy transfer, we use a joystick to collect a pool of 30 episodic demonstrations from the same human expert demonstrator and guarantee that each demonstration succeeds in the target task. The initial states of these demonstrations are decided by uniformly sampling from the initial state distribution of the corresponding target task. During the learning process, the robot may iteratively request 10 demonstrations (i.e., demonstration budget _Nd_ = 20) from the pool. When an online query (i.e., _s_<sup>_E_</sup> 0 _,query_<sup>_T_)is</sup> generated, we will choose the demonstration _ξk,demo_<sup>_ET_from</sup> the pool whose initial state is closest to the queried one based on their Euclidean distance in the state space, and use this demonstration as the queried online demonstration. 

It should be noted that the distribution of demonstrations in the pool is unknown to the robot throughout the training process. It is only a methodological trick to function as an unknown human-expert policy. It iteratively outputs human demonstrations and feeds them back to the robot upon request. How each demonstration is retrieved from the pool is also unknown to the robot. This is equivalent to having a real human expert available throughout the training phase, iteratively providing demonstrations with the joystick whenever the robot queries. 

## _C. Baselines_ 

We compare our method with 3 other popular LfD baselines in the scenario of policy transfer, including 2 canonical LfD methods using offline demonstrations and 1 active LfD method using online demonstrations. Each baseline is initialized with the same trained expert-level policy network of the source task and may request 10 episodic expert demonstrations for the corresponding target task, either iteratively 

during the training process (i.e., online demonstrations) or all before the training process (i.e., offline demonstrations). 

More specifically, we compare our method with 3 other baselines as follows: 

- **AWAC** . An advanced LfD method using offline demonstrations as mentioned in Section III-A. For each transfer scenario, we uniformly sample 10 episodic demonstrations from the corresponding demonstration pool and load them into the demo buffer before the training starts. We employ the same hyperparameter values for policy training as those specified in the original work. 

- **Behavioral Cloning (BC)** . A common offline LfD algorithm that trains the policy via supervised learning [35]. We sample the offline demonstrations in the same way as for the baseline of AWAC. 

- **EARLY** . An active LfD method using online demonstrations as mentioned in Section III-B. When a query is generated by the method, we choose the expert demonstration from the demonstration pool whose initial state is closest to the request one and feed it to the algorithm. All the hyperparemeters are set as the same values as in the original work. 

For our method, we set the max length of shifting history _Nh_ = 20 and the ratio threshold _rquery_ = 0 _._ 1 for all 8 transfer scenarios. We obtain the trained expert-level policies for the source tasks by training the actor-critic models via SAC using the dense reward function shaped by the distance to the goal. We employ the same actor-critic model structure as AWAC with the default hyperparameters as in [32]. Furthermore, we add layer normalization for more stable convergence as in [36]. We also use a balanced-sampling strategy as EARLY for each policy and action-value update by sampling an equal number of transitions from both the demo buffer _D_ and self roll-out buffer _R_ . 


Fig. 4: The scenarios for real-world experiments. 

VI. RESULTS AND DISCUSSION 

## _A. Simulation Experiments_ 

**Higher success rate with improved sample efficiency.** We evaluate each baseline method by measuring the success rate of the target task policy every 5000 environment steps, using 10 random seeds. As shown in Figure 3, our method consistently outperforms all baselines in terms of average success rate across all 8 policy transfer scenarios. Specifically, our method achieves around 100% average success rate in 6 scenarios: _Push2NewObjectShape_ , _Push2NewFriction_ , _Push2NewRobot_ , _Push2WithObstacle_ , _PnP2NewObjectSize_ , and _PnP2NewRobot_ . In contrast, the other baselines struggle to transfer policies effectively, with average success rates generally not exceeding 20%, except in the _PnP2NewObjectSize_ scenario. In that case, while EARLY reaches an 80% success rate, its performance quickly degrades and fails to converge. Although AWAC converges to a 100% success rate, it requires approximately 750 _×_ 10<sup>3</sup> steps, converging abot 50% slower than our method. 

For the remaining 2 scenarios, our method still performs better, achieving over 70% average success rate in _PnP2WithObstacle_ , where other baselines struggle to solve the target tasks. In the _PnP2NewObjectShape_ scenario, our method also reaches around 80% success, while BC and EARLY fail to solve the task, and AWAC converges to only around 60%. 

These strong empirical results demonstrate that our method maintains robust effectiveness across a variety of transfer learning scenarios, successfully transferring policies from source tasks to target tasks across diverse environmental conditions, task objectives, and robotic embodiments. 

## _B. Preliminary Sim-to-Real Tests on the Real Robot_ 

We replicate the target task environments of PushWithObstacle, PushNewObjectShape, and PnPNewObjectSize in the real-world environment (shown in figure 4) and validate the sim-to-real performance of our method on the real Franka 

TABLE I: Results of real-world experiments. 

|Scenario||Success|Rate||
|---|---|---|---|---|
||ours|AWAC|BC|EARLY|
|Push2WithObstacle|**100%**|0%|0%|0%|
|Push2NewObjectShape|**80%**|0%|0%|0%|
|PnP2NewObjectSize|**50%**|**50%**|0%|10%|


Emika manipulator. More specifically, we use an 0 _._ 04m-sized cube for PushWithObstacle and an obstacle with dimensions of (0 _._ 02m, 0 _._ 1m, 0 _._ 02 _m_ ) located it at ( _−_ 0 _._ 11 _,_ 0 _,_ 0 _._ 01). For PushNewObjectShape, we use the a flat cylinder with _h_ = 0 _._ 01m and _r_ = 0 _._ 02m. For PnPNewObjectSize, we use a 0 _._ 02m-sized cube. For both our method and the baselines, we evaluate their performance on the real robot by rolling out the transferred policies saved at the last checkpoint for 10 test episodes. The initial state of each test episode is uniformly sampled from the initial state space. And to simplify the test, we assume that the object pose in the real world matches that in a synchronized simulation environment by using the real-time state in the simulation as the input to the trained policy. The trained policy outputs the real-time action defined as the target 3 _D_ position of the end-effector and sends it to the real robot under a frequency of 100 Hz. Upon receiving the command, the robot converts it into the corresponding joint command and controls its joints with the joint-position controller implemented by the open-sourced library pandapy [37]. As shown in table I, the transferred policies trained by our method achieve the highest success rate compared with other baselines, indicating the efficacy of the transferred policy obtained by our method in the real-world environment. 

## VII. CONCLUSIONS AND LIMITATIONS 

In this work, we present an active LfD algorithm that introduces online demonstrations into the policy transfer process. By optimizing the timing and content of queries for online demonstrations, our method achieves significantly better performance for policy transfer with respect to both average success rate and sample efficiency in 8 robotic scenarios compared with 3 other LfD baselines. However, this work is only focused on scenarios where the target and source tasks share the same state-action space and policy network structure. This limitation may be alleviated if a more unified representation of task space and policy can be used as in [5]. Additionally, we assume access to an environment reset function that can reset the environment to a queried initial state, which may constrain its applicability in real-world settings, though this can be mitigated with human assistance or existing path-planning controllers. Furthermore, additional factors, such as user experience, need to be taken into account when online demonstrations are iteratively collected from real humans interacting with real robots. How to maintain good performance of policy transfer while accounting for human factors will be a key focus of our future work. 

REFERENCES 

   - tasks,” in _2023 32nd IEEE International Conference on Robot and Human Interactive Communication (RO-MAN)_ , 2023, pp. 1745–1752. 

- [1] N. Jaquier, M. C. Welle, A. Gams, K. Yao, B. Fichera, A. Billard, A. Ude, T. Asfour, and D. Kragi´c, “Transfer learning in robotics: An upcoming breakthrough? a review of promises and challenges,” _arXiv preprint arXiv:2311.18044_ , 2023. 

- [2] X. Zhang, C. Wang, L. Sun, Z. Wu, X. Zhu, and M. Tomizuka, “Efficient sim-to-real transfer of contact-rich manipulation skills with online admittance residual learning,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 1621–1639. 

- [3] A. Z. Ren, H. Dai, B. Burchfiel, and A. Majumdar, “Adaptsim: Taskdriven simulation adaptation for sim-to-real transfer,” _arXiv preprint arXiv:2302.04903_ , 2023. 

- [4] A. Hundt, A. Murali, P. Hubli, R. Liu, N. Gopalan, M. Gombolay, and G. D. Hager, “” good robot! now watch this!”: Repurposing reinforcement learning for task-to-task transfer,” in _5th Annual Conference on Robot Learning_ , 2021. 

- [5] P. Jian, E. Lee, Z. Bell, M. M. Zavlanos, and B. Chen, “Policy stitching: Learning transferable robot policies,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 3789–3808. 

- [6] G.-f. Wang, Z. Fang, P. Li, and B. Li, “Transferring knowledge from human-demonstration trajectories to reinforcement learning,” _Transactions of the Institute of Measurement and Control_ , vol. 40, no. 1, pp. 94–101, 2018. 

- [7] T. Fitzgerald, A. K. Goel, and A. L. Thomaz, “Representing skill demonstrations for adaptation and transfer,” in _2014 AAAI fall symposium series_ , 2014. 

- [8] M. Akbulut, E. Oztop, M. Y. Seker, X. Hh, A. Tekden, and E. Ugur, “Acnmp: Skill transfer and task extrapolation through learning from demonstration and reinforcement learning via representation sharing,” in _Conference on Robot Learning_ . PMLR, 2021, pp. 1896–1907. 

- [9] K. Pertsch, R. Desai, V. Kumar, F. Meier, J. J. Lim, D. Batra, and A. Rai, “Cross-domain transfer via semantic skill imitation,” _arXiv preprint arXiv:2212.07407_ , 2022. 

- [10] C. Gao, Y. Jiang, and F. Chen, “Transferring hierarchical structures with dual meta imitation learning,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 762–773. 

- [11] P. Yao and L. Feng, “Integrating policy reuse with learning from demonstrations for knowledge transfer in deep reinforcement learning,” in _Neural Information Processing: 28th International Conference, ICONIP 2021, Sanur, Bali, Indonesia, December 8–12, 2021, Proceedings, Part V 28_ . Springer, 2021, pp. 659–667. 

- [12] S. Ross and D. Bagnell, “Efficient reductions for imitation learning,” in _Proceedings of the thirteenth international conference on artificial intelligence and statistics_ . JMLR Workshop and Conference Proceedings, 2010, pp. 661–668. 

- [13] J. Zhang and K. Cho, “Query-efficient imitation learning for end-toend autonomous driving,” _arXiv preprint arXiv:1605.06450_ , 2016. 

- [14] S.-A. Chen, V. Tangkaratt, H.-T. Lin, and M. Sugiyama, “Active deep q-learning with demonstration,” _Machine Learning_ , vol. 109, no. 9, pp. 1699–1725, 2020. 

- [15] M. Rigter, B. Lacerda, and N. Hawes, “A framework for learning from demonstration with minimal human effort,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 2, pp. 2023–2030, 2020. 

- [16] M. Sakr, Z. Zhang, B. Li, H. Zhang, V. der Loos, H. Machiel, D. Kulic, and E. Croft, “How can everyday users efficiently teach robots by demonstrations?” _arXiv preprint arXiv:2310.13083_ , 2023. 

- [17] M. Hou, K. Hindriks, G. Eiben, and K. Baraka, ““give me an example like this”: Episodic active reinforcement learning from demonstrations,” in _Proceedings of the 12th International Conference on HumanAgent Interaction_ , 2024, pp. 287–295. 

   - [22] A. Najar, O. Sigaud, and M. Chetouani, “Interactively shaping robot behaviour with unlabeled human instructions,” _Autonomous Agents and Multi-Agent Systems_ , vol. 34, no. 2, p. 35, 2020. 

   - [23] S. Griffith, K. Subramanian, J. Scholz, C. L. Isbell, and A. L. Thomaz, “Policy shaping: Integrating human feedback with reinforcement learning,” _Advances in neural information processing systems_ , vol. 26, 2013. 

   - [24] W. B. Knox and P. Stone, “Tamer: Training an agent manually via evaluative reinforcement,” in _2008 7th IEEE international conference on development and learning_ . IEEE, 2008, pp. 292–297. 

   - [25] E. Bıyık, D. P. Losey, M. Palan, N. C. Landolfi, G. Shevchuk, and D. Sadigh, “Learning reward functions from diverse sources of human feedback: Optimally integrating demonstrations and preferences,” _The International Journal of Robotics Research_ , vol. 41, no. 1, pp. 45–67, 2022. 

   - [26] Y. Cui, Q. Zhang, B. Knox, A. Allievi, P. Stone, and S. Niekum, “The empathic framework for task learning from implicit human feedback,” in _Conference on Robot Learning_ . PMLR, 2021, pp. 604–626. 

   - [27] R. P´erez-Dattari, C. Celemin, J. Ruiz-del Solar, and J. Kober, “Interactive learning with corrective feedback for policies based on deep neural networks,” in _Proceedings of the 2018 International Symposium on Experimental Robotics_ . Springer, 2020, pp. 353–363. 

   - [28] E. Chisari, T. Welschehold, J. Boedecker, W. Burgard, and A. Valada, “Correct me if i am wrong: Interactive learning for robotic manipulation,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 2, pp. 3695–3702, 2022. 

   - [29] C. Celemin and J. Kober, “Knowledge-and ambiguity-aware robot learning from corrective and evaluative feedback,” _Neural Computing and Applications_ , vol. 35, no. 23, pp. 16 821–16 839, 2023. 

   - [30] C. Celemin and J. Ruiz-del Solar, “An interactive framework for learning continuous actions policies based on corrective feedback,” _Journal of Intelligent & Robotic Systems_ , vol. 95, pp. 77–97, 2019. 

   - [31] M. Kelly, C. Sidrane, K. Driggs-Campbell, and M. J. Kochenderfer, “Hg-dagger: Interactive imitation learning with human experts,” in _2019 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2019, pp. 8077–8083. 

   - [32] A. Nair, A. Gupta, M. Dalal, and S. Levine, “Awac: Accelerating online reinforcement learning with offline datasets,” _arXiv preprint arXiv:2006.09359_ , 2020. 

   - [33] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, “Soft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor,” in _International conference on machine learning_ . PMLR, 2018, pp. 1861–1870. 

   - [34] Q. Gallou´edec, N. Cazin, E. Dellandr´ea, and L. Chen, “panda-gym: Open-Source Goal-Conditioned Environments for Robotic Learning,” _4th Robot Learning Workshop: Self-Supervised and Lifelong Learning at NeurIPS_ , 2021. 

   - [35] D. A. Pomerleau, “Alvinn: An autonomous land vehicle in a neural network,” _Advances in neural information processing systems_ , vol. 1, 1988. 

   - [36] P. J. Ball, L. Smith, I. Kostrikov, and S. Levine, “Efficient online reinforcement learning with offline data,” in _International Conference on Machine Learning_ . PMLR, 2023, pp. 1577–1594. 

   - [37] J. Elsner, “Taming the panda with python: A powerful duo for seamless robotics programming and integration,” _SoftwareX_ , vol. 24, p. 101532, 2023. [Online]. Available: https://www.sciencedirect.com/ science/article/pii/S2352711023002285 

- [18] K. Kim, Y. Gu, J. Song, S. Zhao, and S. Ermon, “Domain adaptive imitation learning,” in _International Conference on Machine Learning_ . PMLR, 2020, pp. 5286–5295. 

- [19] S. Desai, I. Durugkar, H. Karnan, G. Warnell, J. Hanna, and P. Stone, “An imitation from observation approach to transfer learning with dynamics mismatch,” _Advances in Neural Information Processing Systems_ , vol. 33, pp. 3917–3929, 2020. 

- [20] M. Hou, K. Hindriks, A. Eiben, and K. Baraka, “Shaping imbalance into balance: Active robot guidance of human teachers for better learning from demonstrations,” in _2023 32nd IEEE International Conference on Robot and Human Interactive Communication (ROMAN)_ . IEEE, 2023, pp. 1737–1744. 

- [21] M. Hou, K. Hindriks, A. Eiben, and K. Baraka, “A process-oriented framework for robot imitation learning in human-centered interactive 

