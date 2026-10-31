---
title: "CLOT: Closed-Loop Global Motion Tracking for Whole-Body Humanoid Teleoperation"
date: "2026-02-13"
authors: "Tengjie Zhu; Guanyu Cai; Yang Zhaohui; Guanzhu Ren; Haohui Xie; ZiRui Wang"
url: https://arxiv.org/abs/2602.15060
pdf: https://arxiv.org/pdf/2602.15060
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.15060)** / [論文ページ](https://arxiv.org/abs/2602.15060)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# CLOT: Closed-Loop Global Motion Tracking for Whole-Body Humanoid Teleoperation 

Tengjie Zhu<sup>1,2,*</sup> , Guanyu Cai<sup>1,*</sup> , Zhaohui Yang<sup>1,*</sup> , Guanzhu Ren<sup>1</sup> , Haohui Xie<sup>1</sup> , Junsong Wu<sup>1</sup> , ZiRui Wang<sup>2</sup> , Jingbo Wang<sup>2</sup> , Xiaokang Yang<sup>1</sup> , Yao Mu<sup>1,2,</sup><sup>_†_</sup> , Yichao Yan<sup>1,</sup><sup>_†_</sup> 

> 1MoE Key Lab of Artificial Intelligence, AI Institute, Shanghai Jiao Tong University 

> 2Shanghai AI Laboratory 

- *Authors with equal contribution, _†_ Corresponding author 


Fig. 1: **Long-horizon whole-body teleoperation with global pose closed-loop feedback.** The proposed framework achieves drift-free human-to-humanoid mimicry on a full-size humanoid, enabling real-world high-dynamic motions and whole-body dexterous manipulation in contact-rich tasks over extended time horizons. 

**_Abstract_ —Long-horizon whole-body humanoid teleoperation remains challenging due to accumulated global pose drift, particularly on full-sized humanoids. Although recent learning-based tracking methods enable agile and coordinated motions, they typically operate in the robot’s local frame and neglect global pose feedback, leading to drift and instability during extended execution. In this work, we present CLOT, a real-time wholebody humanoid teleoperation system that achieves closed-loop global motion tracking via high-frequency localization feedback. CLOT synchronizes operator and robot poses in a closed loop, enabling drift-free human-to-humanoid mimicry over long time horizons. However, directly imposing global tracking rewards in reinforcement learning, often results in aggressive and brittle corrections. To address this, we propose a data-driven randomization strategy that decouples observation trajectories from reward evaluation, enabling smooth and stable global corrections. We further regularize the policy with an adversarial motion prior to suppress unnatural behaviors. To support CLOT, we collect 20 hours of carefully curated human motion data for training the humanoid teleoperation policy. We design a transformerbased policy and train it for over 1300 GPU hours. The policy is deployed on a full-sized humanoid with 31 DoF (excluding hands). Both simulation and real-world experiments verify highdynamic motion, high-precision tracking, and strong robustness in sim-to-real humanoid teleoperation. Motion data, demos and** 

**code can be found in our website: CLOT.github.io/.** 

## I. INTRODUCTION 

Collecting high-quality, long-horizon loco-manipulation data is a key prerequisite for advancing general-purpose humanoid robots [1]. Robust humanoid teleoperation systems [2, 3] play a central role in this process by enabling the efficient generation of complex, embodied demonstrations. Ideally, such systems should simultaneously provide (i) whole-body flexibility and coordination required for complex, contact-rich tasks, and (ii) long-term stability to support extended operation without degradation in performance. 

Despite substantial progress in whole-body humanoid teleoperation [4, 5, 6, 7], existing systems continue to face a fundamental trade-off between motion agility and long-term stability. Recent real-time whole-body tracking approaches [8, 9] achieve highly flexible joint-level control, enabling expressive and coordinated motions. However, these methods typically operate in the robot’s local frame and neglect global pose feedback. As a result, accumulated global drift becomes unavoidable during extended operation—particularly for full-sized 

humanoids with higher centers of mass and more challenging control dynamics. Such drift introduces severe safety risks and frequently leads to task failure, as the robot gradually diverges from the operator’s intended global trajectory. While a recent closed-loop teleoperation system [10] partially addresses this issue, its control strategy does not support full whole-body tracking, limiting its applicability across diverse teleoperation scenarios. 

In this work, we introduce CLOT, a real-time humanoid teleoperation system that enables closed-loop global pose control and global motion tracking via high-frequency localization feedback. We employ an optical motion capture [11] system to simultaneously record human motion and the robot’s global pose with high precision. The captured human motions are retargeted online using the Pinocchio [12] inverse kinematics (IK) solver to produce robot target trajectories, after which only a general global body tracking controller needs to be trained. However, directly applying existing approaches [8, 13] to global pose correction often causes the policy to converge to suboptimal local minima. Specifically, conflicts arise between reward terms for global keypoint tracking and local joint-level objectives, while strongly positive tracking rewards encourage overly rapid convergence, resulting in aggressive and potentially unsafe behaviors. 

To address this issue, we propose a new data-driven randomization strategy termed “ **Observation Pre-shift** ”. In this approach, we periodically set the target pose in the observation to a random future timestamp, while keeping the tracking reward aligned with the current time. This effectively decouples the observation trajectory from the reward trajectory, facilitating the implicit learning of motion interpolation directly from data. 

Learning such implicit interpolation imposes two critical requirements. First, it demands a diverse dataset to ensure generalization. As most open-source datasets [14, 15] are primarily designed for animation, a significant portion of these motions exhibit certain discrepancies regarding the kinematic and dynamic properties of physical humanoids. To this end, we captured over 20 hours of human **_PND Adam Pro_** data using a strict protocol to preclude unstable behaviors (e.g., tiptoeing, exces- _1.67m Height_ sive CoM deviation). Furthermore, to enhance the _63Kg Weight_ policy network’s capability in capturing spatiotemporal _31 DoF_ information, we designed a _(excluding hands)_ Transformer-based [16] architecture. In addition, we incorporate an adversarial _6 DoF per Hand_ motion prior (AMP) reward [17] to suppress unnatural motion artifacts. Fig. 2: **Key parameters of** Finally, we deploy the **PNDbotics Adam Pro.** 

Finally, we deploy the **PNDbotics Adam Pro.** proposed teleoperation policy on Adam Pro 2, a **full-sized** humanoid robot with 31 

DoF. Experimental results demonstrate that our system maintains long-term stability during extended teleoperation and successfully performs a variety of loco-manipulation tasks. Furthermore, the robot exhibits diverse skills and exceptional disturbance rejection capabilities in real world. 

Our main contributions are summarized below: 

- Closed-Loop Global Control: We introduce CLOT, a real-time whole-body teleoperation system that achieves closed-loop global pose control through localization feedback. 

- Data-driven randomization strategy: We propose a novel training technique that randomly decouples the policy’s observation trajectory from the reward signal, enabling compliant implicit motion interpolation. 

- Human Motion Dataset: We captured diverse human motions totaling over 20 hours using a strict protocol. 

## II. RELATED WORK 

## _A. Learning-Based Humanoid Whole-Body Control_ 

Recent advances in sim-to-real reinforcement learning [18, 19] (RL) have significantly matured the development of wholebody controllers (WBC) for humanoid robots, enabling a diverse repertoire of agile skills ranging from robust locomotion [20, 21] to highly dynamic maneuvers such as parkour and dancing [22, 23]. By building upon the motion-tracking paradigm [17, 24], RL-based frameworks have emerged as a powerful alternative to exhaustive reward engineering. These methods utilize human motion references to synthesize naturalistic and dynamically feasible behaviors, often leveraging high-quality motion retargeting approaches [25, 26, 27, 28, 29] to bridge the morphological gap between humans and robots. 

Early learning-based trackers focus on robust single-task policy learning using specialized reference motions for gait or athletic behaviors. To improve motion expressiveness and physical feasibility within this paradigm, prior works have incorporated real-to-sim pipelines [30] and adaptive tracking curricula [31], enabling the learning of highly dynamic and balance-critical skills [32]. Advances in high-performance simulation [33] have further supported efficient and physically faithful sim-to-real transfer for humanoid whole-body tracking. Building on these foundations, recent studies have begun to explore scalable frameworks that learn diverse motions within a unified policy [34, 35, 36, 37, 38, 39], typically leveraging large-scale public motion datasets [14, 15, 29] to achieve broad motion coverage and tracking robustness. However, existing datasets are not explicitly curated for realworld humanoid teleoperation, whereas our in-house dataset is deliberately optimized for the dynamics of general-purpose humanoids and collected in a task-agnostic manner to better reflect real-world teleoperation conditions. 

## _B. Humanoid Teleoperation Systems_ 

Humanoid teleoperation is critical for collecting highquality real-world data necessary to advance embodied intelligence. Prior efforts attempted to address the high-dimensional control challenge by decoupling upper-body manipulation 

from lower-body locomotion [4, 24] via external inputs such as joysticks or exoskeletons [6, 40], which ensured stability but inherently restricted the robot’s dynamic potential and precluded naturally coordinated behaviors. Recent works have transitioned toward whole-body control strategies, leveraging goal-conditioned tracking optimization [5, 13, 7, 8, 9]. These paradigms achieve more fluid and diverse movements, demonstrating an improved capacity to mimic complex human motions on humanoid platforms. However, existing whole-body tracking systems primarily focus on local robot frames, leading to accumulated global pose drift during extended operation. Our work, CLOT, addresses this limitation by incorporating real-time global pose feedback into a whole-body tracking framework to ensure drift-free, long-horizon teleoperation. 

## III. METHOD 

## _A. Problem Formulation_ 

We formulate the humanoid whole-body motion tracking task as a goal-conditioned reinforcement learning (RL) problem. The task is modeled as a finite-horizon Markov Decision Process (MDP), defined by the tuple _M_ = _⟨S, A, P, R, γ⟩_ . 

At each time step _t_ , the agent receives an observation _ot ∈O_ , which consists of the proprioceptive state _st ∈S_ and a target motion goal _gt ∈G_ . The agent outputs an action _at ∈_ R<sup>23</sup> , representing proportional-derivative (PD) controller targets for all joints, according to a policy _πθ_ ( _at | st, gt_ ). The agent receives a scalar reward _rt_ = _R_ ( _st, at, gt_ ). The objective is to learn the optimal policy parameters _θ_ that maximize the expected discounted return E _t_ =0<sup>_γtrt_</sup> . We train the policy �� _T_ � 

using Proximal Policy Optimization (PPO) [19]. 

Based on this formulation, our teleoperation system is developed through a pipeline that includes human motion data collection, motion retargeting, RL–based policy training, and the construction of a closed-loop system. For hand and finger motions, we directly apply PD tracking on the retargeted joint references. An overview of the proposed teleoperation pipeline is shown in Fig. 3. 

## _B. Human Motion Data Collection_ 

We collect our own human motion dataset tailored specifically for humanoid robot teleoperation. We employ an OptiTrack optical motion capture system to record approximately 20 hours of high-fidelity full-body human motion data. During data collection, particular emphasis is placed on maintaining physically consistent contacts and motion patterns that are compatible with humanoid kinematic constraints. 

Our dataset covers a diverse set of motion categories, with the distribution summarized in Tab. I. Representative snapshots are shown in Fig. 4. The collected motions include both basic locomotion behaviors and high-dynamic whole-body movements, enabling the training of generalizable and robust teleoperation policies. 

- **Basic locomotion patterns:** walking, running, turning, and crouching; 

- **High-dynamic whole-body motions:** balancing maneuvers, martial arts techniques, and dance movements. 

TABLE I: DISTRIBUTION OF COLLECTED HUMAN MOTION DATA ACROSS DIFFERENT MOTION CATEGORIES 

|**Motion Category**|**(%)**|**Motion Category**|**(%)**|
|---|---|---|---|
|WALK|21.0|FREE|7.0|
|RUN|13.5|CYCLE|5.0|
|BALANCE|10.6|BOXING|4.1|
|HIGH<br>DYNAMIC|8.9|CROUCHING|3.3|
|UNLAB|9.4|PICK|2.3|
|SWING|9.4|DANCE|2.2|
|KUNGFU|1.7|LATERAL|1.7|


All motions are captured with explicit consideration of foot contact consistency and humanoid actuation limits, ensuring direct usability for whole-body control and reinforcement learning. 

## _C. Real-time Motion Retargeting_ 

To bridge the gap between human motion and humanoid kinematics, we implement a real-time motion retargeting algorithm. The primary objective is to minimize tracking errors between robot frames and corresponding human keypoints: 


where _v_ denotes the joint velocity vector and _ei_ represents the tracking error for each task. We leverage the Pinocchio [12] rigid-body dynamics engine to solve high-performance wholebody IK. To ensure safety, we apply a post-optimization clamping step to the computed velocities and the integrated joint positions. 

## _D. Basic Components for RL Training_ 

This section describes the basic components of our RL training framework, including observation design, reward formulation, domain randomization, and curriculum learning. 

_a) Asymmetric Actor–Critic Observations:_ Following previous works [30, 31], we adopt an asymmetric actor–critic observation design. At each timestep _t_ , the actor receives _s_<sup>actor</sup> _t_ = � _gt_ +1: _t_ +10 _, s_<sup>prop</sup> _t_ ; _s_<sup>hist</sup> _t−_ 10: _t−_ 1 �. The proprioceptive state _s_<sup>prop</sup> _t_ = � **_ω_**<sup>root</sup> _t ,_ **g** _t_<sup>proj</sup> _,_ **q** _t,_ **q** ˙ _t,_ **a** _t−_ 1� includes base angular velocity **_ω_**<sup>root</sup> _t ∈_ R<sup>3</sup> , projected gravity **g** _t_<sup>proj</sup> _∈_ R<sup>3</sup> , joint positions **q** _t ∈_ R<sup>23</sup> , joint velocities **q** ˙ _t ∈_ R<sup>23</sup> , and the previous action **a** _t−_ 1 _∈_ R<sup>23</sup> . A history buffer of length _H_ =10 stacks recent proprioceptive states, body-position features, and actions to mitigate partial observability. 

