---
title: "HALO:Closing Sim-to-Real Gap for Heavy-loaded Humanoid Agile Motion Skills via Differentiable Simulation"
date: "2026-03-16"
authors: "Xingyi Wang; Chenyun Zhang; Weiji Xie; Chao Yu; Wei Song; Chenjia Bai"
url: https://arxiv.org/abs/2603.15084
pdf: https://arxiv.org/pdf/2603.15084
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.15084)** / [論文ページ](https://arxiv.org/abs/2603.15084)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Closing Sim-to-Real Gap for Heavy-loaded Humanoid Agile Motion Skills via Differentiable Simulation** 

Xingyi Wang<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> , Chenyun Zhang<sup>2</sup><sup>_∗_</sup> , Weiji Xie<sup>2</sup><sup>_,_3</sup><sup>_∗_</sup> , Chao Yu<sup>4</sup> , Wei Song<sup>1</sup> , Chenjia Bai<sup>2</sup><sup>_†_</sup> , Shiqiang Zhu<sup>1</sup><sup>_†_</sup> 

> 1Zhejiang University 2Institute of Artificial Intelligence (TeleAI), China Telecom 

> 3Shanghai Jiao Tong University 4Lumos Robotics 

*Equal contribution _†_ Corresponding author 

**_Abstract_ — Humanoid robots deployed in real-world scenarios often need to carry unknown payloads, which introduce significant mismatch and degrade the effectiveness of simulation-toreality reinforcement learning methods. To address this challenge, we propose a two-stage gradient-based system identification framework built on the differentiable simulator MuJoCo XLA. The first stage calibrates the nominal robot model using real-world data to reduce intrinsic sim-to-real discrepancies, while the second stage further identifies the mass distribution of the unknown payload. By explicitly reducing structured model bias prior to policy training, our approach enables zero-shot transfer of reinforcement learning policies to hardware under heavy-load conditions. Extensive simulation and real-world experiments demonstrate more precise parameter identification, improved motion tracking accuracy, and substantially enhanced agility and robustness compared to existing baselines. Project Page: HALO-Humanoid** 

## I. INTRODUCTION 

Humanoid robots are increasingly expected to move beyond controlled laboratory settings and perform complex physical tasks in unstructured environments, such as industrial facilities and disaster-response sites. In these scenarios, robots are typically required to manipulate tools, carry equipment, or integrate additional functional modules to accomplish task-specific objectives. Such loads induce substantial shifts in the robot’s system dynamics by altering its total mass, Center of Mass (CoM), and inertia distribution [15]. Although recent advances in deep reinforcement learning (RL) have achieved impressive agility [7], [16], [33], [36], policies trained with nominal dynamics typically degrade when exposed to large, structured payload variations. 

We interpret heavy-load carrying as a structured sim-toreal gap problem. Unlike small stochastic noise, payload changes introduce systematic and large-scale dynamic mismatch between the simulation and the physical robot. A widely adopted strategy to mitigate the sim-to-real gap is Domain Randomization (DR) [23], [31], which improves robustness by exposing policies to diverse, randomized dynamics during training. However, by treating payload variations as disturbances to hedge against, DR often yields conservative behaviors and cannot fully exploit the robot’s physical capabilities. 

Another line of work adopts data-driven approaches that leverage real-world interaction data to reduce model mismatch. Within this category, System Identification (SysID) 


Fig. 1: **Performance of HALO in heavy-loaded scenarios. (a)** The payload settings used by HALO. **(b, c)** Compared to DR, HALO significantly improves the accuracy of straightline bidirectional walking. **(d)** Data collection under payload conditions with a single-foot constraint. **(e)** HALO enables challenging humanoid locomotion skills. 

plays a central role, which directly estimates physical parameters—such as mass, CoM location, and inertia—using real interaction data. However, traditional SysID faces several practical limitations for floating-based systems like humanoid robots. They often rely on specialized sensing equipment, such as joint torque sensors [11] or external motion capture systems [28], [29], which limits applicability. Moreover, many procedures require isolating subsystems or partially disassembling the robot [1], [13], [30], making them impractical for complex platforms. 

To overcome these limitations, we propose **HALO** ( **H** e **A** vy- **LO** aded humanoid motion control), a unified framework that seamlessly integrates differentiable simulation based SysID into the reinforcement learning control pipeline for heavy-loaded humanoids. HALO formulates parameter 


Fig. 2: **Overview of HALO. (a)** **_Data Collection:_** Trajectories are collected under both loaded and unloaded conditions using exploration policy trained with wide DR, followed by real-world deployment with a fixed foot constraint. **(b)** **_Data Processing:_** Full-body trajectories reconstruction from joint-state measurements via forward kinematics and foot-height alignment. **(c)** **_Two-stage Payload-related Parameter Identification:_** Stage 1 optimize the full set of model parameters to yield a calibrated base model using trajectories without payload. Based on the calibrated model, stage 2 optimize only the payload-related parameters, using trajectories collected under loaded conditions. **(d)** **_Heavy-loaded Motion Skills:_** The accurate identified model parameters enabling zero-shot sim-to-real transfer of the learned skills to the physical heavy-loaded humanoid. 

identification as a trajectory-level optimization problem inside a differentiable physics simulator MuJoCo XLA, leveraging the analytical gradients over multiple simulation steps to enable efficient gradient-based optimization of physical parameters directly from real-world interaction data. 

To make such identification practical on floating-base humanoids without relying on external sensing systems, we introduce a lightweight data collection procedure in which one foot is mechanically constrained during trajectory acquisition. This constraint removes the ambiguity in global base drift and enables reliable reconstruction of full-body motion from onboard joint encoders. 

We also identify a central challenge in payload identification: the entanglement between nominal model mismatch and load-induced model change. Without separating these effects, optimization may incorrectly attribute base-model errors to payload parameters. To address this, HALO adopts a two-stage identification strategy that first calibrates the base model and then estimates payload-related parameters under loaded conditions. This structured decomposition significantly improves identification stability and accuracy. 

With the identified dynamics, we can train locomotion policies in simulation and deploy them zero-shot to hardware. In simulation, our approach demonstrates clear advantages over existing methods: against traditional SysID approaches 

such as CMA-ES, HALO yields more accurate estimates of physical parameters, especially under extreme load conditions. Compared to baseline strategies, our policies achieve lower motion-tracking errors. Real-world experiments further validate these results, showing that policies retain high precision and agility under heavy payloads across a range of challenging tasks. These experiments confirm that by reducing structured model bias before policy learning, our framework effectively narrows the sim-to-real gap while preserving agility and robustness. Specifically, under a heavyloaded condition, HALO improves performance by 45 _._ 45% to 73 _._ 33% in the gait precision task and by 72 _._ 97% in the in-place 90<sup>_◦_</sup> yaw jumping task, respectively. Furthermore, HALO achieves 100% success rate in challenging motion tracking tasks. 

In summary, our contributions are summarized as follows: 

- **A Differentiable Two-Stage System Identification Framework:** We propose a trajectory-level gradientbased identification pipeline that decouples base-model calibration from payload parameter estimation, enabling stable and accurate parameter recovery. 

- **Sensor-Minimal Data Collection:** By introducing a fixed-foot constraint, we collect trajectory data by reconstructing full-body states using only joint encoders, removing the dependency on torque sensing or motion 

capture systems. 

- **Agile and Robust Dynamic Performance under Heavy Loads:** By reducing structured model bias prior to policy training, our approach enables zero-shot transfer of reinforcement learning policies to hardware. Extensive simulation and real-world experiments show more accurate parameter identification, improved motion tracking, and superior agility. 

## II. RELATED WORK 

## _A. Domain Randomization and Adaptation Strategy_ 

To bridge the sim-to-real gap without explicit model identification, researchers primarily focus on building policies that are either inherently robust to variations or capable of online compensation. 

_a) Domain Randomization (DR):_ DR remains the de facto standard for building robust policies by exposing the agent to a broad distribution of visual and physical variations during training [17], [21], [23], [31]. Recent advancements have evolved to adaptive schemes, such as curriculum-based or adversarial DR [20], [24], which dynamically adjust parameter distributions. However, DR often requires heuristic tuning of randomization ranges. For heavy-payload tasks, excessive randomization typically leads to overly conservative behaviors, sacrificing the agility required to handle massive inertial shifts. 

