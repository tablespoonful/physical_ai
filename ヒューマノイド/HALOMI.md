---
title: "HALOMI: Learning Humanoid Loco-Manipulation with Active Perception from Human Demonstrations"
date: "2026-06-17"
authors: "Zehui Zhao; Yuxuan Zhao; Gaojing Zhang; Chenxi Liu; Maolin Zheng; Wenzhao Lian"
url: https://arxiv.org/abs/2606.18772
pdf: https://arxiv.org/pdf/2606.18772
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.18772)** / [論文ページ](https://arxiv.org/abs/2606.18772)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **HALOMI: Learning Humanoid Loco-Manipulation with Active Perception from Human Demonstrations** 

Zehui Zhao<sup>1</sup><sup>_,∗_</sup> , Yuxuan Zhao<sup>1</sup><sup>_,∗_</sup> , Gaojing Zhang<sup>1</sup><sup>_,_2</sup> , Chenxi Liu<sup>3</sup> , Maolin Zheng<sup>3</sup> , Wenzhao Lian<sup>1</sup><sup>_,†_</sup> 

> 1Shanghai Jiao Tong University 2University of Sussex 

- 3East China University of Science and Technology 

   - _∗_ Equal Contribution, _†_ Corresponding Author 


**Fig. 1. Humanoid Active-Perception Loco-Manipulation Interface (HALOMI).** Human demonstrations are collected with UMI-style handheld grippers and wearable egocentric sensing. The data processed by the human data processing module are used to train a high-level VLA that predicts head-hand targets. The head-hand targets are then executed by a manifold-constrained whole-body controller on the humanoid robot. 

**_Abstract_ —Human demonstrations, which can be collected at** 

**scale and naturally capture active hand-eye coordination, are a promising data source for learning humanoid loco-manipulation. However, directly transferring human demonstrations to humanoids requires a precise world-frame tracking controller, which is often brittle under Out-of-Distribution(OOD) targets, while human-to-humanoid gaps persist in both egocentric observation and action execution. To address these challenges, we present HALOMI, a scalable framework for learning humanoid loco-manipulation with active perception from human demonstrations. HALOMI extends Universal Manipulation Interface (UMI) with egocentric sensing to collect ego-view and wristview observations along with head-hand trajectories at scale. We further propose a manifold-constrained controller that plans in a learned latent behavior manifold to enable precise and robust head-hand tracking in the world frame. To bridge the human–to-humanoid gap, we perform ego-view alignment and introduce a controller-aware reference trajectory adaptation to reduce mismatch in both observation and action execution. We validate HALOMI on a Unitree G1 humanoid robot with an actuated neck across five real-world tasks involving navigation,** 

**grasping, bimanual manipulation, whole-body coordination, and dynamic behaviors. Across the three quantitatively evaluated tasks, HALOMI achieves an average success rate of 85%, while additional qualitative demonstrations show its ability to support dynamic tossing and deep-squat grasping. Our project website can be found at https://halomi-humanoid.github.io** 

## I. INTRODUCTION 

Humanoid robots, with their human-like morphology and capacity for flexible whole-body coordination, are promising robotic platforms for operating in unstructured human-centric environments. However, collecting large-scale teleoperated demonstrations for humanoids remains difficult, as wholebody teleoperation is costly, time-consuming, and requires access to physical humanoid platforms as well as skilled operators. 

Meanwhile, human demonstrations provide an appealing alternative for scaling humanoid loco-manipulation vision- 

language-action (VLA) models, as they can be collected without costly real-robot teleoperation. Beyond scalability, human demonstrations are ego-view-guided action data. Humans coordinate head and hand motions to maintain task-relevant visual context, enabling long-horizon tasks with multi-stage gaze changes such as search, grasping, and placement [1]. Since the demonstrated actions are generated under actively changing ego-view observations, active perception is also required to transfer such data to humanoids. 

Robot-free demonstration frameworks have combined UMIstyle handheld interfaces [2] with egocentric sensing to collect human demonstrations that capture hand-object interactions and active viewpoint behaviors [3]–[5]. These systems demonstrate the value of human demonstrations for learning manipulation tasks that require hand-eye coordination, yet they primarily focus on fixed-base or wheeled robotic platforms. 

Recent works have extended robot-free demonstrations to humanoid loco-manipulation by augmenting UMI interfaces with additional lower-body references, such as pelvis or foot targets [6], [7]. These additional references help specify humanoid whole-body motion, but require access to lower-body information during data collection. Moreover, these systems do not study active ego-view transfer from humans to humanoids, limiting their applicability to long-horizon tasks that require continual gaze changes. 

Motivated by these limitations, we adopt a task-centric head-hand demonstration interface that captures manipulationrelevant hand motions and active head movements, while a whole-body controller completes the whole-body motion required for stable execution. However, this interface introduces additional challenges, including (1) the ego-view observation gap between humans and humanoids due to morphology and camera-pose differences, (2) directly executing world-frame head-hand trajectories with unspecified lower-body commands is brittle and unstable for the whole-body controller, (3) human demonstrations provide desired head-hand target states, while directly feeding these targets to the humanoid whole-body controller can yield non-negligible tracking errors, thereby degrading human-to-humanoid transfer. 

To address these challenges, we present the **H** umanoid **A** ctive-Perception **Lo** co- **M** anipulation **I** nterface ( **HALOMI** ), as illustrated in Fig. 1, a general and scalable framework for **learning humanoid loco-manipulation with active perception from human demonstrations** . HALOMI includes a **UMI-augmented egocentric data collection** protocol, a **manifold-constrained whole-body controller** for robust and precise tracking of head-hand targets, and an **automated human data processing procedure** to reduce the humanto-humanoid gap. The main contributions of our system are summarized as follows: 

- **HALOMI Data Collection System:** We develop a robotfree egocentric data collection system that combines bimanual UMI-style handheld grippers with a wearable head-mounted egocentric sensing, enabling synchronized collection of multi-view visual observations and corresponding hand-eye motion trajectories. 

- **Manifold-Constrained Whole-Body Controller:** We develop a manifold-constrained reinforcement learning (RL) 

controller that tracks a unified set of head-hand worldframe targets to bridge the high-level VLA action interface and humanoid whole-body execution. Instead of tracking in the joint action space, the controller plans over a learned latent behavior manifold, enabling precise and robust world-frame tracking. 

- **View Alignment & Reference Trajectory Adaptation:** We introduce an automated offline data processing pipeline to reduce the human-to-humanoid embodiment gap in both observation and action spaces. View alignment mitigates visual discrepancies caused by viewpoint mismatch, while controller-aware reference trajectory adaptation reduces execution errors of human head-hand trajectories, mitigating error accumulation during closedloop rollouts. 

- **Hierarchical Learning Framework for Human-toHumanoid Transfer:** We train a high-level VLA policy from scalable human demonstrations processed by the automated data processing pipeline. The VLA policy takes ego-view and dual-hand visual observations as input and predicts head-hand targets, which are then executed by the manifold-constrained whole-body controller for humanoid execution. We conduct real-world experiments on a Unitree G1 humanoid across diverse loco-manipulation tasks, demonstrating effective human-to-humanoid skill transfer. 

## II. RELATED WORK 

## _A. Robot-Free Human Demonstrations_ 

Robot-free demonstrations have emerged as a scalable pathway for robot policy learning without relying on realrobot teleoperation. UMI-style interfaces have shown effective transfer to fixed-base manipulators [2], [8], [9] and have been extended to mobile embodiments [4], [6], [7], [10]. For robotfree human demonstrations with active perception, egocentric sensing captures not only visual observations, but also human head motions that actively reveal task-stage-specific context during long-horizon manipulation [3], [5]. HALOMI builds on these directions by augmenting UMI-style hand-trajectory collection with wearable egocentric head sensing, capturing both hand-object interaction and active viewpoint behavior for humanoid loco-manipulation. 

## _B. Humanoid Whole-Body Controller_ 

Recently, RL-based controllers for humanoid robots have achieved impressive sim-to-real performance, enabling humanoids to perform diverse loco-manipulation tasks. HOMIE [11] and AMO [12] adopt a decoupled humanoid controller, where upper-body motion is specified by joint-space targets and the RL controller handles lower-body locomotion and balance. Another line of work builds on the motion-tracking paradigm [13], [14], enabling humanoids to reproduce humanlike whole-body motions. Recent systems [15], [16] operate in the global frame to reduce global drift during teleoperation. In addition, motion-prior and latent-space controllers [17]–[19] have been explored to constrain whole-body control within 


**(a) (b)** 

Fig. 2: **Hardware overview of the proposed system:** (a) human data collection setup and (b) robot hardware platform. 

a learned behavior manifold, improving motion feasibility compared with unconstrained joint-space tracking. Executing recorded human head-and-hand trajectories requires precise world-frame sparse keypoint tracking, which is sensitive to localization errors and infeasible commands. Since pelvis, foot, and lower-body references are not provided, the controller must infer the remaining whole-body motion from only head-hand targets. Together, these factors make the sparse world-frame tracking challenging. HALOMI therefore adopts the manifold-constrained controller, which tracks the head-hand targets by planning over a learned latent behavior manifold, enabling precise and robust world-frame tracking. 

## _C. Whole-Body Policy Learning from Human Demonstrations_ 

EgoHumanoid [20] attempts to transfer the human egocentric data to the humanoid robot via view and action alignment and human-robot co-training. HoMMI [4] integrates a 3D egocentric representation with a look-at-point head interface to mitigate the embodiment gap for whole-body mobile manipulation. 

HuMI [6] and BifrostUMI [7] extend UMI-style robot-free demonstrations to humanoid loco-manipulation by augmenting hand trajectories with additional lower-body references, such as pelvis and foot targets. These additional references help specify humanoid whole-body motion, but they also require demonstrators to provide lower-body information and rely on morphology-aware adaptation or retargeting for execution. Since pelvis and foot targets lack direct visual anchors, VLApredicted lower-body references can be prone to long-horizon drift. Moreover, both systems do not explicitly include active perception, limiting their applicability to long-horizon tasks that require continual gaze changes. In contrast, HALOMI uses head-hand targets as a task-centric and embodimentagnostic interface. A unified manifold-constrained wholebody controller executes these sparse targets and completes the remaining whole-body motion, while an automated dataprocessing pipeline reduces human-to-humanoid gaps in egocentric observation and action execution. These designs aim to reduce the burden of data collection and enable robot-free human demonstrations with active gaze behaviors to serve 


Fig. 3: **Illustration of the 3-DoF active neck motion:** initial state, positive yaw, positive pitch, and positive roll. as a scalable source for learning humanoid loco-manipulation skills. 

## III. PROPOSED FRAMEWORK 

HALOMI consists of four main components, including a scalable and intuitive human data collection system paired with a humanoid platform (Sec. III-A), a unified wholebody RL controller for precise and robust head-hand target tracking (Sec. III-B), an automated offline alignment pipeline for processing raw human demonstrations (Sec. III-C), and the high-level VLA training and deployment pipeline (Sec. III-D). 

## _A. Data Collection & Robot System_ 

**Scalable and Precise Robot-Free Demonstration.** As shown in Fig. 2(a), our data collection system integrates bimanual UMI-style [2] handheld grippers with wearable egocentric sensing. The demonstrator manipulates objects using two Agilex Robotics Pika Sense handheld grippers while wearing a helmet equipped with an Intel RealSense D435i camera and an additional HTC VIVE Tracker 3.0. With external Lighthouse base stations, the system tracks the relative 6-DOF trajectories of both grippers and the head with millimeter-level accuracy, while each gripper records a continuous gripperwidth signal. Together, these trajectories and gripper states define the unified human-robot action space. The observation space consists of two local gripper-centric RGB streams from the Pika Sense fisheye cameras and one global egocentric RGB stream from the helmet-mounted RealSense camera. All observation and action streams are synchronized at 30 Hz. 

**Robot Hardware with Active Neck.** As depicted in Fig. 2(b), we use the Unitree G1 humanoid robot as the whole-body loco-manipulation platform and augment it with robot-mounted Pika grippers and a self-designed 3-DoF active neck. The robot-mounted Pika grippers share similar gripper geometry, hardware layout, and camera placement with the handheld Pika Sense devices used for human data collection. This mechanically and visually aligned design reduces the gripper-centric observation gap between human demonstrations and humanoid policy execution. 

To enable active perception on the humanoid, we further design a servo-driven 3-DoF active neck and mount it on the head of the Unitree G1. The neck is designed such that the three rotational axes are approximately aligned with the optical center of the RGB camera. In addition, the intermediate links between adjacent servo joints are made as short as possible, making their translational offsets negligible in practice. Hence, the active neck can be modeled as a compact 3-DoF rotational mechanism that directly controls the yaw, pitch, and roll of the robot’s head-mounted camera, as demonstrated in Fig. 3. 


Fig. 4: **Manifold-Constrained Whole-Body Controller** tracks sparse world-frame head–hand targets by predicting latent actions in the BFM-Zero action space. These latent actions are decoded by the BFM-Zero model into feasible whole-body actions, constraining humanoid execution to physically plausible loco-manipulation behaviors. In contrast, directly training RL for sparse world-frame tracking in the raw action space is under-constrained and may lead to aggressive and unstable motions. 

## _B. Manifold-Constrained Whole-Body Control System_ 

To enable scalable and transferable human data collection, we adopt a sparse manipulation-aware interface that records only the head and two hands, without torso, leg, or foot references. As a result, the remaining whole-body motion is under-specified during execution, requiring the controller to infer feasible whole-body motion from sparse head-hand targets. We therefore train a unified whole-body controller that tracks arbitrary feasible three-point world-frame targets while maintaining natural and stable whole-body motion. 

Our whole-body control system, which aims to track the head and hand target poses, consists of two modules: an RL-based humanoid body controller and a 3-DoF active-neck controller with analytical inverse kinematics. Given the headhand targets, the body controller tracks the 6-DoF poses of both hands and the 3D position of the head, while the neck controller converts the head orientation target into 3-DoF neck joint commands. 

This neck–body decoupled design is motivated by the kinematic limitations of the original Unitree G1, which lacks an independently actuated neck. If the whole-body policy directly tracks head orientation, small head rotation changes may require large torso, pelvis, or leg motions, which can compromise whole-body stability and hand-tracking accuracy. 

As illustrated in Fig. 4, directly learning a precise worldframe tracking policy in the raw joint action space is brittle. World-frame tracking is inherently multi-modal: given the same target, the policy can realize it with many different solutions, including aggressive motions. These motions are often unstable, unnatural, and unsafe, but they may receive higher tracking rewards because they reduce tracking errors more quickly. This issue becomes more serious in the sparse world-frame keypoint tracking setting. To address this, we formulate world-frame tracking as planning on a learned behavior manifold rather than directly producing raw joint commands. 

Specifically, we use BFM-Zero [18] as a learned behavior prior for realizing world-frame tracking. BFM-Zero learns a 

spherical latent behavior space, where each latent action can be decoded by the BFM-Zero model into a natural and stable whole-body motion. We therefore train an RL tracking policy in the BFM-Zero latent space to realize sparse world-frame tracking. 

To train a unified head-hand world-frame tracking controller, we curate a large-scale loco-manipulation motion dataset containing over 6,000 motion sequences and adopt a teacher-student training strategy. We first train a teacher policy via RL with access to future reference motions, whole-body global and local tracking targets, and privileged information. We then distill a deployable student policy via DAgger, which only observes head-hand targets and proprioception available on the real robot. 

**Teacher Policy Training** . The teacher policy _π_ tea is trained via RL with task tracking observations, privileged simulation states, and future reference motion: _o_<sup>tea</sup> _t_ = _o_<sup>task</sup> _t , o_<sup>priv</sup> _t , o_<sup>future</sup> _t ._ Here _o_<sup>priv</sup> _t_ � � denotes privileged states available only during teacher training. The teacher task observation contains whole-body reference targets and tracking errors: _o_<sup>task</sup> _t_ = �∆ _p_<sup>root</sup> _t , vt_<sup>root</sup> _, Rt_<sup>root</sup> _, ωt_<sup>root</sup> _,_ ˆ _qt,_ ∆ _p_<sup>body</sup> _t ,_ ∆ _Rt_<sup>body</sup> � _._ where ∆ _p_<sup>root</sup> _t_ denotes the world-frame root position tracking error, _vt_<sup>root</sup> , _Rt_<sup>root</sup> , and _ωt_<sup>root</sup> denote the root linear velocity, root orientation, and root angular velocity, respectively. _q_ ˆ _t_ denotes reference joint positions and ∆ _p_<sup>body</sup> _t_ , ∆ _Rt_<sup>body</sup> denote the world-frame position and orientation tracking errors of the whole-body keypoints. The future term is _o_<sup>future</sup> _t_ = � _o_<sup>task</sup> _t_ + _δ_ � _δ∈{_ 5 _,_ 10 _,...,_ 50 _}_<sup>_._Theteacherfirstoutputsa</sup> 128-D latent command, _zt_<sup>tea</sup> = _π_ tea( _o_<sup>tea</sup> _t_ ), which is projected onto the BFM-Zero spherical latent space as _z_ ˜ _t_<sup>tea</sup> and decoded by the frozen BFM-Zero policy into joint commands _a_<sup>tea</sup> _t_ = _π_ BFM(˜ _zt_<sup>tea</sup> _, s_<sup>bfm</sup> _t_ ). The training rewards include tracking terms for hand poses and head position, together with regularization terms to encourage smooth behaviors. **Deployable Student Policy Distillation** . The student policy _π_ stu observes the deployable proprioceptive history and head-hand task observations: _o_<sup>stu</sup> _t_ = � _s_<sup>stu</sup> _t−_ 10: _t_<sup>_, o_</sup> _t_<sup>task</sup> � _._ The 


Fig. 5: **Controller-Aware Reference Trajectory Adaptation Overview** . We first obtain the tracking errors by rolling out the reference with the whole-body controller, then perform coarseto-fine global and local adaptation with parallel simulation. 

student task observation contains only world-frame head-hand tracking errors: _o_<sup>task</sup> _t_ = �∆ _p_<sup>head</sup> _t ,_ ∆ _p_<sup>lh</sup> _t_<sup>_,_∆</sup><sup>_p_rh</sup> _t_<sup>_,_∆</sup><sup>_R_</sup> _t_<sup>lh</sup><sup>_,_∆</sup><sup>_R_</sup> _t_<sup>rh</sup> � _._ = The student predicts a 128-D latent command _zt_<sup>stu</sup> _π_ stu( _o_<sup>stu</sup> _t_ ) _,_ which is projected onto the spherical latent space = and then decoded by the frozen BFM-Zero policy: _a_<sup>stu</sup> _t π_ BFM(˜ _zt_<sup>stu</sup> _, s_<sup>bfm</sup> _t_ ) _._ We optimize the student policy through DAgger: 


## _C. Human Data Processing to Bridge the Embodiment Gap_ 

Directly training an end-to-end high-level VLA policy on raw human demonstrations can lead to transfer failures during deployment, as human-to-humanoid gaps exist in both egoview observations and action execution. We therefore present a two-step data processing module to ease the embodiment gap, including (1) ego-view alignment, which reduces visual mismatch by transforming human observations toward the humanoid viewpoint, and (2) Controller-aware reference trajectory adaptation adjusts the collected head-hand trajectories to enable the whole-body controller to better reproduce the demonstrated motions during humanoid execution. 

_1) Ego-view Alignment:_ We adopt the ego-view alignment procedure from EgoHumanoid [20]. Specifically, we first reconstruct the human egocentric observation into a 3D scene representation by a learning-based single-view depth estimation model, then reproject it to the humanoid viewpoint, and use image inpainting to fill missing regions caused by reprojection and disocclusion. 

