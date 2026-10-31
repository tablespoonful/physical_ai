---
title: "REFINE-DP: Diffusion Policy Fine-tuning for Humanoid Loco-manipulation via Reinforcement Learning"
date: "2026-03-14"
authors: "Zhaoyuan Gu; Yipu Chen; Zimeng Chai; Alfred Cueva; Thong Nguyen; Yifan Wu"
url: https://arxiv.org/abs/2603.13707
pdf: https://arxiv.org/pdf/2603.13707
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.13707)** / [論文ページ](https://arxiv.org/abs/2603.13707)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED JULY, 2026 

1 

# REFINE-DP: Diffusion Policy Fine-tuning for Humanoid Loco-manipulation via Reinforcement Learning 

Zhaoyuan Gu*, Yipu Chen*, Zimeng Chai*, Alfred Cueva, Thong Nguyen<sup>_†_</sup> , Yifan Wu<sup>_†_</sup> , Huishu Xue<sup>_†_</sup> , Minji Kim, Isaac Legene, Fukang Liu, KyoungMok Kim, Ayan Barula, Yongxin Chen, Ye Zhao 

**_Abstract_ —Humanoid loco-manipulation requires coordinated task-space motion planning with stable loco-manipulation command tracking under complex robot-environment dynamics and long-horizon tasks. While diffusion policies (DPs) show promise for learning from demonstrations, deploying them on humanoids poses critical challenges: the motion planner trained offline is decoupled from the loco-manipulation controller, leading to poor command tracking, compounding distribution shift, and task failures. The common approach of scaling demonstration data is prohibitively expensive for high-dimensional humanoid systems. To address this challenge, we present REFINE-DP (REinforcement learning FINE-tuning of Diffusion Policy), a hierarchical framework that jointly optimizes a DP motion planner and an RL-based loco-manipulation controller. The DP is fine-tuned via a PPO-based diffusion policy gradient to improve task success rate, while the controller is simultaneously updated to accurately track the planner’s evolving command distribution, reducing the distributional mismatch that degrades motion quality. We validate REFINE-DP on a humanoid robot performing locomanipulation tasks, including door traversal and long-horizon object transport. REFINE-DP achieves an over** 90% **success rate in simulation, even in out-of-distribution cases not seen in the pre-training data, and enables real-world execution without privileged state information. Our proposed method substantially outperforms pre-trained DP baselines and demonstrates that RL fine-tuning is key to reliable humanoid loco-manipulation. https://refine-dp.github.io/REFINE-DP/** 

**_Index Terms_ —Diffusion Policy, Fine-tuning, Joint Optimization, Humanoid Robot, Locomotion and Manipulation.** 

## I. INTRODUCTION 

**H** UMANOIDphysical behaviors,robots areyet increasinglythey still lackcapablethe task-levelin their autonomy required to perform human-like tasks, such as coordinating locomotion and manipulation for door traversal. Recent studies have demonstrated agile whole-body control with both model-based methods [1], [2] and learning-based motion imitation [3], [4]. Despite these advances, existing 

Manuscript received: March 1, 2026; Revised: May 31, 2026; Accepted: July 1, 2026. 

This paper was recommended for publication by Editor Olivier Stasse upon evaluation of the Associate Editor and Reviewers’ comments. 

This work was supported in part by the Office of Naval Research (ONR) under Grant N000142312223, in part by the National Science Foundation (NSF) under Grant CMMI-2144309, Grant 2328254, and Grant 2409016, and in part by the United States Department of Agriculture (USDA) under Grant 2022-11065. 

The authors are with the Institute for Robotics and Intelligent Machines, Georgia Institute of Technology, Atlanta, GA 30332 USA (e-mail: _{_ zgu78, yezhao _}_ @gatech.edu). (*<sup>_†_</sup> equally contributed) 

Digital Object Identifier (DOI): see top of this page. 

approaches often struggle to operate autonomously in dynamic environments, with reliable execution still depending significantly on human supervision or heuristic planning. To perform physical tasks reliably, humanoid robots must interact with the physical world through contact, such as manipulating objects and exerting force on the environment, where modeling errors and contact uncertainties frequently lead to task failure. These challenges require real-time adaptation beyond motion tracking control. 

To address these challenges, recent work has explored learning task-level action generation directly from demonstrations, enabling robots to acquire task-level autonomy beyond predefined control policies. For instance, recent advances in diffusion policies (DPs) [5] have introduced a promising behavior cloning (BC) approach for learning action-generative models from expert demonstrations. These models are effective at capturing complex and multimodal expert behaviors. However, their success often relies on offline datasets, which can lead to poor out-of-distribution robustness due to distribution shift and compounding errors. To mitigate this issue, DPs are typically trained on large datasets that require highcapacity models, such as transformers, to improve coverage and generalization. However, for high-dimensional humanoid systems, this scaling strategy incurs prohibitive costs in both data collection and policy training computation, while still failing to achieve robust performance in loco-manipulation, where long horizons, high dimensionality, and compounding execution errors exacerbate distribution mismatch. 

Rather than scaling data, this paper addresses the distribution-shift issue through reinforcement learning finetuning (RLFT) [6], [7], enabling adaptation beyond offline pretraining. Specifically, we fine-tune a DP by exploring interactions in a simulator and collecting trials to directly update the DP via policy gradient [6]. By exploring unseen state–action pairs, RLFT significantly increases the task success rate with only a sparse reward. Additionally, we demonstrate that RLFT enables a pre-trained DP on a small dataset to outperform those trained on substantially larger offline datasets. 

Deploying DP on a humanoid robot remains a challenge due to the complexity of whole-body control. To simplify the DP action space, we adopt a hierarchical framework with explicit roles for each layer. The DP serves as a motion planner that generates Cartesian action chunks, including base velocity and _SE_ (3) hand-pose trajectories. RL-based loco-manipulation controllers consume these action chunks and convert them 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED JULY, 2026 

2 


Fig. 1: Our pipeline consists of three stages: (a) Data Collection, where expert demonstrations are collected in a source environment using a frozen RL-based loco-manipulation controller; (b) Pre-training, where a diffusion policy (DP) motion planner is trained with the expert dataset containing human-demonstrated skills; and (c) Joint Optimization, where the pretrained DP is jointly fine-tuned with the loco-manipulation controller in a target environment. During deployment, the DP generates Cartesian action chunks, and the loco-manipulation controller converts them into joint-position references for tracking. 

into joint-position references while maintaining locomotion stability and manipulation accuracy. This hierarchical framework keeps the DP command space compact and intuitive while delegating the complexity of whole-body control to the dedicated loco-manipulation controller. An illustration of the proposed hierarchical framework is in Fig. 1. 

Based on this hierarchical framework, we introduce REFINE-DP ( **RE** inforcement learning **FINE** -tuning of **D** iffusion **P** olicy), a novel fine-tuning approach that jointly optimizes both the DP motion planner and the RL-based loco-manipulation controller. During joint optimization, the parameters of both the DP and the loco-manipulation controller are updated. This joint optimization maintains distributional consistency between the planner’s outputs and the controller’s inputs, resulting in improved commandtracking performance and higher task success rates. 

In summary, our main contributions are as follows: 

- We design a hierarchical humanoid loco-manipulation framework in which a DP serves as the motion planner and an RL policy acts as the loco-manipulation controller. Instead of operating directly in full-body configuration spaces, our DP outputs low-dimensional Cartesian action chunks (i.e., base velocities and _SE_ (3) hand-pose trajectories) tailored to humanoid loco-manipulation. These action chunks substantially simplify the DP action space, and can be easily teleoperated by human operators and converted by the RL policy into joint-position references. 

- We introduce a joint fine-tuning scheme that simultaneously optimizes a DP motion planner and an RL loco-manipulation controller. This is in contrast to prior RLFT schemes that update a single policy. We show that this joint optimization improves both task success rate and motion-tracking accuracy compared to fine-tuning either component alone. 

- We validate our framework on the T1 humanoid robot, enabling loco-manipulation across a range of tasks, including walking and door opening, long-horizon box transport, and stepping onto an elevated platform to retrieve an object. We further demonstrate the whole pipeline using only onboard 

RGB information for object pose estimation. 

## II. RELATED WORKS 

_A. Sim-to-Real RL for Humanoid Loco-manipulation Control_ 

Loco-manipulation skills involve simultaneous locomotion and manipulation, posing a high-dimensional control problem for humanoid robots [8]. Prior work has addressed this challenge using sim-to-real reinforcement learning (RL), such as for whole-body control frameworks [9], while other approaches decompose the problem into upper- and lower-body controllers [10], [11]. Many of these RL methods [3], [4], [9], [12] support teleoperation, enabling demonstration data collection for training a motion planner. 

Among those RL methods, the first category is learning from scratch, where the desired behavior is specified through a complex reward function. However, learning locomanipulation without demonstrations is challenging due to the high dimensionality of humanoid systems and the diversity and compositional complexity of loco-manipulation tasks. Several studies have demonstrated successful sim-to-real transfer for autonomous object manipulation [13]–[16]. These policies are typically tuned for each specific task, making it difficult to acquire long-horizon, autonomous loco-manipulation skills. 

The second category uses RL for motion tracking of reference, such as a manually designed trajectory [17], [18] or human data [3], [4], [19]. While this paradigm has achieved versatile motion tracking capability, it fundamentally relies on externally provided references and therefore lacks the task- and environment-level awareness required for true autonomy [3]. 

In this paper, our loco-manipulation controller falls in the second category. It can walk and manipulate objects with desired base-velocity and hand-pose commands. Compared with other whole-body controllers with latent vector inputs [11] or whole-body joint-angle references [9], our control policy’s input space is more physically interpretable and enables more intuitive task-level control, either through VR teleoperation or a motion planner. 

GU _et al._ : REFINE-DP: DIFFUSION POLICY FINE-TUNING FOR HUMANOID LOCO-MANIPULATION VIA REINFORCEMENT LEARNING 

3 

## _B. Autonomous Humanoid Loco-Manipulation_ 

To achieve autonomous task execution on humanoid robots, many studies adopt modern behavior cloning (BC) techniques, such as diffusion policy (DP) [5] or action-chunking transformer [20], to learn contact-rich manipulation directly from multi-modal demonstration data. However, while most autonomous policies focus on relatively stable manipulator platforms, extending these approaches to autonomous humanoid loco-manipulation remains challenging due to underactuated and unstable dynamics, and the need to coordinate whole-body motion over long horizons. 

Among the few prior works on autonomous humanoid loco-manipulation, some approaches adopt hierarchical frameworks that decouple motion planning from loco-manipulation command tracking, thereby keeping the action space simple and interpretable. For example, [4], [9], [21] employ a planner–controller hierarchy to structure decision making and execution. Other approaches maintain a unified end-toend policy but rely on large-scale domain randomization to integrate perception and improve sim-to-real robustness, as demonstrated in recent work on humanoid door opening [16], [22]. Our REFINE-DP’s hierarchical framework falls into the first category, with a motion planner offering the advantage of learning a diverse range of tasks. Instead of freezing the control policy during the optimization of a planner policy [23], we jointly optimize both policies to simultaneously achieve better task success rate and tracking performance. 

## _C. Fine-tuning Pre-trained Imitation Learning Policy_ 

To address the inherent issue of compounding error and domain shift in DP, several works have explored integrating RL with DP by learning a residual policy on top of a pre-trained DP to refine actions and enhance performance. These residual policies provide corrective compensations for imitation errors. Existing works have explored on-policy RL [24], [25] and off-policy RL [26] for learning residual refinement to improve precision and sample efficiency. 

Another line of work focuses on fine-tuning diffusion policies with RL. In Diffusion Policy Policy Optimization (DPPO) [6], the authors adapt Proximal Policy Optimization (PPO) [27] and fine-tune a pre-trained diffusion policy for a higher success rate. Another work [28] proposes two algorithms, Diffusion Policy Mirror Descent (DPMD) and Soft Diffusion Actor Critic (SDAC), for online training of diffusion policies from scratch. Both of these methods update the diffusion policies directly. More broadly, _πRL_ [29] adopts RL for fine-tuning vision-language-action models. While prior work optimizes only the planner, few works jointly optimize a diffusion-based motion planner and a loco-manipulation controller within a unified planning and control framework. 

## III. METHODS 

Our pipeline consists of three stages, as illustrated in Fig. 1. It first collects expert loco-manipulation demonstrations, then pre-trains a diffusion policy (DP), which is subsequently finetuned to enhance the task success rate and motion quality. 

**Collecting loco-manipulation data.** Expert demonstrations are collected by teleoperating the robot or by rolling out a heuristic planner in IsaacLab [30]. During the teleoperation, the operator gives commands via a VR device to a pre-trained loco-manipulation policy _π_ loco <u>manip</u><sup>,asdetailedinSec.III-A.</sup> In addition to teleoperation, we leverage heuristic planners to scale up data collection. During data collection, a humanoid robot executes diverse loco-manipulation skills, such as object transportation and door opening. 

**Pre-training the diffusion policy:** For each task, we pretrain a DP _π_ ¯ _θ_ using the collected dataset. The pre-trained DP outputs base velocity and hand pose commands, which are passed to the _π_ loco <u>manip</u><sup>forexecution.</sup> 

**Fine-tuning in target environments:** The pre-trained DP is fine-tuned in the simulator for the same or a more challenging target environment. We adopt two fine-tuning settings: (i) Only the diffusion policy parameters are updated, while the control policy _π_ loco <u>manip</u><sup>remains frozen as a loco-manipulation</sup> controller; (ii) Jointly optimize both the _π_ ¯ _θ_ and _π_ loco <u>manip</u><sup>.</sup> Fine-tuning the DP adapts it to domain-specific dynamics beyond the offline expert data, substantially improving its success rate. Joint optimization further yields better motion quality, namely, more tracking accuracy and less motion jitter. 

## _A. Training Loco-manipulation Controller for Data Collection_ 

We develop a reinforcement learning (RL) policy _π_ loco <u>manip</u> capable of simultaneous locomotion and manipulation. The training and deployment pipeline is illustrated in Fig. 2. _π_ loco <u>manip</u><sup>adoptsadecoupledcontrolarchitecturethatsep-</sup> arates upper-body and lower-body behaviors, similar to prior humanoid loco-manipulation works [10]–[12]. Specifically, a lower-body locomotion policy is responsible for achieving intermediate foot placements while maintaining dynamic balance, whereas an upper-body arm policy tracks desired hand poses to execute manipulation tasks. During training, the two controllers are decoupled, handling disturbances from each other through domain randomization. 

While most existing locomotion policies are formulated as velocity-tracking controllers, their objectives are designed for long-distance periodic walking rather than for the frequent start–stop transitions and precise torso position adjustments required for manipulation tasks. To enable accurate locomotion toward target positions and achieve a high loco-manipulation success rate, we introduce a foot-placement tracking controller _π_ lower that takes discrete foot-placement commands as input. Unlike velocity-tracking controllers that can accumulate positional error over time, our locomotion policy provides direct control over where each footstep lands. Prior studies [31], [32] have demonstrated that this formulation yields substantially improved foot-placement accuracy and locomotion stability. 

We train _π_ lower using RL motion imitation [33] on lowerbody reference trajectories [18]. The policy _π_ lower( **a**<sup>lower</sup> _t |_ **s**<sup>lower</sup> _t ,_ **g** _t_<sup>lower</sup> ) is conditioned on a foot-placement command **g** _t_<sup>lower</sup> , which consists of a swing-foot indicator, a countdown, and a relative target swing-foot pose in the stance-foot frame. The proprioceptive observation **s**<sup>lower</sup> _t_ includes the joint states, the gravity vector, and the previous action. The reward function combines foot tracking terms with regularization terms 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED JULY, 2026 

4 


Fig. 2: The sim-to-real RL of the loco-manipulation control policy, from motion prior generation to deployment. 

to ensure accuracy and stability. Additionally, we address disturbances from upper-body movement by training with randomized arm configurations. 

The upper-body policy _π_ upper( **a** _t_<sup>upper</sup> _|_ **s**<sup>upper</sup> _t ,_ **g** _t_<sup>upper</sup> ) tracks the hand-pose command **g** _t_<sup>upper</sup> , which specifies _SE_ (3) targets for the left and right hands in the robot’s root frame. We generate a set of feasible hand commands via sampling collision-free joint configurations and solving forward kinematics. The proprioceptive observation **s**<sup>upper</sup> _t_ includes arm joint states, current hand poses, and tracking errors. To improve robustness to payload and external forces arising from object interaction and lower-body motion, we apply domain randomization during the training of _π_ upper. 

Both _π_ lower and _π_ upper output joint position commands **a** _t_ = [ **a**<sup>lower</sup> _t_ ; **a**<sup>upper</sup> _t_ ], where **a**<sup>lower</sup> _t ∈_ R<sup>12</sup> corresponds to the leg joints and **a**<sup>upper</sup> _t ∈_ R<sup>14</sup> corresponds to the arm joints. These commands specify joint position offsets relative to a fixed default configuration **q** def . The combined loco-manipulation policy is _π_ loco <u>manip</u><sup>(</sup><sup>**a**</sup> _t |_ **s** _t,_ **g** _t_ ), where **s** _t_ = [ **s**<sup>lower</sup> _t_ ; **s**<sup>upper</sup> _t_ ] is the proprioceptive observation and **g** _t_ = [ **g** _t_<sup>lower</sup> ; **g** _t_<sup>upper</sup> ] is the loco-manipulation command. The resulting target joint positions, **q** target = **q** def + **a** _t_ , are tracked by proportional-derivative (PD) control. Detailed observations and rewards are on our website. 

The primary methods for data collection include teleoperation and the rollout of heuristic planners, both leveraging _π_ loco <u>manip</u><sup>for loco-manipulation in a simulator. These heuristic</sup> planners are designed for each task via stage-conditioned behavior transitions, whose intermediate waypoints are parameterized based on observed object poses. Teleoperation and heuristic rollouts play complementary roles: teleoperation captures recovery behaviors but is costly and low-throughput because humanoid loco-manipulation requires whole-body coordination, whereas heuristic planners scale data collection at the cost of behavioral novelty. Considering this tradeoff, we augment 50 teleoperated trajectories with heuristic planner rollouts, expanding the dataset to 1000 trajectories; the teleoperated trajectories define the core behavioral modes, including recovery responses, and heuristic rollouts augment coverage. To ensure broad coverage of scenarios, we randomize both the initial object configurations and the robot’s initial states during data collection; additional data diversity arises from locomotion drifting, which randomizes torso pose and manipulation timing. We collect only successful trajectories, each containing state-action pairs. The observed states include the robot’s hand and foot poses in the body frame, the gripper 

state, and object information. The action specifies the desired hand poses, gripper state, and a base-velocity command. We use a velocity-to-footstep planner to convert the velocity command into a sequence of footstep commands. 

Another choice of command interface is a pair of global hand poses. Although they are low-dimensional, they underspecify whole-body motion in a kinematically redundant humanoid and can yield undesirable torso configurations [34]. Our interface instead combines hand-pose commands with a lower-body command, similar to OmniH2O and SONIC [3], [35]; this disambiguates locomotion from hand pose tracking and preserves explicit foothold control on rough terrain. 

## _B. Diffusion Policy Pre-training_ 

The collected loco-manipulation data is used to pre-train a DP [5]. Formally, a DP models a conditional action distribution _pθ_ ( **A**<sup>0:</sup> _t_<sup>_K_</sup> _|_ **S** _t_ ) = _p_ ( **A**<sup>_K_</sup> _t_<sup>) �</sup><sup>_K_</sup> _k_ =1<sup>_pθ_(</sup><sup>**A**</sup> _t_<sup>_k−_1</sup> _|_ **A**<sup>_k_</sup> _t_<sup>_,_</sup><sup>**S**</sup><sup>_t_), where</sup><sup>**A**</sup><sup>_k_</sup> _t_ represents an action chunk, and **S** _t_ represents a state observation chunk [20]. The superscript _k_ is the denoising timestep, _K_ is the total number of denoising steps, and the subscript _t_ is the environment timestep. Given the dataset _D_ = _{_ ( **S** _i,_ **A**<sup>0</sup> _i_<sup>)</sup><sup>_}N_</sup> _i_ =1<sup>,</sup> we maximize the approximate log likelihood, which can be reformulated as training a noise prediction network _ϵθ_ by minimizing the noise prediction error [36]: 


where _ϵ ∼N_ (0 _,_ **I** ) is the target noise, and **A**<sup>_k_</sup> _t_ is **A**<sup>0</sup> _t_ corrupted by _ϵ_ through a forward diffusion process. The action generation involves a reverse denoising process. 

## _C. Diffusion Policy Fine-tuning_ 

While using the DP as a motion planner achieves a decent success rate, its performance remains insufficient for reliable task execution. In particular, the pre-trained planner does not explicitly account for the robot’s closed-loop dynamics and execution errors, resulting in deviations that accumulate over long horizons and occasional task failure. This compounding error in pre-training motivates us to further enhance the policy. In this study, we employ RL to fine-tune the pretrained DP. RL fine-tuning offers two key advantages: (i) improving task success through trial-and-error interaction with the simulation environment, and (ii) enhancing robustness to out-of-distribution conditions through domain randomization, enabling zero-shot sim-to-real transfer. 

Conventional policy gradient methods such as Proximal Policy Optimization (PPO) [27] rely on evaluating a policy density function _π_ ¯ _θ_ ( **A**<sup>0</sup> _t_<sup>_|_</sup><sup>**S**</sup><sup>_t_).However,DPsareimplicitpoli-</sup> cies, for which _π_ ¯ _θ_ ( **A**<sup>0</sup> _t_<sup>_|_</sup><sup>**S**</sup><sup>_t_) is not tractable. To address this, we</sup> adopt Diffusion Policy Policy Optimization (DPPO) [6] that augments an environment Markov Decision Process (MDP) by incorporating the denoising process into the MDP and treating each denoising step as a decision step. Since denoising transitions follow a tractable Gaussian distribution, this augmented MDP enables a likelihood-based policy gradient method, such as PPO [27], allowing RL fine-tuning of DP. 

Formally, we define the environment MDP as _M_ ENV := ( _S, A, P_ 0 _, P, R_ ), where _S_ is the state space, _A_ is the action 

5 

GU _et al._ : REFINE-DP: DIFFUSION POLICY FINE-TUNING FOR HUMANOID LOCO-MANIPULATION VIA REINFORCEMENT LEARNING 

space, _P_ 0 is the initial state distribution, _P_ is the transition probabilities, and _R_ is the reward function. We then define a diffusion-process-augmented MDP _M_ DP := ( _S_<sup>¯</sup> _, A_<sup>¯</sup> _, P_<sup>¯</sup> 0 _, P,_<sup>¯</sup> _R_<sup>¯</sup> ), which expands _M_ ENV by inserting one full denoising process in each environment timestep. This augmented _M_ DP defines a unified timestep index _t_<sup>¯</sup> ( _t, k_ ) = _tK_ +( _K −_ 1 _− k_ ), where _K_ is the total number of denoising steps and _k ∈_ [0 _, . . . , K −_ 1]. Accordingly, the augmented MDP is given by 


where **_δ_** is the Dirac distribution. We refer the readers to [6] for detailed derivation. 

We use generalized advantage estimation (GAE) [37] to calculate the advantage estimate _A_<sup>ˆ</sup> (¯ _st_ ¯ _,_ ¯ _at_ ¯) from a replay buffer and optimize the DP using a PPO-style policy gradient. 

## _D. Joint Optimization of the Diffusion and the RL Policies_ 

To improve the motion quality beyond the success rate, we propose a joint optimization technique that fine-tunes both the DP motion planner and the RL-based loco-manipulation controller. Unlike the fine-tuning described in Sec. III-C that optimizes only the DP, we additionally optimize the locomanipulation control policy. 

As shown in Fig. 1(c), the augmented environment _M_ DP produces two sets of states (¯ _st,_ **s** _t_ ) and rewards ( _R_<sup>¯</sup> _t, R_<sup>ˆ</sup> _t_ ). _R_<sup>¯</sup> _t_ is used to update the DP _π_ ¯ _θ_ (¯ _at | s_ ¯ _t_ ) and enhance task success rate. _R_<sup>ˆ</sup> _t_ represents a set of rewards used in pre-training the loco-manipulation control policy _π_ loco <u>manip</u><sup>,anditspurposeis</sup> to further improve motion quality and enable accurate and smooth tracking of the DP commands. Both the DPs and the RL control policy are optimized using PPO. A detailed description of the algorithm is in Alg. 1. 

Joint optimization enables the tracking controller to accurately follow dynamic, task-relevant commands generated by the DP planner. Unlike the independently sampled, stationary commands used during controller pre-training, DP commands represent a moving target along a continuous trajectory, creating a distribution mismatch that degrades tracking performance. Joint optimization alleviates this mismatch by exposing the controller to planner-generated commands, bringing them in-distribution and substantially improving tracking accuracy. Combined with the optimization of DP, this process enhances motion quality and achieves a high success rate. 

## IV. EXPERIMENTS 

## _A. Experiment Setup_ 

We use IsaacLab [30] for expert demonstration collection, RL policy training, and fine-tuning. All policies are trained on 

## **Algorithm 1** REFINE-DP: Joint Optimization of DP and RL 

**Input:** Pre-trained diffusion policy _π_ ¯ _θ_ ( **A**<sup>0</sup> _t_<sup>_|_</sup><sup>**S**</sup><sup>_t_),</sup> locomanipulation policy _π_ loco <u>manip</u><sup>,augmentedMDP</sup><sup>_M_</sup> DP<sup>.</sup> Initialize state _s_ ¯ _t_ from _M_ DP. **for** _iter_ = 0 **to** _L_ **do** Rollout to collect replay buffer _D_ . **for** _iter_ = 0 **to** _M_ **do** Sample a mini-batch _Dk_ from _D_ . Update _π_ loco <u>manip</u><sup>using</sup><sup>_D_</sup> _k_<sup>viaPPO[27].</sup> **end for** Rollout to collect replay buffer _D_<sup>¯</sup> . **for** _iter_ = 0 **to** _N_ **do** Sample a mini-batch _D_<sup>¯</sup> _k_ from _D_<sup>¯</sup> . Update _π_ ¯ _θ_ ( **A**<sup>0</sup> _t_<sup>_|_</sup><sup>**S**</sup><sup>_t_)using</sup><sup>_D_¯</sup><sup>_k_viaDPPO.</sup> **end for end for** 

an NVIDIA H200 GPU. RL pre-training of _π_ loco <u>manip</u><sup>takes</sup> 10h with 4096 parallel environments, while DP pre-training on a 100-trajectory dataset (3h of demonstrations) requires 18h. The pipeline from pre-training to the fully fine-tuned policy requires 22h of wall-clock time. Joint optimization (Alg. 1) takes _L_ = 2 iterations, each costing 9h, split equally between updating _π_ loco <u>manip</u><sup>and</sup><sup>_π_¯</sup> _θ_<sup>.</sup> 

Regarding policy configuration, the DP _π_ ¯ _θ_ has an observation horizon of 8 and an action chunk size of 12, with a 0 _._ 1 s interval between each observation and action. We choose _α_ ¯ _k_ to follow the cosine schedule [38] for DP pre-training. 

For hardware experiments, we use a Booster T1 robot with 29 degrees of freedom. Both the DP motion planner _π_ ¯ _θ_ and the RL-based loco-manipulation controller _π_ loco <u>manip</u><sup>runona</sup> policy computer, with an AMD 7945HX CPU and an NVIDIA RTX 4060 GPU. The loco-manipulation policy _π_ loco <u>manip</u> runs at 50 Hz, while the DP _π_ ¯ _θ_ runs at 10 Hz using NVIDIA TensorRT. This policy computer receives the robot’s proprioceptive states (i.e., joint angles and IMU measurements) from T1’s embedded computer. The policy computer also performs the inference of _π_ ¯ _θ_ that outputs a Cartesian action chunk for the _π_ loco <u>manip</u><sup>, which then outputs upper- and lower-</sup> body joint-position references. We use a state-based DP that relies on the pre-processed pose of the target object relative to the robot torso, which is captured using either a motion capture (MoCap) system or an onboard RGB camera. The MoCap system streams object-state observations at 90 Hz. For the camera setting, a head-mounted Intel RealSense D435i provides video for 6-DoF fiducial-marker-based [39] objectpose estimation at 30 Hz, demonstrating the capability to operate without privileged state information. 

As shown in Fig. 3, we evaluate our REFINE-DP on a set of loco-manipulation tasks. Each of these tasks requires multiple stages of walking and manipulation. Unlike [40], which requires a stage signal, our DP policy infers task stages from object locations and implicitly learns stage transitions, enabling loco-manipulation without explicit stage supervision. 

**Task 1: Object pickup; Task 2: Long-horizon pick-andplace.** Task 1 requires walking to a table to pick up a box, whereas Task 2 is a longer-horizon extension (i.e., 40 s) with 

6 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED JULY, 2026 


Fig. 3: The robot autonomously executes loco-manipulation tasks: (a) door opening, (b) object transportation. 

placing the object on another table. 

**Task 3: Door opening and traversal.** For humanoid door-opening tasks, prior work relies on heuristic planners [41], sim-to-real RL [16], or action-chunking transformer (ACT) [40]. In contrast, we are the first to apply DP to humanoid door traversal. 

**Task 4: Stair-assisted object retrieval.** This locomanipulation task involves uneven terrain, where the humanoid must step onto an elevated platform to retrieve an object. 

## _B. Baseline Methods and Ablation Study_ 

We compare REFINE-DP with planner baselines spanning architectures and fine-tuning strategies: pre-trained DiT, LSTM, and deterministic MLP planners; RL-fine-tuned MLP (MLP-FT); and residual RL [24]. All use the same frozen loco-manipulation controller _π_ loco <u>manip</u><sup>.</sup> 

**DiT.** The DP baseline follows the standard formulation [5] using a transformer backbone. This evaluates the performance of a purely pre-trained DP within our hierarchical framework. **LSTM.** The LSTM baseline serves as a recurrent baseline to the transformer-based diffusion policy (DiT). 

**MLP** and **MLP-FT.** The MLP planner is a separate baseline under the same planner-controller interface, rather than a replacement module inside the learned denoising diffusion process. It directly regresses actions from observations and therefore produces deterministic action predictions. In contrast, the DiT-based diffusion planner samples action trajectories through a denoising diffusion process, which allows stochastic trajectory generation. MLP-FT retains the hierarchical interface: only the MLP planner is fine-tuned, while the deterministic low-level controller remains frozen. This matches DiTFT and isolates the contribution of the diffusion-based policy formulation from the fine-tuning procedure itself. Since PPOstyle fine-tuning relies on stochastic exploration, we convert the pre-trained deterministic MLP into a stochastic policy by interpreting its output as the mean action and sampling around it with an Ornstein Uhlenbeck (OU) process. Specifically, the OU process is a mean-reverting diffusion process, producing temporally correlated and smoothly varying perturbations that are suitable for continuous-control exploration: 


where **_µ_** ˜ _θ_ ( **S** _t_ ) denotes the MLP mean action prediction. The interpolation coefficient _λk_ pulls samples toward the mean policy, while **_σ_** ˜ _k_ controls the exploration magnitude. We adopt a linear schedule for _λk_ and a decreasing noise schedule for **_σ_** ˜ _k_ , encouraging exploration in early steps and concentration around the mean policy in later steps. Compared with the OU 


Fig. 4: Comparison of success rates across tasks in Sec. IV-A and methods in Sec. IV-B. 

process that injects noise to the planner, exploration using _π_ loco <u>manip</u><sup>’sstandarddeviationinsteadproducedexcessive</sup> joint-level noise, preventing task completion and yielding no success signal. 

**Residual RL.** Residual RL [24] improves a pre-trained DP by learning a lightweight corrective residual that is added to the output of the frozen DP. Rather than modifying the parameters of a pre-trained DP, a residual Gaussian policy is optimized with PPO to predict small additive adjustments to the frozen DP’s actions. 

## _C. Quantitative Results and Analysis_ 

## _C-1 Task Success and Planner Capacity_ 

**REFINE-DP improves task success rate (SR).** The task SR comparison with the baselines is reported in Fig. 4. The results show that REFINE-DP, including fine-tuning and joint optimization, substantially outperforms all baselines across all loco-manipulation tasks. REFINE-DP can achieve more than 90% by fine-tuning from the pre-trained policy of 50 _−_ 70%. Since the fine-tuned SR is already high, joint optimization does not further improve SR; instead, it improves motion quality. 

**Stochastic policy shows a superior SR.** We observe a consistent performance gain in the transformer-based diffusion (DiT) over the MLP-based diffusion in Fig. 4. We attribute this improvement to DiT’s ability to model multi-modal action distributions and generate diverse feasible trajectories. In contrast, MLPs perform deterministic regression and tend to average across demonstrations. When multiple valid solutions exist, this averaging effect can produce actions that may not correspond to a viable trajectory. 

MLP-FT partially mitigates this limitation by injecting stochasticity during fine-tuning, enabling exploration and recovery from averaged behaviors. Performance improves as the policy adapts to the target environment and reduces the distribution gap between offline demonstrations and online execution. However, the achievable improvement remains limited by the representational capacity of the backbone. These results 

GU _et al._ : REFINE-DP: DIFFUSION POLICY FINE-TUNING FOR HUMANOID LOCO-MANIPULATION VIA REINFORCEMENT LEARNING 

7 


Fig. 5: Joint optimization achieves better end-effector tracking performance and velocities across tasks in Sec. IV-A. 

highlight the importance of backbone capacity for multi-modal action modeling and the effectiveness of fine-tuning. 

LSTM can achieve comparable SR to DiT in the shorthorizon Task 1. However, it degrades sharply on long-horizon tasks, suggesting its recurrent state is insufficient to capture the action distribution. 

**Pure RL from sparse reward fails.** Successful fine-tuning requires a sufficiently capable pre-trained policy. We find that fine-tuning is effective when a pre-trained policy achieves a moderate success rate (approximately 50 _−_ 70%). In contrast, fine-tuning from random initialization (Pure RL) shows limited improvement, as sparse rewards rarely provide informative learning signals when task success is infrequent. Pre-training alleviates the need for extensive reward shaping typically required in pure RL from scratch [16]. This allows the policy to improve its SR with minimal manual tuning. 

## _C-2 Efficiency Gains from Fine-tuning and Joint Optimization_ 

**Joint optimization improves fine-tuning efficiency and motion quality.** Optimizing the loco-manipulation controller provides three benefits. First, optimizing the RL controller alone using pre-trained DP rollouts _D_ already improves the SR by 18% on the long-horizon pick-and-place task. Second, the jointly optimized loco-manipulation policy _π_ loc<sup>_′_</sup> <u>o manip</u> improves the training efficiency of DP fine-tuning, requiring approximately half as many iterations (20 instead of 40) to achieve a 90% SR compared to fine-tuning with the pretrained RL-based loco-manipulation policy _π_ loco <u>manip</u><sup>. Third,</sup> joint optimization improves motion quality in addition to a consistently high SR, as shown in Fig. 4. Specifically, we evaluate upper-body tracking performance using position and orientation errors, as well as motion smoothness using linear velocity, averaged across 100 trials. Collectively, _π_ loc<sup>_′_</sup> <u>o manip</u> achieves the lowest position error and reduces orientation error by up to 50% compared to the pre-trained _π_ loco <u>manip</u><sup>,as</sup> shown in Fig. 5. This strictly lower tracking error coincides with an average 15% decrease in end-effector velocity, reflecting smoother manipulation. Meanwhile, fine-tuning the DP alone can degrade controller tracking performance, as the fine-tuned DP learns to issue excessive commands that reduce tracking accuracy, exert large forces, and produce jerky motion at unexpected contact changes. 

**Fine-tuning improves data efficiency.** Fig. 6 compares the data scaling behavior with and without fine-tuning on both the box-pick-and-place and door-opening tasks. While the SR improves with more pre-training data, fine-tuning achieves higher performance with substantially fewer demonstrations. 

In particular, reaching a 90% SR through pre-training alone requires approximately 1 _,_ 000 trajectories. In contrast, a DP pre-trained on only 50 trajectories achieves up to 95% SR after fine-tuning. These results demonstrate that fine-tuning significantly reduces the need for expensive pre-training data while yielding a higher final SR. 

**Fine-tuning adapts to out-of-distribution (OOD) scenarios in pre-training.** To extend the pre-trained policy to OOD scenarios, we employ domain randomization with a custom curriculum to expose it to scenarios beyond those observed during pre-training. Specifically, we fine-tune for the object transport task in unseen robot initial locations, which are parameterized by three variables relative to the target object: (i) radial distance, (ii) polar angle, and (iii) heading angle of the robot. The fine-tuning expands the ranges to cover 320%, 125%, and 600% of the corresponding pre-training ranges, respectively. While the pre-trained policy achieves only 0% SR at the maximum randomization level, our curriculum-based fine-tuning improves the SR to over 80%. 

## _D. Hardware Experiment_ 

We demonstrate autonomous loco-manipulation on a Booster T1 humanoid robot, as shown in Fig. 3. For stable and accurate execution, we clamp locomotion speed to 0 _._ 2 m/s and hand speed to 0 _._ 05 m/s. This enables accurate locomanipulation, leading to higher SR. In real-world experiments, REFINE-DP achieves a success rate of 70% (Task 1), 50% (Task 2), and 75% (Task 3), respectively, over _N_ = 20 trials. The failure modes include occasional tripping of the lowerbody controller and unsuccessful grasps on box or handles. 

The sim-to-real gap arises from two primary sources. First, the object observations exhibit systematic offsets from objectpose calibration and become biased under MoCap or perception occlusions, especially during contact-rich phases such as grasping a box or door handle. Second, sim-to-real dynamics mismatch causes locomotion trembling and sliding, which increases the difficulty of manipulation. These factors lead to a reduction from the 90%+ SR in simulation. Despite these gaps, the fine-tuned policy demonstrates improved robustness to noisy observations and execution errors. 

REFINE-DP adapts to environmental perturbations during execution by re-adjusting and re-attempting. As demonstrated in Task 1, when the target object location is altered, the robot re-adjusts its plan on-the-fly and continues the task. Upon execution failures, the policy re-attempts the task. For example, in the door-opening experiment, when the robot misses the door handle, it often takes small footsteps to get closer before attempting the manipulation again. Such corrective behaviors occur consistently under the fine-tuned policy, whereas the pretrained policy often becomes stuck and fails to recover, leading to halted execution. This capability to re-attempt and recover from unexpected changes and failed actions demonstrates the robustness and autonomy of our REFINE-DP. 

During fine-tuning, REFINE-DP improves task efficiency by eliminating redundant and indecisive motions commonly observed in pre-trained policies, thereby increasing task throughput. REFINE-DP achieves average speedups of around 10% and 20% for the box pickup and door-opening tasks. 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED JULY, 2026 

8 


Fig. 6: Comparison of success rate between scaling pretraining data and fine-tuning diffusion policy. 

## V. CONCLUSION 

In this study, we introduced REFINE-DP, a fine-tuning framework that jointly optimizes a hierarchical planner–controller architecture. Fine-tuning the DP motion planner improves data efficiency and enhances generalization to outof-distribution scenarios. Meanwhile, fine-tuning the locomanipulation controller improves tracking accuracy and execution smoothness. Together, these components achieve high success rates on loco-manipulation tasks on a humanoid robot. A current limitation is that the planner remains state-conditioned, which requires an explicit object pose. Future work will focus on an end-to-end RGB-conditioned diffusion-policy planner, more versatile skills in a unified whole-body controller, and a richer planner-controller interface. Pre-training or fine-tuning with real-world data will be explored to better close the simto-real gap. In addition, this study relies on VR teleoperation and per-task heuristic rollouts; supplementing these with more scalable data sources, such as egocentric human data, is a promising direction for reducing the data burden. 

## REFERENCES 

- [1] C. Khazoom, S. Hong, M. Chignoli, E. Stanger-Jones, and S. Kim, “Tailoring solution accuracy for fast whole-body model predictive control of legged robots,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 12, pp. 11 074–11 081, 2024. 

- [2] J. Jang, Z. Wang, Z. Zhou, F. Wu, and Y. Zhao, “Seec: Stable endeffector control with model-enhanced residual learning for humanoid loco-manipulation,” _International Conference on Robotics and Automation_ , 2026. 

- [3] T. He _et al._ , “Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning,” in _Annual Conference on Robot Learning_ , 2024. 

- [4] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” in _Annual Conference on Robot Learning_ , 2024. 

- [5] C. Chi _et al._ , “Diffusion policy: Visuomotor policy learning via action diffusion,” _The International Journal of Robotics Research_ , vol. 44, no. 10-11, pp. 1684–1704, 2025. 

- [6] A. Z. Ren _et al._ , “Diffusion policy policy optimization,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [7] H. Jung, Z. Gu, Y. Zhao, H.-W. Park, and S. Ha, “Ppf: Pre-training and preservative fine-tuning of humanoid locomotion via model-assumptionbased regularization,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 11, pp. 11 466–11 473, 2025. 

- [8] Z. Gu _et al._ , “Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning,” _IEEE/ASME Transactions on Mechatronics_ , vol. 31, no. 2, pp. 2300–2330, 2026. 

- [9] Y. Ze _et al._ , “Twist2: Scalable, portable, and holistic humanoid data collection system,” _arXiv preprint arXiv:2511.02832_ , 2025. 

- [10] Y. Zhang _et al._ , “Falcon: Learning force-adaptive humanoid locomanipulation,” 2025. 

- [11] C. Lu _et al._ , “Mobile-television: Predictive motion priors for humanoid whole-body control,” _arXiv preprint arXiv:2412.07773_ , 2024. 

- [12] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang, “HOMIE: Humanoid Loco-Manipulation with Isomorphic Exoskeleton Cockpit,” in _Proceedings of Robotics: Science and Systems_ , 2025. 

- [13] C. Zhang, W. Xiao, T. He, and G. Shi, “Wococo: Learning whole-body humanoid control with sequential contacts,” in _Annual Conference on Robot Learning_ , 2024. 

- [14] C. Schwarke, V. Klemm, M. v. d. Boon, M. Bjelonic, and M. Hutter, “Curiosity-driven learning of joint locomotion and manipulation tasks,” in _Conference on Robot Learning_ , vol. 229, 2023, pp. 2594–2610. 

- [15] T. Haarnoja _et al._ , “Learning agile soccer skills for a bipedal robot with deep reinforcement learning,” _Science Robotics_ , vol. 9, no. 89, 2024. 

- [16] H. Xue _et al._ , “Opening the sim-to-real door for humanoid pixel-toaction policy transfer,” 2025. 

- [17] J. Dao, H. Duan, and A. Fern, “Sim-to-real learning for humanoid box loco-manipulation,” in _International Conference on Robotics and Automation_ , 2023. 

- [18] F. Liu _et al._ , “Opt2skill: Imitating dynamically-feasible whole-body trajectories for versatile humanoid loco-manipulation,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 11, pp. 12 261–12 268, 2025. 

- [19] Z. Xie, J. Tseng, S. Starke, M. van de Panne, and C. K. Liu, “Hierarchical planning and control for box loco-manipulation,” _Proc. ACM Comput. Graph. Interact. Tech._ , vol. 6, no. 3, 2023. 

- [20] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _ICML Workshop on New Frontiers in Learning, Control, and Dynamical Systems_ , 2023. 

- [21] S. Yin, Y. Ze, H.-X. Yu, C. K. Liu, and J. Wu, “Visualmimic: Visual humanoid loco-manipulation via motion tracking and generation,” 2025. 

- [22] H. Weng _et al._ , “Hdmi: Learning interactive humanoid whole-body control from human videos,” 2025. 

- [23] C. Sferrazza, D.-M. Huang, X. Lin, Y. Lee, and P. Abbeel, “HumanoidBench: Simulated Humanoid Benchmark for Whole-Body Locomotion and Manipulation,” in _Robotics: Science and Systems XX_ , 2024. 

- [24] L. Ankile, A. Simeonov, I. Shenfeld, M. Torne, and P. Agrawal, “From imitation to refinement – residual rl for precise assembly,” 2024. 

- [25] E. Su, T. Westenbroek, A. Nagabandi, and A. Gupta, “Rfs: Reinforcement learning with residual flow steering for dexterous manipulation,” 2026. 

- [26] L. L. Ankile, Z. Jiang, R. Duan, G. Shi, P. Abbeel, and A. Nagabandi, “Residual off-policy RL for finetuning behavior cloning policies,” in _ICLR Workshop on Lifelong Agents: Learning, Aligning, Evolving_ , 2026. 

- [27] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _Computing Research Repository_ , vol. abs/1707.06347, 2017. 

- [28] H. Ma, T. Chen, K. Wang, N. Li, and B. Dai, “Efficient online reinforcement learning for diffusion policy,” 2025. 

- [29] K. Chen _et al._ , “ _π_ RL: Online rl fine-tuning for flow-based visionlanguage-action models,” 2026. 

- [30] M. Mittal _et al._ , “Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning,” _arXiv preprint arXiv:2511.04831_ , 2025. 

- [31] H. Wang _et al._ , “Beamdojo: Learning agile humanoid locomotion on sparse footholds,” in _Robotics: Science and Systems_ , 2025. 

- [32] W. Suliman, E. Davydenko, E. Chaikovskaia, and R. Gorbachev, “Reinforcement learning-based footstep control for humanoid robots on complex terrain,” _IEEE Access_ , 2025. 

- [33] X. B. Peng, P. Abbeel, S. Levine, and M. van de Panne, “Deepmimic: example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics_ , vol. 37, no. 4, 2018. 

- [34] R. Nai _et al._ , “Humanoid manipulation interface: Humanoid whole-body manipulation from robot-free demonstrations,” 2026. 

- [35] Z. Luo _et al._ , “Sonic: Supersizing motion tracking for natural humanoid whole-body control,” 2026. 

- [36] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic models,” _Advances in neural information processing systems_ , vol. 33, pp. 6840– 6851, 2020. 

- [37] J. Schulman, P. Moritz, S. Levine, M. Jordan, and P. Abbeel, “Highdimensional continuous control using generalized advantage estimation,” in _International Conference on Learning Representations_ , 2016. 

- [38] A. Q. Nichol and P. Dhariwal, “Improved Denoising Diffusion Probabilistic Models,” in _Proceedings of the 38th International Conference on Machine Learning_ , 2021, pp. 8162–8171. 

- [39] E. Olson, “Apriltag: A robust and flexible visual fiducial system,” in _International Conference on Robotics and Automation_ , 2011, pp. 3400– 3407. 

- [40] M. Lee _et al._ , “Stageact: Stage-conditioned imitation for robust humanoid door opening,” 2025. 

- [41] D. Calvert _et al._ , “A behavior architecture for fast humanoid robot door traversals,” _Robotics and Autonomous Systems_ , vol. 195, p. 105217, 2026. 

GU _et al._ : REFINE-DP: DIFFUSION POLICY FINE-TUNING FOR HUMANOID LOCO-MANIPULATION VIA REINFORCEMENT LEARNING 

9 


Fig. 7: The foot-placement policy enables the robot to walk on flat ground and stairs. 

## VI. APPENDIX 

## _A. Foot-Placement Policy Training_ 

As described in Sec. III-A, the foot-placement policy _π_ lower is conditioned on discrete foot-placement commands **g** _t_<sup>lower</sup> with three components: (1) a swing-foot indicator specifying which foot is active, (2) a normalized phase countdown progressing from 1 to 0, and (3) a target swing-foot pose relative to the stance foot, parameterized by ( _x, y, z,_ yaw). Given **g** _t_<sup>lower</sup> , _π_ lower generates a stepping motion that places the swing foot at the commanded target pose. During training, the policy learns this behavior by tracking a set of reference trajectories. During inference, however, it receives only the foot-placement command **g** _t_<sup>lower</sup> and does not require access to the reference trajectories. 

The trajectories are generated using a linear inverted pendulum model (LIPM) combined with lower-body inverse kinematics. Each reference motion corresponds to a specific stair rise and tread depth and consists of three phases: preswing, swing, and post-swing. To increase motion diversity, we randomize the lift-off and landing positions of the swing foot relative to the stance foot using discretized grid sampling. Given the sampled lift-off and landing positions, the corresponding swing-foot trajectory is precomputed as a cubic spline that avoids collisions with the stairs. We then solve a trajectory optimization problem to produce a joint-level stepping motion. 

During training, the robot learns to track the reference stepping motions while maintaining balance on stairs. In each parallel simulation environment, the robot is initialized on a stair step whose rise-and-tread configuration matches the pre-swing and post-swing poses associated with the sampled reference trajectory. Detailed observations are listed in Table I. Table II summarizes the reward terms used during training. 

Driven by these inputs and motion-imitation objectives, the policy learns to execute the targeted swing-foot placements precisely. Fig. 7 illustrates the resulting behavior as the robot navigates a multi-level platform. 

## _B. Foot-Placement and Velocity-Tracking Ablation_ 

The loco-manipulation tasks in this work require precise torso positioning in addition to hand tracking because small base-pose errors can prevent the hands from reaching objects such as door handles, boxes, or stair platforms. Velocitytracking interfaces do not directly enforce this positional objective. In practice, low-speed velocity commands can lead to stepping in place, overshoot, or unresponsiveness to small commands when a dead zone is used. In contrast, our footplacement command specifies where each step should land, 


Fig. 8: Position and yaw tracking errors across 10 trials for velocity-based and foot-placement-based lower-body policies. 

TABLE I: Observation terms for RL policy training 

|**Observation**|**Actor**|**Critic**|
|---|---|---|
|_Manipulation_|||
|Projected gravity|✓|✓|
|Arm joint pos.|✓|✓|
|Arm joint vel.|✓|✓|
|Action|✓|✓|
|Hand pose cmd. (**p**<sup>cmd</sup><br>_L _<sup>_,_</sup><sup>**p**cmd</sup><br>_R_ <sup>)</sup>|✓|✓|
|Current hand poses (**p**_L,_**p**_R_)|✓|✓|
|Hand tracking error (**e**_L,_**e**_R_)|✓|✓|
|_Locomotion_|||
|Foot placement cmd.|✓|✓|
|Base angular vel.|✓|✓|
|Projected gravity|✓|✓|
|Leg joint pos.|✓|✓|
|Leg joint vel.|✓|✓|
|Action|✓|✓|
|Reference foot pos.||✓|
|Current foot pos.||✓|
|Base linear vel.||✓|
|Foot wrench||✓|


giving the controller direct control over the number and locations of footsteps used to approach the target. This explicit command interface is therefore better suited to the frequent stopping, restarting, and fine positioning required for humanoid loco-manipulation. 

To quantify this effect, we conducted a torso-positiontracking ablation that isolates the lower-body command interface. We kept all upper-body components fixed and used the same PD feedback controller for torso-position tracking while varying only the lower-body policy. For the foot-placement policy, the feedback command is converted into explicit footstep targets by the velocity-to-footstep planner described in Sec. III-A. For the velocity-tracking policy, the same feedback command is used directly as a velocity command. We then measured the resulting torso position and yaw errors as the robot attempted to reach the target position. As shown in Fig. 8, the foot-placement policy achieves lower tracking error and more consistent target reaching across trials. These results support our choice of foot-placement tracking over velocity tracking for precise loco-manipulation. 

## _C. Additional Results_ 

**Fine-tuning achieves higher throughput.** The fine-tuned policy demonstrates higher throughput, completing the same task in less time. As shown in Fig. 9, fine-tuning reduces task completion time by 15% on average across Task 2, Task 3, and Task 4, due to the improved action efficiency acquired 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED JULY, 2026 

10 

TABLE II: Reward terms for foot-placement tracking policy 


|**Term**|**Formulation**<br>**Weight**|
|---|---|
|_End-effector reference _|_tracking (per foot)_<br>|
|Position (_σ_ = 0_._05)|exp(_−∥_**p**_−_**p**<sup>ref</sup>_∥_<sup>2</sup>_/σ_<sup>2</sup>)<br>+5_._0<br>|
|Yaw (_σ_ = 0_._1)|exp(_−_(_ψ −ψ_<sup>ref</sup>)<sup>2</sup>_/σ_<sup>2</sup>)<br>+3_._0<br>|
|Base vel. (_σ_ = 0_._25)|exp(_−∥_**v**_−_**v**<sup>ref</sup>_∥_<sup>2</sup>_/σ_<sup>2</sup>)<br>+1_._0|
|_Joint reference trackin_|_g_<br>|
|Position (_σ_ = 0_._3)|exp(_−∥_**q**_−_**q**<sup>ref</sup>_∥_<sup>2</sup>_/σ_<sup>2</sup>)<br>+0_._5<br>|
|Velocity (_σ_ = 1_._0)|exp(_−∥_˙**q**_−_˙**q**<sup>ref</sup>_∥_<sup>2</sup>_/σ_<sup>2</sup>)<br>+0_._3|
|_Regularization (with c_|_urriculum →)_<br>|
|Action smoothness<br>Joint acceleration|_∥_**a**_t −_**a**_t−_1_∥_<sup>2</sup><br>_−_0_._001_→−_0_._5<br>_∥_¨**q**_∥_<sup>2</sup><br>_−_10<sup>_−_7</sup> _→−_10<sup>_−_5</sup>|
|Torque limits|max(0_, |_**_τ_**_| −_**_τ_**max)<br>_−_0_._5<br>|
|Joint limits|max(0_, |_**q**_| −_**q**max)<br>_−_10<sup>_−_4</sup><br>|
|Ankle posture|_∥_**q**_−_**q**def_∥_<sup>2</sup><br>_−_2_._0<br>|
|Base ori. (_σ_ = 0_._2)|exp(_−∥_**g**xy_∥_<sup>2</sup>_/σ_<sup>2</sup>)<br>+3_._0|
|Foot airtime (_τ_ = 0_._4) <br>Base height range|<sup>�</sup><br>_i _<sup>_ci_(</sup><sup>_t_air</sup><br>_i_<br>_−τ_)<br>+20_._0<br>[max(0_, h_min_−h_)]<sup>2</sup><br>+ [max(0_, h −h_max)]<sup>2</sup><br>_−_3_._0|


through RL. In contrast, the pre-trained policy often produces hesitant or indecisive motions, resulting in slower execution. 

Fig. 10: (a) Evaluation success rates on different robot initialization ranges. With curriculum checkpoint shows the best performance in high OOD regions. (b) Average sum of upper body joint jerk squared over 100 rollout environments. 

**Fine-tuning using curriculum improves motion quality.** To improve the fine-tuning efficiency with high domain randomization, we introduce a curriculum that progressively increases the randomization ranges by 10% once the policy achieves 90% SR at the current randomization level. This curriculum enables the policy to gradually expand coverage and master increasingly challenging conditions. To evaluate the effectiveness of our proposed curriculum, we compare the final success rates of the pre-trained, curriculum-fine-tuned, and non-curriculum-fine-tuned checkpoints across different regions of the full randomization space, defined by the combination of heading and distance intervals. Both fine-tunes have been 

trained with the same hyper-parameters. The result in Fig. 10 (a) shows that curriculum training adapt the desired behavior to OOD scenarios. In contrast, although fine-tuning without curriculum (directly training on the max randomization ranges) also leads to increased SR, the learned arm behavior exhibits more jitter in OOD scenarios due to the early exposure to high randomization scenarios, where the stochastic actions during rollout are amplified by PPO. This is illustrated by Fig. 10 (b), where we report the squared sum of upper-body 

GU _et al._ : REFINE-DP: DIFFUSION POLICY FINE-TUNING FOR HUMANOID LOCO-MANIPULATION VIA REINFORCEMENT LEARNING 

11 

joint jerk averaged over 100 rollout environments. The withcurriculum fine-tune maintains stable jerk across all OOD and in-distribution (ID) scenarios, whereas the w/o-curriculum fine-tune shows much higher jerk, similar to the pre-trained checkpoint, when deployed to OOD settings. 

**Adding noise to the DP state produces chaotic motion and lowers the success rate.** To test whether injecting observation noise improves the diffusion policy’s (DP) robustness to the sim-to-real gap, we fine-tune DP planners under several observation-noise levels by adding zero-mean Gaussian noise to the observed state. As a result, noise with a standard deviation of 1 cm and 3 cm reduces the real-world Task 1 success rate from 70% to 25% and 20%, respectively. The dominant failure mode is excessive, chaotic motion in the predicted hand poses. We attribute this to the generative nature of the DP: perturbing the observed state corrupts the conditioning signal, so the planner learns to map noisy, inconsistent conditions to actions and produces unstable predictions rather than improved robustness. 

