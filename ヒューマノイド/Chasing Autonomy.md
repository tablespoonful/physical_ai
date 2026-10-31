---
title: "Chasing Autonomy: Dynamic Retargeting and Control Guided RL for Performant and Controllable Humanoid Running"
date: "2026-03-26"
authors: "Zachary Olkin; William D. Compton; Ryan M. Bena; Aaron D. Ames"
url: https://arxiv.org/abs/2603.25902
pdf: https://arxiv.org/pdf/2603.25902
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.25902)** / [論文ページ](https://arxiv.org/abs/2603.25902)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Chasing Autonomy: Dynamic Retargeting and Control Guided RL for Performant and Controllable Humanoid Running** 

Zachary Olkin, William D. Compton, Ryan M. Bena, Aaron D. Ames 

**_Abstract_ — Humanoid robots have the promise of locomoting like humans, including fast and dynamic running. Recently, reinforcement learning (RL) controllers that can mimic human motions have become popular as they can generate very dynamic behaviors, but they are often restricted to single motion play-back which hinders their deployment in long duration and autonomous locomotion. In this paper, we present a pipeline to dynamically retarget human motions through an optimization routine with hard constraints to generate improved periodic reference libraries from a single human demonstration. We then study the effect of both the reference motion and the reward structure on the reference and commanded velocity tracking, concluding that a goal-conditioned and control-guided reward which tracks dynamically optimized human data results in the best performance. We deploy the policy on hardware, demonstrating its speed and endurance by achieving running speeds of up to 3.3 m/s on a Unitree G1 robot and traversing hundreds of meters in real-world environments. Additionally, to demonstrate the controllability of the locomotion, we use the controller in a full perception and planning autonomy stack for obstacle avoidance while running outdoors.** 

## I. INTRODUCTION 

There has been immense progress in achieving dynamic motions on humanoid robots, but questions about how these motions can be generalized and controlled for autonomy still linger. Designing controllers that generate such behaviors is difficult as they require the ability to be both dynamic and robust. Reinforcement learning (RL) has emerged as a common tool of choice to synthesize such controllers due to its ability to leverage the full nonlinear dynamics, automatically adjust the contact with the environment, and domain randomize for robustness. In this work, we examine how reference tracking RL can be leveraged to generate dynamic and controllable humanoid running for application in an autonomy stack. 

Bipedal and humanoid running has an extensive research history. Early work involved the Raibert heuristic [1] for foot step placement in dynamic maneuvers, while later the the hybrid zero dynamics (HZD) methodology [2] was used to achieve running on planar bipedal robots [3], [4], [5]. HZD has also been extended to leverage human data [6], mirroring what modern controllers do. These methods used classical control concepts such as feedback linearization or control Lyapunov functions (CLFs) to stabilize the nonlinear system around reference trajectories that were generated through full order dynamic trajectory optimization. 

The authors are with the Department of Control and Dynamical Systems and the Department of Mechanical and Civil Engineering at the California Institute of Technology. This research is supported by the Technology Innovation Institute (TII). 


Fig. 1: Demonstration of the running controller working inside on a constrained treadmill and in outdoor real world environments. The running appears human-like while still achieving the commanded speed through a combination of optimized retargeted human data and control guided reward shaping. 

More recently, RL has been used for bipedal locomotion, including running. A bipedal robot completed the 100 m dash [7] and separately RL was used for more versatile control which included running and the 400 m dash [8]. Yet, designing rewards for RL can be very difficult as a poor choice of reward can hurt the performance or training time. Therefore, a common approach to designing RL controllers for bipeds and humanoids is to reward the controller for tracking a pre-defined reference motion. This reference tracking RL paradigm can be done with diverse data sources such as a reduced order model (RoM) [9], full order dynamic trajectories [10], and using human data [11]. These “mimic” style results, e.g. [12], [13], which track agile trajectories from human data, have shown exceptional agility but are generally restricted to single motion play back, while we are interested in generating steady state motions and using these in a controlled manner for autonomous locomotion. 

We aim to design agile locomotion controllers that can be used by a higher-level planner in an autonomy stack. Autonomous robots are generally designed with multiple layers wherein each layer provides commands the layer below. Typically, locomotion controllers take in velocity commands, allowing a higher level controller to interface with the robot 

as a single integrator. If the resulting locomotion policy doesn’t track commanded velocities, it is difficult to use the controller in a layered architecture. Historically, model-based controllers fit this paradigm well as we can generate tracking certificates and use those in the higher level control [14]. This motivates both accurate velocity tracking, and investigation into use of model-based control ideas in RL locomotion controllers. 

## _A. Contributions_ 

   - In this paper we answer three main questions: 

- Q1) How can we generate/design agile reference motions that yield the best reference tracking performance? 

- Q2) How does the reward structure effect both the ability to track references and the ability to track desired velocities? 

- Q3) Can we integrate dynamic motions, like running, into a layered autonomy stack? 

