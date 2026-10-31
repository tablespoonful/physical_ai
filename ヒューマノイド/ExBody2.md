---
title: "ExBody2: Advanced Expressive Humanoid Whole-Body Control"
date: "2024-12-17"
authors: "Mazeyu Ji; Xuanbin Peng; Fangchen Liu; Jialong Li; Ge Yang; Xuxin Cheng"
url: https://arxiv.org/abs/2412.13196
pdf: https://arxiv.org/pdf/2412.13196
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2412.13196)** / [論文ページ](https://arxiv.org/abs/2412.13196)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# ExBody **2** : Advanced Expressive Humanoid Whole-Body Control 

Mazeyu Ji<sup>_∗,_1</sup> Xuanbin Peng<sup>_∗,_1</sup> Fangchen Liu<sup>2</sup> Jialong Li<sup>1</sup> Ge Yang<sup>3</sup> Xuxin Cheng<sup>_†,_1</sup> Xiaolong Wang<sup>_†,_1</sup> 1UC San Diego 2UC Berkeley 3MIT _∗_ Equal contribution _†_ Equal advising https://exbody2.github.io (a) (b) (c) (d) (e) (f) 


**Fig. 1:** Humanoid robot executing various expressive whole-body motions in the real world. The robot can (a) walk with a large stride from static standing, (b) dance along a long horizon (43 seconds) choreography, (c) dynamic sidestep with fluid weight shifts, (d) punch with different height configurations, (e) express various upper-body movements while maintaining balance, (f) powerful rightward body hook with dynamic shifts. 

**_Abstract_ —This paper tackles the challenge of enabling realworld humanoid robots to perform expressive and dynamic whole-body motions while maintaining overall stability and robustness. We propose Advanced Expressive Whole-Body Control (Exbody2), a method for producing whole-body tracking controllers that are trained on both human motion capture and simulated data and then transferred to the real world. We** 

**introduce a technique for decoupling the velocity tracking of the entire body from tracking body landmarks. We use a teacher policy to produce intermediate data that better conforms to the robot’s kinematics and to automatically filter away infeasible whole-body motions. This two-step approach enabled us to produce a student policy that can be deployed on the robot that can walk, crouch, and dance. We also provide insight into** 

**the trade-off between versatility and the tracking performance on specific motions. We observed significant improvement of tracking performance after fine-tuning on a small amount of data, at the expense of the others.** 

## I. INTRODUCTION 

The premise of humanoid robots is to enable human-like motions while occupying human living spaces. However, a humanoid robot with human-level _expressiveness_ and _versatility_ that is also robust in maintaining stability and control remains elusive. Inherent to this problem is the dynamic and kinematic gap between robots and biological body structures and the need for the controller to make a trade-off between expressiveness and stability. How to let robots imitate human whole-body motion across this gap and achieve both is a key challenge. 

This paper introduces Advanced Expressive Whole-Body Control (Exbody2), a framework that enables humanoid robots to perform expressive, human-like full-body motions with grace. At its core, Exbody2 features both a generalist and a specialist policy. The generalist policy, trained on diverse motion datasets, **outperforms previous approaches** by achieving high adaptability across a wide range of motions with a single policy. Building on this, we further fine-tune the policy for specific motion groups, producing specialist policies that ensure **even higher fidelity in targeted behaviors** . Our framework also incorporates a decoupled motion-velocity control strategy, allowing for both precise key body tracking and stable motion generation. These innovations set Exbody2 apart from previous methods and push the boundaries of humanoid motion control. Overall, there are three key innovations that distinguish Exbody2 from previous approaches: 

(i) _Generalist policy with automated data curation_ . Human motion datasets often contain movements beyond a robot’s physical limits, making tracking difficult and reducing performance. Some methods refine datasets, like ExBody [3] filtering motions via language labels, though ambiguous terms (e.g., “dance”) may still include infeasible actions. Others [18, 17] use SMPL avatars to simulate motions, but these can exceed real robot capabilities, impacting training. We identify the trade-off between dataset feasibility and diversity and develop an automated curation method that removes unsuitable lowerbody motions while preserving diversity, enabling the policy to learn broad, expressive behaviors. Experiments validate that our method optimally balances feasibility and diversity, leading to improved stability and accuracy across diverse motion tasks. 

(ii) _Specialist policy with finetuning for targeted motions_ . While the generalist policy enables broad motion coverage, finetuning enhances precision for specific motion groups. Motions with similar patterns are easier to learn under a shared policy, as they require consistent control strategies and constraints. Instead of training from scratch, we refine the generalist policy, leveraging its learned priors for efficient adaptation. This allows the policy to better capture fine-grained motion details and improve tracking accuracy for specialized 

tasks. Additionally, motion labels or an action recognition model can classify input motions, enabling dynamic selection of the most suitable specialist policy. 

(iii) _Decoupled motion-velocity control strategy_ . Previous whole-body tracking approaches, such as H2O [18] and OmniH2O [17], rely on global tracking of keypoint positions. This often leads to tracking failures in immediate next steps when robots struggle to align with current global keypoints, limiting their applications to highly stationary scenarios. In contrast, Exbody2 converts keypoints into the local frame and decouples keypoint tracking from velocity control. Velocitybased tracking guides movement, while key body tracking focuses on motion imitation, emphasizing expressive motion reproduction. To improve tracking robustness, Exbody2 adopts a teacher-student framework, where a teacher policy is first trained using PPO [51] with privileged information, including real root velocity, accurate body link positions, and physical properties (e.g., friction). The student policy is then trained via DAgger [50]-style distillation, using historical observations to infer privileged information, enabling real-world deployment without direct access to such data. 

We evaluate our approach on the Unitree G1 against four state-of-the-art baselines, demonstrating higher fidelity across both simulation and real-world tests. In particular, the automated data curation yields a robust generalist policy that outperforms all previous methods as a single policy capable of handling diverse motions. Fine-tuning for specific tasks (e.g., dancing) further enhances motion quality and expressiveness. Overall, our results highlight ExBody2’s potential for bridging the gap between human-level expressiveness and reliable whole-body control in humanoid robots. 

## II. RELATED WORK 

**Humanoid Whole-Body Control.** Whole-body control for humanoid robots remains a complex and challenging problem due to the system’s high non-linearity and degrees of freedom. Traditional approaches predominantly rely on dynamics modeling and control [40, 62, 22, 41, 8, 25, 61, 27, 20, 6, 7, 9, 42, 49], which often require accurate system identification and physical modeling, and intensive online computation for real-time control to handle different external perturbations for locomotion stability. Recent advances in reinforcement learning (RL) and sim-to-real transfer have demonstrated promising results in enabling complex whole-body skills for humanoid robots [32, 33, 53, 10, 34, 35, 48, 23, 24, 47, 55, 52]. These approaches typically rely on training RL policies in simulation using task-specific rewards and environment randomization before transferring them to the real world. Notably, recent works such as [3, 18, 13] have advanced real-world humanoid whole-body control for expressive motion by incorporating human motion datasets [38] to guide RL training, with realworld applications such as motion imitation. However, these approaches still exhibit limitations in expressiveness and maneuverability, highlighting the untapped potential of humanoid robots. In contrast, our method enables the learning of more 

expressive and dynamic motions, enhancing the robot’s ability to perform complex whole-body movements. 

**Robot Motion Imitation.** Robot motion imitation can be broadly categorized into manipulation and locomotion areas. For manipulation tasks, robots are often wheeled or tabletop, prioritizing precise control over balancing and ground contact, making humanoid morphology unnecessary. Such robots can imitate the motion through direct teleoperation [64, 14, 46], portable devices [59, 2, 5, 15] and learn from human videos with hand tracking or motion retargeting [58, 54, 31, 26]. In contrast, motion imitation for locomotion primarily aims to learn lifelike, natural behaviors from human or animal motion capture data. It requires precise control over contact dynamics, balance, and coordination across multiple degrees of freedom to achieve stable and realistic movement. While prior methods have enabled physics-based character motion imitation in simulation [44, 45, 56, 16, 37, 36, 63, 60, 57], transferring diverse motions to real robots [3, 17, 13, 19, 43, 12, 11] remains a significant challenge due to the hardware constraints. Previous methods [3, 17, 13, 19] typically rely on manually filtering feasible motion data with human effort or handcrafted heuristics. However, manually filtered datasets may still contain infeasible motions or lack diversity, limiting the robot’s ability to fully utilize its hardware potential. Our method overcomes this challenge by automatically curating a diverse and feasible motion dataset, enabling more effective real-world deployment. 

## III. EXBODY2: LEARNING EXPRESSIVE HUMANOID WHOLE-BODY CONTROL 

We propose Advanced Expressive Whole-Body Control (Exbody2), a sim-to-real framework for expressive and robust whole-body control. As shown in Figure 2, Exbody2 first retargets human motion data to fit the robot’s morphology, then trains a generalist policy using an automated dataset curation strategy to balance feasibility and diversity. To improve precision on specific motion groups, we further fine-tune specialist policies and deploy it onto real humanoid robots. In the following sections, we detail our generalist-specialist training pipeline, and our policy structure design, the two main contributions of our work. 

## _A. Data-driven Generalist-specialist Training Pipeline_ 

We adopt a Generalist–Specialist pipeline to balance adaptability and precision in whole-body motion tracking. At the heart of this pipeline is our **Feasibility–Diversity Principle** , which guides dataset design by requiring _enough motion diversity_ (particularly in the upper body) to cover a broad distribution of tasks, while maintaining _feasibility_ in the lower body to avoid unachievable or overly dynamic motions that degrade training stability. In practice, this amounts to filtering out extreme lower-body samples and retaining a wide range of upper-body actions. Further details on how we discover and validate this principle are in the appendix Section 3. 

**Generalist Policy.** Leveraging the Feasibility–Diversity Principle, we train a generalist policy on a broad dataset that has 

been automatically pruned to remove infeasible lower-body motions. This ensures that the policy learns expressiveness in upper-body movements without being hindered by physically impractical transitions. 

**Specialist Policies.** Once trained, the generalist policy can be fine-tuned for targeted tasks (e.g., dancing or kung fu), resulting in specialist policies with higher precision. 

This two-step approach balances overall adaptability with focused accuracy, as we demonstrate in both simulation and real-world evaluations. 

_1) Generalist policy with automated data curation:_ To obtain a policy _π_ that performs well across diverse motion inputs, we first train an initial policy _π_ 0 on a comprehensive, unfiltered motion dataset _D_ , which is highly diverse with a lot of infeasible motions. After training _π_ 0, we evaluate its tracking accuracy for each motion sequence _s ∈D_ , obtaining a tracking error metric _e_ ( _s_ ) that focuses on the lower body. The lower body plays a central role in dynamic feasibility and balance; thus, we focus on its tracking error for filtering. This preserves the upper body’s diversity while excluding excessively unstable motions, aligning with our feasibility– diversity principle. Specifically, we define 