_b) Adaptive Policy Learning:_ Alternative approaches attempt to mitigate sim-to-real gap through real-time policy adjustment [14], [19], [25] or data-driven domain transfer [2]. Some even incorporate lifelong learning mechanisms during deployment [27], [32]. However, the effectiveness of these methods is frequently bottlenecked by the requirement for high-quality supervisory signals, and they typically fail to provide the seamless zero-shot transition necessary for immediate field operation. 

_c) Data-driven Dynamics Learning:_ Another class of method involves integrating learned residual model to bridge the gap between idealized simulation and real-world complexity [4], [9]. Instead of identifying physical parameters, these methods deploy neural “patches” to generate corrective efforts or actions for unmodeled dynamics. While these “patch” models perform well in the specific scenarios they were trained for, they often fail to generalize to diverse tasks. 

## _B. Physical Parameter Alignment via System Identification_ 

Rather than learning a robust or adaptive policy that covers a wide range of dynamics, system identification aims to minimize the sim-to-real gap by identifying the true physical parameters. 

_a) Traditional and Sampling-based Methods:_ Traditional system identification relies on specialized hardware or offline calibration to estimate the physical parameters [6], [12]. These approaches are often limited by noise sensitivity and the difficulty of measurement in real-world. More recently, sampling-based evolutionary algorithms have been employed to explore high-dimensional parameter spaces [1], 

[28]. While these methods handle non-differentiable dynamics well, they typically suffer from low sample efficiency due to their reliance on derivative-free optimization, particularly in complex robotic systems. 

_b) Differentiable Simulation Methods:_ Differentiable simulation [5], [35] has emerged as a paradigm-shifting tool for parameter alignment by providing analytical gradients of system dynamics with respect to physical properties. Unlike derivative-free engines, differentiable simulators enable end-to-end gradient-based optimization, allowing for structured, sample-efficient updates in high-dimensional parameter spaces. This approach has demonstrated remarkable success in mitigating sim-to-real discrepancies across diverse robotic platforms, ranging from fixed-base manipulators [3], [26] to floating-base systems such as quadcopters [22] and quadruped robots [10]. While recent breakthroughs have successfully optimized complex actuator parameters for a humanoid system [13], scaling this framework to heavypayload humanoids—where massive inertial shifts and nonlinear dynamics dominate—remains an open, high-stakes challenge that requires a more robust identification strategy. 

## III. METHODS 

We consider a robot with known nominal model parameters that must execute locomotion skills while carrying an unknown payload with its upper limbs. Our goal is to first identify the effective model parameters under the payload and subsequently execute motion skills based on the identified dynamics. 