We answer those questions through the following contributions. (C1) We propose to generate reference trajectories for RL controllers by retargeting human data through multipleshooting dynamic optimization with constraints. This method has two major benefits over other works: (1) by adding in dynamics information and state constraints such as periodicity these trajectories can be tracked with lower error than only kinematically retargeted human data and (2) by adding constraints we can modify the trajectories in a dynamically feasible and principled manner to create a library of references. (C2) We study the effect of different rewards on the quality of the reference and commanded velocity tracking. Mimic style rewards are compared with control guided rewards, i.e. CLF-RL [15], for reference tracking performance. Different methods of tracking commanded velocities are compared including heuristically adjusting the trajectories, goal conditioning, and the effect of using a library of references over a single trajectory with goal conditioning. We conclude that goal conditioned CLF-RL with a library of dynamic optimized human data trajectories yields better performance than the baselines. (C3) We demonstrate how the controllability can be used for heading tracking, lateral position control, and autonomy through extensive hardware experiments. The robot is able to achieve a top speed of 3.3 m/s on the hardware and can traverse paths hundreds of meters in distance in the real world. The controller can also be placed in an autonomy stack for obstacle avoidance. Fig. 1 shows a few snapshots of the running experiments. 

## _B. Related Works_ 

_1) Reference Tracking RL:_ There are many variations of the reference tracking RL concept such as tracking a RoM [16], [9], using a RoM feedback controller [17], tracking animated motions [18], using full order dynamics [10], [19], or embedding a controller and dynamic references into the reward [15]. The most dynamic motions achieved through reference tracking RL track human data kinematically retargeted onto the robot [20], [12], [11], [13]. 

The agility of these methods is exceptional, but for the most part the methods are restricted to re-playing single human motion clips, e.g. dance routines or kung fu moves. A diffusion policy to generate new reference motions was proposed in [20] but the motions generated from the diffusion don’t yet have the same agility as the human motions. On the other hand, in [12], [8] single references for running motions are tracked, and “goal conditioned” rewards are used to make the robot track the desired commands, but this has not demonstrated accurate hardware velocity tracking yet. 

_2) Motion Re-targeting:_ When tracking human motions, the data must be converted to a format that the RL controller can use and generally the data needs to be filtered and cleaned before it can be tracked. Methods such as [11], [21] filter the human data based on stability heuristics and additionally smooth ground contacts. Alternatively, [22] cleans and filters the data by learning a separate controller to determine if the motion is feasible. By using dynamic trajectory optimization, we can clean up the data, ensure it is dynamically feasible, and even improve it without heuristics or separate trainings. Another approach to motion re-targeting uses sampling-based optimization [23]. With sampling based methods, enforcing state constraints, such as periodicity, is prohibitively difficult. Furthermore, such methods have yet to demonstrate success in highly dynamic and agile motions, finding success instead in quasi-static manipulation or low-speed humanoid locomotion. 

On the other end of the spectrum, dynamic trajectory optimization without any human data has been used to generate locomotion references for RL [15], [19], [10]. This approach allows the motion to be highly optimized for the robot. In general these methods have been restricted to less dynamic motions, such as walking, although [24] achieved running without human data, the result had low time to overheat and showed minimal outdoor trials. These methods can generate dynamically feasible and periodic motions, but they are not necessarily as well behaved as optimized humandata retargeted motions. 

## _C. Outline_ 

The overall architecture of the method is shown in Fig. 2. A library of dynamic reference trajectories are generated from a single human data segment. This reference is tracked in an RL training loop where a controller is synthesized. The resulting controller can then be applied on hardware with either joystick tracking or a layered control architecture to achieve controlled dynamic running. Section II provides a background on the hybrid systems model used for the optimization as well as a brief overview of CLFs. Then Section III presents the optimization-based retargeting to generate libraries of dynamically feasible trajectories. The different reward structures are presented in Section IV along with the overall RL environment design. Finally, in Section V, multiple simulation ablation studies are conducted and the proposed controller is applied to a real-world robotic humanoid (a Unitree G1), used outdoors over hundreds of meters, and in an autonomy stack. 


Fig. 2: Architecture of the proposed pipeline. Human data is retargeted using state constrained dynamic optimization with a hybrid system model. This allows us to build a library of references from a single human reference and then track this in the RL controller. The RL controller uses a control-guided cost function. Then the policy is transferred zero-shot to hardware and can be used in an autonomy stack. 

## II. PRELIMINARIES 

## _A. Hybrid Systems_ 

To formulate the dynamic retargeting problem, we use an explicit hybrid system model. Legged locomotion can be modeled as a hybrid dynamical system with impulse effects, including both continuous dynamics and discrete events. We denote the system: _H_ = ( _D, S,_ Γ _,_ ∆ _, F_ ) where the domain _D_ := _X × U_ consists of the state manifold and input space, the set of guards _S_ , the set of transitions Γ, the reset-maps ∆, and the continuous dynamics _F_ . A transition from domain _Di_ to _Di_ +1 is denoted as _γ_ := ( _Di, Di_ +1) _∈_ Γ. Then let _Sγ ⊂X_ and ∆ _γ_ denote the guard and associated reset map for a given transition, and ( _fD, gD_ ) _∈F_ denote the dynamics for a given domain _D ⊂D_ . 

We can write the hybrid dynamics of the system as 


where _x ∈X_ , _u ∈U_ . The continuous dynamics can be represented: 


where _M_ ( _q_ ) : _Q →_ R<sup>_n×n_</sup> is the mass-inertia matrix, _H_ : _Q × T Q →_ R<sup>_n_</sup> the Coriolis and gravity terms, and _B ∈_ R<sup>_n×m_</sup> is the actuation matrix. Contact constraints are enforced via the wrench _F ∈_ R<sup>_h_</sup> and the constraint Jacobian _Jh_ ( _q_ ) _∈_ R<sup>_h×n_</sup> . Finally, the state is _x_ = [ _q, q_ ˙]<sup>_T_</sup> . See [25] for biped hybrid systems modeling details. 

