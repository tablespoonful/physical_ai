---
title: "Switch: Learning Agile Skills Switching for Humanoid Robots"
date: "2026-04-16"
authors: "Yuen-Fui Lau; Qihan Zhao; Yinhuai Wang; Runyi Yu; Hok Wai Tsui; Qifeng Chen"
url: https://arxiv.org/abs/2604.14834
pdf: https://arxiv.org/pdf/2604.14834
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.14834)** / [論文ページ](https://arxiv.org/abs/2604.14834)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Switch: Learning Agile Skills Switching for Humanoid Robots** 

Yuen-Fui Lau<sup>_∗_</sup> , Qihan Zhao<sup>_∗_</sup> , Yinhuai Wang<sup>_∗_</sup> , Runyi Yu, Hok Wai Tsui Qifeng Chen<sup>_†_</sup> , Ping Tan<sup>_†_</sup> 

The Hong Kong University of Science and Technology 


**Fig. 1:** We introduce **Switch** , a hierarchical whole-body control system that enables humanoid robots to perform agile and seamless skill switching between highly dynamic skills: (a) Get up to Kick; (b) Kick to Lay down; (c) Kungfu to Dance; (d) Get up to Dance. 

**_Abstract_ — Recent advancements in whole-body control through deep reinforcement learning have enabled humanoid robots to achieve remarkable progress in real-world challenging locomotion skills. However, existing approaches often struggle with flexible transitions between distinct skills, creating safety concerns and practical limitations. To address this challenge, we introduce a hierarchical multi-skill system, Switch, enabling seamless skill transitions at any moment. Our approach comprises three key components: (1) a Skill Graph (SG) that establishes potential cross-skill transitions based on kinematic similarity within multi-skill motion data, (2) a whole-body tracking policy trained on this skill graph through deep reinforcement learning, and (3) an online skill scheduler to drive the tracking policy for robust skill execution and smooth transitions. For skill switching or significant tracking deviations, the scheduler performs online graph search to find the optimal feasible path, which ensures efficient, stable, and real-time execution of diverse locomotion skills. Comprehensive experiments demonstrate that Switch empowers humanoid to execute agile skill transitions with high success rates while maintaining strong motion imitation performance.** 

## I. INTRODUCTION 

Recent advances in whole-body motion control, powered by simulation and reinforcement learning, have enabled humanoid robots to perform dynamic real-world skills such as highly agile acrobatics (e.g., flips and kicks) and expressive human-like dances[1–5]. For practical deployment, it is essential that robots not only perform individual skills robustly but also switch between them seamlessly. This paper aims to develop a unified framework for flexible skill switching in humanoid robots. 

Multi-skill execution and switching typically require the existence of common states between skills, which imposes 

> _∗_ Equal contribution _†_ Corresponding author 

significant data requirements. Although using large-scale motion data to train a general whole-body tracking controller [6–9] allows skill switching via goal-conditioned tracking, this approach still relies on pre-defined trajectories with feasible transition states. Otherwise, it may lead to low switching success rate with unnatural movements such as tripping or stumbling [8, 10–13]. Furthermore, due to the open-loop nature of tracking predefined motions, the controller is vulnerable to disturbances: once the tracking error exceeds a certain threshold, stability is compromised, potentially resulting in dangerous and uncontrolled behavior. 

We observe that the main challenge in skill switching comes from poorly modeled transitions between different skills. Since the controller lacks training on these transitions, the robot often fails when encountering such unseen states. One straightforward solution is to collect sufficient motion data that cover all possible inter-skill state-level transitions. However, this approach becomes prohibitively expensive as the number of skills grows, since the required transitions scale combinatorially. To overcome this issue, we propose to establish the connections between motion states by exploring state similarity level across different skills, and use reinforcement learning to learn feasible transitions from such augmented data. Furthermore, instead of tracking a fixed reference trajectory in open-loop, the system should have online replanning capabilities. For example, when the tracking error exceeds a safety threshold, the system should replan a feasible trajectory to recover stable execution rather than allowing error to accumulate until failure. 

Based on these insights, we propose **Switch** , a hierarchical whole-body control system that enables seamless skill switching at any moment (Fig. 2). Our framework consists of three key components: a skill graph as augmented dataset, 

a unified whole-body tracking policy, and an online skill scheduler. Specifically, we treat motion data frames as graph nodes and transitions between frames as directed edges. Given multiple skill sequences, we insert edges between previously disconnected nodes based on similarity, thus automatically creating transition opportunities. For newly added transitions with significant gaps, we insert buffer nodes to enhance switching smoothness and stability. The number of buffer nodes is calculated by the distance between the endpoints of each edge, with larger gaps leading to more buffer nodes. This process significantly enriches and augments the reference motion dataset. We then train a unified tracking policy in simulation to control the robot for executing both the skills and the learned transitions. A buffer-aware imitation mechanism is introduced to train the policy by reinforcement learning with transitions involving these buffer nodes. Finally, an online skill scheduler provides real-time tracking guidance to the policy. When a skill switch is intended or when tracking failure is detected, the scheduler performs real-time motion planning via shortest-path search over the skill graph. This generates new tracking targets to guide the tracking policy toward smooth skill switching or recovery. 

The proposed **Switch** is designed to be versatile across a wide range of locomotion skills, significantly improving both skill transition success rate and execution stability compared to existing methods. Experimental results on the Unitree G1 demonstrate that our system can be successfully deployed in the real world to achieve continuous transitions between dynamic and complex motor skills such as Kung Fu squats, back kicks, and rapid recoveries. 

## II. RELATED WORK 

## _A. Learning-Based Motion Tracking_ 

Learning-based tracking has achieved significant progress in character animation, enabling lifelike whole-body motions by imitating individual references [14–17] or learning universal tracking [18–22]. Recent efforts extend these techniques to real-world robots, focusing on improving accuracy [2, 3, 5, 9, 23], generalization [6, 7, 24–27], and robustness [1, 5, 28]. For accuracy, some works [5, 23] achieve low short-term tracking errors, while CLONE [9] mitigates long-horizon drift by incorporating an LiDAR odometry. UniTracker [7] further improves tracking precision by introducing a fast adaptation module. For generalization, GMT [6] employs MoE to handle diverse motion tracking, while UniTracker leverages a teacher-student framework to enable scalable tracking across thousands of motions. For robustness, SoFTA [28] proposes to use a slow-fast agent design for end-effector control. BeyondMimic [1] enhances robustness by distilling a diffusion model. 

Despite these advancements, inter-sequence transitions remain a challenge, often resulting in inefficiencies or failures during skill switching. To bridge this gap, we introduce short buffer states between pre-linked sequences and propose a method to explicitly learn these transitions. 

## _B. Skill Switching and Sequencing_ 

Skill switching and sequencing have been investigated across animation and robotics through kinematic composition, attractor-based primitives, hierarchical decision layers, and reachability-aware planning. Early work in character animation [29–34] addresses switching by organizing motion data into discrete graphs and local blends. Motion Graphs model a dataset as a directed graph whose nodes are poses or short clips and whose edges are kinematically compatible transitions; long behaviors arise by walking paths on the graph [29]. Parametric Motion Graphs and runtime blending further improve connectivity by interpolating families of motions [35]. While these techniques achieve visually smooth transitions (e.g., via LERP/SLERP interpolation), they operate primarily at the kinematic level and do not guarantee dynamic feasibility or stability on physical robots, revealing a persistent kinematics–dynamics gap. 

In robotics, reusable skills are often encoded as dynamical systems with attractors, as in DMP/SEDS, enabling time/space retargeting and composition with stability guarantees [36, 37]. Geometric formulations such as RMPflow provide principled rules to combine task policies while preserving stability properties [38]. Orthogonally, hierarchical RL abstracts time by letting a high-level policy select among low-level options or subgoals [39], and a large body of work discovers/composes skills (e.g., skill chaining and skill graphs) to handle long-horizon tasks [40, 41]. Bridging selection and planning, PRM-RL admits an edge only if a local controller can reliably traverse it, reducing long-range behavior to graph search over feasible edges [42]. In control, Reference/Command Governors and tube-based MPC adjust or filter targets so that tracking remains within constraints, while viability/capture-basin concepts formalize the set of states from which safe progress is possible [43–45]. 

Building upon these principles, our approach, **Switch** , frames switching as _state-conditioned reference selection_ . Specifically, it uses a short-edge skill graph to provide the tracker with feasible subgoals that lead to the target skill. By combining low-level learned tracking with high-level graph search, **Switch** enables smooth transitions and robust recoveries, even with limited transition data or poorly timed user commands. 

## III. METHOD 

## _A. Building a Skill Graph for Data Augmentation_ 

Training a universal whole-body motion tracker to enable state transitions between different skills is challenging, as it requires massive, often unavailable high-quality motion data. Alternatively, stitching motion trajectories between all pairs of states from different skills leads to convergence issues, especially since transitions between distant state neighborhoods may be physically infeasible. To address these issues, we need to establish a feasible state mapping for each neighborhood as shown in fig. 2(a) and identify physically achievable state for skill switching. 


**Fig. 2:** The **Switch** system: **(a)** We retarget human motion capture skills onto the robot. We then construct a skill graph where frames serve as nodes (solid circles) and temporal transitions as edges (solid arrows). **black** and **gray** represents two different skills. Based on frame similarity, we add additional transitions between different skills (dashed arrows). When the added transition has significant gap, we insert buffer nodes (question marks) to enhance switching feasibility. **(b)** The assembled Skill Graph is used for training a motion tracking policy. During normal operation, imitation rewards measure the distance between simulated results and reference frame. When referencing a buffer node, we measure with its first non-buffer successor node. **(c)** During deployment, users can change skill labels at any time, and our online scheduler plans optimal paths through the skill graph based on the robot’s current state, providing real-time targets to guide the tracking policy. 

_1) Definition of Skill Graph:_ We represent candidate stateto-state transitions with a directed, weighted graph _G_ = ( _V, E, w_ ), with edge weight function _w_ : _E →_ R _≥_ 0. Let Φ = _{ϕ_ 1 _, . . . , ϕK}_ be the set of skills. Each skill _ϕ ∈_ Φ provides a reference sequence _{s_ ˆ<sup>_ϕ_</sup> _t_<sup>_}T_</sup> _t_ =1<sup>_ϕ_,where</sup><sup>_Tϕ_isits</sup> length. We collect all reference states as 


