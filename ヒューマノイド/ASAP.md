---
title: "ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills"
date: "2025-02-03"
authors: "Tairan He; Jiawei Gao; Wenli Xiao; Yuanhang Zhang; Zi Wang; Jiashun Wang"
venue: "RSS 2025"
url: https://arxiv.org/abs/2502.01143
pdf: https://arxiv.org/pdf/2502.01143
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2502.01143)** / [論文ページ](https://arxiv.org/abs/2502.01143)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills 

Tairan He<sup>†1,2</sup> Jiawei Gao<sup>†1</sup> Wenli Xiao<sup>†1,2</sup> Yuanhang Zhang<sup>†1</sup> Zi Wang<sup>1</sup> Jiashun Wang<sup>1</sup> Zhengyi Luo<sup>1,2</sup> Guanqi He<sup>1</sup> Nikhil Sobanbabu<sup>1</sup> Chaoyi Pan<sup>1</sup> Zeji Yi<sup>1</sup> Guannan Qu<sup>1</sup> Kris Kitani<sup>1</sup> Jessica Hodgins<sup>1</sup> Linxi “Jim” Fan<sup>2</sup> Yuke Zhu<sup>2</sup> Changliu Liu<sup>1</sup> Guanya Shi<sup>1</sup> 1Carnegie Mellon University 2NVIDIA †Equal Contributions Page: https://agile.human2humanoid.com Code: https://github.com/LeCAR-Lab/ASAP 


Fig. 1. The humanoid robot (Unitree G1) demonstrates diverse agile whole-body skills, showcasing the control policies’ agility: (a) Cristiano Ronaldo’s signature celebration involving a jump with a 180-degree mid-air rotation; (b) LeBron James’s “Silencer” celebration involving single-leg balancing; and (c) Kobe Bryant’s famous fadeaway jump shot involving single-leg jumping and landing; (d) 1.5m-forward jumping; (e) Leg stretching; (f) 1.3m-side jumping. 

**_Abstract_ — Humanoid robots hold the potential for unparalleled versatility for performing human-like, whole-body skills. However, achieving agile and coordinated whole-body motions remains a significant challenge due to the dynamics mismatch between simulation and the real world. Existing approaches, such as system identification (SysID) and domain randomization (DR) methods, often rely on labor-intensive parameter tuning** 

**or result in overly conservative policies that sacrifice agility. In this paper, we present ASAP (Aligning Simulation and Real Physics), a two-stage framework designed to tackle the dynamics mismatch and enable agile humanoid whole-body skills. In the first stage, we pre-train motion tracking policies in simulation using retargeted human motion data. In the second stage, we deploy the policies in the real world and collect real-world data** 


Fig. 2. Overview of ASAP. (a) **Motion Tracking Pre-training and Real Trajectory Collection** : With the humanoid motions retargeted from human videos, we pre-train multiple motion tracking policies to roll out real-world trajectories. (b) **Delta Action Model Training** : Based on the real-world rollout data, we train the delta action model by minimizing the discrepancy between simulation state _st_ and real-world state _s_<sup>_r_</sup> _t_<sup>.(c)</sup><sup>**PolicyFine-tuning**:Wefreezethe</sup> delta action model, incorporate it into the simulator to align the real-world physics and then fine-tune the pre-trained motion tracking policy. (d) **Real-World Deployment** : Finally, we deploy the fine-tuned policy directly in the real world without delta action model. 

**to train a delta (residual) action model that compensates for the dynamics mismatch. Then ASAP fine-tunes pre-trained policies with the delta action model integrated into the simulator to align effectively with real-world dynamics. We evaluate ASAP across three transfer scenarios—IsaacGym to IsaacSim, IsaacGym to Genesis, and IsaacGym to the real-world Unitree G1 humanoid robot. Our approach significantly improves agility and wholebody coordination across various dynamic motions, reducing tracking error compared to SysID, DR, and delta dynamics learning baselines. ASAP enables highly agile motions that were previously difficult to achieve, demonstrating the potential of delta action learning in bridging simulation and real-world dynamics. These results suggest a promising sim-to-real direction for developing more expressive and agile humanoids.** 

## I. INTRODUCTION 

For decades, we have envisioned humanoid robots achieving or even surpassing human-level agility. However, most prior work [46, 74, 47, 73, 107, 19, 95, 50] has primarily focused on locomotion, treating the legs as a means of mobility. Recent studies [10, 25, 24, 26, 32] have introduced wholebody expressiveness in humanoid robots, but these efforts have primarily focused on upper-body motions and have yet to achieve the agility seen in human movement. Achieving agile, whole-body skills in humanoid robots remains a fundamental challenge due to not only hardware limits but also the mismatch between simulated dynamics and real-world physics. 

Three main approaches have emerged to bridge the dynamics mismatch: System Identification (SysID) methods, domain randomization (DR), and learned dynamics methods. SysID methods directly estimate critical physical parameters, such as motor response characteristics, the mass of each robot link, and terrain properties [102, 19]. However, these methods require a pre-defined parameter space [49], which may not fully capture 

the sim-to-real gap, especially when real-world dynamics fall outside the modeled distribution. SysID also often relies on ground truth torque measurements [29], which are unavailable on many widely used hardware platforms, limiting its practical applicability. DR methods, in contrast, first train control policies in simulation before deploying them on real-world hardwares [85, 79, 59]. To mitigate the dynamics mismatch between simulation and real-world physics, DR methods rely on randomizing simulation parameters [87, 68]; but this can lead to overly conservative policies [25], ultimately hindering the development of highly agile skills. Another approach to bridge dynamics mismatch is learning a dynamics model of real-world physics using real-world data. While this approach has demonstrated success in low-dimensional systems such as drones [81] and ground vehicles [97], its effectiveness for humanoid robots remains unexplored. 

To this end, we propose ASAP, a two-stage framework that aligns the dynamics mismatch between simulation and realworld physics, enabling agile humanoid whole-body skills. ASAP involves a pre-training stage where we train base policies in simulation and a post-training stage that finetunes the policy by aligning simulation and real-world dynamics. In the **pre-training** stage, we train a motion tracking policy in simulation using human motion videos as data sources. These motions are first retargeted to humanoid robots [25], and a phase-conditioned motion tracking policy [67] is trained to follow the retargeted movements. However, directly deploying this policy on real hardware results in degraded performance due to the dynamics mismatch. To address this, the **posttraining** stage collects real-world rollout data, including proprioceptive states and positions recorded by the motion capture 


Fig. 3. Retargeting Human Video Motions to Robot Motions: (a) Human motions are captured from video. (b) Using TRAM [93], 3D human motion is reconstructed in the SMPL parameter format. (c) A reinforcement learning (RL) policy is trained in simulation to track the SMPL motion. (d) The learned SMPL motion is retargeted to the Unitree G1 humanoid robot in simulation. (e) The trained RL policy is deployed on the real robot, executing the final motion in the physical world. This pipeline ensures the retargeted motions remain physically feasible and suitable for real-world deployment. 

system. The collected data are then replayed in simulation, where the dynamics mismatch manifests as tracking errors. We then train a delta action model that learns to compensate for these discrepancies by minimizing the difference between real-world and simulated states. This model effectively serves as a residual correction term for the dynamics gap. Finally, we fine-tune the pre-trained policy using the delta action model, allowing it to adapt effectively to real-world physics. 

We validate ASAP on diverse agile motions and successfully achieve whole-body agility on the Unitree G1 humanoid robot [77]. Our approach significantly reduces motion tracking error compared to prior SysID, DR, and delta dynamics learning baselines in both sim-to-sim (IsaacGym to IsaacSim, IsaacGym to Genesis) and sim-to-real (IsaacGym to Real) transfer scenarios. Our contributions are summarized below. 

- 1) We introduce ASAP, a framework that bridges the simto-real gap by leveraging a delta action model trained via reinforcement learning (RL) with real-world data. 

- 2) We successfully deploy RL-based whole-body control policies in the real world, achieving previously difficultto-achieve humanoid motions. 

- 3) Extensive experiments in both simulation and real-world settings demonstrate that ASAP effectively reduces dynamics mismatch, enabling highly agile motions on robots and significantly reducing motion tracking errors. 

- 4) To facilitate smooth transfer between simulators, we develop and open-source a multi-simulator training and evaluation codebase for help accelerate further research. 

## II. PRE-TRAINING: LEARNING AGILE HUMANOID SKILLS 

## _A. Data Generation: Retargeting Human Video Data_ 

To track expressive and agile motions, we collect a video dataset of human movements and retarget it to robot motions, creating imitation goals for motion-tracking policies, as shown in Figure 3 and Figure 2 (a). 

_a) Transforming Human Video to SMPL Motions:_ We begin by recording videos (see Figure 3 (a) and Figure 12) of humans performing expressive and agile motions. Using TRAM [93], we reconstruct 3D motions from videos. TRAM estimates the global trajectory of the human motions in SMPL parameter format [52], which includes global root translation, orientation, body poses, and shape parameters, as shown in Figure 3 (b). The resulting motions are denoted as _D_ SMPL. 

_b) Simulation-based Data Cleaning:_ Since the reconstruction process can introduce noise and errors [25], some estimated motions may not be physically feasible, making them unsuitable for motion tracking in the real world. To address this, we employ a “sim-to-data” cleaning procedure. Specifically, we use MaskedMimic [86], a physics-based motion tracker, to imitate the SMPL motions from TRAM in IsaacGym simulator [58]. The motions (Figure 3 (c)) that pass this simulation-based validation are saved as the cleaned dataset _D_ SMPL<sup>Cleaned.</sup> 

_c) Retargeting SMPL Motions to Robot Motions:_ With the cleaned dataset _D_ SMPL<sup>Cleaned</sup> in SMPL format, we retarget the motions into robot motions following the shape-and-motion two-stage retargeting process [25]. Since the SMPL parameters estimated by TRAM represent various human body shapes, we first optimize the shape parameter **_β_**<sup>_′_</sup> to approximate a humanoid shape. By selecting 12 body links with correspondences between humans and humanoids, we perform gradient descent on **_β_**<sup>_′_</sup> to minimize joint distances in the rest pose. Using the optimized shape **_β_**<sup>_′_</sup> along with the original translation **_p_** and pose **_θ_** , we apply gradient descent to further minimize the distances of the body links. This process ensures accurate motion retargeting and produces the cleaned robot trajectory dataset _D_ Robot<sup>Cleaned,asshowninFigure3(d).</sup> 

## _B. Phase-based Motion Tracking Policy Training_ 