_2) Controller-Aware Reference Trajectory Adaptation:_ As illustrated in Fig. 5, the goal of controller-aware reference 

trajectory adaptation is to adjust the raw human-derived reference trajectory so that, after closed-loop execution by the humanoid whole-body controller, the executed robot trajectory better reproduces the collected human reference trajectory. 

The collected human demonstration is converted into a head-hand reference trajectory anchored at a fixed start pose: **x**<sup>ref</sup> _t_ = � **p**<sup>_L_</sup> _t_<sup>_,_</sup><sup>**p**</sup><sup>_R_</sup> _t_<sup>_,_</sup><sup>**p**</sup><sup>_H_</sup> _t_<sup>_,_</sup><sup>**R**</sup><sup>_L_</sup> _t_<sup>_,_</sup><sup>**R**</sup><sup>_R_</sup> _t_ � _._ Here, **p**<sup>_L_</sup> _t_<sup>_,_</sup><sup>**p**</sup><sup>_R_</sup> _t_<sup>_,_</sup><sup>**p**</sup><sup>_H_</sup> _t_ denote the target positions of the left hand, right hand, and head, and **R**<sup>_L_</sup> _t_<sup>_,_</sup><sup>**R**</sup> _t_<sup>_R_denotethetargetorientationsofthetwohands.</sup> = In practice, we adapt the translational components **p**<sup>ref</sup> _t_ [ **p**<sup>_L_</sup> _t_<sup>_,_</sup><sup>**p**</sup> _t_<sup>_R,_</sup><sup>**p**</sup> _t_<sup>_H_]ofthereferencetrajectorythrougharesidual</sup> trajectory **r** _t_ , which is parameterized by the B-splines. The adapted reference is **p** ˜ _t_ = **p**<sup>ref</sup> _t_ + **r** _t_ . To obtain **r** _t_ , we first roll out the raw reference trajectory in simulation from the same fixed start pose, and compute an initial residual trajectory which serves as the starting point of the subsequent multiscale adaptation: **e**<sup>_t_</sup> = **p**<sup>ref</sup> _t −_ **p**<sup>exec</sup> _t ,_ **r**<sup>0</sup> _t_<sup>=Π(</sup><sup>_G_</sup><sup>**e**</sup><sup>_t_),where</sup><sup>_G_</sup> is a diagonal compensation gain and Π projects the correction to a feasible range. 

