---
title: "SKATER: Synthesized Kinematics for Advanced Traversing Efficiency on a Humanoid Robot via Roller Skate Swizzles"
date: "2026-01-08"
authors: "Junchi Gu; Feiyang Yuan; Weize Shi; Tianchen Huang; Haopeng Zhang; Xiaohu Zhang"
url: https://arxiv.org/abs/2601.04948
pdf: https://arxiv.org/pdf/2601.04948
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.04948)** / [論文ページ](https://arxiv.org/abs/2601.04948)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SKATER: Synthesized Kinematics for Advanced Traversing Efficiency on a Humanoid Robot via Inline-Skate Swizzles** 

Junchi Gu, Feiyang Yuan, Weize Shi, Tianchen Huang, Haopeng Zhang, Xiaohu Zhang, Yu Wang, Wei Gao and Shiwu Zhang 

**_Abstract_ — Humanoid walking and running have advanced rapidly, but their intermittent ground contacts still produce large transient loads at touchdown and cause undesired energy loss. This paper presents a humanoid robot, SKATER, whose feet are equipped with passive inline wheels, and investigates the swizzling gait as a continuous rolling-contact locomotion primitive for advanced efficiency. Because the wheels are neither actuated nor steerable, propulsion must be generated through whole-body motion to take advantage of the anisotropic and nonholonomic wheel-ground constraints. We formulate swizzling as a reference-free deep reinforcement learning problem, where neither motion-capture demonstrations nor predefined reference motions are necessary. Instead, reward design regarding ZMP criterion, inter-foot geometry, bilateral symmetry and wheel axial-slip constraints can guide the learning process without explicit gait-phase scheduling. Ablation study results quantify the contribution of these constraints, and the learned policy is successfully deployed on the physical robot. Against a walking baseline on the same platform with rigid flat feet, the swizzling gait reduces Impact Intensity based on ground reaction forces by** 50 _._ 25% **in simulation, and mechanical Cost of Transport by** 63 _._ 34% **in real-world experiments. Additional hardware tests yield** 10 _/_ 10 **successful** 10 **-m swizzling trials on surfaces including tile, rubber and gravel, as well as dynamic maneuver in obstacle avoidance. In high-speed trials, the robot can reach an average speed of** 2 _._ 99 _±_ 0 _._ 01 **m/s. The video is available here:Video Link** 


Fig. 1: Overview of the SKATER platform and its learned swizzling gait. 

## I. INTRODUCTION 

Humanoid locomotion has progressed rapidly from walking [1] and running [2] to jumping [3] and whole-body skills [4], [5]. Nevertheless, walking and running still involve repeated foot-ground impacts that incur large ground reaction forces (GRFs) and energy losses, thus increase joint loads and acoustic noises. Inline skating replaces discrete touchdown with continuous rolling contact, which has been reported by human biomechanics studies as having lower impact loads than running while retaining efficient forward motion [6]. This motivates inline skating with passive wheels as a complementary mobility mode for humanoid robots on extended flat terrain. 

This work was supported in part by the National Natural Science Foundation of China under Grants U22B2040, in part by the Major Project of Anhui Province’s Science and Technology Innovation Breakthrough Plan (202423h08050003), in part by the Key Science & Technology Project of Anhui Province (202523j08050001), and in part by the Fundamental Research Funds for the Central Universities with grant No. YD2090002019. (Corresponding authors: Wei Gao; Yu Wang.) 

The authors are with the Institute of Humanoid Robots, Department of Precision Machinery and Precision Instrumentation, University of Science and Technology of China, Hefei, Anhui 230026, China. weigao@ustc.edu.cn; wangyuustc@ustc.edu.cn 

Realizing this capability is challenging because passive inline wheels are neither actuated nor steerable. Propulsion and maneuvering must instead arise through whole-body motion under the anisotropic and nonholonomic wheelground contacts, while the controller maintains balance and suppresses lateral slip. Swizzling provides a suitable entrypoint primitive: periodic bilateral abduction and adduction of the feet generate thrust while maintaining continuous support. The controller must therefore coordinate ground contact geometry, wheel heading, support regulation and trunk stabilization without a predefined contact schedule. 

Existing studies only partially address this problem. Early bipedal skating systems rely primarily on planned trajectories or model-based control [7], [8], [9], [10], whereas quadrupedal skating exploits different morphologies and balance mechanisms [11], [12]. On the other hand, learningbased humanoid control has achieved robust locomotion performance [13], [1], but often requires foothold, contactschedule or gait-phase priors [14], [1]. Although hierarchical learning can reduce dependence on full-body motion references [15], learning continuous bilateral-support swizzling without reference motion data on a humanoid robot with passive inline wheels remains sparsely studied. 

To address this gap, we present SKATER (Synthesized Kinematics for Advanced Traversing Efficiency on a humanoid Robot), a 33-degree-of-freedom (DoF) humanoid robot with passive inline-wheel feet, as shown in Fig. 1, and a reference-free and constraint-guided deep reinforcement learning (DRL) framework. Here, _reference-free_ denotes training without motion-capture demonstrations or predefined reference motions. The policy instead uses only proprioceptive history, skating-specific physical constraints and domain randomization, without any explicit gait-phase scheduling. 

The main contributions of this paper include: 

- We develop SKATER, a 33-DoF humanoid platform with four passive inline wheels at each sole for studying continuous rolling-contact locomotion. 

- We formulate swizzling as a reference-free DRL problem that requires no reference motion data. Reward design regarding zero moment point (ZMP) criterion, inter-foot geometry, bilateral symmetry and wheel axialslip suppression can guide learning without explicit gaitphase scheduling. 

- We validate the learned swizzling policy in simulation and on hardware. Relative to a separately trained walking baseline on the same robot but with rigid flat feet, swizzling reduces GRF-based Impact Intensity by 50 _._ 25% in simulation and mechanical CoT by 63 _._ 34% in real world. In high speed trials, swizzling can reach an average speed of 2 _._ 99 _±_ 0 _._ 01 m/s repeatedly. 

## II. RELATED WORK 

## _A. Skating Locomotion in Legged Robots_ 

Passive-wheel skating in legged robots has primarily been addressed through trajectory planning and model-based control. Itabashi _et al._ generate bipedal swizzling trajectories using fifth-order B´ezier curves and a variable-curvature skate mechanism [7]. Hashimoto _et al._ model anisotropic rolling and lateral friction, then modulate a foot reference trajectory from GRF feedback to limit internal forces [8]. IverachBrereton _et al._ incorporate forward GRFs into model-based gait design for skating on solid and even ice ground [9]. These physically interpretable approaches establish the feasibility of bipedal skating and explicitly regulate contact behaviors. Across these studies, the propulsion cycle is prescribed before execution, while feedback mainly stabilizes or schedules the planned motion. This separation provides predictable behavior, but limits adaptation when surface friction, commanded velocity or robot dynamics depart from the design conditions. Extending these approaches to higherdimensional humanoids and broader command ranges therefore requires substantial trajectory and model redesign. 

Work on quadrupedal robots has advanced passive-wheel contact modeling and whole-body control. Bjelonic _et al._ replace the conventional friction cone with a friction triangle and use hierarchical force control on ANYmal, reducing CoT by up to 80% relative to walking [11]. Chen _et al._ combine a geometric wheel-ground contact model 

with a Levenberg–Marquardt controller on a 4-DoF wheellegged quadruped, enabling diverse skating gaits and smallradius turns [12]. The friction-triangle formulation captures direction-dependent traction explicitly, whereas the geometric wheel model improves contact-point accuracy in skating kinematics. Both developments are important for passive wheels, but their controllers remain tied to morphologyspecific force distributions and planned motions. Moreover, quadrupedal skating benefits from a larger support region, redundant contacts and different load distribution. Its planning and stability mechanisms therefore do not transfer directly to a humanoid, leaving learning swizzling on a full-size humanoid without reference motion data unexplored. 

## _B. Locomotion Control of Humanoid Robots_ 

The ZMP criterion [16] and Model Predictive Control [17] provide interpretable foundations for humanoid locomotion, but typically require accurate dynamics, planned CoM or foothold trajectories, and predefined contact sequences. Model-based planning makes stability constraints transparent and allows contact forces to be optimized directly. For a wheel-footed humanoid, however, it requires jointly modeling high-dimensional whole-body dynamics, and changing wheel headings, anisotropic frictions and multiple rolling contacts throughout the propulsion cycle. These assumptions are effective when stance and swing phases are known, but passive inline wheels remain in continuous contact and admit strongly direction-dependent motion. 

Learning-based methods improve adaptability while often preserving similar structure. Lee _et al._ use a Linear Inverted Pendulum model to generate desired footholds for an RL tracking policy [14]. DeepLoco learns robust bipedal skills with limited prior structure, yet still relies on step targets and style objectives [15]. Humanoid-Gym enables large-scale training and zero-shot sim-to-real transfer, while explicitly encoding gait phase and expected foot-contact patterns [1]. Such priors improve learning efficiency and gait regularity, but constrain the learned motion to selected footfall structures and do not directly represent continuous and nonholonomic rolling contact. This distinction matters because swizzling speed emerges from coupled lateral foot motion and wheel orientation rather than choosing when and where to lift and place a foot. Neither discrete foothold targets nor an alternating support schedule naturally describes the propulsion cycle. Therefore, this work adopts a referencefree formulation that learns without reference motion data, using support, geometric, symmetry and rolling constraints instead of explicit gait-phase scheduling. 

## III. METHODOLOGY 

## _A. Hardware Design_ 

As mentioned, SKATER is a humanoid robot with 33 DoFs in total. The 25 actuated DoFs include 6 per leg, 5 per arm, 2 in the waist and 1 in the neck, as shown in Fig. 2. Each foot is equipped with 4 inline wheels. The robot has a total mass of 38 kg and a standing height of 140 cm. Fig. 2 further shows the ankle-joint location and the 


Fig. 2: Hardware design of SKATER and its passive-wheel inline-skate foot module. 

exploded foot assembly. The inline-skate foot module uses polyurethane wheels with diameter _Dw_ = 62 mm, width _Ww_ = 24 mm and center spacing _s_ = 68 mm. Each inlineskate foot module has a mass of 0 _._ 85 kg, while the rigid flat foot used for the walking baseline has a mass of 0 _._ 61 kg. The wheels are mounted on passive 608ZZ bearings, and the foot frame is made of aluminum alloy. 

Here, the inline skate shoes are not directly utilized due to two critical considerations: 1) Inline skate shoes exhibit incompatibility to nominal rigid flat foot, because their outer shells introduce a compliant layer to the foot sole and can cause relative sliding, which compromises the accuracy of force transmission and position control. 2) Roller skate shoes can interfere with the transmission mechanism of the robot’s ankle joints, limiting its range of motion. Another point worth noting is the wheel diameter. Comparing to the wheel diameters between 72-80 mm that are commonly used on standard inline skate shoes, the smaller wheel diameter of 62 mm can lower the CoM of both feet and reduce the torque required around the ankle roll axis. This optimization is particularly critical during the lateral propulsion phase of inline skating, where the ankle joint must withstand significant eversion and inversion moments. 