where _E_ key( _s_ ) is the mean keybody position error for the lower body (preventing extreme deviations such as flipping or rolling), and _E_ dof( _s_ ) measures the mean joint-angle tracking error. The coefficients _α_ and _β_ weight these two terms according to their relative importance for lower-body stability and precision. Once _e_ ( _s_ ) is computed for each sequence, we rank the motions by their tracking errors and derive the empirical distribution _P_ ( _e_ ). 

The objective is to determine an error threshold _τ_ such that the subset of motion sequences with _e_ ( _s_ ) _≤ τ_ , denoted as _Dτ_ = _{s ∈D | e_ ( _s_ ) _≤ τ }_ , enables the training of a new policy _πτ_ that maximizes performance across the full dataset _D_ . Formally, we seek: 


where _πτ_ is trained on _Dτ_ . 

In practice, we divide _P_ ( _e_ ) into evenly spaced error intervals to systematically evaluate the performance of policies trained on subsets corresponding to different thresholds _τ_ . Although we use a greedy search to identify the optimal threshold _τ_<sup>_∗_</sup> , subsequent experiments reveal a strong trend in how the policy’s performance changes with _τ_ . When _τ_ is too small, the filtered motions are overly simple, limiting the policy’s ability to generalize across the full dataset. Conversely, when _τ_ is too large, the inclusion of many infeasible motions introduces noise, degrading the training effectiveness. The best-performing policy is consistently obtained at a moderate _τ_ , balancing diversity and feasibility. 

The optimal threshold _τ_<sup>_∗_</sup> , identified through this process, exhibits generalizability and can be effectively applied to other motion datasets, ensuring robust training and improved performance. 


**Fig. 2:** Exbody2’s framework. (a) Motion retargeting adapts raw human motion datasets to fit the humanoid robot’s morphology, generating a diverse set of training samples. (b) Automated dataset filtering ranks motions based on tracking errors and selects an optimal subset to train a generalist policy, balancing feasibility and diversity. (c) Specialist policy finetuning refines the generalist model for specific motion categories, such as walking, dancing, and kungfu, improving precision for targeted tasks. (d) The trained policies are deployed on a real humanoid robot, demonstrating expressive, dynamic, and stable whole-body motions in real-world environments. 

_2) Specialist policy with finetuning for targeted motions:_ After obtaining the generalist policy _πτ ∗_ , which balances diversity and feasibility across a broad range of motions, we further refine it into a specialist policy tailored for specific, high-precision tasks. This finetuning process leverages the pretrained generalist policy rather than training a new policy from scratch, offering several advantages. 

First, specialist policies require tracking a smaller set of motions with higher precision, making finetuning a more efficient approach. Training directly from scratch for specialized motions is often impractical, as complex actions may be too difficult to learn without a strong prior. In contrast, the generalist policy provides a warm start, enabling the policy to adapt more effectively to challenging motions. 

Second, the generalist policy has been exposed to a wider range of motion sequences, improving robustness to variations and unexpected disturbances. While a policy trained from scratch on specific motions may perform well in simulation, it lacks exposure to diverse conditions. As a result, when deployed in the real world, such a policy may struggle with unseen disturbances or novel states, leading to failures. By finetuning from a generalist model, the specialist policy inherits adaptability and robustness, improving its real-world generalization. 

Finally, finetuning can reduce training time and computational requirements, as it refines an already well-trained model instead of learning from scratch. This makes it a practical and scalable approach for developing high-precision policies for specialized tasks while maintaining strong generalization capabilities. 

## _B. Policy Objective and Architecture_ 

Exbody2 aims at tracking a target motion more expressively in the whole body. To this end, Exbody2 adopts a two-stage teacher-student training procedure as in [29, 28]. Specifically, the oracle teacher policy is first trained with an off-the- 


**Fig. 3:** Teacher-student framework for humanoid motion learning, where the teacher uses privileged information, and the student learns from past observations to generate control actions. 

shelf reinforcement learning (RL) algorithm, PPO [51], with privileged information that can be obtained only in simulators. For the second stage, we replace the privileged information with observations which are aligned with the real world, and distill the teacher policy to a deployable student policy. We train our policies using IsaacGym [39] with efficient parallel simulation. 

_1) Teacher Policy Training:_ We can formulate the humanoid motion control problem as a _Markov Decision Process_ (MDP). The state space _S_ contains privileged observation _X_ , proprioceptive states _O_ and motion tracking target _G_ . A policy _π_ ˆ takes _{pt, ot, gt}_ as input, and outputs action _a_ ˆ _t_ , as illustrated in Figure 3, the teacher policy. The predicted action _a_ ˆ _t ∈ R_<sup>23</sup> is the target joint positions of joint proportional derivative (PD) controllers. We use off-the-shelf PPO [51] algorithm to maximize expectation of the accumulated future rewards _Eπ_ ˆ[<sup>�</sup><sup>_T_</sup> _t_ =0<sup>_γtR_(</sup><sup>_st,_ˆ</sup><sup>_at_)],which</sup> encourages tracking the demonstrations with robust behavior. The predicted _a_ ˆ _t ∈ R_<sup>23</sup> , which is the target position of joint proportional derivative (PD) controllers. 

**Privileged Information.** The privileged information _pt_ contains some ground-truth states of the humanoid robot and the environment, which can only be observed in simulators. It contains the ground-truth root velocity, real body links’ positions, and physical properties (e.g. friction coefficients, motor strength). Privileged information can significantly improve the sample efficiency of RL algorithms, which is often leveraged to obtain a high-performing teacher policy. **Motion Tracking Target.** Similar to Exbody [4], Exbody2 learns a policy that can be controlled by the joystick commands (e.g. the linear velocity and body pose) when accurately tracking a whole-body motion. The motion tracking target consists of two components, which are (1) the desired joints and 3D keypoints in both the upper and lower body and (2) target root velocity and root pose. For the full information about the privileged information, motion tracking information, and proprioceptive observations for the teacher policy, please refer to the supplementary materials. 

**Reward Design.** Our reward function is carefully constructed to enhance the performance and realism of the humanoid robot’s motion. The primary components of the reward include tracking the velocity, direction, and orientation of the root, alongside precise tracking of keypoints and joint positions. Additionally, we incorporate several regularization terms designed to boost the robot’s stability and enhance the transferability from simulation to real-world applications. The main elements of our tracking reward are detailed in Table I, while supplementary rewards aimed at improving stability and sim2real capabilities would discussed in the supplementary materials. 

_2) Student Policy Training:_ In this stage, we remove the privileged information, and use longer history observation to train a student policy. As shown in Figure 3, the student policy encodes a series of past observations _ot−H_ : _t_ together with the encoded _gt_ to get the predicted _at ∼ π_ ( _·|ot−H_ : _t, gt_ ). We supervise _π_ using the teacher’s action _a_ ˆ _t ∼ π_ ˆ( _·|ot, gt_ ) with an MSE loss. 


To train the student, we adopt the strategy used in DAgger [50], we roll out the student policy _π_ in the simulation environment to generate training data. For each visited state, the teacher policy _π_ ˆ computes the oracle action as the supervision signal. We proceed to refine the policy _π_ by iteratively minimizing the loss _l_ on the accumulated data. The training of _π_ ˆ continues through successive rollouts until the loss _l_ reaches convergence. A critical aspect of training the student policy is preserving a sufficiently long sequence of historical observations. Detailed results and further analysis are elaborated in Section IV. 

_3) Motion-velocity Decoupled Control Strategy:_ Motion tracking comprises two objectives: tracking DoF (joint) positions and keypoint (body keypoint) positions. Keypoint tracking usually plays a crucial role in tracking motions during training stage, as joint DoF errors can propagate to the whole 

