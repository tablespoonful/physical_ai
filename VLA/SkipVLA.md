---
title: "SkipVLA: Skipping VLA Steps with Classical Planning for Fast Robot Manipulation"
date: "2026-09-17"
authors: "Kaivalya Agrawal; Md Ashiqur Rahman; Raymond A. Yeh; Zachary Kingston"
url: https://arxiv.org/abs/2609.20648
pdf: https://arxiv.org/pdf/2609.20648
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.20648)** / [論文ページ](https://arxiv.org/abs/2609.20648)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SkipVLA: Skipping VLA Steps with Classical Planning for Fast Robot Manipulation** 

Kaivalya Agrawal, Md Ashiqur Rahman, Raymond A. Yeh, and Zachary Kingston 

**_Abstract_ — Vision-Language-Action (VLA) models are a class of generalist robot policies that map camera images and language instructions directly to robot actions. While promising, these models remain slow at test time, particularly for longhorizon tasks that require many queries to the policy. Recent efforts reduce VLA latency by distilling smaller models, overlapping asynchronous action chunks, or pairing the VLA with a fast low-level policy, but still run a learned policy for the entire task. In contrast to VLA, classical motion planners quickly find collision-free motions, but require an explicit goal and have no semantic understanding of the task. In this work, we present SkipVLA, a hybrid policy that combines a pretrained VLA with a classical motion planner, using the planner for freespace motion and querying the VLA only for contact-rich skills such as grasping and placing. SkipVLA reuses the frozen visionlanguage backbone of the VLA to predict a target pose for each planned motion, and learns this predictor without additional demonstrations introduced into the system by using what was already learnt by the large VLA. We evaluate SkipVLA with three VLAs on 13 LIBERO tasks in simulation and three pickand-place tasks on a physical 6-DoF YAM arm, demonstrating up to 2.5x faster task completion and significantly lower energy consumption while achieving the same task success rate.** 


Fig. 1: Our hybrid method on a real-world pick-and-place task, shown at three points in time. White arrows are free-space transit executed by the planner module. **(** ❶ **, cyan)** From the start pose, the planning module predicts a hover target above the red block and moves the arm to it. **(** ❷ **, red)** The VLA expert module performs the grasp. When the gripper closes, control returns to the planner, which moves the arm to a predicted hover target above the box. **(** ❸ **, yellow)** The VLA expert places the block in the box. 

## I. INTRODUCTION 

Vision-Language-Action (VLA) models [1, 2] have emerged as a promising approach for generalist robot manipulation. By pairing pretrained vision-language backbones with expressive action heads, VLAs map raw camera observations and natural-language task instructions directly to robot actions. This unified formulation enables open-vocabulary instruction following, cross-scene generalization, and longhorizon task execution without handcrafted heuristics. 

Despite their expressive capability, VLAs face a severe practical limitation: high inference latency. Generating each action chunk requires forward passes through multi-billionparameter networks, resulting in latencies that far exceed the robot’s control cycle. In long-horizon tasks requiring dozens or hundreds of queries, this overhead leads to sluggish execution, high energy consumption on edge compute platforms, and compromised reactive safety. 

Prior work to reduce VLA latency typically distills smaller models [3], overlaps asynchronous action chunks [4], or pairs the VLA with a fast low-level policy in a hierarchical setup [5]. However, each introduces notable trade-offs: distilled models frequently suffer performance degradation; asynchronous chunking risks executing stale actions that push the policy out of distribution; and hierarchical setups require 

The authors are with the Department of Computer Science, Purdue University, _{_ agraw201, rahman79, rayyeh, zkingston _}_ @purdue.edu. 

training a completely new policy network from scratch for specialized subtasks. Crucially, all of these methods treat manipulation as a monolithic end-to-end learning problem, querying large neural networks even during simple, unconstrained motions. 

In reality, manipulation tasks exhibit a natural physical decomposition: they alternate between short, _contact-rich manipulation_ skills (e.g., grasping, reorienting, or placing) and long stretches of _free-space transit_ (e.g., reaching toward an object or navigating to a receptacle). Contactrich manipulation requires adaptive, closed-loop visuomotor feedback to manage complex physical contacts, a domain where learned VLAs excel. In contrast, free-space transit is a purely geometric and kinematic problem that requires collision avoidance but minimal semantic reasoning. 

Classical motion planners, such as sampling-based algorithms [6] and trajectory optimizers [7], solve this geometric problem rapidly, generating collision-free trajectories in microseconds to milliseconds with formal safety guarantees. However, classical planners are semantically blind, i.e., they require explicit goal poses and cannot infer them from natural language. Methods that prompt foundation models for zeroshot spatial keypoints [8–10] and only rely on geometric optimization for the entire task struggle with the delicate contact dynamics that VLAs naturally handle. 

This motivates a hybrid architecture that reserves the VLA for contact-rich interactions, offloads free-space transit to a 

fast classical planner, and uses the VLA’s frozen representations to predict the planner’s target poses. 

To this end, we introduce SkipVLA, a modular hybrid policy that dynamically interleaves a pretrained VLA with a classical motion planner. SkipVLA scores candidate 3D object bounding boxes, conditioned on the base VLA’s frozen vision-language features, to determine collision-free hover targets. A classical planner navigates the robot through free space to the target pose, then hands control to the VLA for contact-rich manipulation. Once the manipulation completes as signaled by a gripper state transition, control returns to the planner. We train the target predictor using self-supervision extracted from existing demonstration trajectories at gripper events, requiring no manual annotations, architectural changes, or policy retraining. **Our main contributions are:** 

- We present SkipVLA, a plug-and-play framework that accelerates manipulation by routing free-space transit to classical motion planners and reserving pretrained VLAs solely for contact-rich skills. 

- We develop a lightweight scoring head that uses the VLA’s frozen vision-language tokens to predict 3D target poses and can be trained on an existing imitation learning dataset with no additional annotation. 

- We evaluate SkipVLA across 13 tasks on the LIBERO benchmark in simulation and three physical tasks on a 6- DoF YAM arm, spanning three distinct VLA backbones ( _π_ 0 _._ 5, SmolVLA, and MolmoAct2) and multiple motion planners (VAMP and cuRoboV2). 

- SkipVLA achieves up to a 2 _._ 5 _×_ wall-clock speedup (59 _._ 6% latency reduction) and cuts compute energy by over 52% on an NVIDIA Jetson Thor. 

## II. RELATED WORK 

**Vision-language-action models.** Following the success of Vision-Language Models (VLMs) [11, 12] in scene understanding and cross-modal semantic alignment, substantial research has aimed to construct open-ended robotic policies that unify perception and control within a single end-toend framework, known as VLA models. Recently, VLAs have expanded to incorporate generative architectures for better generalization and performance, such as diffusionand flow-matching-based action heads [2, 13, 14], to capture complex, multimodal action distributions. While these models have been successful in executing semantically aligned, long-horizon tasks, their practical deployment is severely bottlenecked due to their massive parameter counts, making them unsuitable for high-frequency real-world control. 

**Efficient VLA architectures.** Extensive research has been conducted to reduce the high inference latency of VLAs. Large VLAs have been distilled into smaller variants to reduce parameter counts and improve inference speed [3, 15]. However, such models often exhibit drops in performance due to distribution shift and still remain relatively slow for highfrequency control. Other works employ action chunking [4, 16, 17] to overlap asynchronously inferred action chunks, effectively hiding execution pauses due to slow inference. These approaches introduce staleness in the inferred chunk, 

and interleaving action chunks can push the policy off distribution. Finally, hierarchical methods introduce a low-latency, smaller policy module that operates asynchronously alongside a large VLA [5, 18–21], reusing the visual representations of the larger network. 

**Classical motion planning.** Classical planning approaches like Sampling-Based Motion Planning algorithms (SBMP) and trajectory optimization methods have long proven to be successful in solving complex navigation and manipulation tasks. Modern implementations of SBMPs are highly energy- and time-efficient, capable of generating collisionfree trajectories in microseconds [6, 22]. Similarly, gradientbased trajectory optimization frameworks [23, 24] and GPUaccelerated solvers [7] calculate dynamically feasible motion in real time. Despite their safety guarantees and low-latency planning, classical planners are semantically blind. They operate purely on coordinate geometry and require welldefined goal states or objective functions. 

**Combining learning with classical planning.** Recent works have attempted to combine the semantic reasoning of foundation models with the reliability of classical planners. One line of research, including VoxPoser [8] and ReKep [9], prompts VLMs to output spatial cost maps or relational constraints that are then solved by trajectory optimization. However, because these methods rely entirely on zero-shot geometric optimization rather than learned action priors, they struggle to execute dynamic, contact-rich manipulation that cannot be represented as a cost function. 

A parallel line of work attempts to integrate classical planning directly with trained behavioral policies like LiLoVLA [25] and MPVI [26]. However, these methods suffer from distinct architectural bottlenecks. Frameworks like MPVI treat the motion planner primarily as a recovery mechanism, using it to veer the policy back to in-distribution only after it drifts out-of-distribution. Other works, like LiLoVLA, rely on pre-defined action sequences before performing simple skill chaining. 

In contrast to these frameworks, SkipVLA interleaves a generalist VLA with classical sampling-based motion planning at planning and execution time. By leveraging the VLA’s pretrained representations strictly for target pose prediction, we dynamically hand off all free-space navigation in between atomic skills to the fast classical planner. This achieves massive latency reductions and guarantees collision-free transit without compromising on task success rate or introducing shifts in policy and data distribution within the VLA and builds on top of the base VLA architecture. 

## III. BACKGROUND 

In this section, we introduce the background and notation used in this work. 

**VLA.** We denote a generalist VLA robot policy as _π_<sup>vla</sup> . This policy maps an observation _Os_ , a natural-language instruction _L_ (task description), and an optional proprioceptive state **p** _s_ to a robot action 


Fig. 2: **SkipVLA on a single LIBERO-Object episode.** Top: five keyframes from one successful rollout of _π_ 0 _._ 5 + SkipVLA with the VAMP planner. **(a)** The scoring module selects a target object and pose. **(b)** VAMP’s plan is followed from start to target pose and control is handed over to VLA. **(c)** The VLA completes the skill of grasping and the control is handed over to SkipVLA which scores the next target. **(d)** VAMP’s plan is followed from start to target pose and control is handed over to VLA. **(e)** The VLA completes the skill of placing and task is marked complete. Bottom: the scoring module’s probability over all seven tracked object bounding boxes for the same episode, with background shading showing which policy holds control at each step: planner transit (blue) and VLA (orange). Control returns to the planner at exactly the grasp and release transitions. Over the 6.8s episode, the planner drives 54% of the task. The deployed system queried the scorer twice; the continuous probability curves are an offline re-scoring of every frame with a fresh latent to show the change in the scoring signal throughout the trajectory. 

at step _s_ . The robot’s proprioceptive state **p** _s_ consists of the joint angles and gripper state (with corresponding endeffector pose **p**<sup>_ee_</sup> _s_<sup>).Theobservation</sup><sup>_Os_includesanimage</sup> and depth map from a workspace viewpoint RGBD camera and an image from a wrist-mounted RGB camera. 

**Trajectory.** We use the term _trajectory_ to denote a sequence of proprioceptive states _τ_ as 


where _N_ = _|τ |_ is the trajectory length and _as_ = **p** _s_ +1 _−_ **p** _s_ is the action taken at step _s_ that changes the robot’s proprioceptive state from **p** _s_ to **p** _s_ +1. 

**Action chunks.** Different VLA architectures generate actions at different granularities. A VLA when queried at step _s_ can produce an action _chunk_ of _K_ future actions 


For a given VLA, the action chunk horizon _K ≥_ 1 is a fixed constant. Therefore, the VLA is queried every _K_ steps. We denote the set of these _query steps_ by _Q_ = _{_ 1 _,_ 1 + _K,_ 1 + 2 _K, . . . } ⊂{_ 1 _, . . . , N }_ , with _|Q|_ = _⌈N/K⌉_ . 

**Execution time.** The total execution time for a trajectory _τ_ of length _N_ = _|τ |_ is governed by two factors: the control period ∆ _t_ ctrl = _f_ <u>1ctrl</u><sup>,dictatedbythesamplingfrequency</sup><sup>_f_ctrl</sup> of the robot controller, and the inference latency ∆ _t_ lat, which is the processing time required by the VLA to generate each action chunk. 

The total execution time of the trajectory _τ_ generated by policy _π_ is given by: 


where ∆ _t_ ctrl and ∆ _t_ lat are the control period and inference latency of _π_ , and _|Q|_ = _N/K_ is the number of query steps (assuming _N_ is a multiple of _K_ for simplicity). For a generalist VLA with a large number of parameters, ∆ _t_ lat is often the bottleneck of the execution time (∆ _t_ lat _≫_ ∆ _t_ ctrl). 

**Imitation learning.** In robot manipulation, policies are mainly trained via imitation learning on a static dataset _D_ = _{_ ( _τ_<sup>_e,i_</sup> _, {O}_<sup>_i_</sup> _, L_<sup>_i_</sup> ) _}_ of expert demonstrations. The objective trains the policy to imitate expert actions step-by-step: 


where _a_<sup>_e_</sup> _s_<sup>is the expert action at step</sup><sup>_s_and</sup><sup>_ℓ_is an appropriate</sup> loss for the task. 

## IV. METHOD 

We propose SkipVLA which augments a generalist VLA policy _π_<sup>vla</sup> with a lightweight, low-latency classical control module _π_<sup>fast</sup> (∆ _t_<sup>fast</sup> lat<sup>_≪_∆</sup><sup>_t_vla</sup> lat<sup>).Itdynamicallyroutesbetween</sup> classical motion planning (for free-space transit) and a VLA (for contact-rich manipulation) (see Fig. 2). 

## _A. Problem Formulation and Objective_ 

We achieve this hybrid execution through an indicator module _I_ that determines which policy to execute at each timestep. Given an observation _Os_ , task instruction _L_ , and proprioceptive state **p** _s_ , the indicator outputs a binary decision _Is ∈{_ 0 _,_ 1 _}_ , yielding the hybrid policy: 


The latency of the hybrid policy at step _s_ is expressed as: 


**Trajectory-level objective.** To keep the latency low, the _π_<sup>fast</sup> module is designed to be lightweight using classical motion planning. However, classical motion planners (such as RRT or PRM) generate collision-free paths that optimize geometric or kinematic criteria rather than mimicking human demonstration trajectories step by step. Consequently, a peraction imitation loss as in Eq. (5) would incorrectly penalize such valid transit trajectories, even when they reach the destination or the target pose safely and faster. 

To address this, we use a trajectory-level _imitation learning_ objective where, rather than matching every action, the trajectory rolled out by _π_<sup>hyb</sup> is constrained to pass through key _waypoints_ of the expert trajectory, which ensures successful task completion. To minimize total execution time, the overall objective can be expressed as follows: 


where _τ_<sup>hyb</sup> is the trajectory rolled out by _π_<sup>hyb</sup> , _τ_<sup>_e_</sup> is the corresponding expert trajectory, _T_ ( _τ_<sup>hyb</sup> ) is the execution time, and _λ >_ 0 is a hyper-parameter of choice. _ℓ_ traj( _τ_<sup>hyb</sup> _, τ_<sup>_e_</sup> ) = 0 implies the hybrid trajectory passes through all required key waypoints, ensuring task completion. 

**Key-waypoints extraction.** The trajectory _τ_ for completing a task can be partitioned into segments, each associated with a subtask. Broadly, these subtasks fall into two categories: _active object manipulation_ , where the robot’s endeffector or gripper performs grasping, reorientation, or other contact-rich interactions with the object; and _reach-and-place_ (approach/placement), where the robot primarily moves its end-effector with or without a grasped object. 

In more detail, given a trajectory _τ_ , we partition it as _τ_ = [ _τ_<sup>1</sup> _, τ_<sup>2</sup> _· · · τ_<sup>_n_</sup> ], where we concatenate each segment _τ_<sup>_j_</sup> corresponding to either active object manipulation or reachand-place. 

For an expert trajectory segment _τ_<sup>_e,j_</sup> corresponding to active object manipulation, the matching segment _τ_<sup>hyb</sup><sup>_,j_</sup> rolled out by _π_<sup>hyb</sup> should closely follow the expert at each step to ensure successful completion of the subgoal. On the other hand, for an expert reach-and-place segment _τ_<sup>_e,j_</sup> , successful completion requires the corresponding segment _τ_<sup>hyb</sup><sup>_,j_</sup> to match only the initial and final end-effector poses. Based on this structure, we define the segment-level loss as follows: 


where _τs_<sup>hyb</sup><sup>_,j_</sup> and _τs_<sup>_e,j_</sup> represent the end-effector poses at step _s_ for the respective segments. Additionally, _Nj_ = _|τ_<sup>hyb</sup><sup>_,j_</sup> _|_ and _Nj_<sup>_e_=</sup><sup>_|τ e,j|_indicatethelengthsoftherespectivesegments,</sup> while _d_ ( _·, ·_ ) denotes the chosen distance metric. 

The full trajectory-level loss is then defined as the sum of segment-level losses as: 


_B. Implementation Details_ 

In this section, we detail the design of the fast control module _π_<sup>fast</sup> and the policy indicator module _I_ . Our hybrid policy _π_<sup>hyb</sup> is designed to allocate tasks to the policies based on their complexity: _π_<sup>fast</sup> executes reach-and-place subtasks, while _π_<sup>vla</sup> handles active object manipulation. This division leverages the fact that contact-rich manipulation demands expressive, learned visuomotor control, whereas free-space transit is purely geometric and can be completed significantly faster using classical motion planning. 

**Fast control module** _π_<sup>**fast**</sup> **.** The fast control module _π_<sup>fast</sup> is composed of two key components: a _target pose predictor f_ tgt and a _low-level motion planner P_ . 

The target pose predictor _f_ tgt maps the current observation _Os_ , language instruction _L_ , and current proprioceptive state **p** _s_ to the target end-effector pose at the end of the current subtask (trajectory segment), denoted by **p** _s_<sup>tgtas:</sup> 


The low-level motion planner _P_ then takes the current state **p** _s_ , target pose **p**<sup>tgt</sup> _s_<sup>,andcurrentobservation</sup><sup>_O_</sup> _s_<sup>togenerate</sup> an action sequence ( _as, . . . , as_ + _m_ ) of horizon _m_ that moves the robot from **p** _s_ to **p**<sup>tgt</sup> _s_<sup>whileavoidingcollisions,i.e.,</sup> 


**Target pose predictor** _f_ **tgt.** The target pose predictor identifies the relevant object for the current subtask and determines a collision-free hover pose directly above it. Specifically, from the observation _Os_ , we first extract 3D bounding boxes _B_ = _{_ **b** _i}_<sup>_M_</sup> _i_ =1<sup>fortheobjectsinthescene,</sup> where **b** _i_ = ( **c** _i,_ **e** _i_ ) consists of 3D centroid **c** _i ∈_ R<sup>3</sup> and 3D extents **e** _i ∈_ R<sup>3</sup> . 

We score candidate object boxes by cross-attention between a learned positional embedding of each bounding box **b** _i_ (acting as the query) and the vision-language feature tokens extracted from the scene (acting as keys and values). More concretely, for the _i_ -th object bounding box **b** _i_ , its relevance score _ri_ is computed as: 


where **q**<sup>box</sup> _i_ = _ϕ_ pos( **b** _i_ ) _∈_ R<sup>_dk_</sup> is the learned positional embedding of the box, **K** vl _,_ **V** vl _∈_ R<sup>_T ×dk_</sup> are linear projections of the _T_ vision-language feature tokens **F** vl. A lightweight MLP head then maps the attended feature representation to a scalar score _ri ∈_ R. The target object is selected via ˆ _i_ = arg max _i ri_ , and a top-down, collision-free hover pose above candidate box **b** ˆ _i_ is assigned as the target pose **p** _s_<sup>tgt.</sup> 

We extract the vision-language features **F** vl using the vision-language backbone of _π_<sup>vla</sup> to reuse its pretrained 

Fig. 3: **Inference pipeline of our proposed SkipVLA.** We represent our input data as _Os, L,_ **p** _s_ , where _Os_ contains a workspace image, a wrist image, and a workspace depth map, _L_ represents the language instruction of the task, and **p** _s_ represents the proprioceptive state. The base expert component _π_<sup>_vla_</sup> comprises a VLM and an action head that process the input stream to output an action vector and a vision-language context latent. The object detection module takes in a different subset of inputs and uses FastSAM [27] and DBSCAN to generate object bounding boxes. The scoring module _ftgt_ selects the target object given the bounding boxes and latent context from the VLM. We use PyRoki [28] and VAMP to generate an action sequence. Finally, the indicator module _I_ decides which action sequence to execute. 

representations. Only the positional embedding _ϕ_ pos, crossattention projections, and the scoring MLP are trained from scratch. The target pose predictor is only called once at the beginning of every reach-and-place phase ( _I_ = 1). 

**Low-level motion planner** _P_ **.** Our framework is agnostic to the planner choice, and we instantiate _P_ using classical motion planners such as cuRoboV2 and VAMP. 

**Policy indicator module** _I_ **.** Learning task boundaries directly from visual observations is an active research area. As in this work, we focus on hybridizing the VLA with a fast motion planner; we choose an effective and fast heuristic based on gripper state and target pose proximity to indicate the task boundaries. 

The policy begins in a reach-and-place phase ( _I_ 0 = 1), using _π_<sup>fast</sup> to navigate toward the target pose **p** _s_<sup>tgt.Oncethe</sup> end-effector reaches the target ( _d_ ( **p**<sup>_ee_</sup> _s_<sup>_,_</sup><sup>**p**</sup> _s_<sup>tgt)</sup><sup>_< ϵ_</sup> _d_<sup>, where</sup><sup>_ϵ_</sup> _d_<sup>_>_</sup> 0 is some tolerance threshold), control is handed over to _π_<sup>vla</sup> ( _Is_ = 0). Once active manipulation is complete, signaled by a toggle in the gripper state ( _gs̸_ = _gs−_ 1), the indicator switches back to _Is_ = 1, returning control to _π_<sup>fast</sup> . Formally, let _gs ∈{_ 0 _,_ 1 _}_ be the binary gripper state (open or closed) at step _s_ , **p**<sup>_ee_</sup> _s_<sup>betheend-effectorpose, and</sup><sup>**p**</sup> _s_<sup>tgtbetheactive</sup> target pose. With initial state _I_ 0 = 1, the indicator _Is_ is recursively defined as: 


_C. Training the Hybrid Architecture_ 

Our hybrid policy design naturally simplifies the optimization in Eq. (8) and does not require end-to-end policy 

optimization. First, we freeze the pretrained _π_<sup>vla</sup> , which already handles contact-rich manipulation. Furthermore, _P_ guarantees reachability to any valid goal pose with minimal latency; the reach-and-place trajectory loss in Eq. (9) is minimized whenever the target pose **p**<sup>tgt</sup> _s_<sup>iscorrectlypredicted.</sup> Consequently, optimizing Eq. (8) reduces solely to training the target pose predictor _f_ tgt (specifically its box-scoring head) to identify the target object. 

**Automated data generation and training.** To train the target scoring function without manual annotation, we extract supervision directly from expert demonstration trajectories. Reach-and-place segments correspond to free-space transit motions that precede an interaction. We detect the completion of each reach-and-place segment by identifying gripper events, namely any change in the gripper state across a threshold (closing to grasp or opening to release). At this gripper event, the target object or receptacle is identified by finding the bounding box closest to the robot’s end-effector **p**<sup>_ee_</sup> event<sup>as:</sup> 


We then assign _i_<sup>_∗_</sup> as the ground-truth target for all preceding states _Os_ within that reach-and-place segment. For any observation _Os_ , given candidate bounding boxes _B_ and frozen vision-language tokens **F** vl, the scoring head computes relevance scores _{ri}_<sup>_M_</sup> _i_ =1<sup>accordingtoEq.(13).Weoptimize</sup> the trainable parameters of _f_ tgt using a cross-entropy loss: 


This allows SkipVLA to learn robust target prediction across varying viewpoints throughout transit, requiring no additional 

|Policy|SR (%) _↑_|_n_succ|Wall Clock Time (s) _↓_|VLA q _↓_|
|---|---|---|---|---|
|_π_0_._5 (base)|99_._0|495|8_._33_±_1_._18 (8_._3)|17_._0_±_2_._4 (17)|
|+ SkipVLA + VAMP|99_._0|495|5_._27_±_2_._19 (4_._4)|10_._6_±_4_._7 (9)|
|+ SkipVLA + cuRoboV2|99.2|496|6_._28_±_2_._82 (5_._3)|**9**_._**9**_±_**4**_._**8** (8)|
|+ Heuristic Ablation|**99**_._**6**|**498**|**5**_._**11**_±_**1**_._**16** (4_._7)|10_._7_±_2_._2 (10)|
|SmolVLA (base)|39_._0|195|12_._61_±_4_._99 (10_._8)|21_._3_±_8_._3 (18)|
|+ SkipVLA + VAMP|77_._0|385|**6**_._**96**_±_**3**_._**76** (5_._8)|11_._4_±_6_._2 (10)|
|+ SkipVLA + cuRoboV2|**82**_._**0**|**410**|7_._85_±_3_._94 (6_._8)|**10**_._**8**_±_**6**_._**5** (9)|
|+ Heuristic Ablation|79.0|395|7_._25_±_3_._02 (6_._2)|12_._6_±_5_._0 (11)|


TABLE I: **LIBERO-object Evaluation.** We evaluate SkipVLA across 10 pick and place tasks in simulation. We also ablate the indicator heuristics to show the model’s adaptability. We calculate statistics over successful trials only. **Bold** : best; <u>underline:</u> second-best in each backbone block. Numbers shown as Mean _±_ Standard Deviation (Median). 

## data collection or manual annotations. 

## V. EXPERIMENTS 

Our evaluation investigates whether interleaving a fast, point-to-point classical motion planner with a VLA model achieves faster execution and better compute efficiency than purely end-to-end VLA execution without compromising on task success. Specifically, our experiments aim to answer two core questions: 

- **Efficiency:** Does offloading free-space transit to a classical planner significantly reduce wall-clock execution time and VLA query frequency across varying task horizons without compromising on task success? 

- **Modularity:** Is the framework robust to variations in the underlying planner, latent context representation, and indicator function? 

## _A. Simulation Experiments_ 

On a standardized benchmark, we test for task speedup, VLA query reduction, and task completion. 

**Task setup & benchmark.** We evaluate on 13 topdown pick-and-place tasks drawn from two suites in the LIBERO [29] tabletop benchmark: LIBERO-OBJECT (short-horizon, single-object manipulation) and LIBERO-10 (longer-horizon multi-object manipulation). We deliberately select tasks solvable via top-down grasps since our objective is not to stress-test complex grasp synthesis, but to isolate and measure the efficiency gains of hybrid planning. We train a lightweight multi-head cross-attention scorer with a 3- layer MLP bounding box encoder on the human teleoperation demonstrations from LIBERO using all 50 demonstrations per task, 650 demonstrations in total. 

**Baselines & evaluation metrics.** As our base VLAs, we choose _π_ 0 _._ 5 [2], a large-scale pretrained model with 3 _._ 5 _B_ parameters, and SmolVLA [30], a comparatively smaller and faster model with 0 _._ 5 _B_ parameters. For both of these VLAs, we use the publicly released fine-tuned weights on LIBERO. We experiment with using our SkipVLA framework on each VLA and report results using different planner algorithms, such as VAMP [6] and cuRoboV2 [7]. 

For evaluation, each method is repeated across 50 trials per task, measuring success rate (SR, %), total successful 

|Policy|SR (%) _↑_|_n_succ|Wall Clock Time (s) _↓_|VLA q _↓_|
|---|---|---|---|---|
|_π_0_._5 (base)|94.7|142|15_._69_±_2_._35 (15_._2)|31_._7_±_4_._7 (31)|
|+ SkipVLA + VAMP|94.7|142|**13**_._**84**_±_**7**_._**07** (11_._0)|26_._5_±_14_._4 (21)|
|+ SkipVLA + cuRoboV2|**95**_._**3**|**143**|17_._84_±_4_._99 (16_._3)|**24**_._**1**_±_**9**_._**9** (21)|
|+ Heuristic Ablation|94.7|142|15_._28_±_6_._02 (13_._2)|31_._4_±_12_._0 (27)|
|SmolVLA (base)|5_._3|8|26_._91_±_7_._40 (23_._7)|45_._0_±_12_._3 (39_._5)|
|+ SkipVLA + VAMP|24_._7|37|**15**_._**29**_±_**9**_._**17** (11_._3)|24_._6_±_15_._8 (17)|
|+ SkipVLA + cuRoboV2|**29**_._**3**|**44**|17_._97_±_8_._02 (15_._1)|**22**_._**8**_±_**12**_._**4** (18_._5)|
|+ Heuristic Ablation|26.7|40|15_._61_±_4_._75 (14_._2)|26_._6_±_7_._8 (25)|


TABLE II: **LIBERO-10 Evaluation.** We evaluate SkipVLA across 3 pick and place tasks in simulation against 2 baselines. We also ablate the indicator heuristics to show the model’s adaptability. We calculate statistics over successful trials only. **Bold** : best; <u>underline:</u> second-best in each backbone block. Numbers shown as Mean _±_ Standard Deviation (Median). 

attempts ( _nsucc_ ), wall-clock time (Wall s), and VLA query count (VLA q). We use a hard limit of 600 environment steps in MuJoCo as a timeout. 

**Results.** We present the results in Tab. I and Tab. II. First, we note that, regardless of the planner, SkipVLA matches the base model’s performance. Across both VLA base models, SkipVLA with VAMP as the planner reduces the wall-clock time by 40% and 27% on LIBERO-object and LIBERO-10, respectively. We also see a proportional drop in the number of VLA queries, indicating that the time reduction is largely due to fewer VLA queries. We also note that SkipVLA shows consistent performance regardless of the planner choice. While cuRoboV2 has a slightly higher success rate, VAMP demonstrates a shorter wall-clock time. 

**Ablation of indicator heuristics.** We provide ablations on the heuristics to identify the task boundary. For this ablation, we use changes in object height as an indicator of the transition between reach-and-place and active manipulation; i.e., a change beyond a threshold denotes the transition. We choose Vamp as the planner. From Tab. I and Tab. II, we observe that the height-based heuristic performs comparably to other configurations, showing the stability of SkipVLA. However, our proposed indicator heuristics with the VAMP planner yield the shortest overall wall clock time, indicating the fastest task completion. 

## _B. Real-World Experiments_ 

**Experiment setup.** To validate our method in the real world, we deployed SkipVLA on a physical 6-DoF YAM manipulator. Our method is tested against two baselines across three tasks in the real world: _π_ 0 _._ 5 [2] and MolmoAct2 [31], each fine-tuned on 50 teleoperated demonstrations per task. 

We evaluate across three top-down pick-and-place tasks of increasing horizon complexity. In addition to success rate, wall-clock time, and VLA query count, we also measure the total energy consumption per trial on the NVIDIA Jetson Thor onboard compute platform. Each task is evaluated over 20 independent trials: 

- **Single-Object:** Put the red block in the box (90-second timeout). 

- **Multi-Object:** Put the red and blue blocks in the box (120-second timeout). 


Fig. 4: Cumulative distribution of success rate (%) vs. wall clock (s) for 3 tasks across _π_ 0 _._ 5, MolmoAct2, _π_ 0 _._ 5 + SkipVLA and MolmoAct2 + SkipVLA measured across 20 trials per task. **(a)** put the red block in the box. **(b)** put both the red and blue blocks in the box. **(c)** stack the 3 blocks in a tower. 

||||**Wall Time (**|**s)** _↓_|**VLA Calls**|_↓_|**Energy (J)**|_↓_|
|---|---|---|---|---|---|---|---|---|
|Task|Policy|SR _↑_|mean_±_std|median|mean_±_std|median|mean_±_std|median|
||_π_0_._5 (base)|**20/20**|19_._81_±_1_._73|20_._33|9_._15_±_0_._75|9|835_._1_±_73_._9|845_._3|
|**Single-Object**<br>|+ SkipVLA (ours)|**20/20**|**14**_._**11**_±_**4**_._**16**|**12**_._**91**|**6**_._**10**_±_**1**_._**55**|**6**|**577**_._**9**_±_**167**_._**1**|**539**_._**0**|
|_Put red block in box_|MolmoAct2 (base)|18_/_20|46_._56_±_9_._53|42_._56|18_._06_±_3_._44|17|1876_._6_±_383_._5|1720_._8|
||+ SkipVLA (ours)|**19/20**|**18**_._**82**_±_**6**_._**27**|**15**_._**93**|**8**_._**16**_±_**2**_._**77**|**7**|**712**_._**1**_±_**236**_._**4**|**610**_._**0**|
||_π_0_._5 (base)|18_/_20|41_._77_±_5_._09|41_._36|17_._89_±_2_._22|18|1727_._0_±_214_._5|1710_._0|
|**Multi-Object**<br>|+ SkipVLA (ours)|**20/20**|**25**_._**53**_±_**3**_._**72**|**24**_._**56**|**11**_._**15**_±_**1**_._**53**|**11**|**1050**_._**8**_±_**146**_._**4**|**1017**_._**0**|
|_Put red & blue in box_|MolmoAct2 (base)|18_/_20|76_._04_±_7_._17|76_._45|29_._00_±_2_._72|29|3236_._8_±_303_._8|3251_._4|
||+ SkipVLA (ours)|**20/20**|**41**_._**66**_±_**9**_._**48**|**39**_._**73**|**17**_._**85**_±_**4**_._**11**|**17**|**1562**_._**2**_±_**355**_._**3**|**1488**_._**1**|
||_π_0_._5 (base)|14_/_20|47_._62_±_11_._91|42_._73|20_._79_±_5_._40|19|1976_._2_±_502_._5|1781_._2|
|**Precision Stacking**<br>|+ SkipVLA (ours)|**17/20**|**36**_._**13**_±_**9**_._**68**|**32**_._**41**|**16**_._**77**_±_**5**_._**41**|**15**|**1631**_._**4**_±_**476**_._**0**|**1429**_._**9**|
|_Stack tower_|MolmoAct2 (base)|9_/_20|87_._13_±_9_._85|85_._26|31_._89_±_3_._59|31|3829_._6_±_792_._3|3621_._2|
||+ SkipVLA (ours)|**11/20**|**58**_._**11**_±_**17**_._**75**|**56**_._**19**|**25**_._**82**_±_**8**_._**12**|**25**|**2167**_._**1**_±_**669**_._**2**|**2112**_._**4**|


TABLE III: **Real-World Evaluation.** We evaluate SkipVLA against two baselines in the real world on a physical 6-DoF YAM robot arm across three tasks (20 trials per task). Statistics for wall-clock time, VLA calls, and energy are calculated only from successful trials. SR higher is better; all other metrics lower is better; **bold** and shading mark the better value within each backbone block. 

- **Multi-Object with precision placing:** Stack three blocks into a tower (120-second timeout). 

**Main results.** Consistent with our simulation results, SkipVLA outperforms both _π_ 0 _._ 5 and MolmoAct2 across all tasks and measured metrics, as shown in Tab. III. Specifically, SkipVLA achieves substantial reductions in execution time across all three tasks: wall-clock completion time decreases by an average of 46 _._ 0% on MolmoAct2 (up to 59 _._ 6%, a 2 _._ 47 _×_ speedup) and 30 _._ 6% on _π_ 0 _._ 5. Concurrently, VLA queries drop by an average of 33 _._ 8% across tasks (reducing calls by over half on MolmoAct2 for single-object), confirming that offloading free-space transit bypasses a large fraction of costly policy evaluations. Crucially, these efficiency gains come with matched or strictly improved success rates on every task: SkipVLA boosts multi-object placement from 90% to a perfect 100% on both backbones, and raises precision stacking success by +15 _._ 0% percentage points for _π_ 0 _._ 5 and +10 _._ 0% percentage points for MolmoAct2. 

Next, in Fig. 4 we report our real-world results as a cumulative distribution that shows the fraction of episodes solved within a given wall-clock budget. As visible from the graphs, SkipVLA encloses a larger area under the curve 

than its baseline counterpart on every task, demonstrating that SkipVLA reaches a higher final success rate within a substantially smaller wall-clock budget. By bypassing the base VLA during free-space transit, the hybrid policy drastically reduces the number of required queries to the generative policies and offloads the work to a lightweight, fast, and efficient CPU-based motion planner (VAMP). 

**Energy comparison.** As shown in Tab. III, SkipVLA is also substantially more energy-efficient on the Jetson Thor compute module, cutting per-trial energy consumption by an average of 52 _._ 4% on MolmoAct2 and 29 _._ 1% on _π_ 0 _._ 5. This confirms that our hybrid approach achieves higher physical throughput with a strictly lighter energy footprint. 

**Additional discussion.** Although SkipVLA was designed primarily to reduce inference latency by minimizing VLA queries, we observe that it also improves task success rates, such as improving SmolVLA from 39 _._ 0% to 82 _._ 0% on LIBERO-OBJECT and improving real-world precision stacking by approximately 20%. We attribute this gain to the planners, which limit compounding errors. 

Imitation learning bounds a policy’s error as _ϵ_ when its state remains within the experts’ distribution. During 

policy rollout, an out-of-distribution shift in state compounds, incurring a cost bounded by _O_ ( _ϵT_<sup>2</sup> ) over task horizon _T_ [32]. In an end-to-end VLA, a small error during free-space transit can displace the robot out of distribution before it reaches the object, causing grasp failures. SkipVLA mitigates this in two ways: first, restricting VLA queries to short activemanipulation segments of length _T_ manip _≪ T_ shrinks the time horizon over which errors compound. Second, by planning collision-free paths directly to a nominal hover pose above the object, the classical planner physically re-anchors the robot to in-distribution initial states before each active-manipulation subtask, preventing error propagation to subsequent subtasks. 

Lastly, SkipVLA in this work is restricted to pick-and-place tasks due to design choices that were outside the scope of this project: the indicator _I_ depends on gripper-state transitions, which assumes that every active-manipulation segment ends in a grasp or release. Future work aims to make SkipVLA generalizable across all tasks by replacing the heuristicbased indicator with a learned, task-conditioned temporal segmentation module. 

## VI. CONCLUSION 

We present SkipVLA, a method for accelerating pretrained VLAs by offloading free-space motion to a classical motion planner. SkipVLA uses the planner to move the robot to a predicted target pose, hands control to the VLA for contactrich skills, and returns control to the planner when the gripper opens or closes. A lightweight scoring head on the frozen vision-language backbone of the VLA selects the target object and is trained from existing demonstrations with labels extracted from gripper events. Compared to _π_ 0 _._ 5 and MolmoAct2 on a physical 6-DoF YAM arm, SkipVLA completes tasks up to 2.5x faster and uses up to less half the energy of the baseline policy, while matching or improving success rate on every task. The speedup of SkipVLA is larger for the slower MolmoAct2 than for _π_ 0 _._ 5 on every task. In simulation, SkipVLA also raises the success rate of SmolVLA significantly on our LIBERO experiments, suggesting that shorter VLA segments limit compounding error. The performance of SkipVLA demonstrates that VLAs can benefit from classical motion planning without retraining the policy. 

## ACKNOWLEDGMENT 

Gemini and Claude assisted with editing and grammar enhancement; all content was verified by the authors. 

## REFERENCES 

- [1] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, et al., “RT2: Vision-language-action models transfer web knowledge to robotic control,” in _Conf. Robot Learn._ , 2023, pp. 2165–2183. 

- [2] K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. R. Equi, et al., “ _π_ 0 _._ 5: A vision-language-action model with openworld generalization,” in _Conf. Robot Learn._ , 2025, pp. 17–40. 

- [3] J. Wen, Y. Zhu, J. Li, M. Zhu, Z. Tang, K. Wu, Z. Xu, et al., “TinyVLA: Toward fast, data-efficient vision-language-action models for robotic manipulation,” _IEEE Robot. Autom. Lett._ , vol. 10, no. 4, pp. 3988– 3995, Apr. 2025. 

- [4] K. Black, M. Y. Galliker, and S. Levine, “Real-time execution of action chunking flow policies,” in _Adv. Neural Inf. Process. Syst._ , 2025, pp. 37 596–37 620. 

- [5] B. Han, J. Kim, and J. Jang, “A dual process VLA: Efficient robotic manipulation leveraging VLM,” _arXiv:2410.15549_ , 2024. 

- [6] W. Thomason, Z. Kingston, and L. E. Kavraki, “Motions in microseconds via vectorized sampling-based planning,” in _IEEE Int. Conf. Robot. Autom._ , 2024, pp. 8749–8756. 

- [7] B. Sundaralingam, A. Murali, and S. Birchfield, “cuRoboV2: Dynamics-aware motion generation with depth-fused distance fields for high-DoF robots,” _arXiv:2603.05493_ , 2026. 

- [8] W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, and L. Fei-Fei, “VoxPoser: Composable 3D value maps for robotic manipulation with language models,” in _Conf. Robot Learn._ , 2023, pp. 540–562. 

- [9] W. Huang, C. Wang, Y. Li, R. Zhang, and L. Fei-Fei, “ReKep: Spatiotemporal reasoning of relational keypoint constraints for robotic manipulation,” in _Conf. Robot Learn._ , 2024, pp. 4573–4602. 

- [10] K. Fang, F. Liu, P. Abbeel, and S. Levine, “MOKA: Open-world robotic manipulation through mark-based visual prompting,” in _Robot.: Sci. Syst._ , 2024. 

- [11] S. Bai, Y. Cai, R. Chen, K. Chen, X. Chen, Z. Cheng, L. Deng, et al., “Qwen3-VL technical report,” _arXiv:2511.21631_ , 2025. 

- [12] Gemma Team, “Gemma 4 technical report,” _arXiv:2607.02770_ , 2026. [13] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, et al., “ _π_ 0: A vision-language-action flow model for general robot control,” in _Robot.: Sci. Syst._ , 2025. 

- [14] D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, et al., “Octo: An open-source generalist robot policy,” in _Robot.: Sci. Syst._ , 2024. 

- [15] A. Prasad, K. Lin, J. Wu, L. Zhou, and J. Bohg, “Consistency Policy: Accelerated visuomotor policies via consistency distillation,” in _Robot.: Sci. Syst._ , 2024. 

- [16] K. Black, A. Z. Ren, M. Equi, and S. Levine, “Training-time action conditioning for efficient real-time chunking,” _arXiv:2512.05964_ , 2025. 

- [17] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _Robot.: Sci. Syst._ , 2023. 

- [18] H. Chen, J. Liu, C. Gu, Z. Liu, R. Zhang, X. Li, X. He, et al., “Fast-in-Slow: A dual-system VLA model unifying fast manipulation within slow reasoning,” in _Adv. Neural Inf. Process. Syst._ , 2025, pp. 108 704–108 738. 

- [19] J. Zhang, Y. Guo, X. Chen, Y.-J. Wang, Y. Hu, C. Shi, and J. Chen, “HiRT: Enhancing robotic control with hierarchical robot transformers,” in _Conf. Robot Learn._ , 2024, pp. 933–946. 

- [20] Q. Bu, H. Li, L. Chen, J. Cai, J. Zeng, H. Cui, M. Yao, et al., “Towards synergistic, generalized, and efficient dual-system for robotic manipulation,” _arXiv:2410.08001_ , 2024. 

- [21] T. Chen, H. Wu, J. Wang, X. Li, and L. Fang, “StreamVLA: Breaking the reason-act cycle via completion-state gating,” _arXiv:2602.01100_ , 2026. 

- [22] T. S. Wilson, W. Thomason, Z. Kingston, and J. D. Gammell, “AORRTC: Almost-surely asymptotically optimal planning with RRT-Connect,” _IEEE Robot. Autom. Lett._ , vol. 10, no. 12, pp. 13 375– 13 382, Dec. 2025. 

- [23] N. Ratliff, M. Zucker, J. A. Bagnell, and S. Srinivasa, “CHOMP: Gradient optimization techniques for efficient motion planning,” in _IEEE Int. Conf. Robot. Autom._ , 2009, pp. 489–494. 

- [24] J. Schulman, Y. Duan, J. Ho, A. Lee, I. Awwal, H. Bradlow, J. Pan, et al., “Motion planning with sequential convex optimization and convex collision checking,” _Int. J. Robot. Res._ , vol. 33, no. 9, pp. 1251–1270, Aug. 2014. 

- [25] Y. Yang, S. Cheng, Y. Fang, H. Bharadhwaj, M. Ding, G. Bertasius, and D. Szafir, “LiLo-VLA: Compositional long-horizon manipulation via linked object-centric policies,” _arXiv:2602.21531_ , 2026. 

- [26] D. B. Choe, S. V. Sangeetha, S. Coogan, and S. Kousik, “Make your VLA more robust without more data by interleaving motion planning,” _arXiv:2606.00985_ , 2026. 

- [27] X. Zhao, W. Ding, Y. An, Y. Du, T. Yu, M. Li, M. Tang, et al., “Fast segment anything,” _arXiv preprint arXiv:2306.12156_ , 2023. 

- [28] C. M. Kim, B. Yi, H. Choi, Y. Ma, K. Goldberg, and A. Kanazawa, “Pyroki: A modular toolkit for robot kinematic optimization,” in _IEEE/RSJ Int. Conf. Intell. Robots Syst._ , 2025. 

- [29] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “LIBERO: Benchmarking knowledge transfer for lifelong robot learning,” in _Adv. Neural Inf. Process. Syst._ , 2023, pp. 44 776–44 791. 

- [30] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, et al., “SmolVLA: A vision-language- 

action model for affordable and efficient robotics,” _arXiv:2506.01844_ , 2025. 

   - [32] S. Ross and D. Bagnell, “Efficient reductions for imitation learning,” in _Int. Conf. Artif. Intell. Statist._ , 2010, pp. 661–668. 

- [31] H. Fang, J. Duan, D. Clay, S. Wang, S. Liu, W. Huang, X. Fan, et al., “MolmoAct2: Action reasoning models for real-world deployment,” _arXiv:2605.02881_ , 2026. 

