---
title: "A Closed-Form Geometric Retargeting Solver for Upper Body Humanoid Robot Teleoperation"
date: "2026-02-02"
authors: "Chuizheng Kong; Yunho Cho; Wonsuhk Jung; Idris Wibowo; Parth Shinde; Sundhar Vinodh-Sangeetha"
url: https://arxiv.org/abs/2602.01632
pdf: https://arxiv.org/pdf/2602.01632
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.01632)** / [論文ページ](https://arxiv.org/abs/2602.01632)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **A Closed-Form Geometric Retargeting Solver for Upper Body Humanoid Robot Teleoperation** 

Chuizheng Kong<sup>†</sup> , Yunho Cho<sup>†</sup> , Wonsuhk Jung<sup>†</sup> , Idris Wibowo<sup>_∗_†</sup> , Parth Shinde<sup>_∗∥_</sup> , Sundhar Vinodh-Sangeetha<sup>_∗_‡</sup> , Long Kiu Chung<sup>§</sup> , Zhenyang Chen<sup>†</sup> , Andrew Mattei<sup>§</sup> , Advaith Nidumukkala<sup>§</sup> 

Alexander Elias<sup>_∗∗_</sup> , Danfei Xu<sup>†¶</sup> , Taylor Higgins<sup>††</sup> , and Shreyas Kousik<sup>†§</sup> 

_∗_ denotes equal contribution 

- Institute for Robotics and Intelligent Machines 

‡ School of Aerospace Engineering 

- § Woodruff School of Mechanical Engineering 

¶ School of Interactive Computing 

Georgia Institute of Technology, Atlanta, Georgia 30332 

_∥_ Qualcomm, San Diego, California 92121 

_∗∗_ Standard Bots, Glen Cove, New York 11542 

†† Department of Mechanical & Aerospace Engineering 

Florida A&M University-Florida State University, Tallahassee, Florida 32130 


Fig. 1: We propose SEW-Mimic for retargeting human shoulder, elbow, and wrist (SEW) keypoints analytically to robot manipulator joint angles. Our key insight is to focus on limb and hand/tool _orientation error_ as a metric of pose similarity, because it enables a closed-form, provably-optimal retargeting solution that is scale independent, as shown here on Kinova Gen3, Rainbow RB-Y1, and Unitree G1 platforms (shown to scale). Since SEW-Mimic is computationally fast, we use it as an inverse kinematics (IK) solver within a safety filter to prevent self-collisions for bimanual teleoperation. 

**_Abstract_ —Retargeting human motion to robot poses is a practical approach for teleoperating bimanual humanoid robot arms, but existing methods can be suboptimal and slow, often causing undesirable motion or latency. This is due to optimizing to match robot end-effector to human hand position and orientation, which can also limit the robot’s workspace to that of the human. Instead, this paper reframes retargeting as an orientation alignment problem, enabling a closed-form, geometric solution algorithm with an optimality guarantee. The key idea is to align a robot arm to a human’s upper and lower arm orientations, as identified from shoulder, elbow, and wrist (SEW) keypoints; hence, the method is called SEW-Mimic. The method has fast inference (3 kHz) on standard commercial CPUs, leaving computational overhead for downstream applications; an example in this paper is a safety filter to avoid bimanual self-collision. The method suits most 7- degree-of-freedom robot arms and humanoids, and is agnostic to input keypoint source. Experiments show that SEW-Mimic outperforms other retargeting methods in computation time and accuracy. A pilot user study suggests that the method improves teleoperation task success. Preliminary analysis indicates that data collected with SEW-Mimic improves policy learning due to being smoother. SEW-Mimic is also shown to be a drop-in way to accelerate full-body humanoid retargeting. Finally, hardware** 

**demonstrations illustrate SEW-Mimic’s practicality. The results emphasize the utility of SEW-Mimic as a fundamental building block for bimanual robot manipulation and humanoid robot teleoperation.** 

## I. INTRODUCTION 

Retargeting is the process of mapping human poses to robot configurations. For robot teleoperation, this offers a human-centered way to control high degree-of-freedom (DoF) robots, by which training data can be collected for autonomous policies [38]. However due to physical differences between human and robot embodiments, such as size, DoFs, and motion constraints, the retargeting problem can be nontrivial. 

As a result, most existing systems only track human hand motion [18, 17, 8, 6, 34]. These methods solve retargeting as an end-effector inverse kinematics (IK) problem using robot’s Jacobian Matrix [19] whose inverse maps 6-DoF endeffector velocity to robot joint velocities (6-DoF / 7-DoF). This approach prevents robot teleoperation near the limit of the robot’s range of motion or near other joint singularity poses 

due to the inverse becoming degenerate. While degeneracy can be mitigated for 6-DoF arms using pseudo-inverse [5] or optimization-based IK [43], humanoid arms are typically 7-DoF to match human arms. When using 6-DoF hand-only retargeting method, part of the 7-DoF arm corresponding to the human elbow joint can produce unwanted null-space motion [9], increasing collision risk (see Fig. 6 in Sec. VI). 

To overcome limitations from hand-only retargeting, recent learning-based humanoid retargeting approaches optimize over robot joint angles to match the robot to human body keypoints (shoulder, elbow, wrist, ankles, etc.) [44, 21, 15]. While minimizing the Euclidean distance between the human and robot keypoints includes the elbow, solving such a program can average 0.7 seconds [44]. When used in real-time teleoperation for data collection, this delay can insert hesitant behavior, reducing the quality of trained policies. 

This paper addresses the issues of hands-only teleoperation and inference delays by proposing SEW-Mimic, a closedform, provably-optimal, geometric (keypoint-based) retargeting algorithm (see Fig. 1). Unlike existing retargeting methods, SEW-Mimic does not use the robot’s Jacobian matrix or iteratively solve optimization. Instead, it performs pose-retargeting using geometric subproblems [29, 27] similar to [10, 9, 28] that solve end-effector IK. We define human limb vectors as unit vectors between keypoints (shoulder, elbow, wrist, etc.), then solve for robot joint angles that maximize _pose similarity_ by aligning these vectors with corresponding robot limb vectors (see Fig. 2). Critically, we define pose similarity through _orientation error_ , as opposed to Euclidean error, which makes our method calibration-free between different human and robot sizes. 

_Contributions:_ We make three key contributions: 

- We propose SEW-Mimic as a fast, optimal algorithm for upper body humanoid retargeting and teleoperation. 

- We propose a safety filter that uses SEW-Mimic to avoid self collisions for bimanual teleoperation. 

- We provide open-source, standalone applications to integrate SEW-Mimic with either MediaPipe [22] or a Meta Quest headset for teleoperation, and a live web demo to show computation speed (code and web demo to be released after review). 

Furthermore, extensive experiments show that SEW-Mimic not only has high pose similarity and low computation speed, but also impacts teleoperation success rate, autonomous policy learning, and full-body humanoid retargeting speed. We also demonstrate SEW-Mimic on several hardware platforms. 

_Paper Organization:_ Sec. III introduces notation and preliminaries. Sec. IV then details our proposed retargeting problem and solution. Sec. V develops a safety filter for teleoperation. Sec. VI presents experiments evaluating our approach, and Sec. VII presents hardware demonstrations. Finally, Sec. VIII provides concluding remarks and a discussion of limitations. We also provide an extensive appendix. 

## II. RELATED WORK 

State-of-the-art bimanual and full-body robot teleoperation systems can be categorized into hardware puppeteering (Sec. II-A) and software pose retargeting (Sec. II-B). We now review popular works in each category in terms of _computation speed_ and _pose similarity_ (orientation alignment between human and robot links per Sec. I). Our approach uses analytical geometric IK, which we discuss last (Sec. II-C). 

## _A. Hardware-based Teleoperation_ 

Hardware puppeteering pairs target robot arms with leader arm hardware such that a human operator directly provides joint angle commands to the robot (e.g., ALOHA [12] and GELLO [41]). This approach has high _computation speed_ , but low _pose similarity_ due to the embodiment gap of the operator directly controlling robot joints rather than the robot mimicking human arm poses. This issue can be solved with more human-centric leader arms functioning as exoskeleton cockpits [16, 42, 45, 4], but such hardware impacts accessibility and applicability across a variety of robots. We provide a software-based approach that targets similar pose similarity and computation speed to exoskeleton cockpits. 

## _B. Software-based Retargeting Teleoperation_ 

Software-based methods generally support more robot embodiments, but often lack _computation speed_ and/or _pose similarity_ . Such methods usually obtain human motion from cameras or wearable devices and use inverse kinematics (IK) to retarget them to either end-effector motion or the entire arm. 

_1) End-Effector Retargeting:_ Methods in this category typically focus on an operator’s 6D hand pose data (e.g., DexMimicGen [18] and OpenTeach [17]) and compute IK for the corresponding robot joint configurations with solvers such as Mink [43] and OSC [19]; thus, they treat teleoperation as moving the two end-effectors freely in the 3D workspace. This approach, however, struggles when end-effector motion is limited by the arm configurations, especially for singularities at full extension that can cause reduce numerical stability and computation speed [28]. By contrast, our method does not require a Jacobian and thus does not suffer numerical stability issues near singularities. Other optimization-based IK methods avoid entering singularities poses in the first place (e.g., BunnyVisionPro [8] and Open-TeleVision [6] in Unitree’s xr_teleoperate [34]) by using a weighted Jacobian pseudo-inverse (typically solved with Pinocchio [5]). However, for 7DoF humanoid arms, these methods exhibit non-cyclicity due to the redundant DoF [9]: when the robot end-effector returns to a previously visited pose, the elbow may not return to its original position. To alleviate this, OSC [19] allows the user to define a secondary objective in joint space (such as preserving initial joint angles) by projecting the joint error to the Jacobian nullspace. However since we cannot directly map human elbow pose to the robot joint space without solving IK first, this approach still does not give the human operator direct control over the robot’s elbow pose, 

further exacerbating a lack of _pose similarity_ . By contrast, our method enables direct elbow control. 

_2) Keypoint-Based Retargeting:_ To circumvent Jacobian singularities and handle complex full-body humanoid dynamics, several methods use customized optimization cost coupled with large human motion datasets (e.g., AMASS [24]) to train real-time retargeting and balance policies (e.g., H2O [15], CLONE [21], and TWIST [44]). These methods exhibit high _pose similarity_ , but often still suffer large joint position errors that make dexterous tasks difficult compared to iterative methods [18]. Furthermore, these methods suffer high latency (around 0.7 second), some due to a combination of slow convergence of complex optimization programs and wireless communication; this can cause a teleoperator to teach a robot hesitant behaviors [44]. While we do not address communication latency, our method enables high computation speed to help address the overall latency challenge. SEW-Mimic works as a drop-in replacement for General Motion Retargeting (GMR), which TWIST uses as a kinematic initial guess. We treat each leg’s hip-knee-ankle as shoulder-elbow-wrist to give TWIST similar retargeting accuracy to GMR but 1-3 orders of magnitude faster computation speed (see Sec. VI-E). 

## _C. Analytical Geometric IK Solvers_ 

To avoid the above challenges stemming from hardware limitations, Jacobian singularities, and low computation speed, an alternative approach is to use analytical IK solvers, which typically focus on 6DoF manipulators. Such methods have a long history [31, 30], but have recently been improved by ik-geo [10] and EAIK [28]. In particular, [10] provides convenient solutions to the Paden-Kahan subproblems [30] that underlie analytical IK through closed-form, geometric decomposition. A recent follow-up to ik-geo, stereo-sew [9], parameterizes the redundant joint of 7-DoF arms using elbow angles while applying subproblem decomposition for endeffector pose IK; this results in either a closed-form solution or a low-dimensional search, depending on the robot’s morphology. These approaches enable rapid computation speed, but focus on pure IK as opposed to retargeting for high pose similarity. By contrast, SEW-Mimic directly addresses pose similarity while preserving high computation speed by always having a closed-form solution. We note that considering an elbow angle for analytical IK is not new [20, 2, 9, 36], but our SEW keypoint approach in retargeting is novel, to the best of our knowledge. 


Fig. 2: Comparison of human arm with keypoints and 7- DOF upper body robot arm showing links (boxes) and joints (cylinders show rotation axes). 