We formulate the motion-tracking problem as a goalconditioned reinforcement learning (RL) task, where the policy _π_ is trained to track the retargeted robot movement trajectories in the dataset _D_ Robot<sup>Cleaned.Inspiredby</sup> [67], the state _st_ includes the robot’s proprioception _s_<sup>p</sup> _t_<sup>and a time phase variable</sup> _ϕ ∈_ [0 _,_ 1], where _ϕ_ = 0 represents the start of a motion and _ϕ_ = 1 represents the end. This time phase variable alone _ϕ_ is proven to be sufficient to serve as the goal state **_s_**<sup>g</sup> _t_<sup>for</sup> single-motion tracking [67]. The proprioception _s_<sup>p</sup> _t_<sup>isdefined</sup> as _s_<sup>p</sup> _t_<sup>≜</sup> � **_q_** _t−_ 4: _t,_ **_q_ ˙** _t−_ 4: _t,_ **_ω_**<sup>_root_</sup> _t−_ 4: _t_<sup>_,_</sup><sup>**_g_**</sup> _t−_ 4: _t_<sup>_,_</sup><sup>**_a_**</sup><sup>_t−_5:</sup><sup>_t−_1</sup> �, with 5-step history of joint position **_q_** _t ∈_ R<sup>23</sup> , joint velocity **_q_ ˙** _t ∈_ R<sup>23</sup> , root angular velocity **_ω_**<sup>_root_</sup> _t ∈_ R<sup>3</sup> , root projected gravity **_g_** _t ∈_ R<sup>3</sup> , and last action **_a_** _t−_ 1 _∈_ R<sup>23</sup> . Using the agent’s proprioception _s_<sup>p</sup> _t_<sup>andthegoalstate</sup><sup>**_s_**g</sup> _t_<sup>,wedefinetherewardas</sup><sup>_rt_=</sup> _R_ ( _s_<sup>p</sup> _t_<sup>_, s_g</sup> _t_<sup>), which is used for policy optimization. The specific</sup> reward terms can be found in Table I. The action **_a_** _t ∈_ R<sup>23</sup> corresponds to the target joint positions and is passed to a 

PD controller that actuates the robot’s degrees of freedom. To optimize the policy, we use the proximal policy optimization (PPO) [80], aiming to maximize the cumulative discounted reward E _t_ =1<sup>_γt−_1</sup><sup>_rt_</sup> . We identify several design choices �� _T_ � that are crucial for achieving stable policy training: 

_a) Asymmetric Actor-Critic Training:_ Real-world humanoid control is inherently a partially observable Markov decision process (POMDP), where certain task-relevant properties that are readily available in simulation become unobservable in real-world scenarios. However, these missing properties can significantly facilitate policy training in simulation. To bridge this gap, we employ an asymmetric actorcritic framework, where the critic network has access to privileged information such as the global positions of the reference motion and the root linear velocity, while the actor network relies solely on proprioceptive inputs and a time-phase variable. This design not only enhances phase-based motion tracking during training but also enables a simple, phasedriven motion goal for sim-to-real transfer. Crucially, because the actor does not depend on position-based motion targets, our approach eliminates the need for odometry during realworld deployment—overcoming a well-documented challenge in prior work on humanoid robots [25, 24]. 

_b) Termination Curriculum of Tracking Tolerance:_ Training a policy to track agile motions in simulation is challenging, as certain motions can be too difficult for the policy to learn effectively. For instance, when imitating a jumping motion, the policy often fails early in training and learns to remain on the ground to avoid landing penalties. To mitigate this issue, we introduce a termination curriculum that progressively refines the motion error tolerance throughout training, guiding the policy toward improved tracking performance. Initially, we set a generous termination threshold of 1.5m, meaning the episode terminates if the robot deviates from the reference motion by this margin. As training progresses, we gradually tighten this threshold to 0.3m, incrementally increasing the tracking demand on the policy. This curriculum allows the policy to first develop basic balancing skills before progressively enforcing stricter motion tracking, ultimately enabling successful execution of high-dynamic behaviors. 

_c) Reference State Initialization:_ Task initialization plays a crucial role in RL training. We find that naively initializing episodes at the start of the reference motion leads to policy failure. For example, in Cristiano Ronaldo’s jumping training, starting the episode from the beginning forces the policy to learn sequentially. However, a successful backflip requires mastering the landing first—if the policy cannot land correctly, it will struggle to complete the full motion from takeoff. To address this, we adopt the Reference State Initialization (RSI) framework [67]. Specifically, we randomly sample timephase variables between 0 and 1, which effectively randomizes the starting point of the reference motion for the policy to track. We then initialize the robot’s state based on the corresponding reference motion at that phase, including root position and orientation, root linear and angular velocities 

and joint positions and velocities. This initialization strategy significantly improves motion tracking training, particularly for agile whole-body motions, by allowing the policy to learn different motion phases in parallel rather than being constrained to a strictly sequential learning process. 

_d) Reward Terms:_ We define the reward function _rt_ with the sum of three terms: 1) penalty, 2) regularization, and 3) task rewards. A detailed summary of these components is provided in Table I. 

TABLE I 

REWARD TERMS FOR PRETRAINING 

|Term|Weight<br>Term|Weight|
|---|---|---|
||Penalty||
|DoF position limits<br>Torque limits|_−_10_._0<br>DoF velocity limits<br>_−_5_._0<br>Termination|_−_5_._0<br>_−_200_._0|
||Regularization||
|Torques<br>|_−_1_×_10<sup>_−_6</sup><br>Action rate|_−_0_._5|
|Feet orientation<br>Slippage|_−_2_._0<br>Feet heading<br>_−_1_._0|_−_0_._1|
||Task Reward||
|Body position|1_._0<br>VR 3-point|1_._6|
|Body position (feet)|2_._1<br>Body rotation|0_._5|
|Body angular velocity|0_._5<br>Body velocity|0_._5|
|DoF position|0_._75<br>DoF velocity|0_._5|


_e) Domain Randomizations:_ To improve the robustness of the pre-trained policy in Figure 2 (a), we utilized basic domain randomization techniques listed in Table VI. 

III. POST-TRAINING: TRAINING DELTA ACTION MODEL AND FINE-TUNING MOTION TRACKING POLICY 

The policy trained in the first stage can track the reference motion in the real-world but does not achieve high motion quality. Thus, during the second stage, as shown in Figure 2 (b) and (c), we leverage real-world data rolled out by the pre-trained policy to train a delta action model, followed by policy refinement through dynamics compensation using this learned delta action model. 

## _A. Data Collection_ 

We deploy the pretrained policy in the real world to perform whole-body motion tracking tasks (as depicted in Figure 9) and record the resulting trajectories, denoted as _D_<sup>r</sup> = _{s_<sup>r</sup> 0<sup>_, a_r</sup> 0<sup>_, . . . , s_r</sup> _T_<sup>_, a_r</sup> _T_<sup>_}_,asillustratedinFigure2(a).Ateach</sup> timestep _t_ , we use a motion capture device and onboard sensors to record the state: _st_ = [ _p_<sup>base</sup> _t , vt_<sup>base</sup> _, αt_<sup>base</sup> _, ωt_<sup>base</sup> _, qt, q_ ˙ _t_ ] _,_ where _p_<sup>base</sup> _t ∈_ R<sup>3</sup> represents the robot base 3D position, _vt_<sup>base</sup> _∈_ R<sup>3</sup> is base linear velocity, _αt_<sup>base</sup> _∈_ R<sup>4</sup> is the robot base orientation represented as a quaternion, _ωt_<sup>base</sup> _∈_ R<sup>3</sup> is the base angular velocity, _qt ∈_ R<sup>23</sup> is the vector of joint positions, and _q_ ˙ _t ∈_ R<sup>23</sup> represents joint velocities. 

## _B. Training Delta Action Model_ 

Due to the sim-to-real gap, when we replay the real-world trajectories in simulation, the resulting simulated trajectory will likely deviate significantly from real-world recorded trajectories. This discrepancy is a valuable learning signal for learning the mismatch between simulation and real-world 


Fig. 4. Baselines of ASAP. (a) Model-free RL training. (b) System ID from real to sim using real-world data. (c) Learning delta dynamics model using real-world data. (d) Our proposed method, learning delta action model using real-world data. 

physics. We leverage an RL-based delta/residual action model to compensate for the sim-to-real physics gap. 

As illustrated in Figure 2 (b), the delta action model is defined as ∆ _at_ = _πθ_<sup>∆(</sup><sup>_st, at_),wherethepolicy</sup><sup>_π_</sup> _θ_<sup>∆</sup> learns to output corrective actions based on the current state _st_ and the action _at_ . These corrective actions (∆ _at_ ) are added to the real-world recorded actions ( _a_<sup>_r_</sup> _t_<sup>)toaccountfordiscrepancies</sup> between simulation and real-world dynamics. 

The RL environment incorporates this delta action model by modifying the simulator dynamics as follows: _st_ +1 = _f_<sup>sim</sup> ( _st, a_<sup>_r_</sup> _t_<sup>+ ∆</sup><sup>_at_)where</sup><sup>_f_simrepresentsthesimulator’sdy-</sup> namics, _a_<sup>_r_</sup> _t_<sup>isthereferenceactionrecordedfromreal-world</sup> rollouts, and ∆ _at_ introduces corrections learned by the delta action model. 

TABLE II 

_C. Fine-tuning Motion Tracking Policy under New Dynamics_ 

With the learned delta action model _π_<sup>∆</sup> ( _st, at_ ), we can reconstruct the simulation environment with 

_st_ +1 = _f_<sup>ASAP</sup> ( _st, at_ ) = _f_<sup>sim</sup> ( _st, at_ + _π_<sup>∆</sup> ( _st, at_ )) _,_ 

As shown in Figure 2 (c), we keep the _π_<sup>∆</sup> model parameters frozen, and fine-tune the pretrained policy with the same reward summarized in Table I. 

## _D. Policy Deployment_ 

Finally, we deploy the fine-tuned policy without delta action model in the real world as shown in Figure 2 (d). The fine-tuned policy shows enhanced real-world motion tracking performance compared to the pre-trained policy. Quantitative improvements will be discussed in Section IV. 

REWARD TERMS FOR DELTA ACTION LEARNING 

|Term|Weight<br>Term|Weight|
|---|---|---|
||Penalty||
|DoF position limits<br>Torque limits|_−_10_._0 DoF velocity limits<br>_−_0_._1<br>Termination|_−_5_._0<br>_−_200_._0|
||Regularization||
|Action rate|_−_0_._01<br>Action norm|_−_0_._2|
||Task Reward||
|Body position|1_._0<br>VR 3-point|1_._0|
|Body position (feet)|1_._0<br>Body rotation|0_._5|
|Body angular velocity|0_._5<br>Body velocity|0_._5|
|DoF position|0_._5<br>DoF velocity|0_._5|


## During each RL step: 

- 1) The robot is initialized at the real-world state _s_<sup>_r_</sup> _t_<sup>.</sup> 

- 2) A reward signal is computed to minimize the discrepancy between the simulated state _st_ +1 and the recorded real-world state _s_<sup>_r_</sup> _t_ +1<sup>,withanadditionalactionmagni-</sup> tude regularization term exp( _−∥at∥_ ) _−_ 1), as specified in Table II. The workflow is illustrated in Figure 2 (b). 

- 3) PPO is used to train the delta action policy _πθ_<sup>∆, learning</sup> corrected ∆ _at_ to match simulation and the real world. 

