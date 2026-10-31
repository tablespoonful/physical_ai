---
title: "Mind Your Steps: A General Learning Framework for Accurate Humanoid Foothold Tracking"
date: "2026-06-06"
authors: "Alessandro Montenegro; Shihao Li; Puze Liu; Alberto Maria Metelli; Jan Peters"
url: https://arxiv.org/abs/2606.08253
pdf: https://arxiv.org/pdf/2606.08253
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.08253)** / [論文ページ](https://arxiv.org/abs/2606.08253)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Mind Your Steps: A General Learning Framework for Accurate Humanoid Foothold Tracking 

Alessandro Montenegro<sup>1</sup> , Shihao Li<sup>2</sup> , Puze Liu<sup>2, 3, :</sup> , Alberto Maria Metelli<sup>1</sup> , and Jan Peters<sup>3–6</sup> 1Politecnico di Milano 2Tongji University 3Technische Universit¨at Darmstadt 4hessian.AI 

> 5German Research Center for Artificial Intelligence (DFKI) 6Robotics Institute Germany (RIG) 

Project Website: **https://montenegroalessandro.github.io/mind-your-steps/** 

**_Abstract_ —Enabling humanoid robots to operate in complex, dynamic environments remains a critical challenge, fundamentally limited by the ability to navigate robustly, safely, and accurately. While reinforcement learning with velocity-commanded policies has achieved remarkable robustness in humanoid locomotion, this approach lacks explicit control of the foothold placement, leading to unsafe behavior, such as stepping onto human feet, or imprecise navigation, hindering the following manipulation task. Conversely, explicit foothold-tracking policies offer a promising alternative by directly being commanded with target foot poses. However, existing approaches are often limited by unrealistic state assumptions, compromising real-world deployment, or they are part of staged pipelines, making them tied to specific downstream tasks. In this work, we introduce a novel, lightweight framework for training general-purpose 3D foothold-tracking policies. By dynamically providing footstep support through a goal sampler, this method enables the learned policy to be agnostic to specific terrains. Our new target representation effectively mitigates challenges arising in the real world, such as noisy and inaccurate pose estimation and foot contact estimation. Designed for direct real-world transfer, our policy acts as a standalone low-level controller that can be seamlessly paired with various high-level foothold generators. We demonstrate the effectiveness of our framework through extensive experiments in simulation and in the real world. By coupling our policy with different upstream planners, we achieve natural and accurate locomotion in challenging settings, paving the way for loco-manipulation tasks in complex environments.** 

## I. INTRODUCTION 

Recent research on humanoid robotics has demonstrated remarkable progress, enabling humanoids to perform agile and highly dynamic behaviors such as backflips and flying kicks. Despite these achievements, enabling humanoids to operate autonomously in real-world environments remains a critical challenge. A fundamental prerequisite for real-world deployment is the ability to navigate safely, accurately, and reliably in everyday settings [19, 34, 3, 11]. In realistic environments, humanoid robots must contend with numerous challenges, including obstacle avoidance, interaction with humans, traversal of slopes and stairs, and locomotion over uneven or irregular terrain [50, 14, 42]. In such conditions, stable locomotion critically depends on precise and informed foot placement, as feasible footholds are often sparse and constrained. Consequently, endowing humanoids with con- 

> :Correspondence to: Puze Liu (puze_liu@tongji.edu.cn). 

trollers capable of constraining foot placements to valid and safe contact regions explicitly is a critical problem. 

Given its fundamental importance, legged locomotion has become one of the most studied fields in robotics. Extensive investigation, spanning model-based [34, 43, 16], datadriven [22, 20, 27, 23, 29, 51, 5, 12, 24, 3], and hybrid methodologies [48, 8, 45, 31, 17, 14], has yielded approaches with remarkable robustness in both simulation and real-world deployment. However, the predominant paradigm remains the integration of vision pipelines with velocity-commanded policies [42, 14, 11, 4]. In this setting, the control policy typically relies on height map observations and auxiliary reward terms to implicitly select valid footholds while steering the robot away from unsteppable areas. However, the inherent mismatch between continuous velocity commands and discrete foot placement results in degraded tracking accuracy and reduced efficiency in reaching the target. 

Since the aforementioned methodologies do not allow for direct control over the robot’s foot placement, explicit footholdcommanded policies have recently emerged as a promising alternative paradigm [32, 44, 7, 14, 41]. These approaches are designed to enhance accuracy on foot placement targets and enable more flexible gait generation and motion capabilities. However, existing implementations remain severely limited in scope and practicality, far from general-purpose utility. Most have been studied solely in simulation [32, 44], exist only in preliminary forms restricted to simple forward walking on flat terrain [7], or are embedded as low-level components within specific, monolithic pipelines [32, 14]. Consequently, they often fail to support direct real-world usage and remain closely coupled to specific downstream tasks. 

**Original Contribution.** Motivated by achieving stable and accurate locomotion via foothold-conditioned policies, in this work we propose a novel, lightweight, and model-free framework for training general-purpose 3D foothold-tracking policies. Such foothold-trackers are agnostic to the highlevel planner and ready for immediate deployment, enabling seamless integration with diverse downstream tasks. Our specific contributions are as follows: 

- ‚ We propose a framework designed to train policies relying solely on proprioception, gait phase, and stance-relative foothold targets. By expressing commands in the stancefoot frame, the goal remains constant throughout the 


Fig. 1: **Training and Deployment Architecture.** Overview of the training and deployment architecture. _Policy._ The policy _π_ **_θ_** receives proprioception **_o_** proprio _,t_ , the previous action **_a_** _t_ ´1, the foothold goal **_g_** _t_ , and the gait phase **_ϕ_** _t_ . It outputs joint position targets for an underlying PD controller. _Goal Generator._ This modular component supplies foothold targets to the policy. During _training_ , a procedural Goal Sampler generates synthetic targets to enforce tracking accuracy. During _deployment_ (simulation or real-world), this is replaced by task-specific planners, such as a vision-based estimator extracting visual targets from the ground or a teleoperation interface defining step direction, length, and yaw orientation. 

swing phase, removing the need for precise base state estimation [32, 44]. To this end, we propose a novel Goal Sampler (GS) capable of generating feasible 3D foothold targets during training. Our GS does not tie with specific predefined terrains, enabling a general-purpose policy for downstream tasks. Coupled with specific reward terms balancing tracking accuracy with natural locomotion, this enables the agent to achieve accurate foot placement capabilities, thus generalizing locomotion in settings where real-world-like hurdles are present. 

- ‚ Leveraging the independence of our foothold-tracking policy, we show its modularity by pairing it with various high-level planners in simulation. We validate performance on tasks such as goal reaching, cluttered environment navigation, and narrow paths and staircases traversal. In most scenarios, we compare against standard velocitycommanded policy, showing that our approach leads to more efficient and robust solutions. 

- ‚ We deploy the foothold-tracking policy on the Booster T1 humanoid hardware. By integrating a simple vision-based foothold generator, we show zero-shot sim-to-real transfer, tracking the predefined foothold target successfully. This validates the framework’s potential as a foundational block for complex loco-manipulation systems. 

Figure 1 shows the proposed training and deployment pipeline. 

## II. RELATED WORK 

**Locomotion Over Sparse Footholds.** Locomotion over sparse footholds, where the main complexity arises from the combinatorial nature of foothold selection [6], has been extensively studied as a perceptive locomotion problem using model-based methods [34, 43, 16]. Specifically, the literature has focused on developing hierarchical controllers relying on complex pipelines integrating perception, planning, and 

control [10, 15, 25, 26, 9, 28]. While years of research led to high-performing, lightweight, and interpretable approaches [34], these methods often suffer from the common pitfalls of modelbased control. Indeed, they are highly sensitive to model discrepancies and violations of modeling assumptions. Such problems are especially exacerbated in real world locomotion tasks due to the difficulty of terrain modeling, potentially resulting in unsafe or unreliable behavior during deployment. 

To overcome the limitations of model-based methods, research has shifted toward model-free Reinforcement Learning [RL, 40], which learns control policies directly via interaction without relying on explicit priors. Leveraging domain randomization, these approaches have demonstrated remarkable robustness and generalization, enabling effective deployment on real-world hardware [22, 20, 27, 23, 29, 51, 5, 12, 24, 3]. Typically, they learn velocity-tracking policies [1, 46, 5, 47, 50] paired with high-level vision components [11, 4] whose integration is required in sparse foothold scenarios to identify valid places to step on. A major issue in end-to-end modelfree-based methodologies arises from the sparsity of valid footholds which results in sparse reward signals and frequent early episode terminations. To mitigate these limitations, the literature employed curriculum learning [30] and proposed specialized reward structures and architectures, such as a reward account for foot geometry [42] or an attention-based terrain map [11] to achieve robust terrain-aware locomotion. 

Another approach to addressing the limitations of both modelbased and end-to-end model-free methodologies relies on hybrid architectures that combine the two [48, 8, 45, 31, 17, 14]. The objective is to train agents starting from physics priors [21], aiming to retain the best of both worlds: high interpretability, robustness, and generalization capabilities. Model-based and model-free techniques can be merged in various ways. For 

instance, RL has been employed to generate trajectories that are subsequently tracked by model-based controllers [48, 8, 45], or conversely, to train policies capable of tracking modelbased planners [17, 14]. While hybrid approaches preserve the benefits of both paradigms, they also inherit their respective pitfalls. Specifically, they rely on models that may fail when discrepancies with reality are significant. Furthermore, they can be computationally demanding and often require substantial implementation effort, particularly when extending established open-source robot locomotion frameworks [e.g., 2]. 

**Learning Foothold-Tracking Controllers.** Learning foothold-tracking controllers has gained significant attention in recent years. In most cases, such controllers function as part of two-stage architectures, serving as a bridge between high-level vision pipelines and underlying PD controllers to achieve accurate locomotion on sparse footholds. However, these approaches often rely on unrealistic modeling assumptions, making them unsuitable for real-world deployment. For instance, Peng et al. [32] proposed _DeepLoco_ , a two-stage architecture for terrainaware humanoid locomotion employed solely in simulation. Besides requiring proprioceptive information and a gait phase indicator [37] as input, the tracker additionally requires observing binary ground contact flags which are difficult to estimate accurately in the real world. Furthermore, the foothold goals consist of target positions for the next two steps [49] and a target root heading, all expressed in the root frame, as also done in [39]. This implies that real-world deployment would require precise state estimation/localization. Moreover, during training, foothold targets are extracted from motion capture clips to enforce stylistic mimicry. Despite these limitations, [32] is considered a seminal work, inspiring numerous follow-up studies [41, 17, 11]. Another key study focusing on simulationbased foothold tracking is [44]. The authors demonstrate that employing a carefully designed curriculum and a lightweight foothold sampler facilitates learning a tracker capable of traversing stepping stones and generalizing to continuous terrains. As with [32], the reliance on binary contact states and body-frame targets renders such controllers difficult to deploy in the real world, likely necessitating specific highlevel wrappers. Moving toward real-world applicability, Duan et al. [7] extended the work of Xie et al. [44]. During training, they synchronize touchdown events with the gait clock and focus on forward motion on flat terrain. While simple, this approach paves the way for more sophisticated approaches capable of navigating real-world terrains for general-purpose tasks. More recently, Huang et al. [14] proposed an architecture specifically designed for traversing narrow paths in the real world, leveraging a Linear Inverted Pendulum (LIP) model [19]. Then, they integrate a lightweight LiDAR-based perception module to refine the LIP-proposed footholds [38, 18]. 

While foothold trackers have proven to be valuable for achieving robust and accurate locomotion by enabling full control over foot placement, to the best of our knowledge, they have been employed primarily as subordinate components within specific high-level pipelines. Furthermore, they often lack generality regarding downstream tasks or upstream 

gait generators and frequently face challenges in real-world deployment due to the reliance on specific, hard-to-estimate information in their observation space. 

## III. PROBLEM FORMULATION 

In RL, the environment is modeled as a Markov Decision Process [MDP, 35]. An MDP is represented by _M_ :“ p _S, A, p, r, ρ_ 0 _, γ, T_ q, where _S_ Ď R<sup>_dS_</sup> and _A_ Ď R<sup>_dA_</sup> are the measurable state and action spaces; _p_ : _S_ ˆ _A_ ÝÑ ∆p _S_ q<sup>1</sup> is the transition model, where _p_ p **_s_**<sup>1</sup> | **_s_** _,_ **_a_** q is the probability density of landing in state **_s_**<sup>1</sup> P _S_ by playing action **_a_** P _A_ in state **_s_** P _S_ ; _r_ : _S_ ˆ _A_ ÝÑ r´ _R_ max _, R_ maxs is the reward function, where _r_ p **_s_** _,_ **_a_** q is the reward the agent gets when playing action **_a_** in state **_s_** ; _ρ_ 0 P ∆p _S_ q is the initial-state distribution; _γ_ P r0 _,_ 1s is the discount factor. A trajectory _τ_ “ p **_s_** _τ,_ 1 _,_ **_a_** _τ,_ 1 _, . . . ,_ **_s_** _τ,T ,_ **_a_** _τ,T_ q of length _T_ P N Y t`8u is a sequence of _T_ state-action pairs. In the following, we refer to _T_ as the set of all trajectories. The _discounted return_ of a trajectory _τ_ P _T_ is _R_ p _τ_ q :“<sup>ř</sup><sup>_T_</sup> _t_ “1<sup>_γt_´1</sup><sup>_r_p</sup><sup>**_s_**</sup><sup>_τ,t,_</sup><sup>**_a_**</sup><sup>_τ,t_q.2</sup> 

Most of the times, especially in robotics, at the interaction instant _t_ the agent is not provided with the full state **_s_** _t_ , but just with a _partial observation_ of it. Specifically, it is provided with **_o_** _t_ P _O_ Ď R<sup>_dO_</sup> , which can be expressed as **_o_** _t_ “ _f_ p **_s_** _t_ q, where _f_ : _S_ Ñ _O_ . Furthermore, as commonly done in this setting [42, 14, 17, 11], we frame our problem as a goal-based RL one, meaning that we extend the _observation space_ to incorporate a goal set _G_ Ď R<sup>_dG_</sup> , part of the state space of the MDP. Thus, the goal **_g_** _t_ P _G_ influences the reward function _r_ . 

An RL agent interacts with the environment according to a _parametric stochastic policy π_ **_ζ_** : _O_ ˆ _G_ Ñ ∆p _A_ q, where **_ζ_** P _Z_ is the policy parameterization in the parameter space _Z_ Ď R<sup>_dZ_</sup> . The policy is employed to sample actions **_a_** _t_ „ _π_ **_ζ_** p¨ | **_o_** _t,_ **_g_** _t_ q to be played at _every interaction_ instant _t_ , being conditioned on the observation **_o_** _t_ P _O_ and the goal **_g_** _t_ P _G_ . The performance of a policy _π_ **_θ_** is assessed via the _expected return J_ : _Z_ Ñ R, which is defined as: _J_ p **_ζ_** q :“ E _τ_ „ _p_ **_ζ_** r _R_ p _τ_ qs, where _p_ **_ζ_** p _τ_ q is the density function of a trajectory _τ_ induced by _π_ **_ζ_** . The goal is to learn the optimal policy _π_ **_ζ_** ‹ , with **_ζ_**<sup>‹</sup> P arg max **_ζ_** P _Z J_ p **_ζ_** q. 

## IV. METHODOLOGY 

In this section, we detail the proposed framework. First, we define the foothold command formulation provided as input to the policy and describe the observation space, which is explicitly designed to facilitate real-world deployment. Next, we outline the characteristics of our training pipeline, detailing the employed agent structure and the goal sampler functioning. Finally, we introduce the reward function, focusing on the specific terms for foothold tracking and locomotion style. 

## _A. Goal and Observation Formulation_ 

At each time step _t_ , the policy observes _proprioceptive information_ **_o_** proprio :“ p **_θ_** base _,_ **_ω_** _,_ **_q_** _,_ **_q_** 9q (including base orientation **_θ_** base, base angular velocity **_ω_** , joint positions **_q_** and velocities **_q_** 9) along with a _goal command_ specifying the desired footholds 

> 1∆p _X_ q is the set of probability distributions over a measurable space _X_ . 

> 2We let _γ_ “ 1 only when _T_ ă `8. 

in terms of position and yaw orientation. We formulate the foothold target goal as a vector **_g_** _t_ , defined as: 


where<sup>_s_</sup> _l_<sup>**_p_**</sup><sup>_t, s_</sup> _r_<sup>**_p_**</sup><sup>_t_PR3denotethepositionoffsetsofthenext</sup> desired left and right footholds, expressed in the _current stance foot frame_ . Similarly,<sup>_s_</sup> _l_<sup>**_ψ_**</sup><sup>_t, s_</sup> _r_<sup>**_ψ_**</sup><sup>_t_representthedesired</sup> orientations (expressed as quaternions) in the _stance foot frame_ . As these foothold targets are expressed in the _stance foot frame_ , the targets are holding a constant value during each swing phase, significantly reducing target variability during movement compared to previous methods [32, 44, 39]. 

The agent also observes _gait phase_ information: **_ϕ_** _t_ :“ pcosp2 _πϕt_ q; sinp2 _πϕt_ qq, where _ϕt_ P r0 _,_ 1s. If _ϕt_ P r0 _,_ 0 _._ 5q, the left foot acts as the swing foot; otherwise, the right foot swings. As commonly done in this setting [32, 37, 44], we consider the phase variable to evolve like a clock, enforcing a constant locomotion cadence. Specifically, it evolves according to _ϕt_ `1 Ð _ϕt_ ` _δϕ_ mod 1, where _δϕ_ is the _fixed_ gait offset determining the rapidity of gait phase switches. 

**Design Choices.** Several aspects of this formulation differ from prior art. First, all targets in **_g_** _t_ are expressed in the _stancefoot frame_ . Consequently, the target remains constant until a phase switch occurs. Notice that the target corresponding to the current stance foot is effectively a zero offset (identity pose) for the whole phase duration. This contrasts with methods using the base frame [32, 44, 14, 39] or the specific foot frame [7]. This choice facilitates real-world deployment by removing the need for precise base state estimation (localization) to update targets in real-time, as the relative command remains constant throughout the swing phase. Second, we avoid providing binary ground contact flags [32, 44], which are difficult to estimate reliably on hardware. Finally, by explicitly commanding 3D positions and yaw orientations, we ensure general-purpose navigation capabilities on complex terrain, surpassing prior works that control only subsets of these dimensions [7, 14]. Indeed, by training agents to track full 3D foothold targets, the humanoid enables omnidirectional locomotion (forward, backward, and lateral) while simultaneously controlling swing foot height and orientation. This comprehensive set of control possibilities allows the agent to execute precise footstep plans and complex walking patterns. 

## _B. Training Architecture and Goal Sampling_ 

For training our policy, we employ asymmetric Proximal Policy Optimization (PPO) [36, 33], a common used modelfree RL algorithm in locomotion [3]. We build upon the open-source library _LocoMuJoCo_ [2], originally designed for velocity-commanded tasks, adapting its infrastructure to support our foothold-tracking framework. 

**Agent Structure.** As done in asymmetric actor-critic, the actor _π_ **_ζ_** , which is parameterized by a 512ˆ256ˆ128 network, receives proprioceptive observation as input, whereas the critic network shares the same network structure but takes privileged state as observation. The overall observation of the actor is 


Fig. 2: **Goal Sampling.** Representation of the sampling process during a left-swing phase ( _ϕt_ ă 0 _._ 5). The global vectors **_u_** ˆmove and **_u_** ˆfeet define the nominal locomotion heading and foot orientation, fixed for the entire episode. At each gait switch, the angles _α_ and _β_ are sampled from independent uniform distributions to perturb the nominal directions. The scalars _d_ and _z_ determine the planar distance and vertical offset, respectively, relative to the current stance foot. 

where the components are defined in the preceding section. In addition to the actor’s observation, the critic also observes the linear velocity of the robot base **_v_** base. Regarding the output action **_a_** _t_ „ _π_ **_θ_** p¨ | **_x_** _t_ q, we consider **_a_** _t_ to specify the target joint positions for a low-level PD controller, a common hierarchy in the literature [32, 14, 11]. In this work, we target the Booster T1 humanoid, though the formulation is robotagnostic. Figure 1 illustrates the complete architecture. 

**Goal Sampling.** During training, we employ a Goal Sampler (GS) responsible for generating feasible foothold targets and supports. In the following, we denote quantities in the world frame _w_ unless otherwise specified. We remark that the GS operates just in simulation, while the agent is then provided with the observation described above. At the _beginning of each episode_ ( _t_ “ 1), the GS defines the global locomotion heading. It samples a desired movement direction _θ_ move P r´ _π, π_ q and a nominal feet orientation _θ_ feet P r´ _π, π_ q. These global directions _remain constant_ throughout the episode to enforce motion consistency. The gait phase _ϕ_ 1, defining the start of the motion with either the left or the right foot, is initialized conditioned to _θ_ move or sampled at random whenever possible. _Target sampling_ is triggered at every _gait phase switch_ (i.e., whenever the swing and stance roles swap). The GS computes the target position _w_ **_p_** tgt and yaw orientation<sup>_w_</sup> _ψ_ tgt for the swing foot as follows: 

- 1) The GS samples a deviation angle _α_ „ _U_ p _α_ min _, α_ maxq<sup>3</sup> and a step length _d_ „ _U_ p _d_ min _, d_ maxq. The planar displacement is computed by perturbing the nominal movement direction _θ_ move: 


