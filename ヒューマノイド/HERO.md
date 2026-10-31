---
title: "HERO: Learning Humanoid End-Effector Control for Visual Whole-Body Open-Vocabulary Object Grasping"
date: "2026-02-18"
authors: "Runpei Dong; Ziyan Li; Arjun Gupta; Xialin He; Saurabh Gupta"
url: https://arxiv.org/abs/2602.16705
pdf: https://arxiv.org/pdf/2602.16705
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.16705)** / [論文ページ](https://arxiv.org/abs/2602.16705)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **HERO: Learning Humanoid End-Effector Control for Visual Whole-Body Open-Vocabulary Object Grasping** 

**Runpei Dong**<sup>_†_</sup> **Ziyan Li**<sup>_†_</sup> **Arjun Gupta Xialin He Saurabh Gupta** _University of Illinois Urbana-Champaign_ 

**hero-humanoid.github.io** 


**Figure 1: Open-vocabulary visual loco-manipulation with humanoids.** We enable a humanoid to _autonomously_ loco-manipulate _novel_ objects in _novel_ scenes using onboard sensors. A modular system combines large vision models for visual generalization with an accurate end-effector tracking policy. It achieves an _83 .8_ % average success rate at reaching and picking up novel objects in challenging real-world scenes that require whole-body bending, squatting, and twisting. 

**Abstract:** Visual loco-manipulation of arbitrary in-the-wild objects requires accurate end-effector (EE) control and a generalizable understanding of the scene from visual inputs ( _e.g._ , RGB-D images). Existing imitation and sim2real methods jointly learn both these aspects via monolithic end-to-end learning and are thus hard to scale. In this work, we bring to bear the best tools for each of these problems – large vision models for generalizable scene understanding and simulated training for accurate EE control – leading to an overall modular loco-manipulation system that exhibits strong generalization. Our core technical innovation is HERO, an accurate residual-aware EE tracking policy made possible by combining classical robotics with machine learning. It uses a) inverse kinematics to convert residual end-effector targets into reference trajectories, b) a learned neural forward model for accurate forward kinematics, and c) goal adjustment and replanning. Together, these innovations reduce the end-effector tracking error to 2.44cm, outperforming the strongest prior method by 5.5 _×_ . Our overall system operates in diverse real- 

> _†_ Equal contribution. 

10th Conference on Robot Learning (CoRL 2026), Austin TX, USA. 

world environments, from offices to coffee shops, where the robot reliably grasps various everyday objects ( _e.g._ , mugs, apples, toys) on surfaces ranging from 43cm to 92cm in height. Systematic modular and end-to-end tests demonstrate the effectiveness of our proposed design. We believe our advances open up new ways of training humanoids to interact with daily objects. 

## **1 Introduction** 

Think about reaching to pick up the objects placed on the various table tops in Fig. 1. As humans we can reliably and robustly use our whole bodies to execute such pick ups. We can reach across a table with our back, rotate our torso for objects to the side, or squat for low coffee tables, all while balancing on two legs. We can pick up seen objects on seen tables, but also novel objects on novel tables in novel scenes. Once we have glanced at the object and scene, we can even do this with our eyes closed. In this paper, we develop a framework that equips humanoids with this fundamental capability: _autonomously reach over to pick up novel objects in novel everyday environments._ 

Humanoids are doing backflips [1–5], so why would we be writing about such a mundane and seemingly unimpressive task? There are two key differences that make the problem of manipulating novel objects harder. First, in-the-wild operation means that neither reference motions nor privileged sensors ( _e.g._ MOCAP) are available. But instead we need to process high-dimensional RGB-D image observations to infer object locations and plan trajectories. Second, object manipulation requires _precise_ and _goal-directed_ behavior: a robot needs to get its hand _where the object actually is_ , different from a backflip where the focus is on landing safely rather than at a precise location. Operation in novel environments, sensing using on-board RGB-D sensors, precise end-effector (EE) control, and maintaining balance while reaching around, make this problem challenging. 

The state-of-the-art for training humanoids for such tasks is end-to-end imitation learning in the real world [6–10] or end-to-end visual RL in simulation [11]. However, the difficulty of real-world data collection and of setting up photo- and physically-realistic scenes in simulation [11] limits the amount of data diversity and thus the generalization capabilities of learned policies. This causes them to fall short of the goal of manipulating _novel_ objects in _novel_ environments. In this paper, we pursue an alternate approach. We take inspiration from strong results with modular systems for tabletop object manipulation problems [12–14]. We use large vision models to translate high-level instructions ( _e.g._ grasp the red coke can) into actionable plans by identifying the target objects in complex scenes and synthesizing a grasp on them; and a simulation-trained low-level control module then conveys the robot EE to the grasp location. Being able to use large pre-trained models enables broad generalization and even open-vocabulary reasoning. In many ways, this is the more direct, obvious, and performant way to build such a system. So why is such a modular method not already the go-to approach for building a humanoid object manipulation system? 

While it is easy to get a Franka Emika robot to where you want, it turns out it is current methods aren’t able to accurately control a humanoid hand. SONIC [15], the leading tracker achieves only a 13.38 cm tracking error in the real world, an error rate that is simply too large for object manipulation.<sup>1</sup> Our key technical contribution is to develop, HERO, an accurate EE tracking policy that cuts this error down by 5.5 _×_ to 2.44cm. This unlocks the possibility of developing modular humanoid systems for object manipulation that generalize without large-scale real-world imitation demos. 

So what are the ingredients of building a highly accurate end-effector tracker? Our accurate endeffector control algorithm is based on multiple innovations. First, rather than directly trying to get the end-effector to the target location, we use a motion planner to generate an upper-body reference motion that gets the end-effector to the desired target. Second, the policy receives as input not just the current and target joint angles (output of the motion planner), but also the current and target endeffector position. Third, it is important to obtain a high-quality estimate of the current end-effector position, as we found that the default analytical forward kinematics and odometry on a low-cost 

> 1Existing works do not focus on end-effector tracking accuracy. Imitation learning stacks built on top of inaccurate trackers still work because the IL policy learns to correct for the inaccurate tracking. 

2 


**Figure 2: Overall architecture for our proposed modular system for open-vocabulary object grasping.** Given a free-form natural language text query indicating which object needs to be picked, we use open-vocabulary large vision models (LVMs: Grounding DINO [16] and SAM [17]) to segment out the object of interest and predict parallel jaw grasps (using the AnyGrasp model [18]). We retarget the predicted grasp to a Dex-3 hand. We use our proposed whole-body end-effector tracker to convey the robot arm to the predicted grasp before picking up the object. By decomposing _action planning_ ( _i.e._ identifying which object to pick and using what grasp) from _action execution_ ( _i.e._ actual control of the robot), we inherit the strong visual generalization from pre-trained models as well as strong control capabilities for simulated training of the tracking policy. 

humanoid robot like Unitree G1 are not accurate. We mitigate this issue by training neural forward models: an upper body model that provides accurate EE pose relative to the base, and a base odometry model that provides an accurate base pose relative to the stationary feet. Fourth, because whole-body balancing causes the planned reference to drift relative to the target, we periodically replan from the current state and odometry-corrected goal in a closed loop. Finally, a goal-adjustment loop iteratively nudges the commanded pose to remove the systematic sim2real gap. 

Using this performant end-effector tracking policy, we develop a modular system for picking up open-vocabulary novel objects in novel everyday environments. This modular system leverages an open-vocabulary perception module to detect and segment the target object using large pre-trained vision models (Grounding DINO 1.5 [16] and SAM-3 [17]). We next use the AnyGrasp model [18] to produce parallel jaw grasps on the candidate object. We retarget them to the Dex-3 dexterous hand on the Unitree robot. Finally, we use our tracker as a low-level controller to achieve the grasp pose. In real-world testing for grasping open-vocabulary object queries in novel environments, our system achieves a success rate of 90% on 10 daily objects across standard and short table heights, 73.3% success rate on generalization to 10 daily scenes, and 80% success rate on cluttered scenes. 

## **2 Related Works** 

**Loco-manipulation via Motion Tracking.** Motion tracking is a central tool for humanoid locomanipulation: teleoperation or generated references provide whole-body motions, and RL policies learn to track them for sim-to-real transfer [6, 9, 19–22]. Recent work improves tracking accuracy, agility, robustness, reachability, and generalization [5, 15, 23–31], including force- and stabilityaware end-effector control [32–34]. Teleoperation systems further enable imitation learning for rich manipulation [35–43]. In contrast, HERO does not require human teleoperation at test time; it converts visual grasp goals into end-effector targets and executes them with a learned tracker. 

**Visual Loco-Manipulation.** Visual loco-manipulation often uses imitation data collected by teleoperation [6–9, 44] or reference-state policies that map depth observations to high-level commands or generated motions [45–48]. End-to-end visual RL has also shown strong results on selected object categories [11], and recent foundation-model approaches aim at universal humanoid policies [49, 50]. These systems remain limited by collected demonstrations, generated assets, or object categories. HERO instead pairs open-vocabulary perception with modular task-space control, enabling novel language queries and objects without task-specific teleoperation demonstrations. 

**System Identification.** Real robots deviate from their nominal models because of hardware inaccuracies, joint elasticity, and dynamics [51–53]. System identification mitigates this sim-to-real gap either through online adaptation [54–59] or offline correction from collected data [5, 60, 61]. Our learned residual FK and base-odometry models follow the offline direction, using MOCAP data to correct the task-space signals required by the tracking policy. 

3 

## **3 HERO: Humanoid End-Effector ContROl** 


Upper-Body Reference Trajectory Given a desired end-effector pose in the robot Goal Adjustment frame, HERO outputs motor commands for all Replanning Adjusted 29 DoFs of a Unitree G1 humanoid [62]. AlGoal though the feet remain planted, far-reaching moEE tions require coordinated waist, torso, and leg Proprio. _Upper-Body_ Target Drift motion. We therefore combine classical IK and ReferenceHistory Whole-Body Body MLPWhole-Body MLPWhole-WholeDrifted motion planning with learned task-space feedMLP back instead of learning a monolithic pose-toDrifted action mapping. The overall tracker is shown Goal EE Tracking Policy _Lower-Body_ in Fig. 3. HERO first converts the target _T_<sup>EE</sup> _∈_ **Figure 3: HERO end-effector control.** HERO SE(3) into a base height _h_ and upper-body joint outputs IK and planned references from an EE goal, goal **q**<sup>_∗_</sup> _∈_ R<sup>17</sup> using IK, then uses a collisionthen tracks them with a learned whole-body policy, free planner [63] to produce reference joint and which leverages residual EE error computed from end-effector trajectories. A learned whole-body learned FK and odometry. Replanning and goal policy _π_ t tracks these references with joint poadjustment compensate drift and sim2real bias. sition commands at 50Hz. To make the residual task-space feedback accurate, _π_ t uses learned end-effector FK _η_ and base odometry _ξ_ . During execution, we also replan periodically and apply a small goal adjustment to compensate systematic sim-to-real bias. 

**Figure 3: HERO end-effector control.** HERO outputs IK and planned references from an EE goal, then tracks them with a learned whole-body policy, which leverages residual EE error computed from learned FK and odometry. Replanning and goal adjustment compensate drift and sim2real bias. 

### **3.1 Whole-body End-Effector Tracking Policy,** _π_ **t** 