_b) Tracking-Oriented Reward Formulation:_ We design a tracking-oriented reward to encourage accurate teleoperation while penalizing unsafe behaviors and constraint violations. Detailed reward definitions and weighting schemes are provided in the supplementary material. 


Fig. 3: **Overview of the CLOT pipeline. Phase 1: Data Pipeline.** Human motion is captured using a hybrid optical–inertial motion capture system and retargeted to the humanoid kinematic motion via IK-based retargeting. **Phase 2: RL Training Framework.** We propose a random observation pre-shift strategy that decouples policy observations from reward-aligned references, enabling implicit learning of smooth motion interpolation and compliant global corrections. A Transformer policy models long-horizon dependencies, while an adversarial motion prior (AMP) enforces motion realism. Simulation training was performed in mjlab [33]. **Phase 3: Sim-to-Real Development.** Real-time retargeted operator motions provide reference commands, while high-frequency global pose estimates of the robot close the feedback loop, enabling stable and drift-free long-horizon teleoperation. 


Fig. 4: **Samples from our captured motion dataset.** The dataset includes diverse motions, from locomotion to highdynamic whole-body behaviors. 

with _σ_ denoting the error tolerance, which is adaptively optimized during training [31]. This formulation yields smooth gradients and promotes stable optimization throughout learning. 

