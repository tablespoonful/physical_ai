---
title: "FastStair: Learning to Run Up Stairs with Humanoid Robots"
date: "2026-01-15"
authors: "Yan Liu; Tao Yu; Haolin Song; Hongbo Zhu; Nianzong Hu; Yuzhi Hao"
url: https://arxiv.org/abs/2601.10365
pdf: https://arxiv.org/pdf/2601.10365
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.10365)** / [論文ページ](https://arxiv.org/abs/2601.10365)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **FastStair: Learning to Run Up Stairs with Humanoid Robots** 

Yan Liu<sup>1</sup><sup>_,_2</sup> , Tao Yu<sup>2</sup> , Haolin Song<sup>4</sup> , Hongbo Zhu<sup>2</sup><sup>_,_5</sup> , Nianzong Hu<sup>2</sup> , Yuzhi Hao<sup>2</sup><sup>_,_6</sup> , Xiuyong Yao<sup>2</sup> , Xizhe Zang<sup>1†</sup> , Hua Chen<sup>2</sup><sup>_,_3†</sup> , Jie Zhao<sup>1</sup> 

**_Abstract_ — Running up stairs is effortless for humans but remains extremely challenging for humanoid robots due to the simultaneous requirements of high agility and strict stability. Model-free reinforcement learning (RL) can generate dynamic locomotion, yet implicit stability rewards and heavy reliance on task-specific reward shaping tend to result in unsafe behaviors, especially on stairs; conversely, model-based foothold planners encode contact feasibility and stability structure, but enforcing their hard constraints often induces conservative motion that limits speed. We present FastStair, a planner-guided, multistage learning framework that reconciles these complementary strengths to achieve fast and stable stair ascent. FastStair integrates a parallel model-based foothold planner into the RL training loop to bias exploration toward dynamically feasible contacts and to pretrain a safety-focused base policy. To mitigate planner-induced conservatism and the discrepancy between low- and high-speed action distributions, the base policy was fine-tuned into speed-specialized experts and then integrated via Low-Rank Adaptation (LoRA) to enable smooth operation across the full commanded-speed range. We deploy the resulting controller on the Oli humanoid robot, achieving stable stair ascent at commanded speeds up to 1.65 m/s and traversing a 33step spiral staircase (17 cm rise per step) in 12 s, demonstrating robust high-speed performance on long staircases. Notably, the proposed approach served as the champion solution in the Canton Tower Robot Run Up Competition. Project Page: https://npcliu.github.io/FastStair.** 


Fig. 1. Full-scale humanoid robot Oli performing agile stair-climbing locomotion: (a) parallel foothold planning in IsaacLab, (b) climbing a staircase with 20 cm step height, (c) Canton Tower Run-up, and (d) highspeed ascent. 

## I. INTRODUCTION 

Humanoid robots have attracted significant interest because of their superior terrain adaptability, yet they remain far from matching human agile and stable locomotion. Staircases, a ubiquitous feature of human environments, present a particular challenge. While humans navigate them intuitively, robots face an inherent trade-off between agility and stability that remains unresolved. This trade-off has plagued state-ofthe-art locomotion control methods, hindering the deployment of humanoid robots in real-world stair-climbing tasks. 

* Work done at LimX Dynamics. Project lead: Tao Yu † Corresponding author 

> 1School of Mechanics Engineering, Harbin Institute of Technology (HIT), Harbin Heilongjiang 150001, China. Email: liuyan98@stu.hit.edu.cn, zangxizhe@hit.edu.cn, jzhao@hit.edu.cn 

> 2 LimX Dynamics, Shenzhen, China. 

> 3 Zhejiang University-University of Illinois Urbana-Champaign Institute (ZJUI), Haining, China. Email: huachen@intl.zju.edu.cn 

> 4 Department of Electronic Engineering and Information Science (EEIS), University of Science and Technology of China, Hefei 230027, China. Email: hlsong@mail.ustc.edu.cn 

> 5 Hong Kong University of Science and Technology, Hong Kong SAR, China. Email: Email: hzhubi@connect.ust.hk 

> 6 Department of Mechanical Engineering, National University of Singapore, Singapore 117575. Email: yuzhihao@u.nus.edu 

Reinforcement Learning (RL) has emerged as a powerful paradigm for generating dynamic humanoid locomotion [1]– [3]. Although RL can achieve impressive speeds on flat terrain [1], its application to challenging terrains like staircases often exposes a fragility. This vulnerability stems from the reliance on implicit stability rewards, where dynamic stability is not explicitly guaranteed but is instead encouraged through a ensemble of heuristic reward terms, such as alive, posture, and gravity-projection. On stairs, these implicit objectives frequently conflict with task-level rewards such as high-velocity tracking. This inherent contradiction forces the learning process into a trade-off where the pursuit of agility often leads the robot to sacrifice the very rewards that maintain stability. Consequently, most current stairclimbing control schemes, including both ”blind” [4], [5] and perception-augmented [6]–[9] approaches, tend to prioritize safety by heavily weighting stability terms over speed. This prioritization effectively forfeits the potential for high-speed locomotion and results in the conservative behaviors typical of existing RL-based stair climbers. 

In contrast, model-based planner provides explicit stability guarantees by computing feasible footholds under model 

and environment constraints [10]–[13]. By enforcing hard constraints on capture regions and footstep placement, the planner ensure a high degree of safety. However, this rigorous adherence to feasibility constraints often induces conservative motion, which narrows the exploration space and limits the robot’s dynamic agility. 

A natural strategy to bridge this gap is to utilize modelbased planners to guide RL exploration toward explicitly safe and feasible contacts. However, such guidance often transfers planner’s inherent conservatism to the learned policy, resulting in behaviors that are safe but lack the requisite agility for high-speed tasks. This persistent tension between plannerguided safety and learned agility motivates the development of a framework that can reconcile these complementary strengths. 

In this work, we propose FastStair, a planner-guided, multi-stage learning framework that reconciles model-based stability with learned agility to achieve high-speed stairclimbing locomotion. 

First, regarding the foothold planner, compared with mainstream ALIP-based MPC methods [10], [13], planners based on the Divergent Component of Motion (DCM) admit analytical expressions [14] and permit relatively simple constraint formulations. These properties make DCM-based planners readily convertible into discrete-search formulations that are well suited for GPU-parallel computation and therefore appropriate for guiding RL training. 

Second, to resolve the inefficiency of implicit safety exploration, we integrate a parallel DCM-based foothold planner [14] into the RL loop. By reformulating the optimization as a parallel discrete search, we avoid reliance on parallel real-time optimization solvers and guide exploration toward dynamically feasible safety regions. This ”optimization-assearch” approach provides the real-time guidance necessary to pretrain a safety-focused base policy with negligible computational overhead. 

Finally, to mitigate planner-induced conservatism, we adopt a multi-stage training framework. Owing to the discrepancy in action distributions between low- and highvelocity motion, a single policy struggles to track the full commanded-speed range efficiently. Accordingly, in the second stage, the base policy was fine-tuned into two speedspecialized experts via velocity-related reward reweighting. However, direct switching between these experts causes instability (e.g., chattering). To address this, in the third stage, the parameters of both experts were integrated into a single network with low-rank adaptation (LoRA) layers on their branches. The integrated model was then fine-tuned over the full commanded speed range, yielding a unified policy that transitions smoothly across full speed range and enables stable, high-speed stair climbing. 

Our main contributions can be summarized as follows: 

- To enhance stability on challenging staircases, we introduce a DCM-based foothold planner as an explicit stability reward, which guides the reinforcement learning exploration toward dynamically feasible footholds on challenging stairs. 

- To mitigate the prohibitive training overhead of incorporating real-time optimization into parallel RL, we reformulate the foothold optimization as a parallelized discrete search, accelerating the training speed by approximately 25 times. 

- To mitigate planner-induced conservatism and improve velocity-tracking performance, we propose a multi-stage framework that fine-tunes high-speed and low-speed experts from a safety-focused base policy, achieving high-speed locomotion without sacrificing stability or low-speed tracking accuracy. 

- To address instabilities arising from expert switching, the experts were merged into a single network and finetuned using LoRA, which enabled smooth transitions between experts and produced a unified policy that operates robustly across the full commanded-speed range. 

## II. RELATED WORK 

## _A. Model-based Locomotion on Challenging Terrains_ 

Classical model-based methods, such as those based on the DCM [14] and Model Predictive Control (MPC), provide a rigorous mathematical foundation for foothold planning [10], [12], [15]. By encoding contact feasibility and balance criteria as explicit kinemodynamic constraints, these methods excel at maintaining stability on discrete terrains like stairs or stepping stones. However, ensuring real-time computational feasibility often necessitates simplifying assumptions, such as the linear inverted pendulum model, alongside the use of conservative safety margins. These constraints inevitably restrict the reachable solution space, inducing the conservative locomotion that hinder high-speed agility. 

## _B. Learning-based Humanoid Locomotion on Stairs_ 

Recent advancements in deep reinforcement learning (RL) have significantly enhanced the terrain adaptability of humanoid robots. Residual-based methods [8], [9], [16] typically employ a two-stage pipeline where a vision-based network provides corrective residuals to a frozen blind policy. While effective, these decoupled architectures often require complex coordination and may limit the robot’s peak agility due to the restricted search space of the residual. Conversely, end-to-end frameworks [6], [7] unify perception and control, but they often struggle with the severe exploration bottlenecks of pure RL, especially when traversing discrete terrains like stairs without explicit motion priors. 

To further enhance locomotion performance, researchers have explored specialized training strategies. For instance, [17] uses a curriculum based on scan points, while [18] leverages human motion retargeting to induce natural behaviors. However, these methods often fail to ensure strict dynamical feasibility at high speeds. Our work diverges by using a multi-stage training framework—transitioning from safety-critical pre-training to specialized experts. By integrating these experts into a single network via LoRA [19], we achieve high-speed stair climbing that surpasses the conservative limits of single-policy RL. 


Fig. 2. Overview of the FastStair framework. During the pre-training stage, a parallel DCM-based foothold optimizer generates dynamically feasible contacts to guide policy learning via a foothold-tracking reward. In the post-training stage, the pre-trained base model is fine-tuned into high- and low-speed expert policies by expanding the commanded velocity range and adjusting reward weights to mitigate planner-induced conservatism; this decomposition is motivated by the distinct action distributions at high versus low speeds. However, direct switching between experts can cause control discontinuities, so in the LoRA fine-tuning stage we merge their parameters into a single network and fine-tune it with LoRA. The resulting unified policy ensures robust tracking across the full velocity range for deployment on the physical robot. 

## III. METHOD 

We propose a multi-stage training framework, FastStair, designed to enable high-speed stair climbing while ensuring robust traversal success rates. An overview is depicted in Fig. 2. In the pre-training stage, we incorporate parallel DCM-based foothold planning to guide the policy via a large foothold-tracking reward. While this prioritization ensures safety, it inevitably compromises velocity tracking accuracy. To address this, the post-training stage rebalances reward weights to prioritize velocity tracking and trains separate high-speed and low-speed expert policies, initialized from the pre-trained model. Finally, in the fine-tuning stage, these experts are integrated into a network and fused via LoRA. This yields a single unified policy capable of reliable traversal across the full commanded velocity range. The details of this three-stage procedure are described below. 

## _A. Parallel Foothold Planning_ 

Traversing complex terrain requires selecting safe, flat footholds. However, acquiring this capability is often challenging for pure RL. To bridge this gap, we incorporate a model-based planner to guide foothold selection. While conventional planning methods [10], [20] demonstrate robust 

performance, they typically rely on serial CPU-based optimization solvers, rendering them incompatible with massive parallel RL frameworks. Even recent advancements in parallel optimization [21] often incur non-trivial computational overhead when scaled. To address this, we formulate a DCM-based foothold optimization problem and reformulate it as a parallel discrete search task. By solving this task via vectorized tensor operations, we leverage the GPU’s massive parallelism, ensuring the planner incurs negligible computational overhead during training. 

_1) DCM for Stair Climbing:_ Following [22], we model the system dynamics using the Variable-Height Inverted Pendulum (VHIP), governed by: _x_ ¨ = _ω_<sup>2</sup> _x,_ where _x ∈_ R denotes position in the forward direction. To accommodate stair climbing, we define the Center of Mass (CoM) height trajectory _z_ ( _t_ ) during the swing phase (duration _T_ ) as a linear function _z_ ( _t_ ) = _kt_ + _z_ 0, where _z_ 0 represents the nominal standing height and _k_ denotes the vertical slope. Consequently, the natural frequency is given by _ω_ = ~~�~~ _g/z_ ( _t_ ), where _g_ is the gravitational acceleration. Fig. 3 illustrates this VHIP formulation applied to stair negotiation. The DCM is defined as _ξ_ = _x_ + _ω_<sup><u>1</u></sup><sup>_x_˙.Differentiatingwithrespecttotime</sup> 


