---
title: "Embodiment-Aware Generalist Specialist Distillation for Unified Humanoid Whole-Body Control"
date: "2026-02-03"
authors: "Quanquan Peng; Yunfeng Lin; Yufei Xue; Jiangmiao Pang; Weinan Zhang"
url: https://arxiv.org/abs/2602.02960
pdf: https://arxiv.org/pdf/2602.02960
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.02960)** / [論文ページ](https://arxiv.org/abs/2602.02960)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Embodiment-Aware Generalist Specialist Distillation for Unified Humanoid Whole-Body Control** 

Quanquan Peng<sup>1*</sup> , Yunfeng Lin<sup>1*</sup> , Yufei Xue<sup>1</sup> , Jiangmiao Pang<sup>2</sup> , Weinan Zhang<sup>1 2†</sup> 1Shanghai Jiao Tong University, 2Shanghai AI Lab 


Fig. 1: In this work, we propose a distillation framework that yields a _single_ whole-body controller that runs on heterogeneous humanoids. Through cyclic forking of embodiment-specific specialists and distillation back into the generalist, the resulting policy executes rich commands (walking, squatting, and leaning) in simulation and the real world, outperforming baselines in tracking accuracy and robustness. 

**_Abstract_ —Humanoid Whole-Body Controllers trained with reinforcement learning (RL) have recently achieved remarkable performance, yet many target a single robot embodiment. Variations in dynamics, degrees of freedom (DoFs), and kinematic topology still hinder a single policy from commanding diverse humanoids. Moreover, obtaining a generalist policy that not only transfers across embodiments but also supports richer behaviors—beyond simple walking to squatting, leaning— remains especially challenging. In this work, we tackle these obstacles by introducing EAGLE, an iterative generalist-specialist distillation framework that produces a single unified policy that controls multiple heterogeneous humanoids without per-robot reward tuning. During each cycle, embodiment-specific specialists are forked from the current generalist, refined on their respective robots, and new skills are distilled back into the generalist by training on the pooled embodiment set. Repeating this loop until performance convergence produces a robust Whole-Body Controller validated on robots such as Unitree H1, G1, and Fourier N1. We conducted experiments on five different robots in simulation and four in real-world settings. Through quantitative evaluations, EAGLE achieves high tracking accuracy and robustness compared to other methods, marking a step toward scalable, fleet-level humanoid control.** 

# I. INTRODUCTION 

Training one policy that can transfer across different robot platforms is emerging as a key challenge in robotics research. 

* denotes equal contribution † denotes corresponding author 

In manipulation, for example, large-scale visuomotor models trained on cross-domain datasets have been shown to generalize to different manipulators in various tasks [1, 2], while similar results also appear in navigation [3, 4]. These successes suggest that cross-embodiment learning is feasible and promising. 

For humanoid whole-body control (WBC), however, the situation is different. Large-scale, data-hungry paradigms that work in manipulation, where human operators can teleoperate robot arms [5–7] to collect hundreds of demonstrations for training, do not easily translate to legged locomotion, since a robot without an existing controller simply cannot be controlled via teleoperation. Therefore, this imitation-learning pipeline stalls at the data-collection stage. As an alternative, reinforcement learning (RL) algorithms [8, 9] have propelled WBC to impressive heights, allowing robots to run, hop, dance, and manipulate [10–13]. Yet almost every milestone is tied to one specific embodiment. Discrepancies in hardware attributes across dynamics, kinematics, and morphology block a single policy from transferring directly; each new robot typically forces the entire training and reward-tuning pipeline to start over, slowing down deployment. Recent studies have explored bridging this gap with diffusion-based motion priors [14] or by massively randomizing URDF parameters during training [15–17]. However, these methods are 

still limited to low-dimensional velocity commands, leaving other behaviors such as torso pitching beyond reach, and importantly, they have not yet been validated on diverse real humanoid hardware. 

Naturally, a question was raised: _Can one policy control multiple humanoids while still supporting diverse whole-body commands?_ In this work, we propose **EAGLE** , an embodiment-aware generalist-specialist distillation framework for unified humanoid whole-body control. EAGLE couples an iterative generalist-specialist distillation loop with a unified, high-dimensional command interface. The loop begins with a generalist trained in a simulator that pools multiple different humanoid models (Unitree H1, Unitree G1, Booster T1, Fourier N1, and PNDbotics Adam); from this policy, we spawn embodiment-specific specialists, fine-tune them on their respective robots, and then distill their new skills back into the generalist in a DAgger-based [18] way, repeating the cycle until the generalist policy converges. Built on the HugWBC [11], our command vector encodes base linear and angular velocities, body pitch, and base height, enabling behaviors far richer than pure walking—such as leaning and squatting—without any per robot-specific reward tuning. 

In summary, our key contributions are as follows: 

- We introduce an embodiment-aware generalist-specialist distillation loop that unifies whole-body control across heterogeneous humanoids without per-robot reward tuning. 

- We deploy a unified high-dimensional command interface, which allows one policy to perform squatting, leaning, and base velocity tracking, capabilities that previous approaches cannot support. 

- We conduct extensive experiments on five humanoid robots in simulation and four in the real world, showing that EAGLE achieves higher command-tracking accuracy and superior performance compared with baseline methods. 

# II. RELATED WORKS 

**Cross-embodiment learning.** Training a model that is able to transfer across different robot platforms can be promising [19–21]. Many works have attempted to address this issue by training on diverse datasets [1, 2, 22, 23], finding a unified action representation [24], or domain randomization and adaptation [25]. Meanwhile, humanoid robots have more DoFs and distinct morphological structures, making the task of finding a general controller more challenging. Some RLbased works tried to adopt diffusion models along with a residual term [14] or by training Transformers with a large pool of URDF randomized robots [15–17]. Though substantial progress has been made, most methods still support only lowdimensional velocity commands, and other diverse behaviors remain underexplored. Moreover, these approaches remain limited to simulation studies and do not demonstrate transfer to multiple physical humanoid robots, which is the central focus of our work. 

**Learning-based humanoid control.** Recent learning-based methods combine massively parallel simulation and reinforcement learning to achieve robust locomotion, recovery, and terrain traversal [26–28]. Building on these advances, recent work on humanoids has spanned real-world whole-body control [12, 13, 29], teleoperation interfaces [5, 30], and improved robustness under disturbances [31]. Meanwhile, HugWBC [11] introduces a unified, high-dimensional command space that enables a single policy to easily switch between walking, standing, and hopping, providing a versatile backbone for whole-body control. We adopt this framework and focus on closing the cross-embodiment gap. 

**Policy distillation.** Many works study transferring knowledge from teacher to deployable student models. Classical knowledge distillation compresses a network into a smaller policy via soft targets [32–34]. For multi-task RL, Distral distills task policies into a shared policy to aid transfer [35], and Kickstarting warm-starts learners from a fixed teacher with a decaying KL [36]. DAgger aggregates on-policy states with teacher relabels to reduce covariate shift [18]. In robotics, teacher-student pipelines have proved effective for legged locomotion [26, 37]. Building on these ideas, we adopt iterative generalist-specialist distillation, producing a generalist policy that scales across heterogeneous humanoids while preserving rich whole-body commands. 

# III. PRELIMINARIES 

We consider _N_ humanoid robots with heterogeneous morphologies. For robot _i ∈{_ 1 _,..., N}_ , we model the control problem as a Markov Decision Process (MDP): _Mi_ = _⟨Si, Ai, Pi, Ri, H⟩_ , where _xt_<sup>_i∈Si,a_</sup> _t_<sup>_i∈Ai_istherobotstate</sup> and action at time step _t_ , _Pi_ is the state-action transition dynamics, _Ri_ is the reward function, and _H_ is the episode horizon. Formally, our goal is to get a generalist policy _πg_ such that, given command vector _ct_ , it can generate _at ∼ πg_ ( _ot_ ) to maximize the objective function: 


where _γ ∈_ (0 _,_ 1) is the reward discount factor, _ot_ is the ( _st , ct_ ) pair, and _τi_ = _{_ ( _s_<sup>_i_</sup> _, s_<sup>_i′_</sup> _, a_<sup>_i_</sup> _, r_<sup>_i_</sup> )0: _H }_ denotes a rollout on embodiment _i_ . 

# IV. METHODOLOGY 

In this section, we introduce EAGLE, our crossembodiment training framework. Sec. IV-A describes how we build a unified, high-dimensional command and observation space for humanoid control for diverse robot behaviors. Because the robots differ in their DoF counts and kinematic layouts, Sec. IV-B explains how we align heterogeneous observation-action vectors , enabling the neural network to exploit morphological information while handling all embodiments. Sec. IV-C then outlines the reward-function design used for RL training. Finally, Sec. IV-D details the iterative generalist–specialist distillation loop that transfers embodiment-specific skills back into a shared policy. 


Fig. 2: **Method Overview. (a)** Unified command interface. The command vector **c** _t_ comprises _task_ commands **v** _t_ (linear velocities _vx, vy_ , angular velocity _ω_ ) and _behavior_ commands **b** _t_ (base height _h_ , body pitch _p_ ); together with a window of robot proprioception _st_ , they form the observation _ot_ . **(b)** Generalist-specialist distillation framework. Each round _copies πg_ to _N_ specialists _{πsi}_ for per-robot fine-tuning, then _distills_ back by running _πg_ , relabeling actions with the corresponding specialist, and updating with the loss in Eq. 9. Repeating this loop yields a single controller that scales across embodiments while retaining rich whole-body commands. 

# _A. Unified Command and Observation Space._ 

# _1) Command Design_ 

To make the robot support richer behaviors, not limited to walking, we should design a unified high-dimensional command space. Inspired by the generalized command interface of HugWBC [11], we design the command vector (shown in Fig. 2(a)) 


where _vx_ and _vy_ are desired base-frame linear velocities (m _/_ s), _ω_ is the angular velocity (rad _/_ s), _h_ is the base height offset (m), and _p_ is the body-pitch angle (rad). 

The first three components **v** _t_ = [ _vx, vy, ω_ ]<sup>_⊤_</sup> , specify _task command_ : they define where the robot should go. The last two **b** _t_ = [ _h, p_ ]<sup>_⊤_</sup> , modulate _behavior command_ , let the robot do behaviors like squatting, leaning, or standing. Separating **v** _t_ and **b** _t_ allows a single policy to realize a rich repertoire of movements beyond simply walking. 

# _2) Embodiment-aware Observation_ 

As for the policy observation, the actor receives a chunk of proprioception _o_<sup>_prio_</sup> (joint positions _q_ , joint velocities _q_ ˙, base angular velocity _ωbase_ , and projected gravity **g**<sup>proj</sup> w.r.t. the robot’s base frame) of _K_ = 5 frames: _st_ = [ _ot_<sup>_prio_</sup> _, ··· , ot_<sup>_prio_</sup> _−K_ +1<sup>].</sup> To help the robot learn foot lifting that follows a gait pattern, we add a gait clock function sin(2 _πφ_ ) in observation: 


where _f ∈_ R is the command gait frequency (Hz) and _ϕ ∈_ [0 _,_ 1) is the phase offset between the two legs. Moreover, we adopt the asymmetric actor-critic paradigm [38], where the critic 

receives additional privileged information: the base linear velocity, height error, foot clearance and contact forces, link collision state, terrain friction coefficient, and height scan samples. 

To let the network reason about the differences in robot morphology, we additionally provide _embodiment-aware observation oea ∈_ R<sup>_m×_10</sup> as privileged information for the critic and task the actor to estimate it. Here _m_ is the number of predicted rigid bodies, and in this work, we pick the torso and both feet ( _m_ = 3) to preserve locomotion-critical signals instead of upper-body links. For each rigid body, _oea_ contains information of the corresponding mass (in R), CoM position (in R<sup>3</sup> ), and inertia matrix (in R<sup>6</sup> ). Exp. V-C shows that this helps the model to distinguish across robots and their locomotion patterns. 

# _B. Embodiment Alignment._ 

As mentioned above, different humanoids expose distinct observation and action spaces, which prevents a single network from sharing weights across embodiments. We resolve this by embedding all robots into _unified_ observation-action spaces via zero padding and fixed index mappings. Specifically, we choose a unified action length _Da_ = 32, covering lower limbs (6 DoFs per leg with hip RPY, knee P, ankle RP), the waist (RPY), the head (RPY), and upper limbs (7 DoFs per arm with shoulder RPY, elbow P, wrist RPY), where RPY denotes roll/pitch/yaw. For robot _i_ , its native action _at_<sup>_i∈_R</sup><sup>_ni_is</sup> embedded as 


**Algorithm 1** Overall Process 

**Require:** Number of different robots: _N_ , Rollout buffer: _D_ ; 

- 1: Train generalist policy _πg_ on _N_ robots; _▷_ see Sec. IV-B for details 

- 2: **while** _πg_ doesn’t converge **do** 3: For _i ∈{_ 1 _,..., N}_ , _πsi ← πg_ ; _▷_ initialize model by copying weight 

- 4: Fine-tune each _πsi_ on _i_ -th robot; 5: **for** _k_ = 1 **to** _T_ epochs **do** 6: _Dπg ←{_ ( _s, s_<sup>_′_</sup> _, ag, r_ ) _}_ ; _▷_ collect parallel env trajectories 

- 7: Relabel _Dπg_ with specialist action _as_ from _πs_ 1: _N_ ; 8: Update _πg_ by Eq. 9; 9: **end for** 

10: **end while** 

11: **return** _πg_ ; 

where **0** _∈_ R<sup>_Da−ni_</sup> is a zero vector and _Pm ∈{_ 0 _,_ 1 _}_<sup>_Da×Da_</sup> is a robot-specific permutation matrix that maps each joint to a fixed global index (e.g., Right-Hip-Pitch joint _→_ 0, Left-Hip-Pitch joint _→_ 1, ...). At execution time, the environment wrapper applies the inverse mapping to recover native actions: 


We preserve robot-specific parameters, such as the swing height of both feet _ℓ_ target _, j_ ( _j ∈{_ 0 _,_ 1 _}_ ), as well as joint stiffness and damping parameters, as these will significantly impact the training phase. 

Moreover, to train the generalist policy _πg_ , we will also spawn different humanoids together in parallel within the same training environment with equal probability. As for how to _·_ align them into the reward function _Ri_ � �, please see Sec. IV-C for details. 

# _C. Reward Function Design._ 

We adopt PPO [8] algorithm with asymmetric actor-critic paradigm (see Sec. IV-A) as our Reinforcement Learning algorithm. The per-step reward is decomposed into a task term _rt_<sup>task</sup> , a behavior term _rt_<sup>beh</sup> , and a regularization term _rt_<sup>reg</sup> : 


Here, _rt_<sup>task</sup> encourages tracking of the task command **v** _t_ , _rt_<sup>beh</sup> encourages tracking of the behavior command **b** _t_ , and _rt_<sup>reg</sup> penalizes failures and undesirable actions (e.g., falls, excessive torques, abrupt changes). For most of the reward, we inherit them from HugWBC [11]. See Tab. I for details. 

Since we train multiple robots jointly, reward terms must be aligned across embodiments. In practice, we keep the weights shared across robots and adjust only term-specific targets or scales to account for morphology. For example, in the baseheight tracking term _∥h_<sup>target</sup> _− h∥_<sup>2</sup> , the target _h_<sup>target</sup> is set per robot (e.g., its nominal base height). 

TABLE I: **Training reward terms** (for simplicity, note that _ρκ_ ( _x_ ) = exp( _−x/κ_ )). For the definition of _C_ ( _φ_ ) function, please refer to HugWBC [11]. 

|**Term**|**Definition**|**Coefficient**|
|---|---|---|
||_Task Reward_: _r_<sup>task</sup><br>_t_||
|Lin. vel. tracking<br>Ang. vel. tracking|_ρ_0_._25<br>�<br>_∥_**v**<sup>target</sup><br>_xy_<br>_−_**v**_xy∥_<sup>2�</sup><br>_ρ_0_._25<br>�<br>_∥ω_<sup>target</sup><br>_z_<br>_−ωz∥_<sup>2�</sup>|2<br>2_._5|
||_Behavior Reward_: _r_<sup>beh</sup><br>_t_||
|Base height<br>Body pitch|_∥h_<sup>target</sup> _−h∥_<sup>2</sup><br>_∥p_<sup>target</sup> _−p∥_<sup>2</sup>|_−_60<br>_−_1|
|Foot-swing position|∑<br>_j_<br>�<br>1_−C_(_φj_)<br>���_ℓ_target_,j −ℓ_foot_,j_<br>��2|_−_30|
|Contact vel.|∑<br><br>_C_(_φj_)<br>�<br>1_−ρ_5(_∥_**v**<sup>foot</sup><br>_xy,j_<sup>_∥_2)</sup><br>�|_−_1|
|Contact force|_j_<br>∑<br>_j_<br>�<br>1_−C_(_φj_)<br>�<sup>�</sup><br>1_−ρ_50(_∥_**f**<sup>foot</sup><br>_xy,j_<sup>_∥_2)</sup><br>�|_−_1|
|_Re_|_gularization Reward_: _r_<sup>reg</sup><br>_t_||
|Roll-pitch Ang. vel.|_∥ωxy∥_<sup>2</sup>|_−_0_._1|
|Vertical speed|_∥vz∥_<sup>2</sup><br>|_−_2|
|Foot slip|1_−_∑_j ρ_1(_∥_**v**<sup>foot</sup><sup>_,j_</sup><br>_xy_<br>_∥_<sup>2</sup>)|_−_0_._1|
|Action rate|_∥at −at−_1_∥_<sup>2</sup>|_−_2_×_10<sup>_−_3</sup>|
|Action smoothness<br>Joint torque|_∥at−_2_−_2_at−_1+_at∥_<sup>2</sup><br>_∥τ∥_<sup>2</sup>|_−_2_×_10<sup>_−_3</sup><br>_−_1_×_10<sup>_−_5</sup>|
|Joint acceleration|_∥_¨**q**_∥_<sup>2</sup>|_−_5_×_10<sup>_−_8</sup>|
|Upper-joint deviation|_∥_**q**<sup>default</sup><br>upper <sup>_−_</sup><sup>**q**upper</sup><sup>_∥_2</sup>|_−_5|
|Hip-joint deviation|_∥_**q**<sup>default</sup><br>hip<br>_−_**q**hip_∥_<sup>2</sup><br>|_−_0_._4|
|Base Orientation|_∥_**g**<sup>proj</sup><br>_xy _<sup>_∥_2</sup>|_−_5|


# _D. Distillation Loop Overview._ 

So far, the alignment scheme in Sec. IV-B enables a PPO policy _πg_ to control different robots, but its performance soon saturates at a mediocre level. To further improve it, we introduce an iterative _generalist-specialist distillation loop_ (shown in Fig. 2(b)), that alternates between _specialize_ phase and _generalize_ phase: 

- 1) **specialize.** Copy the current generalist to _N_ robotspecific specialists _{πsi}_ and fine-tune each on its own robot only. 