_B. Reinforcement Learning of Swizzling_ 

_1) Problem Formulation:_ We model the simulated swizzling task as a finite-horizon MDP [18] and optimize a stochastic policy _πθ_ ( **_a_** _t|_ **_o_** _t_ ) by maximizing the expected discounted return _J_ ( _θ_ ) = E _πθ_ [<sup>�</sup><sup>_T_</sup> _t_ =0<sup>_−_1</sup><sup>_γtrt_],where</sup><sup>_T_isthe</sup> episode horizon and _γ ∈_ [0 _,_ 1] is the discount factor. The policy is trained with PPO [19] using an asymmetric actor– critic in Isaac Lab [20] with 4096 parallel environments. Command ranges and domain-randomization magnitudes are expanded progressively to stabilize exploration. 

_2) Observation Space:_ As shown in Fig. 3, the Actor uses a five-step history of proprioceptive observations: 


where the current state is defined as 


Here **_q_** _t,_ **_q_** ˙ _t ∈_ R<sup>_nj_</sup> are the actuated joint positions and velocities, with _nj_ = 25 for SKATER, **_ω_** _t ∈_ R<sup>3</sup> is the base 

angular velocity, **_g_** _∈_ R<sup>3</sup> is the gravity vector projected in the base frame, **_v_**<sup>cmd</sup> _t ∈_ R<sup>3</sup> is the commanded horizontal velocity and yaw rate, and **_a_** _t−_ 1 _∈_ R<sup>_nj_</sup> is the previous action. The eight passive wheel DoFs are excluded from both Actor and Critic observations because they are not actuated; Their rolling and slip effects are inferred from proprioceptive history rather than direct wheel-state inputs. 

