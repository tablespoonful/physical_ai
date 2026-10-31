---
title: "Open-Source Reinforcement Learning Environments Implemented in MuJoCo with Franka Manipulator"
date: "2023-12-21"
authors: "Zichun Xu; Yuntao Li; Xiaohang Yang; Zhiyuan Zhao; Lei Zhuang; Jingdong Zhao"
url: https://arxiv.org/abs/2312.13788
pdf: https://arxiv.org/pdf/2312.13788
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2312.13788)** / [論文ページ](https://arxiv.org/abs/2312.13788)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Open-Source Reinforcement Learning Environments Implemented in MuJoCo with Franka Manipulator** 

Zichun Xu, Yuntao Li, Xiaohang Yang, Zhiyuan Zhao, Lei Zhuang, and Jingdong Zhao<sup>*</sup> 

**_Abstract_ —This paper presents three open-source reinforcement learning environments developed on the MuJoCo physics engine with the Franka Emika Panda arm in MuJoCo Menagerie. Three representative tasks, push, slide, and pick-and-place, are implemented through the Gymnasium Robotics API, which inherits from the core of Gymnasium. Both the sparse binary and dense rewards are supported, and the observation space contains the keys of desired and achieved goals to follow the MultiGoal Reinforcement Learning framework. Three different offpolicy algorithms are used to validate the simulation attributes to ensure the fidelity of all tasks, and benchmark results are also given. Each environment and task are defined in a clean way, and the main parameters for modifying the environment are preserved to reflect the main difference. The repository, including all environments, is available at https://github.com/ zichunxx/panda** **<u>mujoco gym.</u>** 

**_Index Terms_ —Reinforcement Learning, MuJoCo, MuJoCo** 

## **Menagerie** 


Fig. 1: Base simulation environment implemented with the Franka model in MuJoCo Menagerie. 

# I. INTRODUCTION 

Reinforcement learning (RL) has been widely applied to sophisticated decision-making tasks, such as assembly tasks [1] and connector insertion [2], and has performed well even with high-dimensional vision input tensors [3]. This advantage is due to the fact that the goal and reward can be implicitly defined, and the agent can explore the environment to gather valuable actions. In recent years, many contributions have been made to the RL community, especially Gymnasium [4], which is a fork of the OpenAI Gym library and provides lots of APIs and wrappers to formalize the standard pipeline. 

Nevertheless, both the contact-rich task [5] and reward engineering [6], which dominate the training process, preclude training in the open world to some extent. Therefore, a realistic simulation environment can further minimize the sim-to-real gap and serve as a reference for deployment in the real scenario. So far, convincing researches [7]–[9] have demonstrated that training in simulation is informative and the derived policy can be transferred to real scenarios, which also raises high demands on the computational speed and accuracy of the physics engine. Some options can be considered to realize parallel simulation, e.g., MuJoCo<sup>1</sup> , Bullet<sup>2</sup> , and PhysX<sup>3</sup> , and the accessible environments built within them lower the entry barrier for RL researchers. 

MuJoCo enables different types of contact dynamics and actuation models with various optimization solvers, which makes 

> All authors are with the State Key Laboratory of Robotics and Systems, Harbin Institute of Technology, Harbin 150001, Heilongjiang Province, China. 

> *Corresponding author: zhaojingdong@hit.edu.cn 

> 1https://mujoco.org/ 

> 2https://pybullet.org/ 

> 3https://github.com/NVIDIAGameWorks/PhysX 

it a popular choice and has been adopted in many studies [10], [11]. Meanwhile, a collection of fine-tuned robot models is published in MuJoCo Menagerie<sup>4</sup> . Gymnasium [4] integrates with many out-of-box classic RL environments developed on MuJoCo, such as Humanoid and Ant. With the development of operation tasks, environments focused on collaborative manipulators are gradually receiving more attention. Gymnasium Robotics<sup>5</sup> is presented including the Fetch [12] and Franka Kitchen [13] environments, in which the Fetch environments consist of four representative tasks: FetchReach, FetchPush, FetchSlide, and FetchPickAndPlace. These continuous control tasks are provided as guidance on how to define similar behaviors and the goal-conditioned observation space. Furthermore, Robosuite [14], which is a modular simulation framework powered by MuJoCo, encapsulates some benchmark manipulation environments with seven commercially available arms. 

Pybullet<sup>6</sup> , which is a python module for robotics simulation, also encapsulates a suite of basic Gym environments. Beyond that, the KUKA IIWA arm is incorporated to construct KukaBulletEnv and KukaCamBulletEnv, in which the observation for the latter is camera pixels. Inspired by the Fetch environments, panda-gym [15] is developed on Pybullet with two extra tasks, PandaFlip and PandaStack. All environments in panda-gym follow the Multi-Goal RL framework and are defined as the robot and task in an individual way for more flexible development. 

> 4http://github.com/google-deepmind/mujoco <u>menagerie</u> 

> 5http://github.com/Farama-Foundation/Gymnasium-Robotics 

> 6https://github.com/bulletphysics/bullet3 


Fig. 2: Overview of the benchmark environment, including registration and the training process. 

Isaac Gym [16], built on NVIDIA PhysX, features accelerating the training process on GPU and also incorporates a host of robotics-related environments. Factory [17] resorts to reproduce the realistic contact-rich assembly scenario in simulator, and thus three environments are developed to solve the assembly tasks on the NIST task board, e.g., FrankaNutBoltEnv, FrankaInsertionEnv, and FrankaGearsEnv. Single and dual KUKA arm manipulation environments with each of the three task variants (reorientation, regrasping, and grasp-and-throw) are also created with the 16-DoF Allegro Hand [18]. 

Motivated by the preceding work, we aim to provide a unified framework that encompasses benchmark environments powered by MuJoCo for two key reasons: First, compared to other engines, MuJoCo is designed for robotics and performs impressively with the fastest and most accurate simulations [19]. Some benchmark environments built on MuJoCo are easy to build and can be simply deployed with only a single CPU. NVIDIA’s Isaac Sim requires a high-performance GPU as the hardware foundation for building environments, which is a disincentive for beginners. Second, the modular design of some environments, like Robosuite, is user- and developerfriendly, but it is not intuitive for researchers to build their own environments on top of it and tune simulation options. Thus, from this perspective, building environments separately in a clean way is preferable. 

Toward this end, some manipulation tasks performed by the Franka arm are built with necessary dependencies and simplified modules. The simulation model of the Franka arm is obtained in MuJoCo Menagerie. The reason for this is that MuJoCo Menagerie offers a wider choice of high-quality robot models, which do not only cover manipulators, and few benchmark environments are built on them. This work can be treated as an extension of panda-gym [15] and migrated from Bullet to MuJoCo. The benchmark results with Deep Deterministic Policy Gradient (DDPG) [20], Soft Actor Critic 

(SAC) [21], [22], and Truncated Quantile Critics (TQC) [23] are also provided. In summary, the main contributions of this paper are twofold: 

- 1) Three benchmark environments are constructed based on MuJoCo Menagerie and powered by MuJoCo. 