Our method consists of three steps. (i) _Data Collection_ : We execute an exploration policy to control the robot under both unloaded and loaded conditions to collect state–action trajectory data. (ii) _Gradient-Based Identification_ : We estimate the effective model parameters via a two-stage gradientbased optimization procedure that minimizes the trajectory matching error under loaded dynamics. (iii) _Heavy-Load Skill Acquisition_ : Using the identified parameters, we train reinforcement learning policies for agile locomotion tasks, including balancing, dancing, and payload-carrying. Fig. (2) provides an overview of the proposed method. 

## _A. Data Collection_ 

Accurate global state trajectories are typically difficult to obtain for a floating-base humanoid robot without external measurement systems such as motion capture (MoCap). To address this, we constrain one foot of the robot using 2 vises, enabling full-body trajectories to be reconstructed from joint-state measurements via forward kinematics. The same kinematic constraint is applied in the simulation to maintain consistency. We heuristically design a robot trajectory with the fixed foot and train an exploration policy to imitate it, following the procedure described in Sec. (III-C). Data is then collected on the physical robot using this policy, recording joint positions, and the corresponding control inputs. Here, the control input refers to the target joint positions commanded by the RL policy and tracked via a low-level PD controller. The policy is trained with nominal 


Fig. 3: **Inconsistent left-right foot heights caused by sensor noise. (a)** In the original trajectory, the right foot position calculated via forward kinematics remains suspended in the air. **(b)** In the optimized trajectory, the right foot maintains physically consistent ground contact. 

model parameters and a wide range of domain randomization to ensure stability under varying payload conditions. Additionally, due to sensor noise, directly recover body state from joint measurements may introduce accumulated drift, leading to inconsistent left–right foot heights, as illustrated in Figure (3). To correct this, at each timestep we solve a constrained quadratic program over the root and lower-body joint increments, minimally adjusting the configuration to eliminate foot-height discrepancies. 

Because small changes in mass or CoM position can quickly cause the simulated trajectory to drift, only a small amount of data is needed to identify the main differences between the model and the real robot. 

where the tracking loss _L_ track( **_θ_** ) measures trajectory discrepancy between the simulated trajectories and the real-world reference trajectories in Cartesian space, and _R_ ( **_θ_** ) denotes regularization terms that enforce physical plausibility and prevent singular solutions. 

The resulting optimization problem is solved via gradientbased methods by leveraging the differentiability of Φsim. The parameters are updated iteratively using Gradient Descent (GD): 


where _k_ denotes the optimization iteration index, _η_ is the learning rate. 

_2) Tracking Loss:_ For a complete real motion trajectory, we uniformly sample a batch of _B_ trajectory fragments. At each sampled starting point, we reset the robot’s state in the simulation environment and execute a rollout of _N_ control steps to calculate loss. The tracking loss consists of two components: (1) the position loss for all bodies _B_ in the robot, and (2) an additional loss for the upper-body subset _U ⊂B_ weighted by _α_<sup>_u_</sup> . This additional term emphasizes accurate tracking of the body links most influenced by the payload. The tracking loss function is formulated as: 


## _B. Gradient-Based Identification_ 

_1) Problem Formulation:_ Let **_θ_** _∈_ R<sup>_d_</sup> denote a set of physical parameters, including link mass, CoM position, inertia, and joint damping coefficients. 

The real-world system evolves according to unknown dynamics: 


where _si_ , _ai_ , and **_θ_**<sup>_r_</sup> denote the system state, control input at timestep _i_ , and the groundtruth parameters of the real system, respectively. 

In simulation, we approximate the dynamics with a differentiable model: 


where the control sequence is fixed to the recorded real-world actions _a_<sup>_r_</sup> _i_<sup>,andtheinitialstateissynchronized:</sup><sup>_s_</sup> 0<sup>_s_=</sup><sup>_sr_</sup> 0<sup>_._</sup> Given a collected real-world trajectory _τ_<sup>_r_</sup> = _{s_<sup>_r_</sup> 0<sup>_, a_</sup> 0<sup>_r, . . . , sr_</sup> _N_<sup>_}_,ourgoalistoestimateparameters</sup><sup>**_θ_**</sup> such that the simulated trajectory _τ_<sup>_s_</sup> ( **_θ_** ) = _{s_<sup>_s_</sup> 0<sup>_, . . . , ss_</sup> _N_<sup>_}_</sup> matches the real trajectory. We formulate system identification as a trajectorymatching optimization: 


where: 

- _B_ denotes the set of all robot 

## bodies, 

- _U ⊂B_ denotes the subset of upper-body links (e.g., torso and hands), 

- **x**<sup>_s_</sup> _b,t,j_<sup>(</sup><sup>**_θ_**)</sup><sup>_,_</sup><sup>**x**</sup> _b,t,j_<sup>_r∈_R3denotethesimulatedandreal</sup> Cartesian positions of body _j_ at timestep _t_ in batch _b_ , which are components of the corresponding system states. 

_3) Regularization Terms:_ To prevent the identified parameters from deviating substantially from their nominal values, we introduce regularization terms that penalize large changes. Let _I_ link and _I_ joint denote the set of links and joints whose parameters are identified, respectively. The total regularization is then defined as a weighted sum of four components: 


