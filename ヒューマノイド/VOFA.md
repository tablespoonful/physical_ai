---
title: "VOFA: Visual Object Goal Pushing with Force-Adaptive Control for Humanoids"
date: "2026-05-02"
authors: "Zichao Hu; Zifan Xu; Dongsik Chang; He Yin; Linh Tran; Roberto Martín-Martín"
url: https://arxiv.org/abs/2605.01518
pdf: https://arxiv.org/pdf/2605.01518
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.01518)** / [論文ページ](https://arxiv.org/abs/2605.01518)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **VOFA: Visual Object Goal Pushing with Force-Adaptive Control for Humanoids** 

**Zichao Hu**<sup>**1**</sup> **, Zifan Xu**<sup>**1**</sup> **, Dongsik Chang**<sup>**2**</sup> **, He Yin**<sup>**2**</sup> **, Linh Tran**<sup>**1**</sup> **, Roberto Mart´ın-Mart´ın**<sup>**1,2**</sup> **Peter Stone**<sup>**1,3**</sup> **, Jingyu Qiao**<sup>**2**</sup> **, Joydeep Biswas**<sup>**1**</sup> 

> 1Department of Computer Science, The University of Texas at Austin 

- 2 Amazon Inc. 3Sony AI 


Fig. 1: We present VOFA, a visual goal-conditioned humanoid loco-manipulation system capable of pushing objects with unknown physical properties. The system adapts to different goal positions (a,b), object masses (c), and center-of-mass configurations (d) while maintaining stable, closed-loop control. 

**_Abstract_ — The ability to push large objects in a goal-directed manner using onboard egocentric perception is an essential skill for humanoid robots to perform complex tasks such as material handling in warehouses. To robustly manipulate heavy objects to arbitrary goal configurations, the robot must cope with unknown object mass and ground friction, noisy onboard perception, and actuation errors; all in a real-time feedback loop. Existing solutions either rely on privileged object-state information without onboard perception or lack robustness to variations in goal configurations and object physical properties. In this work, we present VOFA, a visual goal-conditioned humanoid loco-manipulation system capable of pushing objects with unknown physical properties to arbitrary goal positions.** 

**VOFA consists of a two-level hierarchical architecture with a high-level visuomotor policy and a low-level force-adaptive whole-body controller. The high-level policy processes noisy onboard observations and generates goal-conditioned commands to operate in closed loop across diverse object–goal configurations, while the low-level whole-body controller provides robustness to variations in object physical properties. VOFA is extensively evaluated in both simulation and realworld experiments on the Booster T1 humanoid robot. Our results demonstrate strong performance, achieving over 90% success in simulation and over 80% success in real-world trials. Moreover, VOFA successfully pushes objects weighing up to 17kg, exceeding half of the Booster T1’s body weight.**<sup>1</sup> 

> 1Code is available at https://github.com/ut-amrl/VOFA. 

Correspondence to: zichao@utexas.edu 

## I. INTRODUCTION 

Developing loco-manipulation capabilities for humanoid robots to perform useful tasks has gained increasing attention in robotics research [1]. One such capability is pushing large objects to designated locations to support real-world applications such as warehouse inventory reorganization. Successfully achieving this capability requires addressing several key challenges: (1) handling objects with unknown and diverse physical properties, such as mass and friction; (2) operating with noisy onboard visual observations without access to privileged object-state information; and (3) adapting in closed loop to different object–goal configurations. Recent progress in humanoid loco-manipulation driven by reinforcement learning has demonstrated promising capabilities; however, existing humanoid systems do not fully address the challenges presented by goal-directed object pushing. In particular, existing systems rely on privileged object-state sensing [2]–[6], lack adaptability to different object and goal configurations [7]–[9], or do not explicitly account for variations in object mass [10], [11]. 

In this work, we present VOFA (Visual Object–Goal Pushing with Force-Adaptive Control), a visual goal-conditioned humanoid loco-manipulation system capable of pushing objects with unknown physical properties (e.g., mass and friction) to arbitrary goal positions. VOFA employs a twolevel hierarchical architecture (Fig. 2) composed of a highlevel depth-image-based visuomotor policy and a low-level force-adaptive whole-body controller (WBC). The high-level policy processes onboard observations and outputs goalconditioned commands, which are translated by the lowlevel controller into joint-level control actions. To address unknown object physical properties, the low-level controller is explicitly designed as a force-adaptive controller following the FALCON [12] framework. This controller enables stable object interaction across diverse object masses and ground frictions. Together, the hierarchical design decouples low-level force-adaptive control from high-level visuomotor planning, simplifying policy training [7] while preserving robustness to variations in object physical properties. 

To efficiently learn a high-level policy driven by noisy onboard visual observations, VOFA follows a teacher–student design. The teacher policy is first trained as a goalconditioned policy using privileged proprioceptive and exteroceptive information ( _e.g.,_ the robot’s base linear velocity and the object’s orientation). DAgger [13] is then employed to distill a vision-based student policy that replaces privileged inputs with proprioceptive signals and onboard depth observations. During distillation, visual augmentations including camera extrinsic randomization and depth-noise injection (Fig. 3) are incorporated to improve robustness to perception noise and background distractions at deployment. 

To enable VOFA to adapt in closed loop to arbitrary goal positions, training is conducted in large-scale Isaac Gym simulation with extensive randomization over initial object 

and goal placements. An object–goal alignment reward is further introduced to encourage the robot to first reposition itself to the opposite side of the object relative to the goal before initiating contact (Fig. 5). This simple yet effective reward design removes the need to manually define separate training stages [8], [14] to complete the full task. It promotes consistent object–robot alignment and enables corrective behavior when deviations from the desired object trajectory occur. 

Our system, VOFA, achieves over 90% success rates in simulation and over 80% success rates in real-world experiments across a range of initial object and goal positions and diverse object physical properties. In real-world deployment (Fig. 1), VOFA successfully pushes objects weighing 17 kg (more than half of the Booster T1 robot’s body weight) despite not being trained on such object masses in simulation. Leveraging closed-loop visual feedback, VOFA remains robust even when the object’s center of mass is intentionally shifted to previously unseen locations, and is able to detect and recover from deviations in the object’s motion online. In addition, VOFA supports long-horizon boxpushing tasks, sequentially pushing the object to multiple goal locations. Together, these results demonstrate robust closed-loop performance and highlight the potential of VOFA to enable more complex downstream applications, such as object rearrangement. Overall, our key contributions are: 

- 1) We present a visual humanoid object–goal pushing system that enables closed-loop, goal-directed pushing across diverse object–goal configurations. 