_c) Domain Randomization:_ To reduce sim-real gap, we randomize physical parameters and observation conditions, including body mass and inertia, joint damping and friction, actuator strength, contact properties, and observation noise. The randomized parameters and their ranges are summarized in the supplementary material. 

_d) Curriculum Learning:_ The high-dimensional action space and complex physical constraints of humanoid robots make early-stage policy learning difficult, especially for fullscale humanoids. We therefore adopt a curriculum learn- 

ing [41] strategy. Detailed curriculum settings are provided in the supplementary material. 

_1) Adaptive Sampling:_ To improve the generalization capability, we adopt a difficulty-aware motion resampling strategy [37] that accounts for varying motion complexities in the dataset. More challenging motion instances are sampled more frequently, while a clipping mechanism is applied to ensure sufficient coverage of all motions. 

## _E. Key Design Components for RL Policy Training_ 

To Train control policy that simultaneously achieve generalization capability and high dynamic performance for full-sized humanoid robots, we implemented the following technical approaches: 

_1) Observation Pre-shift:_ To achieve robust real-world performance, the policy must retain sufficient exploration diversity during simulation training. Under global motion tracking objectives, prior work [13] typically encourages exploration by introducing random perturbations to the robot’s initial states, which often leads to overly aggressive recovery behaviors driven by rapid error minimization. 

We propose a **Randomized Observation Pre-shift** strategy to promote implicit smooth interpolation across reference trajectories. During training, with a randomly sampled probability within a predefined range, the reference observation window is randomly shifted forward by a temporal offset _δ ∈_ [0 _, T_ max <u>pre</u><sup>].Theresultingactorobservationisdefined</sup> as: 


Despite the look-ahead reference in the observation, the tracking reward is consistently evaluated against the original reference target at timestep _t_ , ensuring strict trajectory fidelity. 

By exposing the policy to temporally mismatched reference targets while enforcing current-step tracking objectives, this mechanism encourages the learning of a smooth transition manifold across time. Consequently, the policy exhibits improved stability and continuity when traversing gaps or discontinuities in reference motion sequences. This strategy is applied exclusively during training and is disabled during policy inference. 

_2) Transformer-Based Actor–Critic Network:_ To effectively capture spatiotemporal dependencies in the observations and enable stable implicit interpolation, we parameterize both the actor and critic networks using a Transformer architecture. Each observation component is first linearly embedded into a shared token space, and the resulting token sequence is processed by a Transformer encoder that performs global selfattention across historical states, current proprioceptive feedback, and tracking goals. This actor–critic formulation allows the policy to selectively attend to relevant temporal context and goal information conditioned on the robot’s instantaneous physical state, thereby improving stability and expressiveness in long-horizon control. 

_3) Motion Prior reward:_ When the robot deviates from the reference trajectory, handcrafted rewards often induce overaggressive corrections and excessive joint torques. 

To mitigate these issues, we incorporate the AMP framework to regularize policy behaviors toward human-like motion styles via adversarial learning. Specifically, we matches the distribution of generated motions _M_ amp _∼ Gθ_ ( _z_ ), with _z ∼N_ (0 _, I_ ), to the style distribution _P_ style of a target motion dataset _D_ motion. We adopt a composite reward formulation 


