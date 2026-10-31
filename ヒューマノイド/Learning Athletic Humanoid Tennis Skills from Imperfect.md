---
title: "Learning Athletic Humanoid Tennis Skills from Imperfect Human Motion Data"
date: "2026-03-13"
authors: "Zhikai Zhang; Haofei Lu; Yunrui Lian; Ziqing Chen; Yun Liu; Chenghuai Lin"
url: https://arxiv.org/abs/2603.12686
pdf: https://arxiv.org/pdf/2603.12686
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.12686)** / [論文ページ](https://arxiv.org/abs/2603.12686)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Learning Athletic Humanoid Tennis Skills from Imperfect Human Motion Data** 

**Zhikai Zhang**<sup>1</sup><sup>_,_3</sup><sup>_,∗_</sup> , **Haofei Lu**<sup>1</sup><sup>_,_3</sup><sup>_,∗_</sup> , **Yunrui Lian**<sup>1</sup><sup>_,_3</sup><sup>_,∗_</sup> , **Ziqing Chen**<sup>1</sup><sup>_,_3</sup> , **Yun Liu**<sup>1</sup><sup>_,_3</sup> , **Chenghuai Lin**<sup>3</sup> , **Han Xue**<sup>1</sup><sup>_,_3</sup> , **Zicheng Zeng**<sup>3</sup> , **Zekun Qi**<sup>1</sup><sup>_,_3</sup> , **Shaolin Zheng**<sup>3</sup> , **Qing Luan**<sup>3</sup> , **Jingbo Wang**<sup>5</sup> , **Junliang Xing**<sup>1</sup> , **He Wang**<sup>2</sup><sup>_,_3</sup> , **Li Yi**<sup>1</sup><sup>_,_4</sup><sup>_,†_</sup> 

> 1Tsinghua University 2Peking University 3Galbot Inc. 4Shanghai Qi Zhi Institute 5Shanghai AI Laboratory 

> _∗_ Equal Contribution, _†_ Corresponding author 

Human athletes demonstrate versatile and highly-dynamic tennis skills to successfully conduct competitive rallies with a high-speed tennis ball. However, reproducing such behaviors on humanoid robots is difficult, partially due to the lack of perfect humanoid action data or human kinematic motion data in tennis scenarios as reference. In this work, we propose **LATENT** , a system that **L** earns **A** thletic humanoid **TE** nnis skills from imperfect human motio **N** da **T** a. The imperfect human motion data consist only of motion fragments that capture the primitive skills used when playing tennis rather than precise and complete human-tennis motion sequences from real-world tennis matches, thereby significantly reducing the difficulty of data collection. Our key insight is that, despite being imperfect, such quasi-realistic data still provide priors about human primitive skills in tennis scenarios. With further correction and composition, we learn a humanoid policy that can consistently strike incoming balls under a wide range of conditions and return them to target locations, while preserving natural motion styles. We also propose a series of designs for robust sim-to-real transfer and deploy our policy on the Unitree G1 humanoid robot. Our method achieves surprising results in the real world and can stably sustain multi-shot rallies with human players as shown in Figure 1. 

**Code:** `https://github.com/GalaxyGeneralRobotics/LATENT` 

**Project Page:** `https://zzk273.github.io/LATENT/` 


**Figure 1 (a)** The humanoid performs multi-shot rallies with a human player using different stroke types across various court regions. **(b)** The humanoid performs athletic tennis skills to strike an incoming ball traveling at high speed (peak velocities > _15_ m/s). 

## **1 Introduction** 

Learning athletic sports skills remains one of the core challenges for humanoid robots. Such sports typically require highly dynamic motions, rapid reactions, and high precision. Taking tennis as an example, players are often required to sprint across the court at speeds exceeding _6 m/s_ , react to incoming balls traveling at _15–30 m/s_ , and strike the ball within an extremely short ball–racket contact duration of only _a few milliseconds_ . These characteristics make it infeasible to collect humanoid action data via human-humanoid tele-operation for direct imitation learning, posing a significant challenge to reproducing athletic tennis skills on humanoids. 

An alternative approach is to use kinematic human motion data as reference. However, tennis typically involves: **(i)** large-scale human movements that span the half court, **(ii)** sustained multi-rally interactions, and **(iii)** subtle and highly precise wrist motions during ball striking. Such characteristics make it extremely difficult for motion capture systems to collect precise and complete human-tennis motion data from real-world matches. Vid2Player3D [44] alleviates this problem by leveraging broadcast videos. However, it needs a complex pipeline to extract human motion data from monocular videos, including player detection, camera estimation, 2D and 3D human pose estimation, followed by imitation policy with external residual forces to correct motion artifacts. Assembling these modules may require substantial expertise and engineering efforts. 

In this work, we propose **LATENT** , a novel system to **L** earn **A** thletic humanoid **TE** nnis skills from imperfect human motio **N** da **T** a. The _imperfect_ human motion data consist only of motion fragments that capture the primitive skills (e.g., forehand stroke, backhand stroke, lateral shuffle, crossover step) used when playing tennis rather than realistic and complete human-tennis motion sequences from real-world tennis matches, thereby significantly reducing the difficulty of data collection. Here, _imperfect_ manifests in two aspects: ❶ **Imprecise** . Due to the motion capture difficulty and cross-embodiment gap, the wrist motions during racket swinging are often imprecise. ❷ **Incomplete** . The motion data only provide priors about natural motor skills and do not contain any knowledge about how to utilize them for the tennis task. Our key insight is that, despite being imperfect, such quasi-realistic data adequately provide priors about human primitive skills in tennis scenarios. These knowledge, with further correction and composition, can be leveraged to learn tennis skills while maintaining natural human behavior. 

Our method builds upon recent ideas in hierarchical humanoid control with latent action spaces: constructing a latent space to represent nature humanoid actions and then training a high-level policy to sample from it to accomplish the tennis return task. We propose two novel designs to mitigate the imperfections of the data. First, to _bridge the gap between the high-precision nature of human-tennis_ 

_interaction and the imprecise quasi-realistic human motion data_ , we design the latent space to be compatible with potential action corrections predicted by the high-level policy. Second, since the motion data do not contain any knowledge about how these primitive skills should be utilized to return tennis, the high-level policy can easily exploit the latent space while learning to accomplish the task. To _balance the task performance and adherence to the primitive skill priors_ , we design a latent action barrier to constrain the RL exploration of the high-level policy according to the state-based action distribution prior. 

To enable robust sim-to-real transfer, we also propose a series of careful designs for robust sim-to-real transfer, including dynamics randomization and observation noise applied to both the robot and the tennis ball. We deploy our method on Unitree G1 hardware and can stably sustain multi-shot rallies with human players. 

Our contributions are fourfold: 

- We propose **LATENT** , a novel system to learn athletic humanoid tennis skills from imperfect human motion data, paving the way for future research. 

- We propose two novel designs to better construct and utilize a latent action space from imperfect human motion data. 

- We successfully deploy our method on a real-world humanoid robot and can stably sustain multi-shot rallies with human players. 

- Extensive experiments are conducted in both simulation and the real world to validate the effectiveness of our major designs. 

## **2 Related Work** 

### **2.1 Latent Action Space for Humanoid Control** 

Due to the high degrees of freedom (DoFs) of humanoid robots, learning skills from scratch often leads to low RL sampling efficiency and unnatural motions. To address this problem, learning a latent action space that encodes reusable primitive skills from pre-recorded human motion data, and subsequently training a high-level policy to sample within this latent space, has been widely studied [44, 46, 38, 39, 18, 19, 22, 28, 4, 23, 35, 13]. Some prior works [44, 23] learn a kinematic motion latent space, followed by a pretrained motion tracker to accomplish downstream tasks. However, the generated kinematic motions often exhibit physical infeasibility, posing significant challenges for the tracker. In contrast, some works [46, 38, 39, 18, 22, 28, 13] directly learn a latent space of joint actions. PULSE [18] distills a VAE-style latent action space from a universal motion tracker. R<sup>2</sup> S<sup>2</sup> [46] adopts this idea on real humanoid robots and learns a latent space from a set of pre-trained primitive skills to solve loco-manipulation tasks. 

Compared with existing works, we focus on learning athletic 

humanoid tennis skills from imperfect human motion data that contains only imprecise and incomplete primitive skills. We propose two key novel designs to correct and compose these imperfect human motion priors so that the high-level policy can learn to accomplish the task while preserving natural motion styles. 

and high precision requirements, acquiring the primitive action skills involved is considerably more feasible. 

We invited five amateur tennis players to collect primitive skills commonly used in tennis, including forehand stroke, backhand stroke, lateral shuffle, crossover step and so on, within an optical motion capture system. Since we collect only primitive skill demonstrations rather than complete motion sequences from tennis matches, the requirements on the motion capture system are significantly reduced. In our setting, the system covers an effective area of only 3 _m ×_ 5 _m_ , which is more than 17 _×_ smaller than a full-size tennis court, resulting in substantial savings in both capture area and the number of cameras compared to collecting complete human motion data in tennis. 

### **2.2 Humanoid for Sports** 

Humanoid for sports have long been a central topic in character animation. A significant amount of works [44, 20, 32, 41, 37, 11, 45, 30, 36, 15] have been proposed to enable humanoids to play various sports, including tennis [44], basketball [32, 41, 37], and football [11]. Among these, the work most closely related to ours is Vid2Player3D [44], which builds a simulated character that can hit the incoming ball to target positions using a diverse array of strokes. However, this work relies on several physically infeasible assumptions, such as unlimited joint torques and residual force on the root [42], and does not consider the sim-to-real gap of the overall system. In addition, our work focuses on how to leverage easily collected yet imperfect human motion data to learn tennis skills. 

In total, we collect five hours of motion data, without performing any editing or annotation. After collection, we retarget the human motion to humanoid motion with LocoMuJoCo [1]. 

### **3.2 Correctable Latent Action Space Construction** 

To learn a latent space of the primitive skills, we first train a motion tracker to imitate the collected motion data and then distill it to a latent model with a variational information bottleneck. 

With recent advances in humanoid hardware, several works [6, 27, 14, 10, 31, 34, 40, 33, 3, 12, 24] successfully learn sports skills on a real-world humanoid robot, including table tennis [27, 10], badminton [14, 3], football [31, 34, 12], and boxing [40]. However, these works often lack highly dynamic motions, agile body coordination, or rapid reaction. Our work takes a significant step toward achieving athletic humanoid sports skills. 

#### **3.2.1 Motion tracker Pre-training** 

To transform noisy humanoid motion data to executable humanoid primitive skills, we train a motion tracker to imitate the collected motion data. We use the motion tracking framework of Any2Track [47]. Our tracker can be seen as an RL policy _π_ tracker( _a_ ˆ<sup>body</sup> _t |st,_ ˜ _st_ +1), which maps humanoid proprioception state and motion target to lowlevel robot actions. At each timestep _t_ , the inputs of policy _π_ tracker consist of current state _st_ and current motion target _s_ ˜ _t_ +1 from the collected motion data. The current state _st_ includes angular velocity, projected gravity, per-joint position, per-joint velocity, and last-frame action. The policy _π_ tracker needs to output joint actions _a_ ˆ<sup>body</sup> _t_ , which is further fed into a PD controller to compute actuator torques. The task goal of motion tracking is that at timestep _t_ + 1, the robot’s state _st_ +1 should be as close as possible to the target motion depicted by _s_ ˜ _t_ +1 while maintaining balance and safety. 

## **3 Learning Tennis Skills with LATENT** 

The overview of LATENT is shown in Figure 2. Our method consists of three stages. First, we collect imperfect human motion data (i.e., motion fragments of primitive skills such as forehand stroke, backhand stroke, lateral shuffle, crossover step and so on) with a compact motion capture system in Section 3.1. Then we construct a latent action space that is compatible to potential action corrections with the collected imperfect data in Section 3.2. Finally, we train a high-level policy to correct and compose the primitive skills stored in the latent space to perform tennis skills in Section 3.3. 

We use PPO [26]26]] as our reinforcement learning framework and MuJoCo JAX [29,29,, 43]] for simulation in training. We train our policy in parallel on 8 GPUs. Our high-level planner and low-level controller run at 50 Hz, and the simulation frequency is set to 2000 Hz to accurately model ball-racket and ball-ground contact. 