- 2) **generalize.** Collect trajectories of different robots by running the _πg_ . Then relabel actions proposed by the corresponding specialists, and distill _πg_ with it. 

As for the distillation mentioned above, prior approaches such as standard DAgger only align the output action distributions: 


However, since the generalist and specialist share the same model architectures, our framework introduces an additional representation-level alignment loss: 


where _e_ ( _·_ ) denotes the _hidden feature_ of the actor network by taking proprioception buffer _st_ , so _Le_ aligns the two 

policies in representation space rather than actions alone. We show in Sec. V-C that this loss term improves crossembodiment training. Moreover, we want to maintain the critic updated while also preserving the generalist model’s exploration ability, instead of simply mimicking specialists’ behavior. Therefore, we keep the PPO loss for RL exploration, and the total distillation loss becomes: 


where _α_ = 0 _._ 02 and _β_ = 1 are constant coefficients. Algo. 1 summarizes the full procedure. 

This two-way exchange lets the generalist improve steadily while each specialist begins the next round from a stronger baseline, boosting overall control quality and eliminating perrobot reward tuning or network redesign. 

# V. EXPERIMENTS 

In our experiment, we evaluate our method on five different robots in simulation and four in the real world. We intend to answer the following questions: 

- **Q1** : How much does EAGLE improve commandtracking accuracy compared to other methods? 

