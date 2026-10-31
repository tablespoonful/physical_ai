---
title: "HumDex: Humanoid Dexterous Manipulation Made Easy"
date: "2026-03-12"
authors: "Liang Heng; Yihe Tang; Jiajun Xu; Henghui Bao; Di Huang; Yue Wang"
url: https://arxiv.org/abs/2603.12260
pdf: https://arxiv.org/pdf/2603.12260
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.12260)** / [論文ページ](https://arxiv.org/abs/2603.12260)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# HumDex: Humanoid Dexterous Manipulation Made Easy 

Liang Heng<sup>_∗_1</sup><sup>_,_2</sup> Yihe Tang<sup>_∗_1</sup> Jiajun Xu<sup>2</sup> Henghui Bao<sup>2</sup> Di Huang<sup>2</sup> Yue Wang<sup>1</sup> 1USC Physical Superintelligence (PSI) Lab 2WorldEngine AI 

> _∗_ Equal Contribution 


Fig. 1: **The HumDex System.** Our portable teleoperation system enables efficient collection of high-quality dexterous manipulation data. Left: We demonstrate data collection and autonomous policy execution on challenging tasks featuring dexterous manipulation, bimanual coordination, long-horizon planning, deformable and articulated object manipulation, and whole-body movement. Middle: We use a Unitree-G1 humanoid and two 20 DoF dexterous hands. Right: By pretraining robot policy on diverse human data, our policy generalizes to new positions, objects, and backgrounds unseen in robot data. 

**_Abstract_ —This paper investigates humanoid whole-body dexterous manipulation, where the efficient collection of high-quality demonstration data remains a central bottleneck. Existing teleoperation systems often suffer from limited portability, occlusion, or insufficient precision, which hinders their applicability to complex whole-body tasks. To address these challenges, we introduce HumDex, a portable teleoperation system designed for humanoid whole-body dexterous manipulation. Our system leverages IMUbased motion tracking to address the portability-precision tradeoff, enabling accurate full-body tracking while remaining easy to deploy. For dexterous hand control, we further introduce a learning-based retargeting method that generates smooth and natural hand motions without manual parameter tuning. Beyond teleoperation, HumDex enables efficient collection of human motion data. Building on this capability, we propose a two-stage imitation learning framework that first pre-trains on diverse human motion data to learn generalizable priors, and then fine-tunes on robot data to bridge the embodiment gap for precise execution. We demonstrate that this approach significantly improves generalization to new configurations, objects, and backgrounds with minimal data acquisition costs. The entire system is fully reproducible and open-sourced at https://github.com/physical-superintelligence-lab/HumDex.** 

## I. INTRODUCTION 

Humanoid dexterous manipulation holds great promise for unlocking robots to perform complex, long-horizon locomanipulation tasks in the real world. Current robotic systems often resort to imitation learning [6, 28, 10, 11, 8] that has shown great success in acquiring complex manipulation skills. These methods rely heavily on high-quality task demonstration data collected through costly robot teleoperation. However, acquiring such data for humanoid robots with dexterous hands remains a critical bottleneck due to their complex morphology. 

While huge progress has been made on table-top robot data collection [29, 21, 5], teleoperation systems for humanoid robots and dexterous hands are way less mature. Previous efforts with different hardware solutions exhibit their own limitation and trade-off. Motion-capture-based [26] (e.g., optical tracking) or exoskeleton-based [2] systems can achieve high accuracy but require fixed infrastructure, which severely limits the environments in which data can be collected. In contrast, VR-based alternatives [27, 9, 12, 14] offer greater 

portability but suffer from reduced accuracy and occlusion issues. For instance, operators’ hands must remain within the sensors’ field of view to maintain tracking stability, constraining the range of feasible motions and, consequently, the set of tasks that can be demonstrated. Furthermore, despite recent advances in humanoid motion retargeting and low-level locomotion policies [26, 2, 27, 9, 12, 14], dexterous hand control still largely relies on optimization-based retargeting, leading to reduced accuracy and limited generalization. 

In this work, we introduce HumDex(Fig. 1), a portable motion-tracker-based teleoperation system for whole-body dexterous manipulation. Our system addresses the portabilityprecision trade-off by leveraging IMU-based tracking, enabling high-precision tracking while maintaining portability. For dexterous hand control, we propose a learning-based retargeting system trained on collected teleoperation data, which produces smooth and natural hand motions without manual parameter tuning. This hand retargeting method, compared to previous optimization-based alternatives, achieves significantly better performance in real-world deployment. We demonstrate the effectiveness of HumDex on a suite of challenging tasks involving whole-body motion, bimanual coordination, and fine-grained dexterous manipulation. Overall, our system enables faster demonstration collection, higher success rates, and improved data quality relative to existing approaches. 

Beyond teleoperation, our tracking system also enables efficient collection of human data of the same tasks, which offers better collection efficiency than teleoperation, thus serves as an additional data source for pre-training or co-training. However, due to embodiment gaps, directly retargeting human motion to the humanoid leads to inaccurate movements, which often leads to manipulation failures. Consequently, prior works on tabletop dexterous manipulation performs alignment [7, 17] or correction strategies [20] to mitigate this gap, while those on humanoid manipulation rely solely on teleoperation data [9, 27, 4]. To effectively leverage the diversity and motion prior in human data without explicit alignment, we propose a twostage imitation learning framework. First, we train the policy on human demonstrations collected in diverse settings, where we use retargeting results as a joint target, and approximate proprioceptive states with previous action. Then, we fine-tune on robot teleoperation data only, refining movements towards the robot embodiment. As shown in Table III, our approach achieves successful task execution while retaining generalization to new object positions, categories, and backgrounds without requiring robot data under those settings. 

In conclusion, our contributions are: (1) a portable and efficient teleoperation system for humanoid dexterous manipulation, (2) a learning-based hand retargeting method, and (3) a two-stage training pipeline that leverages human data to improve generalization while reducing the need for teleoperation data. 

## II. RELATED WORKS 

## _A. Humanoid Whole-Body Dexterous Teleoperation_ 

Existing humanoid whole-body teleoperation systems can be categorized by their tracking hardware. Motion-capturebased [26] and exoskeleton-based [2] systems achieve high tracking accuracy but suffer from portability issues — mocap requires a dedicated room setup, while exoskeletons are heavy and typically require seated operation. Vision-based and VRbased systems [27, 9, 14, 12] offer better portability but suffer from occlusion: operators must keep their hands visible at all times, restricting feasible motions. In this work, we adopt IMU-based motion tracking, which consists of only 15 lightweight trackers worn on the body, providing unconstrained motion capture with high tracking quality. Beyond hardware, we also investigate a more challenging robot configuration. Prior whole-body teleoperation works employ simplified end-effectors such as parallel grippers or three-fingered hands, often controlled via binary open/close signals (e.g., VR controller triggers). Consequently, demonstrated tasks are limited to simple object interactions such as pick-and-place. In contrast, our system supports full dexterous control of a 20-DoF hand, enabling fine-grained manipulation such as grasping a handheld barcode scanner and pulling its trigger, while simultaneously supporting whole-body movement. 

## _B. Dexterous Hand Retargeting_ 

Dexterous hand retargeting is a key component of teleoperation driven demonstration collection system. It maps human hand features to a robot hand under substantial embodiment gaps. A common approach is optimization-based policy, which formulates the mapping as a constrained inverse kinematics (IK) or nonlinear least squares problem. In these formulations, objective terms typically preserve task-relevant geometric relations, while constraints enforce robot executability. To improve stability in teleoperation and contact-rich manipulation, many methods additionally incorporate temporal-consistency regularizers and contact-consistency/interpenetration penalties to discourage implausible hand and object penetrations and stabilize interaction [15, 13, 23]. 

In contrast, learning-based approaches predict robot hand configurations directly from human observations, reducing reliance on hand-crafted objectives and enabling constant inference. GeoRT [24] proposes an ultrafast neural retargeting approach guided by principled geometric criteria, achieving real-time performance without test-time optimization and supporting scalable teleoperation pipelines [24, 25]. 

Our approach follows this learning-based direction with a lightweight supervised formulation. Given the 3D positions of five fingertips, we train a small MLP regressor to predict robot hand joint angles on paired fingertip–joint samples. 

## _C. Imitation Policy Learning with Human Data_ 

Imitation learning has advanced rapidly, with several works leveraging human data for robot learning. Some approaches use egocentric human video as a diverse source for visual 


Fig. 2: **System Overview.** (A) Our teleoperation pipeline and hand retargeting policy training. (B) Our imitation learning policy architecture. We approximate proprioceptive states missing in human data with previous-frame actions. 

representation learning [16, 22, 18]. For dexterous manipulation specifically, prior works focus primarily on fixed-base arms and tabletop tasks, bridging the human-robot gap through hardware design that mimics human embodiment [7], humanin-the-loop correction [20], or aligning action space [17]. 

However, for humanoid robots, the embodiment gap to humans is substantially larger and cannot be easily addressed through hardware alignment. While human motion data has been widely used for learning humanoid low-level control and general whole-body movements, these works emphasize approximate motion following rather than the precision required for manipulation task success. Consequently, manipulation tasks with humanoids still rely on teleoperated robot data [2, 27, 9]. 

Our approach investigates leveraging human data for humanoid loco-manipulation with dexterous hands. Through our two-stage training framework—pretraining on human demonstrations followed by finetuning on robot data—we achieve improved generalization without requiring special embodiment alignment or extensive data post-processing. 

## III. METHOD 

In this section, we present **HumDex** (Fig. 2), a portable teleoperation system for humanoid whole-body dexterous manipulation, along with a two-stage learning framework to leverage human motion data. The system overview is illustrated in Fig. 2. Sec III-A describes our IMU-based teleoperation system for efficient whole-body data collection. Section III-B presents our learning-based approach for dexterous hand retargeting. Section III-C outlines our imitation learning pipeline and two-stage training strategy that pretrains on human data before finetuning on robot demonstrations. 

## _A. Whole-Body Dexterous Teleoperation System_ 

**Problem Formulation** We address the problem of real-time, whole-body dexterous teleoperation within a unified control framework. Our goal is to map the motion of a human operator, captured via a wearable IMU-based system, to a humanoid robot to execute diverse loco-manipulation tasks. Following the hierarchical architecture proposed in TWIST2 [27], we decouple the system into a task-agnostic low-level controller _πlow_ and a high-level command generator _πhigh_ . 

_1) Low-Level Hierarchical Control Interface:_ To achieve stable whole-body control while enabling precise dexterous manipulation, we adopt a modular control strategy. We leverage the robust general motion tracking policy from TWIST2 [27] to handle the robot’s base and body balancing, while integrating our custom retargeting pipeline for the dexterous hands. 