Here, **p** _i_ denotes the CoM position of the _i_ -th link relative to its parent link, and _mi_ is the corresponding link mass. Their nominal values are given by **p**<sup>base</sup> _i_ and _m_<sup>base</sup> _i_ . The variables _αd,k_ and _αf,k_ represent the joint damping coefficient and static friction of the _k_ -th joint, respectively. 

Accordingly, _R_ com and _R_ mass penalize deviations of link CoM positions and masses from their nominal values, while _R_ damp and _R_ fric softly constrain the joint damping and friction to remain within a reasonable interval using the boxconstraint function: 

_ϕ_ ( _α_ ; _l, u_ ) = max(0 _, l − α_ )<sup>2</sup> + max(0 _, α − u_ )<sup>2</sup> _,_ (9) 

which only penalizes values outside the interval [ _l, u_ ]. 

_4) Two-Stage System Identification:_ Directly optimizing model parameters from nominal values using trajectories collected under loaded conditions can lead to biased estimates. In practice, humanoid robots exhibit Sim-to-Real discrepancies due to wear, calibration drift, and minor structural variations, which exist even in the absence of payloads. Without compensating for this nominal model mismatch, the optimization process may incorrectly attribute base-model errors to payload-related parameters. 

We therefore adopt a two-stage identification procedure that separates base-model calibration from payload estimation. 

- 1) **Stage 1: Base Model Calibration.** Using trajectories collected without payload, we optimize the full set of model parameters starting from their nominal values, yielding a calibrated base model that reduces the inherent Sim-to-Real gap. 

- 2) **Stage 2: Payload Parameter Identification.** With the calibrated model serving as initialization, we optimize only the payload-related parameters, specifically the mass and its CoM positions of the links attached by the payload, i.e., torso and hands, using trajectories collected under loaded conditions. 

In practice, restricting the second stage to mass and CoM parameters is sufficient to significantly reduce the Simto-Real gap in heavy-load scenarios, while avoiding the complexity of optimizing the inertia tensor. 

## _C. Skill Acquisition Under Heavy-Load_ 

The identified parameters can be directly utilized for general simulation training. We adopt a motion imitation method based on mjlab [34] to train RL policies for agile motion skills. A set of reference robot motion trajectories is pre-collected and used as imitation targets. In simulation, 

MLP-based policies are optimized using PPO to maximize a tracking reward that encourages alignment of joint states and body poses with the reference trajectories. After training, policies can be directly deployed on the real robot. Owing to the accurately identified model parameters, only minimal domain randomization is required during training, enabling zero-shot sim-to-real transfer of the learned skills to the physical robot. 

TABLE I: Domain Randomization Settings. 

|**Term**|**Nominal Range**|**Wide Range**|
|---|---|---|
|Base CoM offset (m)|_U_(_−_0_._03_,_0_._03)<br>|_U_(_−_0_._08_,_0_._08)<br>|
|Torso mass offset (kg)|_U_(_−_0_._5_,_0_._5)|_U_(2_._0_,_8_._0)|
|Hands mass offset (kg)|_U_(_−_0_._5_,_0_._5)|_U_(1_._0_,_4_._0)|
|Hands CoM offset (m)|_U_(_−_0_._02_,_0_._02)|_U_(_−_0_._05_,_0_._05)|
|Encoder bias (rad)|_U_(_−_0_._01_,_0_._01)|_U_(_−_0_._01_,_0_._01)|
|Foot friction|_U_(0_._3_,_1_._2)|_U_(0_._3_,_1_._2)|


## IV. EXPERIMENT 

Our experiments aim to address the following key questions: 

- **Q1:** Can HALO outperform CMA-ES based methods for heavy-loaded humanoid SysID? 

- **Q2:** Does HALO bring better performance compared to other methods for motion tracking tasks under heavy payloads? 

- **Q3:** Does the two-stage method lead to higher realworld SysID accuracy? 

- **Q4:** Can the parameters identified by HALO improve the robustness of sim-to-real transfer for heavy-loaded motion tracking tasks? 

## _A. Experiment overview_ 

The advantages of HALO are validated through both simulations (Secs. (IV-B), (IV-C)) and real-world experiments (Secs. (IV-D), (IV-E)). 

**Experiment Settings.** We use Unitree G1 to test performance of HALO, which stands approximately 132 cm tall and has a nominal mass of 35 kg. 

- **Simulation Payload Setting** . For simulation, we design three different perturbation settings to manually perturb the physical parameters, simulating the sim2real gap introduced by payloads, as shown in Table (II). 

- **Real-World Payload Setting** . We introduce payload in real-world by manually attaching 6 kg diving counterweights to the torso link, and 2 kg counterweights to each wrist link (hand), as shown in Figure (1)(a). 

## _B. HALO vs. CMA-ES: Performance under Extreme Payload Perturbations_ 

To answer **Q1** , we collect data in simulation using the perturbed values, while setting the nominal values as the optimization start. The regularization terms were not enabled in simulation experiment. HALO utilizes learning rates of 0 _._ 03 for mass and 0 _._ 0002 for CoM position. CMA-ES is configured with a population size of 10. Both methods undergo 

TABLE II: Convergence comparison between CMA-ES and HALO. Results are reported as mean _±_ standard deviation. Groundtruth values (e.g., +6 _._ 000, +2 _._ 4000) denote the incremental offsets added to the absolute nominal values. Bold values indicate performance closer to the ground truth. While CMA-ES converges under light payloads, it exhibits sensitivity to random seeds under heavy payloads. 