Edges _E_ consist of (a) all consecutive pairs within each reference sequence and (b) cross-skill connections between sufficiently similar states. The meaning of the edge weight _w_ ( _u, v_ ) is phase-dependent and will be instantiated in Sec. III-A.2 (training-time) and Sec. III-C.1 (deploymenttime). 

_2) Construction of Skill Graph:_ 

_a) Training-time edge weight (distance):_ During graph construction we instantiate the edge weight primarily via a state distance. In the local frame (with global _x_ – _y_ translation and yaw/twist removed), define 


We then assign the training-time edge weight as 


_b) Cross-skill connections:_ Sample a source skill _ϕp ∈_ Φ and index _i ∈{_ 1 _, . . . , Tϕp}_ , then connect ˆ _si_<sup>_ϕp_</sup> to its nearest neighbor in a different target skill _ϕq ∈_ Φ ( _ϕq̸_ = _ϕp_ ) under _d_ : 


_B. Training a Whole-Body Tracking Controller in Simulation_ 

_1) Problem Formulation:_ We formalize the multi-skill learning problem as a Markov Decision Process (MDP) _M_ = _⟨S, A, P, r, γ⟩_ , where _s ∈ S_ is the robot state, _a ∈ A_ is the action, _P_ ( _· | s, a_ ) is the state-transition kernel over _S_ , _r_ is the reward function (covering motion imitation and regularization terms), and _γ ∈_ [0 _,_ 1) is the discount factor. At time _t_ , the policy input is _ot_ = _⟨s_<sup>_o_</sup> _t_<sup>_, gt⟩_,where</sup><sup>_so_</sup> _t_<sup>≜</sup> _⟨at_ : _t−n, ft_ : _t−n, qt_ : _t−n, q_ ˙ _t_ : _t−n, ωt_<sup>root</sup> : _t−n_<sup>_⟩_with</sup><sup>_at∈_R23the pre-</sup> vious actions (target joint positions), _ft ∈_ R<sup>3</sup> the body-frame gravity vector, _qt, q_ ˙ _t ∈_ R<sup>23</sup> the joint positions/velocities, and _ω_<sup>root</sup> _∈_ R<sup>3</sup> the root angular velocity. The guidance input is _gt_ = _⟨s_ ˆ<sup>_g_</sup> _t_<sup>_, κt⟩_,where</sup><sup>_s_ˆ</sup><sup>_g_</sup> _t_<sup>=</sup><sup>_p_ˆ</sup><sup>_g_</sup> _t_<sup>encodesreferencelocal</sup> rigid-body positions with _p_ ˆ<sup>_g_</sup> _t_<sup>_∈_R3</sup><sup>_×_23,and</sup><sup>_κt∈_N0is</sup> an integer indicating the remaining number of steps to the end of a buffer segment (set _κt_ = 0 if the target is not a buffer node). The instantaneous reward is _rt_ = _r_ ( _s_<sup>_o_</sup> _t_<sup>_,_ˆ</sup><sup>_s_</sup> _t_<sup>_g_),</sup> and the action _at ∈_ R<sup>23</sup> specifies desired joint positions tracked by a PD controller. Our objective is to learn a robust policy _π_ that enables smooth skill transitions while maintaining high-fidelity motion imitation; given reference sequences _ϕp_ = _{s_ ˆ0<sup>_p, . . . ,_ˆ</sup><sup>_sp_</sup> _Tϕp_<sup>_}_and</sup><sup>_ϕq_=</sup><sup>_{s_ˆ</sup> 0<sup>_q, . . . ,_ˆ</sup><sup>_sq_</sup> _Tϕq_<sup>_}_</sup> from any two skills, we maximize E[<sup>�</sup><sup>_T_</sup> _t_ =0<sup>_−_1</sup><sup>_γt−_1</sup><sup>_rt_].We</sup> adopt Proximal Policy Optimization (PPO) for training. 