To track the target EE pose _T_<sup>EE</sup> _∈_ SE(3) defined in the robot frame, our whole-body EE tracking policy _π_ t first obtains an upper-body reference trajectory _{_ **q** _t}_<sup>_T_</sup> _t_ =1<sup>and the corresponding 6-DoF EE</sup> reference trajectory _{eet}_<sup>_T_</sup> _t_ =1<sup>from a motion planner.Given the trajectory, the current proprioceptive</sup> state **s** _t_ , and other commands, _π_ t outputs the 29-DoF joint angles commands that are passed to per-joint PD controllers. 

### **Residual-Aware End-Effector Tracking.** _π_ t output actions **a** _t_ at time _t_ as follows: 


where **s** _t_ is the current proprioception, _ht_ is the reference base height, **q** _t_ are the reference upper-body joint angles, **v** _t_ are the linear and angular velocity locomotion commands, and **s** _t−_ 5: _t−_ 1 _,_ **a** _t−_ 5: _t−_ 1 are five time steps of proprioception and action history. The proprioception include the robot’s joint angles, joint velocities, angular velocity, projected gravity, and roll and pitch encoded from the IMU. We don’t use the IMU yaw as it is inaccurate [9]. **∆** **_E t_** represents the residual pose error between the current and target end-effector pose in the robot frame, _i.e._ , 


where _f_<sup>EE</sup> ( **x** _t_ ) maps the arm states **x** _t ∈_ R<sup>17</sup> to the end-effector pose _Tt_<sup>EE</sup> _∈_ SE(3), and _⊖_ is the inverse pose composition operator.<sup>2</sup> 

**Architecture and Training.** _πt_ uses two three-hidden-layer MLPs that share the same observation but separately predict upper- and lower-body actions; their outputs are combined into 29-DoF joint commands. We train _π_ t in simulation with PPO [64], using AMASS [65] ( _∼_ 8K motion sequences) and a curated set of everyday reaching targets ( _∼_ 8K). Targets are sampled in the robot frame from [0 _._ 1m _, −_ 0 _._ 5m _,_ 0 _._ 65m] to [0 _._ 5m _,_ 0 _._ 5m _,_ 1 _._ 15m], with yaw in [ _−_ 60<sup>_◦_</sup> _,_ 60<sup>_◦_</sup> ]. A motion planner converts each target into upper-body and end-effector reference trajectories for policy training. 

### **3.2 Learned Residual Neural Forward Models** 

**Residual Neural FK.** Our residual neural forward kinematics function, _η_ , learns a correction to the output of the analytical forward kinematic function, FK, to output accurate end-effector poses. 

> 2We use _⊕_ to denote pose composition: **T** 1 _⊕_ **T** 2 = **T** 1 _·_ **T** 2 and _⊖_ for inverse composition: **T** 1 _⊖_ **T** 2 = **T**<sup>_−_</sup> 2<sup>1</sup> _·_ **T** 1. 

4 


**Figure 4: Learned neural forward kinematics and odometry models.** (a) A residual FK model _η_ corrects analytical FK by predicting EE translation and rotation residuals. (b) A residual odometry model _ξ_ estimates base motion from lower-body joints. (c) Whole-body reaching can move the object out of the egocentric view, making purely visual correction unreliable. 

Specifically, given the current proprioceptive state of one operating arm and waist **x** _t ∈_ R<sup>10</sup> at timestep _t_ , and output from analytical FK, FK( **x** _t_ ), the final end-effector pose _f_<sup>EE</sup> ( **x** _t_ ) is obtained as: 


Note that the analytical forward kinematics function FK( **x** _t_ ) uses the robot geometry and coordinate transformations to compute the 6-DoF end-effector pose in the robot base frame. For precise robots, FK is itself quite accurate, however as our experiments will show, FK is inaccurate for our humanoid [51, 52], necessitating the need for learning a correction. 

**Residual Neural Leg Odometry.** Different from fixed-base object manipulation tasks, where the robot’s base is fixed and stable, humanoid robots’ base needs to be dynamically balanced during whole-body reaching. This movement makes the original reaching target inaccurate, as the reaching target defined in the robot frame is no longer the same place where the object lies. One might consider using the egocentric visual information for replanning or motion adjustment. However, as shown in Fig. 4, the egocentric view of the robot is too narrow for the robot to see the object when the robot’s arm and waist movements are large. As a result, using the robot’s odometry to adjust the reaching goal is critical. We assume the feet to be static on the ground and use the lower body joint angles to predict the base pose. By assuming the robot ankle joint as the root joint and the robot base as the end-effector, we can compute the base pose using forward kinematics. 

However, similar to the error in analytical FK for EE, analytical FK to compute the base pose is also inaccurate (see analysis in Sec. 5). Similar to our solution for EE, we adopt a residual model to mitigate these inaccuracies. We estimate the base pose transformation relative to time step 0, rather than the absolute base pose, which avoids depending on a global frame and directly tells the controller how much the base has shifted since planning. 

Concretely, let **y** _t ∈_ R<sup>6</sup> be the 6DOF state of the left (or right) leg motors. We can get analytical base odometry, _i.e._ base pose relative to base pose at time step 0, _O_<sup>FK</sup> ( **y** _t,_ **y** 0) _∈_ SE(3), using analytical forward kinematics and SE(3) difference: _O_<sup>FK</sup> ( **y** _t,_ **y** 0) = FK( **y** 0) _⊖_ FK( **y** _t_ ) _._ Our residual neural leg odometry model _ξ_ learns the residual: 


**Architecture and Training.** Both residual models are lightweight 3-layer MLPs. _η_ predicts a residual SE(3) correction for the end-effector, while _ξ_ predicts the residual between MOCAP odometry and analytical leg-FK odometry. Each model uses separate heads for translation and rotation, outputting a residual translation in R<sup>3</sup> and a residual rotation via the 6D rotation representation [66]. 

5 

_“green apple”_ RGB-D Input Segmented Object AnyGrasp Result Filtered Jaw Grasp Retargeted EE Pose 

**Figure 5: Visual perception for language-conditioned grasping.** An example of target segmentation, grasp proposals, filtering, and retargeted EE poses from onboard RGB-D observations. 

We train both models on MOCAP data [67]. For _η_ , a tracking policy sweeps the EE through the workspace while we record motor encoders and MOCAP EE/base poses; marker poses are converted with the Kabsch-Umeyama algorithm [68, 69] ( _<_ 1 _._ 5mm RMSE). We collect 3 hours of data and use the first 2 hours for training and the last 1 hour for validation. _ξ_ uses the same split, with supervision formed by sampling temporal pairs from trajectories. Both models are optimized with MSE losses on residual translations and rotations, using MOCAP-derived ∆ _Tt_<sup>EE</sup> and ∆ _On−m_ as ground truth. 

### **3.3 Replanning and Goal Adjustment** 

During execution, the robot drifts from the planned reference because of base-pose changes from whole-body balancing and residual sim-to-real bias, leaving the policy with an out-of-distribution input or a target that is no longer reachable. We therefore replan the remaining reference _{_ **q** _t, eet}_ every _k_ = 300 steps (6 sec) with cuRobo [63] ( _∼_ 20 ms), using the current state and the odometrycorrected goal so each fresh trajectory accounts for the latest base displacement. 

To further compensate the steady-state EE tracking offset, we maintain a commanded grasp _g_ initialized to _T_<sup>EE</sup> and apply the damped translational update _g_<sup>_p_</sup> _← g_<sup>_p_</sup> _− β, e_<sup>_p_</sup> _t_<sup>, where</sup><sup>_gp, ep_</sup> _t_<sup>_∈_R3</sup> denote the translational components of _g_ and the SE(3) residual _et_ = _f_<sup>EE</sup> ( **x** _t_ ) _⊖ T_<sup>EE</sup> , _β_ = 0 _._ 6, only when _|e_<sup>_p_</sup> _t_<sup>_| ≤_15cm, clipped to 5mm/step, and stopped once</sup><sup>_|ep_</sup> _t_<sup>_| <_1</sup><sup>_._5cm.We adjust translation only</sup> because scaling the rotation residual the same way does not empirically improve tracking. 

## **4 A Modular System for Open-Vocabulary Humanoid Object Grasping** 

Our task is to pick up novel objects in novel environments from free-form language queries, using only onboard sensing. Our modular pipeline builds on HERO: Grounding DINO [16] detects the queried object, SAM-3 [17] segments it, and AnyGrasp [18] proposes parallel-jaw grasps. We filter and retarget the selected grasp to the Dex-3 hand before HERO executes the reach. Fig. 5 visualizes the pipeline; detailed filtering and retargeting steps are given in Sec. A.5. We use MOCAP to accurately calibrate the egocentric camera, Fig. 6 shows the MOCAP setup and camera calibration. 

For Dex3 retargeting, we rotate the AnyGrasp pose by 45° around the z-axis so the thumb opposes the other two fingers, improving contact area and force closure. We also clip end-effector rotation within 70° to avoid twisted IK postures that degrade tracking. 


**Figure 6: MOCAP and camera calibration.** (a) Using measured marker-to-link offsets, Kabsch– Umeyama [68, 69] recovers 6-DoF EE/base poses from MOCAP coordinates ( _<_ 1 _._ 5 mm RMSE). (b–c) The D435i camera is mounted on the G1 head with a passive neck pitch joint. (d–e) We manually move an ArUco board [70] with MOCAP markers through 60–70 poses, recording board poses in the camera frame and board/base poses in the MOCAP frame. Tsai–Lenz [71] then solves the camera-to-base transform. More details can be found in Sec. B.1 and Sec. B.2. 

6 

**Table 1: Open-vocabulary grasping success.** Compared with direct PD control and automated SONIC [15], HERO achieves 90% success across objects at two table heights. 

||**PD Co**|**ntroller**|**SONI**|**C [15]**|**O**|**urs**|
|---|---|---|---|---|---|---|
|**L**|Gen.|Short|Gen.|Short|Gen.|Short|
|**anguage Query**|0.74 m|0.56 m|0.74 m|0.56 m|0.74 m|0.56 m|
|red coke can|2/3|0/3|0/3|2/3|3/3|3/3|
|e-stop button|0/3|0/3|2/3|0/3|3/3|3/3|
|red piranha plant|0/3|0/3|0/3|0/3|3/3|3/3|
|orange cube|0/3|0/3|0/3|0/3|3/3|3/3|
|olive oil bottle|0/3|1/3|0/3|0/3|2/3|2/3|
|game cartridge|1/3|0/3|0/3|0/3|2/3|3/3|
|chip can|1/3|1/3|0/3|0/3|2/3|3/3|
|hand soap bottle|0/3|0/3|2/3|3/3|3/3|3/3|
|robot hand|0/3|0/3|0/3|0/3|3/3|2/3|
|red apple|0/3|0/3|0/3|1/3|3/3|2/3|
|**Total**|4/30|2/30|4/30|6/30|**27/30**|**27/30**|


**Figure 8: Open-vocabulary grasping in realworld scenes.** HERO achieves 22/30 (73.3%) success across broader novel scenes and 12/15 (80%) success in cluttered layouts. 

## **5 Experiments** 

We evaluate HERO on open-vocabulary grasping, learned FK, and tracking gains from residual feedback, replanning, and goal adjustment. 

Experiments use an _unmodified_ Unitree G1 humanoid with Dex-3 dexterous hands (3-finger hands), a head-mounted Intel D435i RGB-D camera, proprioception, and a base IMU. Visual trials use novel objects and environments; FK and tracking evaluations use a 13-camera Opti- 