|**Method**|**Torso**<br>**Mass(kg)**|**Left Hand**<br>**Mass(kg)**|**Right Hand**<br>**Mass (kg)**|**Torso CoM**<br>**pos x (m)**|**Torso CoM**<br>**pos y (m)**|**Torso CoM**<br>**pos z (m)**|
|---|---|---|---|---|---|---|
|_Absolute Nom_|_inal Values_||||||
||7_._8180|0_._2546|0_._2546|0_._0020|0_._0003|0_._1845|
|_Perturbation _|_Setting 1_||||||
|Groundtruth|+6_._0000|+2_._4000|+2_._0000|+0_._0100|+0_._0200|+0_._0500|
|CMA-ES|+6_._0366_±_ 0_._0128|+2_._4009_±_ 0_._0012|+1_._9970_±_ 0_._0012|+**0**_._**0099**_±_ **0**_._**0000**|+0_._0199_±_ 0_._0001|+0_._0505_±_ 0_._0004|
|**HALO**|+**5**_._**9989**_±_ **0**_._**0000**|+**2**_._**4005**_±_ **0**_._**0000**|+**1**_._**9973**_±_ **0**_._**0000**|+0_._0098_±_ 0_._0000|+**0**_._**0199**_±_ **0**_._**0000**|+**0**_._**0505**_±_ **0**_._**0000**|
|_Perturbation _|_Setting 2_||||||
|Groundtruth|+9_._0000|+3_._2000|+2_._8000|+0_._0200|+0_._0400|+0_._0700|
|CMA-ES|+**8**_._**9988**_±_ **0**_._**0321**|+3_._2055_±_ 0_._0093|+2_._7935_±_ 0_._0184|+**0**_._**0200**_±_ **0**_._**0000**|+**0**_._**0400**_±_ **0**_._**0000**|+0_._0667_±_ 0_._0002|
|**HALO**|+9_._0918_±_ 0_._0000|+**3**_._**1981**_±_ **0**_._**0000**|+**2**_._**7982**_±_ **0**_._**0000**|+0_._0199_±_ 0_._0000|+0_._0492_±_ 0_._0000|+**0**_._**0668**_±_ **0**_._**0000**|
|_Perturbation _|_Setting 3_||||||
|Groundtruth|+12_._0000|+3_._5000|+3_._0000|+0_._0200|+0_._0400|+0_._0700|
|CMA-ES|+12_._4289_±_ 0_._9244|+4_._7885_±_ 2_._7441|+3_._6660_±_ 1_._3323|_−_0_._0616_±_ 0_._1824|_−_0_._0248_±_ 0_._1449|+1_._2141_±_ 2_._5582|
|**HALO**|+**11**_._**9871**_±_ **0**_._**0000**|+**3**_._**5014**_±_ **0**_._**0000**|+**3**_._**0016**_±_ **0**_._**0000**|+**0**_._**0200**_±_ **0**_._**0000**|+**0**_._**0400**_±_ **0**_._**0000**|+**0**_._**0701**_±_ **0**_._**0000**|


2,000 iterations, reaching complete convergence. For CMAES, we take experiments using five different random seeds, meaning different initial exploration paths. The perturbation settings and results are illustrated at Table (II). 

Experimental results demonstrate that under light payload perturbations, both HALO and CMA-ES methods achieve satisfactory convergence performance with comparable accuracy(e.g., Perturbation Setting 1,2). However, under extremely heavy-loaded conditions (e.g., Perturbation Setting 3), CMA-ES using certain seeds converge to local optima with physically unreasonable values, whereas our gradientbased method robustly converges to the vicinity of the reference parameters. These findings validate the superior optimization stability of our HALO for humanoid SysID under payload conditions. 

## _C. Impact of Accurate Payload Identification_ 

To answer **Q2** , we evaluate the proposed framework under payload dynamics, specifically employing the configuration defined as **Perturbation Setting 1** in Table (II). We conducted motion tracking experiments in mjlab using sequences from AMASS [18], LAFAN1 [8] and HuB [36]. The evaluation suite comprises 20 distinct sequences categorized into two difficulty levels: (i) _Steady-state tasks_ (e.g., walking with waving hands) and (ii) _High-agility tasks_ (e.g., side kicking), with 10 motions per category. 

Adopting the benchmarking setting established in [28], we compare our method against two representative base-lines: **(1) Wide Range DR (WDR),** as illustrated in Table (I), (col. 2). WDR uses the nominal model. **(2) Calibrated Mass (CM).** CM use the calibrated mass to simulating manually weighing the load, but the CoM positions are still nominal values. The DR range applied to CM and HALO is specified in Table (I), (col. 1). Finally, all resulting policies are validated on the ground-truth perturbed model to benchmark their tracking precision. 

Following the evaluation framework established in [7], performance is quantified by three key metrics: _Global Mean Per-Joint Position Error_ ( _E_ g-mpjpe, mm) for global 

alignment, _Mean Per-Joint Position Error_ ( _E_ mpjpe, mm) for local precision, _Velocity Error_ ( _E_ vel, m/s) for global root velocities error. 

As summarized in Table (III), HALO consistently outperforms both baselines across all metrics. This superiority stems from its precise identification of payload mass and CoM offsets. In contrast, WDR relies on a broad randomization range which leads to overly conservative tracking, while CM fails to account for the dynamic variations induced by CoM displacement. By explicitly identifying the physical parameters of these rigid bodies, HALO maintains superior tracking precision compared to existing baselines. 

