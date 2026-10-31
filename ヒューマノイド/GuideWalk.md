---
title: "GuideWalk: Learning Unified Autonomous Navigation and Locomotion for Humanoid Robots across Versatile Terrains"
date: "2026-06-09"
authors: "Haoxuan Han; Chen Chen; Linao Gong; Xin Yang; Hao Hu; Junhong Guo"
url: https://arxiv.org/abs/2606.10449
pdf: https://arxiv.org/pdf/2606.10449
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.10449)** / [論文ページ](https://arxiv.org/abs/2606.10449)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **GuideWalk: Learning Unified Autonomous Navigation and Locomotion for Humanoid Robots across Versatile Terrains** 

Haoxuan Han<sup>1</sup> , Chen Chen<sup>1</sup> , Linao Gong<sup>1</sup> , Xin Yang<sup>1</sup> , Hao Hu<sup>1</sup> , Junhong Guo<sup>1</sup><sup>_,_2</sup> , Zhicheng He<sup>1</sup><sup>_,_2</sup> , Yao Su<sup>2</sup> and Fenghua He<sup>1</sup> 

**_Abstract_ — Humanoid robots have achieved strong locomotion capabilities, but reliable navigation on versatile terrains remains challenging because obstacle avoidance must be coordinated with dynamically feasible motion. In this work, we present GuideWalk, a unified end-to-end framework that integrates traversability-aware navigation guidance with terrain-adaptive locomotion teacher for humanoid navigation. Specifically, we introduce a navigation module that provides explicit velocity guidance, decoupling obstacle avoidance from terrain conditions to enable robust planning across diverse environments. We propose an efficient two-stage training strategy with composite teacher distillation, where goal-directed commands and dynamically consistent actions are aggregated and distilled into a single policy. To further improve robustness, the distilled policy is refined with reinforcement learning and an auxiliary behavior cloning objective, which promotes exploration while preserving desirable teacher behaviors. Experiments demonstrate that GuideWalk achieves terrain-adaptive, goal-directed obstacle navigation across diverse terrains. Videos are available on our project website: https://guide-walk.github.io/GuideWalk.** 

## I. INTRODUCTION 

Humanoid locomotion has achieved remarkable progress in balance [1], agility [2], and highly dynamic motion [3]. However, deploying humanoids in cluttered real-world environments requires more than stable locomotion. A robot must simultaneously account for terrain geometry to maintain stability and surrounding obstacles to ensure collisionfree navigation. Achieving robust navigation across diverse terrains while satisfying spatial constraints remains a challenging open problem. 

Recent humanoid locomotion methods have extended stable motion beyond flat terrain by incorporating onboard perception, such as depth cameras [4]–[6] and LiDAR [7]– [9], together with terrain representations such as elevation maps or depth observations. These approaches demonstrate the feasibility of terrain-aware locomotion in challenging environments. In parallel, learning-based navigation has evolved from decoupled navigation and locomotion pipelines [10] toward hierarchical [11]–[13] and fully endto-end approaches [14]–[16]. By directly mapping onboard observations to motion, end-to-end methods enable more reactive navigation without relying on explicitly separated planning and control. However, existing end-to-end approaches often require complex network architectures [16] and high-dimensional spatial representations [15], imposing substantial computational and GPU memory overhead during training and deployment. Moreover, jointly learning navigation and terrain-adaptive locomotion remains traininginefficient, as sparse navigation rewards provide limited 

supervision for learning coordinated navigation and full-body locomotion behaviors. 

To address these challenges, we propose GuideWalk, a unified end-to-end framework for terrain-aware humanoid navigation and obstacle avoidance. Rather than learning these capabilities jointly through sparse task rewards starting from scratch, we introduce a composite teacher that provides complementary navigation and locomotion supervision. The student first distills navigation and locomotion behaviors from the composite teacher via Dataset Aggregation (DAgger), providing an effective initialization for the second training stage. It is then finetuned with Reinforcement Learning (RL), where velocity tracking rewards guided by the navigation guidance provide denser navigation supervision, while an Behavior Cloning (BC) objective preserves desirable teacher behaviors. The main contributions are summarized as follows: 

- 1) We present an end-to-end navigation framework that integrates supervision from navigation guidance and a locomotion teacher, enabling a unified policy for terrainaware navigation with obstacle avoidance. 

- 2) We propose an efficient two-stage training strategy that first distills teacher knowledge via DAgger with critic pretraining, and then refines the student via RL finetuning with navigation-guided rewards and an auxiliary BC loss. 

- 3) We validate the proposed approach through simulation and real-world experiments, demonstrating its effectiveness and robustness. 

II. METHODOLOGY 

- _A. System Overview_ 