During training, the Critic receives a separate noise-free privileged observation with the same history length: 


where 


The additional privileged terms are the simulator groundtruth base linear velocity **_v_**<sup>lin</sup> _t ∈_ R<sup>3</sup> , the centroidal ZMP offset with respect to the whole-body CoM in the world horizontal plane ∆ **_p_**<sup>zmp</sup> _t ∈_ R<sup>2</sup> , the distance between the two ankle joints _d_<sup>ankle</sup> _t ∈_ R, and the orientation angles of the two ankle joints with respect to the base’s forward direction **_θ_**<sup>ankle</sup> _t ∈_ R<sup>2</sup> . These privileged terms provide the Critic with direct information about velocity tracking, support stability, swizzling geometry and foot heading during training. 

_3) Action Space:_ The policy outputs a dimensionless action vector **_a_** _t ∈_ R<sup>_nj_</sup> for all 25 actuated DoFs. At each control step, the action is scaled about the nominal configuration **_q_** default to form the desired joint positions 


where the action scale is set to _β_ = 0 _._ 25 rad. A joint-level PD controller converts these targets into torques: 


where **_K_** _p_ and **_K_** _d_ are diagonal matrices of joint proportional and derivative gains, respectively. Note that the eight passive wheels are excluded from the action vector; They receive neither position targets nor direct torque commands, and rotate only through ground contact dynamics. Although the action space includes the arms, waist and neck to retain whole-body balance authority, only penalties are applied to softly regularize these joints around **_q_** default and suppress unnecessary upper-body motion. 

_4) Reward Function Design:_ Unlike walking rewards organized around alternating stance and swing contacts, the skating reward must maintain continuous rolling support, bounded lateral foot motion and low wheel axial slip. The instantaneous reward is _rt_ =<sup>�</sup> _k_<sup>_wkrk,t_,where</sup> _rk,t_ and _wk_ denote the _k_ -th reward component and its weight, respectively. No kinematic reference trajectory, gait timing or state machine is imposed. Instead, swizzling is induced by four physical biases: inter-foot distance bounds, wheel axial-slip suppression, ZMP support stability and bilateral leg symmetry. These biases are chosen to capture the physical mechanism of swizzling: inter-foot distance bounds define the opening-and-closing envelope, bilateral 


Fig. 3: Deep reinforcement learning control framework for SKATER. The policy network processes proprioceptive sensor data to generate joint-level commands, enabling adaptive inline skate swizzles. 

symmetry regularizes periodic leg coordination, wheel axialslip suppression preserves the nonholonomic rolling behavior for propulsion, and ZMP terms maintain stable continuous support. 

Let _d_ feet be the horizontal distance between the two feet. The distance-bound terms in Table I constrain the swizzling envelope without prescribing a time-varying foot path. For the _i_ -th passive wheel, **v** _i_ , **a** _i_ and _Fi_ denote the wheel-center velocity, axle direction and normal contact force; the axialslip term in Table I is activated only for contacting wheels. 

Support stability is enforced by ZMP terms. With wholebody CoM position **c** , CoM acceleration **a** _c_ , centroidal angular-momentum rate **h**<sup>˙</sup> and net contact force **F** = _M_ ( **a** _c−_ **g** ) = [ _Fx, Fy, Fz_ ]<sup>_⊤_</sup> , the horizontal ZMP is 


When _Fz ≤_ 0 _._ 1 _M ∥_ **g** _∥_ , the ZMP offset is set to zero. The support polygon _P_ is built from contacting wheels, where the contacting wheels on the left and right feet are counted as _nL_ and _nR_ . With signed ZMP margin _m_ , safety margin _m_ safe = 0 _._ 02 m, smoothing scale _σm_ = 0 _._ 03 m and sigmoid _σ_ ( _·_ ), the support-valid reward is listed in Table I, and the ZMP margin reward is 