We use PPO [26]26]] as our reinforcement learning framework As mentioned before, our collected motion data do not conand MuJoCo JAX [29,29,, 43]] for simulation in training. We tain precise wrist motions during striking a tennis ball, and train our policy in parallel on 8 GPUs. Our high-level errors are further amplified during human-to-humanoid replanner and low-level controller run at 50 Hz, and the targeting. Therefore, in the subsequent steps, the high-level simulation frequency is set to 2000 Hz to accurately model policy needs to provide corrective adjustments to the wrist ball-racket and ball-ground contact. joints. To enable the controller to robustly handle these potential corrections while preserving stability, we remove the **3.1 Collection of Imperfect Human Motion Data** control signals about right wrists (racket-holding) in _a_ ˆ<sup>body</sup> _t_ during training and apply additional random perturbations Although collecting comprehensive human-tennis motion on the right wrist joints. The tracker needs to imitate the data from real-world tennis matches is difficult and costly motions of the remaining joints against the unknown wrist due to the sport’s large movement range, multi-rally nature disturbances. 

Although collecting comprehensive human-tennis motion data from real-world tennis matches is difficult and costly due to the sport’s large movement range, multi-rally nature 


**Figure 2 Overview of LATENT** . **(a)** We pre-train a motion tracker on collected imperfect human motion data. **(b)** We construct a correctable latent action space via online distillation. **(c)** We train a high-level policy to correct and compose latent actions for tennis task. **(d)** We transfer the policy to the real world via dynamics randomization and observation noise. 

