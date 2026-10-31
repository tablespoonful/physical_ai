---
title: "RPG: Robust Policy Gating for Smooth Multi-Skill Transitions in Humanoid Fighting"
date: "2026-04-23"
authors: "Yucheng Xin; Jiacheng Bao; Yubo Dong; Xueqian Wang; Bin Zhao; Xuelong Li"
url: https://arxiv.org/abs/2604.21355
pdf: https://arxiv.org/pdf/2604.21355
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.21355)** / [論文ページ](https://arxiv.org/abs/2604.21355)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **RPG: Robust Policy Gating for Smooth Multi-Skill Transitions in Humanoid Fighting** 

Yucheng Xin<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> , Jiacheng Bao<sup>2</sup><sup>_∗_</sup> , Yubo Dong<sup>3</sup><sup>_,_2</sup> , Xueqian Wang<sup>1</sup> , Bin Zhao<sup>2</sup> Xuelong Li<sup>2</sup> , Junbo Tan<sup>1</sup><sup>_†_</sup> , Dong Wang<sup>2</sup><sup>_†_</sup> 

**_Abstract_ — Humanoid robots have demonstrated impressive motor skills in a wide range of tasks, yet whole-body control for humanlike long-time, dynamic fighting remains particularly challenging due to the stringent requirements on agility and stability. While imitation learning enables robots to execute human-like fighting skills, existing approaches often rely on switching among multiple single-skill policies or employing a general policy to imitate input reference motions. These strategies suffer from instability when transitioning between skills, as the mismatch of initial and terminal states across skills or reference motions introduces out-of-domain disturbances, resulting in unsmooth or unstable behaviors. In this work, we propose RPG, a hybrid expert policy framework, for smooth and stable humanoid multi-skills transition. Our approach incorporates motion transition randomization and temporal randomization to train a unified policy that generates agile fighting actions with stability and smoothness during skill transitions. Furthermore, we design a control pipeline that integrates walking/running locomotion with fighting skills, allowing humanlike long-time combat of arbitrary duration that can be seamlessly interrupted or transit action policies at any time. Extensive experiments in simulation demonstrate the effectiveness of the proposed framework, and real-world deployment on the Unitree G1 humanoid robot further validates its robustness and applicability.** 

## I. INTRODUCTION 

Humanoid robots have shown remarkable progress in recent years, demonstrating agile locomotion [1], [2], [3], [4], [5], dexterous manipulation [6], [7], [8], [9], [10], [11], [12] , and even athletic motions [13], [14], [15]. A complex, practical, and compelling testbed task is enabling humanoid robots to perform human-like fighting actions such as jumping [4], [14], [2], punching [16], sword swings, and kicking [15], [17]. Such task requires whole-body coordination, rapid skill switching, and stable contact control, which place much higher demands on robustness and agility compared to conventional locomotion or manipulation. An ideal humanoid whole-body control policy for fighting would resemble controlling a character in a role-playing game (RPG), where a user can seamlessly trigger and execute diverse combat skills in real time. Achieving this level of flexible and fluid multi-skill control in physical humanoid robots, however, remains a significant challenge. 

Recent advances in imitation learning have enabled robots to learn complex motion skills from reference motion tra- 

> 1Center for Artificial Intelligence and Robotics, Shenzhen International Graduate School, Tsinghua University, China, _{_ xin-yc23@mails., wang.xq@sz., tjblql@sz. _}_ tsinghua.edu.cn, 

> 2Shanghai AI Laboratory, 3Shanghai Jiao Tong University 

> _†_ Corresponding author, _∗_ indicates equal contribution 

jectories. While effective for single-skill learning [13], [15], extending imitation learning to multiple diverse skills is nontrivial. Naive solutions, such as switching between separate policies or using a general policy to mimic diverse reference motions [16], [18], [19], [17], [20], often lead to instability in policy deployment. This is primarily due to mismatched initial and terminal states between reference sequences, leading to out-of-domain disturbances during skill transitions. As a result, robots suffer from jerky or unsmooth motions, particularly when attempting to concatenate different fighting skills for practical human-like combat. 

To overcome these challenges, we propose Robust Policy Gating (RPG), a hybrid expert policy framework designed for multi-skill imitation learning with smooth skill transitions. Our method first trains multiple expert policies on distinct categories of fighting skills. During training, we introduce policy-transition randomization and temporal randomization to explicitly simulate mid-sequence truncations and arbitrary skill switches, forcing each expert to learn robustness against discontinuous motions. Once the experts converge, we freeze them and train a lightweight gating network that outputs weighted combinations of their actions, regularized with torque and contact smoothness objectives. The resulting hybrid expert policy controller enables fluid switching across skills, even under abrupt transitions. 

Extensive experiments in simulation demonstrate that RPG effectively generates agile and seamless fighting behaviors, even under abrupt action switches. Beyond isolated fighting skills, we design a control pipeline that integrates locomotion and combat behaviors. When no fighting action is triggered, the robot maintains a locomotion state; when a skill is commanded, the system seamlessly transitions to the specified action, supporting arbitrary interruptions and varying durations. This design provides a game-like interface for controlling humanoid robots, akin to RPG game combat mechanics. Furthermore, we validate the approach on the Unitree G1 humanoid robot, confirming that RPG transfers successfully to real hardware and enables robust execution of high-agility fighting motions. 

In conclusion, our contributions are as follows: 

1. We introduce Robust Policy Gating (RPG), the framework enabling smooth and robust multi-action transitions for humanoid fighting behaviors. 

2. We introduced a novel method incorporating both policy-transition and temporal randomization during expert policies training, and a new gating network for smoothness regularization, achieving robustness against 


Fig. 1. **Policy Transition Demonstration.** We conducted policy transition tests for robotic combat motions using the proposed RPG. Punching and Sword Swing motions primarily involve the upper body, whereas Jumping and Kicking motions are mainly lower-body actions. We demonstrate 4 distinct policy transition combinations here, highlighting the motion capabilities during transition between upper and lower-body strategies. **a)** Jumping introduces significant instability for humanoid robot. However, by repeatedly executing the jumping policy in succession, we achieved a triple jump sequence. **b)-d)** Other policy transition combinations. 