By learning the delta action model, the simulator can accurately reproduce real-world failures. For example, consider a scenario where the simulated robot can jump because its motor strength is overestimated, but the real-world robot cannot jump due to weaker motors. The delta action model _πθ_<sup>∆willlearn</sup> to reduce the intensity of lower-body actions, simulating the motor limitations of the real-world robot. This allows the simulator to replicate the real-world dynamics and enables the policy to be fine-tuned to handle these limitations effectively. 

IV. PERFORMANCE EVALUATION OF ASAP 

In this section, we present extensive experimental results on three policy transfers: IsaacGym [58] to IsaacSim [63], IsaacGym to Genesis [6], and IsaacGym to real-world Unitree G1 humanoid robot. Our experiments aim to address the following key questions: 

- **Q1** : Can ASAP outperform other baseline methods to compensate for the dynamics mismatch? 

- **Q2** : Can ASAP finetune policy to outperform SysID and Delta Dynamics methods? 

- **Q3** : Does ASAP work for sim-to-real transfer? 

**Experiments Setup.** To address these questions, we evaluate ASAP on motion tracking tasks in both simulation (Section IV-A and Section IV-B) and real-world settings (Section IV-C). 

In the simulation, we use the retargeted motion dataset from the videos we shoot, denoted as _D_ Robot<sup>Cleaned,whichcon-</sup> tains diverse human motion sequences. We select 43 motions categorized into three difficulty levels: easy, medium, and hard (as partially visualized in Figure 6), based on motion complexity and the required agility. ASAP is evaluated through simulation-to-simulation transfer by training policies in IsaacGym and using two other simulators, IsaacSim and Genesis, as a proxy of “real-world” environments. This setup allows for a systematic evaluation of ASAP’s generalization and transferability. The success of the transfer is assessed by metrics described in subsequent sections. 

For real-world evaluation, we deploy ASAP on Unitree G1 robot with fixed wrists to track motion sequences that has obvious sim-to-real gap. These sequences are chosen to 


Fig. 5. Replaying IsaacSim State-Action trajecories in IsaacGym. The upper four panels visualize the Unitree G1 humanoid executing a soccer-shooting motion under four distinct open-loop actions. Corresponding metric curves (bottom) quantify tracking performance. Importantly, our delta action model (ASAP) is trained across multiple motions and is not overfitted to this specific example. 

capture a broad range of motor capabilities and demonstrate the sim-to-real capability for agile whole-body control. 

**Baselines.** We have the following baselines: 

Oracle: This baseline is trained and evaluated entirely within IsaacGym. It assumes perfect alignment between the training and testing environments, serving as an upper bound for performance in simulation. 

Vanilla (Figure 4 a): The RL policy is trained in IsaacGym and evaluated in IsaacSim, Genesis, or the real world. 

SysID (Figure 4 b): We identify the following representative parameters in our simulated model that best align the ones in the real world: base center of mass (CoM) shift ( _cx, cy, cz_ ), base link mass offset ratio _km_ and low-level PD gain ratios ( _kp_<sup>_i, k_</sup> _d_<sup>_i_)where</sup><sup>_i_=1</sup><sup>_,_2</sup><sup>_, ...,_23.Specifically,wesearchthe</sup> best parameters among certain discrete ranges by replaying the recorded trajectories in real with different simulation parameters summarized in Table VII. We then finetune the pretrained policy in IsaacGym with the best SysID parameters. 

DeltaDynamics (Figure 4 c): We train a residual dynamics model _fθ_<sup>∆(</sup><sup>_st, at_)tocapturethediscrepancybetween</sup> simulated and real-world physics. The detailed implementation is introduced in Section VIII-C 

**Metrics.** We report success rate, deeming imitation unsuccessful when, at any point during imitation, the average difference in body distance is on average further than 0.5m. We evaluate policy’s ability to imitate the reference motion by comparing the tracking error of the global body position _E_ g-mpjpe (mm), the root-relative mean per-joint (MPJPE) _E_ mpjpe 

TABLE III OPEN-LOOP PERFORMANCE COMPARISON ACROSS SIMULATORS AND MOTION LENGTHS. 

|Simul|ator & Length||IsaacSi|m|||Genesi|s|
|---|---|---|---|---|---|---|---|---|
|Length|Method|_E_g-mpjpe|_E_mpjpe|Eacc|Evel|_E_g-mpjpe|_E_mpjpe|Eacc Evel|
||OpenLoop<br>|**19.5**<br>|15.1<br>|**6.44 **<br>|**5.80**<br>|19.8<br>|15.3<br>|6.53 5.88<br>|
|025s|SysID<br>|**19.4**<br>|15.0<br>|**6.43 **<br>|**5.74**<br>|19.3<br>|15.0<br>|6.42 5.73<br>|
|.|DeltaDynamics|24.4<br>|**13.6**<br>|9.43 <br>|7.85<br>|20.0<br>|**12.4**|8.42 6.89<br>|
||ASAP|**19.9**|15.6|**6.48 **|**5.86**|**19.0**|14.9|**6.19 5.59**|
||OpenLoop<br>|33.3<br>|23.2<br>|6.80 <br>|6.84<br>|33.1<br>|23.0<br>|6.78 6.82<br>|
|05s|SysID<br>|32.1<br>|22.2<br>|6.57 <br>|6.56<br>|32.2<br>|22.3<br>|6.57 6.57<br>|
|.|DeltaDynamics<br>|36.5<br>|**16.4**<br>|8.89 <br>|7.98<br>|27.8<br>|**14.0**<br>|7.63 6.74<br>|
||ASAP|**26.8**|19.2|**5.09 **|**5.36**|**25.9**|18.4|**4.93 5.19**|
||OpenLoop|80.8|43.5|10.6|11.1|82.5|44.5|10.8 11.4|
|10s|SysID|77.6|41.5|10.2|10.7|76.5|41.6|10.0 10.5|
|.|DeltaDynamics|68.1|**21.5**|9.61|9.14|50.2|**17.2**|8.19 7.62|
||ASAP|**37.9**|22.9|**4.38 **|**5.26**|**36.9**|22.6|**4.23 5.10**|


(mm), acceleration error _E_ acc (mm/frame<sup>2</sup> ), and root velocity _E_ vel (mm/frame). The mean values of the metrics are computed across all motion sequences used. 

## _A. Comparison of Dynamics Matching Capability_ 

To address **Q1** ( _Can ASAP outperform other baseline methods to compensate for the dynamics mismatch?_ ), we establish sim-to-sim transfer benchmarks to assess the effectiveness of different methods in bridging the dynamics gap. IsaacGym serves as the _training environment_ , while IsaacSim and Genesis function as _testing environments_ . The primary objective is to evaluate the generalization capability of each approach when exposed to new dynamics conditions. _Open-loop_ evaluation measures how accurately a method can reproduce testing- 

TABLE IV 

CLOSED-LOOP MOTION IMITATION EVALUATION ACROSS DIFFERENT SIMULATORS. ALL VARIANTS ARE TRAINED WITH IDENTICAL REWARDS. 

||Test Environment|||IsaacSim|||||Genesis|||
|---|---|---|---|---|---|---|---|---|---|---|---|
|Level|Method|Succ_↑_|_E_g-mpjpe _↓_|_E_mpjpe _↓_|Eacc _↓_|Evel _↓_|Succ_↑_|_E_g-mpjpe _↓_|_E_mpjpe _↓_|Eacc _↓_|Evel _↓_|
||Oracle (IsaacGym _→_IsaacGym)|100%_±_0.000%|97.5_±_0.605|43.2_±_0.112|2.56_±_0.024|4.48_±_0.023|100%_±_0.000%|97.5_±_0.605|43.2_±_0.112|2.56_±_0.024|4.48_±_0.023|
|Easy|Vanilla (IsaacGym _→_TestEnv)<br>SysID<br>DeltaDynamics<br>ASAP|100%_±_0.000% <br>100%_±_0.000%<br>100%_±_0.000%<br>100%_±_0.000%|**107** _±_0.578 <br>**105** _±_1.35<br>127_±_2.97<br> **106** _±_0.498|45.4_±_0.169<br>47.8_±_0.970<br>56.7_±_0.390<br> **44.3** _±_0.103|2.83_±_0.012<br>3.09_±_0.011<br>3.50_±_0.028<br> **2.74** _±_0.025|4.59_±_0.021 <br>4.98_±_0.020 <br>5.56_±_0.031 <br> **4.46** _±_0.020|100%_±_0.000%<br> 100%_±_0.000%<br> 83.3%_±_0.000%<br> 100%_±_0.000%|140_±_1.85<br>**127**_±_0.233 <br>168_±_7.62<br>**125**_±_4.75|**70.1**_±_0.626 <br> 79.9_±_0.330 <br>87.0_±_1.51<br>73.5_±_0.570|2.68_±_0.042 <br> 2.99_±_0.035 <br>3.08_±_0.18<br> **2.10**_±_0.083|4.65_±_0.046<br> 4.95_±_0.012<br>5.39_±_0.34<br> **4.11**_±_0.133|
||Oracle (IsaacGym _→_IsaacGym)|100%_±_0.000%|111_±_0.635|48.8_±_0.133|2.63_±_0.017|4.82_±_0.019|100%_±_0.000%|111_±_0.635|48.8_±_0.133|2.63_±_0.017|4.82_±_0.019|
|Medium|Vanilla (IsaacGym _→_TestEnv)<br> <sup>SysID</sup><br>DeltaDynamics<br>ASAP|100%_±_0.000%<br>100%_±_0.000%<br>83.3%_±_0.000%<br>100%_±_0.000%|**114**_±_0.720<br>**115**_±_1.256<br>151_±_2.62<br> **112** _±_1.648|**49.2**_±_0.104<br>**49.1**_±_0.560<br>68.0_±_0.364<br> **49.3** _±_0.574|2.92_±_0.021<br>3.43_±_0.021<br>2.90_±_0.047<br> **2.53** _±_0.019|5.07_±_0.016<br>5.01_±_0.017 <br>5.90_±_0.107 <br> **4.45** _±_0.026|94.3%_±_7.00%<br> 100%_±_0.000%<br> 83.3%_±_0.000%<br> 100%_±_0.000%|169_±_5.76<br>138_±_2.70<br>190_±_1.46<br>**126**_±_1.63|72.0_±_0.692 <br>75.4_±_1.18 <br>89.4_±_0.50<br>**71.2**_±_0.163|3.26_±_0.076 <br> 3.14_±_0.042 <br>3.44_±_0.16<br> **2.81**_±_0.037|5.86_±_0.101<br> 5.50_±_0.058<br>7.49_±_0.11<br> **5.13**_±_0.066|
||Oracle (IsaacGym _→_IsaacGym)|100%_±_0.000%|116_±_0.711|52.5_±_0.298|3.40_±_0.027|6.16 _±_0.028|100%_±_0.000%|116_±_0.711|52.5_±_0.298|3.40_±_0.027|6.16 _±_0.028|
|Hard|Vanilla (IsaacGym _→_TestEnv)<br>SysID<br>DeltaDynamics<br>ASAP|100%_±_0.000%<br>100%_±_0.000%<br>66.7%_±_0.000%<br>100%_±_0.000%|148_±_0.845<br>165_±_3.83<br>137_±_2.59<br>**129** _±_1.57|**51.6**_±_0.137<br>58.4_±_0.229<br>60.2_±_0.477<br>56.5 _±_1.15|4.41_±_0.055<br>4.87_±_0.197<br>4.20_±_0.041<br> **3.72** _±_0.036|6.88_±_0.064<br>7.13_±_0.131 <br>7.10_±_0.024<br> **6.52** _±_0.042|82.9%_±_5.70%<br> 100%_±_0.000%<br>60.0%_±_5.70%<br> 100%_±_0.000%|175_±_9.77<br>186_±_3.84<br>190_±_14.0<br>**129**_±_2.31|80.7_±_1.69 <br>93.0_±_1.49 <br>89.6_±_9.34<br>**77.0**_±_1.07|3.87_±_0.175 <br> 4.98_±_0.245 <br>4.29_±_1.16<br> **2.69**_±_0.040|7.19_±_0.199<br> 8.98_±_0.119<br>8.70_±_2.33<br> **5.65**_±_0.073|