The _n_ -dimensional identity matrix is **I** _n_ . An _n × m_ array of zeros is **0** _n×m_ . The pseudoinverse of a matrix **A** is **A**<sup>†</sup> . For consistency with numbered robot joints, indexing starts at 1. The _i_<sup>th</sup> element of a vector is **v** [ _i_ ], elements _i_ to _j_ are **v** [ _i_ : _j_ ], and the ( _i, j_ )th element of an array is **A** [ _i, j_ ]. We concatenate vectors **a** _,_ **b** as ( **a** _,_ **b** ) = [ **a**<sup>_⊤_</sup> _,_ **b**<sup>_⊤_</sup> ]<sup>_⊤_</sup> . Subscripts indicate labels and superscripts indicate coordinate frames. 

_Common Operations:_ Given a rotation axis **h** _∈_ R<sup>3</sup> and a rotation angle _α ∈_ R, we use Rodrigues’ formula to create the corresponding rotation matrix: 


where sk : R<sup>3</sup> _→_ R<sup>3</sup><sup>_×_3</sup> is the standard “hat” operator that returns a skew-symmetric matrix. We normalize vectors to unit length as unit( **v** ) = **v** _/ ∥_ **v** _∥_ 2. For steps of an algorithm, we use _x ← y_ to denote that variable _x_ has been assigned value _y_ . 

_Coordinate Frames:_ Denote the robot baselink frame as the 0<sup>th</sup> frame. We represent coordinate frames via a rotation matrix and translation vector with respect to the 0<sup>th</sup> frame. For example, frame “f” is ( **R**<sup>0</sup><sup>_,_f</sup> _,_ **p**<sup>0</sup><sup>_,_f</sup> ), and a vector **v** in that frame is **v**<sup>f</sup> . For objects in the inertial frame, we omit the frame label when clear from context. Given two frames ( **R**<sup>0</sup><sup>_,_a</sup> _,_ **p**<sup>0</sup><sup>_,_a</sup> ) and ( **R**<sup>0</sup><sup>_,_b</sup> _,_ **p**<sup>0</sup><sup>_,_b</sup> ), we transform from a to b in the standard way: 


Numbered frames (typically indexed by _i_ ) refer to robot links, whereas other frames are in regular text (e.g. “hm” for the human and “in” for an 3-D keypoint input data stream). 

## III. PRELIMINARIES 

We now introduce notation, model human and robot limbs, and review canonical geometric subproblems used as building blocks for our method. 

## _A. Notation_ 

_Conventions:_ We denote the real numbers as R, the natural numbers as N, and the space of 3-D rotation matrices as SO(3). Scalars are in italic font, such as _x ∈_ R. Vectors and matrices are in bold font, such as **x** _∈_ R<sup>_n_</sup> and **A** _∈_ R<sup>_n×m_</sup> with _n, m ∈_ N. 

## _B. Human and Robot Arm Descriptions_ 

Our method retargets a human limb pose to a corresponding robot limb on a humanoid robot. For ease of exposition, the majority of the paper focuses on a single limb (right arm). The following concepts are shown in Fig. 2. 

_1) Human Arm:_ We consider a tuple of 3-D keypoints representing shoulder **s** , elbow **e** , and wrist **w** , plus a rotation matrix **H** representing the orientation of the person’s hand relative to the 0<sup>th</sup> frame, as shown in Fig. 2. That is, the input 

to our method is ( **s** _,_ **e** _,_ **w** _,_ **H** ) _∈_ R<sup>3</sup> _×_ R<sup>3</sup> _×_ R<sup>3</sup> _×_ SO(3). 

IV. PROPOSED APPROACH 

**Remark 1** (Body-Centric Frame) **.** _Our notation implies all keypoints are in a shared_ 0 _th body-centric frame, which we take as an assumption going forward. We discuss how to ensure this in Sec. B._ 

_2) Robot Arm:_ We consider a 7-DoF series kinematic chain of rotational actuators, where consecutive joints rotate perpendicular to each other, as shown in Fig. 2. We define a rotation angle _qi_ and rotation axis **h**<sup>_i_</sup> _i_<sup>ineachlink’slocalcoordinate</sup> frame for each _i_<sup>th</sup> DoF, where _i_ = 1 is the first joint, resulting in a pose vector **q** = � _q_ 1 _, q_ 2 _, ··· , qn_ � _⊤_ . Each _i_ th joint is associated with a rigid link, with local coordinate frame represented in predecessor frame _i −_ 1 by a rotation matrix and translation vector ( **R**<sup>_i_</sup> local<sup>_−_1</sup><sup>_,i,_</sup><sup>**p**</sup><sup>_i_</sup> local<sup>_−_1</sup><sup>_,i_).Theorientationdifferencebetweenthe</sup> ( _i −_ 1)<sup>th</sup> and _i_<sup>th</sup> local frames is the product between the known fixed local orientation difference and varying axis rotation from _qi_ : **R**<sup>_i−_1</sup><sup>_,i_</sup> ( _qi_ ) = **R**<sup>_i_</sup> local<sup>_−_1</sup><sup>_,iR_(</sup><sup>**h**</sup><sup>_i,qi_).Thentheorientation</sup> difference between the _i_<sup>th</sup> and _j_<sup>th</sup> frames is given by a product of rotation matrices per standard rigid body kinematics. To represent rotation axis **h** _i_ in the _j_<sup>th</sup> local coordinate frame, we write **h** _i_<sup>_j_=</sup><sup>**R**</sup><sup>_j,i_(</sup><sup>**q**)</sup><sup>**h**</sup> _i_<sup>_i_.Finally,wedenotetherobot’send</sup> effector orientation as **T** ( **q** ) = ∏<sup># DOFs</sup> _i_ =1 **R**<sup>_i−_1</sup><sup>_,i_</sup> ( **q** ) **R** align, where **R** align is a fixed transformation such that the end effector obeys a right-hand rule convention; in the case of a dexterous hand, “X/Y/Z” corresponds to index finger extended / palm normal / thumb extended, and “X” is the end effector pointing direction (i.e., normal to the flange). 

## _C. Canonical Geometric Subproblems_ 

We solve retargeting by applying canonical geometric subproblems with closed-form solutions from Elias and Wen [10], which extend classical methods [30, 27]. 

_Subproblem 1:_ Consider two vectors **p** 1 _,_ **p** 2 _∈_ R<sup>3</sup> and a unit vector **k** _∈_ R<sup>3</sup> , representing a rotation axis. Rotate **p** 1 about **k** to align it with **p** 2. That is, find the optimal angle _θ_<sup>_⋆_</sup> that minimizes _∥R_ ( **k** _, θ_ ) **p** 1 _−_ **p** 2 _∥_ : 


We solve Subproblem 1 in closed form using Algorithm 5 (in Sec. A). 

_Subproblem 2:_ Consider two vectors **p** 1 _,_ **p** 2 _∈_ R<sup>3</sup> and two rotation axes **k** 1 _,_ **k** 2 _∈_ R<sup>3</sup> . Align **p** 1 with **p** 2 by simultaneously rotating **p** 1 around **k** 1 and rotating **p** 2 around **k** 2. That is, find a pair of optimal rotation angles: 


where there may be 1 or 2 unique optimizers per joint angle pair. We solve Subproblem 2 in closed form using Algorithm 6 (in Sec. A), which uses Paden-Kahan Subproblem 4 also presented in Sec. A. 

To detail our proposed approach, we first state retargeting as an orientation alignment problem (Sec. IV-A), then present our SEW-Mimic algorithm (Sec. IV-B), and finally show that our method is optimal (Sec. IV-C). 

## _A. Problem Statement_ 

We seek to align an arbitrary robot arm with given human arm keypoints ( **s** _,_ **e** _,_ **w** _,_ **H** ) while accommodating the fact that the robot may have different link and limb lengths. Thus, unlike other methods that focus on keypoint position error (potentially in weighted combination with orientation error [1]), we focus entirely on orientation error between the human and robot upper arms, lower, arms, and wrists. This orientation-focused approach has both theoretical and practical benefits: it enables an optimal geometric solution (Sec. IV-C) and applies directly to teleoperating robots with different sizes and proportions from humans (Secs. VI and VII). 

Before writing our problem, we define the human and robot upper arm, lower arm, and wrist as follows. We convert input human keypoints to upper and lower arm unit vectors: **u** _←_ unit( **e** _−_ **s** ) and **l** _←_ unit( **w** _−_ **e** ). For the robot, we use the 3<sup>rd</sup> joint rotation axis **h** 3 as the upper arm direction, which we find applies for a variety of manipulator robots (see Sec. VI). Similarly, we treat the robot’s lower arm as its 5<sup>th</sup> joint rotation axis **h** 5. Note that these human and robot vectors are generally given in two separate coordinate frames. We propose a calibration-free procedure to sync the coordinate frames in Sec. B. For the wrist, we use the human hand orientation **H** as a target for aligning the robot end effector orientation **T** ( **q** ). We assume the end effector mount normal is parallel to the final joint axis, and discuss the perpendicular case in Sec. C. Now we are ready to state our retargeting problem. 

**Problem 2.** _We pose the retargeting problem as_ 


_where vector orientation error is given by cosine similarity_ 


_and rotation matrix orientation error is_ 


_where ∥·∥_ F _is the Frobenius norm._ 

Note we use a minor modification of the standard chordal rotation matrix error metric [13], where the square root scales the error to [0 _,_ 2] and makes it more linear near 0; this is not critical to our method, but provides nicer behavior for comparing errors between retargeting methods. Next, we solve Problem 2 by minimizing each cost term separately. 


Fig. 3: SEW-Mimic takes in human arm keypoints (left) and aligns the robot’s upper arm, then lower arm, then wrist. 

## _B. Proposed Solution_ 

Our closed-form geometric retargeting method operates iteratively down the arm from shoulder to elbow to wrist as shown in Fig. 3, so we call it SEW-Mimic for “Shoulder-ElbowWrist Mimic.” Our approach is summarized in Algorithm 1. Here, we provide supporting explanation. 

_1) Upper and Lower Arm Alignment:_ We begin by creating the robot pose and upper and lower arm vectors (Algorithm 1– Algorithm 1). Second, we align the robot’s **h** 3 axis with the human upper arm **u** (Algorithm 1). Third, we similarly align **h** 5 with the human lower arm **l** (Algorithm 1). For both of these alignment steps, we solve for two joint angles at a time using Algorithm 2. 

_2) Aligning Joint Axes to Given Vectors:_ Algorithm 2 aligns the _i_ th robot joint axis **h** _i_ to a given vector **v** (i.e., minimize _µ_ c( **h** _i,_ **v** )) by finding optimal angles for joints _i −_ 1 and _i −_ 2. We operate in the _i −_ 2 coordinate frame (Algorithm 2– Algorithm 2) map to that frame), and uses Subproblem 2 (Algorithm 6) to find the predecessor joint angles (Algorithm 2). We filter out solutions that do not obey joint angle limits (Algorithm 2); note, this does _not_ consider self-collision, which we handle with a safety filter in Sec. V. Finally, we choose the closest solution to the robot’s current configuration (Algorithm 2). 

_3) Wrist Alignment:_ We seek to have the tool orientation **T** ( **q** ) match the desired hand orientation by solving for ( _q_ 5 _, q_ 6 _, q_ 7). We assume the wrist has the end effector mount pointing parallel to the 7th joint axis per Sec. III-B2. Then, we apply Subproblem 2 to find _q_ 5 and _q_ 6 that align **h** 7 with the human hand pointing direction (Algorithm 3), and finally Subproblem 1 to solve for _q_ 7. 

## _C. Optimality of Proposed Algorithm_ 

To conclude the section, we confirm that Algorithm 1 returns an optimal solution to Problem 2. 

**Proposition 3.** _Consider a robot arm with consecutive perpendicular joint axes, baselink mounted in a humanoid configuration as shown in Fig. 2(b), and no joint angle limits or self-collisions. Suppose the robot is at an initial configuration_ **q** 0 _. Suppose we are given keypoints of the human shoulder_ **s** _, elbow_ **e** _, and wrist_ **w** _, and a hand orientation_ **H** _. Using Algorithm 1, compute_ **q** _←_ SEW-Mimic( **q** 0 _,_ **s** _,_ **e** _,_ **w** _,_ **H** ) _. Then_ **q** _is a global optimizer of Problem 2._ 

See Sec. D for the proof. Note that the solution is optimal _in the body-centric frame_ , meaning that human input torso 

- **Algorithm 1: q** _←_ SEW-Mimic( **q** 0 _,_ **s** _,_ **e** _,_ **w** _,_ **H** ) **Input:** Initial robot pose **q** 0, human shoulder position **s** , human elbow position **e** , wrist position **w** , and human hand orientation **H** 

- **1** // Sync human and robot frames per Sec. B **q** _←_ **q** 0 // Initialize solution 