track MOCAP room (see Sec. B.1). Selected design choices are validated in Isaac Gym [72] and MuJoCo [73]. In addition, Sec. A reports language sensitivity, moving-object grasping, door opening, walking FoV analysis, tracking-error CDFs, trajectory curves, and workspace coverage. 

### **5.1 End-to-end System Testing** 

**Experimental Setup.** Each trial starts 10-20 cm from a table (43-92cm high). The robot must grasp the queried object using onboard sensing and lift it for more than 2 seconds. We run 3 trials per object per table height; Fig. 7 shows the objects and Tab. 1 lists the queries. 

**Baselines.** We compare HERO to two alternate controllers. To maximally isolate the impact of the tracking quality, we plug in these alternate controllers into the same overall modular pipeline as HERO. _PD Controller_ tracks IK reference joints without a learned policy. For _SONIC_ [15], we use the three-point VR teleoperation interface. We use the predicted grasp as the right EE target and place the head and the left EE targets via FK from upper-body joint positions obtained from right EE IK. 

**Results:** ❶ **10 Daily Objects.** Tab. 1 shows that HERO succeeds in 90% of trials across objects, queries, and two table heights, _vs._ 10% for PD control and 16.7% for automated SONIC. Accurate whole-body end-effector tracking is essential for turning visual grasp goals into physical grasps. ❷ **10 Daily Scenes.** Fig. 8(a) evaluates broader scenes such as robot labs and classrooms, where HERO reaches 73.3% success. ❸ **5 Cluttered Layouts.** In cluttered layouts (Fig. 8(b)), HERO achieves 80% success without teleoperation demonstrations, remaining language-sensitive under distractors. On 1,450 queries constructed from OCID-Ref images [74], our perception module detects targets in 73.8% of canonical-name queries and 89.7% of queries with attributes and spatial relations (Tab. 7). 

### **5.2 End-effector Tracking Accuracy Evaluation and Ablation Study** 

We evaluate tracking on 180 reaching goals in simulation and real MOCAP: 60 poses across three table heights, sampled 5-15cm above the table. We report EE translation/orientation error against 

7 

**Table 2: Simulation tracking comparison.** End-effector translation, orientation, and jointtracking errors averaged over three table heights in MuJoCo. HERO attains the lowest error; SONIC lacks in EE tracking feedback and joint <u>position only baselines fall behind.</u> 

|**Method**|**Trans.**|**Orient.**|**Joint**|
|---|---|---|---|
||**(cm)**|**(deg)**|**(rad)**|
|FALCON [33]|13_._57_±_4_._41|19_._33_±_5_._30|**0**_._**02**_±_**0**_._**00**|
|AMO [25]|8_._29_±_3_._82|13_._85_±_5_._91|**0**_._**02**_±_**0**_._**00**|
|SONIC [15]|4_._10_±_2_._12|16_._65_±_9_._27|–|
|HERO (ours)|**2**_._**48**_±_**1**_._**15**|**11**_._**23**_±_**3**_._**97**|0_._17_±_0_._03|


**Table 3: Real-world tracking comparison.** MoCap-measured EE errors on hardware. HERO retains sub-3 cm accuracy in the real world, while SONIC baseline degrade by 4–5 _×_ compared to simulation. Lacking dynamic gravity compensation, the PD controller leaves the EE persistently low and misoriented. 

|**Method**|**Trans.**|**Orient.**|**Joint**|
|---|---|---|---|
||**(cm)**|**(deg)**|**(rad)**|
|PD Controller|12_._09_±_3_._14|40_._82_±_36_._27|0_._24_±_0_._03|
|SONIC [15]|13_._38_±_1_._43|16_._75_±_10_._06|–|
|HERO (full)|**2**_._**44**_±_**0**_._**86**|**8**_._**22**_±_**3**_._**52**|**0**_._**21**_±_**0**_._**05**|


**Table 4: Forward-model ablation.** Replacing analytic FK with our learned models reduces sim2real bias and approaches the MoCap oracle. 

|**EE**<br>**Pose**|**Base**<br>**Pose**|**Trans.**<br>**(cm)**|**Orient.**<br>**(deg)**|**Joint**<br>**(rad)**|
|---|---|---|---|---|
|FK|FK|4_._67_±_1_._30|14_._59_±_3_._99|0_._20_±_0_._03|
|Ours|FK|3_._35_±_0_._70|14_._07_±_3_._93|0_._19_±_0_._03|
|FK|Ours|3_._89_±_1_._06|14_._28_±_4_._75|0_._20_±_0_._04|
|Ours|Ours|**2**_._**56**_±_**1**_._**23**|**12**_._**06**_±_**4**_._**38**|**0**_._**18**_±_**0**_._**03**|
|_MoCap _|_MoCap _|_2.44 ± 0.86_|_8.22 ± 3.52_|_0.21 ± 0.05_|


**Table 5: Closed-loop feedback ablation.** Realworld MoCap tracking with replanning or goal adjustment removed. Replanning significantly improves tracking accuracy, while goal adjustment further reduces errors. 

|**Method**|**Trans.**|**Orient.**|**Joint**|
|---|---|---|---|
||**(cm)**|**(deg)**|**(rad)**|
|HERO (full)|**2**_._**44**_±_**0**_._**86**|**8**_._**22**_±_**3**_._**52**|0_._21_±_0_._05|
|w/o Replan|5_._17_±_2_._21|16_._13_±_4_._66|0_._21_±_0_._03|
|w/o Goal Adj.|2_._71_±_0_._87|9_._38_±_2_._72|**0**_._**20**_±_**0**_._**03**|


MOCAP and upper-body joint error from motors. Baselines include the PD controller, AMO [25], FALCON [33], and automated SONIC [15]. We also conduct ablation study on forward model accuracy (Sec. 3.2), closed-loop adapation strategies (Sec. 3.3). 

**Comparisons against state-of-the-art.** Tab. 2 reports simulation results averaged over three table heights. HERO achieves the lowest errors, with 2.48cm translation error versus 4.10cm for SONIC, 8.29cm for AMO, and 13.57cm for FALCON. SONIC is the closest translation baseline since it also reasons about EE targets, but its lack of end-effector error feedback leads to higher tracking error. The gap between joint and task-space metrics also shows that joint accuracy alone does not ensure end-effector accuracy. Tab. 3 shows the same trend on real-world MOCAP: full HERO achieves 2.44cm translation and 8.22<sup>_◦_</sup> orientation error, outperforming both PD control (12.09cm, 40.82<sup>_◦_</sup> ) and automated SONIC (13.38cm, 16.75<sup>_◦_</sup> ). In simulation, analytical FK and odometry are exact, so HERO uses them directly; replanning and goal adjustment remain enabled as in real-world deployment without further specifications. 

**Forward models and closed-loop adaptation.** Tab. 4 shows that learned EE/base estimates reduce analytical-FK bias and give the best non-oracle tracking accuracy. Using learned estimates for both EE and base poses reduces translation error from 4.67cm to 2.56cm, close to the MOCAP oracle at 2.44cm. Tab. 5 ablates the feedback terms on real hardware. Removing replanning roughly doubles translation error from 2.44cm to 5.17cm, while removing goal adjustment gives a smaller degradation. These results indicate that learned pose estimation and closed-loop replanning improve accuracy. 

|**Vanilla FK**_vs._ **Learned**<br>**FK.** We measure FK er-<br>ror by marking the robot<br>base and EE and us-<br>ing their MOCAP relative|**Table 6: FK and odomet**<br>errors from MOCAP; kin<br>**Method**|**ry accurac**<br>ematic calib<br>**a) End-eff**<br>**Translation**<br>**Error (cm)**|**y.** EE/base<br>ration and<br>**ector Pose**<br>**Rotation**<br>**Error (deg)**|translation<br>residuals re<br>**b) Base O**<br>**Translation**<br>**Error (cm)**|and rotation<br>duce bias.<br>**dometry**<br>**Rotation**<br>**Error (deg)**|
|---|---|---|---|---|---|
|transform as ground truth.|Analytical FK|1.30|6.03|1.00|0.49|
|We record poses and joint|Kinematic Calibration|0.58|**2.83**|**0.51**|0.51|
|<br>l th|Learned FK, no residual (ours)|4.44|7.06|0.53|0.75|
|anges, en compare our<br>method to a) analytical|Learned FK (ours)|**0.50**|3.18|0.52|**0.46**|


FK and b) kinematic calibration, where we learn URDF geometric model parameters [75–77]. 

8 


**Figure 9: Failure mode examples** . (a) Object slips from the hand. (b) Object knocked over. 


**Figure 10: Door opening with HERO** . (a) The egocentric RGB-D visual inputs. (b) Given a language query for the door handle ( _e.g._ , ‘‘fridge handle’’ prompted here), our modular system obtains the grasping pose, same as the pipeline for picking up objects. (c) The robot executes the reaching trajectory and closes the hand when reaching the target poses closely, and then returns to the default pose with the door opened. Note that while the door is heavy, HERO successfully manages to open the door with a smooth and stable door motion. 

Tab. 6 shows systematic bias in analytical FK for both EE pose and base odometry. FK corrections, through kinematic calibration or our residual model, reduce this bias. Ours achieves lower errors on 2 of 4 metrics, possibly because the neural model may be able to capture non-geometric effects ( _e.g._ , elasticity [51, 53]). While we use the neural model for HERO, this experiment suggests that the calibrated model would also offer improvements over the default calibration. 

### **5.3 Failure Mode Analysis** 

Fig. 9 shows two common failures: _object slipping_ on large or irregular objects, and _object knock-over_ when grasp orientation or hand size contacts unstable objects such as standing books. 

### **5.4 Extending HERO to Other Tasks Like Door Opening** 

As HERO constructed a modular system that coordinates high-level planning and low-level endeffector control, it reveals a possibility of extending HERO to broader tasks like door opening, which is a challenging loco-manipulation task [78–80]. In Fig. 10, we directly employ HERO to identify the target grasping pose for fridge door handle, followed by the same pipeline as object grasping, enabling the humanoid to grasp the fridge handle and finally open it when returning to the default position. Note that the door requires a large force to open because of magnetic attraction; we leave the door unlatched beforehand. This result shows _HERO_ ’s modular potential, and it is also possible to extend our system to broader loco-manipulation tasks by incorporating off-the-shelf trajectory generation frameworks [13, 81–83]. 

## **6 Discussions and Limitations** 

We present a modular humanoid system that separates open-vocabulary _action planning_ from simulator-trained _action controller_ , achieving 90% success on daily-object grasping without largescale real-world imitation. This decomposition lets large vision models handle visual generalization while a learned motion tracker executes whole-body reaching. The experiments show two lessons: task-space state must be accurate (analytical FK has 1.30cm EE error while ours reaches 0.50cm), and explicit error feedback during closed-loop execution effectively reduces real-world drifts (our tracker reaches 2.5cm error). Remaining limitations include restricted egocentric FoV for far or high targets, motivating active neck control and visual servoing [41, 84, 85]; inefficient motions, motivating learned motion priors; and modular failures [14, 83] plus dexterity limits, motivating better hands and retargeting. 

9 

## **Acknowledgement** 

We are grateful to the Coordinated Science Laboratory and the Center for Autonomy for access to experimental space and the G1 humanoid robot used in this work. We thank John Hart for his invaluable help with the humanoid robots. This material is based upon work supported by an NSF CAREER Award (IIS-2143873). 