Fig. 6. Visual comparisons of motion imitation results across different difficulty levels (Easy, Medium, Hard) for various tasks including Jump Forward, Side Jump, Single Foot Balance, Squat, Step Backward, Step Forward, and Walk. 

environment trajectories in the training environment. This is achieved by rolling out the same trajectory executed in the testing environment and assessing tracking discrepancies using key metrics such as MPJPE. An ideal method should minimize the discrepancies between training and testing trajectories when replaying testing-environment actions, thereby demonstrating an improved capacity for compensating dynamics mismatch. Quantitative results in Table III demonstrate that ASAP consistently outperforms the OpenLoop baseline across all replayed motion lengths, achieving lower _E_ g-mpjpe and _E_ mpjpe values, which indicate improved alignment with testingenv trajectories. While SysID helps address short-horizon dynamics gaps, it struggles with long-horizon scenarios due to cumulative error buildup. DeltaDynamics improves upon both SysID and OpenLoop for long horizons but suffers from overfitting, as evidenced by cascading errors magnified over time, as shown in Figure 5. ASAP, however, demonstrates superior generalization by learning residual policies that effectively bridge the dynamics gap. Comparable trends are observed in the Genesis simulator, where ASAP achieves notable improvements across all metrics relative to the baseline. These results emphasize the efficacy of learning delta action model to reduce the physics gap and improve open-loop replay performance. 

## _B. Comparison of Policy Fine-Tuning Performance_ 

To address **Q2** ( _Can ASAP finetune policy to outperform SysID and Delta Dynamics methods?_ ), we evaluate the effectiveness of different methods in fine-tuning RL policies for improved testing-environment performance. We fine-tune RL policies in modified training environments and subsequently deploy them in the testing environments, quantifying motiontracking errors in testing environments. As shown in Table IV, ASAP consistently outperforms baselines such as Vanilla, SysID, and DeltaDynamics across all difficulty levels (Easy, Medium, and Hard) in both simulators (IsaacSim and Genesis). For the Easy level, our method achieves the lowest _E_ g-mpjpe and _E_ mpjpe in IsaacSim ( _E_ g-mpjpe = 106 and _E_ mpjpe = 44 _._ 3) and Genesis ( _E_ g-mpjpe = 125 and _E_ mpjpe = 73 _._ 5), with minimal acceleration (Eacc) and velocity (Evel) errors. In more challenging tasks, such as the Hard level, our method continues to excel, significantly reducing motion-tracking errors. For instance, in Genesis, it achieves _E_ g-mpjpe = 129 and _E_ mpjpe = 77 _._ 0, outperforming SysID and DeltaDynamics by substantial margins. Additionally, our method consistently maintains a 100% success rate across both simulators, unlike DeltaDynamics, which experiences lower success rates in harder environments. To further illustrate the advantages of ASAP, we provide per-step visualizations in Figure 7, comparing ASAP with 


Fig. 7. Visualization of G1 motion tracking before and after ASAP fine-tuning in IsaacGym, IsaacSim and Genesis. Top: LeBron James’ “Silencer” motion tracking policy fine-tuning for IsaacGym to IsaacSim. Bottom: _single foot balance_ motion tracking policy fine-tuning for IsaacGym to Genesis. 

RL policies deployed without fine-tuning. These visualizations demonstrate that ASAP successfully adapts to new dynamics and maintains stable tracking performance, whereas baseline methods accumulate errors over time, leading to degraded tracking capability. These results highlight the robustness and adaptability of our approach in addressing the sim-to-real gap while preventing overfitting and exploitation. The findings validate that ASAP is an effective paradigm for improving closed-loop performance and ensuring reliable deployment in complex real-world scenarios. 

## _C. Real-World Evaluations_ 

To answer **Q3** ( _Does ASAP work for sim-to-real transfer?_ ). We validate ASAP on real-world Unitree G1 robot. 

**Real-World Data.** In the real-world experiments, we prioritize both motion safety and representativeness by selecting five motion-tracking tasks, including (i) _kick_ , (ii) _jump forward_ , (iii) _step forward and back_ , (iv) _single foot balance_ and (v) _single foot jump_ . However, collecting over 400 realworld motion clips— the minimum required to train the full 23-DoF delta action model in simulation, as discussed inSection III-B—poses significant challenges. Our experiments 

involve highly dynamic motions that cause rapid overheating of joint motors, leading to hardware failures (two Unitree G1 robots broke during data collection). Given these constraints, we adopt a more sample-efficient approach by focusing exclusively on learning a 4-DoF ankle delta action model rather than the full-body 23-DoF model. This decision is motivated by two key factors: (1) the limited availability of real-world data makes training the full 23-DoF delta action model infeasible, and (2) the Unitree G1 robot [77] features a mechanical linkage design in the ankle, which introduces a significant sim-to-real gap that is difficult to bridge with conventional modeling techniques [37]. Under this setting, the original 23 DoF delta action model reduces to 4 DoF delta action model, which needs much less data to be trainable. In practice, we collect 100 motion clips, which prove sufficient to train an effective 4-DoF delta action model for real-world scenarios. 

We execute the tracking policy 30 times for each task. In addition to these motion-tracking tasks, we also collect 10 minutes of locomotion data. The locomotion policy will be addressed in the next section, which is also utilized to bridge different tracking policies. 

**Policy Transition.** In the real world, we cannot easily reset 


Fig. 8. Visualization of LeBron James’ “Silencer” motion on the G1 robot before (upper figure enclosed in blue) and after (bottom figure enclosed in red) ASAP policy finetuning. The left half shows the policy finetuning for the in-distribution motions while the right half shows the out-of-distribution ones. After ASAP finetuning, the robot behaves more smoothly and reduces jerky lower-body motions. 


Fig. 9. We deploy the pretrained policy of a forward jump motion tracking task, challenging the 1.35m-tall Unitree G1 robot for a forward leap over 1m. 

the robot as in simulators, and therefore we train a robust locomotion policy for the policy transition between different motion-tracking tasks. Our locomotion command contains ( _v, ω,_ Π), where _v_ and _ω_ indicate the linear and angular velocities while Π indicates the command to walk or stand still. After each motion-tracking task is done, our locomotion policy will take over to keep the robot balance until the next motion-tracking task begins. In this way, the robot is able to execute multiple tasks without manually resetting. 

**Real-World Results.** The sim-to-real gap is more pronounced than simulator-to-simulator discrepancies due to factors such as noisy sensor input, inaccuracies in robot modeling, and actuator differences. To evaluate the effectiveness of ASAP in addressing these gaps, we compare the closedloop performance of ASAP with the _Vanilla_ baseline on two representative motion tracking tasks (kicking and “Silencer”) in which observe obvious sim-to-real gaps. To show the 

TABLE V 

REAL-WORLD CLOSED-LOOP PERFORMANCE COMPARING WITH AND WITHOUT ASAP FINETUNING ON ONE IN-DISTRIBUTION MOTION AND ONE OUT-OF-DISTRIBUTION MOTION. 

|Motion|Real|-World-|Kick||Real-Wo|rld-LeBron (|OOD)|
|---|---|---|---|---|---|---|---|
|Method|_E_g-mpjpe|_E_mpjpe|Eacc|Evel|_E_g-mpjpe|_E_mpjpe Eacc|Evel|
|Vanilla|61.2|43.5|2.96|2.91|159|55.3<br>3.43|6.43|
|ASAP|**50.2**|**40.1**|**2.46 **|**2.70**|**112**|**47.5**<br>**2.84 **|**5.94**|


generalizability of the learned delta action model for out-ofdistribution motions, we also fine-tune the policy for LeBron James’ “Silencer” motion as shown in Figure 1 and Figure 8. The experiment data is summarized in Table V. It shows that ASAP outperforms the baseline on both in-distribution and out-of-distribution humanoid motion tracking tasks, achieving a considerable reduction of the tracking errors across all key metrics ( _E_ g-mpjpe _, E_ mpjpe _, Eacc_ and _Evel_ ). These findings highlight the effectiveness of ASAP in improving sim-to-real transfer for agile humanoid motion tracking. 

## V. EXTENSIVE STUDIES AND ANALYSES 

In this section, we aim to thoroughly analyze ASAP by addressing three central research questions: 

- **Q4** : How to best train the delta action model of ASAP? 

- **Q5** : How to best use the delta action model of ASAP? 

- **Q6** : Why and how does ASAP work? 

## _A. Key Factors in Training Delta Action Models_ 

To Answer **Q4** ( _How to best train the delta action model of ASAP_ ). we conduct a systematic study on key factors influencing the performance of the delta action model. Specifically, we investigate the impact of dataset size, training horizon, and action norm weight, evaluating their effects on both openloop and closed-loop performance. Our analysis uncovers the 


Fig. 10. Analysis of dataset size, training horizon, and action norm on the performance of _π_<sup>∆</sup> . (a) **Dataset Size** : Mean Per Joint Position Error (MPJPE) is evaluated for both in-distribution (green) and out-of-distribution (blue) scenarios. Increasing dataset size leads to enhanced generalization, evidenced by decreasing errors in out-of-distribution evaluations. Closed-loop MPJPE (red bars) also shows improvement with larger datasets. (b) **Training Horizon** : Openloop MPJPE (heatmap) improves across evaluation points as training horizons increase, achieving the lowest error at 1.5s. However, closed-loop MPJPE (red bars) shows a sweet spot at a training horizon of 1.0s, beyond which no further improvements are observed. The red dashed line represents the pretrained baseline without _π_<sup>∆</sup> fine-tuning. (c) **Action Norm** : The action norm weight significantly influences performance. Both open-loop and closed-loop MPJPE decrease as the weight increases up to 0.1, achieving the lowest error. However, further increases in the action norm weight result in degradation of open-loop performance, highlighting the trade-off between action smoothness and policy flexibility. 