where _Dϕ_ is an adversarial discriminator trained with 


The reward term _r_ amp enforces stylistic consistency, while _r_ task maintains task-level tracking objectives. The two reward terms are balanced using weighting coefficients _λ_ style and _λ_ task, enabling stable and realistic whole-body motions. 

## _F. Closed-Loop Real-World Teleoperation System_ 

Our system establishes closed-loop humanoid teleoperation through real-time synchronization between the human operator and the robot in the global frame. As shown in Fig. 5, to enable precise and low-latency motion tracking in the real world, we deploy an online streaming pipeline based on a high-fidelity OptiTrack system[11], which captures full-body human motion at 120 Hz, along with finger poses recorded at 60 Hz using Hi5 gloves. The captured human motions are streamed online and retargeted to humanoid kinematics using the IK-based retargeting module described in Section III-C. 


Fig. 5: **Motion capture cameras and marker points.** Our motion capture system obtains the robot’s global pose by tracking the positions of the marker points. 

During deployment, the retargeted motion targets are fed our policy, which runs at 50 Hz on an Intel Core i7-14700KF CPU and outputs joint-level position commands. These commands are executed by a low-level PD controller operating at 400 Hz on the humanoid robot. In addition, first-person visual feedback from the robot’s head-mounted camera is streamed to a Meta Quest 3 headset, enabling immersive teleoperation and closed-loop human-in-the-loop control. 

## IV. EXPERIMENTS AND RESULTS 

We evaluate our method through extensive simulation and real-world experiments to answer three key questions: 

- **Q1:** Does the proposed teleoperation framework generalize across humanoid robots with diverse morphologies and dynamics? 

- **Q2:** How do individual components, including observation pre-shift and the Transformer-based policy, contribute to performance and stability? 

- **Q3:** Can the full system achieve long-horizon, drift-free, and stable loco-manipulation in real-world tasks? 

## _A. Simulation Experiment_ 

We address **Q1** and **Q2** through simulation experiment. **Experimental Setting.** All simulation experiments are conducted in the MuJoCo [42] environment using two humanoid platforms: Unitree G1 and PNDbotics Adam Pro. We evaluate our method on a held-out test set consisting of 30 minutes of additional motion capture data. The test motions cover a diverse set of common human behaviors, including walking, running, dancing, squatting, turning, and jumping. 

**Metrics.** We evaluate tracking accuracy and control smoothness using body-, root-, and joint-level error metrics. Specifically, _Emgbp_ and _Emlbp_ measure global and local body-level tracking errors, _Emgrp_ and _Emdp_ capture root- and joint-level position accuracy, while torque-based metrics reflect control effort and smoothness. _Mjt_ and _σmjt_ quantify the magnitude and variability of joint torques, reflecting control effort and smoothness. 

_1)_ **_Comparison with Prior Methods_** _:_ To address **Q1** , we compare our approach against TWIST2 [9], a representative baseline that provides a portable whole-body humanoid teleoperation system for long-horizon operation with full-body 


Fig. 6: **Real-world teleoperated loco-manipulation experiments on PNDbotics Adam Pro.** The sequential progression of each task is illustrated from (a) to (e). Throughout the execution, the humanoid robot maintains a constant spatial offset relative to the operator’s movements in the world frame. All robot motions across all tasks was governed by a single operator, demonstrating the system’s efficiency in whole-body teleoperation. 

pose tracking. TWIST2 is evaluated using its officially released pretrained weights. 

Compared with TWIST2, our method reduces all tracking error metrics by more than an order of magnitude on the Unitree G1, while achieving substantially smoother and more stable joint-level control, as summarized in Table II. By explicitly incorporating closed-loop global pose feedback, our approach attains particularly strong tracking accuracy. 

_2)_ **_Ablation Study_** _:_ To address **Q2** , we conduct ablation studies on the Transformer architecture, the adversarial motion prior reward, and the observation pre-shift mechanism. 

Tab. II reports the ablation results on PNDbotics Adam Pro. When only the Transformer network is enabled, the policy exhibits substantially larger tracking errors and higher torque statistics compared to the full system. 

These results highlight the importance of incorporating both the motion prior reward and the observation pre-shift mechanism. The observation pre-shift enables the policy to learn implicit future motion goal differences, which is crucial for avoiding over-aggressive and unstable corrections under 

## large trajectory deviations. 

To further isolate the effect of the observation pre-shift, we simulate abrupt reference motion changes and evaluate the recovery behaviors. As shown in Table III and Fig. 7, policies trained with observation pre-shift consistently achieve lower fluctuation and improved smoothness for both absolute mean joint torque (AMJT) and absolute mean DOF velocity (AMDV). 

These results indicate that observation pre-shift leads to smoother and more stable trajectory error correction under large reference perturbations. 

Finally, we investigate the interaction between the observation pre-shift mechanism and policy architecture. Figure 8 compares the performance of MLP-based and Transformerbased policies under a pre-shift of 2.0 s. While the Transformer-based policy successfully captures long-horizon spatiotemporal dependencies and achieves stable tracking, the MLP-based policy fails to converge and results in a fall. This demonstrates that effectively leveraging observation pre-shift requires sufficient temporal modeling capacity, making the 


Fig. 7: **Ablation study on observation pre-shift mechanism.** (a,b) Quantitative comparison of AMJT and AMDV during trajectory error recovery. Policies trained with observation preshift exhibit reduced torque and joint velocity peaks. (c,d) Corresponding recovery motion sequences. Observation preshift enables stable trajectory error correction. 


Fig. 8: **Network Architecture ablation study.** The proposed randomization strategy requires capturing long-horizon spatiotemporal dependencies. (a) Training Curve indicate that the MLP fails to converge, whereas the Transformer policy achieves stable learning. (b-d) Trajectory visualization with a pre-shift of 2.0s. The Transformer handles the large offset with stable tracking, whereas the MLP fails and results in a fall. 

Transformer architecture essential. 

## _B. Real World Teleoperation_ 

To answer **Q3** , we evaluate our system on PNDbotics Adam Pro[43], a full-sized humanoid robot, equipped with dual 6- DoF dexterous hands (see Fig. 2). We design three real-world teleoperation experiments: _(i)_ long-horizon loco-manipulation teleoperation, _(ii)_ extended-duration continuous teleoperation, and _(iii)_ robustness evaluation under strong external disturbances. 