- **Q2** : How does each component of the generalist-specialist cycle contribute to final performance? 

- **Q3** : What embodiment-aware representation does the EAGLE policy learn? 

- **Q4** : How well does the EAGLE policy transfer to real robots in a zero-shot way? 

**Experiment Setup.** In this work, we test on five humanoid models: Unitree H1, Unitree G1, Booster T1, Fourier N1, and PNDbotics Adam, whose DoFs are 19, 29, 23, 23, 25, respectively. The simulation training is done in Isaac Gym [39] with 4096 parallel environments, each robot type being sampled with equal probability. 

**Comparison Method.** For simplicity, we abbreviate the baseline methods as follows: 

- PPO: RL baseline policy trained on all robots together, _i.e._ , the _πg_ at line 1 of Algo. 1. 

- PPO _w/o_ EO: the same policy but trained without embodiment-aware observation (Sec. IV-A) and the corresponding reconstruction loss. 

- COMPASS [4]: We reimplement COMPASS, a threestage cross-embodiment method that first imitates demonstrations to learn a world-model-conditioned base policy and then trains residual RL specialists and uses KL loss to distill them into a general policy. 

- Kickstarting [36]: a distillation method in which _πg_ is updated by _L_ = _L_ PPO + _βt_ KL� _πs∥πg_ � _,_ where _πs_ is the specialist policy and the coefficient _βt_ = _αexp_ ( _−λt_ ) decays exponentially. 