Fig. 4. Terrain-perception information. Blue markers show terrain scandots, green the averaged gradient map, light blue the local averaged gradient map, and red the optimal footholds. 

Fig. 3. Inverted-pendulum stair-climbing process. 


where _a_ = 1 + 2<sup>_~~√~~_</sup> _<u>kgz</u>_<sup>.Consideringamaximumstairincline</sup> of _±_ 45<sup>_◦_</sup> (implying _k ∈_ [ _−_ 1 _,_ 1]) and a nominal standing height _z_ 0 _≈_ 1 m, the coefficient _a_ remains within the range [0 _._ 84 _,_ 1 _._ 16]. Given that _a_ is close to unity, we approximate _a ≈_ 1 to simplify the optimization. This yields the dynamics _ξ_ ˙ _≈ ωξ_ with a time-varying _ω_ . Consequently, the DCM evolution for stair climbing at time _t ∈_ [0 _, T_ ] is given by: _ξ_ ( _t_ ) = _ξ_ 0 _e_ �0 _t_<sup>_ω_(</sup><sup>_τ_)</sup><sup>_dτ_</sup> _. 2) DCM-based Foothold Optimization:_ Leveraging the structural similarity between our derived dynamics and the standard planar DCM model, we adapt the optimization formulation from [14]: 