Fig. 2. **Recovery Tests.** Due to the short duration of the Jumping motion, it was excluded from consideration. For the other motions, the robot demonstrated the ability to avoid foot sliding and resume a stable, human-like standing posture from any interrupted state during execution. 

disturbances during policy transitions and stable fusion of multiple expert policies. 

3. We designed a pipeline that integrates locomotion and fighting skills, allowing users to control the robot for prolonged combat in a manner similar to playing an action RPG game. 

## II. RELATED WORKS 

## _A. Imitation Learning for Humanoid Whole-Body Control._ 

Recent advances in imitation learning have empowered humanoid robots to acquire dynamic and naturalistic skills by tracking and synthesizing complex human motions. For agile behaviors, works such as [13], [21] focus on jumping, while PBHC [15] demonstrates multi-step motion reproduction for Kungfu and dancing. BeyondMimic [14] further introduces a guided diffusion framework that enables humanoids to execute highly challenging motions, including spins, sprinting, 

and cartwheels, while also supporting zero-shot task-specific control. 

Expressive and resilient skills have also been explored: Exbody [22] and Exbody2 [23] focus on dance imitation, whereas Embrace Collisions [24] tackles recovery behaviors. Humanoid parkour has been showcased in [2], [25]. For contextual imitation, Videomimic [26] leverages everyday human videos with environment reconstruction to teach humanoids real-world tasks such as stair climbing, sitting, and standing. 

On scalable and general motion tracking, GMT [19] employs adaptive sampling and a motion mixture-of-experts (MoE) to capture diverse skills with a single controller, while BumbleBee [27] distills clustered experts into a generalist policy for whole-body humanoid control. HuB [17] further integrates motion refinement, balance-aware learning, and robustness training to master extreme balancing poses such 

as the Swallow Balance and Bruce Lee’s Kick. 

Beyond full-body imitation, recent efforts extend to manipulation and sports. OKAMI [28] and HumanPlus [29] emphasize upper-body skills for object interaction, and HITTER [20] combines model-based planning with reinforcement learning to achieve agile, stable table-tennis rallies. 

## _B. Policy Switching and Motion Transition._ 

Enabling diverse robot skills often involves skill composition or switching mechanisms, such as R2S2’s composable skill library [8] or automatic gait discovery [30]. ASE [31] learns a continuous latent skill space through adversarial imitation, enabling smooth skill transitions without predefined segmentation. Other methods use contextual expert switching: [32] uses uncertainty to switch between RL and BC. For robustness, [33] formalizes policy selection as a multi-armed bandit problem. 

Generating smooth and stable transitions between motions is critical for robust robotic performance and has been addressed through various methods. These include dedicated transition policies like the Expert Composer [34] for skill sequencing, as well as techniques that engineer smoothness directly into controllers through regularization [35], command interpolation [10], and comfort-oriented rewards [36]. Our Robust Policy Gating (RPG) framework builds on this line of work by achieving seamless transitions between diverse skills through a specific randomization method and a learned gating network. 

## III. METHODS 

## _A. Framework._ 

Our proposed Robust Policy Gating (RPG) framework is designed to learn a unified control policy that seamlessly executes and transitions between multiple dynamic fighting skills. The methodology consists of four core components: (i) data acquisition and motion retargeting, (ii) robust expert policies training via policy-transition and temporal randomization, (iii) a gating network for smooth policy fusion, (iv) sim-to-sim and sim-to-real validation and integration with a locomotion policy for a complete control pipeline. The overall framework is depicted in Fig. 3. 

## _B. Data Process._ 

We begin by collecting motion references from two sources: (i) existing public motion datasets [37], and (ii) video recordings obtained from demonstrations or online footage. To convert raw video into motion sequences, we employ the GVHMR [38] framework, which extracts 3D human motions from monocular video. The resulting motion clips are then processed using the PHC retargeting method [39], adapting the human motions to the humanoid robot’s kinematic structure while preserving key dynamics. From this pipeline, we obtain a set of representative actions relevant to humanoid fighting: punching, jumping, sword swings, and kicking. These action segments form the basis for policy training, generating kinematically feasible reference motion sequences _M_<sup>_r_</sup> _m_<sup>_, m ∈M_,where</sup><sup>_M_=</sup><sup>_{j, p, s, k}_represents</sup> motions of jumping, punching, sword swing and kicking. 

## _C. Expert Policy Training with Randomization Strategies._ 