We consider two domains: the single support phase (SSP) and the flight phase (FLT) with transitions (SSP _,_ FLT) (take off) and (FLT _,_ SSP) (impact). These have the associated reset maps: 


and 


with _I_ the identity matrix. 

The domains are defined by the robot’s contacts with the ground, while the guards are determined by the ground height. Each domain specifies the number of active contact forces and their associated Jacobians. 

## _B. Control Lyapunov Functions_ 

Control Lyapunov Functions (CLFs) are a classic tool in nonlinear control theory for designing certifiably stable controllers. Here we will be using the concept in the reward of an RL training routine. For a smooth nonlinear controlaffine system of the form (1), a continuously differentiable, positive definite function _V_ ( _x_ ) : _X →_ R is called an exponentially stabilizing CLF if the set 


is non-empty for all states _x_ in an open region around the origin, for scalar _λ >_ 0. This inequality guarantees that _V_ ( _x_ ) decreases along system trajectories, implying exponential convergence of the state _x_ to the origin. 

## III. REFERENCE GENERATION THROUGH OPTIMIZED DYNAMIC RETARGETING 

Although using human data directly is relatively easy because there is no need for a dynamics or contact model, there are a few issues with this approach: (a) there is still an embodiment gap between humans and humanoids, so a dynamically feasible motion on a human does not imply a feasible motion for a robot, (b) depending on the pipeline, the human data can be noisy, which then requires filtering before training, and (c) for steady-state locomotion, periodicity is required for the locomotion to be kinematically feasible, which in general is impossible to attain directly from human data. Therefore we introduce the use of a multiple shooting optimization problem to dynamically retarget the data, enforce periodicity, generate libraries of references, and otherwise clean the trajectory. 

To start, we assume that we have some human data that has been retargeted onto the robots kinematics. Then, we formulate an optimization problem whose cost encourages the robot to mimic this human data while respecting hard constraints. Ultimately, a running gait library with speeds 


Fig. 3: Visual depiction of the multiple shooting trajectory optimization problem. Two hybrid domains are shown and the node where they meet utilizes the associated reset map. Within each domain, a number of optimization nodes are used. The cost is tracking the human reference motion. 

from 1.2 m/s to 3.6 m/s is generated from single piece of human data from the LAFAN dataset [26]. To choose a portion of the dataset to use, we found a segment in which the human ran fast then we programatically extracted a single stride (both a single support and a flight phase) that was most periodic. To determine how periodic the reference trajectory is we symmetrically mirrored the joints, body positions, and orientations across the robot at the end of the stride and took the difference of this re-mapping compared to the original state. We only require a single stride as the other stride is always a mirror copy when traveling at steady state in a straight line. Fig. 3 gives a visual overview of the optimization process for enhancing human data. 

To optimize the data, the problem is formulated with multiple shooting nodes [27] which allows us to solve the optimization easier for unstable systems (i.e. a humanoid) compared to single shooting methods. We can also enforce hard state constraints, while other tools, like sampling based optimization, would struggle to do this. Solving a multiple shooting optimization problem for a hybrid system is difficult as to achieve global optimality the discrete decisions (the modes of the hybrid model) and the continuous actions should be chosen together. Solving this mixed-integer problem is computationally intensive and difficult to do. Therefore we choose to fix the hybrid domain sequence. We model running with two hybrid domains: the single support phase (SSP) and the flight phase (FLT). The time and order of the domains is extracted from the human data by thresholding the height of the foot above the ground. When in single support phase, a holonomic constraint and friction cone are used to enforce no foot slippage while in flight all ground reaction forces are set to 0. To encode a periodic steady state gait, the impact equations (6) are enforced on the reflected state. Therefore only a single stride is optimized and the other stride is always a mirror image. 

To enforce the domain sequence, we create a set of node indexes _J_ at which the domain must switch. Associated with each of these indexes are a corresponding guard and reset map. We denote the set of these guards and reset maps as _SJ_ and ∆ _J_ . The optimization only operates on discretized 

dynamics, which we denote as _f_<sup>¯</sup> _D_ and _g_ ¯ _D_ . This yields the full optimization problem as follows: 


where Φ =<sup>�</sup><sup>_N_</sup> _k_ =0<sup>_∥xk −x_</sup> _k_<sup>_d∥_</sup> _W_<sup>2with</sup><sup>_W_aweightingmatrix,</sup> _x_<sup>_d_</sup> _k_<sup>thestate(baseposition,orientation,jointangles,andall</sup> velocities) of the human reference, and _cu_ and _cx_ denote generic nonlinear input and state constraints. 

To solve the optimization problem, Casadi [28], Pinocchio [29], and IPOPT [30] are used. To fix a forward speed we can constrain a forward step length based on the total stride time. The creation of a gait library is efficient by using solutions from the faster gaits as a warm start for solves of slower gaits, and modifying the step length constraint while maintaining step time. This allows us to generate incrementally slower gaits, and prevents neighboring gaits from converging to drastically different solutions. Each gait in the library attempts to track the same human reference. 

Using optimization allows for rapid iteration, usually requiring seconds or minutes to solve for a gait. To transfer the gait to RL for training we fit a set of Bezier curves on desired “outputs”, denotes as _y_<sup>_d_</sup> ( _t_ ). These Bezier curves are what is tracked by the RL reward, as discussed next. We choose to track all the joints, the pelvis frame and each of the end effector frames. Each frame is an SE3 pose which is represented by a 3-vector for positions and a quaternion for orientations. Also, all the velocities of the joints and twists of the frames are tracked. 