- **2** // Get upper and lower arm pointing directions **u** _←_ unit( **e** _−_ **s** ) and **l** _←_ unit( **w** _−_ **e** ) 

- **3** // Find ( _q_ 1 _, q_ 2) by aligning **h** 3 (proxy for robot upper arm) with **u** using Subproblem 2 per Algorithm 2 **q** [1 : 2] _←_ AlignAxis(3 _,_ **q** _,_ **u** ) 

- **4** // Find ( _q_ 3 _, q_ 4) by aligning **h** 5 (proxy for robot lower arm) with **l** using Subproblem 2 per Algorithm 2 **q** [3 : 4] _←_ AlignAxis(5 _,_ **q** _,_ **l** ) 

- **5** // Align wrist to get **q** [5 : 7] **q** [5 : 7] _←_ AlignWrist( **q** _,_ **H** ) // See Algorithm 3 

- **Return:** Retargeted robot pose **q** 

**Algorithm 2:** Align Joint Axis _i_ to a Given Vector ( _q_<sup>_⋆_</sup> _i−_ 2<sup>_,q⋆_</sup> _i−_ 1<sup>)</sup><sup>_←_AlignAxis(</sup><sup>_i,_</sup><sup>**q**0</sup><sup>_,_</sup><sup>**v**)</sup> Align the _i_ th joint axis **h** _i_ with a vector **v** by solving for the axis’ predecessor joint angles _qi−_ 2 and _qi−_ 1 **Input:** joint index _i_ , current configuration **q** 0, and vector to align with **v 1 v**<sup>_i−_2</sup> _←_ [ **R**<sup>0</sup><sup>_,i−_2</sup> ( **q** 0)]<sup>_⊤_</sup> **v** // Put vector into _i −_ 2 frame **2 h**<sup>_i_</sup> _i−_ 2<sup>_←_</sup><sup>**R**</sup><sup>_i−_2</sup><sup>_,i_(</sup><sup>**q**0)</sup><sup>**h**</sup><sup>_i_//Putjointaxesin</sup><sup>_i−_2frame</sup> **3 h**<sup>_i_</sup> _i_<sup>_−_</sup> _−_<sup>1</sup> 2<sup>_←_</sup><sup>**R**</sup><sup>_i−_1</sup><sup>_,i_(</sup><sup>**q**0)</sup><sup>**h**</sup><sup>_i−_1</sup> **4** // SP2 aligns **h** _i_ to **v** and returns up to 2 pairs of sols., indexed here by _j_ **5** _{_ ( _qi−_ 2 _, qi−_ 1) _j} ←_ SP2( **v**<sup>_i−_2</sup> _,_ **h**<sup>_i_</sup> _i_<sup>_−_2</sup> _, −_ **h** _i−_ 2 _,_ **h**<sup>_i_</sup> _i_<sup>_−_</sup> _−_<sup>2</sup> 1<sup>)</sup> **6** _{_ ( _qi−_ 2 _, qi−_ 1) _j} ←_ BoundJoints( _{_ ( _qi−_ 2 _, qi−_ 1) _j}_ ) **7** // Update pose with closest angles to init. pose ( _q_<sup>_⋆_</sup> _i−_ 2<sup>_,q⋆_</sup> _i−_ 1<sup>)</sup><sup>_←_argmin</sup> _a,b_<sup>_|_</sup><sup>**q**0[</sup><sup>_i−_2]</sup><sup>_−a|_+</sup><sup>_|_</sup><sup>**q**0[</sup><sup>_i−_1]</sup><sup>_−b|_</sup> s.t. ( _a, b_ ) _∈{_ ( _qi−_ 2 _, qi−_ 1) _j}_ **Return:** Joint angle solution ( _q_<sup>_⋆_</sup> _i−_ 2<sup>_,q⋆_</sup> _i−_ 1<sup>)</sup> 

motion must be canceled out (as per Sec. B) before passing keypoints to SEW-Mimic. Also note, our claim is in the absence of joint angle limits, safety filtering for self-collision avoidance, or joint controller tracking error. That said, our experiments (Sec. VI) indicate a variety of benefits from this optimality. 

## V. SAFETY FILTER FOR SELF-COLLISIONS 

To mitigate the risk of self-collision in bimanual teleoperation, we create a safety filter that takes advantage of our SEW representation. We design it to remove only the harmful component of a user command, preserving tangential motion to collisions so the robot can be operated along safe directions. While the filter does not provide formal guarantees (left to 

**Algorithm 3:** Align Robot Wrist to Hand Orientation <u>(</u> _q_ 5 _, q_ 6 _, q_ 7) _←_ AlignWrist( **q** 0 _,_ **H** <u>)</u> 

**Input:** Init. pose **q** 0, hand orientation **H 1** // Require: **R**<sup>7</sup> local<sup>_,_</sup><sup>**T**(EEorientationin7thjointframe)</sup> **2 R**<sup>0</sup> des<sup>_,_7</sup><sup>_←_</sup><sup>**H**[</sup><sup>**R**align]</sup><sup>_⊤_[</sup><sup>**R**7</sup> local<sup>_,_</sup><sup>**T**]</sup><sup>_⊤_//Desiredorientationof7th</sup> joint 

- **3** // Align **h** 7 with human hand using Subproblem 2 ( _q_ 5 _, q_ 6) _←_ AlignAxis(7 _,_ **q** _,_ **R**<sup>0</sup> des<sup>_,_7[:</sup><sup>_,_1])</sup> 

- **4** // Put **h** 6 and desired direction in 7th joint frame **u**<sup>7</sup> 6<sup>_←_</sup><sup>**R**7</sup><sup>_,_0</sup><sup>**R**0</sup><sup>_,_6(</sup><sup>**q**0)</sup><sup>**h**6</sup> **h**<sup>7</sup> 6<sup>_←_[</sup><sup>**R**6</sup> local<sup>_,_7]</sup><sup>_⊤_</sup><sup>**h**6</sup> 

- **5** // Get _q_ 7 using Subproblem 1 and enforce joint limits _q_ 7 _←_ BoundJoints(SP1( **h**<sup>7</sup> 6<sup>_,_</sup><sup>**u**7</sup> 6<sup>_,−_</sup><sup>**h**7))</sup> 

- **Return:** Final joint angles <u>(</u> _q_ 5 _, q_ 6 _, q_ 7) 

future work), we find it is fast ( _∼_ 250 Hz) and reduces selfcollisions (see Sec. VI-C). 

**Remark 4.** _The key idea is that our fast closed-form solution leaves computation overhead for downstream processes such as safety filtering by serving as a drop-in, fast humanoid IK._ 

**Algorithm 4:** SEW Safety Filter for Self-Collisions **q** safe _←_ SEW-SafetyFilter( **q** 0 _,_ **q** des) 

**Input:** Current pose **q** 0, desired pose **q** des 

- **1** _K_ rb _←_ FK( **q** des) // get keypoints of desired pose 

- **2** _C ←_ MakeCapsules( _K_ rb) // init. collision volumes 

- **3** // Init. XPBD Lagrange multipliers 

- _{λi, j} ←_ 0 // one per ( _i, j_ )th collision pair in _C × C_ 

- **4 for** _k_ = 1 _, ··· , n_ iter _// # of iterations_ **do 5** // Nudge capsules w/ Algorithm 10 in Sec. E ( _C , {λi, j}_ ) _←_ XPBD-Iter( _C , {λi, j}_ ) 

- **6 if** _capsules in C are collision-free_ **then 7** // Recover SEW keypoints from capsules ( **s** lf _,_ **e** lf _,_ **w** lf _,_ **t** lf _,_ **s** rt _,_ **e** rt _,_ **w** rt _,_ **t** rt) _←_ GetKPs( _C_ ) 

- **8** // Recover tool orientations **H** lf _←_ RecoverTool( **T** lf( **q** 0) _,_ **t** lf) **H** rt _←_ RecoverTool( **T** rt( **q** 0) _,_ **t** rt) 

- **9** // Recover left and right arm configurations **q** lf _←_ SEW-Mimic( **s** lf _,_ **e** lf _,_ **w** lf _,_ **H** lf) **q** rt _←_ SEW-Mimic( **s** rt _,_ **e** rt _,_ **w** rt _,_ **H** rt) 

- **Return:** Safe pose **q** safe _←_ ( **q** lf _,_ **q** rt) 

**Return:** Original <u>pose</u> **q** 0 if no safe <u>pose</u> found 

Next, we summarize the method, then detail specific parts. 

_Algorithm Overview:_ The safety filter is summarized in Algorithm 4. Given an initial bimanual pose and a potentiallyunsafe desired pose, we first generate capsules from the robot’s SEW keypoints in that configuration (Algorithm 4). We then adjust the keypoints to safety by applying extended position-based dynamics (XPBD) [23] (Algorithm 4). Finally, we use SEW-Mimic to map the adjusted keypoints back to the robot’s joint angles (Algorithm 4–Algorithm 4), where RecoverTool (Algorithm 12 in Sec. E) obtains the desired robot end-effector orientation. In this context, SEW-Mimic functions as a fast IK solver. We provide more details for each of these steps below. 

_Bimanual Notation:_ We consider a left/right arm pair with pose **q** = ( **q** lf _,_ **q** rt) where **q** lf is the left arm pose and **q** rt right; we redefine **q** here to simplify exposition. We define a tuple of _robot keypoints_ : _K_ rb = ( **s** lf _,_ **e** lf _,_ **w** lf _,_ **t** lf _,_ **s** rt _,_ **e** rt _,_ **w** rt _,_ **t** rt) _←_ FK( **q** ), where FK denotes standard rigid body forward kinematics, **s** lf _∈_ R<sup>3</sup> denotes robot left shoulder location (typically the 1st joint actuator location), and similarly **e** lf for left elbow (4th joint actuator location), **w** lf for left wrist (6th joint actuator location), **t** lf for left tool tip, and **T** lf for left tool orientation; right side quantities are labeled “rt.” 

_Capsule Collision Volumes:_ We construct capsules (i.e., spheres swept along line segments) overapproximating the robot’s links for collision checking, as shown in Fig. 4. A capsule _C_ from **p** 1 to **p** 2 with radius _r_ is 


Thus, we overapproximate the robot’s left upper arm with _U_ lf _←_ Capsule( **s** lf _,_ **e** lf _, r_ upper) where _r_ upper is chosen large 

enough. We similarly construct a capsule _L_ lf to contain the lower arm and a capsule _H_ lf to contain the robot wrist and end effector, and repeat for the right side. We also create a capsule _T_ for the robot’s torso. To simplify notation, we gather the capsules into a set of collision volumes: 

_C ←_ MakeCapsules( _K_ rb) = _{T,U_ lf _,U_ rt _, L_ lf _, L_ rt _, H_ lf _, H_ rt _}._ 

A concrete example of MakeCapsules is in Sec. I. 

_XPBD Iteration:_ The filter uses XPBD [23] to push capsules out of collision and keypoints into obeying kinematic constraints, which we detail in Algorithm 10 in Sec. E and summarieze here. Our XPBD implementation defines a Lagrange multiplier _λi, j_ per collision volume pair, computes a collision gradient by accumulating over contact normals of each collision volumes pair, then uses _λi, j_ with user-specified weights of each volume to move each keypoint. Finally, we enforce kinematic constraints by projecting each link back to original length (see Algorithm 11 in Sec. E). 

_Continuous Time Collision Checking:_ In practice, if the initial and desired pose are far apart, then the safety filter can find a safe pose that requires one robot limb to “jump” through another, which is unsafe. We compensate for this by preprocessing the collision volumes (i.e., modifying Algorithm 4) to find the first collision between the initial and desired poses, as detailed in Sec. E2. 

VI. EXPERIMENTS 

We now evaluate SEW-Mimic experimentally to answer the following questions: 


Fig. 4: Our safety filter uses capsules (right) to compute and avoid self collision, as shown on Rainbow RBY1 hardware. 

- (Sec. VI-A) How does our method compare against other retargeting approaches in terms of speed and accuracy? 

- (Sec. VI-B) How does our method compare in ease-of-use for teleoperation? 

- (Sec. VI-C) How effective is our safety filter? 

- (Sec. VI-D) Is our SEW representation useful for training generative robot motion policies? 

- (Sec. VI-E) Is our SEW representation useful for fullbody humanoid retargeting? 

## _A. Retargeting Performance_ 

We investigate if SEW-Mimic has lower orientation error (as defined in Problem 2), absolute joint position (L2) error, and computation speed than baselines [1] [34]. 