essential principles for effectively training a high-performing delta action model. 

_a) Dataset Size:_ We analyze the impact of dataset size on the training and generalization of _π_<sup>∆</sup> . Simulation data is collected in Isaac Sim, and _π_<sup>∆</sup> is trained in Isaac Gym. Openloop performance is assessed on both in-distribution (training) and out-of-distribution (unseen) trajectories, while closed-loop performance is evaluated using the fine-tuned policy in Isaac Sim. As shown in Figure 10 (a), increasing the dataset size improves _π_<sup>∆</sup> ’s generalization, evidenced by reduced errors in out-of-distribution evaluations. However, the improvement in closed-loop performance saturates, with a marginal decrease of only 0 _._ 65% when scaling from 4300 to 43000 samples, suggesting limited additional benefit from larger datasets. 

_b) Training Horizon:_ The rollout horizon plays a crucial role in learning _π_<sup>∆</sup> . As shown in Figure 10 (b), longer training horizons generally improve open-loop performance, with a horizon of 1.5s achieving the lowest errors across evaluation points at 0.25s, 0.5s, and 1.0s. However, this trend does not consistently extend to closed-loop performance. The best closed-loop results are observed at a training horizon of 1.0s, indicating that excessively long horizons do not provide additional benefits for fine-tuned policy. 

_c) Action Norm Weight:_ Training _π_<sup>∆</sup> incorporates an action norm reward to balance dynamics alignment and minimal correction. As illustrated in Figure 10 (c), both openloop and closed-loop errors decrease as the action norm 

weight increases, reaching the lowest error at a weight of 0 _._ 1. However, further increasing the action norm weight causes open-loop errors to rise, likely due to the minimal action norm reward dominates in the delta action RL training. This highlights the importance of carefully tuning the action norm weight to achieve optimal performance. 

## _B. Different Usage of Delta Action Model_ 

To answer **Q5** _(_ How to best use the delta action model of ASAP?), we compare multiple strategies: fixed-point iteration, gradient-based optimization, and reinforcement learning (RL). Given a learned delta policy _π_<sup>∆</sup> such that: 


and a nominal policy _π_ ˆ( _s_ ) that performs well in simulation, the goal is to fine-tune _π_ ˆ( _s_ ) for real-world deployment. 

A simple approach is one-step dynamics matching, which leads to the relationship: 


We consider two RL-free methods: fixed-point iteration and gradient-based optimization. Fixed-point iteration refines _π_ ˆ( _s_ ) iteratively, while gradient-based optimization minimizes a loss function to achieve a better estimate. These methods are compared against RL fine-tuning, which adapts _π_ ˆ( _s_ ) using reinforcement learning in simulation. The detailed derivation of these two baselines is summarized in Section VIII-D. 

Our experiments in Figure 11 show that RL fine-tuning achieves the lowest tracking error during deployment, outperforming training-free methods. Both RL-free approaches are myopic and suffer from out-of-distribution issues, limiting their real-world applicability (more discussions in Section VIII-D). 


Fig. 11. MPJPE comparison over timesteps for fine-tuning methods using delta actionmodel. RL Fine-Tuning achieves the lowest error, while FixedPoint Iteration and Gradient Search perform worse than the baseline (Before DeltaA) showing the highest error. 

_C. Does ASAP Fine-Tuning Outperform Random Action Noise Fine-Tuning?_ 

To answer **Q6** ( _How does ASAP work?_ ), we validate ASAP finetuning is better than injecting random-action-noise-based finetuning. And we visualize the average magnitude of the delta action model for each joint. 

Random torque noise [7] is a widely used domain randomization technique for legged robots. To determine whether delta action facilitates fine-tuning of pre-trained policies toward real-world dynamics rather than merely enhancing robustness through random action noise, we analyze its impact. Specifically, we assess the effect of applying random action noise during policy fine-tuning in Isaac Gym by modifying the environment dynamics as _st_ +1 = _f_<sup>sim</sup> ( _st, at_ + _βδa_ ), where _δa ∼U_ [0 _,_ 1], and deploy it in Genesis. We conduct an ablation study to examine the influence of the noise magnitude, _β_ , varying from 0 _._ 025 to 0 _._ 4. As shown in Figure 12, within the constrained range of _β ∈_ [0 _._ 025 _,_ 0 _._ 2], policies fine-tuned with action noise outperform those without fine-tuning in terms of global tracking error (MPJPE). However, the performance of the action noise approach (MPJPE of 150) does not match the precision achieved by ASAP (MPJPE of 126). Furthermore, we visualize the average output of _π_<sup>∆</sup> learned from IsaacSim data in Figure 13, which reveals non-uniform discrepancies across joints. For example, in the G1 humanoid robot under our experimental setup, lower-body motors exhibit a larger dynamics gap compared to upper-body joints. Within the lower-body, the ankle and knee joints show the most pronounced discrepancies. Additionally, asymmetries between the left and right body motors further highlight the complexity. Such structured discrepancies cannot be effectively captured by merely adding uniform action noise. These findings, along with the results in Figure 5, demonstrate that delta action 


Fig. 12. MPJPE vs. Noise Level for policies fine-tuned with random action noise. Policies with noise levels _β ∈_ [0 _._ 025 _,_ 0 _._ 2] show improved performance compared to no fine-tuning. Delta action achieves better tracking precision (126 MPJPE) compared to the best action noise (173 MPJPE). 


Fig. 13. Visualization of IsaacGym-to-IsaacSim _π_<sup>∆</sup> output magnitude. We compute the average absolute value of each joint over the 4300-episode dataset. Larger red dots indicate higher values. The results suggest that lowerbody motors exhibit a larger discrepancy compared to upper-body joints, with the most significant gap observed in the ankle pitch joint of the G1 humanoid. 

not only enhances policy robustness but also enables effective adaptation to real-world dynamics, outperforming naive randomization strategies. 

VI. RELATED WORKS 

## _A. Learning-based Methods for Humanoid Control_ 

In recent years, learning-based methods have made significant progress in whole-body control for humanoid robots. Primarily leveraging reinforcement learning algorithms [80] within physics simulators [58, 63, 88], humanoid robots have learned a wide range of skills, including robust locomo- 

tion [44, 98, 45, 48, 47, 74, 73, 19, 106], jumping [46], and parkour [50, 107]. More advanced capabilities, such as dancing [105, 32, 10], loco-manipulation [25, 53, 15, 24], and even backflipping [78], have also been demonstrated. Meanwhile, the humanoid character animation community has achieved highly expressive and agile whole-body motions in physicsbased simulations [71, 86, 55], including cartwheels [67], backflips [69], sports movements [104, 90, 56, 91, 92], and smooth object interactions [86, 17, 22]. However, transferring these highly dynamic and agile skills to real-world humanoid robots remains challenging due to the dynamics mismatch between simulation and real-world physics. To address this challenge, our work focuses on learning and compensating for this dynamics mismatch, enabling humanoid robots to perform expressive and agile whole-body skills in the real world. 

## _B. Offline and Online System Identification for Robotics_ 

The dynamics mismatch between simulators and real-world physics can be attributed to two primary factors: inaccuracies in the robot model descriptions and the presence of complex real-world dynamics that are difficult for physics-based simulators to capture. Traditional approaches address these issues using system identification (SysID) methods [39, 5], which calibrate the robot model or simulator based on real-world performance. These methods can be broadly categorized into _offline SysID_ and _online SysID_ , depending on whether system identification occurs at test time. _Offline SysID_ methods typically collect real-world data and adjust simulation parameters to train policies in more accurate dynamics. The calibration process may focus on modeling actuator dynamics [85, 29, 99], refining robot dynamics models [36, 2, 18, 21, 30], explicitly identifying critical simulation parameters [102, 9, 13, 96], learning a distribution over simulation parameters [75, 27, 4], or optimizing system parameters to maximize policy performance [64, 76]. _Online SysID_ methods, in contrast, aim to learn a representation of the robot’s state or environment properties, enabling real-time adaptation to different conditions. These representations can be learned using optimizationbased approaches [101, 103, 43, 70], regression-based methods [100, 40, 89, 19, 31, 60, 14, 72, 61, 41, 62, 42], next-state reconstruction techniques [65, 51, 54, 94, 83], direct reward maximization [47], or by leveraging tracking and prediction errors for online adaptation [66, 57, 28, 16]. Our framework takes a different approach from traditional SysID methods by learning a residual action model that directly compensates for dynamics mismatch through corrective actions, rather than explicitly estimating system parameters. 

## _C. Residual Learning for Robotics_ 

Learning a residual component alongside learned or predefined base models has been widely used in robotics. Prior work has explored residual policy models that refine the actions of an initial controller [84, 34, 8, 1, 12, 20, 3, 33, 42]. Other approaches leverage residual components to correct inaccuracies in dynamics models [66, 35, 38, 82, 23] or to model residual trajectories resulting from residual actions [11] 

for achieving precise and agile motions. RGAT [35] uses a residual action model with a learned forward dynamics to refine the simulator. Our framework builds on this idea by using RL-based residual actions to align the dynamics mismatch between simulation and real-world physics, enabling agile whole-body humanoid skills. 

## VII. CONCLUSION 

We present ASAP, a two-stage framework that bridges the sim-to-real gap for agile humanoid control. By learning a universal delta action model to capture dynamics mismatch, ASAP enables policies trained in simulation to adapt seamlessly to real-world physics. Extensive experiments demonstrate significant reductions in motion tracking errors (up to 52.7% in sim-to-real tasks) and successful deployment of diverse agile skills—including agile jumps and kicks—on the Unitree G1 humanoid. Our work advances the frontier of simto-real transfer for agile whole-body control, paving the way for versatile humanoid robots in real-world applications. 

## VIII. LIMITATIONS 

While ASAP demonstrates promising results in bridging the sim-to-real gap for agile humanoid control, our framework has several real-world limitations that highlights critical challenges in scaling agile humanoid control to real-world: 

- **Hardware Constraints** : Agile whole-body motions exert significant stress on robots, leading to motor overheating and hardware failure during data collection. Two Unitree G1 robots were broken to some extent during our experiments. This bottleneck limits the scale and diversity of real-world motion sequences that can be safely collected. 

- **Dependence on Motion Capture Systems** : Our pipeline requires MoCap setup to record real-world trajectories. This introduces practical deployment barriers in unstructured environments where MoCap setups are unavailable. 

- **Data-Hungry Delta Action Training** : While reducing the delta action model to 4 DoF ankle joints improved sample efficiency, training the full 23 DoF model remains impractical for real-world deployment due to the large demand of required motion clips (e.g., _>_ 400 episodes in simulation for the 23 DoF delta action training). 

Future directions could focus on developing damage-aware policy to mitigate hardware risks, leveraging MoCap-free alignment to eliminate the reliance on MoCap, and exploring adaptation techniques for delta action models to achieve sample-efficient few-shot alignment. 

## ACKNOWLEDGMENTS 