IV. REWARD STRUCTURE AND RL DESIGN 

## _A. Reward Structure_ 

We analyze two separate reference tracking rewards: a mimic style reward where the bodies, their velocities, and joints are tracked in separate terms [13], [20], [11], and a CLF-RL reward where there is a single Lyapunov reward and a decrescent reward. Table I gives a list of all the rewards for each of the methods and their weights. Since all the mimic rewards have the same form (except the quaternion which uses a box minus operator) we only list the expression once. All of the numerical values can be found in our open source code<sup>1</sup> . Note that the regularization and contact rewards are used for every method and the goal conditioning is only used in certain ablations. 

_1) CLF Rewards:_ Motivated by control Lyapunov functions (CLFs), we embed a Lyapunov function and its decrescent conditioning into the reward to encourage Lyapunov stable behavior. A quadratic Lyapunov function is used as 

1https://github.com/Zolkin1/robot_rl/tree/main 

TABLE I: Reward terms used for each of the different training types. 

|**Reward Term**|**Expression**|**Weight**|
|---|---|---|
|**Regularization**|||
|Torque|_∥τ∥_<sup>2</sup><br>|_−_1_×_10<sup>_−_5</sup><br>|
|Action-rate|_∥at −at−_1_∥_<sup>2</sup><br>|_−_1_×_10<sup>_−_3</sup>|
|Torque limit|_∥|τt| −τ_lim_∥_<sup>+</sup><br>1<br><br>|_−_1_._0|
|Joint limit|_∥_(_q_<br>_−qt_)<sup>+ </sup>+(_qt −_¯_q_)<sup>+</sup>_∥_1|_−_1_._0|
|**CLF-RL**|||
|CLF tracking reward|exp<br>�<br>_−Vt_<br>_σv_<br>�<br><br>|10_._0|
|CLF decay penalty|clip<br>�˙_Vt_+_λVt_<br>_σ_ ˙_v_<br>_,_ 0_,_ 1<br>�|_−_5_._0|
|**Mimic**|||
|Generic tracking (10x)|exp(_−∥z −z_<sup>_d_</sup>_∥_<sup>2</sup>_/σz_)|1.5|
|**Contact**<br>Holonomic pos.|exp<br>�<br>_−_<sup>_∥p_st</sup><sup>_−p_0</sup><br>st<sup>_∥_</sup><br>_σp_<br>�<br><br><br>|4_._0|
|Holonomic vel.|exp<br>�<br>_−_<sup>_∥v_st</sup><sup>_∥_</sup><br>_σv_<br>�|2_._0|
|**Goal Conditioning**|||
|Linear (_x, y_) velocity|exp(_−∥v −v_<sup>_d_</sup>_∥_<sup>2</sup>_/σv_)<br><sup>˙˙</sup>|1.0|
|Yaw rate|exp(_−∥ϕ −ϕ_<sup>_d_</sup>_∥/σ_˙_ϕ_)|1.0|


we treat each output as a fully actuated double integrator [15]. Therefore the Lyapunov function takes the form of _V_ = _η_<sup>_T_</sup> _Pη_ where _P_ is the solution to the continuous time Ricatti equation and _η_ denotes the output tracking error: 


where _y_ ( _q_ ) is the function mapping the configuration to the measured output. 

The stability condition on the CLF is also put into the reward, where behaviors are penalized for not satisfying the CLF decrescent condition, i.e. if _V_<sup>˙</sup> _t_ + _λVt >_ 0. 

_2) Mimic Rewards:_ Mimic style rewards incentive tracking the reference trajectory too, but in multiple separate rewards and without the decrescent condition or the _P_ weighting matrix. Following common practice we choose all the weights to be the same and to track each group with a separate reward. The tracking groups include the joints, base position, base orientation, and end effector positions and orientations as well as all their linear and angular velocities, totaling to 10. The weight on the mimic rewards is set so that the total weight matches the total weight on the CLF rewards for a fair comparison. To tune the mimic rewards we started with the values given in [13] then tuned the standard deviations for performance in this application. 

_3) Goal Conditioning and Velocity Tracking:_ The mimic and CLF rewards are generally used only for reference tracking. Although the reference travels at a given velocity, it only moves straight, so the robot will not yaw or move laterally. There are two approaches that can be used at this point in the pipeline: (1) we can kinematically adjust the reference trajectory in the training loop to obey these motions or (2) we can add a goal conditioning reward. By kinematically adjusting the reference trajectory no additional reward is needed and therefore no additional tuning is required. Yet this is potentially a much weaker signal for the learning than goal conditioning. The goal conditioned reward incentivizes the robot’s root velocity to match the commanded velocity, even if this contradicts the reference. 

## _B. RL Design and Training_ 

We use IsaacLab and IsaacSim for GPU-accelerated physics simulation [31] and the PPO implementation from RSL-RL [32]. We use asymmetric actor critic where both the actor and critic networks use a fully connected feedforward architecture with three hidden layers, using the ELU activations at each layer. The actor’s observations include the base angular velocity, projected gravity, commanded velocity, joint angles, joint velocities, the previous action, and sin and cos phases as observations. The phase observations have a period of exactly one full gait period. Note that the reference motion is not an observation to the policy which makes deployment very easy. To facilitate learning, the critic receives additional privileged information, such as end effector and base frame linear and angular velocities, reference trajectory positions and velocities, and binary contact state indicators. 