The integrated natural frequency is explicitly given 2<sup>_~~<u>√</u>~~_</sup> _<u>g</u>_ ~~<u>(</u>~~ _~~<u>√</u>~~ kt_ + _z_ 0 _−_<sup>_~~<u>√</u>~~_</sup> _<u>z</u>_ 0 ~~<u>)</u>~~ by: _σ_ ( _t_ ) = �0 _t_<sup>_ω_(</sup><sup>_τ_)</sup><sup>_dτ_=</sup> _k ._ The decision variable _uT ∈_ R<sup>2</sup> represents the planar projection of the candidate foothold, while _b_ denotes the DCM offset [14]. The nominal step targets are defined as _L_ nom = _vx_<sup>_dT_and</sup><sup>_W_nom=</sup> _vy_<sup>_dT_+ (</sup><sup>_−_1)</sup><sup>_il_,where(</sup><sup>_v_</sup> _x_<sup>_d, v_</sup> _y_<sup>_d_)isthedesiredcommandedve-</sup> locity, _i_ is the leg index (left/right), and _l_ denotes the nominal lateral inter-foot distance. Accordingly, the nominal DCM offset is formulated as _b_ nom = [ _e_<sup>_σ_(</sup><sup>_T_</sup> _<u>L</u>_<sup>)</sup> _−_ 1<sup>_,_(</sup><sup>_−_1)</sup><sup>_i_</sup> 1+ _elp_<sup>_σ_(</sup><sup>_T_)</sup><sup>_−_</sup> 1 _−eW_<sup>_σ_(</sup><sup>_T_)]. The feasible foothold set</sup><sup>_P_is derived from a local</sup> elevation map (spanning 1 _._ 8 m _×_ 1 _._ 2 m) centered on the robot, as visualized by the blue points in Fig. 4. The term _S_ ( _uT_ ) quantifies the terrain steepness cost (indicated by light-blue points in Fig. 4). 