- 2) Our system handles objects with diverse and even previously unseen masses, successfully pushing objects up to 17kg—more than half of the robot’s body weight. 

- 3) We validate our approach in both large-scale simulation and real-world experiments on the Booster T1 humanoid robot, achieving high success rates across diverse scene configurations and object physical properties. 

## II. RELATED WORK 

In this section, we review related work on humanoid whole-body control and autonomous legged locomanipulation. 

## _A. Humanoid Whole Body Control_ 

A substantial body of recent work has explored learningbased whole-body control (WBC) for humanoid robots, demonstrating stable and expressive full-body behaviors such as locomotion, balance, and dynamic motion generation [16]–[20]. Many of these approaches rely on largescale motion imitation and primarily focus on reproducing coordinated human motions. Beyond expressive wholebody motions, other work investigates WBC for teleoperated loco-manipulation, enabling humanoids to interact with objects while maintaining whole-body stability [12], 


Fig. 2: **VOFA Design.** VOFA adopts a hierarchical architecture that combines a high-level visuomotor policy with a force-adaptive whole-body controller [12] for humanoid visual object–goal pushing. The high-level policy is trained in a teacher–student framework: a teacher policy is trained with privileged observations and goal positions using PPO [15], and a vision-based student policy is distilled via DAgger [13] using onboard sensory inputs and goal information. Training uses four reward terms—reach, push, track, and alignment—to promote robust closed-loop object–goal interaction. 

[21]–[25]. Among these works, FALCON [12] introduces a force-adaptive whole-body controller for humanoid locomanipulation, providing robustness to substantial and unknown external forces at the end-effector during object interaction. In this work, we build on FALCON and extend it with a hierarchical, vision-based framework to enable goalconditioned visual object pushing for humanoid robots. 

## _B. Sim-to-Real Reinforcement Learning for Autonomous Humanoid Loco-Manipulation_ 

Enabling legged robots to autonomously perform locomanipulation is important for deploying robots to perform useful tasks in human-inhabited environments. Prior work on autonomous loco-manipulation has studied both quadruped [2], [3] and humanoid [4]–[6] robots; however, these approaches typically rely on privileged object state information rather than onboard visual perception. More recently, vision-based humanoid loco-manipulation has been explored by incorporating onboard visual perception into whole-body policies [7], [8], [10]; however, these approaches do not explicitly study goal-conditioned object interaction or robustness to variations in object physical properties. Visual, goal-directed humanoid loco-manipulation under variations in object mass and physical properties is still challenging. In this work, we aim to address this gap through sim-to-real reinforcement learning. 

## III. METHOD 

**Problem Setup:** We consider the problem of visual goaldirected object pushing with a humanoid robot. At each timestep _t_ , the robot receives observations consisting of proprioceptive measurements **_o_**<sup>prop</sup> _t_ , depth observations **_o_**<sup>depth</sup> _t_ , and a desired object goal position **_p_**<sup>goal</sup> _t_ . The objective is to learn a control policy that maps a history of observations to 

humanoid joint position targets **_a_** _t_ such that it controls the robot to push the object to the specified goal location. 