For each action category, we train a dedicated policy _π_<sup>_m_</sup> _, m ∈ M_ using Proximal Policy Optimization (PPO). Each policy is optimized to imitate its corresponding reference motion _M_<sup>_r_</sup> _m_<sup>.Allpoliciessharethesameenvironment,</sup> but only one policy is updated per step. This means that the update of each policy is unaffected by the other policies, but only influenced indirectly through the changes in the robot’s state caused by other policies in the simulation environment. 

For imitation learning–based multi-policy-transfer smoothness and robustness, the primary challenge is that outof-domain disturbances during policy switching arise from large discontinuities in the reference motions encoded by different policies. To address this issue, we take a twofold approach: (i) introducing policy-transition scenarios during training, and (ii) injecting sudden perturbations to the robot’s body state through temporal discontinuities in the reference motions. In particular, to improve the smoothness and robustness against action transitions, we introduce two forms of randomization operation during training: 

1) **Randomization for Policy Transition Robustness:** A key innovation in our training pipeline is the incorporation of a randomization method to explicitly train for transition scenarios, moving beyond naive single-skill imitation. During training, an episode does not necessarily consist of a single full motion playback. The length of a complete episode _Te_ is defined as the sum of the durations of the all categories of reference motions _Tm, m ∈ M_ . At any timestep _t_ , with fixed probability _ptrans ∈_ [0 _,_ 1], a transition event is triggered stochastically as follows: 


If _bt_ = 1, the current policy _π_<sup>_m_</sup> and reference motion _Mm_<sup>_r_is</sup> abruptly truncated. Based on the current simulator and robot state, the update of the original policy network _π_<sup>_m_</sup> is frozen, and the training randomly switches to another action-specific policy _π_<sup>_m′_</sup> , where _m_<sup>_′_</sup> is sampled uniformly from the motion set _M_ , with the reference motion _Mt_ reset accordingly. 


This process forces each expert _π_<sup>_m_</sup> to learn to start and terminate from a broad distribution of states, effectively simulating the situation that frequent interruptions and transitions in combat scenarios, and improving the robustness when policy switching. 

2) **Randomization for Temporal Discontinuities:** When sampling a reference state from _M_<sup>_r_</sup> _m_<sup>,wedonotstrictly</sup> follow consecutive frames. With a fixed probability _pjump_ , the reference motion at the next timestep _Mt_ +1 is randomly replaced by the reference motion from _k ∼U{_ 1 _, K}_ steps 


Fig. 3. **Framework. a)** Collection of human demonstration data for combat motions (jumping, punching, sword swing, kicking), with video-based motion conversion and retargeting to adapt to the Unitree G1 humanoid robot; **b)** Expert networks are trained for each motion type via imitation learning. All experts are loaded concurrently, though only one policy is updated per step. Policy-transition and temporal randomization are introduced: at any time step, the system may stochastically switch to a new motion, freezing the current policy, resetting the reference motion, and enabling a new policy to update. Additionally, random time-jumping in reference motion sequences is applied to simulate abrupt motion changes and enhance robustness. **c)** After the expert policies convergence, the expert policies are frozen while the randomization method remains active. A gating network is trained to blend outputs from the experts. The action output is decomposed into components for upper and lower bodies, and the gating network computes weighted combinations for each. The gating network is optimized with smoothness regularization to improve motion fluency during policy transition. 

**Algorithm 1** Randomization Strategies 

- 1: Load policies for all categories of motions 

- 2: Choose one policy _π_<sup>_m_</sup> _, m ∈ M_ to be activated, others are frozen 

- 3: **for** each timestep _t_ in an episode **do** 

- 4: Sample current reference frame _Mt_ = _M_<sup>_r_</sup> _m,t_ 

- 5: Execute action _at ∼ π_<sup>_m_</sup> ( _St_ ) 

- 6: Update policy _π_<sup>_m_</sup> 

- 7: — Randomization for Policy Transition — 

- 8: **if** Bernoulli( _ptrans_ ) = 1 **then** 

- 9: Freeze update of _π_<sup>_m_</sup> Sample New Reference Motion _m_<sup>_′_</sup> _∈ M_ 

- 10: Activate a new policy _π_<sup>_m_</sup> = _π_<sup>_m′_</sup> 

- 11: Reset reference motion _Mt_ +1 = _M_<sup>_r_</sup> _m_<sup>_′_</sup> _,t_ =0 

- 12: **end if** 

- 13: — Randomization for Temporal Discontinuities — 

- 14: **if** Bernoulli( _pjump_ ) = 1 **then** 

- 15: Replace _M_<sup>_r_</sup> _m,t_ +1<sup>with</sup><sup>_Mr_</sup> _m,t_ + _k_<sup>,</sup><sup>_k∼U_(1</sup><sup>_, K_)</sup> 

- 16: **end if** Update States _St_ 

malized in pseudocode as presented in Algorithm 1. This approach of imitation learning with randomized cross-policy and cross-temporal domain sampling effectively simulates two critical aspects of combat motions: the necessity to terminate ongoing actions and transition to new strategies at any moment, and the ability to handle abruptly changing motion references. Consequently, it significantly enhances the robustness of each individual expert policy. 

For the above expert networks, we employ an Asymmetric PPO algorithm for imitation learning training. All expert networks have an identical architecture. Upon completion of the described training process, we obtain multiple expert networks that can operate independently to execute their respective reference motions. In the Asymmetric PPO framework, the observations for the actor and critic networks are detailed in Table I. All networks employ an MLP architecture. The output of all networks is a 23-dimensional joint actions _a ∈_ R<sup>23</sup> for the robot. 