|Term|Expression|Weight|
|---|---|---|
|Ex|pression Goal _G_<sup>_e_</sup>||
|DoF Position|exp(_−_0_._7_|_**q**ref_−_**q**_|_)|3.0|
|Keypoint Position|exp(_−|_**p**ref_−_**p**_|_)|2.0|
|Root|Movement Goal _G_<sup>_m_</sup>||
|Linear Velocity|exp(_−_4_._0_|_**v**ref_−_**v**_|_)|6.0|
|Velocity Direction|exp(_−_4_._0 cos(**v**ref_,_**v**))|6.0|
|Roll & Pitch|exp(_−|_**Ω**<sup>_ϕθ_</sup><br>ref <sup>_−_</sup><sup>**Ω**</sup><sup>_ϕθ|_)</sup>|1.0|
|Yaw|exp(_−|_∆_y|_)|1.0|


**TABLE I:** Rewards Specification for Exbody2. 

body, while keypoint tracking is directly applied to the body. Existing work like H2O, OmniH2O [18, 17] learns to follow the trajectory of global keypoints. However, this global tracking strategy usually results in suboptimal or failed tracking behavior, as global keypoints may drift through time, resulting in cumulative errors that eventually hinder learning. To address this, we map global keypoints to the robot’s current coordinate frame, and instead utilize velocity-based global tracking. The coordination of velocity and motion allows tracking completion with maximal expressiveness, even if slight positional deviations arise. Moreover, to further enhance the robot’s capabilities in following challenging keypoint motions, we allow a small global drift of keypoints during training stage and periodically correct them to the robot’s current coordinate frame. During deployment, we strictly employ local keypoint tracking with motion-velocity decoupled control. 

## IV. EXPERIMENTS 

In this section, we present experiments to evaluate the effectiveness of Exbody2. We first introduce the experimental setup and the baselines, followed by a detailed analysis addressing the following key research questions: 

**Q1.** (Section IV-B) Does Exbody2 generalist policy achieve higher tracking accuracy in both simulation and real-world deployment compared to prior methods? 

**Q2.** (Section IV-C) What selection criteria lead to the optimal subset of a human motion dataset for learning a better generalist policy? 

**Q3.** (Section IV-D) Does finetuning a specialist policy for specific motion groups further improve tracking performance? 

## _A. Experimental Setup_ 

**Baselines.** To examine the effectiveness of varying tracking methods, motion control strategies, and training techniques, we evaluate four baselines using a classic CMU dataset [1], which includes a wide variety of action types. 

- **Exbody** [4]: This method utilizes one-stage RL training pipeline, and only tracks the upper body movements from the human data, while tracking the root motion of the lower body without explicitly following step patterns and focusing on partial body tracking. 

|Method|_E_vel _↓_|_E_mpkpe _↓_|_E_<sup>upper</sup><br>mpkpe <sup>_↓_</sup>|_E_<sup>lower</sup><br>mpkpe <sup>_↓_</sup>|_E_mpjpe _↓_|_E_<sup>upper</sup><br>mpjpe <sup>_↓_</sup>|_E_<sup>lower</sup><br>mpjpe <sup>_↓_</sup>|
|---|---|---|---|---|---|---|---|
|Exbody<br>|0.4700|0.1339|0.1249|0.1428|0.2020|0.1343|0.2952|
|Exbody<sup>_†_</sup>|0.4195|0.1150|0.1106|0.1198|0.1496|0.1416|0.1607|
|OmniH2O*|0.3725|0.1253|0.1266|0.1240|0.1681|0.1564|0.1843|
|Exbody2-w/o-Filter|**0.2787**|0.1133|0.1087|0.1182|0.1355|0.1192|0.1579|
|**Exbody2(Ours)**|0.2930|**0.1000**|**0.0960**|**0.1040**|**0.1079**|**0.0953**|**0.1253**|


**TABLE II:** Comparisons with baselines on dataset _DCMU_ for Unitree G1. We loop each motion trajectory 10 times in simulation and compute the per-step average error for each policy over all repetitions. The lowest error in each column for each group is highlighted in bold. 

|**Method**|_E_mpjpe _↓_|_E_<sup>upper</sup><br>mpjpe <sup>_↓_</sup>|_E_<sup>lower</sup><br>mpjpe <sup>_↓_</sup>|
|---|---|---|---|
|Exbody|0.2178|0.1223|0.3239|
|Exbody<sup>_†_</sup>|0.1465|0.1314|0.1672|
|OmniH2O*|0.1396|0.1273|0.1533|
|Exbody2-w/o-Filter|0.1361|0.1254|0.1481|
|Exbody2(Ours)|**0.1074**|**0.1092**|**0.1054**|


**TABLE III:** Comparisons with baselines on selected motions for Unitree G1 in real world. 

- **Exbody**<sup>_†_</sup> : The whole-body control version of Exbody, where the full-body movements are tracked based on human data. This setup enables comprehensive human motion imitation, attempting to match the entire body posture to the reference data. 

- **OmniH2O*** : Our reproduction of the OmniH2O [17], using global keypoints tracking and the same observation space as described in the original paper. During deployment, we adapt OmniH2O to our local tracking evaluation for fair comparison. 

- **Exbody2** : Our method utilizes local keypoint tracking and employs data curation to refine the training set. It incorporates various training techniques to enhance overall motion fidelity and improve sim-to-real transfer. 

**Metrics.** We evaluate the policy’s performance using several metrics calculated across all motion sequences from the dataset. The _mean linear velocity error E_ vel (m/s) measures the error between the robot’s root linear velocity and that of the demonstration, indicating the policy’s ability to track velocity. We calculate tracking error in terms of keybody positions and joint angles. The _Mean Per Keybody Position Error_ (MPKPE) _E_ mpkpe (m) evaluates the overall keypoint position tracking ability. For more detailed analysis, we report the MPKPE for the upper body _E_ mpkpe<sup>upper(m)andthelower</sup> body _E_ mpkpe<sup>lower(m),assessingthekeypointpositiontrackingof</sup> the upper and lower body, respectively. Similarly, the _Mean Per Joint Position Error_ (MPJPE) _E_ mpjpe (rad) measures the joint tracking ability. We also report the MPJPE for the upper body _E_ mpjpe<sup>upper(rad)andthelowerbody</sup><sup>_E_</sup> mpjpe<sup>lower(rad)toevaluate</sup> tracking performance in different body regions. 

More details about environment designs and baseline implementations can be found in the supplementary material. 

## _B. Generalist Policy Performance_ 

As shown in Table II, our _Exbody2_ policy already surpasses prior baselines ( _Exbody_ , _Exbody_<sup>_†_</sup> , and _OmniH2O*_ ) across all reported metrics in simulation without motion filter when trained on the complete dataset. By further incorporating motion filtering, _Exbody2_ achieves additional gains in both upper- and lower-body tracking. The improvement in lowerbody accuracy is especially notable, leading to greater global stability and, consequently, more precise upper-body control. 

The only trade-off observed is a slight increase in velocity tracking error compared to the unfiltered version. We attribute this to the broader velocity patterns found in the full dataset, which facilitate more diverse dynamic behaviors but also introduce additional noise. Overall, the modest velocity tradeoff is outweighed by significant enhancements in stability and precision. These trends are observed under simulation conditions, and we further analyze real-world performance in the following section. 

In real-world experiments, we selected a representative subset from the CMU dataset, encompassing a diverse range of actions—such as expressive standing postures, walking at various speeds and patterns, squatting, and dancing. Using the robot’s onboard motor readings, we computed the joint position error, as reported in Table III. The experimental outcomes closely mirror the simulation results, demonstrating that our algorithm achieves higher tracking accuracy compared to other baselines for both upper and lower body segments. Notably, the integration of automated data curation has substantially enhanced performance. This improvement is critical in real-world environments, where unanticipated disturbances are more prevalent, underscoring the importance of maintaining robust and consistent behavior to achieve highprecision tracking throughout the motion sequences. 

Overall, our generalist policy achieves significant improvements in full-body tracking accuracy for both upper and lower body, and velocity tracking accuracy compared to the baseline algorithms both in simulation and the real world, demonstrating stable and effective tracking performance in dynamic environments. 

## _C. Impact of Automatic Data Curation_ 

To experimentally examine the selection criteria for constructing an optimal human motion dataset that enhances generalist policy learning, we conducted the following experiment, 


**Fig. 4:** Impact of dataset filtering thresholds on policy tracking errors. The figure shows the tracking error trends across different dataset filtering thresholds. Policies trained on datasets with filtering thresholds that balance diversity and stability (e.g., _πτ_ =0 _._ 150) achieve the lowest tracking errors. The base policy exhibits suboptimal performance due to unfiltered data, while overly restrictive thresholds (e.g., _πτ_ =0 _._ 075) and overly lenient thresholds (e.g., _πτ_ =0 _._ 175) show reduced effectiveness. We compute the error metric _e_ ( _s_ ) = _α E_ key( _s_ )+ _β E_ dof( _s_ ) with _α_ = 0 _._ 1 _, β_ = 0 _._ 9, assigning heavier weight to the joint-angle term. 

reconstructing the full pipeline of our automated data curation method and evaluating its effect on policy performance. 

- 1) **Base Policy Training** : We first trained a base policy on the unfiltered _DCMU_ dataset, which encompasses a broad range of human motions, including both stable and highly dynamic sequences, as well as infeasible movements that exceed the robot’s physical limitations. 