_a) Body Controller Interface:_ We utilize the pre-trained motion tracking policy _πlow_ from TWIST2 [27] as the foundation for body stability. Consistent with the standard interface, the whole-body reference command vector _pcmd_ is defined as: _pcmd_ = [ **v** _root, zref ,_ **Θ** _root, ψ_<sup>˙</sup> _ref , qref_ ]<sup>_⊤_</sup> (1) 

where _qref ∈_ R<sup>_N_</sup> represents the whole-body joint targets. Crucially, we conceptually decompose the joint targets into two distinct components for execution: _qref_ = [ _qbody, qhand_ ]. The body component _qbody_ is fed into the policy _πlow_ to generate actuation torques for dynamic balancing and locomotion, while _qhand_ is directly executed via joint position controllers to track precise dexterous motions. 

Beyond TWIST2 [27], our framework also maintains compatibility with other low-level controllers such as SONIC [14]. The reference command _qbody_ is efficiently streamed to these 

controllers via ZMQ messaging backbone, ensuring lowlatency synchronization between the high-level retargeting and low-level execution. 

_b) Dexterous Hand Control:_ Unlike TWIST2, which simplifies the hand control to a binary open-close mechanism, we implement a fine-grained dexterous retargeting module. Specifically, we train a lightweight MLP regressor that maps the 3D positions of the operator’s five fingertips (captured via IMU gloves) directly to the robot’s 20-DoF hand joint angles. This learning-based approach ensures smooth and natural motion reconstruction without manual parameter tuning. The computed hand targets _qhand_ are then concatenated with the body targets _qbody_ to form the unified _qref_ in Eq. (1). 

_2) High-Level Teleoperation via IMU-based Retargeting:_ In the teleoperation phase, the high-level policy _πhigh_ is composed of the human operator and a retargeting algorithm. Unlike prior works constrained by VR-based tracking [27] or bulky optical motion capture, we utilize a custom IMUbased wearable interface designed for minimal intrusiveness. The system is lightweight and unobtrusive, ensuring the operator’s motion remains natural and unencumbered. Furthermore, it supports continuous operation exceeding 10 hours and maintains robust connectivity over a range of 50+ meters, significantly expanding the data collection envelope beyond room-scale setups. 

To map the IMU-derived skeleton _SH_ to robot commands, we employ the General Motion Retargeting (GMR) framework [1, 26]. Given that IMU-based systems inherently suffer from global position drift, we adopt a _pelvis-centric_ optimization formulation. Specifically, we solve for the robot configuration _q_<sup>_∗_</sup> that minimizes the orientation error of all links and the _relative_ position error of key end-effectors: 


where _LR_ and _LP_ denote the sets of links for orientation and position tracking, respectively. Crucially, _p_<sup>_H,_</sup> _j_<sup>rel</sup> represents the position of the _j_ -th end-effector relative to the operator’s pelvis frame, rather than the absolute world frame. This formulation [27] allows us to leverage the standard GMR solver to achieve robust whole-body tracking without relying on drift-prone absolute position measurements. 

_3) Hardware Setup:_ To ensure robustness against occlusion and achieve true “in-the-wild” portability, our system utilizes a fully tether-free inertial motion capture interface. The hardware configuration is divided into whole-body tracking and dexterous hand tracking. 

