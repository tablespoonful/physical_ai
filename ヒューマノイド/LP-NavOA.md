---
title: "LP-NavOA: Integrated Local Navigation and Obstacle Avoidance for Humanoid Robots under Limited Perception"
date: "2026-06-22"
authors: "Yukun Luo; Jianjun Ma; Yuyao Min; Jinzhe Li; Kaihong Huang; Peng Li"
url: https://arxiv.org/abs/2606.23249
pdf: https://arxiv.org/pdf/2606.23249
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.23249)** / [論文ページ](https://arxiv.org/abs/2606.23249)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# LP-NavOA: Integrated Local Navigation and Obstacle Avoidance for Humanoid Robots under Limited Perception 

1<sup>st</sup> Yukun Luo 2<sup>nd</sup> Jianjun Ma 3<sup>rd</sup> Yuyao Min _College of Intelligence Science and Technology College of Intelligence Science and Technology College of Intelligence Science and Technology National University of Defense Technology National University of Defense Technology National University of Defense Technology_ Changsha, China Changsha, China Changsha, China 4<sup>th</sup> Jinzhe Li 5<sup>th</sup> Kaihong Huang 6<sup>th</sup> Peng Li _College of Intelligence Science and Technology College of Intelligence Science and Technology College of Intelligence Science and Technology National University of Defense Technology National University of Defense Technology National University of Defense Technology_ Changsha, China Changsha, China Changsha, China 

**_Abstract_ —Humanoid local navigation in cluttered environments must jointly resolve obstacle avoidance, sparse-goal recovery, and stable whole-body locomotion under short-range and partially observable sensing. Explicit planner-control decompositions introduce latency and can mismatch agile humanoid command-tracking limits, while purely reactive controllers may lose the goal after obstacle occlusion. We present LP-NavOA, a limited-perception navigation and obstacle-avoidance framework for humanoid robots. A raycast-conditioned perceptionaction proximal policy optimization (PPO) locomotion backbone is first trained with a robot-centered circular heading-speed command and a shared command-side safety filter. With this backbone frozen, A-star and waypoint teachers generate rollouts for distilling a recurrent local planner that overwrites only the heading command at deployment, leaving the whole-body policy intact. At runtime, LP-NavOA uses proprioception, shortrange local range sensing, and a body-frame goal direction, requiring no global map, waypoint stream, or external planner. In MuJoCo open-wall and indoor layouts, the distilled planner produces obstacle bypassing and post-avoidance goal recovery, raising teacher-calibrated on-time arrival from 38–40% to 85– 97% and reducing brush/contact-heavy progress relative to a backbone-only controller. Ablations show that dynamic route shaping, teacher-active data collection, and the circular command interface are important for navigation efficiency and for training the 3.0 m/s backbone. A Unitree G1 deployment analysis demonstrates hardware executability without continuous joystick steering.** 

**_Keywords_ —humanoid robot, local navigation, obstacle avoidance, limited perception, reinforcement learning** 

### I. INTRODUCTION 

Humanoid robots fit human-scale spaces, but local navigation is tightly coupled with whole-body locomotion. A policy must decide when to walk, turn, slow down, or return toward a hidden goal while preserving balance and contact quality. Under partial observability [1], short-range sensing may reveal an obstacle without resolving when to continue bypassing or resume goal seeking. 

Classical pipelines separate mapping, planning, and control with explicit planners such as A-star and dynamic win- 

dows [2], [3]. These interfaces are interpretable but awkward for agile legged systems, where simplified planning abstractions meet latency, body sway, and command-tracking limits. Learned navigation systems have reduced some of these costs [4]–[6], and recent work extends the same trend to humanoid visual navigation [7]. In parallel, reinforcement learning has produced robust legged locomotion under increasingly realistic dynamics, from agile motor skills [8] to blind locomotion over challenging terrain [9] and perceptive locomotion in the wild [10]. Rapid motor adaptation pushes this line further by handling unmodelled dynamics directly at deployment [11], a property that humanoid systems have begun to inherit alongside real-world whole-body control [12], expressive whole-body tracking [13], and large-scale imitation from human motion [14]. Scalable simulators such as Isaac Gym have made massively parallel training practical [15], with curricula that learn to walk in minutes [16]; lightweight MuJoCo-based systems such as mjlab further expose managerbased robot-learning workflows for GPU-accelerated policy training [17]. Building on this style of simulation infrastructure, recent studies pursue collision-free high-speed locomotion [18], extreme parkour [19], and rapid-locomotion benchmarks [20]. Yet goal-directed local navigation still requires recovering the sparse goal after avoidance, not only reacting to the nearest obstacle. 

We separate _training instruments_ from the _inference interface_ . Planners, privileged scans, and waypoint curricula generate safe supervision, but the deployed controller keeps only raycast and goal-direction inputs. A proximal policy optimization (PPO) backbone learns a compact heading-speed command [21]; frozen-backbone rollouts under planner or waypoint teachers then provide behavior-cloning data for a recurrent local planner [22]–[24]. The result is a compact steering layer that preserves the learned locomotion interface while adding memory-based decisions about when to bypass an obstacle and when to recover the sparse goal. 

LP-NavOA makes three contributions: 

where superscripts _b_ and _w_ denote body and world frames, _ωt_<sup>_b_isbodyangularvelocity,</sup><sup>_g_</sup> _t_<sup>_b_isgravityprojectedintothe</sup> body frame, _qt − q_ 0 and _q_ ˙ _t_ are joint offsets and velocities, _at−_ 1 is the previous normalized action, and _bt_ is the gait/order phase feature. The tensors _ρ_<sup>_f_</sup> _t_<sup>_, ρℓ_</sup> _t_<sup>_, ρ_</sup> _t_<sup>_r∈_[0</sup><sup>_,_1]8</sup><sup>_×_8are front, left,</sup> and right normalized raycast grids; smaller entries are nearer obstacles and 1 is the 4 m range limit. The PD controller receives _qt_<sup>des</sup> = _q_ 0 + _sa ⊙ at_ , with nominal pose _q_ 0, perjoint scale _sa_ , elementwise product _⊙_ , and normalized joint action _at ∈_ [ _−_ 1 _,_ 1]<sup>_D_</sup> , where _D_ is the action dimension. The critic is asymmetric and additionally observes a yaw-aligned downward terrain scan during training. 

- We design a planner-free limited-perception navigation interface that uses local range observations and goal state to steer a frozen whole-body locomotion foundation policy through heading commands. 

- We introduce a planner-supervised training pipeline that combines circular heading-speed PPO, waypoint/planner supervision, dynamic route shaping, and teacher-active rollouts to distill obstacle bypassing and post-avoidance goal recovery into the deployment policy. 

- We validate the system in MuJoCo open-wall and indoor layouts with timing, brush/contact, and collision diagnostics, and include a Unitree G1 deployment-feasibility check of the compact interface. 

_1) Circular goal command:_ The command must teach smooth goal-directed locomotion before navigation teachers are introduced. We therefore sample the target heading around the current robot yaw, 