_1)_ **_Long-Horizon Loco-Manipulation Performance_** _:_ To evaluate the stability and data collection efficiency of CLOT in long-horizon loco-manipulation tasks, we showcase three representative experiments: 

- **Task 1 (T1): Desktop Manipulation.** The robot performs tabletop pick-and-place with multiple objects, evaluating operational flexibility and control precision against an MPC-based teleoperation baseline. 

- **Task 2 (T2): Table-to-Shelf Bin Transfer.** The robot sequentially picks three objects from a table, places them into a top-shelf bin, and then moves the bin to a lower shelf. This long-horizon task challenges whole-body coordination, stable walking, and precise shelf placement. 

- **Task 3 (T3): Ground-to-Table Bucket Placement.** The robot retrieves a bucket from the floor and places it upright on a table, requiring low-height grasping, reorientation, and whole-body balance under large CoM shifts. 

As illustrated in Fig. 6, the robot executes teleoperated locomanipulation with fluent and coordinated whole-body motion. We report the success rate (SR) and average task success time (ATST), and compare our method with an MPC-based baseline on the desktop manipulation task in Table IV. 

The recorded data highlights our method completes locomanipulation tasks with high speed and accuracy. Furthermore, it outperforms the MPC approach even in desktop manipulation, thanks to its expanded workspace. 

_2)_ **_Long-horizon Teleoperation Stability_** _:_ To evaluate longhorizon tracking stability, we conduct a 30-minute uninterrupted teleoperated loco-manipulation experiment. Tracking errors are recorded at 1 Hz throughout the session. 

All tracking error metrics, including _Emgbp_ , _Emgrp_ , and _Emdp_ , remain consistently low and stable over the entire duration. The consistently low and bounded error distributions over an extended duration demonstrate the effectiveness of the 

TABLE II: SIMULATION PERFORMANCE COMPARISON AND ABLATION RESULTS ACROSS ROBOT PLATFORMS. 

|**Method**|_Emgbp ↓_|_Emlbp ↓_|_Emgrp ↓_|_Emdp ↓_|_Mjt ↓_|_σmjt ↓_|
|---|---|---|---|---|---|---|
|**Unitree G1**|||||||
|TWIST2 [9]<br>**Ours**|5.094<br>**0.056**|0.340<br>**0.061**|5.164<br>**0.054**|0.364<br>**0.158**|**6.270**<br>6.604|11.203<br>**1.806**|
|**Adam Pro**|||||||
|Ours (Transf.-only)|0.410|0.170|0.405|0.291|12.896|18.214|
|**Ours**|**0.116**|**0.107**|**0.122**|**0.136**|**12.404**|**8.906**|


Fig. 9: **Real-world robustness evaluation under strong external disturbances.** During teleoperation, the full-sized humanoid robot is subjected to a strong external kick. Despite the large impulsive disturbance, the robot successfully recovers its balance and resumes stable motion, demonstrating the robustness of our teleoperation framework. 

TABLE III: EFFECT OF OBSERVATION PRE-SHIFT ON LARGE-MAGNITUDU TRAJECTORY ERROR CORRECTION 

|**Metric**||**Method**|**Std**_↓_|**Smoothness**_↓_|
|---|---|---|---|---|
|**Abs. Mean **|**Joint torque**|No Pre-shift<br>With Pre-shift|1.107<br>**0.990**|7.015<br>**5.485**|
|**Abs. Mean **|**DOF Vel.**|No Pre-shift<br>With Pre-shift|5.059<br>**3.468**|28.242<br>**20.442**|


TABLE IV: Performance comparison across real-world teleoperated manipulation tasks. 

|**Category**|**Task**|**Method**|**SR**_↑_|**ATST (s)**_↓_|
|---|---|---|---|---|
|Desktop-Manip.|T1<br>T1|MPC-based<br>**Ours**|20/30<br>**27/30**|**22**<br>25|
|Loco-Manip.|T2<br>T3|**Ours**<br>**Ours**|**24/30**<br>**26/30**|**82**<br>**42**|


closed-loop global pose feedback in suppressing drift accumulation, thereby enabling reliable long-horizon teleoperation. 

_3)_ **_Robustness Performance under Strong External Disturbances_** _:_ To assess robustness under real-world perturbations, we apply strong external kicks to the humanoid robot during teleoperation. As shown in Fig. 9, high-impulse posterior kicks are delivered to the robot. 

Despite sudden perturbations, the robot maintains balance and smoothly resumes its motion trajectory. As shown in Fig. 11, joint torques and velocities remain within physical limits during impact and recovery, demonstrating robust teleoperation under strong external disturbances in real-world deployment. 

## V. CONCLUSION 

In this work, we presented CLOT, a closed-loop whole-body teleoperation system validated on a full-sized humanoid robot. We introduce a data-driven randomization strategy to improve stability and smoothness during global error correction, and 


Fig. 10: **Error distributions during long-horizon teleoperated loco-manipulation.** Violin plots of the _Emgbp_ , _Emgrp_ , and _Emdp_ over a 30-minute teleoperation session. The distributions remain stable throughout the long-horizon execution, indicating robust and consistent tracking performance. 


Fig. 11: **Joint-level torque and velocity limits during realworld teleoperation under strong external disturbances.** Even under a severe external kick, all joints operate within their physical limits. 

collect a 20-hour human motion dataset tailored for fullsized humanoid teleoperation. A Transformer-based policy is designed to effectively exploit spatiotemporal information. Together, these components enable robust, high-fidelity, and driftfree teleoperation in real-world deployment. Future work will explore lightweight, cost-effective global localization [44, 45] 

systems and VR-based human motion tracking, to improve system accessibility. 

## VI. ACKNOWLEDGMENTS 

We would like to sincerely thank PNDbotics for providing the robotic platform and comprehensive support related to the robot hardware. We also thank Baidu for providing the GPU resources. 

## REFERENCES 

- [1] Ri-Zhao Qiu, Shiqi Yang, Xuxin Cheng, Chaitanya Chawla, Jialong Li, Tairan He, Ge Yan, David J. Yoon, Ryan Hoque, Lars Paulsen, Ge Yang, Jian Zhang, Sha Yi, Guanya Shi, and Xiaolong Wang. Humanoid policy human policy, 2025. 