_1) Experiment Design:_ We evaluate SEW-Mimic per Algorithm 1 and the baselines [1] [34] for retargeting both left and right arms of the Ubisoft LAFAN1 [14] dataset, processed to solely contain upper body motion. 

_2) Results and Discussion:_ The results are summarized in Fig. 5. A Kruskal-Wallis test was conducted to evaluate the effect of retargeting solver on alignment error and inference time. We see a statistically significant effect of solver on both alignment error ( _H_ = 215864 _._ 09, _p <_ 0 _._ 001) and inference time ( _H_ = 277254 _._ 30, _p <_ 0 _._ 001). Dunn’s post-hoc comparisons with Bonferroni correction confirm that SEW-Mimic achieves significantly lower alignment error (Median = 1 _._ 57 _×_ 10<sup>_−_13</sup> , IQR = [1 _._ 06 _×_ 10<sup>_−_13</sup> _,_ 1 _._ 66 _×_ 10<sup>_−_5</sup> ]) and inference time (Median = 0 _._ 587 ms, IQR = [0 _._ 573 _,_ 0 _._ 612] ms) than both GMR [1] and xr_teleoperate [34] ( _p <_ 0 _._ 001 for all pairwise comparisons). Altogether, as expected given its closed-form and optimality, SEW-Mimic achieves greater accuracy and faster inference than the baselines, with alignment errors comparable to floating-point numerical precision and 2-3 orders of magnitude lower inference time. Note, SEW-Mimic does not beat GMR on its own custom retargeting objective, as expected (see Sec. G); the point of this result is to confirm our optimality proof. 

## _B. Pilot User Study_ 

We investigate if SEW-Mimic enables users to complete bimanual manipulation tasks more successfully than endeffector control with MINK-IK [43]. 

_1) Experiment Design:_ We arrange a 2 _×_ 3 factorial design repeated measures (within subjects) user study ( _N_ = 8) with the teleoperation solver and specific manipulation tasks as independent variables. Per user and task, we measure total attempts, successes, and failures. Users teleoperate a Dual 


Fig. 5: Retargeting alignment error and inference time of SEW-Mimic vs. baselines. 

Kinova Gen3 robot in Robosuite [46] using SEW-Mimic and MINK-IK on three tasks (see Sec. H, Fig. 10): 

- _Cabinet_ : Move a box from a table into a raised cabinet. 

- _Glass Gap_ : Pick a box from between two rows of wine glasses and place it to the right (Fig. 6). 

_• Handover_ : Move a box from start to goal, where the start and goal are far apart, necessitating a bimanual handover. The order of tasks and teleoperation methods is randomized per user. Users wear a Meta Quest3 VR headset to which we stream binocular vision. Users are given 5 minutes per task and controller, and are instructed to achieve as many successes as possible in the allotted time. Further details are in Sec. H. 

_2) Results and Discussion:_ An Aligned Rank Transform (ART) ANOVA was conducted to evaluate the effect of task type and teleoperation solver on total attempts, total successes, and total failures. We see statistically significant interaction between teleoperation methods SEW-Mimic and MINK-IK across number of successes ( _p <_ 0 _._ 01), and number of failures ( _p <_ 0 _._ 01). Additionally, task had a significant effect ( _p <_ 0 _._ 05) across all comparisons. That said, post-hoc simple main effects analysis did not indicate statistically significant interaction when comparing the same task across different controllers for any dependent variable. Note our raw data are presented in Table I in the appendix. 

The statistically significant interaction between methods across all dependent variables suggests that SEW-Mimic has an effect on user performance. The significant effect of task on all dependent variables indicates our tasks are all different, supporting our evaluation procedure. A considerable limitation was the small sample size, which we suspect is why there is no significant effect of method on any one task, only in aggregate across all tasks; further study is needed on how SEW-Mimic affects user performance. Qualitatively, we noticed an interesting failure mode for MINK-IK: given the fixed scaling factor between user and robot end effector displacement, users with shorter arms were unable to reach the box and thus could not succeed. Finally, the raw data are promising in an informal sense that warrants further investigation: SEW-Mimic has 125 total successes summed across all tasks and users, versus 68 for MINK-IK. 


Fig. 6: The Glass Gap task requires moving a red box from between wine glasses to a large green goal on the left. We show an example pose from our user study showing SEW-Mimic on the left vs. MINK-IK on the right, which shows how a lack of explicit elbow control can cause task failure from unexpected joint self-motion. 

## _C. Safety Filter Ablation Study_ 

We now investigate how our safety filter influences operation of SEW-Mimic near self-collisions. 

_1) Experiment Design:_ To create near self-collision poses, we record a continuous “rolling punch” motion of both human arms completing 10 full rotations in 10 seconds in front of the chest (Fig. 4). We use SEW-Mimic to retarget this motion to the RB-Y1 robot and measure the alignment error, number of self collisions, and computation speed with and without the proposed safety filter. Further details in Sec. I. 

_2) Results and Discussion:_ See Fig. 11 in Sec. I SEW-Mimic without safety filter has zero alignment error, about 0.8 ms (1250 Hz) computation time for both arms, and self-collision in nearly half of the retargeted poses. With the safety filter, we have on average higher alignment error of 0.019, longer computation time of about 4.0 ms (250 Hz), but much lower self-collision instances in only around 1.3% of the retargeted poses. Thus we conclude that our safety filter can reduce self-collision instances with some compromise in pose similarity and computation speed. This tradeoff between accuracy and safety can be adjusted by each link’s capsule size; we leave finding optimal tradeoffs to future work. 

## _D. Policy Learning_ 

We now explore if data collected with SEW-Mimic results in a policy that has higher success rate and lower task completion time than data collected with end-effector-only motion and MINK-IK [43]. 

_1) Experiment Design:_ To test the hypothesis, we collect two matched demonstration datasets on the Glass Gap task (Fig. 6): one using MINK-IK and one using SEW-Mimic. Each dataset contains 50 demonstrations. Across demonstrations, the box is initialized at random locations between the wine glasses. To control for demonstration quality, both datasets are collected by the same expert tele-operator. We then train Diffusion Policy [7, 32] separately on each dataset. For each dataset, we run 3 training seeds for 500 epochs and select 


Fig. 7: Kinematic-to-dynamic error, controller tracking error, and inference time when using SEW-Mimic and GMR in TWIST. 

the best-performing checkpoint for final evaluation. During evaluation, we sample 250 initial conditions and compute the task success rate, reporting results across the three seeds. 

_2) Results and Discussion:_ The policy trained on demonstrations collected by SEW-Mimic achieves a substantially higher success rate (approximately 3 _×_ ) than the policy trained on MINK-IK demonstrations, while achieving shorter task completion time (see Fig. 12 in the appendix). We suspect the performance gap is related to demonstration smoothness, which we investigate in Sec. J. In particular, SEW-Mimic data shows smoother joint angle trajectories and lower desired joint velocities (see Fig. 16). This is associated with lower action prediction error (see Fig. 15), despite shorter teleoperation horizons (see Fig. 14). Establishing whether these factors causally explain the gap requires further investigation and is deferred to future work. 

## _E. Full-Body Retargeting_ 

Finally, we explore if SEW-Mimic improves a pretrained full-body humanoid retargeting policy’s computational efficiency without negatively impacting accuracy. 

_1) Experiment Design:_ We apply SEW-Mimic as a drop-in replacement for the GMR retargeter [1] in the TWIST full-body teleoperation framework [44] by treating each leg’s hip-kneeankle as shoulder-elbow-wrist. GMR generates a kinematic initial guess of joint angles, which TWIST converts into a dynamically feasible pose (passed to a PD controller for a Unitree G1 humanoid in MuJoCo). We do not retrain or finetune TWIST (which is trained on data generated by GMR). We measure three metrics for SEW-Mimic and GMR: inference time, kinematic-to-dynamic “kin2dyn” joint angle error between the input and output of TWIST, the PD controller joint angle tracking error. Further details are in Sec. K. 

_2) Results and Discussion:_ SEW-Mimic performs 1-3 orders of magnitude faster than GMR, with no increase in either kin2dyn error or tracking error, per Fig. 7. This is a remarkable result, because SEW-Mimic optimizes for a different metric than GMR, and is not designed for full-body retargeting, yet operates as a satisfactory drop-in accelerator for TWIST. 

## VII. DEMONSTRATIONS 

We demonstrate SEW-Mimic on a Rainbow Robotics RBY1 and Kinova Gen3 dual arm systems in the video supplement. Qualitatively, our method enables fast robot motion, avoids self-collision, and operates smoothly near singularities. Hardware setup details are explained in Sec. F. We test on 

motions such as snatching a wooden block, rolling punches (see Sec. VI-C), crossing arms, and reaching full extension. 

## VIII. CONCLUSION AND LIMITATIONS 

This paper presents SEW-Mimic, a closed-form geometric retargeting method for upper body humanoid robots. The method optimally maps human to robot pose with respect to limb orientations, and is used to implement a fast safety filter for self collisions. Experiments show that SEW-Mimic is much faster and more accurate than other retargeting baselines, has a significant effect on task success in a pilot user study, has potential for future policy learning, and improves full-body humanoid retargeting speed. 

_Limitations:_ As is, SEW-Mimic is kinematic and constrained to humanoid morphologies (inapplicable for standard mounting of tabletop manipulators). Our optimality proof ignores joint angle limits and self collisions; proof is potentially impossible if these factors are included. Our method’s accuracy also depends on human keypoint detection accuracy, so is susceptible to perception errors (though these may be mitigated by filtering and high computation speed). The proposed safety filter, while fast and effective in practice, also lacks a correctness proof; one solution could be incorporating recent provably-correct collision avoidance methods [37, 25, 40, 26]. Another major limitation (seen in demonstrations) is remaining latency due to wireless communication and tracking control. This may be mitigated by incorporating feedforward velocity, which puts more pressure on the safety filter to correct future unsafe poses, versus just current poses. Finally, a larger and more detailed user study is needed to elucidate how and why SEW-Mimic may increase teleoperation performance. 

## REFERENCES 

- [1] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [2] Milad Asgari, Ilian A Bonev, and Cl´ement Gosselin. Singularities of abb’s yumi 7-dof robot arm. _Mechanism and Machine Theory_ , 205:105884, 2025. 

- [3] Sivakumar Balasubramanian, Alejandro MelendezCalderon, Agnes Roby-Brami, and Etienne Burdet. On the analysis of movement smoothness. _Journal of neuroengineering and rehabilitation_ , 12(1):112, 2015. 

- [4] Qingwei Ben, Feiyu Jia, Jia Zeng, Junting Dong, Dahua Lin, and Jiangmiao Pang. Homie: Humanoid locomanipulation with isomorphic exoskeleton cockpit. _arXiv preprint arXiv:2502.13013_ , 2025. 

- [5] Justin Carpentier, Guilhem Saurel, Gabriele Buondonno, Joseph Mirabel, Florent Lamiraux, Olivier Stasse, and Nicolas Mansard. The pinocchio c++ library – a fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives. In _IEEE International Symposium on System Integrations (SII)_ , 2019. 

- [6] Xuxin Cheng, Jialong Li, Shiqi Yang, Ge Yang, and Xiaolong Wang. Open-TeleVision: Teleoperation with Immersive Active Visual Feedback, July 2024. URL http://arxiv.org/abs/2407.01512. arXiv:2407.01512 [cs]. 

- [7] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11):1684–1704, 2025. 

- [8] Runyu Ding, Yuzhe Qin, Jiyue Zhu, Chengzhe Jia, Shiqi Yang, Ruihan Yang, Xiaojuan Qi, and Xiaolong Wang. Bunny-VisionPro: Real-Time Bimanual Dexterous Teleoperation for Imitation Learning, July 2024. URL http://arxiv.org/abs/2407.03162. arXiv:2407.03162 [cs]. 

- [9] Alexander J Elias and John T Wen. Redundancy parameterization and inverse kinematics of 7-dof revolute manipulators. _Mechanism and Machine Theory_ , 204: 105824, 2024. 

- [10] Alexander J Elias and John T Wen. Ik-geo: Unified robot inverse kinematics using subproblem decomposition. _Mechanism and Machine Theory_ , 209:105971, 2025. 

- [11] Christer Ericson. _Real-time collision detection_ . Crc Press, 2004. 

- [12] Zipeng Fu, Tony Z. Zhao, and Chelsea Finn. Mobile aloha: Learning bimanual mobile manipulation with lowcost whole-body teleoperation. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [13] Richard Hartley, Jochen Trumpf, Yuchao Dai, and Hongdong Li. Rotation averaging. _International journal of computer vision_ , 103(3):267–305, 2013. 