_a) Body Tracking Interface:_ Our framework is compatible with diverse inertial motion capture solutions. We primarily utilize a commercial 15-node system placed on standard kinematic chains, Vdmocap, to ensure high-precision baseline tracking. To further demonstrate the accessibility and 

scalability of our approach, we implemented a highly costeffective ( _<_ $200) custom wearable system based on the opensource SlimeVR ecosystem [19]. We adopted the architecture from the official hardware guide, allowing for flexible configurations ranging from 6 to 16 nodes to dynamically adjust setup complexity. 

**Sensor and Electronics.** Each custom node is powered by an ICM-45686 6-axis IMU. We specifically selected this high-performance sensor for its superior precision and low gyroscope drift, ensuring the tracking fidelity required for fine-grained teleoperation. To ensure stable connectivity in complex Wi-Fi environments (e.g., crowded labs), we adopted the non-standard wireless communication scheme supported by the SlimeVR software. Specifically, we utilize the Nordic nRF52840 SoC running the Enhanced ShockBurst (ESB) protocol, which significantly reduces packet loss and interference compared to standard UDP-over-WiFi solutions. 

**Form Factor and Efficiency.** The trackers are assembled for minimal intrusiveness. Each node weighs less than 20g and is encased in a compact 3D-printed housing. By leveraging the optimized power management features of the ecosystem, the system achieves over 20 hours of continuous operation on a single charge, supporting extensive data collection sessions. The raw IMU data is fused on a central receiver dongle to reconstruct the full human skeleton _SH_ . 

_b) Dexterous Hand Interface.:_ For fine-grained manipulation, we leverage high-fidelity commercial inertial gloves—supporting both Vdhand and Manus—for hand motion capture. Each glove utilizes an array of IMUs distributed across the dorsum and finger segments. Unlike vision-based tracking, which suffers from severe self-occlusion during object interaction, this pure inertial solution ensures that complex grasping motions are accurately captured even when the hands are obstructed by objects or the robot’s body. 

## _B. Learning-Based Dexterous Hand Retargeting._ 

As mentioned above, our teleoperation setup uses inertial gloves for hand tracking. At each timestep, the glove provides the 3D positions of five fingertips (thumb, index, middle, ring, and little). We express these fingertip positions in the glove wrist frame to avoid sensitivity to global drift. The goal is to map this human fingertip observation to executable robot hand joint targets for a 20-DoF dexterous hand in real time. Formally, let _pt ∈_ R<sup>15</sup> be the concatenated fingertip positions and _qt ∈_ R<sup>20</sup> be the robot hand joint angles. We learn a retargeting function _fθ_ : R<sup>15</sup> _→_ R<sup>20</sup> , and at runtime we directly set _qhand_ = _fθ_ ( _pt_ ), which is concatenated with _qbody_ to form the full reference command for the low-level controller. 

We formulate this as a regression problem to achieve constant-time inference and low operational overhead. Specifically, we parameterize _fθ_ as a lightweight MLP that maps fingertip positions to robot joint angles, and train it on a paired dataset _D_ = ( _pt, qt_ ) using a mean-squared error (MSE) objective: 


Fig. 3: **Evaluation Tasks and Generalization.** We visualize the initial state and key steps in our evaluated tasks. In the Task 5 generalization test, robot data used for training only consists of the Seen (position, object, background) setting. 

The training dataset _D_ is generated via an offline optimization-based retargeting process [3] across a diverse range of hand poses. Once trained, the MLP _fθ_ generalizes to various hand sizes and provides smooth, continuous joint trajectories without the high computational cost of per-frame optimization. 

## _C. Two-Stage Imitation Learning with Human Data_ 

_a) Policy Learning Setup:_ We perform imitation learning with the following setup. We use Action Chunking Transformer (ACT) [29] as our policy backbone with a ResNet18 pre-trained visual encoder. The observation space consists of an RGB image _It_ of shape 640 _×_ 480 from the G1 builtin RealSense D435i camera, and the proprioceptive state _st_ comprising joint positions of the body and hands. The action space _at_ includes 20 dimensions per hand and 35 dimensions for the humanoid body. Following TWIST2 [27], we predict low-level motion tracker targets instead of direct joint positions, enabling real-world adjustment and balancing. 

_b) Two-Stage Training with Human Data:_ Our tracking system enables collecting human demonstration data more 

efficiently than robot teleoperation. However, robot proprioceptive states **s** _t_ are not directly available from human data. We approximate them using the previous timestep’s action **a** _t−_ 1, validated by analyzing action-state correspondence in robot data, which confirms **a** _t_ corresponds to **s** _t_ +1 with minimal latency. 

Due to morphological differences between humans and the G1 robot, human motion cannot be directly replayed. Rather than aligning human and robot data for mixed training [7], we train sequentially: stage 1 only on human data to learn generalizable motion priors, stage 2 on robot data to refine toward robot embodiment. This enables fast human data collection without alignment. 

## IV. EXPERIMENTS 

With our experiments, we seek to answer the following questions: (A) How does our system’s data collection efficiency and quality compare to existing methods on challenging whole-body dexterous tasks? (B) How to evaluate our system’s capability of hand retargeting, specifically for the dynamic tasks. (C) Does incorporating human data improve generalization to new positions, objects, and backgrounds? 

|Metric|Method|||Task|s|||
|---|---|---|---|---|---|---|---|
|||_Scan&Pack_|_Hang Towel_|_Open Door_|_Place Basket_|_Pick Bread_|**Avg**<sup>_†_</sup>|
|ClliTii|Baseline|-|68|75|46|50|59.8|
|oecton me (mn) _↓_|Ours|**78**|**53**|**62**|**35**|**27**|**44.3**|
|Collection Success Rate _↑_|Baseline<br>Ours|0/60<br>**54/60**|26/60<br>**50/60**|52/60<br>**57/60**|47/60<br>**58/60**|54/60<br>**55/60**|74.6%<br>**91.7%**|
|Policy Success Rate _↑_|Baseline<br>Ours|0/30<br>**20/30**|11/30<br>**19/30**|10/30<br>**22/30**|22/30<br>**26/30**|26/30<br>**29/30**|57.5%<br>**80.0%**|


TABLE I: **Data Collection Comparison.** We report the total time to collect 60 episodes, the number of successful teleoperation attempts out of 60, and the success rate of the trained policy over 30 trials. (-) indicates the task was infeasible with the baseline setup. **Note:** All values in the **Avg** column are calculated on the subset of four tasks successfully performed by both methods (excluding _Scan&Pack_ ). 

## _A. Whole-Body Dexterous Teleoperation_ 

_1) Tasks:_ We evaluate teleoperation success rate and perepisode time on a suite of challenging loco-manipulation tasks, as visualized in Fig. 3. 

## **_<u>Scan&Pack</u>_** 

**Goal and Success Criteria.** The robot grasps a barcode scanner with one hand and a toy with the other, then pulls the trigger to scan the barcode on the toy. It then places the toy into a shopping bag, grasps the bag handle, and hands it to a human. A successful trial requires: the scanner trigger pulled with the scanner aimed at the barcode (indicated by red light), the toy inside the shopping bag, and the robot lifting the bag from the table. 