The proposed framework combines guidance from a composite teacher with policy optimization via RL, enabling the student to efficiently acquire coordinated navigation and locomotion behaviors while improving robustness and performance. As illustrated in Fig. 1, this is achieved through a two-stage training pipeline featuring a composite teacher and a unified student policy. Specifically, the composite teacher consists of a Dynamic Window Approach (DWA) [17]-based navigation guidance and a privileged locomotion teacher, jointly providing coherent supervision for high-level navigation and low-level control. 

In the first stage, the student policy and critic are trained using DAgger [18]. Specifically, the student policy interacts with the simulation environment to collect visited states, while the composite teacher is queried to generate corresponding target actions. The student policy is optimized 


Fig. 1: **Overview of GuideWalk.** Left: a composite teacher consisting of a DWA-based navigation module and a pre-trained locomotion policy. Middle: Stage 1, where the student policy and critic are trained via DAgger-based imitation from the composite teacher. Right: Stage 2, where reinforcement learning with an imitation objective further refines the policy. 

through supervised learning to imitate the teacher, while the critic is pretrained by regressing the returns collected from student rollouts. This stage enables the student policy to acquire both navigation and locomotion behaviors while providing a suitable value-function initialization for subsequent refinement stage. 

In the second stage, the student policy is further refined using RL based on Proximal Policy Optimization (PPO) [19], with linear and angular velocity tracking rewards guided by the navigation guidance to provide dense navigation guidance. An BC loss is incorporated alongside the RL task objective, forming a joint optimization that improves navigaion and locomotion performance while maintaining consistency with teacher behaviors. 

## _B. Composite Teacher_ 

The composite teacher consists of two complementary components: a DWA-based navigation guidance for traversability-aware velocity generation and a privileged locomotion teacher for terrain-adaptive control. The navigation guidance first generates a target velocity command ( _v_<sup>_∗_</sup> _, ω_<sup>_∗_</sup> ) from the target position and obstacle observations, which is then tracked by the locomotion teacher using privileged terrain and proprioceptive information. The resulting hierarchical structure provides action-level supervision that jointly captures obstacle-aware navigation and terrain-adaptive lo- 

## comotion. 

_1) Navigation Guidance:_ The navigation guidance employs a DWA-based local planner that evaluates candidate velocity commands via trajectory rollouts and selects the optimal command according to multiple criteria. To accelerate training, it takes the robot’s current pose in the global frame, the target position, and obstacle observations within the FoV as inputs, where the angular span and sensing range are designed to match the depth-camera specifications for simto-real fidelity. The resulting velocity command serves as the high-level locomotion target for the subsequent locomotion teacher. 

To provide the navigation guidance with prior knowledge of obstacle traversability, we record the positions and geometries of obstacles during environment construction and store them in a 2D obstacle map. During training, obstacle observations are generated online by ray casting on this map, providing obstacle-only information. In contrast to the depth image, which simultaneously captures obstacles and terrain ahead of the robot, this representation distinguishes genuine obstacles from traversable terrain, such that structures such as stairs and slopes are not treated as obstacles. 

To adapt the navigation speed to terrain difficulty, we use the elevation map to estimate terrain complexity and dynamically adjust the upper bound of the DWA output velocity. More challenging terrain, such as stairs, imposes 

a lower speed limit, whereas simpler terrain allows a higher limit. 

Although the humanoid robot possesses omnidirectional locomotion capabilities, its velocity tracking is less robust for lateral commands than for forward and yaw angular velocities. Therefore, we model the navigation guidance using a differential-drive kinematic model, restricting the output to forward linear velocity _v_ and yaw angular velocity _ω_ to ensure reliable execution by the locomotion teacher. 

For each sampled velocity pair ( _v, ω_ ), future trajectories are generated via the differential-drive kinematic model, starting from the current pose and rolled out over a short horizon. The optimal velocity pair ( _v_<sup>_∗_</sup> _, ω_<sup>_∗_</sup> ) is chosen by maximizing the following objective: 


where h( _v, ω_ ) measures the alignment between the trajectory endpoint and the goal direction, d( _v, ω_ ) measures the minimum clearance from nearby obstacles, and v( _v, ω_ ) biases the selection toward higher forward speeds. _Vs_ is determined by the terrain-adaptive maximum velocity limits, while _Vd_ is determined by the prescribed acceleration limits. 

Unlike standard DWA, which treats collision avoidance as a hard constraint, we incorporate obstacle clearance as a soft constraint through c( _v, ω_ ). This design avoids an empty feasible velocity set when the robot is already within an obstacle’s inflation radius, allowing the guidance to select a relatively optimal velocity that moves the robot away from the obstacle and facilitates recovery. 

_2) Locomotion Teacher:_ The locomotion teacher maps the target velocity command and privileged terrain and proprioceptive observations to full-body joint actions. Specifically, we formulate it as a parameterized policy 