**System Overview:** We present VOFA, a visual goalconditioned loco-manipulation system with a two-level hierarchical architecture. The high-level policy _πH_ ( **_u_** _t |_ **_o_**<sup>prop</sup> _t−h_ 1: _t_<sup>_,_</sup><sup>**_o_**depth</sup> _t−h_ 2: _t_<sup>_,_</sup><sup>**_p_**</sup> _t_<sup>goal</sup> ) first maps a history of proprioceptive and depth observations and the goal position to a high-level command **_u_** _t_ (Sec. III-A). Then, the high-level command is provided as input to a low-level force-adaptive controller _πL_ ( **_a_** _t |_ **_u_** _t_ ), which outputs joint position targets **_a_** _t_ (Sec. IIIB). Both policies are trained in IsaacGym simulation and operate at 50Hz. Beyond the architectural design, we detail the reward formulation (Sec. III-C) and the domain randomization strategy enabling zero-shot transfer to the real robot (Sec. III-D) in the following subsections as well. 

## _A. High-Level Policy Design and Training_ 

To efficiently train the high-level policy, we adopt a teacher–student paradigm. 

_a) Teacher Policy Design:_ We first train a goalconditioned teacher policy to output actions within the lowlevel WBC’s valid command range [7]. The teacher policy is trained using privileged observations with PPO [15] under an asymmetric actor–critic framework [26], which has been shown to be effective in prior work [3]. 

The actor receives privileged observations **_o_**<sup>priv</sup> _t_ = ( **_o_**<sup>prop-priv</sup> _t ,_ **_o_**<sup>exte-priv</sup> _t ,_ **_p_**<sup>goal</sup> _t_ ), consisting of privileged proprioceptive information, privileged exteroceptive information, and the goal position. Proprioceptive inputs are given by **_o_**<sup>prop-priv</sup> _t_ = ( **_v_** _t,_ **_ω_** _t,_ **_g_** _t,_ **_u_**<sup>teacher</sup> _t−_ 1<sup>_,_</sup><sup>**_q_**</sup> _t_<sup>upper</sup> _,_ **_q_** ˙<sup>upper</sup> _t_ ), including linear and angular velocities, projected gravity, the previous high-level action, upper-body joint positions and ve= locities. Exteroceptive inputs are given by **_o_**<sup>exte-priv</sup> _t_ ( **_p_**<sup>ee,r-obj</sup> _t ,_ **_p_**<sup>ee,l-obj</sup> _t ,_ **_R_** _t_ ), comprising the relative positions of the 

right and left end effectors with respect to the object and the object orientation. All quantities are expressed in the robot base frame. 

The critic observes all actor inputs and additionally = receives privileged object state information **_o_**<sup>priv-critic</sup> _t_ � _ct,_ **_p_**<sup>obj</sup> _t_<sup>_,m_obj</sup> _t_<sup>_,_</sup><sup>**_d_**obj</sup> _t_<sup>_,_</sup><sup>**_v_**obj</sup> _t_<sup>_,_</sup><sup>**_ω_**obj</sup> _t_ � _,_ where _ct_ denotes the object contact flag, **_p_**<sup>obj</sup> _t_ is the object center-of-mass position, _m_<sup>obj</sup> _t_ and **_d_**<sup>obj</sup> _t_ represent the object mass and dimensions, and **_v_**<sup>obj</sup> _t_ and **_ω_**<sup>obj</sup> _t_ are the object linear and angular velocities. _b) Student Policy Design:_ We employ DAgger [13] to distill a vision-based student policy from the teacher by replacing privileged proprioceptive and exteroceptive inputs ( **_o_**<sup>prop-priv</sup> _t ,_ **_o_**<sup>exte-priv</sup> _t_ ) with a history of onboard proprioceptive observations and depth images ( **_o_**<sup>prop</sup> _t−_ 50: _t_<sup>_,_</sup><sup>**_o_**depth</sup> _t−_ 3: _t_<sup>).Thepropri-</sup> oceptive observation **_o_**<sup>prop</sup> _t_ = ( **_ω_** _t,_ **_g_** _t,_ **_u_**<sup>student</sup> _t−_ 1<sup>_,_</sup><sup>**_q_**</sup> _t_<sup>_,_</sup><sup>**_q_**˙</sup> _t_<sup>)consists</sup> of the base angular velocity, projected gravity, the previous high-level action, and the joint positions and velocities. The student policy encodes the proprioceptive history using temporal 1D convolutions [14], while each depth observation is processed by a convolutional neural network to extract visual features. The proprioceptive and visual embeddings are then fused and passed through an MLP projection head that aggregates the combined representation for action prediction. To improve training efficiency, the policy maintains a rolling buffer of the three most recent depth frames, processes depth observations at 5Hz, and downsamples the resolution of images (from 640 _×_ 360 to 32 _×_ 32). 

## _B. Low-Level Policy Design and Training_ 