We define many of the reward terms in the following format: 

- 17: **end for** 

ahead. 


This compels the policy to handle non-smooth, discontinuous reference commands, significantly improving its robustness to timing misalignments during transitions. 

The aforementioned randomization techniques are for- 


where the _w_<sup>_e_</sup> is weight for expert policies training, meanwhile _w_<sup>_g_</sup> firstly mentioned in Table. II is for the gating policy training. The update rule for the _σsi_ value follows the same definition as presented in the PBHC [15]. 

The reward function used during training is outlined in Table II. The reward is primarily divided into two components: 

TABLE I 

OBSERVATION SPACE FOR THE EXPERT NETWORKS 

|**Observation States**|**Actor Dims**|**Critic Dims**|
|---|---|---|
|Joint Positions|23|23|
|Joint Velocities|23|23|
|Root Angular Velocity|3|3|
|Root Projected Gravity|3|3|
|Actions|23|23|
|Reference Motion Phase|1|1|
|History (above)|76_×_4|76_×_4|
|Reference Joint Positions|23|23|
|Reference Joint Velocities|23|23|
|Reference Body Positions|81|81|
|Future Reference Joint Positions|23_×_2|23_×_2|
|Future Reference Body Positions|81_×_2|81_×_2|
|Root Linear Velocity|-|15|
|Body Position Difference|-|81|
|Randomized Base CoM offset|-|3|
|Randomized Base Link Mass|-|22|
|**Total Dimensions**|**715**|**836**|


one for motion tracking, and another for ensuring smooth task execution. For the latter component, we specifically introduce penalties on the absolute values of output torques and their temporal differences to ensure motion fluency. Furthermore, to prevent biologically implausible phenomena such as foot sliding during policy transitions, where feet might drag along the ground to reach target positions, we designed additional reward terms that penalize foot-ground sliding and encourage prolonged foot aerial phases. This design promotes lifting the feet during movement, better mimicking natural human motion characteristics. 

TABLE II 

REWARDS OF EXPERT POLICIES 

|**Rewards**|**Expression**|_w_<sup>_e_</sup>|_w_<sup>_g_</sup>|
|---|---|---|---|
|Joint Positions|_R_(_qt_)|1.0|0.3|
|Joint Velocities|_R_( ˙_qt_)<br>|1.0|0.3|
|Body Positions|_R_(_pt_)|2.0|0.6|
|Body Rotations|_R_(_θt_)|0.5|0.2|
|Body Velocities|_R_( ˙_pt_)<br>|0.5|0.2|
|Body Ang-Velocities|_R_( ˙_wt_)<br>|0.5|0.1|
|Upper Body Positions|_R_(_p_<sup>_up_</sup><br>_t_ <sup>)</sup><br>|4.0|0.2|
|Feet Positions|_R_(_p_<sup>_feet_</sup><br>_t_<br>)<br><br>|1.0|0.6|
|Max Joint Positions|exp (_−||qt −q_<sup>_r_</sup><br>_t _<sup>_||∞/σmj_)</sup><br>|1.0|1.0|
|Joint Position Limits|I(_qt /∈_[_qmin, qmax_])|-10.0|-5.0|
|Joint Velocity Limits|I( ˙_qt /∈_[ ˙_qmin,_ ˙_qmax_])|-5.0|-3.0|
|Joint Torque Limits|I(_τt /∈_[_τmin, τmax_])<br>|-5.0|-4.0|
|Feet Contact Forces|min(_||F _<sup>_feet _</sup>_−_400_||_<sup>2</sup><br>2<sup>_,_ 0)</sup><br>|-1e-2|-1e-2|
|Feet Air Time|I[_Tair >_0_._3]<br><br>|-1.0|-1.0|
|Feet Slipping Penalty|_||v_<sup>_feet_</sup>_||_<sup>2</sup><br>2 <sup>_·_ I[</sup><sup>_||F feet||_2</sup> <sup>_>_ 1]</sup><br>|-3.0|-2.0|
|Torque|_||τ||_<sup>2</sup><br>2|-1e-6|-1e-6|
|Collision Penalty|I_collision_|-30.0|-20.0|
|Termination Penalty|I_termination_|-300.0|-300.0|
|Alive|1<br>|0.8|0.8|
|Torque Difference|_||τt −τt−_1_||_<sup>2</sup><br>2<br>|-|-0.5|
|Task ID Check|exp(_−||ct −c_<sup>_r_</sup><br>_t _<sup>_||_2</sup><br>2<sup>)</sup>|-|2.0|


During the training process, we also incorporated elements of curriculum learning by progressively tightening the precision requirements for motion tracking errors, thereby enhancing the convergence effectiveness of the policy. 

## _D. Gating Policy Training._ 