- EAGLE (ours): our framework after a _single_ round of distillation, the same as Kickstarting. 

- EAGLE _w/_ ID (ours): the full iterative distillation variant until the generalist’s performance converges. 

We also use the same model architecture and reward functions for fair comparison. 

# _A. Command Tracking Accuracy Analysis._ 

To quantitatively understand how well our method compares to baseline methods, we refer to the command tracking error. **Metric definition.** For each command dimension _d ∈ {vx, vy, ω, h, p}_ we define the _episode tracking error_ : 


where _ct_<sup>_d_isthecommandedtargetdrawnfromthepredefined</sup> range (Tab. III), and _c_ ˆ _t_<sup>_d_</sup> is the value read from the robot’s proprioceptive state. We report five errors _Evx , Evy, Eω , Eh, Ep_ separately; lower values indicate more accurate command tracking. 

**Results.** Tab. II summarizes the episode-averaged single command tracking errors. We can see that compared to the PPO method, which was trained on all different robots together, both EAGLE and EAGLE _w/_ ID surpass it on most metrics. As for the ablation on distillation method (Tab. II(b)), compared with the KL-based Kickstarting baseline, our singleround EAGLE already wins on 80% robot–metric pairs and is never catastrophic, whereas Kickstarting can become unstable on certain embodiment like G1, Adam and T1 (e.g. _Evx_ =0 _._ 761 on T1 is five times higher than PPO). The result confirms that the DAgger-style loss in Eq. 9 is more robust across very different embodiments. 