Finally, bilateral symmetry acts as a soft gait prior. With ∆ **q** = **q** _L −_ **_S_ q** _R_ and ∆˙ **q** = **q** ˙ _L −_ **_S_** ˙ **q** _R_ , where **_S_** mirrors right-leg coordinates to the left-leg convention. The corresponding reward is summarized in Table I. Upper-body deviation penalties keep the arms, waist and head near a nominal posture while preserving balance authority. 

The remaining task, contact, posture, smoothness and energy terms follow standard locomotion regularization practice. All 22 terms are summarized in Table I. 

_5) Sim-to-Real Transfer:_ The sim-to-real transfer gap constitutes one of the key challenges in reinforcement learning for physical robots. To improve transfer robustness, domain randomization is applied during training by perturbing wheel-ground contact properties, robot inertial parameters, actuator gains and external disturbances. The randomized quantities and their ranges are listed in Table II. 

## IV. EXPERIMENTS AND RESULTS 

To evaluate the performance of inline skate swizzles, nominal bipedal walking gaits are also tested on SKATER with the wheel mechanisms replaced by normal rigid flat feet. The walking baseline is trained using the same RL training pipeline as the skating policy, including the same simulator, PPO implementation, policy network structure, action interface and PD control layer. The reward functions are task-specific: the walking policy uses standard bipedal locomotion rewards for velocity tracking, posture stabilization, regular foot contacts and smooth joint motion, whereas the skating policy additionally incorporates rolling-contact and nonholonomic constraints introduced in Section III-B.4. For both swizzling and walking gaits, the learned policy is first deployed in the MuJoCo physics engine [21] for sim-to-sim tests given its high-precision contact force simulation, and then deployed on SKATER for sim-to-real evaluation. 

## _A. Simulation Results_ 

_1) Impact Force Analysis:_ Fig. 4 presents a temporal comparison of vertical Ground Reaction Forces (GRF) between the swizzling and the walking gait during the first 3 s at a commanded speed of 1 m/s. Given the weight of SKATER being approximately 372 _._ 4 N, it can be seen that nominal walking generates pronounced impact peaks at each heel strike, reaching 1 _._ 5-2 _._ 0 times body weight during the approximately 50-100 ms time window, imposing substantial loads on the joints. In contrast, the force profile of the swizzling gait exhibits smooth periodic variations. Excluding 

TABLE I: Reward Function Terms 

|**Reward Term**|**Formula**|**Weight**|
|---|---|---|
|**_Task Rewards_**|||
|Alive|**1**alive<br><br><sup>cmd</sup><br><sup>yaw</sup><br><sup>2</sup><br>|0_._15|
|Linear Velocity Track|exp<br>�<br>_−_<br>_∥_**v**<br>_xy_<br>_−_**v**<br>_xy_<br>_∥_<br>0_._25<br>�|1_._8|
|Angular Velocity Track|exp<br>�<br>_−_<br>(_ω_<sup>cmd</sup><br>_z_<br>_−ω_<sup>base</sup><br>_z_<br>)<sup>2</sup><br>0_._25<br>�|1_._2|
|**_Joint Penalties_**|||
|Arms Deviation|�<br>arms <sup>_|qi −q_0</sup><br>_i _<sup>_|_</sup><br>|_−_0_._4|
|Waist Deviation|�<br>waist <sup>_|qi −q_0</sup><br>_i _<sup>_|_</sup>|_−_0_._4|
|Head Deviation|_|q_head _−q_<sup>0</sup><br>head<sup>_|_</sup>|_−_1_._0|
|Ankle Roll Deviation|�<br>ankle roll <sup>_|qi −q_0</sup><br>_i _<sup>_|_</sup>|_−_0_._2|
|**_Posture Penalties_**|||
|Flat Orientation|_g_<sup>2</sup><br>proj_,x_ <sup>+</sup><sup>_g_2</sup><br>proj_,y_|_−_2_._0|
|Base Height|(_h_base _−_0_._66)<sup>2</sup>|_−_2_._0|
|**_Swizzling Constraints_**|||
|Inter-foot Distance Lower Bound|max(0_,_0_._2_−d_feet)|_−_2_._0|
|Inter-foot Distance Upper Bound|max(0_, d_feet _−_0_._5)|_−_5_._0|
|**_Wheel and ZMP Rewards_**|||
|Wheel Axial Slip|�<br>_i_<sup>(</sup><sup>**v**</sup><sup>_i·_</sup><sup>**a**</sup><sup>_i_)2</sup><sup>**1**</sup><sup>_F_</sup>_i_<sup>_>_1N</sup><br>|_−_0_._1|
|ZMP Support Valid|�<br>1_,_<br>_nL ≥_2_, nR ≥_2<br>_−_1_,_<br>otherwise|0_._2|
|ZMP Support Margin|Eq. (8)|0_._5|
|**_Symmetry Rewards_**|||
|Limb Symmetry|1<br>1_._5<br>�<br>1_._0 exp<br>�<br>_−_<sup>_∥_∆</sup><sup>**q**</sup><sup>_∥_2</sup><br>0_._25<br>�|0_._5|
||+ 0_._5 exp<br>�<br>_−_<sup>_∥_∆˙</sup><sup>**q**</sup><sup>_∥_2</sup><br>4_._0<br>�<br>�||
|**_Contact Penalties_**|||
|Undesired Contacts|�<br>body<br>_/_<br>_∈_wheel<br>**1**_F_contact_>_1N|_−_1_._0|
|**_Regularization Penalties_**|||
|Angular Velocity XY|_ω_<sup>2</sup><br>_x_ <sup>+</sup><sup>_ω_2</sup><br>_y_|_−_0_._05|
|Joint Velocity|_∥_˙**q**_∥_<sup>2</sup>|_−_0_._001|
|Joint Acceleration|_∥_¨**q**_∥_<sup>2</sup>|_−_2_._5_×_10<sup>_−_7</sup>|
|Action Rate|_∥_**a**_t −_**a**_t−_1_∥_<sup>2</sup>|_−_0_._05|
|Energy|�<br>_i _<sup>_|τi||_ ˙</sup><sup>_qi|_</sup><br>|_−_2_×_10<sup>_−_5</sup>|
|Joint Position Limits|�<br>_i_<br>[max(0_, q_min_,i −qi_)<br>+ max(0_, qi −q_max_,i_)]|_−_5_._0|