- 2) DDPG, SAC, and TQC are trained over all tasks, and benchmark results are provided with essential analyses. 

The remainder of this paper is organized as follows: Sec. II first reviews all the off-policy RL algorithms used in this paper. Sec. III introduces the implementation details for all environments, and Sec. IV presents the benchmarking results over random seeds with essential analysis. Finally, Sec. V concludes this paper and illustrates some future works. 

# II. PRELIMINARIES 

Each task addressed in this paper can be formulated as a finite-horizon Markov decision process consisting of state space _S_ , action space _A_ , starting state distribution _ρ_ 0, transition probability function _P_ : _S × A →S_ , reward function _r_ : _S × P →R_ , and discount factor _γ ∈_ [0 _,_ 1]. After resetting the environment, each episode will start with _s_ 0 _∈ ρ_ 0. The policy _π_ ( _at|st_ ) is the mapping from _S_ to _A_ , from which the agent will take the action _at ∈A_ at the timestep _t_ . Then the reward _rt_ , the new state _st_ +1 _∼P_ , and the signal _d_ are received at the next timestep, where _d_ is used to distinguish whether the current episode is terminated or truncated. The above transition tuple ( _st, at, rt, st_ +1 _, d_ ) will be stored in replay buffer _D_ for training. The goal for RL is to select an optimal policy _π_<sup>_∗_</sup> to maximize the expected return E[<sup>�</sup><sup>_T_</sup> _i_ = _t_<sup>_γi−tri_],where</sup><sup>_T_denotestheepisodehorizon.</sup> 