### II. METHOD 

### _A. Framework Overview: Planner-Supervised Training and Planner-Free Inference_ 


We consider a Unitree G1 humanoid in MuJoCo that must reach sparse planar goals in unknown static-obstacle layouts using only proprioception, short-range raycasts, and relative goal direction at deployment. Three information boundaries define the system. The locomotion backbone _πθ_ ( _at | o_<sup>ll</sup> _t_<sup>_, ct_)</sup> maps proprioception, raycasts, and _ct_ = [∆ _ψt, vt_<sup>_∗_]tonormal-</sup> ized joint action _at_ . Training-time teachers provide intermediate waypoints for curricula and data collection. A recurrent local planner _fϕ_ ( _ot_<sup>lp</sup><sup>_, ht−_1)predictsaboundedsteeringcom-</sup> mand from inference-time observations and recurrent memory _ht−_ 1, then overwrites only the heading component. The two learning stages are 

_−_ and the policy receives [∆ _ψt, vt_<sup>_∗_] with ∆</sup><sup>_ψt_= wrap(</sup><sup>_θ_</sup> _t_<sup>_w,_cmd</sup> _ψt_ ). Here _ψt_ and _p_<sup>_w_</sup> _t_<sup>are robot yaw and planar world position,</sup> _p_<sup>_w,_</sup> _t_<sup>goal</sup> is the sampled goal point, _U_ ( _a, b_ ) is a uniform sample, _R_ is the goal radius, and _θ_ max bounds the angular spread around the robot heading. The wrap operation makes ∆ _ψt_ the signed shortest heading error in [ _−π, π_ ]. This converts sparse goal tracking into heading-and-speed tracking; obstacle curricula later reuse the same two-dimensional interface [25]. 

_2) Rewards, safety filter, and teacher-active curricula:_ Tracking targets are _ωt_<sup>_∗_=clip(</sup><sup>_kψ_∆</sup><sup>_ψt, −ω_max</sup><sup>_, ω_max)and</sup> _vt_<sup>_∥_=</sup><sup>_v_</sup> _t_<sup>_x_cos ∆</sup><sup>_ψt_+</sup><sup>_v_</sup> _t_<sup>_y_sin ∆</sup><sup>_ψt_,withexponentialrewardsfor</sup> yaw-rate and goal-directed velocity tracking. Here _kψ_ maps heading error to yaw-rate command, _ω_ max is the yaw-rate limit, ( _vt_<sup>_x, v_</sup> _t_<sup>_y_)isplanarbasevelocityintheheadingframe,</sup> _vt_<sup>_∥_isitscomponentalongthecommandedgoaldirection,</sup> and _vt_<sup>_∗_isthetargetspeed.Acommand-sidesafetyfiltercaps</sup> forward speed from front-ray stopping time and damps unsafe yaw commands. It is shared by all inference conditions, so comparisons measure steering rather than low-level emergency logic. The reachable-goal curriculum is staged: flat circulargoal locomotion first learns the command interface, A-starguided visual generalization then introduces obstacle bypassing through intermediate waypoints, and an optional final stage adapts the same policy to rougher terrain. Across these stages, teachers may change the commanded heading, but the policy still sees only [∆ _ψt, vt_<sup>_∗_].</sup> 