To correct the reference trajectory at different temporal scales, we decompose **r** _t_ into a full-horizon residual component and a local residual component: **r** 1: _T_ = **r**<sup>global</sup> 1: _T_ + **r**<sup>local</sup> 1: _T_<sup>.</sup> We adopt a coarse-to-fine strategy for the full-horizon global adaptation, and then further apply chunk-wise local adaptation over short temporal windows. 

We first fit an initial set of global B-spline control points **C**<sup>0</sup> global<sup>from</sup><sup>**r**</sup> 1:<sup>0</sup> _T_<sup>.Afterglobaladaptation,localadaptationis</sup> performed over short temporal windows _Wm_ , each initialized from its corresponding residual within that window: 


These global and local control points serve as the initialization of the subsequent optimization. Since the controllersimulation loop is non-differentiable, we further optimize these control points using CEM-based [21] sampling. 

For the global and local adaptation stages, we optimize the B-spline control points with CEM-based sampling. At each iteration, we sample _K_ candidate control-point sets _{_ **C**<sup>(</sup><sup>_i_)</sup> _}_<sup>_K_</sup> _i_ =1<sup>andevaluatetheminparallelusing</sup><sup>_K_simulation</sup> environments. For each sampled candidate, we reconstruct the corresponding corrected trajectory, convert it into delta commands, and execute the resulting candidate via the controller in simulation, and score it by 