_2) Reference State Inititaion:_ Proper task initialization is critical for reinforcement learning (RL) training, and previous works have employed Reference State Initialization (RSI) [2, 14, 46–48] to enhance the learning process. However, directly applying RSI to our augmented motion trajectories hinders the learning of skill transitions when states are sampled uniformly across the entire motion sequence, some sampled states occur after skill transitions, leading to scenarios where the agent fails to experience skill transitions when initialized from these states. To resolve this issue, we modify RSI by only sampling initial states that are _n_ steps before skill transitions. This adjustment ensures that every 

sampled initial state allows the agent to encounter a skill transition during training. 

_3) Buffer-aware Imitation Learning:_ Basic imitation learning methods are constrained by their reliance on explicitly defined reference states for supervision, yet crossskill transition states are often unavailable. Furthermore, their quantity grows polynomially with the number of skills which make data collection prohibitively expensive and their sparsity may render single-step transitions infeasible. To address this, we insert _N_ buffer nodes between states, with the number _N_ determined by the similarity level between the states; these nodes act as temporal buffers to bridge distant transitions, enabling the agent to explore viable paths instead of relying on unavailable predefined reference trajectories. Formally, the motion trajectory is constructed as: 


where _N_ is computed similarly to [49]. Unlike [49], which omits reward computation during the buffer stage, we use the target state _s_ ˆ _j_<sup>_ϕq_</sup> to calculate rewards in this phase as demonstrated in fig. 2(b). This guides the model toward the target state, facilitating convergence and preventing drastic deviations that could cause performance collapse. 

_4) Unified Imitation Rewards:_ We observe that standard imitation rewards underweight high-frequency foot–ground events (e.g., dancing, martial arts), causing the policy to act conservatively and degrade agility and motion fidelity. To explicitly supervise contact events, we add a Foot–Ground Contact Reward (FGR). 