where _O_<sup>˜</sup> prop denotes the privileged proprioceptive observation space available during training, _O_ ˜elev denotes the clean elevation map observation space, _V ⊂_ R<sup>2</sup> denotes the target velocity command space, and _A_ represents the fullbody joint action space. Given the privileged proprioception **_o_** ˜prop _∈ O_<sup>˜</sup> prop, the clean elevation map **_o_** ˜elev _∈ O_<sup>˜</sup> elev, and the target velocity command ( _v_<sup>_∗_</sup> _, ω_<sup>_∗_</sup> ) _∈V_ generated by the navigation guidance, the locomotion teacher outputs the fullbody joint action **_a_**<sup>_∗_</sup> _∈A_ . 

Locomotion teacher is trained via RL with Adversarial Motion Priors (AMP) [20], where the reference behaviors are derived from our self-collected motion capture (MoCap) data. This approach promotes human-like locomotion while reducing reliance on hand-crafted, terrain-specific reward shaping, which is difficult to tune consistently across diverse terrains. 

Together, the navigation guidance and locomotion teacher form the composite teacher policy. Let _O_ tar and _O_ ˜scan denote the target position space and forward 2D scan space, 

TABLE I: Observation spaces of different modules during training and deployment. 

|**Observation**|**Student**|**DWA**|**Loco. Teacher**|**Critic**|
|---|---|---|---|---|
|Target position|✓|✓||✓|
|DWA velocity command|||✓|✓|
|Noisy depth image|✓||||
|Clean depth image||||✓|
|Forward 2D scan||✓|||
|Noisy elevation map|✓||||
|Clean elevation map|||✓|✓|
|Proprioception|✓||✓|✓|
|Privileged proprioception|||✓|✓|


respectively, with **_o_** tar _∈O_ tar and **_o_** ˜scan _∈ O_ ˜scan. The navigation guidance first computes 


which is then passed to the locomotion teacher together with **_o_** ˜prop and **_o_** ˜elev. Thus, the composite teacher is written as 


This hierarchical composition provides a teacher that jointly captures obstacle-aware navigation and terrain-adaptive locomotion for subsequent policy distillation. 

## _C. Student Policy_ 

We define the student policy as a mapping from the deployable observation space to the full-body joint action space: _π_ s : _O →A_ , where 


with _O_ depth and _O_ elev denoting the noisy depth image and elevation map spaces, respectively, and _O_ prop denoting the non-privileged proprioceptive observation space. Here, _O_ prop<sup>5denotesthehistoryoffiveconsecutiveproprioceptive</sup> observations, while the depth image, elevation map, and target position are provided at the current time step. We use proprioceptive history to provide temporal cues that facilitate the distillation of locomotion-relevant latent information from the privileged teacher [21]. All observation spaces are summarized in Tab. I. All components of _O_ are available during deployment. 

The student policy consists of two independent Convolutional Neural Network (CNN)s followed by a shared Multi-Layer Perceptron (MLP). The two CNNs encode the elevation map and depth image separately, and their features are concatenated with the proprioceptive history and target position. The resulting representation is processed by the MLP to produce the joint action. 

To reduce the sim-to-real gap in depth perception, we augment the simulated depth images with the noise model proposed in [22]. The simulated depth images before and after noise augmentation are shown in Fig. 2. To provide 


Fig. 2: Comparison of simFig. 3: Complementary percepulated depth images before tion coverage of the depth image and after noise injection. and elevation map. 

the policy with both terrain and obstacle information, the elevation map is used together with the depth image. As illustrated in Fig. 3, the elevation map primarily covers the region beneath the robot, whereas the depth image mainly covers the region directly in front of the robot, providing complementary spatial coverage for obstacle avoidance and traversing complex terrains. 

## _D. DAgger Distillation_ 

We employ DAgger to distill the composite teacher into the student policy. During the distillation process, the student policy _π_ s interacts with the environment and generates state trajectories according to its current policy. Let **_s_** _t ∈S_ denote the environment state at time step _t_ . For the environment state _st_ , the student receives an observation **_o_** _t_ , while the corresponding privileged observation **_o_** ˜ _t_ is available only during training. At each visited state, the frozen composite teacher is queried using **_o_** ˜ _t_ to provide the reference action **_a_**<sup>_∗_</sup> _t_<sup>=</sup><sup>_π_t(˜</sup><sup>**_o_**</sup><sup>_t_).Theresultingobservation-actionpairs(</sup><sup>**_o_**</sup><sup>_t,_</sup><sup>**_a_**</sup><sup>_∗_</sup> _t_<sup>)</sup> are progressively aggregated into a growing dataset _D_ , which uses states visited by the student policy and reduces the distribution shift in BC. 

At iteration _i_ , the student policy _π_ s _,i_ is optimized with respect to the state distribution induced by the previous policy _π_ s _,i−_ 1: 