the startup portion where the robot must exert force to accelerate, the peak forces are reduced to 1 _._ 1-1 _._ 3 times body weight with significantly decreased force variation rates. 

To further quantify the impact severity difference, we define an Impact Intensity metric as: 


As a result, the Impact Intensity for walking is _I_ bipedal = 2283 _._ 17 N/s, while that for swizzling is _I_ roller = 1135 _._ 93 N/s, which is an reduction of 50 _._ 25% and indicates the advantage of skating locomotion in reducing joint impacts. Additional tests at speed commands of 0 _._ 5, 1 _._ 5 and 2 _._ 0 m/s observe consistent reductions of 44 _._ 97%, 50 _._ 18% and 44 _._ 64%, respectively. 

_2) Velocity Tracking Performance:_ To evaluate SKATER’s velocity tracking performance, the desired forward velocity sequence was set to 0 _._ 7, 1 _._ 4, 2 _._ 0, 1 _._ 4, 0 _._ 7, 0 _._ 0 m/s in MuJoCo, with a switching interval of 7 _._ 0 s. The results presented in Fig. 5 show reasonable velocity tracking, with 

TABLE II: Domain Randomization Parameters 

|**Term**|**Value**|
|---|---|
|**_Material Physics - Wheels_**||
|Static Friction Coefficient|_U_(0_._1_,_0_._8)|
|Dynamic Friction Coefficient|_U_(0_._1_,_0_._4)|
|**_Base Mass Offset_**|_U_(_−_1_._0_,_3_._0)kg added to pelvis|
|**_CoM Offset - Pelvis and Torso_**<br>_x/y/z_ axes|_U_(_−_0_._01_,_0_._01) m|
|**_Actuated Joint Parameters - Non-_**|**_wheel Joints_**|
|Proportional Gain Scale|_U_(0_._9_,_1_._1)|
|Derivative Gain Scale|_U_(0_._9_,_1_._1)|
|Motor Zero Offset|_U_(_−_0_._02_,_0_._02) rad|
|**_External Disturbance_**||
|Push Velocity _x_|_U_(_−_0_._4_,_0_._5) m/s|
|Push Velocity _y_|_U_(_−_0_._8_,_0_._8) m/s|
|Push Interval|5_._0 s|


Fig. 4: Comparison of vertical GRF profiles. 

accelerating transitions producing short speed spikes and decelerating exhibiting a slower response. These behaviors reflect the limited braking and speed-regulation authority of passive-wheel rolling contact compared with conventional foot-ground stance control. 

_3) Gait Pattern Visualization:_ For a swizzling gait, Fig. 6 shows the temporal coordination between the ankle motions and the opening-and-closing foot distance. The ankle angles exhibit periodic left-right coordination, while the inter-foot distance follows the desired swizzling envelope after a short initial transient. These results demonstrate that through appropriately designed physical constraints and reward terms, DRL can form and optimize swizzling gaits without reference motion data or an explicit state machine. This datadriven approach provides a practical way for inline skating locomotion control of humanoid robots with passive wheels. 

## _B. Ablation Study_ 

To identify the contribution of individual reward terms, we conduct ablations over five random seeds. All policies are evaluated in Isaac Lab under the same nominal protocol on a fixed 18-command grid with _vx ∈ {−_ 1 _._ 0 _, −_ 0 _._ 5 _,_ 0 _._ 5 _,_ 1 _._ 0 _,_ 1 _._ 5 _,_ 2 _._ 0 _}_ m/s, _vy_ = 0, and _ωz ∈ {−_ 0 _._ 5 _,_ 0 _,_ 0 _._ 5 _}_ rad/s. For each command, we collect 100 completed episodes using 32 parallel environments, with physical-parameter domain randomization disabled. The results are presented in Table III. The task survival rate represents the fraction of episodes completed without falling, 


Fig. 5: Velocity tracking performance of SKATER following step commands. 


Fig. 6: Temporal analysis of the learned swizzling gait: ankle joint angle profiles and inter-foot distance variation with the reward bounds indicated. 

while worst-command survival is the minimum across command pairs. Because survival alone does not establish the desired swizzling pattern, we also report command-tracking RMSE and joint mechanical energy per meter. Diagnostic metrics follow the skating-specific rewards: ZMP inside rate and margin measure support inclusion and clearance, inter-foot bound violations and leg symmetry quantify gait geometry, wheel axial slip measures nonholonomic slip, and wheel contact validity checks whether ZMP support has sufficient contacts. 