We adopt a force-adaptive whole-body controller (WBC) as the low-level policy to handle substantial and unknown end-effector interaction forces, which commonly arise in object-pushing tasks due to variations in object physical properties (e.g., mass). In this work, we choose FALCON [12] as it is explicitly trained for force-adaptive control using a curriculum that progressively increases external forces at the end-effectors. In addition, FALCON is trained on the AMASS [27] motion dataset, which spans a broad range of natural human motions, including behaviors relevant to box pushing. FALCON receives a high-level command **_u_** _t_ = ( **_u_**<sup>lower</sup> _t ,_ **_q_**<sup>upper</sup> _t_ ), where the lower-body locomotion command **_u_**<sup>lower</sup> _t_ = ( **_v_**<sup>lin</sup> _t_<sup>_,_ang</sup> _, ϕ_<sup>stance</sup> _t , h_<sup>root</sup> _t , ωt_<sup>yaw</sup> ) specifies the desired root linear and angular velocities, walking-mode indicator, root height, and waist yaw angle, and **_q_**<sup>upper</sup> _t_ denotes upper-body target joint positions. In this work, the walkingmode indicator, root height, and waist yaw angle are set to their default values (1, 0 _._ 62, and 0, respectively), while learning a residual upper-body target joint position ∆ **_q_**<sup>upper</sup> _t_ . FALCON is trained for 10k epochs using PPO and is kept frozen during subsequent high-level policy training. 

## _C. Reward Design_ 

To enable the teacher policy to learn effective object goal pushing behavior, we design four main rewards: 


Fig. 3: **Egocentric vision of the humanoid robot** . During training, we apply three vision augmentations: _farplane depth perturbation_ , _correlated depth noise_ , and _pixel dropout_ . 

- 1) **Reaching the object with both end-effectors.** To encourage both end-effectors to approach the object, we define the per–end-effector reaching terms as 


The overall reaching reward is computed as the harmonic mean of the two end-effector terms: 


- 2) **Pushing the object toward the goal.** The robot is rewarded for reducing the object–goal distance: 


- 3) **Head tracking reward.** The robot is encouraged to visually track the object: 


where _θt_ is the angular deviation between the head (camera optical axis) and the object direction, and _θ_ fov denotes half of the camera field of view. 

- 4) **Object–goal alignment reward.** To promote goaldirected pushing configurations, we define: 


where _θt_<sup>align</sup> is the normalized angle between the object–robot and object–goal direction vectors. 

Notably, the object–goal alignment reward is critical for learning effective goal-conditioned pushing behavior, as demonstrated by the ablation study in Sec. IV-C. In addition to these four main task rewards, we incorporate several penalty terms to regularize the robot’s behavior and improve stability. 

TABLE I: Performance under different initial goal positions. 

||Overall||Front|||Lateral|||Rear||
|---|---|---|---|---|---|---|---|---|---|---|
|Method|SR(%) _↑_|SR(%) _↑_|Pre-C.(%) _↓_|Post-C. _↓_|SR (%) _↑_|Pre-C.(%) _↓_|Post-C.(%) _↓_|SR(%) _↑_|Pre-C.(%) _↓_|Post-C.(%) _↓_|
|Teacher w/ FA (ours)|**97****_._84**|**98****_._12**|**0****_._72**|**0****_._96**|**97****_._58**|**1****_._00**|**1****_._16**|**97****_._34**|**1****_._12**|**1****_._08**|
|Teacher w/o FA|76_._94|83_._78|2_._92|5_._52|79_._00|4_._88|6_._58|71_._86|6_._46|7_._38|
|Student w/ FA (ours)|**91****_._38**|**91****_._97**|**1****_._84**|**2****_._42**|**91****_._40**|**1****_._30**|**3****_._22**|**90****_._22**|**1****_._92**|**3****_._98**|
|Student w/o FA|59_._32|71_._16|2_._68|7_._00|64_._90|4_._52|7_._78|56_._06|5_._64|8_._84|


TABLE II: Performance under different box mass. 

|||Light|||Medium|||Heavy||Ext|ra Heavy|(Unseen)|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Method|SR(%) _↑_|Pre-C.(%) _↓_|Post-C.(%) _↓_|SR(%) _↑_|Pre-C.(%) _↓_|Post-C.(%)|_↓_SR (%) _↑_|Pre-C.(%) _↓_|Post-C.(%) _↓_|SR(%) _↑_|Pre-C.(%)|_↓_Post-C.(%) _↓_|
|Teacher w/ FA (ours)|**97****_._40**|**1****_._12**|**1****_._34**|**98****_._22**|**0****_._92**|**0****_._74**|**97****_._46**|**1****_._06**|**1****_._08**|**87****_._92**|**0****_._88**|**4****_._16**|
|Teacher w/o FA|82_._18|5_._40|9_._00|80_._98|5_._08|6_._06|69_._76|4_._64|6_._06|53_._68|4_._78|5_._66|
|Student w/ FA (ours)|**93****_._50**|**1****_._46**|**3****_._06**|**93****_._30**|**1****_._40**|**2****_._74**|**89****_._16**|**1****_._22**|**3****_._22**|**69****_._00**|**1****_._30**|**6****_._30**|
|Student w/o FA|70_._98|6_._60|9_._46|62_._68|5_._98|7_._64|48_._66|6_._56|9_._58|32_._00|5_._36|9_._94|