This ensures that while the robot follows a general direction, it must handle lateral and angular variations. 

> 3 _U_ p _a, b_ q denotes a uniform distribution continuous in r _a, b_ s. 

- 2) Similarly, the target foot yaw is generated by perturbing the global feet orientation with an offset _β_ „ _U_ p _β_ min _, β_ maxq, yielding<sup>_w_</sup> _ψ_ tgt “ _θ_ feet ` _β_ . 

- 3) The vertical component is sampled as an offset _z_ „ _U_ p _z_ min _, z_ maxq relative to the current stance foot height. The final world-frame target is: 


Crucially, to ensure physical feasibility in simulation, we implement a _terrain adaptation_ mechanism: the environment consists of moving pillars that automatically adjust their height to match the sampled _z_ -coordinate of the target, guaranteeing a valid contact surface. 

Finally, the sampled target p<sup>_w_</sup> **_p_** tgt _,_<sup>_w_</sup> _ψ_ tgtq is transformed into current stance foot frame and clipped to feasible region to avoid leg crossing pl<sup>_s_</sup><sup>**_p_**</sup><sup>_t,_</sup> l<sup>_s_</sup><sup>**_ψ_**</sup><sup>_t_q,wherelPt</sup><sup>_l, r_udepending</sup> on the current swing foot index, to build the goal vector **_g_** _t_ as previously described. We highlight that in **_g_** _t_ the part related to the stance foot is taken as the offsets in the stance foot frame of the last observed position and orientation of the stance foot itself at the _gait switch instant_ . To enable _standing capabilities_ , with probability _p_ hold, the GS enters a “hold-still” mode. In this case, the target position is set to maintain a nominal stance width relative to the stance foot, the orientation is aligned with the current stance foot (identity relative quaternion), and the gait phase is frozen providing the agent with **_ϕ_** _t_ “ p0; 0q for every _t_ in which the GS remains in the still mode. Figure 2 shows the sampling strategy. 

**Additional Training Details.** As previously mentioned, we utilize Asymmetric PPO [36, 33], a standard model-free RL algorithm in robot learning [3]. Specifically, we adopt an asymmetric actor-critic architecture, where the critic has access to privileged simulation states unavailable to the actor. We define an episode as _terminated_ (absorbing state) if the robot’s base height falls below a critical threshold. Furthermore, we employ extensive _domain randomization_ , including perturbations to link geometries, masses, and contact friction, as well as observation noise and external force disturbances (simulating kicks). Further details are provided in the supplementary material. Finally, we implement a _two-stage training_ curriculum. Initially, we train the agent on flat terrain ( _z_ min “ _z_ max “ 0) to learn a robust planar tracker, then we fine-tune the agent on full 3D terrain. 

## _C. Reward Design_ 

The reward function is mainly composed by tracking reward terms, the responsible ones for making the agent learn foothold-tracking capabilities and penalization terms employed to enforce a natural locomotion style. Penalization terms, which are taken from the velocity-based locomotion reward implemented in _LocoMuJoCo_ [2], allow to learn a natural locomotion style, without relying on motion capture-based terms [32]. In this section we focus on tracking terms, while the penalization ones are detailed in appendix. 

**Foothold-Tracking Terms.** The fundamental term of our reward function is represented by the one responsible for tracking the goal **_g_** _t_ . Let pl<sup>_w_</sup><sup>**_p_**¯</sup><sup>_t_;</sup> l _w_<sup>**_ψ_**¯</sup><sup>_t_q,withlPt</sup><sup>_l, r_u,be</sup> 


Fig. 3: **Swing-based Reward.** Illustration of the desired swing interval. The reward term _r_ feet incentivizes foot clearance specifically when the phase variable _ϕt_ lies within the window 2 _δ_ sw. A non-zero reward is accumulated only if the correct foot breaks contact with the ground during this allotted time. 

the target foothold positions and orientations to be tracked by both feet. We define the foothold-tracking term as follows: 


where _r_ sw and _r_ st refer to the swing and stance foot, respectively. Notice that we explicited the fact that this reward term depends on the state **_s_** _t_ rather than on the observation **_o_** _t_ , since it needs world frame coordinates, always accessible in simulation. Specifically, we define _swing_ -related term as: 


where l P t _l, r_ u depends on the current _ϕt_ value, l<sup>_wψt_and</sup> l _w_<sup>_ψ_¯</sup><sup>_t_</sup> are the yaws (wrapped in r´ _π, π_ q) relative to the quaternions l _w_<sup>**_ψ_**</sup><sup>_t_and</sup> l _w_<sup>**_ψ_**¯</sup><sup>_t_,and</sup><sup>**_p_**</sup><sup>_t,xy_and</sup><sup>**_p_**</sup><sup>_t,z_representtheplanarandthe</sup> height components of vector **_p_** _t_ , respectively. The _r_ swp **_s_** _t,_ **_a_** _t_ q explicitly allows the policy to track the 3D target foothold for the swinging foot. Notice that decoupling planar and height components in _r_ swp **_s_** _t,_ **_a_** _t_ q allows to define different sharpness coefficients _ξ_ 1 and _ξ_ 2. In this context, this is needed given the different ranges covered by planar and height components. Finally, the _stance_ reward term _r_ stp **_s_** _t,_ **_a_** _t_ q is designed to retain the final value of the swing reward _r_ sw computed at the moment of touchdown. Specifically, for the entire duration of the stance phase, this term equals the accuracy achieved by the foot at the instant it transitioned from swing to stance. 

**Feet Swing Term.** To ensure adherence to the commanded gait schedule, we introduce the term _r_ feet. This reward encourages the feet to lift during the allotted swing phase defined by the variable _ϕt_ . Similar swing-phase incentives are standard in humanoid locomotion frameworks [2]. As depicted in Figure 3, we employ a temporal window within each gait phase where foot clearance is mandatory. Formally: 


where _δ_ sw represents the half-width of the swing window, and Cl (l P t _l, r_ u) acts as a binary “no-contact” indicator 


Fig. 4: **Evaluation Tasks in Simulation.** Simulation environments considered in Section V. Evaluations were conducted on: goal reaching, narrow bridge traversal, navigation in cluttered environments, and stairs and ramp climbing. 

(returning 1 when the foot is in the air). Also in this case, this term depends on the full state **_s_** _t_ rather than the observation **_o_** _t_ , as it relies on ground truth contact data. Note that, unlike the tracking term, _r_ feet is purely locomotion-related and does not depend on the foothold goal **_g_** _t_ . 

**Swing Knee Height Term.** The last fundamental tracking term encourages the robot to raise the knee of the swing leg, a particularly important skill when tracking the _z_ component of the desired foothold. Specifically, lifting the knee ensures sufficient clearance to bring the swing foot to the target height, avoiding collisions with steps or obstacles. This term is defined exclusively for the swing leg. The reward term is as follows: 


where l P tl _,_ ru depends on the current _ϕt_ to select the swing leg, l<sup>_w_</sup> **_<u>p</u>_** _t,z_ is the _z_ target for the swing foot in the world frame, _δ_ k is a slack representing a knee clearance margin, and l _,w_ k<sup>**_p_**</sup><sup>_t,z_</sup> is the world-frame _z_ coordinate of the knee joint of the swing leg. This term is one-sided: the reward is maximal whenever the knee exceeds the threshold l<sup>_w_</sup> **_<u>p</u>_** _t,z_ ` _δ_ k, and decays otherwise. 