We also compare with the cross-embodiment baseline **COMPASS** [4]. Although it achieves good results on some robots like Fourier N1, it fails to generalize across all embodiments. In contrast, our method maintains low _Evx_ on all robots while keeping other metrics competitive or superior, demonstrating stable, single-policy control across heterogeneous humanoids. 

# _B. Ablation of the Distillation Loop._ 

Furthermore, Tab. II contrasts EAGLE after a _single_ distillation round with its iterative variant. For most task commands, EAGLE _w/_ ID achieves lower task-command errors compared to EAGLE, which wasn’t trained after the iterative loop. Although a few behavior-command errors increase slightly, the overall gains outweigh these minor regressions. Fig. 3 plots the evolution of task-command errors across rounds and shows that, after each distillation cycle, both the specialists (highlighted in yellow) and the generalists improve in most cases. This suggests that repeating the loop until convergence is more effective than a single distillation pass. 

We additionally train _single-robot_ PPO policies that are exposed to only one robot type. As Tab. IV shows, on robots such as H1, our generalist achieves performance comparable to these specialized baselines, while the corresponding EAGLEspecialist even surpasses them. This means cross-embodiment training has the potential to match, and sometimes exceed, policies tailored to a single embodiment. 

# _C. Analysis of Learned Representations._ 

As we can see in Tab. II(a), without the embodimentaware observation, PPO _w/o_ EO’s overall performance drops, 

TABLE II: **Command-tracking errors** (lower is better). _Evx_ and _Evy_ are linear-velocity error in m _/s_ , _Eω_ is angular-velocity error in rad _/s_ , _Eh_ is base height error in m, and _Ep_ is body-pitch error in rad. Each tracking error is averaged over 2048 environments and 1000 steps. Our method maintains low errors across all robots compared to other cross-embodiment baselines. 

|**Robot Type**||**U**|**nitree H**|**1**|||**U**|**nitree G**|**1**|||**PND**|**botics A**|**dam**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Tracking Error (_↓_)|_Evx_|_Evy_|_Eω_|_Eh_|_Ep_|_Evx_|_Evy_|_Eω_|_Eh_|_Ep_|_Evx_|_Evy_|_Eω_|_Eh_|_Ep_|
|(a) Ablation: embodime|nt-awar|e obser|vation|||||||||||||
|PPO|0.108|0.129|0.114|**0.075**|0.182|0.092|0.127|0.121|0.051|**0.164**|0.328|0.107|0.235|0.051|0.204|
|PPO _w/o_ EO|0.290|0.161|0.152|0.078|0.189|0.104|0.113|0.095|0.052|0.165|0.375|0.158|0.310|0.063|0.218|
|(b) Ablation: baseline|& distill|ation m|ethod|||||||||||||
|COMPASS [4]|0.725|0.390|0.476|0.085|0.273|0.171|0.119|0.124|**0.035**|0.169|0.763|0.371|0.339|0.045|0.233|
|Kickstarting [36]|0.323|0.141|0.122|**0.075**|0.182|0.117|0.118|0.075|0.050|0.167|0.399|0.086|0.141|**0.041**|**0.192**|
|EAGLE (ours)|0.061|0.117|**0.054**|0.076|**0.169**|**0.066**|0.105|0.077|0.049|**0.164**|0.182|**0.084**|**0.115**|0.050|0.196|
|EAGLE _w/_ ID (ours)|**0.051**|**0.110**|**0.054**|0.082|0.186|0.067|**0.095**|**0.071**|0.047|0.176|**0.156**|0.101|0.117|0.056|0.197|