- [14] F´elix G. Harvey, Mike Yurick, Derek Nowrouzezahrai, and Christopher Pal. Robust motion in-betweening. _ACM Transactions on Graphics (Proceedings of ACM SIGGRAPH)_ , 39(4), 2020. 

- [15] Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning Human-to-Humanoid Real-Time Whole-Body Teleoperation. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 8944–8951, Abu Dhabi, United Arab Emirates, October 2024. IEEE. ISBN 979-8-3503-7770-5. doi: 10.1109/ IROS58592.2024.10801984. URL https://ieeexplore.ieee. org/document/10801984/. 

- [16] Yasuhiro Ishiguro, Tasuku Makabe, Yuya Nagamatsu, Yuta Kojio, Kunio Kojima, Fumihito Sugai, Yohei Kakiuchi, Kei Okada, and Masayuki Inaba. Bilateral humanoid teleoperation system using whole-body exoskeleton cockpit tablis. _IEEE Robotics and Automation Letters_ , 5(4):6419–6426, 2020. 

- [17] Aadhithya Iyer, Zhuoran Peng, Yinlong Dai, Irmak Guzey, Siddhant Haldar, Soumith Chintala, and Lerrel Pinto. OPEN TEACH: A Versatile Teleoperation System for Robotic Manipulation, March 2024. URL http://arxiv.org/abs/2403.07870. arXiv:2403.07870 [cs]. 

- [18] Zhenyu Jiang, Yuqi Xie, Kevin Lin, Zhenjia Xu, 

Weikang Wan, Ajay Mandlekar, Linxi Fan, and Yuke Zhu. DexMimicGen: Automated Data Generation for Bimanual Dexterous Manipulation via Imitation Learning, March 2025. URL http://arxiv.org/abs/2410.24185. arXiv:2410.24185 [cs]. 

- [19] Oussama Khatib. A unified approach for motion and force control of robot manipulators: The operational space formulation. _IEEE Journal on Robotics and Automation_ , 3(1):43–53, 2003. 

- [20] Kenneth Kreutz-Delgado, Mark Long, and Homayoun Seraji. Kinematic analysis of 7-dof manipulators. _The International journal of robotics research_ , 11(5):469– 481, 1992. 

- [21] Yixuan Li, Yutang Lin, Jieming Cui, Tengyu Liu, Wei Liang, Yixin Zhu, and Siyuan Huang. Clone: Closed-loop whole-body humanoid teleoperation for long-horizon tasks. _arXiv preprint arXiv:2506.08931_ , 2025. 

- [22] Camillo Lugaresi, Jiuqiang Tang, Hadon Nash, Chris McClanahan, Esha Uboweja, Michael Hays, Fan Zhang, Chuo-Ling Chang, Ming Yong, Juhyun Lee, et al. Mediapipe: A framework for perceiving and processing reality. In _Third workshop on computer vision for AR/VR at IEEE computer vision and pattern recognition (CVPR)_ , volume 2019, 2019. 

- [23] Miles Macklin, Matthias M¨uller, and Nuttapong Chentanez. Xpbd: position-based simulation of compliant constrained dynamics. In _Proceedings of the 9th International Conference on Motion in Games_ , pages 49–54, 2016. 

- [24] Naureen Mahmood, Nima Ghorbani, Nikolaus F. Troje, Gerard Pons-Moll, and Michael J. Black. AMASS: Archive of Motion Capture as Surface Shapes, April 2019. URL http://arxiv.org/abs/1904.03278. arXiv:1904.03278 [cs]. 

- [25] Jonathan Michaux, Adam Li, Qingyi Chen, Che Chen, and Ram Vasudevan. Safe Planning for Articulated Robots Using Reachability-based Obstacle Avoidance With Spheres. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, July 2024. doi: 10.15607/ RSS.2024.XX.035. 

- [26] Jonathan Michaux, Patrick Holmes, Bohao Zhang, Che Chen, Baiyue Wang, Shrey Sahgal, Tiancheng Zhang, Sidhartha Dey, Shreyas Kousik, and Ram Vasudevan. Can’t touch this: Real-time, safe motion planning and control for manipulators under uncertainty. _IEEE Transactions on Robotics_ , 2025. 

- [27] Richard M Murray, Zexiang Li, and S Shankar Sastry. _A mathematical introduction to robotic manipulation_ . CRC press, 2017. 

- [28] Daniel Ostermeier, Jonathan K¨ulz, and Matthias Althoff. Automatic Geometric Decomposition for Analytical Inverse Kinematics. _IEEE Robotics and Automation Letters_ , 10(10):9964–9971, October 2025. ISSN 23773766. doi: 10.1109/LRA.2025.3597897. URL https: //ieeexplore.ieee.org/document/11122599. 

- [29] Bradley E. Paden. _Kinematics and Control of Robot_ 

_Manipulators_ . PhD thesis, EECS Department, University of California, Berkeley, 1 1986. URL http://www2.eecs. berkeley.edu/Pubs/TechRpts/1986/631.html. 

- [30] Bradley E. Paden. _Kinematics and Control of Robot Manipulators_ . PhD thesis, EECS Department, University of California, Berkeley, January 1986. URL http://www2. eecs.berkeley.edu/Pubs/TechRpts/1986/631.html. 

- [31] Donald Lee Pieper. _The kinematics of manipulators under computer control_ . Stanford University, 1969. 

- [32] Moritz Reuss, Maximilian Li, Xiaogang Jia, and Rudolf Lioutikov. Goal-Conditioned Imitation Learning using Score-based Diffusion Policies. In _Proceedings of Robotics: Science and Systems_ , Daegu, Republic of Korea, 7 2023. doi: 10.15607/RSS.2023.XIX.028. 

- [33] Moritz Reuss, Maximilian Li, Xiaogang Jia, and Rudolf Lioutikov. Goal conditioned imitation learning using score-based diffusion policies. In _Robotics: Science and Systems_ , 2023. 

- [34] Unitree Robotics. xr <u>teleoperate.</u> https://github.com/ unitreerobotics/xr <u>teleoperate,</u> 2024. 

- [35] Jaiyoung Ryu, William P Cooney III, Linda J Askew, Kai-Nan An, and Edmund YS Chao. Functional ranges of motion of the wrist joint. _The Journal of hand surgery_ , 16(3):409–419, 1991. 

- [36] Durgesh Haribhau Salunkhe, Sthithpragya Gupta, and Aude Billard. Cuspidal redundant robots: Classification of infinitely many iks of special classes of 7r robots. _IEEE Robotics and Automation Letters_ , 2025. 

- [37] Sven R Schepp, Jakob Thumm, Stefan B Liu, and Matthias Althoff. Sara: A tool for safe human-robot coexistence and collaboration through reachability analysis. In _2022 International Conference on Robotics and Automation (ICRA)_ , pages 4312–4317. IEEE, 2022. 

- [38] TRI LBM Team, Jose Barreiros, Andrew Beaulieu, Aditya Bhat, Rick Cory, Eric Cousineau, Hongkai Dai, Ching-Hsin Fang, Kunimatsu Hashimoto, Muhammad Zubair Irshad, Masha Itkina, Naveen Kuppuswamy, Kuan-Hui Lee, Katherine Liu, Dale McConachie, Ian McMahon, Haruki Nishimura, Calder Phillips-Grafflin, Charles Richter, Paarth Shah, Krishnan Srinivasan, Blake Wulfe, Chen Xu, Mengchao Zhang, Alex Alspach, Maya Angeles, Kushal Arora, Vitor Campagnolo Guizilini, Alejandro Castro, Dian Chen, Ting-Sheng Chu, Sam Creasey, Sean Curtis, Richard Denitto, Emma Dixon, Eric Dusel, Matthew Ferreira, Aimee Goncalves, Grant Gould, Damrong Guoy, Swati Gupta, Xuchen Han, Kyle Hatch, Brendan Hathaway, Allison Henry, Hillel Hochsztein, Phoebe Horgan, Shun Iwase, Donovon Jackson, Siddharth Karamcheti, Sedrick Keh, Joseph Masterjohn, Jean Mercat, Patrick Miller, Paul Mitiguy, Tony Nguyen, Jeremy Nimmer, Yuki Noguchi, Reko Ong, Aykut Onol, Owen Pfannenstiehl, Richard Poyner, Leticia Priebe Mendes Rocha, Gordon Richardson, Christopher Rodriguez, Derick Seale, Michael Sherman, Mariah Smith-Jones, David Tago, Pavel Tokmakov, Matthew Tran, Basile Van Hoorick, Igor Vasiljevic, Sergey Za- 

kharov, Mark Zolotas, Rares Ambrus, Kerri FetzerBorelli, Benjamin Burchfiel, Hadas Kress-Gazit, Siyuan Feng, Stacie Ford, and Russ Tedrake. A careful examination of large behavior models for multitask dexterous manipulation, 2025. URL https://arxiv.org/abs/2507.05331. 

- [39] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 5026–5033. IEEE, 2012. doi: 10.1109/IROS.2012.6386109. 

- [40] Shiqing Wei, Rooholla Khorrambakht, Prashanth Krishnamurthy, Vinicius Mariano Gonc¸alves, and Farshad Khorrami. Collision avoidance for convex primitives via differentiable optimization-based high-order control barrier functions. _IEEE Transactions on Control Systems Technology_ , 2025. 

- [41] Philipp Wu, Yide Shentu, Zhongke Yi, Xingyu Lin, and Pieter Abbeel. Gello: A general, low-cost, and intuitive teleoperation framework for robot manipulators. in 2024 ieee. In _RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 12156–12163, 2023. 

- [42] Shiqi Yang. Ace: A cross-platform visual-exoskeleton system for low-cost dexterous teleoperation. Master’s thesis, University of California, San Diego, 2025. 

- [43] Kevin Zakka. Mink: Python inverse kinematics based on MuJoCo, May 2025. URL https://github.com/ kevinzakka/mink. 

- [44] Yanjie Ze, Zixuan Chen, Jo˜ao Pedro Ara´ujo, Zi-ang Cao, Xue Bin Peng, Jiajun Wu, and C. Karen Liu. TWIST: Teleoperated Whole-Body Imitation System, May 2025. URL http://arxiv.org/abs/2505.02833. arXiv:2505.02833 [cs]. 

- [45] Rui Zhong, Chuang Cheng, Junpeng Xu, Yantong Wei, Ce Guo, Daoxun Zhang, Wei Dai, and Huimin Lu. Nuexo: A wearable exoskeleton covering all upper limb rom for outdoor data collection and teleoperation of humanoid robots. _arXiv preprint arXiv:2503.10554_ , 2025. 

- [46] Yuke Zhu, Josiah Wong, Ajay Mandlekar, Roberto Mart´ın-Mart´ın, Abhishek Joshi, Soroush Nasiriany, and Yifeng Zhu. robosuite: A modular simulation framework and benchmark for robot learning. _arXiv preprint arXiv:2009.12293_ , 2020. 

## APPENDIX 

## _A. Canonical Geometric Subproblem Algorithms_ 

Here we present closed-form geometric methods (see Algorithms 5 to 7) to solve Subproblems 1, 2, and 4 following the method of [10]. First, we present Subproblem 4, which is a dependency of Algorithm 6 to solve Subproblem 2. The subproblems themselves are illustrated by example in Fig. 8. 


Fig. 8: Examples of Subproblems 1, 2, and 4. For Subproblems 2 and 4, the two solution cases are shown. Adapted from [10]. 

_Subproblem 4:_ Consider a vector **p** , a unit vector **k** defining a rotation axis, and a unit vector **h** defining a plane offset from the origin by a distance _d_ . Rotate **p** about **k** by an angle _θ_ such that the vector _R_ ( **k** _, θ_ ) **p** is either on, or as close as possible to, the plane: 


which returns either 1 or 2 optimizers depending on whether or not **p** can be rotated to touch the plane. We solve Subproblem 4 in closed form using Algorithm 7 (in Sec. A). 

- **Algorithm 5:** Subproblem 1 _θ_<sup>_⋆_</sup> _←_ SP1( **p** 1 _,_ **p** 2 _,_ **k** ) Find an angle _θ_<sup>_⋆_</sup> that aligns **p** 1 with **p** 2 by rotating **p** 1 <u>about</u> **k Input: p** 1 _,_ **p** 2 _,_ **k** 

- **1** // Project vectors onto plane perpendicular to **k** and find rotation angle in that plane 