V. EXPERIMENTS 

We evaluate the effectiveness of the proposed framework in simulation by comparing our Foothold-Tracking (FT) policy ( _π_ FT) against a state-of-the-art Velocity-Tracking (VT) baseline ( _π_ VT) trained via _LocoMuJoCo_ [2]. Due to the discrepancy of the command types, to ensure a fair comparison, both policies are trained within a equivalent command region, where velocity command _v_ FT can be converted by the foot distance _v_ VT and frequency _ν_ as _d_ FT _v_ VT “ 2 _d_ FT _ν_ . Through 


Fig. 5: **Goal-Reaching Experiment.** Time required to reach a target below different thresholds. Mean mean and standard deviation are shown for each setting with 1000 trials. 

a comprehensive set of carefully designed experiments, we demonstrate the agility, accuracy, and flexibility of our FT policy, showing that it enables a general-purpose locomotion policy with a wide range of motion capabilities. We use multiple task-specific high-level planners for _π_ FT in each experiment. This highlights the framework’s modularity, demonstrating that the learned policy serves as a general-purpose low-level controller capable of seamless integration with diverse upstream generators. Evaluation environments are illustrated in Figure 4. 

## _A. Goal Reaching Task_ 

We first evaluate the policies on the task of reaching a goal precisely and efficiently, which is an essential requirement for whole-body manipulation tasks. Here, we deploy a variant of _π_ FT trained on flat ground to isolate planar maneuvering performance. Targets are sampled in a r´3 _,_ 3sm region, and task success is defined by multiple distance-based thresholds. Additionally, we compare _π_ FT against _π_ FT-R, a baseline identical to our method except that foothold targets are expressed in the _root_ frame rather than the _stance foot_ frame. This ablation isolates the contribution of the stance-foot frame formulation. 

**High-Level Planners.** For _π_ FT and _π_ FT-R, we implement a simple planner that generates footholds along the vector connecting the robot’s base position to the goal. The step length is clamped to a maximum of 0 _._ 5 m, and footholds are constrained to feasible regions to prevent leg crossing. In the meantime, the foot orientation is steered towards the target direction to encourage forward walking. Footholds are generated respecting the gait frequency the policy saw during training. For _π_ VT, we employ a standard proportional controller: the target velocity is computed as **_v_** cmd “ _K_ p **_p_** goal ´ **_p_** baseq, saturated to the robot’s maximum velocity limits. The angular velocity is controlled by a separate P-controller to maintain the heading towards the target. In both methods, we assume the base positions are directly observable. Although unrealistic for real-world deployments, it allows us to decouple the effect from the localization errors encountered by both methods. 

**FT vs. VT.** We quantify performance by measuring the time-to-goal under three distinct acceptance radii, specifically, 0 _._ 2m, 0 _._ 1m, and 0 _._ 05m. For each threshold, we evaluate 1,000 

|**Policy**|FT (Ours)|FT-R|FT-R|FT-R|
|---|---|---|---|---|
|(_σ_xyz (m), _σ_yaw (deg))|—|(0, 0)|(3_e_´2, 2.0)|(6_e_´2, 3.0)|
|Accuracy (cm)<br>(mean ˘ std)|2.15 ˘ 0.164|1.66 ˘ 0.170|2.07 ˘ 0.237|2.86 ˘ 0.264|


TABLE I: **Frame Ablation.** Foothold-tracking accuracy across 1000 targets on flat terrain, comparing _π_ FT and _π_ FT´R. _σ_ xyz (m) and _σ_ yaw (deg) are the position and yaw noise scales for estimating base estimation errors for _π_ FT´R. 