where _dπ_ s _,i−_ 1 denotes the state visitation distribution induced by the student policy _π_ s _,i−_ 1. This iterative procedure progressively aligns the student policy with the composite teacher over the states encountered by the student itself, while requiring only the deployable observation **_o_** _t_ as input to the student policy. 

To provide accurate value estimates at the beginning of Stage 2 and improve training efficiency, the critic is pretrained using the state trajectories collected by the student policy. For each visited state **_s_** _t_ , the corresponding return _Gt_ is computed from the rewards observed along the student rollout: 


TABLE II: Reward Terms 

|**Term**|**Function**|
|---|---|
|DWA lin. vel. tracking<br>DWA ang. vel. tracking|exp(_∥vxy −v_<sup>DWA</sup><br>_xy _<sup>_∥_2)</sup><br>exp(_∥ωz −ω_<sup>DWA</sup><br>_z_<br>_∥_<sup>2</sup>)|
|Undesired termination|**1**reset<br>1|
|Position tracking|1 + (_d_goal_/_2)<sup>2</sup> <sup>_·_</sup><sup>**1**</sup><sup>_t>T −_2</sup><br>|
|Heading tracking|1<br>1 + (∆_ψ/_1)<sup>2</sup> <sup>_·_</sup><sup>**1**</sup><sup>_t>T −_2</sup><br>|
|Standing posture at goal|_∥q −_¯_q_stand_∥_1_·_**1**_t>T −_1_·_**1**_d_goal_<_0_._5<br><br>|
|Correct-direction velocity|max<br>�<br>ReLU<br>�_vx_<br>_V_max <sup>_·_</sup><sup>**1**dir</sup><br>�<br>_,_**1**_d_goal_<_0_._5<br>�|
|Regularization reward terms|-|


where _H_ denotes the episode horizon and _γ_ is the discount factor. The critic _Vϕ_ is then optimized to regress the value of the current student policy: 


Thus, the distillation stage jointly pretrains the policy and value function, providing a policy initialization through behavioral cloning and a value-function initialization consistent with the student-induced state distribution. The resulting actor and critic parameters are subsequently used to initialize the refinement stage. 

## _E. RL Finetune_ 

To further refine the student policy _π_ s while preserving the desirable behaviors learned from the composite teacher, the second stage jointly optimizes reinforcement learning and behavioral cloning objectives. The overall objective is defined as 


where _λ_ balances task-driven policy improvement and consistency with the composite teacher. 

The auxiliary BC objective constrains the student’s joint actions to remain close to those of the composite teacher, providing a behavior regularization effect. This constraint reduces the need for manually designed motion-style rewards and prevents the student from developing undesirable motions while optimizing the task reward: 


where _D_ denotes the online trajectory buffer collected by the current student policy. 

The PPO objective complements this behavior regularization by directly incorporating the navigation guidance into the task reward. Specifically, the linear and angular velocity tracking terms encourage the student to follow ( _v_<sup>_∗_</sup> _, ω_<sup>_∗_</sup> ) = DWA( **_o_** tar _,_ ˜ **_o_** scan), providing dense navigation supervision throughout the rollout. Compared with relying solely on navigation rewards, this guidance provides more frequent learning signals and improves training efficiency. All reward terms are summarized in Table II. 

TABLE III: Curriculum terrain generation parameters. 

|Terrain type _τ_|Parameter|_p_<sup>min</sup><br>_τ_|_p_<sup>max</sup><br>_τ_|
|---|---|---|---|
|Obstacles|Minimum obstacle spacing (m)<br>Number of trees (-)|2.00<br>5|1.00<br>40|
|Upslope|The slope angle ranges (<sup>_◦_</sup>)|5.00|25.00|
|Downslope|The slope angle ranges (<sup>_◦_</sup>)|5.00|25.00|
|Bridge|Beam width (m)<br>Beam height (m)|0.40<br>2.00|0.30<br>5.00|
|Upstair|Width of each step (m)<br>Height of each step (m)|0.50<br>0.00|0.30<br>0.20|
|Downstair|Width of each step (m)<br>Height of each step (m)|0.50<br>0.00|0.30<br>0.20|


Fig. 4: Basic terrain primitives and obstacle configurations used to construct training environments. 

The policy parameters _θ_ are optimized using the PPO loss: _L_<sup>PPO</sup> ( _θ_ ) = E [min ( _rt_ ( _θ_ ) _At,_ clip ( _rt_ ( _θ_ ) _,_ 1 _− ϵ,_ 1 + _ϵ_ ) _At_ )] _,_ (12) where _rt_ ( _θ_ ) = _ππ_ ss _,_ old( **_a_** _t_ ( _<u>|</u>_ **_ao_** _tt|_ <u>;</u> **_o_** _θt_ <u>))</u><sup>istheprobabilityratioand</sup><sup>_At_</sup> denotes the advantage estimate. 