where _θ_ and _ϕ_ are backbone and planner parameters, _γ_ is the discount factor, _rt_<sup>llisthelocomotionreward,and</sup><sup>_Dπ_</sup> _θ_<sup>is</sup> collected by rolling out the frozen backbone under teachers. Each dataset sample contains _o_<sup>lp</sup> _t_<sup>,recurrentstate,andteacher</sup> label _yt_ , equal to ∆ _ψt_<sup>_∗_forodometryand[∆</sup><sup>_ψ_</sup> _t_<sup>_∗, v_</sup> _t_<sup>_x_]fordead</sup> reckoning, where _vt_<sup>_x_isforwardbody-framevelocity;</sup><sup>_ℓ_isthe</sup> masked behavior-cloning error. The first stage learns _how_ to walk under commands; the second learns _which_ heading command to send without planner waypoints. Fig. 1 summarizes this deployment interface: planner and waypoint information is absent at runtime, the local planner reads only deploymentavailable observations and recurrent state, and its output modifies the heading component before the shared command-side safety filter passes the command to the frozen PPO backbone. 

### _C. Teacher-Distilled Local Planner for Goal Recovery_ 

After the backbone is frozen, the local planner chooses the heading command from goal direction, local raycasts, and short-horizon memory [1]. It addresses the gap left by pure reactive avoidance: deciding when to bypass and when to return toward the sparse goal. The student observes only inference-time signals, 

### _B. Perception-Action PPO Training for the Locomotion Backbone_ 

The first stage trains a perception-action locomotion policy rather than a global planner. The actor maps proprioception, three local raycast views, and the compact command to wholebody joint targets: 


## **Planner-Free Inference: Heading-Only Injection into a Frozen PPO Backbone** 


Fig. 1. Planner-free inference interface of LP-NavOA. The recurrent steering module overwrites only the heading command, while the frozen PPO backbone converts the filtered command and local observations into full-body joint targets. 

where _ηt_ = [cos _ψt,_ sin _ψt_ ] encodes yaw, _νt_ is selected joint velocities (DR) or measured body-frame velocity (odometry), and _ξt_ stores the body-frame offset to the current key goal, divided by 10, plus unit bearing (cos _βt,_ sin _βt_ ), with _βt_ = atan2( _d_<sup>_y_</sup> _b,t_<sup>_, d_</sup> _b,t_<sup>_x_).Raycastfeaturesarefusedwiththe</sup> state by a multilayer perceptron (MLP) and gated recurrent unit (GRU) [26]: 


Here _s_ indexes front/left/right raycast groups, _Eρ_ is the shared CNN encoder, and _zt_<sup>_s_isits32-Drangefeature,</sup><sup>_φ_</sup> is the fusion MLP, _ht ∈_ R<sup>48</sup> is recurrent memory, and _Wψ_ is the yaw-output head. The tanh bound limits ∆<sup>�</sup> _ψt_ to [ _−_ ∆ _ψ_ max _,_ ∆ _ψ_ max], where ∆ _ψ_ max is the maximum steering angle. The dead-reckoning variant also predicts forward velocity for goal integration; the odometry variant removes that head. 

_1) Route-shaping teacher control:_ For distillation, the frozen backbone is rolled out under planner or waypoint teachers. The active waypoint is the intermediate bypass target; the key goal is the sparse task goal recovered after avoidance. The teacher target blends their signed body-frame bearings: 


The gate _αt ∈_ [0 _,_ 1] uses the same raycasts: _αt_ = 0 selects the bypass waypoint and _αt_ = 1 selects the key goal. Let _d_ max = 4 m, _d_<sup>_f_</sup> _t_<sup>=</sup><sup>_d_maxmin</sup><sup>_ρf_</sup> _t_<sup>be forward clearance, and</sup><sup>_d_gs</sup> _t_ 

the minimum left/right clearance on the key-goal side. In the default distance-based mode, 