_3) Steepness Score Calculation:_ The steepness score _S_ ( _uT_ ) evaluates local terrain gradients to identify feasible contact patches. Upon acquiring the elevation map, we 

compute the spatial gradient using a Sobel operator, implemented efficiently as a GPU-parallelized convolution. To account for the robot’s planar foot morphology, we apply a subsequent local neighborhood aggregation step (also via convolution) over a kernel matching the foot dimensions. In the resulting cost map, higher values correspond to steeper terrain, indicating reduced suitability for foothold placement. 

_4) Optimization-to-Search Reformulation:_ Directly solving large-scale optimization problems in real-time typically incurs prohibitive computational overhead, creating a bottleneck for parallel RL. To overcome this, we reformulate the optimization into a parallel discrete search. We observe that the feasible foothold set _P_ (blue points in Fig. 4) is naturally discretized by the elevation map resolution and can be encoded as a tensor on the GPU. Leveraging the equality constraint in Eq. (3), we analytically map each candidate foothold _uT ∈P_ to its corresponding DCM offset _b_ . Consequently, the cost function in Eq. (2) can be evaluated in parallel across the entire batch of candidate footholds using efficient vectorized tensor operations. The optimal foothold is then identified via a simple argmin reduction. To further accelerate the query, we constrain the search window to a 0 _._ 6 m _×_ 0 _._ 6 m region of interest centered on the nominal target [ _L_ nom _, W_ nom]<sup>_⊤_</sup> , as indicated by the light-blue region in Fig. 4. 

While this formulation relies on simplified dynamics (approximating _a ≈_ 1), it provides a computationally lightweight yet effective heuristic sufficient to guide the RL policy. Moreover, this _optimization-to-search_ paradigm offers a generalizable strategy for tightly coupling model-based planners with massive parallel RL environments without sacrificing training speed. 

## _B. Three-Stage Reinforcement Learning Framework_ 

_1) Observation Space:_ The policy’s state space is partitioned into proprioceptive observations (available during both training and deployment) and privileged observations (restricted to the training phase). The proprioceptive observations primarily comprise the user command vector **_c_** _t_ = [ _vx_<sup>_d, v_</sup> _y_<sup>_d, w_</sup> yaw<sup>_d_]</sup><sup>_⊤_, base angular velocity, projected gravity</sup> vector, joint positions, joint velocities, and the previous action history. To encode timing, we include gait clock signals _{_ sin(2 _πft_ ) _,_ cos(2 _πft_ ) _}_ , where _f_ denotes the stepping frequency. Crucially, the robot also perceives the terrain via elevation map centered on the robot. 

The privileged observations augment this set with groundtruth states and explicit model-based guidance. These include the base linear velocity, base height, external contact forces, joint accelerations, and joint torques. Importantly, to guide the learning process, we incorporate the optimal foothold computed by the parallel planner described in Sec. III-A. 

_2) Reward Function and Network Architecture:_ Since our primary contribution lies in the multi-stage framework, we adopt the actor-critic network architecture and the baseline reward formulation from [23]. However, to drive stagespecific behaviors, we adjust specific reward scalars across the three training stages, as detailed in Table I. 

Crucially, to enforce the guidance provided by the parallel planner, we introduce a specific foothold-tracking reward not present in [23]: _r_ foot = exp� _−_ 10 _∥_ **p** _f −_ **p**<sup>_d_</sup> _f_<sup>_∥_</sup> � _,_ where **p** _f ∈_ R<sup>3</sup> denotes the current swing-foot position and **p**<sup>_d_</sup> _f_<sup>_∈_R3</sup> represents the desired instantaneous position for the next time step. The desired trajectory **p**<sup>_d_</sup> _f_<sup>is generated via interpolation</sup> (e.g., B´ezier curves) defined by three keyframes: the liftoff position, the swing apex, and the target landing position [ _u_<sup>_⊤_</sup> _T_<sup>_, hz_]</sup><sup>_⊤_.Here,</sup><sup>_uT_istheoptimalplanarfootholdderived</sup> in Sec. III-A, and _hz_ is the corresponding terrain height retrieved directly from the elevation map. To prevent tripping, the swing apex is configured to ensure sufficient clearance above the maximum height difference between the lift-off and landing points. 