#### **3.2.2 Online Distillation with Variational Bottleneck** 

After learning to imitate the collected human motion fragments, the tracker now contains sufficient primitive skills to play tennis. To learn a compact and structured representation of these primitive skills, we train a student network with a latent representation via online distillation [18, 46, 17]. For the student network, we adopt an encoder-decoder framework with a conditional variational information bottleneck to encode skills in a continuous skill space, which includes a posterior variational encoder _E_ ( _zt_<sup>_q|st,_˜</sup><sup>_st_+1)=</sup><sup>_N_(</sup><sup>_z_</sup> _t_<sup>_q_;</sup><sup>_µe_(</sup><sup>_st,_˜</sup><sup>_st_+1)</sup><sup>_, σe_(</sup><sup>_st,_˜</sup><sup>_st_+1))tomodel</sup> the latent code distribution conditioned on current state and motion target, a decoder _D_ ( _a_ ˆ<sup>body</sup> _t |st, zt_<sup>_q_)mapsthesam-</sup> pled latent code to action conditioned on state. 

During training, we encode ( _st,_ ˜ _st_ +1) via _E_ and sample latent code _zt_<sup>_q∼N_(</sup><sup>_z_</sup> _t_<sup>_q_;</sup><sup>_µe, σe_).Thenweusethedecoder</sup> to decode _zt_<sup>_q_intohumanoidactions</sup><sup>_a_body</sup> _t_ . We train the networks to reconstruct the action of the teacher tracker _a_ ˆ<sup>body</sup> _t_ and keep the latent distribution to be close to the prior. The total loss can be written as: 


where 


is the supervision loss of DAgger [25], an online distillation method. _D_ agg represents the data buffer consist of student 

current state _st_ and teacher action _a_ ˆ<sup>body</sup> _t_ . Meanwhile, _a_<sup>body</sup> _t_ denotes the action from the student policy. As mentioned before, _a_ ˆ<sup>body</sup> _t_ and _a_<sup>body</sup> _t_ do not contain any control signals for the right wrist. We maintain disturbances on the right wrist joints during online distillation so that the latent space becomes robust to such perturbations. 

Rather than training the networks against a fixed unimodal Gaussian as commonly used by VAEs, we utilize a learnable conditional prior _P_ ( _zt_<sup>_p|st_)=</sup><sup>_N_(</sup><sup>_z_</sup> _t_<sup>_p_;</sup><sup>_µp_(</sup><sup>_st_)</sup><sup>_, σp_(</sup><sup>_st_))to</sup> capture state-based action distribution since the action distributions of different robot states differ significantly (e.g., lateral shuffle versus racket-swinging for ball striking). The KL-divergence loss: 


encourages the encoded posterior distribution to be close to the learnable prior. 

### **3.3 High-Level Policy Learning** 

We train a high-level policy _π_ planner to correct and compose the primitive skills stored in the pre-constructed latent action space to achieve athletic humanoid tennis behavior. At each timestep _t_ , the inputs of the high-level policy _π_ planner consist of current robot state _st_ , global information about the robot root pose _gt_ , and ball state _bt_ . 

**Table 1 Reward terms used in LATENT.** The reward terms are divided into three types: Task, Regularization, and Termination. 

|Term<br>|Weight<br>T<br>|Term<br>ask<br>|Weight<br>|
|---|---|---|---|
|Approach to ball<br>Hit success<br>|10_._0<br>200_._0<br>Regul<br>|Ball landing<br>arization<br>|30_._0<br>|
|High-level action|_−_5_·_10<sup>_−_3</sup>|Torque penalty|_−_2_·_10<sup>_−_5</sup>|
|Lower body action rate<br>Racket acceleration|_−_1_._0<br>_−_1_·_10<sup>_−_6</sup>|Whole body action rate<br>Joint smoothness|_−_0_._5<br>_−_2_·_10<sup>_−_6</sup>|
|Correction action|_−_5_._0<br>|Correction action rate|_−_1_._0<br>|
|Wrist torque|_−_4_·_10<sup>_−_5</sup>|Wrist joint smoothness|_−_4_·_10<sup>_−_6</sup>|
|Joint position limit|_−_10_._0|Joint velocity limit|_−_5_._0|
|Self-collision|_−_10_._0|Net clearance|100_._0|
|Ball velocity constraint|50_._0|Racket velocity constraint|50_._0|
|Pelvis facing forward|1_._0|||
||Term|ination<br>||
|Fall|_−_200_._0|Miss ball|_−_200_._0|
|Ball-net collision|_−_50_._0|Ball out of bounds|_−_50_._0|
|Stroke style violation|_−_50_._0|||


#### **3.3.1 Task Setting** 

At the beginning of each episode, the humanoid robot is randomly initialized at a position on the court in a ready pose. In each episode, the robot is required to consecutively return eight tennis balls to the target location, each initialized with different positions and velocities, to the target location. The generated ball trajectories in our work is visualized in Figure 3. The incoming balls are launched every 2 seconds. The rewards are shown in Table 1. 


**Figure 3 Visualization of generated ball trajectories.** 

#### **3.3.2 Action Correction** 

Accurately capturing the subtle wrist motions of human athletes during racket swings is extremely challenging. The embodiment gap between humans and humanoids further amplifies this discrepancy. As a result, the retargeted wrist motions are highly inaccurate and cannot be directly utilized. To mitigate this issue, we adopt a hybrid control approach [44]. The high-level policy simultaneously outputs _a_<sup>planner</sup> _t_ = [ _a_<sup>latent</sup> _t , a_<sup>correct</sup> _t_ ], including latent actions and direct control commands for the right wrist. Since the latent action space is designed to be robust to right wrist corrections, the high-level policy can output arbitrary wrist motion adjustments without compromising the stability and agility of the lower-body movements. 