Once the individual expert policies are obtained, and to involve the smoothness constraints on controlling, we freeze their parameters and design a gating network to produce smooth transitions while leveraging the motion capabilities of existing expert policies. Since the upper and lower limbs play different roles in the tracking task during motion execution, we define the dimension of the gating network output _w_ ˆ as twice the number of expert policies _w_ ˆ _∈_ R<sup>2</sup><sup>_N_</sup> . Specifically, separate weight coefficients are assigned to the outputs of each expert policy for the upper and lower limbs, which are then applied independently to generate the final actions. The gating network receives the current robot states _St_ , which are the same as the input states of expert policies, and an optional task embedding _ct_ that encodes the highlevel combat instruction. It outputs a weight vector _w_ ˆ _t_ = [ ˆ _wt_<sup>_u,_1</sup> _, . . . , w_ ˆ _t_<sup>_u,N_</sup> _, w_ ˆ _t_<sup>_l,_1</sup><sup>_, . . . ,w_ˆ</sup> _t_<sup>_l,N_</sup> ] through a softmax layer, where _N_ denotes the number of expert policies, _{u, l}_ represents the weights for upper and lower body actions. The final control action _a_<sup>_g_</sup> is then computed as a weighted mixture of the experts: 


specifically, _ct_ is an _N_ -dimensional one-hot vector, where the _i_ -th entry is set to 1 for specific motion index( _m_ ), and all other entries are 0. 


The training procedure of the gating network follows the same scheme as that of the expert networks, adopting an asymmetric PPO structure. The actor policy is employed as a MLP network, followed by a softmax output. This lightweight architecture ensures real-time inference on physical hardware. In addition, we regularize the gating output with a temporal smoothness constraint to discourage rapid fluctuations between experts, which can otherwise result in discontinuous or unstable motions. 

Its observation state is identical to that listed in Table I, but further augmented with a task vector _ct_ in actor network. During algorithm updates, the gating network places greater emphasis on task scheduling, as well as the smoothness and stability of output torques. Therefore, its reward design differs from that of the expert networks. As shown in Table II, the single-step reward is defined as: 


## _E. Validation and Deployment._ 

After completing the training of all experts and gating policies, we validated our framework in the MuJoCo simulation environment and subsequently deployed it onto the Unitree G1 humanoid robot. 

Additionally, we specifically designed a control pipeline for robotic combat tasks. In the real-world control pipeline, 

action commands are issued via a game joystick similar to playing an RPG action game: holding down a specific button triggers the execution of the corresponding action policy, while the robot defaults to locomotion mode when no command is given. For locomotion, we integrate a policy trained with the RoboMimic framework, ensuring stable operation of the robot outside combat tasks. We implemented a complete control pipeline that enables RPGstyle interaction: the robot can execute any fighting skill on demand, smoothly stop and switch between different actions at arbitrary timesteps, and seamlessly return to a locomotion state when no fighting commands are issued. 

## IV. EXPERIMENTS 

## _A. Experimental Setup._ 

We ultimately recorded monocular video data and converted them into SMPL-format motions, which were then retargeted to the Unitree G1 humanoid robot. Four representative fighting skills are considered: _punching_ , _jumping_ , _sword swing_ , and _kicking_ . Both the _punching_ and _sword swing_ motions are composed of multiple consecutive striking actions combined to form a complete movement. Based on the proposed RPG framework, we obtained multiple imitationlearning expert policies capable of executing individual actions, as well as a multi-policy control pipeline that enables stable and seamless policy transitions. The experiments were trained on the IsaacGym simulation platform using an RTX 4090 GPU, with sim-to-sim policy validation performed in MuJoCo prior to deployment. The control frequency on the real robot is 50 Hz. Finally, the proposed framework was successfully deployed on the real Unitree G1 robot. As illustrated in Fig. 1 and Fig. 2, the final demonstration shows that the robot not only executes individual expert actions effectively, but also achieves smooth and stable transitions across multiple action policies. 

The proposed RPG framework makes two primary contributions: (i) a training methodology incorporating policytransition and temporal randomization mechanisms, and (ii) a gating network for policies merging. To validate the effectiveness of the proposed RPG framework, we conduct ablation studies, which will be discussed in the following sections. 

## _B. Baseline and Metrics._ 

We employ the ASAP framework as the baseline for experimental comparisons, and all subsequent comparative experiments are conducted based on variants of the ASAP framework. 

To evaluate the effectiveness of imitation learning for motion tracking, we introduce the following metrics to evaluate joint tracking performance: _Empjpe_ (mean per-joint position error), _Empjae_ (mean per-joint angle error), _Empjve_ (mean per-joint velocity error), and metrics to assess root body tracking: _Erootpe_ (root position error), _Erootre_ (root rotation error), _Erootve_ (root velocity error). 

To evaluate the robustness and control stability of the algorithm during cross-policy transitions, we propose a success 

rate metric denoted as _Esucc,n_<sup>_a→b_,whichrepresentsthesuccess</sup> rate of the robot completing the transition from motion _a_ to motion _b_ across _n_ experimental trials. The motion indexes can be described as _j_ for jumping, _p_ for punching, _s_ for sword swing, and _k_ for kicking. 

Additionally, we introduce _Emaccj_ (mean acceleration of joints) to evaluate the smoothness of robot control. 

## _C. Main Results._ 

For the overall framework, our investigation focuses on the following key questions: 

## **Q1: The impact of policy-transition and temporal randomization on individual expert networks.** 

To explore the impact of the RPG method on individual expert policies, we design a set of controlled experiments. The baseline approach involves using the ASAP framework to train imitation learning policies for each action separately. In contrast, the experimental group employs the RPG framework, where multiple expert networks are trained simultaneously using policy-transition and temporal randomization. After the training convergence, the corresponding individually trained expert networks from RPG are compared with those from the baseline. 

TABLE III 

EXPERT POLICIES COMPARISON OF TRACKING EFFECTIVENESS 