## _D. Environment Setup and Domain Randomization_ 

During training, we randomize object physical properties and initial object–goal configurations. We consider a boxshaped object and randomize its mass (1–8 kg) and friction coefficients (0.1–1.0) to promote robustness across diverse physical conditions. Goals are placed uniformly over a 360<sup>_◦_</sup> arc around the robot at a radius of 2.5–3.5 m. Objects are randomly initialized within the robot’s field of view ( _±_ 60<sup>_◦_</sup> ) and initial distances of 1.8–2.2 m. 

To reduce the sim-to-real gap in visual perception, we match the camera intrinsics in simulation to those of the real robot’s cameras (ZED 2i). However, small differences in camera mounting can result in slight viewpoint variations, even across robots of the same model. To account for this variability, we apply random extrinsic perturbations during training, including translations of _±_ 3 cm in x,y,z and rotations of _±_ 5° (yaw), _±_ 5° (pitch), and _±_ 2° (roll). In addition, real-world depth images exhibit sensor artifacts such as interference from background objects and isolated pixels with spuriously large depth values, as shown in Fig. 3b. To emulate these effects, we apply three visual randomizations as shown in Fig. 3c. First, we introduce _far-plane depth perturbation_ , where random rectangular patches are placed in the upper image region (above an estimated ground boundary) and overwritten with blocky far-depth noise to simulate transient background clutter. Second, we apply _correlated depth noise_ by adding spatially correlated low-frequency Gaussian noise to the depth map, modeling structured sensor distortions. Third, we apply _pixel dropout_ , randomly zeroing depth pixels to simulate missing or unreliable returns. An ablation study on the effectiveness of these randomizations is presented in Sec. IV-E. 

## IV. EXPERIMENTAL RESULTS 

In this section, we conduct a series of simulation and realworld experiments, with policies trained in IsaacGym and 

deployed on the Booster T1 humanoid robot, to answer the following research questions: 

- 1) How robust is VOFA across varying initial goal configurations and object masses (Sec. IV-A)? 

- 2) Is using a force-adaptive whole-body control beneficial for VOFA (Sec. IV-B)? 

- 3) Does the object–goal alignment reward design mitigate failure modes in challenging initial configurations (Sec. IV-C)? 

- 4) How well does the policy transfer from simulation to the real world (Sec. IV-D)? 

- 5) How effective is the proposed visual randomization strategy for sim-to-real transfer (Sec. IV-E)? 

- 6) Can the policy perform with closed-loop control when pushing the object (Sec. IV-F)? 

## _A. Performance Across Initial Configurations and Masses_ 

We conduct two sets of quantitative simulation experiments using three metrics: _Success Rate (SR)_ , _Terminated Pre-Contact (Pre-C.)_ , and _Terminated Post-Contact (PostC.)_ . An episode is successful if the object is pushed within 0.3 m of the goal and remains there for 2 s. Pre-C. and PostC. denote that the robot falls before and after object contact, respectively. 

As shown in Tab. I, we evaluate three goal-position categories based on the relative goal angle _θ_ : _front_ ( _|θ| ∈_ [0<sup>_◦_</sup> _,_ 60<sup>_◦_</sup> ]), _lateral_ ( _|θ| ∈_ [60<sup>_◦_</sup> _,_ 120<sup>_◦_</sup> ]), and _rear_ ( _|θ| ∈_ [120<sup>_◦_</sup> _,_ 180<sup>_◦_</sup> ]). Performance remains consistently high across all configurations, with success rates above 97% for the teacher and 90% for the student. Even in rear configurations, which require longer-horizon repositioning, performance degrades only marginally. 

As shown in Tab. II, we evaluate four mass ranges: _light_ (1–3 kg), _medium_ (3–5 kg), _heavy_ (5–8 kg), and _extra-heavy_ (8–12 kg), with the last range outside the training distribution. The policy remains robust across all in-distribution 


(a) w/ Force-Adaptive Controller (ours) 


Fig. 4: **Force-Adaptive Controller Ablation.** With the force-adaptive controller, the robot stably pushes the object using its end-effector (a). Without it, the robot struggles to apply consistent forces, often resorting to kicking, which results in unstable behavior and a higher risk of falling. 


(b) w/o Align Reward 

Fig. 5: **Object-Goal Alignment Reward Ablation.** The alignment reward enables the policy to reposition around the object before pushing it toward the goal (a). Without it, the robot tends to make premature contact and fails to push the object to the goal (b). 

masses and achieves a 69% success rate in the extra-heavy setting. 