The resulting policy should be able to track both joystick velocity commands and commands from a high level controller. To mitigate distribution shift with the commanded velocity, the policy is trained with three main groups of velocity commands: open loop velocity commands, heading control, and a P controller on both the heading and the lateral position. In this way the robot learns to obey the velocity commands while also being able to interface with a higher level controller. At episode reset the reference trajectory matching the desired speed is used for initialization, similar to what is done in [12]. Since it never starts standing, we instead choose to have 40% of the environments start on a configuration from the fastest walking reference (1 m/s), encouraging the policy to learn the transition from walking to running. The same transition is learned for the walking policy to facilitate the run to walk transition. The running policy is trained on speeds between 1.1 and 3.7 m/s. During an episode, the commanded forward speed is used to index into the reference library. 

Friction, mass, and motor properties are domain randomized. The full list and values can be found in our open source code. Additionally, a velocity-based push is periodically applied to the root of the robot. We find that sampling friction and gain randomization is very helpful for transferring the high speed running policy to hardware. The resulting control policy outputs joint angle setpoints at 50 Hz which are then tracked by high rate PD controllers. We use PD gains from [20] which over-damps the controllers. We find that this tends to prevent high frequency chatter on hardware. 

## V. RESULTS 

To evaluate the effect of the optimized reference motions and the different reward structures we perform two simulation experiments. Then we apply the controller to the realworld robot for indoor and outdoor testing. 

## _A. Reference Motion and Tracking Reward Ablation Study_ 

We compare the effects of using optimization to dynamically retarget the reference motion vs both generating a reference motion without any human data and tracking the kinematically retargeted trajectory. We also ablate the effect 

TABLE II: Velocity tracking error of the moving average (mean _±_ std) across policies and speeds. Bold indicates best per-metric value. Shading indicates policy with lowest total error per speed. 

||||||**CLF-RL**||||**Mi**|**mic**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||Kinematic Retar|geted Hum|an Data|Dyn|amic Opt. Human|Data|Dynamic O|pt. Human Data|Kinematic Reta|rgeted Hu|man Data|
|Speed|Metric|Goal + Adjust|3x Goal|+ Adjust|Adjust|Goal + Adjust|Goal Only|Goal + Adjust|3x Goal + Adjust|Goal + Adjust|3x Goal|+ Adjust|
||_evx_ (m/s)|0_._437_±_0_._054|0_._228_±_|0_._063|0_._251_±_0_._106|0_._157_±_0_._056|**0.139** _±_<br>0_._045|0_._293_±_0_._057|0_._236_±_ 0_._050|2_._281_±_0_._032|0_._438_±_|0_._110|
|1.4 m/s|_evy_ (m/s)<br>_e_ ˙_ψ_ (rad/s)|0_._223_±_0_._321<br>0_._214_±_0_._241|0_._196_±_ <br>0_._188_±_|0_._322<br> 0_._248|0_._319_±_0_._297<br>0_._202_±_0_._229|0_._221_±_0_._313<br>0_._192_±_0_._249|**0.198** _±_<br>0_._285<br>0_._216_±_<br>0_._258|0_._221_±_0_._310<br>0_._249_±_0_._264|0_._214_±_ 0_._310<br>**0.187** _±_ 0_._235|0_._264_±_0_._274<br>0_._259_±_0_._295|0_._201_±_<br>0_._200_±_|0_._325<br>  0_._248|
||_evx_ (m/s)|0_._335_±_0_._083|0_._237_±_|0_._062|**0.096** _±_0_._081|0_._129_±_0_._064|0_._104_±_<br>0_._058|0_._240_±_0_._065|0_._206_±_ 0_._055|1_._672_±_0_._033|0_._599_±_|0_._128|
|2.0 m/s|_evy_ (m/s)<br>_e_ ˙_ψ_ (rad/s)|0_._201_±_0_._311<br>0_._230_±_0_._254|**0.181** _±_ <br>**0.201** _±_|0_._309<br> 0_._244|0_._334_±_0_._289<br>0_._207_±_0_._234|0_._209_±_0_._310<br>0_._219_±_0_._256|0_._188_±_<br>0_._286<br>0_._232_±_<br>0_._264|0_._213_±_0_._299<br>0_._257_±_0_._273|0_._204_±_ 0_._299<br>0_._205_±_ 0_._234|0_._252_±_0_._273<br>0_._265_±_0_._293|0_._194_±_<br>0_._248_±_|0_._305<br>  0_._263|
||_evx_ (m/s)|0_._298_±_0_._077|0_._253_±_|0_._060|0_._316_±_0_._130|0_._107_±_0_._081|**0.081** _±_<br>0_._081|0_._177_±_0_._071|0_._162_±_ 0_._058|1_._065_±_0_._034|0_._605_±_|0_._121|
|2.6 m/s|_evy_ (m/s)|0_._185_±_0_._303|0_._178_±_|0_._298|0_._341_±_0_._288|0_._192_±_0_._299|**0.170** _±_<br>0_._281|0_._205_±_0_._289|0_._185_±_ 0_._292|0_._246_±_0_._278|0_._173_±_|0_._297|
||_e_ ˙_ψ_ (rad/s)|0_._248_±_0_._275|0_._217_±_|0_._255|**0.214** _±_0_._239|0_._238_±_0_._272|0_._245_±_<br>0_._279|0_._262_±_0_._284|0_._223_±_ 0_._250|0_._268_±_0_._292|0_._266_±_|0_._282|
||_evx_ (m/s)|0_._246_±_0_._081|0_._251_±_|0_._066|0_._674_±_0_._136|0_._083_±_0_._111|0_._076_±_<br>0_._123|**0.070** _±_0_._113|0_._090_±_ 0_._088|0_._456_±_0_._045|0_._484_±_|0_._103|
|3.2 m/s|_evy_ (m/s)<br>_e_ ˙_ψ_ (rad/s)|0_._171_±_0_._292<br>0_._262_±_0_._292|0_._172_±_ <br>0_._232_±_|0_._286<br> 0_._262|0_._342_±_0_._290<br>**0.222** _±_0_._248|0_._173_±_0_._289<br>0_._252_±_0_._289|**0.157** _±_<br>0_._278<br>0_._255_±_<br>0_._291|0_._197_±_0_._286<br>0_._273_±_0_._292|0_._177_±_ 0_._287<br>0_._235_±_ 0_._261|0_._239_±_0_._287<br>0_._271_±_0_._296|**0.157** _±_<br>0_._272_±_|0_._290<br>  0_._285|
|50<br>100<br>150<br>200<br>250<br>Reference Tracking Squared Error (_eTe_)|~~CLF~~<br>Mimic||||||out-perfor<br>ence track<br>data out-p<br>doesn’t ha<br>of the traje<br>This plo<br>the effect <br>that CLF-|ms kinemat<br>ing. We ca<br>erforms a h<br>ve human d<br>ctory is cr<br>t also answ<br>of reward s<br>RL rewards|ically retarge<br>n also see t<br>and-crafted d<br>ata. These res<br>itical for acc<br>ers part of ou<br>tructure on t<br> out-perform|ted human <br>hat the opt<br>ynamic op<br>ults imply t<br>urate tracki<br>r question (<br>racking by <br> the mimic|data f<br>imized <br>timizat<br>hat the<br>ng.<br>Q2) re<br> demon<br> rewar|or refe<br> huma<br>ion th<br>quali<br>gardin<br>stratin<br>ds. Th|
|0|Dynamic Op<br>Human Dat|t.<br>a<br>Kinematic<br>Human|Opt.<br>Data|Kinemati<br>targeting <br>Dat|c Re-<br>Human<br>a<br>Dyna|mic Opt.|highlights <br>|the fact tha<br>|t reward stru<br>|cture matte<br>|rs. In <br>|the ca<br>|