Here, _R_<sup>(</sup> _t_<sup>_i_)</sup> regularizes the smoothness of the executed trajectory. The sample distribution is then updated from the elite set _E_ with the lowest rollout costs: 


Finally, we replay the adapted reference trajectories over the full horizon and select the one with the best execution score, accepting it only when it improves over the original reference trajectory. 


Fig. 6: **Real-world task setup.** We evaluate HALOMI on five diverse humanoid loco-manipulation tasks involving navigation, hand-eye coordination, active perception, and dynamic interaction. The task instruction and sub-stage are overlaid on each policy rollout sequence, and task-relevant objects or motion directions are highlighted with visual markers for better visualization. 

## _D. Loco-Manipulation Policy Learning and Deployment_ 

We use the processed human data to fine-tune _π_ 0 _._ 5 [22] as the high-level policy. This high-level VLA takes all synchronized RGB images and the corresponding task prompts, and predicts the action chunk. Following FastUMI [23], we represent each action chunk as relative trajectories for three tracking targets: the left hand, right hand, and head. Thus, we slice the human dataset and form the action chunk, for which the k-th relative pose inside the action chunk of the timestamp t for each target can be expressed as 


where the _p_ and _R_ denote the position and rotation parts of the pose. Both continuous gripper values from the encoders of the left and right Pika Sense are appended to the back of their relative pose. 