TABLE III: Experimental results of motion tracking performance across various tasks. 

|**Method**|_E_g-mpjpe|_E_mpjpe|_E_vel|
|---|---|---|---|
|_Steady-sta_|_te tasks_|||
|WDR|94_._91_±_ 3_._21|70_._54_±_ 2_._13|0_._157_±_ 0_._008|
|CM|85_._87_±_ 2_._54|56_._33_±_ 2_._27|0_._130_±_ 0_._006|
|**HALO**|**52**_._**47**_±_ 2_._11|**44**_._**87**_±_ 1_._82|**0**_._**098**_±_ 0_._008|
|_High-agili_|_ty tasks_|||
|WDR|132_._89_±_ 2_._89|81_._54_±_ 2_._43|0_._136_±_ 0_._016|
|CM|92_._82_±_ 3_._21|67_._06_±_ 3_._21|0_._125_±_ 0_._011|
|**HALO**|**78**_._**83**_±_ 2_._55|**59**_._**54**_±_ 2_._07|**0**_._**106**_±_ 0_._009|


## _D. Effectiveness of the Two-Stage Strategy_ 

In this section, we compare two-stage method with onestage baseline. The one-stage method directly identifies masses and CoM positions of loaded torso link and hand links, using only the loaded trajectories collected from the real-world. We collect three trajectories with payload and three trajectories without payload, and take the average of the final converged values as identification results. Reference masses are reported as the sum of the nominal masses and the masses of additional counterweights for loaded links. We conduct an initial assessment by evaluating how close the identified masses are to reference masses, because the groundtruth values of CoM positions cannot be obtained in realworld. 


Fig. 4: **Comparison of convergence performance between two-stage and one-stage methods.** The proposed Two-Stage method HALO (orange) demonstrates superior accuracy, converging significantly closer to the estimated reference values (red dashed lines) compared to the One-Stage baseline (blue). 


Fig. 5: **Experiment settings and results of scenario 1.** The metrics we defined are shown in the image, HALO outperforms the baselines across all metrics. 

The comparison of convergence performance between two-stage method (showing only the second stage) and onestage method is illustrated in Fig. (4). The final results are summarized in Table (IV). Compared to the one-stage method, the two-stage method demonstrates superior convergence accuracy, yielding mass estimates that are significantly closer to the reference values. This improvement suggests that our coarse-to-fine strategy effectively decouples global modeling errors from local payload variations. Furthermore, we will prove the effectiveness of the identified parameters by real-world downstream tasks as shown in Sec. (IV-E). 

TABLE IV: Summary of identified parameters. 

|**Method**|**Torso Mass (kg)**|**L-Hand Mass (kg)**|**R-Hand Mass (kg)**|
|---|---|---|---|
|Reference|13.82|2.25|2.25|
|One-Stage|12_._93_±_0_._32|3_._22_±_0_._23|3_._16_±_0_._44|
|**HALO**|**13**_._**83**_±_0_._43|**2**_._**13**_±_0_._07|**2**_._**71**_±_0_._29|


## _E. Real-World Validation Under Heavy Payload Conditions_ 

Based on the optimized robot model identified via the HALO framework, we evaluate the effectiveness of our approach across different real-world tasks. Consistent with Sec. (IV-C), we compare against two baseline methods, WDR and CM, on two scenarios: 

- **Scenario 1: Quantitative Analysis of Fundamental Locomotion.** 

- **Scenario 2: Evaluation of High-Agility Motion Tasks.** 

In Scenario 1, to evaluate sim-to-real consistency under heavy payload conditions, we benchmark our method on two locomotion tasks: bidirectional walking (forward-andbackward) and in-place 90° yaw jumping. To formally quantify the sim-to-real gap, we introduce three evaluation metrics: _Maximum Forward Position Error_ ( _Efpos_ , m), defined as the absolute discrepancy in forward displacement during the walking task; _End-point Residual Error_ ( _Eepos_ , m), representing the positional discrepancy at the final stopping state of the walking task; and _Angular Tracking Error_ ( _Eang_ , deg) for assessing orientation deviation during jumping maneuvers. Notably, the WDR baseline failed to initiate the takeoff phase during the jumping task, primarily due to the inability to manage the heavy payload dynamics; its angular deviation was thus recorded as a task failure. 

The experimental results are visualized in Fig. (5), with the corresponding numerical analysis summarized in Table (V). Compared to the baseline methods (WDR and CM), HALO significantly mitigates sim-to-real positional drift. Specifically, our approach reduces _Efpos_ by 73.33% and 45.45%, and decreases _Eepos_ by 70.79% and 42.22%, respectively. Furthermore, in the jumping task, HALO diminishes the angular tracking error _Eang_ by 72.97% compared to the CM baseline. These empirical results validate the efficacy of the HALO framework in enhancing the robustness and deployment fidelity of heavy-loaded humanoid systems in real-world environments. 

While all methods achieve comparable performance in simulation, WDR fails to generate sufficient vertical impulse in the real-world. CM partially completes the maneuver but exhibits significant orientation deviation. In contrast, HALO achieves the lowest angular error, demonstrating that accurate identification of inertial and actuation parameters is critical for transferring explosive whole-body maneuvers. 

TABLE V: Performance of Walking Forward and Backward. 