# _A. Deep Deterministic Policy Gradient_ 

DDPG is an off-policy algorithm that concurrently learns a deterministic policy _πθ_ and a Q-function _Qϕ_ ( _s, a_ ) for continuous action, where _θ_ and _ϕ_ are initial policy and Q- function network parameters. At each timestep, the policy and 


(a) FrankaPush (b) FrankaSlide (c) FrankaPickAndPlace 

Fig. 3: Three proposed environments with the Franka model in MuJoCo Menagerie, in which the red point indicates the target. 

Q-function networks are updated by sampling a minibatch _B_ = _{_ ( _st, at, rt, st_ +1 _, d_ ) _}_ from _D_ . Notably, _at_ is obtained by adding the mean-zero Gaussian noise at the training time and saved in _D_ . After that, _Qϕ_ ( _st, at_ ) is updated utilizing gradient descent with 

# _C. Truncated Quantile Critics_ 

TQC is an extension of SAC but learns the distributional representation for _N_ Q-function critics. Each critic _Qϕn_ ( _st, at_ ) _, n ∈{_ 1 _, ..., N }_ estimates the distribution over the sum of discount rewards and contains _M_ atoms, i.e., 


where the target is calculated by 

All atoms of _Qϕ_ targ _,n_ ( _st_ +1 _,_ ˜ _at_ +1) are pooled into a set 


_πθ_ is updated using 


and sorted in ascending order _zi_ ( _st_ +1 _,_ ˜ _at_ +1) _, i ∈{_ 1 _...NM }_ , in which the _j × N_ largest elements are truncated. The remaining _k × N_ atoms form a target distribution 

at a certain frequency. The weights of target networks _θ_ targ and _ϕ_ targ will be updated by polyak averaging with a certain step delay. 


# _B. Soft Actor Critic_ 

that is used to calculate the critic loss, where 

In contrast to DDPG, SAC trains a stochastic policy and two Q-functions _Qϕ_ 1 and _Qϕ_ 2 based on the entropy framework. For the variant with the fixed entropy temperature coefficient _α_ , the target in Eq. 1 is given by 


The critic loss can be derived by 


where _a_ ˜ _t_ +1 _∼ πθ_ ( _·|st_ +1) is sampled from the current policy via the reparameterization trick. The policy is updated by gradient ascent with 

with the Huber quantile loss 


where _L_<sup>1</sup> _H_<sup>(</sup><sup>_u_)istheHuberlosswiththelinear/quadratic</sup> changepoint 1. The policy of TQC is updated as in SAC to minimize 

which uses the minimum of _Qϕ_ 1 and _Qϕ_ 2. In addition, _α_ can be dynamically adjusted concerning the loss 


where _θϕ_<sup>_m_</sup> _n_<sup>(</sup><sup>_st,_˜</sup><sup>_at_+1)</sup><sup>_, n∈_[1</sup><sup>_...N_]</sup><sup>_, m∈_[1</sup><sup>_...M_]arenottrun-</sup> cated. 

and thus balances exploration and exploitation, where _HT_ = _−_ dim _A_ . 

TABLE I: Hyperparameters used for the training of all offpolicy algorithms 