- **2 p** ˆ 1 _←_ unit( **p** 1 _−_ ( **p** 1 _·_ **k** ) **k** ) **3 p** ˆ 2 _←_ unit( **p** 2 _−_ ( **p** 2 _·_ **k** ) **k** ) **4** _θ_<sup>_⋆_</sup> _←_ 2 _·_ atan2( _∥_ **p** ˆ 1 _−_ **p** ˆ 2 _∥ , ∥_ **p** ˆ 1 + ˆ **p** 2 _∥_ ) **5 if k**<sup>_⊤_</sup> ( **ˆp** 1 _×_ **ˆp** 2) _<_ 0 **then 6** _θ_<sup>_⋆_</sup> _←−θ_<sup>_⋆_</sup> // Correct sign of rotation if needed **Return:** _<u>θ</u>_<sup>_⋆_</sup> 

## _B. Syncing Human and Robot Frames_ 

We propose a calibration-free procedure to map human and robot upper body and wrist keypoints into the robot’s 0th frame, which we treat as a shared reference frame; we call this the _body-centric frame_ . This is necessary because human keypoints are typically given in an arbitrary frame defined by an input streaming device (e.g., VR headset or external camera). 

## **Algorithm 6:** Subproblem 2 


Find a set of angles to rotate vector **p** 1 about axis **k** 1 and vector **p** 2 about axis **k** 2 to minimize the 2-norm <u>error between the</u> rotated <u>vectors</u> 

- **2 Input: p** 1 _,_ **p** 2 _,_ **k** 1 _,_ **k** 2 

- **4** // Normalize input vectors 

- **5 p** ˆ 1 _←_ unit( **p** 1) and **p** ˆ 2 _←_ unit( **p** 2) 

- **7** // Use Subproblem 4 for each angle; the first angle solution set is indexed by _i_ and the second by _j_ and each may have 1 or 2 solutions 

- **8** _{θ_ 1<sup>_⋆_</sup> _,_ 1<sup>_,θ ⋆_</sup> 1 _,_ 2<sup>_} ←_SP4(</sup><sup>**k**2</sup><sup>_,_ˆ</sup><sup>**p**1</sup><sup>_,_</sup><sup>**k**1</sup><sup>_,_</sup><sup>**k**</sup> 2<sup>_⊤_</sup><sup>**p**ˆ2)</sup> **9** _{θ_ 2<sup>_⋆_</sup> _,_ 1<sup>_,θ ⋆_</sup> 2 _,_ 2<sup>_} ←_SP4(</sup><sup>**k**1</sup><sup>_,_ˆ</sup><sup>**p**2</sup><sup>_,_</sup><sup>**k**2</sup><sup>_,_</sup><sup>**k**</sup> 1<sup>_⊤_</sup><sup>**p**ˆ1)</sup> 

- **11** // Return set of 1, 2 solutions **Return:** _{_ ( _θ_ 1<sup>_⋆_</sup> _,_ 1<sup>_,θ ⋆_</sup> 2 _,_ 2<sup>)</sup><sup>_,_(</sup><sup>_θ ⋆_</sup> 1 _,_ 2<sup>_,θ ⋆_</sup> 2 _,_ 1<sup>)</sup><sup>_}_</sup> 

_1) Creating the Body-Centric Frame:_ To put human upper body keypoints in the 0th frame, we create the transformations ( **R**<sup>0</sup><sup>_,_in</sup> _,_ **p**<sup>0</sup><sup>_,_in</sup> ), where “in” refers to the input streaming frame. Suppose we are given left and right shoulder keypoints **s**<sup>in</sup> lf<sup>_,_</sup><sup>**s**</sup> rt<sup>in</sup> as input keypoints. We define a lower body anchor point **p**<sup>in</sup> torso<sup>,</sup> typically a torso-fixed keypoint such as a vertebra position or the hip center, depending on the input streaming device. Then, we create the body-centric frame with Algorithm 8: 


Relative to the human torso, this treats the point between the shoulders as its origin, and front/left/up as the orthonormal frame direction order (i.e., “X/Y/Z”), as shown in Fig. 2. 

Humanoid robots typically come with a predefined upper body frame analogous to the human upper body frame, which we use as the 0th or baselink frame. However, if a robot uses a different convention, we must create the transformations ( **R**<sup>0</sup><sup>_,_rb</sup> _,_ **p**<sup>0</sup><sup>_,_rb</sup> ), where “rb” refers to the robot’s default frame. In this case, just as for the human, we define shoulder and torso keypoints ( **s**<sup>rb</sup> lf<sup>_,_</sup><sup>**s**</sup> rt<sup>rb</sup><sup>_,_</sup><sup>**p**rb)fortherobot,thenapplyAlgorithm8</sup> to redefine the 0th frame: 


Finally, we map all keypoints for the human and robot arms into the 0th frame per Eq. (2). 

_2) Creating Wrist Frames:_ Different input streaming methods often use different conventions for wrist or hand orientation, necessitating the following preprocessing steps to get the hand orientation **H**<sup>in</sup> . Typically, we receive a hand orientation **H**<sup>˜in</sup> in the input frame with an arbitrary convention, but our method assumes that the hand orientation follows the right-hand rule (index finger extended / palm normal / thumb extended for “X/Y/Z”). To correct this, we apply an appropriate rotation **R**<sup>in</sup> align<sup>to get</sup><sup>**H**in that obeys our assumption</sup> as **H**<sup>in</sup> _←_ **R**<sup>in</sup> align<sup>**H**˜in</sup> 

Often the hand orientation is not directly available as an input, but finger and wrist keypoints are. In this case, we 

## **Algorithm 7:** Subproblem 4 

_{θ j_<sup>_⋆} ←_SP4(</sup><sup>**p**</sup><sup>_,_</sup><sup>**h**</sup><sup>_,_</sup><sup>**k**</sup><sup>_,d_)</sup> 

Find a set of angles _{θ j_<sup>_⋆}_bywhichtorotatevector</sup><sup>**p**</sup> about axis **k** to minimize the distance of the rotated vector to a plane with normal **h** offset from the origin by distance _d_ 

**Input: p** _,_ **h** _,_ **k** _, d_ 

- **1** // Define plane parallel to the circle traced by rotating **p** about **k** , into which we project to find a solution; columns of **F** are a basis of this plane 

- **2 F** _←_ �sk( **k** ) **p** _, −_ sk( **k** )<sup>2</sup> **p** � 

- **3** // Set up linear system **Ax** = _b_ where **A** _∈_ R<sup>1</sup><sup>_×_2</sup> and **x** = [sin _θ ,_ cos _θ_ ]<sup>_⊤_</sup> to allow solving for _θ_ 

- **4 A** _←_ **h**<sup>_⊤_</sup> **F** and _b ← d −_ **h**<sup>_⊤_</sup> **kk**<sup>_⊤_</sup> **p** 

**Algorithm 8:** Make Frame from Keypoints ( **R** _,_ **p** ) _←_ MakeFrame( **k** lf _,_ **k** rt _,_ **k** b) 

// Given three non-collinear keypoints in R<sup>3</sup> , output a coordinate frame parameterized by a rotation matrix <u>and translation vector</u> 

**Input:** Left, right, and bottom keypoints **k** lf _,_ **k** rt _,_ **k** b 

**1** // Set translation vector between left/right keypoints **2 p** _←_ 2<sup><u>1</u>(</sup><sup>**k**lf +</sup><sup>**k**rt)</sup> 

**3** // Represent frame orientation as a rotation matrix 

- **4 u** y _←_ unit( **k** lf _−_ **k** rt) 

- **5 u** x _←_ unit( **u** y _×_ ( **p** _−_ **k** b)) 

- **6 u** z _←_ **u** x _×_ **u** y 

- **7 R** _←_ [ **u** x _,_ **u** y _,_ **u** y] 

**Return:** Rotation matrix **R** and translation vector **<u>p</u>** 

- **5 x** _←_ **A**<sup>†</sup> _b_ // Least-squares solution 

- **6** // If least squares solution is not on the circle, two unique angles can rotate **p** to contact the plane 

- **7 if** _∥_ **A** _∥_<sup>2</sup> 2<sup>_> b_2</sup><sup>**then**</sup> 

- **8** // Offset the least-squares solution **x** in the nullspace of **A** to get solutions on the circle 

- **9** _z ←_ ( _∥_ **A** _∥_<sup>2</sup> 2<sup>_−b_2)1</sup><sup>_/_2</sup> 

- **10 x** + and **x** – _←_ **x** _± z_ � **A** [2] _, −_ **A** [1]� **11** _θ_ +<sup>_⋆←_atan2(</sup><sup>**x**+[1]</sup><sup>_,_</sup><sup>**x**+[2])</sup> **12** _θ_ –<sup>_⋆←_atan2(</sup><sup>**x**–[1]</sup><sup>_,_</sup><sup>**x**–[2])</sup> **Return:** _{θ_ +<sup>_⋆,θ ⋆_</sup> –<sup>_}_</sup> 

- **13 else** 

- **14** // Least-squares solution is the only solution **15** _θ_<sup>_⋆_</sup> _←_ atan2( **x** [1] _,_ **x** [2]) **Return:** _{θ_<sup>_⋆_</sup> _}_ 

consider the index and little finger root keypoints **p**<sup>in</sup> index<sup>and</sup> **p**<sup>in</sup> pinky<sup>(typicallyattheintersectionbetweenthemetacarpal</sup> bone and the proximal phalanges bone), and wrist **w**<sup>in</sup> . Then we have 


Similar to the human, the robot’s end effector mount orientation may not follow our right-hand rule convention, which we denote **T**<sup>˜</sup> ( **q** ). In this case, we again apply an appropriate rotation to get **T** ( **q** ) _←_ **R**<sup>rb</sup> align<sup>**T**˜(</sup><sup>**q**).</sup> 

## _C. Perpendicular Wrist_ 

For some robots, such as the Rainbow RB-Y1 and Unitree G1, the end effector mounting orientation is perpendicular to the final joint axis (not parallel as we assume in Sec. III-B2 or Fig. 2). We adjust Algorithm 3 as follows to accommodate this wrist type. Instead of using Subproblems 1 and 2, perpendicular wrists can be solved with Euler angle decomposition. We take the following steps to derive an Euler angle order “A5 _/_ A6/A7” (e.g., “X/Y/Z” or “X/Y/X”) of the final three joints. First we represent the 7<sup>th</sup> frame orientation in the 

robot’s 5<sup>th</sup> joint frame with the current joint configuration **q** :: 


Next, we inspect the correspondence between the rotation axis ( **h** 5 _,_ **h** 6 _,_ **h** 7) and the current 5<sup>th</sup> joint frame axis: 


For each of the 5th-7th joints, the order of the body frame Euler rotation depends on **u** _i_ ’s value ( _i_ = 5 _,_ 6 _,_ 7): 


Then we use Euler decomposition to find the wrist angles ( _q_ 5 _, q_ 6 _, q_ 7) _←_ EulerDecomp( **R**<sup>5</sup> des<sup>_,_7</sup><sup>_,_“A5</sup><sup>_/_A6</sup><sup>_/_A7”)</sup> (19) 

Finally, we compute **T** ( **q** ) as in Sec. III-B2. 

**Remark 5.** _A limitation of this approach can arise when_ **h** 5 _and_ **h** 7 _become parallel, when q_ 6 = _±_ 90<sup>_◦_</sup> _(i.e., gimbal lock). However, we find that this rarely occurs during human to robot pose retargeting, because the active range of motion for a human wrist in the q_ 6 _is typically well below_ 90<sup>_◦_</sup> _[35]._ 

## _D. Optimality Proof_ 

We take advantage of the fact that each closed-form subproblem algorithm is optimal (Lemmata 6 to 8). Note, we work in reverse order from Subproblem 4 to 2 to 1, because the subproblems are ultimately used in this order in Algorithm 1. The final result is then below in Proposition 3. 

**Lemma 6** (Optimality of Solving Subproblem 4) **.** _Consider a vector_ **p** _, a unit vector_ **k** _defining a rotation axis, and a unit vector_ **h** _defining a plane offset from the origin by a distance d. Algorithm 7 finds an optimal solution θ_<sup>_⋆_</sup> _to_ min _θ_ �� **h** _⊤R_ ( **k** _, θ_ ) **p** _− d_ �� _._ 