- 2) **Dataset Filtering** : The base policy’s tracking performance was evaluated on _DCMU_ , and each motion sequence was assigned a tracking error score. Based on these scores, we sorted the sequences and applied filtering thresholds to create progressively refined datasets: _Dτ_ =0 _._ 075, _Dτ_ =0 _._ 1, _Dτ_ =0 _._ 125, _Dτ_ =0 _._ 15, _Dτ_ =0 _._ 175. A lower threshold retains only motions with the lowest tracking errors, ensuring high stability but reducing diversity. Conversely, a higher threshold allows more challenging and diverse motions but introduces tracking instability. 

   - These thresholds were determined based on the error distribution of the base policy, as detailed in the appendix Section 4.B. The distribution-informed selection ensures that the filtering process is not arbitrary but rather grounded in empirical data. This selection strategy is not limited to a specific dataset; rather, it generalizes to other datasets with similar policy architectures and training conditions. When applied to new datasets, it effectively filters motions while maintaining a balance between feasibility and diversity. 

- 3) **Filtered Policy Resume:** For each filtered dataset _Dτ_ , we resume training from the base policy _π_ 0 to obtain a new policy _πτ_ . Concretely, thresholds _τ ∈_ 

   - _{_ 0 _._ 075 _,_ 0 _._ 1 _,_ 0 _._ 125 _,_ 0 _._ 15 _,_ 0 _._ 175 _}_ each yield a distinct subset _Dτ_ , and thus a correspondingly refined policy _πτ_ . This resumption process leverages the base model’s learned prior, enabling faster adaptation to each subset’s motion characteristics and improving overall training efficiency. 

- 4) **Evaluation** : All the resulting policies were evaluated on the full _DCMU_ dataset, measuring tracking performance across multiple metrics. The results are visualized in Figure 4. 

The results confirm that dataset selection significantly influences both generalization and tracking accuracy. A wellchosen dataset, striking a balance between stability and diversity, produces more robust and adaptable policies, in line with our _feasibility-diversity principle_ . 

- **Low Thresholds** (e.g., _πτ_ =0 _._ 075): Policies trained on heavily filtered datasets exhibited poor generalization, as they primarily learned from static and simple motions. While these datasets ensured stability, the lack of diversity limited the policy’s ability to handle more complex behaviors. 

- **High Thresholds** (e.g., _πτ_ =0 _._ 175 _, π_ 0): Policies trained on datasets with high thresholds struggled due to the inclusion of highly dynamic and unstable motions. The increased data variability introduced noise during training, leading to inconsistent policy behavior and reduced tracking accuracy. 

- **Moderate Thresholds** (e.g., _πτ_ =0 _._ 15): Policies trained on datasets with intermediate thresholds achieved the best trade-off between feasibility and diversity. The dataset _Dτ_ =0 _._ 15 retained sufficient variability to improve generalization while excluding excessively difficult or unstable motions, leading to the lowest overall tracking error. 

These findings validate the importance of carefully balancing feasibility and diversity in dataset selection. The dataset _Dτ_ =0 _._ 15 and its corresponding policy _πτ_ =0 _._ 15 emerged as the optimal choice, ensuring both strong generalization and stable tracking performance. This highlights the necessity of structured dataset curation in developing robust robotic policies, particularly for real-world deployment where adaptability and reliability are crucial. 

## _D. Specialist Policy finetuning_ 

We evaluate the effectiveness of the pretrain-finetune paradigm in enhancing policy performance. To this end, we compare three distinct training strategies: 

- **Generalist** : A generalist policy trained on the automatically filtered dataset ( _πτ_ =0 _._ 15), designed to provide broad motion coverage and strong generalization across diverse tasks. 

- **Specialist** : A specialist policy obtained by fine-tuning the pretrained generalist policy on task-specific datasets, enabling higher precision for specialized motions. 

- **Scratch** : A policy trained from scratch on the same taskspecific datasets. To ensure fairness, we match its total 

|**Method**|_E_vel _↓_|_E_mpkpe _↓_|_E_<sup>upper</sup><br>mpkpe <sup>_↓_</sup>|_E_<sup>lower</sup><br>mpkpe <sup>_↓_</sup>|_E_mpjpe _↓_|_E_<sup>upper</sup><br>mpjpe <sup>_↓_</sup>|_E_<sup>lower</sup><br>mpjpe <sup>_↓_</sup>|
|---|---|---|---|---|---|---|---|
|**(b)** _Deasy_||||||||
|Specialist|**0.0828**|**0.0561**|**0.0564**|**0.0558**|**0.0772**|**0.0647**|**0.0944**|
|Scratch|0.0853|0.0608|0.0623|0.0592|0.0843|0.0711|0.1024|
|Generalist|0.0986|0.0699|0.0708|0.0690|0.1041|0.0882|0.1259|
|**(a)** _DModer_|_ate_|||||||
|Specialist|**0.0991**|**0.0571**|**0.0582**|**0.0559**|**0.0760**|**0.0636**|**0.0930**|
|Scratch|0.1188|0.0676|0.0688|0.0663|0.0924|0.0794|0.1103|
|Generalist|0.1217|0.0741|0.0727|0.0755|0.1092|0.0914|0.1337|
|**(c)** _DHard_||||||||
|Specialist|0.1712|**0.0827**|**0.0829**|**0.0826**|**0.1047**|**0.0911**|**0.1234**|
|Scratch|0.1631|0.0886|0.0898|0.0873|0.1188|0.1067|0.1354|
|Generalist|**0.1452**|0.0890|0.0867|0.0912|0.1181|0.1011|0.1414|
|**(d)** _DACCA_|_D_|||||||
|Specialist|0.4021|**0.1149**|**0.1079**|**0.1215**|**0.1402**|**0.1290**|**0.1557**|
|Scratch|0.4153|0.1246|0.1154|0.1332|0.1609|0.1490|0.1771|
|Generalist|**0.3361**|0.1268|0.1156|0.1391|0.1716|0.1532|0.1967|


**TABLE IV:** Comparison of three training strategies ( _Generalist_ , _Specialist_ , _Scratch_ ) across four dataset groups ( _Deasy_ , _Dmoderate_ , _Dhard_ , and _DACCAD_ ). 


**Fig. 5:** A sequence of a robot performing the Cha-Cha dance. From top to bottom: the reference motion represented by an avatar, our algorithm’s performance in the simulation, and its performance on a real robot. The bottom three rows show the per-frame errors: wholebody joint DoF error, upper-body joint DoF error, and lower-body DoF error, with the blue curve representing _Exbody2-Specialist_ policy finetuned on _Ddancing_ , orange for _Exbody2-Scratch_ policy training from scratch on _Ddancing_ , green for our _Exbody2-Generalist_ policy trained on filtered _DCMU_ . 

training iterations to the sum of _pretraining_ plus _finetuning_ iterations used in the Specialist approach. 

To assess the robustness and adaptability of these policies, we conduct experiments across four manually curated datasets: 

- _D_ easy _, D_ moderate _, D_ hard: A series of datasets with increasing difficulty levels, categorized based on motion dynamics. Lower-difficulty datasets mainly contain static or lowmovement motions, while higher-difficulty datasets in- 

clude more dynamic and high-momentum movements. This progression allows us to assess how well the policies generalize to increasingly complex motions. 

- _D_ ACCAD: An out-of-distribution (OOD) dataset used to evaluate the generalization capability of the learned policies on previously unseen motion patterns. 

The quantitative evaluation results are summarized in Table IV. The key findings from these experiments are discussed below. 

- 1) **Performance on** _D_ **easy** _, D_ **moderate** _, D_ **hard** : The finetuned policy achieves the best performance across all difficulty levels. The more challenging the dataset, the greater the advantage of finetuning over training from scratch, demonstrating the importance of leveraging a pretrained policy as a foundation for specialized tasks. For highly dynamic motions, the generalist policy exhibits slightly better velocity tracking due to its broader exposure to diverse movements. However, the specialist policy consistently achieves higher overall precision. 

- 2) **Performance on** _D_ **ACCAD** : The finetuned policy significantly outperforms both the pretrained and scratch policies on the OOD dataset, highlighting its superior generalizability and adaptability to unseen scenarios. This result further confirms that the pretrained generalist policy provides a strong foundation, while finetuning enhances task-specific adaptation. 

To better illustrate the effectiveness of the specialist policy, we select the Cha-Cha dance as a case study, as shown in Figure 5. Cha-Cha is one of the representative motions in the dance group and involves dynamic lower-body movements combined with expressive upper-body gestures. By comparing policies trained from scratch, the generalist policy, and the specialist policy fine-tuned on the dancing dataset, we observe that the specialist policy achieves significantly lower tracking errors across all key metrics. This result further confirms the 

advantage of task-specific finetuning in capturing fine-grained motion details while maintaining stability. 

In conclusion, the pretrain-finetune paradigm proves to be an effective strategy for achieving robust and adaptable policies. The pretrained generalist policy ( _πτ_ =0 _._ 15) provides a strong starting point, while finetuning allows specialization for specific tasks, resulting in superior performance across diverse datasets. This approach demonstrates significant benefits, particularly in challenging and OOD scenarios, and highlights the importance of combining generalist capabilities with taskspecific specialization. 