out-performs kinematically retargeted human data for reference tracking. We can also see that the optimized human data out-performs a hand-crafted dynamic optimization that doesn’t have human data. These results imply that the quality of the trajectory is critical for accurate tracking. 

This plot also answers part of our question (Q2) regarding the effect of reward structure on tracking by demonstrating that CLF-RL rewards out-perform the mimic rewards. This highlights the fact that reward structure matters. In the case of CLF-RL we design the reward to directly encourage theoretically sound stability to the reference. 

Fig. 4: Reference tracking comparison between reference and rewards types. Error bars show one std. dev. The dynamically optimized human data performs the best, and the CLF rewards outperform the Mimic rewards. Optimized retargeted references outperform kinematic human data retargeting. 

## _B. Velocity Tracking Ablation Study_ 

Now we can study which reward and reference combination yields the best velocity tracking which is critical to embedding dynamic motions in an autonomy stack. Velocity tracking performance is tested in Mujoco after the policies are trained in IsaacLab to help verify sim-to-sim performance. These policies are all trained to track a variety of speeds: _vx ∈_ [1 _._ 1 _,_ 3 _._ 7] _, vy ∈_ [ _−_ 0 _._ 75 _,_ 0 _.,_ 75] _, vϕ_ ˙ _∈_ [ _−_ 0 _._ 75 _,_ 0 _._ 75]. Here we ablate the reference type between dynamic optimized human data and kinematically retargeted human data and we also ablate the tracking reward between mimic and CLF-RL, then finally we examine the effect of kinematic trajectory adjustments, goal conditioning on a library of references and goal conditioning on a single kinematically retargeted human trajectory. We choose to compare the dynamic optimized human data because this performed best in our first ablation study and we choose to compare to kinematically retargeted human data with goal conditioning because this is a baseline that has been done before [8], [12], and is a very natural next step for a mimicbased pipeline that can re-play human motions. This helps to address the question whether using the library generation from the retargeting optimization provides value. 

of using the optimization, but without any dynamics (i.e. kinematic optimization). The RL policies are trained to track a single reference motion which allows us to examine the reference tracking alone without worrying about velocity tracking or libraries of references. There are two groups of policies trained here: one group using the CLF-RL rewards and the other using the mimic rewards. Within each group there is a policy trained on each of the 4 types of references. Other than the reward differences between groups and the reference motions between policies, the environments of the training are identical. It should be noted that for the dynamic optimization without human data that the optimizer would not converge at speeds over 3 m/s while all the human data based references are at 3.6 m/s. 

Once the policies are trained we generate the experiment data by spawning 200 robots in IsaacSim with domain randomization. We then play the simulation for 7 seconds giving the robots the single velocity command they were trained on. The reported error metric is the mean over the environments of the squared tracking error averaged across time. Fig. 4 shows the collected simulation data. There are two main takeaways from this plot: (1) Across both rewards we can see that optimizing the human data results in more accurate reference tracking than kinematic retargeting, and dynamic optimization out-performs kinematic optimization, (2) for every reference type the CLF reward yields a lower tracking error than the mimic rewards. This answers our question (Q1) by demonstrating that optimized human data 