_Proof:_ See [10, Appendix A, Subproblem 4] for a detailed proof by construction, which we summarize here. First, note that the rotation of **p** about **k** traces a circle in 3-D, which intersects the plane defined by **h** at either 0, 1, or 2 points. The algorithm constructs a basis **F** for the plane in which this circle is embedded. We then find the closest points on that circle to the line created by the intersection with the plane defined by **h** and _d_ , as a least-squares solution. To see this, first note that _R_ ( **k** _, θ_ ) = **kk**<sup>_⊤_</sup> +sin _θ_ sk( **k** ) _−_ cos _θ_ sk( **k** )<sup>2</sup> . Then **h**<sup>_⊤_</sup> _R_ ( **k** _, θ_ ) **p** = _d_ can be written as a linear equation: 


In the case of 0 or 1 intersection points, the solution is given by least squares: **x** = **A**<sup>†</sup> _b_ and _θ_<sup>_⋆_</sup> = atan2( **x** [1] _,_ **x** [2]). In the case of 2 intersection points, the plane intersects the circle traced by **p** about **k** , with radius ( _∥_ **A** _∥_<sup>2</sup> 2<sup>+</sup><sup>_b_2)1</sup><sup>_/_2.Theleast-</sup> squares solution **x** lies inside that circle. Thus, one can find solutions on the circle by moving orthogonal to **x** (i.e., in the nullspace of **A** ) by a distance _z_ = ( _∥_ **A** _∥_<sup>2</sup> 2<sup>_−b_2)1</sup><sup>_/_2,resultingin</sup> two optimizers _θ_ +<sup>_⋆_and</sup><sup>_θ_</sup> –<sup>_⋆_.</sup> 

**Lemma 7** (Optimality of Solving Subproblem 2) **.** _Consider two unit vectors_ **u** _,_ **v** _∈_ R<sup>3</sup> _and two rotation axes_ **k** 1 _,_ **k** 2 _∈_ R<sup>3</sup> _. Algorithm 6 finds optimal values of θ_ 1 _and θ_ 2 _that minimize µ_ c( _R_ ( **k** 1 _, θ_ 1) **u** _, R_ ( **k** 2 _, θ_ 2) **v** ) _, where µ_ c _is as in Eq._ (5) _._ 

_Proof:_ From [10, Appendix A, Subproblem 2], we have that Algorithm 6 returns _θ_ 1 and _θ_ 2 that minimize the quantity _∥R_ ( **k** 1 _, θ_ 1) **u** _− R_ ( **k** 2 _, θ_ 2) **v** _∥_ 2 exactly to 0; the key idea is to use two instances of Subproblem 4, then rely on Lemma 6. Then, to show that an optimizer of the 2-norm is also an optimizer of _µ_ c, notice that, for unit vectors **a** and **b** , if _∥_ **a** _−_ **b** _∥_ 2 = 0, then 1 _−_ **a** _·_ **b** = 0. 

**Lemma 8** (Optimality of Solving Subproblem 1) **.** _Consider two unit vectors_ **u** _and_ **v** _∈_ R<sup>3</sup> _, and a rotation axis_ **k** _∈_ R<sup>3</sup> _. Assume all three vectors are not collinear. Then, Algorithm 5 finds an optimal angle θ_<sup>_⋆_</sup> _that minimizes ∥R_ ( **k** _, θ_<sup>_⋆_</sup> ) **u** _−_ **v** _∥._ 

_Proof:_ See [10, Appendix A, Subproblem 1]. The key idea is to project **p** 1 and **p** 2 into the plane perpendicular to **k** , then apply basic planar trigonometry. 

Finally, we prove Proposition 3 (restated here). 

**Proposition 3.** _Consider a robot arm with consecutive perpendicular joint axes, baselink mounted in a humanoid configuration as shown in Fig. 2(b), and no joint angle limits or self-collisions. Suppose the robot is at an initial configuration_ **q** 0 _. Suppose we are given keypoints of the human shoulder_ **s** _, elbow_ **e** _, and wrist_ **w** _, and a hand orientation_ **H** _. Using Algorithm 1, compute_ **q** _←_ SEW-Mimic( **q** 0 _,_ **s** _,_ **e** _,_ **w** _,_ **H** ) _. Then_ **q** _is a global optimizer of Problem 2._ 

_Proof:_ We consider each cost term in Problem 2, which are all nonnegative. From Algorithm 1 (Algorithm 1) and Lemma 7 we have that _µ_ c( **u** _,_ **R**<sup>0</sup><sup>_,_3</sup> ( **q** ) **h** 3) = 0. Similarly, from Algorithm 1 (Algorithm 1) and Lemma 7 we 

have that _µ_ c( **l** _,_ **R**<sup>0</sup><sup>_,_5</sup> ( **q** ) **h** 5) = 0. It remains to show that ��( **T** ( **q** ) _⊤_ **H** )1 _/_ 2 _−_ **I** ��F<sup>= 0, which can be shown by demonstrat-</sup> ing that **T** ( **q** ) = **H** . Per Algorithm 3, the claim follows from Lemmata 7 and 8; the use of Subproblem 2 ensures that the first column of the tool and hand orientation matrices are equal ( **T** ( **q** )[: _,_ 1] = **H** [: _,_ 1]), then Subproblem 1 ensures that second and third columns are equal ( **T** ( **q** )[: _,_ 2 : 3] = **H** [: _,_ 2 : 3]). 

Note, in the case of a perpendicular wrist as in Sec. C we still have optimality (assume no gimbal lock per Remark 5), because **R**<sup>5</sup><sup>_,_7</sup> des<sup>isavalidrotationmatrixbyconstructionand</sup> Euler angle decomposition is exact. 

_E. Safety Filter Details_ 

_1) Collision Checking:_ For each relevant collision pair of capsules _Ci,C j_ , let 


where _d_ is the signed distance between the capsules (negative when the capsules are intersecting) and **n** _i_ is the contact normal on _Ci_ and similarly **n** _j_ . We compute _d_ per [11, §5.9.1]. We approximate the contact normals **n** _i_ as follows. First, note that standard implementations of capsule collision checking return the quantities ( **c** _i,_ **c** _j, τi, τ j_ ), where **c** _i_ is the closest point on the line segment defining _Ci_ to the line segment defining _C_ 2, and **c** 2 similarly and the values _τi_ and _τ_ 2 define where these points occur on their corresponding line segments. That is, if _Ci_ = _C_ ( **p** _i,_ 1 _,_ **p** _i,_ 2 _, ri_ ), then **c** _i_ = _τi_ **p** _i,_ 1 +(1 _− τi_ ) **p** _i,_ 2. Then we approximate the contact normal for _Ci_ **n** _i_ = _τi ·_ unit( **c** 2 _−_ **c** 1), and **n** _j_ similarly. 

_2) Continuous Time Approximation for Collision Check:_ As robots move in continuous time, collision checking must consider the full path between the current pose and the desired pose. For our safety filter, we propose a simple continuous collision check by linearly interpolating between the current keypoints and the desired keypoints using the function linspace, which takes start point, end point (inclusive), and number of interpolated points as the inputs. We summarize this process in Algorithm 9. We first determine the number of interpolated points _n_ interp _∈_ N by the distance between the keypoints and the radius of the capsules (Algorithm 9– Algorithm 9). The key idea is to update the desired pose with the first interpolated keypoints where collision occurs, such that colliding bodies do not “jump” over each other. We first interpolate between the robot’s current and desired SEW keypoints, and use them to represent links (Algorithm 9– Algorithm 9). We then identify the first instance of collision in the interpolation (Algorithm 9–Algorithm 9), and return the corresponding collision volumes. 

_3) XPBD Iteration:_ The XPBD iteration (Algorithm 4 of Algorithm 4) is detailed in Algorithm 10. The overall idea is to push the robot’s capsules out of collision. The algorithm operates by accumulating a gradient for each link’s pair of keypoints, computed using collision normals between each pair of possibly colliding links. Then, each keypoint is adjusted by its corresponding gradient, weighted by the Lagrange multiplier for that pair of links. Finally, since this procedure 

**Algorithm 9:** Continuous-Time Collision Check _C ←_ FindFirstCollision( **q** 0 _,_ **q** des) 

- **Algorithm 10:** ( _C , {λi, j}_ ) _←_ XPBD-Iter( _C , {λi, j}_ ) 

**Input:** Collision volumes _C_ , one multiplier _λi, j_ 

- // Given initial and desired configurations 

- **1** for each collision volume pair 

**Input:** Initial pose **q** 0 and desired pose **q** des 

   - **2** // Require: Safety margin _d_ min, activation distance _d_ act, release distance _d_ rel, per-joint weights _wk_ , per-link lengths _ℓk_ , compliance _α_ 

- **1** // Determine number of interpolation points by getting initial and final keypoints, finding max distance between corresponding keypoints, then dividing by capsule radius 

   - **3 for** _each collision pair_ ( _Ci,C j_ ) _∈ C × C_ **do** 

- capsule radius **4** // Denote _Ci_ as parameterized by ( **p** _i,_ 1 _,_ **p** _i,_ 2 _, ri_ ) and _K_ 0 _←_ FK( **q** 0) and _K_ des _←_ FK( **q** des) _C j_ similarly by ( **p** _j,_ 1 _,_ **p** _j,_ 2 _, r j_ ) 

- **2** // Let **r** be a vector of capsule radii corresponding to **5** // Get signed distances and contact normals the keypoints, and of appropriate size, then compute: **6** ( _d,_ **n** _i,_ **n** _k_ ) _←_ CollisionCheck( _Ci,C j_ ) **n** = _∥K_ 0 _− K_ des _∥ /_ **r** // operations are elementwise **7** // Check if in collision or hysteresis 

- **3** _n_ interp _←⌈_ max _i_ **n** [ _i_ ] _⌉_ **8 if** _d ≥ d_ rel _OR (d ≥ d_ act _AND λi, j_ = 0 _)_ **then 45** // _{K_ Interpolaterb _, i}ni_ =interp0 _←_ robotlinspacearm keypoints(FK( **q** 0)and _,_ FK(make **q** des) _,_ capsules _n_ interp + 1) **9** _λi, j ←_ 0 and **continue 6** _{Ci}ni_ =interp1 _←{_ MakeCapsules( _K_ rb _, i_ ) _}ni_ =interp1 **10** _c_ = _d − d_ min **11 if** _c <_ 0 **then** 

- **7** // Find the first collided interpolation **12 for** _k_ = _i, j_ **do** 

- **8 if** _∃ i ∈{_ 1 _, ··· , n_ interp _}_ s.t. _Ci is in collision_ **then 9** _i_<sup>_∗_</sup> = min **13 g** _k,_ 1 and **g** _k,_ 2 _←_ **0** 3 _×_ 1 // Init. gradients _i∈{_ 1 _,··· ,n_ interp _}_<sup>_{Ci_isincollision</sup><sup>_}_</sup> **14 if** _Ck is an upper arm_ **then** 

- **10 else 15** // Only accumulate elbow gradient **11** _i_<sup>_∗_</sup> = _n_ interp **16 g** _k,_ 2 _←_ **g** _k,_ 2 + **n** _k_ **12** _C ← Ci_<sup>_∗_</sup> **17 else if** _Ck is a lower arm or hand_ **then Return:** <u>Collision volumes</u> _<u>C</u>_ **18** // Accumulate both keypoint gradients **19 g** _k,_ 1 _←_ **g** _k,_ 1 +(1 _−∥_ **n** _k∥_ 2) **n** _k_ **20 g** _k,_ 2 _←_ **g** _k,_ 2 + **n** _k_ 

- may change the link lengths, we adjust the links back to their **21** // Update multipliers, keypoints, capsules original lengths (Algorithm 11); in this case, we again apply **22** _λ_ old _← λi, j_ 

- XPBD but per link. **23** ∆ _λ ←−_ ( _c_ + _αλ_ old) _/_ ( _α_ + ∑ _k wk ∥_ **g** _k∥_<sup>2</sup> 2<sup>)</sup> 

- _F. Hardware Setup Details_ **24** _λi, j ←_ max (0 _, λ_ old + ∆ _λ_ ) **25 p** _k,_ 1 _←_ **p** _k,_ 1 + _wk_ ( _λi, j − λ_ old) **g** _k,_ 1 

- _1) Kinova Gen3 Dual Arm:_ We use a custom-built dual **26 p** _k,_ 2 _←_ **p** _k,_ 2 + _wk_ ( _λi, j − λ_ old) **g** _k,_ 2 

- Kinova Gen3 7-DOF arm setup, controlled by a laptop workstation with 24 core Intel i9 CPU and NVIDIA RTX 4090 **27** _Ck ←_ Capsule( **p** _k,_ 1 _,_ **p** _k,_ 2 _, rk_ ) 

