---
title: "Enhancing Sim2Real Transfer for Torque-Controlled Robots through Real2Sim Dynamics Estimation and Reinforcement Learning"
date: "2026-08-23"
authors: "Davide Bargellini; Alex Pasquali; Andrea Govoni; Riccardo Zanella; Gianluca Palli"
url: https://arxiv.org/abs/2608.22629
pdf: https://arxiv.org/pdf/2608.22629
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2608.22629)** / [論文ページ](https://arxiv.org/abs/2608.22629)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Enhancing Sim2Real Transfer for Torque-Controlled Robots through Real2Sim Dynamics Estimation and Reinforcement Learning** 

Davide Bargellini<sup>1</sup> Alex Pasquali<sup>1</sup> Andrea Govoni<sup>1</sup> Riccardo Zanella<sup>2</sup> and Gianluca Palli<sup>1</sup> 

**_Abstract_ —Transferring reinforcement learning policies from simulation to Real-World robots remains a major challenge, particularly when dealing with low-level torque control, where even small modelling inaccuracies can lead to unstable or unsafe behaviours. In this work, we propose a Real2Sim2Real pipeline that improves Sim2Real transfer for torque-controlled robotic arms by combining trajectory matching, parameter optimization via genetic algorithms, and domain randomization. Using the 7-DOF Franka Emika Panda robot, we first identify friction, inertia, and gravity compensation parameters by minimizing the error between real and simulated joint trajectories. These calibrated dynamics are then used to train a TQC-based reinforcement learning agent in simulation. The trained policy is evaluated in both Gazebo and MuJoCo environments, and finally deployed on the real robot. Our results demonstrate a significant improvement in tracking accuracy and policy robustness after parameter tuning, with smooth policy transfer from simulation to the Real-World across multiple target-reaching tasks. This work highlights the effectiveness of accurate physical modelling in enabling stable and generalizable torque-based reinforcement learning policies.** 

To mitigate this gap, recent studies have focused on improving the physical accuracy of simulations through better calibration of parameters such as dynamics, friction, and sensor feedback [8], [9], [10]. 

Our study focuses on optimizing the Sim2Real transfer, particularly emphasizing the development of a Reinforcement Learning (RL) agent using different policies such as DDPG [11], SAC [12], TD3 [13], and TQC [14], for the 7-axis Franka Emika Panda robot that utilizes joint torques to reach a position. This preliminary work aims to fill the gap in torque control before the robot interacts with the environment. The paper is organized as follows: Sec II summarizes the related works, while Sec. III provides a detailed overview of the methodology and the mathematical tools used. Finally, Sec. IV presents the experiments and results of the Sim2Real transfer, and Sec. V discusses the conclusions drawn from the developed work and outlines future directions. 

## II. RELATED WORKS 

## I. INTRODUCTION 

Torque control has emerged as a promising approach to improve interaction with the environment, since it enables more precise responses to physical forces and constraints [1], [2]. However, training directly in the real world with _joint torques_ is time-consuming, resource-intensive, and safetycritical. Simulations mitigate these limits by enabling faster and safer policy development before hardware deployment. 

However, a key challenge arises when these control policies, developed in the simulated environment, are transferred to Real-World robots [3], [4]. This issue is commonly referred to as the Sim2Real transfer problem [5]. Despite the advantages of simulation, there are often discrepancies between simulated and Real-World environments, such as differences in physical parameters or contact forces, and between different simulators themselves [6]. Each simulator may implement physics and models differently, leading to variations in the results. These discrepancies create a ”reality gap” [7], where control policies that perform well in simulation may fail to generalize in RealWorld scenarios, leading to a decline in performance. 

1D. Bargellini, A. Pasquali, A. Govoni, and G. Palli are with the Department of Electrical, Electronic, and Information Engineering (DEI), University of Bologna, 40136 Bologna, Italy. 

2R. Zanella is with the Robotics and Mechatronics (RaM) group, University of Twente, Enschede, The Netherlands. 

This work is supported by the Horizon Europe project IntelliMan-AIPowered Manipulation System for Advanced Robotic Service, Manufacturing and Prosthetics [grant number 101070136]. 

Training robotic agents in joint space is a promising approach for addressing complex robot-environment interactions, as demonstrated in [8], [15]. This method provides a deeper understanding of how the robot interacts with its surroundings and allows the exploitation of full-model dynamics. As a result, it can lead to improved performance while requiring less domain-specific knowledge, especially when dealing with complex floating-base robots with discrete contact dynamics. However, the effectiveness of an agent trained in simulation heavily depends on how accurately the physical parameters of the robot and its environment are modelled. The discrepancy between simulated and Real-World parameters, known as the reality gap, can hinder the transfer of learned policies from simulation to the Real-World (Sim2Real transfer). Therefore, accurate parameter estimation is crucial to improve the alignment between simulation and reality, and consequently, the success of the agent’s training. 

One of the most common approaches to tackle the reality gap is domain randomization (DR) [8], [10], which introduces controlled variability in simulated physical parameters, such as mass, friction, inertia, and material resistance, during agent training. This method aims to make the agent robust to uncertainties in the Real-World, allowing the robot to learn from more scenarios and achieve better results in reality. Another approach is trajectory matching [16], [17], which attempts to bridge the reality gap by using Real-World data to create simulations with dynamics that closely resemble those observed in practice. 


Fig. 1: Diagram illustrating the workflow for validating and executing an RL policy in both simulation and Real-World scenarios. The process includes parameter estimation (e.g., torque/position curves, friction, inertias, and gravity compensation), training via RL (TQC with GridSearch optimization), policy validation, and execution for Real2Sim and Sim2Real applications. 

RL algorithms enable robots to adapt and learn in dynamic, uncertain environments. They can optimize control strategies for motor torques based on feedback, improving control accuracy and efficiency, and ultimately enhancing the robot’s performance across a wide range of tasks and environments [15]. 

One of the challenges in using RL with torque control is the complexity of modelling motor dynamics, especially when considering interactions between motors and their impact on the robot’s movement. Designing control algorithms that can effectively manage motor torques requires a deep understanding of the system’s dynamics. 

The challenge we address is how to accurately encode realistic dynamics by reducing the gap between simulation and reality, aiming to achieve robot behaviour in simulation that closely reflects Real-World dynamics through careful fine-tuning of parameters, particularly friction and inertia, using trajectory matching and genetic algorithm [18], [19]. Friction parameters are calculated based on [20], while inertia parameters are optimized using trajectory matching, through a genetic optimization algorithm discussed in detail in Sec. III-B. Once these initial parameters are estimated, the RL agent is trained over a domain randomized around that value. This approach aims to ensure more robust performance in RealWorld tasks. 

## III. METHODOLOGIES 

This section presents the methodology used to achieve torque-level control on robotic manipulators. We first reduce the Sim2Real gap by calibrating key dynamics parameters via Real2Sim trajectory matching, using a genetic algorithm to minimize the discrepancy between measured and simulated joint responses. The resulting calibrated simulator is then used to train a control policy entirely in simulation, improving the fidelity of policy transfer to the real robot. 

## _A. Reinforcement Learning Overview_ 

In robotics, RL is often used to learn control policies directly from interaction, which is convenient when torque-level behaviours must emerge from complex robot–environment dynamics. An agent interacts with an environment, chooses actions from its current state, receives reward feedback, and updates its behaviour to maximize long-term cumulative reward through exploration and exploitation. In this work, RL’s agent is a 7-DoF Franka Emika Panda arm. To obtain a policy that outputs joint torque commands. The policy is trained to reach Cartesian target positions in the workspace while maintaining smooth and stable motion in transfer from simulation to the real robot. 

The RL agent is trained in simulation, using techniques such as DR to ensure robust performance when transferring the learned control policies to Real-World scenarios. The agent’s goal is mathematically represented as maximizing the expected cumulative reward, defined as: 


where _Rt_ is the expected cumulative reward at time _t_ , _rt_ + _k_ is the reward received at time _t_ + _k_ , and _γ_ is the discount factor, which determines the importance of future rewards. 

The reward function _r_ for the RL agent, in our environment, is expressed as: 


Here, _k_ 1 _, ..., k_ 6 are positive scaling constants. In our settings: _k_ 1 = 2 weights distance-to-goal, _k_ 2 = 0 _._ 03 weights 

velocity penalty, _k_ 3 = 0 _._ 05 weights acceleration penalty, and _k_ 4 = 1 _._ 15 _, k_ 5 = 0 _._ 03 _, k_ 6 = 0 _._ 15 are small positive constants used in the acceleration denominators. The normalized distance _d_ is evaluated keeping the maximum distance as the norm between the end effector’s initial position and the target. _θ_ ˙ _i_ and _θ_ ¨ _i_ denote joint velocity and acceleration; tanh bounds their contributions to encourage smooth motions. 

The reward function is designed to balance accuracy in reaching the goal position with smooth and energy-efficient joint movements. The first term encourages proximity to the goal, while the velocity and acceleration penalties (via _θ_<sup>˙</sup> _i_ and _θ_ ¨ _i_ ) discourage abrupt or unstable motion. The use of tanh ensures numerical stability and limits the influence of extreme values. 

Through iterative training, the agent learns to associate specific joint torques with successful task completion, gradually improving its policy _π_ to minimize errors and enhance task efficiency. The policy update can be expressed as: 


where Θ _t_ represents the parameters of the policy at time _t_ , _η_ ( _t_ ) is the learning rate, _L_ (Θ) is the loss function and _∇L_ denotes the gradient of the loss [21]. 

This approach fundamentally relies on tuning the reward function and simulation parameters to replicate Real-World dynamics closely. 

## _B. The Parameter Estimation Problem_ 

The effectiveness of RL in robotic control is heavily influenced by the accuracy of the model parameters that define the robot’s dynamics. In this section, we focus on the parameter estimation problem. 

To describe the robot’s dynamics, we consider the standard equation of motion for an _n_ -DOF manipulator: 


where _τ_ is the vector of joint torques, _M_ ( _q_ ) is the inertia matrix, _C_ ( _q, q_ ˙) represents Coriolis friction and centrifugal effects, and _G_ ( _q_ ) is the gravity vector. In simulation, inertial and geometric parameters are taken from the robot description file. Instead of using standard friction and damping coefficients from the robot description file, they are modelled separately, following the identified parameters in [20], [22], and include directional asymmetry, i.e., different friction levels for positive and negative joint velocities. For each joint _j_ , the (velocitydependent) dynamic friction torque is computed as: 


Where _τf,j_ is the friction compensation torque, _φ_ 1 _,j_ , _φ_ 2 _,j_ , and _φ_ 3 _,j_ are parameters specific to each joint to be estimated. Static friction is not identified by the velocity-dependent model in eq.(5) and is instead introduced manually as a joint-wise term. In practice, we define a dead-zone around zero velocity, 

i.e., _|_ ˙ _qj| < q_ ˙min, within which a constant breakaway torque _τj_<sup>st</sup> (tuned empirically for each joint) is applied with sign given by the desired motion direction: 


The estimation problem for these parameters is based on minimizing the error between the simulated and Real-World trajectories, which is expressed as: 


where _E_ ( **p** ) is the error function, **y** sim( _t,_ **p** ) is the simulated trajectory based on the parameter set **p** , **y** real( _t_ ) is the corresponding Real-World trajectory, and _T_ is the total time of observation. Minimizing this error ensures that the simulated dynamics closely replicate the Real-World behaviour, serving as the basis for successful policy transfer. Each optimization iteration improves the fidelity of simulated joint trajectories. 

To bridge the simulation-to-reality gap, we adopted a genetic algorithm approach [18] that minimizes trajectory tracking error by iteratively adjusting the parameter set **p** for each joint, which includes the previously mentioned parameters in eq.(4). The algorithm calibrates the simulated joint dynamics to better match Real-World behaviour, improving Sim2Real transfer of the learned control policies. A genetic algorithm iteratively tunes the parameters by minimizing an error metric, yielding a robust estimate that enhances the RL agent’s performance in both simulation and on the real robot (see Alg. 1) 

## **Algorithm 1** Genetic Algorithm for Parameter Estimation 

- 1: Sample a real trajectory **y** real( _t_ ) 2: **Initialize** population _P_ = _{_ **p** 1 _,_ **p** 2 _, . . . ,_ **p** _N }_ 3: **while** not converged **and** generation _< G_ max **do** 4: **for** each **p** _i ∈P_ **do** 5: Simulate trajectory **y** sim( _t,_ **p** _i_ ) 6: Compute error using Eq. 7 7: **end for** 8: Select top-performing individuals based on _E_ ( **p** _i_ ) 9: Apply mutation to generate new individuals 

- 10: Update population _P_ 11: **end while** 12: **return** best parameter set **p**<sup>_∗_</sup> 

## IV. EXPERIMENTS AND RESULTS 

We evaluated DDPG, SAC, TD3, and TQC, tuning each method via grid search. Overall, TQC provided the most robust and stable performance across metrics (Fig. 2) and showed lower sensitivity to hyperparameters, which is desirable for Sim2Real deployment. For this reason, we report the Sim2Real transfer results using TQC. 


Fig. 2: Episode mean reward comparison across DDPG, SAC, TD3, and TQC algorithms. TQC demonstrates consistently higher rewards, underscoring its superior performance and robustness in our environment. 


Fig. 3: Comparison of the Sim2Real RL model transfer for the Panda robot. (a) Joint 1 torque comparison without parameter tuning. (b) Joint 2 torque comparison without parameter tuning. (c) Joint 1 torque comparison with parameter tuning. (d) Joint 2 torque comparison with parameter tuning. 

## _A. Parameters Estimation_ 

Figs.3a and 3b show some tests at the joint level without parameter calibration, inadequate gravity compensation, and unmodelled joint dynamics in load-bearing configurations. To solve the gravity compensation issues, a torque offset was introduced for each joint, which aimed to make positive and negative trajectories visually similar. The offset values applied to each joint were determined through a manual adjustment process. The obtained torque values are described in Table I. 

Regarding the static friction, for accurate modelling, we applied a linearly increasing torque to each joint until movement was detected, establishing the minimum torque required to overcome static friction for both positive and negative directions. The resulting torque values, shown in Table II, were used in simulation to replicate Real-World conditions by setting an action threshold; if the joint velocity remained within a small range and the applied torque was below the identified threshold, the action was nullified, simulating the static friction’s hold on the joint. 

After applying the Genetic Algorithm, the resulting inertia 

**J1 J2 J3 J4 J5 J6 J7 Torque** **<u>(Nm)</u>** -0.13 -0.73 0.03 0.53 0 -0.06 0 

TABLE I: Offset Values for Gravity Compensation and static friction. 

|**Torque**|**J1**|**J2**|**J3**|**J4**|**J5**|**J6**|**J7**|
|---|---|---|---|---|---|---|---|
|**Pos.** **_τ_ (Nm)**|0.65|0.88|0.51|0.61|0.44|0.40|0.32|
|**Neg.** **_τ_ (Nm)**|-0.62|-0.81|-0.42|-0.51|-0.67|-0.23|-0.35|


TABLE II: Positive and Negative Friction Values for Each Joint. 

and friction parameters obtained are shown in Table III and IV. 

## _B. Sim2Sim_ 

In the simulation setup, the TQC agent is trained in MuJoCo to reach random target points across diverse workspace coordinates, since MuJoCo provides higher simulation speed and is therefore better suited for rapid policy training. Before deploying the agent in the Real-World, we used the Gazebo simulator with different Panda model parameters inside the training domain, in order to test the behaviour of the robot with different targets. 

The primary task for the agent is to guide the robotic arm to reach random target points within its workspace, simulating Real-World challenges where the arm must adapt to varying target positions. The agent’s adaptability is thoroughly tested by assigning random target coordinates, requiring it to handle diverse end-effector locations. In addition to target variability, DR was applied to the simulation by perturbing all 21 jointspecific friction parameters _φ_ within a range of _±_ 10%, and all 42 elements of the joint inertia matrices within a range of _±_ 5% of their previously estimated values (see Table III). These perturbation ranges were selected based on preliminary empirical tests to balance variability with stability. Larger perturbations led to unstable training, while smaller ones reduced the agent’s generalization capability. This setup not only validates the algorithm’s robustness but also highlights its practical applicability in dynamic and uncertain scenarios. 

## _C. Sim2Real_ 

In transferring our RL agent from simulation to the RealWorld environment, we focused on ensuring robust performance by preparing the agent for varied conditions during training. One technique we used to support this transition was DR, where simulated physical parameters such as friction and inertia were randomized. This method helps bridge the ”reality gap” by training the agent across a broad spectrum of conditions, making it more adaptable to Real-World uncertainties. 

After training, the agent was deployed on the physical Franka Emika Panda robot, achieving high reward scores and demonstrating reliable control. The agent’s exposure to domain-randomized parameters during simulation enabled it to generalize effectively to Real-World conditions, requiring minimal adjustments. As shown in the comparison between MuJoCo simulation and Real-World trials, the plots illustrating 

||**Inertia**|**Link 1**|**Link 2**|**Link 3**|**Link 4**|**Link 5**|**Link 6**|**Link 7**|
|---|---|---|---|---|---|---|---|---|
|**OLD**|_Ixx_<br>_Iyy_<br>_Izz_|7_._03_×_10<sup>_−_1</sup><br>7_._07_×_10<sup>_−_1</sup><br>9_._12_×_10<sup>_−_3</sup>|7_._96_×_10<sup>_−_3</sup><br>2_._81_×_10<sup>_−_2</sup><br>2_._60_×_10<sup>_−_2</sup>|3_._72_×_10<sup>_−_2</sup><br>3_._62_×_10<sup>_−_2</sup><br>1_._08_×_10<sup>_−_2</sup>|2_._59_×_10<sup>_−_2</sup><br>1_._96_×_10<sup>_−_2</sup><br>2_._83_×_10<sup>_−_2</sup>|3_._56_×_10<sup>_−_2</sup><br>2_._95_×_10<sup>_−_2</sup><br>8_._63_×_10<sup>_−_3</sup>|1_._96_×_10<sup>_−_3</sup><br>4_._35_×_10<sup>_−_3</sup><br>5_._43_×_10<sup>_−_3</sup>|1_._25_×_10<sup>_−_2</sup><br>1_._00_×_10<sup>_−_2</sup><br>4_._82_×_10<sup>_−_3</sup>|
||_Ixy_|_−_1_._39_×_10<sup>_−_4</sup>|_−_3_._93_×_10<sup>_−_3</sup>|_−_4_._76_×_10<sup>_−_3</sup>|7_._80_×_10<sup>_−_3</sup>|_−_2_._12_×_10<sup>_−_3</sup>|1_._09_×_10<sup>_−_4</sup>|_−_4_._28_×_10<sup>_−_4</sup>|
||_Ixz_<br>_Iyz_|6_._77_×_10<sup>_−_3</sup><br>1_._92_×_10<sup>_−_2</sup>|1_._03_×_10<sup>_−_2</sup><br>7_._04_×_10<sup>_−_4</sup>|_−_1_._14_×_10<sup>_−_2</sup><br>_−_1_._28_×_10<sup>_−_2</sup>|_−_1_._33_×_10<sup>_−_3</sup><br>8_._64_×_10<sup>_−_3</sup>|_−_4_._04_×_10<sup>_−_3</sup><br>2_._29_×_10<sup>_−_4</sup>|_−_1_._16_×_10<sup>_−_3</sup><br>3_._41_×_10<sup>_−_4</sup>|_−_1_._20_×_10<sup>_−_3</sup><br>_−_7_._41_×_10<sup>_−_4</sup>|
|**NEW**|_Ixx_<br>_Iyy_<br>_Izz_|5_._12_×_10<sup>_−_1</sup><br>5_._15_×_10<sup>_−_1</sup><br>6_._60_×_10<sup>_−_3</sup>|1_._09_×_10<sup>_−_2</sup><br>3_._84_×_10<sup>_−_2</sup><br>3_._56_×_10<sup>_−_2</sup>|4_._23_×_10<sup>_−_2</sup><br>4_._11_×_10<sup>_−_2</sup><br>1_._23_×_10<sup>_−_2</sup>|2_._53_×_10<sup>_−_2</sup><br>1_._91_×_10<sup>_−_2</sup><br>2_._77_×_10<sup>_−_2</sup>|4_._29_×_10<sup>_−_2</sup><br>3_._55_×_10<sup>_−_2</sup><br>1_._04_×_10<sup>_−_2</sup>|1_._48_×_10<sup>_−_3</sup><br>3_._29_×_10<sup>_−_3</sup><br>4_._10_×_10<sup>_−_3</sup>|1_._48_×_10<sup>_−_2</sup><br>1_._19_×_10<sup>_−_2</sup><br>5_._70_×_10<sup>_−_3</sup>|
||_Ixy_|_−_1_._00_×_10<sup>_−_4</sup>|_−_5_._37_×_10<sup>_−_3</sup>|_−_5_._41_×_10<sup>_−_3</sup>|7_._61_×_10<sup>_−_3</sup>|_−_2_._55_×_10<sup>_−_3</sup>|8_._20_×_10<sup>_−_5</sup>|_−_5_._10_×_10<sup>_−_4</sup>|
||_Ixz_|4_._90_×_10<sup>_−_3</sup>|1_._40_×_10<sup>_−_2</sup>|_−_1_._30_×_10<sup>_−_2</sup>|_−_1_._30_×_10<sup>_−_3</sup>|_−_4_._87_×_10<sup>_−_3</sup>|_−_8_._70_×_10<sup>_−_4</sup>|_−_1_._42_×_10<sup>_−_3</sup>|
||_Iyz_|1_._40_×_10<sup>_−_2</sup>|9_._60_×_10<sup>_−_4</sup>|_−_1_._46_×_10<sup>_−_2</sup>|8_._44_×_10<sup>_−_3</sup>|2_._80_×_10<sup>_−_4</sup>|2_._60_×_10<sup>_−_4</sup>|_−_8_._80_×_10<sup>_−_4</sup>|


TABLE III: Inertia tensor components before (Old) and after (New) optimization for the 7 links. 

||**Friction**|**J1**|**J2**|**J3**|**J4**|**J5**|**J6**|**J7**|
|---|---|---|---|---|---|---|---|---|
||_φ_1_,j_|0.55|0.87|0.64|1.28|0.84|0.30|0.56|
|**OLD**|_φ_2_,j_|5.12|9.07|10.14|5.59|8.35|17.13|10.34|
||_φ_3_,j_|0.04|0.03|-0.05|0.04|0.03|-0.02|0.01|
||_φ_1_,j_|3.40|1.98|2.51|2.44|2.60|1.19|1.55|
|**NEW**|_φ_2_,j_|9.67|28.67|9.83|18.78|4.19|5.75|1.70|
||_φ_3_,j_|0.01|0.01|-0.01|0.01|0.01|-0.01|0.01|


TABLE IV: Friction parameters before (Old) and after (New) optimization. 


Fig. 5: Visualization of the Panda robot reaching the goal in the MuJoCo simulator. The image depicts the simulated trajectory and final pose, showcasing task completion in the virtual environment. 


Fig. 6: Visualization of the Panda robot reaching the goal position in the Gazebo simulator. The image highlights the robot’s path and final pose, demonstrating successful performance in the simulated setting. trained model in a Real-World setting. 

The evaluation across different environments shows the generalizability and robustness of the trained model, allowing possible applications in Real-World settings. 

## V. CONCLUSIONS 

Fig. 4: Comparison of the TQC agent’s performance in the MuJoCo and Gazebo simulators. The plots display the rewards obtained across four random goal scenarios, emphasizing the performance variations resulting from the distinct dynamics and properties of each simulation environment. 

the Real-World evaluation indicate that the model trained with DR performs remarkably well in the actual physical environment. The end effector consistently approaches and maintains its position near the randomized goal. Notably, some minor uncertainties are observed in reaching the target, as depicted in Fig. 8 (b) and Fig. 8 (c). Despite these slight deviations, the overall performance demonstrates the effectiveness of the 

In this work, we presented a _Real2Sim2Real_ pipeline for RL in torque-controlled robots, aimed at improving Sim2Real transfer under low-level actuation. By combining trajectory matching, DR, and genetic optimization of simulation parameters, we reduced the reality gap on a 7-DOF Franka Emika Panda. 

Our results show that physics-aware system identification, especially relying on tuning a custom function of friction and inertia instead of relying on simulation friction parameters, increases simulation fidelity, enabling policies trained entirely in simulation to transfer to the real robot. Among the evaluated RL methods, TQC provided the most reliable performance. 


Fig. 7: Visualization of the Panda robot reaching the goal position in the Real-World environment. The image captures the robot’s trajectory and final pose, emphasizing successful task execution in a physical setup. 


Fig. 8: Comparison between MuJoCo and Real-World for four random goals. MuJoCo shows smoother transitions while Gazebo introduces disturbances mimicking physical inconsistencies, serving as an intermediate test-bed before real deployment. The proposed reward, balancing task accuracy and smooth actuation, led to stable and physically plausible motions. 

We validated the framework not only in Sim2Real, but also in _Sim2Sim_ across two simulators (MuJoCo and Gazebo), highlighting that the proposed calibration and training procedure is effective beyond a single simulation domain. Realrobot experiments further confirmed robustness under practical disturbances (e.g., backlash, cable drag, and unmodelled delays). 

Future directions include extending to contact-rich manipulation tasks, investigating online system identification, generalizing to other robot platforms, and integrating safetyaware RL and compliance control. 

## REFERENCES 

- [1] L. Roveda, M. Magni, M. Cantoni, D. Piga, and G. Bucca, “Human–robot collaboration in sensorless assembly task learning enhanced by uncertainties adaptation via bayesian optimization,” _Robotics and Autonomous Systems_ , 2021. 

- [2] J. Luo, E. Solowjow, C. Wen, J. A. Ojea, A. M. Agogino, A. Tamar, and P. Abbeel, “Reinforcement learning on variable impedance controller for high-precision robotic assembly,” in _2019 International Conference on Robotics and Automation (ICRA)_ , 2019. 

- [3] W. Zhao, J. P. Queralta, and T. Westerlund, “Sim-to-real transfer in deep reinforcement learning for robotics: A survey,” _arXiv preprint arXiv:2009.13303_ , 2020. 

- [4] M. Malmir, J. Josifovski, N. Klarmann, and A. Knoll, “Diarel: Reinforcement learning with disturbance awareness for robust sim2real policy transfer in robot control,” _arXiv preprint arXiv:2306.09010_ , 2023. 

- [5] B. Mehta, A. Handa, D. Fox, and F. T. Ramos, “A user’s guide to calibrating robotics simulators,” _ArXiv_ , 2020. 

- [6] J. Albardaner, A. S. Miguel, N. Garcia, and M. Dalmau, “Sim-to-real gap in rl: Use case with tiago and isaac sim/gym,” _arXiv preprint arXiv:2403.07091v2_ , 2024. 

- [7] N. Jakobi, P. Husbands, and I. Harvey, “Noise and the reality gap: The use of simulation in evolutionary robotics,” in _Advances in artificial life: Third European conference on artificial life granada, Spain, june 4–6, 1995 proceedings 3_ . Springer, 1995. 

- [8] X. B. Peng, M. Andrychowicz, W. Zaremba, and P. Abbeel, “Sim-to-real transfer of robotic control with dynamics randomization,” in _2018 IEEE International Conference on Robotics and Automation (ICRA)_ , 2018. 

- [9] Y. Du, O. Watkins, T. Darrell, P. Abbeel, and D. Pathak, “Auto-tuned sim-to-real transfer,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , 2021. 

- [10] G. Tiboni, K. Arndt, and V. Kyrki, “Dropo: Sim-to-real transfer with offline domain randomization,” _Robotics and Autonomous Systems_ , 2023. 

- [11] T. P. Lillicrap, J. J. Hunt, A. Pritzel, N. Heess, T. Erez, Y. Tassa, D. Silver, and D. Wierstra, “Continuous control with deep reinforcement learning,” 2015. [Online]. Available: https://arxiv.org/abs/1509.02971 

- [12] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, “Soft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor,” in _International conference on machine learning_ . Pmlr, 2018. 

- [13] S. Fujimoto, H. Hoof, and D. Meger, “Addressing function approximation error in actor-critic methods,” in _International conference on machine learning_ . PMLR, 2018. 

- [14] A. Kuznetsov, P. Shvechikov, A. Grishin, and D. Vetrov, “Controlling overestimation bias with truncated mixture of continuous distributional quantile critics,” in _International conference on machine learning_ . PMLR, 2020. 

- [15] D. Kim, G. Berseth, M. Schwartz, and J. Park, “Torque-based deep reinforcement learning for task-and-robot agnostic learning on bipedal robots using sim-to-real transfer,” _IEEE Robotics and Automation Letters_ , 2023. 

- [16] Y. Chebotar, A. Handa, V. Makoviychuk, M. Macklin, J. Issac, N. Ratliff, and D. Fox, “Closing the sim-to-real loop: Adapting simulation randomization with real world experience,” in _2019 International Conference on Robotics and Automation (ICRA)_ , 2019. 

- [17] P. Chang and T. Padif, “Sim2real2sim: Bridging the gap between simulation and real-world in flexible object manipulation,” in _2020 Fourth IEEE International Conference on Robotic Computing (IRC)_ , 2020. 

- [18] A. Pasquali, K. Galassi, and G. Palli, “A fast score-based method for robotic task-free point-to-point path learning,” in _2023 IEEE/ASME International Conference on Advanced Intelligent Mechatronics (AIM)_ , 2023. 

- [19] A. Pasquali, M. M. Alunni, D. Chiaravalli, and G. Palli, “Stiffness-aware genetic algorithm for robotic path finding optimization,” in _2024 IEEE International Conference on Advanced Intelligent Mechatronics (AIM)_ , 2024. 

- [20] C. Gaz, M. Cognetti, A. Oliva, P. Giordano, and A. Luca, “Dynamic identification of the franka emika panda robot with retrieval of feasible parameters using penalty-based optimization,” _IEEE Robotics and Automation Letters_ , 2019. 

- [21] Y. Wu and L. Liu, “Selecting and composing learning rate policies for deep neural networks,” _ACM Transactions on Intelligent Systems and Technology_ , 2023. 

- [22] D. Bargellini, A. Govoni, R. Zanella, and G. Palli, “Closing the sim-toreal gap for dynamics-static friction and inertial parameters: A franka robot case study,” in _European Robotics Forum 2024_ , C. Secchi and L. Marconi, Eds. Springer Nature Switzerland, 2024. 