Fig. 1 illustrates the deployment pipeline of HALOMI. At inference time, we launch an asynchronous image acquisition thread that synchronizes all camera streams at 30 Hz and continuously updates an image buffer with the latest timestamped observations. The high-level VLA queries the buffer for the most recent synchronized egocentric and grippercentric images together with the language instruction. It then predicts an action chunk consisting of relative pose commands for the left hand, right hand, and head, together with the gripper control signals. Each relative pose command is anchored at the corresponding absolute pose and converted into a sequence of world-frame Cartesian targets. These head-hand targets are streamed to the whole-body controller, which runs at 50 Hz. The controller tracks the VLA-generated targets while maintaining balance and completing the remaining wholebody motion. 

## IV. EVALUATION 

We conduct simulation and real-world experiments to evaluate whether HALOMI can effectively learn humanoid locomanipulation with active perception from human demonstrations. Our evaluation is designed to address the following key questions: 

**Q1: Loco-Manipulation Capability.** Can HALOMI accomplish diverse loco-manipulation tasks through sparse headhand interface? 

**Q2: Human-to-Humanoid Alignment.** Do ego-view alignment and controller-aware reference trajectory adaptation improve human-to-humanoid transfer? 

**Q3: Active Perception.** What role does active perception play in learning humanoid loco-manipulation from human demonstrations? 