We thank Zhenjia Xu, Yizhou Zhao, Yu Fang for help with hardware. We thank Pulkit Goyal, Hawkeye King, Peter Varvak and Haoru Xue for help with motion capture setup. We thank Ziyan Xiong, Yilin Qiao and Xian Zhou for support on Genesis integration. We thank Rui Chen, Yifan Sun, Kai Yun, Yaru Niu, Yikai Wang and Ding Zhao for help with G1 hardware. We thank Xuxin Cheng, Chong Zhang and Toru Lin for always being there to help with any problem. We thank Unitree Robotics for help with G1 support. 

REFERENCES 

- [1] Minttu Alakuijala, Gabriel Dulac-Arnold, Julien Mairal, Jean Ponce, and Cordelia Schmid. Residual reinforcement learning from demonstrations. <u>arXiv preprint arXiv:2106.08050,</u> 2021. 

- [2] Chae H An, Christopher G Atkeson, and John M Hollerbach. Estimation of inertial parameters of rigid body links of manipulators. In <u>1985 24th IEEE Conference on Decision and Control,</u> pages 990–995. IEEE, 1985. 

- [3] Lars Ankile, Anthony Simeonov, Idan Shenfeld, Marcel Torne, and Pulkit Agrawal. From imitation to refinement–residual rl for precise assembly. <u>arXiv preprint arXiv:2407.16677,</u> 2024. 

- [4] Rika Antonova, Jingyun Yang, Priya Sundaresan, Dieter Fox, Fabio Ramos, and Jeannette Bohg. A bayesian treatment of real-to-sim for deformable object manipulation. <u>IEEE Robotics and Automation Letters,</u> 7(3): 5819–5826, 2022. 

- [5] Karl Johan Astr¨om<sup>˚</sup> and Peter Eykhoff. System identification—a survey. <u>Automatica,</u> 7(2):123–162, 1971. 

- [6] Genesis Authors. Genesis: A universal and generative physics engine for robotics and beyond, December 2024. URL https://github.com/Genesis-Embodied-AI/ Genesis. 

- [7] Luigi Campanaro, Siddhant Gangapurwala, Wolfgang Merkt, and Ioannis Havoutis. Learning and deploying robust locomotion policies with minimal dynamics randomization. In <u>6th Annual Learning for Dynamics & Control Conference,</u> pages 578–590. PMLR, 2024. 

- [8] Joao Carvalho, Dorothea Koert, Marek Daniv, and Jan Peters. Residual robot learning for object-centric probabilistic movement primitives. <u>arXiv preprint arXiv:2203.03918,</u> 2022. 

- [9] Yevgen Chebotar, Ankur Handa, Viktor Makoviychuk, Miles Macklin, Jan Issac, Nathan Ratliff, and Dieter Fox. Closing the sim-to-real loop: Adapting simulation randomization with real world experience. In <u>2019 International Conference on Robotics and Automation (ICRA),</u> pages 8973–8979. IEEE, 2019. 

- [10] Xuxin Cheng, Yandong Ji, Junming Chen, Ruihan Yang, Ge Yang, and Xiaolong Wang. Expressive wholebody control for humanoid robots. <u>arXiv preprint arXiv:2402.16796,</u> 2024. 

- [11] Cheng Chi, Benjamin Burchfiel, Eric Cousineau, Siyuan Feng, and Shuran Song. Iterative residual policy: for goal-conditioned dynamic manipulation of deformable objects. <u>The International Journal of Robotics Research,</u> 43(4):389–404, 2024. 

- [12] Todor Davchev, Kevin Sebastian Luck, Michael Burke, Franziska Meier, Stefan Schaal, and Subramanian Ramamoorthy. Residual learning from demonstration: Adapting dmps for contact-rich manipulation. <u>IEEE Robotics and Automation Letters,</u> 7(2):4488–4495, 2022. 

- [13] Yuqing Du, Olivia Watkins, Trevor Darrell, Pieter 

Abbeel, and Deepak Pathak. Auto-tuned sim-to-real transfer. In <u>2021 IEEE International Conference on Robotics and Automation (ICRA),</u> pages 1290–1296. IEEE, 2021. 

- [14] Zipeng Fu, Xuxin Cheng, and Deepak Pathak. Deep whole-body control: learning a unified policy for manipulation and locomotion. In <u>Conference on Robot Learning,</u> pages 138–149. PMLR, 2023. 

- [15] Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. Humanplus: Humanoid shadowing and imitation from humans. <u>arXiv preprint arXiv:2406.10454,</u> 2024. 

- [16] Feng Gao, Chao Yu, Yu Wang, and Yi Wu. Neural internal model control: Learning a robust control policy via predictive error feedback. <u>arXiv preprint arXiv:2411.13079,</u> 2024. 

- [17] Jiawei Gao, Ziqin Wang, Zeqi Xiao, Jingbo Wang, Tai Wang, Jinkun Cao, Xiaolin Hu, Si Liu, Jifeng Dai, and Jiangmiao Pang. Coohoi: Learning cooperative humanobject interaction with manipulated object dynamics. <u>arXiv preprint arXiv:2406.14558,</u> 2024. 

- [18] Maxime Gautier, Pierre-Olivier Vandanjon, and Alexandre Janot. Dynamic identification of a 6 dof robot without joint position data. In <u>2011 IEEE International Conference on Robotics and Automation,</u> pages 234– 239. IEEE, 2011. 

- [19] Xinyang Gu, Yen-Jen Wang, Xiang Zhu, Chengming Shi, Yanjiang Guo, Yichen Liu, and Jianyu Chen. Advancing humanoid locomotion: Mastering challenging terrains with denoising world model learning. <u>arXiv preprint arXiv:2408.14472,</u> 2024. 

- [20] Siddhant Haldar, Jyothish Pari, Anant Rai, and Lerrel Pinto. Teach a robot to fish: Versatile imitation from one minute of demonstrations. <u>arXiv preprint arXiv:2303.01497,</u> 2023. 

- [21] Yong Han, Jianhua Wu, Chao Liu, and Zhenhua Xiong. An iterative approach for accurate dynamic model identification of industrial robots. <u>IEEE Transactions on Robotics,</u> 36(5):1577–1594, 2020. 

- [22] Mohamed Hassan, Yunrong Guo, Tingwu Wang, Michael Black, Sanja Fidler, and Xue Bin Peng. Synthesizing physical character-scene interactions. In <u>ACM SIGGRAPH 2023 Conference Proceedings,</u> pages 1–9, 2023. 

- [23] Guanqi He, Yogita Choudhary, and Guanya Shi. Selfsupervised meta-learning for all-layer dnn-based adaptive control with stability guarantees. <u>arXiv preprint arXiv:2410.07575,</u> 2024. 

- [24] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning. <u>arXiv preprint arXiv:2406.08858,</u> 2024. 

- [25] Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning human-to-humanoid real-time whole-body teleop- 

eration. <u>arXiv preprint arXiv:2403.04436,</u> 2024. 

- [26] Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Jan Kautz, Changliu Liu, Guanya Shi, Xiaolong Wang, et al. Hover: Versatile neural whole-body controller for humanoid robots. <u>arXiv preprint arXiv:2410.21229,</u> 2024. 

- [27] Eric Heiden, Christopher E Denniston, David Millard, Fabio Ramos, and Gaurav S Sukhatme. Probabilistic inference of simulation parameters via parallel differentiable simulation. In <u>2022 International Conference on Robotics and Automation (ICRA), pages 3638–3645.</u> IEEE, 2022. 

- [28] Kevin Huang, Rwik Rana, Alexander Spitzer, Guanya Shi, and Byron Boots. Datt: Deep adaptive trajectory tracking for quadrotor control. <u>arXiv preprint arXiv:2310.09053,</u> 2023. 

- [29] Jemin Hwangbo, Joonho Lee, Alexey Dosovitskiy, Dario Bellicoso, Vassilios Tsounis, Vladlen Koltun, and Marco Hutter. Learning agile and dynamic motor skills for legged robots. <u>Science Robotics,</u> 4(26):eaau5872, 2019. 

- [30] Alexandre Janot, Pierre-Olivier Vandanjon, and Maxime Gautier. A generic instrumental variable approach for industrial robot identification. <u>IEEE Transactions on Control Systems Technology,</u> 22(1):132–145, 2013. 

- [31] Gwanghyeon Ji, Juhyeok Mun, Hyeongjun Kim, and Jemin Hwangbo. Concurrent training of a control policy and a state estimator for dynamic and robust legged locomotion. <u>IEEE Robotics and Automation Letters,</u> 7 (2):4630–4637, 2022. 

- [32] Mazeyu Ji, Xuanbin Peng, Fangchen Liu, Jialong Li, Ge Yang, Xuxin Cheng, and Xiaolong Wang. Exbody2: Advanced expressive humanoid whole-body control. <u>arXiv preprint arXiv:2412.13196,</u> 2024. 

- [33] Yunfan Jiang, Chen Wang, Ruohan Zhang, Jiajun Wu, and Li Fei-Fei. Transic: Sim-to-real policy transfer by learning from online correction. <u>arXiv preprint arXiv:2405.10315,</u> 2024. 

- [34] Tobias Johannink, Shikhar Bahl, Ashvin Nair, Jianlan Luo, Avinash Kumar, Matthias Loskyll, Juan Aparicio Ojea, Eugen Solowjow, and Sergey Levine. Residual reinforcement learning for robot control. In <u>2019 international conference on robotics and automation (ICRA),</u> pages 6023–6029. IEEE, 2019. 

- [35] Haresh Karnan, Siddharth Desai, Josiah P Hanna, Garrett Warnell, and Peter Stone. Reinforced grounded action transformation for sim-to-real transfer. In <u>2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS),</u> pages 4397–4402. IEEE, 2020. 

- [36] Pradeep K Khosla and Takeo Kanade. Parameter identification of robot dynamics. In <u>1985 24th IEEE conference on decision and control,</u> pages 1754–1760. IEEE, 1985. 

- [37] Donghyun Kim, Steven Jens Jorgensen, Jaemin Lee, Junhyeok Ahn, Jianwen Luo, and Luis Sentis. Dy- 

namic locomotion for passive-ankle biped robots and humanoids using whole-body locomotion control. <u>Int. J. Robotics Res., 39(8), 2020. doi: 10.1177/027836492091</u> 8014. URL https://doi.org/10.1177/0278364920918014. 

- [38] Alina Kloss, Stefan Schaal, and Jeannette Bohg. Combining learned and analytical models for predicting action effects from sensory data. <u>The International Journal of Robotics Research,</u> 41(8):778–797, 2022. 

- [39] F Kozin and HG Natke. System identification techniques. <u>Structural safety,</u> 3(3-4):269–316, 1986. 

- [40] Ashish Kumar, Zipeng Fu, Deepak Pathak, and Jitendra Malik. Rma: Rapid motor adaptation for legged robots. <u>arXiv preprint arXiv:2107.04034,</u> 2021. 