## III. EXPERIMENTS 

## _A. Experimental Setup_ 

We train our policy in the Isaac Sim simulation platform on a single NVIDIA RTX 5080 GPU with 16 GB of memory using 2048 parallel environments. Across the two student training stages, the policy is trained for 10,000 iterations, with a total training cost of 37.7 GPU hours, including the training of the privileged locomotion teacher. The training environments, shown in Fig. 4, are constructed from basic terrain primitives, including up and down stairs, up and down slopes, and narrow bridges, while obstacle configurations can be combined with any of these terrain types, enabling terrainaware navigation and obstacle avoidance. The curriculum terrain generation parameters are summarized in Table III. We define a difficulty scalar _s ∈_ [0 _,_ 1] and interpolate the terrain parameters as 


Fig. 5: GuideWalk navigating diverse simulated environments. 


where **p**<sup>min</sup> _τ_ and **p**<sup>max</sup> _τ_ denote the easiest and hardest settings, respectively. For evaluation, each terrain type is instantiated at _s_ = 1, corresponding to its own maximum-difficulty setting. All simulation experiments use these maximumdifficulty terrain configurations unless otherwise specified. 

We conduct ablation experiments to evaluate the contribution of each component. _w/o Nav. guidance_ removes the navigation guidance by omitting Stage 1 and replacing the velocity command in Stage 2 with the student’s body-frame linear and angular velocities from the previous timestep. _w/o Loco. teacher_ removes the locomotion teacher by omitting Stage 1 and the BC loss from Stage 2, while additionally incorporating AMP to preserve the motion priors. _w/o Stage 1_ trains the policy with Stage 2 from scratch, whereas _w/o Stage 2_ retains only the distillation stage and removes the subsequent refinement. We further compare GuideWalk with the composite teacher as a reference and a deployable hierarchical baseline consisting of DWA navigation and a deployable locomotion policy obtained via AMP. 

We evaluate the policy using four metrics. The _navigation success rate_ (NSR) measures the proportion of parallel environments in which the robot reaches within a 1m radius of the target without collision within a given time limit. The _navigation traversal time_ (T) is defined as the average time required to reach the target across all successful episodes. The _terrain traversal success rate_ (TSR) measures the proportion of parallel environments in which the robot successfully traverses the terrain without falling within a given time limit. The _Proximity to Obstacles_ (PO) measures the minimum distance between the robot and surrounding obstacles along the trajectory. Specifically, NSR, T, and PO are evaluated for obstacle navigation, while TSR is used to evaluate traversal performance across different terrains. 

## _B. Main Simulation Results_ 

As illustrated in Fig. 5, the trained policy is successfully transferred to a MuJoCo simulation environment, demonstrating its ability to perform obstacle avoidance across 

TABLE IV: Performance comparison under different ablations and settings. 

|Method|Obs|tacle Navigati|on|||Terrain|Traversability|||
|---|---|---|---|---|---|---|---|---|---|
||T(s) _↓_|NSR(%) _↑_|PO(m) _↑_|Flat|Upstair|Downstair|Upslope|Downslope|Narrow bridge|
|w/o Nav. guidance<br>w/o Loco. teacher<br>w/o Stage 1<br>w/o Stage 2<br>Composite Teacher<br>Deployable hierarchical|23.14_±_1_._8<br>18.07_±_1_._3<br>16.72_±_1_._4<br>19.09_±_1_._6<br>15.93_±_1_._5<br>16.14_±_1_._4|69.9_±_2_._4<br>61.5_±_1_._6<br>11.4_±_1_._2<br>18.3_±_1_._5<br>73.6_±_2_._0<br>60.5_±_2_._1|0.25_±_0_._1<br>0.43_±_0_._2<br>0.21_±_0_._1<br>0.51_±_0_._2<br>0.62_±_0_._2<br>0.57_±_0_._2|**100.0**_±_0_._0<br>**100.0**_±_0_._0<br>**100.0**_±_0_._0<br>98.1_±_0_._8<br>**100.0**_±_0_._0<br>**100.0**_±_0_._0|96.2_±_0_._8<br>92.7_±_0_._4<br>96.3_±_0_._8<br>84.9_±_1_._4<br>**98.6**_±_0_._8<br>89.1_±_1_._3|96.4_±_0_._7<br>90.6_±_0_._6<br>97.9_±_0_._5<br>89.2_±_1_._1<br>97.6_±_0_._5<br>82.6_±_1_._6|96.7_±_0_._6<br>96.8_±_0_._2<br>96.5_±_0_._7<br>96.8_±_0_._7<br>98.1_±_0_._3<br>93.4_±_1_._0|92.4_±_1_._3<br>95.3_±_1_._0<br>**97.4**_±_0_._6<br>90.6_±_1_._2<br>96.4_±_0_._6<br>95.1_±_1_._1|92.3_±_1_._2<br>78.5_±_0_._6<br>98.3_±_0_._5<br>75.1_±_1_._5<br>99.2_±_0_._3<br>86.7_±_1_._4|
|GuideWalk|**15.51**_±_1_._2|**99.0**_±_0_._5|**0.65**_±_0_._1|**100.0**_±_0_._0|96.8_±_1_._2|**98.5**_±_0_._4|**98.8**_±_0_._8|96.9_±_0_._9|**99.8**_±_0_._1|