|Parameter|Value|
|---|---|
|Action size<br>Observation size<br>Network size|3 (Push, Slide), 4 (Pick & Place)<br>18 (Push, Slide), 19 (Pick & Place)<br>[256_,_256_,_256] (Pick & Place, Push)<br>[512_,_512_,_512] (Slide)|
|Batch size|512 (Pick & Place, Push)<br>2048 (Slide)<br>|
|Buffer size|10<sup>6</sup>|
|Optimizer|Adam|
|Action noise|_N_(0_,_0_._2) (DDPG, SAC)|
|Learning rate|0_._001|
|Polyak update|0_._05|
|Discount factor|0_._95|
|Evaluation frequency|2_,_000|
|Evaluation episode|15<br>|
|Training steps|5_×_10<sup>5 </sup>(Pick & Place, Push)<br>10<sup>6 </sup>(Slide)|
|HER strategy|Future|
|Number of HER per transition|4|
|Reward|Sparse|
|Number of critics|2 (TQC only)|
|Number of quantiles|25 (TQC only)|
|Quantiles to drop per critic|2 (TQC only)|
|Entropy regularization coefficient|Autotune (SAC, TQC)|


# III. ENVIRONMENTS 

All tasks in this paper follow the Multi-Goal RL framework, which is similar to panda-gym and Fetch. However, the main difference with panda-gym is that MuJoCo is employed as the physics engine with the Franka model in MuJoCo Menagerie. The settings for each environment, including feasible simulation options and attributes, are given in a separate XML document encapsulating each task. The training script is integrated based on the MujocoRobotEnv API in Gymnasium Robotics. The included tasks can be ranked in the ascending order of complexity: 

- FrankaPush The object needs to be pushed by the arm to the target on the floor. 

- FrankaSlide The arm will strike the puck toward the target on the floor, where the floor is slippery with low friction. 

- FrankaPickAndPlace The arm first picks an object and moves to the desired target, where the target has a certain probability of being chosen above the floor. 

The above environments are rendered in Fig. 3 and implemented with the (7 + 1)-DOF (i.e., seven arm joints and one gripper joint) Franka arm with its default parallel gripper. The orientation of the end-effector (EE) is fixed with a grasp pose, and thus the action space is 4-dim for the FrankaPickAndPlace task: the 3-dim movement of EE and the actuation of the gripper. However, the gripper is locked for the FrankaPush and FrankaSlide tasks. A mocap<sup>1</sup> body is bound to EE to maintain its orientation, and the joint angles are derived depending on its position variation, which is equivalent to the inverse kinematics algorithm. The simulation 

1https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-mocap 

TABLE II: Success rate of each algorithm in different tasks 

|Tasks|DDPG|SAC|TQC|
|---|---|---|---|
|Push|11.7 _±_ 0.3|100.0 _±_ 0.0|100.0 _±_ 0.0|
|Slide|71.7 _±_ 0.5|85.0 _±_ 0.4|85.1 _±_ 0.4|
|Pick & Place|58.3 _±_ 0.4|75.0 _±_ 0.5|100.0 _±_ 0.0|


timestep for MuJoCo is 2 ms based on the speed-accuracy trade-off. It can be further reduced for more stable contacts but with massive computational costs. An extremely small timestep wastes CPU time without meaningful improvement in accuracy. Due to the smaller contact area of the Franka gripper pads, the friction coefficients and contact-related parameters are further tuned, which are given in the XML documents. 

For all tasks in this paper, the observation space includes the Cartesian position and linear velocity of EE ( _xe_ , _ve ∈_ R<sup>3</sup> ) and the pose (i.e., Cartesian position and Euler angles), linear, and angular velocities of the object ( _xb_ , _eb_ , _vb_ , _wb ∈_ R<sup>3</sup> ). An additional finger width (1-dim) is added to the observation space for the FrankaPickAndPlace task. The achieved and desired goals, which are keys in the dictionary observation space, are the positions of the object and goal, respectively. Similarly, two variants of reward are retained for all tasks. For the sparse reward, the agent that moves within the target area (i.e., a given distance threshold from the target position) gets a reward of 0 and -1 otherwise. The dense reward is simply defined as a linear function of the distance between the achieved and desired goals. 