Let _G_ denote the index set of foot end-effectors that can contact the ground (e.g., _G_ = _{_ LF _,_ RF _}_ ). For each _i ∈ G_ and time _t_ , let _c_<sup>ref</sup> _i,t_<sup>_∈{_0</sup><sup>_,_1</sup><sup>_}_bethereferencecontact</sup> label (obtained via self-labeling adapted from [3]) and _ci,t ∈ {_ 0 _,_ 1 _}_ be the measured contact status. We define 


The overall reward function _rt_ is the sum of three components: task rewards for achieving precise whole-body tracking, penalties for preventing undesirable motions, and a regularizations for refining motion. 

_5) Skills Training Curriculum:_ Training a policy to achieve smooth skill transitions in simulation remains challenging, particularly during early stages when the agent lacks prior knowledge of locomotor skills. To address this, we introduce three progressive training curricula for step-by-step learning, ensuring that the agent builds foundational locomotive skills first before tackling complex skill transitions. 

- _Skill Augmentation Curriculum_ initializes with a 10% augmented motion trajectories and 90% of trajectories are single-skill to let the agent focus on learning basic locomotion through consistent single-skill practice. As training progress, the probability is incrementally raised to 50%, systematically increasing demands for exploring and mastering skill transitions. 

**TABLE I:** Reward Specification 

||**Task Rew**|**ard**||
|---|---|---|---|
|Body position|1_._125|VR 3-point|1_._8|
|Body position (feet)|2_._3625|Body rotation|0_._5|
|Body angular velocity|0_._5|Body velocity|0_._5|
|DoF position|0_._75|DoF velocity|0_._5|
|FGR|1_._8|||
||**Penalty**|||
|DoF position limits|_−_10_._0|DoF velocity limits|_−_5_._0|
|Torque limits|_−_5_._0|Termination|_−_200_._0|
||**Regulariza**|**tion**||
|Torques|_−_1_×_10<sup>_−_5</sup>|Action rate|_−_0_._5|


- _Reward Penalty Curriculum_ [2, 7] applies to regularization and penalty terms: it allows the policy to prioritize core tasks (e.g., basic locomotion or singleskill tracking) initially without being overwhelmed by extra constraints. By introducing these components incrementally, the policy can develop more reasonable, well-adjusted behaviors over time, rather than struggling to balance multiple objectives from the start 

- _Termination Curriculum_ [2] terminates episodes when the robot deviates from the reference motion beyond a threshold: starting with a generous threshold, it is gradually tightened to incrementally raise tracking demands, facilitating the learning of agile motions and improving tracking performance. 

_C. Deploy: Online Scheduling with Search-Based Planners_ 

After training, the tracking policy demonstrates seamless tracking of skills and skill switching, while maintaining robustness against certain level of disturbances. Nevertheless, a naive approach that merely follows a predefined motion reference suffers from active runtime controllability [2, 6]. This deficiency becomes particularly problematic when addressing accumulated tracking errors or severe perturbations, as illustrated in Fig. 3b. We therefore employ an _online skill scheduler_ in deployment for switching and safety. When a trigger occurs, it invokes a _planner_ to produce an entry and a path to a target set _T_ , from which we synthesize the reference for the controller. 

_1) Shared Graph Model and Planner Interface:_ In deployment, we reuse the identical skill graph _G_ constructed during training. Reference frames serve as nodes, and directed edges correspond to the transitions established in training. Given that collecting or learning transitions for all _O_ ( _n_<sup>2</sup> ) skill pairs is impractical, this graph acts as a datadriven prior—restricting the planner to search only over edges sampled or synthesized during training. 

Each edge is assigned a nonnegative deployment-time weight _w_ deploy( _u → v_ ) = _c_ ( _u → v_ ). We set _c_ = 1 for consecutive edges (ˆ _s_<sup>_ϕ_</sup> _t → s_ ˆ<sup>_ϕ_</sup> _t_ + 1) within the same skill. For 


**Fig. 3:** Effect of the online skill scheduler. (a) When the robot performs a kicking skill, we apply a 500N disturbance force causing it to fall. This triggers the scheduler to automatically replan based on tracking errors, selecting an appropriate path (utilizing get-up skill segments) to resume the kicking execution. (b) Without the scheduler, tracking errors will gradually amplify and unable to recover. 

cross-skill edges (ˆ _s_<sup>_ϕ_</sup> _i_<sup>_p_</sup> _→ s_ ˆ<sup>_ϕ_</sup> _j_<sup>_q,ϕp̸_=</sup><sup>_ϕq_)weuseadistance-</sup> plus-penalty form: 


where _d_ ( _·, ·_ ) is the state distance defined in Sec. III-A.2 . The total path weight is the sum of edge weights, and planning is posed as a shortest-path-to-set problem on _G_ : 


_a) Graph-Search planner:_ We run a reverse multisource shortest path from _T_ to obtain a value function _V_ and a next-hop map NextHop. Given an entry, the path is reconstructed by iterating NextHop. This global view can leverage overlaps between RoAs e.g., briefly proceeding in the current skill to a nearby feasible state before merging into the target (see Fig. 3). 