Across these experiments, we observe three failure modes: failing to push the box to the target, falling before contact, and falling after contact. Compared with the teacher, the student exhibits more target-reaching failures and postcontact falls, highlighting the added challenge of replacing privileged object-state information with noisy onboard visual observations while maintaining closed-loop performance. 

## _B. Effect of Force-Adaptive Whole-Body Control on VOFA_ 

To evaluate the impact of force-adaptive whole-body control, we train ablated variants of VOFA by disabling random end-effector force perturbations during FALCON pretraining. We evaluate both teacher and student policies under varying initial goal configurations and object masses using the same setup as Sec. IV-A (Tab. I and Tab. II). Across all settings, force-adaptive control yields higher success rates and fewer terminations. Without force adaptation, performance degrades notably in lateral and rear configurations and for heavier objects, as the robot struggles to push the object to the target goal location. Fig. 4 presents a qualitative comparison of the robot’s behavior with and without the force-adaptive controller. Without the force-adaptive controller, the robot struggles to apply consistent contact forces and often resorts to impulsive kicking motions, leading to unstable behavior and an increased risk of falling. Overall, these results show that force-adaptive whole-body control is beneficial for robust loco-manipulation in VOFA. 

## _C. Impact of Object–Goal Alignment Reward_ 

Without the object–goal alignment reward, we observe a consistent failure mode in which the robot prematurely approaches the object when the object lies on the opposite side of the robot from the goal as shown in Fig. 5. In such cases, the policy is driven by the _R_ reach reward to make early contact, which prevents effective pushing toward the goal. As a result, the policy struggles to explore behaviors that require first repositioning the robot to a more favorable location before pushing. In contrast, introducing the object–goal alignment reward encourages deliberate repositioning prior to contact, significantly improving task success in these challenging configurations by promoting long-horizon execution rather than myopic contact strategies. 

## _D. Sim-to-Real Transfer Performance_ 

To evaluate sim-to-real transfer, we deploy the policy on the Booster T1 humanoid to push a 5kg cardboard box measuring approximately 1 _._ 0 _×_ 1 _._ 0 _×_ 0 _._ 7m. During deployment, we use motion capture to provide the relative goal position. While this quantity could also be obtained from a separate localization system, using motion capture allows us to focus the evaluation on the proposed visual object-pushing system. We first evaluate performance across three goal configurations: _front_ (goal at 0<sup>_◦_</sup> ), _lateral_ (goal at _±_ 90<sup>_◦_</sup> ), and _rear_ (goal at 180<sup>_◦_</sup> ). For each configuration, we perform 10 real-world trials, with the object randomly placed within the robot’s initial field of view following the ranges 


Fig. 6: **Real World Deployment Results** . VOFA demonstrates strong sim-to-real transfer performance. Real-world experiments highlight the benefits of visual randomization across different goal positions (a) and the force-adaptive low-level controller across varying object masses (b). 


Fig. 7: **Closed-Loop Demonstration.** The policy reacts to external disturbances (a) and supports sequential goal switching without reset (b), illustrating closed-loop control. 

used during training. As shown in Fig. 6a, the policy achieves consistently strong real-world performance across all goal configurations. In addition, we evaluate robustness to object mass by attaching additional weights to the box. We perform 5 real-world trials for each of the four mass conditions: _light_ (no additional weight), _medium_ (2.5kg), _heavy_ (4.5kg), and _extra-heavy_ (12kg). To isolate the effect of object mass, we fix the goal location 4m directly in front of the robot. As shown in Fig. 6b, the policy equipped with force-adaptive whole-body control maintains stable performance across all tested mass conditions, whereas the non–force-adaptive baseline degrades substantially as object mass increases. Notably, VOFA successfully pushes a 17kg object (12kg payload + 5kg box), exceeding half of the Booster T1 robot’s body weight, despite not being trained on such heavy objects in simulation. This real-world trend mirrors the simulation results, further validating the role of force-adaptive control in enabling robust sim-to-real transfer. 

## _E. Effectiveness of Visual Randomization_ 

To assess the effectiveness of the proposed visual randomization strategy, we conduct an ablation study by training a policy without visual randomization and evaluating it under 

the same real-world conditions described in the previous subsection (Fig. 6a). Without visual randomization, policy performance degrades substantially for tasks that require longer-horizon execution, particularly in lateral and rear goal configurations. As the robot moves through the environment, it encounters a wider range of background structures and viewpoints, increasing sensitivity to visual noise and domain mismatch. In the absence of visual randomization during training, these effects lead to unstable behaviors, including confusion between background objects and the target object or failure to correctly localize the goal. In contrast, visual randomization improves robustness to such visual variations, enabling more reliable sim-to-real transfer. 

## _F. Closed-Loop Object Pushing_ 

To evaluate whether the policy performs closed-loop control during object pushing, we conduct three experiments in both simulation and the real world. 