where _σ_ is the logistic sigmoid, _kα_ is transition sharpness, _d_ turn is the release clearance, and _d_ block is the goal-side blocking threshold. The raw gate is smoothed with an asymmetric EMA _αt_ = _αt−_ 1 + _µt_ ( _αt_<sup>raw</sup> _− αt−_ 1), _µt_ = _µ_ up if _αt_<sup>raw</sup> _>αt−_ 1 else _µ_ down, which reduces label chatter. The gate _αt_ is close to zero when the waypoint should dominate near an obstacle and moves toward one when clearances permit direct keygoal recovery. These quantities define both the supervised yaw target and, by default, the heading command injected into the frozen backbone during data collection. Thus _αt_ shapes the rollout route rather than merely renaming labels; the student never observes _αt_ and is trained with masked recurrent behavior cloning. Fig. 2 explains the resulting supervision trade-off. Waypoint-only control keeps the label tied to teacher waypoints, so the student can replay a teacher-route template when those points are absent instead of grounding avoidance in the observed obstacle geometry. Key-goal-only control points through blocked space and provides no bypass supervision. Dynamic route shaping addresses both failure modes by using waypoint bearing only as an obstacle-conditioned bypass cue and releasing toward the sparse goal when clearance opens. 


Fig. 2. Route-shaping teacher control in the open-wall setting. Waypoint-only supervision can become route-template replay when teacher points are unavailable, while key-goal-only supervision gives no bypass target. The dynamic target ties bypassing to observed obstacle clearance and then releases the command toward sparse-goal recovery. 

### III. EXPERIMENTS 

### _A. Command-Form Ablation for Fast Backbone Training_ 

Before evaluating navigation, we test whether the command interface can train the fast locomotion primitive that the later planner relies on. The flat-terrain PPO ablation changes only the goal-command generator: it tests whether fixed worldframe waypoints can train the high-speed tracking skill needed by the later navigation stack. 

The _circular_ condition uses the robot-centered command in (3), so the target remains a local heading and speed command as the robot moves. The _fixed-sequence_ condition replaces it with four world-frame goals at nominal offsets (0 _,_ 2 _._ 5), (0 _,_ 5 _._ 0), (0 _,_ 7 _._ 5), (0 _,_ 10 _._ 0) m, each scattered by approximately _±_ 2 _._ 0 m laterally and _±_ 0 _._ 5 m longitudinally at reset. Both conditions share the reward body, runner, 8192 environments, 1600 PPO iterations, and a three-stage velocity curriculum ending at _v_ max = 3 _._ 0 m/s, where _v_ max is the final commandedspeed cap. 

Table I reports reward-independent metrics over three training seeds: velocity RMSE along the active goal direction, rollout completion, hard termination rate, and the largest speed bin with mean velocity error below 0.5 m/s and fall rate below 5%. 

The circular command remains trackable at 3.0 m/s with 0.52 m/s RMSE and 99.51% rollout completion. The fixed sequence rarely falls, but its trackable speed is only 1.44 m/s and only 40.07% of rollouts complete, showing that the 

#### TABLE I 

COMMAND-FORM ABLATION FOR FAST BACKBONE TRAINING AT _v_ max = 3 _._ 0 M/S. ENTRIES ARE MEAN _±_ STD OVER THREE TRAINING SEEDS AND REPORT REWARD-INDEPENDENT VELOCITY TRACKING, ROLLOUT COMPLETION, HARD TERMINATIONS, AND THE LARGEST TRACKABLE SPEED BIN. 

|Command|Vel. RMSE<br>(m/s)|Rollout<br>compl. (%)|Fall<br>rate (%)|Trackable<br>speed (m/s)|
|---|---|---|---|---|
|Circular moving<br>goal|**0.52**_±_**0.02**|**99.51**_±_**0.15**|0.49_±_0.15|**3.00**_±_**0.00**|
|Fixed scattered|1.36_±_0.03|40.07_±_2.95|**0.09**_±_**0.04**|1.44_±_0.10|
|sequence|||||


circular command is a training interface for the fast backbone rather than a notational convenience. 

### _B. Simulation Evaluation of Obstacle Avoidance and GoalDirected Navigation_ 

The formal simulation benchmark evaluates the frozen backbone with planner-assisted teachers and planner-free localplanner inference in the same MuJoCo G1 simulator. The official navigation scope is two obstacle families: **open straightwall** , where the robot approaches a wall at 0.5–1.2 m/s and must bypass it, and **indoor obstacle layout** , with room boundaries, a central wall, and box obstacles. 

_1) Policy conditions and metrics:_ **R1 (Backbone-only)** sends the heading command directly toward the active key goal and acts as a sanity-check lower bound in wall-obstructed scenes. **OURS (DR)** uses the frozen backbone and learned planner in planner-free (NoPP) inference with dead-reckoning (DR) state. **OURS (Odom)** uses the same steering interface but computes the relative goal from odometry, removes the velocity head, and excludes joint velocities. **T1 (Teacher, PP)** keeps the teacher active under planner-present (PP) inference and is used only as a calibration reference, not as a method row in Table II. All conditions share raycast sensors, episode limits, and the same command-side safety filter. 