## V. CONCLUSION 

This paper introduces Advanced Expressive Whole-Body Control (Exbody2), a novel framework for humanoid wholebody control that achieves superior tracking accuracy, stability, and adaptability through automated dataset filtering, a generalist-specialist training pipeline, and a decoupled keypoint-velocity tracking strategy. Experiments show that Exbody2 outperforms prior methods by balancing feasibility and diversity in dataset selection, enabling more robust whole-body tracking, and improving generalization across diverse motion tasks. The specialist finetuning further refines performance for high-precision tasks, demonstrating the effectiveness of a structured pretrain-finetune paradigm. These contributions push the boundaries of humanoid motion control, paving the way for more expressive and stable real-world deployments. 

## VI. LIMITATIONS 

Although our _generalist_ policy already provides broad coverage of diverse motions, it does not capture the fine-grained precision of each specialist policy within a single framework. One limitation of our approach is the inability to seamlessly recombine policies that have been fine-tuned for specific motion groups. This constraint reduces the flexibility of switching between different policies within a single tracking session, as each specialist policy remains focused on a particular subset of motions. Consequently, transitions between different motion types may not be handled as smoothly or efficiently as desired. 

_In principle, unifying the broad coverage of the generalist policy with the high-accuracy tracking of individual specialists could provide the best of both worlds._ Addressing this limitation by incorporating a dynamic policy-integration mechanism—where specialized policies can be adaptively blended or switched in real time—could significantly improve overall tracking precision, adaptability, and robustness, especially when dealing with complex, multi-modal motion sequences. 

REFERENCES 

- [1] Carnegie Mellon University. Carnegie-Mellon mocap database. http://mocap.cs.cmu.edu/, Mar 2007. [Online]. 

- [2] Sirui Chen, Chen Wang, Kaden Nguyen, Li Fei-Fei, and C Karen Liu. Arcap: Collecting high-quality human demonstrations for robot learning with augmented reality feedback. _arXiv preprint arXiv:2410.08464_ , 2024. 

- [3] Xuxin Cheng, Yandong Ji, Junming Chen, Ruihan Yang, Ge Yang, and Xiaolong Wang. Expressive whole-body control for humanoid robots, 2024. URL https://arxiv. org/abs/2402.16796. 

- [4] Xuxin Cheng, Yandong Ji, Junming Chen, Ruihan Yang, Ge Yang, and Xiaolong Wang. Expressive wholebody control for humanoid robots. _arXiv preprint arXiv:2402.16796_ , 2024. 

- [5] Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and Shuran Song. Universal manipulation interface: Inthe-wild robot teaching without in-the-wild robots. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- [6] Matthew Chignoli, Donghyun Kim, Elijah Stanger-Jones, and Sangbae Kim. The mit humanoid robot: Design, motion planning, and control for acrobatic behaviors. In _2020 IEEE-RAS 20th International Conference on Humanoid Robots (Humanoids)_ , pages 1–8. IEEE, 2021. 

- [7] Antonin Dallard, Mehdi Benallegue, Fumio Kanehiro, and Abderrahmane Kheddar. Synchronized humanhumanoid motion imitation. _IEEE Robotics and Automation Letters_ , 8(7):4155–4162, 2023. doi: 10.1109/LRA. 2023.3280807. 

- [8] Behzad Dariush, Michael Gienger, Bing Jian, Christian Goerick, and Kikuo Fujimura. Whole body humanoid control from human motion descriptors. In _2008 IEEE International Conference on Robotics and Automation_ , pages 2677–2684. IEEE, 2008. 

- [9] Kourosh Darvish, Yeshasvi Tirupachuri, Giulio Romualdi, Lorenzo Rapetti, Diego Ferigo, Francisco Javier Andrade Chavez, and Daniele Pucci. Wholebody geometric retargeting for humanoid robots. In _2019 IEEE-RAS 19th International Conference on Humanoid Robots (Humanoids)_ , pages 679–686, 2019. doi: 10.1109/Humanoids43949.2019.9035059. 

- [10] Helei Duan, Bikram Pandit, Mohitvishnu S Gadde, Bart Jaap van Marum, Jeremy Dao, Chanho Kim, and Alan Fern. Learning vision-based bipedal locomotion for challenging terrain. _arXiv preprint arXiv:2309.14594_ , 2023. 

- [11] Pranay Dugar, Aayam Shrestha, Fangzhou Yu, Bart van Marum, and Alan Fern. Learning multi-modal wholebody control for real-world humanoid robots, 2024. URL https://arxiv.org/abs/2408.07295. 

- [12] Alejandro Escontrela, Xue Bin Peng, Wenhao Yu, Tingnan Zhang, Atil Iscen, Ken Goldberg, and Pieter Abbeel. Adversarial motion priors make good substitutes 

for complex reward functions. 2022 ieee. In _International Conference on Intelligent Robots and Systems (IROS)_ , volume 2, 2022. 

- [13] Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. Humanplus: Humanoid shadowing and imitation from humans, 2024. URL https://arxiv.org/abs/ 2406.10454. 

- [14] Zipeng Fu, Tony Z Zhao, and Chelsea Finn. Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. _arXiv preprint arXiv:2401.02117_ , 2024. 

- [15] Huy Ha, Yihuai Gao, Zipeng Fu, Jie Tan, and Shuran Song. Umi on legs: Making manipulation policies mobile with manipulation-centric whole-body controllers. _arXiv preprint arXiv:2407.10353_ , 2024. 

- [16] Mohamed Hassan, Yunrong Guo, Tingwu Wang, Michael Black, Sanja Fidler, and Xue Bin Peng. Synthesizing physical character-scene interactions. 2023. doi: 10.1145/3588432.3591525. URL https://doi.org/10.1145/ 3588432.3591525. 

- [17] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning, 2024. URL https://arxiv.org/abs/2406.08858. 

- [18] Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning humanto-humanoid real-time whole-body teleoperation. _arXiv preprint arXiv:2403.04436_ , 2024. 

- [19] Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Changliu Liu, Guanya Shi, Xiaolong Wang, Linxi Fan, and Yuke Zhu. Hover: Versatile neural whole-body controller for humanoid robots. _arXiv preprint arXiv:2410.21229_ , 2024. 

- [20] Kazuo Hirai, Masato Hirose, Yuji Haikawa, and Toru Takenaka. The development of honda humanoid robot. In _Proceedings. 1998 IEEE international conference on robotics and automation (Cat. No. 98CH36146)_ , volume 2, pages 1321–1326. IEEE, 1998. 

- [21] Albert S. Huang, Edwin Olson, and David C. Moore. Lcm: Lightweight communications and marshalling. _2010 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 4057–4062, 2010. URL https://api.semanticscholar.org/CorpusID:10900899. 

- [22] Marco Hutter, Christian Gehring, Dominic Jud, Andreas Lauber, C Dario Bellicoso, Vassilios Tsounis, Jemin Hwangbo, Karen Bodie, Peter Fankhauser, Michael Bloesch, et al. Anymal-a highly mobile and dynamic quadrupedal robot. In _IROS_ , 2016. 

- [23] Hiroshi Ito, Kenjiro Yamamoto, Hiroki Mori, and Tetsuya Ogata. Efficient multitask learning with an embodied predictive model for door opening and entry with wholebody control. _Science Robotics_ , 7(65):eaax8177, 2022. 

- [24] Seunghun Jeon, Moonkyu Jung, Suyoung Choi, Beomjoon Kim, and Jemin Hwangbo. Learning wholebody manipulation for quadrupedal robot. _arXiv preprint_ 

_arXiv:2308.16820_ , 2023. 

- [25] Shuuji Kajita, Fumio Kanehiro, Kenji Kaneko, Kazuhito Yokoi, and Hirohisa Hirukawa. The 3d linear inverted pendulum mode: A simple modeling for a biped walking pattern generation. In _Proceedings 2001 IEEE/RSJ International Conference on Intelligent Robots and Systems. Expanding the Societal Role of Robotics in the the Next Millennium (Cat. No. 01CH37180)_ , volume 1, pages 239–246. IEEE, 2001. 

- [26] Simar Kareer, Dhruv Patel, Ryan Punamiya, Pranay Mathur, Shuo Cheng, Chen Wang, Judy Hoffman, and Danfei Xu. Egomimic: Scaling imitation learning via egocentric video, 2024. URL https://arxiv.org/abs/2410. 24221. 

- [27] Ichiro Kato. Development of wabot 1. _Biomechanism_ , 2:173–214, 1973. 

- [28] Ashish Kumar, Zipeng Fu, Deepak Pathak, and Jitendra Malik. Rma: Rapid motor adaptation for legged robots. _arXiv preprint arXiv:2107.04034_ , 2021. 

- [29] Joonho Lee, Jemin Hwangbo, Lorenz Wellhausen, Vladlen Koltun, and Marco Hutter. Learning quadrupedal locomotion over challenging terrain. _Science robotics_ , 5 (47):eabc5986, 2020. 

- [30] Jiefeng Li, Chao Xu, Zhicun Chen, Siyuan Bian, Lixin Yang, and Cewu Lu. Hybrik: A hybrid analyticalneural inverse kinematics solution for 3d human pose and shape estimation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 3383–3393, 2021. 