|**Robot Type**||**Fo**|**urier N**|**1**|||**Bo**|**oster **|**T1**||
|---|---|---|---|---|---|---|---|---|---|---|
|Tracking Error (_↓_)|_Evx_|_Evy_|_Eω_|_Eh_|_Ep_|_Evx_|_Evy_|_Eω_|_Eh_|_Ep_|
|(a) Ablation: embodim|ent-awa|re obse|rvation||||||||
|PPO|0.124|0.141|0.107|0.073|0.165|0.147|0.203|0.105|0.047|0.156|
|PPO _w/o_ EO|0.126|0.144|0.076|0.079|0.162|0.140|0.194|0.104|0.046|0.151|
|(b) Ablation: baseline|& distil|lation|method||||||||
|COMPASS [4]|0.060|**0.117**|0.137|**0.056**|0.160|0.831|0.307|0.179|**0.044**|0.151|
|Kickstarting [36]|0.147|0.142|0.130|0.077|0.168|0.761|0.190|0.100|0.047|**0.149**|
|EAGLE (ours)|0.068|0.126|0.058|0.074|**0.157**|0.109|**0.187**|0.045|0.045|0.152|
|EAGLE _w/_ ID (ours)|**0.056**|0.135|**0.056**|0.074|0.168|**0.090 **|**0.187 **|**0.041 **|**0.044**|0.159|


Fig. 3: **Tracking-error curves for** _Evx_ **,** _Evy_ **, and** _Eω_ (left to right). The <mark>△</mark> , ▲ represents the specialist and generalist policy respectively (as described at lines 2-9 of Algo. 1). We can see the trend that, after each distillation cycle, both symbols move downward, showing that iterative distillation steadily improves tracking accuracy for specialists and generalists. 

TABLE III: **Command ranges.** “Initial” and “Finishing” denote the RL curriculum learning stage (all in SI units). 