Timeout-based final-goal completion is intentionally not used as the success criterion: the simulator leaves enough time for a failed first approach to circle back to the target, a behavior with little practical value in crowded indoor spaces. We therefore evaluate whether the robot reaches the goal on its first useful approach and without scraping through the safety envelope. The objective reference time is _T_ 0 = _L_ obj _/v_ cmd, with nominal obstacle-aware route length _L_ obj and commanded speed _v_ cmd. The displayed _T-rel. on-time_ metric uses the same task/seed T1 stream as calibration: successful teacher-present episodes define the 98% threshold of _d_ eff = _T_ ep _v_ cmd, where _T_ ep is episode time and _d_ eff is the corresponding effective distance. Thus T-rel. on-time is the percentage of episodes reaching the goal within the T1-calibrated effective-distance budget. Expressed as time, this T-rel. window is about 25–26 s for the open-wall task and 23–31 s for the indoor task, roughly 5–12 s longer than the nominal best-path time depending on the seed and layout. Table II reports T-rel. on-time together with the observed overhead ∆ _t_ = _T_ ep _− T_ 0, so the reader can see how many seconds each method spends beyond _T_ 0. _Any brush_ combines sustained safety-envelope braking and body/foot contact brush; _contact brush_ counts body or foot obstacle contact below hard collision termination, and _hard collision_ is a termination-level collision. 

Table II quantifies how much of the teacher behavior is retained by the planner-free recurrent local planner while the frozen whole-body controller, sensors, episode limits, and safety filter remain fixed. 

The compact timing column exposes the main pattern. R1 often reaches the final goal eventually, but its mean overhead is about +14 s beyond the nominal best-path time and only about 38–40% of its runs arrive within the T1-calibrated budget. This happens because the shared safety envelope and jointly trained perception-action locomotion model already give the backbone a weak ability to avoid and edge around obstacles, but the behavior is indirect and frequently contact-heavy. The learned planners reduce the overhead to about +5 _._ 5–+7 _._ 5 s, raising T-rel. on-time arrival to 85–97%. Brush diagnostics follow the same trend, while hard collisions remain rare; the benefit is therefore direct, timely arrival rather than simply avoiding catastrophic failure. Fig. 3 supports this interpretation by pairing representative planner-free trajectories with navigation-quality diagnostics: the traces recover toward the goal after bypassing the obstacle, and the aggregate panel 

shows the corresponding gain in on-time arrival and reduction in brush/contact-heavy progress. 

_C. Ablations on Route-Shaping Control, Odometry, and Safety Filtering_ 

The navigation ablation uses the open straight-wall task, where the distinction between obstacle avoidance and returning to the key goal is easiest to attribute. For the DR variant, target-shaping ablations compare waypoint-only and key-goalonly route targets against the dynamic route-shaping control in (6). Table III then quantifies the same variants for both deadreckoning and odometry state, including delayed arrival, brush events, and the teacher-forced-to-planner-free transfer gap. The “no teacher forcing” row removes the default path in which this target is also injected into the frozen backbone during data collection. Both modes include a safety-filter stress test that disables the velocity envelope on the same checkpoint. Fig. 4 provides the qualitative counterpart to these rows: keygoal-only control fails to learn a bypass around the occluded direct route, waypoint-only control tends to carry the teacherroute template into NoPP rollout, and dynamic route shaping supplies an obstacle-conditioned bypass-and-recover pattern. 

The ablation isolates three effects. Key-goal-only control fails in both modes: only about one third of runs arrive on time, and any-brush rates exceed 65%. Waypoint-only control avoids the direct-target failure mode, but its labels are anchored to teacher waypoints; once those waypoints are removed at NoPP inference, the student can reproduce a memorized detour template rather than condition avoidance on the currently observed obstacle. Dynamic route shaping is more efficient because it makes the waypoint bearing active only when local clearance indicates that bypassing is needed and otherwise returns supervision to the key goal. For DR, removing teacher-label-to-policy injection raises any brush from 23.1% to 53.8% and increases the PP–NoPP gap from 0.0% to 4.1%, confirming that route shaping must affect the rollout state distribution. The no-safety-filter rows give the best simulated timing and brush rates, which indicates that the front local planner can already perform strong obstacle avoidance in MuJoCo. The safety filter is therefore retained mainly for real-robot deployment as a final braking layer: it may make simulated motion more conservative, but it provides the last line of defense against an unmodelled obstacle or sensing error. 

### _D. Real-Robot Deployment Analysis_ 