_3) Pre-training Stage:_ In the Pre-training Stage, we prioritize traversal stability over precise velocity tracking. Accordingly, we assign a dominant weight to the footholdtracking reward defined above. This constraint compels the policy to target safe contact regions—specifically the centers of stair treads—rather than risky edge placements, thereby maximizing the probability of successful traversal. Through this process, the policy effectively encodes the geometric intuition of the model-based planner. However, the emphasis on foothold accuracy leads to increased speed-tracking error. 

_4) Post-training Stage:_ To recover velocity-tracking precision and increase climbing speed, the reward weights were adjusted by increasing the weight of the speed-tracking term and reducing the foothold-tracking weight. 

We partition the command space into two distinct regimes: a high-velocity band ([0 _._ 8 _,_ 1 _._ 6] m/s) and a low-velocity band ([ _−_ 0 _._ 3 _,_ 0 _._ 8] m/s). Initialized from the pre-trained policy, two separate expert model are trained to master each specific regime. This divide-and-conquer strategy is essential; empirical results indicate that training a single policy directly over the full union of ranges ([ _−_ 0 _._ 3 _,_ 1 _._ 6] m/s) leads to mode collapse towards moderate velocities, significantly degrading tracking accuracy at the operational extremes (i.e., very slow or very fast motion). 

_5) LoRA Fine-tuning Stage:_ Because joint-action distributions differ between high- and low-speed locomotion, directly switching between discrete expert policies induces control discontinuities and physical instability during deployment. To resolve this, we integrate the parameters of both the high-speed and low-speed experts into a unified 

network (see Fig. 2). We then fine-tune the model using LoRA to smooth the transition boundaries and ensure robust performance across the full command spectrum. 

Within the unified network, we employ a rule-based switcher driven by the user command: the high-speed expert is activated to generate joint actions when the commanded forward velocity _vx_<sup>_d>_0</sup><sup>_._8 m/s,whilethelow-speedexpert</sup> governs the regime below this threshold. 

TABLE I 

THE REWARD WEIGHTS FOR THE THREE STAGES 

|Reward Term|Stage 1 Weights|Stage 2 Weights|Stage 3 Weights|
|---|---|---|---|
|Lin. velocity track|1.0|1.35|1.1|
|Base height<br>(w.r.t. feet)|0.4|0.3|0.4|
|Action smoothness|_−_2_._5e-03|_−_2e-03|_−_2e-03|
|Joint accel. L2|_−_5e-07|_−_4e-07|_−_4e-07|
|Joint torque L2|_−_4e-07|_−_3e-07|_−_3e-07|
|Torque rate|_−_1_._5e-07|_−_2e-08|_−_2e-08|
|Joint power|_−_2_._5e-07|_−_2e-07|_−_2e-07|
|Lin. accel. L2|_−_2e-03|_−_1_._5e-03|_−_1_._5e-03|
|Proj. gravity L2|_−_0_._15|_−_0_._1|_−_0_._1|
|Feet stumble|_−_1_._5|_−_1_._5|_−_2|
|Foothold|0_._6|0_._5|0_._4|


## _C. Elevation Maps Reconstruction_ 

The locomotion policy relies on egocentric local elevation maps (visualized as blue markers in Fig. 4) for terrain awareness. During simulation training, we extract groundtruth height samples directly from the IsaacLab interface. 

For physical deployment, we implement the perception pipeline proposed in [23] using an Intel RealSense D435i depth camera. This module processes raw depth frames in real-time to reconstruct a local terrain grid covering a 1 _._ 8 m _×_ 1 _._ 2 m area centered on the robot, with a spatial resolution of 5 cm. The resulting terrain scandots serves as the primary exteroceptive input for the onboard policy. 

## IV. EXPERIMENTS 

## _A. Robot Platform_ 

We conduct all experiments using the full-scale humanoid robot LimX Oli [24] (Fig. 5). The robot weighs 55 kg and stands 1.65 m tall, featuring 31 actuated degrees of freedom (DoF): 6 per leg, 7 per arm, 3 in the waist, and 2 in the head. In this study, all 31 joints are actively controlled. For onboard computing, the system integrates an NVIDIA Jetson Orin NX and a Rockchip RK3588-based single-board computer to handle real-time perception and policy inference. 

## _B. Traning and Deployment_ 

Following [23], we utilize IsaacLab to construct a diverse training curriculum featuring flat ground, rough terrain, and pyramid-shaped stairs (both ascent and descent). To facilitate agile maneuvers, we constrain the gait frequency to [1 _._ 0 _,_ 1 _._ 5] Hz. We simulate 4096 environments in parallel, randomizing the robot’s base pose upon each reset and 


resampling command velocities every 10 seconds. While the forward velocity range varies across the three training stages (as detailed in Sec. III-B.4), the lateral velocity and yaw rate are fixed at _vy_<sup>_d∈_[</sup><sup>_−_0</sup><sup>_._3</sup><sup>_,_0</sup><sup>_._3] m/s and</sup><sup>_w_</sup> yaw<sup>_d∈_[</sup><sup>_−_1</sup><sup>_._0</sup><sup>_,_1</sup><sup>_._0] rad/s,</sup> respectively. 