|**Method**|_Efpos_|_Eepos_|_Eang_|
|---|---|---|---|
|WDR|0_._45_±_ 0_._13|0_._89_±_ 0_._15|_N/A_|
|CM|0_._22_±_ 0_._09|0_._45_±_ 0_._13|41_._8_±_ 3_._6|
|**HALO**|**0**_._**12**_±_ 0_._03|**0**_._**26**_±_ 0_._07|**11**_._**3**_±_ 2_._1|


In Scenario 2, to assess the performance on high-agility tasks, we benchmark our method on three challenging maneuvers: **swallow balancing, side kicking, and roundhouse kicking** [36]. These tasks are characterized by complex whole-body coordination and substantial dynamic challenges to the robot’s equilibrium. Success is quantified by the deviation from the nominal trajectory; specifically, a trial is deemed successful if the robot executes the maneuver without significant divergence from the reference motion. Detailed experimental behaviors are provided in the supplementary videos. Our results (Table (VI)) indicate that the proposed method consistently outperforms baselines in terms of reliability. 

TABLE VI: Comparison of success rates for performing challenging maneuvers between HALO and baselines. 

|**Method**|**Swallow**|**Side Kicking**|**Roundhouse**|
|---|---|---|---|
||**Balancing**||**Kicking**|
|WDR|0_/_10|0_/_10|0_/_10|
|CM|5_/_10|7_/_10|5_/_10|
|**HALO**|**10**_/_**10**|**10**_/_**10**|**10**_/_**10**|


## V. CONCLUSIONS 

In this paper, we present HALO, a framework with twostage system identification based on differentiable simulation to address the significant sim-to-real gap for heavy-loaded humanoid robots. By leveraging analytical gradients from MuJoCo XLA, our approach achieves accurate and efficient estimation of robot physical parameters and payload mass distribution with only joint encoders, eliminating the need for expensive torque sensors or motion capture systems. The proposed two-stage optimization strategy achieves improved SysID accuracy, and enables robust sim-to-real transfer for heavy-loaded humanoid motion skills. 

## REFERENCES 

- [1] Filip Bjelonic, Fabian Tischhauser, and Marco Hutter. Towards bridging the gap: Systematic sim-to-real transfer for diverse legged robots. _arXiv preprint arXiv:2509.06342_ , 2025. 

- [2] Avinandan Bose, Simon Shaolei Du, and Maryam Fazel. Offline multi-task transfer rl with representational penalization. _arXiv preprint arXiv:2402.12570_ , 2024. 

- [3] Peter Yichen Chen, Chao Liu, Pingchuan Ma, John Eastman, Daniela Rus, Dylan Randle, Yuri Ivanov, and Wojciech Matusik. Learning object properties using robot proprioception via differentiable robotobject interaction. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5997–6004. IEEE, 2025. 

- [4] Nolan Fey, Gabriel B Margolis, Martin Peticco, and Pulkit Agrawal. Bridging the sim-to-real gap for athletic loco-manipulation. _arXiv preprint arXiv:2502.10894_ , 2025. 

- [5] C Daniel Freeman, Erik Frey, Anton Raichuk, Sertan Girgin, Igor Mordatch, and Olivier Bachem. Brax–a differentiable physics engine for large scale rigid body simulation. _arXiv preprint arXiv:2106.13281_ , 2021. 

- [6] Jinrui Han, Dewei Wang, Chenyun Zhang, Xinzhe Liu, Ping Luo, Chenjia Bai, and Xuelong Li. Husky: Humanoid skateboarding system via physics-aware whole-body control. _arXiv preprint arXiv:2602.03205_ , 2026. 

- [7] Jinrui Han, Weiji Xie, Jiakun Zheng, Jiyuan Shi, Weinan Zhang, Ting Xiao, and Chenjia Bai. Kungfubot2: Learning versatile motion skills for humanoid whole-body control. _arXiv preprint arXiv:2509.16638_ , 2025. 

- [8] F´elix G Harvey, Mike Yurick, Derek Nowrouzezahrai, and Christopher Pal. Robust motion in-betweening. _ACM Transactions on Graphics (TOG)_ , 39(4):60–1, 2020. 

- [9] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. _arXiv preprint arXiv:2502.01143_ , 2025. 

- [10] Eric Heiden, David Millard, Erwin Coumans, Yizhou Sheng, and Gaurav S Sukhatme. Neuralsim: Augmenting differentiable simulators with neural networks. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9474–9481. IEEE, 2021. 

- [11] Jemin Hwangbo, Joonho Lee, Alexey Dosovitskiy, Dario Bellicoso, Vassilios Tsounis, Vladlen Koltun, and Marco Hutter. Learning agile and dynamic motor skills for legged robots. _Science robotics_ , 4(26):eaau5872, 2019. 

- [12] Jipeng Kong, Xinzhe Liu, Yuhang Lin, Jinrui Han, S¨oren Schwertfeger, Chenjia Bai, and Xuelong Li. Learning soccer skills for humanoid robots: A progressive perception-action framework, 2026. 

- [13] Vyacheslav Kovalev, Ekaterina Chaikovskaia, Egor Davydenko, and Roman Gorbachev. Achieving precise and reliable locomotion with differentiable simulation-based system identification. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 4767–4772. IEEE, 2025. 

- [14] Ashish Kumar, Zhongyu Li, Jun Zeng, Deepak Pathak, Koushil Sreenath, and Jitendra Malik. Adapting rapid motor adaptation for bipedal robots. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1161–1168. IEEE, 2022. 

- [15] Junyoung Lee, Pyung Hun Chang, Byeonggi Yu, and Maolin Jin. An adaptive pid control for robot manipulators under substantial payload variations. _IEEE Access_ , 8:162261–162270, 2020. 