**Main Challenge.** The scanning step requires **high dexterity** , as the robot must stably hold the scanner while using a spare finger to pull the trigger. This makes the task extremely challenging for simpler hand hardware used in previous works. Additionally, this task is **long-horizon** . 

## **_HangTowel_** 

**Goal and Success Criteria.** The robot grasps a hanger from a rod, threads a towel through the hanger’s horizontal bar with the other hand, and returns the hanger to the rod. Success requires the towel draped over the bar and the hanger back on the rod. 

**Main Challenge.** Successful completion requires **bimanual coordination** when threading the towel onto the hanger, as well as robustness to disturbance, since the hanger may rotate upon contact when reaching and grasping. 

## **_OpenDoor_** 

**Goal and Success Criteria.** The robot needs to grasp a realworld office door handle, press it down to unlatch the door, and walk forward to push the door open. The task is considered successful if the door is opened more than 45 degrees. 

**Main Challenge.** This task involves **articulated object manipulation** , as the robot must grasp and press down the handle to unlatch before pushing. It also requires **coordinated locomotion** , since the robot needs to walk forward while pushing the door open. 

## **_PlaceBasketOnShelf_** 

**Goal and Success Criteria.** The robot squats down to pick up a basket, stands up, rotates its upper body, and places the basket on a small shelf. The task is considered successful if the basket ends up stably on the shelf. 

**Main Challenge.** This task requires coordinated **wholebody movement** to be completed. 

## **_<u>PickBread</u>_** 

**Goal and Success Criteria.** The robot grasps a bread roll from the table, places it into a basket, and returns. The task is considered successful if the bread is stably placed inside the basket. 

**Main Challenge.** In generalization evaluation, this task requires grasping of objects with diverse geometry. 

_2) Baseline and Comparison:_ **Baseline.** We compare our system with existing vision-based teleoperation systems. In our baseline, the humanoid motion is teleoperated with PICO following the setup in TWIST2. Yet in the original TWIST2 controller, triggers are used to control the binary open-close of the hand, so we further add the vision-based hand tracking module to allow dexterous hand teleoperation. 

**Setup and Metrics.** For each task and teleoperation solution, we perform 60 teleoperation attempts (operators practice in advance). We compute the successfully teleoperated trails in these attempts, and the total time used. To compare the data quality of obtained demonstrations, we train an imitation learning policy on collected demos following the setup in III-C (no human data). We compare the task success rate of the trained policies and report them in Table I. 

_3) Results:_ The quantitative results of our whole-body teleoperation evaluation are summarized in Table I. First, we note that the baseline system was unable to perform the _Scan&Pack_ task due to severe occlusion issues, whereas our system achieved a 90% teleoperation success rate. To ensure a fair quantitative comparison, the following average metrics are calculated only on the four tasks feasible for both systems ( _Hang Towel, Open Door, Place Basket, Pick Bread_ ). 

**Task Coverage and Reliability.** The baseline’s failure in _Scan&Pack_ highlights the fundamental limitations of visionbased teleoperation: susceptibility to jitter and severe occlusion. In this task, when the operator grasps the barcode 

scanner, the device itself occludes a significant portion of the hand from the headset’s cameras. For vision-based algorithms, this loss of visual features leads to tracking failure or excessive jitter, making it impossible to precisely control the index finger to pull the trigger. This failure mode is critical because tool use—which inherently causes self-occlusion—is ubiquitous in real-world daily tasks. Consequently, vision-based methods are often restricted to simple, non-occluded interactions where the full hand remains visible at all times. In contrast, _HumDex_ is immune to visual occlusion, reliably capturing fine-grained finger articulation during complex tool manipulation, achieving a 90% teleoperation success rate on this challenging task. 

**Collection Efficiency.** On the common task set, _HumDex_ demonstrates significantly higher efficiency. The average time required to collect 60 episodes is reduced from 59.8 minutes (Baseline) to 44.3 minutes (Ours), representing a **26% improvement** . This efficiency gain is largely attributed to the robustness of our IMU-based tracking against occlusion constraints. In the baseline vision-based system, the operator is strictly required to keep their hands within the headset’s field of view to prevent tracking loss. This constraint forces the operator to frequently adjust their head orientation to follow their hands, introducing unnatural body movements that compromise the stability of the data collection process. Furthermore, inevitable momentary tracking losses often necessitate pausing or resetting the episode to regain lock. In contrast, our system allows for unconstrained motion, enabling the operator to focus entirely on task execution without managing tracking visibility, resulting in a smoother and faster workflow. 

**Success Rate and Quality.** Our system also achieves higher reliability. The average teleoperation success rate on the common tasks is **91.7%** for _HumDex_ , compared to **74.6%** for the baseline. Crucially, this improvement in data quality translates to downstream policy performance. Policies trained on our data achieve an average success rate of **80.0%** , significantly outperforming the baseline’s **57.5%** . For challenging bimanual tasks like _Hang Towel_ , the performance gap is particularly evident (19/30 vs. 11/30), confirming that our system captures the precise, smooth motions required for complex manipulation. 

## _B. Dexterous Hand Retargeting_ 

We evaluate the effectiveness of our learning based hand retargeting on the Wuji dexterous hand using the Vdhand. We compare against a classical optimization-based retargeting baseline that solves a constrained inverse-kinematics / nonlinear least-squares problem per frame. Both methods consume the same human hand observations and output 20-DoF Wuji hand joint targets at the same control rate. 

**Input/Output.** The retargeting input is a compact 15D representation formed by the 3D positions of five fingertips (thumb, index, middle, ring, little) in the glove hand frame. The output is the 20-DoF joint angle vector of the Wuji hand. 

**(B1) Qualitative motion/pose reproduction.** We first evaluate whether a retargeting method can reproduce representative dexterous hand poses _faithfully and stably_ under a 


Fig. 4: **Qualitative pose reproduction on the Wuji hand.** We compare an optimization-based retargeting baseline and our learning-based retargeter on canonical dexterous poses captured by the inertial glove, including _touch middle finger_ , _touch index finger_ , _touch ring finger_ , and the _rock sign_ . 

controlled open-loop replay setting. This evaluation intentionally removes whole-body locomotion and task interaction, so that observed differences can be attributed primarily to the hand retargeting module itself. Concretely, we curate a set of canonical poses that stress finger individuation and crossfinger coordination, including _touch middle finger_ , _touch index finger_ , _touch ring finger_ , _one-finger extension_ , and the _rock sign_ (Fig. 4). For each pose, we feed the same glove-tracked input—the 3D positions of the five fingertips—to each retargeting method, and replay the resulting joint trajectories on the Wuji hand. We then present side-by-side snapshots comparing our learning-based retargeter against an optimization-based baseline. 

Our qualitative assessment focuses on two observable criteria: (1) _pose correctness_ , i.e., whether the intended finger configuration is achieved (e.g., the specified finger reaches/contacts the thumb while non-target fingers remain in the desired state); (2) _unwanted coupling_ , i.e., whether irrele- 