We compare each of these policies tracking the given target speed (in the body forward direction) moving straight, as well as with the lateral and yaw rate inputs set to their max values: _vy_<sup>_d_=</sup><sup>_±_0</sup><sup>_._75and</sup><sup>_v_</sup> _ϕ_<sup>˙=</sup><sup>_±_0</sup><sup>_._75fordifferentsubsets</sup> of the simulation time. Domain randomization on the torso mass, CoM position, and D gains for each joint is applied in Mujoco and 50 trials at each speed are logged in Table II. 


Fig. 5: Outdoor long range experiments. The robot runs outdoors over distances of more than 150 m. The robot was given yaw targets in the global frame, a target position to track with body lateral motion and a feedforward velocity in the body forward direction. Lidar odometry and a P controller were used for global pose tracking. 

There are three main conclusions we can draw from the data: (1) although only kinematically adjusting the trajectory does achieve some amount of tracking, goal conditioning provides a better signal in the training process, (2) the CLF reward in general facilitates better velocity tracking, and (3) even across rewards the dynamic optimized reference trajectory yields better tracking than goal conditioning a single human trajectory, even if we increase the the goal conditioning weight by 3x. We increased the goal conditioning weights by 3x on the kinematic retargeting to address the fact that the reference motion is not consistent with the commanded velocity so there will inevitably need to be more deviation. This finishes the answer to our question (2): we can see that goal conditioning improves the velocity tracking but it is best paired with a dynamic reference library and a CLF tracking reward. 

The dynamic optimization of the human data also immensely improves the tracking at lower speeds which is mostly due to the fact that the reference motion from the human is a high speed run. Therefore the “style” that comes from that motion is most accurate for faster speeds. This is why in general the forward velocity error increases with slower speeds: because the reference is fast. The dynamic optimization allows us to get better tracking from a single human data trajectory for a much larger range of velocities. 

_C. Hardware Results, Integration with Autonomy Stack_ 

We deploy the policy on a Unitree G1 robot on an indoor treadmill environment, in large scale outdoor tests, and 

in autonomous obstacle avoidance scenarios. The running includes a full flight phase with the robot completely in the air. All policies and computation are run on-board using a mini-pc powered by the robot. Running the robot on an indoor treadmill (see Figs 1 and 2) demonstrates that the robot achieves high speeds (up to 3.3m/s) in a tight environment. Additionally, the robot has run more than 250 m consecutively on outdoor sidewalks. Fig. 5 shows two example runs. In these experiments a feedforward velocity is set by a remote and the robot tracks global yaw angles and tracks a global position target with only lateral motion using a P controller, which sends velocity commands to the running controller. In this way the running controller is operating in a layered control stack. We get position and yaw estimates from FastLio [33] at 10 Hz. The velocity data in Fig. 5 is obtained by finite differencing the odometry data. 

The running can also be controlled to perform collision avoidance within an autonomy stack. Specifically, we implement a model predictive control (MPC) algorithm that generates velocity commands for the running controller. This MPC layer uses real-time lidar scans to construct and update a local occupancy map, as in [34], which is then used to synthesize a smooth Poisson safety function [35]. We employ the Poisson safety function to formulate a control barrier function (CBF) collision avoidance constraint along the MPC horizon. The robot is commanded to run straight ahead while the MPC + CBF layer 1) characterizes the environment, 2) plans a new path, and 3) updates the running command 


Fig. 6: Autonomous collision avoidance while running with CBFconstrained MPC. The robot perceives it environment with a lidar, continuously re-computes a plan to avoid collisions, and passes the corresponding velocity commands to the running controller. With this architecture, the robot can avoid real-world obstacles while running. 

to avoid collisions. The resultant controller is agile enough to maintain forward speeds around 2 m/s while dodging detected obstacles. Fig. 6 shows a demonstration of this endto-end collision avoidance capability in a real-world outdoor environment. 

## VI. CONCLUSION 

In this paper we presented a pipeline for using optimization with hard constraints to dynamically retarget human data and then track this with CLF-RL. We studied both the effect of the reference motion and the reward on the reference and velocity command tracking. We concluded that goal conditioned control-guided RL (i.e. CLF-RL) in conjunction with dynamic optimized human data yields the best tracking performance. The resulting controller is applied on a real humanoid robot which achieves controllable and performant running in outdoor real world environments. Further, the running controller is integrated into an autonomy stack for perceptive real-time obstacle avoidance and navigation. 

## REFERENCES 

- [1] M. Raibert, _Legged Robots That Balance_ . The MIT Press, Mar. 2000. 

- [2] E. Westervelt, J. Grizzle, and D. Koditschek, “Hybrid zero dynamics of planar biped walkers,” _IEEE Transactions on Automatic Control_ , Jan. 2003. 

- [3] W.-L. Ma _et al._ , “Bipedal Robotic Running with DURUS-2D: Bridging the Gap between Theory and Experiment,” in _HSCC_ . ACM, 2017. 

- [4] K. Sreenath _et al._ , “Embedding active force control within the compliant hybrid zero dynamics to achieve stable, fast running on MABEL,” _The International Journal of Robotics Research_ , Mar. 2013. 

- [5] B. Morris _et al._ , “Achieving Bipedal Running with RABBIT: Six Steps Toward Infinity,” in _Fast Motions in Biomechanics and Robotics_ . Springer Berlin Heidelberg, 2006. 

- [6] A. D. Ames, “Human-inspired control of bipedal walking robots,” _IEEE Transactions on Automatic Control_ , vol. 59, no. 5, pp. 1115– 1130, 2014. 

- [7] D. Crowley _et al._ , “Optimizing Bipedal Locomotion for The 100m Dash With Comparison to Human Running,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , May 2023. 