To bridge the sim-to-real gap, we apply domain randomization. Randomized parameters include the mass and inertia of links (base, waist, legs), contact friction, restitution coefficients, and joint PD gains. Additionally, we inject random external force and impulse perturbations. For the final LoRA fine-tuning stage we configure the LoRA hyperparameters as _α_ = 16 and _γ_ = 8. 

For real-world deployment, we employ a distributed computing architecture. The Intel RealSense D435i captures depth frames, which are processed by the perception pipeline on the NVIDIA Jetson Orin NX to generate local elevation maps. These maps are transmitted to the Rockchip RK3588based computer, which executes the final unified policy. This decoupling of perception and control workloads ensures efficient onboard processing and maintains the strict control loop timing required for stable agile locomotion. 

## _C. Foothold Tracking and Computational Efficiency_ 

_1) Foothold Tracking:_ In our framework, planned footholds serve as supervisory signals within the reward function, guiding the policy toward safe contact regions. Fig. 6 illustrates the optimal footholds (red point in the figure) generated via Eq. 2 during ascent; notably, the planner concentrates targets near the centers of the stair treads. By minimizing the tracking error against these targets, the robot implicitly learns to identify and exploit safe, planar contact surfaces. 

To evaluate this guidance, both the pre-trained and the final unified policies were deployed in IsaacLab and data were collected at commanded forward velocities of _{_ 0 _._ 4 _,_ 0 _._ 6 _,_ 0 _._ 8 _,_ 1 _._ 0 _}_ m/s. Performance was quantified by the mean planar Euclidean distance between executed and planned footholds. As illustrated in Fig. 6, simulation screenshots show that the swing foot generally lands near the desired foothold; nevertheless, the foothold-tracking error of the final unified policy is larger than that of the pre-trained policy. By contrast, the velocity-tracking analysis in Fig. 9 indicates that the final unified policy attains lower velocity error. This pattern is explained by the training design: during pre-training a larger weight is placed on foothold accuracy to prioritize safety, and only after a safe baseline has been 


Fig. 6. Foothold screenshots and Foothold-tracking error. For each commanded speed, the error was computed by averaging the absolute foothold-position errors recorded over a time window. 

learned is post-training used to explore more agile behaviors. The results therefore reflect the intended trade-off between safety and agility embodied by the proposed multi-stage framework. 

_2) Computational Efficiency:_ The complete planning pipeline—including elevation map processing and the parallel discrete search—incurs a latency of approximately 4 ms per step for a batch of 4096 environments on an NVIDIA RTX 4090. This represents an approximate 25 _×_ speedup compared to recent parallel MPC implementations using CusADi [25] under similar hardware conditions, highlighting the scalability of our approach for large-scale RL. 

## _D. Full-Range Velocity-Tracking Experiments_ 

To assess policy robustness beyond the training simulator, we conduct validation in MuJoCo on a staircase with a step height of 15 cm. Fig. 7 presents both a simulation snapshot and a time-series plot of the forward velocity response during a stair descent maneuver. 

Experimental results demonstrate that the unified policy effectively tracks velocity commands across the entire operational range. Notably, the robot maintains stability and tracking accuracy from a stationary stance (0 m/s) up to the maximum commanded velocity of 1 _._ 6 m/s, validating the effectiveness of the multi-stage training framework. 

## _E. Training Framework Evaluation_ 

We evaluated the following methods in terms of terrain traversal success ratio and velocity-tracking mean absolute error (MAE): 

- **Baseline [23]:** A standard end-to-end RL policy trained without model-based foothold guidance, which has twice the parameters of a velocity expert policy. 

- **Pre-trained (Ablation):** An intermediate variant (Stage 1 only) incorporates DCM-based foothold guidance and uses twice the parameters of a velocity expert, but lacks the velocity-specific split and LoRA integration. 

- **AMP [18]:** A policy trained using Adversarial Motion Priors (AMP), where exploration is guided by retargeted 


Fig. 7. MuJoCo simulation snapshot and velocity-tracking performance during stair descent. The plot shows commanded and measured forward velocities over time. 

   - human reference motions rather than terrain-aware geometric planning. 

- **FastStair (ours):** The complete proposed framework (see Fig. 2). 

_1) Terrain Traversal Success Ratio:_ The traversal success ratio was evaluated on a staircase with 25 cm step height at commanded forward speeds of 0.5, 1.0, 1.5, and 2.0 m/s. In IsaacSim we initialized 500 robots around the center of a pyramidal staircase with randomized headings and commanded them to traverse in all directions. The success ratio is defined as the fraction of environments in which the robot reached the far edge of the terrain within an episode without falling. Results are presented in Fig. 8. 

As illustrated, FastStair achieves the highest success rate across all tested velocities. The Pre-trained policy also significantly outperforms the baselines, a result we attribute to the parallel foothold planning incorporated during pre-training. This explicitly imparts geometric guidance, enabling the robot to identify optimal contact regions on the stair treads. 

In contrast, while the AMP method performs well at lower velocities ( _≤_ 1 _._ 0 m/s), its performance degrades sharply at higher speeds, eventually underperforming even the unguided Baseline. In simulation, we observed that the AMP policy exhibited a tendency to stall at the base of the stairs when commanded above 1 _._ 0 m/s. We hypothesize this stems from two factors: the lack of high-speed climbing examples in the reference dataset (distributional shift) and a conservative reward structure that penalizes the deviations required for aggressive maneuvers. 