The ablation results should be interpreted as a multiobjective swizzling-quality analysis rather than a single survival leaderboard. The best result in each column of Table III is shown in bold, while the second-best result is underlined. The full reward does not maximize survival alone; instead, it achieves the best yaw-rate tracking, ZMP inside rate, ZMP margin reward, leg symmetry score and wheel contact validity, indicating a balanced trade-off among tracking, support stability, gait regularity and rolling contact. Removing the ZMP reward degrades the ZMP inside rate from 99 _._ 47% to 62 _._ 23% and reduces the worst-command survival rate from 64 _._ 80% to 26 _._ 40%, showing its role in stable support. Removing the ZMP margin reward leads to zero worst-command survival, while removing the foot-distance reward increases inter-foot bound violation to 76 _._ 14%. Removing the wheel axial-slip reward increases axial slip from 0 _._ 191 to 2 _._ 541 and yields the highest energy consumption, 


Fig. 7: Horizontal foot trajectories under representative reward term ablations and their motion-level failure modes. 

confirming its role in enforcing nonholonomic rolling. The symmetry ablation is particularly revealing that, although removing symmetry gives the highest nominal survival rate, it substantially degrades yaw-rate tracking, energy efficiency and leg symmetry. This indicates that the symmetry term is not mainly a fall-prevention term, but a gait-quality term that prevents the policy from surviving through asymmetric or shuffling motions that no longer match the intended swizzling primitive. 

Fig. 7 links the metrics to motion-level failures through horizontal foot trajectories. The full reward and the variant without the ZMP margin reward retain swizzling-like trajectories; removing symmetry produces low-clearance shuffling, removing the ZMP or axial-slip reward induces stepping-like lift-off, and removing the foot-distance reward breaks the desired swizzling geometry. 

## _C. Experimental Results_ 

The learned control policy is then transferred to the physical robot for real world evaluation. The policy is run at 50 Hz through the onboard computer to show its efficacy. _1) Real-World Mobility Evaluation:_ The real-world mobility of SKATER is evaluated from three aspects: basic omnidirectional locomotion, high-speed flat-ground traversal and multi-surface robustness. Forward, backward and obstacle-crossing swizzling trials were conducted from rest, followed by stable braking through a pigeon-toed stance. As shown in Fig. 8(a), the obstacle-crossing trial validates turning maneuverability. For high-speed traversal, five repeated trials were performed over a marked 9 m straight section, with traversal time recorded by stopwatch and crosschecked using video timestamps. The trials reported a traversal time of 3 _._ 01 _±_ 0 _._ 01 s and an average traversal speed of 2 _._ 99 _±_ 0 _._ 01 m/s over the measured section, with Fig. 8(b) showing a representative trial. Additionally, to evaluate the robot’s adaptability to surfaces with distinct contact and rolling-resistance characteristics, tests were conducted on tile, rubber and gravel pavement. On each surface, the robot performed 10 repeated 10-m swizzling trials and achieved 10 _/_ 10 success. A trial was considered successful if the robot completed the course without falling or human intervention. 

TABLE III: Reward term ablations. Values are reported as mean _±_ standard deviation over five random seeds. 

|**(a) Main performance metr**|**ics**||||||
|---|---|---|---|---|---|---|
|Method|Task Survival (%) _↑_|Worst-cmd. Survival (|%) _↑_<br>Fall Rate (%) _↓_|Forward Vel. RMSE (m/s) _↓_|Yaw-rate RMSE (rad/s)|_↓_<br>Energy per Meter _↓_|
|Full reward|94.62 _±_ 0.75|64.80 _±_ 9.09|5.38 _±_ 0.75|0.236 _±_ 0.001|**0.194** _±_ **0.001**|113.95 _±_ 0.27|
|w/o symmetry reward|**99.17** _±_ **0.41**<br>|**93.00** _±_ **3.08**<br>|**0.83** _±_ **0.41**<br>|0.257 _±_ 0.000<br>|0.329 _±_ 0.000<br>|140.13 _±_ 0.11<br>|
|w/o ZMP reward|87.22 _±_ 1.13<br>|26.40 _±_ 2.70<br>|12.78 _±_ 1.13<br>|**0.196** _±_ **0.001**<br>|0.255 _±_ 0.002<br>|**81.91** _±_ **0.61**<br>|
|w/o ZMP margin reward|90.00 _±_ 0.93|0.00 _±_ 0.00|10.00 _±_ 0.93|0.241 _±_ 0.003|0.251 _±_ 0.000|90.92 _±_ 0.84|
|w/o foot-distance reward|86.19 _±_ 0.93|0.00 _±_ 0.00|13.81 _±_ 0.93|0.273 _±_ 0.001|0.326 _±_ 0.004|154.34 _±_ 1.15|
|w/o wheel axial-slip reward|91.40 _±_ 0.30|33.20 _±_ 9.18|8.60 _±_ 0.30|0.235 _±_ 0.004|0.285 _±_ 0.001|167.47 _±_ 0.15|
|**(b) Diagnostic metrics**|||||||
|Method<br>|ZMP Inside Rate (%) _↑_|ZMP Margin Reward _↑_|Inter-foot Bound Viol.|(%) _↓_<br>Leg Symmetry Score _↑_|Wheel Axial Slip _↓_<br>Whee|l Contact Validity (%) _↑_|
|Full reward|**99.47** _±_ **0.02**<br>|**0.768** _±_ **0.001**<br>|4.27 _±_ 0.07<br>|**0.894** _±_ **0.000**<br>|0.191 _±_ 0.000<br>|**97.11** _±_ **0.08**<br>|
|w/o symmetry reward|99.28 _±_ 0.01|0.740 _±_ 0.000|**2.09** _±_ **0.02**|0.233 _±_ 0.000|0.226 _±_ 0.000|95.33 _±_ 0.04|
|w/o ZMP reward|62.23 _±_ 0.09|0.000 _±_ 0.002|8.01 _±_ 0.07|0.756 _±_ 0.001|**0.063** _±_ **0.000**|39.68 _±_ 0.13|
|w/o ZMP margin reward|97.44 _±_ 0.10|0.640 _±_ 0.002|3.54 _±_ 0.09|0.877 _±_ 0.000|0.130 _±_ 0.000|92.70 _±_ 0.11|
|w/o foot-distance reward|95.36 _±_ 0.03|0.643 _±_ 0.001|76.14 _±_ 0.41|0.843 _±_ 0.001|0.095 _±_ 0.000|87.05 _±_ 0.14|
|w/o wheel axial-slip reward|96.63 _±_ 0.13|0.654 _±_ 0.002|56.49 _±_ 0.28|0.651 _±_ 0.000|2.541 _±_ 0.022|83.41 _±_ 0.20|