_a) External Perturbation.:_ As shown in Fig. 7a, we apply a lateral impulse perpendicular to the pushing direction, displacing the object from its nominal path. The robot reacts by halting forward motion, reorienting to locate the displaced object, navigating around it to re-establish 

object–goal alignment, and subsequently resuming pushing toward the target. Successful task completion under this disturbance demonstrates online feedback correction rather than open-loop execution. 

_b) Off-Centered Mass Distribution.:_ As shown in Fig. 1d, we attach additional weights to one side of the object to create an off-centered center of mass (COM). This causes the box to rotate and deviate from the desired trajectory when being pushed. Similar to the externalperturbation example in Fig. 7a, the robot detects this deviation and repositions itself to push the box to the goal. 

_c) Sequential Goal Switching.:_ As shown in Fig. 7b, we evaluate reactive re-planning by assigning multiple goals sequentially. The robot first pushes the object to a front goal location. Upon reaching this target, a new goal is issued behind the robot. The robot repositions itself by navigating around the object and then pushes it toward the updated goal position without reset. 

Collectively, these experiments qualitatively demonstrate that the policy operates in a closed-loop manner: actions are continuously conditioned on updated observations, enabling disturbance rejection, dynamic re-alignment, and goal adaptation during object pushing. 

V. CONCLUSION, LIMITATIONS, AND FUTURE WORK 

In this work, we present VOFA, a visual goal-conditioned humanoid object pushing system. By integrating a forceadaptive whole-body controller with a depth-based visuomotor policy trained via teacher–student distillation and extensive domain randomization, VOFA achieves robust closedloop performance under diverse goal configurations and object physical properties. Extensive simulation and real-world experiments demonstrate strong generalization across goal positions, robustness to object masses, and effective sim-toreal transfer. Despite these results, our approach has several limitations. First, we focus on single-object scenarios and do not explicitly consider environments with multiple objects or highly diverse background variations, which may introduce additional perceptual ambiguity. Second, the system assumes access to the relative goal position during deployment. Although this information could be supplied by a localization system, integrating such a system would introduce additional complexity. In future work, we aim to extend VOFA to more cluttered multi-object environments and develop an end-toend framework that jointly reasons about object and goal localization from onboard perception. 

REFERENCES 

- [1] Z. Gu, J. Li, W. Shen, _et al._ , “Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning,” 2025. [Online]. Available: https://arxiv.org/abs/2501.02116 

- [2] S. Jeon, M. Jung, S. Choi, _et al._ , “Learning whole-body manipulation for quadrupedal robot,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 1, pp. 699–706, 2024. 

- [3] I. Dadiotis, M. Mittal, N. Tsagarakis, _et al._ , “Dynamic object goal pushing with mobile manipulators through model-free constrained reinforcement learning,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , 2025, pp. 13 363–13 369. 

- [4] Z. Zhang, C. Chen, H. Xue, _et al._ , “Unleashing humanoid reaching potential via real-world-ready skill space,” _IEEE Robotics and Automation Letters_ , vol. 11, no. 2, pp. 2082–2089, 2026. 

- [5] H. Weng, Y. Li, N. Sobanbabu, _et al._ , “Hdmi: Learning interactive humanoid whole-body control from human videos,” 2025. [Online]. Available: https://arxiv.org/abs/2509.16757 

- [6] Z. Su, B. Zhang, N. Rahmanian, _et al._ , “Hitter: A humanoid table tennis robot via hierarchical planning and learning,” 2025. [Online]. Available: https://arxiv.org/abs/2508.21043 

- [7] S. Yin, Y. Ze, H.-X. Yu, _et al._ , “Visualmimic: Visual humanoid locomanipulation via motion tracking and generation,” 2025. [Online]. Available: https://arxiv.org/abs/2509.20322 

- [8] H. Xue, T. He, Z. Wang, _et al._ , “Opening the sim-to-real door for humanoid pixel-to-action policy transfer,” 2025. [Online]. Available: https://arxiv.org/abs/2512.01061 

- [9] P. Zhi, P. Li, J. Yin, B. Jia, and S. Huang, “Learning unified force and position control for legged loco-manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2505.20829 

- [10] T. He, Z. Wang, H. Xue, _et al._ , “Viral: Visual sim-to-real at scale for humanoid loco-manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2511.15200 

- [11] J. Hu, P. Stone, and R. Mart´ın-Mart´ın, “Slac: Simulation-pretrained latent action space for whole-body real-world rl,” 2025. [Online]. Available: https://arxiv.org/abs/2506.04147 

- [12] Y. Zhang, Y. Yuan, P. Gurunath, _et al._ , “Falcon: Learning force-adaptive humanoid loco-manipulation,” _arXiv preprint arXiv:2505.06776_ , 2025. 

- [13] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” ser. Proceedings of Machine Learning Research. PMLR, 2011. [Online]. Available: https://proceedings.mlr.press/v15/ross11a.html 