#### **3.3.3 Latent Action Barrier** 

The learned latent space creates a compact and continuous manifold of the primitive skills characterized by the precollected human motion data. We aim to learn a high-level policy that can correct and compose these primitive skills to accomplish the tennis return task, thereby enabling the policy to complete the task while preserving the motion naturalness. However, since our imperfect human motion data only provides priors about natural motor skills and does not contain any knowledge about how to utilize them for the tennis return task, the high-level policy needs to discover how to leverage these skills for task accomplishment via reinforcement learning. A key challenge lies the balance between task performance and adherence to the primitive skill priors during high-level policy training. Although the latent space contains many high-quality primitive skills, without proper constraints, the high-level policy can easily exploit this space during RL training, sampling suboptimal actions and composing them into unnatural, jittery motion sequences. For example, the high-level policy may switch back and forth between different locomotion primitives while running toward the incoming ball, resulting in low-quality motions that nevertheless succeed in completing the task. 


**Figure 4 The motivation of Latent Action Barrier (LAB).** 

To address this problem, we propose to constrain the exploration space of the high-level policy. The learnable conditional prior distribution _P_ depicts state-dependent action distribution and can serve as a good starting point. The action space of _a_<sup>latent</sup> _t_ can be formed as a residual action space [18, 46] with respect to the prior’s mean _µ_<sup>_p_</sup> _t_<sup>.</sup> 

However, the manifold of primitive skills is not solely determined by the prior mean, but is also shaped by the associated variance. If the exploration space of the residual latent action _a_<sup>latent</sup> _t_ is not constrained, the high-level policy can still easily sample latent actions that deviate significantly from the prior’s mean _µ_<sup>_p_</sup> _t_<sup>,ultimatelydecodingthem</sup> into suboptimal motor actions. Therefore, we propose to constrain the exploration range of the residual latent action _a_<sup>latent</sup> _t_ within a Latent Action Barrier around the prior’s mean _µ_<sup>_p_</sup> _t_<sup>.Inoursetting,weobservethattheprior’sstan-</sup> dard deviation _σt_<sup>_p_variessignificantlyacrossdifferentstates,</sup> as well as across different dimensions of the latent space. Thus, we design the barrier based on the Mahalanobis distance rather than the Euclidean distance (i.e., the barrier range is adaptively scaled according to the state-dependent standard deviation). The final PD target action can be 

written as: 


where the hyperparameter _λ_ is a scale factor to control the exploration range. Figure 4 demonstrates the intuitive motivation behind Latent Action Barrier (LAB). 

## **4 Sim-to-Real Transfer** 

Due to the high dynamics of humanoid movement, the high speed of the tennis ball, and the high precision of humanoid-tennis interaction, transferring the learned policy from simulation to the real world is non-trivial. We will first introduce our dynamics randomization techniques in Section 4.1. Then we will introduce the observation noise in Section 4.2. At last, we will introduce our real-world deployment in Section 4.3. 

### **4.1 Dynamics Randomization** 

To mitigate the dynamics gap between simulation and the real world, we introduce dynamics randomization of the humanoid and the tennis ball, as shown in Table 2. 

For the robot, we introduce randomization in friction, armature, mass, and center of mass. 

For the tennis ball, a major challenge lies in modeling contacts between the ball and the ground or racket, as well as the aerodynamic effects on ball. These factors can significantly influence ball trajectories and constitute the primary sources of the sim-to-real gap. Existing works [27, 44] often rely on precise system identification and explicit modeling of complex aerodynamic effects. However, we found that sufficient domain randomization in dynamics enables effective sim-to-real transfer and greatly improve the robustness of the system (Table 2). We introduce randomization in ball mass, ball-ground restitution, tangential damping, and the air-drag coefficient _k_ . The air-drag force is modeled as **_f_** _air_ = _−k ∗ m ∗_ **_v_** _∗||_ **_v_** _||_ , where _m_ is the mass of the object and **_v_** denotes its velocity. 

**Table 2 Dynamics randomization used in LATENT.** We randomize robot dynamics and tennis ball physics. 

|Term|Value|
|---|---|
|Robot||
|Feet friction|_U_(1_._0_,_2_._5)|
|Joint friction|_×U_(0_._75_,_1_._25)|
|Armature|_×U_(1_._0_,_1_._05)|
|Body mass|_×U_(0_._75_,_1_._25)|
|Body CoM|_U_(_−_0_._05_,_0_._05)|
|Racket CoM|_U_(_−_0_._1_,_0_._1)|
|Racket mass|_×U_(0_._8_,_1_._2)|
|Tennis Ball||
|Ball mass|_×U_(0_._95_,_1_._05)|
|Ball-ground restitution|_U_(0_._71_,_0_._79)|
|Ball-ground tangential damping|_U_(0_._4_,_0_._7)|
|Ball air-drag coefficient|_U_(0_._01_,_0_._04)|


### **4.3 Real-world Deployment** 

In the real world, we attach a tennis racket to the humanoid’s right wrist using a 3D-printed connector and replace the right hand. To obtain the global state of the robot and the tennis ball, we utilize an optical motion capture system. We attach multiple reflective markers to the robot base and model them as a rigid body to estimate its global 6D pose. The ball is covered with reflective tape and modeled as a passive reflective marker. 

## **5 Experiments** 

In this section, we provide extensive experimental results in both the MuJoCo [29] simulator and the real-world deployment. We choose the 29-DoF Unitree G1 humanoid robot for all our experiments. Here, we aim at addressing the following three questions: 

- **Q1** : How does LATENT perform on the tennis return task compared with existing methods? 

- **Q2** : How does each component contribute to the final performance of LATENT? 

- **Q3** : How does LATENT perform in the real world? 

### **4.2 Observation Noise** 

To mitigate observation errors caused by inaccurate realworld state estimation and system latency, we introduce our modeling of the observation noise in the simulation. 

We add uniform noise, frame-level dropouts, and latency in the policy observations. Due to the high speed nature of tennis, accurately estimating the ball’s state is crucial for successful ball striking. We first obtain the ball position and then compute its velocity via finite differencing. However, we observe that even small amounts of noise in position estimation can significantly degrade the accuracy of the inferred velocity. To mitigate this issue, we maintain a four-frame sliding window in both simulation and the real world, and use the averaged velocity within this window as the ball observation. 

### **5.1 Comparison of Performances** 