## **References** 

- [1] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body locomanipulation and scene interaction. In _2026 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11691–11698. IEEE, 2026. 

- [2] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _Science Robotics_ , 11 (117):eadx8924, 2026. 

- [3] X. He, R. Dong, Z. Chen, and S. Gupta. Learning Getting-Up Policies for Real-World Humanoid Robots. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. 

- [4] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang. Learning Humanoid Standing-up Control across Diverse Postures. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. 

- [5] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbabu, C. Pan, Z. Yi, G. Qu, K. Kitani, J. K. Hodgins, L. Fan, Y. Zhu, C. Liu, and G. Shi. ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. 

- [6] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn. Humanplus: Humanoid shadowing and imitation from humans. In _8th Annual Conference on Robot Learning_ , 2024. 

- [7] Helix: A vision-language-action model for generalist humanoid control, 2025. URL https: //www.figure.ai/news/helix. 

- [8] Tesla. Artificial intelligence & autopilot, 2021. URL https://www.tesla.com/AI. 

- [9] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. M. Kitani, C. Liu, and G. Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. In _8th Annual Conference on Robot Learning_ , 2024. 

- [10] J. Barreiros, A. Beaulieu, A. Bhat, R. Cory, E. Cousineau, H. Dai, C.-H. Fang, K. Hashimoto, M. Z. Irshad, M. Itkina, et al. A careful examination of large behavior models for multitask dexterous manipulation. _arXiv preprint arXiv:2507.05331_ , 2025. 

- [11] T. He, Z. Wang, H. Xue, Q. Ben, Z. Luo, W. Xiao, Y. Yuan, X. Da, F. Castaneda, S. Sastry,˜ et al. Viral: Visual sim-to-real at scale for humanoid loco-manipulation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 13430–13441, 2026. 

- [12] M. Dalal, M. Liu, W. Talbott, C. Chen, D. Pathak, J. Zhang, and R. Salakhutdinov. Local policies enable zero-shot long-horizon manipulation. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 13875–13882. IEEE, 2025. 

- [13] Z. Qi, W. Zhang, Y. Ding, R. Dong, X. Yu, J. Li, L. Xu, B. Li, X. He, G. Fan, J. Zhang, J. He, J. Gu, X. Jin, K. Ma, Z. Zhang, H. Wang, and L. Yi. Sofar: Language-grounded orientation bridges spatial reasoning and object manipulation. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

10 

- [14] P. Liu, Y. Orru, J. Vakil, C. Paxton, N. M. M. Shafiullah, and L. Pinto. Demonstrating okrobot: What really matters in integrating open-knowledge models for robotics. In D. Kulic, G. Venture, K. E. Bekris, and E. Coronado, editors, _Robotics: Science and Systems XX, Delft, The Netherlands, July 15-19, 2024_ , 2024. 

- [15] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Castaneda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, et al.˜ Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [16] S. Liu, Z. Zeng, T. Ren, F. Li, H. Zhang, J. Yang, Q. Jiang, C. Li, J. Yang, H. Su, et al. Grounding dino: Marrying dino with grounded pre-training for open-set object detection. In _European conference on computer vision_ , pages 38–55. Springer, 2024. 

- [17] N. Carion, L. Gustafson, Y.-T. Hu, S. Debnath, R. Hu, D. S. Coll-Vinent, C. Ryali, K. V. Alwala, H. Khedr, A. Huang, J. Lei, T. Ma, B. Guo, A. Kalla, M. Marks, J. Greer, M. Wang, P. Sun, R. Radle, T. Afouras, E. Mavroudi, K. Xu, T.-H. Wu, Y. Zhou, L. Momeni, R. HAZRA, S. Ding,¨ S. Vaze, F. Porcher, F. Li, S. Li, A. Kamath, H. K. Cheng, P. Dollar, N. Ravi, K. Saenko, P. Zhang, and C. Feichtenhofer. SAM 3: Segment anything with concepts. In _The Fourteenth International Conference on Learning Representations_ , 2026. 

- [18] H.-S. Fang, C. Wang, H. Fang, M. Gou, J. Liu, H. Yan, W. Liu, Y. Xie, and C. Lu. Anygrasp: Robust and efficient grasp perception in spatial and temporal domains. _IEEE Transactions on Robotics_ , 39(5):3929–3945, 2023. 

- [19] X. B. Peng, P. Abbeel, S. Levine, and M. van de Panne. Deepmimic: example-guided deep reinforcement learning of physics-based character skills. _ACM Trans. Graph._ , 37(4):143, 2018. 

- [20] T. He, Z. Luo, W. Xiao, C. Zhang, K. Kitani, C. Liu, and G. Shi. Learning human-to-humanoid real-time whole-body teleoperation. In _IEEE/RSJ International Conference on Intelligent Robots and Systems, IROS 2024, Abu Dhabi, United Arab Emirates, October 14-18, 2024_ , pages 8944–8951. IEEE, 2024. 

- [21] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang. Expressive Whole-Body Control for Humanoid Robots. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, July 2024. 

- [22] Z. Qi, X. Chen, J. Wang, C. Lin, Y. Lian, W. Zhang, X. Yu, H. Wang, and L. Yi. Humanoid generative pre-training for zero-shot motion tracking. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 20834–20844, June 2026. 

- [23] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang. Exbody2: Advanced expressive humanoid whole-body control. In _RSS 2025 Workshop on Whole-body Control and Bimanual Manipulation: Applications in Humanoids and Beyond_ , 2025. 

- [24] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, J. Kautz, C. Liu, G. Shi, X. Wang, et al. Hover: Versatile neural whole-body controller for humanoid robots. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9989–9996. IEEE, 2025. 

- [25] J. Li, X. Cheng, T. Huang, S. Yang, R.-Z. Qiu, and X. Wang. AMO: Adaptive Motion Optimization for Hyper-Dexterous Humanoid Whole-Body Control. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. 

- [26] T. Portela, A. Cramariuc, M. Mittal, and M. Hutter. Whole-body end-effector pose tracking. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11205–11211. IEEE, 2025. 

- [27] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang. Gmt: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 

11 

- [28] Z. Zhang, C. Chen, H. Xue, J. Wang, S. Liang, Y. Liu, Z. Zhang, H. Wang, and L. Yi. Unleashing humanoid reaching potential via real-world-ready skill space. _IEEE Robotics and Automation Letters_ , 11(2):2082–2089, 2025. 

- [29] Z. Cao, L. Yan, Y. Zhang, S. Chen, J. Ma, T. Zhan, S. Fu, Y. Jia, C. Lu, and Y. Gao. Hiwet: Hierarchical world-frame end-effector tracking for long-horizon humanoid loco-manipulation. _arXiv preprint arXiv:2602.06341_ , 2026. 

- [30] X. Luo, X. Chen, X. Yin, H. Wu, B. Xia, Z. Chen, J. Li, B. Chen, and X. Cheng. Ceer: Compliant end-effector and root control as a unified interface for hierarchical humanoid loco-manipulation. _arXiv preprint arXiv:2605.19981_ , 2026. 

- [31] J. Ren, Y. Li, K. Zhang, P. Fu, H. Jiang, Y. Pan, G. Zeng, T. Huang, W. Guo, P. Lu, et al. Smash: Mastering scalable whole-body skills for humanoid ping-pong with egocentric vision. _arXiv preprint arXiv:2604.01158_ , 2026. 

- [32] Y. Li, Y. Zhang, W. Xiao, C. Pan, H. Weng, G. He, T. He, and G. Shi. Hold my beer: Learning gentle humanoid locomotion and end-effector stabilization control. In _Conference on Robot Learning_ , pages 4506–4523. PMLR, 2025. 

- [33] Y. Zhang, Y. Yuan, P. Gurunath, I. Gupta, S. Omidshafiei, A.-a. Agha-mohammadi, M. VazquezChanlatte, L. Pedersen, T. He, and G. Shi. Falcon: Learning force-adaptive humanoid locomanipulation. In _8th Learning for Dynamics & Control Conference_ , 2026. 

- [34] J. Jang, Z. Wang, Z. Zhou, F. Wu, and Y. Zhao. Seec: Stable end-effector control with modelenhanced residual learning for humanoid loco-manipulation. _arXiv preprint arXiv:2509.21231_ , 2025. 

- [35] C. Stanton, A. Bogdanovych, and E. Ratanasena. Teleoperation of a humanoid robot using full-body motion capture, example movements, and machine learning. In _Proc. Australasian Conference on Robotics and Automation_ , volume 8, page 51, 2012. 

- [36] O. Porges, M. Connan, B. Henze, A. Gigli, C. Castellini, and M. A. Roa Garzon. A wearable, ultralight interface for bimanual teleoperation of a compliant, whole-body-controlled humanoid robot. In _2019 International Conference on Robotics and Automation, ICRA 2019_ . IEEE, 2019. 

- [37] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang. HOMIE: Humanoid Loco-Manipulation with Isomorphic Exoskeleton Cockpit. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. 

- [38] Y. Ze, Z. Chen, J. P. Araujo, Z.-a. Cao, X. B. Peng, J. Wu, and K. Liu. Twist: Teleoperated whole-body imitation system. In J. Lim, S. Song, and H.-W. Park, editors, _Proceedings of The 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pages 2143–2154. PMLR, 27–30 Sep 2025. 

- [39] F. Liu, Z. Gu, Y. Cai, Z. Zhou, H. Jung, J. Jang, S. Zhao, S. Ha, Y. Chen, D. Xu, et al. Opt2skill: Imitating dynamically-feasible whole-body trajectories for versatile humanoid locomanipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- [40] C. Lu, X. Cheng, J. Li, S. Yang, M. Ji, C. Yuan, G. Yang, S. Yi, and X. Wang. Mobile-television: Predictive motion priors for humanoid whole-body control. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5364–5371. IEEE, 2025. 

- [41] L. Wei, X. Peng, R.-Z. Qiu, X. Cheng, and X. Wang. Hmc: Learning heterogeneous metacontrol for contact-rich loco-manipulation. In _RSS 2025 Workshop on Whole-body Control and Bimanual Manipulation: Applications in Humanoids and Beyond_ , 2025. 

- [42] T. Wu, X. Kong, Y. Chen, Q. Yu, H. Ye, J. Li, Y. Wang, and H. Dong. Sugar: A scalable human-video-driven generalizable humanoid loco-manipulation learning framework. _arXiv preprint arXiv:2605.20373_ , 2026. 

12 

- [43] K. Lin, A. Mandlekar, C. R. Garrett, N. Chernyadev, Y. Fang, R. Ding, Y. Xie, J. Tran, L. Fan, and Y. Zhu. Humanoidmimicgen: Data generation for loco-manipulation via whole-body planning, 2026. 

- [44] H. Ha, Y. Gao, Z. Fu, J. Tan, and S. Song. Umi-on-legs: Making manipulation policies mobile with manipulation-centric whole-body controllers. In _Conference on Robot Learning_ , pages 5254–5270. PMLR, 2025. 

- [45] M. Liu, Z. Chen, X. Cheng, Y. Ji, R.-Z. Qiu, R. Yang, and X. Wang. Visual whole-body control for legged loco-manipulation. In _Conference on Robot Learning_ , pages 234–257. PMLR, 2025. 

- [46] S. Yin, Y. Ze, H.-X. Yu, C. K. Liu, and J. Wu. Visualmimic: Visual humanoid loco-manipulation via motion tracking and generation. _arXiv preprint arXiv:2509.20322_ , 2025. 