|**Motions**|**Experiments**|||**Met**|**rics**|||
|---|---|---|---|---|---|---|---|
|||_Empjpe_|_Empjae_|_Empjve_|_Erootpe_|_Erootre_|_Erootve_|
|Jumping|baseline<br>RPG (ours)|**0.1492**<br>0.1594|**0.0346**<br>0.0382|**1.6895**<br>1.8231|0.1521<br>**0.1387**|1.5218<br>**1.3874**|**0.2915**<br>0.3342|
|Punching|baseline<br>RPG (ours)|0.1428<br>**0.1321**|0.0315<br>**0.0283**|**1.5218**<br>1.6254|0.1289<br>**0.1164**|**1.2186**<br>1.3247|**0.2489**<br>0.2753|
|Sword Swing|baseline<br>RPG (ours)|0.1689<br>**0.1524**|**0.0321**<br>0.0368|1.8927<br>**1.7346**|**0.1298**<br>0.1423|1.4672<br>**1.3429**|0.3028<br>**0.2784**|
|Kickin|baseline|**0.1412**|**0.0302**|1.7825|0.1357|1.3984|**0.2631**|
|g|RPG (ours)|0.1537|0.0339|**1.6428**|**0.1225**|**1.2873**|0.2896|


We evaluated the policies trained for jumping, punching, sword swing, and kicking using the aforementioned motion tracking metrics. For lower-body dominant motions such as jumping and kicking, the tracking performance of RPG is generally weaker. This may be attributed to the greater disturbance impact on the lower limbs when handling abrupt motion transitions. Meanwhile, the baseline method shows relatively stronger performance in velocity tracking, likely because the robot’s control is subject to safety constraints when sudden changes in reference motion cause sharp velocity variations. 

However as the results, as shown in the table, indicate that there is no significant difference between the two methods in terms of motion tracking performance. 

## **Q2: The effect of the proposed framework on robustness in multi-policy transitions.** 

To evaluate the robustness of the control methods, we aim to determine which approach enables the robot to maintain better motion completion when facing out-of-domain states and disturbances during policy transitions. For this purpose, we employ the _Esucc,n_ metric to assess whether the robot can successfully execute motion switches without falling. In this 

set of baseline experiments, expert networks trained using the ASAP framework are directly integrated into the pipeline to perform policy switching. For the experimental group, the pipeline incorporates the framework trained with the RPG method. Each motion transition is repeated 20 times, and the success rate is calculated. 

TABLE IV 

SUCCESS RATE OF TRANSITION 

|**Start (a)**|_E_<sup>_a→b_</sup><br>_succ_20||**Target **|**Motion (b)**||
|---|---|---|---|---|---|
||_,_|Jumping|Punching|Sword Swing|Kicking|
|Jumping|baseline<br>RPG (ours)|0.25<br>**0.70**|0.15<br>**0.85**|0.15<br>**0.80**|0.05<br>**0.75**|
|hi|baseline|0.35|0.60|0.50|0.45|
|Puncng|RPG (ours)|**0.80**|**0.95**|**0.75**|**0.75**|
|SdSi|baseline|0.30|0.50|0.45|0.65|
|wor wng|RPG (ours)|**0.70**|**0.95**|**0.90**|**0.90**|
|Kiki|baseline|0.30|0.65|0.40|0.50|
|cng|RPG (ours)|**0.70**|**0.90**|**0.75**|**0.85**|


As shown in the results Table. IV, the success rate of motion transitions is closely related to the primary body parts involved in the movements. For example, transitions between lower-body motions—such as from jumping to kicking or from jumping to jumping—exhibit the highest level of difficulty. It also shows that RPG framework significantly improves the success rate of motion transitions. This demonstrates that the RPG framework exhibits stronger robustness in scenarios involving multi-policy switching. 

**Q3: The effect of the proposed framework on control smoothness in multi-policy transitions.** 

Ensuring smooth motion execution is critically important when handling abrupt action changes or cross-policy scenarios. Our experimental design follows the same setup as described for Q2, and we select _Emaccj_ as the metric for evaluation. To assess control smoothness during policy transitions, we analyze a time window spanning from 50 timesteps before to 50 timesteps after each motion transition. 

TABLE V 

SMOOTHNESS COMPARISON WHILE TRANSITION 

|**Start (a)**|_Emaccj_||**Target **<br>|**Motion (b)**<br>||
|---|---|---|---|---|---|
|||Jumping|Punching|Sword Swing|Kicking|
||baseline|1.8520|1.9533|1.8925|1.7633|
|Jumping|RPG w/o Gating|1.9197|1.8649|1.9024|1.5323|
||RPG (ours)|**1.5235**|**1.6421**|**1.5875**|**1.4524**|
||baseline|1.9233|**1.2383**|1.8738|1.9642|
|Punching|RPG w/o Gating|1.8125|1.3096|1.9482|1.9773|
||RPG (ours)|**1.6237**|1.3529|**1.7821**|**1.6535**|
||baseline|1.8735|**1.8127**|1.3525|1.8239|
|Sword Swing|RPG w/o Gating|1.7769|1.8322|1.2617|1.8254|
||RPG (ours)|**1.5841**|1.9031|**1.1424**|**1.5432**|
||baseline|1.9637|1.9826|1.8936|1.7235|
|Kicking|RPG w/o Gating|1.7689|1.8236|1.9341|1.8099|
||RPG (ours)|**1.6539**|**1.6724**|**1.5937**|**1.4528**|


