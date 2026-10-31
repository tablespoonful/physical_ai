---
title: "Humanoid-Gym: Reinforcement Learning for Humanoid Robot with Zero-Shot Sim2Real Transfer"
date: "2024-04-08"
authors: "Xinyang Gu; Yen-Jen Wang; Jianyu Chen"
url: https://arxiv.org/abs/2404.05695
pdf: https://arxiv.org/pdf/2404.05695
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2404.05695)** / [論文ページ](https://arxiv.org/abs/2404.05695)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Humanoid-Gym: Reinforcement Learning for Humanoid Robot with Zero-Shot Sim2Real Transfer** 

Xinyang Gu<sup>2</sup><sup>_∗_</sup> , Yen-Jen Wang<sup>13</sup><sup>_∗_</sup> , Jianyu Chen<sup>123</sup> 

**_Abstract_ — Humanoid-Gym is an easy-to-use reinforcement learning (RL) framework based on Nvidia Isaac Gym, designed to train locomotion skills for humanoid robots, emphasizing zero-shot transfer from simulation to the realworld environment. Humanoid-Gym also integrates a sim-tosim framework from Isaac Gym to Mujoco that allows users to verify the trained policies in different physical simulations to ensure the robustness and generalization of the policies. This framework is verified by RobotEra’s XBot-S (1.2-meter tall humanoid robot) and XBot-L (1.65-meter tall humanoid robot) in a real-world environment with zero-shot sim-to-real transfer. The project website and source code can be found at: sites.google.com/view/humanoid-gym.** 

## I. INTRODUCTION 

Modern environments are primarily designed for humans. Therefore, humanoid robots, with their human-like skeletal structure, are especially suited for tasks in human-centric environments, offering unique advantages over other types of robots. Recently, massively parallel deep reinforcement learning (RL) in simulation has become popular [1], [2], [3]. However, due to the complex structure of humanoid robots, the sim-to-real gap [4], [5], [6], [7] exists and is larger than that of quadrupedal robots. Therefore, we release HumanoidGym, an easy-to-use RL framework based on Nvidia Isaac Gym [8], designed to train locomotion skills for humanoid robots, emphasizing zero-shot transfer from simulation to the real-world environment. Humanoid-Gym features specialized rewards and domain randomization techniques for humanoid robots, simplifying the difficulty of sim-to-real transfer. Furthermore, it also integrates a sim-to-sim framework from Isaac Gym [8] to MuJoCo [9] that allows users to verify the trained policies in different physical simulations to ensure the robustness and generalization of the policies, shown in Fig. 1. Currently, Humanoid-Gym is verified by multiple humanoid robots with different sizes in a real-world environment with zero-shot sim-to-real transfer, including RobotEra’s XBot-S (1.2-meter tall humanoid robot) and XBot-L (1.65-meter tall humanoid robot) [10]. The contribution of Humanoid-Gym can be summarized as follows: 

- We launch an open-source reinforcement learning (RL) framework with meticulous system design. 

- Our framework enables zero-shot transfer from simulation to the real world, which has been rigorously tested across humanoid robots of various sizes. 

> _∗_ Equal contribution. Listed alphabetically. 

> 1Shanghai Qi Zhi Institute, Shanghai, China. 

> 2RobotEra TECHNOLOGY CO., LTD., Beijing, China 

> 3Tsinghua University, Beijing, China. 


**(b) Zero-Shot Sim-to-Real Transfer** 

Fig. 1: Humanoid-Gym enables users to train their policies within Nvidia Isaac Gym and validate them in MuJoCo. Additionally, we have successfully tested the complete pipeline with two humanoid robots. They were trained in HumanoidGym and transferred to real-world environments in a zeroshot manner. 

- Our open-source library features a sim-to-sim validation tool, enabling users to test their policies across diverse environmental dynamics rigorously. 

## II. RELATED WORKS 

## _A. Robot Learning on Locomotion Tasks_ 

Reinforcement learning (RL) has shown promise in enabling robots to achieve stable locomotion [6], [11], [12]. Compared to prior RL efforts with quadrupedal robots [1], [13] and bipedal robots like Cassie [14], [15], our work with humanoid robots introduces a more challenging scenario for robot control. Recent studies [16], [17] have applied transformer architecture to improve the walking performance of humanoid robots on flat surfaces. Beyond lower-body control, some works [18], [19] have also explored more complex upper-body skills for humanoid robot control. However, 


Fig. 2: Pipeline of Humanoid-Gym. Initially, we employ massively parallel deep reinforcement learning (RL) within Nvidia Isaac Gym, incorporating diverse terrains and dynamics randomization. Subsequently, we undertake sim-to-sim transfer to test policies. Due to our meticulous calibration, the performance in both MuJoCo and real-world settings aligns closely. 

the sim-to-real transition for humanoid locomotion remains a significant challenge, with a notable lack of open-source resources in the robot learning community. To contribute to this area, we have developed Humanoid-Gym, an accessible framework with full codebase. 

## III. METHOD 

The workflow of Humanoid-Gym is illustrated in Fig. 2. In this section, we will introduce the problem setting, system design, and reward design of our Humanoid-Gym. 


## _B. System design_ 

The base poses of the robot, denoted as _P_<sup>_b_</sup> , are sixdimensional vectors [ _x, y, z, α, β, γ_ ], representing both the position coordinates _x, y, z_ and the orientation angles _α, β, γ_ in Euler notation. The joint position for each motor is represented by _θ_ , and the corresponding joint velocity by _θ_<sup>˙</sup> . Furthermore, we define a gait phase [24], [25], which comprises two double support phases (DS) and two single support phases (SS) within each gait cycle. The cycle time, denoted as _CT_ , is the duration of one full gait cycle. A sinusoidal wave is employed to generate reference motion, reflecting the repetitive nature of the gait cycle involving pitch, knee, and ankle movements. Notably, we also designed a periodic stance mask _Ip_ ( _t_ ) (Fig 6) that indicates foot contact patterns in synchronization with the reference motion. For instance, if the reference motion lifts the left foot, the right foot should be in the single support phase, with the foot contact mask indicated as [0 _,_ 1]; during DS phases, it would be [1 _,_ 1]. 

The chosen action is the target joint position for the Proportional-Derivative (PD) controller. The policy network integrates proprioceptive sensor data, a periodic clock signal [sin(2 _πt/CT_ ) _,_ cos(2 _πt/CT_ )], and velocity commands _P_ ˙ _x,y,γ_ . A single frame of input are elaborated in Table I. Additionally, the state frame includes feet contact detect _Id_ ( _t_ ) and other privileged observations. 

TABLE I: Summary of Observation Space. The table categorizes the components of the observation space into observation and state. The table also details their dimensions. 

## _A. Reinforcement Learning For Robot Control_ 

Our approach employs a reinforcement learning model _M_ = _⟨S, A, T, O, R, γ⟩_ , with _S_ and _A_ denoting state and action spaces, _T_ ( **s**<sup>_′_</sup> _|_ **s** _,_ **a** ) the transition dynamics, _R_ ( **s** _,_ **a** ) the reward function, _γ ∈_ [0 _,_ 1] the discount factor, and _O_ the observation space. The framework is designed for both simulated and real-world settings, transitioning from full observability in simulations ( **s** _∈S_ ) to partial observability in the real world ( **o** _∈O_ ). This necessitates operating within a Partially Observable Markov Decision Process (POMDP) [20], with the policy _π_ ( **a** _|_ **o** _≤t_ ) mapping observations to action distributions to maximize the expected return _J_ = E[ _Rt_ ] = E [<sup>�</sup> _t_<sup>_γtrt_].</sup> 

We leverage Proximal Policy Optimization (PPO) [21] loss, supplemented by the Asymmetric Actor Critic [22] method and the integration of privileged information during training, shifting to partial observations during deployment. The policy loss is defined as: 


Advantage estimation utilizes Generalized Advantage Estimation (GAE) [23], requiring an updated value function: 

|**Components**|**Dims**|**Observation**|**State**|
|---|---|---|---|
|Clock Input (sin(_t_)_,_cos(_t_))<br><sup>˙</sup>|2|✓|✓|
|Commands ( _Px,y,γ_)<br>|3|✓|✓|
|Joint Position (_θ_)<br><sup>˙</sup>|12|✓|✓|
|Joint Velocity (_θ_)<br><sup>˙</sup>|12|✓|✓|
|Angular Velocity ( _P _<sup>_b_</sup><br>_αβγ_<sup>)</sup><br>|3|✓|✓|
|Euler Angle (_P _<sup>_b_</sup><br>_αβγ_<sup>)</sup>|3|✓|✓|
|Last Actions (_at−_1)|12|✓|✓|
|Frictions|1||✓|
|Body Mass|1||✓|
|Base Linear Velocity|3||✓|
|Push Force|2||✓|
|Push Torques|3||✓|
|Tracking Difference|12||✓|
|Periodic Stance Mask|2||✓|
|Feet Contact detection|2||✓|


Our control policy operates at a high frequency of 100Hz, providing enhanced granularity and precision beyond standard RL locomotion approaches. The internal PD controller runs at an even higher frequency of 1000Hz. For training simulations, Isaac Gym is utilized [8], while MuJoCo, known for its accurate physical dynamics, is chosen for sim2sim validation. This approach combines the benefits of high-speed GPU-based parallel simulation, albeit with less accuracy, and the high accuracy but slower CPU-based simulation. 

The detailed settings for both algorithms and the environment designed are shown in Appendix TABLE II. We 

use multi-frames of observations and privilege observation, which is crucial for locomotion tasks on uneven terrain. 

## _C. Reward Design_ 

Our reward function directs the robot to adhere to velocity commands, sustain a stable gait, and achieve smooth contact. The reward function is structured into four key components: (1) velocity tracking, (2) gait reward, and (3) regularization terms. 

The reward function is summarized in Appendix Table IV. It is important to note that the commands CMD _z,γ,β_ (velocity mismatch term) are intentionally set to zero. This is because we do not control them; rather, we aim to maintain their values at zero to ensure stable and smooth walking. In addition, the reward (contact pattern) encourages feet to align with their contact masks, denoting swing, and stance phases, as illustrated in Appendix Fig. 6. Therefore, the total reward at any time step _t_ is computed as the weighted sum of individual reward components, expressed as _rt_ =<sup>�</sup> _i_<sup>_ri · µi_,</sup> where _µi_ represents the weighting factor for each reward component _ri_ . 

## IV. EXPERIMENTS 

In this section, we will illustrate the result of zeroshot transfer for both sim-to-sim and sim-to-real scenarios. Additionally, we also provide visualization of the calibration for MuJoCo to verify the effectiveness of sim-to-sim. For the validation, we utilized Robot Era’s humanoid robots, XBot-S and XBot-L, measuring 1.2 meters and 1.65 meters in height, shown in Appendix Fig. 5, respectively. 

## _A. Zero-shot Transfer_ 

We carefully design domain randomization terms, as detailed in Appendix TABLE III, to minimize the sim2real gap, following the approach outlined in [26]. Our agents are capable of transitioning to real-world environments via zero-shot sim-to-real transfer, which is illustrated in Fig. 1. The standard procedure involves training agents on GPUs, followed by policy analysis in MuJoCo. For a comprehensive evaluation, we developed two types of terrains: flat and uneven, as depicted in Appendix Fig. 7. The flat terrain replicates the environment encountered during training in Isaac Gym, while the uneven terrain offers a substantially more challenging landscape, differing significantly from our initial training scenarios. Remarkably, our trained policies enable the robots to traverse both types of terrain successfully. 

## _B. Calibration for MuJoCo_ 

We meticulously calibrated the MuJoCo environment to align its dynamics and performance more closely with that of the real world. By comparing the leg swing sine waves in both the MuJoCo and the real-world environments, which represent joint positions over time that track a specified sine wave, we observed nearly identical trajectories. These are depicted in Fig. 3. Furthermore, we also compare the resulting phase portrait of the left knee joint and left ankle pitch joint[17] within 5-second trajectories, 0.5 n/s heading 

velocity, as shown in Fig. 4. It is clear to see that the dynamics in MuJoCo are closer to the real environment than Isaac Gym. 


Fig. 3: Sine wave in Both MuJoCo and real-world environment. It can be found that the trajectories of the two are very close after calibration. 


Fig. 4: Phase Portrait for MuJoCo, Real-World Environment, and Isaac Gym. 

## V. CONCLUSIONS 

Humanoid-Gym facilitates zero-shot transfer for humanoid robots of two distinct sizes, from sim-to-sim and sim-toreal, via a specialized reward function tailored for humanoid robotics. Our experimental outcomes reveal that the adjusted MuJoCo simulation closely mirrors the dynamics and performance of the real-world environment. This congruence enables researchers lacking physical robots to validate training policies through sim-to-sim, significantly enhancing the potential for successful sim-to-real transfers. 

## ACKNOWLEDGMENT 

The implementation of Humanoid-Gym relies on resources from legged ~~g~~ ym and rsl ~~r~~ l projects[1] created by the Robotic Systems Lab. We specifically utilize the ‘LeggedRobot‘ implementation from their research to enhance our codebase. 

REFERENCES 

- [1] N. Rudin, D. Hoeller, P. Reist, and M. Hutter, “Learning to walk in minutes using massively parallel deep reinforcement learning,” in _Conference on Robot Learning_ . PMLR, 2022, pp. 91–100. 

- [2] A. Kumar, Z. Fu, D. Pathak, and J. Malik, “Rma: Rapid motor adaptation for legged robots,” _arXiv preprint arXiv:2107.04034_ , 2021. 

- [3] Y. Guo, Z. Jiang, Y.-J. Wang, J. Gao, and J. Chen, “Decentralized motor skill learning for complex robotic systems,” _IEEE Robotics and Automation Letters_ , 2023. 

- [4] X. B. Peng, M. Andrychowicz, W. Zaremba, and P. Abbeel, “Sim-toreal transfer of robotic control with dynamics randomization,” in _2018 IEEE international conference on robotics and automation (ICRA)_ . IEEE, 2018, pp. 3803–3810. 

- [5] W. Zhao, J. P. Queralta, and T. Westerlund, “Sim-to-real transfer in deep reinforcement learning for robotics: a survey,” in _2020 IEEE symposium series on computational intelligence (SSCI)_ . IEEE, 2020, pp. 737–744. 

- [6] J. Tan, T. Zhang, E. Coumans, A. Iscen, Y. Bai, D. Hafner, S. Bohez, and V. Vanhoucke, “Sim-to-real: Learning agile locomotion for quadruped robots,” _arXiv preprint arXiv:1804.10332_ , 2018. 

   - [21] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

   - [22] L. Pinto, M. Andrychowicz, P. Welinder, W. Zaremba, and P. Abbeel, “Asymmetric actor critic for image-based robot learning,” _arXiv preprint arXiv:1710.06542_ , 2017. 

   - [23] J. Schulman, P. Moritz, S. Levine, M. Jordan, and P. Abbeel, “Highdimensional continuous control using generalized advantage estimation,” _arXiv preprint arXiv:1506.02438_ , 2015. 

   - [24] J. Siekmann, Y. Godse, A. Fern, and J. Hurst, “Sim-to-real learning of all common bipedal gaits via periodic reward composition,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2021, pp. 7309–7315. 

   - [25] Y. Yang, T. Zhang, E. Coumans, J. Tan, and B. Boots, “Fast and efficient locomotion via learned gait transitions,” in _Conference on robot learning_ . PMLR, 2022, pp. 773–783. 

   - [26] J. Tobin, R. Fong, A. Ray, J. Schneider, W. Zaremba, and P. Abbeel, “Domain randomization for transferring deep neural networks from simulation to the real world,” in _2017 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ . IEEE, 2017, pp. 23–30. 

- [7] A. Kadian, J. Truong, A. Gokaslan, A. Clegg, E. Wijmans, S. Lee, M. Savva, S. Chernova, and D. Batra, “Sim2real predictivity: Does evaluation in simulation predict real-world performance?” _IEEE Robotics and Automation Letters_ , vol. 5, no. 4, pp. 6670–6677, 2020. 

- [8] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, _et al._ , “Isaac gym: High performance gpu-based physics simulation for robot learning,” _arXiv preprint arXiv:2108.10470_ , 2021. 

- [9] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control,” in _2012 IEEE/RSJ international conference on intelligent robots and systems_ . IEEE, 2012, pp. 5026–5033. 

- [10] RobotEra, “Robotera technology co.,ltd.” [Online]. Available: https: //www.robotera.com/ 

- [11] J. Hwangbo, J. Lee, A. Dosovitskiy, D. Bellicoso, V. Tsounis, V. Koltun, and M. Hutter, “Learning agile and dynamic motor skills for legged robots,” _Science Robotics_ , vol. 4, no. 26, p. eaau5872, 2019. 

- [12] J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning quadrupedal locomotion over challenging terrain,” _Science robotics_ , vol. 5, no. 47, p. eabc5986, 2020. 

- [13] G. B. Margolis, G. Yang, K. Paigwar, T. Chen, and P. Agrawal, “Rapid locomotion via reinforcement learning,” _The International Journal of Robotics Research_ , p. 02783649231224053, 2022. 

- [14] Z. Li, X. Cheng, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Reinforcement learning for robust parameterized locomotion control of bipedal robots,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2021, pp. 2811–2817. 

- [15] A. Kumar, Z. Li, J. Zeng, D. Pathak, K. Sreenath, and J. Malik, “Adapting rapid motor adaptation for bipedal robots,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2022, pp. 1161–1168. 

- [16] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Learning humanoid locomotion with transformers,” _arXiv preprint arXiv:2303.03381_ , 2023. 

- [17] I. Radosavovic, B. Zhang, B. Shi, J. Rajasegaran, S. Kamat, T. Darrell, K. Sreenath, and J. Malik, “Humanoid locomotion as next token prediction,” _arXiv preprint arXiv:2402.19469_ , 2024. 

- [18] T. He, Z. Luo, W. Xiao, C. Zhang, K. Kitani, C. Liu, and G. Shi, “Learning human-to-humanoid real-time whole-body teleoperation,” _arXiv preprint arXiv:2403.04436_ , 2024. 

- [19] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” _arXiv preprint arXiv:2402.16796_ , 2024. 

- [20] M. T. Spaan, “Partially observable markov decision processes,” in _Reinforcement learning: State-of-the-art_ . Springer, 2012, pp. 387– 414. 

APPENDIX 


Fig. 5: Hardware Platform. Our Humanoid-Gym framework is tested on two distinct sizes of humanoid robots, XBot-S and XBot-L, provided by Robot Era. 


Fig. 6: The stance mask is the contact planning for the left (L) and right (R) feet, where 0 indicates the swing phase and 1 indicates the stance phase is expected. 


Fig. 7: Terrains in MuJoCo. Humanoid-Gym provides two types of terrains utilized for sim-to-sim validation: flat planes and uneven terrains. 

TABLE II: Hyperparameters. 

|**Parameter**|**Value**|
|---|---|
|Number of Environments|8192|
|Number Training Epochs|2|
|Batch size|8192_×_24|
|Episode Length|2400 steps|
|Discount Factor|0.994|
|GAE discount factor|0.95|
|Entropy Regularization Coefficient|0.001|
|_c_1|0.8|
|_c_2|1.2|
|Learning rate|1e-5|
|Frame Stack of Single Observation|15|
|Frame Stack of Single Privileged Observation|3|
|Number of Single Observation|47|
|Number of Single Privileged Observation|73|


TABLE III: Overview of Domain Randomization. Presented are the domain randomization terms and the associated parameter ranges. Additive randomization increments the parameter by a value within the specified range while scaling randomization adjusts it by a multiplicative factor from the same range. 

|**Parameter**|**Unit**|**Range**|**Operator**|**Type**|
|---|---|---|---|---|
|Joint Position|rad|[-0.05, 0.05]|additive|Gaussian (1_σ_)|
|Joint Velocity|rad/s|[-0.5, 0.5]|additive|Gaussian (1_σ_)|
|Angular Velocity|rad/s|[-0.1, 0.1]|additive|Gaussian (1_σ_)|
|Euler Angle|rad|[-0.03, 0.03]|additive|Gaussian (1_σ_)|
|System Delay|ms|[0, 10]|-|Uniform|
|Friction|-|[0.1, 2.0]|-|Uniform|
|Motor Strength|%|[95, 105]|scaling|Gaussian (1_σ_)|
|Payload|kg|[-5, 5]|additive|Gaussian (1_σ_)|


TABLE IV: In defining the reward function, we use a tracking error metric denoted by _ϕ_ ( _e, w_ ). This metric is expressed as _ϕ_ ( _e, w_ ) := exp( _−w · ∥e∥_<sup>2</sup> ) _,_ where _e_ represents the tracking error, and _w_ is the associated weight. The target base height is set to 0 _._ 7 m. 

|**Reward**|**Equation (**_ri_**)**|**reward scale(**_µi_**)**|
|---|---|---|
|Lin. velocity tracking|_ϕ_( <sup>˙</sup>_P _<sup>_b_</sup><br>_xyz _<sup>_−_CMD</sup><sup>_xyz,_ 5)</sup><br><sup>˙</sup>|1.2|
|Ang. velocity tracking|_ϕ_( _P _<sup>_b_</sup><br>_αβγ _<sup>_−_CMD</sup><sup>_αβγ,_ 5)</sup><br>|1.0|
|Orientation tracking|_ϕ_(_P _<sup>_b_</sup><br>_αβ_<sup>_,_ 5)</sup><br>|1.0|
|Base height tracking|_ϕ_(_P _<sup>_b_</sup><br>_z _<sup>_−_0</sup><sup>_._7</sup><sup>_,_ 100)</sup><br><sup>˙</sup>|0.5|
|Velocity mismatch|_ϕ_( _P _<sup>_b_</sup><br>_z,γ,β _<sup>_−_CMD</sup><sup>_z,γ,β,_ 5)</sup>|0.5|
|Contact Pattern|_ϕ_(_Ip_(_t_)_−Id_(_t_)_, ∞_)<br>|1.0|
|Joint Position Tracking|_ϕ_(_θ −θ_target_,_2)<br>|1.5|
|Default Joint|_ϕ_(_θt −θ_0_,_2)<br><sup>˙</sup>|0.2|
|Energy Cost|_|τ||_ _θ|_|-0.0001|
|Action Smoothness|_∥at −_2_at−_1+_at−_2_∥_2<br>|-0.01|
|Large contact|max(_FL,R −_400_,_0_,_100)|-0.01|