_b) Nearest-Neighbor (NN) planner:_ We select the entry by nearest-neighbor similarity (optionally among a small candidate set) and form a single-hop or short-hop transition toward _T_ without global graph search. This planner has minimal latency and a simple implementation; in our hardware deployment we use the NN variant. 

_3) Problem A: Intent-Driven Switching:_ Given a commanded skill, we define the target set as its prefix _T_ cmd (e.g., the first _τ_ fraction of frames) and seek a plan that reaches any _t ∈ T_ cmd with minimum cost. 

_Entry check and selection._ We compute similarity in the local pose–velocity subspace. If sim _≤ A_ , the state lies in a reference RoA and we attach directly. If sim _≥ B_ , we defer switching and enter emergency stop (e-stop). For _A <_ sim _< B_ , we evaluate the top- _k_ candidates by a composite score 


where _V_ is used when the Graph-Search planner is selected; with NN this term is omitted. The scheduler then calls Plan( _G, T_ cmd _, x,_ candidates) and installs the synthesized reference. 

_4) Problem B: Safety Recovery (emergency stop):_ Safety recovery is triggered when safety checks detect excessive divergence either when the similarity _sim ≥ B_ during tracking, or when the best candidate still violates _B_ during entry selection. By default, recovery retains the original 

commanded target set _Tcmd_ . The planner is allowed to route through recovery skills as intermediate segments on the path to _Tcmd_ whenever this yields a lower-cost or safer plan. For the Graph-Search planner, we set _T_ = _Tcmd_ and compute the shortest path, with recovery skills naturally integrated into the path. For the Nearest-Neighbor (NN) planner, if a direct jump toward _Tcmd_ is unsafe, we optionally introduce a recovery target _Trec_ and adopt a two-stage plan: first reach _Trec_ , then re-plan to _Tcmd_ . During e-stop, we override the policy with a damping controller and wait until the system is stationary (e.g. angular velocity of the root below thresholds) before executing the recovery plan. 

_5) Online Skill Scheduling:_ The planner is invoked under four conditions: initialization, a user-commanded target change, approaching the end of the current reference, and safety-threshold events when sim crosses _A_ or _B_ . On a trigger, the scheduler performs the RoA-based entry check, forms candidates, and invokes the selected planner with _T_ = _T_ cmd ( _for the NN planner only_ , if a direct switch toward _T_ cmd is unsafe, we optionally use a two-stage call with a recovery target _T_ rec before returning to _T_ cmd). With Graph Search, caching _V_ and NextHop makes replanning a nearest-neighbor lookup plus pointer chasing; With NN, replanning is just the nearest-neighbor lookup. Both yield low online latency. 

IV. EXPERIMENT 

## _A. Experiment Setup_ 

_1) Hardware Setup:_ We conduct experiments on the Unitree G1 humanoid robot with 29 DoF. The learned policy runs onboard the robot using a Jetson Orin NX. 

_2) Baseline:_ We compare **Switch** with its ablated versions and GMT [6]. 

- Base: The basic RL policy trained on single skill data only using motion tracking method [2]. 

- Base + SG: Trained using motion tracking on Skill Graph-augmented trajectories. 

- Base + SG + B: Trained using motion tracking on Skill Graph-augmented trajectories with buffer states. 

- Base + SG + B + C ( **Switch** ): Trained using motion tracking on Skill Graph-augmented trajectories with buffer states and incorporating Foot-Ground Contact Reward (FGR). 

- GMT [6]: A state-of-the-art general tracking model. 


**Fig. 4:** Quantitative Evaluation of Skill Execution Performance. We analyzes the full-body tracking performance of the proposed **Switch** , alongside baselines ASAP and GMT, under both perturbed and unperturbed conditions. The results show that Switch maintains lower overall full-body tracking errors in single-skill execution experiments regardless of the presence of perturbation demonstraing its robotness to disturbance. Additionally, we also investigate the effectiveness of the Foot-Ground Contact Reward (FGR) on tracking performance. The results shows that it enhance full body motion with a more distinct improvement observed in the lower body motion tracking. 

**TABLE II: Sim2Sim Comparison in MuJoCo** . We compare **Switch** with ablated versions and GMT across three task difficulty levels. **Switch** consistently achieves the highest Skill Switching Success Rate (SSR) and lowest motion errors, highlighting the effectiveness of each component. Here we use SG to represent the skill graph, B for the buffer state inpainting, and C for the foot-ground contact reward. 