**Q4: Generalization.** Can HALOMI generalize beyond the demonstrated settings to unseen object positions/appearances? 

## _A. Experimental Setup_ 

We evaluate HALOMI in two parts: controller execution and the entire system for loco-manipulation. We first perform simulation and real-world experiments to test the whole-body controller, evaluating whether it can achieve precise and robust head-hand tracking. 

We then evaluate HALOMI on five representative real-world humanoid loco-manipulation tasks, as shown in Fig. 6. For _Bag Transfer_ , _Pick Bread and Place_ , and _Transfer Towel to Basket_ , we train policies using 102, 95, and 96 human demonstrations, respectively, and conduct quantitative realworld evaluations with 20 rollouts per setting. Extensive ablations and generalization tests are further conducted to analyze how key components support learning humanoid locomanipulation from human demonstrations. For _Squat-andGrasp_ and _Tossing_ , we provide qualitative analysis to evaluate capabilities beyond standard pick-and-place, including wholebody posture adaptation and dynamic motions. 

## _B. Can HALOMI Achieve Diverse Loco-Manipulation Tasks Through Sparse Head-Hand Interface?_ 

The controller executes the sparse head-hand targets predicted by the high-level VLA and completes the remaining whole-body motion. Therefore, we first test its tracking performance and robustness. As shown in Table I, we replay collected human head-hand trajectories that were not used for controller training and report the tracking errors. We use 

_E_ MGBP to measure the average global tracking error over the head-hand target points. We evaluate three tasks that require accurate head-hand tracking for successful execution and cover diverse motion patterns. We further evaluate the controller under sudden large target changes and infeasible motions. As shown in Fig. 7, the controller maintains stable, non-aggressive behavior under these challenging commands. 

TABLE I: TRACKING PERFORMANCE. 

|Task|_E_MGBP (m)|_E_MGBP w/ Adapt. (m)|Improvement (%)|
|---|---|---|---|
|Pick Bread and Place|0.0436|0.0409|6.193|
|Transfer Towel to Basket|0.0568|0.0523|7.923|
|Squat-and-Grasp|0.1238|0.1163|6.058|


Fig. 7: **Controller Robustness Evaluation.** Top row: raw action-space tracking loses balance under OOD target commands. Below: the manifold-constrained controller maintains stable and feasible whole-body behaviors under challenging OOD commands. 

From the perspective of the entire system, HALOMI is evaluated on five representative real-world loco-manipulation tasks. Specifically, Fig. 6(a) shows _Bag Transfer_ , which evaluates long-range navigation with active visual search. Fig. 6(b) shows _Pick Bread and Place_ , which evaluates moderately precise tabletop pick-and-place with active perception. Fig. 6(c) shows _Transfer Towel to Basket_ , which evaluates bimanual manipulation, whole-body coordination, and active perception. Fig. 6(d) and Fig. 6(e) further show _Tossing_ and _Squat-andGrasp_ , which evaluate dynamic motion and deep-squat pickand-place behaviors, respectively. 

For the three quantitatively evaluated tasks, HALOMI achieves success rates of 90%, 85%, and 80%, on Bag Transfer, Pick Bread and Place, and Transfer Towel to Basket, respectively. In _Tossing_ , the robot performs a fast objectrelease motion toward the target region, while in _Squat-andGrasp_ , the robot performs a deep squat to grasp a lowpositioned object, stands up, and turns to place it in the bag. Together, these results show that HALOMI can achieve 

diverse loco-manipulation behaviors from sparse head-andhand targets with natural and stable whole-body hand-eye coordination. 

_C. Does Our Human Data Processing Improve Human-toHumanoid Transfer?_ 

We investigate whether our human data processing improves human-to-humanoid transfer by reducing observation-space and action-execution gaps. 


Fig. 8: **Bag Transfer Task.** (a) Test scenarios with varied cabinet placements. (b) Quantitative results under ablation and generalization settings. (c) Representative failure and OOD cases across different settings. 

**Ego-view alignment.** The ablation on _Bag Transfer_ shows the importance of ego-view alignment. As shown in Fig. 8(b), removing ego-view alignment decreases the success rate from 90% to 10%. Without ego-view alignment, we observe that the robot can still approach the target but often stops at a constant offset from the desired placement region. This suggests that the human-to-humanoid ego-viewpoint gap biases the learned visual-action mapping, leading to systematic errors in egoview guided manipulation. 

**Controller-aware reference trajectory adaptation.** The effect of controller-aware reference trajectory adaptation is first quantified through tracking-error analysis. As shown in Table I, reference adaptation consistently reduces tracking errors across all three tasks, yielding an average error reduction of approximately 6 _._ 725%. 

Its downstream effect on human-to-humanoid transfer is further evaluated through task success rate and execution quality. 

_Pick Bread and Place._ As shown in Fig. 9(b), adding controller-aware reference trajectory adaptation improves the success rate from 75% to 85%. Among successful trials, we observe improved execution accuracy: the robot grasps closer to the bread center and places the bread closer to the intended plate region. 