- [31] Jinhan Li, Yifeng Zhu, Yuqi Xie, Zhenyu Jiang, Mingyo Seo, Georgios Pavlakos, and Yuke Zhu. Okami: Teaching humanoid robots manipulation skills through single video imitation. In _8th Annual Conference on Robot Learning_ , 2024. 

- [32] Zhongyu Li, Xuxin Cheng, Xue Bin Peng, Pieter Abbeel, Sergey Levine, Glen Berseth, and Koushil Sreenath. Reinforcement learning for robust parameterized locomotion control of bipedal robots. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 2811–2817. IEEE, 2021. 

- [33] Zhongyu Li, Xue Bin Peng, Pieter Abbeel, Sergey Levine, Glen Berseth, and Koushil Sreenath. Robust and versatile bipedal jumping control through multi-task reinforcement learning. _arXiv preprint arXiv:2302.09450_ , 2023. 

- [34] Zhongyu Li, Xue Bin Peng, Pieter Abbeel, Sergey Levine, Glen Berseth, and Koushil Sreenath. Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control. _arXiv preprint arXiv:2401.16889_ , 2024. 

- [35] Qiayuan Liao, Bike Zhang, Xuanyu Huang, Xiaoyu Huang, Zhongyu Li, and Koushil Sreenath. Berkeley humanoid: A research platform for learning-based control. _arXiv preprint arXiv:2407.21781_ , 2024. 

- [36] Hung Yu Ling, Fabio Zinno, George Cheng, and Michiel Van De Panne. Character controllers using motion 

vaes. _ACM Transactions on Graphics (TOG)_ , 39(4):40–1, 2020. 

- [37] Zhengyi Luo, Jinkun Cao, Josh Merel, Alexander Winkler, Jing Huang, Kris M. Kitani, and Weipeng Xu. Universal humanoid motion representations for physicsbased control. In _The Twelfth International Conference on Learning Representations_ , 2024. URL https: //openreview.net/forum?id=OrOd8PxOO2. 

- [38] Naureen Mahmood, Nima Ghorbani, Nikolaus F. Troje, Gerard Pons-Moll, and Michael J. Black. Amass: Archive of motion capture as surface shapes. In _The IEEE International Conference on Computer Vision (ICCV)_ , Oct 2019. URL https://amass.is.tue.mpg.de. 

- [39] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- [40] Hirofumi Miura and Isao Shimoyama. Dynamic walk of a biped. _IJRR_ , 1984. 

- [41] Federico L Moro and Luis Sentis. Whole-body control of humanoid robots. _Humanoid Robotics: A reference, Springer, Dordrecht_ , 2019. 

- [42] Luigi Penco, Nicola Scianca, Valerio Modugno, Leonardo Lanari, Giuseppe Oriolo, and Serena Ivaldi. A multimode teleoperation framework for humanoid loco-manipulation: An application for the icub robot. _IEEE Robotics and Automation Magazine_ , 26(4):73–82, 2019. doi: 10.1109/MRA.2019.2941245. 

- [43] Xue Bin Peng, Erwin Coumans, Tingnan Zhang, TsangWei Edward Lee, Jie Tan, and Sergey Levine. Learning agile robotic locomotion skills by imitating animals. In _Robotics: Science and Systems_ , 07 2020. doi: 10.15607/ RSS.2020.XVI.064. 

- [44] Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 

- [45] Xue Bin Peng, Yunrong Guo, Lina Halper, Sergey Levine, and Sanja Fidler. Ase: Large-scale reusable adversarial skill embeddings for physically simulated characters. _ACM Trans. Graph._ , 41(4), July 2022. 

- [46] Yuzhe Qin, Hao Su, and Xiaolong Wang. From one hand to multiple hands: Imitation learning for dexterous manipulation from single-camera teleoperation. _IEEE Robotics and Automation Letters_ , 7(4):10873–10881, 2022. 

- [47] Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Realworld humanoid locomotion with reinforcement learning. _arXiv:2303.03381_ , 2023. 

- [48] Ilija Radosavovic, Bike Zhang, Baifeng Shi, Jathushan Rajasegaran, Sarthak Kamat, Trevor Darrell, Koushil Sreenath, and Jitendra Malik. Humanoid locomotion as next token prediction. _arXiv:2402.19469_ , 2024. 

- [49] Joao Ramos and Sangbae Kim. Dynamic locomotion synchronization of bipedal robot and human operator via bilateral feedback teleoperation. _Science Robotics_ , 4(35):eaav4282, 2019. doi: 10.1126/ scirobotics.aav4282. URL https://www.science.org/doi/ abs/10.1126/scirobotics.aav4282. 

- [50] St´ephane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , 2011. 

- [51] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [52] Mingyo Seo, Steve Han, Kyutae Sim, Seung Hyeon Bang, Carlos Gonzalez, Luis Sentis, and Yuke Zhu. Deep imitation learning for humanoid loco-manipulation through human teleoperation. In _2023 IEEE-RAS 22nd International Conference on Humanoid Robots (Humanoids)_ , pages 1–8. IEEE, 2023. 

Strategy and skill learning for physics-based table tennis animation. In _ACM SIGGRAPH 2024 Conference Papers_ , pages 1–11, 2024. 

   - [61] Eric R Westervelt, Jessy W Grizzle, and Daniel E Koditschek. Hybrid zero dynamics of planar biped walkers. _IEEE transactions on automatic control_ , 48(1): 42–56, 2003. 

   - [62] KangKang Yin, Kevin Loken, and Michiel Van de Panne. Simbicon: Simple biped locomotion control. _ACM Transactions on Graphics_ , 2007. 

   - [63] Haotian Zhang, Ye Yuan, Viktor Makoviychuk, Yunrong Guo, Sanja Fidler, Xue Bin Peng, and Kayvon Fatahalian. Learning physically simulated tennis skills from broadcast videos. _ACM Trans. Graph._ , 42(4), jul 2023. ISSN 0730-0301. doi: 10.1145/3592408. URL https://doi.org/10.1145/3592408. 

   - [64] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

- [53] Jonah Siekmann, Kevin Green, John Warila, Alan Fern, and Jonathan Hurst. Blind bipedal stair traversal via sim-to-real reinforcement learning. _arXiv preprint arXiv:2105.08328_ , 2021. 

- [54] Mohan Kumar Srirama, Sudeep Dasari, Shikhar Bahl, and Abhinav Gupta. Hrp: Human affordances for robotic pre-training. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- [55] Annan Tang, Takuma Hiraoka, Naoki Hiraoka, Fan Shi, Kento Kawaharazuka, Kunio Kojima, Kei Okada, and Masayuki Inaba. Humanmimic: Learning natural locomotion and transitions for humanoid robot via wasserstein adversarial imitation. _arXiv preprint arXiv:2309.14225_ , 2023. 

- [56] Chen Tessler, Yoni Kasten, Yunrong Guo, Shie Mannor, Gal Chechik, and Xue Bin Peng. Calm: Conditional adversarial latent models for directable virtual characters. In _ACM SIGGRAPH 2023 Conference Proceedings_ , SIGGRAPH ’23, New York, NY, USA, 2023. Association for Computing Machinery. ISBN 9798400701597. doi: 10.1145/3588432.3591541. URL https://doi.org/10.1145/ 3588432.3591541. 

- [57] Chen Tessler, Yunrong Guo, Ofir Nabati, Gal Chechik, and Xue Bin Peng. Maskedmimic: Unified physics-based character control through masked motion inpainting. _ACM Transactions on Graphics (TOG)_ , 2024. 

- [58] Chen Wang, Linxi Fan, Jiankai Sun, Ruohan Zhang, Li Fei-Fei, Danfei Xu, Yuke Zhu, and Anima Anandkumar. Mimicplay: Long-horizon imitation learning by watching human play. _arXiv preprint arXiv:2302.12422_ , 2023. 

- [59] Chen Wang, Haochen Shi, Weizhuo Wang, Ruohan Zhang, Li Fei-Fei, and C. Karen Liu. Dexcap: Scalable and portable mocap data collection system for dexterous manipulation. _arXiv preprint arXiv:2403.07788_ , 2024. 

- [60] Jiashun Wang, Jessica Hodgins, and Jungdam Won. 

APPENDIX 

## _A. Real-world Deployment_ 

Our real robot employs a Unitree G1 platform, with an onboard Jetson Orin NX acting as the primary computing and communication device. The control policy receives motiontracking target information as input, computes the desired joint positions for each motor, and sends commands to the robot’s low-level interface. The policy’s inference frequency is set at 50 Hz. The commands are sent with a delay kept between 18 and 30 milliseconds. The low-level interface operates at a frequency of 500 Hz, ensuring smooth real-time control. The communication between the control policy and the low-level interface is realized through LCM (Lightweight Communications and Marshalling) [21]. 

## _B. State Space Definition_ 

In this section, we provide detailed information on the state space used for policy training, including proprioceptive states, privileged information, and motion tracking targets. **Robot Proprioceptive States.** The robot proprioceptive states for the teacher and the student policy can be found in Table V. Note that the student policy is trained on longer history length compared to the teacher, as it cannot observe privileged information but have to learn from a longer sequence of past observations. 

**Privileged Information.** The teacher policy leverages privileged information to obtain accurate motion-tracking performance. The complete information about the privileged states is listed in Table VI. 

**Tracking Target Information.** Both the teacher policy and student policy also take the motion tracking goal as part of their observations, which consists of the keypoint positions, DoF (joint) positions, as well as root movement information. The detailed components of the motion tracking target can be found in Table VII. 