- [2] Michael A Goodrich, Jacob W Crandall, and Emilia Barakova. Teleoperation and beyond for assistive humanoid robots. _Reviews of Human factors and ergonomics_ , 9(1):175–226, 2013. 

- [3] Zhaoyuan Gu, Junheng Li, Wenlan Shen, Wenhao Yu, Zhaoming Xie, Stephen McCrory, Xianyi Cheng, Abdulaziz Shamsah, Robert Griffin, C Karen Liu, et al. Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning. _arXiv preprint arXiv:2501.02116_ , 2025. 

- [4] Chenhao Lu, Xuxin Cheng, Jialong Li, Shiqi Yang, Mazeyu Ji, Chengjing Yuan, Ge Yang, Sha Yi, and Xiaolong Wang. Mobile-television: Predictive motion priors for humanoid whole-body control. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5364–5371. IEEE, 2025. 

- [5] Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. Humanplus: Humanoid shadowing and imitation from humans. _arXiv preprint arXiv:2406.10454_ , 2024. 

- [6] Qingwei Ben, Feiyu Jia, Jia Zeng, Junting Dong, Dahua Lin, and Jiangmiao Pang. Homie: Humanoid locomanipulation with isomorphic exoskeleton cockpit. _arXiv preprint arXiv:2502.13013_ , 2025. 

- [7] Jialong Li, Xuxin Cheng, Tianshu Huang, Shiqi Yang, Ri-Zhao Qiu, and Xiaolong Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid wholebody control. _arXiv preprint arXiv:2505.03738_ , 2025. 

- [8] Yanjie Ze, Zixuan Chen, Joao Pedro Ara´ujo, Zi-ang Cao, Xue Bin Peng, Jiajun Wu, and C Karen Liu. Twist: Teleoperated whole-body imitation system. _arXiv preprint arXiv:2505.02833_ , 2025. 

- [9] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C Karen Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025. 

- [10] Yixuan Li, Yutang Lin, Jieming Cui, Tengyu Liu, Wei Liang, Yixin Zhu, and Siyuan Huang. Clone: Closed-loop whole-body humanoid teleoperation for long-horizon tasks. _arXiv preprint arXiv:2506.08931_ , 2025. 

- [11] Patric Eichelberger, Matteo Ferraro, Ursina Minder, Trevor Denton, Angela Blasimann, Fabian Krause, and Heiner Baur. Analysis of accuracy in optical motion capture–a protocol for laboratory setup evaluation. _Journal of biomechanics_ , 49(10):2085–2088, 2016. 

- [12] Justin Carpentier, Guilhem Saurel, Gabriele Buondonno, Joseph Mirabel, Florent Lamiraux, Olivier Stasse, and Nicolas Mansard. The pinocchio c++ library – a fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives. In _IEEE International Symposium on System Integrations (SII)_ , 2019. 

- [13] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 

- [14] Naureen Mahmood, Nima Ghorbani, Nikolaus F. Troje, Gerard Pons-Moll, and Michael J. Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , October 2019. 

- [15] Jiaman Li, Jiajun Wu, and C. Karen Liu. Object motion guided human motion synthesis. _ACM Transactions on Graphics (TOG)_ , 42:1 – 11, 2023. 

- [16] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 

- [17] Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 

- [18] Younggyo Seo, Carmelo Sferrazza, Juyue Chen, Guanya Shi, Rocky Duan, and Pieter Abbeel. Learning sim-toreal humanoid locomotion in 15 minutes, 2025. 

- [19] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [20] Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 9(89):eadi9579, 2024. doi: 10.1126/scirobotics. adi9579. 

- [21] Yufei Xue, Wentao Dong, Minghuan Liu, Weinan Zhang, and Jiangmiao Pang. A unified and general humanoid whole-body controller for versatile locomotion. 2025. 

- [22] Ziwen Zhuang, Shenzhe Yao, and Hang Zhao. Humanoid parkour learning. _ArXiv_ , abs/2406.10759, 2024. 

- [23] Mazeyu Ji, Xuanbin Peng, Fangchen Liu, Jialong Li, Ge Yang, Xuxin Cheng, and Xiaolong Wang. Exbody2: Advanced expressive humanoid whole-body control. _ArXiv_ , abs/2412.13196, 2024. 

- [24] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. 

_ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [25] Zhengyi Luo, Jinkun Cao, Kris Kitani, Weipeng Xu, et al. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10895–10904, 2023. 

- [26] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C. Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [27] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interactionpreserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

- [28] Chaoyi Pan, Changhao Wang, Haozhi Qi, Zixi Liu, Homanga Bharadhwaj, Akash Sharma, Tingfan Wu, Guanya Shi, Jitendra Malik, and Francois Hogan. Spider: Scalable physics-informed dexterous retargeting, 2025. 

- [29] Kyungmin Lee, Sibeen Kim, Minho Park, Hyunseung Kim, Dongyoon Hwang, Hojoon Lee, and Jaegul Choo. Phuma: Physically-grounded humanoid locomotion dataset, 2025. 

- [30] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. _arXiv preprint arXiv:2502.01143_ , 2025. 

- [31] Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. Kungfubot: Physics-based humanoid wholebody control for learning highly-dynamic skills. _arXiv preprint arXiv:2506.12851_ , 2025. 

- [32] Tong Zhang, Boyuan Zheng, Ruiqian Nai, Yingdong Hu, Yen-Jen Wang, Geng Chen, Fanqi Lin, Jiongye Li, Chuye Hong, Koushil Sreenath, and Yang Gao. Hub: Learning extreme humanoid balance. _ArXiv_ , abs/2505.07294, 2025. 

- [33] Kevin Zakka, Qiayuan Liao, Brent Yi, Louis Le Lay, Koushil Sreenath, and Pieter Abbeel. mjlab: A lightweight framework for gpu-accelerated robot learning, 2026. 