As shown in the Table. V, the smoothness of motion is highly correlated with the range of motion. For instance, transitions involving punching can achieve relatively smooth results even with the baseline method. For motions with large amplitude action such as jumping and sword-swinging, 


Fig. 4. Policy Transition Example: Jumping-Punching-Sword SwingKicking. The upper curve graph represents the variation of _w_ ˆ _t_<sup>_u,m_</sup> along the time. The lower curve graph represents the _w_ ˆ _t_<sup>_l,m_</sup> variation. 

the RPG generates significantly smoother motion executions. Even in cases where the smoothness of motions generated by RPG is inferior to that of the baseline, the difference between the two is not significant. The results indicate that the RPG method yields significantly smoother control outputs across the majority of motion transitions. 

## **Q4: How does the gating policy perform in merging the expert policies?** 

We selected a motion transition combo as an example and recorded the gating policy output. The results are shown in Fig. 4. Since the weight values output by the gating policy account for the coordination between the upper and lower body of the robot, we recorded them separately. It can be observed that during action transitions, the weight values corresponding to the executed actions output by the gating network are more pronounced. 

We also designed an ablation experiment comparing the performance with/without the gating mechanism. As shown in the Table. V, it tells that the gating policy significantly improves the control smoothness during policy transitions. 

## _D. Discussion._ 

Based on the aforementioned experiments, it can be observed that the use of the RPG significantly enhances the stability and success rate of action policy transitions while improving the smoothness of robot control—all without substantially compromising the motion tracking performance of individual expert policies. This improvement can be attributed, in part, to the policy-transition and temporal randomization mechanisms, which expand the robot’s state domain, and through RL reward constraints, enhance both control smoothness and disturbance resistance in the face of abrupt motion changes. 

## V. CONCLUSION 

This paper proposed RPG, a robust policy gating framework for multi-policies transition in humanoid fighting. RPG integrates policy-transition and temporal randomization mechanism for training with a smoothly regularized gating network, enabling stable and interruptible motion execution. Simulations and real-world tests on a Unitree G1 robot demonstrate that RPG achieves high transition success rates and improved control smoothness and robustness without compromising tracking accuracy. Meanwhile we developed a multi-policy control pipeline that enables robot combat tasks to be executed in a manner reminiscent of controlling a character in an action RPG game. Our approach provides a practical solution for dynamic multi-skill imitation in realworld humanoid applications. 

In future work, we plan to integrate perception and recognition capabilities to enable the robot to autonomously track and engage targets in combat tasks. 

## REFERENCES 

- [1] I. Radosavovic, S. Kamat, T. Darrell, and J. Malik, “Learning Humanoid Locomotion over Challenging Terrain,” Oct. 2024. 

- [2] Z. Zhuang, S. Yao, and H. Zhao, “Humanoid parkour learning,” _arXiv preprint arXiv:2406.10759_ , 2024. 

- [3] Z. Wang, J. Zhou, and Q. Wu, “Dribble Master: Learning Agile Humanoid Dribbling Through Legged Locomotion,” May 2025. 

- [4] Y. Xue, W. Dong, M. Liu, W. Zhang, and J. Pang, “A Unified and General Humanoid Whole-Body Controller for Fine-Grained Locomotion,” Feb. 2025. 

- [5] Y. Zhang, Z. Cao, B. Nie, H. Li, and Y. Gao, “Learning Robust Motion Skills via Critical Adversarial Attacks for Humanoid Robots,” Jul. 2025. 

- [6] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang, “Homie: Humanoid loco-manipulation with isomorphic exoskeleton cockpit,” _arXiv preprint arXiv:2502.13013_ , 2025. 

- [7] Z. Gu, J. Li, W. Shen, W. Yu, Z. Xie, S. McCrory, X. Cheng, A. Shamsah, R. Griffin, C. K. Liu, A. Kheddar, X. B. Peng, Y. Zhu, G. Shi, Q. Nguyen, G. Cheng, H. Gao, and Y. Zhao, “Humanoid Locomotion and Manipulation: Current Progress and Challenges in Control, Planning, and Learning,” Jan. 2025. 

- [8] Y. Liu, Z. Zhang, H. Wang, and L. Yi, “Unleashing Humanoid Reaching Potential via Real-world-Ready Skill Space,” May 2025. 

- [9] A. Schakkal, B. Zandonati, Z. Yang, and N. Azizan, “Hierarchical Vision-Language Planning for Multi-Step Humanoid Manipulation,” Jun. 2025. 

- [10] W. Sun, L. Feng, B. Cao, Y. Liu, Y. Jin, and Z. Xie, “ULC: A Unified and Fine-Grained Controller for Humanoid Loco-Manipulation,” Jul. 2025. 

- [11] C. Tessler, Y. Jiang, E. Coumans, Z. Luo, G. Chechik, and X. B. Peng, “MaskedManipulator: Versatile Whole-Body Control for LocoManipulation,” May 2025. 

- [12] D. J. Agravante, A. Cherubini, A. Sherikov, P.-B. Wieber, and A. Kheddar, “Human-humanoid collaborative carrying,” _IEEE Transactions on Robotics_ , vol. 35, no. 4, pp. 833–846, 2019. 