# IV. EVALUATION 

This section verifies the feasibility of benchmark environments, i.e., whether the RL algorithm can accomplish these tasks. Thus, three representative off-policy RL algorithms, DDPG, SAC, and TQC, are selected for training. From DDPG to TQC, the main improvements are dedicated to enhancing the performance of continuous policy to alleviate the overestimation bias. Unlike DDPG and SAC, TQC models the distribution over the critic value instead of the Q-function, from which several topmost atoms are truncated. The evaluation results in [23] indicate that TQC can obtain higher episode returns compared to SAC on MuJoCo environments. The performance of different algorithms when acting on our benchmark environments is also verified in this section. The implementation of the above algorithms is based on StableBaselines3 [24]. 

At the beginning of each episode, the arm is reset to the initial configuration, and the positions of target and goal are randomized within the specified area. For the pick-andplace task, the trick of the target position being randomized on the floor facilitates convergence, and the corresponding random probability can be adjusted. The episode length is 50 by default. Truncated and terminated signals are detected after each step. Termination can end the current episode in advance without wandering up to the maximum step limit. The transitions are saved in the replay buffer with Hindsight Experience Replay (HER) [25]. The policy is evaluated via 


Fig. 4: Median success rates and standard deviations indicated by shaded areas over three random seeds. 


Fig. 5: The execution processes of different tasks via the trained policies. 

50 episodes at an interval of 2,000 training steps. Once the object reaches the desired goal point within the episode length, this episode is labeled as successful. Thus, the success rate will serve as the primary evaluation metric. The detailed hyperparameters are available in Table I. Actor and critic share the same structure of multilayer perceptron (MLP), and the network size indicated in Table I refers to the hidden layers. 

Each algorithm is trained over three random seeds, and all training processes are deployed on a workstation with an NVIDIA RTX 3070Ti GPU and an i7-12700K CPU. Fig. 4 depicts the evaluation curves with the sparse reward for all tasks. DDPG performs the worst across all tasks and its success rate is less than 0.2 in the FrankaPush task. Fig. 4a typically reveals the disadvantage of DDPG that overestimation bias causes cumulative errors and thus leads to suboptimal strategies and divergent behaviors [26]. Then, clipped double-Q learning is proposed in [26] to reduce the overestimation bias effectively and is incorporated in SAC. 

The evaluation results in Fig. 4 also demonstrate that SAC performs better than DDPG across all tasks. Meanwhile, TQC performs the best and achieves a success rate close to 1 after training, which is consistent with the evaluation scores in [23]. 

For FrankaSlide, the target will be randomly distributed to the unreachable area for the Franka arm, which makes it hard to consistently adjust the object position. Thus, the training takes 1 million steps to improve the agent’s performance. As shown in Fig. 4b, SAC and TQC stabilize around the 80% success rate after training and rarely increase further, which is similar to the distributions in Fetch and panda-gym. For FrankaPush, SAC and TQC reach a success rate of more than 80% in around 2 _×_ 10<sup>5</sup> steps. Finally, each trained model is tested over 20 random episodes, and the corresponding success rate of each algorithm is counted in Table II. Fig. 5 illustrates the deterministic episode for each task with the trained TQC model, where the Franka arm will drive the object to reach the goal position from the left to right columns. 

# V. CONCLUSION AND FUTURE WORK 

Three open-source environments corresponding to three manipulation tasks are proposed in this paper, where each environment follows the Multi-Goal Reinforcement Learning framework. These benchmark environments are built with the Franka model in MuJoCo Menagerie and powered by MuJoCo. Note that each environment is defined in a clean way in which unnecessary dependencies and modules are omitted. Three representative off-policy algorithms with Hindsight Experience Replay are implemented to validate the feasibility of each environment. To the best of our knowledge, there are a few benchmark environments built on top of MuJoCo Menagerie. We expect that our open-source environments can gain some attention to create more benchmark environments with MuJoCo Menagerie and thus lower barriers for researchers to test algorithms. 