|Task|_Glove_+|_Glove_+|_PICO_+|_PICO_+|
|---|---|---|---|---|
||_Learn._|_Opt._|_Learn._|_Opt._|
|_Scanner Triggering_|20/30|14/30|13/30|12/30|
|_Hanger Stabilization_|20/30|21/30|15/30|18/30|
|_Doll Grasping_|29/30|23/30|17/30|15/30|


TABLE II: Teleoperation success rate (#success/#trials) across tasks under different hand retargeting interfaces. 

vant fingers exhibit spurious bending, participation, or collapse to easier but incorrect configurations; and This qualitative study provides an interpretable sanity check of hand mapping quality and demonstrates that our learned retargeter yields more reliable pose realization than per-frame optimization in representative dexterous configurations. 

**(B2) Teleoperation task evaluation.** We further evaluate retargeting performance under closed-loop humanoid teleoperation with _task-critical hand sub-tasks_ that impose the highest dexterity requirements in our data-collection suite, so that grasp stability and contact transitions directly determine success. Concretely, we derive three evaluation sub-tasks from the full demonstrations: _Scanner Triggering_ (from _Scan&Pack_ ), _Hanger Stabilization_ (from _HangTowel_ ), and _Doll Grasping_ (from _Scan&Pack_ ). Importantly, we enforce stricter success criteria to better reflect real-world use. In _Scanner Triggering_ , the robot must actuate the scanner trigger _five consecutive times_ , and each actuation must be _held for 3 seconds_ , matching realistic scanning behavior rather than a single tap. In _Hanger Stabilization_ , the robot must maintain a stable grasp on the hanger while the operator rotates the wrist _back and forth for five cycles_ , approximating the disturbance and wrist motion that occur when threading a towel; a trial is successful only if the hanger remains securely grasped throughout the entire sequence. In _Doll Grasping_ , we increase difficulty by using a doll that is _3× larger_ than the one in the original task, making it harder to envelop and stabilize. The results are shown in (Tab. II) 

**Efficiency.** Besides effectiveness, we emphasize deployment efficiency. Our retargeting model is a lightweight MLP trained on paired samples of five-fingertip positions and robot joint targets, requiring only a short calibration dataset(typically about 20k frames, i.e., and less than 20 minutes of recording). 

## _C. Human Data for Policy Generalization_ 

We evaluate how leveraging human data improves policy generalization on the _PickBread_ task. 

**Data Collection.** We use our portable system to efficiently collect a dataset covering diverse environmental variations. Specifically, the dataset consists of: 

- **Robot Data (Base):** 50 episodes of teleoperation data where the robot picks up a bread roll from a fixed position on a plain table. 

- **Human Data (Position Var.):** 100 episodes of human operation where the bread is placed at random positions across the table surface. 

- **Human Data (Object Var.):** 300 episodes (3 items _×_ 100 each) of human operation picking diverse items (apple, banana, leaf) to introduce visual and shape diversity. 

- **Human Data (Background Var.):** 300 episodes (3 backgrounds _×_ 100 each) of human operation picking the bread with varied table textures and distractors. 

**Comparison Baselines.** We compare two primary policies: (1) _RobotOnly_ , trained solely on the 50 robot episodes; and (2) _Ours_ , trained using our two-stage framework (human pre-training _→_ robot fine-tuning). To validate our sequential design, we also attempted to train a policy by naively mixing human and robot data ( _Mix_ ). However, this baseline failed to converge and achieved a **0% success rate** , likely due to the conflicting gradient signals arising from the significant embodiment gap between human and robot kinematics. 

**Generalization Evaluation.** To demonstrate that our framework learns robust representations, we evaluate success rates across three out-of-distribution (OOD) settings: 

- 1) _UnseenPos:_ The object is placed in locations not covered in the robot dataset (but within the range of human data). 

- 2) _UnseenObj:_ The target object is replaced with new items unseen in robot data (but seen in human data). 

- 3) _UnseenBg:_ The background is altered with new tablecloths unseen in robot data (but seen in human data). 

**Results.** The quantitative results are reported in Table III. Each policy is evaluated for 30 trials under each setting. 

|**Settings**|**Seen**|**Unseen**<br>**Position**|**Unseen**<br>**Object**|**Unseen**<br>**Background**|
|---|---|---|---|---|
|Robot Data Only|29/30|12/30|10/30|9/30|
|**Ours**|**30/30**|**21/30**|**20/30**|**25/30**|


TABLE III: Policy Generalization Success Rate (%). We compare the policy trained only on robot data against our twostage approach leveraging human data. 

**Human data improves generalization at a lower cost.** As illustrated in Table III, the _RobotOnly_ policy suffers from severe overfitting. While it performs perfectly in the ”Seen” setting, its performance drops drastically (e.g., to 30% in UnseenBg) when facing distribution shifts. In contrast, _Ours_ significantly boosts robustness, improving success rates by nearly **2** _×_ **across all generalization settings** . This confirms that pre-training on diverse human data allows the policy to learn invariant visual features and high-level motion priors—such as ”reach towards the object regardless of background”—which are successfully transferred to the robot embodiment during fine-tuning. 

**Sequential training is essential for bridging the gap.** The complete failure of the _Mix_ baseline (0% success) highlights the challenge of the embodiment gap. Direct mixing forces the network to map similar visual states to two distinct action spaces (human vs. robot), causing optimization conflicts. Our sequential approach resolves this by using human data to learn generalizable features first, and then using robot data solely to adapt the action output to the robot’s specific kinematics, 

effectively combining the diversity of human data with the precision of robot data. 

## V. CONCLUSION 

We presented HumDex, a portable teleoperation system for humanoid whole-body dexterous manipulation. By combining IMU-based full-body motion capture with a learning-based dexterous hand retargeting module, HumDex enables reliable demonstration collection for long-horizon, contact-rich manipulation tasks that are difficult or infeasible for vision-based or infrastructure-heavy systems. Our system significantly improves data collection efficiency, teleoperation success rate, and downstream policy performance across a diverse set of whole-body manipulation tasks. 

Beyond teleoperation, HumDex enables efficient collection of human whole-body motion data in unconstrained environments. We show that, when leveraged through a two-stage imitation learning framework, such human data provides strong motion and perception priors that substantially improve generalization to unseen object positions, object categories, and visual backgrounds—while requiring only a small amount of robot-specific data for embodiment adaptation. Together, these results suggest that portable human motion capture, combined with appropriate training strategies, offers a practical path toward scalable data acquisition for general-purpose humanoid manipulation. We plan to open-source the full system to support future research in humanoid dexterous manipulation. 

## VI. LIMITATION. 

Although HumDex achieves strong whole-body dexterous manipulation capabilities, several challenges remain. First, due to computational and time constraints, we are unable to scale the training data to a larger scale, which may further improve performance. Second, while the collected hand data is sufficient for the tasks studied, extending to a broader range of hand postures, contact modes, and force-sensitive interactions remains an open challenge. Third, hardware payload limits and actuation strength prevent us from exploring potentially more capable manipulation behaviors. We leave addressing these limitations to future work. 