|**Method**|SSR (%) _↑_|NR _↑_|Eg-mpbpe _↓_|Empbpe _↓_|Empjpe _↓_|Empjve _↓_|Empbve _↓_|Empbae _↓_|
|---|---|---|---|---|---|---|---|---|
|**_Easy_**|||||||||
|GMT [6]|30.00|2.636|0.396|0.392|0.295|1.420|**0.391**|**5.651**|
|Base|2.00|4.520|0.120|0.118|0.307|**1.310**|0.398|6.669|
|Base + SG|**100.0**|5.802|0.115|0.121|0.241|1.489|0.451|7.883|
|Base + SG + B|**100.0**|6.629|0.087|0.092|**0.213**|1.472|0.446|8.089|
|Base + SG + B + C (**Switch**)|**100.0**|**7.029**|**0.075**|**0.078**|0.220|1.483|0.454|8.026|
|**_Medium_**|||||||||
|GMT [6]|10.00|2.531|0.491|0.486|0.304|1.476|0.397|**5.681**|
|Base|2.00|4.505|0.120|0.120|0.307|**1.275**|**0.393**|6.560|
|Base + SG|**100.0**|5.175|0.147|0.151|0.255|1.464|0.460|7.734|
|Base + SG + B|**100.0**|6.128|0.103|0.106|**0.214**|1.492|0.459|8.304|
|Base + SG + B + C (**Switch**)|**100.0**|**6.616**|**0.090**|**0.098**|0.223|1.484|0.475|7.778|
|**_Hard_**|||||||||
|GMT [6]|2.00|2.877|0.588|0.591|0.236|**1.400**|**0.405**|**6.062**|
|Base|2.00|3.570|0.251|0.253|0.306|1.630|0.468|6.416|
|Base + SG|**100.0**|5.091|0.146|0.150|0.246|1.531|0.469|8.129|
|Base + SG + B|**100.0**|6.015|0.105|0.105|**0.213**|1.446|0.460|8.078|
|Base + SG + B + C (**Switch**)|**100.0**|**6.284**|**0.098**|**0.093**|0.225|1.458|0.463|7.909|


_3) Evaluation Tasks:_ We evaluate the policy’s tracking performance using a motion dataset that encompasses 4 distinct skills. Skill transitions are categorized into three difficulty levels, easy, medium, and hard, based on their number of transition to perform. Specifically, an ”easy” transition refers to switching between skills once, a ”medium” transition involves switching skills twice, and a ”hard” transition refers switching skills three times. For each of these difficulty settings, the policies are trained in IsaacGym and subsequently evaluated in MuJoCo [50] over 50 trials each. 

_4) Evaluation Metric:_ We employ a set of metrics to assess both the skill transition effectiveness and motion imitation accuracy of the proposed method. First, the Skill 

Switching Success Rate (SSR) quantifies the percentage of successful target skill transitions when the policy is initialized from an arbitrary state different from the target skill; a transition is deemed unsuccessful if the average body position error relative to the root frame exceeds 0.5 meters at any point during imitation. Second, the Normalized Reward (NR) calculates the average reward per frame, formulated as _NR_ = _T_ <u>1</u> � _Tt_ =0 _−_ 1<sup>_r_¯</sup><sup>_t_where</sup><sup>_r_¯</sup><sup>_t_denotesthenormalized</sup> reward at time _t_ and _T_ is the total number of frames processed. Additionally, we evaluate motion imitation fidelity via multiple tracking error metrics: Global Mean Per Body Position Error ( _E_ g-mpbpe, in meters), Root-Relative Mean Per Body Position Error ( _E_ mpbpe, in meters), Mean Per Joint 


**Fig. 5: Skill switching success rate under perturbation.** The perturbation is random 25 N pushes in simulation. 


**Fig. 6:** Visual comparisons of skill execution (wo/Perturbation) across different methods in dancing which requires high-frequency foot-ground contact. **Switch** demonstrates more coordinated lowerbody movement and attains better foot-ground interaction while ASAP [2] and GMT [6] exhibit conservative and jerky lower body motions, particularly when agile movements are required. 

_2) Performance in Skills Execution:_ In terms of performance on skill execution, **Switch** maintains the lowest errors in key metrics across most difficulty levels. From Table II, its Global Mean Per Body Position Error is 0.075m (Easy), 0.090m (Medium), and 0.098m (Hard), substantially lower than GMT’s 0.396m, 0.491m, and 0.588m, and also outperforming Base + SG + B (0.087m, 0.103m, 0.105m). Similarly, Switch achieves the smallest Root-Relative Mean Per Body Position Error (0.078m, 0.098m, 0.093m), reflecting precise whole-body motion alignment with reference trajectories. The improvement is particularly pronounced in lower-body motion as shown in Figure 6, which demonstrates Switch’s more coordinated lower-body movements compared to GMT [6] and ASAP [2]. Critically, even in the Hard difficulty level (involving three consecutive skill switches) as shown in Figure 4, Switch retains low tracking errors, demonstrating its robustness to perturbation and escalating task complexity. 

_3) Effectiveness of Foot-Ground Contact Reward:_ To investigate the impact of the Foot-Ground Contact Reward (FGR) on motion tracking, we compared the upper and lower body motion tracking performance for individual skills by assessing our policy trained both with and without FGR. From Figure 4, we found that when FGR is incorporated, the tracking performance improves, with the lower body exhibiting a more pronounced enhancement . This is attributed to the fact that the foot-ground contact reward directly strengthens the interaction between the robot’s lower body and the ground, refining the precision of lower-body motion. Figure 6 presents the qualitative comparsion between **Switch** and other motion tracking baseline. It can be observed that **Switch** achieves better foot-ground contact compared to GMT and ASAP on agile skill execution such as dancing, and demonstrates stable, high-fidelity motion imitation. 

## V. CONCLUSION 

Position Error ( _E_ mpjpe, in radians), Mean Per Joint Velocity Error ( _E_ mpjve, in radians per frame), Mean Per Body Velocity Error ( _E_ mpbve, in meters per frame), and Mean Per Body Acceleration Error ( _E_ mpbae, in meters per frame<sup>2</sup> ). 

## _B. Experimental Results_ 