To address **Q1** ( _How does LATENT perform on the tennis return task compared with existing methods?_ ), we compare LATENT with baseline methods on a simulated tennis return task. 

#### **5.1.1 Experiment Setting** 

In this experiment, we evaluate the humanoid’s performance of the tennis return task. We use the method described in Section 3.3 to randomly initialize the ball and the robot. We evaluate the performance of our method under different stroke types (forehand and backhand) and across different court regions (forecourt and backcourt). The results are averaged over a total of 10,000 trials. 

**Table 3 Comparison with baseline methods. Bold** numbers indicate the best performance. 

|Method|||**For**|**ehand**|||||**B**|**ackhand**|||**Fo**|**recourt**|||**Ba**|**ckcourt**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||SR↑|DE↓|Smth↓|Torque|↓<br>SR↑|D|E|↓|Smth↓|Torque↓|SR↑|DE↓|Smth↓|Torque↓|SR↑|DE↓|Smth↓|Torque↓|
|PPO [26]||N/A|N/A|N/A|N/A|N/A|N|/|A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|MotionVAE|[44]|N/A|N/A|N/A|N/A|N/A|N|/|A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|AMP [21]||41.32|4.71|46.52|13.79|36.81|5|.2|2|37.68|15.74|49.48|4.20|36.16|18.26|41.73|4.85|41.77|19.20|
|ASE [22]||63.47|3.62|38.91|11.84|55.22|4|.0|1|31.75|12.92|71.36|3.28|30.84|14.05|68.59|3.90|35.12|15.27|
|PULSE [18]||71.85|3.01|32.44|9.76|63.38|3|.1|5|29.60|10.83|74.52|2.97|28.11|12.01|72.94|3.02|31.27|13.44|
|**Ours**||**96.52**|**1.32**|**25.61**|**7.40**|**82.10**|**1**|**.8**|**9**|**27.76**|**7.71**|**86.35**|**1.73**|**25.51**|**7.47**|**89.80**|**1.55**|**27.20**|**7.60**|
|||||**Ta**|**ble 4 Ab**|**lation stu**|**dy.**||**B**|**old** nu|mbers ind|icate th|e best|perfor|mance.|||||
|Mthd||**F**|**orehan**|**d**|||**Ba**|**c**|**k**|**hand**|||**Fore**|**court**|||**Ba**|**ckcourt**||
|eo|SR↑|DE↓|Smth|↓To|rque↓|SR↑<br>D|E↓||S|mth↓<br>T|orque↓|SR↑<br>|DE↓<br>S|mth↓<br>|Torque↓|SR↑|DE↓|Smth↓|Torque↓|
|w/o Corr.|82.36|3.41|26.7|2<br>|8.85|68.94<br>3.|03||2|9.55|8.92|74.21<br>|3.18<br>|26.86|9.64|79.05|3.52|29.94|9.38|
|w/o LAB|93.12|2.17|37.6|4<br>1|2.53|76.96<br>2.|21||3|1.77|12.11|84.73<br>|1.96<br>|30.59|10.94|87.44|2.05|32.08|13.62|
|**Ours**|**96.52**|**1.32**|**25.6**|**1**<br>**7**|**.40**|**82.10**<br>**1.**|**89**||**2**|**7.76**|**7.71**|**86.35**<br>|**1.73**<br>|**25.51**|**7.47**|**89.80**|**1.55**|**27.20**|**7.60**|


#### **5.1.2 Experiment Metrics** 

We use the following two metrics to measure the task performance: 

- **Success Rate (SR)** records the percentage of trials that humanoids successfully return an incoming tennis ball to within 2.5 meters of the target location. 

- **Distance Error (DE)** is the averaged distance between the returned tennis ball’s actual landing position and the target location. 

We also use the following two metrics to measure the action quality of the humanoid: 

- **Smoothness(Smth)** is the averaged acceleration of every joint to measure the naturalness and stability of the humanoid actions. 

- **Torque** is the averaged torque of every joint to measure the physical feasibility and hardware safety of the humanoid actions. 

#### **5.1.3 Baselines** 

We choose the following methods as baselines: 

- **PPO** [26]: We directly train the policy with the vanilla PPO algorithm to accomplish the tennis return task without any human motion prior. 

- **MotionVAE** [44]: We adopt the MotionVAE framework used in Vid2Player3D, where we train a kinematicsbased motion VAE. The high-level policy is trained to sample in the latent motion space. The sampled latent is decoded into kinematic motions, which are then tracked by a decoupled motion tracker. 

- **AMP** [21]: We adopt AMP, a reinforcement learning framework that incorporates human motion prior through adversarial training. 

- **ASE** [22]: We adopt ASE, a method that learns reusable adversarially trained skill embeddings to accomplish high-level tasks. 

- **PULSE** [18]: We adopt PULSE, which learns VAEstyle motion representation through online distillation from a pre-trained motion tracker. The key difference from our method is that, in this baseline, we strictly follow the original paper’s procedure to construct and sample from the latent space and do not apply any wrist corrections. 

#### **5.1.4 Experiment Results** 

The results are shown in Table 3. “N/A” indicates that the method fails to converge. LATENT outperforms baseline methods in tennis return task performance and action quality. For vanilla PPO, it is extremely difficult to learn tennis skills from scratch without any motion prior. We implement the MotionVAE proposed in Vid2Player3D. However, we found that the decoupled design of the motion generator and the tracker places stringent requirements on both components. Low-quality motions generated by the motion generator can make accurate tracking difficult, which in turn further degrades the quality of the autoregressively generated kinematic motions. Such accumulated errors can quickly cause the robot to lose balance and fall. Vid2Player3D [44] alleviates this issue by introducing residual force and relying on unrealistic physics assumptions. However, the requirement of real-robot deployment prevents us from adopting such assumptions. For AMP and ASE, we found that these adversarial learning-based methods struggle to strike a balance between task completion and adherence to the motion prior. For PULSE, we found that its approach to constructing and utilizing the latent action space leads to lower-quality sampled actions. Moreover, the absence of wrist-level correction further degrades its task completion performance. 

### **5.2 Ablation of Key Components** 

To address **Q2** ( _How does each component contribute to the final performance of LATENT?_ ), we conduct ablation studies on each key component of our method. 

#### **5.2.1 Experiment Setting and Metrics** 

We adopt the same experiment setting and metrics in Section 5.1. 

#### **5.2.2 Baselines** 

We choose the following methods as baselines: 

- **Ours w/o Correction (w/o Corr.)** : We train a whole-body motion tracker, including the right wrist joints, and then distill it to a latent space for all joints. The highlevel policy is not allowed to correct the right wrist actions. 