## REFERENCES 

- [1] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [2] Qingwei Ben, Feiyu Jia, Jia Zeng, Junting Dong, Dahua Lin, and Jiangmiao Pang. Homie: Humanoid locomanipulation with isomorphic exoskeleton cockpit. _arXiv preprint arXiv:2502.13013_ , 2025. 

- [3] Guanqi He and Wentao Zhang. Wujihand retargeting, 2025. URL https://github.com/wuji-technology/wuji retargeting. * Equal contribution. 

- [4] Liang Heng, Haoran Geng, Kaifeng Zhang, Pieter Abbeel, and Jitendra Malik. Vitacformer: Learning crossmodal representation for visuo-tactile dexterous manipulation, 2025. URL https://arxiv.org/abs/2506.15953. 

- [5] Liang Heng, Xiaoqi Li, Shangqing Mao, Jiaming Liu, Ruolin Liu, Jingli Wei, Yu-Kai Wang, Yueru Jia, Chenyang Gu, Rui Zhao, et al. Rwor: Generating robot demonstrations from human hand collection for policy learning without robot. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 13544–13551. IEEE, 2025. 

- [6] Liang Heng, Jiadong Xu, Yiwen Wang, Xiaoqi Li, Muhe Cai, Yan Shen, Juan Zhu, Guanghui Ren, and Hao Dong. Imagine2act: Leveraging object-action motion consistency from imagined goals for robotic manipulation. _arXiv preprint arXiv:2509.17125_ , 2025. 

- [7] Simar Kareer, Dhruv Patel, Ryan Punamiya, Pranay Mathur, Shuo Cheng, Chen Wang, Judy Hoffman, and Danfei Xu. Egomimic: Scaling imitation learning via egocentric video. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 13226– 13233. IEEE, 2025. 

- [8] Chenxuan Li, Jiaming Liu, Guanqun Wang, Xiaoqi Li, Sixiang Chen, Liang Heng, Chuyan Xiong, Jiaxin Ge, Renrui Zhang, Kaichen Zhou, and Shanghang Zhang. A self-correcting vision-language-action model for fast and slow system manipulation, 2025. URL https://arxiv.org/ abs/2405.17418. 

- [9] Jialong Li, Xuxin Cheng, Tianshu Huang, Shiqi Yang, Rizhao Qiu, and Xiaolong Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control. _Robotics: Science and Systems 2025_ , 2025. 

- [10] Xiaoqi Li, Liang Heng, Jiaming Liu, Yan Shen, Chenyang Gu, Zhuoyang Liu, Hao Chen, Nuowei Han, Renrui Zhang, Hao Tang, et al. 3ds-vla: A 3d spatialaware vision language action model for robust multitask manipulation. In _9th Annual Conference on Robot Learning_ . 

- [11] Xiaoqi Li, Jingyun Xu, Mingxu Zhang, Jiaming Liu, Yan Shen, Iaroslav Ponomarenko, Jiahui Xu, Liang Heng, Siyuan Huang, Shanghang Zhang, and Hao Dong. Object-centric prompt-driven vision-languageaction model for robotic manipulation. In _Proceedings_ 

_of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 27638–27648, June 2025. 

- [12] Yixuan Li, Yutang Lin, Jieming Cui, Tengyu Liu, Wei Liang, Yixin Zhu, and Siyuan Huang. Clone: Closed-loop whole-body humanoid teleoperation for long-horizon tasks. _arXiv preprint arXiv:2506.08931_ , 2025. 

- [13] Xiaoyi Lin, Kunpeng Yao, Lixin Xu, Xueqiang Wang, Xuetao Li, Yuchen Wang, and Miao Li. Dexflow: A unified approach for dexterous hand pose retargeting and interaction, 2025. URL https://arxiv.org/abs/2505.01083. 

- [14] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Casta˜neda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, Xingye Da, Runyu Ding, Cyrus Hogg, Lina Song, Edy Lim, Eugene Jeong, Tairan He, Haoru Xue, Wenli Xiao, Zi Wang, Simon Yuen, Jan Kautz, Yan Chang, Umar Iqbal, Linxi Fan, and Yuke Zhu. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [15] Zhao Mandi, Yifan Hou, Dieter Fox, Yashraj Narang, Ajay Mandlekar, and Shuran Song. Dexmachina: Functional retargeting for bimanual dexterous manipulation, 2025. URL https://arxiv.org/abs/2505.24853. 

- [16] Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3m: A universal visual representation for robot manipulation. _arXiv preprint arXiv:2203.12601_ , 2022. 

- [17] Ri-Zhao Qiu, Shiqi Yang, Xuxin Cheng, Chaitanya Chawla, Jialong Li, Tairan He, Ge Yan, David J Yoon, Ryan Hoque, Lars Paulsen, et al. Humanoid policy˜ human policy. _arXiv preprint arXiv:2503.13441_ , 2025. 

- [18] Ilija Radosavovic, Tete Xiao, Stephen James, Pieter Abbeel, Jitendra Malik, and Trevor Darrell. Real-world robot learning with masked visual pre-training. In _Conference on Robot Learning_ , pages 416–426. PMLR, 2023. 

human-to-robot retargeting for dexterous manipulation, 2025. URL https://arxiv.org/abs/2506.09384. 

   - [24] Zhao-Heng Yin, Changhao Wang, Luis Pineda, Krishna Bodduluri, Tingfan Wu, Pieter Abbeel, and Mustafa Mukadam. Geometric retargeting: A principled, ultrafast neural hand retargeting algorithm, 2025. URL https: //arxiv.org/abs/2503.07541. 

   - [25] Zhao-Heng Yin, Changhao Wang, Luis Pineda, Francois Hogan, Krishna Bodduluri, Akash Sharma, Patrick Lancaster, Ishita Prasad, Mrinal Kalakrishnan, Jitendra Malik, Mike Lambeta, Tingfan Wu, Pieter Abbeel, and Mustafa Mukadam. Dexteritygen: Foundation controller for unprecedented dexterity, 2025. URL https://arxiv.org/ abs/2502.04307. 

   - [26] Yanjie Ze, Zixuan Chen, Jo˜ao Pedro Ara´ujo, Zi ang Cao, Xue Bin Peng, Jiajun Wu, and C. Karen Liu. Twist: Teleoperated whole-body imitation system. _arXiv preprint arXiv:2505.02833_ , 2025. 

   - [27] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C. Karen Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025. 

   - [28] Rongyu Zhang, Menghang Dong, Yuan Zhang, Liang Heng, Xiaowei Chi, Gaole Dai, Li Du, Yuan Du, and Shanghang Zhang. Mole-vla: Dynamic layer-skipping vision language action model via mixture-of-layers for efficient robot manipulation, 2025. URL https://arxiv. org/abs/2503.20384. 

   - [29] Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware, 2023. URL https://arxiv. org/abs/2304.13705. 

- [19] SlimeVR Contributors. Slimevr: Open source fullbody tracking, 2025. URL https://github.com/SlimeVR/ SlimeVR-Server. Open-source full-body tracking server for virtual reality. 