_1) Performance in Skills Switching:_ As summarized in Table II, **Switch** (denoted as Base + SG + B + C) achieves consistent and superior performance across all difficulty levels, outperforming all compared baselines. Regarding SSR, the Base model, trained solely on single-skill data stagnates at a mere 2.00% across all levels, failing to execute even simple skill switching. The state-of-the-art general tracking model GMT [6] exhibits a drastic decline in SSR with increasing difficulty, dropping from 30.00% (Easy) to 2.00% (Hard), showing the limitation of general tracking model’s reliance on pre-defined trajectories with feasible transition states in skill switching tasks. In contrast, models integrating the Skill Graph (SG) (Base + SG, Base + SG + B, **Switch** ) attain a perfect 100% SSR across all levels, proving the effectiveness of SG in enabling cross-skill transitions learning. 

In this paper, we propose **Switch** , which addresses the critical challenge of multi-skill switching in humanoid robots by integrating a Skill Graph for data augmentation, a reinforced whole-body tracking controller with buffer states and foot-ground contact optimization, and an online scheduler for real-time planning. Unlike baselines that struggle with increasing task difficulty or perturbations, Switch achieves 100% SSR across all skill switching levels, maintains low tracking errors, and autonomously recovers from disturbances, demonstrating its ability to enable agile, seamless skill execution and laying a foundation for practical deployment of humanoid robots in dynamic real-world scenarios. 

## REFERENCES 

- [1] T. E. Truong, Q. Liao, X. Huang, G. Tevet, C. K. Liu, and K. Sreenath, “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

- [2] T. He et al., “Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” _arXiv preprint arXiv:2502.01143_ , 2025. 

- [3] W. Xie et al., “Kungfubot: Physics-based humanoid wholebody control for learning highly-dynamic skills,” _arXiv preprint arXiv:2506.12851_ , 2025. 

- [4] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” _arXiv preprint arXiv:2402.16796_ , 2024. 

- [5] M. Ji et al., “Exbody2: Advanced expressive humanoid whole-body control,” _arXiv preprint arXiv:2412.13196_ , 2024. 

- [6] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang, “Gmt: General motion tracking for humanoid whole-body control,” _arXiv preprint arXiv:2506.14770_ , 2025. 

- [7] K. Yin et al., “Unitracker: Learning universal whole-body motion tracker for humanoid robots,” _arXiv preprint arXiv:2507.07356_ , 2025. 

- [8] T. He et al., “Omnih2o: Universal and dexterous human-tohumanoid whole-body teleoperation and learning,” _arXiv preprint arXiv:2406.08858_ , 2024. 

- [9] Y. Li et al., “Clone: Closed-loop whole-body humanoid teleoperation for long-horizon tasks,” _arXiv preprint arXiv:2506.08931_ , 2025. 

- [10] T. He et al., “Learning human-to-humanoid real-time whole-body teleoperation. in 2024 ieee,” in _RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 8944–8951. 

- [11] X. Cheng, J. Li, S. Yang, G. Yang, and X. Wang, “Open-television: Teleoperation with immersive active visual feedback,” _arXiv preprint arXiv:2407.01512_ , 2024. 

- [12] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” _arXiv preprint arXiv:2406.10454_ , 2024. 

- [13] C. Lu et al., “Mobile-television: Predictive motion priors for humanoid whole-body control,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , IEEE, 2025, pp. 5364–5371. 

- [14] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, 2018. 

- [15] Y. Wang, J. Lin, A. Zeng, Z. Luo, J. Zhang, and L. Zhang, “Physhoi: Physics-based imitation of dynamic human-object interaction,” _arXiv preprint arXiv:2312.04393_ , 2023. 

- [16] M. Xu, Y. Shi, K. Yin, and X. B. Peng, “Parc: Physics-based augmentation with reinforcement learning for character controllers,” in _Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Papers_ , 2025, pp. 1–11. 

- [17] Y. Wang et al., “Skillmimic: Learning basketball interaction skills from demonstrations,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 17 540–17 549. 

- [18] Z. Luo, J. Cao, K. Kitani, W. Xu, et al., “Perpetual humanoid control for real-time simulated avatars,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2023, pp. 10 895–10 904. 

- [19] Z. Luo et al., “Universal humanoid motion representations for physics-based control,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [20] S. Xu, H. Y. Ling, Y.-X. Wang, and L.-Y. Gui, “Intermimic: Towards universal whole-body control for physics-based human-object interactions,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 12 266–12 277. 

- [21] C. Tessler, Y. Guo, O. Nabati, G. Chechik, and X. B. Peng, “Maskedmimic: Unified physics-based character control through masked motion inpainting,” _ACM Transactions on Graphics (TOG)_ , vol. 43, no. 6, pp. 1–21, 2024. 

- [22] C. Tessler, Y. Jiang, E. Coumans, Z. Luo, G. Chechik, and X. B. Peng, “Maskedmanipulator: Versatile whole-body control for locomanipulation,” _arXiv preprint arXiv:2505.19086_ , 2025. 

- [23] Y. Ze et al., “Twist: Teleoperated whole-body imitation system,” _arXiv preprint arXiv:2505.02833_ , 2025. 

- [24] Y. Shao et al., “Langwbc: Language-directed humanoid whole-body control via end-to-end learning,” _arXiv preprint arXiv:2504.21738_ , 2025. 

- [25] Y. Wang et al., “From experts to a generalist: Toward general wholebody control for humanoid robots,” _arXiv preprint arXiv:2506.12779_ , 2025. 