Although all policies were trained with a maximum commanded velocity of 1 _._ 6 m/s, we extended the evaluation to 2 _._ 0 m/s to assess robustness. Notably, FastStair maintains a success rate exceeding 70% even in this out-of-distribution regime, demonstrating superior generalization of the learned agile locomotion skills. 

_2) Velocity-Tracking Evaluation:_ We evaluate the velocity-tracking fidelity of the four methods on a staircase with a 25 cm step height. forward velocity commands are 


Fig. 8. Success-rate comparison for traversing a staircase with 25 cm step height at various commanded speeds. 


Fig. 9. Mean absolute error (MAE) of velocity tracking for four methods on a staircase with 25 cm step height. 

sampled uniformly from [ _−_ 0 _._ 3 _,_ 1 _._ 6] m/s at 3 s intervals. For each trial, we compute the Mean Absolute Error (MAE) between the commanded and actual velocities. The resulting error distributions are presented in Fig. 9. 

As illustrated, FastStair achieves the lowest MAE (approximately 0 _._ 5 m/s), validating the effectiveness of the full training pipeline. Notably, the Pre-trained policy exhibits a slightly higher MAE than the Baseline. This result is consistent with our design intent: the heavy weighting of the foothold-tracking reward during pre-training biases the policy toward precise, safe foot placement (as evidenced in Fig. 6) at the expense of velocity-tracking performance. This safety-versus-agility trade-off explicitly justifies the necessity of the subsequent post-training stage to recover velocitytracking precision while retaining the learned foothold priors. 

Conversely, the AMP method yields the largest MAE. As noted in Sec. IV-E.1, the AMP policy frequently exhibits stagnation behavior at the stair base under high-velocity commands, leading to significant tracking deviations. Finally, we note that the maximum error values across all methods are inflated by velocity measurements recorded immediately prior to falls; therefore, maximum error is not a reliable indicator of tracking quality. 

## _F. Real-World Deployment_ 

We deploy the final policy on the full-scale humanoid robot “LimX Oli,” executing directly on the onboard RK3588-based computer at a control frequency of 100 Hz, without any additional task-level fine-tuning. We conduct a series of outdoor experiments to validate performance (see Fig. 1 and Fig. 10). Detailed video recordings are provided 


Fig. 10. Outdoor experiments of perception-enabled agile stair climbing, including high-speed ascent and descent and turning maneuvers on stairs. 

in the supplementary material<sup>1</sup> . 

We perform comprehensive stair-climbing tests covering the full velocity range (0 to 1.5 m/s) on an outdoor staircase with a 15 cm step height (Fig. 10). The robot successfully executes both ascent and descent across the full commanded velocity range, achieving ascent velocities up to 1.5 m/s. To accommodate such high-speed motion, the robot exhibits an emergent step-skipping behavior, clearing two steps in a single stride to maximize forward progress. Notably, the robot successfully negotiated 33 stairs (17 cm/step) at the Canton Tower within 12 seconds, reaching a peak velocity of 1.65 m/s during the final steps of the ascent. 

Further validation includes the continuous negotiation of steeper staircases (20 cm step height, Fig. 1) and dynamic turning maneuvers between flight segments. All tasks were completed successfully, demonstrating that FastStair enables stable, perception-aware agile locomotion in challenging real-world environments. 

## V. CONCLUSION 

In this paper, we presented FastStair, a multi-stage learning framework that reconciles model-based stability with learned agility for high-speed stair climbing. By reformulating DCMbased foothold optimization into a GPU-parallel discrete search, we provided real-time guidance within the RL loop with negligible computational overhead. To mitigate plannerinduced conservatism and improve velocity-tracking performance, the base policy was fine-tuned into separate lowand high-speed experts to accommodate differing action distributions. To eliminate instabilities associated with hard switching, the experts were merged into a single network and consolidated via LoRA fine-tuning, yielding a unified policy that operates robustly across the full commandedspeed range. Experimental results on the Oli robot demonstrate robust performance, achieving agile stair ascent at speeds up to 1.65 m/s. The successful navigation of a 33-step spiral staircase in 12 seconds underscores the efficiency and high-speed capabilities of FastStair in challenging real-world environments. 

For future work, we aim to extend the parallel planning paradigm to a broader spectrum of challenging terrains. Furthermore, we plan to investigate generalized methodologies for tightly coupling model-based geometric priors with large-scale RL, ultimately enabling reliable deployment in complex, unstructured field environments. 

1https://youtu.be/SoLBK7VEGDo 

## REFERENCES 

- [1] Z. Li, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control,” _The International Journal of Robotics Research_ , vol. 44, no. 5, pp. 840–888, 2025. 

- [2] Q. Liao, T. E. Truong, X. Huang, G. Tevet, K. Sreenath, and C. K. Liu, “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

- [3] T. Peng, L. Bao, and C. Zhou, “Gait-conditioned reinforcement learning with multi-phase curriculum for humanoid locomotion,” _arXiv preprint arXiv:2505.20619_ , 2025. 