_1) Kinova Gen3 Dual Arm:_ We use a custom-built dual Kinova Gen3 7-DOF arm setup, controlled by a laptop workstation with 24 core Intel i9 CPU and NVIDIA RTX 4090 GPU. Each arm is equipped with a Psyonic Ability hand (6-DOF) as its end effector, each controlled by Teensy 4.0 microcontrollers and the Psyonic Ability API. The robot has a StereoLabs ZED X binocular camera as its head, mounted atop consisting of a 2-DOF neck (two Dynamixel XC330M288-T servos), interfaced with the rest of the robot through an NVIDIA Jetson Orin NX (also used for video streaming). The depth camera streams to a Meta Quest 3 VR headset. For a user to control the head, camera azimuth and elevation from the headset are sent as desired joint angles to the neck servos. 

**28** // Fix links if keypoint adjustment changed lengths **29** _λk ←_ 0 _∀ k_ = 1 _, ··· ,_ 7 // initialize per-link multipliers **30** _C ←_ XPBD-Iter-L( _C , {λk}_ ) // Algorithm 11 **Return:** Updated capsules _C_ and multipliers _{λi, j}_ 

## _G. Retargeting Performance Additional Details_ 

We run this experiment using MuJoCo simulator [39] on a desktop workstation with Intel(R) Core(TM) i9-13900K CPU, NVIDIA RTX 4090 GPU, and 128 GB RAM. 

_2) Rainbow Robotics RB-Y1:_ We used RB-Y1m v1.3 equipped with an omni-directional base and a pair of full spherical perpendicular wrist. The robot has a 2 DoF neck with a StereoLabs ZED 2 binocular camera. 

On the same dataset discussed in the main text, we compare SEW-Mimic and GMR on the metric from [1, Eq. (1)], as shown in Fig. 9. As expected, SEW-Mimic is significantly worse in this metric. 

In demo videos, we also used RB-Y1a v1.1 equipped with a differential drive base and a pair of spherical parallel wrist (similar to Kinova Gen3). A pair of 12 DoF X-Hand was used in demo videos and the hand was controlled using OpenTelevision [6]. 

## _H. User Study Additional Details_ 

We run this experiment using Robosuite [46] on a desktop workstation with Intel(R) Core(TM) i9-13900K CPU, 

## **Algorithm 11:** _C ←_ XPBD-Iter-L( _C ,_ _<u>{λk}</u>_ <u>)</u> 

**Input:** Collision volumes _C_ , one multiplier _λk_ per link 

- **1** // Require: Per-link lengths _lk_ , per-joint weights _wk_ , compliance _α_ 

- **2 for** _each collision volume Ck ∈ C and length lk_ **do** 

- **3** // Denote _Ck_ as parameterized by ( **a** _,_ **b** _, r_ ) 

- **4** // Compute current length and constraint violation 

- **5 d** _←_ **b** _−_ **a** ; _ℓ ←∥_ **d** _∥_ 2 

- **6 if** _ℓ< ε_ **then** 

- **7 continue** 

- **8** _c ← ℓ − lk_ 

- **9** // Compute gradients 

- **10 g** b _←_ **d** _/ℓ_ and **g** a _←−_ **g** b 

- **11** // Update multiplier, endpoints 

- **12** _λ_ old _← λk_ **13** ∆ _λ ←−_ ( _c_ + _αλ_ old) _/_ ( _α_ + _w_ a _∥_ **g** a _∥_<sup>2</sup> 2<sup>+</sup><sup>_w_b</sup><sup>_∥_</sup><sup>**g**b</sup><sup>_∥_2</sup> 2<sup>)</sup> **14** _λk ← λ_ old + ∆ _λ_ 

- **15** // Apply position corrections 

- **16 a** _←_ **a** + _w_ a∆ _λ_ **g** a; **b** _←_ **b** + _w_ b∆ _λ_ **g** b 

- **17** _Ck ←_ Capsule( **a** _,_ **b** _, r_ ) 

**Return:** Updated capsules _C_ 

## **Algorithm 12:** Recover Tool Orientation 

**H** _←_ RecoverTool( **T** _,_ **t** ) 

// Given a tool frame orientation matrix and a desired alignment vector for x-axis in R<sup>3</sup> , compute a new <u>desired tool</u> frame <u>orientation</u> matrix 

**Input:** Current tool orientation and desired alignment 

vector **T** _,_ **t** 

**1** // obtain the tool frame pointing direction as x-axis 

- **2 u** x _←_ **T** [: _,_ 1] 

**3 u** t _←_ unit( **t** ) 

**4** // find difference between x-axis and alignment vector 

- **5 k** _←_ **u** x _×_ **u** t **6** _θ ←_ arccos ( **u**<sup>_⊤_</sup> x<sup>**u**t)</sup> 


Fig. 9: Evaluation of SEW-Mimic and GMR according to the GMR’s optimization loss formulation [1, Eq. (1)]. 


Fig. 10: User experiment task environments. We provide three tasks for users to complete during the user study, as described in Sec. VI-B; each column shows one task from multiple views. Left: Cabinet. Middle: Glass Gap. Right: Handover. 

- **7 H** _← R_ ( **k** _, θ_ ) **T** 

**Return:** Desired <u>tool</u> frame <u>orientation</u> matrix **H** 

## NVIDIA RTX 4090 GPU, and 128 GB RAM. 

All tasks are visualized in Fig. 10. 

Before testing each control method, we allow the user five minutes to accustom themselves to the control method. Before each teleoperation task, we provide verbal instructions which informs users the goal of the task and obstacles to avoid. Each user is given five minutes to complete the task successfully in as many attempts as they are able to do. During user operation for each task attempt, we measure whether the goal was achieved successfully or not. Task attempts were marked as successful when the goal object (the red cube) entered the goal area (the translucent green cube). Attempts were 

alternatively marked as failures when the goal object reached an unrecoverable position, such as having fallen off the table, or when time for completion runs out during the trial. In the case of Glass Gap (Fig. 6), we add an additional case of marking the attempt as a failure when either stack of wine glasses are knocked over by the robot arm. 

## _I. Safety Filter Evaluation Additional Details_ 

We run this experiment using MuJoCo simulator on a laptop workstation with Intel(R) Core(TM) i9-13950HK CPU, NVIDIA RTX 4090 GPU, and 64 GB of RAM. Note that the GPU is not needed for SEW-Mimic or to run this experiment. 

When creating capsules around the RB-Y1 robot upper body, we used the following capsule radius: torso - 0.15 m, shoulder - 0.12 m, upper arm - 0.06 m, lower arm - 0.065 m, 

TABLE I: User study data (bold values are best per task/controller). 

|||**Cab**|**inet**|||**Glass**|**Gap**|||**Han**|**dover**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**User**|**SEW**||**MIN**|**K**|**SEW**||**MIN**|**K**|**SEW**||**MIN**|**K**|
||**Success**|**Fail**|**Success**|**Fail**|**Success**|**Fail**|**Success**|**Fail**|**Success**|**Fail**|**Success**|**Fail**|
|**1**|2|2|1|2|2|11|0|15|3|3|0|7|
|**2**|6|1|4|0|6|7|3|6|6|4|8|0|
|**3**|10|0|8|0|5|5|0|17|4|2|9|0|
|**4**|3|1|1|2|1|7|0|11|6|0|0|2|
|**5**|8|0|6|0|3|3|0|9|5|0|3|0|
|**6**|7|0|3|0|1|5|1|5|3|1|0|4|
|**7**|8|0|8|0|6|2|2|9|7|1|4|0|
|**8**|10|0|6|0|5|1|0|16|8|2|1|4|
|**total:**|**54**|4|37|4|**29**|**41**|6|88|**42**|**13**|25|17|


Fig. 11: SEW-Mimic alignment error, collision instances, and computation time abolition study on whether safety filter is used in the pose-retargeting pipeline. 

We report results over three random seeds, evaluated on 250 randomly sampled initial states. To isolate the effect of action abstraction, we use the same number of demonstrations for both representations. 

## _K. Full-Body Retargeting Additional Details_ 

We run this experiment using MuJoCo simulator on a desktop workstation with Intel(R) Core(TM) i9-13900K CPU, NVIDIA RTX 4090 GPU and 128 GB RAM. 

We show in Fig. 13 that SEW-Mimic provides dynamically feasible retargeting joint goals for TWIST without any finetuning. 

wrist arm - 0.07 m. The length of each capsules are determined using their corresponding keypoints defined on the robot link. 

## _J. Policy Learning Additional Details_ 


Fig. 12: We train the same imitation learning policy on _Glass Gap_ demonstrations collected using SEW-Mimic or MINK-IK. SEW-Mimic yields higher success rate and lower task completion time. Bars show mean across training seeds; error bars indicate variability across seeds. 

We run this experiment using MuJoCo simulator [39] on a desktop workstation with Intel(R) Core(TM) i9-13900K CPU, NVIDIA RTX 4090 GPU, and 128 GB RAM. 

For each representation, we trained for 600 epochs and selected the checkpoint with the best evaluation performance. 


Fig. 13: Inferencing LAFAN1 jumps1 <u>subject1</u> (06 : 42 _−_ 06 : 55) action on the SEW-TWIST pipeline for full body retargeting with dynamics. 

## _L. Policy Learning Additional Experiment_ 

We run this experiment using MuJoCo simulator on a desktop workstation with Intel(R) Core(TM) i9-13900K CPU, NVIDIA RTX 4090 GPU. 

_1) Hypothesis:_ We hypothesize that using absolute SEW pose as an action abstraction improve sample efficiency and higher performance of trained policy. 

_2) Experiment Design:_ We process the DexMimicGen dataset [18] for the Fourier GR1 humanoid to extract SEW keypoints for the Pouring and Coffee tasks. We then train a diffusion policy [7, 33] _πθ_ ( **a** _t |_ **o** _t_ ) where the action **a** _t_ is the absolute SEW pose, and **o** _t_ is the observation (RGB-D / proprioception). We compare against the same policy trained on the same dataset with widely used action abstraction: desired end-effector poses with the default Mink representation 

[18], and desired joint angles. We measure task success and task completion time. 

_3) Results and Discussion:_ Task success rate is shown in Fig. 17. We see that the SEW representation performs similarly to data collected with MINK-IK on the Coffee task, but worse on the Pouring task; our preliminary investigation has not yet revealed the cause of this issue. That said, the key takeaway we have is that the SEW representation warrants further investigation as an action representation. 


Fig. 14: **Demo collection time.** Time required to collect a single demonstration with MINK-IK and SEW-Mimic. The left panel shows the per-demonstration distribution (boxplot with individual trials); the right panel shows the mean with error bars indicating variability across demonstrations. 


Fig. 15: **Action prediction error.** We compare action prediction error for imitation policies trained on demonstrations collected with MINK-IK and SEW-Mimic. From the expert dataset, we randomly sample observation–action-chunk pairs, predict the corresponding action chunk with the trained policy, and compute the mean squared error (MSE) between the predicted and ground-truth action chunks (reported as L2 error in the plot). For each group, we evaluate the best-performing checkpoint. We report errors separately for the left and right desired joint position components. 


(a) Per-joint commanded joint velocity magnitude for the left (L) and right (R) arms. 


(b) Per-joint trajectory smoothness measured by SPARC [3] for the left (L) and right (R) arms. 

Fig. 16: **Demonstration quality comparison.** We report (a) the magnitude of commanded joint velocity and (b) actiontrajectory smoothness measured by SPARC [3], for both the left (L) and right (R) arms. Bars show the mean across demonstrations. Overall, SEW-Mimic produces lower commanded joint velocities and smoother trajectories (higher SPARC). 


Fig. 17: **Action abstraction ablation.** Success rate of Diffusion Policy [7] trained with three action representations—desired joint angles (Joint), end-effector pose commands via MINK-IK (Mink), and desired SEW (Sew)—on DexmimicGen tasks (Pouring, Coffee). Bars report mean performance across training seeds; error bars indicate variability across seeds. 


Fig. 18: **DexMimicGen tasks.** We evaluate on two bimanual manipulation tasks: (a) Pouring—transfer the ball from the yellow cup into the bowl, then place the bowl onto the green plate; (b) Coffee—grasp the coffee capsule, insert it into the coffee machine, and close the lid. 


Fig. 19: **Coffee task rollout with SEW actions.** We show four snapshots from a rollout of the Coffee task executed by a policy trained with the SEW action representation. Snapshots progress from the initial state (left) to task completion (right). Colored markers overlay the predicted SEW action poses at each timestep. 