- [13] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan _et al._ , “Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” _arXiv preprint arXiv:2502.01143_ , 2025. 

- [14] T. E. Truong, Q. Liao, X. Huang, G. Tevet, C. K. Liu, and K. Sreenath, “BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion,” Aug. 2025. 

- [15] W. Xie, J. Han, J. Zheng, H. Li, X. Liu, J. Shi, W. Zhang, C. Bai, and X. Li, “KungfuBot: Physics-Based Humanoid Whole-Body Control for Learning Highly-Dynamic Skills,” Jun. 2025. 

   - [17] T. Zhang, B. Zheng, R. Nai, Y. Hu, Y.-J. Wang, G. Chen, F. Lin, J. Li, C. Hong, K. Sreenath, and Y. Gao, “HuB: Learning Extreme Humanoid Balance,” May 2025. 

   - [18] T. He, Z. Luo, W. Xiao, C. Zhang, K. Kitani, C. Liu, and G. Shi, “Learning human-to-humanoid real-time whole-body teleoperation,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 8944–8951. 

   - [19] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang, “GMT: General Motion Tracking for Humanoid Whole-Body Control,” Jun. 2025. 

   - [20] Z. Su, B. Zhang, N. Rahmanian, Y. Gao, Q. Liao, C. Regan, K. Sreenath, and S. S. Sastry, “HITTER: A HumanoId Table TEnnis Robot via Hierarchical Planning and Learning,” Aug. 2025. 

   - [21] Z. Li, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Robust and versatile bipedal jumping control through reinforcement learning,” _arXiv preprint arXiv:2302.09450_ , 2023. 

   - [22] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” _arXiv preprint arXiv:2402.16796_ , 2024. 

   - [23] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang, “Exbody2: Advanced expressive humanoid whole-body control,” _arXiv preprint arXiv:2412.13196_ , 2024. 

   - [24] Z. Zhuang and H. Zhao, “Embrace collisions: Humanoid shadowing for deployable contact-agnostics motions,” _arXiv preprint arXiv:2502.01465_ , 2025. 

   - [25] Z. Zhuang, Z. Fu, J. Wang, C. Atkeson, S. Schwertfeger, C. Finn, and H. Zhao, “Robot parkour learning,” _arXiv preprint arXiv:2309.05665_ , 2023. 

   - [26] A. Allshire, H. Choi, J. Zhang, D. McAllister, A. Zhang, C. M. Kim, T. Darrell, P. Abbeel, J. Malik, and A. Kanazawa, “Visual Imitation Enables Contextual Humanoid Control,” May 2025. 

   - [27] Y. Wang, M. Yang, W. Zeng, Y. Zhang, X. Xu, H. Jiang, Z. Ding, and Z. Lu, “From Experts to a Generalist: Toward General Whole-Body Control for Humanoid Robots,” Jun. 2025. 

   - [28] J. Li, Y. Zhu, Y. Xie, Z. Jiang, M. Seo, G. Pavlakos, and Y. Zhu, “Okami: Teaching humanoid robots manipulation skills through single video imitation,” in _8th Annual Conference on Robot Learning_ , 2024. 

   - [29] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” _arXiv preprint arXiv:2406.10454_ , 2024. 

   - [30] W. Yu, F. Acero, V. Atanassov, C. Yang, I. Havoutis, D. Kanoulas, and Z. Li, “Discovery of skill switching criteria for learning agile quadruped locomotion,” Feb. 2025. 

   - [31] X. B. Peng, Y. Guo, L. Halper, S. Levine, and S. Fidler, “Ase: Largescale reusable adversarial skill embeddings for physically simulated characters,” _ACM Transactions On Graphics (TOG)_ , vol. 41, no. 4, pp. 1–17, 2022. 

   - [32] N. S. Neggatu, J. Houssineau, and G. Montana, “Evaluation-Time Policy Switching for Offline Reinforcement Learning,” Mar. 2025. 

   - [33] D. K. Panda and W. Guo, “Robust Policy Switching for Antifragile Reinforcement Learning for UAV Deconfliction in Adversarial Environments,” Jun. 2025. 

   - [34] G. Christmann, Y.-S. Luo, and W.-C. Chen, “Expert Composer Policy: Scalable Skill Repertoire for Quadruped Robots,” Mar. 2024. 

   - [35] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang, “Learning Humanoid Standing-up Control across Diverse Postures,” Feb. 2025. 

   - [36] Z. Wang, X. Yang, J. Zhao, J. Zhou, T. Ma, Z. Gao, A. Ajoudani, and J. Liang, “End-to-End Humanoid Robot Safe and Comfortable Locomotion Policy,” Aug. 2025. 

   - [37] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black, “Amass: Archive of motion capture as surface shapes,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2019, pp. 5442–5451. 

   - [38] Z. Shen, H. Pi, Y. Xia, Z. Cen, S. Peng, Z. Hu, H. Bao, R. Hu, and X. Zhou, “World-Grounded Human Motion Recovery via GravityView Coordinates,” in _SIGGRAPH Asia 2024 Conference Papers_ , Dec. 2024, pp. 1–11. 

   - [39] Z. Luo, J. Cao, A. Winkler, K. Kitani, and W. Xu, “Perpetual Humanoid Control for Real-time Simulated Avatars,” Sep. 2023. 

- [16] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi, “Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning,” _arXiv preprint arXiv:2406.08858_ , 2024. 