- [47] Z. Liang, Y.-L. Wei, X. Chen, M. Lin, Y.-X. He, Z. Luo, J.-H. Liu, K.-Y. Lin, and W.-S. Zheng. Humanoid whole-body manipulation via active spatial brain and generalizable action cerebellum. _arXiv preprint arXiv:2605.21133_ , 2026. 

- [48] Z. Hu, Z. Xu, D. Chang, H. Yin, L. Tran, R. Mart´ın-Mart´ın, P. Stone, J. Qiao, and J. Biswas. Vofa: Visual object goal pushing with force-adaptive control for humanoids. _arXiv preprint arXiv:2605.01518_ , 2026. 

- [49] S. Wei, H. Jing, B. Li, Z. Zhao, J. Mao, Z. Ni, S. He, J. Liu, X. Liu, K. Kang, et al. _ψ_ 0: An open foundation model towards universal humanoid loco-manipulation. _arXiv preprint arXiv:2603.12263_ , 2026. 

- [50] B. Chen, Y. Chen, L. Qiu, J. Bai, Y. Ge, and Y. Ge. Unit: Toward a unified physical language for human-to-humanoid policy learning and world modeling. _arXiv preprint arXiv:2604.19734_ , 2026. 

- [51] M. Filipovic, V. Potkonjak, and M. Vukobratovi´ c.´ Elasticity in humanoid robotics. _Scientific Technical Review, Military Technical Institute, Belgrade_ , 1:24–33, 2007. 

- [52] J. Tenhumberg and B. Bauml.¨ Calibration of an elastic humanoid upper body and efficient compensation for motion planning. In _20th IEEE-RAS International Conference on Humanoid Robots, Humanoids 2021, Munich, Germany, July 19-21, 2021_ , pages 98–103. IEEE, 2021. 

- [53] J. Tenhumberg, D. Winkelbauer, D. Burschka, and B. Bauml.¨ Self-contained calibration of an elastic humanoid upper body using only a head-mounted RGB camera. In _21st IEEE-RAS International Conference on Humanoid Robots, Humanoids 2022, Ginowan, Japan, November 28-30, 2022_ , pages 702–707. IEEE, 2022. 

- [54] W. Yu, C. K. Liu, and G. Turk. Policy transfer with strategy optimization. In _7th International Conference on Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019_ . OpenReview.net, 2019. 

- [55] W. Yu, J. Tan, Y. Bai, E. Coumans, and S. Ha. Learning fast adaptation with meta strategy optimization. _IEEE Robotics Autom. Lett._ , 5(2):2950–2957, 2020. 

- [56] A. Kumar, Z. Fu, D. Pathak, and J. Malik. RMA: rapid motor adaptation for legged robots. In _Robotics: Science and Systems XVII, Virtual Event, July 12-16, 2021_ , 2021. 

- [57] Z. Fu, X. Cheng, and D. Pathak. Deep whole-body control: Learning a unified policy for manipulation and locomotion. In K. Liu and D. K. andD Jeffrey Ichnowski, editors, _Conference on Robot Learning, CoRL 2022, 14-18 December 2022, Auckland, New Zealand_ , volume 205 of _Proceedings of Machine Learning Research_ , pages 138–149. PMLR, 2022. 

- [58] N. Fey, G. B. Margolis, M. Peticco, and P. Agrawal. Bridging the Sim-to-Real Gap for Athletic Loco-Manipulation. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. 

13 

- [59] H. Wang, H. Luo, W. Zhang, and H. Chen. CTS: concurrent teacher-student reinforcement learning for legged locomotion. _IEEE Robotics Autom. Lett._ , 9(11):9191–9198, 2024. 

- [60] J. Tan, T. Zhang, E. Coumans, A. Iscen, Y. Bai, D. Hafner, S. Bohez, and V. Vanhoucke. Sim-to-real: Learning agile locomotion for quadruped robots. In H. Kress-Gazit, S. S. Srinivasa, T. Howard, and N. Atanasov, editors, _Robotics: Science and Systems XIV, Carnegie Mellon University, Pittsburgh, Pennsylvania, USA, June 26-30, 2018_ , 2018. 

- [61] J. Lee, A. Dosovitskiy, D. Bellicoso, V. Tsounis, V. Koltun, and M. Hutter. Learning agile and dynamic motor skills for legged robots. _Sci. Robotics_ , 4(26), 2019. 

- [62] Unitree. Unitree G1: Humanoid Agent AI Avatar. 2024. URL https://www.unitree. com/g1. 

- [63] B. Sundaralingam, S. K. S. Hari, A. Fishman, C. Garrett, K. Van Wyk, V. Blukis, A. Millane, H. Oleynikova, A. Handa, F. Ramos, et al. Curobo: Parallelized collision-free robot motion generation. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8112–8119. IEEE, 2023. 

- [64] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [65] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 5442–5451, 2019. 

- [66] Y. Zhou, C. Barnes, J. Lu, J. Yang, and H. Li. On the continuity of rotation representations in neural networks. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 5745–5753, 2019. 

- [67] Optitrack. URL https://optitrack.com/. 

- [68] W. Kabsch. A solution for the best rotation to relate two sets of vectors. _Foundations of Crystallography_ , 32(5):922–923, 1976. 

- [69] S. Umeyama. Least-squares estimation of transformation parameters between two point patterns. _IEEE Transactions on pattern analysis and machine intelligence_ , 13(4):376–380, 2002. 

- [70] S. Garrido-Jurado, R. Munoz-Salinas, F. J. Madrid-Cuevas, and M. J. Mar˜ ´ın-Jimenez. Automatic´ generation and detection of highly reliable fiducial markers under occlusion. _Pattern Recognition_ , 47(6):2280–2292, 2014. 

- [71] R. Y. Tsai, R. K. Lenz, et al. A new technique for fully autonomous and efficient 3 d robotics hand/eye calibration. _IEEE Transactions on robotics and automation_ , 5(3):345–358, 1989. 

- [72] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, and G. State. Isaac gym: High performance GPU based physics simulation for robot learning. In J. Vanschoren and S. Yeung, editors, _Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks 1, NeurIPS Datasets and Benchmarks 2021, December 2021, virtual_ , 2021. 

- [73] E. Todorov, T. Erez, and Y. Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems, IROS 2012, Vilamoura, Algarve, Portugal, October 7-12, 2012_ , pages 5026–5033. IEEE, 2012. 

- [74] K.-J. Wang, Y.-H. Liu, H.-T. Su, J.-W. Wang, Y.-S. Wang, W. Hsu, and W.-C. Chen. OCID-ref: A 3D robotic dataset with embodied language for clutter scene grounding. In _Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies_ , pages 5333–5338. Association for Computational Linguistics, 2021. doi:10.18653/v1/2021.naacl-main.419. 

14 

- [75] Z. Roth, B. Mooring, and B. Ravani. An overview of robot calibration. _IEEE Journal on Robotics and Automation_ , 3(5):377–385, 1987. 

- [76] D. Huczala, T. Kot, J. Mlotek, J. Suder, and M. Pfurner. An automated conversion between selected robot kinematic representations. In _2022 10th International Conference on Control, Mechatronics and Automation (ICCMA)_ , pages 47–52. IEEE, 2022. 

- [77] G. Franzese, M. Spahn, J. Kober, J. Alonso-Mora, and C. Della Santina. Accurate and affordable cobot calibration without external measurement devices. _Communications Engineering_ , 2026. 

- [78] A. J. Schmid, N. Gorges, D. Goger, and H. Worn. Opening a door with a humanoid robot using multi-sensory tactile feedback. In _2008 IEEE international conference on robotics and automation_ , pages 285–291. IEEE, 2008. 

- [79] E. Krotkov, D. Hackett, L. Jackel, M. Perschbacher, J. Pippine, J. Strauss, G. Pratt, and C. Orlowski. The darpa robotics challenge finals: Results and perspectives. In _The DARPA robotics challenge finals: Humanoid robots to the rescue_ , pages 1–26. Springer, 2018. 

- [80] H. Xue, T. He, Z. Wang, Q. Ben, W. Xiao, Z. Luo, X. Da, F. Castaneda, G. Shi, S. Sastry, et al.˜ Opening the sim-to-real door for humanoid pixel-to-action policy transfer. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 6642–6652, 2026. 

- [81] H. Huang, F. Lin, Y. Hu, S. Wang, and Y. Gao. Copa: General robotic manipulation through spatial constraints of parts with foundation models. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 9488–9495. IEEE, 2024. 

- [82] W. Huang, C. Wang, Y. Li, R. Zhang, and L. Fei-Fei. Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation. In _Conference on Robot Learning_ , pages 4573–4602. PMLR, 2025. 

- [83] A. Gupta, M. Zhang, R. Sathua, and S. Gupta. Demonstrating MOSART: Opening Articulated Structures in the Real World. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. 

- [84] H. Qi, Y.-J. Wang, T. Lin, B. Yi, Y. Ma, K. Sreenath, and J. Malik. Coordinated humanoid manipulation with choice policies. _arXiv preprint arXiv:2512.25072_ , 2025. 

- [85] Y. Ze, S. Zhao, W. Wang, A. Kanazawa, R. Duan, P. Abbeel, G. Shi, J. Wu, and C. K. Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. In _2026 IEEE International Conference on Robotics and Automation (ICRA)_ , 2026. 

- [86] J. Wang, M. Chen, N. Karaev, A. Vedaldi, C. Rupprecht, and D. Novotny. Vggt: Visual geometry grounded transformer. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 5294–5306, 2025. 

- [87] Y. Chen, Z. Qi, W. Zhang, X. Jin, L. Zhang, and P. Liu. Reasoning in space via grounding in the world. In _The Fourteenth International Conference on Learning Representations_ , 2026. 

- [88] T. Ren, Q. Jiang, S. Liu, Z. Zeng, W. Liu, H. Gao, H. Huang, Z. Ma, X. Jiang, Y. Chen, et al. Grounding dino 1.5: Advance the” edge” of open-set object detection. _arXiv preprint arXiv:2405.10300_ , 2024. 

- [89] H.-S. Fang, H. Yan, Z. Tang, H. Fang, C. Wang, and C. Lu. Anydexgrasp: General dexterous grasping for different hands with human-level learning efficiency. _arXiv preprint arXiv:2502.16420_ , 2025. 

- [90] A. Tabb and K. M. Ahmad Yousef. Solving the robot-world hand-eye (s) calibration problem with iterative methods. _Machine Vision and Applications_ , 28(5):569–590, 2017. 

15 

- [91] M. Shah, R. D. Eastman, and T. Hong. An overview of robot-sensor calibration methods for evaluation of perception systems. In _Proceedings of the Workshop on Performance Metrics for Intelligent Systems_ , pages 15–20, 2012. 

- [92] G. Bradski. The opencv library. _Dr. Dobb’s Journal: Software Tools for the Professional Programmer_ , 25(11):120–123, 2000. 

- [93] R. Y. Tsai. Efficient and accurate camera calibration technique for 3d machine vision. In _IEEE conference on computer vision and pattern recognition_ , 1985. 

- [94] M. Mittal, P. Roth, J. Tigue, A. Richard, O. Zhang, P. Du, A. Serrano-Munoz, X. Yao, R. Zurbrugg, N. Rudin, et al.¨ Isaac lab: A GPU-accelerated simulation framework for multimodal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. 