- [41] Ashish Kumar, Zhongyu Li, Jun Zeng, Deepak Pathak, Koushil Sreenath, and Jitendra Malik. Adapting rapid motor adaptation for bipedal robots. In <u>2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS),</u> pages 1161–1168. IEEE, 2022. 

- [42] Joonho Lee, Jemin Hwangbo, Lorenz Wellhausen, Vladlen Koltun, and Marco Hutter. Learning quadrupedal locomotion over challenging terrain. <u>Science robotics,</u> 5(47):eabc5986, 2020. 

- [43] Kuang-Huei Lee, Ofir Nachum, Tingnan Zhang, Sergio Guadarrama, Jie Tan, and Wenhao Yu. Pi-ars: Accelerating evolution-learned visual-locomotion with predictive information representations. In <u>2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS),</u> pages 1447–1454. IEEE, 2022. 

- [44] Tianyu Li, Hartmut Geyer, Christopher G Atkeson, and Akshara Rai. Using deep reinforcement learning to learn high-level policies on the atrias biped. In <u>2019 International Conference on Robotics and Automation (ICRA),</u> pages 263–269. IEEE, 2019. 

- [45] Zhongyu Li, Xuxin Cheng, Xue Bin Peng, Pieter Abbeel, Sergey Levine, Glen Berseth, and Koushil Sreenath. Reinforcement learning for robust parameterized locomotion control of bipedal robots. In <u>2021 IEEE International Conference on Robotics and Automation (ICRA),</u> pages 2811–2817. IEEE, 2021. 

- [46] Zhongyu Li, Xue Bin Peng, Pieter Abbeel, Sergey Levine, Glen Berseth, and Koushil Sreenath. Robust and versatile bipedal jumping control through reinforcement learning. <u>arXiv preprint arXiv:2302.09450,</u> 2023. 

- [47] Zhongyu Li, Xue Bin Peng, Pieter Abbeel, Sergey Levine, Glen Berseth, and Koushil Sreenath. Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control. <u>The International Journal of Robotics Research, page 02783649241285161, 2024.</u> 

- [48] Qiayuan Liao, Bike Zhang, Xuanyu Huang, Xiaoyu Huang, Zhongyu Li, and Koushil Sreenath. Berkeley humanoid: A research platform for learning-based control. <u>arXiv preprint arXiv:2407.21781,</u> 2024. 

- [49] Lennart Ljung. System identification. In <u>Signal analysis and prediction,</u> pages 163–173. Springer. 

- [50] Junfeng Long, Junli Ren, Moji Shi, Zirui Wang, Tao Huang, Ping Luo, and Jiangmiao Pang. Learning 

humanoid locomotion with perceptive internal model. <u>arXiv preprint arXiv:2411.14386,</u> 2024. 

- [51] Junfeng Long, Zirui Wang, Quanyi Li, Liu Cao, Jiawei Gao, and Jiangmiao Pang. Hybrid internal model: Learning agile legged locomotion with simulated robot response. In <u>The Twelfth International Conference on Learning Representations,</u> 2024. 

- [52] Matthew Loper, Naureen Mahmood, Javier Romero, Gerard Pons-Moll, and Michael J Black. Smpl: A skinned multi-person linear model. In <u>Seminal Graphics Papers: Pushing the Boundaries, Volume 2,</u> pages 851– 866. 2023. 

- [53] Chenhao Lu, Xuxin Cheng, Jialong Li, Shiqi Yang, Mazeyu Ji, Chengjing Yuan, Ge Yang, Sha Yi, and Xiaolong Wang. Mobile-television: Predictive motion priors for humanoid whole-body control. <u>arXiv preprint arXiv:2412.07773,</u> 2024. 

- [54] Shixin Luo, Songbo Li, Ruiqi Yu, Zhicheng Wang, Jun Wu, and Qiuguo Zhu. Pie: Parkour with implicit-explicit learning framework for legged robots. <u>IEEE Robotics and Automation Letters,</u> 2024. 

- [55] Zhengyi Luo, Jinkun Cao, Kris Kitani, Weipeng Xu, et al. Perpetual humanoid control for real-time simulated avatars. In <u>Proceedings of the IEEE/CVF International Conference on Computer Vision,</u> pages 10895–10904, 2023. 

- [56] Zhengyi Luo, Jiashun Wang, Kangni Liu, Haotian Zhang, Chen Tessler, Jingbo Wang, Ye Yuan, Jinkun Cao, Zihui Lin, Fengyi Wang, et al. Smplolympics: Sports environments for physically simulated humanoids. <u>arXiv preprint arXiv:2407.00187,</u> 2024. 

- [57] Shangke Lyu, Xin Lang, Han Zhao, Hongyin Zhang, Pengxiang Ding, and Donglin Wang. Rl2ac: Reinforcement learning-based rapid online adaptive control for legged robot robust locomotion. In <u>Proceedings of the Robotics: Science and Systems,</u> 2024. 

- [58] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, et al. Isaac gym: High performance gpu based physics simulation for robot learning. In <u>Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2),</u> 2021. 

- [59] Gabriel B Margolis, Ge Yang, Kartik Paigwar, Tao Chen, and Pulkit Agrawal. Rapid locomotion via reinforcement learning. <u>arXiv preprint arXiv:2205.02824,</u> 2022. 

- [60] Gabriel B Margolis, Xiang Fu, Yandong Ji, and Pulkit Agrawal. Learning to see physical properties with active sensing motor policies. <u>arXiv preprint arXiv:2311.01405,</u> 2023. 

- [61] Gabriel B Margolis, Ge Yang, Kartik Paigwar, Tao Chen, and Pulkit Agrawal. Rapid locomotion via reinforcement learning. <u>The International Journal of Robotics Research,</u> 43(4):572–587, 2024. 

- [62] Takahiro Miki, Joonho Lee, Jemin Hwangbo, Lorenz 

Wellhausen, Vladlen Koltun, and Marco Hutter. Learning robust perceptive locomotion for quadrupedal robots in the wild. <u>Science robotics,</u> 7(62):eabk2822, 2022. 

- [63] Mayank Mittal, Calvin Yu, Qinxi Yu, Jingzhou Liu, Nikita Rudin, David Hoeller, Jia Lin Yuan, Ritvik Singh, Yunrong Guo, Hammad Mazhar, Ajay Mandlekar, Buck Babich, Gavriel State, Marco Hutter, and Animesh Garg. Orbit: A unified simulation framework for interactive robot learning environments. <u>IEEE Robotics and Automation Letters,</u> 8(6):3740– 3747, 2023. doi: 10.1109/LRA.2023.3270034. 

- [64] Fabio Muratore, Christian Eilers, Michael Gienger, and Jan Peters. Data-efficient domain randomization with bayesian optimization. <u>IEEE Robotics and Automation Letters,</u> 6(2):911–918, 2021. 

- [65] I Made Aswin Nahrendra, Byeongho Yu, and Hyun Myung. Dreamwaq: Learning robust quadrupedal locomotion with implicit terrain imagination via deep reinforcement learning. In <u>2023 IEEE International Conference on Robotics and Automation (ICRA), pages</u> 5078–5084. IEEE, 2023. 

- [66] Michael O’Connell, Guanya Shi, Xichen Shi, Kamyar Azizzadenesheli, Anima Anandkumar, Yisong Yue, and Soon-Jo Chung. Neural-fly enables rapid learning for agile flight in strong winds. <u>Science Robotics,</u> 7(66): eabm6597, 2022. 

- [67] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. <u>ACM Transactions On Graphics (TOG),</u> 37(4): 1–14, 2018. 

- [68] Xue Bin Peng, Marcin Andrychowicz, Wojciech Zaremba, and Pieter Abbeel. Sim-to-real transfer of robotic control with dynamics randomization. In <u>2018 IEEE international conference on robotics and automation (ICRA),</u> pages 3803–3810. IEEE, 2018. 

- [69] Xue Bin Peng, Angjoo Kanazawa, Jitendra Malik, Pieter Abbeel, and Sergey Levine. Sfv: Reinforcement learning of physical skills from videos. <u>ACM Transactions On Graphics (TOG),</u> 37(6):1–14, 2018. 

- [70] Xue Bin Peng, Erwin Coumans, Tingnan Zhang, TsangWei Lee, Jie Tan, and Sergey Levine. Learning agile robotic locomotion skills by imitating animals. <u>arXiv preprint arXiv:2004.00784,</u> 2020. 

- [71] Xue Bin Peng, Yunrong Guo, Lina Halper, Sergey Levine, and Sanja Fidler. Ase: Large-scale reusable adversarial skill embeddings for physically simulated characters. <u>ACM Transactions On Graphics (TOG),</u> 41 (4):1–17, 2022. 

- [72] Haozhi Qi, Ashish Kumar, Roberto Calandra, Yi Ma, and Jitendra Malik. In-hand object rotation via rapid motor adaptation. In <u>Conference on Robot Learning,</u> pages 1722–1732. PMLR, 2023. 

- [73] I Radosavovic, B Zhang, B Shi, J Rajasegaran, S Kamat, T Darrell, K Sreenath, and J Malik. Humanoid locomotion as next token prediction. arxiv. 2024. <u>arXiv</u> 

<u>preprint arXiv:2402.19469,</u> 2024. 

- [74] Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Realworld humanoid locomotion with reinforcement learning. <u>Science Robotics,</u> 9(89):eadi9579, 2024. 

- [75] Fabio Ramos, Rafael Carvalhaes Possas, and Dieter Fox. Bayessim: adaptive domain randomization via probabilistic inference for robotics simulators. <u>arXiv preprint arXiv:1906.01728,</u> 2019. 

- [76] Allen Z Ren, Hongkai Dai, Benjamin Burchfiel, and Anirudha Majumdar. Adaptsim: Task-driven simulation adaptation for sim-to-real transfer. <u>arXiv preprint arXiv:2302.04903,</u> 2023. 

- [77] Unitree Robotics. Unitree g1 humanoid agent ai avatar, 2024. URL https://www.unitree.com/g1. 

- [78] Unitree Robotics. Unitree h1 the world’s first full-size motor drive humanoid robot flips on ground, 2024. URL https://www.youtube.com/watch?v=V1LyWsiTgms. 

- [79] Nikita Rudin, David Hoeller, Philipp Reist, and Marco Hutter. Learning to walk in minutes using massively parallel deep reinforcement learning. In <u>Conference on Robot Learning,</u> pages 91–100. PMLR, 2022. 

- [80] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. <u>arXiv preprint arXiv:1707.06347, 2017.</u> 

- [81] Guanya Shi, Xichen Shi, Michael O’Connell, Rose Yu, Kamyar Azizzadenesheli, Animashree Anandkumar, Yisong Yue, and Soon-Jo Chung. Neural lander: Stable drone landing control using learned dynamics. In <u>2019 international conference on robotics and automation (icra),</u> pages 9784–9790. IEEE, 2019. 

- [82] Guanya Shi, Wolfgang H¨onig, Xichen Shi, Yisong Yue, and Soon-Jo Chung. Neural-swarm2: Planning and control of heterogeneous multirotor swarms using learned interactions. <u>IEEE Transactions on Robotics,</u> 38(2): 1063–1079, 2021. 