_Transfer Towel to Basket._ As shown in Fig. 10(b), adaptation improves the success rate from 75% to 80%. Beyond success rate improvement, qualitative results show more accurate 


Fig. 9: **Pick Bread and Place Task.** (a) Test scenarios with varied bread and plate placements. (b) Quantitative results under ablation and generalization settings. (c) Representative failure and capability cases across different settings. 

grasps and smoother whole-body execution. The smoother execution also leads to steadier ego-view observations during transport and placement. 


Fig. 10: **Transfer Towel to Basket** (a) Test scenarios with varied towel and basket placements. (b) Quantitative results under ablation and generalization settings. (c) Representative failure cases across different settings. 

_D. What Is the Role of Active Perception in Human-toHumanoid Transfer?_ 

To evaluate the role of active perception in human-tohumanoid transfer, we ablate active neck control in two settings: tasks that require active viewpoint changes and tasks that can be completed from a static view. 

**Tasks requiring active perception.** In _Bag Transfer_ and _Transfer Towel to Basket_ , active perception is required to maintain task-relevant visual context across execution stages. 

For _Bag Transfer_ , as shown in Fig. 8(b), disabling active neck control reduces the success rate to 30%. Most failures occur when the cabinet is not in the center: as the robot walks forward, the cabinet gradually moves out of the central field of the ego-view, causing the policy to lose target localization. 

For _Transfer Towel to Basket_ , as shown in Fig. 10(b), disabling active neck control reduces the success rate from 80% to 10%. We observe that the robot can often still approach and grasp the towel, but fails in the subsequent placement stage because it cannot actively search for the basket and bring it into the center of the head-camera view. These indicate that active head-view control is particularly important for tasks where the task-relevant visual focus changes across execution stages. **Tasks solvable with a static view.** In _Pick Bread and Place_ , a static ego-view can provide sufficient visual coverage for task completion. However, during human data collection, demonstrators naturally coordinate head and hand motions by shifting their gaze between the grasping and placement phases. As shown in Fig. 9(b), disabling active head control still reduces the success rate from 85% to 20%. This suggests that active perception is not only necessary to enlarge the visual field, but also crucial to preserve the hand-eye coupling in human demonstrations. 

## _E. Generalization Ability of HALOMI_ 

We further evaluate whether HALOMI generalizes beyond the demonstrated settings under the representative distribution shifts: unseen spatial configurations and unseen object appearances. 


Fig. 11: **OOD Test Configurations** (a) Bag Transfer. (b) Pick Bread and Place. (c) Transfer Towel to Basket. 

**Unseen Object Appearances.** For _Transfer Towel to Basket_ , as shown in Fig. 11(c), we evaluate novel towels with appearances different from those in the demonstrations. The policy achieves a 60% success rate in the generalization setting, suggesting that HALOMI retains object-level visual generalization. 

**Unseen Spatial Configurations.** For _Bag Transfer_ , we evaluate the cabinet at unseen locations, as shown in Fig. 11(a). The policy maintains a 60% success rate under OOD cabinet placements, suggesting that our relative head-hand pose interface enables generalization to unseen target locations beyond the demonstration settings. 

For _Pick Bread and Place_ , we further stress-tested this by introducing two types of spatial shifts, as illustrated in Fig. 11(b): changing the absolute bread/plate positions while preserving their relative layout, and changing both the absolute positions and the relative bread-to-plate layout. The policy remains robust to global translations, achieving 6/10 success when the relative bread-to-plate arrangement is preserved. As 

shown in Fig. 9(c), the robot can synthesize whole-body coordination that is not explicitly demonstrated, enabling the robot to reach far-away targets beyond the demonstrated workspace. However, under bread-to-plate relative layout changes, the success rate dropped to 0/10. In these failures, the robot often grasps the bread but fails during placement, since the handtarget trajectory required to complete the placement is not covered by the demonstrated head-hand dataset. 

## V. CONCLUSIONS 

We present HALOMI, a system for learning whole-body humanoid loco-manipulation with active perception directly from human demonstrations. We couple the robot-free egocentric demonstration interface with an automated human data processing pipeline, providing a scalable route to collect human data and bridge the human-to-humanoid embodiment gap. For robot execution, we integrate a humanoid platform with an active neck and a manifold-constrained whole-body controller, enabling robust world-frame tracking of sparse head-hand targets. Real-world experiments demonstrate that HALOMI enables versatile and challenging long-horizon humanoid locomanipulation tasks with active perception. 

## REFERENCES 

- [1] H. Xiong, X. Xu, J. Wu, Y. Hou, J. Bohg, and S. Song, “Vision in action: Learning active perception from human demonstrations,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 5450–5463. 