- [95] I. Loshchilov and F. Hutter. Decoupled weight decay regularization. In _International Conference on Learning Representations_ , 2019. 

- [96] J. Tobin, R. Fong, A. Ray, J. Schneider, W. Zaremba, and P. Abbeel. Domain randomization for transferring deep neural networks from simulation to the real world. In _2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 23–30, 2017. 

16 

**APPENDIX** 

|**A Add**|**itional Experimental Analysis**|**17**|
|---|---|---|
|A.1|Language Sensitivity . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . .<br>17|
|A.2|Tracking Error Distribution Analysis . . . . . . . . . . . . . . . . .|. . . . . . . .<br>18|
|A.3|Moving Object Grasping with Visual Replanning . . . . . . . . . .|. . . . . . . .<br>18|
|A.4|Field of View Analysis . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . .<br>18|
|A.5|Visual Perception Details . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . .<br>20|
|A.6|Analytical FK Error Visualization<br>. . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>21|
|A.7|Tracking Error Curves with and without Replanning . . . . . . . . .|. . . . . . . . .<br>21|
|A.8|Whole-Body Reaching Workspace Analysis . . . . . . . . . . . . .|. . . . . . . .<br>22|
|**B Add**|**itional Implementation Details**|**23**|
|B.1|MOCAP Setup<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . .<br>23|
|B.2|Onboard Egocentric RGB-D Camera . . . . . . . . . . . . . . . . .|. . . . . . . .<br>24|
|B.3|Hyper-parameters . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . .<br>24|
|B.4|Rewards . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . .<br>24|
|B.5|Policy Training . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . .<br>26|
|B.6|Deployment Hardware<br>. . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . .<br>26|
|B.7|Testing Assets Details . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . .<br>27|
|B.8|Testing Scenes Details<br>. . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . .<br>27|


## **A Additional Experimental Analysis** 

### **A.1 Language Sensitivity** 

We evaluate target detection on OCID-Ref images [74] using 1,450 language queries; Tab. 7 reports accuracy for selected query types. 

**Table 7: OCID-Ref query sensitivity.** Detection accuracy on our 1,450-query evaluation (58 classes, five views, five query types). Selected types are shown; overall includes all five. 

|Query type|Detection accuracy (%)|
|---|---|
|Canonical name|73.8|
|Canonical name + attribute|86.6|
|Canonical name + attribute + spatial relation|89.7|
|Overall (all five query types)|82.6|


Fig. 11 illustrates red- and green-apple selection among distractors in robot grasping. 

17 


**Figure 11: HERO is able to distinguish the target object via language queries.** (a) Picking up a red apple; (b) Picking up a green apple instead of red apple. 

### **A.2 Tracking Error Distribution Analysis** 

We visualize the CDFs of EE tracking errors in Fig. 12. 

**Top row.** HERO dominates all baselines: at 80%, HERO achieves 3.9 cm / 6.7<sup>_◦_</sup> (pos/rot), versus 20.9 cm / 25.3<sup>_◦_</sup> for FALCON and 9.8 cm / 19.5<sup>_◦_</sup> for AMO. At 90%, HERO remains below 4.6 cm and 8.2<sup>_◦_</sup> , indicating strong tail robustness. 

**Bottom row.** Replanning (Sec. 3.3) is critical: at 80%, HERO achieves 3.1 cm vs. 6.3 cm without replanning (2.1 _×_ worse), and at 90% 3.4 cm vs. 7.1 cm. Rotation gains are smaller but consistent (median 13.6<sup>_◦_</sup> vs. 16.1<sup>_◦_</sup> ). 

### **A.3 Moving Object Grasping with Visual Replanning** 

HERO derives target grasping poses from vision and language queries, enabling the robot to capture moving objects through closed-loop replanning. Fig. 13(a-b) illustrates this dynamic adaptation: while the system initially generates an EE trajectory based on the first vision perception, it re-estimates the pose as the object moves. This visual feedback triggers the update of the target grasp, allowing the robot to seamlessly adjust its trajectory and successfully secure the moving object. Note that, in these two trials, the robot successfully sees the object after moving, but the object can only be seen at the corner due to the rather limited field of view. 

### **A.4 Field of View Analysis** 

Our system uses the onboard camera for visual perception, which, however, has a limited field of view. As shown in Fig. 14, the robot first stands randomly at a distance of 1.28m from the object, while the target object (stapler) is not visible at this distance; after walking forward under a consistent velocity command to a distance of 0.6m and continuously detecting the object, the egocentric view successfully captures the target object, which makes the robot stops at about 0.5m from the object. Then the robot coordinates the whole-body reaching motion and successfully grasps the object. This visualization indicates that the robot’s onboard egocentric view is limited, and the robot can only see the object within a short distance ( _<_ 0 _._ 6m), which makes the availability of the 3D spatial understanding beforehand [14, 86, 87] critical for searching objects, which could be a future exploration. 

18 


**Figure 12: CDF analysis of end-effector tracking errors.** Top row: Comparison of translation (left) and rotation (right) error distributions across HERO, FALCON [33], and AMO [25] for all table heights. The steeper curves of HERO indicate consistently lower errors and tighter distributions. Bottom row: Ablation study showing translation (left) and rotation (right) error distributions with and without replanning (Sec. 3.3). The steeper CDF curves with replanning demonstrate their significant contribution to tracking accuracy. 


**Figure 13: HERO enables a humanoid to grasp a moving object via visual closed-loop replanning.** (a-b) Two examples of visual closed-loop replanning. The goal is to grasp black can. 

19 


**Figure 14: Field of view (FoV) visualization using HERO** . We let the robot stand at a random distance from the object ( _e.g._ , 1.28m), and the robot keeps walking forward until the target object (stapler) is detected.stapler) is detected.) is detected. After successfully detecting the target object, the robot stops walking and grasps the object via whole-body coordination. The robot can only see the object within 0.6m, which makes it hard for the robot to search for the object in a random room. 

**Figure 15: Visualization of analytical forward kinematics error** . We plot the 60 data points collected in the MOCAP room. The error is indicated in the color bar on the left side of the figure, and the size of the scatter also increases with the error. 

### **A.5 Visual Perception Details** 

Fig. 16 illustrates how HERO leverages LVMs to obtain the targeted EE grasping pose, following a modular perception-to-action design that is similar to prior systems [13, 14]. 

**Object of Interest from Language.** Given an ego-centric RGB-D observation and a natural-language query specifying the target object, HERO first applies GroundingDINO to produce a languageconditioned detection box [88]. The detected box is then used to prompt SAM-3 for segmentation of the object of interest [17]. 

**Grasp Proposals.** This mask serves as a spatial constraint for grasp proposal generation: HERO runs AnyGrasp [18] to produce a set of candidate grasps, and then filters out proposals outside the segmented object region. Note that AnyDexGrasp [89] can also be used here, but we find that the Dex-3 hand lacks dexterity, and the difference between these two methods is limited. 

**Grasp Selection.** To select the best jaw grasp, we first filter out the grasp poses that lie on the opposite side of the object relative to the robot’s hand ( _e.g._ , for an object to the right side of the hand, 

20 


**Figure 16: Visual perception for language-conditioned grasping.** Examples of target segmentation, grasp proposals, filtering, and retargeted EE poses from onboard RGB-D observations. 

the left approaching grasps are abandoned). Then we filter out grasps that are too high or too low based on a gravity-aligned height estimation of objects using depth. Afterward, we select the grasp that lies most parallel to the ground with the highest confidence as the final grasp. 

**Grasp Retargeting.** The selected grasp is retargeted to a 6-DoF end-effector pose for dexterous grasping with the Dex-3 hand. We first rotate the gripper pose by 45 degrees around the _z_ -axis to improve the grasp robustness and pose error tolerance. After that, we clip the yaw angle within 70 degrees to ensure the orientation is not too large. 

**Approach-angle sweep.** In a preliminary 0<sup>_◦_</sup> –90<sup>_◦_</sup> sweep, wrist distortion increased from 22<sup>_◦_</sup> to 104<sup>_◦_</sup> as the angle increased, while the observed object knock-over rate fell from 45 _._ 1% at 0<sup>_◦_</sup> to 7 _._ 4% at 45<sup>_◦_</sup> . We use the 45<sup>_◦_</sup> offset as a compromise between these effects. 

### **A.6 Analytical FK Error Visualization** 

In Fig. 15, we visualize the translation error of analytical forward kinematic results. We plot the error via the collected 60 samples in the MOCAP room, where the error is recorded when time is 1 minute. From the figure, we can observe that the error generally increases when the EE location becomes larger along the Y and Z axes, which may form a pattern that can be learned from a neural model. 

### **A.7 Tracking Error Curves with and without Replanning** 

Fig. 17 shows how end-effector tracking error evolves over the course of a real-world reach, complementing the aggregate ablations in Tab. 5. Without replanning, the error plateaus at a higher level because the policy commits to a stale reference; with replanning, the error continues to decrease as fresh references compensate for accumulated drift. The fact that HERO with learned _η, ξ_ closely tracks the MOCAP-oracle curve also confirms that our learned forward models suffice for accurate real-world deployment. 

21 


**Figure 17: Impact of replanning on end-effector tracking error in the real world** . We plot the end-effector translation error as a function of execution time steps. The plot shows 1 minute of execution at 50Hz. The transparent lines are individual 60 real-world rollouts, and the corresponding solid line indicates the average value. The gray vertical dashlines indicate the replanning every 6 seconds (0.15Hz). Cyan line shows HERO without replanning and while purple line shows HERO with re-planning. Re-planning leads to more accurate tracking. Orange line uses end-effector estimates from our neural model which leads to tracking performance very close to the oracle purple line that uses end-effector estimates from MOCAP. 

### **A.8 Whole-Body Reaching Workspace Analysis** 

We quantify how enabling torso motion via the waist DoFs affects end-effector reachability. We compare two kinematic settings: _i) arms-only_ , where IK optimizes the 14-DoF arm joints, and _ii) arms+waist_ , where IK additionally optimizes the 3-DoF waist (17 DoFs total). 

**Workspace estimation.** We define an axis-aligned 3D candidate region in the robot base frame: 


discretized at 0 _._ 02 m resolution. For each grid point **p** we attempt IK with cuRobo [63] under joint-limit constraints; a point is _reachable_ if the solver converges within a fixed iteration budget and the EE position residual lies below a preset tolerance. The workspace volume is approximated by voxel counting, 


where _N_ reach is the number of reachable points. 

**Effect of waist DoFs.** Tab. 8 reports the resulting volumes. Enabling the waist substantially enlarges reachability: the combined two-arm workspace grows from 0 _._ 248 m<sup>3</sup> to 0 _._ 523 m<sup>3</sup> ( _∼_ 2 _._ 1 _×_ ), and the single-arm workspace grows from 0 _._ 166 m<sup>3</sup> to 0 _._ 426 m<sup>3</sup> . Bending and twisting the torso effectively repositions the shoulder frame, allowing the EE to cover farther-forward and lower-height targets that are infeasible with a non-actuated waist. 

**Workspace showcase.** Fig. 18 illustrates HERO retrieving objects distributed across an expansive tabletop workspace. Every object is positioned beyond 0 _._ 4 m from the robot base, so the task requires whole-body coordination to reach precisely while remaining stable. HERO composes expressive whole-body motion with the precision needed for successful grasping. 

22 

**Table 8: Reachable workspace volume** across configurations. 