- [83] Aditya Shirwatkar, Naman Saxena, Kishore Chandra, and Shishir Kolathaya. Pip-loco: A proprioceptive infinite horizon planning framework for quadrupedal robot locomotion. <u>arXiv preprint arXiv:2409.09441,</u> 2024. 

- [84] Tom Silver, Kelsey Allen, Josh Tenenbaum, and Leslie Kaelbling. Residual policy learning. <u>arXiv preprint arXiv:1812.06298,</u> 2018. 

- [85] Jie Tan, Tingnan Zhang, Erwin Coumans, Atil Iscen, Yunfei Bai, Danijar Hafner, Steven Bohez, and Vincent Vanhoucke. Sim-to-real: Learning agile locomotion for quadruped robots. <u>arXiv preprint arXiv:1804.10332,</u> 2018. 

- [86] Chen Tessler, Yunrong Guo, Ofir Nabati, Gal Chechik, and Xue Bin Peng. Maskedmimic: Unified physicsbased character control through masked motion inpainting. <u>ACM Transactions on Graphics (TOG), 43(6):1–21,</u> 2024. 

- [87] Josh Tobin, Rachel Fong, Alex Ray, Jonas Schneider, Wojciech Zaremba, and Pieter Abbeel. Domain random- 

ization for transferring deep neural networks from simulation to the real world. In <u>2017 IEEE/RSJ international conference on intelligent robots and systems (IROS),</u> pages 23–30. IEEE, 2017. 

- [88] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In <u>2012 IEEE/RSJ International Conference on Intelligent Robots and Systems,</u> pages 5026–5033. IEEE, 2012. doi: 10.1109/IROS.2012.6386109. 

- [89] Hongxi Wang, Haoxiang Luo, Wei Zhang, and Hua Chen. Cts: Concurrent teacher-student reinforcement learning for legged locomotion. <u>IEEE Robotics and Automation Letters,</u> 2024. 

- [90] Jiashun Wang, Jessica Hodgins, and Jungdam Won. Strategy and skill learning for physics-based table tennis animation. In <u>ACM SIGGRAPH 2024 Conference Papers,</u> pages 1–11, 2024. 

- [91] Yinhuai Wang, Jing Lin, Ailing Zeng, Zhengyi Luo, Jian Zhang, and Lei Zhang. Physhoi: Physics-based imitation of dynamic human-object interaction. <u>arXiv preprint arXiv:2312.04393,</u> 2023. 

- [92] Yinhuai Wang, Qihan Zhao, Runyi Yu, Ailing Zeng, Jing Lin, Zhengyi Luo, Hok Wai Tsui, Jiwen Yu, Xiu Li, Qifeng Chen, et al. Skillmimic: Learning reusable basketball skills from demonstrations. <u>arXiv preprint arXiv:2408.15270,</u> 2024. 

- [93] Yufu Wang, Ziyun Wang, Lingjie Liu, and Kostas Daniilidis. Tram: Global trajectory and motion of 3d humans from in-the-wild videos. In <u>European Conference on Computer Vision,</u> pages 467–487. Springer, 2025. 

- [94] Zhicheng Wang, Wandi Wei, Ruiqi Yu, Jun Wu, and Qiuguo Zhu. Toward understanding key estimation in learning robust humanoid locomotion. <u>arXiv preprint arXiv:2403.05868,</u> 2024. 

- [95] Lior Wolf. Ai for humanoid robotics - a lecture by mentee robotics’ ceo, prof. lior wolf. YouTube video, 2025. URL https://www.youtube.com/watch?v=y1LG 4YwUtoo. Accessed: 2025-01-31. 

- [96] Peilin Wu, Weiji Xie, Jiahang Cao, Hang Lai, and Weinan Zhang. Loopsr: Looping sim-and-real for lifelong policy adaptation of legged robots. <u>arXiv preprint arXiv:2409.17992,</u> 2024. 

- [97] Wenli Xiao, Haoru Xue, Tony Tao, Dvij Kalaria, John M Dolan, and Guanya Shi. Anycar to anywhere: Learning universal dynamics model for agile and adaptive mobility. <u>arXiv preprint arXiv:2409.15783,</u> 2024. 

- [98] Zhaoming Xie, Patrick Clary, Jeremy Dao, Pedro Morais, Jonanthan Hurst, and Michiel Panne. Learning locomotion skills for cassie: Iterative design and sim-toreal. In <u>Conference on Robot Learning, pages 317–329.</u> PMLR, 2020. 

- [99] Yuxiang Yang, Guanya Shi, Changyi Lin, Xiangyun Meng, Rosario Scalise, Mateo Guaman Castro, Wenhao Yu, Tingnan Zhang, Ding Zhao, Jie Tan, et al. Agile continuous jumping in discontinuous terrains. <u>arXiv preprint arXiv:2409.10923,</u> 2024. 

- [100] Wenhao Yu, Jie Tan, C Karen Liu, and Greg Turk. Preparing for the unknown: Learning a universal policy with online system identification. <u>arXiv preprint arXiv:1702.02453,</u> 2017. 

- [101] Wenhao Yu, C Karen Liu, and Greg Turk. Policy transfer with strategy optimization. <u>arXiv preprint arXiv:1810.05751,</u> 2018. 

- [102] Wenhao Yu, Visak CV Kumar, Greg Turk, and C Karen Liu. Sim-to-real transfer for biped locomotion. In <u>2019 ieee/rsj international conference on intelligent robots and systems (iros),</u> pages 3503–3510. IEEE, 2019. 

- [103] Wenhao Yu, Jie Tan, Yunfei Bai, Erwin Coumans, and Sehoon Ha. Learning fast adaptation with meta strategy optimization. <u>IEEE Robotics and Automation Letters,</u> 5(2):2950–2957, 2020. 

- [104] YE YUAN and Viktor Makoviychuk. Learning physically simulated tennis skills from broadcast videos. 2023. 

- [105] Chong Zhang, Wenli Xiao, Tairan He, and Guanya Shi. Wococo: Learning whole-body humanoid control with sequential contacts. <u>arXiv preprint arXiv:2406.06005,</u> 2024. 

- [106] Qiang Zhang, Peter Cui, David Yan, Jingkai Sun, Yiqun Duan, Gang Han, Wen Zhao, Weining Zhang, Yijie Guo, Arthur Zhang, et al. Whole-body humanoid robot locomotion with human reference. In <u>2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS),</u> pages 11225–11231. IEEE, 2024. 

- [107] Ziwen Zhuang, Shenzhe Yao, and Hang Zhao. Humanoid parkour learning. <u>arXiv preprint arXiv:2406.10759,</u> 2024. 

APPENDIX 

- _D. Derivation of Training-free Methods of Using Delta Action_ 

## _A. Domain Randomization in Pre-Training_ 

To improve the robustness and generalization of the pretrained policy in Figure 2 (a), we utilized the domain randomization technics listed in Table VI. 

TABLE VI 

DOMAIN RANDOMIZATIONS 

|Term<br>Value|
|---|
|Dynamics Randomization|
|Friction<br>_U_(0_._2_,_1_._1)<br>P Gain<br>_U_(0_._925_,_1_._05)_×_ default|
|Control delay<br>_U_(20_,_40)ms|
|External Perturbation|
|Push robot<br>interval = 10_s, vxy_ = 0_._5 m_/_s|


To formalize the problem, we start by assuming one-step consistency between real and simulated dynamics: 

_f_<sup>real</sup> ( _s, π_ ( _s_ )) = _f_<sup>sim</sup> ( _s, π_ ( _s_ ) + _π_<sup>∆</sup> ( _s, π_ ( _s_ ))) _._ 

Under this assumption, one-step matching leads to the condition: 


To solve Equation (2), we consider: 

- 1) **Fixed-Point Iteration** : We initialize _y_ 0 = _π_ ˆ( _s_ ) and iteratively update: 


where _yk_ converges to a solution after _K_ iterations. 

## _B. SysID Parameters_ 

We identify the following representative robot parameters in our simulated model that best align the ones in the real world: base center of mass (CoM) shift ( _cx, cy, cz_ ), base link mass offset ratio _km_ and low-level PD gain ratios ( _kp_<sup>_i, k_</sup> _d_<sup>_i_)where</sup> _i_ = 1 _,_ 2 _, ...,_ 23, as shown in Table VII. . 

TABLE VII SYSID PARAMETERS 

|Parameter|Range<br>P|arameter<br>R|ange|
|---|---|---|---|
|_cx_|[_−_0_._02_,_0_._0_,_0_._02]|_cy_<br>[_−_0_._02|_,_0_._0_,_0_._02]|
|_cz_<br>|[_−_0_._02_,_0_._0_,_0_._02]|_km_<br>[0_._95_,_ <br>|1_._0_,_1_._05]|
|_k_<sup>_i_</sup><br>_p_|[0_._95_,_1_._0_,_1_._05]|_k_<sup>_i_</sup><br>_d_<br>[0_._95_,_|1_._0_,_1_._05]|


## _C. Implementation of Delta Dynamics Learning_ 

Using the collected real-world trajectory, we replay the action sequence _{a_<sup>real</sup> 0<sup>_, . . . , a_real</sup> _T_<sup>_}_insimulationandrecord</sup> the resulting trajectory _{s_<sup>sim</sup> 0<sup>_, . . . , s_sim</sup> _T_<sup>_}_.Theneuraldynamics</sup> model _fθ_<sup>∆istrainedtopredictthedifference:</sup> 

- 2) **Gradient-Based Optimization** : Define the loss function: 


A gradient descent method minimizes this loss to solve for _y_ . 

These methods approximate _π_ ( _s_ ), but suffer from OOD issues when trained on limited trajectories. RL fine-tuning, in contrast, directly optimizes _π_ ( _s_ ) for real-world deployment, resulting in superior performance. 

**Problem of One-Step Matching.** Note that Equation (2) is derived from the one-step matching assumption (i.e., _π_ ( _s_ ) + _π_<sup>∆</sup> ( _s, π_ ( _s_ )) = _π_ ˆ( _s_ )). For multi-step matching, one has to differentiate through _f_<sup>sim</sup> , which is, in general, intractable. Therefore, both fixed-point iteration and gradient-based optimization assume one-step matching. This also explains the advantages of RL-based fine-tuning: it effectively performs a gradient-free multi-step matching procedure. 


In practice, we compute the mean squared error (MSE) loss in an autoregressive setting, where the model predicts forward for _K_ steps and uses gradient descent to minimize the loss. To balance learning efficiency and stability over long horizons, we implement a schedule that gradually increases _K_ during training. Formally, the optimization objective is: 


After training, we freeze the residual dynamics model _fθ_<sup>∆</sup> and integrate it into the simulator. During each simulation step, the robot’s state is updated by incorporating the delta predicted by the dynamics model. In this augmented simulation environment, we finetune the previously pretrained policy to adapt to the corrected dynamics, ensuring improved alignment with real-world behavior. 