- [2] C. Chi, Z. Xu, C. Pan, E. Cousineau, B. Burchfiel, S. Feng, R. Tedrake, and S. Song, “Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

   - [14] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi, “Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning,” _arXiv preprint arXiv:2406.08858_ , 2024. 

   - [15] Y. Li, Y. Lin, J. Cui, T. Liu, W. Liang, Y. Zhu, and S. Huang, “Clone: Closed-loop whole-body humanoid teleoperation for longhorizon tasks,” in _9th Annual Conference on Robot Learning_ , 2025. 

   - [16] T. Zhu, G. Cai, Y. Zhaohui, G. Ren, H. Xie, Z. Wang, J. Wu, J. Wang, X. Yang, Y. Mu _et al._ , “Clot: Closed-loop global motion tracking for whole-body humanoid teleoperation,” _arXiv preprint arXiv:2602.15060_ , 2026. 

   - [17] Z. Luo, J. Cao, J. Merel, A. Winkler, J. Huang, K. Kitani, and W. Xu, “Universal humanoid motion representations for physics-based control,” in _International Conference on Learning Representations_ , vol. 2024, 2024, pp. 56 766–56 782. 

   - [18] Y. Li, Z. Luo, T. Zhang, C. Dai, A. Kanervisto, A. Tirinzoni, H. Weng, K. Kitani, M. Guzek, A. Touati _et al._ , “Bfm-zero: A promptable behavioral foundation model for humanoid control using unsupervised reinforcement learning,” _arXiv preprint arXiv:2511.04131_ , 2025. 

   - [19] Y. Li, M. Lin, Z. Lin, Y. Deng, Y. Cao, and L. Yi, “Learning physicsbased full-body human reaching and grasping from brief walking references,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2025, pp. 27 673–27 682. 

   - [20] M. Shi, S. Peng, J. Chen, H. Jiang, Y. Li, D. Huang, P. Luo, H. Li, and L. Chen, “Egohumanoid: Unlocking in-the-wild loco-manipulation with robot-free egocentric demonstration,” _arXiv preprint arXiv:2602.10106_ , 2026. 

   - [21] C. Pinneri, S. Sawant, S. Blaes, J. Achterhold, J. Stueckler, M. Rolinek, and G. Martius, “Sample-efficient cross-entropy method for real-time planning,” in _Conference on Robot Learning_ . PMLR, 2021, pp. 1049– 1065. 

   - [22] K. Black _et al._ , “ _π_ 0 _._ 5: a vision-language-action model with open-world generalization,” in _9th Annual Conference on Robot Learning_ , 2025. 

   - [23] K. Liu, C. Guan, Z. Jia, Z. Wu, X. Liu, T. Wang, S. Liang, P. Chen, P. Zhang, H. Song _et al._ , “Fastumi: A scalable and hardwareindependent universal manipulation interface with dataset,” _arXiv preprint arXiv:2409.19499_ , 2024. 

- [3] Q. Zeng, C. Li, J. S. John, Z. Zhou, J. Wen, G. Feng, Y. Zhu, and Y. Xu, “Activeumi: Robotic manipulation with active perception from robot-free human demonstrations,” _arXiv preprint arXiv:2510.01607_ , 2025. 

- [4] X. Xu, J. Park, H. Zhang, E. Cousineau, A. Bhat, J. Barreiros, D. Wang, and S. Song, “Hommi: Learning whole-body mobile manipulation from human demonstrations,” _arXiv preprint arXiv:2603.03243_ , 2026. 

- [5] J. Yu, Y. Shentu, D. Wu, P. Abbeel, K. Goldberg, and P. Wu, “Egomi: Learning active vision and whole-body manipulation from egocentric human demonstrations,” _arXiv preprint arXiv:2511.00153_ , 2025. 

- [6] R. Nai, B. Zheng, J. Zhao, H. Zhu, S. Dai, Z. Chen, Y. Hu, Y. Hu, T. Zhang, C. Wen _et al._ , “Humanoid manipulation interface: Humanoid whole-body manipulation from robot-free demonstrations,” _arXiv preprint arXiv:2602.06643_ , 2026. 

- [7] C. Yu, H. Wang, Y. Hu, J. Zhang, Y. Li, and S. Luo, “Bifrostumi: Bridging robot-free demonstrations and humanoid whole-body manipulation,” _arXiv preprint arXiv:2605.03452_ , 2026. 

- [8] H. Choi, Y. Hou, C. Pan, S. Hong, A. Patel, X. Xu, M. R. Cutkosky, and S. Song, “In-the-wild compliant manipulation with umi-ft,” _arXiv preprint arXiv:2601.09988_ , 2026. 

- [9] M. Xu, H. Zhang, Y. Hou, Z. Xu, L. Fan, M. Veloso, and S. Song, “Dexumi: Using human hand as the universal manipulation interface for dexterous manipulation,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 437–459. 

- [10] H. Ha, Y. Gao, Z. Fu, J. Tan, and S. Song, “UMI on legs: Making manipulation policies mobile with manipulation-centric whole-body controllers,” in _Proceedings of the 2024 Conference on Robot Learning_ , 2024. 

- [11] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang, “Homie: Humanoid loco-manipulation with isomorphic exoskeleton cockpit,” _arXiv preprint arXiv:2502.13013_ , 2025. 

- [12] J. Li, X. Cheng, T. Huang, S. Yang, R.-Z. Qiu, and X. Wang, “AMO: Adaptive Motion Optimization for Hyper-Dexterous Humanoid WholeBody Control,” in _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. 

- [13] Y. Ze, Z. Chen, J. P. Ara´ujo, Z. ang Cao, X. B. Peng, J. Wu, and C. K. Liu, “Twist: Teleoperated whole-body imitation system,” _arXiv preprint arXiv:2505.02833_ , 2025. 

