---
title: "ExtremControl: Low-Latency Humanoid Teleoperation with Scaled Velocity Feedforward"
date: "2026-02-11"
authors: "Ziyan Xiong; Lixing Fang; Junyun Huang; Kashu Yamazaki; Hao Zhang; Chuang Gan"
url: https://arxiv.org/abs/2602.11321
pdf: https://arxiv.org/pdf/2602.11321
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.11321)** / [論文ページ](https://arxiv.org/abs/2602.11321)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **ExtremControl: Low-Latency Humanoid Teleoperation with Scaled Velocity Feedforward** 

**Ziyan Xiong**<sup>1</sup><sup>_∗†_</sup> **Lixing Fang**<sup>1</sup><sup>_∗_</sup> **Junyun Huang**<sup>1</sup><sup>_∗_</sup> **Kashu Yamazaki**<sup>2</sup> **Hao Zhang**<sup>1</sup> **Chuang Gan**<sup>1</sup> 

1University of Massachusetts Amherst 2Carnegie Mellon University 

> _∗_ Equal contribution _†_ Corresponding author: ziyanxiong@umass.edu 


Figure 1: Unitree G1 demonstrates a diverse set of loco-manipulation tasks under teleoperation: (a) returning a ping-pong ball from varying positions; (b) balancing a ping-pong ball on a paddle through rapid orientation adjustments; (c) juggling a ping-pong ball; (d) catching a frisbee while moving; (e) catching thrown objects using a handheld basket while in motion; and (f) cooperatively lifting a box. Tasks (a-e) are performed using an optical MoCap system to achieve lower latency, while task (f) is operated using a VR system. 

**Abstract:** Building a low-latency humanoid teleoperation system is essential for collecting diverse reactive and dynamic demonstrations. However, end-to-end latencies in existing approaches consistently hover around 200 ms, roughly equal to human reaction time, that severely limits responsiveness and prevents tasks requiring rapid feedback. We identify position-only PD control as the root cause of this latency floor and propose _ExtremControl_ , a low-latency whole-body control framework that: (1) incorporates scaled velocity feedforward in low-level control, reducing tracking delay by approximately 70 ms with a provably optimal feedforward ratio; (2) operates directly on SE(3) poses of selected rigid links, primarily humanoid extremities, to avoid joint-space retargeting in the control loop. To minimize retargeting time, we derive a closed-form Cartesian-space mapping that uses a single anthropomorphic calibration step to translate human motion into humanoid link targets, accommodating operators with varying body proportions. Furthermore, we provide a theoretical framework for selecting control hyperparameters, and validate the effectiveness of velocity feedforward control in the reinforcement learning for locomotion setting through experiments in both simulation and the real world. Building on _ExtremControl_ , we implement a teleoperation system supporting both optical motion capture and VR-based tracking, achieving end-to-end latency as low as 50 ms — well beneath the threshold at which system delay adds a full human reaction cycle to the control loop. This enables a qualitatively new class of reactive behaviors, including ping-pong ball balancing, juggling, and real-time return, that are beyond the capability of existing teleoperation systems. Project page: https://extremcontrol.github.io/. 

**Keywords:** Humanoid, Teleoperation, Control, Retargeting 

10th Conference on Robot Learning (CoRL 2026), Austin TX, USA. 

|**Teleoperation System**|**Control Interface**|**Wrist Control**|**Foot Control**|**Task-Space Retargeting**|**End-to-End Latency**|
|---|---|---|---|---|---|
|HOMIE [1]|Exoskeleton|✓|_×_|✓|_∼_454ms|
|HumanPlus [2]|RGB Camera|✓|✓|_×_|_∼_340ms|
|OmniH2O [3]|VR|✓|_×_|✓|_∼_**185 ms**|
|H2O [4]|RGB Camera|_×_|✓|_×_|_∼_373ms|
|AMO [5]|VR|✓|_×_|_×_|_∼_380ms|
|CLONE [6]|VR|✓|_×_|✓|_∼_**178 ms**|
|AMS [7]|MoCap|_×_|✓|_×_|_∼_201ms|
|TWIST [8]|MoCap|_×_|✓|_×_|_>_ 700ms|
|TWIST2 [9]|VR|✓|✓|_×_|_∼_234ms|
|SONIC [10] WBC|RGB Camera, VR|✓|✓|_×_|_∼_427ms<sup>a</sup><br>|
|SONIC [10] Keypoint|VR|✓|_×_|✓|—<sup>b</sup>|
|ExtremControl (Ours)|VR, MoCap|✓|✓|✓|_∼_**54 ms**|


> a Measured under VR setting. RGB camera will introduce 0.1 s additional latency. 

> b Latency not measurable as the teleoperator is not visible in the released video. 

Table 1: Existing humanoid teleoperation systems with latencies estimated by optical flow on released videos. 

## **1 Introduction** 

Humanoid robots have long attracted significant attention in the robotics community due to their human-like morphology and kinematic structure. Because modern environments, tools, and tasks are predominantly designed around human bodies, humanoids represent a natural embodiment for general-purpose robotic systems capable of operating in unstructured, human-centric settings. Moreover, the close correspondence between humanoid and human morphology enables the direct exploitation of large-scale human motion and skill datasets, alleviating the reliance on expensive and limited robot-collected data. However, these same properties that make humanoids appealing also pose substantial challenges for traditional control frameworks. In particular, the high-dimensional state and action spaces, underactuated floating-base dynamics, intermittent contacts, and frequent hybrid mode transitions inherent to humanoid locomotion and manipulation render classical modelbased control approaches difficult to scale and deploy robustly in practice. Accurate modeling, realtime optimization, and contact-consistent planning become increasingly intractable as task complexity grows, motivating the exploration of alternative control paradigms better suited to the complexity of humanoid systems. 

With the advent of large-scale parallel simulation, reinforcement learning has become a dominant paradigm for humanoid locomotion and whole-body control, and the design of control interfaces has undergone a clear evolution over time. Inheriting from quadruped locomotion, early approaches relied on explicit Cartesian-space objectives [3, 4] or command-based interfaces [11, 12]. Subsequently, influenced by advances in physics-based character animation [13, 14], many methods shifted toward dense joint-space pose supervision adopted from the human model, enabling humanoids to reproduce expressive and highly dynamic motions derived from human demonstrations [2, 15]. More recent efforts further narrowed the control objective to optimization of selected reference trajectories, achieving high-fidelity motion reproduction at the cost of generalization across tasks and behaviors [16, 17, 18, 19]. In parallel, teleoperation-oriented methods introduce intermediate representations to flexibly map human motion to humanoid embodiments [5, 7, 8, 9]. These approaches first compute target poses for a set of robot links and then solve inverse kinematics to obtain joint configurations that realize those poses. However, although policies are executed in joint space, the underlying optimization objective remains defined in terms of matching Cartesian link poses. 

A large portion of the literature on humanoid control focuses on teleoperation [1, 2, 3, 4, 5, 6, 7, 8, 9], as it provides an effective mechanism for collecting data to train general-purpose robotic intelligence. Because teleoperation operates in a human-in-the-loop closed-loop setting, system latency critically determines the operator’s ability to perform responsive tasks. Among the existing teleoperation systems listed in Tab. 1, we observe a striking consistency: **all existing humanoid teleoperation systems exhibit end-to-end latencies over 150 ms** , independent of the robot, retargeting strategy, or the length of future motion used [3, 6, 7, 9].<sup>1</sup> We identify position-only PD control as a 

> 1We estimate latencies by our proposed optical flow method on authors’ released videos. 

2 

common contributing factor to this latency floor: without a velocity feedforward term, the low-level controller introduces an inherent tracking delay that the learned policy cannot fully compensate for, particularly in the teleoperation setting where future reference is limited and rapid response is most critical. 

To address this problem, we introduce _ExtremControl_ , a humanoid whole-body control framework that: (1) incorporates a scaled velocity feedforward term for extremely responsive low-level actuation, supported by a whole-body impedance calibration that tightly couples simulation with realworld deployment and provides a principled basis for hyperparameter selection; and (2) utilizes a closed-form Cartesian-space mapping with one-shot anthropomorphic calibration to convert human motion to SE(3) poses of selected rigid links spanning all humanoid extremities, generalizing across operators of varying body proportions without requiring a human shape prior. The overall design aims to minimize system latency while preserving full whole-body control capability. 

The contributions of this work are fourfold. First, we present a theoretical framework for velocity feedforward control in the reinforcement learning for locomotion setting, deriving the relationship between the feedforward ratio _η_ and tracking delay, establishing a principled upper bound on _η_ to prevent discrete-time overshoot, and providing whole-body impedance calibration as a systematic procedure for PD gain selection; we validate this framework through experiments in both simulation and the real world. Second, we introduce Direct Extremity Control, a retargeting-free Cartesianspace mapping that achieves higher end-effector fidelity than full-body joint-space retargeting while requiring only a one-shot calibration and supporting operators of varying body proportions. Third, we propose an optical-flow-based latency estimation method that measures end-to-end teleoperation delay directly from video without requiring internal timestamps, enabling fair cross-system comparison from publicly released demonstrations. Finally, leveraging _ExtremControl_ , **we develop a humanoid teleoperation system achieving as low as 50 ms end-to-end latency** , well beneath the threshold at which system delay adds a full human reaction cycle to the control loop, thereby unlocking a qualitatively new class of reactive loco-manipulation tasks, including ping-pong ball balancing, juggling, and real-time return (Fig. 1), that lie beyond the reach of existing teleoperation systems. 

## **2 Related Work** 

**Reinforcement Learning for Locomotion** Reinforcement learning has become a dominant paradigm for learning agile locomotion policies, due to its ability to optimize high-dimensional control objectives directly from interaction. Early work demonstrated that model-free RL can produce robust locomotion behaviors in simulation and transfer them to real robots through domain randomization and privileged training signals [20, 21, 22, 23, 24, 25]. Subsequent studies improved robustness and versatility by introducing curriculum learning, command-conditioned policies [26, 27, 28, 29, 30, 31]. Hybrid approaches further combine trajectory optimization, modelbased priors, or analytical controllers with RL fine-tuning to enhance stability and tracking accuracy [32, 33, 34, 35]. Together, these works establish RL as a practical framework for locomotion across diverse tasks and robot embodiments. 

**Humanoid Whole-Body Control** Compared to quadrupeds, humanoid locomotion and locomanipulation involve high degrees of freedom, underactuated contacts, and complex whole-body coordination. Whole-body control (WBC) frameworks address these challenges by tracking jointspace or task-space objectives under full-body dynamics and contact constraints [27, 36, 37, 38, 39, 40]. Recent approaches integrate reinforcement learning with WBC, using motion capture and animation data to provide expressive reference motions [7, 10, 13, 14, 41, 42, 43, 44, 45, 46]. Humanoid teleoperation, which is a fundamental mechanism for large-scale data collection, fits naturally into this paradigm. Early methods specify Cartesian objectives for selected body links [1, 3, 6, 47, 48, 49] with control interfaces ranging from exoskeleton to single rgb camera; whereas recent approaches relied on full-body joint-space retargeting, incurring added latency [4, 8, 16, 50, 51, 52]. Overall, WBC serves as a unifying backbone for complex humanoid systems. 

3 

## **3 Method** 

### **3.1 Velocity Feedforward Control** 

**Whole-Body Impedance Calibration** To facilitate a principled design of joint-level PD controllers, we calibrate gains using a sequential, simulation-based procedure that estimates effective joint impedance under whole-body closed-loop control. For each joint, the derivative gain is temporarily set to zero and the proportional gain is sampled as _kp_<sup>(</sup><sup>_e_)</sup> _∼U_ (0 _._ 5 _kp,_ 1 _._ 5 _kp_ ) across parallel simulation environments _e ∈ E_ . Applying a small perturbation and measuring the induced oscillation period _P_<sup>(</sup><sup>_e_)</sup> , the effective joint impedance is estimated as (see Sec. A.1 for proof) 


The average effective joint impedance _M_ eff over different environments is then used to set the PD gains given a target natural frequency _ωn_ and damping ratio _ζ_ : 


This procedure iterates over all joints from distal to proximal, yielding dynamically consistent gains that serve as a stable and well-scaled initialization for downstream control and learning. 


Prior work has shown that position targets outperform velocity targets when used independently as policy actions [53]. Due to safety considerations, position-based action spaces have become the predominant choice in reinforcement learning for locomotion. Our method retains position targets as policy outputs while approximating velocity targets through finite differences of consecutive policy actions as 


This allows _η_ to be tuned as a continuous knob between pure position control ( _η_ = 0) and full velocity feedforward ( _η_ = 1). The following two theorems characterize the effects of _η_ on tracking delay and control stability, providing a principled basis for selecting the velocity feedforward ratio (proofs in Sec. A). 

**Theorem 1.** Under whole-body impedance calibration with critical damping _ζ_ = 1, the tracking delay _ℓ_ control for a sinusoidal target _q_<sup>_∗_</sup> = _A_ sin( _ωt_ ) satisfies 


When _η <_ 1, one might expect the policy to implicitly compensate for this delay by learning to output joint positions that are offset from the true targets, effectively anticipating future states. However, we will show in Sec. 4 that such learned compensation cannot fully eliminate the delay in the teleoperation setting where responsiveness is required. 

**Theorem 2.** Under zero-order hold with control interval ∆ _t_ , to prevent overshoot caused by excess acceleration within a single control interval, the feedforward ratio must satisfy 


The standard formulation _η_ = 1 is therefore suboptimal, and the admissible range of _η_ shrinks with higher natural frequency _ωn_ or longer control interval ∆ _t_ . 

### **3.2 Direct Extremity Control** 

4 

**Tracking Objectives** The choice of tracking objectives fundamentally determines the feasiArm length bility and robustness of a teleoperation system. Under the contact-sparse assumption that covShoulderposition ers most practical scenarios, we select six links of the Unitree G1, which are hands, feet, torso, Pelvis and pelvis, yielding **T**<sup>_r_</sup> _∈_ SE(3)<sup>6</sup> . These six height links are sufficient to convey the operator’s intent for manipulation, locomotion, and global (a) VR (b) MoCap (c) Robot posture, while remaining minimal enough to avoid over-constraining the system. Although Figure 2: **Tracking objectives** for humans and huthe Cartesian pose of a hand does not uniquely manoids under VR and MoCap settings. determine the arm’s joint configuration, joint limits, self-collision constraints, and temporal continuity strongly restrict the feasible solution space. We further demonstrate in Sec. 4 that extremity poses alone achieve performance comparable to adding retargeted joint configurations, while greatly surpassing retargeted joint configurations only. 

Figure 2: **Tracking objectives** for humans and humanoids under VR and MoCap settings. 

**Mapping Design** We define a Cartesian-space mapping _M_ : SE(3)<sup>6</sup> _→_ SE(3)<sup>6</sup> following three principles: (i) _anthropomorphic compensation_ : explicitly handling differences in body proportions; (ii) _mathematical consistency_ : reproducing identical poses at calibration; and (iii) _real-time efficiency_ : avoiding multi-link or joint-space optimization. 

**One-Shot Calibration** At initialization, the human stands in a neutral pose as shown in Fig. 2. Per-link rotational offsets are estimated to resolve coordinate-system differences and held fixed at runtime. A small set of anthropomorphic measurements is extracted from **T**<sup>_h_</sup> : pelvis height _z_ pelvis<sup>_h_,shoulderpositionsinthepelvisframe</sup><sup>**p**</sup> _k_<sup>_h_</sup> ~~s~~ houlder<sup>,andarmlengths</sup><sup>_l_</sup> _k_<sup>_h_</sup> ~~a~~ rm<sup>foreachside</sup> _k ∈{_ left _,_ right _}_ . Corresponding humanoid parameters _{z_ pelvis<sup>_r,_</sup><sup>**p**</sup> _k_<sup>_r_</sup> ~~s~~ houlder<sup>_, l_</sup> _k_<sup>_r_</sup> ~~a~~ rm<sup>_}_arereaddirectly</sup> from the kinematic model. A fixed foot offset _δk_ ~~f~~ oot<sup>=</sup><sup>**p**</sup><sup>_r_</sup> _k_ ~~f~~ oot<sup>_−_(</sup><sup>_z_</sup> pelvis<sup>_r/z_</sup> pelvis<sup>_h_)</sup><sup>_·_</sup><sup>**p**</sup> _k_<sup>_h_</sup> ~~f~~ oot<sup>isalso</sup> recorded. At runtime, humanoid targets **T**<sup>_r_</sup> = _M_ ( **T**<sup>_h_</sup> ) are computed as follows. 

**Pelvis and feet** are height-ratio scaled: 


**Torso** position is rigidly attached to the pelvis via the fixed kinematic offset **p** diff: 


**Hands** are mapped by aligning shoulder positions and scaling arm lengths in the torso frame: 


The entire mapping consists solely of rigid transformations and is computed in closed form making it fully feedforward and parallelizable. 

**Policy Learning** We adopt an RL+BC+RL three-stage framework to learn a deployable wholebody tracking policy. In the first stage, we train a teacher policy _π_ teacher via PPO [54] with privileged observations, including retargeted joint configurations from GMR [50], global pose discrepancies, domain randomization parameters, and foot contact forces over a long future horizon of 32 frames. In the second stage, we distill _π_ teacher into a student policy _π_ student via DAgger [55], removing all privileged observations (including the retargeted joint configurations) and reducing the future horizon to a single frame; this inevitably introduces a performance gap as the student loses access to the joint-space retargeting signal. The third stage recovers this capability by fine-tuning _π_ student with PPO over a large, diverse motion dataset to obtain _π_ teleop, where online exploration is stabilized by freezing the actor for the first 200 iterations and annealing the entropy coefficient toward zero. Please refer to Sec. C for policy learning details. 

5 


Figure 3: **Optical flow visualization of hand movements.** Upward and downward optical flow extracted from video clips are visualized in the two rightmost images. Separate tracking regions are defined for the human and robot hands to isolate their respective motion. The average optical flow magnitude within each region serves as a proxy for hand velocity, as it is approximately proportional to the hand’s image-plane speed. 

## **4 Evaluation** 

To measure end-to-end latency without requiring internal timestamps, we develop a video-based optical flow method that captures externally observable cumulative latency across all system components. As illustrated in Fig. 3, we define tracking regions on both the human operator and the robot, compute dense optical flow [56] between consecutive frames, and project averaged flow vectors onto a predefined motion axis to yield a one-dimensional motion signal per region. A deliberate reciprocating hand motion produces a quasi-periodic signal for robust temporal alignment, and latency is estimated as the temporal offset that maximizes waveform alignment between the two signals. The same procedure is applied to public video demonstrations of third-party systems to enable fair comparison. Under this metric, _ExtremControl_ achieves 54 ms end-to-end latency under the wired MoCap setup and 64 ms under the wireless VR setup, outperforming all baselines as shown in Tab. 1 and Fig. 4. 


Figure 4: **Human and robot optical flow trajectories** , along with the corresponding system latency estimates derived from selected video clips of exsisting systems. 

The correctness of **whole-body impedance calibration** , theoretical results of **velocity feedforward control** , and **end-to-end latency estimation** are validated through experiments in both simulation and real world. These experiment results as well as all experiment setups are detailed in Sec. B. Further experiments address the following questions: 

### **Q1: How does Velocity Feedforward Control affect the policy performance?** 

From a control perspective, any desired joint torque _τ_<sup>_∗_</sup> ( _t_ ) can theoretically be achieved under different velocity feedforward ratios _η_ by policy predicted target joint positions _qη_<sup>_∗_(</sup><sup>_t_) that satisfy that satisfy</sup> 

_η_<sup>_∗_(</sup><sup>_t_) that satisfy that satisfy</sup> 


However, this equivalence does not necessarily hold from a reinforcement learning perspective. To encourage smooth actions for sim-to-real transfer, locomotion policies are commonly trained with a penalty on consecutive action differences, _|at −at−_ 1 _|_ . Although different values of _η_ can achieve the same torque, they generally require different action sequences and therefore incur different smoothness penalties. Consequently, _η_ changes the effective optimization objective and can lead to different learned behavior, even when all reward terms and their weights are kept identical. 

To systematically investigate the effect of _η_ on control performance, we consider two settings: (1) **teleoperation** , where the policy receives only the current reference frame and must respond immediately without access to future motion; and (2) **motion tracking** , where the policy is conditioned on 32 future reference frames spanning 0.64 s, allowing it to anticipate upcoming motion. Within each setting, we independently train policies with different values of _η_ , while keeping all other configu- 

6 

rations identical, including the reward functions and their weights. During evaluation, each policy uses the same _η_ as in its training. We train each policy with five different random seeds. 


Fig. 5 illustrates the control characteristics of policies trained with different velocity feedforward ratios. Notably, in both teleoperation and motion tracking settings, the DoF acceleration per unit action rate (equivalently, torque per unit action rate) increases approximately linearly with _η_ , indicating greater control responsiveness to changes in policy actions. Under a fixed action rate penalty _|at − at−_ 1 _|_<sup>2</sup> , this increased control responsiveness leads to higher measured joint accelerations, as shown in upper-left panel of Fig. 5. 

Figure 5: **Analysis of control characteristics under different velocity feedforward ratios.** We train motion tracking and teleoperation policies with varying velocity feedforward ratios and evaluate their control behavior across six metrics. 

In **teleoperation** setting, as shown in the ratios and evaluate their control behavior across six metrics. middle column of Fig. 5, both average action rate and action acceleration consistently decrease as _η_ increases, indicating progressively smoother policy outputs. This improved control responsiveness also helps reduce tracking latency under the same action rate penalty, as demonstrated in Fig. 6. In contrast, in **motion tracking** setting, increasing _η_ initially reduces both the action rate and action acceleration. However, excessively large _η_ leads to overly aggressive joint responses and potential overshooting, requiring the policy to make frequent corrective adjustments. As a result, the action acceleration begins to increase first, followed by the action rate, revealing that access to future motion references reduces the need for a large velocity feedforward ratio. 

To investigate action interpretability, we measure the cosine similarity between policy actions and measured joint positions (right column of Fig. 5). We consider both elbow and knee joints to capture non-contact and contact-rich settings, respectively. Across both teleoperation and motion tracking settings, cosine similarity consistently increases with the velocity feedforward ratio _η_ , indicating that policy actions become more closely aligned with the actual joint positions. 

Fig. 6 illustrates the tracking performance of policies with different velocity feedforward ratios, measured by tracking delay and tracking error, in relation to the average measured DoF acceleration. Tracking delay is estimated as the temporal offset that best aligns the reference and measured end-effector trajectories (hand trajectories in our setting). In **motion tracking** setting, the tracking delay remains approximately constant at 20 ms (top row), corresponding to a single policy action interval, regardless of the velocity feedforward ratio _η_ . This suggests that access to future motion references allows the policy to effectively compensate for low-level tracking delays, leaving little additional benefit from velocity feedforward in terms of latency reduction. In contrast, in **teleoperation** setting, where future motion is unavailable, tracking delay decreases approximately linearly as _η_ increases, demonstrating the effectiveness of velocity feedforward in improving control responsiveness without future motion information. 

Tracking error consistently increases with the velocity feedforward ratio _η_ in both settings. However, tracking error exhibits a stronger linear correlation with the mea- 


Figure 6: **Policy tracking performance with respect to different velocity feedforward ratio.** Each dot represents a policy. 

7 

sured average DoF acceleration, as indicated by a higher regression _R_<sup>2</sup> . As discussed earlier, the average DoF acceleration increases along with _η_ when reward terms are kept identical. 

We illustrate the tracking delay of velocity feedforward control, realworld teleoperation system, and policy rollout in simulation in Fig. 7, under _ωn_ = 10 rad/s, where the dashed line represents the predicted result from Theorem 1. Two key observations emerge: (1) the low-level control delay is accurately predicted by Theorem 1 at low _η_ , with deviations at high _η_ consistent with the discrete-time overshoot described in Theorem 2; and (2) the policy is able to compensate for low-level control delay up to _η_ = 0 _._ 9, where policy delay matches low-level control delay. Together with the instability observed at _ωn_ = 15 rad/s, these results suggest that 50 ms represents a practical lower bound on achievable end-to-end teleoperation latency under our current hardware, and that _ExtremControl_ operates at this limit. 


Figure 7: Different tracking delays with respect to velocity feedforward ratios. 

During real-world deployment, we use PD gains _kp_ and _kd_ computed from Eq. 2, with the position target _qt_<sup>_∗_=</sup><sup>_k · at_+</sup><sup>_c_,where</sup><sup>_k_and</sup><sup>_c_arefixedactionscalingandoffsetparameters,respectively.</sup> The velocity target is defined as _q_ ˙ _t_<sup>_∗_=</sup><sup>_η ·_(</sup><sup>_q_</sup> _t_<sup>_∗−q_</sup> _t_<sup>_∗_</sup> _−_ 1<sup>)</sup><sup>_/_∆</sup><sup>_t_.Compared to existing systems,</sup><sup>**the only**</sup> **modification is replacing the zero velocity target with scaled velocity feedforward.** 

### **Q2: How does Direct Extremity Control affect the teleoperation system?** 

The closed-form Cartesian mapping incurs a fixed computational cost of approximately 0.3 ms regardless of input motion, whereas joint-space retargeting via inverse kinematics introduces variable and potentially unbounded computation time due to the iterative nature of IK solvers. 

Benefiting from the one-shot calibration, Direct Extremity Control requires no human shape prior for retargeting, which is particularly advantageous in real-world deployment, because operators may vary significantly in heights, limb lengths, etc. To evaluate retargeting quality, we compare our method against GMR [50] using five motion capture sequences collected from two operators, as well as ACCAD dataset, which contains short motion clips from 20 subjects. 

Direct Extremity Control achieves higher Pearson correlation in retargeted hand position relative to the original motion compared to GMR [50] (Tab. 2), indicating more faithful preservation of the operator’s intended motion. We attribute this to GMR being over-constrained by 14 links, which reduces retargeting flexibility. This is particularly consequential for manipulation tasks, where end-effector accuracy directly determines whether contacts and grasps are successfully reproduced. The asymmetry between _x_ and _y_ correlations reflects a directional bias in the MoCap collected dataset, as all sequences were recorded with the teleoperator facing the x-axis. The inverse 

|Alignment|GMR|**Ours**|
|---|---|---|
|_Rx_|0.78_±_0.21|**0.91**_±_**0.11**|
|_Ry_|0.62_±_0.24|**0.76**_±_**0.19**|
|_Rz_|0.20_±_0.26|**0.41**_±_**0.15**|


Table 2: **Pearson correlation between hand trajectories before and after retargeting** , averaged across our collected MoCap dataset and ACCAD dataset, weighted by the number of samples in each dataset. 

kinematics process after cartesian mapping in GMR introduces 72 mm and 0.025 rad error for hands and 24 mm and 0.044 rad error for the feet, which already exceed the policy tracking error as illustrated in Tab. 3. Further more, GMR persists 95.2% of still-foot frames defined as foot velocity under 0.25 m/s, while GMR persists 100%. 

Although reducing observations inevitably degrades performance, selecting the right observations can substantially mitigate this degradation. Regarding end-effector tracking accuracy, which is critical in loco-manipulation tasks, ob- 

|Observation|**T**<sup>_r_</sup>|(**T**<sup>_r_</sup>_, q_<sup>_∗_</sup>)|_q_<sup>_∗_</sup>|
|---|---|---|---|
|Tracking Pos Error (mm)|49_±_7|**43**_±_**8**|105_±_23|
|Tracking Rot Error (rad)|0.19_±_0.03|**0.17**_±_**0.02**|0.48_±_0.07|


Table 3: Policy tracking errors in simulation, _η_ = 0 _._ 9. 

serving selected link poses alone is inferior to providing both link poses and retargeted joint configurations, yet significantly outperforms observing retargeted joint configurations alone. All policies evaluated in Tab. 3 are trained with the same mixed dataset of Cartesian-space mapped motions from our collected dataset with inverse kinematics results and GMR retargeted public motion datasets. 

8 

### **Q3: Does end-to-end latency play a critical role in real-world data collection?** 

Yes, and this holds consistently across all closed-loop tasks. Existing teleoperation systems often introduce delays comparable to the typical human reaction time of approximately 200 ms, effectively doubling the response time of the human-in-the-loop system. In contrast, _ExtremControl_ achieves an end-to-end latency of only 54 ms under the optical MoCap setting, substantially reducing the additional delay imposed on the operator and enabling reaction-sensitive tasks such as the pingpong return demonstrated in Fig. 1. To evaluate teleoperation performance under varying systemlevel latencies, we introduce an artificial delay by adding a FIFO queue to the motion observations received by the policy. We apply delays of 0, 2, 5, and 8 frames, corresponding to approximate overall latencies of 50 ms, 100 ms, 150 ms, and 200 ms, respectively. 

|As shown in Tab.4, increasing latency||<br>|
|---|---|---|
|<br>|Latency<br>Ping-pong Return_↑_|Ping-pong Balance_↑_<br>Cube Stack_↓_|
|leads to consistent performance degra-|<br>|<br>|
|i  ll kll|_∼_50ms<br>**80%**|**7.3**_±_**3.1 s**<br>**7.6**_±_**2.0 s**|
|daton across a tass. For cosed-oop<br>iii k h ff i|_∼_100ms<br>60%|3.6_±_1.7 s<br>8.3_±_2.7 s|
|reacton-senstve tass, te eect s se-<br>|_∼_150ms<br>30%|1.3_±_0.4 s<br>9.5_±_2.1 s|
|vere: ping-pong return rate drops from|_∼_200ms<br>20%|1.5_±_0.6 s<br>10.1_±_3_._8s|
|80% to 20% and ball balance duration|||
|from 7.3 s to 1.5 s as latency increases|Table 4: Performance of_Extre_|_mControl_over 10 trials per task.|
|from 50 ms to 200 ms, as delayed visual fe<br>time-critical tasks such as cube stacking,|edback causes corrective ac<br>  the effect is milder but still|tions to arrive too late. For less<br>measurable, with completion|
|time increasing from 7.6 s to 10.1 s. The<br>trol is fundamentally bottlenecked by tra|se results confirm that hum<br>nsmission latency, particula|an-in-the-loop humanoid con-<br>rly for tasks demanding rapid|
|closed-loop corrections.|||


## **5 Conclusion and Limitations** 

In this work, we present _ExtremControl_ , a low-latency humanoid teleoperation framework combining scaled velocity feedforward with direct extremity control. Our key findings are: 

- _ExtremControl_ achieves end-to-end latencies of 54 ms and 64 ms under MoCap and VR settings, 

- respectively, enabling highly dynamic and reaction-sensitive tasks. Controlled latency experiments further demonstrate the critical importance of low latency for closed-loop teleoperation. 

- Velocity feedforward plays a crucial role in reducing policy tracking delay in teleoperation settings where future motion references are unavailable. It also promotes smoother policy actions by increasing the joint acceleration and torque generated per unit action rate. 

- Direct extremity control eliminates the need for joint-space retargeting during deployment, avoiding its computational overhead and additional errors introduced by inverse kinematics, at the cost of only a small increase in policy tracking error. 

Despite these advances, several limitations remain. First, the Unitree G1’s seven DoFs per arm introduce inverse kinematics ambiguity, which, combined with direct extremity pose mapping and the distribution of wrist and elbow joints, can lead to unnatural arm poses. Second, while our work primarily targets control-level responsiveness, lower-body latency remains governed by policy-level center-of-mass regulation, such as distinguishing walking initiation from simply lifting a foot. Finally, our framework assumes limited environmental contact and focuses on sparse extremity tracking. Extending it to dense whole-body contact scenarios, such as climbing or crawling, may require additional contact-aware objectives and more sophisticated motion representations. 

### **Acknowledgments** 

This work was supported by NSF IIS-2441250, NSF IIS-2404386, MURI N000142412748, and Amazon’s gift funding. We thank our colleagues for their valuable discussions, insightful feedback, and support throughout this project. The first author would also like to thank his cats, Cookie and Mochi, for their love and companionship. 

9 

## **References** 

- [1] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang. HOMIE: Humanoid Loco-Manipulation with Isomorphic Exoskeleton Cockpit. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. doi:10.15607/RSS.2025.XXI.070. 

- [2] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn. Humanplus: Humanoid shadowing and imitation from humans. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [3] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 

- [4] T. He, Z. Luo, W. Xiao, C. Zhang, K. Kitani, C. Liu, and G. Shi. Learning human-to-humanoid real-time whole-body teleoperation. _arXiv preprint arXiv:2403.04436_ , 2024. 

- [5] J. Li, X. Cheng, T. Huang, S. Yang, R.-Z. Qiu, and X. Wang. AMO: Adaptive Motion Optimization for Hyper-Dexterous Humanoid Whole-Body Control. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. doi:10.15607/RSS.2025.XXI.061. 

- [6] Y. Li, Y. Lin, J. Cui, T. Liu, W. Liang, Y. Zhu, and S. Huang. Clone: Closed-loop wholebody humanoid teleoperation for long-horizon tasks. In J. Lim, S. Song, and H.-W. Park, editors, _Proceedings of The 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pages 4493–4505. PMLR, 27–30 Sep 2025. URL https: //proceedings.mlr.press/v305/li25h.html. 

- [7] Y. Pan, R. Qiao, L. Chen, K. Chitta, L. Pan, H. Mai, Q. Bu, H. Zhao, C. Zheng, P. Luo, and H. Li. Agility meets stability: Versatile humanoid control with heterogeneous data, 2025. URL https://arxiv.org/abs/2511.17373. 

- [8] Y. Ze, Z. Chen, J. P. Araujo, Z. ang Cao, X. B. Peng, J. Wu, and K. Liu. TWIST: Teleoperated whole-body imitation system. In _9th Annual Conference on Robot Learning_ , 2025. URL https://openreview.net/forum?id=htgNQHa6Ta. 

- [9] Y. Ze, S. Zhao, W. Wang, A. Kanazawa, R. Duan, P. Abbeel, G. Shi, J. Wu, and C. K. Liu. Twist2: Scalable, portable, and holistic humanoid data collection system, 2025. URL https: //arxiv.org/abs/2511.02832. 

- [10] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Casta˜neda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, X. Da, R. Ding, C. Hogg, L. Song, E. Lim, E. Jeong, T. He, H. Xue, W. Xiao, Z. Wang, S. Yuen, J. Kautz, Y. Chang, U. Iqbal, L. J. Fan, and Y. Zhu. Sonic: Supersizing motion tracking for natural humanoid whole-body control, 2025. URL https://arxiv.org/abs/2511. 07820. 

- [11] C. Zhang, W. Xiao, T. He, and G. Shi. Wococo: Learning whole-body humanoid control with sequential contacts, 2024. 

- [12] Z. Zhuang, S. Yao, and H. Zhao. Humanoid parkour learning. In _8th Annual Conference on Robot Learning_ , 2024. URL https://openreview.net/forum?id=fs7ia3FqUM. 

- [13] Z. Luo, J. Cao, A. Winkler, K. Kitani, and W. Xu. Perpetual humanoid control for real-time simulated avatars. In _2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 10861–10870, 2023. doi:10.1109/ICCV51070.2023.01000. 

- [14] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa. Amp: adversarial motion priors for stylized physics-based character control. _ACM Trans. Graph._ , 40(4), July 2021. ISSN 07300301. doi:10.1145/3450626.3459670. URL https://doi.org/10.1145/3450626. 3459670. 

10 

- [15] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, J. Kautz, C. Liu, G. Shi, X. Wang, L. J. Fan, and Y. Zhu. Hover: Versatile neural whole-body controller for humanoid robots. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9989–9996, 2025. doi:10.1109/ICRA55743.2025.11128549. 

- [16] A. Allshire, H. Choi, J. Zhang, D. McAllister, A. Zhang, C. M. Kim, T. Darrell, P. Abbeel, J. Malik, and A. Kanazawa. Visual imitation enables contextual humanoid control. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- [17] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang. Gmt: General motion tracking for humanoid whole-body control, 2025. URL https://arxiv.org/abs/2506.14770. 

- [18] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbabu, C. Pan, Z. Yi, G. Qu, K. Kitani, J. K. Hodgins, L. Fan, Y. Zhu, C. Liu, and G. Shi. ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. doi:10. 15607/RSS.2025.XXI.066. 

- [19] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion, 2025. URL https: //arxiv.org/abs/2508.08241. 

- [20] J. Fu, K. Luo, and S. Levine. Learning robust rewards with adverserial inverse reinforcement learning. In _International Conference on Learning Representations_ , 2018. URL https: //openreview.net/forum?id=rkHywl-A-. 

- [21] A. Kumar, Z. Fu, D. Pathak, and J. Malik. Rma: Rapid motor adaptation for legged robots. 2021. 

- [22] N. Rudin, D. Hoeller, P. Reist, and M. Hutter. Learning to walk in minutes using massively parallel deep reinforcement learning. In A. Faust, D. Hsu, and G. Neumann, editors, _Proceedings of the 5th Conference on Robot Learning_ , volume 164 of _Proceedings of Machine Learning Research_ , pages 91–100. PMLR, 08–11 Nov 2022. URL https: //proceedings.mlr.press/v164/rudin22a.html. 

- [23] J. Tan, T. Zhang, E. Coumans, A. Iscen, Y. Bai, D. Hafner, S. Bohez, and V. Vanhoucke. Simto-real: Learning agile locomotion for quadruped robots. In _Proceedings of Robotics: Science and Systems_ , Pittsburgh, Pennsylvania, June 2018. doi:10.15607/RSS.2018.XIV.010. 

- [24] Z. Xiong, B. Chen, S. Huang, W.-W. Tu, Z. He, and Y. Gao. Mqe: Unleashing the power of interaction with multi-agent quadruped environment, 2024. 

- [25] L. Fang, Z. Xiong, S. Chen, Z. Dou, and C. Gan. Spot: Spatial perception-oriented longhorizon humanoid teleoperation, 2026. URL https://arxiv.org/abs/2609.07933. 

- [26] P. Chen, Y. Wang, C. Luo, W. Cai, and M. Zhao. Hifar: Multi-stage curriculum learning for high-dynamics humanoid fall recovery, 2025. URL https://arxiv.org/abs/2502. 20061. 

- [27] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang. Expressive Whole-Body Control for Humanoid Robots. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, July 2024. doi:10.15607/RSS.2024.XX.107. 

- [28] J. Hwangbo, J. Lee, A. Dosovitskiy, D. Bellicoso, V. Tsounis, V. Koltun, and M. Hutter. Learning agile and dynamic motor skills for legged robots. _Science Robotics_ , 4(26):eaau5872, 2019. doi:10.1126/scirobotics.aau5872. URL https://www.science.org/doi/abs/ 10.1126/scirobotics.aau5872. 

11 

- [29] G. B. Margolis and P. Agrawal. Walk these ways: Tuning robot control for generalization with multiplicity of behavior. In K. Liu, D. Kulic, and J. Ichnowski, editors, _Proceedings of The 6th Conference on Robot Learning_ , volume 205 of _Proceedings of Machine Learning Research_ , pages 22–31. PMLR, 14–18 Dec 2023. URL https://proceedings.mlr. press/v205/margolis23a.html. 

- [30] N. Rudin, D. Hoeller, P. Reist, and M. Hutter. Learning to walk in minutes using massively parallel deep reinforcement learning. In _5th Annual Conference on Robot Learning_ , 2021. URL https://openreview.net/forum?id=wK2fDDJ5VcF. 

- [31] Z. Zhuang, Z. Fu, J. Wang, C. Atkeson, S. Schwertfeger, C. Finn, and H. Zhao. Robot parkour learning. In _Conference on Robot Learning (CoRL)_ , 2023. 

- [32] T. Johannink, S. Bahl, A. Nair, J. Luo, A. Kumar, M. Loskyll, J. A. Ojea, E. Solowjow, and S. Levine. Residual reinforcement learning for robot control. In _2019 International Conference on Robotics and Automation (ICRA)_ , pages 6023–6029, 2019. doi:10.1109/ICRA.2019. 8794127. 

- [33] Y. Li, Y. Zhang, W. Xiao, C. Pan, H. Weng, G. He, T. He, and G. Shi. Hold my beer: Learning gentle humanoid locomotion and end-effector stabilization control, 2025. URL https:// arxiv.org/abs/2505.24198. 

- [34] Y. Yang, X. Meng, W. Yu, T. Zhang, J. Tan, and B. Boots. Continuous versatile jumping using learned action residuals. In N. Matni, M. Morari, and G. J. Pappas, editors, _Proceedings of The 5th Annual Learning for Dynamics and Control Conference_ , volume 211 of _Proceedings of Machine Learning Research_ , pages 770–782. PMLR, 15–16 Jun 2023. URL https:// proceedings.mlr.press/v211/yang23b.html. 

- [35] D. Youm, H. Jung, H. Kim, J. Hwangbo, H.-W. Park, and S. Ha. Imitating and finetuning model predictive control for robust and symmetric quadrupedal locomotion. _IEEE Robotics and Automation Letters_ , 2023. 

- [36] S. Feng, E. Whitman, X. Xinjilefu, and C. G. Atkeson. Optimization based full body control for the atlas robot. In _2014 IEEE-RAS International Conference on Humanoid Robots_ , pages 120–127, 2014. doi:10.1109/HUMANOIDS.2014.7041347. 

- [37] B. Henze, M. A. Roa, and C. Ott. Passivity-based whole-body balancing for torque-controlled humanoid robots in multi-contact scenarios. _The International Journal of Robotics Research_ , 35(12):1522–1543, 2016. doi:10.1177/0278364916653815. URL https://doi.org/10. 1177/0278364916653815. 

- [38] A. Herzog, L. Righetti, F. Grimminger, P. Pastor, and S. Schaal. Balancing experiments on a torque-controlled humanoid with hierarchical inverse dynamics. _2014 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 981–988, 2013. URL https://api. semanticscholar.org/CorpusID:3104000. 

- [39] L. Sentis and O. Khatib. A whole-body control framework for humanoids operating in human environments. In _Proceedings 2006 IEEE International Conference on Robotics and Automation, 2006. ICRA 2006._ , pages 2641–2648, 2006. doi:10.1109/ROBOT.2006.1642100. 

- [40] L. SENTIS and O. KHATIB. Synthesis of whole-body behaviors through hierarchical control of behavioral primitives. _International Journal of Humanoid Robotics_ , 02(04):505– 518, 2005. doi:10.1142/S0219843605000594. URL https://doi.org/10.1142/ S0219843605000594. 

- [41] J. Han, W. Xie, J. Zheng, J. Shi, W. Zhang, T. Xiao, and C. Bai. Kungfubot2: Learning versatile motion skills for humanoid whole-body control. _arXiv:2509.16638_ , 2025. 

12 

- [42] Y. Li, Z. Luo, T. Zhang, C. Dai, A. Kanervisto, A. Tirinzoni, H. Weng, K. Kitani, M. Guzek, A. Touati, A. Lazaric, M. Pirotta, and G. Shi. Bfm-zero: A promptable behavioral foundation model for humanoid control using unsupervised reinforcement learning, 2025. URL https: //arxiv.org/abs/2511.04131. 

- [43] H. Lv. Lafan1 retargeting dataset. https://huggingface.co/datasets/ lvhaidong/LAFAN1_Retargeting_Dataset, 2025. 

- [44] J. Mao, S. Zhao, S. Song, C. Hong, T. Shi, J. Ye, M. Zhang, H. Geng, J. Malik, V. Guizilini, and Y. Wang. Universal humanoid robot pose learning from internet human videos. In _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ , pages 1–8, 2025. doi:10.1109/Humanoids65713.2025.11203143. 

- [45] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction, 2025. URL https://arxiv.org/abs/2509. 26633. 

- [46] T. Zhang, B. Zheng, R. Nai, Y. Hu, Y.-J. Wang, G. Chen, F. Lin, J. Li, C. Hong, K. Sreenath, and Y. Gao. Hub: Learning extreme humanoid balance. In _9th Annual Conference on Robot Learning_ , 2025. URL https://openreview.net/forum?id=FCpYuGtN4j. 

- [47] N. Myers, O. Kwon, S. Yamsani, and J. Kim. Child (controller for humanoid imitation and live demonstration): A whole-body humanoid teleoperation system. In _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ , pages 1–6, 2025. doi:10.1109/ Humanoids65713.2025.11203119. 

- [48] A. Purushottam, J. Yan, C. Xu, and J. Ramos. Heavy lifting tasks via haptic teleoperation of a wheeled humanoid. In _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ , pages 345–350, 2025. doi:10.1109/Humanoids65713.2025.11203084. 

- [49] S. Yang, M. Liu, Y. Qin, R. Ding, J. Li, X. Cheng, R. Yang, S. Yi, and X. Wang. ACE: A crossplatform and visual-exoskeletons system for low-cost dexterous teleoperation. In _8th Annual Conference on Robot Learning_ , 2024. URL https://openreview.net/forum?id= 7ddT4eklmQ. 

- [50] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu. Retargeting matters: General motion retargeting for humanoid motion tracking, 2025. URL https://arxiv.org/abs/2510.02252. 

- [51] C. Lu, X. Cheng, J. Li, S. Yang, M. Ji, C. Yuan, G. Yang, S. Yi, and X. Wang. Mobiletelevision: Predictive motion priors for humanoid whole-body control. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5364–5371, 2025. doi: 10.1109/ICRA55743.2025.11128652. 

- [52] Y. Sun, R. Chen, K. S. Yun, Y. Fang, S. Jung, F. Li, B. Li, W. Zhao, and C. Liu. SPARK: Safe protective and assistive robot kit. In _IFAC Symposium on Robotics_ , 2025. URL https: //intelligent-control-lab.github.io/spark/. 

- [53] X. B. Peng and M. van de Panne. Learning locomotion skills using deeprl: Does the choice of action space matter? In _Proceedings of the ACM SIGGRAPH / Eurographics Symposium on Computer Animation_ , SCA ’17, pages 12:1–12:13, New York, NY, USA, 2017. ACM. ISBN 978-1-4503-5091-4. doi:10.1145/3099564.3099567. URL http://doi.acm.org/10. 1145/3099564.3099567. 

- [54] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms, 2017. URL https://arxiv.org/abs/1707.06347. 

13 

- [55] S. Ross, G. Gordon, and D. Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In G. Gordon, D. Dunson, and M. Dud´ık, editors, _Proceedings of the Fourteenth International Conference on Artificial Intelligence and Statistics_ , volume 15 of _Proceedings of Machine Learning Research_ , pages 627–635, Fort Lauderdale, FL, USA, 11–13 Apr 2011. PMLR. URL https://proceedings.mlr.press/v15/ross11a.html. 

- [56] G. Farneb¨ack. Two-frame motion estimation based on polynomial expansion. In _Scandinavian conference on Image analysis_ , pages 363–370. Springer, 2003. 

- [57] G. Authors. Genesis: A generative and universal physics engine for robotics and beyond, December 2024. URL https://github.com/Genesis-Embodied-AI/Genesis. 

- [58] G. A. Hassaan. Tuning of a pd controller used with second order processes. _International Journal of Engineering_ , 2, 2014. URL https://api.semanticscholar.org/ CorpusID:195955908. 

- [59] N. Inc. Optitrack - motion capture systems, 2026. URL https://www.optitrack. com/. 

- [60] Meta. Meta quest vr headsets and accessories — meta store, 2026. URL https://www. meta.com/quest/. 

- [61] H. Corporation. Vive ultimate tracker - full-body tracking, steamvr support, 2026. URL https://www.vive.com/us/accessory/vive-ultimate-tracker/. 

- [62] V. Corporation. Steamvr - valve corporation, 2026. URL https://www.steamvr.com/. 

- [63] F. G. Harvey, M. Yurick, D. Nowrouzezahrai, and C. Pal. Robust motion in-betweening. _ACM Transactions on Graphics (TOG)_ , 39(4):60–1, 2020. 

- [64] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 5442–5451, 2019. 

14 

## **A Additional Proof** 

### **A.1 Whole-Body Impedance Calibration** 

Define the displacement _x_ ≜ _q − q_ 0. Substituting into the governing equation yields 


which is the equation of an undamped simple harmonic oscillator (the derivative gain having been set to zero by construction). Seeking a solution of the form _x_ ( _t_ ) = _Ae_<sup>_iωt_</sup> and substituting gives the characteristic equation 


Since the oscillation period satisfies _P_ = 2 _π/ω_ , it follows that 


Squaring both sides and solving for _M_ eff yields 


_∼_ To obtain an estimate that is robust to modeling errors and sensor noise, we sample _kp_<sup>(</sup><sup>_e_)</sup> _U_ (0 _._ 5 _kp,_ 1 _._ 5 _kp_ ) independently across parallel environments _e ∈ E_ . Since the relation above holds for any positive gain value, applying it environment-wise gives 


where _P_<sup>(</sup><sup>_e_)</sup> denotes the oscillation period measured in environment _e_ . The final estimate is taken as the ensemble mean 


whose variance decreases as _O_ ( _|E|_<sup>_−_1</sup> ) by the law of large numbers, yielding a statistically consistent estimator. 

### **A.2 Theoretical Tracking Delay with Scaled Velocity Feedforward** 

For analysis, we model the joint dynamics as _M_ eff ¨ _q_ = _τ_ . Following the whole-body impedance calibration described in Sec. 3.1, we parameterize the PD gains using a target natural frequency _ωn_ with critical damping _ζ_ = 1. Substituting into the closed-loop dynamics yields 


Since the closed-loop system is linear and time-invariant, its response to an arbitrary reference trajectory can be expressed as a superposition of responses to sinusoidal components via Fourier decomposition. Therefore, without loss of generality, we analyze a sinusoidal reference 


which fully characterizes the frequency-dependent tracking behavior of the controller. Taking the Laplace transform, the transfer function from reference _qt_ to realized joint position _q_ is 


For a sinusoidal input, the steady-state response takes the form 

_q_ ( _t_ ) = _A |H_ ( _jω_ ) _|_ sin� _ωt_ + _ϕ_ ( _ω_ )� _,_ (20) 

15 

where the phase lead between the realized motion and the reference is 


In the low-frequency regime _ω ≪ ωn_ , the phase shift admits an interpretation as an equivalent tracking delay, 


### **A.3 Velocity Feedforward Ratio Upper Bound** 

We derive a practical upper bound on the feedforward ratio _η_ by analyzing the torque balance within a single control interval of duration ∆ _t_ . We assume that at the beginning of each control interval the joint position matches the reference, _q ≈ qt_ , and that the desired trajectory evolves linearly within the interval at constant velocity _q_ ˙ _t_ . 

Under zero-order hold, the target position is fixed at the value commanded at the start of the interval, while the true reference advances continuously. The average positional deviation accumulated between the held target and the true reference over one control step is therefore 


This deviation gives rise to two competing torque contributions: a proportional restoring torque driven by the position error, and a velocity feedforward torque injected to anticipate the reference motion, 


To prevent these combined contributions from inducing additional acceleration within the interval that could cause overshoot, we require their sum to remain within the damping budget _kd_ ˙ _qt_ , i.e., 


Substituting _τp_ and _τv_ , and using the whole-body impedance calibration results described in Sec. 3.1, the inequality simplifies to 


which yields the following upper bound on the admissible feedforward ratio, 


Equation (27) reveals a fundamental trade-off: higher natural frequencies _ωn_ or longer control intervals ∆ _t_ necessitate a more conservative feedforward ratio to maintain stable, non-overshooting tracking. 

16 

## **B Additional Evaluation** 

### **B.1 Simulation Setup** 

We leverage Genesis [57] as the simulation backbone, with a simulation timestep of sim ~~d~~ t = 2001<sup>s</sup> and a single physics substep across all experiments, including whole-body impedance calibration, velocity feedforward ratio validation, and policy training. During policy training, we run 8,192 parallel environments, achieving over 100k policy steps per second on an NVIDIA L40s GPU with a control decimation of 4. Detailed simulation parameters and domain randomizations are provided in the appendix. 

### **B.2 Real-World Robot Setup** 

Following common practice in control literature [58], we set the PD gains in simulation based on a target natural frequency of _ωn_ = 10 rad _/_ s with a damping ratio _ζ_ = 1. The velocity feedforward ratio is set to 0.9, while it is disabled for all indirect-drive joints, which are ankle and waist joints for Unitree G1. The low-level PD controller operates at 1000 Hz, whereas the high-level control policy runs at 50 Hz. This setting yields an upper bound on the velocity feedforward ratio of 0.95. To ensure consistent forward kinematics in observation computation, we apply a low-pass filter with coefficient _α_ = 0 _._ 1 at 1000 Hz to smooth the measured joint configuration. 

### **B.3 MoCap System Setup** 

We employ an optical motion capture system, OptiTrack [59], to obtain the global position and rotation of human body links. Although the OptiTrack Motive software is capable of reconstructing a full-body human pose, our system only utilizes the subset of links described in Sec. 3.2, which are sufficient for the proposed Cartesian-space mapping and tracking framework. 

Human motion is streamed at 120 Hz. In contrast to TWIST [8], we implement a non-blocking streaming pipeline specifically designed for real-time control rather than offline recording. The pipeline minimizes transmission latency such that, when link poses are queried, the effective delay is bounded within a single MoCap streaming cycle ( 120<sup><u>1</u>s).Inalocalsetup,thesystemlatencyis</sup> less than 10 ms. 

### **B.4 VR System Setup** 

We employ a VR-based input system composed of a Meta Quest 2 [60] headset, hand controllers, and three VIVE Ultimate Trackers [61], with SteamVR [62] used as a unifying middleware to resolve cross-device compatibility. The trackers are mounted on the waist and both feet as in Fig. 2, providing direct pose measurements for the corresponding body links. 

Because the torso pose is not directly tracked, we estimate the torso orientation from the planar motion of the headset expressed in the pelvis frame. Specifically, we compute the rotation that aligns the vertical axis _⃗z_ with ( **R** pelvis)<sup>_−_1</sup> **p** headset, along the rotation axis orthogonal to the plane spanned by them. The headset’s own orientation is intentionally not used, allowing the user to freely observe the environment. 

### **B.5 System-Level Latency Breakdown** 

We define end-to-end latency as the time between a motion of the human operator and the corresponding motion of the robot. As shown in Fig. 8, each human pose passes through four stages before it is reflected in the robot motion. (1) _Sensing_ : the pose is captured by OptiTrack and streamed through NatNet at 120 Hz, or captured by the VR system and published at 60 Hz over a wireless link. (2) _Transmission_ : the pose is sent over a wired network to the desktop that runs the broadcaster and the policy. (3) _Computation_ : Direct Extremity Control maps the human pose to humanoid link targets, and the policy, running at 50 Hz, outputs target joint positions. Mapping, policy inference, 

17 


Figure 8: Teleoperation system setup. Solid arrows denote wired connections and dashed arrows denote wireless connections. 

and robot communication via unitree ~~s~~ dk2 ~~p~~ ython (1000 Hz over CycloneDDS/UDP) run in a single Python process. At each control step, the Unitree G1 receives the PD gains ( _kp, kd_ ), the target joint position _qt_<sup>_∗_, and the target joint velocity</sup><sup>_η_(</sup><sup>_q_</sup> _t_<sup>_∗−q_</sup> _t_<sup>_∗_</sup> _−_ 1<sup>)</sup><sup>_/_∆</sup><sup>_t_.(4)</sup><sup>_Tracking_: the low-level PD controller</sup> drives the joints toward these targets, and the robot motion lags behind the target by the closed-loop tracking delay. Tab. 5 lists the delay contributed by each stage. 

|Component|MoCap (ms)|VR (ms)|
|---|---|---|
|Pose streaming (average sample age)|4|8|
|Wireless transmission|–|8|
|Inter-desktop communication|0.4|0.4|
|Direct extremity mapping|0.3|0.3|
|Policy inference|0.06|0.06|
|Robot communication|_<_1|_<_1|
|Closed-loop motion tracking|46|46|
|Sum of components|51|63|
|Measured end-to-end|54|64|


Table 5: System-level latency breakdown. Closed-loop motion tracking is measured in simulation with _η_ = 0 _._ 9 and includes the average 10 ms wait induced by the 50 Hz policy update. 

The breakdown shows that end-to-end latency is dominated by closed-loop tracking. Tracking contributes 46 ms, which accounts for about 85% of the measured latency under MoCap and about 70% under VR. Sensing is the second largest source: since poses arrive asynchronously, each pose has waited on average half a streaming period before it is used, which is 4 ms at 120 Hz and 8 ms at 60 Hz, and the wireless link adds another 8 ms for VR. These two sensing terms explain the 10 ms difference between the MoCap and VR settings. All transmission and computation steps together contribute less than 2 ms, so the use of Python and the communication stack does not noticeably affect latency. The sum of all components is within 3 ms of the measured latency in both settings, and we attribute the remaining difference to internal processing in the motion capture and VR systems. Since tracking delay is the only large component, reducing it is the most effective way to reduce end-to-end latency, which is exactly what scaled velocity feedforward does. 

### **B.6 Whole-Body Impedance Calibration** 


Figure 9: Whole-body impedance calibration of Unitree G1 elbow joint. Solid lines correspond to proportional gains _kp_ , dashed lines depict the effective impedance. 

As shown in Fig.9, we evaluate the proposed whole-body impedance calibration under different target natural frequencies _ωn_ and initial proportional gains _kp_ on the Unitree G1 elbow joint, while 

18 

three additional distal joints are calibrated simultaneously but not visualized. The derivative gain _kd_ is computed using a fixed damping ratio _ζ_ = 1 as defined in Eq. (2). Despite large variations in initialization, the calibration process consistently converges to stable effective impedance values that differ across _ωn_ , demonstrating robustness to initial gains and reliable recovery of _M_ eff induced by whole-body coupling. 

### **B.7 Velocity Feedforward Control** 


Figure 10: Measured tracking delay in simulation and real world as a function of velocity feedforward ratio. Dashed line represents the theoretical value<sup>2(1</sup> _ω_<sup>_−_</sup> _n_<sup>_<u>η</u>_</sup><sup><u>)</u></sup> . 

Using the PD gains obtained from whole-body impedance calibration, we evaluate the low-level tracking delay predicted by Eq. (5) in both simulation and on hardware. A sinusoidal reference with frequency _ω_ = 3 _._ 14 rad _/_ s is applied as the target joint position _qt_ . 

As shown in Fig. 10, the theoretical predictions closely match the measured delays for _ωn_ = 10 rad _/_ s and _ωn_ = 15 rad _/_ s, with the remaining discrepancy explained by the control period ∆ _t_ = 0 _._ 02 s. For _ωn_ = 5 rad _/_ s, deviations arise from violation of the assumption _ω ≪ ωn_ and numerical inaccuracies. With a control update frequency of 50 Hz, the measured delay increases at higher velocity feedforward ratios, producing the upward trend observed at the right end of the curves. This effect is consistent with the discrete-time overshoot discussed by Eq. (6). These results validate the theoretical analysis of velocity feedforward and impedance calibration and the correctness of the low-level system design. 

### **B.8 Optical Flow-based Latency Estimation** 


Figure 11: Experimental setup for latency validation, with two cameras and an optical motion capture system simultaneously recording. 

To demonstrate the accuracy and reliability of the proposed video-based latency estimation method, we conduct a controlled validation experiment using multi-view video recordings together with motion-capture-based ground-truth measurements. Specifically, we record a single reciprocating hand motion simultaneously using two cameras placed at different viewpoints, observing the same motion from distinct perspectives, as shown in Fig. 11. For each camera view, we independently apply the optical-flow-based pipeline described in Sec. 4 to extract a one-dimensional motion signal and estimate the temporal offset between the human and robot motions, yielding two latency estimates. 

19 


Figure 12: Normalized optical-flow projections and the corresponding position trajectories of the human and robot are shown on the right. 

Fig. 12 presents the experimental results. For the two camera views, the middle column visualizes the projected optical flows, while the right column shows the accumulated displacement obtained by integrating the projected flow over time, which approximates the underlying motion trajectory. **The estimated latencies are 55 ms and 60 ms** , and their agreement serves as a consistency check for view invariance and robustness of the method. For the motion-captured end-effector positions, the middle column compares the estimated velocities, and the right column shows the directly tracked position waveforms. **The ground-truth latency calculated directly from the tracked positions is 51 ms** , which, together with the velocities computed from these positions, is consistent with the optical-flow-based estimates, confirming that the proposed method accurately captures end-to-end system latency. Minor discrepancies may arise due to non-ideal camera viewpoints or imperfect alignment between the chosen projection direction and the true motion. As illustrated in Fig. 12, the projected optical flow in View 1 closely aligns with the motion-capture-derived velocity, whereas the flow in View 2 is noticeably noisier, leading to a less accurate latency estimate. In addition, subframe-level variance (less than 16 ms for 60 FPS videos) can naturally occur due to measurement noise and temporal discretization effects. 

20 

## **C Policy Learning Details** 

To clarify the policy learning formulation, we first introduce the notation used in this section. As defined in Sec. 3.2, we denote the target pose of each tracking link as **T**<sup>_r_</sup> link<sup>= [</sup><sup>**R**</sup><sup>_r_</sup> link<sup>_,_</sup><sup>**p**</sup><sup>_r_</sup> link<sup>]</sup><sup>_∈_SE(3),</sup> and use **T**<sup>_r_</sup> to represent the collection of all tracked link poses. The pose discrepancy between the measured and target link poses is denoted as ∆ **T**<sup>_r_</sup> link<sup>=[∆</sup><sup>**R**</sup><sup>_r_</sup> link<sup>_,_∆</sup><sup>**p**</sup><sup>_r_</sup> link<sup>].Notably, the pelvis link</sup> serves as the root link in simulation and as the IMU mounting base in the real robot; therefore, it is used to represent the global position and orientation of the robot. 

Based on the foot link position **p**<sup>_r_</sup> _k,_ foot<sup>,weestimatetheprobabilityoffoot–groundcontactasfol-</sup> lows: 


Based on the estimated contact probability and the principle of momentum conservation, we approximate the contact force. We denote F as the proportion of the total body weight supported by each contact. 


where E denotes a weighted sum with a quadratic weighting function that vanishes at both endpoints. 

### **C.1 Problem Formulation** 

We model the control problem as a Markov Decision Process ( _O, A, P, R, γ_ ), where the policy _π_<sup>_∗_</sup> : _O →A_ maps observations **o** _t ∈_ O to actions **a** _t ∈_ A, interpreted as scaled joint target positions **q**<sup>_∗_</sup> _t_<sup>=</sup><sup>_k ·_</sup><sup>**a**</sup><sup>_t_for a fixed scalar</sup><sup>_k∈_R</sup><sup>_>_0.Teleoperation is formulated as a one-step-ahead</sup> motion tracking problem, where the operator provides end-effector target poses **T** _t ∈ SE_ (3) one timestep in advance, and the policy minimizes the tracking error _||_ **Tt** _−_ **T**<sup>_r_</sup> _t−_ 1<sup>_||_where</sup><sup>_∥· ∥_denotes</sup> an appropriate _SE_ (3) distance metric. 

### **C.2 Observation** 

Since our control interface operates solely on a selected set of robot link poses, we introduce a future interpretation function to encode reference motion over a finite horizon _H_ 


where **V**<sup>_r_</sup> = **T**<sup>˙</sup><sup>_r_</sup> ( **T**<sup>_r_</sup> )<sup>_−_1</sup> represents the target velocities in the global frame. _I_ is defined as follow: 

|Future pelvis translation|**p**<sup>_r_</sup><br>pelvis_,_t:t+H <sup>_−_</sup><sup>**p**</sup><sup>_r_</sup><br>pelvis_,_t_−_1|
|---|---|
|Future pelvis rotation|**r**<sup>_r,⊤_</sup><br>pelvis_,_t:t+H <sup>_·_</sup><sup>**r**</sup><sup>_r_</sup><br>pelvis_,_t_−_1|
|Link poses|**T**<sup>_r′_</sup><br>_t_:_t_+_H_|
|Link velocities (privilege)|**V**<sup>_r_</sup><br>_t_:_t_+_H_|
|Retargeted joint configuration (privilege)|_qt,_ ˙_qt_|
|Foot contact probability|Pk<br>~~f~~oot|


To explicitly capture extremity pose errors and account for the IMU being mounted on the pelvis of the Unitree G1, we express both target poses **T**<sup>_r′_</sup> and actual poses **U**<sup>_r′_</sup> in the pelvis frame, where **U**<sup>_r′_</sup> is obtained via forward kinematics from the pelvis, and compute the local pose discrepancy as 


For deployable policies _π_ student and _π_ teleop, we use a single future frame to maximize responsiveness, resulting in the observation vector [ **o**<sup>ref</sup> (1) _,_ **o**<sup>diff</sup> _,_ **o**<sup>proprio</sup> ] where **o**<sup>proprio</sup> denotes proprioceptive observations. The oracle policy _π_ teacher leverages a longer horizon together with privileged observations **o**<sup>priv</sup> , including global-frame pose discrepancies, joint configurations after inverse kinematics, domain randomization parameters and foot contact forces, yielding [ **o**<sup>ref</sup> (32) _,_ **o**<sup>diff</sup> _,_ **o**<sup>proprio</sup> _,_ **o**<sup>priv</sup> ]. 

21 

The proprioception observation **o**<sup>proprio</sup> is listed below: 

|Last action|_at−_1|
|---|---|
|Joint configuration|_q,_ ˙_q_|
|Pelvis rotation|**r**pelvis|
|Pelvis linear velocity (privilege)|˙**p**pelvis|
|Pelvis angular velocity|˙**r**pelvis|


Additional privileged observation **o**<sup>priv</sup> is listed below: 

|Domain Randomization Parameters|—|
|---|---|
|Residual joint configuration|∆_q,_∆˙_q_|
|Residual link poses|∆**T**<sup>_r_</sup>|
|Foot contact force|F<sup>target</sup><br>k<br>~~f~~oot<sup>_,_ Fmeasure</sup><br>k<br>~~f~~oot|


### **C.3 Reward Function** 

To improve exploration stability in online reinforcement learning, we formulate all reward terms as negative-valued and compute the exponential of their weighted sum as the total reward. This formulation ensures that (i) the per-step total reward lies within (0 _,_ 1), and (ii) the gradient of the total reward with respect to each individual term is preserved. The complete specification of the reward functions is provided in the appendix. 

The exact reward formulation involves axis- and link-specific weighting terms and is therefore omitted for brevity. Below, we present the simplified primary reward components. 

|**Reward Term**|**Expression**|**Scale**|
|---|---|---|
|Global tracking link poses|_−||_(**U**<sup>_r_</sup>)<sup>_−_1</sup>**T**<sup>_r_</sup>_||_<sup>2</sup><br>2|30|
|Local tracking link poses|_−||_(**U**<sup>_r′_</sup>)<sup>_−_1</sup>**T**<sup>_r′_</sup>_||_<sup>2</sup><br>2|20|
|Retargeted DoF position|_−||qt −q||_<sup>2</sup><br>2|3|
|Retargeted DoF velocity|_−||_˙_qt −_˙_q||_<sup>2</sup><br>2|0.02|
|Foot contact reward|_−_<br>�<br>F<sup>target</sup><br>k<br>~~f~~oot <sup>_−_Fmeasure</sup><br>k<br>~~f~~oot<br>�2|3|
|Foot contact penalty|_−_(I[Pk<br>~~f~~oot <sup>_<_ 0</sup><sup>_._2]</sup><sup>_·_ Fmeasure</sup><br>k<br>~~f~~oot<br>)<sup>2</sup>|10|
|Torque Penalty|_−||τ||_<sup>2</sup><br>2|0.0001|
|Action rate|_−||at−_1_−at||_<sup>2</sup><br>2|0.2|


### **C.4 Motion Dataset** 

As observed in prior work [8, 9], incorporating in-domain motion data significantly improves policy performance during teleoperation. We collect a set of motion sequences _S_ teleop using an optical motion capture system; however, to ensure fair evaluation and reproducibility, these user-specific datasets are excluded from policy training experiments unless explicitly stated. 

Aiming for task-agnostic policy learning, we use the widely adopted LAFAN1 dataset _S_ lafan [63] retargeted by Unitree [43], as dynamic and challenging motions, and AMASS _S_ amass [64] as a largescale and diverse motion corpus. Unless otherwise specified, we use _S_ lafan in teacher and student learning stages, _S_ lafan _∪S_ amass in RL finetune stage. For evaluation, we additionally collect a trajectory _S_ teleop<sup>_′_=</sup><sup>_{s_eval</sup><sup>_}, s_eval</sup><sup>_∈S/_teleopcomprising common daily motions to assess teleoperation</sup> performance. 

22 

### **C.5 Domain Randomization** 

Domain randomization is applied to motor dynamics, contact friction, and torso mass distribution. For motor dynamics, we apply four randomizations: 

_τ_ = _α_ strength( _αkpkp_ ( _qt − q_ + _β_ offset) + _αkd_ ( _η q_ ˙ _t − qt_ )) 

Detailed distributions are as follows: 

|_kp_ratio_αkp_|_U_(0_._8_,_1_._2)|
|---|---|
|_kd_ratio_αkd_|_U_(0_._8_,_1_._2)|
|Motor strength_α_strength|_U_(0_._8_,_1_._2)|
|Motor offset_β_offset|_U_(_−_0_._1_,_0_._1)|
|Friction ratio|_U_(0_._3_,_1_._0)|
|Torso added mass (kg)|_U_(_−_2_,_5)|
|Torso CoM displacement (m)|_U_(_−_0_._05_,_0_._05)<sup>3</sup>|


### **C.6 Hyperparameters** 

All actor and critic networks are implemented as MLPs with hidden dimensions [1024, 512, 256] and ReLU as activation layer. We adopt an adaptive learning rate schedule in PPO with a target KL divergence of 0.01. The remaining PPO hyperparameters are listed below: 

|_γ_|0.99|
|---|---|
|_λ_GAE|0.95|
|Entropy coefficient|0.003|
|Value loss coefficient|1.0|
|Rollout length|24|
|Optimizer|ADAM|
|#epoch|5|
|#mini batch|8|
|#iteration|6000|


We utilize DAgger with the following hyperparameters: 

|learning rate_η_|0.0003|
|---|---|
|Batch size|256|
|Rollout length|24|
|Optimizer|ADAM|
|#epoch|10|
|#iteration|1500|


23 