- [16] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [17] Antonio Loquercio, Elia Kaufmann, Ren´e Ranftl, Alexey Dosovitskiy, Vladlen Koltun, and Davide Scaramuzza. Deep drone racing: From simulation to reality with domain randomization. _IEEE Transactions on Robotics_ , 36(1):1–14, 2019. 

- [18] Naureen Mahmood, Nima Ghorbani, Nikolaus F Troje, Gerard PonsMoll, and Michael J Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 5442–5451, 2019. 

- [19] Gabriel B Margolis, Xiang Fu, Yandong Ji, and Pulkit Agrawal. Learning to see physical properties with active sensing motor policies. _arXiv preprint arXiv:2311.01405_ , 2023. 

- [20] Bhairav Mehta, Manfred Diaz, Florian Golemo, Christopher J Pal, and Liam Paull. Active domain randomization. In _Conference on Robot Learning_ , pages 1162–1176. PMLR, 2020. 

- [21] Melissa Mozian, Juan Camilo Gamboa Higuera, David Meger, and Gregory Dudek. Learning domain randomization distributions for training robust locomotion policies. In _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 6112– 6117. IEEE, 2020. 

- [22] Jiahe Pan, Jiaxu Xing, Rudolf Reiter, Yifan Zhai, Elie Aljalbout, and Davide Scaramuzza. Learning on the fly: Rapid policy adaptation via differentiable simulation. _IEEE Robotics and Automation Letters_ , 2026. 

- [23] Xue Bin Peng, Marcin Andrychowicz, Wojciech Zaremba, and Pieter Abbeel. Sim-to-real transfer of robotic control with dynamics randomization. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pages 3803–3810. IEEE, 2018. 

- [24] Lerrel Pinto, James Davidson, Rahul Sukthankar, and Abhinav Gupta. Robust adversarial reinforcement learning. In _International conference on machine learning_ , pages 2817–2826. PMLR, 2017. 

- [25] Haozhi Qi, Ashish Kumar, Roberto Calandra, Yi Ma, and Jitendra Malik. In-hand object rotation via rapid motor adaptation. In _Conference on Robot Learning_ , pages 1722–1732. PMLR, 2023. 

- [26] Lu Shi, Yuxuan Xu, Shiyu Wang, Jinhao Huang, Wenhao Zhao, Yufei Jia, Zike Yan, Weibin Gu, and Guyue Zhou. An real-sim-real (rsr) loop framework for generalizable robotic policy transfer with differentiable simulation. _arXiv preprint arXiv:2503.10118_ , 2025. 

- [27] Laura Smith, J Chase Kew, Xue Bin Peng, Sehoon Ha, Jie Tan, and Sergey Levine. Legged robots that keep on learning: Fine-tuning locomotion policies in the real world. In _2022 international conference on robotics and automation (ICRA)_ , pages 1593–1599. IEEE, 2022. 

- [28] Nikhil Sobanbabu, Guanqi He, Tairan He, Yuxiang Yang, and Guanya Shi. Sampling-based system identification with active exploration for legged robot sim2real learning. _arXiv preprint arXiv:2505.14266_ , 2025. 

- [29] Nitish Sontakke, Hosik Chae, Sangjoon Lee, Tianle Huang, Dennis W Hong, and Sehoon Hal. Residual physics learning and system identification for sim-to-real transfer of policies on buoyancy assisted legged robots. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 392–399. IEEE, 2023. 

- [30] Jie Tan, Tingnan Zhang, Erwin Coumans, Atil Iscen, Yunfei Bai, Danijar Hafner, Steven Bohez, and Vincent Vanhoucke. Sim-toreal: Learning agile locomotion for quadruped robots. _arXiv preprint arXiv:1804.10332_ , 2018. 

- [31] Josh Tobin, Rachel Fong, Alex Ray, Jonas Schneider, Wojciech Zaremba, and Pieter Abbeel. Domain randomization for transferring deep neural networks from simulation to the real world. In _2017 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ , pages 23–30. IEEE, 2017. 

- [32] Peilin Wu, Weiji Xie, Jiahang Cao, Hang Lai, and Weinan Zhang. Loopsr: Looping sim-and-real for lifelong policy adaptation of legged robots. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 5649–5656. IEEE, 2025. 

- [33] Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. Kungfubot: Physicsbased humanoid whole-body control for learning highly-dynamic skills. _arXiv preprint arXiv:2506.12851_ , 2025. 

- [34] Kevin Zakka, Qiayuan Liao, Brent Yi, Louis Le Lay, Koushil Sreenath, and Pieter Abbeel. mjlab: A lightweight framework for gpuaccelerated robot learning, 2026. 

- [35] Kevin Zakka, Baruch Tabanpour, Qiayuan Liao, Mustafa Haiderbhai, Samuel Holt, Jing Yuan Luo, Arthur Allshire, Erik Frey, Koushil Sreenath, Lueder A Kahrs, et al. Mujoco playground. _arXiv preprint arXiv:2502.08844_ , 2025. 

- [36] Tong Zhang, Boyuan Zheng, Ruiqian Nai, Yingdong Hu, Yen-Jen Wang, Geng Chen, Fanqi Lin, Jiongye Li, Chuye Hong, Koushil Sreenath, et al. Hub: Learning extreme humanoid balance. _arXiv preprint arXiv:2505.07294_ , 2025. 