- [4] X. Gu, Y.-J. Wang, and J. Chen, “Humanoid-gym: Reinforcement learning for humanoid robot with zero-shot sim2real transfer,” _arXiv preprint arXiv:2404.05695_ , 2024. 

- [5] Z. Wang, W. Wei, R. Yu, J. Wu, and Q. Zhu, “Toward understanding key estimation in learning robust humanoid locomotion,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 11 232–11 239. 

- [6] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang, “Learning humanoid locomotion with perceptive internal model,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 9997–10 003. 

- [7] W. Sun, B. Cao, L. Chen, Y. Su, Y. Liu, Z. Xie, and H. Liu, “Learning perceptive humanoid locomotion over challenging terrain,” _arXiv preprint arXiv:2503.00692_ , 2025. 

- [8] M. S. Gadde, P. Dugar, A. Malik, and A. Fern, “No more blind spots: Learning vision-based omnidirectional bipedal locomotion for challenging terrain,” in _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2025, pp. 601–608. 

- [9] J. Ren, T. Huang, H. Wang, Z. Wang, Q. Ben, J. Long, Y. Yang, J. Pang, and P. Luo, “Vb-com: Learning vision-blind composite humanoid locomotion against deficient perception,” _arXiv preprint arXiv:2502.14814_ , 2025. 

- [10] B. Acosta and M. Posa, “Bipedal walking on constrained footholds with mpc footstep control,” in _2023 IEEE-RAS 22nd International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2023, pp. 1– 8. 

- [11] L. Penco, B. Park, S. Fasano, N. Poddar, S. McCrory, N. Kitchel, T. Bialek, D. Anderson, D. Calvert, and R. Griffin, “Anticipatory and adaptive footstep streaming for teleoperated bipedal robots,” in _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2025, pp. 1–8. 

- [12] Y. Shi, S. Li, Y. Wu, J. Liu, X. Leng, X. Zang, and S. Piao, “Bipedal robust walking on uneven footholds: Piecewise slope lipm with discrete model predictive control,” _arXiv preprint arXiv:2504.02255_ , 2025. 

- [13] B. Acosta and M. Posa, “Perceptive mixed-integer footstep control for underactuated bipedal walking on rough terrain,” _arXiv preprint arXiv:2501.19391_ , 2025. 

- [14] M. Khadiv, A. Herzog, S. A. A. Moosavian, and L. Righetti, “Walking control based on step timing adaptation,” _IEEE Transactions on Robotics_ , vol. 36, no. 3, pp. 629–643, 2020. 

- [15] A. Shamsah, Z. Gu, J. Warnke, S. Hutchinson, and Y. Zhao, “Integrated task and motion planning for safe legged navigation in partially observable environments,” _IEEE Transactions on Robotics_ , vol. 39, no. 6, pp. 4913–4934, 2023. 

- [16] H. Duan, B. Pandit, M. S. Gadde, B. Van Marum, J. Dao, C. Kim, and A. Fern, “Learning vision-based bipedal locomotion for challenging terrain,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 56–62. 

- [17] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang, “Beamdojo: Learning agile humanoid locomotion on sparse footholds,” _arXiv preprint arXiv:2502.10363_ , 2025. 

- [18] D. Wang, X. Wang, X. Liu, J. Shi, Y. Zhao, C. Bai, and X. Li, “More: Mixture of residual experts for humanoid lifelike gaits learning on complex terrains,” _arXiv preprint arXiv:2506.08840_ , 2025. 

- [19] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen, _et al._ , “Lora: Low-rank adaptation of large language models.” _ICLR_ , vol. 1, no. 2, p. 3, 2022. 

- [20] O. Dosunmu-Ogunbi, A. Shrivastava, G. Gibson, and J. W. Grizzle, “Stair climbing using the angular momentum linear inverted pendulum model and model predictive control,” in _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2023, pp. 8558–8565. 

- [21] S. H. Jeon, S. Hong, H. J. Lee, C. Khazoom, and S. Kim, “Cusadi: A gpu parallelization framework for symbolic expressions and optimal control,” _IEEE Robotics and Automation Letters_ , 2024. 

- [22] S. Caron, A. Escande, L. Lanari, and B. Mallein, “Capturabilitybased pattern generation for walking with variable height,” _IEEE Transactions on Robotics_ , vol. 36, no. 2, pp. 517–536, 2019. 

- [23] H. Song, H. Zhu, T. Yu, Y. Liu, M. Yuan, W. Zhou, H. Chen, and H. Li, “Gait-adaptive perceptive humanoid locomotion with real-time under-base terrain reconstruction,” _arXiv preprint arXiv:2512.07464_ , 2025. [Online]. Available: https://arxiv.org/abs/2512.07464 

- [24] “Limx Oli,” https://www.limxdynamics.com/en/oli, 2025, Accessed: July 30, 2025. 

- [25] J. Kamohara, F. Wu, C. Wamorkar, S. Hutchinson, and Y. Zhao, “Rlaugmented adaptive model predictive control for bipedal locomotion over challenging terrain,” _arXiv preprint arXiv:2509.18466_ , 2025. 