- [8] Z. Li _et al._ , “Reinforcement Learning for Versatile, Dynamic, and Robust Bipedal Locomotion Control,” Jan. 2024, arXiv:2401.16889. 

   - [11] W. Xie _et al._ , “KungfuBot: Physics-Based Humanoid WholeBody Control for Learning Highly-Dynamic Skills,” Jun. 2025, arXiv:2506.12851. 

   - [12] X. B. Peng _et al._ , “DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills,” _ACM Transactions on Graphics_ , vol. 37, no. 4, pp. 1–14, Aug. 2018, arXiv:1804.02717. 

   - [13] J. P. Sleiman _et al._ , “ZEST: Zero-shot Embodied Skill Transfer for Athletic Robot Control,” Jan. 2026, arXiv:2602.00401. 

   - [14] N. Csomay-Shanklin and A. D. Ames, “B´ezier Reachable Polytopes: Efficient Certificates for Robust Motion Planning with Layered Architectures,” in _2025 American Control Conference (ACC)_ , 2025. 

   - [15] K. Li _et al._ , “CLF-RL: Control Lyapunov Function Guided Reinforcement Learning,” _IEEE Robotics and Automation Letters_ , Mar. 2026. 

   - [16] R. Batke _et al._ , “Optimizing Bipedal Maneuvers of Single Rigid-Body Models for Reinforcement Learning,” Jul. 2022, arXiv:2207.04163. 

   - [17] H. J. Lee, S. Hong, and S. Kim, “Integrating Model-Based Footstep Planning with Model-Free Reinforcement Learning for Dynamic Legged Locomotion,” in _2024 International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, Oct. 2024, pp. 11 248–11 255. 

   - [18] R. Grandia _et al._ , “Design and Control of a Bipedal Robotic Character,” in _Robotics: Science and Systems XX_ , Jul. 2024, arXiv:2501.05204. 

   - [19] F. Liu _et al._ , “Opt2Skill: Imitating Dynamically-feasible Whole-Body Trajectories for Versatile Humanoid Loco-Manipulation,” Oct. 2025, arXiv:2409.20514. 

   - [20] Q. Liao _et al._ , “BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion,” Aug. 2025, arXiv:2508.08241. 

   - [21] T. Zhang _et al._ , “HuB: Learning Extreme Humanoid Balance,” Aug. 2025, arXiv:2505.07294. 

   - [22] T. He _et al._ , “ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills,” Apr. 2025, arXiv:2502.01143. 

   - [23] C. Pan _et al._ , “SPIDER: Scalable Physics-Informed Dexterous Retargeting,” Feb. 2026, arXiv:2511.09484. 

   - [24] Z. Olkin _et al._ , “Chasing stability: Humanoid running via control lyapunov function guided reinforcement learning,” 2025. [Online]. Available: https://arxiv.org/abs/2509.19573 

   - [25] J. Grizzle _et al._ , “3D Bipedal Robotic Walking: Models, Feedback Control, and Open Problems,” _IFAC Proceedings Volumes_ , Sep. 2010. 

   - [26] F. Harvey _et al._ , “Robust Motion In-Betweening,” _ACM Transactions on Graphics_ , 2020. 

   - [27] M. Diehl _et al._ , “Fast Direct Multiple Shooting Algorithms for Optimal Robot Control,” in _Fast Motions in Biomechanics and Robotics_ , M. Diehl and K. Mombaur, Eds. Springer Berlin Heidelberg, 2006, vol. 340, pp. 65–93, series Title: Lecture Notes in Control and Information Sciences. 

   - [28] J. Andersson _et al._ , “CasADi - A software frameowrk for nonlinear optimization and optimal control,” _Mathematical Programming Computation_ , vol. 11, pp. 1–36, 2019. 

   - [29] J. Carpentier _et al._ , “The Pinocchio C++ library : A fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives,” in _2019 IEEE/SICE International Symposium on System Integration (SII)_ . IEEE, Jan. 2019, pp. 614–619. 

   - [30] A. W¨achter and L. T. Biegler, “On the implementation of an interiorpoint filter line-search algorithm for large-scale nonlinear programming,” _Mathematical Programming_ , vol. 106, no. 1, pp. 25–57, Mar. 2006. 

   - [31] NVIDIA _et al._ , “Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning,” Nov. 2025, arXiv:2511.04831. 

   - [32] N. Rudin _et al._ , “Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning,” Aug. 2022, arXiv:2109.11978. 

   - [33] W. Xu and F. Zhang, “FAST-LIO: A Fast, Robust LiDAR-inertial Odometry Package by Tightly-Coupled Iterated Kalman Filter,” Apr. 2021, arXiv:2010.08196. 

   - [34] E. Yamaguchi _et al._ , “Layered safety: Enhancing autonomous collision avoidance via multistage cbf safety filters,” 2026. [Online]. Available: https://arxiv.org/abs/2603.00338 

   - [35] G. Bahati, R. M. Bena, and A. D. Ames, “Dynamic safety in complex environments: Synthesizing safety filters with poisson’s equation,” _Robotics: Science and Systems (RSS)_ , 2025. 

- [9] K. Green _et al._ , “Learning Spring Mass Locomotion: Guiding Policies with a Reduced-Order Model,” Mar. 2021, arXiv:2010.11234. 

- [10] Z. Li _et al._ , “Reinforcement Learning for Robust Parameterized Locomotion Control of Bipedal Robots,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, May 2021. 