- [34] Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. Gmt: General motion tracking for humanoid whole-body control. _ArXiv_ , abs/2506.14770, 2025. 

      - Maoqi Liu, Jiangran Lyu, Huaping Liu, He Wang, and Li Yi. Track any motions under any disturbances, 2025. 

   - [37] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

   - [38] Yitang Li, Zhengyi Luo, Tonghe Zhang, Cunxi Dai, Anssi Kanervisto, Andrea Tirinzoni, Haoyang Weng, Kris Kitani, Mateusz Guzek, Ahmed Touati, Alessandro Lazaric, Matteo Pirotta, and Guanya Shi. Bfm-zero: A promptable behavioral foundation model for humanoid control using unsupervised reinforcement learning, 2025. 

   - [39] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Casta˜neda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, Xingye Da, Runyu Ding, Cyrus Hogg, Lina Song, Edy Lim, Eugene Jeong, Tairan He, Haoru Xue, Wenli Xiao, Zi Wang, Simon Yuen, Jan Kautz, Yan Chang, Umar Iqbal, Linxi ”Jim” Fan, and Yuke Zhu. Sonic: Supersizing motion tracking for natural humanoid whole-body control, 2025. 

   - [40] Shiqi Yang, Minghuan Liu, Yuzhe Qin, Runyu Ding, Jialong Li, Xuxin Cheng, Ruihan Yang, Sha Yi, and Xiaolong Wang. Ace: A cross-platform visual-exoskeletons system for low-cost dexterous teleoperation. _ArXiv_ , abs/2408.11805, 2024. 

   - [41] Yoshua Bengio, J´erˆome Louradour, Ronan Collobert, and Jason Weston. Curriculum learning. In _Proceedings of the 26th annual international conference on machine learning_ , pages 41–48, 2009. 

   - [42] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ international conference on intelligent robots and systems_ , pages 5026–5033. IEEE, 2012. 

   - [43] PNDbotics. Pndbotics adam pro. https://wiki.pndbotics. com/robot/humanoid <u>robot/,</u> 2026. Accessed: January 31, 2026. 

   - [44] Yanbo Wang, Zipeng Fang, Lei Zhao, and Weidong Chen. Learning to tune like an expert: Interpretable and scene-aware navigation via mllm reasoning and cvae-based adaptation. _arXiv preprint arXiv:2507.11001_ , 2025. 

   - [45] Jinyu Li, Xiaokun Pan, Gan Huang, Ziyang Zhang, Nan Wang, Hujun Bao, and Guofeng Zhang. Rd-vio: Robust visual-inertial odometry for mobile augmented reality in dynamic environments. _IEEE transactions on visualization and computer graphics_ , 30(10):6941–6955, 2024. 

- [35] Kangning Yin, Weishuai Zeng, Ke Fan, Zirui Wang, Qiang Zhang, Zheng Tian, Jingbo Wang, Jiangmiao Pang, and Weinan Zhang. Unitracker: Learning universal whole-body motion tracker for humanoid robots. _ArXiv_ , abs/2507.07356, 2025. 

- [36] Zhikai Zhang, Jun Guo, Chao Chen, Jilong Wang, Chenghuai Lin, Yunrui Lian, Han Xue, Zhenrong Wang, 

## APPENDIX A RL TRAINING DETAILS 

## _A. Reward Terms and Weights in RL Training_ 

The reward terms are grouped into positive rewards and penalty terms, as summarized in Table V. Positive rewards focus on tracking performance at multiple levels, including extended body pose, joint kinematics, keypoint alignment, and foot motion, while also encouraging stable contacts and sustained locomotion through air-time and alive bonuses. Penalty terms are introduced to regularize control behaviors and enforce physical constraints, discouraging excessive torques, abrupt actions, contact instabilities, joint limit violations, and unsafe collisions. 

TABLE V: REWARD TERMS AND THEIR WEIGHTS, GROUPED INTO POSITIVE REWARDS ADN PENALTIES 

|**Reward term**|**Weight**|
|---|---|
|**Positive rewards**||
|Contact Consistency Tracking|0.5|
|Joint Limit Satisfaction Reward|1.0|
|Extended Body Position Tracking|1.2|
|VR Keypoint (3-Point) Tracking|1.6|
|Feet Position Tracking|1.5|
|Extended Body Orientation Tracking|1.5|
|Extended Body Angular Velocity Tracking|0.6|
|Extended Body Linear Velocity Tracking|0.6|
|Joint Position Tracking|1.0|
|Joint Velocity Tracking|1.0|
|Feet Air-Time Reward|160.0|
|Alive Bonus|0.2|
|**Penalty rewards**||
|Feet Height Deviation Penalty|-20.0|
|Torque Limit Violation Penalty|-1.0e-4|
|Action Rate Penalty|-0.1|
|Action Smoothness Penalty|-0.2|
|Feet Contact Force Penalty|-5.0e-4|
|Stumbling Penalty|-20.0|
|Feet Slippage Penalty|-2.0|
|Joint Position Limit Penalty|-10.0|
|Joint Velocity Limit Penalty|-10.0|
|Torque Limit Penalty|-10.0|
|Collision Penalty|-30.0|
|Early Termination Penalty|-200.0|


## _B. Observation Setup_ 

To enhance the performance of our control policy, we provide abundant perceptual information. The complete specification of the observation components, which is identical for both the Unitree G1 and the PNDbotics Adam Pro, is summarized in Table VI. 

## _C. Domain Randomization Paramters in RL Training_ 

To improve robustness and reduce the sim-to-real gap, we employ domain randomization during training. The detailed domain randomization parameters of PNDbotics Adam Pro and their corresponding ranges are summarized in Table VII. All parameters are independently sampled from uniform distributions within the specified ranges. 

## TABLE VI: OBSERVATION DETAILS 

|**Observation term**|**Dimension**|
|---|---|
|last action|1*23|
|base ang|1*3|
|dof pos|1*23|
|dof vel|1*23|
|future dif pos|10*29*3|
|future ref pos|10*29*3|
|history base ang|10*1*3|
|history projected gravity|10*1*3|
|history dof pos|10*1*23|
|history dof vel|10*1*23|
|history dif pos|10*29*3|
|history body pos|10*29*3|
|history actions|10*1*23|


## TABLE VII: DOMAIN RANDOMIZATION PARAMETERS 