We use the real-robot run as a deployment-feasibility check for the compact inference interface. The deployed stack pairs the raycast-conditioned locomotion backbone with the odometry-assisted front local planner; on hardware, odometry supports target recovery while local range observations remain in the locomotion loop. The check covers representative wallocclusion layouts: frontal single-wall barriers of different lengths, an obliquely placed single-wall barrier, and a front– rear two-wall barrier configuration. In all cases, the commanded target is placed in front of the robot, so the policy must first select a feasible bypass direction and then recover toward 

TABLE II 

FORMAL V6 NAVIGATION QUALITY ON OPEN-WALL AND INDOOR LAYOUTS. PERCENTAGE COLUMNS ARE MEAN _±_ STD OVER SEEDS 0 _,_ 1 _,_ 2; THE TIMING COLUMN REPORTS T-REL. ON-TIME ARRIVAL WITH THE MEAN OVERHEAD ∆ _t_ = _T_ ep _− T_ 0. BOLDFACE MARKS THE BEST DISPLAYED MEAN WITHIN EACH TASK BLOCK. 

|Task|Method|T-rel.<br>on-time / ∆_t_|Any brush|Contact<br>brush|Hard coll.|
|---|---|---|---|---|---|
||R1 Backbone-only|38.3_±_5.2 / +14_._1s|70.9_±_7.7|69.7_±_7.4|0.3_±_0.1|
|Open wall|OURS (DR) NoPP|85.1_±_1.3 / +7_._5s|24.0_±_1.7|**9.5**_±_**2.0**|0.2_±_0.2|
||OURS (Odom) NoPP|**91.9**_±_**2.1 /** +6_._1**s**|**23.7**_±_**1.4**|10.1_±_0.8|**0.1**_±_**0.1**|
||R1 Backbone-only|40.3_±_15.3 / +14_._4s|77.7_±_7.3|76.5_±_7.4|0.5_±_0.4|
|Indoor|OURS (DR) NoPP|88.0_±_4.3 / +7_._4s|21.2_±_2.7|12.4_±_1.9|0.1_±_0.1|
||OURS (Odom) NoPP|**96.6**_±_**2.6 /** +5_._5**s**|**9.7**_±_**2.1**|**4.9**_±_**1.6**|**0.0**_±_**0.0**|


Fig. 3. Representative planner-free trajectories and navigation-quality diagnostics. The figure links post-obstacle goal recovery in sample rollouts with the aggregate timing and brush/contact trends reported in Table II. 

the forward target after the occlusion is cleared. The recorded trials span commanded speeds from 0.5 to 1.0 m/s, and the available front-range trace records a closest observed clearance of 0.281 m. These deployment logs verify that the compact inference interface can issue executable bypass-and-recover steering commands on the Unitree G1 without continuous joystick guidance. Fig. 5 shows one representative montage, trajectory, and sensor record; detailed videos are included with the open-source artifacts in the Appendix. 

### IV. CONCLUSION 

We presented LP-NavOA, a limited-perception framework that integrates local navigation and obstacle avoidance for humanoid robots by placing a learned recurrent steering module above a frozen raycast-conditioned whole-body locomotion backbone. The central design is to use planners and waypoint teachers only during training, while deployment retains a compact interface: proprioception, local range sensing, bodyframe goal direction, a command-side safety filter, and a 

TABLE III 

OPEN-WALL ROUTE-CONTROL ABLATION OVER THREE SEEDS. T-REL. ON-TIME USES THE FIRST-APPROACH BUDGET DEFINED FOR TABLE II; T-REL. LATE IS THE COMPLEMENTARY DELAYED-ARRIVAL RATE AMONG COMPLETED EPISODES, AND PP–NOPP GAP IS THE TEACHER-FORCED REFERENCE MINUS PLANNER-FREE ROLLOUT COMPLETION. BOLDFACE MARKS THE BEST MEAN WITHIN EACH MODE BLOCK. 

|Mode|Variant|T-rel.<br>on-time|T-rel.<br>late|Any brush|Hard coll.|PP–NoPP gap|
|---|---|---|---|---|---|---|
|DR|Full|85.3|14.5|23.1|**0.1**|**0.0**|
|DR|Waypoint-only control|72.6|22.3|33.0|0.3|4.9|
|DR|Key-goal-only control|33.9|**0.1**|66.5|0.5|65.9|
|DR|No teacher forcing|67.9|27.9|53.8|**0.1**|4.1|
|DR|No safety filter|**87.0**|12.5|**15.6**|0.5|0.3|
|Odom|Full|92.5|7.5|24.2|**0.0**|**-0.1**|
|Odom|Waypoint-only control|89.8|10.2|19.1|**0.0**|**-0.1**|
|Odom|Key-goal-only control|32.4|**0.1**|67.7|**0.0**|67.4|
|Odom|No safety filter|**95.7**|4.2|**16.8**|0.1|**-0.1**|


Fig. 4. Open-wall route-control ablation snapshots. Each panel compares the planner/waypoint teacher rollout (PP) with the corresponding plannerfree local-planner rollout (NoPP), highlighting whether the learned policy reproduces bypassing and goal recovery. 

heading command sent to the backbone. This separation lets the system inherit stable learned locomotion while adding memory-based decisions about when to bypass an obstacle and when to recover the sparse goal. 

The experiments show that this integrated steering layer changes the quality of navigation rather than merely the final timeout-based completion rate. On open-wall and indoor layouts, the distilled planner substantially improves T- rel. on-time arrival and reduces brush/contact-heavy progress compared with the backbone-only controller, while keeping hard collisions rare. The ablations further indicate that the circular heading-speed command is important for training the 3.0 m/s backbone, and that dynamic route shaping plus 


Fig. 5. Real-robot feasibility validation. After receiving a staged body-frame target and commanded speed, the planner-free steering policy approaches the obstacle, selects a bypass direction, and returns toward the target without continuous joystick steering. 

teacher-active data collection are necessary for the plannerfree student to reproduce obstacle-conditioned bypass and goal-recovery behavior without relying on explicit teacher waypoints at inference. The no-safety-filter results suggest that the learned local planner already handles most simulated obstacle avoidance; the command-side safety filter is retained primarily as a conservative deployment safeguard. 

The Unitree G1 deployment check confirms executable planner-free steering on hardware; repeated trials, moving obstacles, and richer indoor layouts remain natural extensions. 

### APPENDIX 

### IMPLEMENTATION DETAILS 

Table IV summarizes the reproducibility configuration. Source code, configuration files, and supplementary real- 

TABLE IV 

REPRODUCIBILITY CONFIGURATION FOR THE SIMULATED TRAINING AND EVALUATION SETUP. 

|Item|Setting|
|---|---|
|Open-source base|mjlab manager-based RL environment, task registry, and<br>PPO training/evaluation scripts.|
|Robot / simulator|Unitree G1 humanoid in MuJoCo.|
|Range sensing|Three VL53L8CX-style front/left/right raycast groups, each<br>8_×_8, 45<sup>_◦_</sup>FOV, 4 m range, base-aligned, 12 Hz.|
|Backbone network|Actor/critic MLP (512_,_256_,_128) with ELU activations and<br>observation normalization; each raycast group uses a small<br>convolutional encoder.|
|PPO training|Clip 0.2, entropy 0.01, GAE _γ_ = 0_._99_, λ_ = 0_._95, adaptive<br>LR 10<sup>_−_3</sup>, 5 epochs, 4 mini-batches, 24 steps per<br>environment.|
|Goal-command ablation|8192 parallel environments, 1600 iterations per seed, three<br>train seeds, velocity curriculum ending at 3.0 m/s.|
|Navigation evaluation|Seeds 0_,_1_,_2, 500 episodes per seed, 256 parallel<br>environments; formal scope limited to open straight-wall and<br>indoor layouts.|
|Training hardware|Intel Core i9-14900K CPU and NVIDIA GeForce RTX<br>4090D GPU.|


#### TABLE V 

PRINCIPAL LOCOMOTION REWARD TERMS USED TO TRAIN THE G1 BACKBONE. 

|Term|Weight|Role|
|---|---|---|
|track_ang_vel_cmd|1.3–1.8|yaw-rate command tracking|
|track_goal_velocity|2.0<br>|goal-directed speed tracking<br>|
|flat_orientation_l2|-5.0|upright torso regulation|
|is_terminated|-200|fall or illegal termination penalty|
|joint_pos_limits|-10|joint-limit avoidance|
|action_rate_l2|-0.05|smooth joint targets|
|foot_slip|-0.25|foot-slip suppression|
|body_collision|-1.0|obstacle/body contact penalty|
|feet_collision|-0.5|horizontal foot-impact penalty|
|in_place_turn_bonus|+1.0|large heading-error turning|


robot videos are available at https://shenqiqishi.github.io/ LP-NavOA/. 

Table V lists the principal locomotion reward terms; navigation comparisons keep the backbone and safety filter fixed. 

### REFERENCES 

- [1] L. P. Kaelbling, M. L. Littman, and A. R. Cassandra, “Planning and acting in partially observable stochastic domains,” _Artificial Intelligence_ , vol. 101, no. 1–2, pp. 99–134, 1998. 

- [2] P. E. Hart, N. J. Nilsson, and B. Raphael, “A formal basis for the heuristic determination of minimum cost paths,” _IEEE Transactions on Systems Science and Cybernetics_ , vol. 4, no. 2, pp. 100–107, 1968. 

- [3] D. Fox, W. Burgard, and S. Thrun, “The dynamic window approach to collision avoidance,” _IEEE Robotics & Automation Magazine_ , vol. 4, no. 1, pp. 23–33, 1997. 

- [4] G. Kahn, P. Abbeel, and S. Levine, “BADGR: An autonomous selfsupervised learning-based navigation system,” _IEEE Robotics and Automation Letters_ , vol. 6, no. 2, pp. 1312–1319, 2021. 

   - [8] J. Hwangbo, J. Lee, A. Dosovitskiy, D. Bellicoso, V. Tsounis, V. Koltun, and M. Hutter, “Learning agile and dynamic motor skills for legged robots,” _Science Robotics_ , vol. 4, no. 26, p. eaau5872, 2019. 

   - [9] J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning quadrupedal locomotion over challenging terrain,” _Science Robotics_ , vol. 5, no. 47, p. eabc5986, 2020. 

   - [10] T. Miki, J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning robust perceptive locomotion for quadrupedal robots in the wild,” _Science Robotics_ , vol. 7, no. 62, p. eabk2822, 2022. 

   - [11] A. Kumar, Z. Fu, D. Pathak, and J. Malik, “RMA: Rapid motor adaptation for legged robots,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2021. 

   - [12] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Real-world humanoid locomotion with reinforcement learning,” _Science Robotics_ , vol. 9, no. 89, p. eadi9579, 2024. 

   - [13] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

   - [14] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “HumanPlus: Humanoid shadowing and imitation from humans,” in _Proceedings of Machine Learning Research_ , vol. 270, Munich, Germany, 2024, pp. 2828–2844. 

   - [15] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, and G. State, “Isaac Gym: High performance GPU-based physics simulation for robot learning,” _arXiv preprint arXiv:2108.10470_ , 2021. 

   - [16] N. Rudin, D. Hoeller, P. Reist, and M. Hutter, “Learning to walk in minutes using massively parallel deep reinforcement learning,” in _Proceedings of the 5th Conference on Robot Learning (CoRL)_ , 2022, pp. 91–100. 

   - [17] K. Zakka, Q. Liao, B. Yi, L. Le Lay, K. Sreenath, and P. Abbeel, “mjlab: A lightweight framework for GPU-accelerated robot learning,” _arXiv preprint arXiv:2601.22074_ , 2026. 

   - [18] T. He, C. Zhang, W. Xiao, G. He, C. Liu, and G. Shi, “Agile but safe: Learning collision-free high-speed legged locomotion,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

   - [19] X. Cheng, K. Shi, A. Agarwal, and D. Pathak, “Extreme parkour with legged robots,” in _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2024, pp. 11 443–11 450. 

   - [20] G. B. Margolis, G. Yang, K. Paigwar, T. Chen, and P. Agrawal, “Rapid locomotion via reinforcement learning,” _The International Journal of Robotics Research_ , vol. 43, no. 4, pp. 572–587, 2024. 

   - [21] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

   - [22] M. Bain and C. Sammut, “A framework for behavioural cloning,” in _Machine Intelligence 15_ . Oxford, U.K.: Oxford University Press, 1995, pp. 103–129. 

   - [23] S. Ross, G. J. Gordon, and J. A. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” in _Proceedings of the 14th International Conference on Artificial Intelligence and Statistics (AISTATS)_ , 2011, pp. 627–635. 

   - [24] D. Chen, B. Zhou, V. Koltun, and P. Kr¨ahenb¨uhl, “Learning by cheating,” in _Proceedings of the Conference on Robot Learning (CoRL)_ , 2020, pp. 66–75. 

   - [25] Y. Bengio, J. Louradour, R. Collobert, and J. Weston, “Curriculum learning,” in _Proceedings of the 26th International Conference on Machine Learning (ICML)_ , 2009, pp. 41–48. 

   - [26] K. Cho, B. van Merri¨enboer, C. Gulcehre, D. Bahdanau, F. Bougares, H. Schwenk, and Y. Bengio, “Learning phrase representations using RNN encoder-decoder for statistical machine translation,” in _Proceedings of the Conference on Empirical Methods in Natural Language Processing (EMNLP)_ , 2014, pp. 1724–1734. 

- [5] D. Shah, A. Sridhar, N. Dashora, K. Stachowicz, K. Black, N. Hirose, and S. Levine, “ViNT: A foundation model for visual navigation,” in _Proceedings of the 7th Conference on Robot Learning (CoRL)_ , 2023, pp. 711–733. 

- [6] A. Sridhar, D. Shah, C. Glossop, and S. Levine, “NoMaD: Goal masked diffusion policies for navigation and exploration,” in _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2024, pp. 63–70. 

- [7] F. Huang, H. Mou, and Q. Li, “TNavRL: Cross-modal transformer for humanoid visual navigation,” _IEEE Robotics and Automation Letters_ , vol. 11, no. 5, pp. 5374–5381, 2026. 