(a) Mean episode reward during (b) Stage 2 training with and Stage 1 and Stage 2. without critic pretraining. 

Fig. 6: Mean episode reward curves under different settings. 


Fig. 7: Trajectory comparison under identical configurations. (a) GuideWalk, (b) w/o Nav. guidance, and (c) w/o Nav. guidance with increased obstacle-proximity penalty. 

diverse terrains, such as navigating around obstacles on stairs. 

We first compare GuideWalk with the Composite Teacher to assess whether the student preserves terrain-adaptive locomotion while improving obstacle navigation. As shown in Tab. IV, GuideWalk maintains comparable performance across non-flat terrains while substantially improving obstacle-navigation success, demonstrating effective transfer and further refinement of the teacher’s behaviors. The training curve in Fig. 6a shows a further increase in mean episode reward after transitioning to Stage 2. 

We further compare GuideWalk with a deployable hierarchical baseline combining DWA navigation and an AMP locomotion policy. Its lower performance mainly arises from the difficulty of distinguishing traversable terrain from obstacles, which can lead to unnecessary detours or infeasible commands. In contrast, GuideWalk separates obstacle perception from terrain traversability during training, enabling unified terrain-aware obstacle avoidance with deployable observations. 


Fig. 8: Motion and trajectory smoothness analysis. 

## _C. Ablation Studies_ 

To evaluate the role of navigation guidance, we compare GuideWalk with _w/o Nav. guidance_ under identical obstacle configurations. Removing the guidance causes directional oscillations and closer obstacle approaches, resulting in less smooth trajectories (Fig. 7b, 8a). Increasing the obstacleproximity penalty alleviates close approaches but induces unnecessary detours (Fig. 7c), particularly with multiple obstacles. These results highlight the advantage of DWAbased guidance, which evaluates future trajectories to provide forward-looking guidance on goal alignment and obstacle clearance. 

We next examine the contribution of the locomotion teacher. Removing the locomotion guidance substantially degrades terrain traversal, particularly on narrow bridges and stairs, despite retaining the AMP-based motion prior. Compared with the general motion prior provided by AMP, the locomotion teacher offers state-dependent, joint-level supervision conditioned on terrain geometry and target velocity, providing more informative guidance for terrain-adaptive whole-body control. As shown in Fig. 8b, it also reduces the average joint acceleration, indicating smoother motion. 

We further investigate the necessity of the two-stage training strategy. Removing Stage 1 has little effect on terrain traversal but severely degrades obstacle navigation. This indicates that obstacle navigation is highly sensitive to policy initialization and the resulting state distribution. Starting Stage 2 from an uninitialized policy leads to poor exploration of meaningful navigation states, making online teacher supervision less effective for learning long-horizon obstacle avoidance. Stage 1 via DAgger instead provides a meaningful initialization and teacher actions, enabling more effective exploration and refinement. 


Fig. 9: Real-world deployment of GuideWalk in diverse scenarios. 

We further investigate the necessity of the two-stage training strategy. The complementary role of Stage 2 is evident from the _w/o Stage 2_ results. Without RL refinement, the distilled policy performs substantially worse in obstacle navigation, particularly in the multiple-obstacle scenario, due to the lack of task-level correction from environment feedback. Stage 2 addresses this limitation by optimizing the policy with environment feedback while preserving teacher behaviors through the auxiliary BC objective. 

The auxiliary components used to stabilize Stage 2 provide complementary benefits. Without critic pretraining, the actor still inherits the navigation and locomotion behaviors from DAgger, but the randomly initialized critic produces inaccurate value estimates on the student-induced state distribution, leading to unreliable advantage estimates and unstable early PPO updates that can cause policy drift from the Stage 1 behavior. This instability is also reflected in the training curves in Fig. 6b, where _w/o Critic Pretrain_ initially improves rapidly but subsequently undergoes a pronounced reward drop, whereas GuideWalk exhibits a more stable and sustained improvement throughout Stage 2. Removing the BC loss mainly affects motion quality, resulting in more irregular upper-body motions and greater deviation from the teacher. Without the joint-level imitation constraint, the policy relies more heavily on task rewards to shape its motion, making the resulting motion style more sensitive to reward design. Thus, critic pretraining stabilizes valuebased policy optimization, while BC preserves desirable teacher behaviors during task-driven refinement. Together, they reduce the need for laborious reward engineering to simultaneously shape navigation performance and wholebody motion quality. 