|**Domain Rand Params**|**Range**|
|---|---|
|Base COM [m]|[_−_0_._08_,_0_._08]|
|Link COM [m]|[_−_0_._02_,_0_._02]|
|Link Mass Scale|[0_._90_,_1_._10]|
|Link Inertia Scale|[0_._85_,_1_._15]|
|PD Gain Scale (_Kp_, _Kd_)|[0_._90_,_1_._10]|
|Friction Scale|[0_._80_,_1_._50]|
|External Push Velocity XY [m/s]|[_−_0_._20_,_0_._20]|
|External Push Interval [s]|[3_._00_,_6_._00]|
|RFI Limit Scale|[0_._50_,_1_._50]|
|Control Delay [steps]|[0_._00_,_2_._00]|


## _D. Curriculum Learning Paramters in RL Training_ 

In the early training stage, we reduce penalty, noise and randomization, allowing the policy to focus on learning motion tracking behaviors. As tracking performance improves, these parameters are progressively increased, enabling the policy to adapt to more challenging and realistic conditions. The parameter adaptation rules are defined as follows: 


where _θi_<sup>(</sup><sup>_t_)</sup> denotes the Value of _i_ -th parameter at iteration _t_ , _σi >_ 0 represents a parameter-specific adaptation rate, _η_<sup>(</sup><sup>_t_)</sup> denotes the motion completion ratio at iteration _t_ , and _η_ 0 is the performance threshold for triggering updates. Corresponding parameters are summarized in Table VIII. 

TABLE VIII: CURRICULUM LEARNING PARAMETERS 

|**Curriculum Learning Parameters**|**Sigma**|**Range**|
|---|---|---|
|Reward Penalty|3e-6|[0_._05_,_1_._0]<br>|
|Reward Limits|2.5e-7|[0_._9_,_0_._95]|
|Push Robots interval|1.5e-5|[1_,_50]<br>|
|Observation Pre-shift|5e-6|[1_,_2]<br>|
|Termination Distance|3e-6|[2_._5_,_3_._0]|
|Termination Scale|1e-5|[0_._8_,_4_._0]|
|Noise|3e-6|[0_._05_,_1_._0]|


## _E. Detailed Neural Network Architecture_ 

To enhance the generalization of our control policy, we change our backbone network from MLP to Transformer. Meanwhile, the discriminator network still use MLP. The specific parameters are shown in Table IX. 

TABLE IX: Neural Network Architecture Parameters 

|**Component**|**Actor & Critic**|**Discriminator**|
|---|---|---|
|Architecture|Transformer|MLP|
|Model dimension|192|–|
|Number of heads|4|–|
|Feedforward dimension|768|–|
|Number of blocks|3|–|
|Number of layers|–|4|
|Hidden units|–|1024|
|Activation|ReLU|ReLU|
|Layer normalization|Yes|Yes|


## _F. Proportional–Derivative Controller Paramters_ 

During training and deployment, the RL policy outputs target joint positions, which are tracked by a joint-space proportional–derivative (PD) controller to generate torque commands: 


where **q**<sup>_⋆_</sup> and **q** ˙<sup>_⋆_</sup> denote the target joint positions and velocities predicted by the policy. 

The PD gains are fixed across all experiments and are selected based on joint functionality. The complete set of PD controller parameters of PNDbotics Adam Pro is reported in Table X. 

TABLE X: PD CONTROLLER PARAMETERS 

|**Joint DoF**|**Stiffness** _Kp_|**Damping** _Kd_|
|---|---|---|
|Hip Pitch|305.0|5.0|
|Hip Roll|255.0|3.5|
|Hip Yaw|255.0|3.5|
|Knee Pitch|305.0|5.0|
|Ankle Pitch|50.0|0.8|
|Ankle Roll|30.0|0.35|
|Waist Roll|255.0|3.5|
|Waist Pitch|305.0|5.0|
|Waist Yaw|255.0|3.5|
|Shoulder Pitch|40.0|1.0|
|Shoulder Roll|40.0|1.0|
|Shoulder Yaw|40.0|1.0|
|Elbow|40.0|1.0|


## _B. Evaluation Metrics_ 

We evaluate both tracking accuracy and control smoothness using body-, root-, and joint-level metrics. Let _t_ = 1 _, . . . , T_ denote timesteps. We use **p** _i_ ( _t_ ) _∈_ R<sup>3</sup> to denote the Cartesian position of the _i_ -th tracked body point from the robot, and **p**<sup>_⋆_</sup> _i_<sup>(</sup><sup>_t_)thecorrespondingreferencetarget.Let</sup><sup>**r**(</sup><sup>_t_)</sup><sup>_∈_R3and</sup> **r**<sup>_⋆_</sup> ( _t_ ) be the root (base) positions, **q** ( _t_ ) _∈_ R<sup>_n_</sup> and **q**<sup>_⋆_</sup> ( _t_ ) be the joint positions, and **_τ_** ( _t_ ) _∈_ R<sup>_n_</sup> be the joint torques. 

_a) Body-level tracking errors:_ We report global and local body-position errors. The global mean body-position error is 


where _Nb_ is the number of tracked body points. We also compute the local mean body-position error: 


where **p** ˜ _i_ ( _t_ ) = **R** ( _t_ )<sup>_⊤_�</sup> **p** _i_ ( _t_ ) _−_ **r** ( _t_ )� and **p** ˜<sup>_⋆_</sup> _i_<sup>(</sup><sup>_t_)</sup> = **R**<sup>_⋆_</sup> ( _t_ )<sup>_⊤_�</sup> **p**<sup>_⋆_</sup> _i_<sup>(</sup><sup>_t_)</sup><sup>_−_</sup><sup>**r**</sup><sup>_⋆_(</sup><sup>_t_)</sup> � are expressed in the root frame, with **R** ( _t_ ) _∈ SO_ (3) the root orientation. 

_b) Root- and joint-level accuracy:_ Root-level position accuracy is measured by 


Joint-level (DOF) position accuracy is computed as 


where _na_ is the number of actuated joints. 

_c) Torque-based control metrics:_ To quantify control effort, we compute the mean joint-torque magnitude: 


To measure smoothness/stability, we report the temporal variability of the per-timestep mean torque magnitude: 


A smaller _Mjt_ indicates lower control effort, while a smaller _σmjt_ implies reduced torque fluctuations and smoother control. 

## APPENDIX B EXPERIMENTAL DETAILS 

## _A. Experiment Setup_ 

**Compute platform:** The Final policy training was performed in the MJLab simulation using eight NVIDIA RTX 4090 GPUs, with a total training time of approximately one week. 