Fig. 8: Real-world mobility validation: (a) obstacle-crossing swizzling and (b) high-speed flat-ground traversal. 

_2) Joint Impact Load Evaluation:_ To quantitatively assess the mechanical impact of walking and swizzling gaits on robot joints, joint torque data were collected from SKATER under both gaits at a commanded speed of 1 m/s. Peak torque is employed as the evaluation metric, focusing mainly on the dynamic characteristics of the 12 lower-limb joints. Table IV presents the detailed results, indicating that the swizzling gait reduces peak torques across most lower-limb joints. The most pronounced reductions are observed in the sagittal-plane joints: the left and right hip pitch torques are reduced by 69 _._ 53% and 73 _._ 45%, respectively; the left and right ankle pitch torques are reduced by 70 _._ 71% and 61 _._ 66%, respectively. This is attributed to the continuous sliding motion in the swizzling gait, which avoids the periodic impacts at touchdown during walking. These results indicate that swizzling can reduce peak impact loads on key lowerlimb joints. 

_3) Joint-Mechanical Cost of Transport Comparison:_ For energy-efficiency evaluation, the walking baseline replaces the passive-wheel feet with rigid flat feet while preserving the same sensing and actuation stack. With each inline skate module being 0 _._ 24 kg heavier than the rigid flat foot, the 

TABLE IV: Comparison of peak joint torques between swizzling and walking 

|**Joint Name**|**Swizzling(N·m)**|**Walking(N·m)**|**Difference (%)**|
|---|---|---|---|
|L Hip Pitch|20_._86_±_6_._22|68_._47_±_1_._91|_−_69.53|
|L Hip Roll|56_._22_±_4_._08|60_._62_±_2_._25|_−_7.26|
|L Hip Yaw|23_._18_±_1_._39|33_._82_±_1_._19|_−_31.46|
|L Knee|49_._48_±_2_._98|51_._76_±_6_._84|_−_4.41|
|L Ankle Pitch|13_._58_±_2_._51|46_._37_±_6_._10|_−_70.71|
|L Ankle Roll|11_._80_±_2_._77|11_._08_±_1_._84|+6.55|
|R Hip Pitch|17_._87_±_3_._31|67_._32_±_0_._92|_−_73.45|
|R Hip Roll|59_._85_±_7_._91|85_._04_±_9_._45|_−_29.63|
|R Hip Yaw|23_._50_±_3_._19|40_._23_±_3_._62|_−_41.58|
|R Knee|42_._88_±_8_._85|45_._37_±_1_._99|_−_5.49|
|R Ankle Pitch|15_._21_±_2_._21|39_._67_±_0_._85|_−_61.66|
|R Ankle Roll|11_._78_±_1_._36|12_._45_±_0_._97|_−_5.37|


skating configuration is 0 _._ 48 kg heavier than the walking configuration, corresponding to 1 _._ 26% of its 38 kg total mass. Thus, the reported energy reduction cannot be attributed to a lighter skating setup. Each locomotion mode performs 5 repeated straight-line trials over 15 m at a commanded speed of 1 m/s. Since computing and sensing power are comparable, we report mechanical CoT [22]: 


where _τi_ and _ωi_ are the torque and angular velocity of joint _i_ , _M_ is the robot mass, _g_ is the gravitational acceleration, _D_ is the travel distance, and _n_ is the number of joints. 

Fig. 9 shows that swizzling reduces mechanical CoT by 63 _._ 34% compared with walking. The main savings occur in sagittal-plane joints: energy consumption of hip pitch decreases by approximately 95 _._ 39% and ankle pitch by 92 _._ 29%, while other joints show smaller changes. These results indicate that continuous rolling contact reduces the actuation demand associated with discrete stance-swing walking. 

## V. CONCLUSIONS 

This work demonstrates that swizzling is an effective entry-point gait primitive for passive-wheel humanoid inline skating. Built on the 33-DoF SKATER humanoid robot, the proposed reference-free deep reinforcement learning framework synthesizes swizzling without motion-capture demon- 


Fig. 9: Energy efficiency results: joint-level energy consumption and mechanical Cost of Transport comparison between swizzling and walking gaits. 

strations or manually designed reference motions. Rather than tracking a prescribed motion or using explicit gaitphase scheduling, the policy uses skating-specific physical constraints, including ZMP support, inter-foot geometry, bilateral symmetry and wheel axial-slip suppression, to guide whole-body motion learning under passive nonholonomic wheel-ground contact. Compared with a walking baseline on the same robot but with rigid flat feet, the learned swizzling gait reduces GRF-based Impact Intensity by 50 _._ 25% in simulation and mechanical CoT by 63 _._ 34% in real-world trials. Hardware experiments across different surfaces and high-speed traversal trials on flat ground further indicate the robustness and speed potential of the learned policy. These results suggest that continuous bilateral-support swizzling provides a practical foundation for low-impact and energyefficient humanoid inline skating. 