- [14] Z. Xu, M. Seo, D. Lee, _et al._ , “Learning agile striker skills for humanoid soccer robots from noisy sensory input,” 2025. [Online]. Available: https://arxiv.org/abs/2512.06571 

- [15] J. Schulman, F. Wolski, P. Dhariwal, _et al._ , “Proximal policy optimization algorithms,” _ArXiv_ , vol. abs/1707.06347, 2017. [Online]. Available: https://api.semanticscholar.org/CorpusID:28695052 

- [16] T. He, J. Gao, W. Xiao, Y. Zhang, _et al._ , “Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” _arXiv preprint arXiv:2502.01143_ , 2025. 

- [17] M. Ji, X. Peng, F. Liu, _et al._ , “Exbody2: Advanced expressive humanoid whole-body control,” _arXiv preprint arXiv:2412.13196_ , 2024. 

- [18] Q. Liao, T. E. Truong, X. Huang, _et al._ , “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” 2025. [Online]. Available: https://arxiv.org/abs/2508.08241 

- [19] T. Zhang, B. Zheng, R. Nai, _et al._ , “Hub: Learning extreme humanoid balance,” _arXiv preprint arXiv:2505.07294_ , 2025. 

- [20] Z. Luo, Y. Yuan, T. Wang, _et al._ , “Sonic: Supersizing motion tracking for natural humanoid whole-body control,” _arXiv preprint arXiv:2511.07820_ , 2025. 

- [21] J. Li, X. Cheng, T. Huang, _et al._ , “Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control,” _Robotics: Science and Systems 2025_ , 2025. 

- [22] Y. Li, Y. Lin, J. Cui, _et al._ , “Clone: Closed-loop whole-body humanoid teleoperation for long-horizon tasks,” 2025. 

- [23] Q. Ben, F. Jia, J. Zeng, _et al._ , “Homie: Humanoid locomanipulation with isomorphic exoskeleton cockpit,” _arXiv preprint arXiv:2502.13013_ , 2025. 

- [24] T. He, Z. Luo, X. He, _et al._ , “Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning,” in _8th Annual Conference on Robot Learning_ , 2024. 

- [25] Y. Ze, Z. Chen, J. P. Araujo, _et al._ , “Twist: Teleoperated whole-body imitation system,” in _Proceedings of The 9th Conference on Robot Learning_ , vol. 305. PMLR, 27–30 Sep 2025, pp. 2143–2154. [Online]. Available: https://proceedings.mlr.press/v305/ze25a.html 

- [26] L. Pinto, M. Andrychowicz, P. Welinder, _et al._ , “Asymmetric actor critic for image-based robot learning,” 2017. [Online]. Available: https://arxiv.org/abs/1710.06542 

- [27] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, _et al._ , “Amass: Archive of motion capture as surface shapes,” in _The IEEE International Conference on Computer Vision (ICCV)_ , Oct 2019. [Online]. Available: https://amass.is.tue.mpg.de 

APPENDIX 

|**Actor observations**|**Dimensions**|
|---|---|
|EE-object relative position|9|
|Object rotation matrix|3|
|Arm dof position|10|
|Arm dof velocity|10|
|Base linear velocity|3|
|Base angular velocity|3|
|Projected gravity|3|
|Relative goal position|2|
|Last action|13|
|Total dim|56|
|**Priv. critic observations**|**Dimensions**|
|Object contact|1|
|Object CoM|3|
|Object mass|9|
|Object dimension|9|
|Object linear velocity|3|
|Object angular velocity|3|
|Total dim|84|


TABLE III: Observation dimensions for an asymmetric actorcritic setup used to train the high-level teacher policy. 

|**Student proprioception observations**|**Dimensions**|
|---|---|
|Projected gravity<br>|3|
|Base angular velocity|3|
|Dof position|23|
|Dof velocity|23|
|Last action|13|
|Relative goal position|2|
|Total dim|67|
|**Student image observations**|**Dimensions**|
|Depth image (_N_img_× H × W_)|3_×_32_×_32|


TABLE IV: Observation dimensions for the high-level student policy. 

|**Main Reward**|**Param.** _σ_|**Weight**|
|---|---|---|
|Reach object|_σ_reach = 2_._0|1_._25|
|Push object to goal|_σ_push = 10_._0|2_._5|
|Head track object|_σ_track = 0_._5|1_._0|
|Object-goal alignment|_σ_align = 0_._25|2_._0|
|**Auxilary Penalty**|**Expression**<br>|**Weight**|
|Command smoothness|_∥_**u**_t −_**u**_t−_1_∥_<sup>2</sup><br>2<br>|_−_1_._0|
|Object balance|_∥θ_object tilt_∥_<sup>2</sup><br>2|_−_0_._5|
|Upper joint action|<br>_∥_**q**<sup>upper</sup><br>_t_<br>_∥_<sup>2</sup><br>2|_−_0_._5|


TABLE V: Reward terms and weights 