However, there are some limitations in our work. More diverse and realistic controllers, like the impedance controller, should be adopted to minimize the sim2real gap. Moreover, a smaller timestep has not been tested in MuJoCo considering the computing resources that we have. Future work will further dive into these limitations to be as faithful as possible to the real environment and offer more test results. Extra tasks and manipulators can also be considered to be added to the current work. 

# VI. ACKNOWLEDGMENT 

This work was supported by the National Natural Science Foundation of China [grant numbers: 92148203 and T2388101]. 

# REFERENCES 

- [1] J. Yamada, Y. Lee, G. Salhotra, K. Pertsch, M. Pflueger, G. S. Sukhatme, J. J. Lim, and P. Englert, “Motion Planner Augmented Reinforcement Learning for Robot Manipulation in Obstructed Environments.” in _Conference on Robot Learning (CoRL)_ , 2020, pp. 589–603. 

- [2] J. Zhao, Z. Wang, L. Zhao, and H. Liu, “A learning-based two-stage method for submillimeter insertion tasks with only visual inputs,” _IEEE Transactions on Industrial Electronics_ , 2023. 

- [3] T. Zhang, K. Zhang, J. Lin, W.-Y. G. Louie, and H. Huang, “Sim2real learning of obstacle avoidance for robotic manipulators in uncertain environments,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 1, pp. 65–72, 2021. 

- [4] M. Towers, J. K. Terry, A. Kwiatkowski, J. U. Balis, G. d. Cola, T. Deleu, M. Goul˜ao, A. Kallinteris, A. KG, M. Krimmel, R. PerezVicente, A. Pierr´e, S. Schulhoff, J. J. Tai, A. T. J. Shen, and O. G. Younis, “Gymnasium,” Mar. 2023. [Online]. Available: https://zenodo. org/record/8127025 

- [5] K. Zakka, P. Wu, L. M. Smith, N. Gileadi, T. Howell, X. B. Peng, S. Singh, Y. Tassa, P. Florence, A. Zeng, and P. Abbeel, “Robopianist: Dexterous Piano Playing with Deep Reinforcement Learning.” in _Conference on Robot Learning (CoRL)_ , 2023, pp. 2975–2994. 

- [6] A. Singh, L. Yang, K. Hartikainen, C. Finn, and S. Levine, “End-toend robotic reinforcement learning without reward engineering,” _arXiv preprint arXiv:1904.07854_ , 2019. 