- **Ours w/o Latent Action Barrier (w/o LAB)** : We remove the latent action barrier and allow the high-level policy to output residual latent actions in an unconstrained manner. 

**Table 5 Real-world performance. Bold** numbers indicate the best, 

and <u>underlined</u> numbers indicate the second. 

|Mthd|**Foreha**|**nd**|**Backh**|**and**|**Foreco**|**urt**|**Backc**|**ourt**|
|---|---|---|---|---|---|---|---|---|
|eo|SR↑|DE↓|SR↑|DE↓|SR↑|DE↓|SR↑|DE↓|
|w/o DR|16.67%|5.60|25.00%|4.57|28.57%|3.59|14.29%|6.23|
|w/o ON|50.00%|3.28|0.00%|N/A|28.57%|3.69|37.50%|3.97|
|**Ours**|**90.90% **|**3.15**|**77.78% **|**3.89**|**88.89% **|**3.57**|**81.82% **|**3.80**|


- **Ours w/o Observation Noise (w/o ON)** : In this baseline, we remove all observation noise applied to the ball. 

#### **5.3.4 Experiment Results** 

The real-world evaluation results are shown in Table 5. Our method demonstrates strong real-world performance. We show that adequately randomizing ball dynamics and observation can enable effective sim-to-real transfer without relying on precise system identification. 

#### **5.2.3 Experiment Results** 

The results are shown in Table 4. Our key designs contribute to the final performance. Without wrist correction, the policy’s success rate drops significantly. Without the latent action barrier, the high-level policy tends to exploit the latent space to sample suboptimal actions, resulting in jittery motion sequences and ultimately degrading the overall policy performance. 

### **5.3 Evaluation of real-world performance** 

To address **Q3** ( _How does LATENT perform in the real world?_ ), we conduct real-world experiments. 

#### **5.3.1 Experiment Setting** 

We conduct 20 consecutive human-robot rally matches to evaluate our policy’s tennis return performance in the real world, with randomized initial positions and velocities of the ball. For each successfully returned ball, we record the landing position, categorize it into forecourt or backcourt regions, and analyze the usage of forehand and backhand strokes. 

## **6 Conclusion** 

We propose LATENT, a novel system to learn athletic humanoid tennis skills from imperfect human motion data. We successfully deploy our method on a real-world humanoid robot and can stably sustain multi-shot rallies with human players. Although this work primarily focuses on the tennis return task, the proposed framework has the potential to generalize to a broader range of tasks where complete and high-quality human motion data are unavailable (e.g., soccer and parkour). The current work presents several potential directions for improvement. First, the proposed method relies on a motion capture system for real-world deployment. Incorporating active vision could help alleviate this limitation. Second, the current task formulation focuses on returning randomly initialized incoming balls to target locations, which still differs from a real two-player tennis match. Achieving a level of performance comparable to professional human players may require introducing a multi-agent training framework. 

#### **5.3.2 Experiment Metrics** 

We still adopt **Success Rate (SR)** and **Distance Error (DE)** as our metrics. However, due to the sim-to-real gap, we observe that the landing accuracy on the real-world performance is relatively low. Therefore, we consider a trial successful if the robot successfully returns the ball within the opponent’s court boundaries. 

#### **5.3.3 Baselines** 

Since sim-to-real transfer for the humanoid robot itself has been extensively studied in prior works [47, 8, 7] and is not the primary focus of this paper, we design the baseline mainly to validate the effectiveness of incorporating dynamics randomization and observation noise for the ball. 

- **Ours w/o Dynamics Randomization (w/o DR)** : In this baseline, we remove all dynamics randomization applied to the ball. 

## **References** 

- [1] Firas Al-Hafez, Guoping Zhao, Jan Peters, and Davide Tateo. Locomujoco: A comprehensive imitation learning benchmark for locomotion. _arXiv preprint arXiv:2311.02496_ , 2023. 

- [2] Trapit Bansal, Jakub Pachocki, Szymon Sidor, Ilya Sutskever, and Igor Mordatch. Emergent complexity via multi-agent competition. _arXiv preprint arXiv:1710.03748_ , 2017. 

- [3] Yeke Chen, Shihao Dong, Xiaoyu Ji, Jingkai Sun, Zeren Luo, Liu Zhao, Jiahui Zhang, Wanyue Li, Ji Ma, Bowen Xu, et al. Learning human-like badminton skills for humanoid robots. _arXiv preprint arXiv:2602.08370_ , 2026. 

- [4] Zhiyang Dou, Xuelin Chen, Qingnan Fan, Taku Komura, and Wenping Wang. C· ase: Learning conditional adversar- 

ial skill embeddings for physics-based characters. In _SIGGRAPH Asia 2023 Conference Papers_ , pages 1–11, 2023. 

- [5] Jakob Foerster, Gregory Farquhar, Triantafyllos Afouras, Nantas Nardelli, and Shimon Whiteson. Counterfactual multi-agent policy gradients. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 32, 2018. 

- [6] Tuomas Haarnoja, Ben Moran, Guy Lever, Sandy H Huang, Dhruva Tirumala, Jan Humplik, Markus Wulfmeier, Saran Tunyasuvunakool, Noah Y Siegel, Roland Hafner, et al. Learning agile soccer skills for a bipedal robot with deep reinforcement learning. _Science Robotics_ , 9(89):eadi8022, 2024. 

- [7] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 

- [8] Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning humanto-humanoid real-time whole-body teleoperation. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 8944–8951. IEEE, 2024. 

- [9] Johannes Heinrich and David Silver. Deep reinforcement learning from self-play in imperfect-information games. _arXiv preprint arXiv:1603.01121_ , 2016. 

- [10] Muqun Hu, Wenxi Chen, Wenjing Li, Falak Mandali, Zijian He, Renhong Zhang, Praveen Krisna, Katherine Christian, Leo Benaharon, Dizhi Ma, et al. Towards versatile humanoid table tennis: Unified reinforcement learning with prediction augmentation. _arXiv preprint arXiv:2509.21690_ , 2025. 

- [11] Minsu Kim, Eunho Jung, and Yoonsang Lee. Physicsfc: Learning user-controlled skills for a physics-based football player controller. _arXiv preprint arXiv:2504.21216_ , 2025. 

- [12] Jipeng Kong, Xinzhe Liu, Yuhang Lin, Jinrui Han, Sören Schwertfeger, Chenjia Bai, and Xuelong Li. Learning soccer skills for humanoid robots: A progressive perception-action framework. _arXiv preprint arXiv:2602.05310_ , 2026. 