- [26] H. Xue et al., “Leverb: Humanoid whole-body control with latent vision-language instruction,” _arXiv preprint arXiv:2506.13751_ , 2025. 

- [27] Y. Wang et al., “Humanx: Toward agile and generalizable humanoid interaction skills from human videos,” _arXiv preprint arXiv:2602.02473_ , 2026. 

      - _Whole-body Control and Bimanual Manipulation: Applications in Humanoids and Beyond_ . 

   - [29] L. Kovar, M. Gleicher, and F. Pighin, “Motion graphs,” _ACM Transactions on Graphics (TOG)_ , vol. 21, no. 3, pp. 473–482, 2002. 

   - [30] R. Heck and M. Gleicher, “Parametric motion graphs,” in _Proceedings of the 2007 Symposium on Interactive 3D Graphics and Games (I3D)_ , ACM, 2007, pp. 129–136. 

   - [31] L. Zhao and A. Safonova, “Achieving good connectivity in motion graphs,” in _Eurographics/SIGGRAPH Symposium on Computer Animation (SCA)_ , Eurographics Association, 2008, pp. 127–136. 

   - [32] P. Beaudoin, S. Coros, M. van de Panne, and P. Poulin, “Motionmotif graphs,” in _Eurographics/SIGGRAPH Symposium on Computer Animation (SCA)_ , Eurographics Association, 2008, pp. 117–126. 

   - [33] P. S. A. Reitsma and N. S. Pollard, “Evaluating motion graphs for character animation,” _ACM Transactions on Graphics (TOG)_ , vol. 26, no. 4, 18:1–18:es, 2007. 

   - [34] L. Kovar and M. Gleicher, “Automated extraction and parameterization of motions in large data sets,” _ACM Transactions on Graphics (TOG)_ , vol. 23, no. 3, pp. 559–568, 2004. 

   - [35] R. Heck and M. Gleicher, “Parametric motion graphs,” in _Proceedings of the 2007 symposium on Interactive 3D graphics and games_ , 2007, pp. 129–136. 

   - [36] A. J. Ijspeert, J. Nakanishi, H. Hoffmann, P. Pastor, and S. Schaal, “Dynamical movement primitives: Learning attractor models for motor behaviors,” _Neural computation_ , vol. 25, no. 2, pp. 328–373, 2013. 

   - [37] S. M. Khansari-Zadeh and A. Billard, “Learning stable nonlinear dynamical systems with gaussian mixture models,” _IEEE Transactions on Robotics_ , vol. 27, no. 5, pp. 943–957, 2011. 

   - [38] C.-A. Cheng et al., “Rmp flow: A computational graph for automatic motion policy generation,” in _International Workshop on the Algorithmic Foundations of Robotics_ , Springer, 2018, pp. 441–457. 

   - [39] R. S. Sutton, D. Precup, and S. Singh, “Between mdps and semimdps: A framework for temporal abstraction in reinforcement learning,” _Artificial intelligence_ , vol. 112, no. 1-2, pp. 181–211, 1999. 

   - [40] G. Konidaris and A. Barto, “Skill discovery in continuous reinforcement learning domains using skill chaining,” _Advances in neural information processing systems_ , vol. 22, 2009. 

   - [41] A. Bagaria, J. K. Senthil, and G. Konidaris, “Skill discovery for exploration and planning using deep skill graphs,” in _International conference on machine learning_ , PMLR, 2021, pp. 521–531. 

   - [42] A. Faust et al., “Prm-rl: Long-range robotic navigation tasks by combining reinforcement learning and sampling-based planning,” in _2018 IEEE international conference on robotics and automation (ICRA)_ , IEEE, 2018, pp. 5113–5120. 

   - [43] A. Bemporad, “Reference governor for constrained nonlinear systems,” _IEEE Transactions on Automatic Control_ , vol. 43, no. 3, pp. 415–419, 2002. 

   - [44] S. Rakovi´c and D. Mayne, “A simple tube controller for efficient robust model predictive control of constrained linear discrete time systems subject to bounded disturbances,” _IFAC proceedings volumes_ , vol. 38, no. 1, pp. 241–246, 2005. 

   - [45] J.-P. Aubin, A. M. Bayen, and P. Saint-Pierre, _Viability theory: new directions_ . Springer Science & Business Media, 2011. 

   - [46] T. Haarnoja et al., “Learning agile soccer skills for a bipedal robot with deep reinforcement learning,” _Science Robotics_ , vol. 9, no. 89, eadi8022, 2024. 

   - [47] T. He et al., “Hover: Versatile neural whole-body controller for humanoid robots,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , IEEE, 2025, pp. 9989–9996. 

   - [48] X. B. Peng, Y. Guo, L. Halper, S. Levine, and S. Fidler, “Ase: Largescale reusable adversarial skill embeddings for physically simulated characters,” _ACM Transactions On Graphics (TOG)_ , vol. 41, no. 4, pp. 1–17, 2022. 

   - [49] R. Yu et al., “Skillmimic-v2: Learning robust and generalizable interaction skills from sparse and noisy demonstrations,” in _Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Papers_ , 2025, pp. 1–11. 

   - [50] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control,” in _2012 IEEE/RSJ international conference on intelligent robots and systems_ , IEEE, 2012, pp. 5026–5033. 

- [28] Y. Li et al., “Hold my beer: Learning gentle humanoid locomotion and end-effector stabilization control,” in _RSS 2025 Workshop on_ 