- [7] L. Pinto, M. Andrychowicz, P. Welinder, W. Zaremba, and P. Abbeel, “Asymmetric Actor Critic for Image-Based Robot Learning.” in _Robotics: Science and Systems Conference (RSS)_ , 2018. 

   - [9] B. Tang, M. A. Lin, I. Akinola, A. Handa, G. S. Sukhatme, F. Ramos, D. Fox, and Y. S. Narang, “Industreal: Transferring Contact-Rich Assembly Tasks from Simulation to Reality.” in _Robotics: Science and Systems Conference (RSS)_ , 2023. 

   - [10] Y. Lee, E. S. Hu, and J. J. Lim, “IKEA Furniture Assembly Environment for Long-Horizon Complex Manipulation Tasks,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2021, pp. 6343–6349. 

   - [11] A. Nair, B. McGrew, M. Andrychowicz, W. Zaremba, and P. Abbeel, “Overcoming Exploration in Reinforcement Learning with Demonstrations.” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2018, pp. 6292–6299. 

   - [12] M. Plappert, M. Andrychowicz, A. Ray, B. McGrew, B. Baker, G. Powell, J. Schneider, J. Tobin, M. Chociej, P. Welinder _et al._ , “Multi-goal reinforcement learning: Challenging robotics environments and request for research,” _arXiv preprint arXiv:1802.09464_ , 2018. 

   - [13] A. Gupta, V. Kumar, C. Lynch, S. Levine, and K. Hausman, “Relay Policy Learning: Solving Long-Horizon Tasks via Imitation and Reinforcement Learning.” in _Conference on Robot Learning (CoRL)_ , 2019, pp. 1025–1037. 

   - [14] Y. Zhu, J. Wong, A. Mandlekar, R. Mart´ın-Mart´ın, A. Joshi, S. Nasiriany, and Y. Zhu, “robosuite: A modular simulation framework and benchmark for robot learning,” in _arXiv preprint arXiv:2009.12293_ , 2020. 

   - [15] Q. Gallou´edec, N. Cazin, E. Dellandr´ea, and L. Chen, “panda-gym: Open-source goal-conditioned environments for robotic learning,” _arXiv preprint arXiv:2106.13687_ , 2021. 

   - [16] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, and G. State, “Isaac Gym: High Performance GPU Based Physics Simulation For Robot Learning.” in _Conference on Neural Information Processing Systems (NeurIPS)_ , 2021. 

   - [17] Y. S. Narang, K. Storey, I. Akinola, M. Macklin, P. Reist, L. Wawrzyniak, Y. Guo, A.<sup>´</sup> Morav´anszky, G. State, M. Lu, A. Handa, and D. Fox, “Factory: Fast Contact for Robotic Assembly.” in _Robotics: Science and Systems Conference (RSS)_ , 2022. 

   - [18] A. Petrenko, A. Allshire, G. State, A. Handa, and V. Makoviychuk, “Dexpbt: Scaling up Dexterous Manipulation for Hand-Arm Systems with Population Based Training.” in _Robotics: Science and Systems Conference (RSS)_ , 2023. 

   - [19] T. Erez, Y. Tassa, and E. Todorov, “Simulation tools for model-based robotics: Comparison of Bullet, Havok, MuJoCo, ODE and PhysX.” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2015, pp. 4397–4404. 

   - [20] T. P. Lillicrap, J. J. Hunt, A. Pritzel, N. Heess, T. Erez, Y. Tassa, D. Silver, and D. Wierstra, “Continuous control with deep reinforcement learning,” in _International Conference on Learning Representations (ICLR)_ , 2016. 

   - [21] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, “Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor.” in _International Conference on Machine Learning (ICML)_ , 2018, pp. 1856–1865. 

   - [22] T. Haarnoja, A. Zhou, K. Hartikainen, G. Tucker, S. Ha, J. Tan, V. Kumar, H. Zhu, A. Gupta, P. Abbeel _et al._ , “Soft Actor-Critic algorithms and applications,” _arXiv preprint arXiv:1812.05905_ , 2018. 

   - [23] A. Kuznetsov, P. Shvechikov, A. Grishin, and D. P. Vetrov, “Controlling Overestimation Bias with Truncated Mixture of Continuous Distributional Quantile Critics.” in _International Conference on Machine Learning (ICML)_ , 2020, pp. 5556–5566. 

   - [24] A. Raffin, A. Hill, A. Gleave, A. Kanervisto, M. Ernestus, and N. Dormann, “Stable-baselines3: Reliable reinforcement learning implementations,” _Journal of Machine Learning Research_ , vol. 22, no. 268, pp. 1–8, 2021. [Online]. Available: http://jmlr.org/papers/v22/20-1364.html 

   - [25] M. Andrychowicz, D. Crow, A. Ray, J. Schneider, R. Fong, P. Welinder, B. McGrew, J. Tobin, P. Abbeel, and W. Zaremba, “Hindsight Experience Replay.” in _Conference on Neural Information Processing Systems (NeurIPS)_ , 2017, pp. 5048–5058. 

   - [26] S. Fujimoto, H. v. Hoof, and D. Meger, “Addressing Function Approximation Error in Actor-Critic Methods.” in _International Conference on Machine Learning (ICML)_ , 2018, pp. 1582–1591. 

- [8] Y. Chebotar, A. Handa, V. Makoviychuk, M. Macklin, J. Issac, N. Ratliff, and D. Fox, “Closing the sim-to-real loop: Adapting simulation randomization with real world experience,” in _2019 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2019, pp. 8973–8979. 