- [13] Yitang Li, Mingxian Lin, Zhuo Lin, Yipeng Deng, Yue Cao, and Li Yi. Learning physics-based full-body human reaching and grasping from brief walking references. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 27673–27682, 2025. 

- [14] Chenhao Liu, Leyun Jiang, Yibo Wang, Kairan Yao, Jinchen Fu, and Xiaoyu Ren. Humanoid whole-body badminton via multi-stage reinforcement learning. _arXiv preprint arXiv:2511.11218_ , 2025. 

- [15] Libin Liu and Jessica Hodgins. Learning basketball dribbling skills using trajectory optimization and deep reinforcement learning. _Acm transactions on graphics (tog)_ , 37(4):1–14, 2018. 

- [16] Ryan Lowe, Yi I Wu, Aviv Tamar, Jean Harb, OpenAI Pieter Abbeel, and Igor Mordatch. Multi-agent actor-critic for mixed cooperative-competitive environments. _Advances in neural information processing systems_ , 30, 2017. 

- [17] Haofei Lu, Yifei Shen, Dongsheng Li, Junliang Xing, and Dongqi Han. Habitizing diffusion planning for efficient and 

effective decision making. _arXiv preprint arXiv:2502.06401_ , 2025. 

- [18] Zhengyi Luo, Jinkun Cao, Josh Merel, Alexander Winkler, Jing Huang, Kris Kitani, and Weipeng Xu. Universal humanoid motion representations for physics-based control. _arXiv preprint arXiv:2310.04582_ , 2023. 

- [19] Zhengyi Luo, Jinkun Cao, Sammy Christen, Alexander Winkler, Kris Kitani, and Weipeng Xu. Grasping diverse objects with simulated humanoids. _arXiv preprint arXiv:2407.11385_ , 2024. 

- [20] Zhengyi Luo, Jiashun Wang, Kangni Liu, Haotian Zhang, Chen Tessler, Jingbo Wang, Ye Yuan, Jinkun Cao, Zihui Lin, Fengyi Wang, et al. Smplolympics: Sports environments for physically simulated humanoids. _arXiv preprint arXiv:2407.00187_ , 2024. 

- [21] Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 

- [22] Xue Bin Peng, Yunrong Guo, Lina Halper, Sergey Levine, and Sanja Fidler. Ase: Large-scale reusable adversarial skill embeddings for physically simulated characters. _ACM Transactions On Graphics (TOG)_ , 41(4):1–17, 2022. 

- [23] Jiawei Ren, Mingyuan Zhang, Cunjun Yu, Xiao Ma, Liang Pan, and Ziwei Liu. Insactor: Instruction-driven physicsbased characters. _Advances in Neural Information Processing Systems_ , 36:59911–59923, 2023. 

- [24] Junli Ren, Junfeng Long, Tao Huang, Huayi Wang, Zirui Wang, Feiyu Jia, Wentao Zhang, Jingbo Wang, Ping Luo, and Jiangmiao Pang. Humanoid goalkeeper: Learning from position conditioned task-motion constraints. _arXiv preprint arXiv:2510.18002_ , 2025. 

- [25] Stéphane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , pages 627–635, 2011. 

- [26] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [27] Zhi Su, Bike Zhang, Nima Rahmanian, Yuman Gao, Qiayuan Liao, Caitlin Regan, Koushil Sreenath, and S Shankar Sastry. Hitter: A humanoid table tennis robot via hierarchical planning and learning. _arXiv preprint arXiv:2508.21043_ , 2025. 

- [28] Chen Tessler, Yoni Kasten, Yunrong Guo, Shie Mannor, Gal Chechik, and Xue Bin Peng. Calm: Conditional adversarial latent models for directable virtual characters. In _ACM SIGGRAPH 2023 Conference Proceedings_ , pages 1–9, 2023. 

- [29] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ international conference on intelligent robots and systems_ , pages 5026–5033. IEEE, 2012. 

- [30] Jiashun Wang, Jessica Hodgins, and Jungdam Won. Strategy and skill learning for physics-based table tennis anima- 

tion. In _ACM SIGGRAPH 2024 Conference Papers_ , pages 1–11, 2024. 

- [31] Quanyou Wang, Mingzhang Zhu, Ruochen Hou, Kay Gillespie, Alvin Zhu, Shiqi Wang, Yicheng Wang, Gaberiel I Fernandez, Yeting Liu, Colin Togashi, et al. A hierarchical, model-based system for high-performance humanoid soccer. _arXiv preprint arXiv:2512.09431_ , 2025. 

- [32] Yinhuai Wang, Qihan Zhao, Runyi Yu, Hok Wai Tsui, Ailing Zeng, Jing Lin, Zhengyi Luo, Jiwen Yu, Xiu Li, Qifeng Chen, et al. Skillmimic: Learning basketball interaction skills from demonstrations. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 17540–17549, 2025. 

- [33] Yinhuai Wang, Qihan Zhao, Yuen Fui Lau, Runyi Yu, Hok Wai Tsui, Qifeng Chen, Jingbo Wang, Jiangmiao Pang, and Ping Tan. Humanx: Toward agile and generalizable humanoid interaction skills from human videos. _arXiv preprint arXiv:2602.02473_ , 2026. 

- [34] Yushi Wang, Changsheng Luo, Penghui Chen, Jianran Liu, Weijian Sun, Tong Guo, Kechang Yang, Biao Hu, Yangang Zhang, and Mingguo Zhao. Learning vision-driven reactive soccer skills for humanoid robots. _arXiv preprint arXiv:2511.03996_ , 2025. 

_Advances in Neural Information Processing Systems_ , 33: 21763–21774, 2020. 

   - [43] Kevin Zakka, Baruch Tabanpour, Qiayuan Liao, Mustafa Haiderbhai, Samuel Holt, Jing Yuan Luo, Arthur Allshire, Erik Frey, Koushil Sreenath, Lueder A Kahrs, et al. Mujoco playground. _arXiv preprint arXiv:2502.08844_ , 2025. 

   - [44] Haotian Zhang, Ye Yuan, Viktor Makoviychuk, Y Guo, S Fidler, X Peng, and K Fatahalian. Learning physically simulated tennis skills from broadcast videos. _ACM Trans. Graph_ , 42(4), 2023. 

   - [45] Zhikai Zhang, Yitang Li, Haofeng Huang, Mingxian Lin, and Li Yi. Freemotion: Mocap-free human motion synthesis with multimodal large language models. In _European Conference on Computer Vision_ , pages 403–421. Springer, 2024. 

   - [46] Zhikai Zhang, Chao Chen, Han Xue, Jilong Wang, Sikai Liang, Yun Liu, Zongzhang Zhang, He Wang, and Li Yi. Unleashing humanoid reaching potential via real-world-ready skill space. _arXiv preprint arXiv:2505.10918_ , 2025. 

   - [47] Zhikai Zhang, Jun Guo, Chao Chen, Jilong Wang, Chenghuai Lin, Yunrui Lian, Han Xue, Zhenrong Wang, Maoqi Liu, Jiangran Lyu, et al. Track any motions under any disturbances. _arXiv preprint arXiv:2509.13833_ , 2025. 