- [20] Chen Wang, Haochen Shi, Weizhuo Wang, Ruohan Zhang, Li Fei-Fei, and C Karen Liu. Dexcap: Scalable and portable mocap data collection system for dexterous manipulation. _arXiv preprint arXiv:2403.07788_ , 2024. 

- [21] Philipp Wu, Yide Shentu, Zhongke Yi, Xingyu Lin, and Pieter Abbeel. Gello: A general, low-cost, and intuitive teleoperation framework for robot manipulators. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 12156–12163, 2024. doi: 10. 1109/IROS58592.2024.10801581. 

- [22] Tete Xiao, Ilija Radosavovic, Trevor Darrell, and Jitendra Malik. Masked visual pre-training for motor control. _arXiv preprint arXiv:2203.06173_ , 2022. 

- [23] Chendong Xin, Mingrui Yu, Yongpeng Jiang, Zhefeng Zhang, and Xiang Li. Analyzing key objectives in 

## APPENDIX 

## METHOD ADDITIONAL DETAILS 

## _A. Hardware Setup_ 

We visualize our hardware integration and teleoperation setup in Fig. A1. Our system is composed of three key components: 


(c) First-preson Robot View 

Fig. A1: **System Hardware Overview. (a)** The Unitree G1 Edu+ humanoid robot integrated with custom WUJI dexterous hands. **(b)** The human operator wearing the VIRDYN inertial motion capture suit and data gloves for immersive teleoperation. **(c)** Visual feedback is provided by the robot’s built-in RealSense camera. 

- **Robot Platform:** We utilize the **Unitree G1 Edu+** humanoid robot. This upgraded version features **29 active degrees of freedom (DoF)** to support complex wholebody locomotion and manipulation. For visual perception, we utilize the robot’s built-in Intel RealSense D435i camera to capture high-fidelity egocentric RGB observations. 

- **Dexterous Hands:** The robot is equipped with two custom **WUJI** dexterous hands. Each hand possesses **20 actuated DoFs** , featuring 4 independent DoFs per finger. This high-dimensional actuation space enables the execution of fine-grained manipulation tasks comparable to human hand dexterity. 

- **Teleoperation Interface:** A key advantage of our framework is its highly modular hardware design, allowing for the free combination of different body and hand tracking solutions. To ensure both accessibility and precision, we decouple the hardware into two independent modules: 

   - _Body Tracking Options:_ We provide two distinct full-body tracking configurations. The primary setup utilizes the **Vdmocap** 15-node commercial suit for high-precision baseline tracking on standard kinematic chains. As a highly cost-effective ( _<_ $200) 

alternative, we also custom-built a scalable system based on the open-source **SlimeVR** ecosystem. It employs ICM-45686 6-axis IMUs and nRF52840 SoCs (running the ESB protocol) to ensure stable, low-latency connectivity in complex Wi-Fi environments. 

- _Dexterous Hand Tracking Options:_ For fine-grained manipulation, the system integrates seamlessly with commercial high-fidelity inertial gloves, specifically supporting both **Vdhand** and **Manus** . Each glove utilizes an array of IMUs distributed across the dorsum and finger segments. This purely inertial approach ensures that complex grasping motions are accurately captured even under severe self-occlusion. 

Crucially, our control pipeline is hardware-agnostic. Operators can freely mix and match these body and hand modules without requiring any modifications to the underlying retargeting algorithms. 

## _B. Hand Retargeting Details_ 

**Data Collection.** To train the retargeting function, we collected a paired dataset of human hand poses and robot hand joint configurations. The operator wears the data glove and performs a predefined set of random finger movements and canonical poses. The corresponding robot joint angles are solved via an offline optimization-based IK solver to ensure kinematic feasibility. The collection process takes approximately 20 minutes, resulting in _∼_ 20k paired frames. 

**Training Hyperparameters.** The retargeting network is a Multi-Layer Perceptron (MLP). 

- **Architecture:** The IK model employs a finger-wise modular design. For each of the five fingers, the sub network is structured as: [Input(3) _→_ FC(128) _→_ LeakyReLU _→_ BN _→_ FC(128) _→_ LeakyReLU _→_ BN _→_ FC(4) _→_ Tanh]. The outputs from all sub-networks are concatenated to form the final Output(20). 

- **Optimizer:** AdamW ( _lr_ = 1 _e−_ 4, _β_ 1 = 0 _._ 9 _, β_ 2 = 0 _._ 999). 

- **Batch Size:** 2048. 

- **Epochs:** 300 (with early stopping based on validation loss). 

## _C. Data Collection Process_ 

We describe the specific protocols for the two data sources. All data is managed via a Redis-based distributed framework to ensure low-latency synchronization between vision and proprioception. 

## **1. Human Data Collection** 

- **Setup & Vision:** The operator wears the VIRDYN suit and gloves without active robot execution. To emulate the robot’s egocentric view, an Intel RealSense D435i camera is mounted on a neckband worn by the operator. 

- **Pipeline:** Raw motion capture data is processed via the General Motion Retargeting (GMR) model. This optimization-based solver maps human motion to the robot’s 35-DoF configuration space in real-time. 

- **Recorded Modalities:** We record the egocentric RGB images (640 _×_ 480 resolution) alongside the retargeted 35DoF whole-body targets (output of GMR) and 40-DoF bimanual hand targets (20 DoF per hand). 

- **Frequency & Trigger:** The teleoperation and retargeting loop runs at 100 Hz for smoothness, while the recorder saves data at 30 Hz. A USB foot pedal is used to trigger episode start/stop for clean segmentation. 

## **2. Robot Data Collection** 

- **Setup & Vision:** The operator controls the physical G1 robot via the teleoperation system. We utilize the robot’s built-in Intel RealSense D435i head camera for vision. 

- **Pipeline:** The operator’s motion is mapped to robot commands via the same GMR solver in real-time. These commands are executed by the robot and simultaneously fetched from Redis for recording, synchronized with the ZMQ video stream. 

- **Recorded Modalities:** We record the egocentric RGB images (640 _×_ 480 resolution) alongside the full robot state (23-DoF body + 40-DoF hand joints) and the applied action commands (35-DoF whole-body targets + 40-DoF bimanual hand targets). 

- **Frequency & Trigger:** The recording script runs at 30 Hz. Similar to the human phase, the same global foot pedal trigger is used to manage episode recording and save data in a standardized JSON + JPEG format. 

## _D. Policy Learning Details_ 

**Input/Output Modalities.** 

- **Observation Space:** Includes egocentric RGB images (480 _×_ 640) and robot joint positions (Whole Body 31 dimensions + 20 dimensions per hand). 

- **Action Space:** Target joint positions for the whole body (including 35 DoF for body and 20 DoF per hand). 

- **Network and Training.** We employ a standard Action 

- Chunking Transformer [29] backbone. 

- **Hardware:** All models are trained on a single NVIDIA RTX 4090 GPU. 