**Figure 18: HERO enables a humanoid picking up objects from a standard table (0** _._ **74m) across a large workspace with open-vocabulary queries.** (a-c) The robot can reach and pick up a red apple placed at different heights, poses, and locations. 

## **B Additional Implementation Details** 

### **B.1 MOCAP Setup** 

**MOCAP System.** We use the modern MOCAP system Optitrack [67] with 13 cameras which provides _≤_ 0 _._ 2mm measure accuracy. 

**Robot Link Pose.** To obtain the end-effector pose in the robot frame, we put several markers onto both links, and we show markers on the hand in Fig. 6(a). Although the MOCAP system provides constructed asset poses via selected marker groups, there exists a misalignment between the MOCAP asset frame and the robot link frame. To address this, we carefully measure each marker’s relative offset to the link’s origin, followed by the Kabsch-Umeyama (KU) algorithm [68, 69] that transforms individual marker coordinates into 6-DoF link pose in the MOCAP frame within _<_ 1 _._ 5mm RMSE error. The relative transformation of EE and the robot base is thus obtained as they are all in the MOCAP frame. This approach ensures an accurate measurement of both the end-effector and the robot base, setting a solid ground for our evaluation and camera calibration, introduced next. 

**Training-data quantity.** In a separate subsampling study, retraining the learned FK model with 100%, 50%, 25%, and 10% of a two-hour MOCAP dataset yielded mean EE translation errors of 0.51, 0.61, 0.68, and 0.70 cm, respectively. Base odometry remained usable with 25% of the data (about 30 minutes). 

23 

### **B.2 Onboard Egocentric RGB-D Camera** 

**Setup.** We use the onboard RGB-D camera D435i mounted on the humanoid’s head, as shown in Fig. 6(b). The humanoid’s neck features a pitch degree of freedom enabling head rotation within a limited range, necessitating precise camera calibration for accurate 3D perception. 

**Calibration with MOCAP.** Standard hand-eye calibration [90, 91] typically relies on analytical forward kinematics to obtain end-effector poses. However, as shown in Tab. 6, analytical forward kinematics has a mean EE translation error of 1.30 cm due to hardware inaccuracies, limiting its suitability for precise camera calibration. 

We instead leverage the MOCAP system for ground-truth pose measurement. Following the markerbased approach described previously, we attach reflective markers to an ArUco calibration board [70] and apply the KU algorithm [68, 69] for 6-DoF pose estimation. During data collection, we manually move the board through 60-70 diverse poses in front of the camera. For each pose _i_ , we record: 1) the robot base pose in MOCAP frame _T_ MOCAP<sup>base, 2) the board pose in MOCAP frame</sup><sup>_T_</sup> MOCAP<sup>board</sup><sup>_,i_, and 3)</sup> the board pose in camera frame _T_ camera<sup>board</sup><sup>_,i_via ArUco detection using the OpenCV library [92].</sup> 


using the Tsai-Lenz method [71, 93]. This MOCAP-assisted calibration achieves a reprojection error within 2.5mm, ensuring accurate egocentric 3D perception. 

**Image Resolution & FPS.** We use the RGB-D images with a resolution of 640 _×_ 480 in a 60Hz FPS. 

### **B.3 Hyper-parameters** 

**Motion planning** For motion planning, we use cuRobo and set the planning _dt_ to 7.25e-6. 

**Grasping Threshold** When the robot approaches the object, it autonomously close the hand when the hand distance to the target grasp **∆** **_E t_** _≤ δ_ where _δ >_ 0 is a threshold. At the moment when this threshold is reached, we pass the same local waypoint of the planned motion trajectory to the policy to ensure stability, and the hand is immediately closed for grasping. In this paper, we utilize a threshold of _δ_ = 1 _._ 5cm, which we find most effective across tested objects. 

### **B.4 Rewards** 

Tab. 9 summarizes reward components and weights used for RL training of _π_ t, which is structured into four categories: _tracking task_ , _penalties_ , _regularization_ , and _locomotion task_ . To ensure precise manipulation, the tracking rewards weigh the alignment of the end-effector based on our newly proposed residual **∆** **_E t_** . Note that EE orientation is represented with the continuous 6D parameterization (first two columns of the rotation matrix) [66]. To encourage the planned upper-body posture ( _e.g._ , waist bending or torso twisting), we also add a joint-space tracking term. Penalties strictly enforce safety constraints ( _e.g._ , joint limits, termination), while regularization terms—such as costs on torque, acceleration, and stance symmetry—are essential for generating smooth, stable motions capable of robust and natural Sim2Real transfer. To train the robot to follow locomotion commands, we also use a flag variable to control the standing and waking mode switching. 

**Table 9: Reward terms and nominal weights.** _m_ = 1 denotes walking ( _m_ = 0 standing); _hc_ is commanded base height, **g** _xy_ projected gravity, and _ep, eR_ EE position and mean axis-angle errors. Each weight multiplies the control-step duration; _†_ terms also use a penalty scale _s ∈_ [0 _,_ 1] initialized at 0 _._ 1. Here [ _x_ ]+ = max( _x,_ 0), and soft position bounds cover the central 95% of each joint range. 

|TERM|EXPRESSION|WEIGHT|
|---|---|---|
|**_Tracking task_**<br>EE position (stance)|(1_−m_) exp(_−∥ep∥_<sup>2</sup><br>2<sup>_/_0</sup><sup>_._05)</sup><br>|2_._0|
|EE orientation (stance)|(1_−m_) exp(_−eR/_0_._10)|2_._0|


Continued on next page 

24 

**Table 9 (continued)** 

|TERM|EXPRESSION|WEIGHT|
|---|---|---|
|Upper-body DoF|exp(_−∥_**q**arm_−_**q**<sup>ref</sup><br>arm<sup>_∥_2</sup><br>2<sup>_/_0</sup><sup>_._1)</sup>|4_._0|
|<br>Base height (stance)|(1_−m_) exp(_−|h −hc|/_0_._05)|4_._0|
|Base height (walk)|_m_exp(_−|h −hc|/_0_._05)|1_._0|
|<br>Waist DoF (stance)|<br>(1_−m_) exp(_−∥_**q**waist_−_**q**<sup>_c_</sup><br>waist<sup>_∥_2</sup><br>2<sup>_/_0</sup><sup>_._05)</sup><br>|3_._0|
|Waist DoF (walk)|_m_exp(_−∥_**q**waist_−_**q**<sup>_c_</sup><br>waist<sup>_∥_2</sup><br>2<sup>_/_0</sup><sup>_._05)</sup>|0_._5|
|**_Locomotion task_**|||
|Base velocity_x_<br>|exp(_−_(_vx −v_<sup>_c_</sup><br>_x_<sup>)2</sup><sup>_/_0</sup><sup>_._25)</sup><br><br>|2_._0|
|Base velocity_y_|exp(_−_(_vy −v_<sup>_c_</sup><br>_y_<sup>)2</sup><sup>_/_0</sup><sup>_._25)</sup>|1_._5|
|Base yaw rate|exp(_−_(_ωz −ω_<sup>_c_</sup><br>_z_<sup>)2</sup><sup>_/_0</sup><sup>_._25)</sup><br>|4_._0|
|Feet air time|1_∥_**v**_cxy∥_2_>_0_._1<br>�<br>_i_<br>1_t_air<br>_i_<br>_>_0|4_._0|
||1max(_Fizt,Fizt−_1)_>_1(_t_<sup>air</sup><br>_i_<br>+ ∆_t −_0_._5)||
|Foot-heading alignment|_,,,,_<br><br>�<br>_i∈{_L_,_R_} _<sup>_|_ wrap(</sup><sup>_ψi −ψ_base)</sup><sup>_|_</sup>|_−_0_._25|
|**_Regularization_**|||
|Lower-body torque<sup>_†_</sup>|_∥_**_τ_**lower_∥_<sup>2</sup><br>2|_−_10<sup>_−_5</sup>|
|Upper-body torque<sup>_†_</sup>|_∥_**_τ_**upper_∥_<sup>2</sup><br>2|_−_10<sup>_−_5</sup>|
|Lower-body DoF velocity<sup>_†_</sup><br>|_∥_˙**q**lower_∥_<sup>2</sup><br>2<br>|_−_10<sup>_−_3</sup><br>|
|Upper-body DoF velocity<sup>_†_</sup><br>|_∥_˙**q**upper_∥_<sup>2</sup><br>2<br>|_−_10<sup>_−_3</sup><br>|
|Lower-body DoF acceleration<sup>_†_</sup>|_∥_( ˙**q**_t −_˙**q**_t−_1)lower_/_∆_t∥_<sup>2</sup><br>2|_−_2_._5_×_10<sup>_−_7</sup>|
|Upper-body DoF acceleration<sup>_†_</sup><br>|_∥_( ˙**q**_t −_˙**q**_t−_1)upper_/_∆_t∥_<sup>2</sup><br>2<br>|_−_2_._5_×_10<sup>_−_7</sup>|
|Lower-body action rate<sup>_†_</sup><br>|_∥_**a**lower_,t −_**a**lower_,t−_1_∥_<sup>2</sup><br>2<br>|_−_0_._1|
|Upper-body action rate<sup>_†_</sup>|_∥_**a**upper_,t −_**a**upper_,t−_1_∥_<sup>2</sup><br>2|_−_0_._1|
|<br>EE linear-velocity change|�<br>_i∈{_L_,_R_} _<sup>_∥_</sup><sup>**v**EE</sup><br>_i,t _<sup>_−_</sup><sup>**v**EE</sup><br>L_,t−_1<sup>_∥_2</sup><br><br>|_−_0_._2|
|EE angular-velocity change|�<br>_i∈{_L_,_R_} _<sup>_∥_</sup><sup>**_ω_**EE</sup><br>_i,t _<sup>_−_</sup><sup>**_ω_**EE</sup><br>R_,t−_1<sup>_∥_2</sup>|_−_0_._02|
|Base vertical velocity|_m_(_v_<sup>base</sup><br>_z_<br>)<sup>2</sup>|_−_2_._0|
|Base angular velocity|_∥_**_ω_**<sup>base</sup><br>_xy _<sup>_∥_2</sup><br>2<br><br>|_−_0_._05|
|Torso angular velocity|_∥_**_ω_**<sup>torso</sup><br>_xy_<br>_∥_<sup>2</sup><br>2<br><br>|_−_1_._0|
|Base orientation|_∥_**g**<sup>base</sup><br>_x _<sup>_∥_2</sup><br>2|_−_1_._5|
|Torso orientation|_y _<br><br>_∥_**g**<sup>torso</sup><br>_xy_<br>_∥_1<br>|_−_1_._0|
|Base-height deviation|(5_−_4_m_)(_h −hc_)<sup>2</sup>|_−_10_._0|
|Hip roll/yaw position|[_m_+ (1_−m_)_hc_]_∥_**q**hip_,_roll_/_yaw_∥_<sup>2</sup><br>2|_−_2_._5|
|Stance DoF velocity|(1_−m_)_∥_˙**q**lower_∥_<sup>2</sup><br>2|_−_10<sup>_−_3</sup>|
|Stance symmetry|(1_−m_)(_∥_**q**<sup>_s_</sup><br>L <sup>_−_</sup><sup>**q**</sup><sup>_s_</sup><br>R<sup>_∥_1</sup> <sup>+</sup><sup>_∥_</sup><sup>**q**</sup><sup>_a_</sup><br>L <sup>+</sup><sup>**q**</sup><sup>_a_</sup><br>R<sup>_∥_1)</sup>|_−_0_._5|
|Ankle roll|_|q_ankle_,_L_|_+_|q_ankle_,_R_|_|_−_2_._0|
|Stance root offset|(1_−m_)_|_[_R_<sup>_⊤_</sup><br>pel<sup>(</sup><sup>**p**</sup>pel|_−_5_._0|
||_−_<sup>1</sup><br>2<sup>(</sup><sup>**p**L +</sup><sup>**p**R))]</sup><sup>_y|_</sup>||
|Stance foot offset|(1_−m_1_|vcx|>_0)|_−_5_._0|
||_|_[_R_<sup>_⊤_</sup><br>pel <sup>abs(</sup><sup>**p**</sup>L <sup>_−_</sup><sup>**p**</sup>R<sup>)]</sup>_x_<sup>_|_</sup>||
|Zero-command translation|_m_1_∥_**v**_c∥<_0_._2_∥_**v**<sup>root</sup><sup>_,_world</sup><br>_xy_<br>_∥_2|_−_1_._5|
|Zero-command rotation|_xy_<br><br>_m_1_|ωcz|<_0_._1_|ω_<sup>root</sup><sup>_,_world</sup><br>_z_<br>_|_|_−_1_._5|
|Contact slip|(10_−_9_m_)<br>�<br>1_∥_**F**_i∥_2_>_1|_−_0_._2|
||_i_<br>_∥_**v**<sup>foot</sup><br>_i_<br>_∥_<sup>2</sup><br>2||
|Foot-contact pattern|(1_−m_)1_nf <_2+_m_1_nf̸_=1_,_|_−_4_._0|
||_̸_<br>_nf_ =<br>�<br><br>1_Fi,z>_1||
|Standing foot contact|_i_<br>(1_−m_)1min_i Fiz<_0_._1|_−_0_._15|
|<br>Feet orientation|_,_<br>�<br>_i∈{_L_,_R_} _<sup>_∥_</sup><sup>**g**</sup><sup>_i_</sup><br>_xy_<sup>_∥_</sup>2|_−_2_._0|
|Foot target height|_m_[min_i |zi −_0_._11_| −_0_._02]+|_−_5_._0|
|Swing-foot height|�<br>|_−_20_._0|
||_i_:_∥_**F**_i∥_2_≤_1||
||(_zi −_0_._11_m −_0_._025(1_−m_))<sup>2</sup>||


