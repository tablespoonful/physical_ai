---
title: "Terrain Consistent Reference-Guided RL for Humanoid Navigation Autonomy"
date: "2026-05-15"
authors: "William D. Compton; Zachary Olkin; Aaron D. Ames"
url: https://arxiv.org/abs/2605.15517
pdf: https://arxiv.org/pdf/2605.15517
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.15517)** / [論文ページ](https://arxiv.org/abs/2605.15517)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Terrain Consistent Reference-Guided RL for Humanoid Navigation Autonomy** 

William D. Compton<sup>1</sup> , Zachary Olkin<sup>1</sup> , and Aaron D. Ames<sup>1</sup> 

**_Abstract_ — We present a method for training referenceguided, perceptive reinforcement learning locomotion policies for humanoid robots in which reference trajectories are modulated in training to be consistent with terrain geometry. Aiming to deploy our method with standard navigation autonomy infrastructure, we synthesize** _SE_ (2) **-controllable reference trajectories inside the RL training loop, projecting desired footsteps onto valid footholds and adjusting swing-foot and center-of-mass trajectories to match the terrain. The resulting policy exposes a clean** _SE_ (2) **velocity interface compatible with standard navigation planners. In simulation, environmentallyconditioned references significantly improve reference tracking performance compared to environment agnostic references. On hardware, we integrate the policy with an MPC + control barrier function planner and demonstrate long-horizon (** _>_ **70m) closed-loop autonomous navigation on the Unitree G1 through outdoor environments containing rough terrain and consecutive flights of stairs, with all sensing and computation onboard.** 

## I. INTRODUCTION 

As contemporary locomotion methods for humanoid robots achieve high levels of agility and robustness, the bottleneck increasingly lies in deploying these behaviors as part of a larger navigation stack in complex and unstructured environments. While embedding motion priors from human data or trajectory optimization into RL training has led to state-of-the-art performance and robustness for humanoid locomotion, these methods struggle to address two main problems: interfacing with planner-issued commands and conditioning on the terrain geometry such as valid footholds. Our method tackles both of these shortcomings, training a reference-shaped, perceptive locomotion policy designed to integrate with navigation architectures by leveraging reduced order models to synthesize environmentally consistent, _SE_ (2) controllable reference signals in the RL training loop. 

Controllability and environmental conditioning of the locomotion policy are critical components of any general humanoid navigation stack. Environmental factors such as stairs, constrained footholds, and tight spaces necessitate tight coupling with perception. Jointly addressing low-level stabilization and long horizon, non-convex and terrain dependent problem of navigation exceeds modern resource budgets on compute, data, and observability. These limitations necessitate the division between navigation planning, typically providing waypoints or paths, from locomotion control, tasked with realizing the navigation plan. Therefore, the locomotion policy must expose a planner-compatible, perception-aware interface. 

*This research is supported by Technology Innovation Institute (TII). 

> 1Authors are with the Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, CA 91125. 


Fig. 1. LIP-CLF RL trains a unstructured terrain locomotion policy using a single stage, MLP based training pipeline and a single depth camera. The policy is _SE_ (2) controllable, enabling integration with standard navigation planning methods. In the pictured experiment, the Unitree G1 robot autonomously navigates into a building, climbing two flights of stairs. Video available at https://youtu.be/rTWgR_VxL5Y. 

In the context of humanoid robots, training agile locomotion often leverages human data or trajectory optimization to guide the RL. By training the policy to follow trajectories obtained from human data or trajectory optimization, emergent undesirable behaviors are substantially reduced. This approach can leverage the significant capabilities and inherent robustness of reference motions to generate more agile, dynamic, and robust motions than possible with other reference-free methods. 

While reference-guided RL makes significant progress on the agile locomotion front, it is often not conducive with integration into navigation planning architectures. Many approaches require reference trajectories as inputs, often live motion-capturing and imitating human motions. Either synthesizing environmentally consistent whole-body references online or sequencing discrete capabilities to accomplish general locomotion tasks are prohibitively challenging planning problems on their own. This lack of an interface with planning methods limits the applicability of these methods in standard navigation architectures. 

Additionally, conditioning reference-guided RL pipelines on environmental factors, such as terrain geometry, remains 


Fig. 2. System Architecture Diagram. References are generated in the CLF-RL training loop, and modified to be consistent with the environment. When deployed on hardware, lidar is used for odometry and localization in a map, and a ZED Mini mounted on the robot’s chest obtains depth images. MPC plans trajectories for the robot; a tracking controller sends velocity commands to the RL policy to realize the plan. 

a difficult problem. Standard motion-capture pipelines do not collect terrain information, and even if references are generated with terrain geometry, it is nontrivial to map these references on to new terrains not in the reference library. 

Our proposed method is designed to solve the problem of reference-guided perceptive locomotion capable of integrating with existing planning architectures. To accomplish this, we propose a novel method leveraging reduced order models to synthesize environmentally consistent reference signals rapidly in the RL training loop. The policy tracks _SE_ (2) velocity commands, which enables direct integration with standard navigation planning architectures, shown in Fig. 2. Our policy is conditioned directly on depth camera data, allowing robust navigation over complex and unstructured terrain, which we demonstrate on the Unitree G1. 

Specifically, we make the following contributions: 

- We introduce an environment-conditioned reference synthesis method based on the Linear Inverted Pendulum (LIP) model that runs inside the RL training loop. To our knowledge, this is the first reference-guided RL pipeline for humanoids in which references are modulated online to be consistent with terrain geometry. Further, our policy uses only an MLP, no history, and can be trained without distillation, vastly simplifying the learning problem relative to other state of the art methods. 

- We integrate the resulting perceptive locomotion policy into a complete navigation autonomy stack via a classic _SE_ (2) velocity interface, demonstrating outdoor longhorizon ( _>_ 70m) closed-loop autonomous navigation through human-centric environments including stairs, rough terrain, and flat ground. As shown in Table I, prior humanoid navigation autonomy work has relied on blind, model-based locomotion controllers, while existing perceptive RL locomotion policies have not been deployed in autonomy stacks at this scale. 

## II. RELATED WORK 

Humanoid locomotion has a relatively long history, ranging from model-based works leveraging structured perception to reinforcement learning methods acting on raw sensor data. We organize related work into three categories, summarized in Table I. First, perceptive locomotion methods that achieve robust hardware deployment, without reference trajectories, which have yet to demonstrate integration with navigation autonomy stacks. Second, reference-tracking methods which lack environmental conditioning and typically require fullDoF reference trajectories at inference time, and are thus not compatible with standard navigation planning techniques. Third, autonomous humanoid navigation systems, which close the autonomy gap, but lack strong perceptive locomotion, and cannot traverse common urban and humancentric terrains such as stairs. As we discuss below, no prior work known to the authors lies at this intersection: perceptive, reference guided RL-based locomotion deployed in a closed-loop navigation autonomy stack in unstructured human-centric environments. 

## _A. Perceptive RL Locomotion_ 

Locomotion over rough terrains such as stairs or discrete footholds represents a key advantage for legged robots over other locomotion modalities. To handle rough terrain, stateof-the-art approaches leverage environment sensing, typically through either depth cameras or LiDAR units. Several methods construct environment representations such as heightmaps or occupancy grids, which can be queried as policy inputs [4], [5], [2], [3]. Alternatively, sensor data can be used as raw inputs to the policy; in this case, recursive or historybased policies are typically used to deal with limitations of raw sensor data including occlusion or partial observability [20], [8], [6]. While such methods have achieved incredible robustness and agility in unstructured environments, it is worth noting that, as opposed to reference tracking pipelines, 

TABLE I: Comparison of related works. “Method characterization” columns describe the policy and its training; “Deployment characterization” columns describe how the policy is used downstream. “Env. cond.” refers to environmental conditioning of the reference. 

|||**Method **|**characteriz**|**ation**|**De**|**ployment ch**|**aracterization**||
|---|---|---|---|---|---|---|---|---|
|**Method**|**Robot**|**Ref. source**|**Env. cond.**|**Perception**|**Interface**|**Auto. Nav.**|**Long horiz.**|**Terrain**<sup>_†_</sup>|
|_Perceptive locomot_|_ion_||||||||
|DTC [1]|ANYmal|TO (in loop)|✓|Heightmap|Path/footstep|✗|✗|Urban|
|BeamDojo [2]|G1|—|—|Heightmap|SE(2) vel.|✗|✗|Custom|
|Gallant [3]|G1|—|—|Voxel grid|Goal pose|✗|✗|Custom|
|PIM [4]|Various|—|—|Heightmap|SE(2) vel.|✗|✗|Urban|
|AME [5]|ANYmal|—|—|Heightmap|SE(2) vel.|✗|✗|Custom|
|RPL [6]|G1|—|—|Depth|SE(2) vel.|✗|✗|Urban|
|PHP [7]|G1|Mocap<br>|✗|Depth|SE(2) vel.|✗|✗|Parkour|
|Su _et al._ [8]|Biped|LIPM<sup>_‡_ </sup>(in loop)|✗|Depth|SE(2) vel.|✗|✗|Urban|
|_Reference-tracking _|_methods_||||||||
|BeyondMimic [9]|G1|Mocap|✗|—|Full traj.|✓|✗|Flat|
|ZEST [10]|Atlas/G1|Mocap|✗|—|Full traj.|✗|✗|Parkour|
|ASAP [11]|G1|Video|✗|—|Full traj.|✗|✗|Flat|
|VideoMimic [12]|G1|Video|✗|Heightmap|Full traj.|✗|✗|Urban|
|Opt2Skill [13]|Digit|TO|✗|—|Task space|✗|✗|Flat|
|CLF-RL [14], [15]|G1|TO + Mocap|✗|—|SE(2) vel.|✓|✗|Flat|
|_Humanoid navigati_|_on autonomy_||||||||
|Huang _et al._ [16]|Cassie<sup>_∗_</sup>|—|—|Heightmap|Path|✓|✓|Rough|
|StateNav [17]|Digit<sup>_∗_</sup>|—|—|Heightmap|Path|✓|✗|Rough|
|Xiong _et al._ [18]|Cassie<sup>_∗_</sup>|—|—|None|Goal pose|✓|✗|Flat|
|NavILA [19]|G1/Booster|—|—|Heightmap|SE(2) vel.|✓|✗|Flat|
|**Ours**|**G1**|**LIP (in loop)**|✓|**Depth**|**SE(2) vel.**|✓|✓|**Urban**|


> _†_ Terrains deployed on. Rough indicates non-flat terrain. Custom indicates terrains built in lab. Parkour indicates use of non-foot terrain contact. Urban indicates deployment in human environments.<sup>_‡_</sup> Reference is CoM position only.<sup>_∗_</sup> Locomotion controller model-based, operating on ALIP or LIP models. 

reference-free pipelines often give rise to undesirable behaviors such as period-two gaits, undesired environmental contacts such as stair edges or risers, or un-anthropomorphic behaviors. While some work exists on leveraging references to guide RL in unstructured environments for quadrupeds [1] or very recently on humanoids [7], it is a largely undeveloped field for humanoid robots due to the complexity of generating environmentally consistent references. As far as the authors are aware, no work exists where humanoid locomotion is trained using reference-guided RL where the references are modulated to be environmentally consistent during training. 

## _B. Reference-Guided RL for Humanoid Locomotion_ 

Rather than learning complex motion from scratch, many works leverage reference trajectories to guide the reinforcement learning. These are typically seeded with human data, [9], [10], [12], [11], or trajectory optimization [14], [13], [15], [21]. Most methods require a full body trajectory during execution as an input to track, potentially balanced with goal conditioning to accomplish behavioral goals. Requiring reference trajectories for deployment presents a significant bottleneck when deploying the controller in an autonomy stack, especially when interactions with the environment are nontrivial. Some preliminary work using diffusion models to generate reference trajectories online has been investigated [9], but has yet to demonstrate navigation beyond short indoor trajectories avoiding a single obstacle on flat ground. In general, few reference-tracking pipelines are conditioned on environmental perception, and deployment in autonomous navigation is underdeveloped. 

The use of reduced order models to shape rewards has also been investigated, although synthesizing full-body reference trajectories has not been studied. The LIP model was used to plan footsteps [22], but hardware deployment was blind on flat ground. Perceptive techniques have been investigated on a simple 6-DoF point foot biped [8], where the LIP model is used to incentivize the CoM to stay within stable regions. 

## _C. Humanoid Navigation Autonomy_ 

Despite great strides being made in quadruped autonomy [23], [24], and humanoid locomotion, relatively few works exist on humanoid navigation autonomy in unstructured environments. The use of model predictive control for humanoid path planning is well studied [18], and has been combined with traversability analysis for handling rough terrain [25], [16], [17]. However, in the context of terrainaware navigation, nearly all works utilize blind locomotion policies, and handle roughness in the terrain through robustness rather than perception. Modern perception-based locomotion approaches have yet to be deployed in autonomous navigation architectures. The authors hypothesize that nonstandard interfaces with higher level planning layers (training only to reach goal positions [3], requiring full degree of freedom reference trajectories at runtime [9], etc.) make this integration into autonomous navigation difficult. Our method interfaces with _SE_ (2) velocity commands, integrating with standard autonomous navigation pipelines. Our deployment on long-horizon navigation tasks through human-centric environments containing both rough terrain and stairs is novel and highlights the utility of our training methodology. 

## III. ENVIRONMENTALLY CONSISTENT REFERENCE GENERATION 

This section details the use of the Linear Inverted Pendulum (LIP) model to generate environmentally consistent reference trajectories for the feet, center of mass, and arms. Humanoid locomotion is inherently underactuated, as the center of mass cannot be arbitrarily controlled due to contact and input constraints. The LIP model is a standard in humanoid locomotion which models the robot as a point mass vaulting over its stance foot, as shown in Fig. 3. 

## _A. Gait Synthesis via Linear Inverted Pendulum_ 

The LIP model is described by a state **x** _l_ := [ _p v_ ]<sup>_⊤_</sup> , with _p_ the position of the center of mass with respect to the stance foot, and _v_ its velocity. Assuming the mass remains at a constant height _z_ 0 above the ground, the LIP evolves according to dynamics [26], with _λ_ = ~~�~~ _g/z_ 0 


Finally, the LIP model is assumed to step at a fixed period _T_ = 0 _._ 4 _s_ . Upon a step, the position state _p_ is updated to be relative to the new stance foot. Given a step of length _u_ , the step-to-step dynamics [26] are given by integrating the continuous time dynamics and applying the position reset: 


We treat the sagittal and lateral planes of the robot as decoupled LIP models. During steady-state walking, the sagittal plane will evolve according to a period one gait, while the lateral plane is period two. 

Next, consider a desired _SE_ (2) velocity command, **v**<sup>_d_</sup> = [ _vx_<sup>_d,v_</sup> _y_<sup>_d,ω_</sup> _z_<sup>_d_]</sup><sup>_⊤_,wherethesubscript</sup><sup>_x_correspondstothe</sup> sagittal plane, and _y_ the lateral plane. The linear velocities correspond directly to desired step lengths in the sagittal and lateral planes, **u**<sup>_d_</sup> = [ _u_<sup>_d_</sup> _x_<sup>_,ud_</sup> _y_<sup>]</sup><sup>_⊤_:</sup> 


where _u_<sup>_d_</sup> _y,_ 1<sup>and</sup><sup>_ud_</sup> _y,_ 2<sup>arethefirstandsecondstepsofthe</sup> period two lateral gait, and _w >_ 0 is the nominal lateral step width. Given these desired step lengths, the post-impact state of the center of mass can be solved for as the fixed point of the step-to-step dynamics. First, in the sagittal plane: 


And second, solving for both steps in the lateral plane: 


Where **x**<sup>_d_</sup> _x_<sup>isthedesiredpost-impactsagittalpositionand</sup> velocity of the CoM, and **x**<sup>_d_</sup> _y,_ 1<sup>,</sup><sup>**x**</sup><sup>_d_</sup> _y,_ 2<sup>arethedesiredpost-</sup> impact lateral position and velocity, for the first and second step respectively. The position of the center of mass at time _t ∈_ [0 _, T_ ) is then recovered from the continuous time dynamics: 


where _i_ indexes the sagittal and lateral planes, and _j_ indexes the first and second steps for the period two lateral gait. Finally, the yaw of the CoM is computed to ensure zero yaw relative to the stance foot during mid-stance: 


Given the center of mass trajectory and desired footstep locations, the rest of the humanoid reference trajectory is established heuristically. The roll and pitch of the root are fixed to zero, as are the arm and waist joints. The swing foot trajectory is a bezier curve connecting the initial position of the swing foot, **x** _sw,_ 0 to the desired step location **u**<sup>_d_</sup> : 


with _b_ ( _t_ ) the unique third order polynomial satisfying 


The _z_ height of the swing foot follows an identical bezier curve up and down, with _z_ ¯ _sw_ the maximum swing height: 


The roll and pitch of the swing foot are held at zero, and the yaw of the swing foot follows a similar bezier curve, such that it will align with the CoM at the next mid-stance: 


The z-height of the center of mass ( _zd_ ( _t_ )) and the arms ( _θd_<sup>_i_(</sup><sup>_t_)</sup> for _i ∈{l, r}_ ) are given sagittal velocity dependent sinusoids: 


where _za, θa_ are the amplitudes at the maximum forward speed, _v_ ¯ _x_<sup>_d_,and</sup><sup>_θ_</sup> 0<sup>_i_arephaseoffsetssuchthatthearmsswing</sup> in opposite phase to the legs. 

This construction specifies a complete _SE_ (2) controllable reference trajectory for the humanoid robot while walking on flat ground. This construction is not novel, and follows closely from previous work [26], with the addition of heuristic references for the arms and vertical component of the center of mass. 


Fig. 3. Modification of the LIP reference for terrain consistency. (a) The nominal reference, composed of footstep **u**<sup>_d_</sup> , swing foot trajectory **x** _sw_ ( _t_ ), and pelvis reference **x**<sup>_d_</sup> ( _t_ ). (b) Projected footstep **u** _∗_<sup>_d_and upper convex hull</sup> of terrain. (c) Modified swing trajectory **s**<sup>_∗_</sup> _sw_<sup>(</sup><sup>_t_)andverticalstepdeviation</sup> line. (d) Modified pelvis trajectory **x**<sup>_d_</sup> _∗_<sup>(</sup><sup>_t_),terrainconsistentreferences.</sup> 

## _B. Adjustment for Terrain Consistency_ 

The primary contribution of this work is the rapid synthesis of an environmentally consistent reference in the training loop. To accomplish this, we adjust the CoM and swing foot trajectories to be consistent with the environment over the next step, as pictured in Fig. 3. First, we project the desired footstep location onto a valid foothold. 


Where _G_ ( _a, b_ ) takes the _x, y_ position _a_ expressed in the frame of _b_ and expresses it in the world frame, and proj( _u_ ) projects a desired footstep location onto the nearest valid footstep location. **x**<sup>_W_</sup> _st_<sup>isthelocationofstancefootinthe</sup> world frame. To facilitate rapid GPU-parallelized projection, polygons denoting valid footholds are constructed with the terrain. The terrain is divided into a grid, and each grid cell stores an array of possible polygons to project to from within its grid cell. To query the projection operation, the desired foothold is projected onto every polygon in its corresponding grid cell, and the shortest projection is taken. The roll and pitch ( _rd, pd_ ) of the terrain at the projection point are noted. 

The _x, y, θ, ϕ, ψ_ of the swing foot trajectory are all modified to connect the initial foot pose to the desired pose (including the roll and pitch of the terrain at the step location), using the same bezier construction as in (10). With the _x, y_ trajectory of the swing foot fixed, the height of the terrain is scanned along the trajectory. The _z_ swing height is modified by adding the height of the upper convex hull of the terrain points on the swing trajectory. Finally, the height of the line joining the current stance foot to the projected step location is added to the _z_ height of the CoM trajectory. These modifications to enforce terrain consistency are visualized in Fig. 3. Importantly, these modifications are general, working for a variety of terrains including stairs, slopes, and discrete footholds, allowing the method to be adapted to any terrain. 

## IV. LOCOMOTION AND NAVIGATION METHODOLOGY 

We outline a single-stage, MLP-based locomotion training setup which maps the current depth image and proprioception directly to actions. 

## _A. Reward Design via CLF-RL_ 

We build on previous work leveraging Control Lyapunov Functions for Reward Design [14], [15]. Given desired trajectories for the pelvis, swing foot, and joints, we design quadratic Lyapunov functions _Vi_ ( _x_ ) for each of the tracking objectives. For each tracking objective, we then provide two reward terms, 


Where _wj,i >_ 0 are reward weights and _σj,i >_ 0 are scaling parameters. The first reward encourages tracking the reference signal closely, while the second condition incentivizes satisfying the Lyapunov decrescent condition. This effectively densifies the reward, allowing the system to achieve some reward even when tracking is poor, provided the system is moving towards the reference as quantified by the Lyapunov function. 

## _B. Depth Camera Simulation_ 

The robot is equipped with a single ZED Mini depth camera mounted on the torso, facing downwards. At deployment, the ZED SDK [27] runs depth reconstruction on the 1080p image at 35Hz using the ’NEURAL’ setting onboard the Jetson Orin integrated with the Unitree G1 robot. The image is then down-sampled via nan-aware averaging to a resolution of 26x30. To simulate this sensor in IsaacLab, a 26x30 raycast is performed using a pinhole camera model with intrinsics reported by the ZED Mini camera. Following [3], self-scans of the robot geometry (dynamic meshes) are handled by transforming the rays into each mesh’s local frame before raycasting: 


The goal is to cast a ray starting from position **p** , in direction **d** , onto a mesh _M_ which has been transformed by homogeneous transform _T_ with rotational component _R_ relative to its mesh frame. We instead compute the raycast by transforming the ray origin into the mesh local frame via _T_<sup>_−_1</sup> **p** , and rotating the cast directions into the mesh frame, _R_<sup>_−_1</sup> **d** , then casting against a static mesh in its own frame. The result of the raycast is reported in Z-depth to match the depth image computation. 

## _C. Asymmetric Actor-Critic Implementation_ 

As the RL pipeline is centered around reward tracking, the reward signals are quite dense, and the training pipeline can be considerably simplified relative to existing humanoid perceptive locomotion pipelines. We adopt a single-stage asymmetric actor-critic framework with MLP 

networks, where the actor is given noised proprioception and depth measurements, as well as noise-free velocity commands and phasing variable. Our depth noise model is simple compared to most (the image is aggressively downsampled, which smooths edge artifacts and other standard depth image artifacts); we first sample a random bias plane which is added to the entire image, and then add uniform random noise. The critic is given noise-free observations and additional privileged information including desired reference trajectories and actual outputs of the system, desired and actual contact states, and a ground truth height scan. 

We train on a curriculum-based, randomized terrain consisting of rough terrain, slopes and stairs, pictured in Fig. 2. Velocity commands are randomized, consisting of sampleand-hold commands, and PD control to target positions. To facilitate transfer to hardware, we domain randomize across parameters including actuator gains, friction coefficients, mass distributions, disturbances, and joint offsets. 

## _D. Model Predictive Control for Navigation_ 

The output of our RL pipeline is a reference-guided perceptive locomotion policy which takes _SE_ (2) velocity commands as input. To solve navigation problems, we pair this locomotion policy with a navigation planner, which takes in an environment representation and a goal pose, and drives the robot along a collision free path to the goal. We use model-predictive control on a single integrator with heading, discretized at _δt_ = 0 _._ 4 _s_ , which interfaces naturally with _SE_ (2) velocity commands. This model has state **z** = [ _x, y, θ_ ]<sup>_⊤_</sup> _∈_ R<sup>3</sup> the position and heading, and input **v** = [ _v∥, v⊥, ω_ ]<sup>_⊤_</sup> _∈_ R<sup>3</sup> the parallel, perpendicular, and angular velocities. The navigation MPC problem is written over horizon _N_ = 25: 


Where the cost _J_ is composed of a geometrically consistent quadratic distance to goal penalty ( _c_ handles the cost on heading in a geometrically consistent way, which is locally quadratic) and quadratic input penalty, 


where **z** _g_ = [ _xg, yg, θg_ ]<sup>_⊤_</sup> is the goal pose. The single integrator with heading dynamics are enforced in (17b), the initial condition constraint (17c) extracts the position and heading via the projection map **Π** : _X →_ R<sup>3</sup> given by: 


TABLE II: Cross-attention actor architecture. Depth imagery is fused with proprioception via cross-attention with proprio-query and visual key/value. Input depth image is 26 _×_ 30. 

|**Module**|**Layer**|**Config**|**Output**|
|---|---|---|---|
|Spatial CNN|Conv2D _×_2|ch. [32_,_64], 5_×_5, stride 2,<br>zero-pad|(64_,_7_,_8)<br>|
|Token proj.|Linear|64_→_64|(56_,_64)|
|Proprio enc.|MLP, ELU|_n_prop _→_64_→_64|(64)|
|Cross-attn.|MHA + LN|_d_=64, _h_=4|(64)|
|Actor head|MLP, ELU|128_→_256_→_128_→na_|(_na_)|


TABLE III: Tracking error (norm of position error) by terrain. 

|||Foot|||CoM||
|---|---|---|---|---|---|---|
|Method|Flat|Slopes|Stairs|Flat|Slopes|Stairs|
|unMod-Ref|0.037|0.055|0.142|**0.020**|**0.027**|0.083|
|Ours|0.038|0.053|**0.074**|0.025|0.032|**0.042**|
|Ours (Attn)|**0.032**|**0.045**|0.074|0.021|0.032|0.045|


Lastly, given functions _hi_ : R<sup>3</sup> _→_ R encoding distance to each obstacle _i_ , we enforce separate discrete-time control barrier constraints (17e) to perform obstacle avoidance [28]. 


The parameter _α ∈_ (0 _,_ 1) controls how quickly obstacles can be approached, and the parameter _δ >_ 0 robustifies the obstacle by a margin, enforcing a distance the plan must stay away from obstacle boundaries. Choosing _α, δ_ conservatively robustifies the plan against the tracking error which will occur when the plan is tracked on the full order system [29]. 

## V. EXPERIMENT AND RESULTS 

We deploy the trained policy on hardware, and evaluate the impact of the environmentally consistent reference in simulation. Additionally, we demonstrate integration in a navigation autonomy stack by pairing the controller with an MPC controller through its _SE_ (2) velocity interface, performing indoor and outdoor navigation tasks autonomously. 

## _A. Training and Deployment_ 

Policies are trained for 30k iterations over 4096 environments on a single NVIDIA 5080 GPU (16GB) in under 20 hours in the IsaacLab [30] training environment using the RSL-RL PPO implementation [31]. During deployment, depth reconstruction for the chest mounted ZED Mini runs on Unitree G1’s integrated NVIDIA Jetson Orin. The policy is inferenced on CPU at 50Hz on an onboard System76 Meerkat minipc. When executing closed loop navigation control, we leverage a localization stack [32] which combines FAST-LIO2 [33], [34] for odometry and lidar deskewing with GICP [35] for localization within a pre-built map. These processes leverage the Livox MID360 LiDAR mounted in the head of the Unitree G1, and both run on the System76 Meerkat minipc. All sensing and compute for deployment is contained and powered onboard the robot. 


Fig. 4. Outdoor autonomous navigation. The robot is localized within an existing map, while MPC plans trajectories through the environment over rough terrain and stairs. Depth images are rendered at a few frames, showing self-scans and terrain geometry. (Left) robot autonomously navigates 15 consecutive stairs. (Right) robot autonomously navigates over 70m, including two staircases. 

## _B. Simulation Study_ 

We validated two key claims in simulation. First, conditioning the references on the environment yields significantly better tracking performance than tracking the nominal references alone. Second, unlike several reference-free papers in the current literature, we are able to achieve similar performance with a much simpler model. To complete this analysis we train two additional versions of our method; first we do not condition the reference on the environment (unMod-Ref). Second, we use an actor network with CNN and an attention-based perception encoder in an architecture similar to recent results in the field, whose architecture is described in Table II. The other policies use an MLP with layers [1024 _,_ 512 _,_ 256 _,_ 128]. Then, we compare the mean normed tracking error across flat, sloped, and stair terrains in Table III. Critically, Ours and Ours (Attn) have statistically similar tracking error in each environment type, but Ours without the attention head is much simpler to implement and inference, and requires significantly less VRAM during training (14Gb vs 60Gb). Additionally, we see that enforcing references to be consistent with the environment improves tracking error by a factor of two in the stairs environment. 

## _C. Real-world deployment_ 

To emphasize the controllability of the learned locomotion policy, we integrate the policy with the MPC-based navigation planner detailed in Section IV. First, a point cloud map of the relevant environment is created by scanning the environment with lidar while running FAST-LIO2. When the robot is deployed, FAST-LIO2 generates high-rate odometry, while GICP matches scans against the precomputed map at a low rate, compensating for potential odometry drift. 

Obstacles in the environment are fit with ellipses or halfplane constraints to promote ease of transcription into 

a nonlinear program. The MPC problem is transcribed via CasADi [36] and solved online via IPOPT [37] once every two steps (0 _._ 8 _s_ ). Inputs are constrained to lie in the set (17d) 


MPC outputs a discrete trajectory ( **z** _k,_ **v** _k_ ). First, we construct a continuous _SE_ (2) trajectory ( **z** MPC( _t_ ) _,_ **v** MPC( _t_ )) obtained by linearly interpolating **z** _k_ and sample-and-holding **v** _k_ . This continuous trajectory is then tracked via a feedback controller: 


This controller adds a feedback term on the system’s tracking error to the feedforward velocity from the MPC plan, and rotates the linear components of the velocity into the robot’s local frame through **R** ( _t_ ). We recompute this velocity command **v** ( _t_ ) at 10Hz, and pass it to the locomotion controller. 

We successfully deploy this framework in several outdoor environments for long-horizon autonomous navigation. We autonomously navigate standard human staircases, including a section of 15 stairs (Fig. 4 left), and a trial spanning over 70m including tree roots, rough terrain, curbs, and two sets of stairs (Fig. 4 right). An additional trial, where the robot climbs a staircase, enters a building through a door, and then climbs indoor stairs, is pictured in Fig. 1. As surveyed in Table I, prior humanoid navigation autonomy systems rely on blind, model-based locomotion, and prior perceptive locomotion methods have not been integrated into closedloop autonomy at this scale. The deployment described here demonstrates a perception-conditioned, reference-guided RL policy serving as the locomotion layer of a long-horizon autonomy stack on a humanoid platform. 

## VI. CONCLUSION 

We have presented a method for synthesizing environmentally-consistent reference trajectories inside the RL training loop for humanoid locomotion, and demonstrated its integration into a closed-loop navigation autonomy stack on the Unitree G1. The proposed LIP-based reference synthesis is fast enough to run inside the training loop, and the resulting policy substantially reduces stair tracking error compared to tracking references which are not modified to be consistent with the environment. Furthermore, the method exposes a useful _SE_ (2) velocity interface, enabling long-horizon outdoor deployments to demonstrate its efficacy as the locomotion layer of a humanoid autonomy stack in human-centric environments. 

Future work looks to extend this result in two directions. First, modulating references from other sources, such as human data or trajectory optimization, to be consistent with arbitrary terrain online stands to reduce the demands of offline data collection, and improve the distribution of environments seen during training. Second, we plan to incorporate knowledge of the terrain-dependent capabilities of the locomotion controller (traversability, risk) into the planning layer to allow autonomous deployment of policies with highly varied and dynamic skill sets such as running, which add significant terrain-dependent constraints on what commands the mid-level controller can send to the locomotion policy. 

## REFERENCES 

- [1] F. Jenelten, J. He, F. Farshidian, and M. Hutter, “Dtc: Deep tracking control,” _Science Robotics_ , vol. 9, no. 86, p. eadh5401, 2024. 

- [2] H. Wang _et al._ BeamDojo: Learning Agile Humanoid Locomotion on Sparse Footholds. [Online]. Available: http://arxiv.org/abs/2502.10363 

- [3] Q. Ben _et al._ Gallant: Voxel Grid-based Humanoid Locomotion and Local-navigation across 3D Constrained Terrains. [Online]. Available: http://arxiv.org/abs/2511.14625 

- [4] J. Long _et al._ , “Learning humanoid locomotion with perceptive internal model,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 9997–10 003. 

- [5] J. He, C. Zhang, F. Jenelten, R. Grandia, M. B¨acher, and M. Hutter, “Attention-based map encoding for learning generalized legged locomotion,” _Science Robotics_ , vol. 10, no. 105, p. eadv3604, 2025. 

- [6] Y. Zhang _et al._ , “Rpl: Learning robust humanoid perceptive locomotion on challenging terrains,” _arXiv preprint arXiv:2602.03002_ , 2026. 

- [7] Z. Wu _et al._ , “Perceptive humanoid parkour: Chaining dynamic human skills via motion matching,” _arXiv preprint arXiv:2602.15827_ , 2026. 

- [8] H. Su, H. Luo, S. Yang, K. Jiang, W. Zhang, and H. Chen, “Lipmguided reinforcement learning for stable and perceptive locomotion in bipedal robots,” in _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2025, pp. 1031–1038. 

- [9] Q. Liao _et al._ , “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

- [10] J. P. Sleiman _et al._ , “Zest: Zero-shot embodied skill transfer for athletic robot control,” _arXiv preprint arXiv:2602.00401_ , 2026. 

- [11] D.-H. Lee, S. Choi, and K.-I. Na, “Asap: Agile and safe pursuit for local planning of autonomous mobile robots,” _IEEe Access_ , vol. 12, pp. 99 600–99 613, 2024. 

- [12] A. Allshire _et al._ , “Visual imitation enables contextual humanoid control,” _arXiv preprint arXiv:2505.03729_ , 2025. 

- [13] F. Liu _et al._ , “Opt2skill: Imitating dynamically-feasible whole-body trajectories for versatile humanoid loco-manipulation,” _IEEE Robotics and Automation Letters_ , 2025. 

- [14] K. Li, Z. Olkin, Y. Yue, and A. D. Ames, “Clf-rl: Control lyapunov function guided reinforcement learning,” _IEEE Robotics and Automation Letters_ , 2026. 

- [15] Z. Olkin, W. D. Compton, R. M. Bena, and A. D. Ames, “Chasing autonomy: Dynamic retargeting and control guided rl for performant and controllable humanoid running,” _arXiv preprint arXiv:2603.25902_ , 2026. 

- [16] J.-K. Huang and J. W. Grizzle, “Efficient anytime clf reactive planning system for a bipedal robot on undulating terrain,” _IEEE Transactions on Robotics_ , vol. 39, no. 3, pp. 2093–2110, 2023. 

- [17] Z. Yoon, L. Y. Zhu, J. Lu, L. Gan, and Y. Zhao, “State-nav: Stabilityaware traversability estimation for bipedal navigation on rough terrain,” _IEEE Robotics and Automation Letters_ , vol. 11, no. 2, pp. 2338– 2345, 2025. 

- [18] X. Xiong, J. Reher, and A. Ames. Global Position Control on Underactuated Bipedal Robots: Step-to-step Dynamics Approximation for Step Planning. [Online]. Available: http://arxiv.org/abs/2011.06050 

- [19] A.-C. Cheng _et al._ , “Navila: Legged robot vision-language-action model for navigation,” _arXiv preprint arXiv:2412.04453_ , 2024. 

- [20] Z. Zhuang, S. Yao, and H. Zhao, “Humanoid parkour learning,” _arXiv preprint arXiv:2406.10759_ , 2024. 

- [21] F. Yu, R. Batke, J. Dao, J. Hurst, K. Green, and A. Fern, “Dynamic bipedal turning through sim-to-real reinforcement learning,” in _2022 IEEE-RAS 21st International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2022, pp. 903–910. 

- [22] H. J. Lee, S. Hong, and S. Kim, “Integrating model-based footstep planning with model-free reinforcement learning for dynamic legged locomotion,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 11 248–11 255. 

- [23] A. Agha _et al._ , “Nebula: Team costar’s robotic autonomy solution that won phase ii of darpa subterranean challenge,” _Field robotics_ , vol. 2, pp. 1432–1506, 2022. 

- [24] A. Dixit, D. D. Fan, K. Otsu, S. Dey, A.-A. Agha-Mohammadi, and J. Burdick, “Step: Stochastic traversability evaluation and planning for risk-aware navigation; results from the darpa subterranean challenge,” _Field Robotics_ , vol. 4, pp. 182–210, 2024. 

- [25] Y.-C. Lin and D. Berenson, “Long-horizon humanoid navigation planning using traversability estimates and previous experience,” _Autonomous Robots_ , vol. 45, no. 6, pp. 937–956, 2021. 

- [26] X. Xiong and A. Ames. 3D Underactuated Bipedal Walking via H-LIP based Gait Synthesis and Stepping Stabilization. [Online]. Available: http://arxiv.org/abs/2101.09588 

- [27] Stereolabs, “ZED SDK,” https://www.stereolabs.com/developers/, 2024, version 5.1. 

- [28] A. Agrawal and K. Sreenath, “Discrete control barrier functions for safety-critical control of discrete systems with application to bipedal robot navigation.” in _Robotics: Science and Systems_ , vol. 13. Cambridge, MA, USA, 2017, pp. 1–10. 

- [29] M. H. Cohen, N. Csomay-Shanklin, W. D. Compton, T. G. Molnar, and A. D. Ames, “Safety-critical controller synthesis with reducedorder models,” in _2025 American Control Conference (ACC)_ . IEEE, 2025, pp. 5216–5221. 

- [30] M. Mittal _et al._ , “Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning,” _arXiv preprint arXiv:2511.04831_ , 2025. [Online]. Available: https://arxiv.org/abs/2511.04831 

- [31] C. Schwarke, M. Mittal, N. Rudin, D. Hoeller, and M. Hutter, “Rsl-rl: A learning library for robotics research,” _arXiv preprint arXiv:2509.10771_ , 2025. 

- [32] W. Compton, “LIO-Localization: A ROS2 workspace for LiDARinertial odometry-based mapping and localization,” https://github.com/ wdc3iii/LIO-Localization, 2026, accessed: 2026-04-26. 

- [33] W. Xu and F. Zhang, “Fast-lio: A fast, robust lidar-inertial odometry package by tightly-coupled iterated kalman filter,” _IEEE Robotics and Automation Letters_ , vol. 6, no. 2, pp. 3317–3324, 2021. 

- [34] W. Xu, Y. Cai, D. He, J. Lin, and F. Zhang, “Fast-lio2: Fast direct lidarinertial odometry,” _IEEE Transactions on Robotics_ , vol. 38, no. 4, pp. 2053–2073, 2022. 

- [35] A. Segal, D. Haehnel, and S. Thrun, “Generalized-ICP,” in _Proceedings of Robotics: Science and Systems_ , Seattle, USA, June 2009. 

- [36] J. A. E. Andersson, J. Gillis, G. Horn, J. B. Rawlings, and M. Diehl, “CasADi – A software framework for nonlinear optimization and optimal control,” _Mathematical Programming Computation_ , vol. 11, no. 1, pp. 1–36, 2019. 

- [37] A. W¨achter and L. T. Biegler, “On the implementation of an interiorpoint filter line-search algorithm for large-scale nonlinear programming,” _Mathematical programming_ , vol. 106, no. 1, pp. 25–57, 2006. 