TABLE V: Comparison of computational and deployment requirements. 

|Method|Network|Train GPU|Infer. Mem.|
|---|---|---|---|
|Gallant [15]|3_×_2D CNN + MLP|8_×_4090 / 24 GB|_∼_1.3 MB|
|FocusNav [16]|3D CNN + BEV<br>+ Attn. + GRU|4_×_4090 / 24 GB|–|
|**GuideWalk**|**2**_×_**CNN + MLP**|**1**_×_**5080 / 16 GB**|_<_**1 MB**|


## _D. Computational and Deployment Efficiency_ 

To assess the efficiency of GuideWalk, we compare its computational and deployment requirements with representative humanoid navigation methods. As shown in Tab. V, GuideWalk achieves its unified navigation capability with substantially lower resource requirements. This efficiency comes from both the training strategy and system design: teacher distillation provides an effective initialization before reinforcement learning, while navigation-guided velocity rewards provide dense learning signals during refinement. In addition, the simulation-friendly perception design supports efficient large-scale training, and the compact student architecture reduces computation and memory requirements for training and deployment. 

## _E. Real World Experiments_ 

The robot is equipped with a Livox MID360 LiDAR and an Orbbec Gemini 335Lg depth camera. On a Jetson Orin NX, we deploy FastLIO2 [23] and Elevation Mapping [24] to provide real-time robot localization and elevation maps. The stereo RGB images are processed by Fast Foundation Stereo [25] to obtain depth observations at over 50 Hz, while 

TABLE VI: Real-world navigation performance. 

||Upstair|Downstair|Downslope|Upslope|Obstacles|
|---|---|---|---|---|---|
|Success Rate|7 / 10|10 / 10|10 / 10|10 / 10|10 / 10|
|Avg. Speed (m/s)|0.40|0.42|0.48|0.36|0.56|


the navigation policy is deployed on the onboard NUC for real-time inference at 50 Hz. 

We validate GuideWalk on a hardware platform, evaluating its navigation capabilities across stairs, slopes, and obstaclerich environments, as illustrated in Fig. 9. As summarized in Tab. VI, GuideWalk achieves robust real-world performance across diverse terrains, with 100% success rates on down stairs, down slopes, up slopes and multiple-obstacle scenarios. The lower success rate on up stairs is primarily attributed to the torque limitations of the hardware platform, while the 10/10 success rate in obstacle-rich environments demonstrates reliable obstacle avoidance. The variation in average speed across terrains reflects the terrain-aware adjustment of the upper bound of the DWA velocity. 

## IV. CONCLUSIONS 

In this work, we presented GuideWalk, a unified end-toend framework for autonomous navigation and locomotion of humanoid robots in diverse environments. Extensive simulation and real-world experiments demonstrate that GuideWalk effectively coordinates goal-directed navigation with stable and feasible locomotion, achieving robust performance across diverse terrains and obstacle-rich environments. 

Despite these promising results, two limitations remain. First, the use of both elevation maps and depth images introduces sensing redundancy and computational overhead. Future work will explore deriving elevation maps from continuous depth observations to reduce reliance on onboard LiDAR. Second, the current policy lacks explicit spatial memory, limiting its ability to reuse information from previously observed regions. Future work will investigate incorporating spatial memory to improve navigation in more complex, partially observed environments. 

## REFERENCES 

- [1] T. Zhang, B. Zheng, R. Nai, Y. Hu, Y.-J. Wang, G. Chen, F. Lin, J. Li, C. Hong, K. Sreenath, and Y. Gao, “Hub: Learning extreme humanoid balance,” in _Proceedings of The 9th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, J. Lim, S. Song, and H.-W. Park, Eds., vol. 305. PMLR, 27–30 Sep 2025, pp. 686–704. [Online]. Available: https://proceedings.mlr.press/v305/zhang25b.html 

- [2] Z. Wu, X. Huang, L. Yang, Y. Zhang, K. Sreenath, X. Chen, P. Abbeel, R. Duan, A. Kanazawa, C. Sferrazza _et al._ , “Perceptive humanoid parkour: Chaining dynamic human skills via motion matching,” _arXiv preprint arXiv:2602.15827_ , 2026. 

- [3] Y. Wang, S. Zhu, P. Zhi, Y. Li, J. Li, Y.-L. Li, Y. Xiao, X. Wang, B. Jia, and S. Huang, “Omnixtreme: Breaking the generality barrier in high-dynamic humanoid control,” _arXiv preprint arXiv:2602.23843_ , 2026. 