|E III: **Co**<br>e the RL c<br>|**mmand **<br>urriculum<br><br>|**ranges.** “Init<br> learning stag<br><br>|ial” and “Finishing”<br>e (all in SI units).<br>|TABLE IV: **Unitree H1 com**<br>better). After cross-embodim<br>matches, and its robot-specii|**mand-tracking errors** (lower is<br>ent training, EAGLE-generalist<br>fic policy EAGLE-specialist sur-|
|---|---|---|---|---|---|
|**Group**|**Term**<br>|**Initial Range**<br>|**Finishing Range**|passes a policy trained exclu|sively on H1.|
|Task<br>Commands|_vx_<br>_vy_|[_−_0_._3_,_0_._6]<br>[_−_0_._5_,_0_._5]<br>|[_−_0_._6_,_1_._2]<br>[_−_0_._4_,_0_._4]<br>|**Tracking Error (**_↓_**)**<br>_Evx_|_Evy_<br>_Eω_<br>_Eh_<br>_Ep_|
||_ω_|[_−_0_._5_,_0_._5]|[_−_1_._0_,_1_._0]|single-robot PPO<br>0.067|**0.101**<br>0.052<br>**0.072**<br>0.181|
|Behavior|_h_|[_−_0_._3_,_0]|[_−_0_._3_,_0]|EAGLE-generalist<br>0.061|0.117<br>0.054<br>0.076<br>**0.169**|
|Commands|_p_|[_−_0_._3_,_0_._5]|[_−_0_._3_,_0_._5]|EAGLE-specialist<br>**0.048**|0.105<br>**0.042**<br>**0.072**<br>0.174|


and for some robots like H1, its _Evx_ tracking error increases significantly, showing that the policy fails to integrate different robot-specific knowledge together. 

In Fig. 4, we also use t-SNE to visualize the latent embedding _eπ_ ( _·_ ) (in Eq. 8) by commanding the robot to walk forward. The _left_ panel depicts the PPO trained _without_ embodiment-aware observation: several robot types collapse into an overlapping cluster (dashed ellipse), indicating that the encoder cannot distinguish their dynamics. In contrast, the 

_right_ panel shows our policy, whose latent space forms wellseparated clusters for all five embodiments, confirming that the embodiment cue helps the network learn morphology-specific representations. 

# _D. Zero-shot Sim2real Performance._ 

To demonstrate the policy’s ability to deploy on real-world hardware, we tested it on four real humanoid robots: Unitree H1, Unitree G1, Booster T1, and Fourier N1 in a zero-shot 


Fig. 4: **t-SNE visualization of policy latent-space representation.** By commanding different robots to walk forward for certain timesteps, we can see _w/o_ embodimentaware observation _(left)_ , the policy outputs latent vectors _eπ_ ( _·_ ) collapse into overlapping clusters. In contrast, our method _(right)_ is better separated, showing successful morphologyaware representation. 


Fig. 6: **Real-world experiment.** We evaluate our policy across four embodiments: (I) Unitree H1, (II) Unitree G1, (III) Fourier N1, and (IV) Booster T1. Each robot successfully executes diverse commands, including (a) walking, (b) leaning, and (c) squatting, demonstrating robust zero-shot transfer from simulation to the real world. 

# VI. DISCUSSION 

In this work, we do not exhaustively evaluate on _unseen_ humanoid embodiments at test time. A promising direction is to combine our distillation framework with explicit URDF randomization or morphology randomization during training, as explored by previous works like [15–17], so the generalist learns to cover a wider space of structures. 

Fig. 5: **Real-world synchronous movement.** We also developed a shared low-level control framework to show our policy can let different robots execute synchronous movement, from leaning (II) to squatting (III). 

manner. We use UniCon [40] as a unified control interface for operating different robot platforms. 

Another limitation is that our embodiment-aware observation is still coarse; future work could enrich it with finergrained morphology descriptors such as limb lengths, joint topology, and kinematic tree structure, which may further improve cross-embodiment generalization. 

In Fig. 6 and Fig. 5, the policy, trained purely in simulation, executes diverse behaviors including walking, leaning, and squatting. Despite variations in morphology and hardware dynamics, the controller consistently produces stable motions across embodiments. These results confirm that our distillation framework supports robust sim2real transfer and enables a single policy to generalize effectively to heterogeneous humanoid platforms. 

# VII. CONCLUSION 

In this paper, we present EAGLE, an embodiment-aware generalist-specialist distillation framework for unified humanoid whole-body control. By combining a high-dimensional 

command interface with an iterative distillation loop, EAGLE enables a single policy to control five structurally diverse humanoids without per-robot reward tuning. Through extensive simulation and real-world experiments, we show that our approach not only achieves superior command-tracking accuracy but also supports rich behaviors like squatting and leaning. These results highlight the potential of embodimentaware distillation as a scalable solution for cross-embodiment learning in complex locomotion tasks. 

# VIII. ACKNOWLEDGMENT 

The SJTU team is supported by National Natural Science Foundation of China (62322603), Shanghai Municipal Science and Technology Major Project (2025SHZDZX025D08) and Shanghai Artificial Intelligence Laboratory. 

# REFERENCES 

- [1] A. O’Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain _et al._ , “Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 6892–6903. 

- [2] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [3] K.-H. Zeng, Z. Zhang, K. Ehsani, R. Hendrix, J. Salvador, A. Herrasti, R. Girshick, A. Kembhavi, and L. Weihs, “Poliformer: Scaling on-policy rl with transformers results in masterful navigators,” _arXiv preprint arXiv:2406.20083_ , 2024. 

- [4] W. Liu, H. Zhao, C. Li, J. Biswas, S. Pouya, and Y. Chang, “Compass: Cross-embodiment mobility policy via residual rl and skill synthesis,” _arXiv preprint arXiv:2502.16372_ , 2025. 

- [5] X. Cheng, J. Li, S. Yang, G. Yang, and X. Wang, “Open-television: Teleoperation with immersive active visual feedback,” _arXiv preprint arXiv:2407.01512_ , 2024. 

- [6] S. Luo, Q. Peng, J. Lv, K. Hong, K. R. Driggs-Campbell, C. Lu, and Y.-L. Li, “Human-agent joint learning for efficient robot manipulation skill acquisition,” _arXiv preprint arXiv:2407.00299_ , 2024. 

- [7] H. Fang, H.-S. Fang, Y. Wang, J. Ren, J. Chen, R. Zhang, W. Wang, and C. Lu, “Airexo: Low-cost exoskeletons for learning whole-arm manipulation in the wild,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 15 031–15 038. 

- [8] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [9] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, “Soft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor,” in _International conference on machine learning_ . Pmlr, 2018, pp. 1861–1870. 

- [10] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang, “Exbody2: Advanced expressive humanoid whole-body control,” _arXiv preprint arXiv:2412.13196_ , 2024. 

- [11] Y. Xue, W. Dong, M. Liu, W. Zhang, and J. Pang, “A unified and general humanoid whole-body controller for fine-grained locomotion,” _arXiv preprint arXiv:2502.03206_ , 2025. 

- [12] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi, “Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning,” _arXiv preprint arXiv:2406.08858_ , 2024. 

- [13] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, J. Kautz, C. Liu, G. Shi, X. Wang _et al._ , “Hover: Versatile neural whole-body controller for humanoid robots,” _arXiv preprint arXiv:2410.21229_ , 2024. 

- [14] S. Yang, Z. Fu, Z. Cao, G. Junde, P. Wensing, W. Zhang, and H. Chen, “Multi-loco: Unifying multi-embodiment legged locomotion via reinforcement learning augmented diffusion,” _arXiv preprint arXiv:2506.11470_ , 2025. 

- [15] N. Bohlinger, G. Czechmanowski, M. Krupka, P. Kicki, K. Walas, J. Peters, and D. Tateo, “One policy to run them all: an end-to-end 

   - learning approach to multi-embodiment locomotion,” _arXiv preprint arXiv:2409.06366_ , 2024. 

- [16] B. Ai, L. Dai, N. Bohlinger, D. Li, T. Mu, Z. Wu, K. Fay, H. I. Christensen, J. Peters, and H. Su, “Towards embodiment scaling laws in robot locomotion,” _arXiv preprint arXiv:2505.05753_ , 2025. 

- [17] M. Liu, D. Pathak, and A. Agarwal, “Locoformer: Generalist locomotion via long-context adaptation,” _arXiv preprint arXiv:2509.23745_ , 2025. 

- [18] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” in _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ . JMLR Workshop and Conference Proceedings, 2011, pp. 627–635. 

- [19] W. Yu, J. Tan, C. K. Liu, and G. Turk, “Preparing for the unknown: Learning a universal policy with online system identification,” _arXiv preprint arXiv:1702.02453_ , 2017. 

- [20] C. Ying, H. Zhongkai, X. Zhou, X. Xu, H. Su, X. Zhang, and J. Zhu, “Peac: Unsupervised pre-training for cross-embodiment reinforcement learning,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 54 632–54 669, 2024. 

- [21] J. Yang, C. Glossop, A. Bhorkar, D. Shah, Q. Vuong, C. Finn, D. Sadigh, and S. Levine, “Pushing the limits of cross-embodiment learning for manipulation and navigation,” _arXiv preprint arXiv:2402.19432_ , 2024. 

- [22] M. Xu, Z. Xu, C. Chi, M. Veloso, and S. Song, “Xskill: Cross embodiment skill discovery,” 2023. 

- [23] R. Doshi, H. Walke, O. Mees, S. Dasari, and S. Levine, “Scaling crossembodied learning: One policy for manipulation, navigation, locomotion and aviation,” _arXiv preprint arXiv:2408.11812_ , 2024. 

- [24] L. Shao, F. Ferreira, M. Jorda, V. Nambiar, J. Luo, E. Solowjow, J. Ojea, O. Khatib, and J. Bohg, “Unigrasp: Learning a unified model to grasp with multifingered robotic hands,” _IEEE Robotics and Automation Letters_ , vol. PP, pp. 1–1, 01 2020. 

- [25] J. Tobin, R. Fong, A. Ray, J. Schneider, W. Zaremba, and P. Abbeel, “Domain randomization for transferring deep neural networks from simulation to the real world,” in _2017 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ . IEEE, 2017, pp. 23–30. 

- [26] A. Kumar, Z. Fu, D. Pathak, and J. Malik, “Rma: Rapid motor adaptation for legged robots,” _arXiv preprint arXiv:2107.04034_ , 2021. 

- [27] X. Cheng, K. Shi, A. Agarwal, and D. Pathak, “Extreme parkour with legged robots,” _arXiv preprint arXiv:2309.14341_ , 2023. 

- [28] J. Hwangbo, J. Lee, A. Dosovitskiy, D. Bellicoso, V. Tsounis, V. Koltun, and M. Hutter, “Learning agile and dynamic motor skills for legged robots,” _Science Robotics_ , vol. 4, no. 26, p. eaau5872, 2019. 

- [29] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” _arXiv preprint arXiv:2406.10454_ , 2024. 

- [30] Y. Ze, Z. Chen, J. P. Ara´ujo, Z.-a. Cao, X. B. Peng, J. Wu, and C. K. Liu, “Twist: Teleoperated whole-body imitation system,” _arXiv preprint arXiv:2505.02833_ , 2025. 

- [31] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang, “Learning humanoid standing-up control across diverse postures,” _arXiv preprint arXiv:2502.08378_ , 2025. 

- [32] G. Hinton, O. Vinyals, and J. Dean, “Distilling the knowledge in a neural network,” _arXiv preprint arXiv:1503.02531_ , 2015. 

- [33] J. Gou, B. Yu, S. J. Maybank, and D. Tao, “Knowledge distillation: A survey,” _International journal of computer vision_ , vol. 129, no. 6, pp. 1789–1819, 2021. 

- [34] W. Park, D. Kim, Y. Lu, and M. Cho, “Relational knowledge distillation,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2019, pp. 3967–3976. 

- [35] Y. Teh, V. Bapst, W. M. Czarnecki, J. Quan, J. Kirkpatrick, R. Hadsell, N. Heess, and R. Pascanu, “Distral: Robust multitask reinforcement learning,” _Advances in neural information processing systems_ , vol. 30, 2017. 

- [36] S. Schmitt, J. J. Hudson, A. Zidek, S. Osindero, C. Doersch, W. M. Czarnecki, J. Z. Leibo, H. Kuttler, A. Zisserman, K. Simonyan _et al._ , “Kickstarting deep reinforcement learning,” _arXiv preprint arXiv:1803.03835_ , 2018. 

- [37] T. Miki, J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning robust perceptive locomotion for quadrupedal robots in the wild,” _Science robotics_ , vol. 7, no. 62, p. eabk2822, 2022. 

- [38] S. Choi, G. Ji, J. Park, H. Kim, J. Mun, J. H. Lee, and J. Hwangbo, “Learning quadrupedal locomotion on deformable terrain,” _Science Robotics_ , vol. 8, no. 74, p. eade2256, 2023. 

- [39] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, 

D. Hoeller, N. Rudin, A. Allshire, A. Handa _et al._ , “Isaac gym: High performance gpu-based physics simulation for robot learning,” _arXiv preprint arXiv:2108.10470_ , 2021. 

- [40] Y. Lin, L. Xu, Y. Yu, J. Pang, and W. Zhang, “Unicon: A unified system for efficient robot learning transfers,” _arXiv preprint arXiv:2601.14617_ , 2026. 