- **Single-stage training on robot data:** 8000 epochs for _HangTowel_ , _Scan&Pick_ , _OpenDoor_ and _PlaceBasketOnShelf_ , 5000 epochs for _PickBread_ . Initial learning rate 2 _e_<sup>_−_5</sup> . Batch size 16. Chunk size 200 for _PickBread_ , 400 for _OpenDoor_ and 300 for the rest. Takes 2 _∼_ 7 hours depending on demonstration trajectory length and number of episodes. 

- **Two-stage training with human data:** Stage 1 trained on human data only for 1000 epochs ( _∼_ 5 hours). Batch size 16. Stage 2 trained on robot data only for 4000 epochs ( _∼_ 3 hours). Batch size 16. 

- **Inference:** During deployment, the policy inference runs at 30 Hz. 

## ADDITIONAL EXPERIMENT DETAILS 

## _E. Teleoperation System Validation_ 

To assess the precision and reliability of our low-cost teleoperation solution, we conducted a comparative study against 

the commercial Vdmocap system. We also performed an ablation study on the number of trackers within the SlimeVR setup (14, 10, and 7 nodes). We selected three representative tasks from those detailed in the main paper— _HangTowel_ , _PlaceBasketOnShelf_ , and _PickBread_ —to evaluate performance across different manipulation complexities. 

- As shown in Table A1, the results indicate that: 

- **Commercial vs. Low-Cost:** The 14-node SlimeVR setup achieves a success rate comparable to the commercial baseline (e.g., 48/60 vs. 50/60 on _HangTowel_ ), proving that our _<_ $200 solution is sufficient for high-quality data collection. 

- **Tracker Density:** Reducing tracker count degrades performance, particularly in whole-body tasks. While the 10node setup remains robust for simpler reaching ( _PlaceBasket_ ), the 7-node configuration suffers a significant performance drop (42/60 on _HangTowel_ ), highlighting the necessity of the full 14-node configuration for complex, coordinated manipulation. 

TABLE A1: **Teleoperation Success Rate Comparison.** We report success trials out of 60 attempts. The 14-node SlimeVR setup yields performance close to the commercial VIRDYN suit, whereas reducing nodes (7 or 10) leads to lower reliability in complex tasks. 

|**Task**|**VIRDYN**|**SlimeV**|**R Configur**|**iations**|
|---|---|---|---|---|
|||**14 Nodes**|**10 Nodes**|**7 Nodes**|
|_HangTowel_|50/60|48/60|44/60|42/60|
|_PlaceBasket_|58/60|57/60|57/60|51/60|
|_PickBread_|55/60|55/60|54/60|53/60|


## _F. Failure Case Analysis_ 

We provide a qualitative analysis of typical failure modes observed across the five tasks. Representative failure sequences are visualized in Fig. A2. 

Detailed analysis for each task is as follows: 

- **Scan & Pack (Dexterous Manipulation Failure):** As shown in the first row of Fig. A2, the primary failure mode is the inability to trigger the scanner. This typically occurs when the initial grasp on the scanner handle is too low or rotated. Although the robot holds the object, the thumb’s kinematic reach is restricted, preventing it from pressing the button effectively. 

- **Hang Towel (Bimanual Coordination Failure):** Failures in this task often stem from spatial misalignment between the left hand (holding the hanger) and the right hand (holding the towel). If the coordination policy fails to synchronize the two end-effectors precisely, the towel may hit the rim of the hanger and fall, rather than threading through the bar. 

- **Open Door (Loco-Manipulation Failure):** The crucial failure mode involves the coordination between the arm and the base. In some cases, the robot successfully 


Fig. A2: **Visualization of Failure Cases.** We showcase common failure modes for each task: (a) **Scan&Pack:** The thumb fails to press the trigger due to an inappropriate initial grasp. (b) **Hang Towel:** The towel misses the hanger due to misalignment between the two hands. (c) **Open Door:** The robot unlatches the door but fails to open it fully ( _>_ 45<sup>_◦_</sup> ) due to insufficient forward locomotion. (d) **Place Basket:** The basket is not placed stably due to whole-body uncoordination and foot instability. (e) **Pick Bread:** The robot grasps empty air due to estimation errors when the bread is placed in an unseen generalized position. 

unlatches the door handle, but the locomotion policy fails to execute a continuous forward walk. Consequently, the door is merely unlatched or slightly ajar but does not reach the required 45<sup>_◦_</sup> opening angle. 

- **Place Basket (Whole-Body Stability Failure):** This task requires significant vertical motion (squatting and standing). Failures occur when the robot loses balance or exhibits jittery foot movement during the lifting phase. This instability propagates to the upper body, causing the basket to be placed on the edge of the shelf and subsequently fall off. 

- **Pick Bread (Generalization Failure):** When evaluating on unseen positions (Generalization Setting), the policy occasionally fails to adapt to large spatial shifts. As illustrated in the last row, the robot may execute a grasp at a position offset from the actual bread, resulting in a 

grasp on empty air. This indicates the limitations of the policy’s spatial generalization boundary. A3 

## _G. Generalization Setting Details_ 

To evaluate whether the diversity of our large-scale human data is effectively transferred to the robot, we introduce three generalization categories beyond the standard ”Seen Setting”. Specifically, the **Seen Setting** aligns with the constrained distribution of the _Robot Data_ (used for fine-tuning), while the **Generalization Settings** (Position, Object, Background) mimic the extensive variations present in the _Human Data_ (used for pre-training). The visual configurations are illustrated in Fig.. 

- **Seen Setting (Robot Domain):** This setting replicates the exact distribution of the robot fine-tuning data. The object 


Fig. A3: **Generalization Protocols.** We evaluate the policy under four conditions: (a) **Seen Setting:** Matches the robot finetuning data (fixed setup). (b) **Position Generalization:** Random initialization within a bounding box, reflecting spatial variance in human data. (c) **Object Generalization:** Unseen instances (Apple, Banana, Leaf) to test semantic robustness. (d) **Background Generalization:** Unseen table textures (Pink, Blue, Green) to test visual robustness. 

position is fixed (or has negligible variance), and the object instance and background texture remain identical to the specific tasks defined in the fine-tuning stage. 

- **Position Generalization:** To verify if the policy inherits spatial awareness from human data, we randomize the target object’s position. The object is placed at random coordinates ( _x, y_ ) within a predefined **bounding box** (e.g., 22 _._ 5 _cm ×_ 18 _._ 0 _cm_ ) on the table surface. This forces the robot to dynamically adapt its approach trajectory rather than overfitting to a fixed motion path. 

- **Object Generalization:** We replace the manipulation 

target with semantically similar but geometrically distinct objects (e.g., replacing a standard bread with an **Apple** , **Banana** , or **Leaf** ). This tests whether the representation learned from diverse human interactions allows the robot to handle novel shapes and grasp affordances zero-shot. 

- **Background Generalization:** We drastically alter the workspace appearance by covering the table with **Pink** , **Blue** , and **Green** tablecloths. This evaluates the vision encoder’s ability—gained from the diverse visual backgrounds in human data—to ignore task-irrelevant shifts and focus on the target object. 