trials with randomly sampled target positions. As shown in Figure 5, _π_ FT consistently outperforms _π_ VT, reaching the target significantly faster across all acceptance radii. This performance gain exhibit higher agility of the foot-tracking policy due to explicit control of the feet. Notably, as the success threshold decreases, the time-to-goal increases for _π_ FT by only 5.3%, whereas _π_ VT exhibits a substantially larger increase of 18.9%. This degradation for _π_ FT majorly stems from the inherit mismatch between the continuous velocity commands and discretized footstep execution, which necessitates multiple correcting steps near the target. On the contrary, footholdtracking directly command next foothold based on its current state and is therefore limited mainly by tracking accuracy. The results validate that explicit foothold control enables more aggressive and precise maneuvering compared to velocitybased commands, further narrowing the gap between high-level planning and low-level execution. 

**Frame Ablation.** Table I reports foothold-tracking accuracy across 1000 targets on flat terrain. To simulate real-world deployment conditions, we inject uniform noise into the base state estimate of _π_ FT´R, considering two noise scales to cover a range from mild to realistic localization error. Without noise, _π_ FT´R improves over _π_ FT in tracking accuracy, as the root frame provides a precise target signal under ideal conditions. However, performance degrades sharply even under small noise magnitudes, demonstrating that root-frame policies are sensitive to localization errors. By contrast, _π_ FT is unaffected by state estimation noise by design, validating the stance-foot frame as the more robust formulation for real-world deployment. 

## _B. Narrow Bridge Traversal_ 

In this experiment, we challenge motion accuracy between two tracking policies ( _π_ FT and _π_ VT) in a narrow bridge traversal task as shown in Fig 4-UpperRight. This scenario demands high-precision foot placement, as the tolerance for error is extremely low. The robot is initialized at a different location, aiming to pass a bridge with different widths and lengths. 

**High-Level Planners.** Both agents employ similar planners introduced in the goal-reaching experiment, with additional task-specific modifications. In particular, auxiliary waypoints are placed at the entrance and exit of the bridge to enforce the robot moving parallel to the bridge’s longitudinal direction. Due to the bridge’s restricted width, successful traversal requires precise lateral control. For _π_ FT, the planner generates foothold targets that explicitly maintain the robot’s footsteps near the centerline of the bridge. For _π_ VT, we increase the control gain on the robot’s heading direction to correct deviations that could otherwise result in a fall. 


Fig. 6: **Narrow Bridge Experiment.** The success rate(Ò) and traversing time(Ó) to cross a narrow bridge of different widths and lengths. Bridge width varies from 0.15 to 0.25m and length varies from 2 to 4m. Each configuration is conducted with 1000 trials with randomly sampled initial states and targets. 

|# Cones|**Success (%)**<br>Fall (%)<br>Plan|fail (%)|
|---|---|---|
|10|99<br>1|0|
|15|98<br>0|2|
|20|90<br>0|10|


TABLE II: **Cluttered Environment Experiment.** 100 episodes in a 6 m ˆ 6 m workspace with randomly placed cones. 

**Results.** We evaluate performance by measuring both success rate and traversal time across a range of bridge widths (0.15–0.25 m) and lengths (2–4 m). While both methods achieve high success rates, for less challenging configurations with a wider and shorter bridge, our _π_ FT controller consistently completes the traversal in less time, indicating more efficient motion execution. As the task difficulty increases, in the critical scenarios with a width of 0.15m, narrower than the robot’s foot length, the success rates for the VT controller drops drasticaly, whereas the FT-controller maintains almost the same performance. This is because the FT-tracking explicitly sets the desired target to be at the center of the bridge, eliminating the errors derived from proportional controller. Our foothold tracking controller provides a transparent and interpretable control interface enabling precise step-level reasoning and correction. This capability is crucial for safety-critical locomotion tasks, where accurate contact placement is required to prevent catastrophic failures, demonstrating the suitability of footholdbased control for real-world, constrained navigation scenarios. 

## _C. Traversing Complex Environments_ 

Finally, we demonstrate the integration of the trained _π_ FT in four additional tasks: cluttered environment traversal, straight and spiral staircase climbing, and ramp traversal. 

**Traversing Cluttered Environments.** Here the humanoid 