**Action Space.** The action is the target position of joint proportional derivative (PD) controllers, which is 23 dimensions for Unitree G1. 

|**State**|**Dimensions**|
|---|---|
|DoF Difference|23|
|Keybody Difference|36|
|Root velocity|3|
|**Total dim**|**62**|


### **TABLE VI:** Privileged information used in Exbody2. 

|**State**|**Dimensions**|
|---|---|
|DoF position|23|
|Keypoint position|36|
|Root Velocity|3|
|Root Angular Velocity|3|
|Roll|1|
|Pitch|1|
|Yaw|1|
|Height|1|
|**Total dim**|**69**|


**TABLE VII:** Reference information used in Exbody2. 

extended Exbody to tracking the all three dofs of the waist, while keeping other aspects identical. The key differences between Exbody and our method are as follows: Exbody focuses solely on upper-body motion tracking, does not utilize a teacher-student structure, uses a history length of only 5, and performs tracking entirely with local keypoints. 

**Exbody**<sup>_†_</sup> : Exbody<sup>_†_</sup> is the full-body version of Exbody. It maintains most aspects of the original Exbody design but tracks the entire body’s keypoints and joint positions instead of just the upper body. 

**OmniH2O**<sup>_∗_</sup> [17]: The main difference between OmniH2O<sup>*</sup> and our method lies in the training phase. Specifically, OmniH2O<sup>*</sup> does not use the robot’s velocity as privileged information and relies solely on global tracking during training. For fairness, while OmniH2O<sup>*</sup> retains its original training method, we adapted it during testing to use local keypoints for evaluating tracking accuracy. Apart from this, we ensured that the observation space and reward design were consistent with the original OmniH2O implementation. 

## _D. Policy Training Hyper-parameters_ 

|**State**|**Dimensions**|
|---|---|
|DoF position|23|
|DoF velocity|23|
|Last Action|23|
|Root Angular Velocity|3|
|Roll|1|
|Pitch|1|
|Yaw|1|
|**Total Dim**|**75*10**|


**TABLE V:** Proprioceptive states used in Exbody2. The rotation information is from IMU. 10 is the length of the history proprioception 

Exbody2 adopts a teacher-student training framework. The teacher policy is trained with standard PPO [51] algorithm on privileged information, tracking target and proprioceptive states. The student policy is trained with Dagger [50] without privileged information, but using longer history. For both teacher and student policies, we concatenate the corresponding inputs and feed them into MLP layers for policy learning. We provide the detailed training hyper-parameters for our teacher and student policy in Table VIII. 

## _E. Reward Design_ 

## _C. Baseline Implementation_ 

**Exbody** [4]: The implementation of Exbody is consistent with the original Exbody design, tracking only the upper-body keypoints and joint positions. For the Unitree G1 robot, we 

In the main paper, we partially introduced our trackingbased reward design. Additionally, our reward also contains other penalties and regularization terms. The regularization reward components and their weights to compute the final rewards are introduced in Table IX. The final reward combines 


**Fig. 6:** Illustration of ExBody2’s multi-source application, demonstrating how VR, RGB, motion capture, and generative models can be combined to produce diverse humanoid behaviors. **(a) Motion Datasets:** specialized policies (e.g., kung fu, dancing) finetuned on specialist motion datasets. **(b) Real-time Whole-body Mimic:** real-time replication of human motions from monocular RGB via HybrIK. **(c) Motion Synthesis:** a CVAE-based approach for extended and varied motion generation. Experiments demonstrate ExBody2’s capability to seamlessly integrate multiple motion sources in both simulation and real-world scenarios. 

|Hyperparameter|Value|
|---|---|
|Optimizer|Adam|
|_β_1_, β_2|0.9, 0.999<br>|
|Learning Rate|1_e_<sup>_−_4</sup>|
|Batch Size|4096|
|**Teacher Policy**||
|Discount factor (_γ_)|0.99|
|Clip Param|0.2|
|Entropy Coef|0.005|
|Max Gradient Norm|1|
|Learning Epoches|5|
|Mini Batches|4|
|Value Loss Coef|1|
|Entropy Coef|0.005|
|Value MLP Size|[512, 256, 128]|
|Actor MLP Size|[512, 256, 128]|
|**Student Policy**||
|Student Policy MLP Size|[1024, 1024, 512]|


**TABLE VIII:** Hyperparameters related to the teacher and student policy’s training. 

both the regularization with the tracking-based reward to train a robust RL policy. 

|**Term**|**Expression**|**Weight**|
|---|---|---|
|DoF position limits|1(_dt /∈_[_q_min_, q_max])<br>|_−_10|
|DoF acceleration|_∥_<sup>¨</sup>_dt∥_<sup>2</sup><br>2<br>|_−_3_e_<sup>_−_7</sup>|
|DoF error|_∥dt −d_0_∥_<sup>2</sup><br>2<br>|_−_0_._1|
|Action rate|_∥at −at−_1_∥_<sup>2</sup><br>2|_−_0_._1|
|Feet air time|_T_air_−_0_._5|10|
|Feet contact force|_∥F_feet_∥_<sup>2</sup><br>2|_−_0_._003|
|Stumble|1(_F _<sup>_x_</sup><br>feet <sup>_>_ 5</sup><sup>_× F z_</sup><br>feet<sup>)</sup>|_−_2|
|Waist roll pitch error|<br><br>_∥p_<sup>wrp</sup><br>_t_<br>_−p_<sup>wrp</sup><br>0 <sup>_∥_2</sup><br>2<br><br>|_−_0_._5|
|Ankle Action|_∥a_<sup>ankle</sup><br>_t_<br>_∥_<sup>2</sup><br>2|_−_0_._1|


**TABLE IX:** Regularization rewards for preventing undesired behaviors for sim-to-real transfer and refined motion. 

In the main paper, we propose a **Feasibility–Diversity Principle** , which posits that a good motion dataset for humanoid tracking must be: 

1) _Diverse enough_ (especially in upper-body movements) 

||||||**Metrics**||||
|---|---|---|---|---|---|---|---|---|
|**Training Dataset**|**In dist.**|_E_vel _↓_|_E_mpkpe _↓_|_E_<sup>upper</sup><br>mpkpe <sup>_↓_</sup>|_E_<sup>lower</sup><br>mpkpe <sup>_↓_</sup>|_E_mpjpe _↓_|_E_<sup>upper</sup><br>mpjpe <sup>_↓_</sup>|_E_<sup>lower</sup><br>mpjpe <sup>_↓_</sup>|
|**(a) Eval. on** _D_50|||||||||
|_D_50|✓|**0.1375**|**0.0627**|**0.0571**|**0.0682**|**0.0753**|**0.0626**|**0.0928**|
|_D_250|✓|0.1454|0.0669|0.0600|0.0738|0.0870|0.0689|0.1119|
|_D_CMU|✓|0.1543|0.0767|0.0649|0.0885|0.1099|0.0854|0.1437|
|**(b) Eval. on** _D_**CMU**|||||||||
|_D_50|✗|0.3509|0.1076|0.1074|0.1076|0.1338|0.1285|0.1410|
|_D_250|✗|0.2834|**0.1048**|**0.1021**|**0.1073**|**0.1148**|**0.1012**|**0.1335**|
|_D_CMU|✓|**0.2622**|0.1071|0.1036|0.1110|0.1291|0.1129|0.1512|
|**(c) Eval. on** _D_**ACCAD**|||||||||
|_D_50|✗|0.4226|0.1277|0.1210|0.1330|0.1720|0.1618|0.1861|
|_D_250|✗|0.3533|**0.1234**|**0.1141**|**0.1315**|**0.1421**|**0.1223**|**0.1692**|
|_D_CMU|✗|**0.3452**|0.1267|0.1146|0.1381|0.1780|0.1635|0.1979|


**TABLE X:** Dataset Ablation Study: Evaluation on _D_ 50, _D_ CMU, and _D_ ACCAD datasets with models trained on various datasets. Statistically significant results are highlighted in bold across 5 random seeds. 

to ensure the learned policy can generalize beyond very simple or repetitive actions. 

- 2) _Feasible enough_ that lower-body motions do not exceed the robot’s mechanical limits, avoiding extreme samples (e.g., tumbling, handstands) that hamper training. 

To illustrate how we arrived at this principle, We manually design three datasets of varying sizes, where the largest being the complete CMU dataset. The remaining datasets, with sizes 50, and 250, are subsets of the CMU dataset, each constructed with different levels of action diversity: 

- **50-action dataset** ( _D_ 50): A minimal set containing only fundamental and mostly static actions (e.g., standing, simple walking). While highly feasible, it lacks diversity in both upper and lower limb motions. 

- **250-action dataset** ( _D_ 250): A moderate-sized set extending _D_ 50 with additional upper-limb variations (e.g., arm gestures, some dance moves) and moderately dynamic lower-body actions (e.g., running, mild jumps). Crucially, it avoids highly extreme motions that are difficult for the robot to replicate. 

- **Full CMU dataset** ( _DCMU_ ): The complete CMU motion-capture repository of 1,919 sequences, including extreme movements like push-ups, rolling on the ground, and somersaults. Although highly diverse, it contains many infeasible actions that can introduce significant training noise. 