Continued on next page 

25 

**Table 9 (continued)** 

|TERM|EXPRESSION|WEIGHT|
|---|---|---|
|Feet too close|1_∥_**p**<sup>_xy_</sup><br>L <sup>_−_</sup><sup>**p**</sup><sup>_xy_</sup><br>R <sup>_∥_2</sup><sup>_<_0</sup><sup>_._17</sup>|_−_10_._0|
|Knee below threshold|�<br>_i∈{_L_,_R_}_ <sup>1</sup><sup>_q_</sup>knee_,i_<sup>_<_0</sup><sup>_._2</sup><br><br>|_−_1_._0|
|Feet air-time asymmetry|_|t_<sup>last</sup><br>L<br>_−t_<sup>last</sup><br>R <sup>_|_</sup>|_−_5_._0|
|**_Penalties_**|||
|Lower-body DoF position limit<sup>_†_</sup><br>|�<br>_j∈_lower <sup>dist(</sup><sup>_qj,_ [</sup><sup>_q_soft</sup><br>_j,_min<sup>_, q_soft</sup><br>_j,_max<sup>])</sup><br><br>|_−_5_._0|
|Upper-body DoF position limit<sup>_†_</sup><br>|�<br>_j∈_upper <sup>dist(</sup><sup>_qj,_ [</sup><sup>_q_soft</sup><br>_j,_min<sup>_, q_soft</sup><br>_j,_max<sup>])</sup>|_−_5_._0|
|Upper-body DoF velocity limit<sup>_†_</sup><br>|�<br>_j∈_upper <sup>min</sup><sup>_{_1</sup><sup>_,_ [</sup><sup>_|_ ˙</sup><sup>_qj| −_˙</sup><sup>_qj,_max]+</sup><sup>_}_</sup>|_−_5_._0|
|Upper-body torque limit<sup>_†_</sup>|�<br>_j∈_upper<sup>[</sup><sup>_|τj| −_0</sup><sup>_._9</sup><sup>_τ_max</sup><sup>_,j_]+</sup><br>|_−_0_._1|
|Termination|_b_reset(1_−b_timeout)|_−_250|


### **B.5 Policy Training** 

**Simulation & Training Setup.** We train our end-effector tracking policy _π_ t in Isaac Gym [72] or Isaac Sim via Isaac Lab [94], and transfer this policy to the MuJoco simulator [73] for Sim2Sim evaluations before deploying it in the real world. We train our policy with 4,096 environments for overall 20K iterations in parallel, with a learning rate of 1e-4 for both the actor and critic models. AdamW optimizer [95] is used with a weight decay of 1e-2. We use a high simulation frequency of 500Hz, with the low-level PD controller running at 50Hz. All the policy training is conducted on a single NVIDIA RTX 4090 or an L40S GPU. 

**Sim2Real Domain Randomization.** Following previous works [3, 5, 9], we employ standard domain and dynamics randomization to facilitate Sim2Real transfer [96], including variations in link center of mass (CoM) and control delay. Notably, we identify that randomizing the _end-effector mass_ is essential; without this specific randomization, the policy exhibits end-effector instability, leading to high-frequency hand oscillations that compromise tracking accuracy. 

### **B.6 Deployment Hardware** 

We run all modules ( _e.g._ , _π_ t and SAM-3 [17]) off-the-shelf on a 32-GB RAM laptop equipped with NVIDIA RTX 5070Ti GPU and Intel Core Ultra 9 275HX CPU processor (24 CPU cores / 24 threads). We run cuRobo with CUDA graph acceleration, which largely improve the efficiency on the edge [63]. For the detection module, we have tested both Grounding DINO base [16] and Grounding DINO 1.5 [88], where the base version can be deployed on the laptop, and Grounding DINO 1.5 only provides access through online APIs. However, we find that Grounding DINO base is sufficient for most scenes and objects. Tab. 10 reports deployment runtime; conservative robot motion accounts for most of the roughly 55-second execution. 

**Table 10: Deployment runtime.** Measured on the local laptop with Grounding DINO base. GroundingSAM and AnyGrasp are included in perception; replanning is a per-update latency and is not an additional phase in the total. 

|Phase or component|Time|
|---|---|
|Perception (query to grasp)|1.33 s|
|GroundingSAM|950 ms|
|AnyGrasp|377 ms|
|Reaching|20.39 s|
|Closure|1.20 s|
|Return|32.14 s|
|Total (four phases)|_≈_55s|
|Replanning (per update)|_≈_20ms|


26 

### **B.7 Testing Assets Details** 

In the paper, we have tested HERO with 20 daily objects; these objects have different sizes and weights, while being made with different materials, making it challenging to grasp with a Dex-3 hand. We list the detailed sizes, weights, materials, and language queries of all objects tested in Tab. 11. Note that the size is roughly measured as the shape is irregular and cannot be easily described. 

### **B.8 Testing Scenes Details** 

Tab. 12 lists the details of the novel scenes tested in this paper, which are mainly chosen from Coordinated Science Laboratory Studio (CSL Studio) and the Thomas M. Siebel Center for Computer Science at the University of Illinois Urbana-Champaign, Urbana, IL. The snapshot of these testing scenes can be found in Fig. 8. 

27 

**Table 11: Testing objects, sizes, weights, materials, and language queries.** Sizes are roughly measured due to irregular shapes. Weights are measured with an accurate food scale. 

|**Object **|**Size**|**Weight**|**Material**|**Language Query**|
|---|---|---|---|---|
|_10 daily_|_object evaluation._||||
||4.9_×_4.9_×_4.9 cm|58.06 g|Wood|orange cube|
||12_×_6_×_6 cm|14.97 g|Aluminum|coke can|
||8.5_×_7.5_×_7.5 cm|15.88 g|Plastic|red apple|
||9_×_5_×_5 cm|137.89 g|Plastic & Metal|emergency stop<br>button|
||15_×_6_×_5 cm|239.95 g|Plastic & Metal|robot hand|
||16.5_×_10.5_×_3.3 cm|185.07 g|Plastic|game cartridge|
||27.5_×_9.5_×_9.5 cm|79.83 g|Plastic|olive oil bottle|
||16_×_8.5_×_8.5 cm|392.81 g|Plastic & Liquid|hand soap|
||23_×_7.9_×_7.9 cm|43.09 g|Paperboard & Plastic|chip can|
||17_×_11_×_11 cm|73.94 g|Plush|red piranha plant|
|_10 daily_|_objects used in 10 da_|_ily scenes eva_|_luation._||
||21_×_12_×_43 cm|215.91 g|Plastic|kettle|
||16.5_×_11_×_21 cm|213.19 g|Plush|toy dog|
||17.2_×_9_×_9 cm|24.95 g|Paperboard & Plastic|Starbucks coffee|
||11.5_×_9.4_×_9.4 cm|526.17 g|Ceramic|orange mug|
||18.5_×_6.3_×_6.3 cm|286.22 g|Plastic & Metal|water bottle|
||7_×_7.7_×_7.7 cm|14.97 g|Plastic|green apple|
||18.8_×_2.4_×_13.3 cm|301.19 g|Paper|purple book|
||14_×_8_×_39 cm|234.96 g|Plastic & Metal|helicopter|
||8_×_5.6_×_10 cm|367.41 g|Metal & Spam|spam|
||19_×_5_×_5 cm|86.18 g|Plastic & Liquid|cleaner bottle|


Continued on next page 

28 

|**Object **|**Size**|**Weight**|**Material**|**Language Query**|
|---|---|---|---|---|
|_Additio_|_nal objects._||||
||24.5_×_8_×_6.5 cm|135.17 g|Plush|carrot|
||23_×_8_×_8 cm|307.08 g|Plush|broccoli|
||7.5_×_7.2_×_7.5 cm|19.05 g|Plastic|orange|
||21_×_2.3_×_13.8 cm|376.03 g|Paper|book|
||15.3_×_6.5_×_6.5 cm|18.14 g|Aluminum|black can|


**Table 12: Testing scenes, table heights, language queries.** Here we list the novel scenes chosen in this paper for evaluation, and the corresponding table height. The snapshot of these scenes can be found in Fig. 8. 

|**Scene**|**Location**|**Table**<br>**Height**|**Language Query**|
|---|---|---|---|
|corridor|CSL Studio UIUC|0.43m|kettle|
|office lounge|CSL Studio UIUC|0.48m|toy dog|
|building caf´e|Siebel CS Building UIUC|0.72m|Starbucks coffee|
|office|CSL Studio UIUC|0.74m|orange mug|
|building lounge|Siebel CS Building UIUC|0.74m|water bottle|
|office kitchenette|CSL Studio UIUC|0.74m|green apple|
|building den|Siebel CS Building (RM 3333)<br>UIUC|0.74m|purple book|
|robotics lab|CSL Studio UIUC|0.86m|helicopter|
|office kitchen|CSL Studio UIUC|0.87m|spam|
|classroom|Siebel CS Building (RM 1302)<br>UIUC|0.92m|cleaner bottle|


29 