The current study remains limited to swizzling gaits with continuous contact of both feet. Lateral drift during straight-line skating and delayed velocity regulation during acceleration and braking remain observable, reflecting the limited steering and braking authority of passive inline wheels. Future work will extend this foundation toward more dynamic skating skills, such as push-step and single-support skating, integrate perception for autonomous navigation, and explore switchable wheel/flat-foot mechanisms to improve terrain adaptability. 

## REFERENCES 

   - [5] J. Han, W. Xie, J. Zheng, J. Shi, W. Zhang, T. Xiao, and C. Bai, “Kungfubot2: Learning versatile motion skills for humanoid wholebody control,” _arXiv:2509.16638_ , 2025. 

   - [6] A. T. Mahar, T. R. Derrick, J. Hamill, and G. E. Caldwell, “Impact shock and attenuation during in-line skating.” _Medicine and Science in Sports and Exercise_ , vol. 29, no. 8, pp. 1069–1075, 1997. 

   - [7] K. Itabashi and M. Kumagai, “Development of a human type legged robot with roller skates,” in _2010 IEEE/SICE International Symposium on System Integration_ , 2010, pp. 120–125. 

   - [8] K. Hashimoto, Y. Sugahara, H. O. Lim, and A. Takanishi, “Swizzle movement for biped walking robot having passive wheels,” _Journal of Robotics and Mechatronics_ , vol. 20, no. 3, pp. 413–419, 2008. 

   - [9] C. Iverach-Brereton, J. Baltes, J. Anderson, A. Winton, and D. Carrier, “Gait design for an ice skating humanoid robot,” _Robotics and Autonomous Systems_ , vol. 62, no. 3, pp. 306–318, 2014. 

   - [10] N. Takasugi, K. Kojima, S. Nozawa, F. Sugai, K. Yohei, K. Okada, and M. Inaba, “Extended three-dimensional walking and skating motion generation for multiple noncoplanar contacts with anisotropic friction: Application to walk and skateboard and roller skate,” _IEEE Robotics and Automation Letters_ , vol. 4, no. 1, pp. 9–16, 2019. 

   - [11] M. Bjelonic, C. D. Bellicoso, M. E. Tiryaki, and M. Hutter, “Skating with a force controlled quadrupedal robot,” in _2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2018, pp. 7555–7561. 

   - [12] J. Chen, R. Qin, L. Huang, Z. He, K. Xu, and X. Ding, “Unlocking versatile locomotion: A novel quadrupedal robot with 4-dofs legs for roller skating,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 8037–8043. 

   - [13] C. Tang, B. Abbatematteo, J. Hu, R. Chandra, R. Mart´ın-Mart´ın, and P. Stone, “Deep reinforcement learning for robotics: A survey of real-world successes,” _Annual Review of Control, Robotics, and Autonomous Systems_ , vol. 8, no. 1, pp. 153–188, 2025. 

   - [14] H. J. Lee, S. Hong, and S. Kim, “Integrating model-based footstep planning with model-free reinforcement learning for dynamic legged locomotion,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 11 248–11 255. 

   - [15] X. B. Peng, G. Berseth, K. Yin, and M. Van De Panne, “Deeploco: Dynamic locomotion skills using hierarchical deep reinforcement learning,” _Acm transactions on graphics (tog)_ , vol. 36, no. 4, pp. 1–13, 2017. 

   - [16] M. Vukobratovi´c and B. Borovac, “Zero-moment point—thirty five years of its life,” _International journal of humanoid robotics_ , vol. 1, no. 01, pp. 157–173, 2004. 

   - [17] S. Katayama, M. Murooka, and Y. Tazaki, “Model predictive control of legged and humanoid robots: models and algorithms,” _Advanced Robotics_ , vol. 37, no. 5, pp. 298–315, 2023. 

   - [18] M. L. Puterman, _Markov decision processes: discrete stochastic dynamic programming_ . John Wiley & Sons, 2014. 

   - [19] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

   - [20] M. Mittal, P. Roth, J. Tigue, A. Richard, O. Zhang, P. Du, A. SerranoMu˜noz, X. Yao, R. Zurbr¨ugg, N. Rudin _et al._ , “Isaac lab: A gpuaccelerated simulation framework for multi-modal robot learning,” _arXiv preprint arXiv:2511.04831_ , 2025. 

   - [21] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control,” in _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ . IEEE, 2012, pp. 5026–5033. 

   - [22] Y. G. Alqaham, J. Cheng, and Z. Gan, “Energy-optimal asymmetrical gait selection for quadrupedal robots,” _IEEE Robotics and Automation Letters_ , 2024. 

- [1] X. Gu, Y.-J. Wang, and J. Chen, “Humanoid-gym: Reinforcement learning for humanoid robot with zero-shot sim2real transfer,” _arXiv preprint arXiv:2404.05695_ , 2024. 

- [2] Z. Li, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control,” _The International Journal of Robotics Research_ , vol. 44, no. 5, pp. 840–888, 2025. 

- [3] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan _et al._ , “Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” _arXiv preprint arXiv:2502.01143_ , 2025. 

- [4] Z. Zhang, J. Guo, C. Chen, J. Wang, C. Lin, Y. Lian, H. Xue, Z. Wang, M. Liu, J. Lyu _et al._ , “Track any motions under any disturbances,” _arXiv preprint arXiv:2509.13833_ , 2025. 