- [4] A. Agarwal, A. Kumar, J. Malik, and D. Pathak, “Legged locomotion in challenging terrains using egocentric vision,” in _Proceedings of The 6th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, K. Liu, D. Kulic, and J. Ichnowski, Eds., vol. 205. PMLR, 14–18 Dec 2023, pp. 403–415. [Online]. Available: https://proceedings.mlr.press/v205/agarwal23a.html 

- [5] Z. Zhuang, S. Yao, and H. Zhao, “Humanoid parkour learning,” in _Proceedings of The 8th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, P. Agrawal, O. Kroemer, and W. Burgard, Eds., vol. 270. PMLR, 06–09 Nov 2025, pp. 1975–1991. [Online]. Available: https://proceedings.mlr.press/v270/ zhuang25a.html 

- [6] S. Zhu, Z. Zhuang, M. Zhao, K.-Y. Lee, and H. Zhao, “Hiking in the wild: A scalable perceptive parkour framework for humanoids,” 2026. [Online]. Available: https://arxiv.org/abs/2601.07718 

- [7] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang, “Learning humanoid locomotion with perceptive internal model,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , 2025, pp. 9997–10 003. 

- [8] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang, “BeamDojo: Learning Agile Humanoid Locomotion on Sparse Footholds,” in _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. 

- [9] C. Zhang, V. Klemm, F. Yang, and M. Hutter, “Ame-2: Agile and generalized legged locomotion via attention-based neural map encoding,” 2026. [Online]. Available: https://arxiv.org/abs/2601.08485 

- [10] O. A. Donca, C. Beokhaimook, and A. Hereid, “Real-time navigation for bipedal robots in dynamic environments,” _arXiv preprint arXiv:2210.03280_ , 2022. 

- [11] T. He, C. Zhang, W. Xiao, G. He, C. Liu, and G. Shi, “Agile but safe: Learning collision-free high-speed legged locomotion,” in _Robotics: Science and Systems (RSS)_ , 2024. 

- [12] J. Lee, M. Bjelonic, A. Reske, L. Wellhausen, T. Miki, and M. Hutter, “Learning robust autonomous navigation and locomotion for wheeledlegged robots,” _Science Robotics_ , vol. 9, no. 89, p. eadi9641, 2024. 

- [13] M. Seo, R. Gupta, Y. Zhu, A. Skoutnev, L. Sentis, and Y. Zhu, “Learning to walk by steering: Perceptive quadrupedal locomotion in dynamic environments,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , 2023, pp. 5099–5105. 

- [14] F. Huang, H. Mou, and Q. Li, “Tnavrl: Cross-modal transformer for humanoid visual navigation,” _IEEE Robotics and Automation Letters_ , 2026. 

- [15] Q. Ben, B. Xu, K. Li, F. Jia, W. Zhang, J. Wang, J. Wang, D. Lin, and J. Pang, “Gallant: Voxel grid-based humanoid locomotion and local-navigation across 3d constrained terrains,” _arXiv preprint arXiv:2511.14625_ , 2025. 

- [16] Y. Zhang, J. Ma, L. Yan, Z. Cao, Y. Zhang, H. Li, and Y. Gao, “Focusnav: Spatial selective attention with waypoint guidance for humanoid local navigation,” _arXiv preprint arXiv:2601.12790_ , 2026. 

- [17] D. Fox, W. Burgard, and S. Thrun, “The dynamic window approach to collision avoidance,” _IEEE Robotics & Automation Magazine_ , vol. 4, no. 1, pp. 23–33, 1997. 

- [18] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” in _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ . JMLR Workshop and Conference Proceedings, 2011, pp. 627–635. 

- [19] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [20] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Trans. Graph._ , vol. 40, no. 4, Jul. 2021. [Online]. Available: http://doi.acm.org/10.1145/3450626.3459670 

- [21] J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning quadrupedal locomotion over challenging terrain,” _Science robotics_ , vol. 5, no. 47, p. eabc5986, 2020. 

- [22] W. Sun, Y. Su, L. Huang, A. Zhang, D. Wei, M. San, D. Tian, E. Cao, F. Yan, E. Xie, and Z. Xie, “Now you see that: Learning end-to-end humanoid locomotion from raw pixels,” 2026. [Online]. Available: https://arxiv.org/abs/2602.06382 

- [23] W. Xu, Y. Cai, D. He, J. Lin, and F. Zhang, “Fast-lio2: Fast direct lidarinertial odometry,” _IEEE Transactions on Robotics_ , vol. 38, no. 4, pp. 2053–2073, 2022. 

- [24] T. Miki, L. Wellhausen, R. Grandia, F. Jenelten, T. Homberger, and M. Hutter, “Elevation mapping for locomotion and navigation using gpu,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2022, pp. 2273–2280. 

- [25] B. Wen, S. Dewan, and S. Birchfield, “Fast-FoundationStereo: Realtime zero-shot stereo matching,” _CVPR_ , 2026. 