- [35] Jungdam Won, Deepak Gopinath, and Jessica Hodgins. Physics-based character controllers using conditional vaes. _ACM Transactions on Graphics_ , 41(4):1–12, 2022. 

- [36] Michael Xu, Yi Shi, KangKang Yin, and Xue Bin Peng. Parc: Physics-based augmentation with reinforcement learning for character controllers. In _Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Papers_ , pages 1–11, 2025. 

- [37] Pei Xu, Zhen Wu, Ruocheng Wang, Vishnu Sarukkai, Kayvon Fatahalian, Ioannis Karamouzas, Victor Zordan, and C Karen Liu. Learning to ball: Composing policies for long-horizon basketball moves. _ACM Transactions on Graphics (TOG)_ , 44(6):1–14, 2025. 

- [38] Heyuan Yao, Zhenhua Song, Baoquan Chen, and Libin Liu. Controlvae: Model-based learning of generative controllers for physics-based characters. _ACM Transactions on Graphics_ , 41(6):1–16, 2022. 

- [39] Heyuan Yao, Zhenhua Song, Yuyang Zhou, Tenglong Ao, Baoquan Chen, and Libin Liu. Moconvq: Unified physicsbased motion control via scalable discrete representations. _ACM Transactions on Graphics (TOG)_ , 43(4):1–21, 2024. 

- [40] Kangning Yin, Zhe Cao, Wentao Dong, Weishuai Zeng, Tianyi Zhang, Qiang Zhang, Jingbo Wang, Jiangmiao Pang, Ming Zhou, and Weinan Zhang. Robostriker: Hierarchical decision-making for autonomous humanoid boxing. _arXiv preprint arXiv:2601.22517_ , 2026. 

- [41] Runyi Yu, Yinhuai Wang, Qihan Zhao, Hok Wai Tsui, Jingbo Wang, Ping Tan, and Qifeng Chen. Skillmimicv2: Learning robust and generalizable interaction skills from sparse and noisy demonstrations. _arXiv preprint arXiv:2505.02094_ , 2025. 

- [42] Ye Yuan and Kris Kitani. Residual force control for agile human behavior imitation and extended motion synthesis. 

## **A Additional Experiments** 

In this section, we provide further analysis of our policy. 

### **A.1 Robot Movement Coverage** 

To further analyze the robot’s movement behavior during rallies, we study the spatial distribution of the robot’s pelvis positions across consecutive ball returns, as is demonstrated in Figure 5. We aggregate the pelvis trajectories from different numbers of consecutive ball returns (8, 16, 80, and 400) to examine how the spatial coverage evolves as more interactions are accumulated. Positions with density lower than 0.01% are filtered out for better visualization. 


**Figure 5 Robot movement coverage during consecutive ball returns.** Heatmaps of the robot’s global positions accumulated over different numbers of consecutive ball returns (8, 16, 80, and 400). The learned policy enables effective court coverage and adaptive repositioning during consecutive rallies. 

From the resulting distributions, we observe that the robot consistently explores a wide region of the court while maintaining a stable movement structure across episodes. Figure 5 (a)-(d) indicate that the robot is capable of dynamically repositioning itself and maintaining broad court coverage during repeated rallies. 

### **A.2 Robot-Robot Self-Play** 

To further evaluate the learned policy, we conduct robot-robot self-play experiments in simulation. In this setting, two instances of the policy are deployed on opposite sides of the court to exchange tennis returns. The results show that the two robots can maintain stable rallies and is able achieve up to 25 consecutive rallies, demonstrating the robustness of the policies trained with LATENT. 


**Figure 6 Robot-robot self-play evaluation in simulation.** (a) Visualization of two robots performing self-play on opposite sides of the court. (b) Distribution of number of consecutive rallies over 50 random games. 

To further improve rally performance between the robot and human players, as well as between robots, future works may incorporate reinforcement learning with self-play. Methods such as Neural Fictitious Self-Play (NFSP) [9] and other multi-agent reinforcement learning approaches [2, 16, 5] provide a potential framework for iterative policy improvement through competitive interaction. 

## **B Additional Visualizations** 

In this section, we provide additional qualitative visualization for both simulation and real-world deployment. 

### **B.1 Training in Simulation** 

Figure 7 shows representative hitting events in simulation. The red curves denote incoming ball trajectories (e.g., serves or opponent shots). The robot posture corresponds to the moment of ball contact. The green curves indicate the resulting return trajectories after the hit. These examples illustrate that the learned policy can adapt its body posture and racket motion to intercept diverse incoming trajectories and generate consistent return shots. 


**Figure 7 Different hitting events in simulation.** The red curves denote incoming ball trajectories, the robot posture corresponds to the moment of ball contact, and the green curves indicate the trajectories of the returned balls. 

### **B.2 Close-up Views of the Robot During Rallies in the Real World** 

In our experiments, we build our system based on Unitree G1 and introduce several hardware modifications to improve robustness during motion capture and interaction. Light-diffuse surfaces are added to the robot body to improve motion capture system stability and eliminate spurious reflective areas. A standard tennis racket is mounted to the robot’s right end-effector using a 3D-printed adapter (Figure 2). In addition, the end-effector joint connectors are redesigned to improve structural stability during dynamic motions. 

As shown in Figure 8, the robot exhibits diverse motion patterns when interacting with incoming balls. Across different rallies and ball trajectories, it adapts its body posture and swing timing to reach the ball and execute stable returns. These behaviors resemble those of human tennis players, where the body dynamically adjusts to maintain balance and achieve effective ball contact. Generally, the learned policy produces robust and natural motion strategies in the real world, enabling the robot to perform dynamic tennis returns under varying conditions. 


**Figure 8 Close-up real-world examples.** Representative frames from real-world rallies showing diverse tennis return behaviors, including forehand and backhand strokes, dynamic footwork, and coordinated whole-body motion. 