We train separate policies with our Exbody2 framework on each dataset above and test them on three different evaluation sets: 

- 1) _D_ 50 (in-distribution for the simplest data). 

- 2) _DCMU_ (the full, more complex dataset). 

- 3) _DACCAD_ , an out-of-distribution set containing actions not found in any of the training subsets. 

Table X summarizes our findings: 

- **Evaluation on** _D_ 50: Policies trained on _D_ 50 unsurprisingly achieve the highest tracking accuracy for _indistribution_ actions, as reflected in metrics across all categories. This suggests that additional data does not necessarily benefit in-distribution tasks. While the policy trained on _D_ 250 performs similarly to _D_ 50, the policy trained on _DCMU_ exhibits a substantial drop in tracking accuracy. 

- **Evaluation on** _DCMU_ : Policies trained on _D_ 250 achieve the best performance on _DCMU_ , surpassing those trained on the full _DCMU_ dataset. Due to the limited diversity of the _D_ 50 dataset, especially in upper limb movements, the _D_ 50-trained policy struggles to maintain high accuracy for out-of-distribution actions. Unexpectedly, the _D_ 250trained policy generalizes better than the one trained on _DCMU_ . This result underscores that noisy datasets degrade policy performance, as the policy may expend unnecessary effort on tracking infeasible actions, lowering the accuracy of feasible actions. 

- **Evaluation on** _DACCAD_ : This experiment further emphasizes the importance of clean datasets. Here, the ACCAD dataset ( _DACCAD_ ) consists of actions that are entirely not in the training data. The policy trained on _D_ 250 outperforms the others, achieving the best tracking accuracy. Additionally, the _D_ 250 and _DCMU_ -trained policies perform relatively well in velocity tracking. However, the _D_ 50-trained policy suffers from substantial tracking errors, suggesting the limitations of a small, simple dataset in handling unseen data. 

In conclusion, these results validate the core insight behind our **Feasibility–Diversity Principle** . A small dataset ( _D_ 50) is indeed easy for the policy to master but lacks sufficient variety to generalize well. On the other hand, a fully unfiltered 


**Fig. 7:** Sim-to-real experiment results showcasing diverse motions across SMPL, simulation, and real-world environments. Examples include: (a) Clasping Fists, (b) Clapping Twist, (c) Greeting Gesture, (d) Punching, (e) Crouching, and (f) Defensive Pose. 

large dataset ( _DCMU_ )—while highly diverse—contains many motions well beyond the robot’s capabilities, introducing detrimental noise. The _D_ 250 subset thus provides the best balance between feasible lower-body motions and diverse upper-body actions, enabling our policy to learn robust and expressive whole-body control. 

## _F. Ablation on Policy Training_ 

We conduct ablation studies on our policy design to highlight the effectiveness of both (i) the history length for the student policy and (ii) the teacher–student (DAgger) distillation. 

_a) History length.:_ We test student policies trained with different history lengths in Table XI (a). When no extra history is used, the policy struggles to learn effectively. Among the non-zero history lengths, most policies perform similarly while the history length of 10 yields the best results, which is used by us in the main experiments. Longer history lengths increase the difficulty of fitting the privileged information, ultimately reducing tracking performance. 

_b) Teacher–student distillation.:_ Table XI (b) shows that removing DAgger-style distillation severely degrades performance. Without privileged velocity guidance, the student policy must learn velocity tracking directly from raw observations, making it harder to track fast or dynamic motions accurately. 

## _G. Distribution-Guided Threshold Selection_ 

To choose filtering thresholds in a principled manner, we first analyze the error distribution of the base policy across the entire dataset. Figure 8 presents the empirical cumulative distribution of _e_ ( _s_ ), with the x-axis indicating the percentile 

of motion sequences (from lowest to highest error) and the y-axis displaying the corresponding error value. 

We derive thresholds directly from the empirical distribution, ensuring a data-driven rather than arbitrary cutoff. Smaller thresholds yield mostly lower-body motions with limited dynamics, while gradually increasing the threshold admits more dynamic behaviors. Higher thresholds include samples with excessive errors that could degrade policy learning. Consequently, we select _τ_ = 0 _._ 075 _,_ 0 _._ 10 _,_ 0 _._ 125 _,_ 0 _._ 15 _,_ 0 _._ 175 to filter the dataset into subsets of varying feasibility and diversity. This data-driven approach aligns with our **feasibilitydiversity principle** , yielding balanced subsets that support robust policy learning. 

## _H. Real-world Results Visualization_ 

Figure 7 illustrates how ExBody2 successfully replicates various motions in both simulation and real-world settings. We align each frame’s pose from (i) the reference SMPL animation, (ii) our simulated humanoid robot, and (iii) the real robot deployment. These snapshots confirm that our learned policy retains high fidelity to the target motion, including lower-body poses critical for balance. Additional results can be viewed in the supplementary video. 

One key advantage of ExBody2 is its flexibility in handling multiple motion sources. In the main text, we focus primarily on motion capture data (i.e., offline datasets). Below, we highlight two other sources— _Real-time Whole-body Mimic_ (RGBbased) and _Motion Synthesis_ (latent generative model)—that can drive ExBody2 for more interactive and long-horizon tasks. Figure 6 visually summarizes these capabilities alongside possible VR or IMU-based streams. 

|**Method**|_E_vel _↓_|_E_mpkpe _↓_|_E_<sup>upper</sup><br>mpkpe <sup>_↓_</sup>|_E_<sup>lower</sup><br>mpkpe <sup>_↓_</sup>|_E_mpjpe _↓_|_E_<sup>upper</sup><br>mpjpe <sup>_↓_</sup>|_E_<sup>lower</sup><br>mpjpe <sup>_↓_</sup>|
|---|---|---|---|---|---|---|---|
|**(a) History Length Ablatio**|**n**|||||||
|Exbody2-History10 (Ours)|0.2930|**0.1000**|0.0960|**0.1040**|**0.1079**|**0.0953**|**0.1253**|
|Exbody2-History0|0.4151|0.1047|0.1010|0.1081|0.1119|0.0986|0.1303|
|Exbody2-History25|0.2950|0.1032|0.0984|0.1078|0.1128|0.0965|0.1351|
|Exbody2-History50|**0.2648**|0.1004|**0.0956**|0.1051|0.1114|0.0967|0.1317|
|Exbody2-History100|0.3242|0.1063|0.1001|0.1122|0.1225|0.1050|0.1466|
|**(b) DAgger Ablation**||||||||
|Exbody2(Ours)|**0.2930**|**0.1000**|**0.0960**|**0.1040**|**0.1079**|**0.0953**|**0.1253**|
|Exbody2-w/o-DAgger|0.4195|0.1150|0.1106|0.1198|0.1496|0.1416|0.1607|


**TABLE XI:** Self Ablation Study: Evaluation of different configurations of our method on dataset _DCMU_ . The table is divided into two parts: (a) History Length Ablation and (b) DAgger Ablation. 

## _I. Real-time Whole-body Mimic (RGB Input)_ 

We implement a real-time tracking pipeline that uses only _monocular RGB input_ to mimic human movements. Our system first applies the HybrIK algorithm [30] to extract 3D human poses from each image frame. We then retarget this sequence of poses to the robot’s kinematic structure and feed it into the ExBody2 whole-body policy. Because our policy is trained to be robust to partial or noisy signals, it can accommodate real-time streaming of 3D keypoints and still maintain stable lower-body tracking. Figure 6 (b) demonstrates a user controlling the robot to lift and carry an object, showcasing responsive teleoperation. 

Relying on monocular pose estimates is more lightweight than requiring a full-body Mocap or multi-camera setup. Although the 3D pose can be less accurate than multi-view solutions, our control policy’s robust design helps it remain stable even under potential keypoint noise. 

## _J. Motion Synthesis for Extended Behaviors_ 

We further incorporate a _Conditional Variational Autoencoder (CVAE)_ to generate new motion segments based on a short sequence of past motions, as Figure 6 (c) illustrated. During inference, each latent code _z_ is sampled (or set to the prior mean) to produce new motion trajectories that seamlessly continue from the current pose. Unlike naive random sampling, the CVAE ensures continuity by conditioning on past pose context and penalizing abrupt transitions with a smoothness loss. 

_a) Training details.:_ The CVAE is trained on a broad set of humanoid motion clips, optimizing a reconstruction loss plus KL-divergence for the latent space. We also add a small penalty for high-frequency velocity changes, improving the realism of the generated motions. 


**Fig. 8:** Empirical CDF of the base policy’s error metric _e_ ( _s_ ) on the entire _D_ CMU dataset. The horizontal axis indicates the percentile of motion sequences from 0% (lowest error) to 100% (highest error), while the vertical axis shows _e_ ( _s_ ). We overlay dashed horizontal lines at key thresholds ( _τ_ = 0 _._ 075 _,_ 0 _._ 10 _,_ 0 _._ 125 _,_ 0 _._ 15 _,_ 0 _._ 175) to illustrate how we systematically determine feasible versus unfeasible motions based on the empirical distribution. 

_b) Integration with ExBody2.:_ The generated motion frames are retargeted in exactly the same way as a regular Mocap clip, so the policy sees no difference. This allows the robot to perform extended, varied sequences—e.g., spontaneously transitioning from walking to an upper-body gesture—without needing to rely on a fixed database of motion capture clips. 