TABLE III: **Traversing Straight and Spiral Stairs.** Each cell reports success rate, riser-contact falls (R) and balance falls (B), and mean ˘ std 3D foot placement error (m). 100 evaluations with initial robot yaw sampled from _U_ p´ _π_ {6 _, π,_ 6q. 

is tasked with navigating a 6ˆ6 m region with up to 20 traffic cones, as shown in Figure 4. We employ Anytime Repairing A<sup>˚</sup> (ARA<sup>˚</sup> ) planner [13] to generate a sequence of foothold targets. The target candidates are selected from a set defined within the policy’s training range. We evaluate scenarios with 10, 15, and 20 traffic cones, conducting 100 trials for each configuration. Table II shows that our _π_ FT integrates seamlessly with the planner across all tested cases, with only one falling case observed. Failures are primarily due to the planning algorithms not finding a feasible path within the time budget. 

**Traversing Straight Stairs.** We evaluate the 3D-trained _π_ FT on a structured obstacle comprising an ascending staircase (5 steps), a landing platform, and a descending staircase (5 steps). _π_ FT was trained with elevation targets sampled in r´0 _._ 15 _,_ 0 _._ 15s m. We analyze performance over 100 episodes, randomizing the initial yaw orientation in _U_ p´ _π_ {6 _, π_ {6q and varying stair geometry (step length and height). A deterministic planner feeds _π_ FT with 3D footholds matching the terrain profile. Table IIIa shows that as the step height increases, the step length becomes a decisive factor: shorter steps leave little margin for tracking errors, as the swing foot must lift nearly vertically to clear the riser, making even minor inaccuracies likely to cause collisions. Longer steps provide a greater safety margin, allowing the policy to tolerate small placement imperfections without contacting the subsequent riser. This is further confirmed by the failure mode breakdown. At shorter step lengths, failures are dominated by riser contacts, reflecting the tight clearance constraints. As step length enlarges, risercontact failures decrease and balance-related falls become the primary failure mode, a consequence of the wider stance required to sustain a longer gait cycle. 

**Traversing Spiral Stairs.** We further evaluate the 3Dtrained _π_ FT on a more challenging terrain consisting of an ascending staircase with rotating steps (´10<sup>˝</sup> yaw offset per step) terminating on a flat platform, designed to emulate a spiral staircase and to validate the omnidirectional capabilities of policies trained within the proposed framework. The policy is identical to that used in the straight staircase experiment. Table IIIb shows that the results mirror those of the straight staircase: longer steps consistently reduce riser-contact failures. However, due to the step rotation, targets are no longer placed at uniform lateral and vertical distances, meaning that further 

|**Step**<br>**Length**||||**Final Rise (m)**||||
|---|---|---|---|---|---|---|---|
|**(m)**|**0.05**|**0.10**|**0.15**|**0.20**|**0.25**|**0.30**|**0.35**|
||100%|100%|99%|76%|47%|7%|0%|
|**0.300**|B:0|B:0|B:1|B:24|B:53|B:93|B:100|
||0.039˘0.009|0.046˘0.007|0.058˘0.015|0.133˘0.093|0.155˘0.085|0.319˘0.172|0.350˘0.154|
||100%|100%|99%|96%|87%|35%|5%|
|**0.325**|B:0|B:0|B:1|B:4|B:13|B:65|B:95|
||0.037˘0.004|0.043˘0.009|0.057˘0.015|0.092˘0.071|0.120˘0.060|0.230˘0.140|0.338˘0.151|
||100%|100%|97%|96%|89%|68%|6%|
|**0.350**|B:0|B:0|B:3|B:4|B:11|B:32|B:94|
||0.040˘0.011|0.045˘0.010|0.064˘0.049|0.090˘0.051|0.110˘0.057|0.199˘0.113|0.380˘0.170|
||100%|100%|95%|85%|47%|46%|57%|
|**0.375**|B:0|B:0|B:5|B:15|B:53|B:54|B:43|
||0.054˘0.019|0.065˘0.016|0.104˘0.060|0.115˘0.064|0.173˘0.065|0.207˘0.101|0.201˘0.103|


TABLE IV: **Traversing Ramps.** Each cell reports success rate, balance falls (B), and mean ˘ std 3D foot placement error (m). 100 evaluations with initial robot yaw „ _U_ p´ _π_ {6 _, π_ {6q). 

increasing the step length does not monotonically reduce failures. As evidenced by the results, the optimal step length is 0 _._ 35 m, beyond which balance-related failures begin to increase. Together with the straight staircase experiment, these results confirm that _π_ FT is capable of complex omnidirectional locomotion while operating without terrain perception, relying solely on proprioception. 

**Traversing Ramps.** Finally, we evaluate _π_ FT on an additional obstacle, structurally analogous to the straight staircase scenario, but replacing discrete steps with continuous ascending and descending ramps of varying inclination. This experiment is critical for assessing the generalization capabilities of a policy trained within the proposed framework. Indeed, as described in Section IV, the 3D fine-tuning stage employs moving pillars as contact surfaces, meaning the policy never encounters sloped foot placements during training. Successfully traversing ramps therefore requires the policy to generalize its _z_ -tracking capabilities to unseen foot pitch configurations. Table IV shows that _π_ FT handles this setting effectively. A trend consistent with the staircase experiments emerges: longer steps yield higher success rates as task difficulty increases. However, this phenomenon has a different explanation here. At high inclinations with short steps, the robot loses balance due to the steep vertical rise demanded per foothold. Conversely, excessively long steps also increase balance failures, as the robot must sustain a longer gait cycle. The optimal step length sits around 0 _._ 35 m across most inclinations. These results confirm that the proposed framework produces policies with strong generalization capabilities. 


Fig. 7: **Real-World Deployment.** Sequence of the robot tasked with traversing a corridor while stepping on predefined targets. Markers are detected via the onboard camera and then mapped to valid footholds targets in the stance foot frame via a transformation by forward kinematics. For each pose snapshot, we display the corresponding camera frame with highlighted targets. The second pose from the right details the target generation logic during a gait phase switch. Here, the right foot becomes the new stance foot. 

## VI. REAL-WORLD RESULTS 

In the real-world experiment, to avoid additional complexity introduced by the localization problem, we employ a visionbased foothold tracking task to verify our FT policy. As illustrated in Figure 7, a sequence of blue circular markers is manually placed on the ground in a corner of a corridor to serve as visual foothold targets. We use the onboard RealSense D455 camera of the Booster T1 robot to extract the targets. By fusing RGB-based target detection, the depth measurements, and the robot’s kinematic model, we compute the relative transformations between the targets and the robot’s current stance foot. The foothold orientations are heuristically determined based on the upcoming swing targets to ensure the feasibility of the future targets. A snapshot of the target detection results is illustrated in Figure 7. Due to delays introduced by camera frame rate limitations, communication latency, and policy inference time, the swing foot may not reach the commanded foothold exactly at the nominal swing–stance transition defined by the gait phase. To address this issue, we implement a simple delay compensation mechanism that repeats the same gait phase **_ϕ_** _t_ and foothold target **_g_** _t_ until the relative height between the swing and the stance foot falls below a threshold, ensuring the relative targets are computed with the next stance on the ground. 

**Results** . We evaluate the system over 20 real-world trials, including both forward and backward traversals in the corridor with manual resets. An uncut video of the experiments is provided as supplementary. Despite sensing noise and system delays, the robot achieves 93.08% success of stepping on designated foothold targets while maintaining stable locomotion. These results demonstrate the practical viability of the proposed FT controller in real-world settings, even when driven by 

imperfect visual perception. The primary sources of footplacement error arise from motion-induced image blur, which degrades target detection accuracy, and from depth sensing artifacts, as the depth camera is not optimized for highly dynamic motion. Furthermore, although the sim-to-real gap is significantly mitigated by the large-scale domain randomization, it also poses costs in losing tracking accuracy. Despite the presence of tracking error, this experiment successfully verifies that _π_ FT can be seamlessly integrated into sophisticated highlevel planners to support various downstream tasks. 

## VII. CONCLUSION 

In this work, we present a general foothold-conditioned training framework that integrates seamlessly with a wide range of high-level planning algorithms. By introducing a generalpurpose 3D goal sampler, our approach enables adaptive terrain generation and supports stable foot placement. To address the limitations of prior methods that rely on accurate pose estimation or explicit foot–contact estimation, we represent foothold targets in the stance-foot frame and hold them constant throughout each swing phase. This design ensures consistent target tracking and robust execution. Through extensive comparisons with a standard velocity-tracking policy, we show that our foothold tracking controller achieves more agile and efficient goal reaching, delivers consistent performance in precision-critical tasks, and robustly traverses challenging cluttered environments and staircases. Finally, we validate the real-world deployability of our approach through a fully visionbased foothold tracking experiment, demonstrating reliable sim-to-real transfer without reliance on external localization. Together, these results highlight the practicality, versatility, and robustness of the proposed framework for humanoid locomotion in complex safety-critical scenarios. 

## ACKNOWLEDGMENTS 

This publication was funded with the contribution of Ministero dell’Universita` e della ricerca pursuant to D.D. n. 7206 of 17 April 2025 – BANDO FIS 2. Project FIS-2023-02598 (Starting Grant), title: “Unified Learning from Diverse Human Feedback” (HUmLrn). CUP: D53C25000710001. The project is supported by the Fundamental Research Funds for the Central Universities. 

## REFERENCES 

- [1] Ananye Agarwal, Ashish Kumar, Jitendra Malik, and Deepak Pathak. Legged locomotion in challenging terrains using egocentric vision. In _Conference on robot learning_ , pages 403–415. PMLR, 2023. 

- [2] Firas Al-Hafez, Guoping Zhao, Jan Peters, and Davide Tateo. Locomujoco: A comprehensive imitation learning benchmark for locomotion. In _6th Robot Learning Workshop, NeurIPS_ , 2023. 

- [3] Lingfan Bao, Joseph Humphreys, Tianhu Peng, and Chengxu Zhou. Deep reinforcement learning for bipedal locomotion: A brief survey. _arXiv preprint arXiv:2404.17070_ , 2024. 

- [4] Qingwei Ben, Botian Xu, Kailin Li, Feiyu Jia, Wentao Zhang, Jingping Wang, Jingbo Wang, Dahua Lin, and Jiangmiao Pang. Gallant: Voxel grid-based humanoid locomotion and local-navigation across 3d constrained terrains. _arXiv preprint arXiv:2511.14625_ , 2025. 

- [5] Xuxin Cheng, Kexin Shi, Ananye Agarwal, and Deepak Pathak. Extreme parkour with legged robots. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11443–11450. IEEE, 2024. 

- [6] Thomas Corberes,` Carlos Mastalli, Wolfgang Merkt, Jaehyun Shim, Ioannis Havoutis, Maurice Fallon, Nicolas Mansard, Thomas Flayols, Sethu Vijayakumar, and Steve Tonneau. Perceptive locomotion through whole-body mpc and optimal region selection. _IEEE Access_ , 2025. 

- [7] Helei Duan, Ashish Malik, Jeremy Dao, Aseem Saxena, Kevin Green, Jonah Siekmann, Alan Fern, and Jonathan Hurst. Sim-to-real learning of footstep-constrained bipedal dynamic walking. In _2022 International Conference on Robotics and Automation (ICRA)_ , pages 10428–10434. IEEE, 2022. 

- [8] Siddhant Gangapurwala, Mathieu Geisert, Romeo Orsolino, Maurice Fallon, and Ioannis Havoutis. Rloc: Terrain-aware legged locomotion using reinforcement learning and optimal control. _IEEE Transactions on Robotics_ , 38(5):2908–2927, 2022. 

- [9] Ruben Grandia, Fabian Jenelten, Shaohui Yang, Farbod Farshidian, and Marco Hutter. Perceptive locomotion through nonlinear model-predictive control. _IEEE Trans. Robotics_ , 39(5):3402–3421, 2023. 

- [10] Robert J. Griffin, Georg Wiedebach, Stephen McCrory, Sylvain Bertrand, Inho Lee, and Jerry E. Pratt. Footstep planning for autonomous walking over rough terrain. In _19th IEEE-RAS International Conference on Humanoid_ 

_Robots, Humanoids 2019, Toronto, ON, Canada, October 15-17, 2019_ , pages 9–16. IEEE, 2019. 

- [11] Junzhe He, Chong Zhang, Fabian Jenelten, Ruben Grandia, Moritz Bacher,¨ and Marco Hutter. Attention-based map encoding for learning generalized legged locomotion. _Science Robotics_ , 10(105):eadv3604, 2025. 

- [12] Tairan He, Chong Zhang, Wenli Xiao, Guanqi He, Changliu Liu, and Guanya Shi. Agile but safe: Learning collision-free high-speed legged locomotion. _arXiv preprint arXiv:2401.17583_ , 2024. 

- [13] Armin Hornung, Andrew Dornbush, Maxim Likhachev, and Maren Bennewitz. Anytime search-based footstep planning with suboptimality bounds. In _2012 12th IEEE-RAS International Conference on Humanoid Robots (Humanoids 2012)_ , pages 674–679. IEEE, 2012. 

- [14] TianChen Huang, Runchen Xu, Yu Wang, Wei Gao, and Shiwu Zhang. Traversing narrow paths: A two-stage reinforcement learning framework for robust and safe humanoid walking. _arXiv preprint arXiv:2508.20661_ , 2025. 

- [15] Fabian Jenelten, Takahiro Miki, Aravind E Vijayan, Marko Bjelonic, and Marco Hutter. Perceptive locomotion in rough terrain–online foothold optimization. _IEEE Robotics and Automation Letters_ , 5(4):5370–5376, 2020. 

- [16] Fabian Jenelten, Ruben Grandia, Farbod Farshidian, and Marco Hutter. Tamols: Terrain-aware motion optimization for legged systems. _IEEE Transactions on Robotics_ , 38 (6):3395–3413, 2022. 

- [17] Fabian Jenelten, Junzhe He, Farbod Farshidian, and Marco Hutter. Dtc: Deep tracking control. _Science Robotics_ , 9 (86):eadh5401, 2024. 

- [18] Tobias Johannink, Shikhar Bahl, Ashvin Nair, Jianlan Luo, Avinash Kumar, Matthias Loskyll, Juan Aparicio Ojea, Eugen Solowjow, and Sergey Levine. Residual reinforcement learning for robot control. In _2019 international conference on robotics and automation (ICRA)_ , pages 6023–6029. IEEE, 2019. 

- [19] Shuuji Kajita, Fumio Kanehiro, Kenji Kaneko, Kiyoshi Fujiwara, Kensuke Harada, Kazuhito Yokoi, and Hirohisa Hirukawa. Biped walking pattern generation by using preview control of zero-moment point. In _2003 IEEE international conference on robotics and automation (Cat. No. 03CH37422)_ , volume 2, pages 1620–1626. IEEE, 2003. 

- [20] Ashish Kumar, Zipeng Fu, Deepak Pathak, and Jitendra Malik. Rma: Rapid motor adaptation for legged robots. _arXiv preprint arXiv:2107.04034_ , 2021. 

- [21] Ho Jae Lee, Seungwoo Hong, and Sangbae Kim. Integrating model-based footstep planning with model-free reinforcement learning for dynamic legged locomotion. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 11248–11255. IEEE, 2024. 

- [22] Joonho Lee, Jemin Hwangbo, Lorenz Wellhausen, Vladlen Koltun, and Marco Hutter. Learning quadrupedal locomotion over challenging terrain. _Science robotics_ , 5(47): 

eabc5986, 2020. 

- [23] Junfeng Long, Zirui Wang, Quanyi Li, Jiawei Gao, Liu Cao, and Jiangmiao Pang. Hybrid internal model: Learning agile legged locomotion with simulated robot response. _arXiv preprint arXiv:2312.11460_ , 2023. 

- [24] Gabriel B Margolis, Ge Yang, Kartik Paigwar, Tao Chen, and Pulkit Agrawal. Rapid locomotion via reinforcement learning. _The International Journal of Robotics Research_ , 43(4):572–587, 2024. 

- [25] Carlos Mastalli, Ioannis Havoutis, Michele Focchi, Darwin G Caldwell, and Claudio Semini. Motion planning for quadrupedal locomotion: Coupled planning, terrain mapping, and whole-body control. _IEEE Transactions on Robotics_ , 36(6):1635–1648, 2020. 

- [26] Oliwier Melon, Romeo Orsolino, David Surovik, Mathieu Geisert, Ioannis Havoutis, and Maurice Fallon. Recedinghorizon perceptive trajectory optimization for dynamic legged locomotion with learned initialization. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9805–9811. IEEE, 2021. 

- [27] Takahiro Miki, Joonho Lee, Jemin Hwangbo, Lorenz Wellhausen, Vladlen Koltun, and Marco Hutter. Learning robust perceptive locomotion for quadrupedal robots in the wild. _Science robotics_ , 7(62):eabk2822, 2022. 

- [28] Bhavyansh Mishra, Duncan Calvert, Sylvain Bertrand, Jerry Pratt, Hakki Erhan Sevil, and Robert Griffin. Efficient terrain map using planar regions for footstep planning on humanoid robots. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8044–8050. IEEE, 2024. 

- [29] I Nahrendra, Byeongho Yu, and Hyun Myung. Dreamwaq: Learning robust quadrupedal locomotion with implicit terrain imagination via deep reinforcement learning. _arXiv preprint arXiv:2301.10602_ , 2023. 

- [30] Sanmit Narvekar, Bei Peng, Matteo Leonetti, Jivko Sinapov, Matthew E Taylor, and Peter Stone. Curriculum learning for reinforcement learning domains: A framework and survey. _Journal of Machine Learning Research_ , 21 (181):1–50, 2020. 

- [31] Shafeef Omar, Lorenzo Amatucci, Victor Barasuol, Giulio Turrisi, and Claudio Semini. Safesteps: Learning safer footstep planning policies for legged robots via modelbased priors. In _2023 IEEE-RAS 22nd International Conference on Humanoid Robots (Humanoids)_ , pages 1–8. IEEE, 2023. 

- [32] Xue Bin Peng, Glen Berseth, KangKang Yin, and Michiel Van De Panne. Deeploco: Dynamic locomotion skills using hierarchical deep reinforcement learning. _Acm transactions on graphics (tog)_ , 36(4):1–13, 2017. 

- [33] Lerrel Pinto, Marcin Andrychowicz, Peter Welinder, Wojciech Zaremba, and Pieter Abbeel. Asymmetric actor critic for image-based robot learning. In _Proceedings of Robotics: Science and Systems_ , Pittsburgh, Pennsylvania, June 2018. doi: 10.15607/RSS.2018.XIV.008. 

- [34] Jerry Pratt, John Carff, Sergey Drakunov, and Ambarish Goswami. Capture point: A step toward humanoid push 

recovery. In _2006 6th IEEE-RAS international conference on humanoid robots_ , pages 200–207. Ieee, 2006. 

- [35] Martin L. Puterman. _Markov Decision Processes: Discrete Stochastic Dynamic Programming_ . Wiley Series in Probability and Statistics. John Wiley & Sons, 2014. 

- [36] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [37] Jonah Siekmann, Yesh Godse, Alan Fern, and Jonathan Hurst. Sim-to-real learning of all common bipedal gaits via periodic reward composition. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7309–7315. IEEE, 2021. 

- [38] Tom Silver, Kelsey Allen, Josh Tenenbaum, and Leslie Kaelbling. Residual policy learning. _arXiv preprint arXiv:1812.06298_ , 2018. 

- [39] Rohan P Singh, Mehdi Benallegue, Mitsuharu Morisawa, Rafael Cisneros, and Fumio Kanehiro. Learning bipedal walking on planned footsteps for humanoid robots. In _2022 IEEE-RAS 21st International Conference on Humanoid Robots (Humanoids)_ , pages 686–693. IEEE, 2022. 

- [40] Richard S Sutton, Andrew G Barto, et al. _Reinforcement learning: An introduction_ , volume 1. MIT press Cambridge, 1998. 

- [41] Vassilios Tsounis, Mitja Alge, Joonho Lee, Farbod Farshidian, and Marco Hutter. Deepgait: Planning and control of quadrupedal gaits using deep reinforcement learning. _IEEE Robotics and Automation Letters_ , 5(2): 3699–3706, 2020. 

- [42] Huayi Wang, Zirui Wang, Junli Ren, Qingwei Ben, Tao Huang, Weinan Zhang, and Jiangmiao Pang. Beamdojo: Learning agile humanoid locomotion on sparse footholds. _Robotics: Science and Systems (RSS)_ , 2025. 

- [43] Alexander W Winkler, C Dario Bellicoso, Marco Hutter, and Jonas Buchli. Gait and trajectory optimization for legged systems through phase-based end-effector parameterization. _IEEE Robotics and Automation Letters_ , 3(3):1560–1567, 2018. 

- [44] Zhaoming Xie, Hung Yu Ling, Nam Hee Kim, and Michiel Van De Panne. Allsteps: curriculum-driven learning of stepping stone skills. In _Computer Graphics Forum_ , volume 39, pages 213–224. Wiley Online Library, 2020. 

- [45] Zhaoming Xie, Xingye Da, Buck Babich, Animesh Garg, and Michiel van de Panne. Glide: Generalizable quadrupedal locomotion in diverse environments with a centroidal model. In _International workshop on the algorithmic foundations of robotics_ , pages 523–539. Springer, 2022. 

- [46] Ruihan Yang, Ge Yang, and Xiaolong Wang. Neural volumetric memory for visual locomotion control. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 1430–1440, 2023. 

- [47] Ruiqi Yu, Qianshi Wang, Yizhen Wang, Zhicheng Wang, Jun Wu, and Qiuguo Zhu. Walking with terrain reconstruction: Learning to traverse risky sparse footholds. _arXiv_ 

_preprint arXiv:2409.15692_ , 2024. 

- [48] Wenhao Yu, Deepali Jain, Alejandro Escontrela, Atil Iscen, Peng Xu, Erwin Coumans, Sehoon Ha, Jie Tan, and Tingnan Zhang. Visual-locomotion: Learning to walk on complex terrains with vision. In _5th Annual Conference on Robot Learning_ , 2021. 

- [49] Petr Zaytsev, S Javad Hasaneini, and Andy Ruina. Two steps is enough: No need to plan far ahead for walking balance. In _2015 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6295–6300. IEEE, 2015. 

- [50] Chong Zhang, Nikita Rudin, David Hoeller, and Marco Hutter. Learning agile locomotion on risky terrains. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 11864–11871. IEEE, 2024. 

- [51] Ziwen Zhuang, Zipeng Fu, Jianren Wang, Christopher Atkeson, Soeren Schwertfeger, Chelsea Finn, and Hang Zhao. Robot parkour learning. _arXiv preprint arXiv:2309.05665_ , 2023. 

APPENDIX 

Here, we present additional details for the experiments presented in the main paper. All the media reporting videos for the real-world experiment and the simulated ones can be found in the attached zip and in the project website ( **https://montenegroalessandro.github.io/mind-your-steps/** ). 

## _A. Observations for Actor and Critic Networks_ 

The table below details the observations received by the actor and critic networks, specifying whether the components are subject to noise. 

|**Network**|**Observation**|**Noise**|
|---|---|---|
||Base Angular Velocity|✓|
||Projected Gravity|✓|
|**Actor**|Joint Positions|✓|
||Joint Velocities|✓|
||Last Action|✗|
||Goal|✗|
||Base Linear Velocity|✗|
||Base Angular Velocity|✗|
|**Critic**|Projected Gravity|✗|
||Joint Positions|✗|
||Joint Velocities|✗|
||Last Action|✗|
||Goal|✗|


## _B. Domain Randomization_ 

We detail the domain randomization parameters below. Randomization is applied at the beginning of each episode, with the exception of external disturbances, which occur at each timestep with a certain probability. For each parameter, we define the randomization method as follows: 

- ‚ **Direct** : The value is uniformly sampled from the specified interval and directly employed. 

- ‚ **Multiplier** : A scaling factor is uniformly sampled from the reported range and multiplied by the nominal value. 

- ‚ **Additive** _U_ : An offset is sampled uniformly from the range and added to the nominal value. 

- ‚ **Additive** _N_ : Noise is sampled from a Normal distribution with the specified scale and added to the nominal value. 

|**Parameter**<br>**Type**|**Value / Range**|
|---|---|
|_Global Dynamics & Inertial Pro_|_perties_<br>|
|Gravity (_z_-axis)<br>Direct|r9_._51_,_10_._11sm/s<sup>2</sup>|
|Root Body Mass<br>Multiplier|r0_._8_,_1_._2s|
|Link Mass<br>Multiplier|r0_._9_,_1_._1s|
|CoM Displacement (_x, y, z_)<br>Additive _U_|r´0_._05_,_0_._05sm|
|_Terrain Contact Properties (Floor _|_& Pillars)_<br>|
|Tangential Friction<br>Direct|r0_._5_,_1_._5s|
|Torsional Friction<br>Direct|r0_._1_,_0_._3s|
|Rolling Friction<br>Direct|r8ˆ10<sup>´5</sup>_,_1_._2ˆ10<sup>´4</sup>s|
|_Actuation & Joint Properti_|_es_<br>|
|Joint Damping<br>Direct|r0_._005_,_0_._03sNms/rad|
|Joint Friction Loss<br>Direct|r0_._0_,_1_._0sNm|
|Joint Armature<br>Direct|r0_._007_,_0_._03skg m<sup>2</sup>|
|KP Gain Noise<br>Additive _U_|r´0_._15¨_KP ,_0_._15¨_KP_s|
|KD Gain Noise<br>Additive _U_|r´0_._5¨_KD,_0_._5¨_KD_s|
|_Observation Noise_<br>||
|Joint Position<br>Additive _N_|˘0_._03rad|
|Joint Velocity<br>Additive _N_|˘0_._3rad/s|
|Angular Velocity<br>Additive _N_|˘0_._2rad/s|
|Projected Gravity Vector<br>Additive _N_|˘0_._015|
|_External Disturbances_<br>Random Kicks (Velocity)<br>Additive _U_<br>(Per-step w.p. 0_._004)|r0_._1_,_0_._4sm/s|


## _C. PPO Common Training Hyperparameters_ 

The table below details the PPO hyperparameters common to both the flat-terrain and _z_ -tracking training configurations. 

|**Parameter**<br>**Value**|
|---|
|_PPO Algorithm_|
|Discount Factor (_γ_)<br>0_._995|
|GAE Parameter (_λ_)<br>0_._95|
|Clipping Range (_ϵ_)<br>0_._2<br>i|
|Entropy Coefficient<br>0_._01<br>i|
|Value Function Coefficient<br>0_._5|
|Max Gradient Norm<br>1_._0|
|_Adaptive Learning Rate_|
|Initial Learning Rate<br>1ˆ10<sup>´5</sup>|
|Min Learning Rate<br>1ˆ10<sup>´6</sup>|
|Max Learning Rate<br>0_._01|
|KL Target<br>0_._02|
|KL Margin<br>1_._5|
|KL Scale Factor<br>1_._5|
|_Employed Samples_|
|Parallel Environments<br>8192|
|Horizon Steps<br>50|
|Update Epochs<br>20|
|Mini-batches per Epoch<br>1|
|Observation Normalization<br>True|
|Reward Normalization<br>True|
|Observation History Length<br>1|
|_Policy Network_|
|Hidden Layers<br>512ˆ256ˆ128|
|Activation Function<br>ELU|
|Initial Action Std<br>0_._135|
|Learnable Action Std<br>True|


## _D. Additional Reward Terms_ 

While Section IV details the main tracking terms, i.e., _r_ track and _r_ feet, here we specify the additional reward terms employed and report the common used coefficients’ values (Table V). For other penalization terms, please refer to the CrispBoosterLocomotionReward in [2], upon which our implementation is based. 

|**Reward Term**|**Description**|**Coefficients**|
|---|---|---|
|_r_jntp**_s_**_t,_**_a_**_t_q “_ω_jntexp<br>`<br>´_ξ_jnt}**_q_**jnt_,t_´ ¯**_q_**jnt}<sup>2</sup><br>2<br>˘|Tracks upper body joint reference ¯**_q_**jnt.|_ω_jnt “_ξ_jnt “4|
|_r_bhp**_s_**_t,_**_a_**_t_q “ ´_ω_bhp<sup>_w_</sup><br>_b_<sup>**_p_**</sup><sup>_t,z_ ´</sup> <sup>_w_</sup><br>_b_ <sup>¯</sup><sup>**_p_**</sup><sup>_z_q2</sup>|Tracks CoM height reference <sup>_w_</sup><br>_b_ <sup>¯</sup><sup>**_p_**</sup><sup>_z_.</sup>|_ω_bh “10|
|_r_arp**_s_**_t,_**_a_**_t_q “ ´_ω_ar}**_a_**_t_´**_a_**_t_´1}<sup>2</sup><br>2|Penalizes large action changes (smoothness).|_ω_ar “3|
|_r_fsp**_s_**_t,_**_a_**_t_q “ ´_ω_fs<br>ř<br>lPt_l,r_u <sup>}</sup><sup>_w_</sup><br>l <sup>9</sup><sup>**_p_**</sup><sup>_t_</sup> <sup>¨ Cl}2</sup><br>2|Penalizes foot velocity during ground contact (no-slip).|_ω_fs “4|


TABLE V: Additional reward terms and their coefficients. 

For the sake of completeness, we additionally report (Table VI) the terms we detailed in Section IV. 

|**Reward Term**|**Description**|**Coefficients**|
|---|---|---|
|_r_feetp**_s_**_t,_**_a_**_t_q (See Section IV)|Enforces feet swinging in the allotted period.|_ω_feet “6, _δ_sw “0_._1|
|_r_trackp**_s_**_t,_**_a_**_t_q (See Section IV)|Tracks desired foothold targets.|_ω_1 “_ω_2 “_ω_3 “5<br>_ξ_1 “_ξ_3 “100, _ξ_2 “200|
|_r_kp**_s_**_t,_**_a_**_t_q (See Section IV)|Enforces the knee of the swinging foot to stay above a certain height.|_ω_k “4, _ξk_ “200<br>_δk_ “0_._25|


TABLE VI: Tracking and feet swing reward terms and their coefficients. 

## _E. Details on the Employed Velocity-based Policy_ 

In Section V, we compare our approach against a velocity-tracking policy _π_ VT, trained via the _LocoMuJoCo_ pipeline [2]. Specifically, _π_ VT shares the same observation vector as our _π_ FT: 


where the goal **_g_** _t_ specifies the target base velocity and height: 


> _wb_<sup>_ψ_¯99isthetargetangularvelocity,and</sup><sup>_w_</sup> _b_<sup>**_p_**¯</sup><sup>_z_isthe</sup> 

Here, _wb_<sup>**_p_**¯9</sup><sup>_x_and</sup> _wb_<sup>**_p_**¯9</sup><sup>_y_denotethetargetlongitudinalandlateralvelocities,</sup> _b_<sup>_ψ_¯99isthetargetangularvelocity,and</sup><sup>_w_</sup> _b_<sup>**_p_**¯</sup><sup>_z_isthe</sup> target base height. We highlight an additional difference regarding the primary tracking objectives compared to _π_ FT. While the foothold-tracking policy aims at minimizing the error terms detailed in Section IV, _π_ VT utilizes a standard velocity-tracking reward defined as: 


with coefficients set to _ω_ 1 “ _ω_ 2 “ 1 _._ 5, _ω_ 3 “ 1, and _ξ_ 1 “ _ξ_ 2 “ _ξ_ 3 “ 4. Base height tracking follows the formulation described in Appendix D, while all other regularization terms remain identical to those used for _π_ FT. Finally, the target velocities are sampled uniformly: _wb_<sup>**_p_**¯9</sup><sup>_x_„</sup><sup>_U_p´0</sup><sup>_._8</sup><sup>_,_0</sup><sup>_._8qm/s,</sup> _wb_<sup>**_p_**¯9</sup><sup>_y_„</sup><sup>_U_p´0</sup><sup>_._5</sup><sup>_,_0</sup><sup>_._5qm/s,and</sup> _wb_<sup>_ψ_¯9„</sup><sup>_U_p´1</sup><sup>_._5</sup><sup>_,_1</sup><sup>_._5qrad/s.</sup> 

## _F. Training Parameters for the Policy Used for Flat Terrains_ 

The following details hold for both _π_ FT and _π_ FT´R, i.e., the FT policy with targets represented int he stance foot frame and in the root frame, respectively. The policies were trained with PPO for a total of 10<sup>9</sup> timesteps. The table below reports the values used for the goal parameters. Parameters defined by a range are sampled uniformly from the specified interval according to the schedule described in Section IV, while scalar values denote parameters kept constant throughout training. 

|**Parameter**<br>**Value / Range**|
|---|
|_Step Generation_|
|Movement Direction (_θ_move)<br>r´_π, π_q rad|
|Feet Direction (_θ_feet)<br>0 rad|
|Step Length (_d_)<br>r0_._2_,_0_._5s m|
|_θ_move Perturbation (_α_)<br>r´2_π_{9_,_2_π_{9s rad|
|_θ_feet Perturbation (_β_)<br>r´_π_{6_, π_{6s rad|
|Height Offset (_z_)<br>0 m|
|_Gait Constraints_|
|Minimum Feet Distance<br>0_._10 m|
|Hold Still Probability (_p_hold)<br>0_._1|
|Hold Still Feet Width<br>0_._20 m|


For the reward terms, we employed the values detailed in Appendix D, but setting _ω_ 2 “ 0 in order to exclude the tracking of the _z_ -component. Moreover, we set _ω_ k “ 0 in order to exclude the swinging knee height term. 

## _G. Training Parameters for the Policy Used for Stairs_ 

In this experiment, the policy was trained using PPO for 1 _._ 2 ¨ 10<sup>9</sup> timesteps, initialized from the flat-terrain policy weights. The table below lists the goal parameters. Ranges imply uniform sampling according to the schedule in Section IV, while scalar values denote constant parameters. The reward terms are detailed in Appendix D. 

|**Parameter**|**Value / Range**|
|---|---|
|_Step Generat_|_ion_|
|Movement Direction (_θ_move)|_πx_ rad, _x_„_B_p0_._5q|
|Feet Direction (_θ_feet)|0 rad|
|Step Length (_d_)|r0_._2_,_0_._4s m|
|_θ_move Perturbation (_α_)|r´_π_{18_, π_{18s rad|
|_θ_feet Perturbation (_β_)|r´_π_{18_, π_{18s rad|
|Height Offset (_z_)|r´0_._15_,_0_._15s m|
|_Gait Constra_|_ints_|
|Minimum Feet Distance|0_._10 m|
|Hold Still Probability (_p_hold)|0|
|Hold Still Feet Width|0_._20 m|


Notably, for this task, we restricted the motion to strictly forward or backward directions, without the possibility of staying still. This is denoted in the table by _θ_ move “ _πx_ , where _x_ „ _B_ p0 _._ 5q represents a Bernoulli variable yielding discrete values t0 _,_ 1u with equal probability. Notice that the fact that the robot is just trained to go forward or backward it is not restricting the robot’s curving capabilities, as demonstrated by the spiral stairs experiment. 

**On Moving Pillars Terrain.** To ensure continuous foothold availability, we employed a dynamic terrain system comprising three dynamic pillars, with a diameter of 0 _._ 3 m and friction features matching the floor. These pillars are placed such that whenever a new foot placement target is sampled, the currently free pillar is relocated to the goal position. We define a pillar as free when it is not currently supporting a foot. To ensure valid placements, we employ a rejection sampling mechanism (2048 batched samples) that prevents collisions with the robot’s feet or the active stance pillars. Furthermore, to mitigate early termination caused by minor planar tracking errors, we implement an adaptive landing mechanism. During the final portion of the swing phase (specifically when _ϕt_ P r0 _._ 25 ` _δ_ sw _,_ 0 _._ 5q or _ϕt_ P r0 _._ 75 ` _δ_ sw _,_ 1s, see Figure 3), the target pillar shifts its _xy_ -position to track the swinging foot’s projection. Crucially, the pillar’s height _z_ remains fixed to the originally sampled value. 

## _H. High-Level Planners_ 

In this section, we detail the high-level planners employed for both the simulated experiments and the real-world deployment. **Goal-Reaching Planner.** For the goal-reaching task, _π_ FT is guided by a deterministic foothold planner. At each gait update, the goal position and base position are expressed in the _stance-foot frame_ as _g_<sup>_s_</sup><sup>**_p_**and</sup><sup>_s_</sup> _b_<sup>**_p_**,respectively.IftheplanarEuclidean</sup> distance to the goal falls below a threshold } _g_<sup>_s_</sup><sup>**_p_**</sup><sup>_xy_´</sup><sup>_s_</sup> _b_<sup>**_p_**</sup><sup>_xy_}2ď</sup><sup>_ϵ_,therobotiscommandedtostandstill,markingtaskcompletion.</sup> Otherwise, the target for the next swing foot is generated based on the difference vector **_d_** “ _g_<sup>_s_</sup><sup>**_p_**´</sup><sup>_s_</sup> _b_<sup>**_p_**.Thetargetyawis</sup> computed as _θ_ “ clippatan2p **_d_** _y,_ **_d_** _x_ q _,_ ´60<sup>˝</sup> _,_ 60<sup>˝</sup> q, while the foot target is calculated as ˝<sup>_s_</sup><sup>**_p_**“</sup><sup><u>1</u></sup> 2<sup>Is</sup><sup>_d_feet</sup><sup>**_v_**feet `</sup><sup>_d_max</sup> } **_dd_** }2<sup>,where</sup><sup>_d_feet</sup> prescribes the nominal distance between two feet, _d_ max is the maximum distance per step, **_v_** feet “ r0 _,_ 1s<sup>⊺</sup> , and Is P t´1 _,_ 1u is indicator of the swing foot, ´1 for right foot swinging and 1 for left foot swinging. Notice that for _π_ FT´R the same procedure applies, but then the policy is fed with the goal **_g_** _t_ components expressed in the _root frame_ . The resulting swing target is clipped to satisfy the feasible constraints to avoid leg crossing. Finally, the planner constructs the goal vector **_g_** _t_ in the stance-foot frame as described in Section IV: the stance foot reference is set to zero position offset and identity orientation quaternion, while the swing foot reference is the one computed by the planner. Conversely, for the velocity-tracking baseline _π_ VT, a P-controller converts the body-frame planar position error into linear velocity commands (scaled to respect limits), while a separate clipped P-controller generates the yaw rate _ωz_ to align the heading with the goal. The maximum velocity of the VT baseline is clamped to the trained range comparable to the FT policy. The maximum velocity _v_ max is computed by the maximum step distance _d_ max and gait frequency _f_ gait, i.e., _v_ max “ _d_ max{ _f_ gait. We swept the P-gain to choose the best performing one. 

**Narrow Bridge Traversal.** This task comprises an initial platform, a central narrow bridge, and a final goal platform. While the _approach_ and _run-out_ sections utilize the previously described goal-reaching planner, the bridge traversal requires a modified planner for lateral walking. The path is defined by a set of ordered waypoints _P_ “ t **_p_** _i_ u<sup>_N_</sup> _i_ “<sup>´</sup> 0<sup>1,trackedviaaprogressindex</sup><sup>_i_.</sup> To traverse the bridge, the agent adopts a lateral gait strategy. Consequently, the planner sets the target yaw perpendicular to the local path segment p **_p_** _i_ ´1 Ñ **_p_** _i_ q, subject to clipping for meeting yaw constraints. Simultaneously, the foothold position is projected onto the segment connecting **_p_** _i_ ´1 and **_p_** _i_ , ensuring strict alignment with the bridge centerline. 

**Cluttered Environment Traversal.** In this task, the robot is task with reaching a goal position while avoiding obstacles populating the navigation environment. To generate collision-free foothold targets, we employ a search-based footstep planner [13]. The planner operates on a discretized lattice of stance-foot poses **_s_** “ p _x, y, θ_ q, expanding states via alternating support and relative step actions **_a_** “ p∆ _x,_ ∆ _y,_ ∆ _θ_ q. The transition model utilizes a finite action set _A_ defined by discrete parameters: ∆ _x_ P t0 _._ 0 _,_ 0 _._ 10 _,_ 0 _._ 20u m, ∆ _y_ P t0 _._ 20 _,_ 0 _._ 25 _,_ 0 _._ 30 _,_ 0 _._ 35u m, and ∆ _θ_ P t0 _,_ ˘10<sup>˝</sup> _,_ ˘20<sup>˝</sup> _,_ ˘30<sup>˝</sup> u. Given a stance pose **_s_** and an action **_a_** P _A_ , a successor state **_s_**<sup>1</sup> “ _t_ p **_s_** _,_ **_a_** q is generated and snapped to the lattice resolution for hashing. Candidate transitions are filtered by feasibility constraints, including step-length bounds and a minimum inter-foot lateral spacing under alternating support. Furthermore, collision checking discards successors where the foot geometry overlaps with environmental obstacles. Node expansion is prioritized using a Euclidean distance heuristic _h_ p **_s_** q “ } **_p_** _b_ ´ **_p_** _g_ }2, estimating the cost to the goal **_p_** _g_ . The search algorithm minimizes a weighted evaluation function _f_ p **_s_** q “ _g_ p **_s_** q ` _w h_ p **_s_** q, where _g_ p **_s_** q represents the accumulated path cost from the start node (with weight _w_ “ 5). Finally, the computed foothold sequence is encoded into the goal observation **_g_** _t_ for the policy, as detailed in Section IV. 

**Stairs Traversal.** To evaluate the policy on the stairs climbing task, we implemented a deterministic high-level planner that supplies foothold targets. The obstacle geometry is parameterized by the _step length_ , defining the stairs’ steps depth; the _step height_ , defining the stairs’ steps height; the _platform length_ , specifying the flat landing separating the ascending and descending sections; and the _feet width_ , determining the lateral spacing between the left and right foot trajectories. Additionally, we define a set of _approaching steps_ on flat terrain before and after the staircase to stabilize the gait. Based on these dimensions, the planner pre-computes two distinct, parallel sequences of 3D foothold coordinates, _Pl_ “ t<sup>_w_</sup> _l_<sup>**_p_**</sup><sup>_i_u</sup><sup>_N_</sup> _i_ “<sup>´</sup> 0<sup>1</sup> and _Pr_ “ t<sup>_w_</sup> _r_<sup>**_p_**</sup><sup>_i_u</sup><sup>_N_</sup> _i_ “<sup>´</sup> 0<sup>1,for</sup> the left and right feet respectively. The sequence follows the fixed topology enforced by the obstacle’s terrain profile: an initial flat approach, an ascending staircase, a central landing platform, a descending staircase, and a final flat run-out. During 

execution, the robot tracks its progress using two indices, _il_ and _ir_ , pointing to the current target in _Pl_ and _Pr_ . The starting swing foot is selected based on the robot’s initial yaw orientation. At each gait phase switch (swing Ñ stance), the indices are updated to enforce an alternating gait: if the right foot is becoming the swing foot, its target index advances as _ir_ Ð _il_ ` 1; conversely, if the left foot swings, _il_ Ð _ir_ ` 1. Finally, the planner outputs the goal **_g_** _t_ in the _stance-foot frame_ , as described in Section IV. Specifically, the reference for the incoming stance foot is set to a zero position and identity orientation offset, while the reference for the incoming swing foot is computed as the relative transformation between the current stance foot and the target foothold retrieved from the plan. 

**Real-World Vision-Based Planner.** As mentioned in Section VI, the hardware experiments on the Booster T1 humanoid rely on a high-level planner driven by a computer vision module exploiting the onboard camera. The task involves navigating a corridor by stepping onto manually placed circular markers. We employ the onboard color camera, a RealSense D455, to detect these targets. Specifically, at each gait switch instant, the planner fuses RGB detection with depth measurements to extract the next foothold position in the camera frame. Using the robot’s kinematics, this target is transformed into the current stance-foot frame to compute the relative position offsets required by the policy as detailed in Section IV (keeping the stance foot offsets at zero). Orientation targets are determined heuristically to ensure kinematic feasibility. Finally, as already described in Section VI, to account for real-world latencies and imperfect ground contacts, we do not adhere strictly to the open-loop gait clock. Instead, the gait signal is frozen (repeating the last value) until the relative vertical distance between the stance and swing feet falls below a safety threshold, ensuring robust ground contact before transitioning. 

## _I. Section V’s Extended Tables_ 

Here, we report extended tables for the experiments conducted in Section V. Specifically, we include results for the straight and spiral staircase traversal experiments. 

|**Step**<br>**Length**|||||**Step He**|**ight (m)**|||||
|---|---|---|---|---|---|---|---|---|---|---|
|**(m)**|**0.01**|**0.02**|**0.04**|**0.08**|**0.10**|**0.11**|**0.115**|**0.12**|**0.125**|**0.13**|
||100%|100%|100%|95%|76%|60%|52%|56%|38%|12%|
|**0.300**|R:0 B:0<br>0.033˘0.006|R:0 B:0<br>0.034˘0.003|R:0 B:0<br>0.036˘0.005|R:3 B:2<br>0.059˘0.089|R:19 B:5<br>0.071˘0.049|R:40 B:0<br>0.081˘0.048|R:34 B:14<br>0.090˘0.048|R:39 B:5<br>0.083˘0.041|R:47 B:15<br>0.095˘0.038|R:70 B:18<br>0.108˘0.039|
|**0.325**|100%<br>R:0 B:0<br>0.034˘0.004|100%<br>R:0 B:0<br>0.034˘0.005|100%<br>R:0 B:0<br>0.036˘0.003|100%<br>R:0 B:0<br>0.038˘0.005|100%<br>R:0 B:0<br>0.041˘0.006|92%<br>R:5 B:3<br>0.050˘0.029|89%<br>R:11 B:0<br>0.053˘0.027|74%<br>R:22 B:4<br>0.068˘0.042|30%<br>R:54 B:16<br>0.104˘0.045|6%<br>R:80 B:14<br>0.115˘0.038|
||100%|100%|100%|100%|99%|100%|96%|89%|47%|19%|
|**0.350**|R:0 B:0<br>0.039˘0.010|R:0 B:0<br>0.038˘0.011|R:0 B:0<br>0.041˘0.018|R:0 B:0<br>0.040˘0.005|R:1 B:0<br>0.045˘0.022|R:0 B:0<br>0.045˘0.016|R:2 B:2<br>0.050˘0.022|R:7 B:4<br>0.066˘0.056|R:34 B:19<br>0.106˘0.060|R:58 B:23<br>0.136˘0.057|
||100%|100%|100%|100%|100%|99%|86%|88%|87%|46%|
|**0.375**|R:0 B:0<br>0.049˘0.012|R:0 B:0<br>0.052˘0.022|R:0 B:0<br>0.048˘0.010|R:0 B:0<br>0.048˘0.011|R:0 B:0<br>0.052˘0.010|R:0 B:1<br>0.054˘0.017|R:4 B:10<br>0.058˘0.019|R:8 B:4<br>0.079˘0.100|R:6 B:7<br>0.087˘0.112|R:23 B:31<br>0.113˘0.086|


TABLE VII: **Traversing Straight Stairs.** Each cell reports success rate, riser-contact falls (R) and balance falls (B), and mean ˘ std 3D foot placement error (m). 100 evaluations with initial robot yaw sampled from _U_ p´ _π_ {6 _, π,_ 6q. 

|**Step**<br>**Length**|||||**Step He**|**ight (m)**|||||
|---|---|---|---|---|---|---|---|---|---|---|
|**(m)**|**0.01**|**0.02**|**0.04**|**0.08**|**0.10**|**0.11**|**0.115**|**0.12**|**0.125**|**0.13**|
|**0.300**|100%<br>R:0 B:0<br>0.057˘0.008|99%<br>R:0 B:1<br>0.053˘0.012|96%<br>R:4 B:0<br>0.049˘0.020|97%<br>R:2 B:1<br>0.045˘0.017|82%<br>R:17 B:1<br>0.061˘0.029|40%<br>R:40 B:20<br>0.082˘0.028|21%<br>R:61 B:18<br>0.104˘0.031|14%<br>R:71 B:15<br>0.114˘0.034|19%<br>R:73 B:8<br>0.112˘0.030|14%<br>R:72 B:14<br>0.132˘0.053|
||98%|97%|97%|97%|91%|77%|58%|66%|29%|17%|
|**0.325**|R:0 B:2<br>0.066˘0.015|R:2 B:1<br>0.066˘0.020|R:3 B:0<br>0.061˘0.020|R:2 B:1<br>0.049˘0.044|R:3 B:6<br>0.060˘0.025|R:15 B:8<br>0.066˘0.035|R:20 B:22<br>0.085˘0.040|R:31 B:3<br>0.082˘0.050|R:59 B:12<br>0.097˘0.038|R:62 B:21<br>0.104˘0.031|
||94%|97%|97%|96%|94%|91%|84%|79%|57%|28%|
|**0.350**|R:2 B:4<br>0.079˘0.039|R:1 B:2<br>0.082˘0.030|R:1 B:2<br>0.080˘0.029|R:0 B:4<br>0.061˘0.068|R:4 B:2<br>0.065˘0.088|R:3 B:6<br>0.074˘0.098|R:8 B:8<br>0.084˘0.095|R:13 B:8<br>0.093˘0.107|R:25 B:18<br>0.097˘0.059|R:55 B:17<br>0.132˘0.061|
||96%|97%|98%|91%|90%|96%|93%|74%|54%|17%|
|**0.375**|R:1 B:3<br>0.092˘0.044|R:2 B:1<br>0.095˘0.051|R:1 B:1<br>0.099˘0.026|R:4 B:5<br>0.081˘0.038|R:4 B:6<br>0.090˘0.137|R:1 B:3<br>0.069˘0.048|R:1 B:6<br>0.089˘0.126|R:7 B:19<br>0.097˘0.067|R:16 B:30<br>0.125˘0.107|R:45 B:37<br>0.155˘0.097|


TABLE VIII: **Traversing Spiral Stairs.** Each cell reports success rate, riser-contact falls (R) and balance falls (B), and mean ˘ std 3D foot placement error (m). 100 evaluations with initial robot yaw sampled from _U_ p´ _π_ {6 _, π,_ 6q. 

